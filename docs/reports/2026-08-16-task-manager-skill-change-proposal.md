# Предложение по изменению Task Manager skill

Статус: handoff proposal, source не изменён. Дата наблюдения: 2026-08-16.

## Краткий вывод

Task Manager skill нужно изменить. Connector и MCP backend уже предоставляют
необходимую техническую поверхность; продуктовый API менять не требуется.
Изменение относится к marketplace skill и его metadata: из них следует убрать
самостоятельный single-Task delivery workflow и оставить технический adapter.

Task для этой работы можно вести в проекте Task Manager, но фактический source
лежит не в product repository, а в:

```text
/workspace/Srez Marketplace/
  plugins/task-manager/
```

Текущий source commit `351b592` и установленный cache plugin 0.4.1 на момент
анализа byte-identical для `SKILL.md` и `agents/openai.yaml`.

## Почему изменение обязательно

Marketplace `task-manager` сейчас одновременно является:

1. техническим adapter к OAuth/MCP connector;
2. владельцем natural-language single-Task delivery;
3. владельцем Goal prohibition для этого flow;
4. владельцем status lifecycle и terminal transition;
5. владельцем обязательных completion/failure reports и их содержания.

После включения implicit ShipTask запрос `Выполни TM-123` соответствует
description обоих skills. Один запрещает Goal и разрешает брать прямо
запрошенную Backlog Task, другой исключает Backlog и применяет собственную
delivery policy. Простое добавление ShipTask без изменения Task Manager skill
создаст неоднозначный routing и конфликт authority.

Официальная документация OpenAI указывает, что implicit activation зависит от
skill `description`; границы и trigger words должны быть сформулированы там:
<https://learn.chatgpt.com/docs/build-skills>.

## Целевая ответственность Task Manager skill

Оставить в skill только технические знания, нужные любому вызывающему workflow:

- подключение через native OAuth и обработку insufficient scope;
- `get_workspace` и capability discovery;
- разрешение Project/Release/Task names в canonical refs;
- list/detail progressive disclosure и pagination;
- current Task detail, provenance и external context rules;
- safe create/update semantics;
- current `version`, `version_conflict`, reread и read-back;
- null-clearing semantics и защиту от blind create retry;
- native comment/thread operations, idempotency, deduplication и reconciliation;
- честное описание отсутствующих MCP capabilities.

Не оставлять в Task Manager skill:

- выбор single/batch delivery mode;
- разрешение выполнять Task только из delivery phrasing;
- Goal creation либо запрет Goal;
- `Backlog`/`To Do`/`In Progress`/`In Review` бизнес-переходы;
- automatic acceptance и решение о terminal status;
- обязательность, тип и человекочитаемый формат delivery reports;
- release/deploy authority, UAT/production policy и external effects;
- integration, verification и completion evidence policy;
- выбор другой Task после blocker.

Эти решения должен передавать вызывающий business workflow — ShipTask либо
прямое явное указание пользователя для обычной Task Manager mutation.

## Изменения по файлам

### `skills/task-manager/SKILL.md`

1. Переписать frontmatter description как adapter-only trigger.
2. Сохранить и уточнить разделы `Connection`, `Discovery workflow`, `Writes` и
   `Task comments`.
3. Удалить раздел `Single-task delivery` полностью.
4. Удалить раздел `Work completion reports` полностью.
5. Заменить `Results` на adapter-level output: canonical identity, фактический
   read/write result, pagination, new version и unreconciled outcome.
6. Добавить короткий `Business workflow boundary`: skill не выбирает delivery
   lifecycle; когда активен ShipTask, его policy определяет scope и разрешённые
   side effects.

Candidate frontmatter:

```yaml
description: >-
  Use Task Manager through its connected MCP tools as a technical adapter to
  find, filter, inspect, create, update, and comment on tasks and to navigate
  projects and releases. Trigger for Task Manager data access, canonical ref
  resolution, current versions, OAuth capabilities, pagination, safe writes,
  and native comment operations. Do not define or independently run delivery,
  Goal, verification, release, report-content, or terminal-status policy; a
  calling workflow such as ShipTask owns those decisions.
```

`allow_implicit_invocation` можно оставить по умолчанию включённым: adapter
должен автоматически подключаться к запросам о Task Manager. Его description
больше не должен рекламировать `do/fix/finish` как самостоятельный delivery
workflow.

### `skills/task-manager/agents/openai.yaml`

Заменить:

- `short_description: "Deliver one task with a durable report"`;
- default prompt про end-to-end delivery без Goal.

На adapter-oriented metadata, например:

```yaml
interface:
  display_name: "Task Manager"
  short_description: "Find and manage Task Manager data safely"
  default_prompt: "Use $task-manager to inspect Task Manager and apply only the exact task mutation I request."
```

### `.codex-plugin/plugin.json`

Обновить все user-facing claims, которые обещают delivery без Goal:

- top-level `description`;
- `interface.shortDescription`;
- `interface.longDescription`;
- delivery example в `interface.defaultPrompt`.

Рекомендуемый продуктовый смысл metadata: подключить Task Manager, найти и
прочитать work, безопасно создать/изменить Task и работать с native comments.
Не обещать end-to-end software delivery как capability самого connector
plugin.

Поскольку 0.4.1 публично рекламирует single-Task delivery, его удаление является
заметным pre-1.0 behavioral change. Рекомендуемый следующий version — `0.5.0`,
а не patch `0.4.2`.

