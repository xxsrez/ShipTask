# 0034. Luna Max для ordinary Strategic Explainer

Статус: принято, 2026-08-27; caller wiring частично заменено ADR-0035.

Частично заменяет profile routing в
[ADR-0025](0025-cost-aware-subagent-profiles.md) и cost consequence в
[ADR-0033](0033-terminal-provider-and-optional-shiptask-routing.md). Fresh
context, terminal provider role, ordinary-or-native routing и отсутствие
secondary provider сохраняются.

## Контекст

Сравнение двадцати пар ordinary provider outputs на одинаковых clean inputs
показало приемлемое качество Luna Max при существенно меньшей стоимости. Поэтому
ordinary Explainer больше не должен наследовать SOL/current profile основного
агента. Выбор communication mode остаётся простым: установленный и разрешённый
plugin вызывается отдельным clean subagent, а без plugin-а основной агент пишет
сам.

## Решение

- Каждый ordinary provider invocation создаёт новый built-in `default` subagent
  с `fork_turns="none"`, `model="gpt-5.6-luna"` и
  `reasoning_effort="max"`.
- Current caller model/effort не наследуются; SOL не используется как скрытая
  замена.
- Если ordinary plugin отсутствует или отключён, ShipTask сразу использует
  native writing основного агента.
- Failure выбранного ordinary provider, включая недоступный exact Luna Max
  profile, сохраняет существующий переход в native writing без secondary
  provider retry.
- Правило Luna-to-current handoff для genuinely simple implementation/research
  packets не применяется к ordinary Explainer.

## Проверка

- static tests требуют exact `model` и `reasoning_effort` в caller protocol;
- current 20-case model-forward gate запускает released profile именно на Luna
  Max, а SOL остаётся только сравнительным control;
- Marketplace source, installed cache и fresh App Server catalog должны
  подтверждать один ordinary plugin и отсутствие Fast.
