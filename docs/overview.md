# Обзор ShipTask

ShipTask — Task Manager-only delivery policy. Он доводит выбранную Task или
batch до фактически подтверждённого результата и отражает этот результат в
Task Manager понятным человеку образом.

```text
Task Manager skill  = технический адаптер
ShipTask skill      = требования к delivery result
Project memory      = selector и project-specific context
Strategic Explainer = помощник по человеческому объяснению
```

## Constitution-first подход

Текущий contract задан [ADR-0018](decisions/0018-outcomes-not-tool-choreography.md),
который уточняет [ADR-0017](decisions/0017-constitution-first-runtime-contract.md).
Вместо большого универсального сценария runtime содержит несколько обязательных
результатов и жёстких границ. Агент свободен выбирать порядок, инструменты,
реализацию и достаточные проверки.

Неподвижны следующие требования:

- пользовательский outcome важнее Goal, plans и внутренней отчётности;
- status Task соответствует текущим фактам;
- существенный status transition сначала получает понятный native comment и
  comment read-back; исключение — обычный старт `To Do → In Progress`;
- material blocker также получает comment, даже без status change;
- агент сам выбирает и меняет инструменты, способ диагностики и приёмки;
- сбой одного средства сам по себе ничего не доказывает и не обязывает чинить
  именно его;
- acceptance не ослабляется, непроверенное не называется verified;
- Strategic Explainer помогает сформулировать смысл, но не принимает решения;
- production и другие sensitive effects сохраняют явную authority boundary.

## Запуск

ShipTask активируется явным `$ship-tasks` или delivery intent с exact Task
Manager anchor: существующей Task, выбранным Project/Release/current scope.
Явная команда создать ровно одну Task и сразу выполнить её образует single
create-and-deliver.

Обычная просьба исправить код без Task Manager anchor, status/audit/explanation,
planning и backlog capture ShipTask не запускают.

- `single`: одна Task, без Goal.
- `batch`: несколько Tasks/Project/Release/bare scope, с Goal.
- project memory меняется только по явной просьбе.

Task Manager live state всегда перечитывается. Memory не является evidence
текущего status, version, comments, access или runtime result.

## Lifecycle

```text
To Do → In Progress → In Review → Done
                            ↘ In Progress при доказанном дефекте
```

`In Review` нейтрален: candidate предъявлен, но status сам не доказывает ни
успех, ни failure. Manual acceptance не ожидается. При доказанном success
completion comment предшествует `Done`.

При существенном переходе порядок effects один:

1. понятный Task comment;
2. read-back comment;
3. status write;
4. Task read-back.

Ответ в Codex, Goal, reason code или `description` comment не заменяют.
Существенный status transition считается завершённым только при фактическом
comment и read-back; технический путь к этому результату выбирает агент.

## Приёмка

Current facts дают один из четырёх исходов:

- требования текущей Task противоречат друг другу;
- exact candidate доказанно нарушает acceptance;
- доступная проверка не может доказать ни success, ни failure;
- current acceptance и обязательные effects доказаны.

При defect comment объясняет причину возврата, затем Task переходит в
`In Progress`, и rework продолжается в том же run. При невозможности приёмки
Task остаётся `In Review`, а comment предлагает 2–4 способа получить
доказательство. История
редакций acceptance и число прошлых попыток сами по себе не являются problem.

## Инструменты и остановка

Skill не выбирает инструменты за агента. Агент может чинить, заменять или
сочетать средства по собственному инженерному решению. Важно только, чтобы
итоговый evidence действительно доказывал current acceptance.

Нет счётчика обязательных повторов и общей последовательности repair. Остановка
означает, что в текущем scope и полномочиях агент не нашёл достаточного
безопасного способа продолжить. Тогда причина, impact и условие возобновления
сообщаются прямо.

## Autonomy, Goal и release

Изолированный blocker одной Task не останавливает независимую runnable работу.
Goal используется только для batch progress и остаётся active, пока в scope есть
незавершённая работа. Он не определяет Task outcome и число попыток.

Нужные non-production releases в local/dev/test/QA/UAT/staging/preview/sandbox
разрешены после проверки target. Production, destructive durable-data changes,
secrets/privacy/access-policy changes, external recipients и unbounded cost
требуют явной authority.

## Источники

- [Каноническая specification](specs/ship-tasks.md)
- [Constitution-first ADR](decisions/0017-constitution-first-runtime-contract.md)
- [Outcome, не tool choreography](decisions/0018-outcomes-not-tool-choreography.md)
- [Task Manager adapter contract](reference/task-manager-adapter.md)
- [Lifecycle evaluation](reference/shiptask-review-disposition-evaluation.md)
- [Strategic Explainer specification](specs/strategic-explainer.md)

Runtime source — `ship-tasks/SKILL.md`. Plugin distribution и installed cache
должны быть byte-identical repository source; standalone user-level copies не
используются.
