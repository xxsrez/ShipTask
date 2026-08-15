# Ship Tasks

Статус: current contract, 2026-08-15.

Документ описывает единственный workflow `$ship-tasks`. Исполнимый
`ship-tasks/SKILL.md` является компактной procedural-формой этой specification.

## 1. Результат и граница

Skill должен довести выбранный scope уже созданных Task Manager Tasks до одного
проверенного terminal outcome. Scope задаётся одной или несколькими Tasks,
Project либо Release и не создаётся skill из общей идеи. `Backlog` остаётся
intake-зоной вне рабочего scope ShipTask: skill не берёт такие Tasks в работу и
не меняет их status или content.

До первой мутации необходимо установить:

- exact Task refs и terminal criteria;
- полный Task detail: description, acceptance, dependencies, relations,
  lifecycle, access и current concurrency field `version`;
- Project/Release membership и boundary dependencies;
- repository/workspace, integration policy и разрешённые writes;
- per-Task targeted gate, периодический review-batch gate и их trigger policy;
- обязательные external effects и способ их независимо проверить;
- доступность `description` write для обязательного in-Task delivery report;
- acceptance authority и evidence её решения;
- execution mode, capacity, review WIP limit и batch target.

После read-only разрешения exact scope, но до code, Git, Task Manager,
ownership и external writes необходимо сформировать обязательный workflow Goal
по правилам раздела 5. Невозможность создать или продолжить такой Goal является
`TASK CONTEXT ALARM`, а не разрешением выполнять scope без Goal.

Поле Task `version` является optimistic-concurrency данными Task Manager, а не
версией skill или workflow.

Если connector, exact scope, acceptance, authority или integration policy
неоднозначны, остановиться до code, Git, Task Manager, ownership и external
writes с `TASK CONTEXT ALARM`.

## 2. Единственный task source

Task Manager является единственным authoritative task source. Не использовать
fallback provider, repository TODO list, plan, Goal, chat transcript или memory
как замену Task Manager scope.

Обязательный Goal фиксирует выполнение уже разрешённого Task Manager scope и
его критерии выхода, но не создаёт новый scope, не расширяет authority и не
подменяет current connector evidence.

Project context может уточнять Project/Release refs, repository commands,
branches, environments и completion policy, но не заменяет current Task detail.
Наличие OAuth connection не доказывает authority на конкретный Project,
Release или Task.

Если Task Manager tools недоступны, запросить подключение plugin через native
OAuth Connect. Не просить personal token. При недостаточном write scope
запросить reconnect с task-write access.

## 3. Connector workflow

### 3.1 Orientation

1. Вызвать `get_workspace` и проверить signed-in user, `capabilities.read`,
   `capabilities.writeTasks` и status catalog.
2. Разрешить названный Project через `list_projects`; вызвать `get_project`,
   когда нужны releases, counts, access или workflow statuses.
3. Разрешить Release через `list_releases`; перед combined filter вызвать
   `get_release` и проверить принадлежность выбранному Project.
4. Использовать только canonical refs из connector. Не строить refs из display
   names и не подставлять сохранённый ref без current lookup, если scope мог
   измениться.

### 3.2 Inventory и detail

1. Вызвать `list_tasks` с exact `projectRef`, `releaseRef` и другими filters.
   Оба scope refs можно опустить только для явно выбранного all-accessible
   scope.
2. Продолжать по `nextCursor`, пока `hasMore=false`, когда нужен полный Project,
   Release или другой multi-task scope. Первую страницу и counts не считать
   complete inventory.
3. По status отделить рабочие кандидаты `To Do`, `In Progress` и `In Review` от
   исключённого `Backlog` и terminal statuses. Для `Backlog` читать только
   минимальные данные, необходимые для классификации, dependency boundary и
   отчёта; не выполнять и не изменять такую Task.
4. До execution или dependency reasoning вызвать `get_task` для каждого
   рабочего кандидата.
5. Вызвать `get_task_external_context` только когда provenance сообщает о
   контексте и imported comments, attachments или branch metadata материальны
   для acceptance.
6. Перечитать связанные boundary Tasks, когда их status определяет ready
   frontier или completion.
7. При проверке Task разрешить duplicate cluster по relation type
   `duplicate_of`: исходящая relation ведёт от duplicate к canonical Task, а
   входящие relations canonical Task перечисляют её duplicates. Прочитать
   canonical Task и полный detail всех её входящих duplicates. Использовать их
   description, acceptance и материальный external context как дополнительные
   review scenarios, но не выполнять duplicates как отдельную работу.

