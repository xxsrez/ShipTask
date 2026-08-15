# Разработка и проверка

## Перед изменением

1. Прочитайте root `AGENTS.md`, текущий `ship-tasks/SKILL.md` и затронутую
   specification.
2. Для Task Manager mapping сверяйте текущий connector contract и
   [adapter reference](../reference/task-manager-adapter.md).
3. Сначала меняйте единственную
   [specification](../specs/ship-tasks.md), затем runtime skill.

## Изменение skill

- Держите YAML frontmatter только с `name` и `description`.
- Все trigger conditions перечисляйте в `description`.
- Пишите body в imperative/infinitive form и не дублируйте подробные reference
  документы.
- Сохраняйте `policy.allow_implicit_invocation: false`.
- Не добавляйте fallback provider. Task Manager tool names и semantics,
  необходимые для безопасного выполнения, являются частью runtime contract.

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
- после разрешения exact scope и до первой non-Goal mutation создаётся Goal с
  observable done criteria; совместимый активный Goal продолжается,
  несовместимый вызывает `TASK CONTEXT ALARM` и не перезаписывается;
- `Backlog` исключается без Task writes, а явно разрешённый create использует
  current status ref `To Do`;
- `To Do`, `In Progress` и `In Review` маршрутизируются соответственно в новую
  работу, resume и review;
- каждая Task проходит быстрый targeted gate, но дорогой aggregate/full gate
  выполняется один раз на exact review batch по trigger policy, а не на каждый
  member;
- batch target, review WIP и triggers не позволяют запускать дорогой singleton
  gate лишь для удобства, но допускают risk-driven и final singleton;
- failed batch gate возвращает Tasks с недействительным evidence в
  `In Progress`; при неясной attribution reopen получает связанный batch;
- mixed scope однозначно выбирает review/completion перед resume и новой
  работой, затем пересчитывает disposition;
- changes-requested rework сохраняет текущую lane до повторного review или
  blocker;
- review canonical Task читает все входящие `duplicate_of` и превращает иной
  failure scenario в finding, а не в отдельную execution lane;
- missing authority вызывает `TASK CONTEXT ALARM` до mutation;
- `completion-remains` не превращается в `no-work`;
- `In Review` после успешных checks/external effect, но без authorized
  acceptance, оставляет plan и Goal активными и запрещает completion claim;
- Goal остаётся активным при любой подходящей `To Do`, `In Progress`,
  `In Review`, rework/completion remnant или unresolved in-scope defect;
- перед `update_goal(complete)` повторная complete inventory выбранной границы
  подтверждает отсутствие подходящих Tasks и прохождение всех completion gates;
- `no-work` сначала reconciles Task/evidence state и обязательный Goal, затем
  завершает Goal и останавливает workflow;
- out-of-scope defect не исправляется автоматически;
- parallel request честно ограничивается dependency/review capacity;
- изменения после `changes-requested` возвращаются как delta review.

Не передавайте тестовому агенту ожидаемый ответ или скрытую diagnosis.

## Установленная копия

Каталог `ship-tasks/` в этом репозитории является source of truth. Копию в
`~/.codex/skills/ship-tasks` обновляйте только по явной команде пользователя.
После синхронизации сравните `SKILL.md` и `agents/openai.yaml` byte-for-byte и
провалите handoff при расхождении.
