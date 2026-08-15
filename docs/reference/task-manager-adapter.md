# Task Manager adapter

Статус: текущий integration profile, 2026-08-15.

Документ описывает точный OAuth/MCP contract, через который `$ship-tasks`
работает с Task Manager. Он не задаёт Project, Release, status или permission
конкретного продуктового репозитория.

## Проверенная база

Профиль сверён с:

- Task Manager `cf02223fe782304e83b4b7711c9f5dfd943d4b53`:
  `docs/specs/agent-api.md`, ADR-0006, ADR-0008 и
  `lib/task-manager-mcp.ts`;
- Task Manager Marketplace
  `3e18568af206a80d8d9497c13d923d709925d9b5`:
  `plugins/task-manager/skills/task-manager/SKILL.md`;
- живым connector 2026-08-15: `get_workspace` подтвердил read и task-write
  capabilities, status catalog и доступность task-oriented tools; read-only
  выборка подтвердила compact `list_tasks`, полный `get_task`, relations,
  provenance, `availableStatuses` и `version`.

Это датированное подтверждение, а не гарантия будущей схемы. При фактическом
запуске authoritative остаются текущие tool descriptions и ответы connector.

## Scope authority

Task Manager является единственным task-source adapter ShipTask. Exact Project,
Release или Tasks выбираются явным invocation, repository instructions либо
project profile. Установленный plugin, успешный OAuth и видимый Project сами по
себе не разрешают выбрать scope или выполнять writes.

Если несколько Projects или Releases одинаково подходят под запрос,
остановиться с `TASK CONTEXT ALARM`. Imported provenance является read-only
external context и не образует отдельный writable task source.

Обязательный Codex Goal является orchestration state ShipTask, а не частью
Task Manager connector и не вторым task source. Его можно сформировать только
после разрешения exact Task Manager scope; Goal не заменяет canonical refs,
current Task detail, connector access или Task write authority.

## Read-only discovery

Использовать progressive disclosure connector:

1. Вызвать `get_workspace` и проверить `capabilities.read`, нужный write scope
   и status catalog.
2. Разрешить названный Project через `list_projects`, затем получить
   `get_project`, если нужны releases, counts, access или допустимые statuses.
3. Разрешить Release через `list_releases`; перед combined filter проверить
   через `get_release`, что он принадлежит выбранному Project.
4. Получить exact inventory через `list_tasks` только с подтверждёнными
   `projectRef`, `releaseRef` и требуемыми filters. Оба ref можно опустить
   только когда scope действительно охватывает все доступные задачи.
5. Продолжать по `nextCursor`, пока `hasMore=false`, когда нужен полный scope.
   Для выбора одного candidate не загружать лишние страницы.
6. Считать list rows только кандидатами. До execution, dependency reasoning или
   write загрузить `get_task` для каждой выбранной задачи.
7. Читать `get_task_external_context` только когда `provenance` сообщает о
   таком контексте и imported comments, attachments или branch metadata
   материальны для acceptance либо boundary dependencies.

`TaskSummary` подходит для inventory и выбора. Описание, lifecycle, relations,
subtasks, access, provenance, current `version` и `availableStatuses` находятся
в `TaskDetail`.

## Identity и scope

- Использовать immutable Task `ref` как canonical identity, а `identifier`
  наподобие `TM-123` — как человекочитаемую ссылку.
- Использовать только canonical Project/Release/status refs из connector, не
  строить refs из display names.
- Проверять release membership до совмещённого Project+Release filter.
- Не считать counts или первую страницу complete inventory.
- Не выводить task acceptance только из title/status; читать detail и при
  необходимости imported context.
- Проверять `access.canEdit` и connector write capability отдельно: OAuth scope
  не отменяет resource ACL.

## Lifecycle projection

Connector возвращает provider status и одну из системных категорий:
`backlog`, `unstarted`, `started`, `completed`, `canceled`. Category помогает
распознать terminal аналоги, но рабочий stage определяется current status name
и canonical ref.

