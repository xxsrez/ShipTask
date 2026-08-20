# Ship Tasks

Статус: current contract, 2026-08-18.

Документ описывает единственную business delivery policy ShipTask для явного
`$ship-tasks` и подходящих natural-language запросов. Исполнимый
`ship-tasks/SKILL.md` является компактной procedural-формой этой specification.

## 1. Результат и граница

Skill должен довести выбранный scope Task Manager Tasks до одного проверенного
terminal outcome. Он применяется при явном `$ship-tasks` и неявно только когда
текущий запрос одновременно содержит delivery intent и однозначный Task
Manager delivery anchor: exact существующую Task, явно выбранный
Project/Release/current scope либо explicit create-and-deliver ровно одной
новой Task. Обычная просьба исправить продукт, код, repository или plugin без
такого anchor не относится к ShipTask, даже если использует delivery verb.

Обычно scope уже существует и задаётся одной или несколькими Tasks, Project
либо Release. Составная команда явно создать ровно одну Task именно в Task
Manager и сразу начать или выполнить её сама разрешает создать этот exact scope
и продолжить в `single` mode; она не является backlog capture. Неопределённая
идея и один delivery verb сами по себе scope не создают.

Pre-existing `Backlog` остаётся intake-зоной вне рабочего scope ShipTask: skill
не берёт такие Tasks в работу и не меняет их status или content. Узкое
исключение — exact Task, только что созданная самим workflow из текущего
`create-and-deliver` intent: если adapter вернул её в `Backlog`, workflow обязан
вывести эту Task из intake и продолжить delivery. Это исключение не разрешает
выбирать или менять другие Backlog Tasks.

### 1.1 Слои ответственности

```text
user intent
   ↓
ShipTask: routing + business delivery policy + memory contract
   ├── project memory: selectors + project-specific profile
   ├── Task Manager adapter: connector mechanics + live task state
   └── Strategic Explainer: fresh user-language adaptation, no decisions
```

- Task Manager skill владеет техническим adapter contract: connection,
  capabilities, canonical refs, pagination, reads/writes, optimistic
  concurrency, comment operations и post-write read-back.
- ShipTask владеет классификацией delivery intent, scope/Goal/lifecycle policy,
  automatic acceptance, reports, autonomy, release boundaries, verification и
  completion evidence.
- Project memory хранит `current_scope` и project-specific profile: repository,
  branches, commands, environments, external effects, recovery и authority
  hints. Логическая схема задана в
  [project-memory reference](../../ship-tasks/references/project-memory.md).
- Task Manager остаётся единственным authority для текущих Task detail, status,
  `version`, relations, comments и access. Memory никогда их не заменяет.
- Strategic Explainer получает только ограниченный `Technical Brief` и
  возвращает свободное стратегическое объяснение по
  [собственной specification](strategic-explainer.md). Он не владеет evidence,
  scope, lifecycle, status, recovery или authority и не подменяет решения
  ShipTask.

### 1.2 Invocation gate и классификация execution mode

До чтения project memory, обращения к Task Manager adapter, создания Goal или
других scope-changing/delivery mutations проверить invocation gate.

Явный `$ship-tasks` всегда является достаточным invocation anchor. Для
implicit invocation одновременно обязательны delivery intent и ровно один
однозначный Task Manager delivery anchor, уже присутствующий в текущем запросе
или выбранном Task Manager context:

- exact существующая Task, названная canonical identifier/ref вроде `TM-123`
  либо иначе однозначно выбранная как Task Manager Task;
- явно выбранный Task Manager Project, Release или current scope, для которого
  пользователь просит выполнить delivery;
- explicit create-and-deliver: пользователь в одном запросе просит создать
  ровно одну Task именно в Task Manager и сразу начать или выполнить её.

Явная настройка ShipTask project memory остаётся отдельным
`memory-maintenance` trigger. Project memory и adapter lookup можно использовать
для разрешения уже прошедшего gate, но нельзя читать их, чтобы задним числом
превратить обычную просьбу исправить код/продукт/plugin в Task Manager scope.
Текущий repository, software project, code task или release target не являются
Task Manager Project/Release/current scope без такого контекста.

Если gate не пройден, ShipTask не активируется: выполнить обычный запрос его
прямым workflow и не вызывать Task Manager/Goal tools от имени ShipTask. После
успешного gate классифицировать запрос до mutations:

| Intent | Mode | Scope source | Goal |
|---|---|---|---|
| Bare `$ship-tasks` | `batch` | `current_scope` из project memory | обязательный |
| `$ship-tasks` с exact Task | `single` | prompt selector | нет |
| `$ship-tasks` с несколькими Tasks, Project или Release | `batch` | prompt selector | обязательный |
| «выполни/исправь/доведи TM-123» | `single` | ровно одна canonical Task | нет |
| «создай ровно одну Task в Task Manager и сразу начни/выполни её» | `single` (`create-and-deliver`) | exact новая Task в явно выбранном Project/Release | нет |
| «доведи выбранный Task Manager release/project/current scope» | `batch` | выбранный context, затем project memory | обязательный |
| «настрой/обнови ShipTask memory» | `memory-maintenance` | текущий project context | нет |
| list/read/status/audit/planning/backlog capture | `non-delivery` | exact user request | нет |

Один delivery verb недостаточен для implicit invocation и не отменяет явный
read-only/local-only/no-deploy boundary.
Фразы «просто добавь», «положи в backlog», «запланируй» создают или уточняют
planning scope только когда это явно разрешено; они не запускают delivery,
не меняют status существующей Task и не требуют delivery report.

Явная комбинация Task Manager create intent с execution intent — например,
«создай ровно одну Task в Task Manager и начинай делать» — является `single`
delivery. Не переклассифицировать её в planning/backlog capture после
`create_task` и не завершать flow только потому, что default status созданной
Task оказался `Backlog`. Команда лишь создать или описать Task без execution
intent остаётся `non-delivery`. Просьба создать и выполнить сущность, не
названную Task Manager Task, не является ShipTask create-and-deliver.

`single` требует ровно одну canonical Task до implementation. Для обычного
single её разрешить из current Task Manager state. Для `create-and-deliver`
сначала разрешить exact Project/Release, Task content, acceptance и write
authority, создать ровно одну Task, получить её canonical ref/read-back и
считать только её выбранным scope. При нуле или нескольких совпадениях обычного
single остановиться до mutation; не выбирать и не создавать замену. Уже terminal
Task не reopen-ить и не выполнять заново без явной просьбы.

`batch` охватывает несколько Tasks либо динамическую Project/Release boundary.
Bare `$ship-tasks` всегда является предсказуемым batch-run текущего memory
scope. Exact selector из текущего prompt имеет приоритет над memory default,
но не переписывает memory.

