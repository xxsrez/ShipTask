# Сравнение пяти режимов Issue Grinder

Статус: первый пилот завершён 2026-09-01 и признан непригодным для ранжирования;
итог зафиксирован в
[сравнительном отчёте](../reports/2026-09-01-issue-grinder-five-mode-benchmark.md).
Текущая редакция — исправленный runbook для следующей полной серии. Она не
переоценивает результаты первого пилота.
Delivery оставляла candidate до post-run capture, а очистку Team-данных и
возврат UAT baseline выполняла центральная сессия через временный узкий UAT
endpoint. После пяти прогонов и слепой оценки endpoint, flag, secret, тесты и
временная документация полностью удалены из `main` и UAT.

Уточнение протокола от 2026-09-01: межпрогонный reset данных ограничен тремя
Team-таблицами (`team_grants`, `team_memberships`, `teams`). Обычные изменения
строк в остальных UAT D1 tables не являются дефектом режима, не входят в reset
gate, не сравниваются с baseline и не восстанавливаются контроллером. Схема,
migration journal, Git/UAT code baseline и видимое состояние шести Tasks
по-прежнему восстанавливаются и проверяются.

Рабочие деревья и ветки первого пилота намеренно сохраняются как исторические
артефакты и evidence того запуска. Их наличие не является ошибкой готовности,
но ни один новый прогон не продолжает и не переиспользует их. Каждый новый
измеряемый или диагностический запуск получает новую верхнеуровневую Project
Task, новое рабочее дерево и новую ветку строго от заново замороженного
`baseline_sha`.

Это экспериментальный runbook, а не новый источник действующей policy Issue
Grinder. Канонические значения режимов описаны в
[пользовательском руководстве](../guides/issue-grinder-modes.md), а граница
имеющейся evaluation — в
[Issue Grinder evaluation](../skills/issue-grinder/evaluation.md). Текущий
детерминированный mode harness проверяет только механические решения и не
создаёт model-forward сессии, не исполняет Release и не измеряет качество;
поэтому настоящий benchmark организует внешний контроллер по этому документу.

## Назначение

Этот документ является заданием для отдельной центральной Codex-сессии. Она
должна подготовить воспроизводимый стенд, строго последовательно запустить пять
изолированных delivery-сессий с одним и тем же Release, восстановить исходное
состояние между прогонами и выпустить итоговый сравнительный отчёт.

Центральная сессия запускается как обычная Task в Project `Task Manager` на
`gpt-5.6-sol` с `xhigh`, не передаёт наблюдение за дочерними Tasks пользователю
и не заканчивает работу после dispatch. Она автономно ждёт каждую сессию,
снимает evidence, выполняет reset и продолжает до финального отчёта. Рутинных
вопросов пользователю не задаёт; настоящий непреодолимый authority или
infrastructure blocker оформляет как точный возобновляемый checkpoint.

Сравниваются пять канонических режимов Issue Grinder:

1. `Соло`;
2. `Классический`;
3. `Баланс`;
4. `Рой`;
5. `Экономичный`.

`По умолчанию` не участвует: это resolver, а не шестой режим. Единственным
содержательным различием входного prompt пяти delivery-сессий должно быть
явное название режима. Внутренняя topology и intended top-level profile,
определённые контрактом режима, являются частью измеряемого поведения.

В основной серии каждая верхнеуровневая delivery-сессия запускает skill Issue
Grinder сразу с явно заданным profile выбранного режима:

- `Экономичный` — Luna Max (`gpt-5.6-luna`, reasoning effort `max`);
- `Соло`, `Классический`, `Баланс` и `Рой` — Sol Extra High
  (`gpt-5.6-sol`, reasoning effort `xhigh`).

Controller обязан передать model и effort явно при создании delivery thread;
default или inherited profile не считается выполнением протокола. Это
единственный способ проверить обещание `Экономичного` без Sol. Отдельный
fixed-Sol-root diagnostic можно провести после основной серии, но его нельзя
смешивать с ranking: он измеряет overhead transport/authority оболочки, а не
обычный пользовательский `Экономичный`.

Эксперимент состоит ровно из одного комплекта пяти прогонов: по одному запуску
каждого режима. Повторные комплекты не планируются. Итог описывает эти пять
наблюдаемых запусков и не выдаётся за статистически устойчивый рейтинг режимов.

Перед полной серией разрешена отдельная короткая диагностическая перепроверка
одного режима, в том числе выбранного пользователем `Роя`. Она проходит те же
предстартовые проверки маршрутизации, тестирования и изоляции, всегда создаётся
в новом рабочем дереве и не становится шестой строкой сравнения. Её нельзя
ранжировать вместе со старым пилотом или использовать как продолжение старой
ветки.

Исправленный протокол прямо учитывает три ранних провала первого pilot:

- `Экономичный` прошёл с substantive Sol вместо Luna — теперь до дорогой работы
  обязателен actual routing canary и ранний mode-fidelity gate;
- `Соло` остановился на action-time Team-grant confirmation — unattended серия
  больше не считает живую Browser ACL mutation обязательной проверкой:
  Team-grant доказывается на exact candidate автоматическими тестами, а
  отсутствие живого access effect фиксируется как предел evidence, не blocker;
- локальный `attachments-integration.test.ts` ошибочно сочли запрещённым из-за
  содержащихся в нём backup/restore-проверок. Это безопасный локальный тест на
  временных D1/R2, поэтому delivery-сессии вправе запускать его и любые другие
  безопасные локальные проверки; их время и токены входят в стоимость режима.

Если любой из этих preconditions не доказан, новая серия не стартует. Это
важнее получения пяти строк результата любой ценой.

## Текущий целевой scope

- Task Manager Project: `Task Manager`
  (`00000000-0000-4000-8000-2c774e3f0238`).
- Release: `0.4` (`00000000-0000-4000-8000-923bce110ea6`), version `3`,
  lifecycle `planned`.
- Постоянная schema baseline: `TM-330` «Подготовить постоянную schema baseline
  для Teams», `Done` в Release 0.3. Она не входит в измеряемый функциональный
  scope и связана с Epic через `related`.
- Epic: `TM-329` «Добавить изолированные Teams для группового sharing».
- Измеряемые subtasks: `TM-335` — Team runtime/membership API; `TM-331` — Team
  grants; `TM-332` — каталог и карточка Team; `TM-333` — `People & Teams`;
  `TM-334` — ограничение persistent Teams-state тремя baseline-таблицами.

Зависимости scope образуют один проверяемый путь: `TM-335` блокирует `TM-331`
и `TM-332`; `TM-331` блокирует `TM-333`; `TM-331`, `TM-332` и `TM-333`
блокируют финальный `TM-334`.

Этот Release уже выбран пользователем как задача для проверки `Роя`. Отдельный
поиск другой candidate-friendly задачи не выполняется. `Рой` сам определяет,
для каких существенных частей этого scope полезны независимые варианты, и
стоимость таких вариантов является частью измеряемого поведения режима.

На 2026-08-31 Release содержит ровно шесть Tasks: `TM-329`, `TM-331`–`TM-335`.
Все шесть находятся в `Todo`, pagination завершена, незаявленных Tasks в
Release нет. Непосредственно перед первым run controller всё равно перечитывает
scope и сохраняет current versions, потому что этот snapshot может устареть.

Текущий Git/D1 baseline уже материализован:

- clean local `main`, `origin/main` и live remote `main` совпадают на
  `c4db10844ef509a97f2d833939a1d6874b12ec7a`;
- migration `drizzle/0038_purple_the_call.sql` и Drizzle journal создают
  `teams`, `team_memberships` и `team_grants`;
- UAT Sites version `69` сохранена из того же SHA;
- UAT D1 binding `DB` содержит 48 user tables, включая три Team tables;
- все три Team tables существуют с ожидаемыми columns и содержат `0` rows;
- targeted schema tests, typecheck, lint и build прошли.
- observed Issue Grinder package —
  `0.1.0+codex.20260901202349`, runtime `SKILL.md` SHA-256
  `8b34027e20d0d2d668489f2a1d7ed9f0e9c1cbc3001e793266508bda5ff436b8`;
  Task Manager adapter — `0.7.6+codex.20260827141835`.

