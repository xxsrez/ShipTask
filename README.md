# ShipTask

ShipTask — репозиторий Codex skill `$ship-tasks`, который через Task Manager
доводит выбранные Tasks, Project или Release до проверенного terminal outcome
при явном invocation и по natural-language delivery intent с однозначным Task
Manager anchor. Один delivery verb или обычная просьба исправить код/продукт/
plugin без такого anchor ShipTask не активирует. Составная команда явно создать
ровно одну Task в Task Manager и сразу выполнить её запускает `single`, а не
backlog capture. Exact одна Task работает в `single` mode без Goal. Goal нужен
только для `batch-implementation`, когда один run реально имплементирует или
возвращает в rework минимум две concrete Tasks. Project/Release/current scope и
bare `$ship-tasks` — только selectors: mode определяется по live inventory.
Release уже подготовленного candidate, включая production, работает без Goal.
Exact Task/явный список refs образуют закрытый selector. Project, Release и
current scope остаются live selectors: стартовый inventory не замораживает
membership, поэтому новая matching non-Backlog Task автоматически входит в run
без повторного approval, а Backlog остаётся вне delivery.
`blocked by` управляет доступностью реализации, а не terminal lifecycle:
dependent Task становится runnable после подтверждённого fan-in нужного upstream
contract в exact integration candidate, даже если blocking Task ещё не `Done`
из-за собственной проверки. Relation и attribution сохраняются; поздний defect
инвалидирует только доказанно затронутые downstream results.

Документация здесь является исходным кодом, причём source unit — отдельный
skill. В [`docs/skills/<skill>/`](docs/skills/README.md) у каждого skill есть
собственные `requirements.md` (Level 1) и `architecture.md` (Level 2); требования
трёх skills не объединяются. Runtime является компактной стохастической
компиляцией этих двух локальных документов. У Strategic Explainer видимый
`SKILL.md` содержит только router/admission layer, а provider expertise находится
в reference для admitted fresh subagent. Удаление и повторная сборка runtime из
source package должны давать примерно эквивалентный по смыслу package.

Current requirements являются конституцией для агентов: они задают outcome,
rationale, observable evidence и authority/safety boundaries, но оставляют
агенту план, декомпозицию, инструменты и внутренний reasoning. Явное исключение —
fresh stateless invocation Strategic Explainer API. Каждый user-facing publication
unit получает fresh built-in `default` subagent с `fork_turns="none"`, одной compact task и без
inherited process context. Другое исключение — execution topology: без явного
user rule ShipTask сам решает, где
субагенты дают реальную пользу, сохраняя одного integration owner. Пользователь
может свободным языком задать exact/relative count, role scope, общий или узкий
запрет и условие вроде «используй субагентов только для работы дольше получаса»;
coordinator обязан сохранить смысл правила, а не вернуть topology к default.
Root agent не входит в явно названное число субагентов. Каждый
одновременно пишущий implementation subagent получает отдельные feature branch
и Git worktree; read-only роли могут работать без worktree. Без отдельного user
override только genuinely simple bounded packets используют Luna Max; остальные
наследуют current model/effort, а ambiguity или unexpected environment переводят
Luna packet integration owner на current profile без повторного Luna loop.

После ошибки или смены Codex-сессии ShipTask сначала ищет существующий
task-owned checkpoint. Если прежний writer остановлен, незавершённый worktree и
feature branch безопасно переходят новому exclusive owner, и работа продолжается
там, а не начинается с нуля; active или ambiguous ownership не перехватывается.
Ожидаемое пользовательское tiering: простое — Luna Max, большинство — выбранный
current profile (обычно Sol Extra High), ультрасложное — выбранный пользователем
Sol Ultra; ShipTask не повышает модель скрыто. Перед любым
существенным status transition сначала
публикуется и перечитывается понятный native Task comment; обычный старт
`To Do → In Progress` комментария не создаёт. Task description и ответ в Codex
комментарий не заменяют. Native comments являются гарантированной частью Task
Manager adapter и всегда используются для material lifecycle reporting.
Если host показывает title capability и ShipTask доказанно является первым
вызовом новой Codex task с catalog placeholder, после live scope resolution
выполняется не более одной best-effort попытки задать имя `ShipTask · ...`;
существующее meaningful название не перезаписывается, а отсутствие или failure
capability не блокируют delivery.

Каждый комментарий, который создаёт ShipTask, до публикации проходит отдельного
независимого `$strategic-explainer:strategic-explainer`, пока effective user topology rule
не отключило эту роль. Каждый Task/scope report, blocker explanation и final
также является отдельным publication unit. Caller знает только opaque protocol:
новый clean subagent, одна короткая задача, exact scope и resolvable read-only
anchors без analysis, method rules или candidate caller-а. Ready text не
переписывается; opt-out/unavailability не переносят provider method в основной
агент. Routine chat и progress updates Explainer не запускают.

Приёмочный incident сообщается сразу в chat и сохраняется в Task history до
начала repair. Opening comment остаётся видимым после исправления, resolution
comment содержит повторную проверку, а final run report перечисляет material
incidents, включая найденные и исправленные в том же run. Пока incident
unresolved, активный run регулярно напоминает о нём без дублирования Task
comments. Только прямое нарушение acceptance называется bug; невозможность
получить evidence называется verification blocker.

