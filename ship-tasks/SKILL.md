---
name: ship-tasks
description: "Доводить уже созданный и выбранный scope Tasks, Project или Release из Task Manager до проверенного terminal outcome: разрешать canonical refs через Task Manager connector, создавать обязательный workflow Goal и удерживать его активным, пока в выбранной границе есть подходящие рабочие Tasks, выполнять ready Tasks, применять лёгкий per-Task gate и периодический тщательный review-batch gate, безопасно интегрировать результаты, проводить acceptance, обновлять Task statuses с optimistic concurrency и сверять обязательные внешние эффекты. Использовать только при явном вызове $ship-tasks или явной просьбе исполнить ShipTask workflow. Работать только с Task Manager; если connector, exact scope, Goal lifecycle, acceptance, authority или обязательная capability недоступны либо неоднозначны, остановиться до мутаций с TASK CONTEXT ALARM."
---

# Ship Tasks

Доставлять выбранный Task Manager scope как один проверенный результат. Не
создавать scope из общей идеи и не использовать другой task source.

## Установить Task Manager scope

До первой мутации:

1. Вызвать `get_workspace`; проверить signed-in user,
   `capabilities.read`, нужный `capabilities.writeTasks` и status catalog.
2. Разрешить Project через `list_projects`, затем `get_project`, когда нужны
   releases, counts, access или workflow statuses.
3. Разрешить Release через `list_releases`; вызвать `get_release` и проверить
   его принадлежность Project до combined filter.
4. Вызвать `list_tasks` с exact `projectRef`, `releaseRef` и другими filters.
   Оба refs опускать только для явно выбранного all-accessible scope.
5. Для полного multi-task scope следовать `nextCursor` до `hasMore=false`.
   Первую страницу и counts не считать complete inventory.
6. Считать compact rows кандидатами. Вызвать `get_task` для каждой выбранной
   Task до reasoning об acceptance, relations, dependencies, access,
   provenance или `version`.
7. Вызывать `get_task_external_context` только когда provenance сообщает о
   таком контексте и imported comments, attachments или branch metadata
   материальны для acceptance.
8. Прочитать project instructions и определить repository/workspace,
   integration policy, allowed writes, per-Task targeted gate, review-batch
   gate/trigger, external effects, acceptance authority и evidence её решения.

Использовать только canonical refs из connector. Поле Task `version` считать
optimistic-concurrency данными, обязательными для безопасного update.

Если Task Manager tools недоступны, попросить подключить plugin через native
OAuth Connect; не просить personal token. При недостаточном write scope
попросить reconnect с task-write access.

Если connector, exact scope, acceptance, authority или integration policy
неоднозначны, остановиться до code, Git, Task Manager, ownership и external
writes. Выдать `TASK CONTEXT ALARM`: известный scope, конфликтующие факты,
проверенные sources, последний безопасный checkpoint и точное решение или
доступ, который нужен.

## Сформировать обязательный Goal

Считать явный invocation `$ship-tasks` разрешением создать один workflow Goal
для уже разрешённого scope. После exact canonical refs и complete read-only
inventory, но до code, Git, Task Manager, ownership и external writes:

1. Вызвать `get_goal`.
   Если `get_goal` или `create_goal` недоступны, выдать `TASK CONTEXT ALARM` и
   остановиться до code, Git, Task Manager, ownership и external writes.
2. Если незавершённого Goal нет, вызвать `create_goal`. Не задавать token budget
   без отдельного explicit numeric budget пользователя.
3. Продолжить существующий Goal только если его objective и done criteria
   однозначно совпадают с exact scope и terminal outcome текущего запуска.
   Иначе выдать `TASK CONTEXT ALARM`; не завершать, не блокировать и не заменять
   несовместимый Goal ради нового запуска.
4. Проверить, что Goal активен до execution. Если совместимый Goal не активен и
   model tools не могут его возобновить, запросить resume через доступный client
   control и остановить execution до подтверждения.

В Goal записать:

- objective — довести exact Tasks либо все подходящие Tasks выбранного
  Project/Release scope до проверенного terminal outcome;
- done criteria — после повторной complete inventory нет `To Do`,
  `In Progress`, `In Review`, changes-requested/rework, completion remnants и
  unresolved in-scope defects, а все completion gates skill выполнены;
- verification — current Task projection, source/integration identity,
  per-Task targeted gates, exact review-batch gate, authorized acceptance и
  обязательные external effects;
