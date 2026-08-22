# Task Manager adapter

Статус: current compatibility contract, повторно сверен 2026-08-22.

Документ фиксирует только техническую границу между ShipTask и Task Manager
skill/connector. Business delivery policy, lifecycle decisions, Goal,
automatic acceptance, release authority и project memory определяются
[ShipTask specification](../specs/ship-tasks.md), а правила постановки,
decomposition, `Backlog`, Labels и relations —
[Task Composer specification](../specs/task-composer.md), а не adapter.

## Проверенная база

Профиль повторно сверен с marketplace source и installed cache
`task-manager@srez-marketplace` версии `0.7.5+codex.20260821203934`.
Package содержит только adapter skill `task-manager`, не содержит
`ship-tasks`/`task-composer`/`strategic-explainer`, а marketplace source и
installed cache совпадают.
Текущий Task Manager `SKILL.md` прямо запрещает adapter самостоятельно
определять delivery, Goal, verification, release, report-content и terminal-status
policy. При фактическом запуске authoritative остаются current tool descriptions,
capabilities и ответы connector.

## Adapter responsibility

Task Manager skill/connector владеет:

- OAuth connection и workspace access/capability reads;
- Project, Release, Task и status lookup;
- canonical refs, pagination и full detail retrieval;
- ACL checks и optimistic concurrency через current Task `version`;
- Task create/update mechanics;
- native Label catalogs/assignment, parent/subtask hierarchy и Task relations;
- native Task comment create/list/read и reconciliation;
- exact tool errors и retry-safe behavior.

Adapter не выбирает business scope, не решает, нужен ли Goal или Epic, не
определяет `Backlog`/`In Review` business semantics, не выбирает Labels или
dependencies, не принимает result, не классифицирует environment и не разрешает
release. Эти решения получает от Task Composer или ShipTask.

## Minimal read contract

ShipTask передаёт intent/selectors; adapter возвращает live canonical evidence:

1. `get_workspace`: signed-in identity, read/write capabilities и status
   catalog.
2. `list_projects` и при необходимости `get_project`: exact Project ref,
   access, releases и available statuses.
3. `list_releases` и `get_release`: exact Release ref и подтверждённая Project
   membership.
4. `list_labels` и при необходимости label-group reads: live canonical Label
   catalog для planning assignment.
5. `list_tasks`: filtered inventory; для полного Project/Release scope — все
   страницы до `hasMore=false`.
6. `get_task`: full detail каждого выбранного кандидата до dependency,
   acceptance, relation или write reasoning.
7. `get_task_external_context`: только когда provenance сообщает о материальном
   imported context.
8. Native comment list/thread reads: deduplication и read-back Task reports.

List rows и counts не заменяют complete inventory или `TaskDetail`. Human
identifier вроде `TM-123` является selector/display identity; immutable Task
`ref` является write identity.

## Identity and capability invariants

- Использовать только canonical refs, возвращённые current connector. Не
  строить Project/Release/status refs из display names и не доверять remembered
  ref без current lookup.
- Проверять Release membership до combined Project+Release filter.
- Проверять current workspace access и `access.canEdit` отдельно.
- Native comment create/list/read являются гарантированной частью adapter
  contract. ShipTask всегда использует их для обязательного reporting.
- Label, parent Task и relation refs являются canonical opaque identifiers;
  hierarchy и relation direction подтверждаются полным Task read-back.
- Goal tools не являются Task Manager tools.
- Task Manager `Release` не является deployment environment и не доказывает
  production/non-production class.

## Write and concurrency invariants

- До каждого `update_task` заново вызвать `get_task` и передать current
  `version`.
- Брать status ref из current `availableStatuses` либо проверенного
  Project/Release detail.
- Не передавать `null` для `projectRef`, `releaseRef` или `dueDate`, если очистка
  не была явно разрешена.
- При `version_conflict` перечитать Task и повторить update только если intent
  всё ещё применим; не перетирать unrelated newer edits.
- После каждого write перечитать Task и проверить фактические fields, status и
  новую `version`.
- Subtask create и parent mutation используют current parent/child version;
  relation create получает стабильный idempotency key, а relation update/delete
  — current relation version.
- Не повторять `create_task` или comment create вслепую после unknown network
  outcome. Сначала искать возможный созданный object/report.
- Не менять `description`, acceptance или status text ради delivery report.
  Report создаётся только native Task comment operation и независимо
  reconciles через list/read.

Эти invariants ShipTask сохраняет в runtime даже если отдельный Task Manager
skill не был автоматически загружен. Конкретные tool names и payload schema
берутся из current adapter skill/tool descriptions, а не копируются в business
policy.

## Capability gaps

Current adapter может не предоставлять claims, leases, heartbeats, fencing,
idempotency для Task create, Label catalog administration, Project/Release
administration или durable orchestration state. Task Composer и ShipTask не
изображают отсутствующие capabilities существующими.

Если отсутствие capability делает любую следующую mutation небезопасной,
ShipTask применяет `TASK CONTEXT ALARM`. Если gap изолирован одной Task, policy
может оставить её truthful non-terminal и продолжить независимый batch scope.

## Adapter handoff result

Для каждого read/write adapter должен позволить ShipTask зафиксировать:

- resolved canonical identity;
- current detail/status/version/access;
- pagination completeness для multi-task inventory;
- write outcome и post-write read-back;
- фактические Labels, hierarchy и relation type/direction после planning write;
- native comment/report identity и read-back; `write-outcome-unknown` сначала
  reconciles через native reads до retry или status transition;
- exact connector error без выдуманного business interpretation.

Task Manager state доказывает только собственную projection. Commit, build,
deployment, smoke, automatic acceptance decision и другие external effects
требуют независимого evidence по ShipTask policy.
