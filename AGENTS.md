# ShipTask repository instructions

Инструкции действуют для всего репозитория.

## Ключевые документы

- Перед изменением проекта прочитайте [`docs/philosophy.md`](docs/philosophy.md).
  Это ключевой документ о свободе агента, слоях исходного кода и владельцах
  решений.
- [`docs/README.md`](docs/README.md) — канонический индекс документации, а
  [`docs/skills/README.md`](docs/skills/README.md) — техническая схема source
  packages.
- Репозиторий является source of truth для `$issue-grinder`, legacy
  `$ship-tasks`, `$issue-grinder:task-composer`,
  `$issue-grinder:scope-reviewer` и `$strategic-explainer`.
  Runtime находится в `issue-grinder/`, `ship-tasks/`, `task-composer/`,
  `scope-reviewer/` и `strategic-explainer/`.
- Основной язык документации — русский. Точные названия protocol, state и tool
  можно оставлять на английском.

## Документация как исходный код

Единица source — отдельная entity. Для неё используются три независимых
документа:

1. **Overview:** user-owned `docs/skills/<skill>/overview.md` с общим описанием
   цели, адресата и назначения entity.
2. **Requirements:** user-owned `docs/skills/<skill>/requirements.md` с набором
   требований.
3. **Architecture:** agent-owned `docs/skills/<skill>/architecture.md` с
   дополнительными инструкциями и решениями для достижения пользовательской
   цели.

Overview и Requirements принадлежат пользователю. Не создавайте и не
редактируйте `overview.md` или `requirements.md` без явного указания
пользователя обновить соответствующий документ — в том числе ради редакционной
правки. Обычная просьба изменить runtime такого разрешения не даёт.

Обсуждение предложения, review, согласие пользователя с идеей или отдельным
пунктом и просьба продолжить анализ **не являются разрешением на запись** в
Overview или Requirements. Перед любой такой записью нужна отдельная явная
команда пользователя, которая прямо называет изменение Overview или
Requirements. Без неё показывайте только предлагаемый текст или diff, а сами
user-owned файлы сохраняйте byte-identical. Разрешение на одну конкретную правку
не переносится на последующие правки.

Architecture принадлежит агенту только в пределах разрешённой задачи. Меняйте
её для улучшения способа достижения пользовательской цели, но не ослабляйте, не
расширяйте и не переопределяйте Overview или Requirements. Конфликт двух
пользовательских документов разрешает только пользователь.

Runtime является смысловой компиляцией трёх самостоятельных входов. Требуется
трасса `Overview | Requirements | Architecture → runtime entity → observable
evaluation` и возможность восстановить семантически эквивалентный runtime из
трёх локальных документов. ADR, reports, agent memory, реализация и документы
соседней entity не создают скрытую current policy.

## Границы компонентов

- `$issue-grinder` и legacy `$ship-tasks` выполняют delivery только через Task
  Manager connector. Не добавляйте fallback provider или generic tracker
  abstraction.
- `$issue-grinder:task-composer` остаётся Task Manager-only planning workflow:
  без delivery, implementation, release, Goal lifecycle, fallback provider и
  автоматического изменения Label taxonomy.
- `$issue-grinder:scope-reviewer` остаётся Task Manager-only review workflow:
  read/status и Release review не создают writes, явный plan-improvement intent
  разрешает менять только agent-owned planning model, а Human Requirements,
  delivery lifecycle и authority decisions остаются вне его полномочий.
- `$strategic-explainer` остаётся generic communication skill: без ShipTask,
  Task Manager, project lifecycle, mutations и authority decisions в runtime
  contract.
- Запросы создать или разложить Task Manager работу направляйте через Task
  Composer, когда он доступен. Предзапусковое ревью Task Manager плана и
  человекочитаемое изучение активного долгого Issue Grinder run автоматически
  направляйте через Scope Reviewer даже без явного имени skill-а; это не
  запускает delivery. Ordinary read/status/audit одной карточки оставляйте Task
  Manager adapter.
- Project и Release refs, repository path, branch, provider, environment, URL,
  команды и production policy берите из current project context, а не
  зашивайте в skill.
- Каждый `architecture.md` описывает один current workflow. Не создавайте
  параллельные поколения Overview, Requirements или Architecture.

## Изменение source package

- Если пользователь явно поручил обновить Overview ради изменения общего
  смысла, адресата или назначения сущности, начинайте с локального `overview.md`.
- Если пользователь явно поручил обновить Requirements ради изменения outcome
  или boundary, начинайте с локального `requirements.md`, затем обновляйте
  Architecture, runtime и observable evaluation.
- Изменение только способа достижения начинайте с локального `architecture.md`;
  Overview и Requirements не трогайте. Затем обновляйте runtime и evaluation.
- Если классификация неоднозначна, сохраните current Overview и Requirements и
  вынесите вопрос пользователю. Не начинайте с runtime-only правки и не
  восстанавливайте пользовательский смысл из памяти, старого ADR, соседнего
  skill или реализации.
- Сохраняйте `SKILL.md` компактным. Подробные rationale и mechanics держите в
  проектной документации и локальных references.
- Не создавайте placeholder-документы и не добавляйте в Git runtime state,
  secrets, private content или signed URLs.

## Distribution boundaries

- `issue-grinder@srez-marketplace` содержит Issue Grinder, Task Composer и Scope Reviewer;
  `strategic-explainer@srez-marketplace` — только Strategic Explainer.
- `task-manager@srez-marketplace` остаётся отдельным adapter-only package и не
  содержит skills этого репозитория.
- `ship-tasks@srez-marketplace` — неустановленный legacy rollback artifact; его
  нельзя устанавливать одновременно с Issue Grinder.
- Не создавайте standalone user-level копии в
  `~/.codex/skills/{issue-grinder,ship-tasks,task-composer,scope-reviewer,strategic-explainer}`.

## Definition of done для изменения skill

Поведенческое или distribution-изменение runtime skill завершено, только если:

1. Exact repository scope закоммичен и запушен в `origin/main`, а local `HEAD`
   совпадает с `origin/main`.
2. Repository sources byte-identical соответствующим sources в двух
   установленных Marketplace packages: Issue Grinder/Task Composer/Scope Reviewer в
   `Srez Marketplace/plugins/issue-grinder/skills/` и Strategic Explainer в
   `Srez Marketplace/plugins/strategic-explainer/skills/`.
3. Installed cache byte-identical Marketplace sources; оба plugins имеют
   состояние installed/enabled; `ship-tasks@srez-marketplace` не установлен;
   Task Manager остаётся adapter-only; standalone user-level каталоги
   отсутствуют.
4. Если runtime payload изменился, обновлены manifest version или cachebuster,
   marketplace commit запушен, затронутые plugins переустановлены, а новый
   snapshot проверен в свежей Codex-сессии.

Не объявляйте runtime-изменение завершённым при частичном выполнении списка.
Для docs-only правки без изменения runtime payload переустановка не требуется.

## Проверка перед commit

```bash
python3 scripts/validate_repo.py
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py issue-grinder
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py task-composer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py scope-reviewer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Если системный skill path недоступен, обязательным остаётся
`python3 scripts/validate_repo.py`; остальные проверки укажите как
неисполненные, а не симулируйте.
