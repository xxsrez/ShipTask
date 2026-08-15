# Delivery report внутри Task

Использовать этот reference перед первым report write в запуске `$ship-tasks`.
Report является актуальным acceptance/completion artifact конкретной Task, а не
append-only журналом выполнения.

## Содержание

- [Storage contract](#storage-contract)
- [Когда обновлять](#когда-обновлять)
- [Базовый шаблон](#базовый-шаблон)
- [Success profile](#success-profile)
- [Failure profile](#failure-profile)
- [Диаграммы](#диаграммы)
- [Качество и безопасность](#качество-и-безопасность)

## Storage contract

Current Task Manager показывает `description` как plain text. Использовать
короткие headings, bullets и моноширинные text diagrams; не использовать
Markdown table или Mermaid, пока current project context не подтвердит их
фактический render.

Использовать ровно один block с точными sentinel lines:

```text
===== SHIPTASK DELIVERY REPORT: START =====
<report body>
===== SHIPTASK DELIVERY REPORT: END =====
```

Перед write:

1. Вызвать `get_task` и взять current `description` и `version`.
2. Сохранить весь текст вне sentinels без изменений.
3. Если block отсутствует, добавить два line breaks и новый block в конец.
4. Если block один, заменить только его целиком.
5. При нескольких blocks, одном marker без пары, marker внутри report body или
   объявленном другом Task ref выдать `TASK CONTEXT ALARM` до write.
6. Проверить current field limit; не обрезать исходное описание или evidence.
7. Передать current `version`; совместить report и status в одном
   `update_task`, когда stage позволяет.
8. Перечитать Task и проверить exact block, status и новую `version`.

Не добавлять новые blocks для retries, rework или acceptance. Заменять один
managed block актуальным состоянием. Пользовательские заметки принадлежат тексту
вне sentinels и всегда сохраняются.

## Когда обновлять

- `ACCEPTANCE READY`: after passing targeted and exact batch gates, до запроса
  acceptance.
- `REWORK REQUIRED`: material failure инвалидировал candidate; записать до или
  в одном write с `In Review → In Progress`.
- `BLOCKED`: execution уже начался, safe progress остановлен, а blocker
  действительно требует handoff; это не ослабляет Goal blocker threshold.
- `COMPLETED`: после authorized acceptance; финализировать в одном write с
  `Done`, когда возможно.
- `CANCELED`: перед terminal cancel с подтверждённой причиной.

Обычные red/green iterations, transient local mistakes и каждый повтор теста не
создают incident report. Material failure — это user-visible impact, failed
batch/external effect, rollback/revert, invalidated candidate, повторяющийся
rework или blocker после начала execution.

## Базовый шаблон

Писать на языке пользователя. Удалять неприменимые sections, но сохранять
outcome, identity, evidence и next decision.

```text
===== SHIPTASK DELIVERY REPORT: START =====
SHIPTASK DELIVERY REPORT
State: ACCEPTANCE READY | REWORK REQUIRED | BLOCKED | COMPLETED | CANCELED
Task: <identifier and title>
Exact result: <commit/build/artifact/runtime identity>
Review batch: <batch identity or not-applicable>
Acceptance: PENDING | <authority and verified decision evidence>

OUTCOME
<2-5 строк: что теперь получает пользователь или что мешает результату>

HOW IT WORKS
<объяснение основного поведения простыми словами>

<одна полезная text diagram либо compact before/after>

IMPLEMENTATION AND DECISIONS
- <material changed boundary/component and why>
- <important tradeoff or compatibility decision>

EVIDENCE
- <acceptance criterion>: PROVED | FAILED | NOT PROVED — <evidence>
- Targeted gate: <result and identity>
- Batch gate: <result and identity>
- External effect: <verified result or not-applicable>

LIMITATIONS AND RISKS
- <known limitation, residual risk or none known within verified scope>

USER DECISION / NEXT ACTION
<accept exact result, review specific gap, rework, unblock or no action>
===== SHIPTASK DELIVERY REPORT: END =====
```

## Success profile

Сначала ответить на вопросы пользователя:

1. Что изменилось в его сценарии и как этим пользоваться?
2. Как запрос проходит через систему?
3. Какие boundaries/components изменились и почему выбран этот вариант?
4. Что проверено именно на exact result?
5. Какие ограничения или manual steps остались?

Для UI показать короткий user journey/before-after. Для service/data change —
request/data sequence. Для architecture — только затронутый context/container
boundary. Для policy/config — effective before/after и decision path. Для
external effect — target, action, receipt, observed state и reversibility.
Для performance/data change показывать measured before/after с units, workload
и measurement method, а не неподтверждённое «стало быстрее».

Не перечислять все изменённые файлы, если это не помогает понять систему.
Ссылаться на canonical diff/check/deployment evidence, когда оно доступно
читателю; не вставлять полный output.

## Failure profile

При material failure заменить либо расширить центральные sections:

```text
WHAT HAPPENED
<симптом и текущее состояние>

USER IMPACT
<кто/что затронуто, duration/blast radius только если доказаны>

DETECTION AND CAUSAL CHAIN
[Trigger] -> [Failure] -> [Observed impact] -> [Detection]

CAUSE
Confidence: CONFIRMED | PROBABLE | UNKNOWN
<evidence отдельно от inference; без персонального обвинения>

RECOVERY / REWORK
<что исправлено, откатано или ещё требуется>

PREVENTION AND REMAINING RISK
<конкретный проверяемый barrier; новый Task только с authority>
```

Если root cause неизвестен, так и написать; не повышать confidence из-за
правдоподобного объяснения. Разделять mitigation и permanent fix. Action item
должен иметь observable end state; не писать расплывчатое «улучшить тесты».

## Диаграммы

Использовать одну-две схемы только когда они сокращают объяснение:

- runtime/sequence flow: `[User] -> [UI] -> [API] -> [Store]`;
- changed boundary: `[Existing] -> [New component] -> [Consumer]`;
- lifecycle: `[To Do] -> [In Progress] -> [In Review] -> [Done]`;
- causal chain: `[Trigger] -> [Defect] -> [Impact] -> [Detection] -> [Fix]`;
- before/after для локального behavior.
- measured comparison для performance/data, только при сопоставимом evidence.

Держать строку примерно до 80 characters, подписывать неочевидные arrows и
показывать только участвующие nodes. Для cross-component feature предпочитать
один context/container-level view; code-level diagram нужен только когда без
него нельзя понять поведение. Не вставлять diagram ради декоративности.

## Качество и безопасность

- Начинать с outcome, не с процесса агента.
- Писать для пользователя проекта, объяснять неизвестные terms.
- Отделять observed evidence, qualified inference и unknown.
- Не считать report доказательством checks, acceptance или external effect.
- Не включать secrets, tokens, signed URLs, private data, raw stack traces,
  exploit details или недоступные пользователю local paths.
- Не выдумывать metrics, impact, root cause, links, screenshots или results.
- Не копировать полный batch report во все Tasks; оставить только
  task-specific meaning и shared batch identity/result.
- Сохранять concise report для trivial success; при material failure дать
  достаточную глубину для понимания impact, причины, recovery и prevention.
