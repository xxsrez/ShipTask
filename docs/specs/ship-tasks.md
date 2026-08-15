# Ship Tasks

Статус: current contract, 2026-08-16.

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
- exact release targets, их verified environment class и recovery/smoke policy;
- disposition native Task comment capability для optional in-Task delivery
  report: `available` либо `not-available`;
- acceptance authority и evidence её решения;
- execution mode, capacity, review WIP limit и batch target.

После read-only разрешения exact scope, но до code, Git, Task Manager,
ownership и external writes необходимо сформировать обязательный workflow Goal
по правилам раздела 5. Невозможность создать или продолжить такой Goal является
`TASK CONTEXT ALARM`, а не разрешением выполнять scope без Goal.

Поле Task `version` является optimistic-concurrency данными Task Manager, а не
версией skill или workflow.

Если connector, exact scope, Goal, ownership, integration/shared state или
authority неоднозначны так, что любая оставшаяся мутация небезопасна,
остановиться с global `TASK CONTEXT ALARM`. Изолированную неопределённость одной
Task обрабатывать как `deferred` по разделу 5.4 и продолжать остальные.

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
- Явный invocation `$ship-tasks` не разрешает менять `description` ради report.
  Delivery report можно создать только через доступный native Task comment
  write; другие Task fields не являются fallback.
- Тот же invocation разрешает task-specific delivery-report comment только для
  рабочей in-scope Task и только по contract раздела 9.1. Он не разрешает
  произвольные comments или writes в unrelated/duplicate/terminal Tasks.
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
review-batch gate, task acceptance, integration и обязательных effects. Report
comment публиковать при доступной native comments capability, но его отсутствие
или failed/unsupported comment write само по себе не блокирует `Done`.
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
  in-scope defects, нет deferred decision/authority queue, report-comment
  disposition честно классифицирован для изменённых Tasks и требования раздела
  11 выполнены;
- `Verify with`: current Task details/statuses, source/integration identity,
  per-Task targeted gates, exact review-batch gate, authorized acceptance и
  independently verified external effects;
- `Constraints`: точная граница scope, исключённый `Backlog`, разрешённые writes
  и запрет расширять scope либо authority из самого Goal;
- `Blocked when`: после исчерпания runnable work остаётся конкретная
  decision/authority queue либо общая внешняя зависимость, без ослабления
  текущего tool threshold для статуса `blocked`.

Goal остаётся активным, пока хотя бы одна Task в выбранной границе подходит под
рабочие критерии ShipTask. `Backlog` и terminal statuses сами по себе не держат
Goal активным, но могут оставаться dependency boundary. `global-conflict`,
`deferred` или временное отсутствие ready frontier не являются completion и не
разрешают закрыть Goal, если подходящие Tasks либо completion remnants ещё
существуют.
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
| `deferred` | Конкретная Task безопасно изолирована, но требует material decision, отсутствующей authority либо внешнего state change; в текущем run её не переизбирать без нового evidence. |
| `no-work` | После исключения `Backlog` и terminal statuses нет рабочего candidate; это не утверждение, что Backlog пуст. |
| `global-conflict` | Scope, Goal, owner, shared state или evidence противоречат друг другу так, что любая оставшаяся мутация небезопасна. |

Для смешанного scope выбирать disposition по precedence:
`global-conflict → actionable completion-remains → resume → work-remains →
deferred-only → no-work`. Это задаёт первый безопасный stage, а не исключает
остальные Tasks. Acceptance/decision-waiting `In Review` сначала перевести в
`deferred`, затем продолжить actionable review, resume и новую `To Do` работу.
Changes-requested rework текущей review chain имеет приоритет среди
dependency-ready `In Progress`; при task-local blocker defer-нуть lane,
освободить capacity и пересчитать disposition.

Для `no-work` сообщить отдельно исключённые Backlog и terminal counts, выполнить
reconciliation применимого рабочего scope, завершить обязательный Goal только
после прохождения completion gate и остановиться. Не создавать пустой commit,
не повторять дорогой gate и не производить effect только ради свежего отчёта.

### 5.3 Terminal invariant и acceptance authority

Любая `In Review` Task означает `completion-remains`. Пока в exact scope есть
хотя бы одна такая Task, запрещено отмечать весь execution plan завершённым,
объявлять terminal completion или завершать Goal. Допустимый handoff в этом
состоянии — batch/review packet, verified acceptance либо `deferred` с точным
описанием оставшегося decision/authority blocker.

