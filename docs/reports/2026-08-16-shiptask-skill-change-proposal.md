# Предложение по развитию ShipTask skill

Статус: implemented and synced to user-level skill, 2026-08-16. Нормативное решение —
[ADR-0007](../decisions/0007-delivery-policy-and-project-memory.md); этот
документ сохраняется как design rationale и Task Manager cutover checklist.

## Результат анализа

ShipTask следует сделать единственным владельцем бизнес-политики доставки
Task Manager Tasks и поддержать в нём `batch`, `single` и явное
`memory-maintenance`, отдельно распознавая `non-delivery` read/planning intent.
Реальные project-specific значения пока создавать не нужно: skill определяет
их logical contract и помогает заполнить его при первом использовании в
конкретном проекте.

Изменение нельзя ограничить включением implicit invocation. Текущий
Task Manager plugin самостоятельно исполняет одиночную Task, задаёт status
lifecycle, запрещает Goal и требует delivery reports. Пока эта бизнес-логика
остаётся во втором skill, свободная формулировка может активировать два
конкурирующих workflow. Необходим согласованный cutover с
[предложением для Task Manager skill](2026-08-16-task-manager-skill-change-proposal.md).

## Исходное состояние до реализации

- `ship-tasks/agents/openai.yaml` содержит
  `allow_implicit_invocation: false`.
- Frontmatter `ship-tasks/SKILL.md` разрешает использование только при явном
  `$ship-tasks` или прямой просьбе исполнить ShipTask workflow.
- `ship-tasks/SKILL.md` занимает 496 строк и уже находится на границе
  рекомендуемого компактного runtime context; добавлять туда полный memory
  schema и новый routing flow без декомпозиции не следует.
- Текущая specification требует обязательный Goal после exact scope и
  запрещает использовать memory как замену Task Manager scope.
- `docs/reference/task-manager-adapter.md` повторяет значительную часть
  технического adapter flow, который по целевой архитектуре должен принадлежать
  marketplace Task Manager skill.
- Global `~/.codex/AGENTS.md` отдельно дублирует single-Task delivery,
  completion reports и Task Manager release authority. После изменения skills
  этот текст продолжит навязывать старый workflow, если его не сократить.

Официальная документация OpenAI подтверждает, что skill может активироваться
явно или неявно по `description`, а `allow_implicit_invocation: false`
запрещает второй путь. Она также рекомендует держать `SKILL.md` компактным и
выносить подробности в references:
<https://learn.chatgpt.com/docs/build-skills>.

## Целевая граница ответственности

```text
user intent
   │
   ▼
ShipTask
  routing + business delivery policy + memory contract
   │                                      │
   │                                      └── project memory
   │                                          selectors and project profile
   ▼
Task Manager skill
  OAuth/MCP adapter, canonical refs, reads, writes, concurrency
   │
   ▼
live Task Manager state
```

ShipTask должен владеть:

- классификацией delivery intent и выбором execution mode;
- scope, Goal и status lifecycle policy;
- automatic terminal acceptance и report requirements;
- autonomy, defer, production/non-production authority и recovery policy;
- project-memory contract, его проверкой и явным bootstrap/update flow;
- integration, verification, external effects и completion evidence.

ShipTask не должен владеть:

- OAuth setup и конкретной схемой MCP tools;
- pagination, canonical-ref, optimistic-concurrency и comment API mechanics;
- Project/Release/Task данными конкретного проекта;
- фактическим текущим Task status/version или результатом deploy.

`agents/openai.yaml.dependencies` объявляет MCP tool dependency, но официальная
документация не описывает её как жёсткую зависимость от другого skill. Поэтому
runtime нельзя строить на недоказанном предположении, что явный `$ship-tasks`
всегда автоматически загрузит полный `task-manager/SKILL.md`. ShipTask должен
явно использовать adapter skill, когда он доступен, а до подтверждённого
cross-skill loading сохранить минимальные safety invariants: canonical refs,
current Task detail/version, no blind retry и post-write read-back. Подробный
tool procedure и capability semantics при этом всё равно принадлежат Task
Manager skill, а не копируются целиком.

## Предлагаемые invocation modes

| Intent | Режим | Scope | Goal | Mutations |
|---|---|---|---|---|
| Bare `$ship-tasks` | `batch` | `current_scope` из project memory | обязательный | после полного preflight |
| `$ship-tasks` с exact selector | `batch` или `single` по selector | текущий явный selector выше memory default | по выбранному режиму | после полного preflight |
| «выполни/исправь/доведи TM-123» | `single` | ровно одна canonical Task | рекомендуется без Goal | разрешённый single-Task lifecycle |
| «доведи текущий release/project» | `batch` | selector из prompt либо project memory | обязательный | после полного preflight |
| «настрой ShipTask для этого проекта» | `memory-maintenance` | текущий проект | нет | только явное memory update |
| list/read/status/planning/backlog capture | не delivery | только запрос пользователя | нет | только явно запрошенные Task Manager writes |

