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
трёх skills не объединяются. `SKILL.md` является компактной стохастической
компиляцией этих двух локальных документов. Удаление и повторная сборка runtime
из source package должны давать примерно эквивалентный по смыслу skill.

Current requirements являются конституцией для агентов: они задают outcome,
rationale, observable evidence и authority/safety boundaries, но оставляют
агенту план, декомпозицию, инструменты, число попыток и форму context. Явное
исключение — execution topology: без явного user rule ShipTask сам решает, где
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
независимого `$ship-tasks:strategic-explainer`, пока effective user topology rule
не отключило эту роль. При таком запрете тот же quality contract основной агент
выполняет сам и не заявляет независимую проверку там, где её не было.

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
Перед завершением skill сверяет обещанный и фактический результат,
самостоятельно устраняет доступные проблемы внутри выбранной работы и только
затем даёт компактное причинное объяснение понятным человеку языком.
Пока effective topology rule не отключает comment Explainer, каждый комментарий
ShipTask проходит отдельного `$ship-tasks:strategic-explainer`. Субагент
переводит установленные факты и технические изменения в готовый пользовательский
текст; основной агент проверяет точность, но не переписывает текст обратно в
журнал реализации. Если правило отключает Explainer, основной агент применяет
тот же quality contract напрямую без claim независимости. Explainer не выбирает
статус, полномочия или действие и ничего не меняет; общий skill можно
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
  problem-first strategic discovery и communication skill для прямого или
  delegated использования, включая редакторскую реконструкцию сложного текста
  без потери смысла; обязательную ShipTask topology задаёт calling skill.
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
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py task-composer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Единственная runtime-дистрибуция трёх sibling-skills — отдельный plugin
`ship-tasks@srez-marketplace`. Task Manager connector устанавливается отдельно
как adapter-only `task-manager@srez-marketplace`; ShipTask в его package не
входит. Standalone каталоги `~/.codex/skills/ship-tasks`,
`~/.codex/skills/task-composer` и
`~/.codex/skills/strategic-explainer` не устанавливаются: они создают вторые
logical skills рядом с plugin-qualified `ship-tasks:ship-tasks` и
`ship-tasks:task-composer`/`ship-tasks:strategic-explainer`. Repository sources
публикуются через один marketplace package и сверяются с installed plugin
cache.