По умолчанию acceptance является явным решением пользователя по предъявленному
exact result. Project context может заранее определить другую acceptance
authority или автоматический acceptance contract, но только с однозначными
критериями и проверяемым evidence. Standing authority, уже явно записанную в
current project context, не запрашивать повторно. Сам invocation `$ship-tasks`,
успешные checks, deployment или внешний runtime check не являются acceptance,
если project context прямо не определил обратное.

Если acceptance требует нового решения пользователя, не запрашивать его, пока
остаётся другая runnable Task. Оставить candidate в `In Review`, добавить его в
decision queue, при доступных comments обязательно опубликовать `BLOCKED`
handoff и продолжить scope. Когда runnable queue исчерпана, предъявить все такие
решения одним consolidated request.

### 5.4 Autonomous continuation и task-local defer

Следовать [runtime reference](../../ship-tasks/references/autonomy-and-release.md)
и [ADR-0004](../decisions/0004-autonomous-continuation-and-release-authority.md).
Во время long-running scope не прерывать runnable queue task-local вопросами.

Decision ladder:

1. Выбрать и выполнить разумный default, если он обратим, локален, остаётся
   внутри exact scope/acceptance, имеет ограниченный blast radius и не касается
   production, secrets, privacy, существенных расходов либо необратимого
   external effect. Зафиксировать rationale в evidence/report.
2. Если решение materially меняет продуктовый outcome, требует отсутствующей
   authority или остаётся неоднозначным после bounded research, defer-нуть
   только affected Task. Не угадывать, не отменять её и не создавать новую.
3. Остановить весь run с `TASK CONTEXT ALARM` только при global/shared conflict,
   который делает небезопасной любую оставшуюся mutation.

Deferred Task сохраняет truthful status: `To Do`, если execution не начинался;
`In Progress`, если существует partial/rework result; `In Review`, если exact
candidate machine-verified, но ждёт acceptance или production approval. Не
переводить её в `Done`/`Canceled` и не изобретать portable `Blocked` status.

В current run вести decision queue с canonical Task ref, reason, last safe
checkpoint, уже выполненными actions/evidence, recommended default, точным
decision/authority и resume step. Не переизбирать Task без нового evidence,
authority или external state change. При доступной native comments capability
обязательно опубликовать тот же `BLOCKED` handoff в Task; при отсутствии
comments скипнуть write без изменения `description`.

Когда runnable Tasks остаются, продолжать их без вопроса пользователю. Когда
остались только deferred Tasks, предъявить одну consolidated decision queue.
Goal и plan остаются незавершёнными; Goal `blocked` разрешён только после
текущего строгого tool threshold, а не из-за первого defer.

### 5.5 Environment и release authority

Классифицировать exact release target по project instructions, config и current
provider state. Название Task Manager `Release`, URL или прежний deploy сами по
себе не доказывают environment class.

Invocation `$ship-tasks` является standing authority для обычного in-scope
non-production release workflow в local/development/test/QA/UAT/staging/preview/
sandbox environment: build/package, deploy/redeploy, required non-production
migration, smoke, bounded diagnosis и repair/rollback. Не запрашивать отдельное
подтверждение для этих шагов. Если non-production release временно нарушил
in-scope surface, диагностировать и восстановить/исправить его в том же scope.

Production release выполнять только после явного user approval для production
target. Не выводить approval из Task/Release title, acceptance, Goal, checks,
project automation, прошлого approval или самого invocation. Без approval
выполнить безопасную preparation, release и verification на non-production,
затем оставить Task в truthful non-terminal status, defer-нуть её с reason
`production-approval-required`, при доступных comments обязательно записать
`BLOCKED` report и продолжить остальные Tasks. Не задавать production-вопрос
пока есть runnable work.

Если target нельзя надёжно классифицировать как non-production, считать его
production-like и defer-нуть Task. Standing non-production authority не
разрешает unrelated cleanup, permanent deletion, destructive durable-data
reset, secrets exposure/rotation, неограниченные расходы или нарушение explicit
read-only boundary. Deployment не заменяет acceptance и independent smoke.

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
   identity, acceptance, exact release target/environment class и разрешённые
   writes.
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
   finding, defer-нуть affected Task для scope decision и продолжить
   независимые Tasks вместо interrupting question или silent closure.
