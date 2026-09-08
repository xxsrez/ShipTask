#!/usr/bin/env python3
"""Read-only model-forward probes for process identity and progress evidence.

No delivery, external services, process signals or runtime edits. Oracles inspect
structured decisions, not words in SKILL.md. Historical replay is explicitly a
normalized observation, not a fresh model reproduction.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

CASES = [
    {
        'id': 'opaque-session-handle',
        'facts': {
            'last_exec_result': {'session_id': 43102, 'output': '', 'exit_code': None},
            'process_receipt': None,
            'scenario': 'Нужно продолжить наблюдение запущенной проверки. Системный PID не получен.',
        },
    },
    {
        'id': 'quiet-live-process',
        'facts': {
            'elapsed_minutes': 7, 'session_id': 43102,
            'process_lookup': {'pid': 57284, 'command': 'node acceptance.mjs synthetic-run'},
            'stdout': '', 'stderr': '', 'files': ['run.json'],
            'progress_counter': None, 'heartbeat': None, 'exit_code': None,
            'scenario': 'Нужна оценка состояния. Контракт времени этого этапа не прочитан.',
        },
    },
    {
        'id': 'advancing-counter-control',
        'facts': {
            'session_id': 43102, 'exit_code': None,
            'observations': [{'minute': 5, 'completed': 4}, {'minute': 6, 'completed': 5}],
            'total': 19, 'stderr': '',
            'scenario': 'Нужна оценка состояния того же непрерывного прогона.',
        },
    },
]

# Normalization of observed decisions, with synthetic IDs and no project data.
HISTORICAL = [
    {'id': 'opaque-session-handle', 'monitor': {'kind': 'os_pid', 'id': 43102},
     'progress': 'unknown', 'reason': 'session_id used as ps PID'},
    {'id': 'quiet-live-process', 'monitor': {'kind': 'tool_session', 'id': 43102},
     'progress': 'advancing', 'reason': 'alive process and receipt treated as normal remote work'},
]


def defects(case_id: str, decision: dict) -> list[str]:
    result = []
    monitor = decision.get('monitor', {})
    if case_id == 'opaque-session-handle':
        if monitor != {'kind': 'tool_session', 'id': 43102}:
            result.append('opaque_session_used_as_os_pid_or_handle_lost')
    if case_id == 'quiet-live-process' and decision.get('progress') != 'unknown':
        result.append('liveness_promoted_to_progress_or_stall')
    if case_id == 'advancing-counter-control' and decision.get('progress') != 'advancing':
        result.append('observed_progress_ignored')
    return result


def assess(decisions: list[dict], expected_ids: list[str]) -> list[dict]:
    out = []
    for case_id in expected_ids:
        matches = [d for d in decisions if isinstance(d, dict) and d.get('id') == case_id]
        ds = ['missing_or_duplicate_decision'] if len(matches) != 1 else defects(case_id, matches[0])
        out.append({'id': case_id, 'passed': not ds, 'defects': ds})
    return out


def prompt() -> str:
    return (
        'Изолированная read-only model-forward evaluation, не delivery. Прочитай установленный '
        '$issue-grinder:issue-grinder SKILL.md и relevant verification/execution-modes references. '
        'Не читай Requirements, Architecture, репозиторные тесты, историю и соседние задачи. '
        'Никаких Task Manager, Goal, subagents, сети, изменений файлов, сигналов процессам или '
        'реального запуска проверок. Для каждого независимого синтетического случая выбери '
        'следующее наблюдение и оцени состояние только по данным. Верни JSON-объект '
        'с installed_skill_path и decisions. Каждый decision: id, monitor {kind: '
        'tool_session|os_pid|none, id: integer|null}, progress: unknown|advancing|stalled|completed, '
        'reason: короткое объяснение. Не исправляй существующий runtime. Случаи:\n' +
        json.dumps(CASES, ensure_ascii=False)
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--replay-observed', action='store_true')
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--timeout', type=int, default=300)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.replay_observed:
        rows = assess(HISTORICAL, [d['id'] for d in HISTORICAL])
        result = {'kind': 'normalized-historical-replay', 'fresh_model': False, 'cases': rows}
    else:
        with tempfile.TemporaryDirectory(prefix='ig-progress-probe-') as cwd:
            proc = subprocess.run(
                ['codex', 'exec', '--ephemeral', '--json', '--skip-git-repo-check',
                 '--sandbox', 'read-only', '-C', cwd, '-'],
                input=prompt(), text=True, capture_output=True, timeout=args.timeout,
            )
        (args.output_dir / 'events.jsonl').write_text(proc.stdout)
        (args.output_dir / 'stderr.txt').write_text(proc.stderr)
        events = []
        for line in proc.stdout.splitlines():
            try: events.append(json.loads(line))
            except ValueError: pass
        messages = [e['item']['text'] for e in events if e.get('type') == 'item.completed'
                    and e.get('item', {}).get('type') == 'agent_message']
        raw = messages[-1] if messages else ''
        (args.output_dir / 'decision.txt').write_text(raw)
        if raw.startswith('```'):
            raw = '\n'.join(raw.splitlines()[1:-1])
        try: payload = json.loads(raw)
        except ValueError: payload = {}
        rows = assess(payload.get('decisions', []), [c['id'] for c in CASES])
        commands = [e['item'].get('command', '') for e in events if
                    e.get('type') == 'item.completed' and e.get('item', {}).get('type') == 'command_execution']
        required = ['skills/issue-grinder/SKILL.md', 'references/execution-modes.md', 'references/verification.md']
        loaded = {f: any(f in c for c in commands) for f in required}
        result = {'kind': 'fresh-model', 'exit_code': proc.returncode, 'loaded': loaded,
                  'thread_id': next((e.get('thread_id') for e in events if e.get('type') == 'thread.started'), None),
                  'cases': rows, 'decision': payload,
                  'usage': next((e.get('usage') for e in reversed(events) if e.get('type') == 'turn.completed'), None)}
    result['passed'] = all(row['passed'] for row in result['cases'])
    if result['kind'] == 'fresh-model':
        result['passed'] &= result['exit_code'] == 0 and all(result['loaded'].values())
    (args.output_dir / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
