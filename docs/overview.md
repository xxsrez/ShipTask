# Обзор ShipTask

ShipTask — Task Manager-only delivery policy. Он доводит выбранную Task или
batch до фактически подтверждённого результата и отражает этот результат в
Task Manager понятным человеку образом.

```text
Task Manager skill  = технический адаптер
ShipTask skill      = требования к delivery result
Task Composer       = постановка и planning graph в Backlog
Project memory      = selector и project-specific context
Strategic Explainer = помощник по человеческому объяснению
```

## Constitution-first подход

Текущий contract задан [ADR-0018](decisions/0018-outcomes-not-tool-choreography.md)
и [ADR-0019](decisions/0019-goal-only-for-multi-task-implementation.md), а
reporting contract —
[ADR-0020](decisions/0020-visible-acceptance-incidents-and-required-comments.md).
[ADR-0021](decisions/0021-requirements-as-agent-constitution.md) распространяет
этот принцип на agent topology, context и evaluation, а
[ADR-0022](decisions/0022-mandatory-independent-strategic-explainer-for-comments.md)
сохраняет default-требование отдельного Explainer перед каждым комментарием.
[ADR-0024](decisions/0024-adaptive-multi-agent-execution-by-default.md)
добавляет `subagents=auto` для широкого `batch-implementation` и явный
`subagents=off`, а
[ADR-0025](decisions/0025-cost-aware-subagent-profiles.md) направляет только
genuinely simple packets на Luna Max и эскалирует material uncertainty на
current profile. Они уточняют
[ADR-0017](decisions/0017-constitution-first-runtime-contract.md).
Вместо большого универсального сценария runtime содержит несколько обязательных
результатов и жёстких границ. Агент свободен выбирать порядок, инструменты,
реализацию, декомпозицию и число попыток; delegation следует явной политике
ADR-0024.

Неподвижны следующие требования:

- пользовательский outcome важнее Goal, plans и внутренней отчётности;
- несколько независимых safe lanes по умолчанию получают adaptive subagents и
  одного integration owner;
- user-selected subagent profile имеет приоритет; без него только genuinely
  simple packets получают Luna Max, остальные наследуют current model/effort;
- Luna не занимается recovery: ambiguity, surprising environment или proof gap
  возвращают packet current profile без повторного Luna loop;
- общее «без субагентов» означает ноль субагентов, а узкий запрет относится
  только к названной роли;
- status Task соответствует текущим фактам;
- обычный старт `To Do → In Progress` не создаёт комментарий;
- существенный status transition сначала получает понятный native comment и
  comment read-back;
- каждый создаваемый ShipTask-комментарий при разрешённых субагентах до
  публикации проходит отдельного независимого Strategic Explainer;
- material blocker также получает comment, даже без status change;
- native comments являются гарантированной adapter capability и всегда
  сопровождают material lifecycle reporting;
- acceptance incident немедленно виден в chat, durable Task history и final
  run report, даже если defect исправлен в том же run;
- агент сам выбирает и меняет инструменты, способ диагностики и приёмки;
- сбой одного средства сам по себе ничего не доказывает и не обязывает чинить
  именно его;
- acceptance не ослабляется, непроверенное не называется verified;
- явный общий user override включает `subagents=off` для всего run;
- вне `subagents=off` основной агент не заменяет отдельного Strategic
  Explainer собственной редактурой и не публикует комментарий без
  независимого прохода;
- production и другие sensitive effects сохраняют явную authority boundary.

## Запуск

ShipTask активируется явным `$ship-tasks` или delivery intent с exact Task
Manager anchor: существующей Task, выбранным Project/Release/current scope.
Явная команда создать ровно одну Task и сразу выполнить её образует single
create-and-deliver.

Обычная просьба исправить код без Task Manager anchor, status/audit/explanation,
planning и backlog capture ShipTask не запускают.

Planning и backlog capture с Task Manager intent принадлежат Task Composer. Он
оставляет один independently deliverable outcome одной Task, а составной
outcome оформляет как Epic с problem-first описанием через Strategic Explainer,
конкретными подзадачами, live Labels и semantic relations. Это planning-only
projection: новые элементы остаются в `Backlog`, а unknown current Release
опускается без guess.

- `single`: одна Task, без Goal.
- `batch-implementation`: имплементация/rework минимум двух Tasks, с Goal и
  default `subagents=auto`.
- `release`: release уже подготовленного candidate, без Goal.
- project memory меняется только по явной просьбе.

Project, Release, current scope, несколько Tasks и bare invocation являются
selectors, а не автоматическими признаками batch. Goal не создаётся для общего
чтения/приёмки Tasks, commit/push, deploy, smoke или production release.

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
До публикации текст готовит отдельный Strategic Explainer, а основной агент
проверяет его фактическую точность. При явном `subagents=off` тот же quality
contract применяется без отдельного субагента.

## Приёмка

Current facts дают один из четырёх исходов:

- требования текущей Task противоречат друг другу;
- exact candidate доказанно нарушает acceptance;
- доступная проверка не может доказать ни success, ни failure;
- current acceptance и обязательные effects доказаны.

При defect comment объясняет причину возврата, затем Task переходит в
`In Progress`, и rework продолжается в том же run. При невозможности приёмки
Task остаётся `In Review`, а comment рекомендует strongest feasible способ
получить доказательство и сравнивает alternatives только при реальном выборе.
История
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
Goal используется только для прогресса массовой имплементации минимум двух Tasks
и остаётся active, пока в этом scope есть незавершённая работа. Он не определяет
Task outcome и число попыток. Release-only run Goal не создаёт; release может
оставаться done criterion уже существующего совместимого Goal.

Нужные non-production releases в local/dev/test/QA/UAT/staging/preview/sandbox
разрешены после проверки target. Production, destructive durable-data changes,
secrets/privacy/access-policy changes, external recipients и unbounded cost
требуют явной authority.

## Источники

- [Каноническая specification](specs/ship-tasks.md)
- [Constitution-first ADR](decisions/0017-constitution-first-runtime-contract.md)
- [Outcome, не tool choreography](decisions/0018-outcomes-not-tool-choreography.md)
- [Goal только для массовой имплементации](decisions/0019-goal-only-for-multi-task-implementation.md)
- [Видимые приёмочные инциденты и обязательные comments](decisions/0020-visible-acceptance-incidents-and-required-comments.md)
- [Требования как конституция для агентов](decisions/0021-requirements-as-agent-constitution.md)
- [Независимый Strategic Explainer для каждого комментария](decisions/0022-mandatory-independent-strategic-explainer-for-comments.md)
- [Adaptive multi-agent default и explicit opt-out](decisions/0024-adaptive-multi-agent-execution-by-default.md)
- [Cost-aware профили субагентов](decisions/0025-cost-aware-subagent-profiles.md)
- [Task Manager adapter contract](reference/task-manager-adapter.md)
- [Lifecycle evaluation](reference/shiptask-review-disposition-evaluation.md)
- [Strategic Explainer specification](specs/strategic-explainer.md)
- [Task Composer specification](specs/task-composer.md)
- [Task Composer как planning sibling-skill](decisions/0023-task-composer-as-planning-sibling.md)

Runtime sources — `ship-tasks/SKILL.md`, `task-composer/SKILL.md` и
`strategic-explainer/SKILL.md`. Plugin distribution и installed cache должны
быть byte-identical repository source; standalone user-level copies не
используются.
