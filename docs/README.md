# Документация ShipTask

Начните с [обзора](overview.md), чтобы понять назначение и границы skill.

## Skill source packages

[Source model](skills/README.md) задаёт единицу исходного кода: отдельный skill
со своими Requirements и Architecture. Требования разных skills не смешиваются;
общими остаются только repository build и plugin distribution rules.

- `$ship-tasks`: [Requirements](skills/ship-tasks/requirements.md) и
  [Architecture](skills/ship-tasks/architecture.md) — канонический Task
  Manager-only workflow
  для explicit invocation и natural-language delivery с однозначным Task
  Manager anchor: single и release без Goal, Goal только для массовой
  имплементации минимум двух Tasks, automatic delegation при отсутствии user
  topology rule, natural-language exact/relative/role/conditional overrides,
  отдельный worktree на каждого
  concurrent implementation writer, resume existing task-owned worktree/branch
  после interruption или смены сессии, Luna Max только для genuinely simple
  packets с эскалацией на current profile, constitution-first требования, обязательные
  comments, видимые acceptance incidents, свобода выбора инструментов и
  фактическая классификация приёмки; лёгкие per-Task gates и периодические
  thorough UAT batch releases одним exact integrated candidate без approval.
- `$ship-tasks:task-composer`:
  [Requirements](skills/task-composer/requirements.md) и
  [Architecture](skills/task-composer/architecture.md) — planning-only Task
  Manager workflow: одна Task либо strategic Epic с конкретными подзадачами,
  переносом применимого strategic context в каждую child Task, live Labels,
  hierarchy, semantic relations, `Backlog` и необязательным current Release.
- `$strategic-explainer:strategic-explainer`:
  [Requirements](skills/strategic-explainer/requirements.md),
  [Architecture](skills/strategic-explainer/architecture.md) и
  [product vision](skills/strategic-explainer/product-vision.md) — общий contract
  stateless API объяснения на уровне исходного вопроса: каждый user-facing unit
  получает clean `fork_turns="none"` invocation на exact
  `gpt-5.6-luna`/`max`, Explainer сам собирает
  strategic context, но продуктом считает понимание читателя, а не отчёт об
  исследовании. Publication text строится из одной главной причинной мысли,
  verification-only source basis остаётся отдельно, а поведение проверяется
  model-forward regression и независимым пересказом. По явному запросу skill выполняет глубокую
  редакторскую реконструкцию без потери смысла. Он ничего не изменяет и не
  принимает решений о статусе или полномочиях.
Документация является исходным кодом. Локальный Level 1 отвечает за «что обязано
быть истинно», локальный Level 2 — за agent-owned «как сейчас этого достигать»,
а соответствующий `SKILL.md` — компактная исполнимая проекция обоих уровней.

## Decisions

- [0001: Task Manager-only skill](decisions/0001-task-manager-only.md) —
  единственный authoritative task source и граница project context.
- [0002: Managed delivery report внутри Task](decisions/0002-managed-delivery-report-in-task.md)
  — историческое решение о report block в description, заменённое ADR-0003.
- [0003: Delivery reports только как Task comments](decisions/0003-delivery-reports-as-task-comments.md)
  — исторический comments-only contract без изменения description; его
  capability-optional часть последовательно заменена ADR-0006 и ADR-0020.
- [0004: Autonomous continuation и release authority](decisions/0004-autonomous-continuation-and-release-authority.md)
  — task-local defer вместо остановки run, automatic non-production releases и
  explicit-only production boundary; blocker analysis уточнён ADR-0010.
- [0005: Automatic terminal acceptance](decisions/0005-automatic-terminal-acceptance.md)
  — terminal-ready Tasks автоматически переходят в Done; feedback возвращается
  через reopen или новую Task, без blocking human-acceptance round-trip.
- [0006: Delivery comment как обязательный terminal effect](decisions/0006-delivery-comment-as-terminal-effect.md)
  — после появления native comment tools завершение Task требует
  опубликованного и перечитанного `COMPLETED` report до перехода в Done;
  availability-ветвь заменена ADR-0020.
- [0007: Delivery policy и project memory принадлежат ShipTask](decisions/0007-delivery-policy-and-project-memory.md)
  — adapter / policy / context layers, implicit routing, single/batch modes и
  граница Memories как selector/profile, а не live task state.
- [0008: Plugin-only runtime distribution](decisions/0008-plugin-only-runtime-distribution.md)
  — историческое решение о bundled distribution, заменённое ADR-0011.
- [0009: Terminal-report capability как preflight barrier](decisions/0009-terminal-report-capability-preflight.md)
  — superseded incident hypothesis; сохранена как история отменённого
  comment-channel fail-fast решения; current adapter guarantee задан ADR-0020.
- [0010: Осмысленная финализация и глубокий компактный run report](decisions/0010-blocker-analysis-and-human-run-report.md)
  — перед любым terminal outcome агент проверяет целостный результат, устраняет
  доступные проблемы и только затем даёт человеку сжатое причинное объяснение.