### 3.3 Writes

- Перед каждым `update_task` вызвать `get_task` и передать current `version`.
- Использовать status ref из `availableStatuses` Task либо проверенного
  Project/Release detail.
- Не передавать `null` для `projectRef`, `releaseRef` или `dueDate`, если
  очистка поля не была явно разрешена.
- При `version_conflict` перечитать Task и повторить update только если intent
  всё ещё применим. Не перетирать unrelated newer edits.
- После write перечитать Task и проверить фактические status, fields и новую
  `version`.
- Явный invocation `$ship-tasks` разрешает создать или заменить только один
  managed delivery-report block в `description` рабочей in-scope Task. Он не
  разрешает менять исходное описание, acceptance или текст вне этого block.
- Не повторять `create_task` вслепую после неизвестного network outcome:
  сначала искать возможный duplicate.
- Использовать `create_task` только когда пользователь или project policy явно
  разрешили создать отдельную defect Task. Обычный запуск работает с уже
  созданным scope.
- Каждую явно разрешённую новую Task создавать сразу со status `To Do`,
  используя current status ref из проверенного catalog. Не создавать ShipTask
  Tasks в `Backlog`; если `To Do` недоступен, остановиться до create.

## 4. Lifecycle projection

Task Manager status category помогает интерпретации, но не заменяет evidence:

| Task Manager status | Category | ShipTask interpretation |
|---|---|---|
| `Backlog` | `backlog` | Исключённый intake. Не брать в работу, не проверять как candidate и не изменять. |
| `To Do` | `unstarted` | Единственная точка входа для новой работы; после preflight это `ready`. |
| `In Progress` | `started` | Работа уже идёт; продолжать только из coherent checkpoint и с подтверждённой authority. |
| `In Review` | `started` | Targeted-verified candidate уже предъявлен; он может ждать batch gate и acceptance. Проверять exact candidate, evidence и все связанные duplicates. |
| `Done`, `Finished` и аналоги | `completed` | Terminal projection; не создаёт работу, но может участвовать в reconciliation. |
| `Canceled` и аналоги | `canceled` | Terminal outcome; не выполнять и не считать successful completion. |
| `Duplicate` | `canceled` | Отдельной работы не требует; читать как review context связанной основной Task. |

Category используется как fallback для terminal statuses с другими display
names. Для рабочих состояний status name и его current canonical ref должны
соответствовать проверенному catalog.

Нормативная status-проекция:

```text
Backlog                         (excluded; no ShipTask transition)
To Do → In Progress → In Review → Done
                         └──────→ Canceled
Duplicate                       (terminal review context, no own execution)
```

Нормативный task flow:

```text
planned
→ ready
→ running
→ task-verified
→ In Review / batch-candidate
→ batch-verified / acceptance-ready
→ authorized-accepted
→ terminal
```

Возврат на доработку:

```text
In Review / batch-candidate
→ changes-requested
→ rework
→ task-verified
→ In Review / batch-candidate
```

При changes requested вернуть Task из `In Review` в `In Progress`, выполнить
rework и только после повторных checks снова перевести в `In Review`. При
ограниченной capacity сохранять lane за этой review/rework chain до повторного
review или blocker; не переключаться на другую `In Progress` только из-за
смены status.
Переводить `To Do` в `In Progress` только после успешного preflight и получения
write authority. Переводить в `In Review` только exact candidate с passing
targeted gate и candidate evidence. Переводить в `Done` только после passing
review-batch gate, актуального in-Task delivery report, task acceptance,
integration и обязательных effects.
`Canceled` использовать только при подтверждённом canceled outcome. Один status
никогда не доказывает другой evidence layer.

## 5. Goal lifecycle и preflight disposition

### 5.1 Обязательный Goal

Явный вызов `$ship-tasks` или явная просьба исполнить ShipTask workflow
разрешает создание одного workflow Goal для выбранного scope. После разрешения
exact canonical refs и complete read-only inventory, но до первой non-Goal
mutation:

1. Проверить доступность `get_goal` и `create_goal`. При отсутствии обязательной
   Goal capability остановиться с `TASK CONTEXT ALARM` до любых non-Goal
   mutations. Вызвать `get_goal` и проверить current model-visible Goal state.
