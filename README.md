# Issue Grinder и Strategic Explainer

Репозиторий содержит исходники основных действующих навыков:
`$issue-grinder`, `$issue-grinder:task-composer`,
`$issue-grinder:scope-reviewer` и `$strategic-explainer:strategic-explainer`.
В Issue Grinder также входит вспомогательный `consultant`.
Legacy `$ship-tasks` удалён из runtime и Marketplace. Его прежние решения
остались в исторических ADR и защищённом пользовательском Requirements.

`$issue-grinder` выполняет выбранную работу через Task Manager. Он ведёт
scope до проверенного результата или честной возобновляемой контрольной точки.
Доступны четыре режима: `Соло`, `Классический`, `Баланс` и
`Экономичный`. Явный выбор пользователя имеет приоритет; автоматический
выбор учитывает профиль основной модели и содержательный размер работы.
Подробности и ограничения приведены в
[мануале по режимам](docs/guides/issue-grinder-modes.md).

`$issue-grinder:task-composer` формулирует и создаёт задачи в `Backlog`;
delivery не выполняет. `$issue-grinder:scope-reviewer` проверяет план или
активный долгий прогон и составляет понятный отчёт. Только явная просьба
улучшить план разрешает ему менять agent-owned planning model.
`$strategic-explainer:strategic-explainer` готовит текст комментария,
отчёта или итогового ответа по переданным фактам и источникам. Он не решает,
какие действия и изменения статуса допустимы.

Документация является исходным кодом. У каждого действующего навыка в
[`docs/skills/<skill>/`](docs/skills/README.md) отдельно хранятся Overview,
Requirements и Architecture. Общие правила см. в
[философии проекта](docs/philosophy.md); канонический индекс —
[документация](docs/README.md). Исторические документы ShipTask не являются
инструкцией для текущего runtime.

## Структура

- [Issue Grinder](issue-grinder/SKILL.md) — delivery.
- [Task Composer](task-composer/SKILL.md) — планирование и создание задач.
- [Scope Reviewer](scope-reviewer/SKILL.md) — проверка плана и отчёт.
- [Strategic Explainer](strategic-explainer/SKILL.md) — подготовка текста.
- [Валидатор](scripts/validate_repo.py) — структура, контракт и отсутствие
  удалённого runtime.

## Проверка

```bash
python3 scripts/validate_repo.py
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py issue-grinder
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py task-composer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py scope-reviewer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

## Поставка

Current runtime публикуется двумя установленными независимыми plugin:
`issue-grinder@srez-marketplace` содержит Issue Grinder, Task Composer и Scope Reviewer;
`strategic-explainer@srez-marketplace` — только ordinary Strategic Explainer.
Task Manager устанавливается отдельно как adapter-only package. Codex manifest
не умеет автоматически устанавливать plugin dependency: вызывающий навык
использует `$strategic-explainer:strategic-explainer`, когда он доступен и
разрешён, согласно собственному контракту. Каждый repository source
сверяется со своим Marketplace package и installed plugin cache. Каталог
Marketplace не содержит `ship-tasks@srez-marketplace`.
