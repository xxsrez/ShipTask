# 0008: Plugin-only runtime distribution

Статус: accepted. Дата: 2026-08-17.

## Контекст

ShipTask одновременно обнаруживался как standalone user skill и как skill
Task Manager plugin. Одинаковый `name: ship-tasks` не объединяет эти источники:
catalog показывает отдельный `ship-tasks` и plugin-qualified
`task-manager:ship-tasks`. Marketplace snapshot и installed cache также могут
отображаться в диагностике как разные filesystem paths, хотя принадлежат одной
plugin installation.

User-level копия дополнительно объявляла Task Manager MCP dependency без
собственного URL, тогда как plugin bundle уже владеет connector configuration.
Две независимые runtime-дистрибуции поэтому создают неоднозначный picker и две
точки обновления без полезного fallback.

## Решение

- Репозиторий ShipTask остаётся source of truth для исходного каталога
  `ship-tasks/`.
- Единственная runtime installation ShipTask — skill внутри plugin bundle
  `task-manager@srez-marketplace`.
- Standalone user-level каталог
  `~/.codex/skills/ship-tasks` не должен существовать и не должен
  обнаруживаться через `skills/list`.
- Runtime skill должен отображаться как plugin-qualified
  `task-manager:ship-tasks`; plugin должен оставаться installed/enabled.
- Marketplace source должен быть byte-identical repository source. При
  изменении runtime payload обновляются manifest version или cachebuster,
  marketplace commit и установленный plugin cache.
- Marketplace snapshot и installed cache — внутренние стадии одной plugin
  installation. Они не считаются отдельными пользовательскими установками и
  не удаляются вручную.
- После удаления standalone копии или переустановки plugin проверка picker и
  model-visible catalog выполняется в fresh Codex session, поскольку текущая
  сессия может удерживать старый snapshot.

## Последствия

Положительные:

- picker получает один logical ShipTask вместо standalone и plugin-qualified
  дублей;
- skill и Task Manager connector обновляются одним marketplace package;
- исчезает standalone dependency warning и отдельный sync contract.

Ограничения:

- исходный ShipTask repository сам по себе не является runtime installation;
- runtime-изменение требует публикации и переустановки marketplace package;
- filesystem paths marketplace snapshot и cache могут оставаться двумя
  физическими копиями одной plugin installation и сами по себе не доказывают
  дублирование logical skill.

## Заменённые положения

Этот ADR заменяет только правила о standalone user-level копии в
[ADR-0001](0001-task-manager-only.md) и формулировку о user-level snapshot в
[ADR-0007](0007-delivery-policy-and-project-memory.md). Их остальные решения
остаются действующими.
