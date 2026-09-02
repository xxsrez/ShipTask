# Обзор ShipTask

ShipTask — Task Manager-only delivery policy. Он доводит выбранную Task или
batch до фактически подтверждённого результата и отражает этот результат в
Task Manager понятным человеку образом.

```text
Task Manager skill  = технический адаптер
ShipTask skill      = требования к delivery result
Task Composer       = постановка и planning graph в Backlog
Scope Reviewer      = независимый обзор и безопасный repair Agent Plan
Project memory      = selector и project-specific context
Strategic Explainer = stateless API независимого объяснения
```

## Documentation as source

[Философия проекта](philosophy.md) задаёт общую модель свободы агента,
владельцев решений и смысловой компиляции. [Source model](skills/README.md)
применяет её технически и разделяет repository на независимые пакеты
`docs/skills/<skill>/`. У каждой entity три независимых source-документа:
user-owned `overview.md` с общим описанием цели, user-owned `requirements.md` с
набором требований и agent-owned `architecture.md` с дополнительными
инструкциями достижения. Документы соседних skills не смешиваются. Runtime
`SKILL.md` компилирует применимый смысл всех трёх входов. Изменение Overview или
Requirements требует явного поручения пользователя обновить соответствующий
документ; Architecture агент развивает в пределах разрешённой задачи.

## Constitution-first подход

Текущий contract задан [ADR-0018](decisions/0018-outcomes-not-tool-choreography.md)
и [ADR-0019](decisions/0019-goal-only-for-multi-task-implementation.md), а
reporting contract —
[ADR-0020](decisions/0020-visible-acceptance-incidents-and-required-comments.md).
[ADR-0021](decisions/0021-requirements-as-agent-constitution.md) распространяет
этот принцип на agent topology, context и evaluation, а
[ADR-0022](decisions/0022-mandatory-independent-strategic-explainer-for-comments.md)
сохраняет default-требование отдельного Explainer перед каждым комментарием.
[ADR-0024](decisions/0024-adaptive-multi-agent-execution-by-default.md)
задаёт automatic delegation только при отсутствии user rule, natural-language
exact/relative/role/conditional constraints и отдельный worktree каждого
implementation writer, а
[ADR-0025](decisions/0025-cost-aware-subagent-profiles.md) направляет только
genuinely simple packets на Luna Max и эскалирует material uncertainty на
current profile. Они уточняют
[ADR-0017](decisions/0017-constitution-first-runtime-contract.md).
Периодические UAT releases разумными batch-группами, а не после каждой Task,
закреплены [ADR-0026](decisions/0026-periodic-uat-batch-releases.md).
Строго ограниченный weaker `Done` после независимой критической проверки exact
кодовой базы закреплён
[ADR-0027](decisions/0027-critical-codebase-acceptance.md).
Разделение `blocked by`, доступности интегрированной реализации и terminal
acceptance закреплено
[ADR-0028](decisions/0028-integrated-implementation-satisfies-blocked-by.md).
Fresh clean Strategic Explainer API и обязательная reflection-проверка safe
frontier до окончательного blocker claim закреплены
[ADR-0029](decisions/0029-fresh-strategic-explainer-and-blocker-reflection.md).
Самостоятельная Marketplace-поставка Strategic Explainer и первоначальная
logical dependency закреплены
[ADR-0031](decisions/0031-standalone-strategic-explainer-plugin.md).
Terminal ordinary provider и current ordinary-or-native routing
ShipTask закреплены
[ADR-0033](decisions/0033-terminal-provider-and-optional-shiptask-routing.md).
Вместо большого универсального сценария runtime содержит несколько обязательных
результатов и жёстких границ. Агент свободен выбирать порядок, инструменты,
реализацию, декомпозицию и число попыток; delegation следует явной политике
ADR-0024.

Неподвижны следующие требования:

- пользовательский outcome важнее Goal, plans и внутренней отчётности;
- несколько независимых safe lanes по умолчанию получают автоматически
  выбранных субагентов и одного integration owner;
- explicit user topology rule свободным языком имеет приоритет: можно задать
  exact/relative count, role scope, общий или узкий opt-out и condition; root
  agent не считается названным субагентом;
