# Документация ShipTask

Начните с [обзора](overview.md), чтобы понять назначение и границы skill.

## Specification

- [Ship Tasks](specs/ship-tasks.md) — канонический Task Manager-only workflow
  от уже созданных Tasks через обязательный Goal lifecycle, per-Task targeted
  gates и периодические review-batch gates до automatic acceptance и terminal
  evidence.

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

## Reference

- [Task Manager adapter](reference/task-manager-adapter.md) — точный discovery,
  identity, lifecycle, concurrency и текущие capability gaps OAuth/MCP
  connector.

## Guides

- [Разработка и проверка](guides/development.md) — безопасный цикл изменения
  skill и локальные проверки.

## Reports

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