2. Если незавершённого Goal нет, вызвать `create_goal` без token budget, если
   пользователь отдельно не указал положительный numeric budget.
3. Если уже существует незавершённый Goal, продолжить его только когда его
   objective и done criteria однозначно относятся к тому же exact scope и
   terminal outcome. Иначе остановиться с `TASK CONTEXT ALARM`; не завершать,
   не блокировать и не заменять чужой или несовместимый Goal ради запуска.
4. После создания или reuse проверить, что Goal активен до execution. Если
   совместимый Goal существует, но не активен и его нельзя возобновить текущим
   tool contract, запросить resume через доступный client control и остановить
   execution до подтверждения.

Goal должен содержать:

- `Objective`: довести exact выбранные Tasks либо текущие подходящие Tasks
  выбранного Project/Release scope до проверенного terminal outcome;
- `Done when`: повторная complete inventory не находит `To Do`, `In Progress`,
  `In Review`, changes-requested/rework, completion remnants или unresolved
  in-scope defects, все delivery reports актуальны и требования раздела 11
  выполнены;
- `Verify with`: current Task details/statuses, source/integration identity,
  per-Task targeted gates, exact review-batch gate, authorized acceptance и
  independently verified external effects;
- `Constraints`: точная граница scope, исключённый `Backlog`, разрешённые writes
  и запрет расширять scope либо authority из самого Goal;
- `Blocked when`: конкретная внешняя зависимость или решение, без ослабления
  текущего tool threshold для статуса `blocked`.

Goal остаётся активным, пока хотя бы одна Task в выбранной границе подходит под
рабочие критерии ShipTask. `Backlog` и terminal statuses сами по себе не держат
Goal активным, но могут оставаться dependency boundary. `conflict` или
временное отсутствие ready frontier не являются completion и не разрешают
закрыть Goal, если подходящие Tasks либо completion remnants ещё существуют.
Статус `blocked` допустим только после текущего строгого blocker threshold; он
оставляет Goal незавершённым, а после resume workflow продолжается с тем же
Goal и scope.

Для явно перечисленных Task refs граница фиксирована этими refs и отдельно
разрешёнными in-scope defects. Для Project, Release или all-accessible scope
перед terminal claim повторить `list_tasks` по всем страницам до
`hasMore=false`: новая или изменившая status Task внутри той же границы должна
удерживать Goal активным, если она теперь подходит под рабочие критерии.

### 5.2 Preflight disposition

До execution выбрать ровно одну disposition:

| Disposition | Значение |
|---|---|
| `work-remains` | Есть `To Do` Tasks, прошедшие или способные пройти preflight. |
| `completion-remains` | Есть `In Review` либо implementation/rework уже завершены, но result не интегрирован, не принят, не отражён в Task Manager или не доведён до обязательного effect. |
| `resume` | Есть `In Progress` с незавершённым implementation/rework, найден coherent checkpoint и доказана authority продолжения. |
| `no-work` | После исключения `Backlog` и terminal statuses нет рабочего candidate; это не утверждение, что Backlog пуст. |
| `conflict` | Scope, owner, Task state или evidence противоречат друг другу. |

Для смешанного scope выбирать disposition по precedence:
`conflict → completion-remains → resume → work-remains → no-work`. Это задаёт
первый безопасный stage, а не исключает остальные Tasks: после review/completion
пересчитать disposition, затем продолжить resume и только потом dispatch новой
`To Do`, если dependencies и review capacity не требуют иного порядка.
Changes-requested rework текущей review chain имеет приоритет среди
dependency-ready `In Progress`; при blocker пересчитать disposition.

Для `no-work` сообщить отдельно исключённые Backlog и terminal counts, выполнить
reconciliation применимого рабочего scope, завершить обязательный Goal только
после прохождения completion gate и остановиться. Не создавать пустой commit,
не повторять дорогой gate и не производить effect только ради свежего отчёта.

### 5.3 Terminal invariant и acceptance authority

Любая `In Review` Task означает `completion-remains`. Пока в exact scope есть
хотя бы одна такая Task, запрещено отмечать весь execution plan завершённым,
объявлять terminal completion или завершать Goal. Допустимый handoff в этом
состоянии — batch/review packet, запрос acceptance либо точное описание
оставшегося blocker.