Эти значения — проверенный кандидат на baseline, но controller повторно
замораживает их непосредственно перед run 1. Product Production в этот
baseline не входит.

### Предстартовый readiness audit

| Область | Состояние | Что осталось |
|---|---|---|
| Release scope и dependencies | Ready | Fresh reread перед snapshot |
| Git/schema baseline | Ready | Freeze live remote SHA перед run 1 |
| UAT schema и пустые Team tables | Ready | Freeze version/table manifest |
| Local build и targeted schema checks | Ready | Повторить на frozen SHA |
| Независимый UAT Team-data cleanup | Ready | После capture развернуть frozen `main`, удалить rows через временный authenticated UAT endpoint и подтвердить `0/0/0` |
| Task Manager visible-state reset | Ready | Обычные versioned mutations; history/version не откатываются |
| `TM-329`/`TM-334` handoff semantics | Ready | Task versions `36`/`32`: baseline deploy идёт до Team-only очистки, candidate остаётся до capture |
| Mode top-level profiles и wall-time ceiling | Требует повторной проверки | Sol/xhigh для Соло/Классического/Баланса/Роя, Luna/max для Экономичного; standard Task, максимум 8 часов |
| Model routing canary | Ready | 2026-09-01 live canaries: `Баланс` передал research/test в Luna Max; `Рой` создал двух независимых Luna Max candidates и Luna Max critic/reducer; Luna Max top-level автоматически выбрал `Экономичный` и выполнил substantive serial packet. Для `Соло` добавлена отдельная проверка: вся substantive delivery остаётся у одного execution owner, а service-provider agent сам по себе не считается нарушением. Перед серией повторить четыре canary на её frozen installed snapshot |
| Самопроверка delivery и независимая приёмка | Ready | Каждый режим свободно запускает безопасные локальные тесты; controller после handoff повторно выполняет одинаковый frozen acceptance suite exact candidate |
| Action-time access policy | Ready | Живая Browser ACL mutation исключена из unattended acceptance; Team-grant доказывается exact-candidate server/UI tests, а optional attended smoke не входит в ranking |
| Blind evaluator | Ready | Отдельная шестая `gpt-5.6-sol`/`xhigh` сессия после пяти delivery-runs |

UAT сейчас содержит одного registered User и не имеет direct access grants.
Поэтому multi-user membership, strongest-role и no-existence-leak допускается
доказывать обязательными server integration и UI/component tests exact
candidate. Специальная benchmark authorization fixture, фиксированное число
Teams и живая выдача доступа через Browser не требуются. Изменения строк в
existing tables разрешены и не требуют симметричного cleanup; контроллер между
прогонами очищает только три Team-таблицы.

## Роли и границы

### Пользователь

Пользователь уже выбрал Release 0.4 и поручил центральной сессии очистку только
трёх Team-таблиц в UAT между прогонами. Он запускает контроллер на
`gpt-5.6-sol` с `xhigh` в standard Task mode и не использует Codex или ChatGPT
Work до итогового отчёта. Благодаря этому interval token telemetry и недельная
quota delta не смешиваются с его параллельной активностью. Task Manager
возвращается в исходное видимое состояние только обычными versioned mutations.
Product Production не изменяется.

### Центральная сессия

Центральная сессия является контроллером эксперимента. Она:

- разрешает точные Project, Release, repository, UAT и baseline;
- фиксирует mode profile matrix, общий prompt, rubric и порядок прогонов;
- создаёт ровно одну верхнеуровневую delivery-сессию за раз;
- явно задаёт `gpt-5.6-sol`/`xhigh` для `Соло`, `Классического`, `Баланса` и
  `Роя`, `gpt-5.6-luna`/`max` для `Экономичного`, обычную Project Task и
  одинаковый ceiling 8 часов;
- во время активного прогона не занимается другой содержательной работой;
- независимо собирает метрики и evidence, не полагаясь только на self-report;
- возвращает видимое состояние Tasks, Git и UAT к baseline между прогонами;
- снимает post-run candidate до любого reset;
- не исправляет и не дополняет результат отдельного режима;
- после пяти прогонов и финального reset создаёт отдельную шестую evaluator-
  сессию на `gpt-5.6-sol`/`xhigh`, получает слепые оценки и готовит отчёт.

Контроллер не является шестым участником реализации. Его токены, время
подготовки, отката и оценки учитываются отдельно как стоимость benchmark
infrastructure.

### Delivery-сессия

Каждая delivery-сессия получает новый Codex thread и отдельный Git worktree от
одного frozen baseline. Она выполняет Release через Issue Grinder в явно
указанном режиме. Внутренние subagents разрешаются либо запрещаются самим
контрактом выбранного режима.

Старые benchmark worktrees и branches доступны контроллеру только как
неизменяемые исторические артефакты. Delivery-сессия не получает их пути,
названия или содержимое во frozen packet. Если платформа предлагает продолжить
старую Task, ветку или рабочее дерево, контроллер отклоняет такой запуск и
создаёт новую Project Task с новым worktree; удалять старые артефакты ради этого
не нужно.

Delivery-сессия не должна:

- читать ветки, worktrees, отчёты, session logs или результаты других
  прогонов;
- менять режим;
- переиспользовать незаявленный checkpoint другого прогона;
- менять `main` или сливать в него результат;
- изменять `db/schema.ts`, `drizzle/**`, D1 schema или migration journal;
- выполнять controller reset либо возвращать Git/UI/API к baseline до handoff;
- работать с product Production;
- создавать отдельные пользовательские Codex tasks вместо предусмотренной
  режимом внутренней topology.

Task Manager остаётся control plane. После capture центральная сессия обычными
versioned mutations возвращает Tasks в `Todo`, удаляет созданные прогоном
видимые comments и восстанавливает случайно изменённые поля. Monotonic versions,
timestamps, Activity history и обычные row-level изменения прочих UAT D1 tables
не откатываются, не входят в content fingerprint и запрещены как источник
контекста для последующих delivery-сессий. Product effects разрешены только в
подтверждённом UAT.

Backup/export/restore не являются частью controller setup, reset или
независимого acceptance suite. Контроллер их не вызывает и не изменяет. Это не
ограничивает самопроверку delivery-сессии: она вправе запускать безопасные
локальные export/backup/import/restore tests на временных D1/R2, и их стоимость
входит в измеряемый прогон. Полный fingerprint строк existing tables также не
снимается: он не относится к межпрогонному reset.

## Зафиксированная конфигурация и run manifest

Перед запуском контроллер заполняет и сохраняет этот manifest во внешнем
каталоге эксперимента:

```yaml
benchmark_id: <stable id>
task_manager_project: Task Manager / 00000000-0000-4000-8000-2c774e3f0238
target_release: 0.4 / 00000000-0000-4000-8000-923bce110ea6 / version 3
schema_baseline_task: TM-330 / Done / not measured
target_tasks: [TM-329, TM-331, TM-332, TM-333, TM-334, TM-335]
repository: /workspace/Task Manager
baseline_ref: main
baseline_sha: <freeze immediately before benchmark; observed candidate c4db10844ef509a97f2d833939a1d6874b12ec7a>
uat_target: task-manager-uat / Sites project appgprj_6a8215f500cc8191988eb7bf0564f573 / D1 binding DB
uat_baseline_version: <freeze; observed saved version 69>
teams_migration: drizzle/0038_purple_the_call.sql
protected_schema_paths: [db/schema.ts, drizzle/**]
team_tables: [teams, team_memberships, team_grants]
controller_cleanup_mechanism: temporary UAT-only authenticated REST endpoint after baseline redeploy
controller_cleanup_surface: POST /api/admin/benchmark/teams/reset
controller_cleanup_sql_sha256: <hash of the frozen three-statement SQL>
task_manager_reset_policy: visible-content-reset-without-history-rollback
controller_session_mode: standard project task
mode_top_level_profiles:
  solo: gpt-5.6-sol/xhigh
  classic: gpt-5.6-sol/xhigh
  balance: gpt-5.6-sol/xhigh
  swarm: gpt-5.6-sol/xhigh
  economical: gpt-5.6-luna/max
permission_profile: <exact effective profile>
maximum_wall_time_per_run: PT8H
mode_order_policy: randomized-once-before-run-1
blind_evaluator: separate sixth gpt-5.6-sol/xhigh session after final reset
expected_external_codex_activity: zero until final report
prompt_sha256: <hash of the frozen template>
rubric_sha256: <hash of the frozen acceptance rubric>
routing_oracle_sha256: <hash of expected semantic-role/model matrix>
controller_acceptance_sha256: <hash of exact controller checks and working directories>
access_effect_policy: unattended-no-live-browser-acl
metrics_schema_version: 4
issue_grinder_source: <installed package id/version and content hash>
task_manager_adapter: <installed package id/version>
```

