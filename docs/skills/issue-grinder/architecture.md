# Issue Grinder: архитектура

Статус: current agent-owned Architecture, 2026-09-12. Независимые user-owned
источники находятся в локальных [Overview](overview.md) и
[Requirements](requirements.md). Эта Architecture описывает current способ
достижения цели `$issue-grinder` и не может ослаблять, расширять или
переопределять два пользовательских документа. Их возможный конфликт сохраняется
и разрешается только пользователем.

## 0. Compilation contract

Локальные `overview.md`, `requirements.md` и `architecture.md` являются тремя
самостоятельными source-входами `$issue-grinder`. Runtime skill должен быть их
компактной смысловой проекцией: удаление runtime и повторная сборка из этих трёх
документов должны давать примерно эквивалентное наблюдаемое поведение, сохраняя
назначение Overview, все `IG-*` и выбранную здесь реализацию.

Runtime `$issue-grinder` создан в repository как Level 3 compilation. Этот
факт сам по себе ещё не утверждает, что Marketplace package опубликован,
установлен или проверен в fresh Codex session.

## Консультант при затруднении

Runtime mechanics загружаются из `references/consultant.md` по ссылке в delivery
entrypoint при содержательном затруднении.

`IG-FLOW-07` исполняется в delivery loop при возникновении содержательной
неопределённости, а не при старте каждой задачи. Coordinator использует только
явно заданные сведения текущего доверенного контекста: `gpt-6-astra` исключает
автоматический вызов; unknown не считается подтверждённым non-Astra и не
разрешает этот необязательный вызов. Поиск модели или effort не выполняется.

При выполнении условий coordinator читает доступный `$issue-grinder:consultant`
(или однозначно разрешённый `$consultant`) и вызывает его по собственному
контракту skill, без копирования его model/effort/transport в Grinder. Отсутствие
skill либо его точной runtime capability означает unavailable, а не новый
terminal blocker и не разрешение подменить модель или создать CLI-сессию.

Консультант получает один вопрос, факты, уже проверенные гипотезы и ограниченные
anchors. Он может прочитать необходимый контекст, но не получает пакет работы,
реализацию, выполнение тестов, самостоятельное review или acceptance. Такой
совет допускается и в `Соло` как ограниченный service provider, сохраняя одного
исполнителя. Прямой пользовательский запрет на субагентов приоритетнее.
Execution-child без возможности вызвать Консультанта возвращает затруднение
coordinator; тот проверяет собственный профиль и условия обращения. Astra
coordinator не обходит свой guard вызовом от имени более слабого worker.

После совета coordinator проверяет его применимость и продолжает обычный mode
workflow, сохраняя обязательные проверки и authority. Повторная консультация
нуждается в новых существенных фактах или конкретном оставшемся пробеле; тот же
вопрос без нового основания не повторяется. Если препятствие ведёт к остановке
или запросу вмешательства пользователя, обязательный цикл ниже применяется и
к известной нехватке доступа, разрешения, внешнему сбою или неясности требований.

### Обязательная проверка перед остановкой Goal

`IG-GOAL-04/07` имеют отдельный маршрут от обычного `IG-FLOW-07`:
перед остановкой или запросом вмешательства пользователя из-за препятствия coordinator читает
`references/consultant.md`. Только подтверждённая ведущая Astra выбирает
самостоятельный разбор. Для остальных профилей, включая unknown, обязательна
консультация независимо от кажущейся очевидности внешнего препятствия.
Это явный запрос вызывающего workflow, а не общий эвристический auto-trigger
Консультанта. Его собственный контракт допускает caller-owned routing.

Coordinator начинает с вопроса о самостоятельном выходе: current scope и
обязательный результат, причины, факты, попытки, authority и anchors. Ожидаемый
результат — разрешённый путь продолжения либо причинный отчёт и объяснения
каждой причины. Skill Консультанта владеет точным профилем и fresh child transport;
Grinder не дублирует эти параметры. Консультант не получает execution packet,
review/acceptance или право менять Goal. Ведущая Astra сама выполняет тот же
разбор и готовит тот же комплект, без отдельного provider-а.

Coordinator проверяет совет и source basis. Подтверждённый существенный in-scope
шаг отменяет blocker: выполнить, проверить, восстановить frontier. Новые факты
после доработки снова требуют разбора перед новой остановкой; уточнение того же
вопроса следует собственному follow-up контракту Консультанта. Если пути нет,
проверенный вывод показывается пользователю без Strategic Explainer. Общий
report и reason answers — одна publication unit, а не лимит числа консультаций.
Publication/status и platform audit остаются у coordinator.

Одна консультация не завершает разбор при оставшихся предположениях, перспективных
альтернативах или пробелах. Coordinator активно обсуждает отдельные вопросы и
результаты проверок без фиксированного лимита обращений. Для нового вопроса
используется новый fresh child по контракту provider-а, для уточнения — follow-up
с конкретным пробелом или новыми фактами. Неизменный вопрос не повторяется.

Совет «нужно разрешение» проверяется на осуществимость всей последовательности:
доступные проверки совместимости и подготовка выполняются до вопроса человеку.
Если новая проверка открыла самостоятельный путь, coordinator выполняет его;
если обнаружила новый пробел, возвращает его Консультанту. Разрешение на первый
шаг не запрашивается вместо исследования остальных необходимых шагов. При
ведущей Astra этот же цикл проходит самостоятельно.

Если обязательный Консультант недоступен или запрещён пользователем, сохранить
возобновляемый checkpoint и сообщить именно о невыполненной проверке остановки.
Не подменять её native/Explainer и не объявлять Goal blocker проверенным.
Такой checkpoint не является принятым blocker fingerprint и не даёт права
перевести Goal в blocked по накоплению автоматических turns. Неизменный уже
принятый blocker, напротив, переиспользует проверенный вывод без новой
консультации. Single-issue run без Goal сохраняет прежний publication route,
но препятствие перед обращением к пользователю проходит цикл `IG-FLOW-07`.

## 1. Runtime package и distribution

### 1.1 Минимальная форма plugin

`$issue-grinder` поставляется отдельным plugin `issue-grinder`. Plugin содержит
три независимых runtime skill: одноимённый delivery coordinator, канонический
planning-only `task-composer` и `scope-reviewer`. Общий distribution artifact не
смешивает их Overview, Requirements или Architecture: каждый skill сохраняет
собственный source package, boundary и runtime source, но после cutover остаётся
доступен без установки старого ShipTask.

Marketplace package имеет минимальную форму:

```text
plugins/issue-grinder/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    ├── issue-grinder/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   ├── references/
    │   │   ├── mode-help.md
    │   │   ├── run-and-goal.md
    │   │   ├── task-manager-flow.md
    │   │   ├── thread-title.md
    │   │   ├── autonomy-and-environments.md
    │   │   ├── execution-modes.md
    │   │   ├── modes/
    │   │   │   ├── solo.md
    │   │   │   ├── classic.md
    │   │   │   └── economical.md
    │   │   ├── multi-agent-execution.md
    │   │   └── strategic-explainer.md
    │   └── scripts/
    │       ├── model_routing_guard.py
    │       └── writer_worktree_guard.py
    ├── task-composer/
    │   ├── SKILL.md
    │   └── agents/openai.yaml
    └── scope-reviewer/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/
        └── scripts/
```

Plugin не содержит собственный MCP server, UI, assets или hooks. Узкие runtime
scripts механически валидируют объявленный model routing, обеспечивают writer
admission и проверяют маршрут независимых оптик; Task Manager предоставляет
live data, authentication, authorization и controlled mutations; skills
остаются workflow- и orchestration-слоем вокруг этого adapter-а.

