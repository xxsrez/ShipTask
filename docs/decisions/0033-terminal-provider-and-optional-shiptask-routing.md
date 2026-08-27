# 0033. Terminal ordinary provider и optional routing ShipTask

Статус: принято, 2026-08-27.

Частично заменяет ShipTask routing/failure clauses в
[ADR-0022](0022-mandatory-independent-strategic-explainer-for-comments.md),
[ADR-0030](0030-opaque-strategic-explainer-provider-boundary.md),
[ADR-0031](0031-standalone-strategic-explainer-plugin.md) и
[ADR-0032](0032-strategic-explainer-fast-plugin.md). Самостоятельная distribution
обоих providers, opaque ordinary expertise, Task Composer ordinary dependency и
отсутствие комментария для обычного `To Do → In Progress` сохраняются.

## Контекст

Ordinary Strategic Explainer использовал один `SKILL.md` и для caller, и для
provider. Роль определялась по эвристике о текущем context. В реальном
многоагентном вызове fresh provider увидел признаки agent orchestration,
переклассифицировал себя в caller и породил ещё один Strategic Explainer. Такой
self-call не улучшает объяснение, нарушает isolation contract и может создать
рекурсивное дерево agents.

Одновременно ShipTask предпочитал Fast и считал отсутствие или failure обоих
providers capability blocker-ом для comments/status. Это не соответствовало
желаемому A/B: при установленных обоих должен работать проверенный ordinary, а
без plugins ShipTask должен просто писать по собственному contract.

## Решение

### Ordinary provider

- Caller создаёт fresh built-in `default` subagent с `fork_turns="none"` и
  помещает в compact task exact marker `STRATEGIC_EXPLAINER_PROVIDER_V1`.
- `SKILL.md` сначала разрешает роль только по marker. Provider path находится
  перед caller path и терминален; context, tool history, parent metadata и имя
  агента роль не меняют.
- Provider-only `references/provider-entrypoint.md` выполняет admission. Только
  admitted provider читает внутренний `provider-contract.md`.
- Provider имеет одну роль: сформулировать или явно отредактировать одну
  user-facing publication unit read-only способом. Он не становится caller,
  router, coordinator или evaluator, не вызывает Strategic Explainer, не
  создаёт и не продолжает agents.
- Planning, decomposition, implementation, mutation, lifecycle/status/authority
  decision, orchestration и broad research без publication unit возвращают
  `STRATEGIC_EXPLAINER_INVOCATION_ERROR` до domain discovery. Refusal называет
  точный defect, назначение provider-а и clean-call recipe, затем экземпляр
  останавливается.
- Runtime comprehension check выполняет сам provider. Независимый reader
  остаётся только внешним model-forward evaluator и не входит в runtime tree.

### ShipTask routing

В начале run ShipTask выбирает первый разрешённый и доступный mode:

1. ordinary Strategic Explainer;
2. Fast;
3. native ShipTask writing.

Четыре install combinations дают соответственно ordinary, ordinary, Fast и
native. Общий no-subagent rule исключает ordinary и выбирает Fast либо native;
полный Explainer opt-out выбирает native.

Для одной publication unit используется не более одного provider. Failure уже
выбранного provider переводит run в native, не вызывает второй provider и не
создаёт quality retry. Единственное исключение — один corrected fresh retry,
который ordinary client protocol делает для structural invalid invocation.

Native mode следует собственным truth/lifecycle/reporting requirements ShipTask,
не читает и не имитирует provider method и не заявляет эквивалентное качество.
Отсутствие, opt-out или failure providers не создают capability warning, не
мешают обязательному comment/read-back и не блокируют разрешённый status
transition.

## Последствия

Ordinary остаётся более дорогим, но при установке имеет приоритет как основной
проверенный вариант. Fast можно испытать отдельно, отключив ordinary. Полное
отсутствие Explainer plugins сохраняет функциональность ShipTask с более слабой,
честно неэквивалентной communication path, но без служебного шума для человека.

Task Composer не наследует новый routing автоматически: его локальный source
package продолжает определять ordinary dependency и собственную failure policy.

## Проверка

- static runtime tests доказывают marker-first role resolution, provider-only
  entrypoint и отсутствие agent delegation в provider references;
- behavioral regression запускает admitted provider с доступными team tools и
  подтверждает отсутствие child agents;
- off-role behavioral cases возвращают exact invocation error до source/domain
  calls;
- ShipTask evaluation покрывает ordinary+Fast, ordinary-only, Fast-only и
  neither, а также no-subagent, opt-out и provider failure;
- current 20-case blind model-forward suite сохраняет независимый evaluator как
  test harness, не runtime dependency.
