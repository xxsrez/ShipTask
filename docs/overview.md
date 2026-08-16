# Обзор ShipTask

## Назначение

`$ship-tasks` — явно вызываемый Task Manager-only workflow для доставки уже
созданного и выбранного task scope. Skill разрешает Project, Release и Tasks
через connector, читает полный Task detail, проверяет dependencies и authority,
создаёт обязательный workflow Goal и координирует execution, integration,
двухуровневую verification, automatic acceptance и terminal status projection.
Goal остаётся активным, пока в выбранной границе есть `To Do`, `In Progress`,
`In Review`, rework/completion remnants или unresolved in-scope defects.

Конкретные Project/Release refs, repository commands, branches, environments и
внешние эффекты определяются текущим project context. Global конфликт
connector/exact scope/Goal/shared authority останавливает run с
`TASK CONTEXT ALARM`; изолированный вопрос по одной Task откладывает только её.

## Текущий статус

- [Ship Tasks](specs/ship-tasks.md) — единственная каноническая specification.
- `ship-tasks/SKILL.md` — компактный исполнимый contract на её основе.
- [Task Manager adapter](reference/task-manager-adapter.md) — точный OAuth/MCP
  tool flow, identity, status и write semantics.
- Каждый запуск после разрешения exact scope и до первой non-Goal mutation
  создаёт Goal либо продолжает уже активный совместимый Goal. Несовместимый
  незавершённый Goal блокирует запуск с `TASK CONTEXT ALARM`.
- Cross-session scheduler, durable claims и отсутствующие connector capabilities
  не изображаются существующими.
- Delivery report публикуется только как native Task comment, когда current
  connector действительно предоставляет comment write. Пока capability нет,
  report step получает `not-available` и скипается; `description` не меняется.
- Пока существует runnable work, skill не прерывает run task-local вопросами:
  безопасный default выбирается автоматически, сложная Task попадает в decision
  queue, а остальные продолжаются. При доступных comments defer обязательно
  получает `BLOCKED` handoff.
- Dev/test/QA/UAT/staging/preview/sandbox releases автоматически разрешены в
  границах exact Task и проверенного non-production target. Production release
  выполняется только по явному user approval; без него Task откладывается.
- Terminal-ready result автоматически принимается и переводится в `Done` без
  вопроса пользователю. Если позже обнаружен bug, пользователь reopen-ит Task
  либо создаёт новую проблему для следующего ShipTask scope.
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
`In Review` — targeted-verified candidate, который ждёт batch gate, required
effects или terminal reconciliation, но не ручную приёмку. Terminal statuses не
создают работу.
`Duplicate` не получает отдельную execution lane, но все связанные duplicates
обязательно читаются при review основной Task: иной ракурс проблемы должен быть
покрыт evidence либо стать явным finding.

На каждую Task выполняется быстрый targeted gate. Дорогой aggregate/full gate и
общие runtime/external checks выполняются периодически на exact integrated
review batch. Failed batch возвращает затронутые Tasks в `In Progress`; при
неясной attribution reopen получает весь связанный batch. Это уменьшает
стоимость проверок, не ослабляя terminal gate.

Invocation `$ship-tasks` разрешает automatic acceptance после полного terminal
evidence. Пока хотя бы одна Task остаётся `In Review`, Goal и общий execution
plan не могут считаться завершёнными: skill обязан закончить gates, выполнить
rework либо перевести terminal-ready Task в `Done`, а не ждать пользователя.
Старые memory/rollout/report записи о human acceptance являются historical
evidence и не могут вернуть ручной gate. `Acceptance criteria` в Task означают
проверяемые completion criteria; feedback после `Done` приходит через
user-initiated reopen или новую Task.

Когда native comments доступны, пользователь получает report прямо в Task:
outcome-first объяснение feature, exact evidence и полезную diagram для
non-trivial flow. Material failure получает отдельный impact/cause/recovery
analysis с уровнем уверенности и remaining risk. Пока comments недоступны,
тот же report остаётся в review/interaction output, но не сохраняется через
другие Task fields. Report не заменяет evidence, но делает его понятным decision
surface.

## Границы

- Skill не создаёт scope из неопределённого пожелания.
- Goal фиксирует и удерживает уже выбранный Task Manager scope, но не заменяет
  его и не расширяет authority.
- Skill не берёт Tasks из `Backlog` и не меняет их.
- Явно разрешённые новые Tasks создаются в `To Do`, а не в `Backlog`.
- Skill не получает внешние полномочия из одного факта invocation.
- Исключение ограничено ADR-0004: invocation заранее разрешает обычный in-scope
  non-production release workflow, но не production release.
- ADR-0005 отдельно разрешает automatic terminal acceptance после полного
  evidence, но не production/destructive/external authority.
- Skill не работает без подключённого Task Manager connector.
- Наличие connector не заменяет authoritative Project/Release scope и write
  authority конкретного проекта.
- Skill не превращает failed check в разрешение на unrelated cleanup.
- Skill не меняет Task description ради delivery report и не использует другие
  Task fields как fallback для comments.
- Skill не завершает Goal, пока повторная полная инвентаризация выбранной
  границы находит хотя бы одну Task, подходящую под рабочие критерии.
- Skill не считает deferred Task завершённой и не задаёт серию вопросов, пока
  остаётся другая runnable работа.
- Skill не называет plan, worker report, commit, test или deploy достаточным
  доказательством completion другого слоя.