Такая форма следует принципу минимального plugin из
[официальной архитектуры OpenAI](https://developers.openai.com/plugins/concepts/plugins):
plugin может содержать только skills, а MCP server, UI и lifecycle extensions
добавляются позднее без изменения его назначения.

### 1.2 Внутреннее устройство skill

`SKILL.md` остаётся компактным исполнимым entrypoint. В нём находятся:

- trigger и граница между явным и неявным invocation;
- стратегический смысл и обязательные terminal conditions;
- ранняя развилка между чистой справкой и delivery;
- общий delivery loop и terminal conditions;
- routing к условным references;
- жёсткие authority и truth boundaries, которые нельзя потерять при
  progressive disclosure.

Подробности загружаются только тогда, когда меняют текущие решения:

- `mode-help.md` — только для чистого вопроса о режимах, default resolver-е,
  различиях или выборе; этот fast path не загружает delivery protocol;
- `run-and-goal.md` — после подтверждённого delivery intent: invocation
  continuity, selector, title routing и Goal lifecycle;
- `final-report.md` — перед завершением, blocker-handoff или нетерминальным
  checkpoint: восстановление всего run и проверка именно исходящего текста;
- `task-manager-flow.md` — live scope, lifecycle, blocked-by, comment/status
  transaction, read-back и recovery;
- `execution-modes.md` — после однократного выбора режима и перед
  декомпозицией: общий mode resolver, invariants и switch barrier;
- `multi-agent-routing.md` — только вне Соло: профили субагентов, dispatch
  receipts, event coordination и review packet, до первого профильного решения;
- `local-evaluation.md` — только для явно изолированного model-forward запуска;
- `modes/{solo,classic,economical}.md` — ровно один файл после
  сохранения canonical mode; в нём целиком находятся mode-specific topology,
  role/profile routing, fallback, review и stop promise;
- `autonomy-and-environments.md` — только для явно вызванного автономного run и
  действий со средами;
- `multi-agent-execution.md` — только когда существует полезная независимая
  работа или явное topology rule пользователя;
- `strategic-explainer.md` — перед обычным comment, blocker-report без Goal или финальным
  пользовательским текстом.

Reference не создаёт собственную политику и не становится параллельным
Requirements или Architecture. Один режим не должен собираться из фрагментов
нескольких mode-файлов: общая механика загружается отдельно, а выбранная
mode-specific policy имеет ровно одного runtime-владельца. Весь применимый смысл
`IG-*` должен оставаться восстановимым из `SKILL.md` и адресно подключаемых
references. Такой способ
разделения соответствует
[официальной модели skills](https://developers.openai.com/plugins/build/skills),
где `SKILL.md` задаёт workflow, а supporting resources выносят только нужную
условную детализацию.

### 1.3 Metadata, activation и внешние зависимости

`agents/openai.yaml` задаёт:

- `display_name: Issue Grinder` и короткое описание доставки Task Manager
  scope до terminal результата;
- `allow_implicit_invocation: true`, потому что архитектура различает
  автоматическую загрузку и явный `$issue-grinder`;
- MCP dependency `task-manager` с `streamable_http` transport;
- default prompt, который объясняет выбранный scope, но не подменяет текущий
  пользовательский prompt.

Skill description должна привлекать запросы реализовать, исправить, проверить
или доставить существующий Task Manager scope, а также вопросы о собственных
режимах Issue Grinder. Чистая справка является недоставочным fast path;
read/status/audit, иные объяснения и planning-only запросы не должны
маршрутизироваться в Issue Grinder.

Task Manager остаётся отдельно установленным adapter plugin и не копируется в
Issue Grinder package. Task Composer копируется только из канонического
repository source `task-composer/`; его planning-only lifecycle не расширяется
правами Issue Grinder. Scope Reviewer аналогично копируется только из
канонического repository source `scope-reviewer/` и сохраняет собственные
границы review и plan improvement. Strategic Explainer также остаётся отдельным plugin:
при доступности вызывается его semantic facade, при отсутствии применяется
native writing по `IG-FLOW-03`. Жёсткая plugin-to-plugin dependency для него не
моделируется.

### 1.4 Узкие runtime guards вместо скрытого orchestration engine

Runtime script добавляется только для повторяемой детерминированной операции,
которую существующие tools и инструкции не выполняют надёжно. Scope resolution,
Goal, lifecycle, verification, reflection и multi-agent dispatch зависят от
живого контекста и остаются решениями coordinator-а. Выносить их во второй
скрытый orchestration engine нельзя.

Наблюдаемые дефекты реальных прогонов доказали две подходящие для механизации
операции. В первых delivery coordinator прочитал hard invariant worktree, но
несколько writers всё равно начали запись в общий checkout. В других
многоагентных прогонах Luna называлась предпочтительной, однако substantive agents
получали профиль, несовместимый с выбранным режимом. Поэтому runtime содержит
два узких guard-а.

`scripts/model_routing_guard.py`:

- отделяет semantic role от platform `agent_type`;
- связывает unique packet identity, semantic role, explicit model, effort и
  bounded `fork_turns` в один стабильный dispatch fingerprint;
- в `Экономичном` fail-closed требует Luna Max для содержательных ролей;
- не выводит model/effort из имени либо типа агента;
- сравнивает requested и observed child profile и выдаёт стабильный receipt
  `issue-grinder/model-routing/v2`.

`scripts/writer_worktree_guard.py`:

- создаёт новую task-owned branch и linked worktree от exact base через
  `git worktree add --lock` без `--force`;
- выдаёт машинно проверяемый receipt по стабильному
  `git worktree list --porcelain -z`;
- допускает writer только из фактического current working directory exact
  linked worktree;
- фиксирует clean integration checkout и обнаруживает любую Git-visible mutation
  во время writer wave.

Guards не выбирают scope, packet, число writers, смысл роли, owner, integration
strategy или cleanup policy. Они не создают agents, не удаляют worktree, не
reset-ят состояние и не считают receipt доказательством качества реализации.
Это механическая проекция routing и `IG-MA-06..07`; Git сохраняет отдельные
`HEAD` и index каждого linked worktree, но exclusive agent ownership остаётся
ответственностью coordinator-а.
Guard не является filesystem sandbox и сам не отзывает у subagent доступ к
другим путям. Поэтому admission barrier предупреждает обычную ошибку до
implementation dispatch, а integration canary обнаруживает оставшееся нарушение
до fan-in/lifecycle effect и переводит wave в fail-closed reconciliation.
Опора на `--lock` и porcelain format соответствует
[официальному `git-worktree`](https://git-scm.com/docs/git-worktree.html).

Routing guard также не перехватывает raw platform `spawn_agent`: coordinator
может нарушить protocol и не вызвать Python script. Packet-bound fingerprint и
recursive telemetry делают такой обход наблюдаемым и запрещают считать run
валидным cost-aware mode, но не создают физического platform enforcement.
Непропускаемый gate потребовал бы dispatcher tool, который одновременно
валидирует и создаёт child, а direct raw spawn был бы ему недоступен. Runtime не
выдаёт локальный preflight за такую гарантию.

Абсолютные пути обоих bundled guard-ов разрешаются один раз при загрузке
multi-agent runtime и сохраняются в continuity текущего run. Нормальный
dispatch не тратит model turns на поиск script, чтение `--help` или повторное
исследование его interface: эти действия допустимы только как явное
восстановление после доказанного package/path mismatch. Внутренний владелец
волны применяет тот же admission к собственным children, поэтому корневой
дефицитный профиль не обслуживает их receipts.

Build- и evaluation-скрипты на уровне repository по-прежнему проверяют semantic
coverage Level 1/Level 2, behavioural scenarios, Marketplace package и byte
identity. В отличие от них оба guards входят в runtime package, потому что
обеспечивают доказанные хрупкие preconditions до model dispatch и внешней записи.

Hooks являются plugin/Codex lifecycle-механизмом, а не внутренним шагом skill.
Они могут выполняться вместе с hooks из других источников, требуют отдельного
trust review и срабатывают по общим lifecycle events. Поэтому основной цикл,
Production boundary, Goal completion и blocker reflection не реализуются через
hooks. Writer isolation не реализуется hook-ом: admission относится только к
конкретному packet и точному Git state, а глобальный lifecycle event не знает
его owner/base. Это соответствует
[официальной модели Codex hooks](https://learn.chatgpt.com/docs/hooks).

### 1.5 Repository source и установка

Канонический runtime source находится в этом repository:

```text
issue-grinder/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── mode-help.md
│   ├── run-and-goal.md
│   └── ...
└── scripts/
    ├── model_routing_guard.py
    └── writer_worktree_guard.py
```

После проверки `issue-grinder/` и `task-composer/` копируются в отдельный
Marketplace plugin соответственно как `skills/issue-grinder/` и
`skills/task-composer/`. Каждая пара repository source, Marketplace source и
installed cache должна быть byte-identical. Изменение runtime payload требует
новой manifest version, публикации Marketplace commit, переустановки plugin и
проверки свежего snapshot в новой Codex-сессии.

Standalone user-level duplicate не создаётся. Source package документации,
runtime source, Marketplace package и installed cache имеют разные роли и не
смешиваются в один writable каталог.

### 1.6 Переключение с ShipTask

Во время разработки Issue Grinder тестируется явным вызовом либо в изолированной
сессии, где конкурирующая автоматическая маршрутизация исключена. Cutover
устанавливает `issue-grinder@srez-marketplace`, затем удаляет локально
`ship-tasks@srez-marketplace`: Issue Grinder становится единственной
установленной неявной delivery authority, а Task Composer продолжает работать
как `$issue-grinder:task-composer` из нового package.

Старый Marketplace package можно сохранить как неустановленный rollback
artifact, но одновременно устанавливать его с Issue Grinder нельзя: это вернёт
конкурирующий ShipTask и дублирует logical Task Composer. Миграция не объявляется
завершённой, пока fresh skill discovery не показывает
`issue-grinder:issue-grinder`, `issue-grinder:task-composer` и отсутствие
установленного `ship-tasks:ship-tasks`.

## 2. Роль и зависимости

`$issue-grinder` — Task Manager-only coordinator доставки выбранного scope. Он
владеет общей стратегией, Goal, решениями о lifecycle issue, интеграцией кода,
окончательной проверкой и итоговым ответом пользователю.

Внешние интерфейсы разделены так:

- Task Manager adapter разрешает canonical refs, читает live issue, Release и
  связи, выполняет status/comment mutations и подтверждает их read-back;
- Strategic Explainer формулирует отдельные публикационные тексты, но не
  принимает решения о scope, статусе, полномочиях или продолжении работы;
- Goal хранит стратегическую цель и состояние длинного явно вызванного прогона;
- Git worktree и feature branches изолируют одновременно пишущих исполнителей;
- project context и project memory помогают найти Release, UAT и устойчивые
  разрешения, но не заменяют live Task Manager или фактическое состояние среды.

Ни одна зависимость не добавляет `$issue-grinder` полномочия сверх
`requirements.md` и текущего запроса пользователя.

Task Manager adapter является обязательной capability: без canonical reads и
versioned writes Issue Grinder не подменяет его локальным списком, другим
tracker-ом или памятью. Недоступность adapter-а обнаруживается до delivery
mutations и выдаётся как точная technical/context failure. Strategic Explainer,
напротив, остаётся optional communication dependency с native path.

Dependency declaration делает adapter доступным, но не заменяет его current wire
contract. Перед первой Task Manager mutation coordinator сверяет доступные tool
schemas и использует только реально объявленные операции и поля; названия,
idempotency и conflict shape не угадываются и не копируются в Issue Grinder как
вторая быстро устаревающая схема. Если обязательная semantic capability —
pagination, versioned write, comment/read-back или Goal operation — отсутствует,
это exact capability failure до соответствующего write. Механический guard,
если он нужен, принадлежит Task Manager adapter-у, а Issue Grinder сохраняет
собственные lifecycle и authority decisions.

## 3. Режим прогона и ранний context gate

### 3.0 Справочный fast path

До разрешения run coordinator классифицирует запрос. Если пользователь только
спрашивает о канонических режимах, default resolver-е, различиях или выборе,
runtime читает только `issue-grinder/references/mode-help.md` и отвечает без
Task Manager reads/writes, Goal, title mutation, recovery, environment
resolution, subagents и Strategic Explainer. Это observable negative-effects
contract `IG-HELP-01`, а не укороченный delivery run.

Если один prompt одновременно просит справку и явно поручает delivery,
coordinator сначала кратко отвечает или называет выбранный mode, затем отдельно
проходит обычный delivery gate. Наличие справочного вопроса не создаёт scope и
не расширяет authority delivery-части.

В начале нового run coordinator фиксирует три разных факта:

- `explicit invocation` — пользователь назвал `$issue-grinder` в prompt,
  запустившем именно этот run;
- `run mode` — является ли уже начатый run явно вызванным и поэтому автономным.
- `execution mode` — один из `Соло`, `Классический`, `Баланс` или
  `Экономичный`, его origin `explicit|automatic` и профили субагентов.

Прошлый `$issue-grinder` не разрешает начинать новый явный run или новый Goal.
Однако `run mode` не теряется посреди того же незавершённого прогона из-за
следующего turn, compaction, автоматического продолжения или восстановления
контекста. Непрерывность доказывается не одним совпадением selector-а: checkpoint
связывает origin `explicit|implicit`, identity Project/selector, canonical
execution mode, mode origin, профили субагентов, terminal flag, Goal ref при его наличии и task-owned
implementation/effect receipts. Для
single-issue run отсутствие Goal не уничтожает origin: тот же thread lineage и
согласованные checkpoints сохраняют его отдельно. Совместимый активный Goal
является одним из anchors, но сам по себе не доказывает тот же run и не переносит
autonomy в новый implicit request. При отсутствии доказанной непрерывности старый
explicit marker не восстанавливается по догадке. Terminal result либо явная
отмена, замена или существенная смена текущего прогона пользователем закрывают
этот режим.

До изменяющих действий coordinator разрешает:

1. явные уточнения scope и среды из текущего prompt;
2. canonical Project, Release и status refs через live Task Manager;
3. repository/project context и project memory как указатели на текущий Release,
   repository, команды и UAT;
4. фактическое подтверждение, что выбранная среда не является Production.

Устаревающая память используется только как locator и перепроверяется в живом
источнике. Неоднозначный default Release останавливает run до Task Manager
mutations. В явно вызванном автономном run неизвестный UAT также останавливает
работу до environment mutations; Production не используется как fallback.

Default Release разрешается только явному запуску без selector-а. Неявно
активированный skill должен получить однозначный issue, Release, Project или
иной ограниченный selector из текущего запроса и разрешимого непосредственного
контекста. Если такого selector-а нет, coordinator выполняет только безопасное
разрешение контекста и просит уточнение до любых mutations; remembered current
Release не подставляется как скрытое расширение scope.

При неявной загрузке Goal и дополнительные полномочия автономного режима не
создаются. Само исполнение разрешённого пользователем запроса и обычная
делегация независимой работы при этом могут продолжаться только в пределах
обычной authority текущего prompt и действующих платформенных ограничений.

Issue Grinder сам не создаёт routine approval prompt, запрещённый автономным
режимом. Если confirmation технически навязывает платформа или tool policy,
coordinator не выдаёт его за собственную продуктовую неопределённость и после
получения результата продолжает run; обойти платформенный gate скрытым способом
он не пытается.

### 3.1 Startup recovery gate

После разрешения repository и live scope, но до новой implementation, branch
или worktree coordinator выполняет read-only Git inventory. Он читает все
зарегистрированные worktree, локальные task-owned refs и их достижимость от
integration target, staged/unstaged/untracked status каждого доступного
checkout, незавершённые commits и известные run/worker checkpoints. Discovery
не ограничивается текущим `cwd`, текущей branch или артефактами этой Codex
сессии.

Provenance устанавливается по совокупности evidence: сохранённым receipts и
owner, exact issue/packet identity, branch/worktree metadata, commit history,
затронутым поверхностям и live scope. Одного похожего имени branch или каталога
недостаточно. После inventory каждый найденный candidate получает один исход:

- уже интегрированный результат переиспользуется и проверяется, а не
  реализуется повторно;
- exact-scope checkpoint с остановленным owner подхватывается в фактическом
  состоянии: существующий worktree используется на месте, branch без worktree
  получает новый linked checkout той же branch, а staged/unstaged/untracked
  изменения остаются частью checkpoint;
- active owner продолжает владеть worktree; coordinator взаимодействует с ним
  либо ждёт подтверждённой quiescence, но не создаёт replacement writer;
- ambiguous или unrelated artifact сохраняется без reset, cleanup, merge или
  присвоения run. Если он мешает выбранному integration target, coordinator
  использует отдельный clean task-owned integration worktree либо сообщает
  точный конфликт.

Dirty root checkout, доказанно принадлежащий текущему scope, может продолжаться
основным агентом как одна serial exclusive lane. Он не становится общим
integration checkout для параллельной wave и не передаётся subagent-у. Для
linked checkpoint bundled guard выполняет `resume`, затем обычный двухфазный
`admit`; `--allow-dirty` означает только сохранение доказанно task-owned
незавершённого diff после проверки quiescence. Recovery всегда предшествует
fresh `prepare`, поэтому новая branch не может молча дублировать найденную
работу.

### 3.2 Best-effort название текущей Codex task

`IG-UI-01` компилируется тем же безопасным first-turn contract, который
использует legacy ShipTask, но с namespace Issue Grinder. Auto-title является
optional UI metadata Codex: он не меняет Task Manager, не доказывает acceptance,
не создаёт Goal и никогда не блокирует delivery.

Eligibility требует одновременно:

- host явно предоставляет `list_threads`, `read_thread` и `set_thread_title`;
- найден ровно один active candidate calling task на том же host и в том же
  project/cwd;
- complete history доказывает ровно текущий первый user-triggered turn без
  завершённого предыдущего turn;
- current title пуст либо является очевидным catalog placeholder;
- live canonical scope уже разрешён.

Title, preview и summary используются только как untrusted identity evidence и
не меняют prompt или scope. Meaningful title, неизвестная provenance, title с
префиксом `Issue Grinder ·`, later turn, paginated/incomplete history и
неоднозначный candidate всегда сохраняются.

Для eligible calling task coordinator до первой Task Manager mutation делает не
более одной best-effort попытки `set_thread_title` без `threadId`; omission
адресует текущую calling task и не позволяет discovery mistake переименовать
соседнюю. Failed/deferred result не retry-ится и даёт только внутренний
`issue-grinder-title=not-available`.

Формат строится только из canonical scope:

| Scope | Title |
|---|---|
| single issue | `Issue Grinder · <Task ref> · <short Task title>` |
| Project + Release | `Issue Grinder · <Project name> · <Release name>` |
| Project scope без Release | `Issue Grinder · <Project name> · batch` |
| bare `$issue-grinder` | Project + Release после live-разрешения current Release |

Labels не включают status, дату, branch, acceptance text и другие volatile
details. Полный operational contract находится в
`issue-grinder/references/thread-title.md` и читается только когда first-turn
eligibility действительно возможна.

## 4. Режимы исполнения и профильный resolver

Режим выбирается после доказательства нового либо продолжающегося run и до
стратегической декомпозиции. Runtime читает общий
`issue-grinder/references/execution-modes.md`, создаёт либо восстанавливает mode
record, а затем полностью читает ровно один файл из
`issue-grinder/references/modes/`. Во время обычных последующих итераций
canonical mode берётся из run checkpoint и не проектируется заново; повторно
загружается тот же выбранный mode-файл, а не все четыре спецификации.

### 4.1 Однократное разрешение режима

Новый run: явный поддерживаемый режим имеет приоритет. Без него всегда
выбирается `solo`. Оценка объёма остаётся частью планирования работы, но не
выбора режима. Не определяй model/effort основной сессии, не читай её журналы
или конфигурацию и не требуй подтверждения профиля до effects или dispatch.
Неизвестный профиль не является blocker ни в одном режиме.

В mode record сохраняются `canonical_mode`, `mode_origin` и
`mode_selection_reason` (`Solo by default` либо явный выбор пользователя).
Поля основного профиля, его нормализация и классификация объёма для resolver
не нужны. Существующие records поддерживаемых режимов продолжаются с
сохранением работы; старые профильные поля и admission receipts игнорируются.
Механический mode harness принимает explicit choice и continuity без
параметров модели, effort или размера scope.

Стартовый текст в `agents/openai.yaml` поручает использовать Соло, только
если пользователь не указал другой режим. Он не задаёт безусловный override.

Для `Соло` сохраняются aliases `single`, `сингл`, «одним агентом» и
«без субагентов». Случайное слово в описании продукта не является selector-ом.
Удалённые `swarm`, `manager`, `roy`, `roi`,
«Менеджер» и «Рой» при явном mode intent отклоняются с просьбой выбрать
поддерживаемый режим; автоматическая подмена запрещена.

При доказанном продолжении сначала восстанови сохранённый mode record.
Уменьшение scope, новый turn, compaction, смена модели и квоты не меняют режим.
Старый record удалённого режима требует сохранения работы и явного выбора
пользователем нового режима через switch barrier, а не пересчёта default.
Прочитай ровно один mode-файл выбранного поддерживаемого режима.

### 4.2 Профили субагентов

Во всех режимах координация остаётся на текущем основном агенте без определения
его профиля. В `Соло` он единственный исполнитель; supervisor или worker
для delivery-работы не создаётся.

Для явно выбранного многоагентного режима:
- точный пользовательский override профиля субагента применяется первым;
- `Классический`, `Баланс` и `Экономичный` сохраняют baseline
  `gpt-6-luna` с `reasoning_effort=max` для предусмотренных ими Luna-ролей;
- в `Балансе` specialist и final reviewer используют Sol xhigh;
- основной профиль не определяется, не сравнивается с другими и не
  нормализуется; его неизвестность не препятствует исполнению.

Root всегда сохраняет одно владение Goal, Task Manager mutations, integration,
внешними effects и publication unit.

### 4.3 Маршрутный admission

До каждого child dispatch coordinator строит receipt с unique packet identity,
canonical mode, semantic role, platform `agent_type`, exact requested
model/effort, bounded `fork_turns` и fingerprint dispatch args. При доступной
telemetry туда добавляется observed profile; иначе сохраняются
`telemetry_pending` и exact spawn args. Отрицательный receipt запрещает
содержательную wave.

Default child profiles зависят от выбранного mode:

- `Классический`: только его узкие Luna Max packets и independent review;
- `Баланс`: Luna Max ordinary children; Sol xhigh specialist/final_review;
- `Экономичный`: Luna Max analysis, implementation и review children.

Имя роли не обходит routing: обычная implementation, спрятанная под названием
`review` или `material_judgment`, остаётся implementation.

### 4.4 Режимные workflow

| Mode | Runtime owner | Основные Requirement projections |
|---|---|---|
| `solo` | `modes/solo.md` | `IG-MODE-11`, один current profile, terminal-only |
| `classic` | `modes/classic.md` | `IG-MODE-03`, `IG-MA-14..17`, controller-led terminal result |
| `balance` | `modes/balance.md` | `IG-MODE-04`, `IG-MODE-20`, Luna coordinator, Sol specialist/reviewer, terminal-only |
| `economical` | `modes/economical.md` | `IG-MODE-06`, части `IG-MODE-08..09`, resumable checkpoint |

Общие resolver, authority и evidence invariants остаются в
`execution-modes.md`; multi-agent profiles, dispatch и review packet — в
`multi-agent-routing.md`; isolation и fan-in mechanics — в
`multi-agent-execution.md`. Только выбранный mode-файл владеет своей topology,
fallback, review и stop promise. `mode-help.md` остаётся delivery-free справкой.

### Баланс: компактный цикл Luna → Sol

Luna совмещает coordinator, author и integration owner, не создавая supervisor
по формальной причине. Sol получает либо конкретную неопределённость, либо
целый сложный участок. Две разные неуспешные попытки — практический сигнал к
эскалации; уже локализованное обычное исправление Luna доводит сама. Exact
candidate до приёмки обязательно проверяет отдельный Sol xhigh неавтор.
Полная история не наследуется, handoff содержит requirements anchors, diff,
проверки и неизвестное. После material rework продолжается тот же reviewer.
Контрактовый `final_review`/`specialist` маршрут Sol проходит обычный guard;
он не является пользовательским override. Модель не тратит отдельный turn на
учёт каждого шага. Sol writer получает task-owned worktree через существующий admission либо
разрешённый read-only patch handoff; общий checkout не передаётся второму writer.

Для local evaluation `SKILL.md` направляет в `local-evaluation.md`: затем
читаются execution-modes, выбранный mode и PLAN. Вне Соло добавляется
multi-agent-routing; multi-agent mechanics читается перед первым child, когда
нужен его admission. Обычный delivery не загружает evaluation instructions.
Это тот же установленный skill, без экспериментального заменяющего prompt.

### 4.4.1 Проверки, инструменты и стоимость организации

`IG-FLOW-08` реализуется условным чтением актуального
`codex-token-usage-report` перед итоговым ответом delivery (completion, blocker,
checkpoint). Entry point направляет к `execution-modes.md`; там закреплены
границы измерения и передачи полной таблицы. Сравнение расхода по отдельному
запросу использует тот же provider. Доступность определяется каталогом skills
текущей среды, без фиксированного user-level пути или зависимости plugin.

Сохраняй начало run и подтверждённые session IDs root и descendants в continuity.
Перед отчётом фиксируй cutoff последней доступной телеметрии. Используй штатный
фильтр provider-а, если он есть; иначе передай его helper-у временный изолированный
каталог с копиями только подтверждённых session logs через поддерживаемый параметр
входного каталога (у текущего helper это `--codex-home`, с `sessions/` и
`archived_sessions/`). Сохрани исходные записи для дедупликации provider-ом;
временные файлы держи вне Git и удали после чтения результата. Общий временной
интервал по всем сессиям машины не доказывает расход run. Если изоляция невозможна,
сообщи ограничение вместо чужого расхода или самодельного счётчика.

Формат, категории, model rows, цены и калибровка принадлежат provider-у.
Передавай его полную таблицу без сокращения строк, включая строки моделей после
Total; ни native writing, ни Strategic Explainer не должны её пересобирать или
сокращать. Итог сначала сообщает delivery outcome, затем период и таблицу с
оговорками provider-а. Отдельно обозначь cutoff: ещё не записанный финальный
ответ не входит в измерение. Отсутствие skill не требует установки и не мешает
завершению; ошибка измерения раскрывается кратко, без повторного delivery loop.

Общие `IG-MODE-09` и `IG-MODE-19` компилируются в `execution-modes.md` и
применяются также к Solo. Для длительного процесса сохраняй receipt: owner,
candidate/root, command, входы code/tests/config/environment/dependencies,
handle, state, exit code и log/result location. Обновляй его рабочим вызовом,
без отдельного model turn ради bookkeeping. Не теряй session id при сжатии
ответа до stdout. Пока процесс или результат доступны, восстанови ожидание или
чтение вместо повторного запуска. Неизвестный внешний effect сначала reconcile.

После изменения сопоставь реальные входы проверок: имя файла или candidate id
без проверки зависимостей недостаточны. Неизменные применимые результаты
переиспользуются; changed/unknown inputs требуют адресной либо более широкой
проверки. Интеграционная приёмка учитывает итоговое сочетание модулей. Reviewer
получает карту покрытия и raw results, самостоятельно ищет пробелы и при
необходимости перепроверяет их. Смена роли или фазы не обнуляет evidence.
Независимые чтения и проверки можно объединять в tool batch при сохранении
отдельных ошибок и результатов и отсутствии конфликтующих writes/effects.
Solo не исполняет этим способом несколько содержательных пакетов одновременно.

Admission учитывает постановку, context transfer, ожидание, интеграцию и review
без отдельного расчётного отчёта. Classic может оставить simple packet основному
профилю, если передача не окупается; independent review остаётся обязательным.

При Luna top-level Экономичный совмещает operational coordinator,
последовательного автора и integration owner в текущей сессии. Отдельный writer
или supervisor нужен только при конкретной пользе от независимой работы либо
изоляции контекста. Независимый Luna reviewer остаётся неавтором. При non-Luna
root нужен экономичный substantive owner; root сохраняет transport/authority
boundary и не подменяет Luna работой Sol. Max, изоляция, review и checkpoint
gate не меняются.

### 4.7 Capability-aware стадии и событийная координация

Multi-agent campaign состоит из bounded стадий с одним владельцем каждой волны:

- в `Классическом` direct owner выполняет independent review точного кандидата;
- в `Экономичном` Luna top-level остаётся operational owner, а для exact
  candidate создаёт одного independent Luna review owner; non-Luna transport
  shell использует доступные direct Luna stages и не выполняет substantive work.

На большом scope reviewer `Классического` может создать read-only lenses по
реальным risk surfaces при доказанной capability вложенной делегации.

Новый direct owner проходит один заранее разрешённый routing guard, один spawn
и event-driven wait до `complete | needs_attention | deadline`. Wait получает
весь остаток переданного stage deadline, а не произвольные десять минут. Ранний
технический timeout только продолжает то же ожидание без `list`, status probe,
commentary или nudge. Независимых owners одной стадии можно ждать общим event
mechanism. Final response owner-а является его handoff; отдельный parent
messaging tool он не ищет. Deadline короче общего ceiling run, чтобы при
неполном review вернуть partial ledger и не потерять evidence.

После material rework режимы с independent reviewer продолжают существующего
owner-а и того же reviewer-а с exact changed candidate. Нормальный путь содержит
один follow-up и один новый event-driven wait без повторного guard/spawn.

Эта схема не скрывает platform limitation и ограничивает дорогую coordination
числом полезных стадий и mode envelope. Она не ослабляет обязательный
review: меняется форма orchestration, а не evidence gate.

Если sandbox разрешает запись в рабочие файлы, но запрещает Git metadata,
последовательный Luna writer не обязан превращаться в read-only генератор
гигантского патча. Coordinator создаёт task-owned shadow tree exact base без
`.git` внутри разрешённого sandbox и закрепляет его за одним owner-ом. Writer правит и тестирует этот
реальный candidate, после чего coordinator строит и механически применяет exact
diff. Созданный coordinator-ом shadow artifact удаляется только после проверки.
Обычно это не Git worktree и поэтому не используется для параллельных authors.
Shadow path выводится прямо из packet identity без поиска ignore/cache path.
Проверенные owned files переносятся в integration checkout одной механической
операцией с последующей отдельной identity-сверкой; полный patch не проходит
через model context и не набирается вручную по частям. Каждый writer получает
этот абсолютный shadow path в materialized packet и использует его префикс во
всех `apply_patch`/write-вызовах; случайная запись в integration checkout
считается ownership defect и требует reconciliation до review или fan-in.

### 4.8 Review packet и переключение

Expensive review packet содержит exact scope/base/candidate identity,
acceptance, integrated diff и source anchors, выполненные checks, material
решения, rejected alternatives, unresolved objections, known defects, negative
evidence и внешние эффекты. Summary служит навигацией; reviewer самостоятельно
читает существенный код и evidence, но не получает сырой transcript всех waves.

Явное переключение режима является barrier между dispatch waves:

1. новые writers не запускаются, active writers доводятся до task-owned commit
   либо честного checkpoint;
2. integration checkout проходит `assert-unchanged`, candidate identities и
   ownership reconciled;
3. mode record получает новый canonical mode и origin `explicit`;
4. новая policy применяется только к следующей dispatch/review итерации; при
   переходе в `Соло` новые Issue Grinder execution-subagents не создаются, а
   сохранённые пакеты ставятся в последовательную очередь текущей модели.

Scope, environment и authority при переключении не меняются. Automatic switch
по проценту квоты, имени новой модели или факту доступности reviewer-а не
выполняется.

## 5. Scope и стратегическая модель

Scope хранится как правило отбора, а не как замороженный список issue. Его
runtime-представление содержит источник выбора, canonical Project/Release или
явные issue refs, применимые статусы и последний подтверждённый снимок. Каждый
full inventory дочитывает Task Manager pagination до `hasMore=false` или
эквивалентного подтверждённого конца; первая страница не является полным scope.
Названия `To Do`, `In Progress` и `In Review` разрешаются в canonical status
refs текущего workspace/project, а не сравниваются как неподтверждённые строки.
Отсутствующий или неоднозначный обязательный status ref останавливает lifecycle
mutations до разрешения контекста.

Coordinator перечитывает scope:

- перед первой диспетчеризацией;
- после обнаруженного изменения Release, relations или статуса;
- после завершения либо блокировки рабочего пакета;
- перед новой волной параллельной работы;
- перед финальным выводом о завершении.

Непрерывный polling не нужен. Если issue исключено из scope, coordinator
перестаёт управлять его Task Manager lifecycle, сохраняет уже созданный
восстановимый checkpoint и решает судьбу локальной реализации по её фактической
полезности для оставшегося scope. Автоматический rollback или включение такой
работы в интеграцию только по инерции не выполняется.

Для каждого текущего scope coordinator различает:

- **Strategic Outcome** — общий ориентир, по которому выбираются локальные
  решения и проверяется связность работы;
- **Human Requirements** — обязательные результаты и ограничения человека;
- **Agent Plan и issue contracts** — конкретная изменяемая декомпозиция и
  формальная задолженность delivery-прогона.

Для `IG-GOAL-08` в существующем run checkpoint удерживается компактная карта
всей обязательной приёмки активного scope: точный исходный ID критерия issue
или общего scope → ссылка на доказательство с проверенным кандидатом и
существенными условиями либо «нет» → оставшийся пробел. Если ID отсутствует,
сохраняется однозначная ссылка на текст критерия, без создания нового ID.
После сжатия или возобновления карту сверяют с current contracts и receipts,
а не восстанавливают только по последнему сообщению. Перед `Done` отдельного
issue проверяют его доказательства и не теряют остальные открытые критерии;
перед остановкой или терминальным решением сверяют весь применимый scope.
Карта не является вторым tracker или новым issue: подробные receipts остаются
в проектном хранилище и доступны по ссылке.

Strategic Outcome может быть шире формальной задолженности. Он не создаёт issue,
acceptance, verification либо blocker и не удерживает run открытым сам по себе.
Если все issue формально завершены, известный стратегический gap сохраняется в
финальном отчёте и может стать входом отдельного planning flow.

### 5.1 Создание Goal

После live scope resolution coordinator изучает весь текущий фронт, общие
требования и связи issue и формулирует проблему верхнего уровня. Goal objective
содержит:

- ключевой стратегический outcome;
- текущее правило scope;
- обязательство довести все входящие issue из трёх рабочих статусов до выхода
  из них;
- существенные ограничения, включая запрет Production;
- наблюдаемое условие завершения;
- краткое обязательство подготовить и проверить итог всего прогона при завершении,
  блокировке или контрольной точке со ссылкой на доступный абсолютный путь
  `references/final-report.md` фактически загруженного skill. Смена статуса Goal
  не заменяет отчёт; перед финализацией reference перечитывается.

Goal создаётся только при выполнении `IG-GOAL-01`. До `create_goal` coordinator
читает текущий Goal. Совместимый незавершённый Goal переиспользуется только при
доказанной continuity текущего run; совпадения selector-а и objective для этого
недостаточно. Его сохранённый selector сверяется с live scope без ложного
обещания переписать objective через недоступный интерфейс. Новый implicit run не
присваивает даже совместимый Goal и не наследует из него explicit autonomy.
Несовместимый либо не принадлежащий доказанно текущему run Goal не
перезаписывается и не завершается ради Issue Grinder. Если платформа не позволяет
завести второй Goal, coordinator сохраняет найденный безопасный frontier как
read-only checkpoint и сообщает несовместимость как точное препятствие Goal
lifecycle; он не начинает требующую Goal изменяющую работу без обязательного
Goal и не присваивает чужую цель.

Если явный run начался с одного issue, coordinator работает без Goal и создаёт
его лишь после роста scope. После создания Goal уменьшение scope не уничтожает
накопленный контекст. Признак явно запущенного run сохраняется отдельно от
самого факта наличия Goal, поэтому одно issue и временно недоступный Goal не
выключают автономность уже начатого прогона.

Стратегический outcome не остаётся одноразовым текстом при создании Goal. Перед
implementation/rework, новой dispatch wave, существенным integration/review
решением, blocker analysis и финальной reflection coordinator заново соотносит
frontier с этим outcome. После compaction, interruption, resume или material
scope change он восстанавливает контекст до следующего такого решения. Для
single-issue run без Goal outcome выводится из current Task, её parent chain и
выбранного scope. Каждый worker packet получает только применимую к нему
проекцию общей цели, вклад пакета, Human Requirements и exact issue contract;
стратегический контекст не расширяет owned scope и не создаёт обязательств.

### 5.2 Контекст итогового отчёта

`IG-GOAL-02/05/07/08` компилируются в `references/final-report.md`.
При создании Goal относительный путь разрешается от фактически загруженного
skill, доступность проверяется. После смены установки недоступный путь
восстанавливается через текущий skill и сохраняется в continuity; существующий
Goal не пересоздаётся ради ссылки, если его objective нельзя редактировать.
Для уже начатого Goal без ссылки обязательство и путь добавляются в сохраняемый
контекст этого run. Без Goal используется тот же контекст финализации.

В принятом для run хранилище coordinator поддерживает компактные существенные
факты: исходную проблему, достигнутые outcomes с evidence, обнаруженные дефекты
и их disposition, ограничения проверок, текущий остаток и resume condition.
Это часть существующего checkpoint, а не второй tracker или обязательная новая
форма. После существенного результата, обнаружения дефекта или отката запись
обновляется; перед compaction/handoff сохраняется. Неустранённый дефект не
исчезает после смены последней карточки. Откат снимает притязание на исправление,
а workaround и очистка fixtures подтверждают только свой наблюдаемый эффект.

Перед финализацией coordinator перечитывает reference, восстанавливает картину
всего run и сопоставляет её с current evidence. Provider получает эту картину,
а не только последний blocker. После provider reflection и любой редакторской
компрессии проверяется именно исходящий текст: сохранены ли существенные
результаты, нерешённые дефекты, пределы проверок, причины, действие пользователя
и resume condition. При потере смысла текст исправляется до публикации.
Вводный вывод проверяется отдельно: реализация candidate с отложенной приёмкой
не доказывает достижение цели, даже если ниже перечислены deferred gates.
Существенные границы effects и deployment сохраняются отдельно от среды проверок:
успешный тест на UAT не объясняет сам по себе, какие среды затронуты изменениями.
В этой проверке сохраняются квалификаторы: ограничение ресурса выбранным режимом
не превращается в общую недоступность; раскрытый дефект не добавляется к
обязательному следующему шагу без основания в current contract.
Новые доступные обязательные действия возвращают в loop; известные gaps вне
scope раскрываются без добавления работы. Формальное завершение и качество
его сообщения проверяются раздельно.

В принятом blocker checkpoint сохраняются также сам опубликованный итог либо
однозначный read-back anchor и его фактологическое основание. Неизменный automatic
turn использует этот checkpoint и выполняет только разрешённый lifecycle effect;
не выпускает новый краткий финал. Существенные изменения требуют нового отчёта
со всей картиной run, а не дополнения только о последнем событии.

`IG-GOAL-09` проверяется отдельным model-forward corpus финализации из
[evaluation](evaluation.md): модель создаёт реальный исходящий текст по истории
работы и выбирает следующий lifecycle effect. Oracle не передаётся генератору;
независимое смысловое ревью сравнивает публикацию с исходными фактами. Сценарии
включают давний дефект с откатом, удачный workaround, последние зелёные проверки,
потерявший результаты draft, пустой scope с residual gap, checkpoint и повторные
automatic turns. Восстановление из сохранённого состояния моделирует compaction,
но не называется проверкой реального платформенного сжатия или 14-часового run.
Профиль, snapshot, вход, исходящий текст, effects и ограничения сохраняются как
evidence; static проверки не подменяют этот слой.

## 6. Основной delivery loop

Одна итерация цикла состоит из следующих смысловых фаз; конкретные tool calls
могут объединяться или переставляться, если сохраняются инварианты:

1. Перечитать live scope и фактические статусы.
2. Применить сохранённый execution mode, определить dependency-ready frontier,
   role profiles и следующий issue, пакет либо candidate wave.
3. Перевести начинаемое `To Do` в `In Progress` и подтвердить изменение.
4. Реализовать результат локально либо через изолированных субагентов.
5. Проверить точную интегрированную версию пропорционально изменению и
   acceptance issue.
6. Подготовить объяснение следующего нетривиального status transition и пройти
   reflection gate.
7. Опубликовать комментарий, изменить статус и перечитать issue.
8. Заново оценить scope, frontier и необходимость следующей итерации.

Режим не создаёт четыре разных lifecycle. Все варианты используют один loop,
а отличаются dispatch policy, reviewer gates и допустимым выходом. В
`Экономичном` режиме восьмая фаза может сохранить `IG-MODE-06` checkpoint и
закончить текущую попытку без terminal claim; остальные режимы продолжают до
terminal path либо настоящего blocker-а. В `Соло` четвёртая фаза всегда
исполняется текущей моделью, а следующий issue или пакет выбирается только после
завершения текущей итерации.

Issue, уже находящееся в `In Progress` или `In Review`, сначала проходит
recovery фактической target branch, task-owned implementation и доступного
evidence. Один старый status не доказывает наличие реализации или успешной
проверки. Неполный `In Review` возвращается в `In Progress` только через
обязательный причинный comment и повторный delivery loop.

Связь `blocked by` оценивается по наличию требуемой реализации в exact commit,
от которого реально будет выполняться зависимое issue, а не только по статусу
карточки или наличию кода в постороннем worker branch. Если реализация уже
доступна либо сначала безопасно интегрируется в эту base, зависимое issue
допускается в frontier; поздний reopen блокирующего issue добавляет повторную
проверку затронутой части, но не восстанавливает блокировку автоматически.

### Внешняя приёмка и продолжение scope

После доступных необходимых проверок coordinator различает завершённую
разработку с внешней приёмкой и незавершённую реализацию/дефект. Первая остаётся
в `In Review`; сам факт недоступной проверки не требует возврата в `In Progress`.
Вторая требует rework либо сохраняет реальную зависимость. Ожидающее issue
остаётся членом active scope, но не занимает execution lane и не удерживает
следующую итерацию, в том числе в Соло.

В существующем issue comment/checkpoint сохраняются проверенный кандидат,
выполненные проверки, оставшийся критерий, конкретная внешняя граница,
необходимое действие и наблюдаемый сигнал возобновления. Новый tracker или Task
для этого не создаётся. Перед dispatch coordinator пересчитывает весь frontier:
независимые задачи и dependents с доступным необходимым contract выполняются;
неизвестный contract или препятствующий дефект сохраняет блокировку соответствующей
работы. Ожидание внешнего ответа не позволяет пропускать доступные проверки.

Без новых evidence, изменения кандидата или внешнего сигнала та же недоступная
проверка не запускается заново при каждом обходе. Изменение upstream вызывает
оценку влияния и повтор затронутых проверок. Финальный blocker-handoff собирается
только после fresh inventory и исчерпания доступной работы всего scope: единый
список внешней приёмки с issue, доказательствами, необходимыми действиями и
resume signals, отдельно — действительно недоступная разработка и её причины.
Он сохраняет обязательные reason-specific объяснения раздела 9 и не объявляет
релиз завершённым. Экономичный checkpoint остаётся отдельным разрешённым выходом.

## 7. Комментарий и status transition как публикационная операция

Для каждого перехода, кроме `To Do → In Progress`, coordinator сначала собирает
проверенные факты. Если текущий доверенный контекст явно указывает Astra (`gpt-6-astra`), он
выбирает native writing и не вызывает Strategic Explainer. Иначе он формирует
semantic request к доступному `$strategic-explainer:strategic-explainer`. В
запрос входят назначение текста, исходная ситуация, exact scope, язык,
существенные ограничения и разрешимые read-only anchors. Внутреннюю методику
provider-а coordinator не воспроизводит.

Astra guard имеет приоритет над наличием provider-а и ранее сохранённым
communication mode и применяется к каждой новой publication unit. Явный
отдельный пользовательский вызов Strategic Explainer остаётся direct request,
но не меняет автоматический маршрут Issue Grinder.

Publication unit целиком остаётся у основного coordinator-а. Worker, reviewer
или scout может вернуть проверенные facts, evidence и resolvable read-only
anchors, но не получает пакет «сформулировать комментарий», не вызывает
Strategic Explainer и не создаёт отдельную Codex task/session ради текста.
Причина архитектурная: рабочий агент уже является built-in child, а его
top-level tool surface может не содержать `collaboration.spawn_agent`; передача
facade внутрь такого child делает обязательный fresh provider child
невозможным. Coordinator принимает evidence handoff и сам вызывает semantic
facade из своей top-level collaboration surface. Поэтому provider наблюдается
как его прямой built-in child, а не как grandchild worker-а или отдельная
пользовательская task.

Terminal result semantic facade закрывает invocation. Coordinator не сохраняет
provider-child как reusable channel и не вызывает на нём `followup_task` или
`send_message`: исправленный caller request и каждая следующая publication unit
получают отдельный fresh top-level facade call. Исключение не нужно даже для
автоматического Goal turn: неизменный уже опубликованный blocker не является
новой unit и повторного facade call не получает.

Тот же communication route применяется к любому другому Task Manager comment,
который Issue Grinder решает опубликовать, а также к blocker-report без Goal
и успешному final-report. Предполагаемая остановка Goal и её объяснения используют
Консультанта либо самостоятельный разбор ведущей Astra, как описано выше. Routine progress journal в Task Manager по умолчанию не
создаётся: дополнительный comment должен иметь самостоятельную пользовательскую
ценность, но его наличие не обходит Strategic Explainer/native contract.

Полученный либо самостоятельно написанный native text проходит reflection:
объясняет ли он честно фактическое состояние и не обнаруживает ли доступную
существенную незавершённую работу текущего scope. Существенной считается работа,
которая нужна для обязательного результата и acceptance текущего issue,
исправления ложного evidence/status, обработки нового участника dynamic scope
или снятия настоящего blocker-а. Strategic Outcome помогает распознать смысл
этой работы, но сам по себе не делает новую работу обязательной. Необязательное
улучшение, новый возможный feature либо косметический hardening не удерживают
текущий run открытым. Ready result не переписывается ради стилистической
вариативности. Если обнаружен существенный пробел в issue contract, status
transition отменяется и issue возвращается в delivery loop.

После reflection публикационная последовательность такова:

1. опубликовать человекопонятный комментарий;
2. подтвердить его read-back;
3. изменить статус с optimistic concurrency;
4. перечитать итоговое состояние issue.

Если статус не изменился после уже опубликованного правдивого комментария,
coordinator сначала reconciles live state и повторяет только недостающий
эффект. Он не дублирует комментарий вслепую. Для тривиального
`To Do → In Progress` выполняются только status mutation и read-back.

Комментарий описывает уже подтверждённые факты, готовность к целевому статусу и
причину перехода, но не утверждает, что mutation уже состоялась. Поэтому
частичный результат `comment committed / status failed` остаётся правдивым и
восстановимым. Unknown comment outcome сначала разрешается чтением thread;
unknown status outcome — повторным чтением issue. Повторная запись допустима
только после доказательства отсутствующего эффекта.

Publication checkpoint сохраняет доступную identity операции: returned comment
ref или idempotency key adapter-а, exact target issue/version и digest готового
текста. Если adapter не предоставляет operation identity, coordinator не
изобретает поле, а reconciles bounded thread window по фактическому результату.
Одинаковая повторная проверка без изменения live state не создаёт нового права
на запись.

Если активна Astra (`gpt-6-astra`) или Strategic Explainer отсутствует, сразу
используется native writing. Если
установленный facade вернул caller error, coordinator исправляет semantic call
по сообщённой причине. Настоящая техническая ошибка provider-а раскрывается как
таковая и не переименовывается в caller error. По умолчанию coordinator
продолжает через native writing, когда проверенные факты позволяют выполнить
тот же communication contract. Допустимый `IG-FLOW-03` ранний stop применяется
только если provider failure одновременно лишил run возможности безопасно
подготовить обязательную публикацию либо выявил более широкую техническую
неисправность, которая реально препятствует продолжению.

## 8. Verification и прозрачное исключение

Обычный путь в `Done` требует evidence по acceptance issue на точной
интегрированной версии. Размер diff или успешный отчёт отдельного субагента не
заменяют эту проверку.

Исключение `IG-GOAL-06` применяется только когда недоступная проверка относится
к детали, которая не ставит под сомнение обязательный результат, основной
acceptance, целостность данных, безопасность или identity проверяемой версии.
Влияние на Strategic Outcome раскрывается как residual risk, но не является
отдельным completion gate. Если такой вывод нельзя обосновать имеющимися
evidence, проверка не считается несущественной.

При применении исключения coordinator сохраняет в issue comment точный
непроверенный фрагмент, причину, основание non-blocking решения и остаточный
риск. Тот же факт переносится в финальный ответ и, при наличии Goal, в его
финальный комментарий. Формулировка «проверено успешно» для пропущенной проверки
запрещена.

## 9. Blocker reflection и завершение

Candidate blocker сначала становится входом новой итерации осознанности:
coordinator перечитывает scope, зависимости, доступные инструменты, локальные
checkpoints и безопасные действия в пределах имеющихся полномочий. Затем
при Goal обязателен описанный выше маршрут Консультанта/Astra; без Goal
объяснение готовится через обычный Strategic Explainer/native route.

Этот reflection и human blocker-report применяются к любому run, включая один
issue без Goal. Наличие Goal меняет только его lifecycle effect; оно не является
условием честного объяснения или поиска самостоятельного продолжения.

Если при формулировании blocker-report обнаружен реальный существенный шаг
текущего scope, публикация blocker-а отменяется и delivery loop продолжается.
Полученный текст и его source basis обязательно проходят отдельную
`post-explanation reflection` по current primary sources: объяснение не является
доказательством собственной блокировки.

Для `IG-GOAL-07` coordinator до первой публикации собирает цельный blocker
handoff:

1. отделяет подтверждённые current причины от каскадных симптомов и дублей;
2. получает общий blocker-report от Консультанта, а ведущая Astra готовит его сама;
3. тем же способом получает для каждой причины отдельное объяснение, связывающее её с
   остановкой цели, конкретной границей самостоятельного устранения и
   ценностью заблокированного шага для стратегического outcome;
4. совместно проверяет report, все reason-specific units и их source basis в
   `post-explanation reflection`.

Неполный reason-specific answer, общая фраза «нужен пользователь» без
фактической границы или необъяснённая ценность шага для цели делают
весь handoff неготовым. Если любой из этих ответов обнаружил безопасный
самостоятельный путь или опроверг одну причину, coordinator отбрасывает весь
устаревший candidate, пересчитывает frontier и продолжает delivery loop.
Принятый комплект публикуется в порядке: общий report, затем отдельные
ответы по каждой причине. Остановка и `update_goal(status=blocked)` допустимы
только после всего комплекта; platform blocker audit по-прежнему не задерживает
пользовательский handoff.
Отсутствие frontier сначала фиксируется как candidate blocker. После принятой
post-explanation reflection полный blocker handoff показывается пользователю,
затем текущая попытка останавливается с точным resume condition независимо от наличия
Goal. Goal получает terminal `blocked` только когда дальнейшее продвижение
действительно требует пользовательского решения или новой authority и выполнен
действующий платформенный blocker audit. Пока платформа ещё не разрешает
terminal `blocked`, Goal остаётся активным, а report честно называет это
расхождение; audit не задерживает объяснение пользователю и не запускает
внутренний бесконечный цикл.

Первая принятая публикация сохраняет blocker checkpoint с fingerprint из
canonical selector/frontier, exact заблокированного effect, current primary
causes, authority boundary, требуемого user action и observable resume signal.
Этот fingerprint отделяет платформенный подсчёт последовательных Goal turns от
повторного доказательства уже установленного blocker-а.

Если платформа автоматически продолжила Goal, а fingerprint совпадает и не
появилось релевантного user signal либо изменения primary state, coordinator:

1. засчитывает очередной audit turn на прежнем принятом checkpoint;
2. не повторяет browser/profile/account discovery, external proof или другой
   blocked action только ради надежды на самопроизвольное изменение;
3. не создаёт новую publication unit, не вызывает Strategic Explainer или
   Консультанта, не повторяет handoff, reason answers или просьбу пользователю;
4. до платформенного порога завершает turn без нового handoff, а при достижении
   порога выполняет только отсутствующий `update_goal(status=blocked)` и
   останавливается.

Релевантный observable resume signal, изменившийся primary state либо другой
fingerprint инвалидирует checkpoint и возвращает run к bounded live
reconciliation. Сам факт автоматического продолжения новым evidence или
разрешением на повтор проверки не является. Status-вопрос пользователя также
не доказывает изменение blocker-а, если он не совпадает с указанным resume
condition.

Нетерминальный checkpoint `Экономичного` режима проходит отдельную проверку и
не маскируется под blocker. Он допустим, когда рекомендуемый candidate,
ownership, checks, defects, deferred gates и resume point уже сохранены, а
дальнейшее существенное продвижение требует отложенного review либо недоступной
неэкономичной capacity. Такой выход не публикует blocker handoff и не переводит
Goal в `blocked`; он сообщает пользователю фактический checkpoint и оставляет
Goal активным.

Каждая recovery-ветка имеет наблюдаемую границу прогресса. Coordinator сравнивает
scope/frontier, object versions, attempted effect, result/error class, available
authority и новый evidence. Повтор допустим, когда изменился хотя бы один из этих
входов либо выбран другой существенный action. Та же комбинация без нового
evidence не считается продвижением: caller error переходит к исправленному
semantic call, повторившаяся provider failure — к native path, unknown write — к
live reconciliation, а исчерпанный safe path — к candidate blocker. Это не
универсальный лимит попыток, а bounded recovery конкретного effect.

Завершение использует fresh full inventory выбранного scope. Отсутствие issue в
`To Do`, `In Progress` и `In Review` является достаточным предметным критерием;
стратегический outcome не превращается во второй независимый terminal gate.
Финальный текст ещё раз проверяется на изменение scope, скрытый существенный
остаток внутри issue contracts и доступное обязательное действие текущего run.
Новая идея, стратегический gap или необязательное улучшение могут попасть в
итоговый отчёт, но не создают новый цикл сами по себе. Только после чистой
переоценки Goal завершается, а пользователь получает причинный итоговый отчёт.

Наличие `In Progress` или `In Review` запрещает terminal completion, но не
запрещает экономичную контрольную точку. После неё тот же run восстанавливает
mode record и checkpoint до нового dispatch.

## 10. Автономность и среды

В явно вызванном run coordinator самостоятельно выполняет все доступные действия
в scope. Target по умолчанию — подтверждённый UAT; staging и другие доказанно
непроизводственные среды также допустимы. Публичность UAT не повышает действие
до approval gate.

Классификация среды берётся из current project context, project delivery profile
и exact target. Общая подпись connector-а, tool schema или platform guard вроде
`deploy to production`, применяемая ко всем публичным hosted deployment, описывает
тип внешнего effect, но не переименовывает подтверждённый project UAT в Product
Production. При таком расхождении coordinator вызывает обычную прямую операцию
для exact UAT target и не просит у пользователя внутреннее подтверждение. Он не
обходит фактический platform approval gate: отказ платформы сохраняется как
provider evidence и обрабатывается по обычному blocker loop, но не превращается
в permission loop поверх уже действующей UAT authority.

Production отклоняется всегда: Issue Grinder не подключается к production
endpoint, не читает production logs/data, не выполняет smoke и не создаёт там
mutation или deployment. Локальное чтение project metadata, необходимое лишь
для классификации target как Production и отказа от него, не считается работой
с самой средой.

Task Manager lifecycle является отдельным control plane Issue Grinder и не
считается product Production deployment только потому, что сам Task Manager
доступен как hosted service. Его writes всё равно ограничены exact scope,
canonical refs, optimistic concurrency и read-back.

UAT предоставляется агенту для разработки, экспериментов и проверки. Полный цикл
изменений реализации, конфигурации, схемы и данных, создания и удаления ресурсов,
тестового доступа и авторизации, воспроизведения сбоев, исправления, восстановления
и очистки выполняется самостоятельно. Временная поломка среды или необходимость
пересоздать тестовые ресурсы не создаёт запрос разрешения. Разумные меры сохранности
и восстановления выбирает агент. Те же послабления относятся к другим non-production
средам в scope; действующие требования Production ими не меняются.

Перед вопросом coordinator восстанавливает предоставленные полномочия. В continuity
сохраняется разрешённый цикл и его границы: смена модели, инструмента, compaction
или resume не превращает его в набор несогласованных технических шагов.

Если необходимый effect выходит за предоставленные полномочия, coordinator сначала
выполняет доступную разрешённую подготовку и проверяет осуществимость всего пути,
включая последующие шаги и очистку. Неясность при препятствии проходит описанный
выше цикл консультаций. Один вопрос человеку охватывает весь необходимый цикл
и его существенные последствия. Новый вопрос допустим только при существенном
выходе за согласованные границы. Отказ не обходится; неизменный automatic turn
не повторяет вопрос. Обязательный platform/tool gate не обходится и не дополняется
внутренним permission loop. Послабления не распространяются на Production.

UAT target определяется и подтверждается перед первым environment effect, а не
превращается в обязательный preflight для работы, которой среда вообще не
нужна. До environment mutation target должен быть однозначно подтверждён как
UAT либо другая непроизводственная среда; неизвестный target не угадывается.

## 11. Multi-agent orchestration

Делегация работы Issue Grinder применяется при наличии минимум двух независимых полезных пакетов
либо когда выбранный режим оправдывает независимого critic/verifier или
постоянный manager loop одной большой работы. Это решение не включает
максимальную автономность в неявном run и не расширяет authority. Если subagent
capability или изолированная writable capacity недоступны, coordinator
адаптирует работу по mode contract: `Классический` может выполнить frontier
последовательно, а экономичные режимы используют доступную serial economical
lane либо сохраняют честный checkpoint. Отсутствие multi-agent surface само по
себе не является blocker-ом. `Соло` не входит в этот resolver: он всегда имеет
ноль execution-subagents Issue Grinder, одну активную execution lane и
последовательно выполняет весь scope на current main profile независимо от
доступной capacity.

Граница topology определяется семантикой и эффектами, а не положением в
физическом дереве сессий. Агент, на котором загружен Issue Grinder, является
execution owner даже когда его создал внешний controller; этот предок не входит
в mode topology. Потомок становится execution-agent режима, если получает
анализ scope, source research, implementation, tests, technical review,
candidate/reduction, integration decision или другую работу, определяющую
delivery-result. Имя, `agent_type` или технический transport этого не меняют.

Рабочая делегация и provider invocation — разные уровни. Coordinator не
делегирует publication unit рабочему subagent-у: тот возвращает только
проверяемый evidence handoff, после чего coordinator отдельно вызывает
Strategic Explainer. Так worker topology не определяет и не ломает внутренний
provider transport. Strategic Explainer и другие agent-backed semantic
interfaces находятся вне mode topology, пока получают только собственный
ограниченный request и не анализируют, не реализуют и не проверяют delivery
scope. Если provider фактически получает такую работу, он классифицируется по
эффектам как execution-agent и обязан соответствовать mode contract.

Явное правило пользователя о topology — точное или относительное число
субагентов, роли, условие делегации либо opt-out — имеет приоритет. Основной
execution owner не входит в названное число execution-субагентов. Выбор `Соло`
отключает только рабочую делегацию Issue Grinder и не отключает Strategic
Explainer либо другой внешний semantic interface. Только отдельная явная
команда пользователя вообще не создавать никаких субагентов запрещает также
service/provider transport.

Без user override coordinator:

1. разрешает live integration target и не подменяет его текущей случайной
   веткой либо dirty root checkout;
2. строит dependency graph и карту поверхностей записи;
3. выделяет conflict-free dependency-ready packets;
4. разбивает campaign на bounded рабочие и проверочные волны с одним owner-ом;
5. до spawn каждого direct owner-а получает model-routing receipt, переносит
   exact model/effort/fork в фактический dispatch и сверяет observed profile;
   nested owner самостоятельно проводит тот же gate для внутренних children;
6. создаёт branches от подтверждённой integration base и выдаёт каждому writer
   отдельные feature branch и Git worktree;
7. оставляет read-only исследователей без worktree;
8. запускает столько packet owners, сколько оправдано режимом, доступной
   capacity и ожидаемой ценностью;
9. ожидает stage handoffs без polling неизменившегося состояния;
10. передаёт compact results предусмотренному independent reviewer-у, но сам
    объединяет изменения;
11. проверяет exact integrated result;
12. после каждого результата или изменения scope пересчитывает frontier.

Routing admission предшествует writer admission: неверная модель должна быть
остановлена до подготовки implementation turn, а неверный worktree — до первой
FileChange. Оба receipts сохраняются в run continuity и evidence.

### 11.1 Event-driven lifecycle владельца стадии

Перед первой волной coordinator один раз разрешает абсолютный путь bundled
routing guard и его стабильный interface. Normal direct-owner trace:

```text
pre-dispatch guard ×1 → spawn owner ×1 → event wait ×1
```

Ожидание получает весь остаток конечного stage deadline, не больше остатка run
ceiling, и завершается только результатом, запросом внимания либо deadline
handoff. Технический timeout раньше stage deadline немедленно продолжает тот же
wait без `list_agents`, status probe, commentary или nudge. Если
platform прерывает event wait новым пользовательским input, coordinator сначала
обрабатывает этот input; это не превращает normal trace в polling loop.

Rework trace переиспользует идентичности owner/reviewer:

```text
follow-up exact changed candidate ×1 → event wait ×1
```

Повторный guard/spawn нужен только при доказанном replacement condition. Каждый
owner применяет тот же lifecycle к собственной внутренней волне и возвращает
родителю один consolidated handoff.

### 11.2 Двухфазный writer admission

Прямой dispatch implementation writer-а запрещён. Для каждой параллельной wave
coordinator исполняет fail-closed protocol:

1. Выбирает exact clean integration worktree и base SHA. Dirty пользовательский
   checkout не stash-ится и не reset-ится: при необходимости создаётся отдельный
   task-owned integration worktree.
2. До запуска writers сохраняет receipt состояния integration checkout через
   `writer_worktree_guard.py snapshot`; все receipt-файлы находятся вне всех
   Git worktree, чтобы guard сам не создавал mutation.
3. Для каждого нового packet вызывает `prepare` с уникальными owner, branch и
   путём вне всех существующих worktree. Existing unfinished checkpoint не
   дублируется: после startup recovery и проверки quiescence `resume`
   переиспользует exact worktree либо восстанавливает linked worktree той же
   branch, после чего checkpoint проходит admission с текущими branch/HEAD и
   явно разрешённым dirty state.
4. Создаёт subagent сначала только для admission turn. В нём запрещены любые
   FileChange/implementation mutations; subagent запускает `admit` своим первым
   Git-действием именно с `cwd` своего worktree и возвращает JSON receipt.
5. Coordinator со своей стороны сопоставляет owner, absolute worktree, private
   git dir, common dir, branch, HEAD, lock и clean/approved-checkpoint state,
   затем проверяет `assert-unchanged`. Только после этого отдельный follow-up
   разрешает implementation.
6. Пока хотя бы один writer активен, integration checkout обычно остаётся
   read-only; параллельная запись coordinator-а требует собственной admitted writer lane.
7. После каждого agent interaction/return и перед fan-in coordinator повторяет
   `assert-unchanged`. Любое Git-visible изменение integration checkout
   останавливает wave:
   новые mutations и fan-in запрещены, активные writers прерываются, состояние
   сохраняется и reconciles без reset/присвоения неизвестного diff.
8. Для fan-in принимается task-owned commit из ожидаемой branch. Uncommitted
   checkpoint сохраняется, но не интегрируется. После объединения coordinator
   проверяет exact candidate; clean worktree удаляется только отдельным
   безопасным cleanup после доказанной достижимости результата.

Двухфазность нужна не как общий стиль prompting, а как barrier перед
параллельным внешним эффектом. OpenAI рекомендует для coding-agent orchestration
явно задавать delegation, acceptance criteria и проверяемые stopping conditions;
одного логического file ownership недостаточно
([официальная model guidance](https://developers.openai.com/api/docs/guides/latest-model)).

Перед чтением guard implementation и `prepare` coordinator дешёво проверяет
writability фактического Git common dir. В read-only Git sandbox заведомо
невозможный worktree flow не запускается: Luna получает read-only patch packet,
возвращает exact candidate, и coordinator механически применяет его только
после завершения owner-а. Это сохраняет последовательную запись и не передаёт
Sol содержательную реализацию.

Каждый packet содержит Strategic Outcome всего scope, вклад конкретного issue
или пакета, применимые Human Requirements, exact локальный scope, owned
surfaces, Agent Plan, исходные данные, ограничения, ожидаемый результат и способ
проверки. Outcome направляет выбор решения, но не разрешает worker-у добавлять
requirements, work или terminal criteria. Сохранившийся task-owned worktree
является checkpoint: после доказанной остановки прежнего владельца он передаётся
новому exclusive writer, а не дублируется.

Изоляция writer-а подтверждается фактическими `git worktree` и branch refs до
первой записи. Указание пути только в prompt субагента не является evidence.
Coordinator не интегрирует исключённый из dynamic scope packet по инерции:
такой checkpoint попадает в fan-in лишь когда его результат независимо нужен
оставшемуся scope, что подтверждено повторной оценкой поверхностей и acceptance.

Profile routing начинается с mode record и заканчивается выбранным mode-файлом:
общая multi-agent mechanics не решает, какая роль получает конкретный packet.
Requirements предполагают штатную доступность выбранных профилей, поэтому
Architecture не вводит автоматическую замену модели, mode switch или
перераспределение quota. Material uncertainty всегда создаёт evidence handoff,
а не бесконечный Luna retry loop.

## 12. Integrity и восстановление

Каждая Task Manager mutation использует текущую версию объекта, а её результат
подтверждается read-back. Unknown write outcome сначала reconciles через live
read; повторять mutation вслепую нельзя.

Run checkpoint хранит только проверяемую continuity: origin, Project/selector
identity, canonical execution mode и его origin,
профили субагентов, terminal state, Goal ref при наличии, task-owned
Git identity, publication/status receipts и незавершённые effects. Формат и
место хранения выбираются по доступной platform capability; Architecture не
требует несуществующий durable store. Возобновление сначала восстанавливает mode
record, затем сверяет checkpoint с live state и не
принимает совместимый Goal либо тот же Release за достаточную lineage. Даже при
отсутствующем durable run checkpoint startup recovery заново ищет Git-artifacts
по `IG-MA-12`: отсутствие записи прошлой сессии не разрешает игнорировать
однозначно связанную со scope ветку, worktree, commit или локальный diff.

Git integration принимает только task-owned изменения с понятным происхождением.
Чужие или пользовательские изменения не очищаются, не reset-ятся и не
присваиваются run. При interruption сохраняются ветки, worktree, результаты
проверок и незавершённые эффекты Task Manager, достаточные для безопасного
возобновления.

Явная отмена пользователем немедленно прекращает новые изменяющие действия
этого run. Coordinator сохраняет проверяемые checkpoints и фактическое
состояние, но не выдаёт отменённый run за `complete` или `blocked` и не меняет
Task Manager cancellation statuses от имени Issue Grinder.

## Соразмерная проверка и проектный профиль

`IG-VERIFY-01`–`IG-VERIFY-07` реализуются общим для всех режимов выбором по
влиянию изменения. Уровни — область доказательства, а не обязательная лестница:
изменение подтверждает конкретный outcome и риски; интеграция — совместную
работу; полный Quality Gate — предусмотренную проектом итоговую готовность.
Число задач и объект Release не являются триггерами полного набора. Широта
оценивается по общим зависимостям и затронутым границам, риск — по последствиям
ошибки. Независимый reviewer проверяет достаточность доказательств; его наличие
не добавляет полный Quality Gate.

В SKILL.md остаётся короткий цикл: найти правила → оценить влияние и прежние
результаты → выполнить достаточный набор → после ошибки пересмотреть диагностику
→ сохранить итог и оставшиеся обязательства. Reference `verification.md`
читается при выборе проверок, повторном использовании либо адаптации проекта.
Там объясняются уровни, UAT, подготовка доказательств для Production и адаптация.

Проект может дополнить существующий release profile либо один документ,
например `docs/operations/verification.md`, связанный из AGENTS.md. Имя файла,
новый manifest и отдельный отчёт на каждый шаг не обязательны. Адаптация начинается
с инвентаризации имеющихся проверок: что доказывают, примерная стоимость,
условия запуска. Затем выделяются независимо запускаемые блоки, несколько
правил «поверхность/риск → проверки», полный Quality Gate и условия применимости
результатов. UI может требовать затронутого пользовательского пути, хранение —
целостности и восстановления, доступ — изоляции и revoke; это примеры, а не
универсальные обязательные команды. Правила уточняются по лишним повторам и
реально пропущенным дефектам, без предварительной классификации каждого файла.

Результат сохраняет проверенный артефакт/кандидат, версию проверок, существенные
условия среды, итог и ссылку на подробный журнал в принятом проектом хранилище.
Агент использует компактный итог, читая raw log по необходимости. Версия продукта
и тестового инструментария различаются: исправление экспортера требует проверки
достоверности затронутых измерений, но не автоматически всех прежних сценариев.
Применимость к новому кандидату обосновывается влиянием diff и условий; старый
результат не переименовывается в новый запуск. Если проект требует exact-candidate
повтора, это требование нельзя отменить ссылкой на экономию.

Полный Quality Gate запускается по пользовательскому запросу, при широком или
высокорисковом изменении либо подготовке production-ready evidence. Основной
дорогой прогон проводится после готовности кандидата; ранние проверки рисков
остаются допустимыми. При повторных сбоях сначала меняется диагностика. Нет
обязательного полного повтора при публикации в UAT или лимита «не больше двух».
Промежуточная нестабильность UAT допустима по назначению среды; известный дефект
обязательного результата не превращается в успешную приёмку. Оставшиеся
обязательства сохраняются в существующем плане/результате scope, без автоматического
создания новых Tasks и без скрытого расширения terminal scope.

Перед последующим Production-выпуском нужен действующий полный результат;
неизменный проверенный UAT-артефакт не требует повторной матрицы только из-за
перехода к выпуску. Отличия среды могут требовать отдельных проверок уполномоченным
владельцем выпуска. Grinder сам Production не читает и не изменяет.

## 13. Трассировка и наблюдаемая проверка

| Level 1 | Архитектурный механизм | Наблюдаемое evidence |
|---|---|---|
| `IG-FLOW-*` | delivery loop, publication transaction, live read-back | корректная последовательность статусов и причинные комментарии без ложного completion |
| `IG-GOAL-*` | strategic synthesis, persistent execution context, Goal lifecycle, blocker/final reflection, `final-report.md` | Strategic Outcome направляет локальные решения без новой задолженности; Goal завершается после fresh empty active scope даже при известном strategic gap; исходящий итог сохраняет outcomes и остаток всего run, без повторной публикации на неизменном continuation |
| `IG-SCOPE-*` | selector-as-predicate и контрольные refresh points | новые и исключённые issue учитываются до terminal result |
| `IG-AUTO-*` | explicit-mode gate, полный UAT цикл и границы согласования | нет Production access; разрешённая UAT работа не ждёт рутинного approval |
| `IG-MODE-*` | однократный resolver, профили субагентов, mode-specific dispatch/review/checkpoint и semantic topology boundary | по умолчанию всегда `Соло`; другие режимы только явно; профиль основной сессии не определяется и не ограничивает запуск; `Соло` сохраняет current profile и ноль Issue Grinder execution-subagents; `Экономичный` только явно; режимы не дрейфуют |
| `IG-HELP-*` | ранний fast path и компактный `mode-help.md` | чистая справка объясняет четыре режима и default без Task Manager, Goal, title mutations или subagents |
| `IG-MA-*` | dependency-ready packets, isolated writers, integration owner, profile routing и capability-aware stages | параллельные writers изолированы; independent review применяется только там, где его требует contract |

Группированная таблица является только обзором. Точная coverage map связывает
каждый отдельный `IG-*` как минимум с одним runtime surface и одним наблюдаемым
evaluation scenario.
Отсутствующий exact ID считается пробелом компиляции, но совпадение текста или
ID само по себе не доказывает поведение.

Целевой release gate состоит из четырёх слоёв; их текущий фактический статус
фиксируется в `evaluation.md`, а описание слоя не считается доказательством его
исполнения:

1. **Static contract.** Проверяет frontmatter, manifest, ссылки, уникальность и
   полноту `IG-*`, разрешимость references, отсутствие скрытой второй policy и
   byte identity source → Marketplace → installed cache.
2. **Deterministic harnesses.** Получают структурированное синтетическое
   состояние, scripted tool results и fault injection, затем проверяют
   required/forbidden decisions и их порядок. Blocker/writer trace остаётся в
   `scripts/issue_grinder_trace_harness.py`, а mode resolver, profile
   профили субагентов, economical exit и switch barrier — в
   `scripts/issue_grinder_mode_harness.py`. Тот же mode harness
   проверяет матрицу model × число live задач, явный выбор, continuity,
   отклонение удалённых режимов и обязательные review/checkpoint gates.
3. **Independent model-forward evaluation.** Запускает реальный skill на
   синтетическом Task Manager и временном Git repository. Детерминированные
   assertions проверяют effects, а отдельный evaluator — стратегический смысл,
   фактологичность и понятность публикационного текста. Generator не получает
   expected answer или rubric с подсказкой нужного решения. Узкий repository
   runner `scripts/issue_grinder_mode_loading_smoke.py` отдельно запускает три
   fresh read-only сессии и по command-execution trace доказывает, что после
   общего resolver-а агент читает только выбранный mode-файл; обращение к
   соседнему файлу либо всему каталогу закрывает case.
   `scripts/issue_grinder_solo_topology_smoke.py` создаёт локальный synthetic
   scope без Task Manager и publication unit, затем доказывает по root trace,
   что одна Solo-сессия сама выполнила анализ, изменение, тест и self-review без
   `spawn_agent`, `create_thread`, `fork_thread` или другого execution-child
   dispatch. Отдельный provider разрешён общим contract, но намеренно не нужен
   этому case, поэтому любой потомок в нём однозначно является лишней рабочей
   делегацией.
4. **Fresh installed-plugin smoke.** После упаковки plugin проверяется в новой
   Codex-сессии с live synthetic UAT: activation, dependencies, полный workflow,
   Marketplace/cache identity и отсутствие второй implicit delivery authority.

Минимальный fault/scenario corpus включает:

- direct explicit, indirect implicit с selector-ом, implicit без selector-а,
  follow-up, negative routing и boundary prompts;
- чистая и узкая справка о режимах/default/различиях без Task Manager, Goal,
  title mutations, delivery refs и subagents; смешанный help+delivery prompt
  сохраняет обычные scope и authority gates;
- explicit natural-language mode override, Solo default без определения основного профиля, persistence через continuation/model
  change и safe explicit switch;
- `Соло` для одного и нескольких issue с exact current profile, одной
  последовательной execution lane, отсутствием Issue Grinder worker delegation
  и допустимым отдельным Strategic Explainer provider; конкретный
  `Классический`, где Sol/controller делает почти всё, а
  Luna получает только тривиальные packets
- Solo default без проверки основного профиля, explicit role override и
  неизвестное cross-family ordering без догадки;
- zero/one/multiple issue, рост и сокращение scope, late matching issue,
  pagination и concurrent status change;
- недоступный Task Manager adapter и навязанный платформой approval, который не
  превращается во внутренний permission loop;
- совместимый и несовместимый активный Goal, доказанная continuity против одного
  совпадения selector-а, single-issue explicit checkpoint и новый implicit run;
- платформенный blocker audit, включая принятый report при отложенной Goal
  mutation, автоматические продолжения до platform threshold без повторного
  profile/account discovery, публикации или просьбы пользователю и единственный
  `update_goal(status=blocked)` на достигнутом пороге;
- каждый lifecycle transition, `comment committed / status failed`, оба
  unknown outcomes, version conflict и защита от duplicate comment;
- реализацию `blocked by` в integration base, код только в постороннем worker
  branch, поздний reopen и targeted recheck;
- отсутствующий Explainer, caller error, technical failure, reflection finding
  и native continuation; попытку продолжить завершённый provider-child через
  `followup_task`/`send_message` вместо нового facade call;
- non-material verification gap и соседний material gap, где исключение
  запрещено;
- public UAT, неизвестный target, Production alias, попытку production read,
  расхождение project UAT с общей provider-меткой `production`, единый согласованный цикл
  с успешным/неуспешным memory read-back, future equivalent operation и
  несовпадающую категорию;
- synthetic substitute для real data/recipient и настоящий high-risk внешний
  effect, требующий selector-а;
- независимые и конфликтующие writer surfaces, недоступных subagents, worker
  interruption, Luna return и exact integrated verification;
- optional improvement при финальной reflection, который попадает в отчёт, но
  не создаёт бесконечный run;
- повтор recovery с тем же progress fingerprint, changed-input retry, доступный
  fallback и переход к candidate blocker после исчерпания safe path.

Hard invariants — отсутствие Production access и Backlog mutations, корректный
Goal gate, обязательный comment, exclusive writable worktree, отсутствие blind
retry и task lifecycle только от coordinator-а — имеют нулевую терпимость.
Semantic quality оценивается отдельно и не может компенсировать нарушение hard
invariant. Механический regression из реального прогона сводится к минимальному
синтетическому deterministic case; ошибка strategy, language understanding или
review остаётся model-forward case, а не имитируется fake state machine.
Проверка наличия терминов в файлах не заменяет model-forward run.

## Условная загрузка и краткое описание

Description содержит только delivery с выбранным Task Manager scope, справку о режимах и
исключение Backlog/status/planning. Общий execution-modes сохраняет resolver, root
admission, continuity, authority и evidence; multi-agent-routing хранит прежние
профили субагентов, receipts, owner coordination и review packet без изменения профилей. В
Соло этот reference не загружается: работает текущий root, ноль execution-subagents. При
явном переходе из Соло multi-agent-routing читается до профильного решения. Local
evaluation имеет отдельный условный entrypoint; ограничения среды, routing, review и
final gate сохраняются, способ чтения файлов не предписывается.