Рекомендуемое решение для первой реализации: оставить Goal обязательным только
для batch mode. Single-Task mode использует ту же acceptance, report, release
и terminal policy, но не создаёт Goal. Это сохраняет простой on-demand flow и
не превращает каждую короткую задачу в long-running orchestration. Если нужна
полная унификация Goal lifecycle, это должно быть принято отдельным изменением
specification до реализации.

## Разрешение scope

Использовать следующий порядок, не расширяя scope молча:

1. Точный selector из текущего запроса пользователя.
2. Для bare `$ship-tasks` — `current_scope` из project memory, однозначно
   сопоставленной текущему repository/project identity.
3. Live-разрешение сохранённых Project/Release/Task selectors через Task
   Manager adapter.
4. Complete live inventory и полный current Task detail до mutation.

Memory хранит selector, но не список фактически активных Tasks по умолчанию.
Обычный `current_scope.mode = live-query` означает: Project/Release boundary
сохраняется, а Task set каждый run получается заново до `hasMore=false`.
Опциональный `fixed` mode может хранить exact Task refs, но каждая Task всё
равно перечитывается live.

При отсутствии однозначного memory profile, несовпадении repository identity,
устаревшем selector или конфликте с live connector выдать
`TASK CONTEXT ALARM` до code, Git, Task Manager, Goal и external writes.

## Project-memory contract

В `ship-tasks/references/project-memory.md` следует определить логическую, а не
физическую файловую схему. Минимальный профиль:

```yaml
project:
  identity: stable project name or id
  repository_identity: canonical local/remote identity

current_scope:
  mode: live-query | fixed
  project_selector: optional
  release_selector: optional
  task_selectors: optional

integration:
  target_branch: project-defined
  isolation_policy: project-defined

verification:
  targeted_checks: project-defined
  aggregate_checks: project-defined
  review_triggers: project-defined

environments:
  targets: project-defined
  classification_sources: repository config or provider state
  smoke_and_recovery: project-defined

effects_and_authority:
  required_effects: project-defined
  project-specific approval boundaries: project-defined

provenance:
  sources: paths or provider surfaces
  last_verified_at: timestamp
```

Это semantic schema для извлечения контекста, а не требование вручную править
generated memory files. Skill должен:

1. Найти memory profile именно текущего проекта.
2. Проверить обязательные поля, provenance, freshness и противоречия.
3. Получить дешёвые drift-prone факты из live config/provider перед эффектом.
4. Показать недостающие поля и предложенный memory update.
5. Выполнить update только по явной просьбе пользователя и через доступный
   memory control; не обещать немедленную background consolidation.
6. Перепроверить доступный результат либо честно указать pending memory update.

Memories нельзя использовать как единственный источник обязательной
бизнес-политики: они могут быть выключены, не попасть в конкретный chat или
обновиться с задержкой. Обязательные общие правила остаются в ShipTask; memory
содержит project-specific selectors и профиль. Это соответствует официальному
описанию Memories как recall layer, а не единственного источника required
guidance: <https://learn.chatgpt.com/docs/customization/memories>.

Local Codex memories также не являются общей памятью ChatGPT web/Work. Первая
итерация должна явно считать этот flow local Codex/Desktop/CLI/IDE contract.
Cross-surface project context потребует отдельного общего source или connector
capability и не входит в это изменение.

## Что обновить в ShipTask repository

После принятия proposal выполнить изменения в таком порядке:

1. **Canonical specification** — обновить `docs/specs/ship-tasks.md` первой:
   добавить invocation modes, scope precedence, single-Task semantics, memory
   contract, missing-memory alarm и mode-specific Goal lifecycle.
2. **Architecture decision** — добавить один accepted ADR о разделении
   adapter/business/project-context и implicit routing. Не создавать вторую
   параллельную specification.
3. **Runtime skill** — сократить `ship-tasks/SKILL.md` до core router и
   обязательных invariants. Вынести memory details и mode-specific procedure в
   одноуровневые references.
4. **Memory reference** — добавить `ship-tasks/references/project-memory.md` с
   schema, lookup, validation, bootstrap, update и freshness rules.
5. **Invocation metadata** — изменить description так, чтобы оно front-load-ило
   delivery triggers и исключало read-only/planning/backlog-capture intents;
   установить `allow_implicit_invocation: true` и обновить UI metadata/default
   prompt.
