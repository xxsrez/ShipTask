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
  требования. Автовыбор четырёх текущих режимов Issue Grinder, пользовательские
  правила делегации, изоляция writers и Luna Max routing берутся из локальных
  Requirements и Architecture этой entity, не из исторических стратегий.
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
- Ни один Strategic Explainer не получает право решать факты, статус, границы
  работы, полномочия или действие. Действующий provider protocol принадлежит
  Strategic Explainer; вызывающие навыки передают только semantic request и
  resolvable anchors.
- Обычный переход `To Do → In Progress` не создаёт комментарий и поэтому не
  запускает Strategic Explainer.
- Не добавляйте fallback task provider. Task Manager остаётся единственным
  adapter.
- Task Composer остаётся planning-only: он формулирует и создаёт `Backlog`
  scope, но не получает delivery lifecycle. Missing Label не разрешает
  taxonomy mutation; unknown current Release не разрешает guess.
- Scope Reviewer остаётся review-only за исключением явного plan-improvement
  intent. Даже в этом режиме он меняет только Agent Plan, сохраняет Human
  Requirements byte-identical и не получает delivery lifecycle.

YAML frontmatter skill содержит только `name` и `description`. Routing signals
должны покрывать positive Task Manager anchors и negative read/audit/planning/
backlog/generic-code cases. Один delivery verb не является trigger.

## Обязательная локальная проверка

```bash
python3 scripts/validate_repo.py
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py issue-grinder
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py task-composer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py scope-reviewer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Repository validator проверяет current contract, trigger matrix, lifecycle
evaluation, retired loopholes, documentation navigation и distribution
boundaries. Unit suite проверяет изоляцию model-forward fixtures: ordinary
generating subagent получает только raw facts, а semantic rubric остаётся у
evaluator-а.
Current Strategic Explainer suite содержит 28 cases: четырнадцать из ExampleNotes,
одиннадцать из Task Manager и три общих; behavior change прогоняет всю матрицу,
а не удобную выборку.
Проверка не должна требовать конкретных необязательных слов или
числа tool calls вместо observable behavior. Evals проверяют automatic default,
сохранение natural-language exact/relative/role/conditional rules,
writer/worktree isolation через двухфазный admission receipt и canary
неизменяемого integration checkout, а также один Strategic Explainer при
разрешённой роли, а
  для ordinary Explainer также exact clean `fork_turns="none"` admission на
  `gpt-5.6-luna`/`max`,
self-discovery и один publication unit на invocation; вне этих invariants evals не
навязывают topology formula, tool sequence или число alternatives. Auto-title является отдельным best-effort UI convenience:
проверяются попытка только при доказанной first-turn eligibility, сохранение
meaningful title, отсутствие fallback при недоступной capability и адресация
только calling task.

## Forward test

Для изменения поведения используйте fresh blind scenario: действующий skill,
реалистичный Task Manager scope и обычный project context, без диагноза прошлого
прогона и подсказки ожидаемого результата. Проверьте маршрутизацию, границу
полномочий, доказательство результата, read-back существенных записей и
сохранение работы после прерывания. Для Issue Grinder сценарии и четыре режима
описаны в [Evaluation](../skills/issue-grinder/evaluation.md) и
[мануале](issue-grinder-modes.md). Историческая
[матрица ShipTask](../reference/shiptask-review-disposition-evaluation.md)
не является проверкой действующего runtime.

Для Task Composer отдельно проверьте single-vs-Epic decomposition, read-only
draft, explicit write authority, exact `Backlog`, optional unknown Release,
existing-only Labels, semantic relation direction, duplicate prevention и
partial-write reconciliation. Type Labels не должны дублироваться в title:
`BUG:`/`EPIC:` и эквиваленты отсутствуют, а legacy-prefixed title участвует в
duplicate search как clean outcome title. Для каждой child Task также проверьте
её вклад в Epic, self-contained проекцию применимых constraints/non-goals и
сохранение exact scope. Полная матрица:
[Task Composer evaluation](../skills/task-composer/evaluation.md).

Для Scope Reviewer проверьте exact selector и полный versioned snapshot,
обязательную Requirements optic для плана, отдельный fresh Luna Max route каждой
оптики, ноль writes в read/status/Release review, byte-identical Human
Requirements при repair и один понятный report без dump-а findings. Полная
матрица: [Scope Reviewer evaluation](../skills/scope-reviewer/evaluation.md).

## Runtime-дистрибуция

Repository directories `issue-grinder/`, `task-composer/`,
`scope-reviewer/` и `strategic-explainer/` — source of truth.
Runtime-distribution разделена на два независимых plugin:
`issue-grinder@srez-marketplace` содержит `issue-grinder`, `task-composer` и
`scope-reviewer`, а
`strategic-explainer@srez-marketplace` содержит только
`$strategic-explainer:strategic-explainer`. Task Manager connector
устанавливается отдельно как adapter-only `task-manager@srez-marketplace`.
Legacy `ship-tasks@srez-marketplace` удалён из каталога и runtime.

Manifest не поддерживает plugin-to-plugin dependency, поэтому Issue Grinder хранит
availability-based optional routing: ordinary при наличии и разрешении, иначе
native. Отсутствие provider-а не мешает обязательному comment/status write.

При изменении runtime payload:

1. Выполните validations, закоммитьте exact scope и отправьте в `origin/main`;
   проверьте `HEAD == origin/main`.
2. Синхронизируйте `issue-grinder`, `task-composer` и `scope-reviewer` в Issue Grinder plugin, а
   `strategic-explainer` — в его отдельный plugin;
   проверьте каждую пару через `diff -qr`.
3. Получите marketplace name через `read_marketplace_name.py` и обновите только
   cachebuster через `update_plugin_cachebuster.py`; не меняйте
   numeric version ради reinstall.
4. Выполните marketplace/plugin tests, commit/push marketplace и переустановите
   `issue-grinder@srez-marketplace` и `strategic-explainer@srez-marketplace`
   штатным plugin lifecycle.
5. Проверьте quick validation marketplace copies, byte identity installed cache
   и состояние installed/enabled.
6. В fresh App Server catalog подтвердите `issue-grinder:issue-grinder`,
   `issue-grinder:task-composer`, `issue-grinder:scope-reviewer` и
   `strategic-explainer:strategic-explainer`, отсутствие
   установленного `ship-tasks:ship-tasks`,
   standalone user copies и отсутствие этих skills в adapter-only Task Manager
   plugin.

Не создавайте `~/.codex/skills/issue-grinder`,
`~/.codex/skills/ship-tasks`,
`~/.codex/skills/task-composer`,
`~/.codex/skills/scope-reviewer` или
`~/.codex/skills/strategic-explainer`. Marketplace snapshot и
installed cache не удаляются вручную.