- constraints — exact scope, исключённый `Backlog`, allowed writes и запрет
  расширять scope либо authority из Goal;
- blocker — конкретную внешнюю зависимость или решение с сохранением текущего
  tool threshold для `blocked`.

Удерживать Goal активным, пока хотя бы одна Task в выбранной границе подходит
под рабочие критерии. `conflict` или пустой ready frontier не являются
completion, если остаются такие Tasks или completion remnants. Для Project,
Release или all-accessible scope перед terminal claim повторить `list_tasks` до
`hasMore=false`; новая подходящая Task в той же границе продолжает Goal. Для
явно перечисленных Task refs не расширять границу без отдельного разрешения.
Переводить Goal в `blocked` только после текущего строгого blocker threshold;
после resume продолжать тот же Goal и scope.

## Выполнить read-only preflight

1. Получить complete compact inventory. Перечитать полный detail только для
   рабочих candidates и связанных boundary Tasks, необходимых для dependencies,
   review или reconciliation.
2. Классифицировать Tasks по current status:
   - `Backlog` исключить из рабочего scope; не выполнять, не проверять как
     candidate и не изменять;
   - `To Do` считать входом новой работы после preflight;
   - `In Progress` продолжать как уже начатую работу только из coherent
     checkpoint;
   - `In Review` проверять как предъявленный candidate;
   - `Done`, `Finished`, `Canceled` и другие terminal аналоги не выполнять;
   - `Duplicate` не выполнять отдельно, но читать при review связанной Task.
   Использовать current canonical status refs и category как fallback для
   terminal display names. Один status не считать доказательством acceptance
   или результата.
3. Построить dependency-ready frontier по relations и current statuses. Task в
   `Backlog` может блокировать dependency, но не становится от этого рабочим
   candidate. Не угадывать смысл неоднозначной relation.
4. Проверить workspace, Git, branches, worktrees, uncommitted changes и
   provenance существующей работы. Сохранить пользовательские и чужие edits.
5. Проверить active run, writer ownership, claims/coordination records и уже
   выполненные external effects. Без доказанной authority оставаться observer.
6. Построить integration-conflict graph для paths, schema, API, migrations,
   generated artifacts, mutable dependencies, caches, runtime state и
   environments.
7. Определить verification/integration capacity, review WIP, `batch_target` и
   triggers дорогого review-batch gate.

Выбрать ровно одну disposition:

- `work-remains` — есть `To Do`, прошедшие или способные пройти preflight;
- `completion-remains` — есть `In Review` либо implementation/rework уже
  завершены, но result не интегрирован, не принят, не отражён в Task Manager
  или не доведён до effect;
- `resume` — есть `In Progress` с незавершённым implementation/rework, найден
  coherent checkpoint и доказана authority продолжения;
- `no-work` — после исключения `Backlog` и terminal statuses нет рабочего
  candidate; это не утверждение, что Backlog пуст;
- `conflict` — scope, owner, Task state или evidence противоречат друг другу.

Для смешанного scope применять precedence:
`conflict → completion-remains → resume → work-remains → no-work`. Это выбирает
первый stage, а не исключает остальные Tasks. После review/completion
пересчитать disposition, затем продолжить resume и только потом новую `To Do`,
если dependencies и review capacity не требуют иного порядка.
Changes-requested rework текущей review chain выполнять раньше другой
dependency-ready `In Progress`; сохранять lane до повторного review или blocker.

Для `no-work` отдельно сообщить исключённые Backlog и terminal counts, выполнить
reconciliation рабочего scope, завершить обязательный Goal только после
прохождения completion gate и остановиться. Не создавать пустой commit, не
повторять дорогой gate и не производить effect только ради отчёта.

Любая `In Review` Task означает `completion-remains`. Пока такая Task есть, не
отмечать весь plan завершённым, не объявлять completion и не завершать Goal;
выдать batch/review packet и запросить acceptance либо продолжить rework.
По умолчанию acceptance — явное решение пользователя. Применять иную заранее
заданную authority только по однозначному project contract с проверяемым
evidence; standing project authority не запрашивать повторно. Invocation,
successful checks или внешний runtime result сами по себе не равны acceptance.

## Выбрать execution topology

Default — adaptive ceiling до четырёх writable task lanes:

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

