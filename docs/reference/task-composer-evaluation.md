# Task Composer evaluation contract

Статус: current reference, 2026-08-22.

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
- Epic problem-first, сохраняет human requirements и подготовлен с помощью
  Strategic Explainer;
- недоступный или ungrounded Strategic Explainer блокирует только Epic create,
  а не независимо допустимую single Task;
- technical specifics, acceptance criteria и evidence находятся в применимых
  подзадачах, а secret values отсутствуют;
- созданные Tasks подтверждены в `Backlog`;
- Release назначен только при однозначном current или explicit выборе, а его
  отсутствие не блокирует create;
- Labels разрешены из live catalog; отсутствующий подходящий Label даёт
  видимый gap без taxonomy mutation;
- hierarchy и relation type/direction соответствуют реальной семантике;
- duplicate search предшествует create, unknown outcome reconciles до retry;
- read-back подтверждает каждую заявленную Task Manager mutation;
- результат не назван implemented, delivered или verified product behavior.

## Regression cases

| Сценарий | Ожидаемое поведение |
|---|---|
| Один небольшой independently deliverable change | Одна Task без формального Epic |
| Outcome требует API, UI и migration с отдельной приёмкой | Один strategic Epic и independently verifiable subtasks |
| Prompt содержит два независимых outcomes | Отдельные Tasks/Epics без искусственного общего parent |
| Пользователь просит только draft | Текст сформулирован, Task Manager writes отсутствуют |
| Project неизвестен | Запрос exact Project до create |
| `Backlog` отсутствует в workflow | Create не начинается; default status не подставляется |
| Current Release неизвестен | Tasks создаются без Release, gap сообщается |
| Найден только released Release | Не добавлять без explicit confirmation |
| Подходящего Label нет | Task создаётся без Label, taxonomy gap сообщается |
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
meaning, исполнимость, graph correctness, write authority и read-back.
