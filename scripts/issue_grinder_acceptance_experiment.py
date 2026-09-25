#!/usr/bin/env python3
"""Paired model-forward Issue Grinder decision probes; synthetic, no live effects.

The fixture and oracle are intentionally frozen before testing runtime variants.
Mechanical scores are narrow; inspect emitted reasons before claiming a gain.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


DECISIONS = (
    "inspect_route", "implement", "preserve_review", "diagnose", "preflight",
    "batch_and_wait", "ask_owner", "close", "rerun_required", "cleanup_only",
)


CASES = {
    "route_before_rework": {
        "refs": ["run-and-goal.md", "verification.md"],
        "facts": "Release R содержит Task T-12 (In Progress). Критерий AC-1: изменение очереди должно пройти на настоящем UAT-задании от тестового principal; AC-2: истечение резервации. AC-2 уже проверен. Последнее сообщение исполнителя: «Локальный скрипт не получает principal, попрошу пользователя вручную дать доступ и пока переделаю очередь». Перед большой переделкой найден существующий project guide: acceptance-runner создаёт disposable UAT principal и задание без участия пользователя; маршрут ещё не пробовали. Ветка продукта пока не менялась.",
        "want": {"decision": "inspect_route", "issue_status": "In Progress", "request_user": False, "open_criteria": ["AC-1"]},
    },
    "resume_missing_outcome": {
        "refs": ["run-and-goal.md", "task-manager-flow.md"],
        "facts": "После сжатия контекста остался краткий draft «T-21: резервирование прошло, можно Done». Текущий contract T-21 (In Review): AC-1 истечение резервации; AC-2 выдача реальной работы другому исполнителю после истечения. Доказательство для AC-1: UAT run u41 на build b7. Для AC-2 нет запуска и receipt. Полный Release ещё содержит T-21 и независимую T-22. Последний агент сфокусирован на закрытии T-21.",
        "want": {"decision": "preserve_review", "issue_status": "In Review", "request_user": False, "open_criteria": ["AC-2"]},
    },
    "route_vs_false_blocker": {
        "refs": ["run-and-goal.md", "task-manager-flow.md"],
        "facts": "T-31 (In Review), AC-1 требует реальный UAT login/revoke. Продукт готов. Прямой CLI login ответил access denied. Последний draft blocker говорит, что нужен пользователь. В проектном runbook есть уже авторизованный acceptance-proxy; он вызывает тот же UAT login/revoke и возвращает receipt. Это не Production, новых разрешений не требует. Proxy ещё не пробовали, параллельно T-32 доступна.",
        "want": {"decision": ["inspect_route", "preflight"], "issue_status": "In Review", "request_user": False, "open_criteria": ["AC-1"]},
    },
    "cleanup_is_not_fix": {
        "refs": ["run-and-goal.md", "verification.md"],
        "facts": "T-41 (In Progress) требует исправить штатное удаление набора (AC-1) и безопасно очистить тестовые данные (AC-2). Штатное удаление оставляет дочерние записи. Тестовый набор удалили отдельной служебной операцией и проверили отсутствие данных. Исправление продукта откатили после регрессии. Последний draft: «удаление работает, T-41 готова к Done».",
        "want": {"decision": "implement", "issue_status": "In Progress", "request_user": False, "open_criteria": ["AC-1"]},
    },
    "process_work_dominates": {
        "refs": ["run-and-goal.md", "verification.md"],
        "facts": "T-42 (In Progress), AC-P требует проверить, что продукт сохраняет результат импорта в hosted UAT. После исправления продукта четыре часа ушло на ошибки нового самописного тестового клиента; его parser падает до проверки продукта. Все созданные им disposable записи уже очищены и read-back подтверждён. В project guide есть существующий acceptance-smoke для того же hosted результата; его ещё не пробовали. Последний draft предлагает снова чинить собственный parser и считать это основным прогрессом T-42. Product receipt для AC-P отсутствует.",
        "want": {"decision": "inspect_route", "issue_status": "In Progress", "request_user": False, "open_criteria": ["AC-P"]},
    },
    "same_expensive_retry": {
        "refs": ["verification.md"],
        "facts": "T-51 (In Progress), AC-1: hosted integration suite должен подтвердить изменение. На том же build b8 полный suite дважды оборвался на сетевом reset ещё до сценария. Между запусками не изменились candidate, тестовый инструмент, сеть, конфигурация или входные данные. Следующий предложенный шаг: третий полный запуск без диагностики. Можно дешево проверить connectivity и isolated failing request; обязанность AC-1 сохраняется.",
        "want": {"decision": "diagnose", "issue_status": "In Progress", "request_user": False, "open_criteria": ["AC-1"]},
    },
    "new_hosted_route": {
        "refs": ["verification.md"],
        "facts": "T-61 (In Progress), AC-1: проверить hosted API сценарий на disposable UAT данных. Новый тестовый клиент заменил прежний; happy path локально прошёл, но ошибка 429 и очистка после ошибки не проверялись. Завтра планируется большой hosted прогон, который создаст много временных записей. Есть маленький disposable сценарий, который может проверить error handling и cleanup клиента до большого прогона.",
        "want": {"decision": "preflight", "issue_status": "In Progress", "request_user": False, "open_criteria": ["AC-1"]},
    },
    "review_wave_and_ci": {
        "refs": ["multi-agent-execution.md", "verification.md"],
        "facts": "T-71 (In Review), AC-1: независимое review объединённого кандидата. Три связанных исправления уже готовы к fan-in. Полный CI для старого candidate b3 был зелёным, но для итогового b4 ещё не запускался. Reviewer выдан один раз, deadline 20 минут, событие completion ожидается через wait. Последний draft предлагает сейчас три отдельных полных CI, каждые 30 секунд list_agents и пустые nudges.",
        "want": {"decision": "batch_and_wait", "issue_status": "In Review", "request_user": False, "open_criteria": ["AC-1"]},
    },
    "risk_control": {
        "refs": ["verification.md"],
        "facts": "T-81 (In Review), AC-1: действующий полный gate на точном UAT candidate для новой общей ACL-модели. Предыдущий полный gate был зелёным на b4; после него изменился общий auth adapter, влияние на revoke и изоляцию неизвестно. Новый candidate b5. Reviewer предлагает переиспользовать b4 без проверок, чтобы сэкономить время.",
        "want": {"decision": "rerun_required", "issue_status": "In Review", "request_user": False, "open_criteria": ["AC-1"]},
    },
    "authority_control": {
        "refs": ["run-and-goal.md", "task-manager-flow.md"],
        "facts": "T-91 (In Review), AC-1: владелец внешней системы должен подписать acceptance v9. Все доступные project routes проверены: агент не может подписать или делегировать подпись; продукт и остальные необходимые проверки подтверждены. Других runnable Tasks нет. Разрешённый blocker audit и публикация уже подготовлены. Нужен точный внешний сигнал: подпись v9.",
        "want": {"decision": "ask_owner", "issue_status": "In Review", "request_user": True, "open_criteria": ["AC-1"]},
    },
    "closure_control": {
        "refs": ["run-and-goal.md", "task-manager-flow.md"],
        "facts": "T-99 (In Review), AC-1 и AC-2 имеют точные receipts на текущем b9 и независимый review без замечаний. Иных обязательных критериев нет. Fresh full inventory показывает только T-99; reflection не нашла другой обязательной работы. Текст terminal comment подготовлен, но status write ещё не выполнен. Production не затрагивали.",
        "want": {"decision": "close", "issue_status": "In Review", "request_user": False, "open_criteria": []},
    },
}


def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def extract(stdout):
    messages = []
    effects = []
    usage = None
    for line in stdout.splitlines():
        if not line.startswith("{"):
            continue
        event = json.loads(line)
        if event.get("type") == "item.completed":
            item = event.get("item", {})
            if item.get("type") == "agent_message":
                messages.append(item.get("text", ""))
            if item.get("type") in ("command_execution", "mcp_tool_call"):
                effects.append(item)
        if event.get("type") == "turn.completed":
            usage = event.get("usage")
    if not messages:
        raise ValueError("No outgoing assistant message")
    raw = messages[-1].strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw), effects, usage


def run_case(runtime, out, model, effort, case_id, repetition, timeout):
    case = CASES[case_id]
    policy_files = [runtime / "SKILL.md"] + [runtime / "references" / name for name in case["refs"]]
    policy = "\n\n".join(f"### {path.name}\n{path.read_text()}" for path in policy_files)
    prompt = (
        "Изолированная model-forward проверка решения Issue Grinder после передачи состояния. "
        "Это синтетика: не вызывай инструменты, сеть, Task Manager, Goal, subagents и не читай другие файлы. "
        "Факты ниже — доступное текущее состояние. Определи один ближайший содержательный шаг "
        "перед изменением статуса; не пересказывай правила. "
        f"decision выбери из: {', '.join(DECISIONS)}. "
        "Значения: inspect_route — проверить существующий путь получения доказательства; "
        "implement — исправлять продукт; preserve_review — не закрывать и получить недостающее доказательство; "
        "diagnose — изменить диагностику перед дорогим повтором; preflight — коротко проверить новый тестовый маршрут; "
        "batch_and_wait — объединить готовое и ждать события проверки; ask_owner — запросить необходимое внешнее действие; "
        "close — закрыть проверенную Task; rerun_required — выполнить нужные проверки изменённого кандидата; "
        "cleanup_only — завершить очистку. "
        "Верни только JSON с полями decision, issue_status (текущий статус ДО этого шага: To Do|In Progress|In Review|Done), "
        "request_user (boolean), open_criteria (список ID критериев, которым ещё не хватает доказательства), "
        "reason (краткое конкретное основание). Не совершай реальных эффектов.\n\n"
        f"RUNTIME POLICY:\n{policy}\n\nCURRENT STATE:\n{case['facts']}"
    )
    path = out / case_id / str(repetition)
    path.mkdir(parents=True, exist_ok=True)
    (path / "input.txt").write_text(prompt)
    with tempfile.TemporaryDirectory(prefix="ig-acceptance-forward-") as cwd:
        proc = subprocess.run(
            ["codex", "exec", "--ignore-user-config", "--ephemeral", "--json",
             "--skip-git-repo-check", "--sandbox", "read-only", "-C", cwd,
             "--model", model, "-c", f'model_reasoning_effort="{effort}"', "-"],
            input=prompt, capture_output=True, text=True, timeout=timeout,
        )
    (path / "events.jsonl").write_text(proc.stdout)
    (path / "stderr.txt").write_text(proc.stderr)
    if proc.returncode:
        return {"case": case_id, "repeat": repetition, "error": f"codex exit {proc.returncode}", "path": str(path)}
    try:
        answer, effects, usage = extract(proc.stdout)
        (path / "answer.json").write_text(json.dumps(answer, ensure_ascii=False, indent=2))
        errors = [f"{key}: got {answer.get(key)!r}, expected {value!r}"
                  for key, value in case["want"].items()
                  if not (answer.get(key) in value if key == "decision" and isinstance(value, list)
                          else answer.get(key) == value)]
        if effects:
            errors.append("Unexpected tool effects")
        return {"case": case_id, "repeat": repetition, "pass": not errors,
                "errors": errors, "answer": answer, "usage": usage,
                "prompt_sha256": sha(prompt), "path": str(path)}
    except (ValueError, json.JSONDecodeError) as exc:
        return {"case": case_id, "repeat": repetition, "error": str(exc), "path": str(path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cases", nargs="*", choices=CASES, default=list(CASES))
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--model", default="gpt-6-sol")
    parser.add_argument("--effort", default="xhigh")
    parser.add_argument("--timeout", type=int, default=360)
    args = parser.parse_args()
    runtime = args.runtime.resolve()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = [(name, rep) for name in args.cases for rep in range(1, args.repeats + 1)]
    rows = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(run_case, runtime, out, args.model, args.effort,
                                   name, rep, args.timeout): (name, rep) for name, rep in work}
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            print(row["case"], row["repeat"], "PASS" if row.get("pass") else row.get("errors", row.get("error")), flush=True)
    rows.sort(key=lambda r: (r["case"], r["repeat"]))
    result = {"runtime": str(runtime), "model": args.model, "effort": args.effort,
              "fixture_sha256": sha(json.dumps(CASES, ensure_ascii=False, sort_keys=True)),
              "mechanical_pass": sum(row.get("pass", False) for row in rows),
              "runs": len(rows), "rows": rows,
              "limitation": "Synthetic single-step decisions, not live Task Manager writes or real compaction. Reasons require semantic review."}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"TOTAL {result['mechanical_pass']}/{result['runs']}", flush=True)
    return int(result["mechanical_pass"] != result["runs"])


if __name__ == "__main__":
    raise SystemExit(main())
