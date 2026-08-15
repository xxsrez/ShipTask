# ShipTask

ShipTask — репозиторий Codex skill `$ship-tasks`, который через Task Manager
доводит заранее выбранные Tasks, Project или Release до проверенного terminal
outcome под обязательным workflow Goal: выполняет scope, проверяет dependencies,
интегрирует результат, проводит лёгкую проверку каждой Task и тщательную
периодическую проверку review batches, при доступной native comments capability
публикует человекочитаемый delivery report в Task comment, затем согласует
фактические Task statuses. Пока comments недоступны, report step скипается без
изменения Task description. Goal остаётся активным, пока в выбранной границе
есть Tasks, подходящие под рабочие критерии ShipTask.

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
