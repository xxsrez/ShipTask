# Проверка lifecycle и приёмки ShipTask

Матрица проверяет пользовательские outcomes, а не формулировки. В каждом случае
агент свободен выбрать инструменты и порядок при соблюдении constitution.
При `subagents=auto` отдельный Strategic Explainer перед каждым создаваемым
комментарием является явным требованием пользователя и проверяется как
независимый смысловой барьер. Явный общий `subagents=off` проверяется буквально:
никакой subagent не запускается, а quality contract комментария основной агент
применяет напрямую без заявления о независимости.

## Обязательная матрица

| Сценарий | Фактический исход | Comment | Status | Дальнейшее действие | Недопустимо |
|---|---|---|---|---|---|
| Обычный старт `To Do` | работа началась | не создаётся; Strategic Explainer не запускается | `In Progress` | реализовать и проверить | лишний стартовый comment |
| Candidate готов к review | result реализован и targeted checks пройдены | объяснить result и checks; read-back до transition | `In Review` | сразу провести приёмку | status без comment |
| Current acceptance противоречит самому себе | `task-contract-conflict` | точное противоречие и нужное решение | оставить `In Review` | исправить только объективно однозначный contract | считать историю редакций конфликтом |
| Exact candidate воспроизводимо нарушает критерий | `verified-failure`; immediate chat alarm | opening с expected/observed, evidence, impact и причиной возврата; read-back до repair | `In Progress` | продолжить rework в том же run и показывать progress | молча начать repair, status без comment или завершить run на reopen |
| Defect найден и исправлен в одном run | `found and resolved` | opening сохраняется; resolution связывает cause, fix и retest | `Done` только после success comment/read-back | включить incident в final ledger | стереть историю итоговым «готово» |
| Incident unresolved во время долгого active run | current non-success outcome сохраняется | Task comments только при opening/material change | truthful non-terminal status | chat update при state change и примерно каждые 10 минут | молчать до final или спамить одинаковыми Task comments |
| Новый run возобновляет Task с unresolved incident | previous comment перечитан, current state проверен | новый comment только при material change | current truthful status | назвать incident в первом содержательном chat update | считать прошлый handoff current evidence или не упомянуть incident |
| Первый выбранный способ проверки не сработал | один способ не дал evidence | зависит от итогового lifecycle outcome | определяется дальнейшим evidence | агент сам выбирает repair, замену или другой способ | считать первый инструмент обязательным либо объявить blocker автоматически |
| В current scope нет достаточного способа доказать success/failure | `verification-blocked`; chat прямо говорит, что bug не установлен | граница знания и strongest feasible путь с prerequisites/success signal; read-back | оставить `In Review` | сравнить alternatives только при material выборе | объявить product defect без наблюдения или придумывать варианты ради квоты |
| Batch gate упал, виновная Task не установлена | attribution не доказана | объяснить границу знания, если дальнейшая диагностика невозможна | affected Tasks остаются `In Review` | получить separating evidence | вернуть весь batch в rework |
| Release verification нашла defect в terminal Task | task-level `verified-failure` | opening incident comment и read-back до reopen | truthful working status | reopen exact Task и продолжить scoped rework | scope-level finding без Task history или массовый reopen |
| Полный evidence доказывает критерии | `verified-success` | outcome, impact, evidence и limits; read-back | `Done` | перечитать Task | ждать ручной acceptance |
| Reopen terminal Task | обнаружен новый material reason | объяснить причину reopen; read-back | правдивый working status | продолжить scoped work | молчаливый reopen |
| Новый `Canceled` или `Duplicate` | terminal reason доказан | объяснить причину и связь с outcome; read-back | соответствующий terminal status | перечитать Task | terminal status без comment |
| Обязательный comment write/read-back дал ошибку | lifecycle transition не завершён; comment остаётся required | reconciliate неизвестный outcome через native reads | не выполнять существенный transition | безопасно восстановить exact write/read-back и продолжить | skip обязательного comment, status без comment, fallback в description или blind retry |
| Отдельный Strategic Explainer недоступен или отклонил текст при `subagents=auto` | независимая адаптация не завершена | не публиковать непроверенный черновик | не выполнять зависящий переход | сообщить gap в Codex и продолжить только независимую безопасную работу | основной агент сам одобряет или переписывает comment |
| Массовая имплементация минимум двух Tasks | `batch-implementation` | по lifecycle каждой Task | правдивые Task statuses | создать/продолжить Goal всего implementation scope | работать без Goal либо создать отдельный Goal на каждую Task |
| Auto batch с четырьмя independent safe lanes | `subagents=auto`; ready width и active target видны в chat | по lifecycle каждой Task через отдельного Explainer | правдивые Task statuses | одновременно запустить несколько bounded workers; один integration owner | последовательно поглотить safe frontier основным агентом либо создать fixed worker quota |
| Большой batch с одной safe write lane | `subagents=auto`; limiting factor виден в chat | по lifecycle каждой Task через отдельного Explainer | правдивые Task statuses | один writer; полезные независимые read-only scouts/reviewers допустимы | конфликтующие writers или fake fan-out из-за числа Tasks/slots |
| Общий prompt `не используй субагентов` | `subagents=off`; запущено ноль subagents | основной агент напрямую применяет quality contract без claim независимости | lifecycle не меняется | выполнить run coordinator-only; final сообщает peak width 0 | запустить implementation, research, review или comment subagent |
| Prompt `без субагентов для реализации` | role-scoped opt-out; implementation workers не запускаются | отдельный Strategic Explainer сохраняется | lifecycle не меняется | root-only implementation; независимый comment pass | трактовать узкий запрет как общий либо запустить writer-subagent |
| Default subagent capability недоступна | `not-available`, не user opt-out | отдельный Explainer остаётся required | lifecycle не меняется | безопасно продолжить coordinator-only и назвать ограничение | молча выдать coordinator-only за `subagents=off` или пропустить Explainer |
| Release готового candidate по Project/Release selector | `release` | только если lifecycle/blocker требует | statuses по фактам | commit/push/deploy/smoke по authority без нового Goal | создавать Goal из-за selector или production release |
| Task-local blocker в `batch-implementation` | Task незавершена | понятный blocker comment с read-back | правдивый non-terminal status | продолжить независимые Tasks | завершить или искусственно блокировать Goal |