- [0011: Separate ShipTask plugin distribution](decisions/0011-separate-shiptask-plugin-distribution.md)
  — ShipTask и Task Manager connector устанавливаются как два независимых
  Marketplace plugin; Task Manager package остаётся adapter-only; состав
  ShipTask plugin позднее расширен ADR-0012.
- [0012: Strategic Explainer как переносимая роль свежего субагента](decisions/0012-strategic-explainer-as-portable-subagent-role.md)
  — историческая fresh-subagent implementation; sibling-skill distribution и
  независимая роль сохраняются, а точная topology заменена ADR-0021/ADR-0022.
- [0013: Strategic Explainer для всех ShipTask report narratives](decisions/0013-strategic-explainer-for-shiptask-report-narratives.md)
  — исторический invocation pipeline; отдельный Explainer для каждого
  комментария восстановлен ADR-0022 без прежнего жёсткого формата передачи.
- [0014: Problem-first и bounded strategic discovery](decisions/0014-problem-first-bounded-strategic-discovery.md)
  — сохраняет реальную problem framing, bounded read-only discovery и source
  basis; fixed fields/error/context mechanics заменены ADR-0021.
- [0015: Однократная классификация приёмки](decisions/0015-single-pass-review-disposition.md)
  — историческое основание четырёх исходов приёмки; fixed pass и status/comment
  fallback заменены ADR-0017.
- [0016: Единый действующий контракт lifecycle и отчётности](decisions/0016-current-lifecycle-and-reporting-contract.md)
  — сохраняет нейтральный смысл `In Review` и task-level defect attribution;
  прежнее разделение status/comment effect заменено ADR-0017.
- [0017: Constitution-first runtime contract](decisions/0017-constitution-first-runtime-contract.md)
  — исходное constitution-first решение; обязательная tool-recovery
  последовательность заменена ADR-0018, selector-based Goal policy — ADR-0019.
- [0018: Конституция управляет результатом, а не инструментами](decisions/0018-outcomes-not-tool-choreography.md)
  — текущая граница: skill задаёт качество evidence и lifecycle outcomes, а
  агент сам выбирает технический способ достижения результата.
- [0019: Goal только для массовой имплементации Tasks](decisions/0019-goal-only-for-multi-task-implementation.md)
  — Project/Release являются selectors; Goal создаётся только для реализации или
  rework минимум двух Tasks, а release-only выполняется без Goal.
- [0020: Видимые приёмочные инциденты и обязательные comments](decisions/0020-visible-acceptance-incidents-and-required-comments.md)
  — native comments являются гарантией adapter contract; failed/blocked
  acceptance немедленно видна в chat, сохраняется в Task history и остаётся в
  final report после repair.
- [0021: Требования являются конституцией для агентов](decisions/0021-requirements-as-agent-constitution.md)
  — current requirements обычно задают outcome, evidence и authority boundaries,
  а не agent topology, context envelope, retries или tool choreography; явные
  topology-исключения закреплены ADR-0022 и ADR-0024.
- [0022: Каждый комментарий ShipTask проходит независимый Strategic Explainer](decisions/0022-mandatory-independent-strategic-explainer-for-comments.md)
  — сохраняет default-требование отдельной смысловой проверки каждого
  комментария и запрещает комментарий на обычном старте `To Do → In Progress`.
- [0023: Task Composer как planning sibling-skill](decisions/0023-task-composer-as-planning-sibling.md)
  — отделяет качественную постановку и backlog capture от ShipTask delivery и
  добавляет третий runtime skill в тот же Ship Tasks plugin.
- [0024: Automatic delegation и natural-language topology rules](decisions/0024-adaptive-multi-agent-execution-by-default.md)
  — использует automatic default только без user rule, исполняет exact,
  relative, role-scoped и conditional указания пользователя, изолирует каждого
  implementation writer отдельным worktree и сохраняет буквальный общий
  no-subagent opt-out.
- [0025: Cost-aware профили субагентов](decisions/0025-cost-aware-subagent-profiles.md)
  — сохраняет пользовательский model/effort, направляет только genuinely simple
  packets на Luna Max и требует current-profile escalation без Luna retry loop.
- [0026: Периодические UAT batch releases](decisions/0026-periodic-uat-batch-releases.md)
  — отделяет лёгкую проверку каждой Task от периодического thorough gate и одного
  UAT deploy совместимого exact batch; обычный UAT не требует approval.
- [0027: Критическая приёмка по кодовой базе](decisions/0027-critical-codebase-acceptance.md)
  — разрешает явно маркированный weaker `Done` только при исчерпанном active
  frontier, substantial human verification blocker и независимом fresh-context
  critic-review exact candidate.
- [0028: Интегрированная реализация удовлетворяет `blocked by`](decisions/0028-integrated-implementation-satisfies-blocked-by.md)
  — открывает downstream implementation после доказанного fan-in нужного
  upstream contract, не дожидаясь terminal acceptance blocking Task, и
  локализует позднюю invalidation по contract attribution.
