# Предыдущая версия в ExampleNotes

Документ фиксирует provenance переноса, а не делает ExampleNotes policy частью
текущего skill.

## Источники

Состояние изучено 2026-08-11 в
`/workspace/ExampleNotes`.

| Источник | Последнее релевантное изменение | Роль |
|---|---|---|
| `docs/specs/ship-work-release.md` | `e78447ede8c1bbb6c93f949dd9b4f05fd4a7eec8` | Общий execution contract предыдущего поколения. |
| `docs/specs/ship-work-release-project-profile.md` | `9f7490eada68ecc46a29aa2a8fd793b5a7617325` | Structured project commands, environments и evidence. |
| `docs/specs/ship-work-release-task-manager.md` | `9f7490eada68ecc46a29aa2a8fd793b5a7617325` | Provider-neutral task adapter contract. |
| `docs/specs/ship-work-release-linear.md` | `9f7490eada68ecc46a29aa2a8fd793b5a7617325` | Linear mapping и projection protocol. |
| `docs/operations/ship-work-release.md` | `e78447ede8c1bbb6c93f949dd9b4f05fd4a7eec8` | Codex Desktop operator runbook. |
| `docs/operations/ship-work-release-profile.md` | ExampleNotes `HEAD=26442271527842dad6581de032f6c13a88ff2561` | ExampleNotes commands, Sites/UAT target и evidence matrix. |
| `docs/specs/ship-linear-release-v1.md` | `8e8e207d022c27a2a9dd9b68dbc639e448d1d0db` | Упрощённый исполнимый Linear milestone profile. |
| `.agents/skills/ship-linear-release/` | текущий repo-local baseline | Skill, helpers, tests и references старого runtime. |

Каталог `.agents/skills/ship-work-release/` на момент переноса не содержал
tracked source: в checkout оставались только ignored `__pycache__` artifacts.
Поэтому этот проект не заявляет, что портировал отсутствующую runtime
реализацию.

## Что перенесено

- fail-closed authority и read-only preflight;
- complete bounded inventory и dependency-ready frontier;
- single writer на связной write-critical path;
- isolated writable lanes только для независимых scopes;
- различение requested, available, active и sustained capacity;
- immutable result identity и отдельное evidence для task, integration,
  checks и external effects;
- reconciliation перед resume;
- запрет blind retry, destructive cleanup и silent scope expansion;
- separation core workflow от project profile и task-manager adapter.

Эти идеи вошли в текущий baseline и
[v2 proposal](../specs/ship-tasks-v2.md).

## Что адаптировано

| Предыдущая модель | ShipTask |
|---|---|
| Work scope обычно разрешается через task-manager adapter. | Task source условен; authoritative input может быть другим или `N/A`. |
| UAT cut и scope UAT release — основные delivery boundaries. | Review candidate и terminal task outcome не зависят от deployment. |
| Production всегда запрещён конкретным skill. | Внешние эффекты определяет project authority; invocation не расширяет её. |
| Review optional и policy-driven. | Human acceptance предлагается как обязательный v2 gate. |
| Durable run model задаёт большой runtime contract. | Markdown skill остаётся компактным; durable runtime проектируется отдельно. |
| Default flow содержит project profile schema. | До появления generic profile действует awareness contract и alarm. |

## Что не перенесено

- Linear entity mapping, statuses, API/tool calls и projection homes;
- ExampleNotes paths, commands, branches и ownership;
- Sites routes, UAT target, live smoke matrix и production boundary;
- конкретные `shipctl.py` commands и journal schema;
- Goal UI assumptions и Codex Desktop controls, не подтверждённые generic
  runtime;
- historical UAT/CI evidence и product-specific security policy.

Эти части остаются источниками для будущих adapters, но не должны появляться в
`ship-tasks/SKILL.md`.

## Ключевой разрыв предыдущей версии

Старая модель хорошо управляла execution и evidence, но review оставляла
опциональным. Сессия `00000000-0000-4000-8000-3bd4623c02c1` сформулировала
новый bottleneck: очередь человеческой приёмки. Поэтому v2 добавляет
`review-ready`, WIP/backpressure, compact review packet и delta-rework.