`memory-maintenance` читает project sources, помогает сформировать структуру и
пишет memory только по явной просьбе пользователя. Обычный delivery-run не
обновляет memory как побочный эффект.

### 1.3 Проверяемая trigger matrix

Эта matrix является regression contract для discovery description, runtime
gate, repository validator и fresh-session behavioral smoke:

| Prompt | ShipTask activation | Mode/result |
|---|---|---|
| `$ship-tasks` | да | `batch` по memory `current_scope` |
| `Выполни TM-123` | да | `single` для exact существующей Task |
| `Доведи выбранный Task Manager Project Alpha` | да | `batch` выбранного Project |
| `Выпусти выбранный Task Manager Release 0.2` | да | `batch` выбранного Release |
| `Доведи текущий Task Manager scope` | да | `batch` уже выбранного current scope |
| `Создай ровно одну Task в Task Manager: исправить импорт, и сразу начни выполнять её` | да | `single create-and-deliver` |
| `Почини X сейчас` | нет | обычная реализация без Task Manager scope |
| `Исправь баг в plugin` | нет | обычная реализация без Task Manager scope |
| `Реализуй это изменение в коде` | нет | обычная реализация без Task Manager scope |
| `Покажи статус TM-123` | нет | read-only Task Manager adapter |
| `Проведи аудит TM-123` | нет | read-only Task Manager adapter |
| `Создай Task в Task Manager` | нет | planning/write через adapter, без delivery flow |
| `Просто добавь это в backlog` | нет | backlog capture, без delivery flow |

До первой мутации необходимо установить:

- exact Task refs и terminal criteria; для `create-and-deliver` до create —
  exact parent scope, Task fields и criteria, а canonical ref/`version` — сразу
  после create read-back;
- полный Task detail: description, acceptance, dependencies, relations,
  lifecycle, access и current concurrency field `version`;
- Project/Release membership и boundary dependencies;
- repository/workspace, integration policy и разрешённые writes;
- per-Task targeted gate, периодический review-batch gate и их trigger policy;
- обязательные external effects и способ их независимо проверить;
- exact release targets, их verified environment class и recovery/smoke policy;
- native Task comment create/list capability и authority, необходимые для
  обязательного terminal delivery report и read-back;
- hard automatic-terminal policy этого workflow и evidence, достаточный для
  terminal transition;
- отдельно — действительно внешние approval gates, которые нельзя заменить
  automatic acceptance, включая production release authority;
- execution mode; для batch — capacity, review WIP limit и batch target.

В `batch` mode после read-only разрешения exact scope, но до code, Git,
Task Manager, ownership и external writes необходимо сформировать обязательный
workflow Goal по правилам раздела 5. В `single`, `memory-maintenance` и
`non-delivery` Goal не создавать и не проверять. Невозможность создать или
продолжить обязательный batch Goal является `TASK CONTEXT ALARM`, а не
разрешением выполнять batch без Goal.

Поле Task `version` является optimistic-concurrency данными Task Manager, а не
версией skill или workflow.

Если connector, exact scope, обязательный batch Goal, ownership,
integration/shared state или authority неоднозначны так, что любая оставшаяся
мутация небезопасна, остановиться с global `TASK CONTEXT ALARM`. Изолированную
неопределённость одной Task обрабатывать как `deferred` по разделу 5.4 и
продолжать остальные.

## 2. Единственный task source

Task Manager является единственным authoritative live task source. Не
использовать fallback provider, repository TODO list, plan, Goal, chat
transcript или memory как замену current Task Manager inventory/detail.

Обязательный batch Goal фиксирует выполнение уже разрешённого Task Manager
scope и его критерии выхода, но не создаёт новый scope, не расширяет authority
и не подменяет current connector evidence.

Project memory может предложить Project/Release/Task selectors, repository
commands, branches, environments и completion profile, но каждый selector
разрешается заново через current adapter. Приоритет: exact selector текущего
prompt, затем memory `current_scope`, затем live canonical lookup, затем
complete inventory/detail. Конфликт не объединять молча. Наличие OAuth
connection не доказывает authority на конкретный Project, Release или Task.

Если обязательный memory context отсутствует, не загружен, неоднозначен,
устарел или противоречит current evidence до mutation, остановиться с
`TASK CONTEXT ALARM`. Local Codex memory и память другой ChatGPT/Work surface не
считать автоматически синхронизированными.

Если Task Manager tools недоступны, запросить подключение plugin через native
OAuth Connect. Не просить personal token. При недостаточном write scope
запросить reconnect с task-write access.

## 3. Connector workflow

### 3.1 Orientation

1. Вызвать `get_workspace` и проверить signed-in user, `capabilities.read`,
   `capabilities.writeTasks` и status catalog.
2. Разрешить названный Project через `list_projects`; вызвать `get_project`,
   когда нужны releases, counts, access или workflow statuses.
3. Разрешить Release через `list_releases`; перед combined filter вызвать
   `get_release` и проверить принадлежность выбранному Project.
4. Использовать только canonical refs из connector. Не строить refs из display
   names и не подставлять сохранённый ref без current lookup, если scope мог
   измениться.

### 3.2 Inventory и detail

1. Вызвать `list_tasks` с exact `projectRef`, `releaseRef` и другими filters.
   Оба scope refs можно опустить только для явно выбранного all-accessible
   scope.
2. Продолжать по `nextCursor`, пока `hasMore=false`, когда нужен полный Project,
   Release или другой multi-task scope. Первую страницу и counts не считать
   complete inventory.
3. По status отделить рабочие кандидаты `To Do`, `In Progress` и `In Review` от
   исключённого `Backlog` и terminal statuses. Для pre-existing `Backlog` читать
   только минимальные данные, необходимые для классификации, dependency boundary
   и отчёта; не выполнять и не изменять такую Task. Единственное исключение —
   post-create read-back exact Task текущего `create-and-deliver` flow по
   разделу 3.3.
4. До execution или dependency reasoning вызвать `get_task` для каждого
   рабочего кандидата.
5. Вызвать `get_task_external_context` только когда provenance сообщает о
   контексте и imported comments, attachments или branch metadata материальны
   для acceptance.
6. Перечитать связанные boundary Tasks, когда их status определяет ready
   frontier или completion.
7. При проверке Task разрешить duplicate cluster по relation type
   `duplicate_of`: исходящая relation ведёт от duplicate к canonical Task, а
   входящие relations canonical Task перечисляют её duplicates. Прочитать
   canonical Task и полный detail всех её входящих duplicates. Использовать их
   description, acceptance и материальный external context как дополнительные
   review scenarios, но не выполнять duplicates как отдельную работу.

### 3.3 Writes

- Перед каждым `update_task` вызвать `get_task` и передать current `version`.
- Использовать status ref из `availableStatuses` Task либо проверенного
  Project/Release detail.