По умолчанию acceptance является явным решением пользователя по предъявленному
exact result. Project context может заранее определить другую acceptance
authority или автоматический acceptance contract, но только с однозначными
критериями и проверяемым evidence. Standing authority, уже явно записанную в
current project context, не запрашивать повторно. Сам invocation `$ship-tasks`,
успешные checks, deployment или внешний runtime check не являются acceptance,
если project context прямо не определил обратное.

## 6. Execution topology

Default mode — adaptive execution с ceiling до четырёх writable task lanes.
Фактический target вычисляется для каждой execution wave:

```text
active_write_target = min(
  worker_ceiling,
  dependency_ready_width,
  conflict_free_width,
  isolated_task_capacity,
  verification_capacity,
  integration_headroom,
  review_headroom
)
```

Неизвестный task class начинать не шире двух lanes. Увеличивать target после
чистого fan-in и при свободном verification/integration/review buffer.
Уменьшать при новых dependencies, semantic conflict, failed aggregate check,
rework или заполненном review WIP.

`serial` mode использовать для одной ready Task, связного write-critical path,
неизолируемого shared state или ограниченной review capacity. `exact workers=N`
использовать только по явному запросу; невозможность безопасно поддержать N
останавливает dispatch.

Отдельно сообщать execution mode, ceiling, active target, sustained lanes,
ready/blocked/review counts и причины свободной capacity.

### 6.1 Двухуровневая verification

Использовать два уровня проверки:

1. **Per-Task targeted gate** — обязательная быстрая проверка каждой Task до
   включения в review batch: acceptance-specific tests, changed-scope checks,
   воспроизведение исправляемого defect и дешёвые static/build checks, когда они
   материальны. Не запускать полный дорогой project gate для каждой Task, если
   риск и project policy допускают batching.
2. **Review-batch gate** — периодическая тщательная проверка exact
   интегрированного batch: project-defined aggregate/full suite, integration и
   risk-relevant browser/e2e, migration, security, performance, runtime либо
   external checks. Выполнять каждый дорогой check один раз для точной batch
   identity, а не повторять его для каждого member.

На preflight определить `batch_target`, review WIP limit, дорогие checks и
trigger policy. Размер не фиксировать глобально: учитывать dependency fan-in,
конфликтность, риск, длительность gate и review capacity. Если доступно
несколько безопасных кандидатов, не запускать дорогой gate на singleton только
для удобства.

Запускать review-batch gate, когда выполнено хотя бы одно условие:

- достигнут batch target или заполнен review WIP;
- закончилась execution wave либо больше нет готовых Tasks для наполнения
  batch;
- high-risk/coupled change требует раннего gate, включая обоснованный batch из
  одной Task;
- предстоит общий external effect, acceptance или перевод members в `Done`;
- пользователь запросил checkpoint;
- выполняется final flush перед completion.

Batch identity включает member Task refs, exact source/integration identity и
набор проверок. Любое изменение integrated result после passing batch gate
аннулирует относящееся к нему evidence и требует нового gate перед acceptance.
При заполненном review WIP сначала завершить batch/rework, а не продолжать
dispatch новых Tasks.

## 7. Isolation и integration

Для каждой concurrent writable Task использовать отдельную task branch и
worktree. Для non-Git работы требуется эквивалентно изолированная execution
surface.

Инварианты:

- одна active Task и один writer на execution surface;
- branch/worktree привязаны к canonical Task ref;
- worker не пишет в integration target или чужую branch;
- shared schema, generated artifacts, mutable dependencies, caches, runtime
  state и environments либо изолированы, либо делают Tasks конфликтующими;
- reviewer/support role не получает mutation authority;
- один integration owner выполняет fan-in в dependency order;
- после merge повторяются affected targeted checks; aggregate/full checks
  выполняются review-batch gate на exact integrated result.

Merge conflict, semantic conflict или aggregate regression возвращает Task в
rework. Не маскировать конфликт незапланированной правкой integration owner.

## 8. Task execution

Для каждой рабочей Task:

1. Зафиксировать canonical Task ref, current detail/version, status, base
   identity, acceptance и разрешённые writes.
2. По status выбрать stage: `To Do` провести через preflight и перевести в
   `In Progress`; `In Progress` продолжить из проверенного checkpoint;
   `In Review` не реализовывать заново до finding, а сразу проверять exact
   candidate.