Prompt, permission profile, tools, authority и ceiling должны быть одинаковыми
во всех пяти верхнеуровневых сессиях. Model/effort должны точно соответствовать
замороженной mode profile matrix. Если контроллер не может явно закрепить либо
наблюдаемо подтвердить значение, эксперимент не начинается.

## Артефакты эксперимента

Raw evidence не следует складывать в target repository или в ветки прогонов.
Контроллер создаёт отдельный owner-only каталог вида:

```text
<benchmark-root>/<benchmark-id>/
├── manifest.yaml
├── frozen-prompt.txt
├── acceptance-rubric.md
├── metrics-definition.json
├── routing-oracle.json
├── controller-acceptance.yaml
├── readiness.json
├── canaries/
│   ├── solo.json
│   ├── balance.json
│   ├── swarm.json
│   └── economical.json
├── order.json
├── baseline/
│   ├── git.json
│   ├── task-manager-visible-baseline.json
│   ├── controller-cleanup.json
│   ├── uat-deployment.json
│   ├── schema.sql
│   ├── schema-manifest.json
│   ├── schema.sha256
│   ├── migrations.json
│   ├── protected-schema.sha256
│   ├── protected-existing-data.json
│   ├── team-table-counts.json
│   ├── data-manifest.json
│   └── data.sha256
├── runs/
│   ├── A/
│   ├── B/
│   ├── C/
│   ├── D/
│   └── E/
├── resets/
├── overhead/
└── final/
```

Перед blind evaluation контроллер создаёт отдельный owner-only каталог
`<evaluator-root>/<benchmark-id>/` только с frozen rubric и пятью очищенными от
mode/process metadata packets `A..E`. Этот путь не является дочерним каталогом
`<benchmark-root>` и не содержит symlink или обратной ссылки на него.

Не сохранять secrets, bearer tokens, OAuth material, private signed URLs или
полное чувствительное содержимое Tasks. В manifest и отчёте использовать
стабильные refs, хэши и редактированные команды.

Каждая запись evidence содержит время в UTC и `Atlantic/Madeira`, источник,
команду или tool surface, exit/result status и SHA-256 сохранённого артефакта.

## Фаза 0. Разрешить scope и доказать готовность

Контроллер выполняет read-only preflight:

1. Разрешает точные Task Manager Project и Release, перечитывает все страницы
   scope и сохраняет Tasks, статусы, versions, hierarchy, relations, labels,
   comments и acceptance без усечения пагинации.
2. Проверяет, что Release содержит ровно `TM-329`, `TM-331`–`TM-335`, все шесть
   Tasks находятся в `Todo`, `TM-330` остаётся отдельной `Done` baseline Task,
   а hierarchy и relations соответствуют целевому scope. Любой незаявленный
   Task или lifecycle drift блокирует snapshot.
3. Разрешает repository и подтверждает чистый `main`, точный `baseline_sha` и
   совпадение с выбранным remote ref. Existing user changes не сбрасываются и
   не прячутся: при грязном либо неоднозначном baseline эксперимент не
   начинается.
4. Проверяет installed/enabled Issue Grinder, Task Manager adapter и доступные
   Codex tools. Сохраняет versions и хэши runtime payload.
5. Разрешает точный UAT target, baseline Sites version, D1 binding и три Team
   tables. Доказывает, что schema и migration `0038` уже входят в baseline,
   таблицы пусты, а controller умеет независимо удалить только Team rows без
   schema rollback. Product Production не читать и не изменять.
6. Проверяет доступность tool contract для создания fresh Project Task в
   отдельном worktree от frozen SHA и ожидания результата.
7. Проверяет доступность локальной token telemetry и account usage/reset
   evidence, включая `rate_limits.primary.used_percent` и `resets_at` для
   недельного окна. Если точное распределение по thread tree невозможно,
   включает строгий запрет любой другой Codex/ChatGPT Work активности на время
   каждого измерительного окна и явно маркирует interval totals как
   приближение.
8. Фиксирует ожидаемый weekly reset. Не начинает прогон в окне, где reset
   вероятен до его завершения.
9. Подтверждает, что во время каждого измерительного окна нет другой
   model-forward или пользовательской Codex/ChatGPT Work активности. Контроллер
   выполняет только минимальные wait/status и измерительные calls; их токены
   считаются overhead и не выдаются за токены delivery thread tree.
10. На установленном snapshot запускает mode-loading smoke для всех пяти
    режимов и четыре fresh routing canary: `Соло`, `Баланс`, `Рой`,
    `Экономичный`. Canaries не читают Task Manager и не меняют repository. Для
    каждого созданного child они сохраняют requested/observed model, effort,
    `agent_type`, semantic role и `fork_turns`; для top-level дополнительно
    сохраняют фактически выбранный canonical mode. В `Соло` один execution
    owner обязан сам выполнить анализ, реализацию, тест и self-review; child,
    которому передана любая из этих обязанностей, блокирует серию. Внешний
    Strategic Explainer или другой bounded service-provider не считается
    execution-child, пока не выполняет delivery-работу. `Баланс` обязан
    показать Luna research/test packet до root implementation; `Рой` — минимум
    два разных Luna candidates и Luna critic/reducer. В `Экономичном` Luna Max
    top-level должна автоматически выбрать canonical mode и выполнить
    substantive serial packet. Создание отдельного child там не обязательно;
    если режим всё же создаёт child, его observed model также должна быть Luna
    Max. Sol или GPT-5.4 в substantive дереве любого из этих canaries блокирует
    дорогую серию до исправления runtime.
11. Замораживает независимый controller acceptance suite: одинаковые команды,
    test files и working directories, которые controller повторно запускает на
    exact candidate каждого режима после handoff. Этот suite не ограничивает
    собственные безопасные локальные тесты delivery-сессии.
12. Сохраняет предыдущие benchmark branches/worktrees как read-only
    исторические артефакты, не удаляет и не продолжает их. Проверяет, что их
    identity и содержимое не доступны через frozen packet, а audit rule
    признаёт чтение чужой ветки, worktree или thread contamination incident.

Любая неизвестная environment mapping, недоступная прямая Team cleanup или
неустранимая конкурирующая активность являются ошибкой подготовки. Они не
засчитываются как результат режима.

## Фаза 1. Заморозить общий вход

До просмотра любого результата контроллер замораживает:

- полный видимый Release snapshot и правила его логического reset;
- Git baseline SHA;
- UAT deployment и весь восстанавливаемый state;
- installed Issue Grinder payload;
- одинаковый prompt template;
- mode profile matrix и общий permission profile;
- routing oracle и правила mode-fidelity gate;
- независимый controller acceptance suite;
- один access-effect policy для всех пяти прогонов;
- максимальное время прогона;
- acceptance oracle и правила оценки;
- перечень обязательных и вторичных метрик;
- правила классификации infrastructure failure;
- случайный порядок пяти режимов.

Порядок сохраняется в `order.json` как отображение `A..E → mode`. До фиксации
слепых оценок файл не используется для названий веток, таблиц качества или
evaluation packet. Если пользователь заранее задаст порядок, он заменяет
randomization, но также замораживается до первого прогона.

### Acceptance oracle

Контроллер выводит rubric из полного Release и repository acceptance до первого
прогона. Rubric должен содержать:

- требуемые пользовательские outcomes каждого Task;
- hard gates для integrity, authorization, migrations и exact environment
  identity;
- одинаковый набор unit, integration, build, migration и UAT checks;
- ожидаемые UI/API/Agent API/MCP surfaces, если они входят в Release;
- правила тяжести дефектов;
- способ оценить частично готовый или resumable результат;
- критерий `accepted`, который нельзя заменить количеством Tasks в `Done`.

#### Frozen quality rubric

Hard gates применяются до числового score:

1. zero diff в `db/schema.ts` и `drizzle/**`, отсутствие runtime DDL и
   неизменный migration journal;
2. build/typecheck/lint и обязательные targeted tests проходят на exact
   candidate;
3. UAT version собрана из exact candidate SHA и проходит baseline плюс
   Teams/People & Teams smoke; обычные UAT-действия разрешены, но создание,
   изменение и отзыв живого доступа через Browser в этот smoke не входят;
4. обязательные server integration и UI/component tests exact candidate
   подтверждают server-side authorization, Team-grant create/update/revoke,
   Viewer denial, Project inheritance и no-existence-leak;
5. post-run candidate снят до reset, затем три Team-таблицы очищены и
   ограниченный baseline gate снова зелёный;
6. Task Manager lifecycle и комментарии правдиво соответствуют evidence.

Отсутствие живой `team_grants` строки в UAT unattended-прогона не является
hard-gate failure и не запрещает terminal completion. Оно явно записывается как
предел live evidence; соответствующая функциональность обязана быть доказана
автоматическими тестами exact candidate. Rubric не может требовать Browser
submit, который меняет permissions/access.

Hard-gate failure даёт `accepted=false`, но diagnostic score всё равно
сохраняется. Слепой score имеет 100 баллов и замораживается до run 1:

| Область | Баллы |
|---|---:|
| `TM-335`: Team runtime и membership API | 20 |
| `TM-331`: Team grants и effective-role ACL | 25 |
| `TM-332`: каталог Teams и карточка участников | 15 |
| `TM-333`: `People & Teams` и прозрачность access routes | 15 |
| `TM-334`: очищаемый Team-state и evidence трёх baseline-таблиц | 10 |
| Инженерная целостность: tests, UAT evidence, lifecycle, maintainability | 15 |

Каждая область получает одинаковые заранее записанные subcriteria. Баллы не
добавляются за объём diff, число агентов, уверенный self-report или красивый
комментарий без evidence.

После первого старта rubric разрешено менять только из-за доказанной ошибки
самого oracle. В таком случае текущий pilot останавливается, изменение
документируется, а уже выполненные прогоны не сравниваются с последующими.

### Mode-fidelity gate

Quality rubric применяется только после отдельного process gate. Controller
рекурсивно читает delivery thread tree и сверяет каждый child с frozen routing
oracle по semantic role, `agent_type`, requested/observed model, effort и
`fork_turns`. Для трёх исправленных режимов обязательны:

- `Баланс`: Luna Max выполняет обычные research/implementation/tests/critique;
  Sol допускается только для material decision, integration owner и final gate;
- `Рой`: все scouts/candidates/critics/test authors/judges/reducers — Luna Max,
  а candidate-friendly scope содержит хотя бы одну wave `M >= 2`;
- `Экономичный`: top-level и вся substantive работа — Luna Max, Sol/GPT-5.4
  отсутствуют в delivery tree.

Первое нарушение останавливает run до следующей дорогой wave с outcome
`mode_routing_invalid`. Такой candidate можно сохранить для диагностики, но он
не получает quality/efficiency rank и не доказывает свойства режима. Отсутствие
recursive telemetry также делает mode fidelity непроверяемой и блокирует серию.

### Два независимых уровня тестирования

Каждая delivery-сессия сама отвечает за реализацию и самопроверку результата.
Она обязана запустить достаточные проверки exact candidate и вправе выбирать
любые безопасные локальные unit, integration, component, build и другие тесты,
включая полный набор и повтор после исправления. Controller не выдаёт ей
allowlist, denylist или command guard. Все выбранные режимом проверки, повторы,
время и токены остаются внутри его измерительного окна.

После terminal handoff controller независимо запускает на exact candidate один
и тот же заранее замороженный acceptance suite. Только этот общий повторный
набор является сопоставимым внешним доказательством качества пяти кандидатов;
self-report и логи delivery его не заменяют. Controller checks учитываются
отдельно как одинаковая инфраструктурная стоимость benchmark и не приписываются
режиму.

Жёсткие ограничения относятся не к названиям тестов, а к реальным эффектам:
delivery по-прежнему не получает права на Product Production, живое изменение
permissions/access через Browser, внешних получателей или другие запрещённые
действия. Локальные проверки на временных D1/R2 такими эффектами не являются.

## Фаза 2. Снять baseline и зафиксировать reset

### Task Manager

Task Manager возвращается в исходное видимое состояние только обычными
versioned mutations через adapter.

1. Сохранить content baseline шести Tasks: refs, titles, descriptions, status,
   priority, assignee, labels, Release membership, parent, relations, due date,
   archive state и список видимых comments.
2. Зафиксировать разрешённые delivery-effects: переходы статусов и native
   evidence comments внутри выбранного Release. Изменение описаний, hierarchy,
   relations, labels, assignee или Release membership не является штатным
   эффектом и отдельно учитывается как drift.
3. После post-run capture удалить native comments, созданные текущим прогоном,
   вернуть все шесть Tasks в `Todo` и точечно восстановить любой изменённый
   content field через current version.
4. Перечитать Release без усечения pagination и доказать совпадение content
   baseline, отсутствие видимых comments текущего прогона и неизменность
   hierarchy/relations.

Task versions, `updatedAt` и Activity являются монотонной историей и намеренно
не откатываются. Они не входят в content baseline и не используются как вход
последующих delivery-сессий. Frozen prompt запрещает delivery-сессии читать
Activity. Центральная сессия может после `finished_at` прочитать bounded
Activity только для измерения lifecycle truthfulness; такой read учитывается
как controller overhead, не попадает в следующий frozen packet и не передаётся
blind evaluator. Перед новым run видимый comment list снова пуст. Если run
оставил информацию, которую нельзя убрать обычными Task Manager mutations,
серия останавливается.

Монотонные versions и timestamps видимы в connector responses, поэтому
идеальная слепота delivery-сессий по позиции прогона недостижима. Это заранее
фиксируется как limitation: режиму запрещено использовать metadata как контекст,
контроллер не добавляет её в prompt, а итоговый анализ проверяет, не коррелируют
ли результаты с run position.

### Git и UAT application

1. Зафиксировать clean `baseline_sha`; `main` во время эксперимента не
   перемещается.
2. Сохранить точную identity текущего UAT deployment и способ повторно
   опубликовать baseline build.
3. Сохранить read-only smoke baseline.
4. Каждый прогон получает новый opaque worktree/branch `A..E` от того же
   `baseline_sha`. Ветки сохраняются до окончания слепой оценки и не вливаются
   друг в друга. Ни одна ветка или рабочее дерево первого пилота не может быть
   base, recovery point или местом выполнения нового прогона; старые артефакты
   при этом не удаляются.

### D1 schema, migration ledger и data

Schema является постоянным входом эксперимента, а не результатом режима.
Migration `0038_purple_the_call` заранее применена; Team tables остаются между
прогонами. Ни один candidate не вправе менять schema или migration journal.

Сохранить нормализованный структурный manifest, который детерминированно
сортирует и включает:

- application tables и table flags;
- columns, types, nullability, defaults и primary keys;
- indexes, uniqueness, partial/expression definitions и indexed columns;
- foreign keys;
- views и triggers;
- полный allowlist учитываемых служебных объектов.

Состояние применённой migration и Drizzle journal сохраняется отдельно.
Pre-deploy guard каждого candidate обязан доказать zero diff для
`db/schema.ts` и `drizzle/**` и отсутствие runtime DDL (`CREATE`, `ALTER`,
`DROP`). При schema diff candidate не публикуется в общую UAT; это defect
режима, а не повод изменить baseline.