- Не передавать `null` для `projectRef`, `releaseRef` или `dueDate`, если
  очистка поля не была явно разрешена.
- При `version_conflict` перечитать Task и повторить update только если intent
  всё ещё применим. Не перетирать unrelated newer edits.
- После write перечитать Task и проверить фактические status, fields и новую
  `version`.
- ShipTask delivery intent не разрешает менять `description` ради report.
  Delivery report можно создать только через доступный native Task comment
  write; другие Task fields не являются fallback.
- Тот же delivery intent разрешает task-specific delivery-report comment только для
  рабочей in-scope Task и только по contract раздела 9.1. Он не разрешает
  произвольные comments или writes в unrelated/duplicate/terminal Tasks.
- Не повторять `create_task` вслепую после неизвестного network outcome:
  сначала искать возможный duplicate.
- Использовать `create_task` только для explicit `create-and-deliver` intent
  ровно одной новой Task либо когда пользователь или project policy отдельно
  разрешили создать defect Task. Создание не разрешает расширять scope другой
  работой.
- Для `create-and-deliver` до create разрешить exact parent scope, содержимое,
  acceptance, terminal criteria, write authority и current status catalog.
  Запросить создание сразу со status `To Do`, используя current canonical ref,
  затем выполнить canonical Task read-back.
- Если adapter всё же вернул только что созданную exact Task в `Backlog`, не
  применять к ней общий backlog-exclusion как повод остановить delivery.
  Перечитать Task/current `version`, перевести только её в current `To Do` и
  перечитать результат. Не переводить никакую pre-existing или похожую Backlog
  Task.
- После post-create full detail и успешного preflight перевести созданную Task
  из `To Do` в `In Progress`, перечитать её и только затем начинать
  implementation. Если exact Task нельзя безопасно создать, вывести из
  `Backlog`/`To Do` или подтвердить read-back, остановить affected single flow и
  не утверждать, что execution начался.

## 4. Lifecycle projection

Task Manager status category помогает интерпретации, но не заменяет evidence:

| Task Manager status | Category | ShipTask interpretation |
|---|---|---|
| `Backlog` | `backlog` | Исключённый intake. Не брать в работу, не проверять как candidate и не изменять; единственное исключение — вывести exact Task, только что созданную текущим `create-and-deliver` flow. |
| `To Do` | `unstarted` | Единственная точка входа для новой работы; после preflight это `ready`. |
| `In Progress` | `started` | Работа уже идёт; продолжать только из coherent checkpoint и с подтверждённой authority. |
| `In Review` | `started` | Targeted-verified candidate уже предъявлен; он ждёт batch gate, required effects или terminal reconciliation, но не ручную приёмку. Проверять exact candidate, evidence и все связанные duplicates. |
| `Done`, `Finished` и аналоги | `completed` | Terminal projection; не создаёт работу, но может участвовать в reconciliation. |
| `Canceled` и аналоги | `canceled` | Terminal outcome; не выполнять и не считать successful completion. |
| `Duplicate` | `canceled` | Отдельной работы не требует; читать как review context связанной основной Task. |

Category используется как fallback для terminal statuses с другими display
names. Для рабочих состояний status name и его current canonical ref должны
соответствовать проверенному catalog.

Нормативная status-проекция:

```text
Backlog                         (excluded; no pre-existing Task transition)
  └─ exact just-created Task → To Do   (`create-and-deliver` recovery only)
To Do → In Progress → In Review → Done
                         └──────→ Canceled
Duplicate                       (terminal review context, no own execution)
```

Нормативный task flow:

```text
planned
→ ready
→ running
→ task-verified
→ In Review / batch-candidate
→ batch-verified / terminal-ready
→ automatically accepted
→ terminal
```

Возврат на доработку:

```text
In Review / batch-candidate
→ changes-requested
→ rework
→ task-verified
→ In Review / batch-candidate
```

При changes requested вернуть Task из `In Review` в `In Progress`, выполнить
rework и только после повторных checks снова перевести в `In Review`. При
ограниченной capacity сохранять lane за этой review/rework chain до повторного
review или blocker; не переключаться на другую `In Progress` только из-за
смены status.
Переводить `To Do` в `In Progress` только после успешного preflight и получения
write authority. Для `create-and-deliver` этот переход и его read-back должны
произойти до implementation: созданная в `To Do` Task не является завершением
составной команды. Переводить в `In Review` только exact candidate с passing
targeted gate и candidate evidence. Переводить в `Done` только после passing
review-batch gate, выполнения Task acceptance criteria, integration и
обязательных effects. При полном evidence workflow автоматически принимает
result и переводит Task в `Done`; отдельное подтверждение пользователя не
требуется. До `Done` обязательно опубликовать и перечитать native `COMPLETED`
report. Отсутствующий, failed или unreconciled comment write оставляет Task в
`completion-remains`/`deferred` и блокирует её terminal transition.
`Canceled` использовать только при подтверждённом canceled outcome. Один status
никогда не доказывает другой evidence layer.

## 5. Batch Goal lifecycle и общая preflight disposition

### 5.1 Обязательный Goal только для batch

`batch` mode разрешает создание одного workflow Goal для выбранного scope.
`single`, `memory-maintenance` и `non-delivery` не вызывают `get_goal`,
`create_goal` или `update_goal`. После разрешения exact canonical refs и
complete read-only inventory batch, но до первой non-Goal mutation:

1. Проверить доступность `get_goal` и `create_goal`. При отсутствии обязательной
   Goal capability остановиться с `TASK CONTEXT ALARM` до любых non-Goal
   mutations. Вызвать `get_goal` и проверить current model-visible Goal state.
2. Если незавершённого Goal нет, вызвать `create_goal` без token budget, если
   пользователь отдельно не указал положительный numeric budget.
3. Если уже существует незавершённый Goal, продолжить его только когда его
   objective и done criteria однозначно относятся к тому же exact scope и
   terminal outcome. Иначе остановиться с `TASK CONTEXT ALARM`; не завершать,
   не блокировать и не заменять чужой или несовместимый Goal ради запуска.
4. После создания или reuse проверить, что Goal активен до execution. Если
   совместимый Goal существует, но не активен и его нельзя возобновить текущим
   tool contract, запросить resume через доступный client control и остановить
   execution до подтверждения.

Goal должен содержать:

- `Objective`: довести exact выбранные Tasks либо текущие подходящие Tasks
  выбранного Project/Release scope до проверенного terminal outcome;
- `Done when`: повторная complete inventory не находит `To Do`, `In Progress`,
  `In Review`, changes-requested/rework, completion remnants или unresolved
  in-scope defects, нет deferred decision/authority queue, обязательные Task
  comments опубликованы и перечитаны для изменённых Tasks и требования раздела
  11 выполнены;
