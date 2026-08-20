# Обзор ShipTask

## Назначение

ShipTask — Task Manager-only business delivery policy для выбранного task scope.
Она активируется явным `$ship-tasks` и natural-language delivery только при
однозначном Task Manager anchor: exact Task либо уже выбранном
Project/Release/current scope. Один delivery verb и обычная просьба исправить
код/продукт/plugin без такого anchor недостаточны. Обычно scope уже существует;
составная команда явно создать ровно одну Task в Task Manager и сразу выполнить
её создаёт exact `single` scope и продолжает delivery. Skill разрешает Project,
Release и Tasks через connector, читает полный Task detail, проверяет
dependencies и authority и координирует execution, integration, verification,
automatic acceptance и terminal status projection.

Есть четыре intent mode: `single` для одной exact Task без Goal, включая
`create-and-deliver`, `batch` для
нескольких Tasks/Project/Release с обязательным Goal, `memory-maintenance` для
явного оформления project context и `non-delivery` для чтения/планирования.
Bare `$ship-tasks` всегда запускает batch по `current_scope` из project memory.

Конкретные Project/Release selectors, repository commands, branches,
environments и внешние эффекты определяются project memory и проверяются по
current live sources. Global конфликт connector/exact scope/applicable
Goal/shared authority останавливает run с
`TASK CONTEXT ALARM`; изолированный вопрос по одной Task откладывает только её.

```text
Task Manager skill  = technical adapter
ShipTask skill      = business delivery policy
Project Memories    = scope selectors + project-specific profile
Strategic Explainer = fresh user-language adaptation, no decisions
```

## Текущий статус

- [Ship Tasks](specs/ship-tasks.md) — единственная каноническая specification.
- [Strategic Explainer: стратегическое видение](strategic-explainer.md) —
  стабильная продуктовая цель и quality bar независимо от implementation.
- [Strategic Explainer](specs/strategic-explainer.md) — отдельная каноническая
  specification общего Technical Brief → User Brief contract.
- [ADR-0007](decisions/0007-delivery-policy-and-project-memory.md) — принятое
  разбиение adapter / delivery policy / project memory и implicit routing.
- `ship-tasks/SKILL.md` — компактный исполнимый contract на её основе.
- `strategic-explainer/SKILL.md` — generic runtime contract, который можно
  применять напрямую или внутри свежего субагента другого workflow.
- `ship-tasks/references/project-memory.md` — логическая схема, bootstrap,
  freshness, precedence и alarm contract project memory.
- [Task Manager adapter](reference/task-manager-adapter.md) — точный OAuth/MCP
  tool flow, identity, status и write semantics.
- Каждый `batch` после разрешения exact scope и до первой non-Goal mutation
  создаёт Goal либо продолжает уже активный совместимый Goal. `single` Goal не
  создаёт. Несовместимый незавершённый Goal блокирует только новый batch с
  `TASK CONTEXT ALARM`.
- Prompt selector имеет приоритет над memory default, но не переписывает его.
  Task status/detail/version всегда перечитываются из Task Manager.
- Memory обновляется только по явной просьбе пользователя; delivery-run может
  предложить обновление, но не выполняет его молча.
- Cross-session scheduler, durable claims и отсутствующие connector capabilities
  не изображаются существующими.
- Delivery report публикуется только как native Task comment и является
  обязательным terminal effect. Без comment write/read-back affected Task
  остаётся non-terminal с явным blocker; `description` не меняется.
- Перед любым terminal outcome агент выполняет finalization pass: сверяет
  обещанный и фактический результат, объясняет material gaps, выполняет
  доступный safe in-scope recovery и перечитывает affected state. Blocker
  остаётся blocker до устранения; пока meaningful progress возможен, финальный
  Goal status `blocked` ещё не обоснован. Каждый terminal exit заканчивается
  глубоким компактным `SHIPTASK RUN REPORT`, который Task comments не заменяют.