6. Интегрировать targeted-verified result, сформировать candidate evidence и
   обновить Task в `In Review`, если она ещё не в этом status. Это provisional
   review-ready state, а не terminal completion.
7. Наполнить review batch до trigger из раздела 6.1. Провести independent agent
   review без mutation authority, когда его требует risk class или project
   policy, и выполнить review-batch gate на exact integrated result.
8. Выполнить общие обязательные external effects в batch cadence и независимо
   проверить exact target. Non-production release выполнить без confirmation по
   разделу 5.5; production без explicit approval defer-нуть. Не повторять один
   дорогой effect для каждого member.
9. Сформировать batch/review packet. Если current connector предоставляет
   native Task comment write, опубликовать task-specific acceptance-ready
   report там, когда это полезный review surface. Если capability отсутствует
   или ещё неработоспособна, классифицировать шаг как `not-available` и
   продолжить без Task field fallback. Если Task ждёт acceptance/decision,
   defer-нуть её и продолжить runnable queue без вопроса пользователю.
10. При changes requested либо failed batch gate вернуть Tasks, чьё evidence
    стало недействительным, из `In Review` в `In Progress`. При доступной native
    comments capability опубликовать понятный rework/incident comment; иначе
    скипнуть только report step. Сохранить текущие lanes, выполнить rework и
    targeted retest, затем собрать и проверить новый exact batch. После
    authorized acceptance опубликовать final report comment, если capability
    доступна, независимо обновить Task в `Done` и перечитать. Аналогично
    обработать подтверждённый `Canceled` outcome.

При любом task-local blocker сохранить last safe checkpoint, truthful status и
decision queue entry; при доступных comments обязательно опубликовать `BLOCKED`
report. Освободить lane и продолжить другие dependency-ready Tasks. Не
переизбирать deferred Task без нового evidence/authority/state change.

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
defer-нуть affected route для consolidated scope decision и создавать отдельную
defect Task лишь при явной authority. Нормальный workflow обязан провести batch
gate до `Done`.

### 9.1 Delivery report как Task comment

Следовать [runtime format](../../ship-tasks/references/delivery-report.md) и
[ADR-0003](../decisions/0003-delivery-reports-as-task-comments.md). На каждом
запуске проверить current Task Manager tool contract:

1. `available` — connector явно предоставляет native comment-create operation
   для canonical Task ref и текущая authority позволяет её вызвать;
2. `not-available` — operation отсутствует, не поддерживается фактическим
   connector, не разрешена текущей authority либо сообщает, что feature ещё не
   доступна.

Imported comments из `get_task_external_context` являются read-only provenance
и не доказывают native comment write. Не выводить capability из roadmap, версии
или прошлой сессии. Никогда не записывать report в `description`, acceptance,
status text или другой Task field как fallback.

При `not-available` скипнуть report write, сохранить report в review/interaction
output и продолжить основной workflow. Этот gap сам по себе не вызывает
`TASK CONTEXT ALARM`, не создаёт `completion-remains` и не блокирует `Done` или
Goal completion. Если advertised write завершился ошибкой либо outcome
неизвестен, не повторять его вслепую; показать `not-available` или
`write-outcome-unknown` с причиной и также не блокировать terminal workflow.

Когда capability `available`:

- опубликовать `COMPLETED` report при terminal completion каждой изменённой
  рабочей Task;
- опубликовать `REWORK REQUIRED`/`BLOCKED` report при material failure,
  changes-requested или blocker, который важно объяснить пользователю;
- при каждом task-local defer обязательно опубликовать `BLOCKED` handoff с
  reason, last safe checkpoint, completed evidence, recommended default,
  required decision/authority и resume step;
- при необходимости опубликовать `ACCEPTANCE READY` report как review surface,
  но не комментировать обычные внутренние red/green iterations;
- перед write при доступной comment list/read capability проверить, нет ли уже
  report для того же `Task + state + exact result`; после write выполнить
  read-back, если connector его поддерживает;
- при unknown outcome не делать blind retry и не заявлять `published`;
- не backfill-ить pre-existing terminal Tasks и не писать отдельный report в
  `Duplicate` без explicit authority.

Report остаётся task-specific: shared batch evidence кратко отразить в каждом
member, но не копировать полный batch log. Comment write и status update считать
разными side effects и reconciliate независимо, пока connector не гарантирует
их атомарность.

