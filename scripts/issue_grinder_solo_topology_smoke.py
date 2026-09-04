#!/usr/bin/env python3
"""Run a fresh synthetic Solo execution-topology smoke.

The smoke gives an installed Issue Grinder session a local packet containing
analysis, implementation, verification and self-review.  No publication or
external semantic provider is needed, so any child/task dispatch observed in
the root trace is unambiguously Issue Grinder execution delegation and fails
the case.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any, Iterable


SCHEMA = "issue-grinder/solo-topology-smoke/v1"
EXPECTED_RESULT = {
    "ordered_unique": [2, 3, 5, 8],
    "source_count": 5,
    "total": 21,
}
MODE_FILE_RE = re.compile(
    r"(?:^|[\s\"'])(?:[^\s\"']*/)?references/modes/"
    r"(solo|classic|economical)\.md"
)
BROAD_MODE_DIR_RE = re.compile(
    r"(?:^|[\s\"'])(?:[^\s\"']*/)?references/modes"
    r"(?:/\*|/\{|/?(?=$|[\s\"']))"
)
DELEGATION_TOOLS = frozenset(
    {"spawn_agent", "create_thread", "fork_thread"}
)


@dataclass(frozen=True)
class SoloTopologyObservation:
    schema: str
    thread_id: str | None
    trace_path: str | None
    skill_loaded: bool
    execution_modes_loaded: bool
    loaded_mode_files: tuple[str, ...]
    broad_mode_directory_accesses: tuple[str, ...]
    delegation_events: tuple[str, ...]
    result_payload: dict[str, Any] | None
    final_payload: dict[str, Any] | None
    usage: dict[str, Any] | None
    exit_code: int
    passed: bool
    defects: tuple[str, ...]


def build_prompt() -> str:
    return (
        "Используй $issue-grinder:issue-grinder. Это изолированный model-forward "
        "тест execution topology, а не настоящий Task Manager delivery. Явно "
        "выбери режим «Соло»: найди установленный runtime skill, полностью "
        "прочитай его SKILL.md, затем общий references/execution-modes.md и "
        "ровно один references/modes/solo.md; остальные mode-файлы и весь их "
        "каталог не читай. Не обращайся к Task Manager, не создавай Goal, не "
        "используй сеть и не меняй ничего вне текущего временного каталога. "
        "Publication unit здесь не требуется, поэтому не обращайся к external "
        "communication/provider interface. Выполни локальный packet как "
        "execution owner: прочитай и проанализируй input.json, создай result.json с ключами "
        "ordered_unique (отсортированные уникальные числа), source_count "
        "(исходное количество элементов) и total (сумма исходных элементов), "
        "запусти локальную детерминированную проверку result.json и проведи "
        "self-review результата. После успешной проверки верни одну строку JSON "
        "с ключами canonical_mode, result_file и verification."
    )


def parse_json_lines(output: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in output.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def _walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _command_strings(events: Iterable[dict[str, Any]]) -> tuple[str, ...]:
    commands: list[str] = []
    for event in events:
        for item in _walk(event):
            item_type = str(item.get("type", "")).casefold()
            if item_type not in {"command_execution", "commandexecution"}:
                continue
            command = item.get("command")
            if isinstance(command, list):
                commands.append(" ".join(str(part) for part in command))
            elif command is not None:
                commands.append(str(command))
    return tuple(commands)


def _agent_messages(events: Iterable[dict[str, Any]]) -> Iterable[str]:
    for event in events:
        for item in _walk(event):
            item_type = str(item.get("type", "")).casefold()
            if item_type not in {"agent_message", "agentmessage", "message"}:
                continue
            text = item.get("text")
            if isinstance(text, str):
                yield text
            content = item.get("content")
            if isinstance(content, list):
                for part in content:
                    if not isinstance(part, dict):
                        continue
                    candidate = part.get("text")
                    if isinstance(candidate, str):
                        yield candidate


def _last_json_message(events: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    messages = list(_agent_messages(events))
    for message in reversed(messages):
        try:
            candidate = json.loads(message)
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            return candidate
    return None


def _delegation_events(events: Iterable[dict[str, Any]]) -> tuple[str, ...]:
    observed: set[str] = set()
    for event in events:
        for item in _walk(event):
            name = item.get("name") or item.get("tool")
            if isinstance(name, str) and name in DELEGATION_TOOLS:
                item_type = str(item.get("type", "")).casefold()
                if "output" not in item_type:
                    observed.add(name)
            item_type = str(item.get("type", "")).casefold()
            if item_type in {"subagentactivity", "sub_agent_activity"}:
                observed.add("subagent_activity")
    return tuple(sorted(observed))


def _thread_id(events: Iterable[dict[str, Any]]) -> str | None:
    for event in events:
        if event.get("type") == "thread.started":
            value = event.get("thread_id")
            if isinstance(value, str):
                return value
    return None


def _usage(events: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    for event in reversed(list(events)):
        if event.get("type") == "turn.completed":
            value = event.get("usage")
            if isinstance(value, dict):
                return value
    return None


def _trace_candidates(thread_id: str, codex_home: Path) -> Iterable[Path]:
    session_root = codex_home / "sessions"
    now = datetime.now(timezone.utc)
    today = session_root / f"{now.year:04d}" / f"{now.month:02d}" / f"{now.day:02d}"
    if today.is_dir():
        yield from today.glob(f"*{thread_id}.jsonl")
    if session_root.is_dir():
        yield from session_root.glob(f"*/*/*/*{thread_id}.jsonl")


def load_root_trace(
    thread_id: str | None,
    *,
    codex_home: Path,
) -> tuple[Path | None, list[dict[str, Any]]]:
    if thread_id is None:
        return None, []
    candidates = list(dict.fromkeys(_trace_candidates(thread_id, codex_home)))
    if not candidates:
        return None, []
    path = max(candidates, key=lambda item: item.stat().st_mtime_ns)
    return path, parse_json_lines(path.read_text(encoding="utf-8"))


def observe_case(
    *,
    output: str,
    trace_events: list[dict[str, Any]],
    trace_path: Path | None,
    result_payload: dict[str, Any] | None,
    exit_code: int,
) -> SoloTopologyObservation:
    events = parse_json_lines(output)
    thread_id = _thread_id(events)
    commands = _command_strings((*events, *trace_events))
    loaded_mode_files = tuple(
        sorted(
            {
                f"{match.group(1)}.md"
                for command in commands
                for match in MODE_FILE_RE.finditer(command)
            }
        )
    )
    broad_accesses = tuple(
        command for command in commands if BROAD_MODE_DIR_RE.search(command)
    )
    delegation_events = _delegation_events((*events, *trace_events))
    final_payload = _last_json_message(events)
    skill_loaded = any("/skills/issue-grinder/SKILL.md" in cmd for cmd in commands)
    execution_modes_loaded = any(
        "/skills/issue-grinder/references/execution-modes.md" in cmd
        for cmd in commands
    )

    defects: list[str] = []
    if exit_code != 0:
        defects.append(f"codex_exit:{exit_code}")
    if trace_path is None:
        defects.append("missing_root_trace")
    if not skill_loaded:
        defects.append("skill_not_observed")
    if not execution_modes_loaded:
        defects.append("execution_modes_not_observed")
    if loaded_mode_files != ("solo.md",):
        defects.append(
            "mode_files_loaded:"
            + (",".join(loaded_mode_files) if loaded_mode_files else "none")
        )
    if broad_accesses:
        defects.append("broad_mode_directory_access")
    if delegation_events:
        defects.append("execution_delegation:" + ",".join(delegation_events))
    if result_payload != EXPECTED_RESULT:
        defects.append("wrong_result_payload")
    if final_payload is None:
        defects.append("missing_final_json")
    else:
        if final_payload.get("canonical_mode") != "solo":
            defects.append("wrong_reported_mode")
        if final_payload.get("result_file") != "result.json":
            defects.append("wrong_reported_result_file")
        if final_payload.get("verification") != "passed":
            defects.append("verification_not_passed")

    return SoloTopologyObservation(
        schema=SCHEMA,
        thread_id=thread_id,
        trace_path=str(trace_path) if trace_path is not None else None,
        skill_loaded=skill_loaded,
        execution_modes_loaded=execution_modes_loaded,
        loaded_mode_files=loaded_mode_files,
        broad_mode_directory_accesses=broad_accesses,
        delegation_events=delegation_events,
        result_payload=result_payload,
        final_payload=final_payload,
        usage=_usage(events),
        exit_code=exit_code,
        passed=not defects,
        defects=tuple(defects),
    )


def run_case(
    *,
    codex_bin: str,
    model: str,
    reasoning_effort: str,
    timeout_seconds: int,
    codex_home: Path,
) -> tuple[SoloTopologyObservation, str]:
    with tempfile.TemporaryDirectory(prefix="ig-solo-topology-") as temp_dir:
        workspace = Path(temp_dir)
        (workspace / "input.json").write_text(
            json.dumps([8, 3, 5, 3, 2]) + "\n",
            encoding="utf-8",
        )
        command = [
            codex_bin,
            "exec",
            "--json",
            "--skip-git-repo-check",
            "--sandbox",
            "workspace-write",
            "--model",
            model,
            "-c",
            f"model_reasoning_effort='{reasoning_effort}'",
            "-C",
            temp_dir,
            build_prompt(),
        ]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        events = parse_json_lines(completed.stdout)
        thread_id = _thread_id(events)
        trace_path, trace_events = load_root_trace(
            thread_id,
            codex_home=codex_home,
        )
        result_path = workspace / "result.json"
        result_payload: dict[str, Any] | None = None
        if result_path.is_file():
            try:
                value = json.loads(result_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                value = None
            if isinstance(value, dict):
                result_payload = value
        observation = observe_case(
            output=completed.stdout,
            trace_events=trace_events,
            trace_path=trace_path,
            result_payload=result_payload,
            exit_code=completed.returncode,
        )
    return observation, completed.stderr


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--reasoning-effort", default="low")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        observation, stderr = run_case(
            codex_bin=args.codex_bin,
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            timeout_seconds=args.timeout_seconds,
            codex_home=args.codex_home,
        )
    except subprocess.TimeoutExpired as error:
        print(
            json.dumps(
                {
                    "schema": SCHEMA,
                    "passed": False,
                    "defects": [f"timeout:{error.timeout}"],
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    payload = asdict(observation)
    payload["model"] = args.model
    payload["reasoning_effort"] = args.reasoning_effort
    if stderr.strip():
        payload["stderr_tail"] = stderr[-2000:]
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if observation.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
