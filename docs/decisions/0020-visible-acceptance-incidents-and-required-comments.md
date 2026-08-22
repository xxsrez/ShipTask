# 0020. Приёмочные инциденты видимы во всём run, comments обязательны

Статус: accepted, 2026-08-22. Уточняет reporting contract ADR-0017 и
outcome-level свободу ADR-0018. Заменяет capability-optional и comment-channel
availability ветви ADR-0003, ADR-0006, ADR-0009, ADR-0015 и ADR-0016. Native
Task comment create/list/read считается базовой возможностью current Task
Manager adapter, а не условной feature ShipTask.

## Контекст

ShipTask уже требовал comment перед существенным status transition, но
обнаруженный при приёмке defect мог стать почти невидимым: агент публиковал
локальный rework comment, исправлял result в том же run и завершал финальный
ответ текущим успешным состоянием. В чате не было обязательного немедленного
сообщения, opening и resolution не связывались, а final report не сохранял факт
найденного и исправленного defect.

Отдельно current документы продолжали обсуждать отсутствие comment capability и
фиксированные 2–4 способа приёмки. Первая ветвь устарела после появления
полноценных native comments; вторая заставляла придумывать альтернативы там, где
существует один сильный путь получить evidence.

## Решение

### Comments — гарантированный adapter contract

- ShipTask всегда использует native Task comments для lifecycle и blocker
  reporting. Он не выполняет capability-optional preflight и не допускает
  завершение без обязательного comment.
- Comment create сопровождается idempotency/reconciliation и read-back по
  Task Manager adapter contract. Неизвестный write outcome сначала
  reconciles; blind retry и fallback в Task fields запрещены.
- Неожиданный отказ write/read-back является обычной наблюдаемой ошибкой
  текущей операции, а не признаком опциональности feature. Пока обязательный
  comment не существует и не перечитан, связанный существенный transition не
  завершён.

### Приёмочный инцидент — durable факт

Приёмочный инцидент возникает, когда проверка exact candidate или release scope
устанавливает один из трёх non-success outcomes:

- `verified-failure`: current acceptance прямо нарушен; это доказанный defect;
- `verification-blocked`: success/failure нельзя доказать; bug не установлен;
- `task-contract-conflict`: current mandatory contract не задаёт однозначный
  observable result.

Сбой отдельного инструмента, ожидаемая red/green iteration и общий batch failure
без task-level attribution сами по себе инцидентом конкретной Task не являются.

Для exact Task инцидент имеет три обязательные поверхности:

1. Немедленный outcome-first update в Codex chat до repair или status write:
   Task, expected result, observed fact или граница знания, impact,
   classification и следующий шаг.
2. Native opening comment с read-back. Для `verified-failure` он публикуется до
   начала rework; для blocker/conflict — до handoff. Если найден defect уже
   terminal Task, opening comment также является объяснением reopen.
3. Compact incident ledger в final run report независимо от final outcome.

Opening comment не заменяется и не стирается после repair. Когда инцидент
устранён, новый resolution/completion comment явно связывает тот же acceptance
criterion с confirmed или inferred cause, fix/result identity, повторной
проверкой, final state и remaining risk. Human-readable Task ref и criterion
достаточны; внутренний UUID не требуется.

### Инцидент остаётся заметным во время работы

- При каждом material state change (`исправляется`, `повторно проверяется`,
  `устранён` либо `остаётся незакрытым`) Codex публикует короткий chat update.
- Пока инцидент unresolved и active run продолжает работу без material change,
  краткое напоминание появляется не реже одного раза примерно в 10 минут.
- Таймерные повторы не создают одинаковые Task comments. Durable Task history
  получает opening, material blocker/change и resolution; chat несёт progress.
- При resume ShipTask перечитывает relevant comments и в первом содержательном
  update называет unresolved incidents выбранного scope.

Вне активного run skill не является scheduler. Отдельные фоновые напоминания
требуют отдельной явно настроенной automation.

### Final success не стирает найденный defect

Финальный `SHIPTASK RUN REPORT` содержит ledger всех material acceptance
incidents run: Task/criterion, что обнаружено, cause/confidence, что исправлено,
чем повторно проверено и final state. Исправленный defect остаётся видимым как
`found and resolved`; unresolved incident располагается рядом с общим result и
не допускает clean-success формулировку для affected Task.

`verification-blocked` и `task-contract-conflict` также видимы, но никогда не
называются product bug без прямого наблюдения exact candidate.

### Verification blocker предлагает решение, а не заполняет квоту

Blocker comment объясняет границу знания и рекомендует самый сильный feasible
следующий способ получить evidence. Несколько вариантов сравниваются только
когда действительно существуют разные допустимые пути и выбор пользователя
materially меняет risk, cost, authority или доказательную силу.

## Последствия

- Пользователь узнаёт о failed acceptance до того, как агент начнёт молча
  исправлять result.
- Task history сохраняет как обнаружение, так и доказанное закрытие проблемы.
- Успешный final report остаётся честным относительно дефектов, найденных по
  дороге.
- Runtime больше не содержит условную ветвь «comments могут отсутствовать» и не
  генерирует искусственные списки альтернатив.
- Behavioral evals должны проверять cross-surface persistence и found-then-fixed
  сценарий, а не только наличие отдельного comment или финального статуса.
