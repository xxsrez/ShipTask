# ShipTask

ShipTask — репозиторий Codex skill `$ship-tasks`, который через Task Manager
доводит заранее выбранные Tasks, Project или Release до проверенного terminal
outcome: выполняет scope, проверяет dependencies, интегрирует результат,
проводит verification и согласует фактические Task statuses.

## Структура

- [`ship-tasks/SKILL.md`](ship-tasks/SKILL.md) — исполнимый skill.
- [Документация](docs/README.md) — единственная specification, Task Manager
  connector reference и engineering reports.
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
