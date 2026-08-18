# 0010. Причинный анализ перед blocked и человекочитаемый run report

Статус: accepted, 2026-08-18. Отменяет fail-fast policy
[ADR-0009](0009-terminal-report-capability-preflight.md), не меняя действующий
comment lifecycle из [ADR-0006](0006-delivery-comment-as-terminal-effect.md).

## Контекст

В batch-run по Release 0.1 агент завершил implementation, verification и
production release, но оставил двадцать четыре Tasks в `In Review` и перевёл
Goal в `blocked`. Финальный ответ сообщил технический симптом — отсутствующий
terminal comment — но не объяснил человеку причинную цепочку и не проверил,
можно ли устранить состояние доступными агенту действиями.

Пользователю важен не внутренний reason code и не список tool calls. Перед
остановкой агент должен понять, что фактически произошло, отделить симптом от
причины, проверить доступные способы восстановления и продолжить работу, если
найденный путь остаётся безопасным и разрешённым.

## Решение

- Не менять comment capability, обязательность report-comment, status flow или
  release boundaries этим ADR. ADR-0009 больше не задаёт preflight barrier.
- Перед финальным `blocked`, blocking input либо утверждением «продолжить
  невозможно» выполнить причинный анализ:
  1. назвать наблюдаемый симптом и фактический impact;
  2. восстановить последовательность событий и last safe checkpoint;
  3. проверить наиболее вероятные причины текущими sources/tools, отделяя
     подтверждённое от inference;
  4. перечислить доступные безопасные in-scope recovery actions;
  5. выполнить recovery самостоятельно, если authority уже есть и действие не
     расширяет scope;
  6. перечитать Task/Goal/external state и только затем решать, остался ли
     blocker.
- Если анализ обнаружил доступное действие, которое устраняет blocker, статус
  `blocked` запрещён: агент выполняет действие и продолжает workflow. Сложность,
  неожиданность или необходимость ещё одного обычного tool call не являются
  внешним blocker.
- Если safe recovery действительно требует нового user decision, authority или
  недоступного внешнего state change, перед `update_goal(status="blocked")`
  показать человеку plain-language explanation. Один reason code, raw error
  либо фраза «tool unavailable» не считаются объяснением.
- Каждый terminal exit ShipTask — `complete`, `blocked`, partial/deferred или
  `no-work` — заканчивается `SHIPTASK RUN REPORT`. Task comments не заменяют
  этот interaction report.
- Report сначала простыми словами отвечает: что получилось, что произошло,
  почему, что агент проверил и сделал после диагностики, что осталось и какое
  одно следующее действие требуется. Exact refs, statuses, commits, deploys,
  checks, comments и Goal state идут после объяснения как evidence.
- Если root cause не доказан, честно указать confidence и недостающее evidence;
  не выдавать гипотезу за факт. Однако неизвестность сама по себе не отменяет
  доступные безопасные recovery checks.

## Последствия

Положительные:

- агент не блокирует Goal на симптоме, который способен устранить сам;
- пользователь понимает причинную цепочку и реальное состояние scope без
  расшифровки внутренних protocol names;
- terminal report остаётся полезным даже после успешного self-recovery;
- причина, recovery и resume step сохраняются отдельно от raw tool output.

Ограничения:

- анализ не расширяет authority и не разрешает production, destructive,
  privacy, secret или external-recipient action без требуемого approval;
- строгий Goal tool threshold по-прежнему обязателен;
- отчёт не заменяет Task comments, checks, read-back или external verification.
