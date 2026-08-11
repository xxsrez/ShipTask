---
name: ship-tasks
description: "Доводить явно заданный task scope текущего проекта до проверенного terminal outcome: выполнить каждую in-scope task, соблюсти dependencies и ownership, безопасно интегрировать результаты, выполнить обязательные проверки и сверить внешние эффекты. Использовать только при явном вызове $ship-tasks или явной просьбе исполнить установленный task-delivery workflow проекта. Исходить из того, что authoritative task source, exact scope, acceptance, integration policy, verification contract и completion evidence известны из текущего контекста; до любых мутаций остановиться и поднять тревогу, если критичный факт нельзя достоверно установить. Не выводить scope expansion, destructive cleanup или внешние полномочия по умолчанию."
---

# Ship Tasks

Доставлять известный task scope как один проверенный результат. Брать конкретные
задачи, команды, ветки, статусы, среды и инструменты из актуального project
context, а не из этого skill.

## Проверить контракт осведомлённости

До первой мутации уметь точно назвать:

- authoritative task scope, его stable identity и terminal done criteria;
- task source или иной authoritative input, acceptance, dependencies и правила
  изменения состояний;
- применимые project instructions, specifications и tests;
- workspace или repository root, integration policy, текущую ownership и
  допустимые writes;
- targeted checks, обязательный полный gate и другие acceptance checks;
- внешние эффекты, прямо требуемые задачами, и способ независимо их проверить;
- необходимые permissions, credentials, approvals и destructive boundaries;
- запрошенную execution topology и реально доступную capacity.

Считать фазу неприменимой только когда authoritative project context явно
задаёт `N/A`. Не навязывать tracker, Git, workers, deployment или иной механизм
проекту, который его не использует.

Сначала искать недостающие сведения read-only в project context, tool state и
текущем invocation. Не угадывать task source, scope, branch, команды, target,
writer role или смысл `workers=N`.

Если хотя бы один критичный пункт неизвестен, неоднозначен или противоречив:

1. Остановиться до code, Git, task-source, external-effect и ownership writes.
2. Выдать `TASK CONTEXT ALARM` с известным scope, недостающими или
   конфликтующими фактами, проверенными источниками, последним безопасным
   checkpoint и точным решением либо доступом, который нужен.
3. Продолжить только после получения authoritative context. Наличие credentials
   не считать authorization.

## Удерживать один результат

- Считать terminal outcome завершением всего exact scope и только тех defects,
  которые project policy уже включает в него. Отдельная task, worker result,
  merge, check или внешний effect — только промежуточный прогресс.
- Не расширять scope, permissions или external targets самим фактом запуска
  skill.
- Следовать ограничениям текущего invocation, затем task acceptance и
  dependencies, project instructions, specifications/tests и только затем
  этому общему workflow.
- Для многошаговой работы поддерживать актуальный plan. Goal создавать или
  менять только когда это отдельно разрешено текущим runtime и пользователем;
  ни Goal, ни plan, ни journal не считать доказательством внешнего effect.

## Выполнить read-only preflight

1. Прочитать полностью общие инструкции проекта и только документы затронутых
   surfaces; при неизвестной cross-cutting surface расширить чтение.
2. Получить complete, current inventory exact scope. Отделить незавершённую
   работу от historical terminal records и проверить boundary dependencies.
3. Проверить применимые workspace, Git, branches, worktrees, uncommitted changes
   и provenance существующей работы. Сохранить пользовательские и чужие edits.
4. Проверить active run, writer ownership, применимые worker claims и уже
   выполненные внешние эффекты. Без доказанной authority оставаться observer.
5. Построить dependency-aware ready frontier и выделить независимые writable
   scopes.
6. Сверить requested topology с runtime capacity. Не переопределять молча
   `workers=N`; отдельно сообщать requested, available и sustained lanes.

После preflight различить `work-remains`, `completion-remains`, `resume`,
`no-work` и `conflict`. Реализованная, но не интегрированная, не проверенная или
не доведённая до обязательного external effect задача означает
`completion-remains`, а не `no-work`.

