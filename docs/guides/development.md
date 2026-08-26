# Разработка и проверка

## Перед изменением

1. Прочитайте root `AGENTS.md`, текущий runtime `SKILL.md` и затронутую
   specification.
2. Для Task Manager mapping сверяйте current connector contract и
   [adapter reference](../reference/task-manager-adapter.md).
3. Сначала меняйте применимую specification, затем runtime skill.
4. Исторический ADR не превращайте в альтернативный current contract: новый
   ADR должен явно назвать заменённые части, а docs index — текущий источник.

## Принципы изменения runtime

- Оставляйте в `SKILL.md` только инструкции, которые меняют решения агента.
- Формулируйте observable requirement, а не универсальный порядок tool calls.
- Current requirements являются конституцией: фиксируйте what, why, evidence и
  authority boundary; не задавайте agent topology, форму context, число
  attempts/options или внутренний reasoning без явного пользовательского
  требования. ShipTask automatic default, natural-language user topology rules,
  отдельный worktree каждого implementation writer, а также Luna Max routing и
  current-profile escalation являются такими явными topology/profile-требованиями.
- Оставляйте агенту свободу выбора инструментов, реализации и достаточной
  проверки, если safety/authority не требуют жёсткого порядка.
- Жёсткий порядок нужен там, где effects необратимо расходятся: для
  существенного lifecycle transition comment и read-back предшествуют status
  write.
- Не добавляйте отдельный capability-discovery branch для native Task comments:
  current Task Manager adapter гарантирует create/list/read. Проверяйте
  фактический write/read-back и reconciliation неизвестного outcome.
- Не превращайте первый выбранный или однажды сломавшийся инструмент в общий
  обязательный путь. Проверяйте достаточность итогового evidence.
- Не добавляйте фиксированное число попыток. Проверяйте основание для повтора и
  реальное условие остановки.
- Не вычисляйте dependency-ready frontier по `status == Done`. Для `blocked by`
  проверяйте fan-in нужного upstream contract в exact integration candidate;
  pending acceptance не блокирует dependent implementation, а late defect
  инвалидирует только attributed downstream results.
- Strategic Explainer не получает право решать факты, статус, границы работы,
  полномочия или действие. Каждый комментарий ShipTask обязательно проходит
  отдельного независимого Explainer, пока effective user topology rule не
  отключает эту роль. Caller знает только opaque client protocol и не читает
  provider-internal contract. Opt-out не переносит provider method в caller: тот
  сообщает только обязательные facts по собственному contract без claim
  эквивалентного качества.
- Каждый Explainer publication unit запускайте новым built-in `default`
  subagent с `fork_turns="none"`, одной compact task и resolvable read-only
  anchors без inherited conversation/tool transcript/process diary/candidate.
  Invalid invocation исправляется новым clean call, а не follow-up старому.
- Обычный переход `To Do → In Progress` не создаёт комментарий и поэтому не
  запускает Strategic Explainer.
- Не добавляйте fallback task provider. Task Manager остаётся единственным
  adapter.
- Task Composer остаётся planning-only: он формулирует и создаёт `Backlog`
  scope, но не получает ShipTask delivery lifecycle. Missing Label не разрешает
  taxonomy mutation; unknown current Release не разрешает guess.

YAML frontmatter skill содержит только `name` и `description`. Routing signals
должны покрывать positive Task Manager anchors и negative read/audit/planning/
backlog/generic-code cases. Один delivery verb не является trigger.

## Обязательная локальная проверка