Новые Team, membership и Team-grant rows являются расходными. Controller
очищает их только после post-run capture, в dependency-safe порядке:

```sql
DELETE FROM team_grants;
DELETE FROM team_memberships;
DELETE FROM teams;
```

Команды выполняются центральной сессией через временный authenticated UAT-only
endpoint `POST /api/admin/benchmark/teams/reset`. Endpoint включается только
явным UAT marker, feature flag и отдельным secret, не принимает SQL или имена
таблиц и исполняет ровно три замороженных `DELETE` в указанном порядке.
`DROP TABLE` и изменение migration запрещены. Таблицы используют text IDs,
поэтому отдельного autoincrement sequence reset не требуется.

Очистка не является частью candidate: после post-run capture центральная
сессия сначала повторно развёртывает сохранённую UAT version из frozen `main`,
затем вызывает endpoint и через независимую read-only Sites surface
подтверждает `0/0/0`. Неполный `0/0/0` либо schema drift останавливает серию.
Row-level drift в прочих D1 tables не проверяется и не блокирует серию. После
пяти прогонов и слепой оценки временный endpoint, его flag, secret, тесты и
документация обязательно удаляются из `main` и UAT, а старый route должен
возвращать `404`.

Отдельный data manifest включает:

- `0` rows во всех трёх Team tables на baseline;
- current Project/Task/Release/SavedView refs, direct grants, workflow и task
  identifiers;
- видимое Task Manager состояние, которое контроллер восстанавливает обычными
  versioned mutations.

Dedicated Team, membership и Team-grant rows должны жить в трёх Team-таблицах,
чтобы exact cleanup оставался ограниченным и воспроизводимым. Обычные продуктовые
записи в existing D1 tables разрешены, не считаются drift и не требуют от
контроллера дополнительного cleanup либо fingerprint-сравнения.

Если Release способен писать в R2, очереди, фоновые jobs или внешние UAT
resources, такой effect запрещается во всех пяти прогонах, пока для него не
зафиксирован отдельный симметричный cleanup.

### Action-time access policy

Основная сравнимая серия всегда unattended. Создание, изменение и отзыв
реального доступа через Browser заранее исключены из её acceptance и hard
gates. Browser/UI проверяет, что Teams и People & Teams открываются, показывают
правильные controls, роли, inheritance explanations и текущее состояние, но не
нажимает кнопку, создающую, меняющую или отзывающую ACL route.

Team-grant create/update/revoke, strongest-role, Viewer denial,
no-existence-leak и несколько пересекающихся Team routes доказываются
обязательными server integration и UI/component tests exact candidate. Эти
тесты не ограничиваются одной Team и не требуют отдельной benchmark fixture.

Если Browser или другой interactive surface всё же сообщает о необходимом
action-time confirmation для исключённого live ACL smoke, режим прекращает
только эту проверку, записывает точный предел live evidence и продолжает
terminal reconciliation. Он не вызывает `request_user_input`, не ждёт ответа и
не превращает пропущенный live effect в blocker либо defect реализации.

Настоящий live access smoke можно провести один раз отдельно после завершения
всей серии. Он является attended продуктовой проверкой вне пяти measured runs,
не влияет на ranking и не меняет их outcomes.

## Фаза 3. Заморозить prompt delivery-сессии

Создать один текстовый шаблон. Пять фактических prompt должны быть
byte-identical после подстановки одного поля `<MODE>`:

```text
Выполни точно выбранный Task Manager Release <TARGET_RELEASE> через
$issue-grinder в явном режиме <MODE>.

Repository, Task Manager Project, UAT target, baseline, разрешённые полномочия
и acceptance перечислены ниже. Product Production полностью запрещён; обычный
подтверждённый UAT workflow разрешён. Работай автономно в пределах Issue
Grinder contract до terminal результата, настоящего blocker либо допустимого
контрактом Экономичного режима resumable checkpoint.

Не меняй выбранный режим. Не читай и не переиспользуй никакие benchmark-ветки,
worktrees, сессии, отчёты или результаты других прогонов. Не изменяй main и не
сливай результат в него. Внутреннюю topology выбирай только по контракту
указанного режима.

До содержательной child-work соблюдай model-routing gate установленного Issue
Grinder: сохрани requested и observed profile receipts. Несовпадение model,
effort, platform agent type или semantic role не исправляй дорогой root-работой;
останови wave и верни evidence контроллеру.

Не читай Task Manager Activity. Monotonic Task versions и timestamps являются
только transport metadata, а не контекстом задачи; используй current Task
descriptions, hierarchy, relations и видимый comment list.

Teams schema уже является частью baseline. Не изменяй db/schema.ts, drizzle/**,
D1 schema или migration journal и не выполняй runtime DDL. До UAT publication
докажи zero protected-schema diff; при недостаточной schema честно остановись
с blocker.

Заверши handoff с exact candidate, доступным для post-run capture. Для TM-334
докажи изоляцию, rows и read-back таблиц teams, team_memberships и team_grants
обязательными автоматическими тестами exact candidate; live UAT read-back
фиксирует фактически созданные строки, но наличие живой team_grants строки не
является hard gate unattended-прогона. Обычные row-level изменения в прочих UAT
D1 tables разрешены, не являются delivery/reset gate и не требуют доказательства
полного non-Team zero diff. Не трать время на такой fingerprint или ремонт. Не
реализуй и не запускай межпрогонный cleanup; его после capture выполняет
центральный controller только для трёх Team-таблиц.

Самостоятельно выбери и запусти достаточные безопасные локальные проверки exact
candidate. Можно использовать любые test files, test runners, полный набор и
обоснованные повторы; не рассчитывай, что последующая независимая проверка
контроллера заменит твою самопроверку. В measured run не создавай, не меняй и не
отзывай permissions/access через Browser. Такой live submit не входит в
acceptance: докажи Team-grant автоматическими server integration и UI/component
tests exact candidate. Если interactive surface требует action-time
confirmation, пропусти только этот live check, запиши предел evidence и
продолжай до terminal результата без вопроса пользователю и без blocker.

<FROZEN_RELEASE_AND_ENVIRONMENT_PACKET>
```

`<TARGET_RELEASE>` и `<FROZEN_RELEASE_AND_ENVIRONMENT_PACKET>` предварительно
подставляются один раз в общий текст. При создании пяти prompt меняется только
`<MODE>`. Titles, opaque branch labels и app metadata не должны раскрывать mode
будущему blind evaluator.

Не добавлять mode-specific советы, лимиты агентов, способы декомпозиции или
подсказки по реализации. Это изменило бы предмет эксперимента.

Task Manager versions `TM-329@36` и `TM-334@32` уже содержат то же явное
разделение ответственности. Перед run 1 controller перечитывает их и
останавливается при смысловом drift.

## Фаза 4. Один последовательный прогон

Для каждого opaque run `A..E` контроллер проходит одну и ту же state machine.
Новая верхнеуровневая delivery-сессия не создаётся, пока предыдущая не
завершилась и baseline не доказан заново.

### 4.1 Pre-run gate

1. Убедиться, что ни одна другая Codex/ChatGPT Work задача не активна на этом
   account, кроме контроллера.
2. Подтвердить clean frozen `main`, создать именно новый worktree от
   `baseline_sha` и доказать, что его path, branch и Task identity не совпадают
   ни с одним сохранённым benchmark artifact. Старые worktrees остаются на
   месте и не считаются загрязнением сами по себе.
3. Сверить Task Manager visible-content fingerprint с baseline; монотонные
   versions, timestamps и Activity не сравнивать и не читать как context.
4. Сверить UAT baseline version, protected-schema hash, migration identity,
   `teams=0`, `team_memberships=0`, `team_grants=0` и smoke с baseline. Строки
   прочих D1 tables не сравнивать и не восстанавливать.
5. Снять account usage/reset snapshot, включая raw `used_percent`, вычисленный
   `usage_remaining_percent = 100 - used_percent`, `resets_at`, текущую
   UTC/Madeira time и telemetry boundary.
