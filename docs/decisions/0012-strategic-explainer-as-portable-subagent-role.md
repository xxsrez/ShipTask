# 0012. Strategic Explainer как переносимая роль свежего субагента

Статус: partially superseded, 2026-08-22. Plugin distribution и общая read-only
роль сохраняются. [ADR-0022](0022-mandatory-independent-strategic-explainer-for-comments.md)
восстанавливает отдельного независимого субагента для всех комментариев
ShipTask, а точные fresh-subagent/fork/context механизмы остаются заменены
[ADR-0021](0021-requirements-as-agent-constitution.md). ShipTask invocation policy расширена
[ADR-0013](0013-strategic-explainer-for-shiptask-report-narratives.md), а
no-tools input contract заменён bounded read-only discovery из
[ADR-0014](0014-problem-first-bounded-strategic-discovery.md). Дополняет
[ADR-0010](0010-blocker-analysis-and-human-run-report.md) и изменяет состав
plugin, первоначально зафиксированный в
[ADR-0011](0011-separate-shiptask-plugin-distribution.md).

Устойчивую продуктовую цель и current agent-independent contract определяют
[стратегическое видение](../skills/strategic-explainer/product-vision.md); этот ADR фиксирует только
исторический технический способ её реализовать и распространять. Design evidence и
рассмотренные альтернативы находятся в
[research report](../reports/2026-08-20-strategic-explainer-research.md).

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
[Plugin contract](https://developers.openai.com/plugins/concepts/plugins)
распространяет skills и MCP components, но не custom-agent TOML. Глобальная
personal installation нарушила бы требование хранить компонент в том же
переносимом plugin, а project-scoped agent из репозитория ShipTask был бы
недоступен в других проектах.

По [официальной модели orchestration](https://developers.openai.com/api/docs/guides/agents/orchestration)
Explainer является manager-style specialist, а не handoff owner: основной агент
остаётся владельцем user-facing ответа, решений и действий.

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
  его применить установленный catalog skill
  `$ship-tasks:strategic-explainer` к одному самодостаточному `Technical Brief`.
- В Codex запускать такого субагента с `fork_turns="none"`. Перед анализом он
  проверяет, что видит только system/developer instructions, runtime skill и
  один текущий handoff. Более ранние user/assistant turns или tool transcript
  означают загрязнённый вызов: субагент возвращает
  `CONTEXT_INTEGRITY_ERROR` с инструкцией корректного перезапуска и не выполняет
  анализ.
- При полном Technical Brief не выдавать субагенту исследовательскую задачу и
  явно запрещать tool calls. При неполном input он обычным текстом сообщает
  родителю, каких фактов не хватает для честного вывода.
- Использовать отдельный task name `strategic_explainer`, но не выдавать его за
  зарегистрированный native custom agent: plugin contract этого пока не
  поддерживает.
- Strategic Explainer возвращает свободное стратегическое объяснение: outcome,
  impact, подтверждённую границу знания, конкретный user dependency и понятный
  next state. Это не structured result и не copy-ready comment. Он не выполняет
  writes, не выбирает Task/Goal status, не решает scope или authority и не
  публикует ответ пользователю.
- Сохранять scenario-level state `VERIFIED | FAILED | UNVERIFIED |
  NOT_APPLICABLE`, concrete action contract и lossless-by-relevance audit:
  forward trace всех output claims и reverse coverage всех decision-relevant
  input facts.
- Основной агент принимает решения и выполняет actions только по исходному
  evidence и authority. Он читает объяснение как смысловую основу и сам пишет
  окончательный user-facing текст своими словами; не копирует ответ механически
  и не заменяет его собственной process diary.
- Конкретные ShipTask invocation surfaces определяет ADR-0013: все новые Task
  report comments проходят Explainer pipeline, а blocking и aggregate
  user-facing handoffs получают отдельную либо доказанно совместимую адаптацию.
- После recovery или другого изменения facts старый brief считать stale и при
  необходимости вызвать новый свежий субагент.
- Если multi-agent tools или skill недоступны, ShipTask не скрывает фактический
  outcome и не создаёт новый blocker только из-за formatting layer. Он сам
  применяет тот же смысловой contract, явно фиксирует degraded adaptation в
  internal evidence и продолжает действующий lifecycle. Загрязнённый invocation
  является другой ситуацией: родитель обязан исправить вызов, а не переходить к
  локальному fallback.

## Последствия

Положительные:

- технический context остаётся у delivery agent, а пользователь получает
  отдельную outcome-first модель;
- generic skill можно явно применять к другим workflows уже в текущем plugin;
- Explainer не получает право менять состояние или переопределять delivery
  policy;
- будущий перенос skill в отдельный plugin не требует менять его input/output
  contract.
- manager-style ownership не позволяет communication helper незаметно стать
  decision maker или источником новой authority.

Ограничения:

- это реальный свежий субагент, но не native custom-agent type в picker;
- дополнительный model run увеличивает latency и token usage;
- качество объяснения ограничено полнотой `Technical Brief`; свежий context не
  исправляет отсутствующие или ложные исходные факты;
- self-audit и regression cases из
  [evaluation contract](../reference/strategic-explainer-evaluation.md) не
  заменяют проверку понятности на реальных получателях;
- plugin временно содержит capability, не совпадающую с его узким историческим
  названием. Это осознанный промежуточный packaging tradeoff.
