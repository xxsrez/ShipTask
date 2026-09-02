# Task Composer: observable evaluation

Статус: current observable evaluation, 2026-09-02. Документ проверяет
компиляцию локальных [Overview](overview.md), [Requirements](requirements.md) и
[Architecture](architecture.md), но не создаёт новый policy contract.

Проверка оценивает observable planning result `$issue-grinder:task-composer`, а не exact
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
- Epic problem-first, сохраняет human requirements и подготовлен через semantic
  facade Strategic Explainer с назначением, исходным вопросом, exact planning
  scope, языком, material constraints и resolvable source anchors;
- Task Composer знает только semantic request/result contract: не читает
  provider-internal contract, не пишет explanation candidate, не передаёт
  format/method rules и не улучшает ready result самостоятельно;
- каждая подзадача содержит свой вклад в Epic и компактную самодостаточную
  проекцию применимых strategic requirements, constraints и non-goals;
- parent context направляет решение и quality bar, но не расширяет exact scope
  дочерней Task;
- недоступный или ungrounded Strategic Explainer блокирует только Epic create,
  а не независимо допустимую single Task;
- technical specifics, acceptance criteria и evidence находятся в применимых
  подзадачах, а secret values отсутствуют;
- каждый уместный attachment из bug report сохранён как native attachment
  применимой Task; уместность screenshot и любого другого файла обоснована его
  содержанием, связью с Task и пользой исполнителю, а не типом или форматом;
- созданные Tasks подтверждены в `Backlog`;
- Release назначен только при однозначном current или explicit выборе, а его
  отсутствие не блокирует create;
- Labels разрешены из live catalog; отсутствующий подходящий Label даёт
  видимый gap без taxonomy mutation;
- classification хранится в Label/hierarchy и не повторяется в title; missing
  Label не разрешает textual type prefix;
- hierarchy и relation type/direction соответствуют реальной семантике;
- duplicate search предшествует create, unknown outcome reconciles до retry;
- read-back подтверждает каждую заявленную Task Manager mutation, включая
  attachment binding и metadata;
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
| Bug report содержит screenshot интерфейса, на котором видна именно описанная проблема | Создать применимую Task, прикрепить screenshot как native attachment и подтвердить attachment read-back: решение основано на содержании и связи с проблемой, а не на типе файла |
| Bug report содержит screenshot, не связанный с описанной проблемой | Не прикреплять screenshot и явно сообщить его disposition; тип файла не создаёт презумпцию уместности |
| Bug report содержит релевантный log и случайный несвязанный файл | Прикрепить log к применимой Task; случайный файл не добавлять и явно сообщить disposition |
| Составной Epic содержит screenshot, относящийся к одной child Task | Прикрепить screenshot к этой child Task, не копировать механически во все children |
| Native transport обязательного attachment заведомо недоступен | Create не начинается; attachment не заменяется путём, URL или пересказом |
| Task создана, но attachment bind завершился с ошибкой | Сообщить partial result и exact missing attachment; не объявлять planning create полным и не повторять bind с новой identity вслепую |
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
| Facade получил однозначный semantic request, но первый внутренний provider call структурно отклонён | Facade исправляет вызов внутри себя; Task Composer получает только готовый result либо operational unavailability |
| Caller пытается сам применить методику Explainer или передать готовый strategic draft | Не читать provider contract; передать facade только semantic request без leaked framing |
| Create вернул unknown outcome | Сначала найти/read-back возможный объект, не retry вслепую |
| Ошибка после создания части Epic | Перечислить confirmed/not-created scope; не удалять автоматически |
| Описание требует положить token на server | Указать credential reference и target без secret value |
| Создать одну Task и сразу выполнить | Передать в ShipTask create-and-deliver, не выполнять planning-only flow |

Blind forward test получает user requirements, live Task Manager catalog и
candidate duplicates без intended decomposition. Проверяется сохранность
meaning, исполнимость, strategic continuity, graph correctness, write authority
attachment mapping и read-back. Отдельно выбранная child Task должна позволять
новому исполнителю восстановить её вклад и применимую планку качества без scope
expansion; bug evidence должно быть доступно на той Task, которой оно помогает.