| Status | Category | ShipTask policy |
|---|---|---|
| `Backlog` | `backlog` | Исключить из рабочего scope; не выполнять и не изменять. |
| `To Do` | `unstarted` | Брать как новую работу после preflight. |
| `In Progress` | `started` | Продолжать уже начатую работу из coherent checkpoint. |
| `In Review` | `started` | Проверять exact batch-candidate, batch evidence и связанные duplicates. |
| `Done`, `Finished` и другие terminal аналоги | `completed` | Не выполнять; учитывать только при reconciliation. |
| `Canceled` и terminal аналоги | `canceled` | Не выполнять и не считать successful completion. |
| `Duplicate` | `canceled` | Не выделять отдельную execution lane; читать как review context основной Task. |

Relation `duplicate_of` направлена от duplicate к canonical Task. При review
разрешить canonical Task по исходящей relation, если она есть, затем получить
полный `TaskDetail` всех её входящих `duplicate_of`. При материальном imported
context вызвать `get_task_external_context`. Отличающийся problem statement или
failure scenario становится review finding; status `Duplicate` сам по себе не
доказывает, что сценарий покрыт основной Task.

Переход `To Do → In Progress` допустим только после preflight, переход в
`In Review` — только после per-Task targeted gate и формирования candidate
evidence. `In Review` может ждать review-batch gate и acceptance; это всегда
`completion-remains`. Переход в `Done` допустим только после passing exact
batch gate и authorized task acceptance. Failed gate или changes requested
возвращает Tasks с недействительным evidence в `In Progress` до повторной
проверки. Один status не является доказательством результата.

## Writes и concurrency

- Task writes выполнять только при явной authority текущего workflow и
  `capabilities.writeTasks=true`.
- Перед каждым `update_task` повторно вызвать `get_task` и передать его текущий
  `version`.
- Использовать status ref из `availableStatuses` выбранной Task либо из
  подтверждённого Project/Release detail для создания.
- Значение `null` у `projectRef`, `releaseRef` или `dueDate` очищает поле. Не
  передавать `null`, если очистка не входит в запрос.
- При `version_conflict` заново прочитать Task, сравнить новые факты с
  намерением запуска и повторить update только если он всё ещё применим. Не
  перетирать unrelated newer edits.
- Не повторять `create_task` вслепую после неизвестного network outcome:
  сначала искать возможный созданный duplicate.
- Явно разрешённую новую Task создавать с current canonical status ref для
  `To Do`. Не создавать ShipTask Tasks в `Backlog`; при отсутствии `To Do`
  остановиться до write.
- После write перечитать Task и проверить новый status/version/projection.

ShipTask обычно начинает с уже созданных задач. `create_task` нужен только для
отдельно разрешённого defect/task route; invocation skill не даёт такого
разрешения автоматически.

## Текущие capability gaps

MCP connector умеет читать Projects/Releases/Tasks и создавать/изменять Task,
но не предоставляет tools для:

- append-only comments или отдельного task report;
- claims, leases, heartbeats и fencing;
- изменения assignee, labels, parent/subtasks или relations;
- Project/Release mutation, workflow configuration, sharing, ownership,
  Administration и backup/restore;
- idempotency key для `create_task`.

Goal tools также не являются capability Task Manager connector. При запуске
skill необходимо отдельно проверить model-visible Goal state и возможность
создать либо продолжить совместимый Goal. Если обязательный Goal нельзя
сформировать или удерживать, остановиться до mutations с `TASK CONTEXT ALARM`.

Поэтому текущий Task Manager уже может быть authoritative источником scope,
acceptance, dependencies и status projection, но не заменяет durable
coordination runtime. Не использовать `description` как скрытый append-only
журнал и не перезаписывать её отчётом без отдельного project contract. Claims,
run state и review packets должны иметь project-defined durable channel. Если
такой channel обязателен, но отсутствует, остановиться до execution.

## Completion reconciliation

Перед terminal claim:

1. Перечитать все in-scope Tasks по canonical refs.
2. Сверить status, `version`, relations и незавершённые boundary dependencies.
3. Проверить, что Task Manager projection совпадает с exact Git/workspace
   result, per-Task targeted gates, exact review-batch gate, authorized
   acceptance и обязательными external effects.
4. Отделить imported historical context от evidence текущего запуска.
5. Указать capability gaps и project-defined coordination records отдельно от
   Task Manager state.
6. Повторно получить complete inventory выбранного Project/Release scope и не
   завершать Goal, пока хотя бы одна Task всё ещё подходит под рабочие критерии
   ShipTask.

Task Manager state доказывает только собственную projection. Он не доказывает
commit, merge, deployment, UAT, human acceptance или внешний эффект без
независимого evidence.