Для доказанного `no-work` выполнить reconciliation и остановиться. Не создавать
пустые changes, не запускать дорогие checks и не повторять внешние эффекты
только ради нового evidence, если этого прямо не требует project contract.

## Координировать выполнение

- Взять writer roles и shared-write authority только из project contract. Если
  не определено, кто меняет integration target, task source или coordination
  state, поднять `TASK CONTEXT ALARM`, а не назначать writer по умолчанию.
- В serial mode не создавать workers, lanes или worktrees без необходимости.
- В parallel mode дать каждому worker отдельную execution surface, одну active
  task и непересекающийся writable scope. Не разделять mutable dependency,
  cache, tmp или runtime directories между workers.
- В parallel mode до изменений зафиксировать assignment доступным project
  coordination mechanism. Не dispatch-ить конфликтующие dependencies или paths.
- Передать worker только exact task и acceptance, dependencies, base identity,
  ownership paths, нужные документы, targeted checks и запреты на shared writes.
- Потребовать bounded committed result, если проект использует Git, immutable
  result identity, passing targeted checks, scope diff и явные gaps.
- Назначенному integration writer независимо проверить result, интегрировать
  его по project policy и повторить затронутые checks.
- Менять task state на terminal только после выполнения всей acceptance и
  достаточного evidence, а не после одного worker report или merge.
- При conflict или выходе за scope остановить затронутую lane, уточнить ownership
  и повторить проверки после разрешения. Независимые lanes продолжать.

## Выполнять и проверять задачи

Для каждой ready task:

1. Зафиксировать exact scope, base identity и разрешённые writes.
2. Реализовать минимальный целостный результат без unrelated cleanup.
3. Выполнить targeted checks и проверить changed scope.
4. Интегрировать результат только предусмотренным проектом способом.
5. Выполнить обязательные integration и aggregate checks на exact result.
6. Произвести только те внешние эффекты, которые прямо входят в acceptance, и
   независимо проверить их на exact target.
7. Записать bounded evidence без secrets, private content и signed URLs;
   обновить task source только проверенными фактами.

Разделять evidence для task state, source changes, integration, checks и внешних
эффектов. Успех одного слоя не доказывает остальные.

## Обрабатывать defects без расширения scope

- После failed check или сломанного обязательного external effect приостановить
  затронутый ordinary dispatch и сохранить краткий redacted symptom.
- Автоматически исправлять только defect, который acceptance или project policy
  явно включает в текущий scope. Иначе остановиться и запросить scope decision
  до code или task-source writes.
- Для in-scope defect использовать предусмотренный проектом маршрут: bounded
  fix, reopen исходной task, новая дедуплицированная task, waiver, rollback или
  abort. Не превращать fix в тихое расширение scope.
- После изменения повторить все затронутые checks и обязательные внешние эффекты.
- Не использовать failure как разрешение на opportunistic cleanup, unrelated
  fixes или destructive recovery.

## Возобновлять через reconciliation

При resume сначала сверить durable records с реальными workspace, Git,
task-source, checks и external states. Journal, комментарий или прежний report
считать checkpoint, но не proof.

При необъяснимом drift, competing owner или dirty state остановить затронутую
lane и поднять тревогу. Не выполнять автоматические reset, clean, stash,
force-push, takeover, удаление worktree/branch или переписывание чужой работы.

## Завершить и отчитаться

До объявления completion проверить по текущим authoritative sources:

- zero unfinished in-scope tasks и unresolved in-scope defects;
- все lanes освобождены, а принятые результаты присутствуют в integration state;
- применимый workspace clean и exact integrated result однозначен;
- final project checks относятся к exact result;
- все обязательные external effects выполнены и независимо проверены;
- применимая task-source projection соответствует фактам;
- применимые Goal, journal и run records reconciled и terminal.

В финальном отчёте отдельно указать exact scope/task state, source-result
identity, checks, external effects, defects/gaps и любые historical или inherited
проверки. Не объявлять scope завершённым при отсутствующем terminal evidence.
