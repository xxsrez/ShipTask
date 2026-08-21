# 0010. Осмысленная финализация и глубокий компактный run report

Статус: accepted, 2026-08-18. Отменяет fail-fast policy
[ADR-0009](0009-terminal-report-capability-preflight.md), не меняя действующий
comment lifecycle из [ADR-0006](0006-delivery-comment-as-terminal-effect.md).
Требование строгого Goal blocker threshold и повторных attempts заменено
[ADR-0015](0015-single-pass-review-disposition.md); finalization и human-report
части этого решения сохраняются как rationale. Единые lifecycle/reporting
границы из ADR-0016, фиксированная форма pass и порядок recovery заменены
[ADR-0017](0017-constitution-first-runtime-contract.md), который является
current runtime contract.

## Контекст

Terminal decision может быть формально правдивым и при этом бесполезным для
человека: агент повторяет последний технический симптом, не восстанавливает
причину, не замечает доступный способ продолжить и оставляет scope в
незавершённом состоянии без ясного объяснения.

Проблема не относится к одному типу effect. Нужен общий контур финализации,
который одинаково работает перед успехом, partial/no-work handoff, blocking
pause и Goal `blocked`.

## Решение

- Не менять этим ADR обязательность Task comments, их capability rules, Task
  status flow или release boundaries.
- Перед любым terminal outcome выполнить finalization pass:
  1. сопоставить обещанный результат с фактически достигнутым;
  2. перечитать current scope, Tasks, Goal, result/effects и существенное
     evidence;
  3. объяснить причины значимых расхождений, отделив доказанное от inference;
  4. проверить, остаются ли безопасные in-scope действия, способные довести
     результат или устранить найденную проблему;
  5. выполнить такие действия при уже существующей authority, перечитать
     affected state и начать finalization pass заново;
  6. только на устойчивом состоянии выбрать `complete`, partial/no-work,
     blocking handoff или допустимый Goal `blocked`.
- Blocker остаётся blocker до фактического устранения. Наличие разрешённого
  recovery не отменяет blocker; оно означает, что meaningful progress ещё
  возможен и финальный Goal status `blocked` пока не обоснован. После успешного
  recovery зафиксировать, что blocker устранён, и продолжить workflow.
- Если blocker остаётся после одного допустимого bounded repair, показать
  человеку понятную причину, фактический impact, уже выполненное действие и одно
  точное условие возобновления. Task-local blocker оставляет Goal активным; не
  повторять неизменившуюся проверку ради Goal status.
- Каждый terminal exit ShipTask заканчивается человекочитаемым run report.
  Report должен быть глубоким, но компактным: сначала агент строит точную модель
  результата и причин, затем оставляет только то, что помогает человеку понять
  итог, текущий статус, основания и следующий шаг.
- Успешный report объясняет полученный результат, существенные решения и причины,
  проверку и реальные ограничения. Blocked/partial report объясняет недостигнутый
  результат, root cause или честную границу знания, что агент уже сделал для
  продолжения, причину остановки и точное условие возобновления.
- Не превращать report в process diary, postmortem по шаблону или выгрузку
  protocol details. Reason codes, tool names, raw errors, полные Task/file lists
  и technical evidence включать только когда они действительно объясняют или
  доказывают вывод. Форму и длину адаптировать к сложности результата.

## Последствия

Положительные:

- финализация становится последним рабочим этапом, а не оформлением уже принятого
  решения;
- разрешимые проблемы устраняются до terminal status и handoff;
- пользователь получает сжатое понимание результата вместо журнала действий;
- одинаковое качество объяснения требуется при успехе и при блокировке.

Ограничения:

- finalization pass не расширяет scope или authority и не разрешает production,
  destructive, privacy, secret либо external-recipient action без требуемого
  approval;
- анализ не заменяет Task comments, checks, read-back или external verification;
- если safe continuation действительно отсутствует, отчёт не отменяет blocker и
  не разрешает объявить незавершённый scope завершённым.
