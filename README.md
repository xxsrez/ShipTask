# ShipTask

ShipTask — репозиторий универсального Codex skill `$ship-tasks`, который
доводит заранее определённый task scope до проверенного результата, не
угадывая проектные команды, authority или внешние эффекты.

Текущий исполнимый baseline перенесён из user-level skill, созданного
2026-08-11. Следующая версия с отдельной очередью человеческой приёмки пока
описана как proposal и ещё не включена в runtime contract.

## Структура

- [`ship-tasks/SKILL.md`](ship-tasks/SKILL.md) — исполнимый skill.
- [Документация](docs/README.md) — обзор, v2 proposal и происхождение от
  ExampleNotes `ship-work-release`.
- [`scripts/validate_repo.py`](scripts/validate_repo.py) — переносимая
  проверка структуры и project-specific residue.

## Проверка

```bash
python3 scripts/validate_repo.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Установленная копия `~/.codex/skills/ship-tasks` не обновляется из этого
репозитория автоматически. Способ синхронизации или packaging будет принят
отдельным решением.