- `Verify with`: current Task details/statuses, source/integration identity,
  per-Task targeted gates, exact review-batch gate, automatic acceptance record
  и independently verified external effects;
- `Constraints`: точная граница scope, исключённый `Backlog`, разрешённые writes
  и запрет расширять scope либо authority из самого Goal;
- `Blocked when`: после исчерпания runnable work остаётся конкретная
  decision/authority queue либо общая внешняя зависимость, без ослабления
  текущего tool threshold для статуса `blocked`.

Batch Goal остаётся активным, пока хотя бы одна Task в выбранной границе подходит под
рабочие критерии ShipTask. `Backlog` и terminal statuses сами по себе не держат
Goal активным, но могут оставаться dependency boundary. `global-conflict`,
`deferred` или временное отсутствие ready frontier не являются completion и не
разрешают закрыть Goal, если подходящие Tasks либо completion remnants ещё
существуют.
Статус `blocked` допустим только после текущего строгого blocker threshold и
finalization pass с понятным пользователю объяснением по разделу 9.3. Blocker
остаётся blocker до устранения; доступный safe in-scope recovery не отменяет
его, но означает, что meaningful progress ещё возможен и terminal Goal
`blocked` пока не обоснован. Агент обязан выполнить recovery, перечитать
affected state и повторить finalization. Один reason code, raw error или status
write без понятного объяснения, recovery evidence и exact resume condition
недопустимы.
Повторное чтение того же state не создаёт новый blocker occurrence. `blocked`
оставляет Goal незавершённым, а после resume workflow продолжается с тем же
Goal и scope.

Для явно перечисленных batch Task refs граница фиксирована этими refs и отдельно
разрешёнными in-scope defects. Для Project, Release или all-accessible scope
перед terminal claim повторить `list_tasks` по всем страницам до
`hasMore=false`: новая или изменившая status Task внутри той же границы должна
удерживать Goal активным, если она теперь подходит под рабочие критерии.

### 5.2 Preflight disposition

До execution выбрать ровно одну disposition:

| Disposition | Значение |
|---|---|
| `work-remains` | Есть `To Do` Tasks, прошедшие или способные пройти preflight. |
| `completion-remains` | Есть `In Review` либо implementation/rework уже завершены, но result ещё не terminal-qualified, не интегрирован, не отражён в Task Manager или не доведён до обязательного effect. |
| `resume` | Есть `In Progress` с незавершённым implementation/rework, найден coherent checkpoint и доказана authority продолжения. |
| `deferred` | Конкретная Task безопасно изолирована, но требует material decision, отсутствующей authority либо внешнего state change; в текущем run её не переизбирать без нового evidence. |
| `no-work` | После исключения `Backlog` и terminal statuses нет рабочего candidate; это не утверждение, что Backlog пуст. |
| `global-conflict` | Scope, Goal, owner, shared state или evidence противоречат друг другу так, что любая оставшаяся мутация небезопасна. |

Для смешанного scope выбирать disposition по precedence:
`global-conflict → actionable completion-remains → resume → work-remains →
deferred-only → no-work`. Это задаёт первый безопасный stage, а не исключает
остальные Tasks. Обычный terminal-ready candidate автоматически завершить;
`In Review` переводить в `deferred` только при настоящем decision/authority
blocker. Затем продолжить actionable review, resume и новую `To Do` работу.
Changes-requested rework текущей review chain имеет приоритет среди
dependency-ready `In Progress`; при task-local blocker defer-нуть lane,
освободить capacity и пересчитать disposition.

В `single` mode scope содержит ровно одну Task, execution topology всегда
serial, а review batch является risk-appropriate singleton. При material
blocker или failure опубликовать/read-back truthful `BLOCKED` либо
`REWORK REQUIRED` report, сохранить non-terminal status и завершить этот flow;
не выбирать другую Task. Общая automatic acceptance и terminal evidence policy
при этом не ослабляется.

Для `no-work` сообщить отдельно исключённые Backlog и terminal counts, выполнить
reconciliation применимого рабочего scope, в `batch` завершить обязательный
Goal только после прохождения completion gate и остановиться. Не создавать
пустой commit, не повторять дорогой gate и не производить effect только ради
свежего отчёта.

### 5.3 Terminal invariant и automatic acceptance

Любая `In Review` Task означает `completion-remains`. Пока в exact scope есть
хотя бы одна такая Task, запрещено отмечать весь execution plan завершённым,
объявлять terminal completion или завершать применимый batch Goal. `In Review` является
actionable completion stage: skill обязан довести candidate через недостающие
batch/effect/reconciliation gates, а не ждать пользователя.

Любой классифицированный ShipTask delivery intent является standing authority автоматически
принять exact result и перевести Task в `Done`, когда одновременно доказаны:
Task acceptance criteria, targeted gate, applicable exact review-batch gate,
integration identity, required non-production/runtime effects и отсутствие
unresolved in-scope finding. Сам по себе один check, deployment, report или
status этого не доказывает; решение должно опираться на полный evidence set.

В этом workflow `acceptance criteria` означает проверяемые критерии завершения
Task, а не human sign-off. Automatic terminal policy не настраивается Project,
Release или Task context. Изменить её можно только новым явным запросом
пользователя именно на изменение ShipTask contract.

Любое противоречащее этому правило из memory, rollout summary, предыдущего
report/Goal/plan, старой документации или cached project context считать
superseded historical evidence, а не current authority. Оно не создаёт blocker,
decision queue или основание оставить Task в `In Review`, даже если имеет более
раннюю формулировку «release gates не равны user acceptance». Current
specification и текущий delivery intent определяют поведение запуска.

Не запрашивать ручную приёмку, не создавать reason `acceptance-required`, не
оставлять terminal-ready Task в `In Review` и не блокировать batch Goal ожиданием
фразы «принимаю». При passing evidence автоматически записать и перечитать
обязательный completion report, обновить Task в `Done`, перечитать её и
продолжить scope.

Если старый run уже оставил Task/Goal в ожидании ручной приёмки, при resume
удалить retired blocker из текущего reasoning, заново проверить exact evidence
и применить обычный terminal transition. Не повторять ожидание несколько
goal-turns и никогда не переводить Goal в `blocked` по этой причине.

Если gate failed или evidence неполон, автоматически выполнить in-scope
rework/retest либо defer-нуть Task по конкретной причине, например
`ambiguous-product-decision`, `production-approval-required` или
`external-approval-required`. Automatic acceptance не заменяет явное production
approval, destructive/secret/privacy authority или обязательное решение
внешнего approver, прямо заданное Task/project policy.

После `Done` пользовательский bug report не отменяет историческое evidence
молча. Reopen исходной Task является authoritative сигналом rework; новая Task,
созданная отдельным planning request без execution intent, становится обычным
будущим scope. `Create-and-deliver` остаётся текущим single scope. На следующем
запуске старый report/checkpoint перечитывать как историю, а не как proof
текущего состояния.

