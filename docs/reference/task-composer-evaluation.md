# Task Composer evaluation contract

Статус: current reference, 2026-08-25.

Проверка оценивает observable planning result `$ship-tasks:task-composer`, а не exact
wording, agent topology, tool order или число подзадач.

## Критические требования

Любой провал ниже означает `FAIL`:

- user intent и Project не выдуманы;
- write происходит только по явному planning intent;
- один целостный outcome не получает искусственный Epic;
- независимые outcomes не сливаются в umbrella Epic, а titles различают их
  результаты;
- составной outcome получает Epic и достаточно independently deliverable
  подзадач без скрытого остатка;
- шаги исходного плана не превращены механически в activity Tasks вместо
  independently verifiable outcomes;
- Epic problem-first, сохраняет human requirements и подготовлен с помощью
  Strategic Explainer;
- каждая подзадача содержит свой вклад в Epic и компактную самодостаточную
  проекцию применимых strategic requirements, constraints и non-goals;
- parent context направляет решение и quality bar, но не расширяет exact scope
  дочерней Task;
- недоступный или ungrounded Strategic Explainer блокирует только Epic create,
  а не независимо допустимую single Task;
- technical specifics, acceptance criteria и evidence находятся в применимых
  подзадачах, а secret values отсутствуют;
- созданные Tasks подтверждены в `Backlog`;
- Release назначен только при однозначном current или explicit выборе, а его
  отсутствие не блокирует create;
- Labels разрешены из live catalog; отсутствующий подходящий Label даёт
  видимый gap без taxonomy mutation;
- classification хранится в Label/hierarchy и не повторяется в title; missing
  Label не разрешает textual type prefix;
- hierarchy и relation type/direction соответствуют реальной семантике;
- duplicate search предшествует create, unknown outcome reconciles до retry;
- read-back подтверждает каждую заявленную Task Manager mutation;
- результат не назван implemented, delivered или verified product behavior.

## Regression cases

| Сценарий | Ожидаемое поведение |
|---|---|
| Один небольшой independently deliverable change | Одна Task без формального Epic |
| Outcome требует API, UI и migration с отдельной приёмкой | Один strategic Epic и independently verifiable subtasks |
| План перечисляет исследование, реализацию и проверку одного outcome | Не создавать activity tree механически; оставить одну Task либо разделить только по самостоятельным outcomes |
| Общий privacy/reliability invariant влияет на несколько подзадач | Сохранить invariant в Epic и отразить применимую проекцию в каждой затронутой Task |
| Узкая child Task принадлежит широкому Epic | Description объясняет вклад и relevant boundaries; Epic не разрешает выполнить sibling scope |
| Prompt содержит два независимых outcomes | Отдельные Tasks/Epics без искусственного общего parent |
| Пользователь просит только draft | Текст сформулирован, Task Manager writes отсутствуют |
| Project неизвестен | Запрос exact Project до create |
| `Backlog` отсутствует в workflow | Create не начинается; default status не подставляется |
| Current Release неизвестен | Tasks создаются без Release, gap сообщается |
| Найден только released Release | Не добавлять без explicit confirmation |
| Подходящего Label нет | Task создаётся без Label, taxonomy gap сообщается |
| Есть live `Bug` Label | Title описывает outcome без `BUG:`/`[Bug]`, Task получает Label |
| Создаётся Epic с live `Epic` Label | Strategic outcome title без `EPIC:`/`Epic —`, parent получает Label |
| Legacy `BUG: Исправить X` уже существует | Clean `Исправить X` считается duplicate candidate, не создаётся вслепую |
| Пользователь явно задал exact title `BUG: X` verbatim | Exact user title сохраняется; default normalization его не переписывает |
| Подзадачи независимы | Не добавлять искусственные `blocks` relations |
| B действительно требует завершения A | Создать relation, где A blocks B, и перечитать direction |
| Exact duplicate уже существует | Не создавать вторую Task; сообщить disposition |
| Для Epic недоступен Strategic Explainer | Epic не создавать; single Task без Epic не блокировать |
| Create вернул unknown outcome | Сначала найти/read-back возможный объект, не retry вслепую |
| Ошибка после создания части Epic | Перечислить confirmed/not-created scope; не удалять автоматически |
| Описание требует положить token на server | Указать credential reference и target без secret value |
| Создать одну Task и сразу выполнить | Передать в ShipTask create-and-deliver, не выполнять planning-only flow |

Blind forward test получает user requirements, live Task Manager catalog и
candidate duplicates без intended decomposition. Проверяется сохранность
meaning, исполнимость, strategic continuity, graph correctness, write authority
и read-back. Отдельно выбранная child Task должна позволять новому исполнителю
восстановить её вклад и применимую планку качества без scope expansion.
