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

Current requirements являются конституцией для агентов: они задают outcome,
rationale, observable evidence и authority/safety boundaries, но оставляют
агенту план, декомпозицию, инструменты, число попыток, делегирование и форму
context. Перед любым существенным status transition сначала
публикуется и перечитывается понятный native Task comment; обычный старт
`To Do → In Progress` комментария не создаёт. Task description и ответ в Codex
комментарий не заменяют. Native comments являются гарантированной частью Task
Manager adapter и всегда используются для material lifecycle reporting.

Каждый комментарий, который создаёт ShipTask, до публикации проходит отдельного
независимого `$ship-tasks:strategic-explainer`. Основной агент устанавливает и
проверяет факты, но не заменяет независимую смысловую редактуру собственной.

Приёмочный incident сообщается сразу в chat и сохраняется в Task history до
начала repair. Opening comment остаётся видимым после исправления, resolution
comment содержит повторную проверку, а final run report перечисляет material
incidents, включая найденные и исправленные в том же run. Пока incident
unresolved, активный run регулярно напоминает о нём без дублирования Task
comments. Только прямое нарушение acceptance называется bug; невозможность
получить evidence называется verification blocker.

Агент сам выбирает инструменты, способ диагностики и
приёмки; сбой одного средства не навязывает его repair. Ограничение относится к
результату: acceptance нельзя ослаблять, а непроверенное нельзя называть
verified.
Перед завершением skill сверяет обещанный и фактический результат,
самостоятельно устраняет доступные проблемы внутри выбранной работы и только
затем даёт компактное причинное объяснение понятным человеку языком.
Каждый комментарий ShipTask проходит отдельного
`$ship-tasks:strategic-explainer`. Субагент переводит установленные факты и
технические изменения в готовый пользовательский текст; основной агент
проверяет точность, но не переписывает текст обратно в журнал реализации.
Explainer не выбирает статус, полномочия или действие и ничего не меняет. Тот
же общий skill можно использовать отдельно от ShipTask.
Старые memory, rollout или report записи о ручной приёмке не меняют этот
contract: пользователь подключается только через reopen либо новую Task.
Task-local вопросы откладывают только конкретную Task, не прерывая остальные;
non-production releases выполняются автоматически, а production требует явного
разрешения пользователя. Goal массовой имплементации остаётся активным, пока в
его границе есть незавершённая работа; сам release не создаёт Goal. Project
memory хранит только selectors/profile и изменяется лишь по явной просьбе.

Task Composer закрывает соседний planning-only этап: формулирует одну Task либо
Epic с problem-first описанием через Strategic Explainer, конкретными
подзадачами, live Labels и semantic relations. Созданные элементы остаются в
`Backlog`; неизвестный current Release не угадывается и не блокирует создание.

## Структура

- [`ship-tasks/SKILL.md`](ship-tasks/SKILL.md) — исполнимый skill.
- [`task-composer/SKILL.md`](task-composer/SKILL.md) — planning-only
  формулировка, декомпозиция и создание Task Manager scope.
- [`strategic-explainer/SKILL.md`](strategic-explainer/SKILL.md) — общий
  problem-first strategic discovery и communication skill для прямого или
  delegated использования без обязательной orchestration scheme.
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