### 5.4 Autonomous continuation и task-local defer

Следовать [runtime reference](../../ship-tasks/references/autonomy-and-release.md)
и [ADR-0004](../decisions/0004-autonomous-continuation-and-release-authority.md).
Во время long-running scope не прерывать runnable queue task-local вопросами.

Decision ladder:

1. Выбрать и выполнить разумный default, если он обратим, локален, остаётся
   внутри exact scope/acceptance, имеет ограниченный blast radius и не касается
   production, secrets, privacy, существенных расходов либо необратимого
   external effect. Зафиксировать rationale в evidence/report.
2. Если решение materially меняет продуктовый outcome, требует отсутствующей
   authority или остаётся неоднозначным после bounded research, defer-нуть
   только affected Task. Не угадывать, не отменять её и не создавать новую.
3. Остановить весь run с `TASK CONTEXT ALARM` только при global/shared conflict,
   который делает небезопасной любую оставшуюся mutation.

Deferred Task сохраняет truthful status: `To Do`, если execution не начинался;
`In Progress`, если существует partial/rework result; `In Review`, если exact
candidate machine-verified, но ждёт production/external approval или material
decision. Не переводить её в `Done`/`Canceled` и не изобретать portable
`Blocked` status.

В current run вести decision queue с canonical Task ref, reason, last safe
checkpoint, уже выполненными actions/evidence, recommended default, точным
decision/authority и resume step. Не переизбирать Task без нового evidence,
authority или external state change. Обязательно опубликовать и перечитать тот
же `BLOCKED` handoff в Task; при отсутствии comment write/read включить этот
terminal effect в blocker без изменения `description`.

Когда runnable Tasks остаются, продолжать их без вопроса пользователю. Когда
остались только deferred Tasks, предъявить одну consolidated decision queue.
Plan, а в `batch` и Goal, остаются незавершёнными; Goal `blocked` разрешён
только после текущего строгого tool threshold, а не из-за первого defer.

В уже разрешённом exact scope непосредственно перед task-local
`request_user_input`, финальным вопросом с ожиданием ответа или эквивалентным
blocking pause повторить complete inventory и пересчитать `runnable_count` без
уже deferred Tasks. При `runnable_count > 0` blocking input запрещён:
сохранить/обновить queue, освободить lane и выбрать следующую dependency-ready
Task. Использовать cached disposition, review precedence или готовность batch
packet вместо этой проверки нельзя.

### 5.5 Environment и release authority

Классифицировать exact release target по project instructions, config и current
provider state. Название Task Manager `Release`, URL или прежний deploy сами по
себе не доказывают environment class.

ShipTask delivery intent является standing authority для обычного in-scope
non-production release workflow в local/development/test/QA/UAT/staging/preview/
sandbox environment: build/package, deploy/redeploy, required non-production
migration, smoke, bounded diagnosis и repair/rollback. Не запрашивать отдельное
подтверждение для этих шагов. Если non-production release временно нарушил
in-scope surface, диагностировать и восстановить/исправить его в том же scope.

Production release выполнять только после явного user approval для production
target. Не выводить approval из Task/Release title, acceptance, Goal, checks,
  project automation, прошлого approval или самого delivery intent. Без approval
выполнить безопасную preparation, release и verification на non-production,
затем оставить Task в truthful non-terminal status, defer-нуть её с reason
`production-approval-required`, обязательно записать и перечитать `BLOCKED`
report и продолжить остальные Tasks. Не задавать production-вопрос
пока есть runnable work.

Если target нельзя надёжно классифицировать как non-production, считать его
production-like и defer-нуть Task. Standing non-production authority не
разрешает unrelated cleanup, permanent deletion, destructive durable-data
reset, secrets exposure/rotation, неограниченные расходы или нарушение explicit
read-only boundary. Deployment не заменяет полный terminal evidence и
independent smoke.

## 6. Execution topology

Default mode — adaptive execution с ceiling до четырёх writable task lanes.
Фактический target вычисляется для каждой execution wave:

```text
active_write_target = min(
  worker_ceiling,
  dependency_ready_width,
  conflict_free_width,
  isolated_task_capacity,
  verification_capacity,
  integration_headroom,
  review_headroom
)
```

`active_write_target` и `batch_target` — разные величины. Первый ограничивает
реально исполняемые или дорабатываемые Task, второй — число уже
targeted-verified candidates, которое выгодно собрать перед общим gate/effect.
Review batching никогда не превращает `In Progress` в waiting room: candidate,
который уже прошёл targeted gate и интегрирован, должен находиться в
`In Review`, пока ждёт общий commit identity, review-batch gate, UAT/runtime
effect, completion comment или terminal reconciliation.

Run ведёт явный набор `active_lane_tasks`:

- каждый подтверждённый `To Do → In Progress` read-back добавляет Task и
  занимает одну writable lane;
- без фактически запущенных isolated concurrent workers
  `active_write_target = 1`, независимо от размера scope и `batch_target`;
- lane освобождается после подтверждённого `In Review`/terminal read-back либо
  после truthful defer незавершённого partial/rework checkpoint по правилам
  report/autonomy; targeted-verified candidate нельзя выдавать за partial defer;
- unresolved или unknown status write не освобождает lane.

Перед каждым новым `To Do → In Progress` действует обязательный
status-reconciliation barrier. Для каждой Task, занятой текущим run, но больше
не находящейся в implementation/rework, workflow обязан сначала выбрать и
подтвердить ровно один исход: targeted-verified integrated candidate →
`In Review` с read-back; незавершённый material blocker → truthful defer;
terminal result → terminal read-back. Если после этого число занятых lanes не
меньше `active_write_target`, начинать следующую `To Do` запрещено. В serial run
это означает: предыдущая Task должна покинуть активную lane до status-start
следующей.

Неизвестный task class начинать не шире двух lanes. Увеличивать target после
чистого fan-in и при свободном verification/integration/review buffer.
Уменьшать при новых dependencies, semantic conflict, failed aggregate check,
rework или заполненном review WIP.

`serial` mode использовать для одной ready Task, связного write-critical path,
неизолируемого shared state или ограниченной review capacity. `exact workers=N`
использовать только по явному запросу; невозможность безопасно поддержать N
останавливает dispatch.

Отдельно сообщать execution mode, ceiling, active target, sustained lanes,
ready/blocked/review counts и причины свободной capacity.

### 6.1 Двухуровневая verification

Использовать два уровня проверки:

1. **Per-Task targeted gate** — обязательная быстрая проверка каждой Task до
   включения в review batch: acceptance-specific tests, changed-scope checks,
   воспроизведение исправляемого defect и дешёвые static/build checks, когда они
   материальны. Не запускать полный дорогой project gate для каждой Task, если
   риск и project policy допускают batching.
