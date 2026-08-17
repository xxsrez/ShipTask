# ShipTask

ShipTask — репозиторий Codex skill `$ship-tasks`, который через Task Manager
доводит выбранные Tasks, Project или Release до проверенного terminal outcome
при явном invocation и по natural-language delivery intent. Составная команда
создать одну Task и сразу выполнить её также запускает `single`, а не backlog
capture. Exact одна Task работает в `single` mode без Goal; несколько Tasks,
Project, Release и bare `$ship-tasks` — в `batch` mode с обязательным Goal. Bare
scope выбирается из project memory и затем всегда перепроверяется по live Task
Manager state.

Skill выполняет scope, проверяет dependencies, интегрирует результат, проводит
лёгкую проверку каждой Task и тщательную периодическую проверку review batches,
обязательно публикует и перечитывает человекочитаемый delivery report в native
Task comment, затем согласует фактические Task statuses и автоматически
принимает terminal-ready результаты.
Без доказанного comment write/read-back Task остаётся non-terminal; Task
description никогда не используется как fallback.
Старые memory, rollout или report записи о ручной приёмке не меняют этот
contract: пользователь подключается только через reopen либо новую Task.
Task-local вопросы откладывают только конкретную Task, не прерывая остальные;
non-production releases выполняются автоматически, а production требует явного
разрешения пользователя. Batch Goal остаётся активным, пока в выбранной границе
есть Tasks, подходящие под рабочие критерии ShipTask. Project memory хранит
только selectors/profile и изменяется лишь по явной просьбе пользователя.

## Структура

- [`ship-tasks/SKILL.md`](ship-tasks/SKILL.md) — исполнимый skill.
- [`ship-tasks/references/project-memory.md`](ship-tasks/references/project-memory.md)
  — runtime contract project scope/profile memory.
- [Документация](docs/README.md) — единственная specification, Task Manager
  adapter reference, architecture decisions и engineering reports.
- [`scripts/validate_repo.py`](scripts/validate_repo.py) — переносимая
  проверка структуры и project-specific residue.

## Проверка

```bash
python3 scripts/validate_repo.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Установленная копия `~/.codex/skills/ship-tasks` обновляется только по явному
запросу пользователя и после синхронизации должна точно совпадать с каталогом
`ship-tasks/` этого репозитория.
