#!/usr/bin/env python3
"""Run a fresh model-forward progressive-loading smoke for Issue Grinder modes.

The smoke starts an isolated read-only Codex session for every selected mode and
observes the files named by command-execution events.  A case passes only when
the agent reads the installed Issue Grinder entrypoint, the common mode
resolver, and exactly the one selected mode contract.  Reading another mode
contract or addressing the whole mode directory fails the case.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from typing import Any, Iterable


SCHEMA = "issue-grinder/mode-loading-smoke/v1"
MODE_FILES = {
    "solo": ("Соло", "solo.md"),
    "classic": ("Классический", "classic.md"),
    "balance": ("Баланс", "balance.md"),
    "swarm": ("Рой", "swarm.md"),
    "economical": ("Экономичный", "economical.md"),
}
MODE_FILE_RE = re.compile(
    r"(?:^|[\s\"'])(?:[^\s\"']*/)?references/modes/"
    r"(solo|classic|balance|swarm|economical)\.md"
)
BROAD_MODE_DIR_RE = re.compile(
    r"(?:^|[\s\"'])(?:[^\s\"']*/)?references/modes"
    r"(?:/\*|/\{|/?(?=$|[\s\"']))"
)


@dataclass(frozen=True)
class SmokeObservation:
    mode: str
    expected_mode_file: str
    thread_id: str | None
    command_count: int
    skill_loaded: bool
    execution_modes_loaded: bool
    loaded_mode_files: tuple[str, ...]
    broad_mode_directory_accesses: tuple[str, ...]
    final_payload: dict[str, Any] | None
    usage: dict[str, Any] | None
    exit_code: int
    passed: bool
    defects: tuple[str, ...]


def build_prompt(mode: str) -> str:
    russian_name, filename = MODE_FILES[mode]
    return (
        "Используй $issue-grinder:issue-grinder. Это изолированный model-forward "
        "тест прогрессивной загрузки, не delivery. Пройди только этап разрешения "
        f"явно выбранного режима «{russian_name}»: найди установленный runtime "
        "skill, полностью прочитай его SKILL.md, затем общий "
        "references/execution-modes.md, затем ровно один связанный mode contract "
        f"references/modes/{filename}. Не читай mode-help.md, Architecture, "
        "Requirements, остальные четыре mode-файла и не перечисляй каталог "
        "references/modes. Не обращайся к Task Manager, не создавай Goal или "
        "subagents, не меняй файлы. После чтения сразу остановись и верни одну "
        "строку JSON с ключами canonical_mode, loaded_mode_file, "
        "other_mode_files_loaded."
    )


def parse_json_events(output: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in output.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def _completed_items(events: Iterable[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for event in events:
        if event.get("type") != "item.completed":
            continue
        item = event.get("item")
        if isinstance(item, dict):
            yield item


def observe_case(
    mode: str,
    *,
    output: str,
    exit_code: int,
) -> SmokeObservation:
    events = parse_json_events(output)
    thread_id = next(
        (
            event.get("thread_id")
            for event in events
            if event.get("type") == "thread.started"
        ),
        None,
    )
    commands = [
        str(item.get("command", ""))
        for item in _completed_items(events)
        if item.get("type") == "command_execution"
    ]
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

    agent_messages = [
        str(item.get("text", ""))
        for item in _completed_items(events)
        if item.get("type") == "agent_message"
    ]
    final_payload: dict[str, Any] | None = None
    for message in reversed(agent_messages):
        try:
            candidate = json.loads(message)
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            final_payload = candidate
            break

    usage = next(
        (
            event.get("usage")
            for event in reversed(events)
            if event.get("type") == "turn.completed"
            and isinstance(event.get("usage"), dict)
        ),
        None,
    )
    expected_file = MODE_FILES[mode][1]
    defects: list[str] = []
    skill_loaded = any("/skills/issue-grinder/SKILL.md" in cmd for cmd in commands)
    execution_modes_loaded = any(
        "/skills/issue-grinder/references/execution-modes.md" in cmd
        for cmd in commands
    )
    if exit_code != 0:
        defects.append(f"codex_exit:{exit_code}")
    if not skill_loaded:
        defects.append("skill_not_observed")
    if not execution_modes_loaded:
        defects.append("execution_modes_not_observed")
    if loaded_mode_files != (expected_file,):
        defects.append(
            "mode_files_loaded:"
            + (",".join(loaded_mode_files) if loaded_mode_files else "none")
        )
    if broad_accesses:
        defects.append("broad_mode_directory_access")
    if final_payload is None:
        defects.append("missing_final_json")
    else:
        if final_payload.get("canonical_mode") != mode:
            defects.append("wrong_reported_mode")
        if final_payload.get("loaded_mode_file") != f"references/modes/{expected_file}":
            defects.append("wrong_reported_mode_file")
        if final_payload.get("other_mode_files_loaded") not in ([], False):
            defects.append("reported_other_mode_files")

    return SmokeObservation(
        mode=mode,
        expected_mode_file=expected_file,
        thread_id=thread_id if isinstance(thread_id, str) else None,
        command_count=len(commands),
        skill_loaded=skill_loaded,
        execution_modes_loaded=execution_modes_loaded,
        loaded_mode_files=loaded_mode_files,
        broad_mode_directory_accesses=broad_accesses,
        final_payload=final_payload,
        usage=usage,
        exit_code=exit_code,
        passed=not defects,
        defects=tuple(defects),
    )


def run_case(
    mode: str,
    *,
    codex_bin: str,
    model: str,
    reasoning_effort: str,
    timeout_seconds: int,
) -> tuple[SmokeObservation, str]:
    with tempfile.TemporaryDirectory(prefix=f"ig-mode-{mode}-") as temp_dir:
        command = [
            codex_bin,
            "exec",
            "--ephemeral",
            "--json",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--model",
            model,
            "-c",
            f"model_reasoning_effort='{reasoning_effort}'",
            "-C",
            temp_dir,
            build_prompt(mode),
        ]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    return (
        observe_case(mode, output=completed.stdout, exit_code=completed.returncode),
        completed.stderr,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        action="append",
        choices=tuple(MODE_FILES),
        help="Run one or more modes; the default is all five.",
    )
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--model", default="gpt-5.6-luna")
    parser.add_argument("--reasoning-effort", default="low")
    parser.add_argument("--timeout-seconds", type=int, default=120)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    modes = args.mode or list(MODE_FILES)
    cases: list[SmokeObservation] = []
    stderr_tails: dict[str, str] = {}
    for mode in modes:
        try:
            observation, stderr = run_case(
                mode,
                codex_bin=args.codex_bin,
                model=args.model,
                reasoning_effort=args.reasoning_effort,
                timeout_seconds=args.timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            observation = SmokeObservation(
                mode=mode,
                expected_mode_file=MODE_FILES[mode][1],
                thread_id=None,
                command_count=0,
                skill_loaded=False,
                execution_modes_loaded=False,
                loaded_mode_files=(),
                broad_mode_directory_accesses=(),
                final_payload=None,
                usage=None,
                exit_code=124,
                passed=False,
                defects=("timeout",),
            )
            stderr = ""
        cases.append(observation)
        if stderr and observation.exit_code != 0:
            stderr_tails[mode] = stderr[-2000:]

    receipt = {
        "schema": SCHEMA,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "passed": all(case.passed for case in cases),
        "cases": [asdict(case) for case in cases],
        "stderr_tails": stderr_tails,
    }
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