### Файлы, которые менять не требуется

- `.mcp.json`: production `/api/mcp` endpoint остаётся тем же.
- `.app.json`: registered app/OAuth connection не меняется.
- Task Manager backend и MCP tool schema: текущих capabilities достаточно.
- Product Sites UAT/production bindings: plugin refactor не является Sites
  release и не требует migration или synthetic data.

## Технический adapter contract после изменения

Calling workflow должен передавать adapter следующие решения:

| Решение | Владелец |
|---|---|
| Что пользователь хочет: read, planning write или delivery | ShipTask/current request |
| Exact Task/Project/Release selector | ShipTask/current request/project memory |
| Нужно ли создавать Goal | ShipTask |
| Какие status transitions разрешены | ShipTask/current request |
| Нужен ли report и какого типа | ShipTask |
| Разрешён ли deploy/external effect | ShipTask + project context + user authority |
| Как вызвать MCP tool безопасно | Task Manager skill |
| Как обработать version conflict/read-back | Task Manager skill |

Adapter не должен молча ослаблять или усиливать переданную authority. Например,
наличие `update_task` не разрешает status transition, а наличие
`add_task_comment` не делает report обязательным — это определяет business
workflow.

## Предлагаемая Task Manager Task

**Title:** Сделать marketplace Task Manager skill техническим adapter без
delivery business policy

**Problem:** Plugin 0.4.1 самостоятельно исполняет одну Task, запрещает Goal и
определяет lifecycle/reports. После implicit ShipTask это создаёт двух
владельцев одного natural-language delivery intent.

**Scope:**

- изменить marketplace `plugins/task-manager/skills/task-manager/SKILL.md`;
- обновить `agents/openai.yaml` и `.codex-plugin/plugin.json`;
- bump plugin version;
- проверить adapter reads/writes/comments и совместный routing с ShipTask;
- переустановить plugin только в согласованный cutover.

**Acceptance criteria:**

- Skill содержит OAuth/MCP discovery, canonical refs, pagination, safe writes,
  concurrency и comment mechanics.
- Skill не содержит single-Task delivery, Goal, release, verification,
  report-content или terminal lifecycle policy.
- Plugin metadata не обещает delivery одной Task без Goal.
- `Покажи TM-123` и `Обнови title TM-123` корректно используют adapter.
- `Выполни TM-123` при установленном ShipTask маршрутизируется в ShipTask и не
  запускает второй независимый workflow.
- Planning/backlog request не превращается в delivery.
- Existing OAuth endpoint и MCP tool behavior не изменены.
- Source проходит skill/plugin validation; после install проверен fresh chat,
  а installed version и source совпадают.

## Проверка

В marketplace repository выполнить минимум:

1. `quick_validate.py` для `plugins/task-manager/skills/task-manager`.
2. JSON parse/manifest validation для `.codex-plugin/plugin.json`, `.app.json`,
   `.mcp.json` и marketplace catalog.
3. Проверку отсутствия stale claims:
   `Single-task delivery`, `Work completion reports`, `without a Goal`,
   `deliver one`.
4. Adapter smoke: workspace, Project/Release resolution, paginated Task list,
   full Task detail, safe update с current version, comment add/read-back и
   version-conflict recovery на разрешённых тестовых данных.
5. Fresh-chat trigger matrix вместе с новой ShipTask version.
6. Reinstall/update plugin и byte/version reconciliation установленного bundle.

## Cutover dependency

Не публиковать adapter-only plugin как изолированное изменение, если
natural-language delivery должен оставаться доступным непрерывно. Рекомендуемый
cutover:

1. Подготовить и проверить ShipTask с single/batch modes, пока установленная
   копия ещё не синхронизирована.
2. Подготовить Task Manager plugin 0.5.0.
3. Сократить global `~/.codex/AGENTS.md` до routing и hard safety boundaries;
   убрать дублированный single-Task business flow.
4. Согласованно синхронизировать ShipTask и обновить/reinstall plugin.
5. Начать свежий chat и проверить positive/negative routing prompts.

До cutover текущий Task Manager skill остаётся действующим 0.4.1 contract;
этот документ сам по себе его не меняет.

## Риски

- Если включить implicit ShipTask раньше удаления старого delivery flow,
  появится конфликт двух skills.
- Если сначала удалить marketplace flow, но не установить новый ShipTask,
  свободная команда `Выполни TM-123` потеряет end-to-end semantics.
- MCP dependency ShipTask не является доказанной skill-to-skill dependency.
  На fresh-chat тесте нужно подтвердить, что explicit и implicit ShipTask
  получает adapter guidance; до этого нельзя удалять из ShipTask минимальные
  canonical-ref/version/read-back safety invariants.
- Старый открытый chat может сохранить прежний skill/tool snapshot после
  reinstall; обязательна проверка в новой сессии.
- ChatGPT web/Work может не видеть standalone local ShipTask и local project
  memories. Adapter-only plugin на этих поверхностях не должен обещать
  отсутствующий business workflow; cross-surface delivery требует отдельного
  решения о распространении ShipTask и project context.

## Вне scope

- Изменение Task Manager product UI/backend.
- Переключение plugin на UAT.
- Sites deploy или database migration.
- Создание project memory.
- Изменение ShipTask runtime в marketplace repository.
