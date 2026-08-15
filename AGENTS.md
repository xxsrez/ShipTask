# ShipTask repository instructions

Инструкции действуют для всего репозитория.

## Назначение

- Репозиторий является source of truth для Task Manager-only Codex skill
  `$ship-tasks`.
- Исполнимый skill находится в `ship-tasks/`.
- Документация проекта находится в `docs/`; `docs/README.md` — её
  канонический индекс.
- Основной язык документации — русский. Точные protocol/state/tool names можно
  оставлять на английском.

## Границы

- `$ship-tasks` работает только через Task Manager connector. Не добавляйте
  fallback providers, generic task-source abstraction или альтернативный
  tracker workflow.
- Project и Release refs, repository path, branch, deployment provider,
  environment, URL, команды проекта и production policy брать из текущего
  project context, а не зашивать в skill.
- Каноническая specification описывает единственный текущий workflow. Не
  создавайте параллельные поколения или альтернативные specifications.
- Синхронизируйте установленную user-level копию только по явному запросу
  пользователя и проверяйте её точное совпадение с repository source.

## Изменения

- Для поведенческого изменения сначала обновите применимую specification,
  затем `ship-tasks/SKILL.md`.
- Сохраняйте `SKILL.md` компактным и переносите подробные объяснения в
  проектную документацию, а не в runtime context skill.
- Не создавайте пустые каталоги или placeholder-документы.
- Не добавляйте runtime state, secrets, private content или signed URLs в Git.

## Проверка

Перед commit выполните:

```bash
python3 scripts/validate_repo.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Если системные skill paths недоступны на другой машине, обязательным остаётся
`python3 scripts/validate_repo.py`; остальные проверки укажите как
неисполненные, а не симулируйте.

## Plan discipline

- Используйте plan только для действительно многошаговой работы.
- Синхронизируйте plan с фактическим выполнением.
- Перед финальным ответом закройте, измените или явно объясните каждый пункт.
- Verification evidence сообщайте отдельно от статуса plan.