6. **Adapter duplication** — сократить
   `docs/reference/task-manager-adapter.md` до required compatibility contract:
   необходимые capabilities и ShipTask expectations. Точный MCP procedure
   считать source of truth Task Manager skill; минимальные defensive write
   invariants оставить в ShipTask до доказанного cross-skill loading.
7. **Overview/navigation** — обновить `docs/overview.md` и `docs/README.md` после
   изменения действующего contract.
8. **Validators/evals** — добавить проверки новых metadata/reference links и
   trigger matrix. Установленную user-level копию синхронизировать только по
   отдельному явному запросу и затем byte-verify.

Candidate frontmatter description должен быть компактнее текущего и отвечать
за routing, например:

```yaml
description: >-
  Доставлять существующие Task Manager Tasks по бизнес-политике ShipTask.
  Использовать явно через $ship-tasks для полного выбранного/current project
  scope и неявно для запросов выполнить, исправить, завершить или доставить
  точную Task, Project либо Release. Разрешать scope через project memory и
  live Task Manager, применять verification, reports, release authority и
  terminal lifecycle. Не запускать delivery для чтения, планирования или
  backlog capture.
```

## Routing и regression matrix

До cutover проверить минимум такие prompts в свежих chats:

| Prompt | Ожидаемый результат |
|---|---|
| `$ship-tasks` | Batch current memory scope, complete live inventory, Goal |
| `Выполни TM-123` | ShipTask single mode, ровно одна Task, без Goal по рекомендации |
| `Исправь эту задачу` с одной однозначной Task | ShipTask single mode |
| `Доведи текущий релиз` | ShipTask batch mode по memory selector |
| `Покажи TM-123` | Read-only Task Manager adapter, без delivery mutations |
| `Какие задачи в релизе?` | Read-only adapter, без Goal |
| `Просто добавь это в backlog` | Planning write, не delivery flow |
| `Исследуй проблему в TM-123` | Read-only по умолчанию, если execution явно не разрешён |
| Bare `$ship-tasks` без memory profile | `TASK CONTEXT ALARM`, zero mutations |
| Memory selector расходится с live Project/Release | Alarm или явное reconciliation, без догадки |
| Task уже terminal | Не reopen без явного запроса |
| Production нужен, но не разрешён | Без production effect; mode-specific blocker flow |

Проверять не только хороший outcome, но и какой skill был загружен, был ли
создан Goal, какие Task Manager writes произошли и не активировался ли второй
delivery owner. Отдельно проверить explicit `$ship-tasks`: доступен ли ему
adapter contract, когда пользователь не упомянул `$task-manager`.

## Cutover

Изменения ShipTask и marketplace Task Manager skill нужно подготовить отдельно,
но активировать согласованно:

1. Реализовать и проверить ShipTask source без преждевременной синхронизации
   user-level copy.
2. Подготовить adapter-only Task Manager plugin release.
3. Удалить дублирующую business policy из global `~/.codex/AGENTS.md`, оставив
   только короткий routing rule и действительно глобальные safety boundaries.
   `AGENTS.md` загружается до начала работы, поэтому старый текст иначе будет
   продолжать влиять на flow:
   <https://learn.chatgpt.com/docs/agent-configuration/agents-md>.
4. Синхронизировать ShipTask, обновить/reinstall Task Manager plugin и начать
   свежий chat, чтобы исключить stale skill/tool snapshot.
5. Выполнить routing/regression matrix до первой реальной delivery.

## Acceptance criteria будущего изменения

- Bare `$ship-tasks` детерминированно разрешает current project memory scope и
  выполняет все текущие qualifying Tasks этого live boundary.
- Natural-language delivery одной Task использует ShipTask policy без явного
  имени skill и не расширяет scope.
- Read-only, planning и backlog capture не запускают delivery.
- ShipTask может проверить и по явному запросу помочь сформировать project
  memory profile, но не хранит project-specific значения в skill.
- Missing, stale или conflicting memory не приводит к guessed mutations.
- Task Manager остаётся единственным live task source; memory не подменяет Task
  detail/status/version.
- В runtime нет двух владельцев Goal, status lifecycle, reports или release
  policy.
- Current production/destructive/secret/privacy/external authority boundaries
  не ослаблены.

## Вне scope этого proposal

- Создание project memory для конкретного проекта.
- Изменение Task Manager MCP/backend, OAuth или Sites endpoint.
- Production deploy любого приложения.
- Cross-surface memory service для ChatGPT web/Work.
- Синхронизация installed ShipTask copy или публикация marketplace release.
