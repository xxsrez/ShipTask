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
- Распространяйте runtime skill только через отдельный plugin
  `ship-tasks@srez-marketplace`. Task Manager connector устанавливается
  отдельно как adapter-only `task-manager@srez-marketplace`; не помещайте
  ShipTask внутрь его package. Не создавайте и не синхронизируйте
  standalone user-level копию `~/.codex/skills/ship-tasks`.

## Изменения

- Для поведенческого изменения сначала обновите применимую specification,
  затем `ship-tasks/SKILL.md`.
- Сохраняйте `SKILL.md` компактным и переносите подробные объяснения в
  проектную документацию, а не в runtime context skill.
- Не создавайте пустые каталоги или placeholder-документы.
- Не добавляйте runtime state, secrets, private content или signed URLs в Git.

## Definition of done для изменения skill

Поведенческое или distribution-изменение `$ship-tasks` не завершено, пока
одновременно не выполнены все три критерия:

1. Exact repository scope закоммичен в этом репозитории.
2. Этот commit запушен в `origin/main`, а local `HEAD` совпадает с
   `origin/main`.
3. Отдельный Marketplace package является единственной runtime-дистрибуцией:
   `Srez Marketplace/plugins/ship-tasks/skills/ship-tasks` byte-identical
   repository source, а installed cache byte-identical marketplace source и
   отображается installed/enabled. Если изменился runtime payload, manifest
   version или cachebuster обновлён, соответствующий marketplace commit запушен
   в `origin/main`, а plugin переустановлен из
   `ship-tasks@srez-marketplace`. Отдельно установленный
   `task-manager@srez-marketplace` остаётся adapter-only и не содержит
   `skills/ship-tasks`.

Standalone user-level каталог `~/.codex/skills/ship-tasks` должен
отсутствовать, а fresh `skills/list` не должен возвращать отдельный user skill.
Plugin-managed marketplace snapshot и installed cache являются внутренними
копиями одной plugin installation и не удаляются вручную.

Не объявляйте изменение завершённым при частичном выполнении этого списка.
Проверку загрузки нового snapshot выполняйте в новой Codex-сессии; текущая
сессия может сохранять старые skill/tool instructions.

## Проверка перед commit

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