- [0029: Fresh Strategic Explainer и reflection до blocker](decisions/0029-fresh-strategic-explainer-and-blocker-reflection.md)
  — задаёт единый stateless API с clean `fork_turns="none"`, самостоятельным
  strategic discovery, одним publication unit на invocation и обязательной
  повторной проверкой safe frontier до окончательного blocker claim ShipTask.
- [0030: Opaque provider boundary для Strategic Explainer](decisions/0030-opaque-strategic-explainer-provider-boundary.md)
  — оставляет caller только clean invocation protocol, переносит provider method
  за admission gate fresh subagent и запрещает caller-authored candidate,
  internal checklist и self-fallback.
- [0031: Strategic Explainer как самостоятельный plugin](decisions/0031-standalone-strategic-explainer-plugin.md)
  — выносит generic Explainer из ShipTask package в отдельный installable
  plugin и фиксирует исходную logical dependency ShipTask и Task Composer.
- [0033: Terminal ordinary provider и optional routing ShipTask](decisions/0033-terminal-provider-and-optional-shiptask-routing.md)
  — запрещает provider-у становиться caller или создавать agents и задаёт
  current ordinary-or-native routing без lifecycle blocker-а.
- [0034: Luna Max для ordinary Strategic Explainer](decisions/0034-luna-max-for-ordinary-strategic-explainer.md)
  — запускает установленный ordinary provider как clean Luna Max subagent без
  наследования SOL/current profile; без plugin-а ShipTask пишет сам.

## Reference

- [Task Manager adapter](reference/task-manager-adapter.md) — точный discovery,
  identity, lifecycle, concurrency, текущие возможности и границы connector.
- [Strategic Explainer evaluation](reference/strategic-explainer-evaluation.md)
  — observable invocation-isolation, self-discovery,
  fidelity/authority/comprehension gates и regression cases без фиксированной
  scoring ceremony.
- [Task Composer evaluation](reference/task-composer-evaluation.md) —
  observable gates для decomposition, metadata, relations, duplicate safety и
  planning-only authority.
- [Проверка классификации `In Review`](reference/shiptask-review-disposition-evaluation.md)
  — decision-level cases для task-contract conflict, proven failure,
  verification blocker, critical codebase fallback, incident persistence и Goal behavior.
- [Project memory contract](../ship-tasks/references/project-memory.md) —
  runtime-схема current scope и project profile, precedence, bootstrap,
  freshness, alarms и cross-surface ограничения.

## Guides

- [Разработка и проверка](guides/development.md) — безопасный цикл изменения
  skill и локальные проверки.

## Reports

- [Strategic Explainer: сравнение SOL и Luna](reports/2026-08-27-strategic-explainer-luna-comparison.md)
  — paired 20-case blind evaluation, человеческий blind vote и решение
  закрепить ordinary provider на `gpt-5.6-luna` с `max`.
- [Terminal Strategic Explainer и ShipTask routing: evaluation](reports/2026-08-27-terminal-provider-routing-evaluation.md)
  — terminal role/off-role regression, ноль provider descendants, full 20-case
  independent evaluation и четыре install combinations ShipTask.
- [Strategic Explainer: model-forward evaluation из 20 сценариев](reports/2026-08-26-strategic-explainer-20-case-evaluation.md)
  — полный fresh-subagent прогон на 10 сценариях ExampleNotes и 10 сценариях Task
  Manager, найденные дефекты первого кандидата и финальный результат 20/20.
- [Исследование подходов для Strategic Explainer](reports/2026-08-20-strategic-explainer-research.md)
  — official agent guidance, clear-communication и handoff patterns,
  существующие skills, принятые механизмы, отклонённые альтернативы и
  ограничения evidence.
- [Глубокая ревизия ShipTask](reports/2026-08-21-shiptask-deep-contract-review.md)
  — исторический snapshot ревизии до ADR-0017; найденные тогда противоречия и
  проверки, но не текущая fallback policy.
- [Предложение по развитию ShipTask skill](reports/2026-08-16-shiptask-skill-change-proposal.md)
  — целевая граница business policy, explicit/implicit modes, project-memory
  contract, runtime refactor, trigger matrix и согласованный cutover.
- [Предложение по изменению Task Manager skill](reports/2026-08-16-task-manager-skill-change-proposal.md)
  — handoff для adapter-only marketplace skill: что удалить, что сохранить,
  какие metadata обновить и как проверить совместный routing с ShipTask.
- [Как на практике разрабатывают с coding agents](reports/2026-08-11-agentic-development-in-practice.md)
  — срез по восьми выступлениям, engineering cases, HN/Reddit,
  surveys и field studies; consensus, разногласия и implications для ShipTask.
- [Production-grade agentic delivery systems](reports/2026-08-11-agentic-delivery-systems-landscape.md)
  — подробный срез архитектурных принципов, рынка, protocols, durability,
  security, evals и возможной roadmap для ShipTask.
- [ShipTask и работа с несколькими AI-агентами](reports/2026-08-11-multi-agent-workload-ideas.md)
  — summary доклада Николая Сенина и exploratory ideas для task typing,
  review batching, high-touch routing, guardrails и удобоваримого
  verification/review report.
