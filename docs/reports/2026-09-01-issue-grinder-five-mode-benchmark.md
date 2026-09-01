# Issue Grinder: сравнение пяти режимов

Дата: 2026-09-01. Benchmark ID:
`20260901-00000000-0000-4000-8000-9fb1a6e0d9a5`.

## Вывод

`Рой` дал лучший принятый результат: 97/100 и ни одного найденного существенного
дефекта. За это он заплатил 225,3 млн токенов, 2 ч 37 мин и эквивалентом
$113,51 по публичным API-тарифам.

`Экономичный` оказался лучшим практическим компромиссом: 85/100, принятый
terminal outcome, 110,3 млн токенов, 1 ч 17 мин и $50,26. Он уступил `Рою` 12
баллов качества, но потребовал примерно вдвое меньше времени, токенов и
стоимости. Найденный high-дефект ограничен конкурентным обновлением grant, а не
основной ACL-моделью.

`Классический` — самый дешёвый и быстрый из принятых результатов: 78/100,
74,6 млн токенов, 1 ч 12 мин и $38,34. Его нельзя считать лучшим default по
одной эффективности: слепая проверка нашла три high-дефекта в privacy, archived
Team ACL и атомарности membership.

`Соло` дошёл до работоспособного candidate за $27,66, но сам заблокировал
terminal delivery из-за лишнего запроса подтверждения уже разрешённого
действия. `Баланс` получил сильные 94/100, но исключён из ranking: прогон вызвал
запрещённые backup/restore subtests и нарушил hard gate, одновременно став самым
дорогим — $194,88 и 378,6 млн токенов.

Практическое решение по этому pilot: использовать `Экономичный` для обычных
широких delivery, `Рой` — когда важнее максимальная надёжность, а
`Классический` — только при низком риске и готовности принять более слабую
проверку. Это не изменение действующей mode policy, а наблюдаемый результат
одной серии.

## Слепая оценка и terminal outcome

Evaluator получил анонимные packets `A..E`; mode mapping был раскрыт только
после фиксации JSON и Markdown с SHA-256. Среди принятых результатов ranking:
`Рой` → `Экономичный` → `Классический`.

| Position | Режим | Terminal outcome | Hard gate | Blind score | High+ дефекты | UAT |
| ---: | --- | --- | --- | ---: | ---: | ---: |
| 1 | Экономичный | accepted | pass | 85 | 1 | v63 |
| 2 | Соло | blocked | pass | 75 | 1 | v64 |
| 3 | Баланс | hard-gate fail | fail: backup/restore | 94 | 2 | v65 |
| 4 | Рой | accepted | pass | 97 | 0 | v67 |
| 5 | Классический | accepted | pass | 78 | 3 | v68 |

`Баланс` сохраняет raw quality score 94, но не место в eligible ranking.
`Соло` прошёл implementation hard gates оценщика, однако не является принятым
delivery из-за terminal blocker и незавершённого lifecycle двух Tasks.

## Ресурсы и время

Токены сняты локальной Codex telemetry на полуоткрытом интервале каждого run.
Интервалы включают минимальные controller wait/status calls, поэтому это точные
account interval totals, а не идеальная атрибуция только delivery tree.

| Режим | Cached input | Input | Output | Всего | Cached / input | Время | Agents | Tool calls | Commits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Экономичный | 106 924 544 | 2 952 772 | 395 163 | 110 272 479 | 97,31% | 1:17:27 | 23 | 309 | 1 |
| Соло | 51 158 784 | 1 083 468 | 142 882 | 52 385 134 | 97,93% | 1:03:50 | 0 | 282 | 1 |
| Баланс | 368 958 976 | 8 581 231 | 1 105 728 | 378 645 935 | 97,73% | 4:04:52 | 18 | 808 | 23 |
| Рой | 219 681 024 | 4 990 640 | 594 176 | 225 265 840 | 97,78% | 2:37:33 | 17 | 496 | 12 |
| Классический | 72 777 600 | 1 654 929 | 200 868 | 74 633 397 | 97,78% | 1:12:16 | 14 | 318 | 1 |

| Режим | SOL + GPT-5.4, млн | Luna, млн | API equivalent | Score / млн total | $ / point |
| --- | ---: | ---: | ---: | ---: | ---: |
| Экономичный | 95,476 | 14,796 | $50,2589 | 0,7708 | $0,5913 |
| Соло | 52,385 | 0 | $27,6550 | diagnostic | diagnostic |
| Баланс | 374,127 | 4,519 | $194,8774 | excluded | excluded |
| Рой | 222,876 | 2,390 | $113,5050 | 0,4306 | $1,1702 |
| Классический | 72,977 | 1,656 | $38,3445 | 1,0451 | $0,4916 |

Производная эффективность рассчитана только для accepted candidates. Численно
`Классический` даёт больше score на токен и доллар, но severity его дефектов
делает этот показатель недостаточным для выбора режима. `Экономичный` даёт
лучший баланс качества и риска; `Рой` максимизирует качество.