2. **Review-batch gate** — периодическая тщательная проверка exact
   интегрированного batch: project-defined aggregate/full suite, integration и
   risk-relevant browser/e2e, migration, security, performance, runtime либо
   external checks. Выполнять каждый дорогой check один раз для точной batch
   identity, а не повторять его для каждого member.

На preflight определить `batch_target`, review WIP limit, дорогие checks и
trigger policy. Размер не фиксировать глобально: учитывать dependency fan-in,
конфликтность, риск, длительность gate и review capacity. Если доступно
несколько безопасных кандидатов, не запускать дорогой gate на singleton только
для удобства.

Запускать review-batch gate, когда выполнено хотя бы одно условие:

- достигнут batch target или заполнен review WIP;
- закончилась execution wave либо больше нет готовых Tasks для наполнения
  batch;
- high-risk/coupled change требует раннего gate, включая обоснованный batch из
  одной Task;
- предстоит общий external effect или перевод members в `Done`;
- пользователь запросил checkpoint;
- выполняется final flush перед completion.

Batch identity включает member Task refs, exact source/integration identity и
набор проверок. Любое изменение integrated result после passing batch gate
аннулирует относящееся к нему evidence и требует нового gate перед terminal
transition.
При заполненном review WIP сначала завершить batch/rework, а не продолжать
dispatch новых Tasks.

## 7. Isolation и integration

Для каждой concurrent writable Task использовать отдельную task branch и
worktree. Для non-Git работы требуется эквивалентно изолированная execution
surface.

Инварианты:

- одна active Task и один writer на execution surface;
- branch/worktree привязаны к canonical Task ref;
- worker не пишет в integration target или чужую branch;
- shared schema, generated artifacts, mutable dependencies, caches, runtime
  state и environments либо изолированы, либо делают Tasks конфликтующими;
- reviewer/support role не получает mutation authority;
- один integration owner выполняет fan-in в dependency order;
- после merge повторяются affected targeted checks; aggregate/full checks
  выполняются review-batch gate на exact integrated result.

Merge conflict, semantic conflict или aggregate regression возвращает Task в
rework. Не маскировать конфликт незапланированной правкой integration owner.

## 8. Task execution

Для каждой рабочей Task:

1. Зафиксировать canonical Task ref, current detail/version, status, base
   identity, acceptance, exact release target/environment class и разрешённые
   writes.
2. По status выбрать stage: `To Do` провести через preflight и перевести в
   `In Progress`; `In Progress` продолжить из проверенного checkpoint;
   `In Review` не реализовывать заново до finding, а сразу проверять exact
   candidate.
3. Для `To Do` и `In Progress` реализовать или завершить минимальный целостный
   result без unrelated cleanup. Для `In Review` использовать уже предъявленный
   result.
4. Выполнить или повторить per-Task targeted gate и проверить changed scope.
5. Перед review прочитать все связанные duplicate Tasks и включить их
   отличающиеся problem statements, acceptance и failure scenarios в checklist.
   Если duplicate описывает материально отдельную проблему, зафиксировать
   finding, defer-нуть affected Task для scope decision и продолжить
   независимые Tasks вместо interrupting question или silent closure.
6. Интегрировать targeted-verified result, сформировать candidate evidence и
   обновить Task в `In Review`, если она ещё не в этом status. Это provisional
   review-ready state, а не terminal completion. Status write и read-back
   являются barrier перед освобождением lane и стартом replacement Task; общий
   commit, review-batch gate или external effect не разрешают отложить этот
   переход.
7. Наполнить review batch до trigger из раздела 6.1. Провести independent agent
   review без mutation authority, когда его требует risk class или project
   policy, и выполнить review-batch gate на exact integrated result.
8. Выполнить общие обязательные external effects в batch cadence и независимо
   проверить exact target. Non-production release выполнить без confirmation по
   разделу 5.5; production без explicit approval defer-нуть. Не повторять один
   дорогой effect для каждого member.
9. Сформировать batch/review packet как evidence artifact, а не user gate. Не
   публиковать `ACCEPTANCE READY` и не запрашивать ручную приёмку. До terminal
   transition опубликовать и перечитать обязательный `COMPLETED` report без Task
   field fallback.
10. При changes requested либо failed batch gate вернуть Tasks, чьё evidence
    стало недействительным, из `In Review` в `In Progress`. При доступной native
    comments capability опубликовать понятный rework/incident comment. Если
    comment write недоступен, defer-нуть affected Task с явным blocker.
    Сохранить текущие lanes, выполнить rework и
    targeted retest, затем собрать и проверить новый exact batch. После полного
    passing terminal evidence автоматически принять result, обязательно
    опубликовать и перечитать final report comment, затем обновить Task в `Done`
    и перечитать. Аналогично
    обработать подтверждённый `Canceled` outcome.

При любом task-local blocker сохранить last safe checkpoint, truthful status и
decision queue entry; обязательно опубликовать и перечитать `BLOCKED` report.
Если comment write/read недоступен, включить его в blocker. Освободить lane и
продолжить другие dependency-ready Tasks. Не
переизбирать deferred Task без нового evidence/authority/state change.

Разделять Task Manager state, source result, checks, automatic acceptance
decision и external effects. Успех одного слоя не доказывает остальные.

## 9. Review и reports

Batch/review packet должен содержать:

- batch identity, member Task identifiers и цель batch;
- summary изменений и exact result identity;
- per-member `acceptance criterion → targeted evidence/result`;
- `duplicate scenario → covered evidence/finding` для каждого связанного
  duplicate;
- targeted checks каждого member и общие batch-gate checks;
- dependency/integration picture;
- risks, limitations и unresolved gaps;
- короткий optional user verification path для понимания и последующего
  feedback, но не как terminal gate;
- recommendation: `terminal-ready`, `rework` или `decision required`.

После changes requested показывать delta: исправленные findings, новый result
identity, повторённые checks и оставшиеся gaps.

Failed batch gate сначала локализовать по member, dependency и shared result:

- доказанно затронутые Tasks вернуть в `In Progress` и исправить в текущем
  scope;
- доказанно незатронутые Tasks можно оставить в `In Review`, только если их
  result identity и evidence не изменились;
- при неясной attribution считать evidence всего связанного batch
  недействительным и вернуть его members в `In Progress`;
- после rework повторить targeted gates затронутых Tasks и новый batch gate на
  exact integrated result.

Если defect обнаружен уже после `Done`, не переписывать terminal history
молча: reopen terminal Task только когда это разрешает project policy, иначе
defer-нуть affected route для consolidated scope decision и создавать отдельную
defect Task лишь при явной authority. Нормальный workflow обязан провести batch
gate до `Done`.

### 9.1 Delivery report как Task comment