3. Для `To Do` и `In Progress` реализовать или завершить минимальный целостный
   result без unrelated cleanup. Для `In Review` использовать уже предъявленный
   result.
4. Выполнить или повторить per-Task targeted gate и проверить changed scope.
5. Перед review прочитать все связанные duplicate Tasks и включить их
   отличающиеся problem statements, acceptance и failure scenarios в checklist.
   Если duplicate описывает материально отдельную проблему, зафиксировать
   finding и запросить scope decision вместо silent closure.
6. Интегрировать targeted-verified result, сформировать candidate evidence и
   обновить Task в `In Review`, если она ещё не в этом status. Это provisional
   review-ready state, а не terminal completion.
7. Наполнить review batch до trigger из раздела 6.1. Провести independent agent
   review без mutation authority, когда его требует risk class или project
   policy, и выполнить review-batch gate на exact integrated result.
8. Выполнить общие обязательные external effects в batch cadence и независимо
   проверить exact target; не повторять один дорогой effect для каждого member.
9. Сформировать batch/review packet и записать task-specific delivery report в
   каждую Task с passing targeted gate, batch gate и полным evidence. Только
   после post-write read-back такой member становится acceptance-ready.
10. При changes requested либо failed batch gate вернуть Tasks, чьё evidence
    стало недействительным, из `In Review` в `In Progress` и записать в них
    понятный rework/incident report; по возможности объединить оба изменения в
    один optimistic update. Сохранить текущие lanes, выполнить rework и targeted
    retest, затем собрать и проверить новый exact batch. После authorized
    acceptance финализировать report, обновить Task в `Done` одним write и
    перечитать. При подтверждённом canceled outcome записать terminal report и
    завершить через `Canceled` по project policy.

Разделять Task Manager state, source result, checks, authorized acceptance и
external effects. Успех одного слоя не доказывает остальные.

## 9. Review и reports

Batch/review packet должен содержать:

- batch identity, member Task identifiers и цель batch;
- summary изменений и exact result identity;
- per-member `acceptance criterion → targeted evidence/result`;
- `duplicate scenario → covered evidence/finding` для каждого связанного
  duplicate;
- targeted checks каждого member и общие batch-gate checks;
- dependency/integration picture;
- risks, limitations и unresolved gaps;
- короткий human verification path;
- recommendation: `accept`, `changes requested` или `decision required`.

После changes requested показывать delta: исправленные findings, новый result
identity, повторённые checks и оставшиеся gaps.

Failed batch gate сначала локализовать по member, dependency и shared result:

- доказанно затронутые Tasks вернуть в `In Progress` и исправить в текущем
  scope;
- доказанно незатронутые Tasks можно оставить в `In Review`, только если их
  result identity и evidence не изменились;
- при неясной attribution считать evidence всего связанного batch
  недействительным и вернуть его members в `In Progress`;
- после rework повторить targeted gates затронутых Tasks и новый batch gate на
  exact integrated result.

Если defect обнаружен уже после `Done`, не переписывать terminal history
молча: reopen terminal Task только когда это разрешает project policy, иначе
запросить scope decision и создавать отдельную defect Task лишь при явной
authority. Нормальный workflow обязан провести batch gate до `Done`.

### 9.1 In-Task delivery report

Connector не предоставляет append-only comments или отдельный task-report
tool, но current `update_task` умеет менять `description` вместе со status.
Использовать это только для одного видимого managed delivery-report block по
[runtime format](../../ship-tasks/references/delivery-report.md), а не как
append-only execution journal.

До каждого report write перечитать Task и current `version`. Исходный
user-authored description сохранить byte-for-byte вне sentinel lines. Если
block отсутствует, добавить его в конец; если ровно один существует — заменить
его целиком; при нескольких/повреждённых markers либо block для другого Task
ref остановиться с `TASK CONTEXT ALARM`. После write перечитать Task и проверить
description, status и новую `version`. Не обрезать исходный текст ради field
limit и не считать report записанным по одному успешному response.

Report lifecycle:

- после passing batch gate записать `ACCEPTANCE READY` report до запроса
  acceptance;
- при material failure, который инвалидирует candidate, до/вместе с reopen
  записать `REWORK REQUIRED` либо `BLOCKED` report;
- после rework заменить тот же block delta-report, не добавлять новую копию;
- после authorized acceptance финализировать `COMPLETED` report и по
  возможности одним `update_task` перевести Task в `Done`;