- user-selected subagent profile имеет приоритет; без него genuinely simple
  implementation/research packets получают Luna Max, остальные рабочие packets
  наследуют current model/effort, а Strategic Explainer не входит в caller
  profile routing и вызывается только через собственный semantic facade;
- при доступной host title capability доказанная первая Codex task с catalog
  placeholder после live scope resolution получает не более одной best-effort
  попытки короткого `ShipTask · ...` title; meaningful title и последующие turns
  не переименовываются, а отсутствие/failure capability не блокируют delivery;
- Luna не занимается recovery: ambiguity, surprising environment или proof gap
  возвращают packet current profile без повторного Luna loop;
- общее «без субагентов» означает ноль субагентов во всём run, а узкое правило
  изменяет только названную роль или условие;
- каждый concurrent implementation writer работает в собственной feature branch
  и собственном Git worktree; writable worktree не разделяется между writers;
- interrupted task-owned worktree/branch после доказанной остановки прежнего
  writer подхватывается следующей сессией и продолжается, а не дублируется;
- `blocked by` открывает dependent implementation после fan-in нужного upstream
  contract в exact integration candidate, а не после `Done` blocking Task;
- Task Composer переносит применимую часть стратегического смысла Epic в каждую
  child Task, а ShipTask перед implementation перечитывает current Epic и
  передаёт bounded context исполнителю/reviewer;
- Epic задаёт общий outcome и quality bar, но не расширяет exact child scope,
  selector или authority и не является completion evidence;
- pending upstream acceptance сохраняет её non-terminal, но не удерживает
  dependent Tasks вне runnable frontier; late attributed defect инвалидирует
  только использующие нарушенный contract downstream results;
- status Task соответствует текущим фактам;
- обычный старт `To Do → In Progress` не создаёт комментарий;
- существенный status transition сначала получает понятный native comment и
  comment read-back;
- каждый создаваемый ShipTask-комментарий, пока effective rule не отключает
  Explainer, до публикации проходит его semantic facade;
- каждый Task/scope report, blocker explanation и final получает отдельный
  semantic call; routine chat/progress его не запускает;
- client передаёт только назначение, исходный вопрос, exact scope, язык,
  material constraints и resolvable source anchors, не читает provider
  contract, не пишет candidate и не улучшает ready text;
- material blocker также получает comment, даже без status change;
- native comments являются гарантированной adapter capability и всегда
  сопровождают material lifecycle reporting;
- acceptance incident немедленно виден в chat, durable Task history и final
  run report, даже если defect исправлен в том же run;
- агент сам выбирает и меняет инструменты, способ диагностики и приёмки;
- сбой одного средства сам по себе ничего не доказывает и не обязывает чинить
  именно его;
- acceptance не ослабляется ради удобства; единственное явное исключение —
  `critical-codebase-accepted` после полного gate ADR-0027, причём непроведённая
  functional check остаётся честно видна;
- для каждой Task выполняется лёгкий targeted gate, а совместимые candidates
  периодически проходят один thorough review-batch gate и один exact UAT deploy;
- UAT — обычный разрешённый non-production effect после проверки target, без
  отдельного approval; production остаётся отдельной authority boundary;
- явный общий user override отключает всех субагентов для всего run;
- пока effective user rule не отключает comment Explainer, основной агент не заменяет отдельного Strategic
  Explainer собственной редактурой и не публикует комментарий без
  независимого прохода;
- до окончательной блокировки ShipTask читает fresh explanation как reflection
  input, заново проверяет safe frontier и продолжает при подтверждённом пути,
  не выдавая wording Explainer за evidence или authority;
- production и другие sensitive effects сохраняют явную authority boundary.

## Запуск

ShipTask активируется явным `$ship-tasks` или delivery intent с exact Task
Manager anchor: существующей Task, выбранным Project/Release/current scope.
Явная команда создать ровно одну Task и сразу выполнить её образует single
create-and-deliver.

Обычная просьба исправить код без Task Manager anchor, status/audit/explanation,
planning и backlog capture ShipTask не запускают.