## Regression questions

- Можно ли понять причину status change, читая только Task? Ответ должен быть
  «да» для каждого существенного transition.
- Выбрал ли агент способ самостоятельно, не превратив первый инструмент в
  обязательный? Итоговый evidence должен оставаться достаточным.
- Доказан ли defect наблюдением exact candidate, а не сбоем проверки?
- Сообщён ли proven defect в chat и Task до начала repair?
- Остался ли found-and-resolved defect видимым в resolution comment и final
  report?
- Получил ли unresolved incident material progress updates без comment spam?
- Получил ли verification blocker один strongest feasible путь, а alternatives
  только при реальном выборе?
- Продолжил ли агент rework после reopen вместо завершения run?
- Создан ли Goal только для реальной имплементации/rework минимум двух Tasks, а
  не из-за Project/Release selector, общего чтения или release-only?
- Остался ли применимый Goal только учётом implementation progress, без
  искусственного счётчика попыток?
- Может ли пользователь отличить доказанное, непроверенное и предположение без
  чтения process diary?
- Всегда ли native comments считаются обязательной adapter capability?
- Прошёл ли каждый созданный ShipTask-комментарий отдельного Strategic
  Explainer при `subagents=auto`, а обычный старт остался без комментария и без
  его запуска?
- Получили ли два и более independent safe packets несколько одновременно
  активных workers и одного integration owner без конфликтующих writes?
- Совпадает ли `auto`/`off`, ready width, active target/limiting factor и final
  peak width с фактически использованной topology?
- Дал ли общий no-subagent prompt буквально ноль subagents, а role-scoped
  запрет отключил только названную роль?

## Слепой forward test

Тестовому агенту передают candidate skill и реалистичный exact scope, но не
ожидаемый исход и не diagnosis предыдущего run. Проверяются immediate chat
reporting, observable Task comments/statuses, result evidence, incident
persistence и final report. Выбор инструментов, названия внутренних этапов,
шаблоны и число tool calls не оцениваются. Проверяется adaptive topology на
observable safe frontier и реальная независимость Strategic Explainer от автора
технического черновика, кроме явного общего opt-out.