Неизвестный task class начинать не шире двух lanes. Scale up после чистого
fan-in и при свободном verification/integration/review buffer. Scale down при
новых dependencies, semantic conflict, failed aggregate check, rework или
заполненном review WIP.

Использовать serial mode для одной ready Task, связного write-critical path,
неизолируемого shared state или ограниченной review capacity. `exact workers=N`
соблюдать только по явному запросу; невозможность безопасно поддержать N
останавливает dispatch.

Для каждой concurrent writable Task использовать отдельную branch и worktree;
для non-Git работы — эквивалентно изолированную execution surface. Один writer
владеет одной active Task. Worker не пишет в integration target или чужую
surface. Один integration owner выполняет fan-in в dependency order.

Отдельно сообщать mode, ceiling, active target, sustained lanes,
ready/blocked/review counts и причины свободной capacity.

## Проверять Tasks и review batches

Для каждой Task до `In Review` выполнять быстрый targeted gate: проверить её
acceptance, changed scope, defect reproduction и дешёвые risk-relevant checks.
Не запускать полный дорогой project gate на каждую Task, если risk и project
policy допускают batching.

Периодически выполнять тщательный review-batch gate один раз для exact
интегрированного batch. Включать project-defined aggregate/full suite и только
релевантные integration, browser/e2e, migration, security, performance,
runtime/external checks. Batch identity фиксирует member refs, exact
source/integration identity и checks; изменение result аннулирует его evidence.

Запускать batch gate при достижении `batch_target`/review WIP, окончании wave
или ready frontier, перед общим external effect, acceptance либо `Done`, по
checkpoint пользователя и при final flush. High-risk/coupled Task может
обоснованно образовать batch из одного member. Если безопасных candidates
несколько, не запускать дорогой singleton gate только для удобства. При
заполненном review WIP сначала завершить batch/rework, затем продолжить dispatch.

## Обновлять Tasks безопасно

- Перед каждым `update_task` вызвать `get_task` и передать current `version`.
- Использовать status ref из `availableStatuses` Task или проверенного
  Project/Release detail.
- Не передавать `null` для `projectRef`, `releaseRef` или `dueDate`, если
  очистка поля не была явно разрешена.
- При `version_conflict` перечитать Task. Повторить update только если intent
  всё ещё применим; не перетирать unrelated newer edits.
- После write перечитать Task и проверить status, fields и новую `version`.
- Не повторять `create_task` вслепую после неизвестного outcome; сначала искать
  возможный duplicate.
- Использовать `create_task` только при явном разрешении создать отдельную
  defect Task. Invocation `$ship-tasks` само по себе этого не разрешает. Новую
  Task создавать сразу с current canonical status ref `To Do`, никогда не в
  `Backlog`; при отсутствии `To Do` остановиться до create.

Переводить `To Do` в `In Progress` только после успешного preflight. Переводить
в `In Review` только exact candidate с passing targeted gate и candidate
evidence; это provisional batch-candidate, а не completion.
После changes requested возвращать Task в `In Progress`, выполнять rework и
повторные checks, сохраняя за ней текущую lane до повторного review или blocker.
Переводить в `Done` только после passing exact batch gate, authorized
acceptance, integration и обязательных effects.
`Canceled` использовать только для подтверждённого canceled outcome.
`Duplicate` не считать success основной Task.

## Выполнять и проверять Tasks

Для каждой рабочей Task:

1. Зафиксировать canonical ref, current detail/version, status, base identity,
   acceptance и разрешённые writes.
2. По status выбрать stage: `To Do` провести через preflight и перевести в
   `In Progress`; `In Progress` продолжить из checkpoint; `In Review` не
   реализовывать заново до finding, а сразу проверять exact candidate.
3. Для `To Do` и `In Progress` реализовать или завершить минимальный целостный
   result без unrelated cleanup. Для `In Review` использовать уже предъявленный
   result.
4. Выполнить или повторить per-Task targeted gate и проверить changed scope.
5. Перед review разрешить duplicate cluster по relations `duplicate_of`:
   outgoing ведёт от duplicate к canonical Task, incoming canonical Task — ко
   всем её duplicates. Вызвать `get_task` для canonical Task и каждого её
   duplicate. Включить отличающиеся problem statements, acceptance и failure
   scenarios в checklist; при материальном provenance прочитать external
   context. Если duplicate описывает отдельную проблему, зафиксировать finding
   и запросить scope decision вместо silent closure.
