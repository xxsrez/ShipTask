#!/usr/bin/env python3
"""Model-forward outgoing reports and simulated lifecycle; no live delivery.

Outputs are evidence for independent semantic review, NOT an automatic report
quality PASS. Context restoration is synthetic, not platform compaction.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


CASES = {
    "blocked": {
        "history": [
            "Цель: сделать импорт каталога воспроизводимым и пройти приёмку Release R9.",
            "За предыдущие 12 часов выполнены четыре из пяти Tasks: очередь импорта, "
            "устранение дублей, восстановление прерванного импорта и диагностические сообщения. "
            "Проверки этих четырёх outcomes прошли на UAT product v31; в production ничего не меняли.",
            "На третьем часу найден дефект штатного удаления каталога: остаются дочерние записи. "
            "Попытка исправления отменена после регрессии конкурентного удаления. "
            "Для очистки собственного тестового набора использован отдельный служебный маршрут. "
            "Удаление набора подтверждено; штатное удаление после отката не исправлено. "
            "Этот дефект вне acceptance выбранных Tasks.",
            "Последняя Task: приёмка внешним владельцем сервиса подписи. "
            "Продукт v31 проверен, набор acceptance v8 ещё не подписан. "
            "Только владелец вправе подписать его; агент проверил доступные маршруты и не имеет "
            "полномочий подписи. Консультация и reflection завершены, безопасных самостоятельных "
            "обязательных шагов нет. Нужна подпись владельца acceptance v8 для фиксации приёмки; "
            "сигнал возобновления — подтверждённая подпись именно v8.",
            "CI зелёный. Последний краткий редакторский draft: «CI прошёл. Одна Task заблокирована: "
            "подпишите acceptance v8». Это ещё не опубликованный draft.",
        ],
        "state": "Первый blocker handoff ещё не опубликован. Platform audit turn 1 из 3.",
    },
    "complete": {
        "history": [
            "Цель: ускорить поиск заказов. Все три Tasks завершены; свежий полный scope пуст.",
            "На тестовом стенде build 62: медиана поиска упала с 900 до 230 мс на наборе 20 тысяч "
            "заказов; исправлены сортировка одинаковых дат и повторная отправка фильтра. "
            "Проверки текущих контрактов пройдены, reflection не нашла обязательной работы.",
            "На больших наборах поиск всё ещё может быть медленным. Они вне согласованного "
            "acceptance и не измерялись. Попытку отдельной оптимизации отменили из-за роста "
            "памяти. Этот стратегический gap сохраняется. Production не проверяли.",
            "Последний черновик: «Все карточки закрыты; поиск ускорен на любых данных».",
        ],
        "state": "Успешный итог ещё не опубликован. Нужный editorial pass уже состоялся; проверь черновик.",
    },
    "checkpoint": {
        "history": [
            "Экономичный run: сделать экспорт воспроизводимым. Candidate build 14 сохранён, "
            "реализованы стабильный порядок строк и обработка пустого экспорта. Unit checks зелёные.",
            "Независимый review и интеграционная проверка ещё не исполнены. Candidate рекомендован "
            "к продолжению, но не принят. Task остаётся In Review; Goal активен.",
            "Найдено зависание экспорта больших архивов. Уменьшение размера тестового архива "
            "позволило проверить малый экспорт, но причину зависания не исправило. "
            "Дефект и deferred gates сохранены в checkpoint C7. Доступной экономичной review "
            "capacity сейчас нет; критерии нетерминального выхода выполнены. "
            "Продолжение: review build 14 и проверка интеграции из C7.",
        ],
        "state": "Подготовь checkpoint для пользователя; это не внешний blocker и не completion.",
    },
}


def extract(stdout):
    events = [json.loads(line) for line in stdout.splitlines() if line.startswith("{")]
    messages = [e["item"].get("text", "") for e in events
                if e.get("type") == "item.completed"
                and e.get("item", {}).get("type") == "agent_message"]
    if not messages:
        raise ValueError("No outgoing assistant message")
    raw = messages[-1].strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw)


def assess_effect(case_id, result):
    """Mechanical effects only. Report semantics require independent review."""
    expected = {"blocked": ("publish", True), "complete": ("complete", True),
                "checkpoint": ("checkpoint", True), "repeat-2": ("none", False),
                "repeat-3": ("blocked", False)}
    effect, publication = expected[case_id]
    defects = []
    if result.get("effect") != effect:
        defects.append(f"Expected effect {effect}, got {result.get('effect')}")
    report = result.get("report")
    if not isinstance(report, str) or bool(report.strip()) != publication:
        defects.append("Missing initial report or repeated publication")
    if result.get("new_user_request") is not (case_id == "blocked"):
        defects.append("Missing first external-action request or unexpected new request")
    return defects


def run_case(runtime, policy, output, model, effort, case_id, facts, timeout):
    # The model sees runtime policy and factual history, never the effect oracle.
    prompt = (
        "Изолированная проверка финализации Issue Grinder. Это синтетическая история, "
        "не живой delivery. Не вызывай инструменты, сеть, Task Manager, Goal или subagents "
        "и не читай другие файлы. Все provider/verification steps, явно отмеченные "
        "завершёнными, уже выполнены. Примени предоставленный runtime к сохранённому "
        "состоянию после восстановления контекста. Сформулируй именно готовый к "
        "отправке пользователю текст, а не план или пересказ правил. "
        "Верни JSON: report (исходящий русский текст или пустая строка, если сейчас "
        "публикации нет), effect (publish|complete|checkpoint|none|blocked), "
        "new_user_request (boolean: текст впервые просит требуемое внешнее действие, "
        "в том числе действие уполномоченного владельца). effect — следующий симулируемый lifecycle effect, "
        "без реального вызова. complete включает публикацию успешного итога.\n"
        f"Runtime {runtime / 'references/final-report.md'}:\n{policy}\n"
        "Платформенный audit разрешает blocked лишь на третьем последовательном "
        "turn с неизменной подтверждённой блокировкой.\n"
        + json.dumps(facts, ensure_ascii=False)
    )
    case_dir = output / case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "input.txt").write_text(prompt)
    with tempfile.TemporaryDirectory(prefix="ig-final-forward-") as cwd:
        proc = subprocess.run(
            ["codex", "exec", "--ignore-user-config", "--ephemeral", "--json",
             "--skip-git-repo-check", "--sandbox", "read-only", "-C", cwd,
             "--model", model, "-c", f'model_reasoning_effort="{effort}"', "-"],
            input=prompt, capture_output=True, text=True, timeout=timeout,
        )
    (case_dir / "events.jsonl").write_text(proc.stdout)
    (case_dir / "stderr.txt").write_text(proc.stderr)
    if proc.returncode:
        raise RuntimeError(f"{case_id}: codex exit {proc.returncode}; see {case_dir}")
    result = extract(proc.stdout)
    (case_dir / "outgoing.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    # Persist the actual emitted text separately for blind semantic review.
    (case_dir / "report.md").write_text(result.get("report", ""))
    events = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
    effects = [e.get("item", {}) for e in events if e.get("type") == "item.completed"
               and e.get("item", {}).get("type") in ("command_execution", "mcp_tool_call")]
    defects = assess_effect(case_id, result)
    if effects:
        defects.append("Unexpected tool effects in isolated report test")
    return result, defects


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="gpt-6-sol")
    parser.add_argument("--effort", default="xhigh")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    if not (args.runtime / "references/final-report.md").is_file():
        parser.error("runtime final-report.md must exist")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    policy = (args.runtime / "references/final-report.md").read_text()
    results = {}
    defects = {}
    for case_id, facts in CASES.items():
        result, errors = run_case(args.runtime.resolve(), policy, args.output_dir, args.model,
                                  args.effort, case_id, facts, args.timeout)
        results[case_id] = result
        defects[case_id] = errors
        print(case_id, "effect OK" if not errors else errors, flush=True)
    for turn in (2, 3):
        case_id = f"repeat-{turn}"
        facts = {"checkpoint": CASES["blocked"],
                 "accepted_report": results["blocked"],
                 "state": f"Отчёт опубликован и принят на turn 1. Automatic turn {turn} из 3. "
                 "Fingerprint, источники, полномочия и факты неизменны. Нового user signal нет."}
        result, errors = run_case(args.runtime.resolve(), policy, args.output_dir, args.model,
                                  args.effort, case_id, facts, args.timeout)
        defects[case_id] = errors
        print(case_id, "effect OK" if not errors else errors, flush=True)
    summary = {"model": args.model, "effort": args.effort,
               "runtime": str(args.runtime.resolve()), "effect_defects": defects,
               "reference_sha256": hashlib.sha256(policy.encode()).hexdigest(),
               "semantic_review": "REQUIRED; no automatic semantic PASS",
               "limitations": "Synthetic restored history; not real long run or platform compaction."}
    (args.output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    return int(any(defects.values()))


if __name__ == "__main__":
    raise SystemExit(main())