Planning и backlog capture с Task Manager intent принадлежат Task Composer. Он
оставляет один independently deliverable outcome одной Task, а составной
outcome оформляет как Epic с problem-first описанием через Strategic Explainer,
конкретными подзадачами, live Labels и semantic relations. Это planning-only
projection: новые элементы остаются в `Backlog`, а unknown current Release
опускается без guess. Task type хранится в Label/hierarchy и не дублируется
префиксом `BUG:`/`EPIC:` или эквивалентом в title. Шаги плана не становятся
Tasks механически: decomposition следует independently verifiable outcomes, а
каждая child Task получает компактную проекцию своего вклада и применимых
strategic constraints/non-goals.

Обзор созданного плана и текущего Release принадлежит Scope Reviewer. Он
собирает один current snapshot, проверяет его через независимые Luna Max оптики
и возвращает человеку одну целостную картину. Plan/Release review read-only;
явный plan-improvement intent разрешает исправить только Agent Plan при
доказанной сохранности Human Requirements.

- `single`: одна Task, без Goal.
- `batch-implementation`: имплементация/rework минимум двух Tasks, с Goal и
  effective user topology rule либо automatic delegation по default.
- `release`: release уже подготовленного candidate, без Goal.
- project memory меняется только по явной просьбе.

Project, Release, current scope, несколько Tasks и bare invocation являются
selectors, а не автоматическими признаками batch. Goal не создаётся для общего
чтения/приёмки Tasks, commit/push, deploy, smoke или production release.

Exact Task и явно перечисленные refs — closed selectors. Project, Release и
resolved current scope — live selectors: стартовый inventory является audit
snapshot, а не замороженным списком/count cap. Новая matching non-Backlog Task
автоматически входит в delivery и применимый Goal без повторного approval;
Backlog остаётся исключённым.

Task Manager live state всегда перечитывается. Memory не является evidence
текущего status, version, comments, access или runtime result.

## Lifecycle

```text
To Do → In Progress → In Review → Done
                            ↘ In Progress при доказанном дефекте
```

`In Review` нейтрален: candidate предъявлен, но status сам не доказывает ни
успех, ни failure. Manual acceptance не ожидается. При доказанном success
completion comment предшествует `Done`; при строгом gate ADR-0027 отдельный
comment может завершить Task как weaker `critical-codebase-accepted`.

При существенном переходе порядок effects один:

1. понятный Task comment;
2. read-back comment;
3. status write;
4. Task read-back.

Ответ в Codex, Goal, reason code или `description` comment не заменяют.
Существенный status transition считается завершённым только при фактическом
comment и read-back; технический путь к этому результату выбирает агент.
До публикации ShipTask использует выбранный mode: ordinary clean terminal
provider, если он доступен и разрешён, иначе native writing. Основной
агент проверяет material factual conflict и не делает второй rewrite. Opt-out,
отсутствие provider-а или provider failure выбирают native: необходимые lifecycle
facts публикуются по собственному truth contract без provider method или claim
эквивалентного качества и без блокировки transition.

## Приёмка

Обычная приёмка даёт один из четырёх исходов:

- требования текущей Task противоречат друг другу;
- exact candidate доказанно нарушает acceptance;
- доступная проверка не может доказать ни success, ни failure;
- current acceptance и обязательные effects доказаны.

Пятый conditional outcome появляется только после fresh full inventory без
`To Do`/`In Progress`, когда все оставшиеся `In Review` исчерпали normal test
frontier и требуют человека как verifier, а не bounded unlocker. Ровно один
read-only critic с `fork_turns="none"` независимо проверяет exact candidate,
current contracts, code и tests. Grounded approval даёт
`critical-codebase-accepted`; defect возвращает exact affected Task в rework;
inconclusive или stale review сохраняет `In Review`.

При defect comment объясняет причину возврата, затем Task переходит в
`In Progress`, и rework продолжается в том же run. При невозможности приёмки
Task остаётся `In Review`, а comment рекомендует strongest feasible способ
получить доказательство и сравнивает alternatives только при реальном выборе.
История
редакций acceptance и число прошлых попыток сами по себе не являются problem.

## Инструменты и остановка

Skill не выбирает инструменты за агента. Агент может чинить, заменять или
сочетать средства по собственному инженерному решению. Важно только, чтобы
итоговый evidence действительно доказывал current acceptance.