6. Создать новую обычную Project Task в новом отдельном worktree строго от
   `baseline_sha`, задав exact top-level profile из mode matrix, общие
   permissions и prompt для текущего mode. Возобновление прежней Task или
   повторное использование её worktree запрещено. Ceiling этой Task — 8 часов.
7. Сохранить thread ID, host ID, worktree/branch identity и фактический
   стартовый SHA.

Любое несовпадение останавливает state machine до восстановления. Таймер режима
не запускается на грязном baseline.

### 4.2 Active run

1. Зафиксировать `started_at` непосредственно перед dispatch.
2. Дождаться результата через thread wait/status mechanism. Внутренние workers
   выбранного режима могут работать параллельно; пять верхнеуровневых прогонов
   — никогда.
3. Сразу после первой dispatch wave снять recursive thread-tree snapshot и
   применить mode-fidelity gate. Пока exact child routing не подтверждён, run не
   переходит к основной implementation wave. Любой inherited Sol, GPT-5.4 или
   отсутствие обязательной Luna topology останавливает run как
   `mode_routing_invalid` и экономит оставшийся budget.
4. Наблюдать command events и останавливать run только при попытке запрещённого
   реального эффекта, включая создание, изменение или отзыв live ACL через
   Browser. Безопасные локальные тесты и их повторы не являются нарушением.
5. Контроллер во время ожидания не анализирует код, не запускает другую модель
   и не помогает delivery-сессии.
6. Не посылать discretionary follow-up. Вопрос, ответ на который уже содержится
   в frozen packet, является дефектом самостоятельности прогона, а не поводом
   выдавать одному mode дополнительный context.
7. Если выявился общий отсутствующий факт или authority, без которого не мог бы
   честно продолжить ни один режим, остановить весь pilot. После исправления
   общего packet начать сравнимую серию заново.
8. Если достигнут одинаковый frozen wall-time ceiling, остановить только
   безопасным способом, сохранить checkpoint и классифицировать outcome по
   заранее заданным правилам.

### 4.3 Post-run capture

До любого отката сохранить. `finished_at` ставится только после terminal root
result и quiescence всех descendants; иначе поздние worker tokens и effects
выпадут из измерительного окна:

- `finished_at`, wall time и time to first reviewable candidate, если он
  наблюдаем;
- terminal outcome: `accepted | failed | blocked | resumable_checkpoint |
  timed_out | mode_routing_invalid | protocol_invalid | infrastructure_invalid`;
- recursive thread tree, requested/observed модели/efforts, semantic roles,
  routing receipts и число фактически запущенных agents;
- exact branch, base SHA, candidate SHA, dirty state и diff summary;
- protected-schema diff и поиск runtime DDL;
- commits, attempts, candidate waves, retries и rejected candidates, насколько
  это объективно извлекается из evidence;
- все самостоятельно выполненные delivery checks и повторы с их результатами;
- результаты отдельного controller acceptance suite exact candidate;
- Task Manager statuses, versions, comments и fresh Release inventory;
- UAT deployment identity, schema/data/migration fingerprints, R2/background
  state и logs/smoke evidence;
- raw results всех применимых rubric checks;
- known defects, unknowns, deferred gates и blocker/checkpoint contract;
- account usage/reset snapshot с `used_percent`, `usage_remaining_percent` и
  `resets_at`, а также token telemetry end boundary;
- audit чтения других benchmark branches/worktrees/threads;
- self-report delivery-сессии как отдельный, неавторитетный источник.

После capture raw artifacts сделать read-only и сохранить их SHA-256. Ветка
результата остаётся доступной для поздней blind evaluation.

## Фаза 5. Контролируемый reset между прогонами

Reset выполняет только центральная сессия, вне измеряемого delivery interval.
Его время и токены записываются как benchmark overhead.

1. Дождаться quiescence writers, deploys, migrations и background jobs текущего
   run. Не менять state, пока его ещё меняет активный процесс.
2. Зафиксировать последнюю post-run identity всех surfaces.
3. Сохранить benchmark branch/worktree; не merge и не удалять её.
4. Повторно развернуть frozen UAT baseline saved version из `baseline_sha`;
   candidate code для очистки не вызывать.
5. Через frozen authenticated UAT-only endpoint выполнить точный Team reset в
   порядке `team_grants` → `team_memberships` → `teams` и сохранить counts
   до/после.
6. Независимо перечитать Team tables через read-only Sites database surface и
   подтвердить `0/0/0` и неизменность schema/migration. Прочие D1 tables не
   проверять на row-level diff и не очищать.
7. Выполнить baseline smoke.
8. Через Task Manager adapter удалить native comments текущего run, вернуть
   шесть Tasks в `Todo` и точечно вернуть любые изменённые content fields к
   frozen values.
9. Перечитать Release и подтвердить visible-content fingerprint. Monotonic
   versions, timestamps и Activity не сбрасывать и не использовать как context
   следующего run.
10. Подтвердить, что `main` по-прежнему указывает на `baseline_sha` и clean;
    повторно построить остальные fingerprints и выполнить baseline smoke.
11. Сохранить reset report: начало/конец, baseline deployment identity,
    D1 write surface, SQL hash, counts до/после, Task Manager mutations,
    команды/tools, остальные hashes, результаты проверки и обнаруженный drift.

Следующий прогон разрешён только при одновременном выполнении:

```text
Task Manager visible-content fingerprint == baseline
Task Manager visible comments from prior run == 0
Git main SHA and cleanliness == baseline
UAT deployment identity == baseline
D1 structural schema hash == baseline
D1 migration ledger == baseline
teams == 0 and team_memberships == 0 and team_grants == 0
R2/background state == baseline or proven irrelevant
baseline smoke == passed
no active writer/deploy/migration/job from prior run
```

Если хотя бы одно условие не доказано, benchmark останавливается. Нельзя
объявлять reset успешным по одному deploy version, визуально пустому списку
Tasks или совпавшему `schema.sql`.

## Неизменяемость схемы каждого кандидата

В этом benchmark UAT schema обязана совпадать с baseline до и после каждого
run. Для каждого candidate controller:

1. до UAT publication сравнивает `db/schema.ts` и `drizzle/**` с
   `baseline_sha`; любой diff блокирует publication;
2. ищет runtime DDL и иные обходные пути изменения schema;
3. после candidate deployment снова строит table/column/index manifest и
   сравнивает migration identity;
4. подтверждает, что Team-specific persistent state осталось только в
   `teams`, `team_memberships`, `team_grants`;
5. после cleanup повторяет те же проверки.

Добавление Team columns или ownership semantics в существующие `users`,
`projects`, `tasks`, `releases`, `saved_views`, workflow/status или task
identifier structures является hard-gate failure. Если schema mutation всё же
попала в общую UAT, текущий candidate получает failure, а серия останавливается
как contaminated infrastructure до доказанного восстановления.

## Метрики

Набор, definition и source каждой метрики замораживаются до run 1. Поздно
найденную диагностику можно добавить отдельно, но нельзя задним числом менять
primary ranking.

### Primary decision metrics

Сравнение лексикографическое, без одной непрозрачной формулы:

1. `accepted` и число пройденных hard gates;
2. слепой quality score `0..100` по frozen rubric;
3. токены дефицитного controller/reviewer profile;
4. total observable tokens;
5. wall-clock time до terminal outcome/checkpoint.

Дешёвый непринятый результат не побеждает принятый. `Экономичный` resumable
checkpoint является валидным контрактным outcome, но не равен принятому
Release; для него отдельно показываются выполненные gates, полезность exact
candidate и оценка оставшегося rework.

### Outcome и качество

| Метрика | Определение | Source |
|---|---|---|
| `terminal_outcome` | `accepted`, `failed`, `blocked`, `resumable_checkpoint`, `timed_out`, `infrastructure_invalid` | thread final + controller reconciliation |
| `hard_gates_passed` | число зелёных gates из frozen списка и их bitset | raw checks |
| `blind_quality_score` | `0..100` до раскрытия mode; `not_scorable` для infrastructure-invalid run | evaluator packet |
| `task_scores` | отдельные баллы `TM-331`–`TM-335` и Epic integrity | frozen rubric |
| `defects_by_severity` | blocker/critical/major/minor с evidence | blind review |
| `escaped_defects` | дефекты, найденные только после self-declared terminal result | controller/evaluator |
| `rework_to_acceptance` | одинаково оценённые человеко- или agent-minutes и material change count | frozen rework protocol |
| `lifecycle_truthfulness` | premature `Done`, reopen/correction, unsupported claims | Task Manager history + evidence |

