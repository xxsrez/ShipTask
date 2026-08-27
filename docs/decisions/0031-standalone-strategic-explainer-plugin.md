# 0031. Strategic Explainer как самостоятельный plugin

Статус: частично заменено ADR-0033, 2026-08-27. Distribution сохраняется;
fail-closed logical dependency заменена только для ShipTask, а Task Composer
остаётся под собственным contract. См.
[ADR-0033](0033-terminal-provider-and-optional-shiptask-routing.md).

Изменяет distribution-часть
[ADR-0011](0011-separate-shiptask-plugin-distribution.md),
[ADR-0012](0012-strategic-explainer-as-portable-subagent-role.md) и
[ADR-0023](0023-task-composer-as-planning-sibling.md). Provider boundary из
[ADR-0030](0030-opaque-strategic-explainer-provider-boundary.md) сохраняется.

## Контекст

Strategic Explainer является generic read-only communication skill и полезен
вне Task Manager delivery. Его упаковка внутри `ship-tasks` заставляла
устанавливать delivery workflow ради самостоятельной работы с объяснениями и
связывала независимый runtime с чужим release cycle.

Codex plugin manifest описывает компоненты одного plugin, но не поддерживает
plugin-to-plugin dependency или автоматическую установку другого Marketplace
package. `agents/openai.yaml` поддерживает только зависимости от MCP tools.

## Решение

- `strategic-explainer@srez-marketplace` становится отдельным installable
  plugin и содержит только runtime source `strategic-explainer/`.
- Его qualified skill — `$strategic-explainer:strategic-explainer`.
- `ship-tasks@srez-marketplace` содержит только `ship-tasks` и
  `task-composer`; provider contract в этот package не копируется.
- ShipTask и Task Composer используют Strategic Explainer как logical runtime
  dependency. Они называют точный qualified skill в opaque client protocol.
- Автоматическая установка не имитируется. Если effective contract требует
  Explainer, а plugin недоступен, зависящие comment/status/Epic write остаются
  незавершёнными по существующим fail-closed требованиям; независимая безопасная
  работа может продолжаться.
- Repository source остаётся в `strategic-explainer/`, а Marketplace и
  installed cache являются отдельными byte-identical distribution copies.
  Standalone user-level duplicate не создаётся.

## Последствия

Explainer можно устанавливать и использовать без ShipTask. ShipTask требует две
явные установки — собственный plugin и Strategic Explainer — но не дублирует
runtime и не расходится с ним по версиям. Marketplace UI и документация должны
прямо сообщать эту зависимость, поскольку manifest не может обеспечить её сам.

## Проверка

- repository validator запрещает `skills/strategic-explainer` внутри
  `plugins/ship-tasks` и требует отдельный Marketplace package;
- source, Marketplace copy и installed cache Strategic Explainer сравниваются
  побайтно;
- fresh Codex session видит `$strategic-explainer:strategic-explainer` и не
  видит прежний `$ship-tasks:strategic-explainer`;
- ShipTask без Explainer проходит fail-closed capability scenario, а с
  установленным plugin создаёт fresh provider invocation по opaque protocol.
