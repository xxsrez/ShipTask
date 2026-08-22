# ShipTask repository instructions

Инструкции действуют для всего репозитория.

## Назначение

- Репозиторий является source of truth для Task Manager-only Codex skills
  `$ship-tasks`, `$task-composer` и общего communication skill
  `$strategic-explainer`.
- Исполнимые skills находятся в sibling-каталогах `ship-tasks/`,
  `task-composer/` и `strategic-explainer/`.
- Документация проекта находится в `docs/`; `docs/README.md` — её
  канонический индекс.
- Основной язык документации — русский. Точные protocol/state/tool names можно
  оставлять на английском.

## Границы

- `$ship-tasks` работает только через Task Manager connector. Не добавляйте
  fallback providers, generic task-source abstraction или альтернативный
  tracker workflow.
- `$task-composer` остаётся Task Manager-only planning workflow: не добавляйте
  delivery, implementation, release, Goal lifecycle, fallback provider или
  право автоматически менять Label taxonomy.
- `$strategic-explainer` остаётся generic: не добавляйте в его runtime contract
  ShipTask, Task Manager, конкретный tracker, project lifecycle или право
  принимать решения/выполнять mutations.
- Requests сформулировать, создать, разложить или положить Task Manager работу
  в backlog направляйте через `$task-composer`, когда он доступен. Это
  planning-only mutation и не запускает ShipTask delivery. Read/status/audit
  без постановки оставляйте техническому Task Manager adapter.
- Project и Release refs, repository path, branch, deployment provider,
  environment, URL, команды проекта и production policy брать из текущего
  project context, а не зашивать в skill.
- Каждая каноническая specification описывает один текущий workflow. Не
  создавайте параллельные поколения или альтернативные specifications одного
  и того же runtime skill.
- Распространяйте все три runtime skills только через отдельный plugin
  `ship-tasks@srez-marketplace`. Task Manager connector устанавливается
  отдельно как adapter-only `task-manager@srez-marketplace`; не помещайте
  ShipTask внутрь его package. Не создавайте и не синхронизируйте
  standalone user-level копии `~/.codex/skills/ship-tasks`,
  `~/.codex/skills/task-composer` и
  `~/.codex/skills/strategic-explainer`.

## Изменения

- Для поведенческого изменения сначала обновите применимую specification,
  затем соответствующий runtime `SKILL.md`.
- Считайте current requirements конституцией для агентов: фиксируйте outcome,
  rationale, observable evidence и authority/safety boundaries, но не
  предписывайте agent topology, tool choreography, число попыток, форму context
  или внутренний reasoning, если только это не является явным требованием
  пользователя. Текущие явные исключения: каждый комментарий ShipTask проходит
  отдельного независимого Strategic Explainer, а обычный переход
  `To Do → In Progress` комментария не создаёт. Точный порядок оставляйте только
  для доказуемого инварианта целостности, безопасности или внешнего эффекта.
- Сохраняйте `SKILL.md` компактным и переносите подробные объяснения в
  проектную документацию, а не в runtime context skill.
- Не создавайте пустые каталоги или placeholder-документы.
- Не добавляйте runtime state, secrets, private content или signed URLs в Git.

## Definition of done для изменения skill

Поведенческое или distribution-изменение любого runtime skill не завершено, пока
одновременно не выполнены все три критерия:

1. Exact repository scope закоммичен в этом репозитории.
2. Этот commit запушен в `origin/main`, а local `HEAD` совпадает с
   `origin/main`.
3. Отдельный Marketplace package является единственной runtime-дистрибуцией:
   `Srez Marketplace/plugins/ship-tasks/skills/ship-tasks`,
   `Srez Marketplace/plugins/ship-tasks/skills/task-composer` и
   `Srez Marketplace/plugins/ship-tasks/skills/strategic-explainer`
   byte-identical соответствующим repository sources, а installed cache
   byte-identical marketplace source и отображается installed/enabled. Если
   изменился runtime payload, manifest version или cachebuster обновлён,
   соответствующий marketplace commit запушен в `origin/main`, а plugin переустановлен из
   `ship-tasks@srez-marketplace`. Отдельно установленный
   `task-manager@srez-marketplace` остаётся adapter-only и не содержит
   `skills/ship-tasks`, `skills/task-composer` или
   `skills/strategic-explainer`.

Standalone user-level каталоги `~/.codex/skills/ship-tasks`,
`~/.codex/skills/task-composer` и
`~/.codex/skills/strategic-explainer` должны отсутствовать, а fresh
`skills/list` не должен возвращать отдельные user skills.
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
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py task-composer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
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