### Токены, профили и quota

Для каждого run и каждой наблюдаемой модели считать три непересекающиеся
категории:

- `Cached input = cached_input_tokens`;
- `Input = input_tokens - cached_input_tokens`;
- `Output = output_tokens`.

Denominator: `Cached input + Input + Output`. Официальный Responses contract
также различает input, cached-input details, output и reasoning details, но
источником чисел benchmark остаётся локальная Codex telemetry, а не
[API schema](https://developers.openai.com/api/reference/cli/resources/responses/methods/create).

Основная token table строится по root delivery thread и всем его descendants,
если task telemetry позволяет надёжную attribution. Отдельно локальный
`codex-token-usage-report` запускается на точном полуоткрытом интервале
`[started_at, finished_at)` и сохраняет JSON плюс Markdown. Он читает
active/archived telemetry и подавляет известные cumulative/fork replays;
простое суммирование JSONL запрещено. Текущий helper не фильтрует по thread ID,
поэтому account interval служит reconciliation total и включает минимальные
wait/status calls контроллера. Он не объявляется чистым расходом режима. Если
thread-tree attribution недоступна, token comparison получает low-confidence
verdict, а interval total маркируется `interval_estimate`.

Дополнительно считать:

- tokens по model и role, насколько thread tree позволяет attribution;
- `scarce_profile_tokens` и `economical_profile_tokens` отдельно;
- cache share `Cached input / total input`;
- output/input ratio;
- API-equivalent list-price cost только для моделей с текущей официальной
  публичной ценой; это не subscription charge и не фактический quota расход.

#### Остаток недельной квоты

Остаток недельной квоты является обязательной ресурсной метрикой каждого run,
хотя его точность ниже token telemetry. Контроллер сохраняет raw account-usage
snapshot непосредственно перед `started_at` и сразу после `finished_at`, когда
все descendants уже quiescent. Для weekly window записываются:

| Поле | Определение |
|---|---|
| `weekly_used_before_percent` | observed `rate_limits.primary.used_percent` до dispatch |
| `weekly_remaining_before_percent` | `100 - weekly_used_before_percent` |
| `weekly_used_after_percent` | observed `rate_limits.primary.used_percent` после quiescence |
| `weekly_remaining_after_percent` | `100 - weekly_used_after_percent` |
| `weekly_quota_consumed_percentage_points` | `remaining_before - remaining_after` |
| `weekly_resets_at_before/after` | observed weekly reset boundary в обоих snapshots |
| `weekly_usage_capture_at_before/after` | фактическое UTC-время обоих чтений |

Дополнительно сохраняется весь доступный redacted `rate_limits` object, чтобы
не потерять вторичные окна, если структура telemetry изменится. Локальный
`codex-token-usage-report --list-resets` используется для подтверждения, что
выбран именно стабильный weekly window, а не соседний session/short window.
Контроллер также снимает snapshots в начале и конце всего benchmark и на
границах reset/evaluation overhead. Если вся серия помещается в одно weekly
window и разрешение счётчика достаточно, остаток между total delta и суммой run
deltas показывается как наблюдаемый controller overhead. При reset между runs
или грубом округлении overhead показывается по token telemetry, а quota residual
не выдумывается.

Интерпретация строгая:

- во время interval не запускается никакая другая пользовательская или
  model-forward Codex/ChatGPT Work activity; остаются только измеряемый delivery
  tree и минимальные controller wait/status calls;
- одинаковый `resets_at` до/после обязателен; reset внутри run делает quota
  delta инфраструктурно невалидной;
- положительная разница remaining показывает наблюдаемую долю недельной квоты,
  потраченную delivery tree вместе с неизбежным controller observation
  overhead; она не считается точной per-mode attribution;
- неизменившийся округлённый процент означает «расход меньше разрешения
  счётчика», а не доказанный нулевой расход;
- рост remaining без reset, отсутствие поля или несовместимые snapshots
  помечаются `quota_measurement_invalid`;
- quota delta показывается рядом с точными токенами, но не участвует в primary
  ranking и API-equivalent расчётах из-за низкой гранулярности и возможной
  нелинейности subscription quota.

Prompt cache создаёт order effect: поздние runs могут получить больше cached
input из общего frozen prefix. Поэтому cache share и run position обязательны в
отчёте, порядок рандомизируется, а устойчивый вывод требует нескольких полных
пятёрок с новой перестановкой.

### Время

- dispatch-to-first-event latency;
- time to first reviewable candidate;
- time to first green typecheck/test/build;
- time to first successful UAT candidate;
- wall-clock time до terminal result/checkpoint;
- суммарные agent-seconds и peak concurrency, если доступны;
- baseline redeploy и Team-only cleanup operation;
- Task Manager logical reset, baseline redeploy и полное reset overhead;
- blind evaluation time.

Setup/capture/reset/evaluation time не приписывается режиму и показывается
отдельно. Queue/service latency сохраняется, но не смешивается с active work.

### Процесс и автономность

- фактическое число agents, peak concurrency, waves и role/profile routing;
- implementation attempts, candidate branches, handoffs и material rework
  cycles;
- tool calls по классам, failed calls и retries;
- test/build/UAT attempts, first-pass success и flaky reruns;
- commits, changed files и added/deleted lines только как диагностика, не как
  quality proxy;
- вопросы пользователю, controller follow-ups и другие human interventions;
- mode drift, чужая branch/worktree/thread access и prompt deviations;
- Task Manager transitions/comments и число исправлений преждевременного
  lifecycle;
- compactions/interruption/resume events, если они наблюдаемы.

### Integrity и reset guardrails

- protected-schema diff count должен быть `0`;
- runtime DDL count должен быть `0`;
- post-reset Team counts должны быть `0/0/0`;
- baseline redeploy/read-back и Task Manager visible-content fingerprint должны
  совпасть;
- Production effects, cross-run reads и unapproved external effects должны быть
  `0`;
- Task Manager Activity reads со стороны delivery-сессии и видимые comments
  предыдущего run должны быть `0`; bounded post-run Activity read контроллера
  разрешён и учитывается отдельно;
- Team-only cleanup operation должна завершиться успешно и независимо
  подтвердиться counts `0/0/0`.

### Производные показатели

Только для accepted candidates с надёжным denominator рассчитывать:

- `blind_quality_score / scarce_profile_tokens_million`;
- `blind_quality_score / total_tokens_million`;
- `time_to_accepted_outcome`;
- API-equivalent cost на один quality point;
- rework-adjusted time до acceptance.

Производные никогда не скрывают абсолютные значения. Weekly quota delta не
используется в denominator из-за грубой гранулярности и возможной нелинейности.

## Слепая итоговая оценка

До чтения `order.json` контроллер формирует для веток `A..E` одинаковые
evaluation packets:

- exact base/candidate identity;
- diff и migrations без mode/thread labels;
- raw checks и UAT evidence;
- Task Manager final snapshot без self-promotional narrative;
- known defects и negative evidence.

После всех пяти delivery-runs и финального reset контроллер создаёт отдельную
свежую evaluator-сессию на `gpt-5.6-sol` с `xhigh`. Это шестая, но не delivery-
сессия; её расход относится только к benchmark overhead. Evaluator получает
rubric и анонимизированные packets `A..E`, но не получает `order.json`, mode-
mapping, process/token metrics или признаки внутренней topology. Он применяет
один frozen rubric ко всем пяти packets и возвращает hard-gate verdict, score
`0..100` и defect list для каждого валидного run. Для infrastructure-invalid
packet он возвращает `not_scorable` и причину, а не нулевой quality score.

Packets копируются в отдельный evaluator-only каталог без ссылки на основной
benchmark root. Prompt evaluator явно запрещает искать `order.json`, controller
artifacts, delivery threads и остальные benchmark worktrees; он читает только
пять выданных packets и exact candidates под opaque labels `A..E`.

Сначала сохраняются scores, hard-gate verdicts и defect lists с hash. Только
после этого раскрывается `A..E → mode`, добавляются process/token metrics и
формулируются выводы.

## Классификация сбоев

### Валидный результат режима

- завершённый и проверенный Release;
- настоящий blocker, возникший из frozen scope/authority;
- допустимый `Экономичным` режимом resumable checkpoint;
- mode-specific ошибка реализации, review или autonomous continuation;
- достижение общего frozen wall-time ceiling без infrastructure drift.

### Невалидный прогон инфраструктуры

- старт не от frozen baseline;
- не восстановленный Task Manager/UAT state;
- потеря связи с thread или worktree из-за controller failure;
- недоступность общего для всех обязательного tool/service;
- посторонняя account activity, делающая основные usage measurements
  неразделимыми;
- weekly reset или изменение common profile/runtime посреди прогона;
- общий prompt/acceptance defect, который одинаково лишил бы все режимы
  необходимого факта.

### Невалидный по mode/protocol прогон

- `mode_routing_invalid`: обязательная Luna topology не появилась, child
  унаследовал Sol, включился GPT-5.4 через platform `critic`/`reviewer`, observed
  profile разошёлся с receipt либо `Рой` не создал требуемую material Best-of-M
  wave;
- `protocol_invalid`: delivery прочитала чужой run либо выполнила запрещённый
  реальный effect вопреки выбранной unattended policy; дополнительные или
  повторные безопасные локальные тесты к protocol violation не относятся;
- режим вызвал `request_user_input`, ожидал action-time confirmation или
  заблокировался только из-за live ACL smoke, заранее исключённого из
  unattended acceptance.

Эти outcomes доказывают дефект runtime или экспериментального протокола, но не
получают quality/efficiency rank. Controller сохраняет ранний trace и не даёт
нарушившему gate run тратить оставшийся восьмичасовой budget.

Infrastructure-, routing- или protocol-invalid run не превращать в плохой score
качества кандидата. В этом pilot
ровно пять delivery-сессий, поэтому replacement run автоматически не создаётся:
после доказанного reset контроллер продолжает к следующему `A..E`, а невалидную
строку исключает из quality/efficiency ranking и оставляет в итоговом отчёте с
причиной. Если общий defect frozen input делает несопоставимыми уже прошедшие
режимы, pilot останавливается с resumable checkpoint; новую полную серию без
пользователя не начинает.

## Финальный отчёт

Итоговый документ создаётся только после пяти post-run captures, пяти доказанных
reset gates — включая reset после последнего режима — и слепой оценки. Он
содержит:

1. benchmark ID, дату, цель и точный Release;
2. per-mode top-level model/effort, общие permissions, runtime versions и
   baseline SHA;
3. frozen prompt/rubric hashes и фактический порядок;
4. доказательство начального baseline и каждого reset;
5. обязательную единую итоговую таблицу по пяти режимам в зафиксированном ниже
   формате;
6. раскрытое отображение `A..E → mode`;
7. подробное приложение с token categories, model rows, cache share и run
   position, необходимое для проверки сумм итоговой таблицы;
8. подробное приложение с weekly usage remaining до/после, наблюдаемой quota
   delta, `resets_at`, точностью замера, timing milestones, agents, attempts,
   interventions, rework и defects;
9. отдельно controller/setup/reset/evaluation overhead;
10. сравнение accepted-result efficiency и checkpoint utility;
11. infrastructure incidents, deviations и limitations;
12. ссылки/пути на raw artifacts и их hashes;
13. состояние оставленных benchmark branches и подтверждение, что `main`,
    Task Manager и UAT не были случайно оставлены в промежуточном состоянии;
14. вывод, какой режим оказался сильнее для каких ограничений, без объявления
    одного пилотного прогона универсальной истиной.

### Обязательная итоговая таблица

В начале итогового отчёта приводится ровно одна компактная сравнительная
таблица. Она отвечает на вопрос о результате и цене каждого режима, а не
заменяет raw artifacts и подробные evidence-приложения.

| Режим | Итог | Качество, баллы | Sol, токены | Luna, токены | GPT-5.4, токены | Время | Объём работы | API-equivalent, USD | Weekly use, п.п. |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| Соло |  |  |  |  |  |  |  |  |  |
| Классический |  |  |  |  |  |  |  |  |  |
| Баланс |  |  |  |  |  |  |  |  |  |
| Рой |  |  |  |  |  |  |  |  |  |
| Экономичный |  |  |  |  |  |  |  |  |  |

Правила заполнения:

- `Итог` использует короткий нормализованный verdict: `PASS`,
  `FAIL — <gate>`, `BLOCKED — <reason>`, `CHECKPOINT` или
  `INVALID — infrastructure|routing|protocol`. Отдельные UAT version, список
  gates и lifecycle-detail в эту таблицу не входят;
- `Качество, баллы` содержит только blind score `0..100`. Для неоцениваемого
  прогона указывается `n/a`; counters вида `High+`, `Major+` и defect severity
  в итоговой таблице запрещены;
- набор model-columns строится после telemetry reconciliation как объединение
  всех точных model IDs, фактически наблюдавшихся хотя бы в одном из пяти
  delivery trees. Одинаковый полный набор этих колонок показывается для всех
  режимов; Sol, Luna и GPT-5.4 в шаблоне выше — текущий ожидаемый набор, а не
  закрытый список;
- каждая model-column содержит полный расход delivery tree именно этой модели:
  `cached input + uncached input + output`. Расход разных моделей нельзя
  объединять, показывать только общим total или скрывать в `Other`;
  отсутствие расхода конкретной модели записывается как `0`, а не как прочерк;
- `Время` — wall-clock от dispatch до terminal outcome/checkpoint без
  setup/reset/evaluation overhead;
- `Объём работы` записывается в одном стабильном формате:
  `<agents> аг. · <tool calls> выз. · <commits> ком. · <tests> тест.`. Agents
  считаются рекурсивно по delivery tree; остальные величины берутся из того же
  run interval и не используются как замена quality score;
- `API-equivalent, USD` — сумма model-by-model по тем же delivery-tree token
  totals и действующим публичным list prices. Это оценка стоимости через API,
  а не фактический subscription charge;
- `Weekly use, п.п.` — `weekly_quota_consumed_percentage_points` для полного
  измерительного окна режима. Если разрешения счётчика недостаточно, пишется
  `<resolution`; при reset или несовместимых snapshots — `invalid`. Значение
  включает неизбежный controller observation overhead и поэтому не подменяет
  точные model token totals.

UAT version, run position, cache share, quota snapshots, defect list и
подробные hard-gate evidence остаются в проверяемом приложении к отчёту, но не
добавляются в эту итоговую таблицу.

## Условие завершения центральной сессии

Центральная сессия завершает работу только когда:

- каждый из пяти режимов имеет валидный outcome либо явно исключённый
  infrastructure-invalid run;
- между последовательными прогонами доказан ограниченный reset: frozen Git/UAT
  code и schema, пустые три Team-таблицы, видимое состояние Tasks и smoke;
- все raw measurements сохранены и reconciled;
- blind scores зафиксированы до раскрытия режимов;
- финальный отчёт отделяет факты, выводы и ограничения;
- текущее состояние Task Manager, `main`, UAT schema, трёх Team-таблиц и
  оставленных веток точно описано пользователю; row-level состояние остальных
  UAT D1 tables не входит в reset contract.

Если эти условия недостижимы, контроллер не сглаживает пробелы и не объявляет
benchmark завершённым: он выдаёт resumable controller checkpoint с точной
причиной, сохранёнными артефактами и следующим безопасным действием.

## Результат

Центральная сессия выполнила все пять прогонов, финальный reset и отдельную
слепую оценку. Замороженные артефакты находятся вне репозитория; основные
результаты, ограничения и cleanup evidence собраны в
[итоговом отчёте](../reports/2026-09-01-issue-grinder-five-mode-benchmark.md).