### 9.2 Человекочитаемый формат

Начинать с результата и пользовательского эффекта, затем объяснять реализацию,
поведение, evidence, ограничения и требуемое решение. Масштабировать глубину по
сложности и риску; не превращать простой change в формальный postmortem и не
вставлять raw logs, огромные file lists или декоративные схемы.

Для non-trivial feature, cross-component change либо material incident включать
одну-две диаграммы, которые объясняют runtime/data flow, changed boundary,
lifecycle или causal chain. Для локального тривиального изменения использовать
compact before/after вместо бесполезной диаграммы. Формат выбирать по
доказанному comment renderer contract: plain text работает как baseline;
Mermaid не выдавать за rendered diagram без подтверждённой поддержки.

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
- Для нового out-of-scope defect не выполнять code или scope-changing Task
  Manager writes. Если finding блокирует текущую Task, defer-нуть только её,
  при доступных comments обязательно опубликовать `BLOCKED`/`decision required`
  report и продолжить независимые Tasks. Включить решение в consolidated queue.
- Не использовать failure как разрешение на cleanup, unrelated fixes,
  destructive recovery или silent task creation.
- При resume перечитать Tasks и сверить их с workspace, Git, checks и external
  states. Старый report comment является checkpoint, но не proof.
- При competing owner, unexplained drift или dirty state остановить затронутую
  lane, defer-нуть affected Task и продолжить изолированные lanes, если shared
  state остаётся безопасным. Не выполнять automatic reset, clean, stash,
  force-push, takeover или удаление чужой worktree/branch.

## 11. Completion

Completion требует:

- zero unfinished рабочих Tasks (`To Do`, `In Progress`, `In Review`) и
  unresolved in-scope defects; Backlog явно исключён и не блокирует этот gate;
- zero unaccepted review-ready candidates;
- zero deferred Tasks и unresolved decision/authority entries;
- final review batch прошёл gate на exact final integrated result;
- все duplicate-derived scenarios покрыты evidence либо вынесены как явные
  findings/scope decisions;
- accepted results присутствуют в exact integration state;
- final project checks относятся к exact result;
- обязательные external effects независимо проверены;
- для каждой изменённой или materially failed рабочей Task report-comment
  disposition отражён как `published`, `not-available` или
  `write-outcome-unknown`; отсутствие comment capability не является evidence
  gap основного результата;
- все рабочие и изменённые Tasks перечитаны и их current statuses соответствуют
  фактам; исключённые Backlog и terminal counts отражены отдельно;
- обязательный Goal относится к exact scope и оставался активным, пока
  существовали подходящие Tasks, rework/completion remnants или unresolved
  in-scope defects;
- run/journal state reconciled, когда он применим.

Перед `update_goal(status="complete")` повторить complete inventory выбранной
границы и проверить все пункты completion. Если хотя бы одна Task подходит под
рабочие критерии, остаётся deferred/decision queue либо отсутствует обязательный
evidence layer, не завершать Goal: продолжить runnable workflow или, когда
runnable work исчерпан, предъявить consolidated queue. Goal `blocked` применять
только по текущему строгому tool threshold.
Goal completion является последним lifecycle write после Task и evidence
reconciliation, а не заменой этой проверки.

Финальный interaction report отдельно показывает Goal identity/status, Task
Manager projection, source/integration identity, checks, acceptance, external
effects, gaps и disposition Task comment reports. Он не выдаёт скипнутые или
unknown writes за опубликованные comments и отдельно показывает deferred Tasks,
их last safe checkpoints и exact decisions/authority needed.

## 12. Non-goals

- Не превращать идею или specification в новый task scope без отдельной
  planning-команды.
- Не использовать другой task provider или generic fallback.
- Не изображать comments, durable claims, background scheduler, Project/Release
  administration или bulk mutation существующими connector capabilities и не
  использовать `description` как fallback для отсутствующих comments.
- Не максимизировать agent count без dependency, isolation, integration и
  review capacity.
- Не считать Task status, plan, worker report, commit, check или deployment
  достаточным evidence другого слоя.
- Не выполнять production release без explicit user approval и не применять
  production-style confirmation к ordinary verified non-production release.
- Не использовать standing non-production authority для destructive,
  secret-related, unrelated или explicitly read-only actions.
