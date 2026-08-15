# Обзор ShipTask

## Назначение

`$ship-tasks` — явно вызываемый Task Manager-only workflow для доставки уже
созданного и выбранного task scope. Skill разрешает Project, Release и Tasks
через connector, читает полный Task detail, проверяет dependencies и authority,
координирует execution, integration, verification, human acceptance и
terminal status projection.

Конкретные Project/Release refs, repository commands, branches, environments и
внешние эффекты определяются текущим project context. Если connector, exact
scope или authority нельзя установить достоверно, skill обязан остановиться с
`TASK CONTEXT ALARM` до первой мутации.

## Текущий статус

- [Ship Tasks](specs/ship-tasks.md) — единственная каноническая specification.
- `ship-tasks/SKILL.md` — компактный исполнимый contract на её основе.
- [Task Manager adapter](reference/task-manager-adapter.md) — точный OAuth/MCP
  tool flow, identity, status и write semantics.
- Cross-session scheduler, connector comments, durable claims и append-only
  task reports не изображаются существующими capabilities.
- User-level копия должна совпадать с repository source после явной
  синхронизации.

## Целевой продуктовый поток

```text
Backlog                           excluded intake
To Do → In Progress → In Review → Done or Canceled
                           ↑
                  duplicate scenarios
```

`To Do` является входом новой работы, `In Progress` — продолжающейся работой,
`In Review` — проверяемым candidate. Terminal statuses не создают работу.
`Duplicate` не получает отдельную execution lane, но все связанные duplicates
обязательно читаются при review основной Task: иной ракурс проблемы должен быть
покрыт evidence либо стать явным finding.

Цель review flow — не заменить человеческую приёмку, а уменьшить число
обращений к пользователю и стоимость каждого переключения контекста.

## Границы

- Skill не создаёт scope из неопределённого пожелания.
- Skill не берёт Tasks из `Backlog` и не меняет их.
- Явно разрешённые новые Tasks создаются в `To Do`, а не в `Backlog`.
- Skill не получает внешние полномочия из одного факта invocation.
- Skill не работает без подключённого Task Manager connector.
- Наличие connector не заменяет authoritative Project/Release scope и write
  authority конкретного проекта.
- Skill не превращает failed check в разрешение на unrelated cleanup.
- Skill не называет plan, worker report, commit, test или deploy достаточным
  доказательством completion другого слоя.
