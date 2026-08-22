# 0016. Единый действующий контракт lifecycle и отчётности

Статус: partially superseded, 2026-08-21. Нейтральный смысл `In Review`,
task-level defect attribution и отказ от счётчика повторов сохраняются. Разрыв
между comment и non-terminal status, `communication remainder` и procedural
form заменены [ADR-0017](0017-constitution-first-runtime-contract.md), а
comment-channel availability и acceptance incident reporting —
[ADR-0020](0020-visible-acceptance-incidents-and-required-comments.md).
Исторически уточнял ADR-0006, ADR-0010, ADR-0013 и
ADR-0015. Отменяет оставшиеся в действующих документах формулировки о
массовом rework без task-level доказательства, трёх повторах ради Goal
`blocked`, обязательной диаграмме и задержке truthful non-terminal
status из-за сбоя comment channel.

## Контекст

Контракт развивался несколькими ADR. После изменения политики приёмки в
обзоре, development guide и ранних accepted ADR остались фразы, которые
давали разные ответы на один и тот же вопрос: когда менять status, что
считать defect, когда ждать комментарий и сколько раз повторять проверку.

Эта неоднозначность опаснее неполного правила: агент может выбрать любую
из совместимых на словах трактовок и получить противоположный lifecycle result.

## Решение

### `In Review` нейтрален

`In Review` означает только, что result предъявлен, а его итог ещё не
установлен. Сам status не доказывает targeted verification, success, failure или
готовность к ручной приёмке. После одного bounded diagnostic pass применяется
матрица ADR-0015.

### Defect требует прямого доказательства

Падение aggregate gate, потеря прежнего success evidence или сбой test harness не
доказывают defect конкретной Task. В `In Progress` возвращаются только Tasks,
для которых exact candidate надёжно и воспроизводимо нарушает current acceptance.
При неясной attribution Tasks остаются `In Review` как `verification-blocked`.

### Status и комментарий — разные эффекты

| Исход | Task Manager status | Комментарий | Если comment channel недоступен |
|---|---|---|---|
| `verified-success` | `Done` только после report | `COMPLETED` | оставить `In Review`; приёмку не повторять |
| `verified-failure` | `In Progress` | `REWORK REQUIRED` | выполнить truthful status transition; сохранить communication remainder |
| `verification-blocked` | оставить `In Review` | `BLOCKED` с 2–4 способами приёмки | не менять status; показать тот же handoff в run report |
| `task-contract-conflict` | оставить `In Review` | `BLOCKED` с точным противоречием | не менять status; показать handoff в run report |
| новый подтверждённый cancel | `Canceled` только после report | `CANCELED` | не выполнять новый terminal status write |

`COMPLETED` и новый `CANCELED` являются барьерами перед terminal status write.
`REWORK REQUIRED` и `BLOCKED` остаются обязательными durable handoff, но их
недоступность не подменяет уже установленный task outcome. Ни один отчёт не
пишется в `description` или другое поле.

### Нет счётчика повторов

Business workflow не ждёт три одинаковых попытки и не создаёт дополнительные Goal
turns ради смены статуса. Повтор разрешён только после названного изменения
result, evidence, среды, доступа, authority или Task contract. Системные
ограничения Goal tool остаются внешней границей, но не становятся продуктовым
циклом ShipTask.

### Форма отчёта подчинена смыслу

Диаграмма, таблица или другая визуализация добавляются только когда они
заметно упрощают понимание. Сложность или размер Task сами по себе не требуют
диаграммы. Plain text и короткий before/after достаточны, если они передают смысл.

### Источники истины

Действующий runtime определяют только каноническая specification,
`ship-tasks/SKILL.md` и прямо связанные runtime references. Superseded ADR и датированные
reports сохраняют историю, но не являются fallback policy. Если accepted ADR частично
заменён более поздним решением, его header обязан прямо назвать заменённую часть.

## Последствия

- Один и тот же failed gate больше не может одновременно означать defect всего batch и
  невозможность установить defect.
- Сбой канала комментариев остаётся видимым незавершённым эффектом, но не фальсифицирует status.
- Одна осмысленная классификация заменяет счётчик повторов.
- Форма отчёта больше не выдаётся за обязательный evidence layer.
