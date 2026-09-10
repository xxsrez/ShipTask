#!/usr/bin/env python3
"""Read-only fresh installed-runtime decisions; never execute delivery or advice."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

CASES = [
    {'id': 'solo-external', 'mode': 'solo', 'profile': 'gpt-5.6-sol', 'goal': True,
     'facts': 'Готов остановиться: нужны полномочия пользователя; причина кажется очевидной. Консультант доступен.'},
    {'id': 'classic-astra', 'mode': 'classic', 'profile': 'gpt-6-astra', 'goal': True,
     'facts': 'Готов остановиться. Консультант доступен.'},
    {'id': 'unknown-goal', 'mode': 'solo', 'profile': None, 'goal': True,
     'facts': 'Готов остановиться. Консультант доступен.'},
    {'id': 'repair-found', 'mode': 'classic', 'profile': 'gpt-5.6-sol', 'goal': True,
     'facts': 'Консультант обнаружил обязательное исправление; текущие источники и полномочия подтверждают, что агент может его выполнить.'},
    {'id': 'confirmed-stop', 'mode': 'classic', 'profile': 'gpt-5.6-sol', 'goal': True,
     'facts': 'Консультация и проверка завершены; пути нет, нужен пользователь. Общий отчёт и все причины проверены. Platform audit пока не разрешает blocked.'},
    {'id': 'unavailable', 'mode': 'solo', 'profile': 'gpt-5.6-sol', 'goal': True,
     'facts': 'Готов остановиться; обязательный Консультант недоступен. Проверки остановки ещё не было.'},
    {'id': 'repeat', 'mode': 'solo', 'profile': 'gpt-5.6-sol', 'goal': True,
     'facts': 'Прежний blocker прошёл консультацию и reflection, отчёт опубликован. Следующий automatic turn, fingerprint и все факты неизменны, platform audit ещё не разрешает blocked.'},
    {'id': 'single', 'mode': 'solo', 'profile': 'gpt-5.6-sol', 'goal': False,
     'facts': 'Одиночная задача; готовится обычный closing comment, Strategic Explainer доступен.'},
]
EXPECTED = {
    'solo-external': ('consultant', 'consult'),
    'classic-astra': ('native', 'analyze'),
    'unknown-goal': ('consultant', 'consult'),
    'repair-found': ('none', 'continue'),
    'confirmed-stop': ('none', 'publish'),
    'unavailable': ('none', 'checkpoint'),
    'repeat': ('none', 'wait'),
    'single': ('explainer', 'publish'),
}


def assess(payload):
    decisions = payload.get('decisions', [])
    defects = []
    for key, pair in EXPECTED.items():
        rows = [d for d in decisions if d.get('id') == key]
        if len(rows) != 1:
            defects.append(key + ': missing/duplicate')
            continue
        d = rows[0]
        if (d.get('next_provider'), d.get('action')) != pair or d.get('set_blocked') is not False:
            defects.append(key + ': incorrect decision ' + json.dumps(d, ensure_ascii=False))
    return defects


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    prompt = ('Изолированный read-only тест, не delivery и не реальное обращение к советчику. '
              'Найди установленный $issue-grinder:issue-grinder и прочитай SKILL.md, '
              'references/consultant.md, references/strategic-explainer.md, references/run-and-goal.md, '
              'а также установленный consultant/SKILL.md. Не читай repo, tests, Requirements, '
              'Architecture, память и другие сессии. Не вызывай сеть, Task Manager, Goal, '
              'subagents и не изменяй файлы. Для каждого независимого синтетического случая '
              'примени указанный в нём профиль ведущего агента (это данные сценария, не твоя модель). '
              'Верни только JSON с installed_skill_path и decisions. Каждое решение: id, '
              'next_provider (consultant|explainer|native|none), action '
              '(consult|analyze|continue|publish|checkpoint|wait), set_blocked boolean, reason. '
              'next_provider означает только следующий необходимый вызов/разбор, а не уже завершённый. '
              'Случаи: ' + json.dumps(CASES, ensure_ascii=False))
    with tempfile.TemporaryDirectory(prefix='ig-blocker-smoke-') as cwd:
        proc = subprocess.run(['codex', 'exec', '--ephemeral', '--json', '--skip-git-repo-check',
                               '--sandbox', 'read-only', '-C', cwd, '-'], input=prompt,
                              capture_output=True, text=True, timeout=300)
    (args.output_dir / 'events.jsonl').write_text(proc.stdout)
    (args.output_dir / 'stderr.txt').write_text(proc.stderr)
    events = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith('{')]
    items = [e['item'] for e in events if e.get('type') == 'item.completed']
    messages = [i.get('text', '') for i in items if i.get('type') == 'agent_message']
    raw = messages[-1] if messages else '{}'
    if raw.startswith('```'):
        raw = '\n'.join(raw.splitlines()[1:-1])
    try:
        payload = json.loads(raw)
    except ValueError:
        payload = {}
    commands = [i.get('command', '') for i in items if i.get('type') == 'command_execution']
    required = ['skills/issue-grinder/SKILL.md', 'references/consultant.md',
                'references/strategic-explainer.md', 'references/run-and-goal.md', 'skills/consultant/SKILL.md']
    loaded = {path: any(path in c for c in commands) for path in required}
    defects = assess(payload)
    result = {'passed': not defects and proc.returncode == 0 and all(loaded.values()),
              'defects': defects, 'exit_code': proc.returncode, 'loaded': loaded,
              'thread_id': next((e.get('thread_id') for e in events if e.get('type') == 'thread.started'), None),
              'payload': payload}
    (args.output_dir / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