Browser/controller/session switch — диагностический путь, а не repair продукта.
Если exact candidate или server path уже доказал product failure, отсутствие
альтернативного login/MFA не отменяет incident и не останавливает безопасную
in-scope repair. В отчёте product outcome идёт раньше browser/OAuth logistics.

Нет счётчика обязательных повторов и общей последовательности repair. Остановка
означает, что в текущем scope и полномочиях агент не нашёл достаточного
безопасного способа продолжить. Тогда причина, impact и условие возобновления
сообщаются прямо.

## Autonomy, Goal и release

Изолированный blocker одной Task не останавливает независимую runnable работу.
Goal используется только для прогресса массовой имплементации минимум двух Tasks
и остаётся active, пока в этом scope есть незавершённая работа. Он не определяет
Task outcome и число попыток. Release-only run Goal не создаёт; release может
оставаться done criterion уже существующего совместимого Goal.
Для live selector Goal хранит identity/predicate, не стартовый список или count,
и завершается только после fresh full current inventory.

Нужные non-production releases в local/dev/test/QA/UAT/staging/preview/sandbox
разрешены после проверки target. Production, destructive durable-data changes,
secrets/privacy/access-policy changes, external recipients и unbounded cost
требуют явной authority.

Если project context содержит UAT, не деплой каждую bug/Task отдельно по
умолчанию. Собирай разумный integrated batch, запускай его при cadence или
observable trigger и публикуй в UAT один exact candidate с deployment/read-back и
smoke evidence. Отсутствующий UAT receipt — proof gap, а не verified release.

## Источники

- [ShipTask Requirements](skills/ship-tasks/requirements.md)
- [ShipTask Architecture](skills/ship-tasks/architecture.md)
- [Constitution-first ADR](decisions/0017-constitution-first-runtime-contract.md)
- [Outcome, не tool choreography](decisions/0018-outcomes-not-tool-choreography.md)
- [Goal только для массовой имплементации](decisions/0019-goal-only-for-multi-task-implementation.md)
- [Видимые приёмочные инциденты и обязательные comments](decisions/0020-visible-acceptance-incidents-and-required-comments.md)
- [Требования как конституция для агентов](decisions/0021-requirements-as-agent-constitution.md)
- [Независимый Strategic Explainer для каждого комментария](decisions/0022-mandatory-independent-strategic-explainer-for-comments.md)
- [Opaque provider boundary Strategic Explainer](decisions/0030-opaque-strategic-explainer-provider-boundary.md)
- [Automatic delegation, natural-language topology rules и writer isolation](decisions/0024-adaptive-multi-agent-execution-by-default.md)
- [Cost-aware профили субагентов](decisions/0025-cost-aware-subagent-profiles.md)
- [Периодические UAT batch releases](decisions/0026-periodic-uat-batch-releases.md)
- [Критическая приёмка по кодовой базе](decisions/0027-critical-codebase-acceptance.md)
- [Task Manager adapter contract](reference/task-manager-adapter.md)
- [Lifecycle evaluation](reference/shiptask-review-disposition-evaluation.md)
- [Strategic Explainer Requirements](skills/strategic-explainer/requirements.md)
- [Strategic Explainer Architecture](skills/strategic-explainer/architecture.md)
- [Task Composer Requirements](skills/task-composer/requirements.md)
- [Task Composer Architecture](skills/task-composer/architecture.md)
- [Task Composer как planning sibling-skill](decisions/0023-task-composer-as-planning-sibling.md)
- [Scope Reviewer Overview](skills/scope-reviewer/overview.md)
- [Scope Reviewer Requirements](skills/scope-reviewer/requirements.md)
- [Scope Reviewer Architecture](skills/scope-reviewer/architecture.md)
- [Scope Reviewer Evaluation](skills/scope-reviewer/evaluation.md)

Runtime sources — `ship-tasks/SKILL.md`, `task-composer/SKILL.md`,
`scope-reviewer/SKILL.md` и package `strategic-explainer/`. `SKILL.md` Explainer является semantic facade и
admission layer к fresh provider, а text-improvement contract загружается только
terminal subagent. Plugin distribution и installed cache должны быть
byte-identical repository source; standalone user-level copies не используются.
