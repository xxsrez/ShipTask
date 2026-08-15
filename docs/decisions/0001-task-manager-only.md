# 0001. Task Manager-only skill

Статус: accepted, 2026-08-15.

## Контекст

ShipTask выполняет уже созданный task scope через собственный Task Manager и
его OAuth/MCP connector. Поддержка нескольких task providers создавала лишний
слой discovery, неоднозначную authority и документацию о поведении, которое не
нужно продукту.

## Решение

- Использовать Task Manager как единственный authoritative task source
  `$ship-tasks`.
- Включить точный connector workflow в исполнимый skill: `get_workspace`,
  разрешение Project/Release, compact `list_tasks`, полный `get_task`,
  optimistic Task updates и post-write reconciliation.
- Не запускать execution, если Task Manager connector недоступен, exact scope
  неоднозначен или обязательная capability отсутствует.
- Брать конкретные Project/Release refs, repository commands, branches,
  environments, external targets и product policy из текущего project context.
- Поддерживать одну каноническую specification и один runtime skill без
  параллельных поколений.
- Синхронизировать user-level копию только по явной команде пользователя и
  проверять её точное совпадение с repository source.

## Последствия

Положительные:

- skill может сразу использовать известные Task Manager tools без
  provider-selection layer;
- list/detail boundary экономит context и не смешивает inventory с acceptance;
- canonical refs и Task `version` защищают scope и writes;
- Project, Release и Task statuses становятся одной видимой системой работы.

Ограничения:

- connector пока не предоставляет native comment writes, durable claims или
  append-only task reports; [ADR-0003](0003-delivery-reports-as-task-comments.md)
  требует скипать report step как `not-available` и запрещает fallback в Task
  description;
- Project/Release administration, sharing, ownership, workflow configuration и
  backup не входят в task-oriented connector;
- отсутствие connector или write scope является blocker, а не поводом выбрать
  другой источник.