Публичный API-equivalent рассчитан по официальным ценам на 2026-09-01:
SOL — $4 input / $0,40 cached / $20 output, Luna — $0,20 / $0,02 / $1,20,
GPT-5.4 — $2,50 / $0,25 / $15 за миллион токенов. Это не сумма подписки и не
точный расход quota. Источники: [GPT-5.6 SOL](https://developers.openai.com/api/docs/models/gpt-5.6-sol),
[GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna),
[GPT-5.4](https://developers.openai.com/api/docs/models/gpt-5.4).

## Недельная квота

| Режим | Used before | Used after | Расход, п.п. | Remaining before → after |
| --- | ---: | ---: | ---: | ---: |
| Экономичный | 23% | 26% | 3 | 77% → 74% |
| Соло | 26% | 27% | 1 | 74% → 73% |
| Баланс | 27% | 37% | 10 | 73% → 63% |
| Рой | 38% | 43% | 5 | 62% → 57% |
| Классический | 44% | 46% | 2 | 56% → 54% |

Во всех delivery intervals boundary оставался
`2026-09-07T02:52:09Z`. Разрывы 37→38 и 43→44 относятся к controller overhead
между прогонами. Счётчик округлён, поэтому quota delta — вторичная метрика, а
не способ пересчитать точные токены. Evaluator добавил 13 745 801 токенов,
14:23 времени и $8,0218; post-evaluator quota snapshot отсутствовал.

Сумма пяти delivery intervals — 841 202 785 токенов, $424,6409 и 10:15:57.
Вместе со слепым evaluator измеренный API-equivalent составляет $432,6627;
setup, reset и подготовка отчёта в эту сумму полностью не атрибутированы.

## Что нашёл evaluator

### Рой

Существенных дефектов в разрешённом evidence не найдено. Ограничения: live UAT
использовал одного principal; global SavedView grant не прошёл полный live
round trip; multi-user privacy и strongest-role были доказаны локально.

### Экономичный

- High: unversioned upsert активного Team grant может перезаписать более новую
  роль.
- Medium: grant update/revoke имеет TOCTOU между проверкой роли и mutation.
- Medium: People picker допускает свободный email через datalist.
- Low: мало focused keyboard/conflict/mobile UI evidence.

### Классический

- High: Viewer может прочитать состав Team grants, которым не может управлять.
- High: archived Team продолжает давать ACL-доступ.
- High: stale membership CAS способен частично сохранить membership.
- Medium: grant TOCTOU, простые People/Team controls и неполный Task sharing
  composition.

### Соло

Помимо лишнего confirmation blocker, evaluator нашёл продолжающий действовать
ACL archived Team, сохранение сырого resource ref, свободный email picker,
неполные exact-final gates и отсутствие живой проверки Team grants.

### Баланс

Результат исключён из ranking из-за запуска запрещённых backup/restore tests.
В коде также найдено расхождение server/UI: Project manager мог вызвать
Task-only Team-grant route через API, хотя UI это запрещал. Diff был существенно
шире остальных кандидатов.

## Исправление протокола

Обычные row-level изменения любых UAT D1 tables вне `teams`,
`team_memberships` и `team_grants` разрешены. Они не являются дефектом режима,
не сравниваются с baseline, не входят в reset gate и не восстанавливаются.
Контроллер между прогонами очищал только три Team-таблицы, возвращал видимое
состояние шести Tasks и восстанавливал frozen Git/UAT code и schema.

Первоначальный controller oracle ошибочно пытался сравнивать non-Team rows.
Правило исправлено ретроактивно до итоговой оценки; прежние проверки и repair
учтены только как controller overhead. Они не ухудшают баллы `Баланс`, `Рой`
или `Классический`. Hard-gate failure `Баланса` относится исключительно к
запрещённым backup/restore subtests.

## Воспроизводимость и ограничения

- Все пять delivery-runs стартовали строго последовательно от одного Git
  baseline `8d0b5d4090e8ad1d874b69da5b115e9efc7f8a45` на
  `gpt-5.6-sol`/`xhigh`; порядок был случайно заморожен заранее.
- Frozen prompt SHA-256:
  `3e62a12d25b955e2307b3e848809c54a0822839264131e01406a61bbd4ed1422`;
  rubric SHA-256:
  `2a8c3bf0da087527e452389715f636491c39b729b51b6b4d6f3c3c62b36f0ab5`.
- Blind evaluation JSON SHA-256:
  `7fb0bcb0d42470ae508c92988a2b75977dcd759d8839f24f40f098bde62ef1da`;
  Markdown SHA-256:
  `771da582c1babbddfd0610324e0a30b3efc04b6f7253e1c6bcbb1f47602932f7`.
- Raw artifacts:
  `~/Documents/Codex/benchmarks/issue-grinder-five-mode/20260901-00000000-0000-4000-8000-9fb1a6e0d9a5`.
- Evaluator-only packet:
  `~/Documents/Codex/benchmarks/issue-grinder-five-mode/evaluator-20260901-09c3e424`.
- Это пять единичных наблюдений, а не повторённый эксперимент. Порядок может
  смешиваться с обучением системы, cache и monotonic Task metadata.
- Protocol correction и controller followups были нужны в D и E. Их расход
  включён в interval totals, но не является candidate defect.
- Один UAT principal ограничивает живое доказательство multi-user ACL.
- Поэтому отчёт пригоден для выбора следующего default pilot, но не доказывает
  универсальное причинное превосходство режима.

## Финальная очистка

Временный reset API удалён из Task Manager `main` в
`c4db10844ef509a97f2d833939a1d6874b12ec7a` и опубликован в UAT v69. Hosted
flag и secret удалены, старый route с прежним валидным token возвращает 404,
read-back подтверждает `teams=0`, `team_memberships=0`, `team_grants=0`.
Access policy осталась `custom`: один owner, ноль групп и external visitors.
`TM-336` в Release 0.3 завершена. Product Production не читался, не изменялся и
не публиковался.
