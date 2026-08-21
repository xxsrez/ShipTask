# Проверка lifecycle и приёмки ShipTask

Матрица проверяет пользовательские outcomes, а не точные внутренние шаги или
формулировки. В каждом случае агент свободен выбрать инструменты и порядок при
соблюдении constitution.

## Обязательная матрица

| Сценарий | Фактический исход | Comment | Status | Дальнейшее действие | Недопустимо |
|---|---|---|---|---|---|
| Обычный старт `To Do` | работа началась | не требуется | `In Progress` | реализовать и проверить | лишний ritual comment |
| Candidate готов к review | result реализован и targeted checks пройдены | объяснить result и checks; read-back до transition | `In Review` | сразу провести приёмку | status без comment |
| Current acceptance противоречит самому себе | `task-contract-conflict` | точное противоречие и нужное решение | оставить `In Review` | исправить только объективно однозначный contract | считать историю редакций конфликтом |
| Exact candidate воспроизводимо нарушает критерий | `verified-failure` | failure, impact и причина возврата; read-back | `In Progress` | продолжить rework в том же run | status без comment или завершить run на reopen |
| Необходимый test/runtime tool сломан, но чинится | tool failure | comment только если после repair остаётся blocker или нужен transition | зависит от результата повторной проверки | восстановить tool и повторить исходную операцию | сразу перейти к слабой альтернативе |
| Test harness или среда не восстановлены в текущей authority | `verification-blocked` | причина и 2–4 способа приёмки; read-back | оставить `In Review` | рекомендовать следующий вариант и success signal | объявить product defect без наблюдения |
| Batch gate упал, виновная Task не установлена | attribution не доказана | объяснить границу знания, если дальнейшая диагностика невозможна | affected Tasks остаются `In Review` | получить separating evidence | вернуть весь batch в rework |
| Полный evidence доказывает критерии | `verified-success` | outcome, impact, evidence и limits; read-back | `Done` | перечитать Task | ждать ручной acceptance |
| Reopen terminal Task | обнаружен новый material reason | объяснить причину reopen; read-back | правдивый working status | продолжить scoped work | молчаливый reopen |
| Новый `Canceled` или `Duplicate` | terminal reason доказан | объяснить причину и связь с outcome; read-back | соответствующий terminal status | перечитать Task | terminal status без comment |
| Comment channel отсутствует или сломан | ShipTask infrastructure failure | сначала попытаться восстановить; факт публикации не выдумывать | не выполнять существенный transition | сообщить причину, impact и resume condition | отложить объяснение на потом, status без comment, fallback в description |
| Task-local blocker в batch | Task незавершена | понятный blocker comment с read-back | правдивый non-terminal status | продолжить независимые Tasks | завершить или искусственно блокировать Goal |

## Regression questions

- Можно ли понять причину status change, читая только Task? Ответ должен быть
  «да» для каждого существенного transition.
- Был ли нужный сломанный инструмент сначала диагностирован и восстановлен, а
  исходная операция повторена? Более слабый обход не проходит.
- Доказан ли defect наблюдением exact candidate, а не сбоем проверки?
- Получил ли реальный verification blocker несколько кратких путей приёмки?
- Продолжил ли агент rework после reopen вместо завершения run?
- Остался ли Goal только учётом batch progress, без искусственного счётчика
  попыток?
- Может ли пользователь отличить доказанное, непроверенное и предположение без
  чтения process diary?

## Слепой forward test

Тестовому агенту передают candidate skill и реалистичный exact scope, но не
ожидаемый исход и не diagnosis предыдущего run. Проверяются observable Task
comments/statuses, tool recovery, result evidence и final report. Названия
внутренних этапов, шаблоны и число tool calls не оцениваются.
