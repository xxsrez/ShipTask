# Документация ShipTask

Начните с [обзора](overview.md), чтобы понять назначение и границы skill.

## Specification

- [Ship Tasks](specs/ship-tasks.md) — канонический Task Manager-only workflow
  от уже созданных Tasks через обязательный Goal lifecycle до human acceptance
  и terminal evidence.

## Decisions

- [0001: Task Manager-only skill](decisions/0001-task-manager-only.md) —
  единственный authoritative task source и граница project context.

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