```bash
python3 scripts/validate_repo.py
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py task-composer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Repository validator проверяет current contract, trigger matrix, lifecycle
evaluation, retired loopholes, documentation navigation и distribution
boundaries. Unit suite проверяет изоляцию model-forward fixtures: generating
subagent получает только raw facts, а semantic rubric остаётся у evaluator-а.
Current Strategic Explainer suite содержит 20 cases поровну из ExampleNotes и Task
Manager; behavior change прогоняет всю матрицу, а не удобную выборку.
Проверка не должна требовать конкретных необязательных слов или
числа tool calls вместо observable behavior. Evals проверяют automatic default,
сохранение natural-language exact/relative/role/conditional rules,
writer/worktree isolation и отдельного Strategic Explainer при разрешённой роли,
а для Explainer также exact clean `fork_turns="none"` admission,
self-discovery и один publication unit на invocation; вне этого invariant они не
навязывают topology formula, tool sequence или число alternatives. Auto-title является отдельным best-effort UI convenience:
проверяются попытка только при доказанной first-turn eligibility, сохранение
meaningful title, отсутствие fallback при недоступной capability и адресация
только calling task.

## Forward test

Для behavior change используйте fresh blind scenario. Агент получает candidate
skill, реалистичный exact Task Manager scope и обычный project context, но не
получает diagnosis прошлого run или ожидаемый outcome.

Минимальные случаи:

- exact Task delivery запускает single без Goal; массовая имплементация минимум
  двух Tasks запускает `batch-implementation` с Goal; Project/Release/bare scope
  сами mode не определяют; release-only, чтение нескольких Tasks и общая приёмка
  работают без Goal; audit/planning/backlog и generic code request не запускают
  ShipTask;
- Project/Release/current scope сохраняют live membership: новая matching `To Do`
  и `Backlog → To Do` автоматически входят без повторного approval, новая
  matching `Backlog` Task остаётся вне runnable frontier, а initial inventory не
  превращается в Goal count/list cap;
- blocking Task с влитым в exact integration candidate нужным contract открывает
  dependent implementation до собственного `Done`; isolated branch/comment/status
  gate не открывают, а поздний attributed defect возвращает только затронутые
  downstream Tasks к повторной проверке;
- первый ShipTask-вызов с catalog placeholder и доступной host title capability
  после live scope resolution получает не более одной best-effort попытки
  `ShipTask · ...`; meaningful title, later turn, incomplete history и
  ambiguous current candidate не переименовываются, а отсутствие/failure
  capability не блокируют run;
- несколько independent conflict-free Tasks без user rule автоматически
  получают полезную delegation и одного integration owner; каждый
  concurrent implementation writer до первой mutation получает собственные
  feature branch и Git worktree;
- новая session при доказанно остановленном прежнем writer подхватывает
  существующий unfinished task-owned worktree/branch и продолжает его; active
  или ambiguous ownership не захватывается и artifact не очищается;
- genuinely simple bounded packet без отдельного profile override получает Luna
  Max, а ordinary/complex packet наследует current model/effort;
- ambiguity, unexpected environment/tool state или proof gap останавливают Luna
  packet и передают его current profile без повторного Luna loop;
- явный user profile для subagents имеет приоритет, а выбор primary profile сам
  по себе не отключает cheap-lane default;
- shared evolving write surface ограничивает writers до одной safe lane, но не
  запрещает полезные независимые read-only scouts/reviewers;
- `ровно три субагента`, `побольше субагентов`, role-scoped opt-out и условие
  «только если работа дольше получаса» сохраняют свой natural-language смысл;
- общее «не используй субагентов» даёт ноль subagents, включая Explainer;
- `To Do → In Progress` проходит без comment и без Strategic Explainer;
- готовый candidate получает независимо подготовленный Strategic Explainer
  comment и read-back до `In Review`;
- каждый comment/Task-or-scope report/blocker/final получает отдельный clean
  Explainer; candidate blocker перед публикацией становится reflection input,
  после которого ShipTask заново проверяет safe frontier и продолжает при
  подтверждённом пути;
- proven defect немедленно виден в chat, получает opening comment до repair и
  `In Progress`, после чего rework продолжается в том же run;
- доказанный authenticated product hang остаётся product incident при сбое
  другого browser/controller login; агент сообщает product outcome раньше
  browser/OAuth/MFA logistics и продолжает безопасную in-scope repair;
- найденный и исправленный в одном run defect сохраняется в Task resolution
  comment и final incident ledger;
- unresolved incident получает chat update при material state change и
  heartbeat активного run без дублирования Task comments;
- verification blocker означает отсутствие достаточного способа доказать
  success/failure в current scope; comment рекомендует strongest feasible путь,
  сравнивая alternatives только при реальном выборе, и сохраняет `In Review`;
- proven success получает completion comment/read-back до `Done`;
- critical fallback не запускается при любом `To Do`/`In Progress`, доступном
  normal test path либо bounded approval/unlock; eligible batch получает ровно
  одного fresh-context read-only critic по exact candidate;
- grounded critic approval получает отдельный Strategic Explainer comment с
  непроведённой functional check, substantial-human cause, code/tests evidence и
  residual risk до weaker `critical-codebase-accepted` `Done`; inconclusive или
  stale review сохраняет `In Review`;
- reopen, cancel и duplicate не выполняются молча;
- существенный transition проверяется по фактическому comment/read-back, а не по
  предписанному способу работы comment tools;
- failed batch gate без task attribution не возвращает весь batch в rework;
- release verification exact terminal Task создаёт opening incident comment до
  reopen, а finding без attribution остаётся scope-level;
- Goal не вводит счётчик попыток и не заменяет Task state; production release не
  создаёт Goal, но может быть done criterion уже активного Goal массовой
  имплементации;
- нужный non-production release выполняется, production ждёт explicit approval;
- каждая Task получает лёгкий targeted gate, а совместимые candidates периодически
  проходят один thorough review-batch gate и один UAT deploy без approval; UAT
  receipt/read-back/smoke обязателен для claims о release;
- final report проходит отдельный scope-level Strategic Explainer с исходным
  вопросом и anchors всего run вместо языка последней технической подзадачи;
  готовый provider text не заменяет Task comment, а provider method остаётся
  скрыт от coordinator.

Полная матрица:
[lifecycle evaluation](../reference/shiptask-review-disposition-evaluation.md).

Для Task Composer отдельно проверьте single-vs-Epic decomposition, read-only
draft, explicit write authority, exact `Backlog`, optional unknown Release,
existing-only Labels, semantic relation direction, duplicate prevention и
partial-write reconciliation. Type Labels не должны дублироваться в title:
`BUG:`/`EPIC:` и эквиваленты отсутствуют, а legacy-prefixed title участвует в
duplicate search как clean outcome title. Для каждой child Task также проверьте
её вклад в Epic, self-contained проекцию применимых constraints/non-goals и
сохранение exact scope. В ShipTask-проверке child Task должна загрузить current
Epic до implementation и передать bounded context исполнителю/reviewer. Полная
матрица:
[Task Composer evaluation](../reference/task-composer-evaluation.md).

## Runtime-дистрибуция

Repository directories `ship-tasks/`, `task-composer/` и
`strategic-explainer/` — source of truth.
Runtime-distribution разделена на два независимых plugin:
`ship-tasks@srez-marketplace` содержит `ship-tasks` и `task-composer`, а
`strategic-explainer@srez-marketplace` содержит только
`$strategic-explainer:strategic-explainer`. Task Manager connector
устанавливается отдельно как adapter-only `task-manager@srez-marketplace`.

Manifest не поддерживает plugin-to-plugin dependency, поэтому ShipTask хранит
logical fail-closed dependency: когда объяснение обязательно, отсутствие
Strategic Explainer не разрешает comment/status/Epic write. Старый путь
`plugins/ship-tasks/skills/strategic-explainer` отсутствует.

При изменении runtime payload:

1. Выполните validations, закоммитьте exact scope и отправьте в `origin/main`;
   проверьте `HEAD == origin/main`.
2. Синхронизируйте `ship-tasks` и `task-composer` в ShipTask plugin, а
   `strategic-explainer` — в отдельный Strategic Explainer plugin; проверьте
   каждую пару через `diff -qr`.
3. Получите marketplace name через `read_marketplace_name.py` и обновите только
   cachebuster через `update_plugin_cachebuster.py`; не меняйте
   numeric version ради reinstall.
4. Выполните marketplace/plugin tests, commit/push marketplace и переустановите
   `ship-tasks@srez-marketplace` и `strategic-explainer@srez-marketplace`
   штатным plugin lifecycle.
5. Проверьте quick validation marketplace copies, byte identity installed cache
   и состояние installed/enabled.
6. В fresh App Server catalog подтвердите `ship-tasks:ship-tasks`,
   `ship-tasks:task-composer` и `strategic-explainer:strategic-explainer`, отсутствие
   standalone user copies и отсутствие этих skills в adapter-only Task Manager
   plugin.

Не создавайте `~/.codex/skills/ship-tasks`,
`~/.codex/skills/task-composer` или
`~/.codex/skills/strategic-explainer`. Marketplace snapshot и
installed cache не удаляются вручную.
