# Документация ShipTask

Начните с [обзора](overview.md), чтобы понять назначение и границы skill.

## Strategic vision

- [Strategic Explainer](strategic-explainer.md) — implementation-independent
  продуктовая цель, место между technical evidence и решениями основного
  агента, устойчивые требования и quality bar стратегического объяснения.

## Specifications

- [Ship Tasks](specs/ship-tasks.md) — канонический Task Manager-only workflow
  для explicit invocation и natural-language delivery с однозначным Task
  Manager anchor: single и release без Goal, Goal только для массовой
  имплементации минимум двух Tasks, constitution-first требования, обязательные
  comments, видимые acceptance incidents, свобода выбора инструментов и
  фактическая классификация приёмки.
- [Strategic Explainer](specs/strategic-explainer.md) — общий contract
  обязательного problem gate, bounded read-only strategic discovery и свободного
  объяснения без mutations, status decisions и новой authority.

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
  — общий sibling-skill поставляется в том же plugin и применяется в новом
  default-субагенте без выдачи за неподдерживаемый plugin-defined custom agent.
- [0013: Strategic Explainer для всех ShipTask report narratives](decisions/0013-strategic-explainer-for-shiptask-report-narratives.md)
  — каждый новый success/failure/blocker Task comment получает объяснение через
  Explainer contract, а blocking handoff имеет отдельный communication barrier.
- [0014: Problem-first и bounded strategic discovery](decisions/0014-problem-first-bounded-strategic-discovery.md)
  — caller обязан передать решаемую проблему, а свежий Explainer сам находит
  релевантный Epic/design/vision через bounded read-only tooling и возвращает
  проверяемый source basis.
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

## Reference

- [Task Manager adapter](reference/task-manager-adapter.md) — точный discovery,
  identity, lifecycle, concurrency, текущие возможности и границы connector.
- [Strategic Explainer evaluation](reference/strategic-explainer-evaluation.md)
  — critical fidelity/authority gates, lossless-by-relevance audit, scoring
  rubric и обязательные regression cases.
- [Проверка классификации `In Review`](reference/shiptask-review-disposition-evaluation.md)
  — decision-level cases для task-contract conflict, proven failure,
  verification blocker, incident persistence и Goal behavior.
- [Project memory contract](../ship-tasks/references/project-memory.md) —
  runtime-схема current scope и project profile, precedence, bootstrap,
  freshness, alarms и cross-surface ограничения.

## Guides

- [Разработка и проверка](guides/development.md) — безопасный цикл изменения
  skill и локальные проверки.

## Reports

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
