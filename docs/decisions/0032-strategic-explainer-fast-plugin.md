# 0032. Strategic Explainer Fast как отдельный in-context plugin

Статус: частично заменено ADR-0033, 2026-08-27. Fast package и in-context
boundary сохраняются; Fast-first routing и fail-closed ShipTask failure policy
заменены [ADR-0033](0033-terminal-provider-and-optional-shiptask-routing.md).

Дополняет [ADR-0031](0031-standalone-strategic-explainer-plugin.md), не изменяя
opaque/stateless boundary ordinary provider из
[ADR-0030](0030-opaque-strategic-explainer-provider-boundary.md).

## Контекст

Обычный Strategic Explainer показал высокое качество на 20-case suite, но
создаёт отдельного generator-subagent для каждой publication unit. Feasibility
experiment в dirty caller context без subagent прошёл 20/20 cases по
self-review и использовал примерно на 67% меньше total tokens. Этот run не был
blind independent evaluation, поэтому не доказывает parity и не оправдывает
замену ordinary provider.

Нужен явный пользовательский A/B без смешения двух несовместимых isolation
contracts.

## Решение

- Создать независимый source package и runtime skill
  `$strategic-explainer-fast:strategic-explainer-fast`.
- Fast переносит все outcome/truth/language/authority requirements ordinary
  provider, но выполняет method текущим агентом и не создаёт subagent.
- Fast не заявляет clean context, statelessness или independent reader. Он
  отделяет authoritative anchors от process history логическим context firewall
  и выполняет in-context comprehension pass.
- Распространять Fast отдельным plugin
  `strategic-explainer-fast@srez-marketplace`. Ordinary plugin и его contract не
  менять.
- ShipTask предпочитает Fast по live skill availability. Ordinary provider
  используется только если Fast отсутствует. Для одной publication unit нельзя
  вызывать оба или использовать ordinary как quality retry Fast.
- Task Composer продолжает использовать ordinary Strategic Explainer: его
  routing не входит в этот эксперимент.
- Shared 20-case facts/rubrics остаются canonical corpus; Fast получает
  отдельный generation/evaluation protocol без копирования fixtures.

## Последствия

Пользователь выбирает эксперимент установкой Fast plugin и откатывается его
удалением или отключением. Если установлены оба, ShipTask использует Fast;
direct invocation по qualified skill остаётся однозначным. Недоступность либо
ошибка выбранного provider проходит fail-closed правила ShipTask и не маскируется
вторым provider.

Fast снижает orchestration cost, но имеет более слабую гарантию независимости.
Заявление о quality parity требует blind one-unit-at-a-time A/B с независимыми
evaluators.

## Проверка

- `SEF-01..SEF-16` имеют локальную трассу Requirements → Architecture → runtime
  → evaluation;
- runtime Fast не содержит `fork_turns` или subagent invocation;
- ShipTask runtime и docs содержат Fast-first/ordinary-fallback routing;
- separate Marketplace plugin содержит только Fast runtime;
- repository, Marketplace и installed cache Fast byte-identical;
- fresh Codex task видит оба qualified skills после их установки.
