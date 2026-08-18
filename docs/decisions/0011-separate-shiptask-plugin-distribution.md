# 0011: Separate ShipTask plugin distribution

Статус: accepted. Дата: 2026-08-18.

Заменяет [ADR-0008](0008-plugin-only-runtime-distribution.md).

## Контекст

Bundled distribution помещала `ship-tasks` внутрь installable package
`task-manager@srez-marketplace`. Поэтому пользователь, которому требовался
только OAuth/MCP connector и технический adapter, автоматически получал также
delivery policy с implicit invocation, Goal lifecycle, release authority и
terminal reporting. Удаление standalone user-level дубликата не требовало
связывать эти две независимо выбираемые возможности в одном package.

## Решение

- Репозиторий ShipTask остаётся source of truth для каталога `ship-tasks/`.
- Единственная runtime installation skill — отдельный plugin
  `ship-tasks@srez-marketplace`.
- `task-manager@srez-marketplace` устанавливается отдельно, владеет production
  OAuth/MCP connector и содержит только adapter skill `task-manager`.
- `ship-tasks@srez-marketplace` содержит только skill `ship-tasks` и не содержит `.mcp.json`;
  он не создаёт собственный connector и использует declared MCP dependency
  `task-manager` из отдельно установленного Task Manager plugin.
- Marketplace source skill находится в
  `Srez Marketplace/plugins/ship-tasks/skills/ship-tasks` и должен быть
  byte-identical source из этого репозитория.
- Standalone user-level каталог `~/.codex/skills/ship-tasks` не
  создаётся. Fresh catalog показывает plugin-qualified
  `ship-tasks:ship-tasks`, а Task Manager plugin не показывает
  `task-manager:ship-tasks`.
- Marketplace snapshot и installed cache каждой plugin installation являются
  внутренними lifecycle-копиями и не удаляются вручную.
- После marketplace upgrade и раздельной установки обоих plugins проверка
  discovery выполняется в fresh Codex session.

## Последствия

Положительные:

- connector-only пользователи не получают ShipTask и его implicit routing;
- ShipTask можно устанавливать, обновлять, включать и отключать независимо;
- Task Manager остаётся узким reusable adapter без delivery policy;
- OAuth connection не дублируется: ею владеет только Task Manager plugin.

Ограничения:

- для ShipTask нужны две явные установки: `task-manager@srez-marketplace` и
  `ship-tasks@srez-marketplace`;
- установка только ShipTask не создаёт connector и не даёт Task Manager tools;
- открытая до обновления Codex-сессия может удерживать старый bundled snapshot.
