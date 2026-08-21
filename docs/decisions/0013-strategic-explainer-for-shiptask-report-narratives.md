# 0013. Strategic Explainer для всех ShipTask report narratives

Статус: accepted, 2026-08-20. Расширяет
[ADR-0012](0012-strategic-explainer-as-portable-subagent-role.md). No-tools
invocation и технически центрированный brief заменены problem-first bounded
discovery из [ADR-0014](0014-problem-first-bounded-strategic-discovery.md). Меняет
invocation policy для ShipTask. Lifecycle, comment capability и terminal-effect
правила из [ADR-0006](0006-delivery-comment-as-terminal-effect.md) не меняются.
Fail-closed status-write часть для proven rework уточнена
[ADR-0015](0015-single-pass-review-disposition.md), а единая граница между
comment effect и status write —
[ADR-0016](0016-current-lifecycle-and-reporting-contract.md).

## Контекст

Strategic Explainer первоначально был обязателен для material partial/blocked
handoff, запроса user action и сложного technical success. При этом durable
Task comment мог быть сформирован delivery agent напрямую, а простой success
вообще не требовал отдельной адаптации. Получался разрыв: основной канал,
который остаётся в Task Manager после run, не был гарантированно пропущен через
свежий пользовательский контекст.

Пользователь ожидает одинаково ясное объяснение, когда Task завершена, требует
rework или заблокирована. Особенно недопустимо переводить Task/Goal в blocked с
comment или chat handoff, состоящим из reason code, технического симптома либо
необъяснённой просьбы о тестовом аккаунте.

## Решение

- Любой новый ShipTask delivery-report comment со state `COMPLETED`,
  `REWORK REQUIRED`, `BLOCKED` или `CANCELED` обязан пройти Strategic Explainer
  communication pipeline. Простота success не отменяет это требование.
- До invocation ShipTask самостоятельно выполняет task-level finalization и
  фиксирует authoritative facts: перечитанные Task/result/effects, выбранный
  report state, verified и unverified scenarios, impact, evidence/confidence,
  ограничения и уже разрешённый next action. Safe bounded repair выполняется до
  brief; material state change перезапускает finalization. Explainer не выбирает
  lifecycle state, blocker, recovery, authority или terminal transition.
- Для каждого comment формируется task-scoped `Technical Brief` с target
  surface `TASK_COMMENT`. Свежий built-in `default` субагент применяет
  `$ship-tasks:strategic-explainer` и возвращает свободное стратегическое
  объяснение без tool calls. Это не structured result и не готовый comment body.
- «Свежий» subagent означает built-in `default` с точным
  `fork_turns="none"`. `fork_turns="all"`, положительное число fork turns и
  старый Explainer thread запрещены.
- Сам Explainer до анализа проверяет context integrity. Более ранние
  user/assistant turns или tool transcript приводят только к
  `CONTEXT_INTEGRITY_ERROR` с инструкцией корректного запуска. ShipTask
  исправляет orchestration и один раз повторяет fresh invocation. Повторный отказ
  использует локальную `degraded-adaptation`: communication helper не блокирует
  truthful rework status, но `COMPLETED` comment остаётся обязательным перед
  `Done`.
- ShipTask читает стратегическое объяснение и самостоятельно пишет final
  comment своими словами. Он сохраняет outcome, user impact, причинную границу,
  confidence и next state, но может сокращать и перестраивать изложение под
  Task Manager. Механическое копирование, противоречие выводу Explainer,
  неподтверждённые добавления и возврат к собственной process diary запрещены.
- Authoritative envelope, report state, identifiers и необходимое evidence
  остаются ответственностью ShipTask и добавляются по исходным фактам, а не
  считаются частью результата Explainer.
- Перед write обязательны forward trace и reverse coverage. Если input
  противоречив или decision-relevant fact отсутствует, исправляется
  finalization/Technical Brief; гладкий comment по неполному состоянию не
  публикуется.
- `BLOCKED` имеет двойной communication barrier:
  1. task-level explanation существует до публикации `BLOCKED` comment;
  2. scope-level explanation существует до user-facing blocking handoff.
- Одно стратегическое объяснение можно переиспользовать между Task comment и chat report
  только когда audience, scope, facts, state, user dependency и next action
  совпадают по смыслу. Planned comment write/read-back и terminal status
  reconciliation не делают explanation stale, если они точно соответствуют уже
  переданному next-state contract и read-back не выявил drift. Recovery,
  divergent outcome или другое material meaning change требуют нового brief.
  Для batch, нескольких blockers или другого audience создаётся новый
  scope-level brief.
- При single success final chat report может использовать task-level brief. При
  aggregate batch result нужен отдельный scope-level brief, потому что один
  Task comment не представляет весь run.
- Если subagent tools или sibling-skill временно недоступны, ShipTask обязан
  применить тот же смысловой contract локально и пройти те же fidelity checks.
  Это `degraded-adaptation` во внутреннем evidence, но не новый Task/Goal
  blocker. Этот fallback не применяется к исправимой ошибке загрязнённого
  invocation.
- Обычные промежуточные red/green iterations по-прежнему не создают comments и
  не запускают Explainer: pipeline применяется к уже требуемому
  user-visible report, а не к каждому внутреннему событию.

## Последствия

Положительные:

- durable Task comment и chat handoff опираются на одну пользовательскую модель;
- успех и failure получают одинаковый quality bar;
- блокировка не может остаться только техническим reason code;
- authoritative state/evidence остаются под контролем ShipTask;
- generic Strategic Explainer не получает Task Manager coupling.

Ограничения:

- каждый новый Task report comment требует дополнительной adaptation работы и
  обычно отдельного model run;
- batch может требовать несколько task-level briefs и один aggregate brief;
- local fallback имеет менее чистый context, поэтому считается degraded, хотя
  не останавливает delivery;
- качество narrative всё ещё ограничено точностью Technical Brief и не заменяет
  verification либо comment read-back.
