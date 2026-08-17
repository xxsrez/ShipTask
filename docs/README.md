# Документация ShipTask

Начните с [обзора](overview.md), чтобы понять назначение и границы skill.

## Specification

- [Ship Tasks](specs/ship-tasks.md) — канонический Task Manager-only workflow
  для explicit и natural-language delivery: single без Goal, batch с Goal,
  project-memory context, per-Task targeted gates и review-batch gates до
  automatic acceptance и terminal evidence.

## Decisions

- [0001: Task Manager-only skill](decisions/0001-task-manager-only.md) —
  единственный authoritative task source и граница project context.
- [0002: Managed delivery report внутри Task](decisions/0002-managed-delivery-report-in-task.md)
  — историческое решение о report block в description, заменённое ADR-0003.
- [0003: Delivery reports только как Task comments](decisions/0003-delivery-reports-as-task-comments.md)
  — исторический comments-only contract без изменения description; его
  capability-optional часть заменена ADR-0006.
- [0004: Autonomous continuation и release authority](decisions/0004-autonomous-continuation-and-release-authority.md)
  — task-local defer вместо остановки run, automatic non-production releases и
  explicit-only production boundary.
- [0005: Automatic terminal acceptance](decisions/0005-automatic-terminal-acceptance.md)
  — terminal-ready Tasks автоматически переходят в Done; feedback возвращается
  через reopen или новую Task, без blocking human-acceptance round-trip.
- [0006: Delivery comment как обязательный terminal effect](decisions/0006-delivery-comment-as-terminal-effect.md)
  — после появления native comment tools завершение Task требует
  опубликованного и перечитанного `COMPLETED` report до перехода в Done.
- [0007: Delivery policy и project memory принадлежат ShipTask](decisions/0007-delivery-policy-and-project-memory.md)
  — adapter / policy / context layers, implicit routing, single/batch modes и
  граница Memories как selector/profile, а не live task state.

## Reference

- [Task Manager adapter](reference/task-manager-adapter.md) — точный discovery,
  identity, lifecycle, concurrency и текущие capability gaps OAuth/MCP
  connector.
- [Project memory contract](../ship-tasks/references/project-memory.md) —
  runtime-схема current scope и project profile, precedence, bootstrap,
  freshness, alarms и cross-surface ограничения.

## Guides

- [Разработка и проверка](guides/development.md) — безопасный цикл изменения
  skill и локальные проверки.

## Reports

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
