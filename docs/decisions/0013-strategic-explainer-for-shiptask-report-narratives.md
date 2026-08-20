# 0013. Strategic Explainer для всех ShipTask report narratives

Статус: accepted, 2026-08-20. Расширяет
[ADR-0012](0012-strategic-explainer-as-portable-subagent-role.md) и меняет
invocation policy для ShipTask. Lifecycle, comment capability и terminal-effect
правила из [ADR-0006](0006-delivery-comment-as-terminal-effect.md) не меняются.

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
  ограничения и уже разрешённый next action. Safe self-recovery выполняется до
  brief; material state change перезапускает finalization. Explainer не выбирает
  lifecycle state, blocker, recovery, authority или terminal transition.
- Для каждого comment формируется task-scoped `Technical Brief` с target
  surface `TASK_COMMENT`. Свежий built-in `default` субагент применяет
  `$strategic-explainer` и возвращает `User Brief` без tool calls.
- ShipTask составляет final comment из двух слоёв:
  1. authoritative envelope — report type, `State`, Task, result identity,
     stable report key и exact evidence;
  2. Explainer narrative — outcome, user impact, понятная причина, ограничение,
     требуемое действие и next state.
- ShipTask может удалить только дублирование между envelope и narrative и
  добавить exact navigation/evidence refs. Он не возвращает technical jargon,
  не меняет смысл `User Brief` и не подменяет его собственной process diary.
- `User Brief` является единственным источником narrative после успешного
  invocation. Родитель не может заново собрать пользовательский текст из raw
  evidence. Для durable Task comment действует compact presentation gate:
  обычно до 1 600 символов narrative и до трёх bullets/строк; URL, параметры,
  transport handles, полные UUID, хэши, provider IDs и raw tool errors не
  попадают в comment без явной необходимости для действия. При нарушении gate
  comment не публикуется до повторной адаптации.
- «Свежий» subagent означает запуск без inherited conversation context
  (`fork_turns="none"` или эквивалент). `fork_turns="all"` и старый
  Explainer thread считаются недействительными; если изоляция невозможна,
  используется локальный `degraded-adaptation` с теми же fidelity checks.
- Перед write обязательны forward trace и reverse coverage. Если input
  противоречив или decision-relevant fact отсутствует, исправляется
  finalization/Technical Brief; гладкий comment по неполному состоянию не
  публикуется.
- `BLOCKED` имеет двойной communication barrier:
  1. task-level explanation существует до публикации `BLOCKED` comment;
  2. scope-level explanation существует до user-facing blocking handoff и до
     допустимого `update_goal(status="blocked")`.
- Один `User Brief` можно переиспользовать между Task comment и chat report
  только когда audience, scope, facts, state, user dependency и next action
  byte-for-meaning совпадают. Planned comment write/read-back и terminal status
  reconciliation не делают brief stale, если они точно соответствуют уже
  переданному next-state contract и read-back не выявил drift. Recovery,
  divergent outcome или другое material meaning change требуют нового brief.
  Для batch, нескольких blockers или другого audience создаётся новый
  scope-level brief.
- При single success final chat report может использовать task-level brief. При
  aggregate batch result нужен отдельный scope-level brief, потому что один
  Task comment не представляет весь run.
- Если subagent tools или sibling-skill временно недоступны, ShipTask обязан
  применить тот же Strategic Explainer contract локально и пройти те же
  fidelity checks. Это `degraded-adaptation` во внутреннем evidence, но не новый
  Task/Goal blocker и не основание публиковать технический текст без адаптации.
- Обычные промежуточные red/green iterations по-прежнему не создают comments и
  не запускают Explainer: pipeline применяется к уже требуемому
  user-visible report, а не к каждому внутреннему событию.

## Последствия

Положительные:

- durable Task comment и chat handoff используют одну пользовательскую модель;
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
