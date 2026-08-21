# 0015. Однократная классификация приёмки

Статус: accepted, 2026-08-21. Уточняет ADR-0005, ADR-0006, ADR-0010 и
ADR-0013. Отменяет использование строгого Goal blocker threshold как части
business workflow для task-local приёмки; остальные system/tool ограничения на
Goal остаются внешней границей. Status/comment эффекты и отмена
оставшихся legacy формулировок собраны в
[ADR-0016](0016-current-lifecycle-and-reporting-contract.md).

## Контекст

Существующий workflow называл любую `In Review` Task `completion-remains`, но не
разделял три принципиально разных ситуации: требования самой Task противоречат
друг другу, проверка доказала defect, либо доступная проверка вообще не позволяет
установить success или failure. Из-за этого агент мог оставить доказанно
сломанный result в `In Review`, объявить проблему проверочной среды product bug
или многократно повторять одну и ту же приёмку ради Goal status.

Несколько изменений acceptance также ошибочно трактовались как самостоятельная
причина недоверия. На практике они могут быть последовательными попытками найти
работающий способ проверить result. Authority имеет current Task contract, а не
само число его редакций.

## Решение

- Каждая `In Review` Task после одного bounded diagnostic pass получает ровно
  один outcome: `task-contract-conflict`, `verified-success`,
  `verified-failure` или `verification-blocked`.
- `task-contract-conflict` означает противоречие в current mandatory contract, а
  не длинную историю изменений. Однозначно разрешимый конфликт исправляется по
  current accepted sources и read-back; material choice остаётся в `In Review`
  с понятным `BLOCKED` handoff.
- `verified-failure` требует прямого воспроизводимого расхождения exact candidate
  с current acceptance в совместимой среде. Перед rework готовится понятный
  `REWORK REQUIRED` narrative, после чего Task переводится
  `In Review → In Progress` и перечитывается.
- Недоступный comment channel не сохраняет proven failure в ложном review-ready
  status. Status transition выполняется, а comment остаётся отдельным
  communication remainder и тем же текстом показывается в run report.
- `verification-blocked` применяется, только когда невозможно доказать ни
  success, ни failure. Task остаётся `In Review`; `BLOCKED` comment объясняет
  точную границу знания и условие следующей попытки.
- Для `verification-blocked` ShipTask просит Strategic Explainer сравнить 2–4
  реалистичных способа получить недостающее доказательство: prerequisites,
  доказательную силу, tradeoff и observable success signal. Explainer может
  рекомендовать вариант, но не выбирает state, authority или action.
- Один и тот же acceptance scenario не повторяется без изменения result,
  проверки, среды, доступа, authority или Task contract. Запрещено создавать
  дополнительные turns, polls или перефразированные comments ради счётчика;
  ShipTask не добивается смены Goal status искусственными повторами.
- Task `BLOCKED`, run `PARTIAL`/`BLOCKED` и Goal status различаются. Task-local
  невозможность приёмки оставляет batch Goal активным; Goal `blocked` не
  используется как её синоним.
- `COMPLETED` comment остаётся обязательным terminal effect до `Done`. Новая
  развязка comment/status относится к truthful rework transition, а не ослабляет
  terminal completion.

## Последствия

Положительные:

- доказанный defect больше не маскируется статусом `In Review`;
- сбой проверки не превращается без доказательств в product bug;
- реальная проблема приёмки получает несколько конкретных путей решения;
- неизменившаяся блокировка диагностируется и объясняется один раз;
- Goal остаётся учётом незавершённого scope, а не причиной повторять работу.

Ограничения:

- если comments недоступны, durable rework/blocker narrative остаётся
  незавершённым communication effect и должен быть опубликован после появления
  capability без повторной приёмки;
- неразрешимое противоречие Task contract всё ещё требует material decision;
- классификация не ослабляет production, secrets, privacy, destructive-data и
  external-recipient authority boundaries.
