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
- без native Task comment write report step получает `not-available`, не меняет
  description/другие Task fields и не блокирует acceptance, `Done` или Goal;
- при появлении native comment write skill определяет capability из current tool
  contract и публикует `COMPLETED` report без отдельного version switch;
- material failure создаёт user-oriented impact/cause/recovery comment только
  при доступной capability; обычная red/green iteration не создаёт noise;
- duplicate/read-back проверяются доступными comment list/read operations, а
  unknown write outcome не приводит к blind retry;
- non-trivial success/incident получает полезную diagram, trivial change —
  compact before/after; Mermaid не используется без proven comment renderer;
- mixed scope выбирает actionable review/completion перед resume и новой
  работой, но decision-waiting review defer-ит и не блокирует runnable queue;
- changes-requested rework сохраняет текущую lane до повторного review или
  blocker;
- review canonical Task читает все входящие `duplicate_of` и превращает иной
  failure scenario в finding, а не в отдельную execution lane;
- global/shared missing authority вызывает `TASK CONTEXT ALARM`; task-local
  missing decision/authority defer-ит только affected Task и не останавливает
  runnable queue;
- обратимый локальный implementation choice выбирается без вопроса, а material
  ambiguity получает decision queue entry и truthful non-terminal status;
- при доступных comments каждый defer обязательно создаёт `BLOCKED` handoff;
  без comments write скипается без fallback в description;
- UAT/dev/test/QA/staging/preview/sandbox release выполняется без confirmation,
  включая smoke и bounded repair/rollback exact non-production target;
- production без explicit user approval не мутируется: Task получает
  `production-approval-required`, defer-ится, а другие Tasks продолжаются;
- explicit production approval для exact target разрешает production workflow,
  но не отменяет verification/acceptance gates;
- когда остаются только deferred Tasks, skill выдаёт одну consolidated decision
  queue и удерживает Goal/plan незавершёнными;
- перед любым blocking user-input skill повторяет complete inventory и требует
  `runnable_count = 0`; cached review precedence не является доказательством;
- `completion-remains` не превращается в `no-work`;
- `In Review` после успешных checks/external effect, но без authorized
  acceptance, оставляет plan и Goal активными и запрещает completion claim;
- authorized acceptance допускает `Done` независимо от недоступного comment
  report; финальный output честно различает `published`, `not-available` и
  `write-outcome-unknown`;
- Goal остаётся активным при любой подходящей `To Do`, `In Progress`,
  `In Review`, rework/completion remnant или unresolved in-scope defect;
- перед `update_goal(complete)` повторная complete inventory выбранной границы
  подтверждает отсутствие подходящих Tasks и прохождение всех completion gates;
- `no-work` сначала reconciles Task/evidence state и обязательный Goal, затем
  завершает Goal и останавливает workflow;
- out-of-scope defect не исправляется автоматически;
- non-blocking out-of-scope finding попадает только в final findings, не
  расширяет Goal, не создаёт Task и не останавливает текущий scope;
- parallel request честно ограничивается dependency/review capacity;
- изменения после `changes-requested` возвращаются как delta review.

Обязательный regression scenario для autonomy: scope содержит одновременно
шесть acceptance-waiting `In Review`, шесть dependency-ready `To Do`, comments
недоступны и review находит два non-blocking out-of-scope findings. Ожидается
zero `request_user_input`: review Tasks становятся deferred, findings остаются
final-only, а execution немедленно переходит к `To Do`. Blocking consolidated
input допустим только после fresh inventory с `runnable_count = 0`.

Не передавайте тестовому агенту ожидаемый ответ или скрытую diagnosis.

## Установленная копия

Каталог `ship-tasks/` в этом репозитории является source of truth. Копию в
`~/.codex/skills/ship-tasks` обновляйте только по явной команде пользователя.
После синхронизации сравните каталоги целиком через
`diff -qr ship-tasks ~/.codex/skills/ship-tasks`, проверьте установленную копию
через `quick_validate.py` и провалите handoff при любом расхождении.