Агент сам выбирает инструменты, способ диагностики и
приёмки; сбой одного средства не навязывает его repair. Acceptance не ослабляется
ради удобства, а непроверенное не называется verified. Единственный явный
fallback — `critical-codebase-accepted`: после fresh inventory без `To Do` и
`In Progress`, когда все оставшиеся `In Review` требуют существенного human
verifier, один fresh-context critic независимо проверяет exact candidate,
code/tests. Grounded approval разрешает weaker `Done` только с обязательным
Strategic Explainer comment о непроведённой functional check и residual risk.
Browser switch допустим как диагностика, но не как repair или причина
отложить уже доказанный product failure, пока безопасная in-scope работа над
продуктом может продолжаться.
До окончательного blocker claim ShipTask перечитывает fresh Explainer result как
independent reflection input и заново проверяет safe frontier. Найденный путь не
принимается на веру: он подтверждается current sources/acceptance; при достаточном
пути stale blocker не публикуется и работа продолжается.
Перед завершением skill сверяет обещанный и фактический результат,
самостоятельно устраняет доступные проблемы внутри выбранной работы и только
затем передаёт final publication unit отдельному Strategic Explainer.
Пока effective topology rule не отключает comment Explainer, каждый комментарий
ShipTask проходит отдельного `$strategic-explainer:strategic-explainer`. Основной агент
знает только client protocol, проверяет material facts и не переписывает ready
text. Если правило отключает Explainer, caller сообщает обязательные lifecycle
facts по собственному contract без provider method. Explainer не выбирает
статус, полномочия или действие и ничего не меняет; общий router можно
использовать отдельно от ShipTask.
Старые memory, rollout или report записи о ручной приёмке не меняют этот
contract: обычный terminal-ready result закрывается автоматически, а существенная
human verification dependency проходит только строгий critical fallback либо
остаётся честно незавершённой.
Task-local вопросы откладывают только конкретную Task, не прерывая остальные;
для каждой Task делается лёгкий targeted gate, а совместимые изменения
периодически выпускаются в UAT одним exact batch без отдельного approval;
non-production releases выполняются автоматически, а production требует явного
разрешения пользователя. Goal массовой имплементации остаётся активным, пока в
его границе есть незавершённая работа; сам release не создаёт Goal. Project
memory хранит только selectors/profile и изменяется лишь по явной просьбе.

Task Composer закрывает соседний planning-only этап: формулирует одну Task либо
Epic с problem-first описанием через Strategic Explainer, конкретными
подзадачами, live Labels и semantic relations, сохраняя применимый strategic
context в каждой child Task. При delivery ShipTask перечитывает current Epic,
но его смысл не расширяет exact child scope. Созданные элементы остаются в
`Backlog`; неизвестный current Release не угадывается и не блокирует создание.

## Структура

- [`ship-tasks/SKILL.md`](ship-tasks/SKILL.md) — исполнимый skill.
- [`task-composer/SKILL.md`](task-composer/SKILL.md) — planning-only
  формулировка, декомпозиция и создание Task Manager scope.
- [`strategic-explainer/SKILL.md`](strategic-explainer/SKILL.md) — общий
  router/admission layer к stateless provider-subagent; внутренний provider
  contract загружается только после clean admission.
- [`docs/skills/README.md`](docs/skills/README.md) — source model и независимые
  Requirements/Architecture packages для каждого skill.
- [`docs/skills/ship-tasks/requirements.md`](docs/skills/ship-tasks/requirements.md)
  и [Architecture](docs/skills/ship-tasks/architecture.md) — source `$ship-tasks`.
- [`docs/skills/task-composer/requirements.md`](docs/skills/task-composer/requirements.md)
  и [Architecture](docs/skills/task-composer/architecture.md) — source Task Composer.
- [`docs/skills/strategic-explainer/requirements.md`](docs/skills/strategic-explainer/requirements.md)
  и [Architecture](docs/skills/strategic-explainer/architecture.md) — source
  Strategic Explainer.
- [`ship-tasks/references/project-memory.md`](ship-tasks/references/project-memory.md)
  — runtime contract project scope/profile memory.
- [Документация](docs/README.md) — канонические specifications, Task Manager
  adapter reference, architecture decisions и engineering reports.
- [`scripts/validate_repo.py`](scripts/validate_repo.py) — переносимая
  проверка структуры и project-specific residue.

## Проверка

```bash
python3 scripts/validate_repo.py
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py task-composer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Runtime публикуется двумя независимыми plugin: `ship-tasks@srez-marketplace`
содержит ShipTask и Task Composer, а
`strategic-explainer@srez-marketplace` — только общий Strategic Explainer.
Task Manager connector устанавливается отдельно как adapter-only
`task-manager@srez-marketplace`. Codex manifest не умеет автоматически
устанавливать plugin dependency, поэтому ShipTask и Task Composer fail-closed
используют отдельно установленный
`$strategic-explainer:strategic-explainer`. Standalone каталоги
`~/.codex/skills/ship-tasks`, `~/.codex/skills/task-composer` и
`~/.codex/skills/strategic-explainer` не устанавливаются: они создают вторые
logical skills рядом с plugin-qualified runtime. Каждый repository source
сверяется со своим Marketplace package и installed plugin cache.