- перед `Canceled` записать terminal report с причиной и последствиями;
- не backfill-ить pre-existing terminal Tasks и не писать отдельный report в
  `Duplicate`, если это не было отдельно разрешено.

Report является task-specific: общий batch evidence кратко отразить в каждом
member, но не копировать полный batch log. Если обязательный report нельзя
безопасно записать или прочитать обратно, Task остаётся `completion-remains`,
переход в `Done` и Goal completion запрещены.

### 9.2 Человекочитаемый формат

Начинать с результата и пользовательского эффекта, затем объяснять реализацию,
поведение, evidence, ограничения и требуемое решение. Масштабировать глубину по
сложности и риску; не превращать простой change в формальный postmortem и не
вставлять raw logs, огромные file lists или декоративные схемы.

Для non-trivial feature, cross-component change либо material incident включать
одну-две plain-text диаграммы, которые объясняют runtime/data flow, changed
boundary, lifecycle или causal chain. Для локального тривиального изменения
использовать компактный before/after вместо бесполезной диаграммы. Пока Task
Manager не рендерит rich text, не выдавать Mermaid/Markdown source за готовую
визуализацию.

При success report должен объяснять: что получил пользователь, как проходит
основной flow, что и почему изменено, как это проверено и какие ограничения
остались. При material failure добавить: наблюдаемый симптом/impact, detection,
trigger, root cause с confidence, recovery/rework, prevention и remaining risk.
Писать blameless, отделять evidence от inference и не создавать follow-up Tasks
без отдельной authority. Обычный red/green test внутри implementation не
является material incident сам по себе.

## 10. Defects и recovery

- Автоматически исправлять только defect, который acceptance или project policy
  включает в exact scope.
- Для нового out-of-scope defect остановиться до code и scope-changing Task
  Manager writes; разрешён только managed `BLOCKED`/`decision required` report
  текущей in-scope Task. Запросить scope decision.
- Не использовать failure как разрешение на cleanup, unrelated fixes,
  destructive recovery или silent task creation.
- При resume перечитать Tasks и сверить их с workspace, Git, checks и external
  states. Старый report является checkpoint, но не proof.
- При competing owner, unexplained drift или dirty state остановить затронутую
  lane. Не выполнять automatic reset, clean, stash, force-push, takeover или
  удаление чужой worktree/branch.

## 11. Completion

Completion требует:

- zero unfinished рабочих Tasks (`To Do`, `In Progress`, `In Review`) и
  unresolved in-scope defects; Backlog явно исключён и не блокирует этот gate;
- zero unaccepted review-ready candidates;
- final review batch прошёл gate на exact final integrated result;
- все duplicate-derived scenarios покрыты evidence либо вынесены как явные
  findings/scope decisions;
- accepted results присутствуют в exact integration state;
- final project checks относятся к exact result;
- обязательные external effects независимо проверены;
- каждая выполненная или materially failed рабочая Task содержит один
  актуальный, прочитанный обратно delivery-report block для exact result/state;
- все рабочие и изменённые Tasks перечитаны и их current statuses соответствуют
  фактам; исключённые Backlog и terminal counts отражены отдельно;
- обязательный Goal относится к exact scope и оставался активным, пока
  существовали подходящие Tasks, rework/completion remnants или unresolved
  in-scope defects;
- run/journal state reconciled, когда он применим.

Перед `update_goal(status="complete")` повторить complete inventory выбранной
границы и проверить все пункты completion. Если хотя бы одна Task подходит под
рабочие критерии либо отсутствует обязательный evidence layer, не завершать
Goal: продолжить workflow или зафиксировать blocker по текущему tool contract.
Goal completion является последним lifecycle write после Task и evidence
reconciliation, а не заменой этой проверки.

Финальный interaction report отдельно показывает Goal identity/status, Task
Manager projection, source/integration identity, checks, acceptance, external
effects, gaps и результат in-Task report writes. Он не заменяет reports внутри
Tasks.

## 12. Non-goals

- Не превращать идею или specification в новый task scope без отдельной
  planning-команды.
- Не использовать другой task provider или generic fallback.
- Не изображать comments, durable claims, background scheduler, Project/Release
  administration или bulk mutation существующими connector capabilities.
- Не максимизировать agent count без dependency, isolation, integration и
  review capacity.
- Не считать Task status, plan, worker report, commit, check или deployment
  достаточным evidence другого слоя.
