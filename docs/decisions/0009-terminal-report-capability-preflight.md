# 0009. Terminal-report capability как preflight barrier

Статус: superseded, 2026-08-18. Fail-fast решение из этого ADR отменено
[ADR-0010](0010-blocker-analysis-and-human-run-report.md). Документ сохранён как
история ошибочной гипотезы и не является текущим runtime contract. ADR-0017
возвращает не старый безусловный fail-fast, а общий contract: необходимый
инструмент сначала диагностируется и восстанавливается; без comment read-back
существенный transition запрещён. Current adapter guarantee без отдельного
comment capability preflight задан
[ADR-0020](0020-visible-acceptance-incidents-and-required-comments.md).

## Контекст

Обязательный delivery comment является общим terminal effect для каждой
изменённой рабочей Task. Предыдущий контракт разрешал при отсутствии native
comment tools продолжить независимые Tasks, оставить их non-terminal и
зафиксировать `comment-delivery-unavailable` только в конце.

В реальном batch-run этот выбор дал системно плохой результат: preflight до
Goal уже видел отсутствие comment create/list/read, но workflow продолжил весь
runnable scope. В результате двадцать четыре Tasks накопились в `In Review`
без единого durable handoff, хотя code, release и verification были завершены.
Production authority не могла устранить проблему, потому что blocker находился
в session-scoped connector tool catalog, а не в release target.

Недоступность общего terminal-report channel нельзя считать изолированным
task-local blocker. Если она известна заранее, безопасный результат — не
начинать delivery, а объяснить, как восстановить capability.

## Решение

- После exact scope и complete read-only inventory, но до batch Goal и любых
  code, Git, Task Manager, ownership, deploy или других delivery mutations,
  проверить current native comment create и list/read tools и authority.
- Если хотя бы одна рабочая Task потребует обязательный report, а channel
  отсутствует, unsupported или unauthorized, выдать global
  `TASK CONTEXT ALARM` с reason `terminal-report-channel-unavailable`. Не
  создавать Goal, не начинать Task и не продолжать runnable queue.
- Узкое bootstrap-исключение разрешено только для exact `single` Task, чьи
  acceptance criteria непосредственно восстанавливают native comment
  create/list/read для ShipTask. Выполнить только её минимальный result,
  остановиться на truthful non-terminal checkpoint и потребовать fresh
  capability preflight; не использовать исключение для Project/Release batch
  или unrelated Tasks.
- Если channel стал unavailable либо write/read-back оказался unreconciled уже
  после delivery mutation, немедленно прекратить новый Task dispatch. Сначала
  reconciliate активные lanes в truthful statuses, затем сформировать один
  scope-wide blocker ledger. Не продолжать остальные Tasks под видом
  независимой работы: terminal channel является общей зависимостью всего run.
- Перед `update_goal(status="blocked")` обязательно опубликовать в текущем
  interaction `GOAL BLOCKER REPORT`: exact reason, affected Task identifiers и
  statuses, complete inventory и `runnable_count`, last safe checkpoint и
  result identities, недостающий effect/evidence, выполненные recovery checks,
  почему текущая session не может исправить blocker, comment disposition и
  один exact resume step. Повторное чтение того же state не заменяет строгий
  blocker threshold Goal tool.
- Если comment channel доступен, каждый task-local defer по-прежнему получает
  собственный `BLOCKED` comment с read-back. Если сам channel является общим
  blocker, `GOAL BLOCKER REPORT` обязан явно перечислить Tasks с
  `commentCount=0`/`not-available`; Task fields не используются как fallback.

## Последствия

Положительные:

- stale connector snapshot обнаруживается до массовых lifecycle/code writes;
- Project/Release не превращаются в большую очередь `In Review` без durable
  reports;
- Goal blocker объясняет не только статус, но и exact impact, checkpoint и
  resume path;
- production approval остаётся независимой authority boundary и не маскирует
  connector capability failure.

Ограничения:

- delivery не начнётся в session, где обязательные comment tools отсутствуют,
  даже если implementation технически возможна;
- self-bootstrap comment capability допускает максимум одну exact Task и всё
  равно требует fresh preflight перед terminal reconciliation;
- Goal tool не хранит отдельное reason field, поэтому blocker ledger остаётся
  обязательной частью interaction history.