- Material partial/blocked handoff, запрос user action/authority и сложный
  technical terminal result проходят через свежий субагент с общим
  `$strategic-explainer`: он превращает ограниченный Technical Brief в понятный
  User Brief, но не выбирает status, recovery или следующий action.
- Пока существует runnable work, skill не прерывает run task-local вопросами:
  безопасный default выбирается автоматически, сложная Task попадает в decision
  queue, а остальные продолжаются. Каждый defer обязательно получает
  опубликованный и перечитанный `BLOCKED` handoff; иначе comment delivery
  остаётся частью blocker.
- Dev/test/QA/UAT/staging/preview/sandbox releases автоматически разрешены в
  границах exact Task и проверенного non-production target. Production release
  выполняется только по явному user approval; без него Task откладывается.
- Terminal-ready result автоматически принимается и переводится в `Done` без
  вопроса пользователю. Если позже обнаружен bug, пользователь reopen-ит Task
  либо создаёт новую проблему для следующего ShipTask scope.
- Marketplace runtime и installed cache обоих sibling-skills должны быть
  byte-identical repository source; standalone user-level копии отсутствуют.

## Целевой продуктовый поток

```text
Backlog                           excluded intake
  └─ exact just-created Task → To Do   create-and-deliver only
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

Число Tasks в `In Progress` не является размером будущего review batch.
Последовательный run без реально запущенных isolated workers имеет одну active
write lane: до старта следующей `To Do` предыдущая targeted-verified и
интегрированная Task обязана перейти в `In Review` с read-back. Общий commit,
UAT, full gate или обязательный completion comment выполняются batch cadence,
но не разрешают накапливать завершённые candidates в `In Progress`.

Любой классифицированный ShipTask delivery intent разрешает automatic acceptance
после полного terminal evidence. Пока хотя бы одна Task остаётся `In Review`,
применимый batch Goal и общий execution plan не могут считаться завершёнными:
skill обязан закончить gates, выполнить rework либо перевести terminal-ready
Task в `Done`, а не ждать пользователя.
Старые memory/rollout/report записи о human acceptance являются historical
evidence и не могут вернуть ручной gate. `Acceptance criteria` в Task означают
проверяемые completion criteria; feedback после `Done` приходит через
user-initiated reopen или новую Task.

Пользователь получает report прямо в Task: outcome-first объяснение feature,
exact evidence и полезную diagram для non-trivial flow. Material failure
получает отдельный impact/cause/recovery analysis с уровнем уверенности и
remaining risk. Если report нельзя опубликовать и перечитать, workflow не
маскирует gap другим Task field и не завершает Task. Report не заменяет
evidence, но является обязательной durable review surface.

## Границы

- Один delivery verb не является implicit invocation. Project memory и Task
  Manager lookup не используются, чтобы придумать anchor для обычной code/
  product/plugin просьбы.
- Skill не создаёт scope из неопределённого пожелания.
- Batch Goal фиксирует и удерживает уже выбранный Task Manager scope, но не
  заменяет его и не расширяет authority. Single-task delivery Goal не создаёт.
- Project memory помогает выбрать scope и project profile, но не заменяет live
  Task Manager state и не меняется без явной просьбы.
- Skill не берёт pre-existing Tasks из `Backlog` и не меняет их.
- `Create-and-deliver` создаёт exact Task в `To Do`; если adapter вернул только
  что созданную Task в `Backlog`, skill выводит только её в `To Do`, завершает
  preflight и переводит в `In Progress` до implementation.
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
- Skill не завершает batch Goal, пока повторная полная инвентаризация выбранной
  границы находит хотя бы одну Task, подходящую под рабочие критерии.
- Skill не считает deferred Task завершённой и не задаёт серию вопросов, пока
  остаётся другая runnable работа.
- Skill не называет plan, worker report, commit, test или deploy достаточным
  доказательством completion другого слоя.
