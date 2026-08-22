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
  требования. ShipTask adaptive multi-agent default и буквальный no-subagent
  opt-out, а также Luna Max routing и current-profile escalation являются такими
  явными topology/profile-требованиями.
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
- Strategic Explainer не получает право решать факты, статус, границы работы,
  полномочия или действие. При `subagents=auto` каждый комментарий ShipTask
  обязательно проходит отдельного независимого Explainer. Явный общий
  `subagents=off` — единственное исключение: основной агент применяет quality
  contract напрямую и не заявляет о независимой проверке.
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
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py task-composer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Repository validator проверяет current contract, trigger matrix, lifecycle
evaluation, retired loopholes, documentation navigation и distribution
boundaries. Проверка не должна требовать конкретных необязательных слов или
числа tool calls вместо observable behavior. Evals проверяют adaptive
`auto`/`off` contract и отдельного независимого Strategic Explainer при
разрешённых субагентах, но не фиксируют fork mode, prompt envelope, retry count
или число alternatives. Auto-title является отдельным явным требованием:
проверяются доказанная first-turn eligibility, сохранение meaningful title и
адресация только calling task.

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
- первый ShipTask-вызов с catalog placeholder после live scope resolution один
  раз получает `ShipTask · ...`; meaningful title, later turn, incomplete
  history и ambiguous current candidate не переименовываются;
- несколько independent conflict-free Tasks в `subagents=auto` одновременно
  получают несколько bounded workers и одного integration owner;
- genuinely simple bounded packet без отдельного profile override получает Luna
  Max, а ordinary/complex packet наследует current model/effort;
- ambiguity, unexpected environment/tool state или proof gap останавливают Luna
  packet и передают его current profile без повторного Luna loop;
- явный user profile для subagents имеет приоритет, а выбор primary profile сам
  по себе не отключает cheap-lane default;
- shared evolving write surface ограничивает writers до одной safe lane, но не
  запрещает полезные независимые read-only scouts/reviewers;
- общее «не используй субагентов» даёт ноль subagents, включая Explainer, а
  узкое «без субагентов для реализации» сохраняет independent comment pass;
- `To Do → In Progress` проходит без comment и без Strategic Explainer;
- готовый candidate получает независимо подготовленный Strategic Explainer
  comment и read-back до `In Review`;
- proven defect немедленно виден в chat, получает opening comment до repair и
  `In Progress`, после чего rework продолжается в том же run;
- найденный и исправленный в одном run defect сохраняется в Task resolution
  comment и final incident ledger;
- unresolved incident получает chat update при material state change и
  heartbeat активного run без дублирования Task comments;
- verification blocker означает отсутствие достаточного способа доказать
  success/failure в current scope; comment рекомендует strongest feasible путь,
  сравнивая alternatives только при реальном выборе, и сохраняет `In Review`;
- proven success получает completion comment/read-back до `Done`;
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
- final report сообщает outcome, proof gaps, primary cause и resume condition,
  но не заменяет Task comment.

Полная матрица:
[lifecycle evaluation](../reference/shiptask-review-disposition-evaluation.md).

Для Task Composer отдельно проверьте single-vs-Epic decomposition, read-only
draft, explicit write authority, exact `Backlog`, optional unknown Release,
existing-only Labels, semantic relation direction, duplicate prevention и
partial-write reconciliation. Type Labels не должны дублироваться в title:
`BUG:`/`EPIC:` и эквиваленты отсутствуют, а legacy-prefixed title участвует в
duplicate search как clean outcome title. Полная матрица:
[Task Composer evaluation](../reference/task-composer-evaluation.md).

## Runtime-дистрибуция

Repository directories `ship-tasks/`, `task-composer/` и
`strategic-explainer/` — source of truth.
Единственная runtime-distribution — sibling skills в plugin
`ship-tasks@srez-marketplace`. Task Manager connector устанавливается отдельно
как adapter-only `task-manager@srez-marketplace`.

При изменении runtime payload:

1. Выполните validations, закоммитьте exact scope и отправьте в `origin/main`;
   проверьте `HEAD == origin/main`.
2. Синхронизируйте все три marketplace skill directory и проверьте `diff -qr`.
3. Получите marketplace name через `read_marketplace_name.py` и обновите только
   cachebuster через `update_plugin_cachebuster.py`; не меняйте
   numeric version ради reinstall.
4. Выполните marketplace/plugin tests, commit/push marketplace и переустановите
   `ship-tasks@srez-marketplace` штатным plugin lifecycle.
5. Проверьте quick validation marketplace copies, byte identity installed cache
   и состояние installed/enabled.
6. В fresh App Server catalog подтвердите `ship-tasks:ship-tasks`,
   `ship-tasks:task-composer` и `ship-tasks:strategic-explainer`, отсутствие
   standalone user copies и отсутствие этих skills в adapter-only Task Manager
   plugin.

Не создавайте `~/.codex/skills/ship-tasks`,
`~/.codex/skills/task-composer` или
`~/.codex/skills/strategic-explainer`. Marketplace snapshot и
installed cache не удаляются вручную.
