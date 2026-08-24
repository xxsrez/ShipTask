# 0027. Критическая приёмка по кодовой базе при исчерпанном frontier

Статус: accepted, 2026-08-24. Решение добавляет явное ослабление
[ST-02/ST-05/ST-09/ST-23](../skills/ship-tasks/requirements.md) через новый
[ST-25](../skills/ship-tasks/requirements.md) и уточняет automatic terminal
acceptance из [ADR-0005](0005-automatic-terminal-acceptance.md).

## Исходное пользовательское требование

Когда во всём выбранном scope не осталось Tasks в `To Do` и `In Progress`, а
все незавершённые Tasks находятся в `In Review` и их обычная функциональная
проверка требует существенной человеческой приёмки, ShipTask не должен
бессрочно оставлять весь результат в review. Вместо этого exact integrated
candidate проходит независимое критическое review кодовой базы и тестов в
свежем контексте. Grounded approval разрешает более слабый `Done`, а найденная
проблема возвращает точно затронутую Task в rework.

Любой переход из `In Review` получает обязательный Task comment. При слабом
`Done` comment через Strategic Explainer должен прямо объяснить, какая
функциональная проверка не состоялась, почему причина требует существенной
работы человека, чем она была заменена и какой риск остался.

## Решение

- Critical fallback запускается только после обычной acceptance matrix и полной
  autonomous test frontier.
- Fresh inventory должен показывать `To Do == 0`, `In Progress == 0` и
  `In Review > 0`; `Backlog` и terminal statuses не участвуют в active gate.
- Каждая оставшаяся Task должна быть `verification-blocked` именно потому, что
  человек должен стать содержательным verifier. Approval, MFA, invite, bounded
  access grant и другое малое unlock-действие gate не открывают.
- Exact integrated candidate фиксируется; stale candidate, Task contract или
  inventory аннулируют review до status writes.
- Выполняется ровно один независимый read-only `critic` с
  `fork_turns="none"`. Он не наследует conversation, producer rationale или
  прежний verdict, самостоятельно перечитывает current Tasks/code/tests и даёт
  per-Task grounded disposition.
- Доказанная проблема следует обычному `verified-failure` и exact attribution.
  Grounded approval создаёт `critical-codebase-accepted`. Inconclusive review
  оставляет Task в `In Review`; отсутствие findings не равно approval.
- Перед каждым переходом отдельный Strategic Explainer готовит понятный Task
  comment. Для `critical-codebase-accepted` он сохраняет непроведённую functional
  check, substantial-human cause, исчерпанные autonomous paths, exact candidate,
  проверенные code/tests, critic verdict и residual risk.
- Effective user rule, запрещающий critic-subagent, отключает fallback: основной
  агент не изображает независимое review.

## Осознанный компромисс

`Done` теперь имеет две доказательственные силы. `verified-success` означает
полную объективную приёмку. `critical-codebase-accepted` означает, что обычная
functional verification честно осталась непроведённой, но strongest available
evidence и независимый critic не нашли material нарушения текущих критериев.
Различие всегда видно в Task history и final report.

Этот компромисс принят сознательно: более слабый, но явно маркированный terminal
outcome полезнее бессрочной очереди `In Review`, когда альтернатива требует
существенной ручной работы проверяющего.

## Не является решением

ADR не разрешает использовать code review вместо доступной functional check,
выдавать tool inconvenience за human blocker, закрывать Task по одному
отсутствию findings или скрывать proof gap. Он не создаёт external effect и не
расширяет production, destructive durable-data, secrets, privacy,
access-policy, external-recipient или unbounded-cost authority.

## Observable evaluation

Regression matrix должна проверять весь eligibility gate, отличие verifier от
unlocker, ровно одного fresh-context critic, per-Task attribution, mandatory
Strategic Explainer comment, явную границу weaker `Done`, stale/inconclusive
ветви и сохранение authority boundaries.