Следовать [runtime format](../../ship-tasks/references/delivery-report.md),
[ADR-0003](../decisions/0003-delivery-reports-as-task-comments.md) и
[ADR-0006](../decisions/0006-delivery-comment-as-terminal-effect.md). На каждом
запуске проверить, что current Task Manager tool contract предоставляет native
comment create и list/read для canonical Task ref, а текущая authority разрешает
write.

Imported comments из `get_task_external_context` являются read-only provenance
и не доказывают native comment write. Не выводить capability из roadmap, версии
или прошлой сессии. Никогда не записывать report в `description`, acceptance,
status text или другой Task field как fallback.

Если create отсутствует/unsupported/unauthorized либо write outcome невозможно
reconciliate через read-back, не повторять write вслепую и не использовать Task
fields как fallback. Сохранить truthful non-terminal status, классифицировать
Task как `completion-remains` или `deferred`, добавить
`comment-delivery-unavailable`/`write-outcome-unknown` в decision queue и
продолжить независимые Tasks. Этот gap блокирует `Done` affected Task и Goal
completion, пока Task остаётся в рабочем scope.

При доступной capability:

- опубликовать `COMPLETED` report при terminal completion каждой изменённой
  рабочей Task;
- опубликовать `REWORK REQUIRED`/`BLOCKED` report при material failure,
  changes-requested или blocker, который важно объяснить пользователю;
- при каждом task-local defer обязательно опубликовать `BLOCKED` handoff с
  reason, last safe checkpoint, completed evidence, recommended default,
  required decision/authority и resume step;
- не публиковать `ACCEPTANCE READY`: terminal-ready evidence автоматически
  приводит к `COMPLETED`, а не к ожиданию пользователя;
- перед write при доступной comment list/read capability проверить, нет ли уже
  report для того же `Task + state + exact result`; после write выполнить
  read-back, если connector его поддерживает;
- при unknown outcome не делать blind retry и не заявлять `published`;
- не backfill-ить pre-existing terminal Tasks и не писать отдельный report в
  `Duplicate` без explicit authority.

Каждый новый report comment независимо от state `COMPLETED`, `REWORK REQUIRED`,
`BLOCKED` или `CANCELED` проходит обязательный Strategic Explainer pipeline из
[ADR-0013](../decisions/0013-strategic-explainer-for-shiptask-report-narratives.md).
Простой success не является исключением. До invocation ShipTask сам фиксирует
authoritative state, exact result, evidence, impact и допустимый next action.
Для этого он выполняет task-level finalization: перечитывает Task/result/effects,
проверяет safe self-recovery и после material state change начинает этот шаг
заново. Explainer адаптирует только человеческое объяснение и не выбирает
report state.

ShipTask читает стратегическое объяснение, использует его как смысловую основу
и самостоятельно пишет final comment своими словами. Comment объединяет
authoritative envelope (`State`, Task, result identity, report key и необходимое
evidence) с понятным outcome, impact, причиной/границей и next state. Родитель
может сокращать, перестраивать и адаптировать текст под Task Manager, но обязан
сохранить material meaning Explainer: нельзя бездумно копировать его ответ,
противоречить ему, добавлять неподтверждённые выводы или заменять объяснение
собственным process diary. Перед write ShipTask выполняет forward trace и
reverse coverage. Explainer output не является evidence.

Report остаётся task-specific: shared batch evidence кратко отразить в каждом
member, но не копировать полный batch log. Comment write и status update считать
разными side effects и reconciliate независимо, пока connector не гарантирует
их атомарность.

### 9.2 Человекочитаемый формат

Начинать с результата и пользовательского эффекта, затем объяснять реализацию,
поведение, evidence, ограничения и требуемое решение. Масштабировать глубину по
сложности и риску; не превращать простой change в формальный postmortem и не
вставлять raw logs, огромные file lists или декоративные схемы.

Диаграмму использовать только когда она заметно быстрее объясняет runtime/data
flow, changed boundary, lifecycle или causal chain, чем короткий текст. Не
добавлять её по формальному признаку сложности. Для локального изменения обычно
достаточно compact before/after. Формат выбирать по доказанному comment renderer
contract: plain text работает как baseline; Mermaid не выдавать за rendered
diagram без подтверждённой поддержки.

При success report должен объяснять: что получил пользователь, как проходит
основной flow, что и почему изменено, как это проверено и какие ограничения
остались. При material failure добавить: наблюдаемый симптом/impact, detection,
trigger, root cause с confidence, recovery/rework, prevention и remaining risk.
Писать blameless, отделять evidence от inference и не создавать follow-up Tasks
без отдельной authority. Обычный red/green test внутри implementation не
является material incident сам по себе.

Человекочитаемые секции каждого Task comment родитель формулирует сам после
чтения task-scoped стратегического объяснения. Он сохраняет смысловую модель,
служебный envelope и необходимое evidence, но не возвращает narrative обратно
в technical vocabulary. В comment не упоминаются субагент, Strategic Explainer,
Technical Brief или внутренняя orchestration.

### 9.3 Осмысленная финализация и terminal interaction report

Перед любым terminal outcome, blocking pause или финальным ответом следовать
[run-report reference](../../ship-tasks/references/run-report.md) и
[ADR-0010](../decisions/0010-blocker-analysis-and-human-run-report.md).

Finalization pass обязан сопоставить requested и actual outcome, перечитать
current scope/Task/Goal/result/effect state, проверить существенное evidence и
объяснить material gaps. Если safe in-scope recovery доступен при существующей
authority, агент выполняет его, повторяет affected checks/read-back и начинает
finalization заново. Terminal report нельзя строить по состоянию до recovery.

Blocker считается существующим до фактического устранения. Возможность recovery
не переименовывает его в non-blocker; она означает, что terminal Goal `blocked`
пока не обоснован, потому что агент ещё способен сделать meaningful progress.
Если blocker сохраняется после self-recovery и выполнен строгий tool threshold,
до `update_goal(status="blocked")` показать человеку plain-language explanation:
что не достигнуто, почему, что уже сделано, почему агент не может продолжить сам
и какое одно условие возобновит run.

Каждый terminal exit ShipTask (`complete`, `blocked`, partial/deferred,
`no-work`) заканчивается глубоким компактным `SHIPTASK RUN REPORT`. Report
сначала передаёт итог, текущий статус и причинную модель простым языком, затем
только необходимые evidence, ограничения и следующий шаг. Форму адаптировать к
результату; не выгружать process diary, raw logs/tool calls или исчерпывающий
inventory. Task comments не заменяют общий interaction report.

Перед каждым Task report comment ShipTask создаёт task-scoped `Technical Brief`
и запускает новый built-in `default` subagent с точным `fork_turns="none"`.
Положительное число fork turns, `fork_turns="all"` и продолжение старого
Explainer thread запрещены. Initial task содержит только инструкцию применить
`$strategic-explainer` и самодостаточный handoff; full conversation, tool
transcript и process diary не передаются.

