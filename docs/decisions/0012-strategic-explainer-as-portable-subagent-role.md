# 0012. Strategic Explainer как переносимая роль свежего субагента

Статус: accepted, 2026-08-20. Дополняет
[ADR-0010](0010-blocker-analysis-and-human-run-report.md) и изменяет состав
plugin, первоначально зафиксированный в
[ADR-0011](0011-separate-shiptask-plugin-distribution.md).

## Контекст

Требование писать человекочитаемый terminal report не гарантирует понятного
результата, если тот же основной агент долго работал с логами, connector
mechanics, status transitions и verification details. Технические термины могут
попасть в сообщение без пользовательского контекста, а несколько независимых
ограничений — слиться в один непонятный запрос.

Нужен отдельный общий интерпретационный слой со свежим context. Он должен быть
пригоден не только для ShipTask, не получать authority основного workflow и не
становиться вторым источником evidence.

Текущий [официальный Codex contract](https://learn.chatgpt.com/docs/agent-configuration/subagents)
позволяет определять native custom agents только как personal
`~/.codex/agents/*.toml` или project-scoped `.codex/agents/*.toml`.
[Plugin contract](https://learn.chatgpt.com/docs/plugins) распространяет skills
и другие plugin components, но не custom-agent TOML. Глобальная personal
installation нарушила бы требование хранить компонент в том же переносимом
plugin, а project-scoped agent из репозитория ShipTask был бы недоступен в
других проектах.

## Решение

- Добавить общий sibling-skill `$strategic-explainer` с user-facing именем
  `Strategic Explainer` в тот же `ship-tasks@srez-marketplace` plugin.
- Хранить repository source в sibling-каталоге `strategic-explainer/`, а
  marketplace source — в
  `plugins/ship-tasks/skills/strategic-explainer`; эти копии и installed cache
  должны быть byte-identical.
- Не создавать standalone `~/.codex/skills/strategic-explainer`;
  fresh catalog должен показывать plugin-qualified
  `ship-tasks:strategic-explainer`.
- Не включать в его runtime contract ShipTask, Task Manager или project-specific
  правила. ShipTask является первым consumer, но не владельцем роли.
- При интеграции из ShipTask запускать новый read-only-by-contract субагент
  built-in типа `default` без унаследованной истории разговора и явно просить
  его применить `$strategic-explainer` к одному самодостаточному
  `Technical Brief`.
- Использовать отдельный task name `strategic_explainer`, но не выдавать его за
  зарегистрированный native custom agent: plugin contract этого пока не
  поддерживает.
- Strategic Explainer возвращает только `User Brief`: outcome, impact,
  подтверждённую границу знания, конкретный user dependency и понятный next
  state. Он не выполняет writes, не выбирает Task/Goal status, не решает scope
  или authority и не публикует ответ пользователю.
- Основной агент принимает решения и выполняет actions только по исходному
  evidence и authority. `User Brief` используется как communication layer и
  проверка понятности, но не как новое evidence.
- Для material partial/blocked outcome и запроса user action/authority
  ShipTask обязан использовать свежий Strategic Explainer перед user-facing
  handoff. Для сложного terminal success использование обязательно, если
  техническая модель иначе попадёт в ответ; для тривиального success отдельный
  субагент не нужен.
- После recovery или другого изменения facts старый brief считать stale и при
  необходимости вызвать новый свежий субагент.
- Если multi-agent tools или skill недоступны, ShipTask не скрывает фактический
  outcome и не создаёт новый blocker только из-за formatting layer. Он сам
  применяет тот же `User Brief` contract, явно фиксирует degraded adaptation в
  internal evidence и продолжает действующий lifecycle.

## Последствия

Положительные:

- технический context остаётся у delivery agent, а пользователь получает
  отдельную outcome-first модель;
- generic skill можно явно применять к другим workflows уже в текущем plugin;
- Explainer не получает право менять состояние или переопределять delivery
  policy;
- будущий перенос skill в отдельный plugin не требует менять его input/output
  contract.

Ограничения:

- это реальный свежий субагент, но не native custom-agent type в picker;
- дополнительный model run увеличивает latency и token usage;
- качество brief ограничено полнотой `Technical Brief`; свежий context не
  исправляет отсутствующие или ложные исходные факты;
- plugin временно содержит capability, не совпадающую с его узким историческим
  названием. Это осознанный промежуточный packaging tradeoff.
