# Разработка и проверка

## Перед изменением

1. Прочитайте root `AGENTS.md`, текущий `ship-tasks/SKILL.md` и затронутую
   specification.
2. Определите, меняется runtime contract или только proposal/reference.
3. Не используйте ExampleNotes документы как authority для другого проекта.

## Изменение skill

- Держите YAML frontmatter только с `name` и `description`.
- Все trigger conditions перечисляйте в `description`.
- Пишите body в imperative/infinitive form и не дублируйте подробные reference
  документы.
- Сохраняйте `policy.allow_implicit_invocation: false`.
- Не добавляйте project-specific terms, commands или provider assumptions.

## Проверка

```bash
python3 scripts/validate_repo.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Repository validator работает без внешних Python dependencies и запускается в
GitHub Actions. System-level validators дают дополнительную локальную проверку
структуры skill и документации.

## Forward test

Для значимого изменения используйте fresh no-write scenario, в котором новый
Codex task получает только:

- путь к candidate skill;
- реалистичный task scope;
- минимальный project context, который увидел бы обычный пользователь.

Проверьте как минимум:

- coherent scope проходит preflight;
- missing authority вызывает `TASK CONTEXT ALARM` до mutation;
- `completion-remains` не превращается в `no-work`;
- out-of-scope defect не исправляется автоматически;
- parallel request честно ограничивается dependency/review capacity;
- изменения после `changes-requested` возвращаются как delta review.

Не передавайте тестовому агенту ожидаемый ответ или скрытую diagnosis.

## Установленная копия

Каталог `ship-tasks/` в этом репозитории является source of truth. Копия в
`~/.codex/skills/ship-tasks` существует отдельно. Не меняйте её, не создавайте
symlink и не удаляйте без явной команды пользователя. После отдельного
решения о packaging этот раздел следует заменить проверенным install/update
workflow.