Strategic Explainer сам проверяет context integrity до анализа. Если он вернул
`CONTEXT_INTEGRITY_ERROR`, ShipTask не использует этот ответ как объяснение, не
делает comment/status/Goal write и исправляет собственную orchestration:
один раз запускает новый default subagent с `fork_turns="none"` и заново
передаёт bounded Technical Brief. Повторный context-integrity отказ останавливает
report workflow до любых Task Manager mutations и сообщается как внутренняя
ошибка orchestration, а не blocker доставляемой Task.

При корректном вызове субагент применяет `$strategic-explainer` и возвращает
свободное стратегическое объяснение. Для user-facing terminal run report
ShipTask может переиспользовать его только при идентичном single-Task scope и
неизменившемся material meaning. Planned comment/read-back и terminal status
reconciliation не делают объяснение stale, если совпали с переданным next-state
contract и не обнаружили drift. Для aggregate batch, нескольких blockers или
другого audience создаётся новый scope-level handoff.

ShipTask читает объяснение и пишет пользовательский текст своими словами, но
выбирает status, recovery, action, report identity и Goal transition только по
исходному evidence и authority. Любой `BLOCKED` Task comment получает
task-level explanation до write. До blocking user handoff и допустимого
`update_goal(status="blocked")` должно существовать scope-level explanation;
при exact single-Task совпадении основой может служить то же проверенное
объяснение.

Нельзя передавать Explainer raw process diary или просить его решить, является
ли состояние blocker. Brief обязан отдельно назвать confirmed outcome,
непроверенный сценарий, user impact, current capability/attempts и только
подтверждённый candidate user dependency. Если recovery изменил состояние,
старое объяснение недействительно. Простота success не отменяет обязательную
адаптацию Task comment; compatible single-Task explanation можно переиспользовать
для финального chat report без второго model run.

Если отдельный субагент или `$strategic-explainer` недоступен, ShipTask применяет
тот же смысловой contract самостоятельно. Потеря communication helper не
изменяет Task/Goal outcome, не создаёт terminal blocker и не разрешает выдать
reason code либо внутренний термин без объяснения.

## 10. Defects и recovery

- Автоматически исправлять только defect, который acceptance или project policy
  включает в exact scope.
- Для нового out-of-scope defect не выполнять code или scope-changing Task
  Manager writes. Если finding блокирует текущую Task, defer-нуть только её,
  обязательно опубликовать и перечитать `BLOCKED`/`decision required` report;
  при невозможности включить comment delivery в blocker и продолжить
  независимые Tasks. Включить решение в consolidated queue.
- Если новый out-of-scope finding не блокирует ни одну in-scope Task, записать
  его как non-blocking final finding и продолжить. Не создавать Task, не
  расширять Goal, не вызывать user input и не удерживать completion текущего
  scope; пользователь может отдельно авторизовать follow-up позднее.
- Не использовать failure как разрешение на cleanup, unrelated fixes,
  destructive recovery или silent task creation.
- При resume перечитать Tasks и сверить их с workspace, Git, checks и external
  states. Старый report comment является checkpoint, но не proof.
- Если пользователь уже reopen-нул terminal Task в рабочий status, считать её
  обычной текущей rework Task; не требовать отдельной приёмки самого reopen.
- При competing owner, unexplained drift или dirty state остановить затронутую
  lane, defer-нуть affected Task и продолжить изолированные lanes, если shared
  state остаётся безопасным. Не выполнять automatic reset, clean, stash,
  force-push, takeover или удаление чужой worktree/branch.

## 11. Completion

Completion требует:

- zero unfinished рабочих Tasks (`To Do`, `In Progress`, `In Review`) и
  unresolved in-scope defects; Backlog явно исключён и не блокирует этот gate;
- zero terminal-ready candidates, оставленных в `In Review`;
- zero deferred Tasks и unresolved decision/authority entries;
- final review batch прошёл gate на exact final integrated result;
- все duplicate-derived scenarios покрыты evidence либо вынесены как явные
  findings/scope decisions;
- automatically accepted results присутствуют в exact integration state;
- final project checks относятся к exact result;
- обязательные external effects независимо проверены;
- для каждой изменённой или materially failed рабочей Task обязательный
  report-comment опубликован и перечитан; `not-available` или
  `write-outcome-unknown` остаются незавершённым terminal effect;
- все рабочие и изменённые Tasks перечитаны и их current statuses соответствуют
  фактам; исключённые Backlog и terminal counts отражены отдельно;
- в `batch` mode обязательный Goal относится к exact scope и оставался
  активным, пока существовали подходящие Tasks, rework/completion remnants или
  unresolved in-scope defects; в `single` mode Goal отсутствует;
- run/journal state reconciled, когда он применим.

Только в `batch` mode перед `update_goal(status="complete")` повторить complete
inventory выбранной границы, выполнить finalization pass и проверить все пункты
completion. Если хотя бы одна Task подходит под рабочие критерии, остаётся
deferred/decision queue, доступный recovery либо отсутствует обязательный
evidence layer, не завершать Goal: продолжить runnable workflow или, когда
runnable work исчерпан, предъявить consolidated queue. Goal `blocked` применять
только по текущему строгому tool threshold, когда blocker остаётся после
self-recovery и понятное пользователю объяснение уже дано по разделу 9.3. Goal
completion является последним lifecycle write после Task и evidence
reconciliation, а не заменой этой проверки.

Финальный interaction report показывает фактический outcome и status; для batch
— также Goal status. Остальные Task/result/effect/comment details включать только
в объёме, который объясняет или доказывает вывод. Report не выдаёт скипнутые или
unknown writes за опубликованные comments; для deferred Tasks компактно
показывает impact, last safe checkpoint и exact decision/authority needed.

## 12. Non-goals

- Не превращать идею или specification в новый task scope без отдельной
  planning-команды.
- Не использовать другой task provider или generic fallback.
- Не изображать durable claims, background scheduler, Project/Release
  administration или bulk mutation существующими connector capabilities и не
  использовать `description` как fallback при проблеме с comments.
- Не максимизировать agent count без dependency, isolation, integration и
  review capacity.
- Не считать Task status, plan, worker report, commit, check или deployment
  достаточным evidence другого слоя.
- Не выполнять production release без explicit user approval и не применять
  production-style confirmation к ordinary verified non-production release.
- Не использовать standing non-production authority для destructive,
  secret-related, unrelated или explicitly read-only actions.
- Не менять project memory без явной просьбы пользователя и не хранить в ней
  live Task state, secrets или невыданное approval.
- Не дублировать OAuth/MCP adapter procedure как business policy; ShipTask
  сохраняет только необходимые safety invariants и делегирует mechanics
  Task Manager adapter.