6. Интегрировать targeted-verified result, сформировать candidate evidence и
   перевести Task в `In Review`, если она ещё не в этом status.
7. По trigger наполнить exact review batch, провести required independent
   review без mutation authority и выполнить batch gate.
8. Выполнить общие обязательные external effects в batch cadence и независимо
   проверить exact target; не повторять дорогой effect для каждого member.
9. Сформировать batch/review packet. Считать acceptance-ready только members с
   passing targeted gate, batch gate и полным evidence.
10. При changes requested или failed batch gate вернуть Tasks с
    недействительным evidence в `In Progress`, сохранить lanes, выполнить
    rework и targeted retest, затем проверить новый exact batch. После
    authorized acceptance перевести Task в `Done` и перечитать. При
    подтверждённом canceled outcome использовать `Canceled` по project policy.

Merge conflict, semantic conflict или aggregate regression возвращает Task в
rework. Не маскировать конфликт незапланированной правкой integration owner.

## Провести review

Сформировать компактный packet:

- batch identity, member Task identifiers и цель batch;
- summary и exact result identity;
- per-member `acceptance criterion → targeted evidence/result`;
- `duplicate scenario → covered evidence/finding` для каждого duplicate;
- targeted checks каждого member и общие batch-gate checks;
- dependency/integration picture;
- risks, limitations и gaps;
- короткий human verification path;
- recommendation: `accept`, `changes requested` или `decision required`.

После changes requested показать delta: исправленные findings, новый result
identity, повторённые checks и оставшиеся gaps.

Failed batch gate локализовать по member/dependency/shared result. Вернуть
доказанно затронутые Tasks в `In Progress`; незатронутые оставить в `In Review`
только при неизменных identity и evidence. При неясной attribution считать
evidence связанного batch недействительным и reopen все его members. После
rework повторить targeted gates затронутых Tasks и gate нового exact batch.

Task Manager connector не предоставляет append-only comments или отдельный
task-report tool. Не перезаписывать Task description журналом. Выдавать review
packet в текущем interaction и использовать Task Manager для status projection,
если project context не определил другой durable report channel.

## Ограничивать defects и recovery

- Автоматически исправлять только defect, который acceptance или project policy
  включает в exact scope.
- Для out-of-scope defect остановиться до code и Task Manager writes и запросить
  scope decision.
- Не использовать failure как разрешение на cleanup, unrelated fixes,
  destructive recovery или silent task creation.
- Если defect найден после `Done`, reopen terminal Task только по project
  policy; иначе запросить scope decision и не создавать defect Task без явной
  authority. Нормальный workflow проводит batch gate до `Done`.
- При resume перечитать Tasks и сверить их с workspace, Git, checks и external
  states. Старый report — checkpoint, не proof.
- При competing owner, unexplained drift или dirty state остановить lane. Не
  выполнять automatic reset, clean, stash, force-push, takeover или удаление
  чужой worktree/branch.

## Завершить

До completion проверить:

- zero unfinished рабочих Tasks (`To Do`, `In Progress`, `In Review`) и
  unresolved in-scope defects; `Backlog` явно исключён и не блокирует gate;
- zero unaccepted review-ready candidates;
- final review batch прошёл gate на exact final integrated result;
- duplicate-derived scenarios покрыты evidence либо вынесены как явные
  findings/scope decisions;
- accepted results присутствуют в exact integration state;
- final checks относятся к exact result;
- обязательные external effects независимо проверены;
- все рабочие и изменённые Tasks перечитаны и current statuses соответствуют
  фактам; исключённые Backlog и terminal counts показаны отдельно;
- обязательный Goal относится к exact scope и оставался активным, пока
  существовали подходящие Tasks, rework/completion remnants или unresolved
  in-scope defects;
- run/journal state reconciled, когда применим.

Перед `update_goal(status="complete")` повторить complete inventory выбранной
границы. Если найдена хотя бы одна подходящая Task или отсутствует обязательный
evidence layer, не завершать Goal: продолжить workflow либо зафиксировать
blocker по текущему tool contract. Завершать Goal последним lifecycle write
после Task и evidence reconciliation.

В финальном отчёте отдельно указать Goal identity/status, Task Manager
projection, source/integration identity, targeted и batch checks, acceptance,
external effects и gaps.
Не объявлять completion при отсутствующем evidence любого обязательного слоя.
