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
- targeted, integration и aggregate checks;
- обязательные external effects и способ их независимо проверить;
- human acceptance authority;
- execution mode, capacity и review WIP limit.

Поле Task `version` является optimistic-concurrency данными Task Manager, а не
версией skill или workflow.

Если connector, exact scope, acceptance, authority или integration policy
неоднозначны, остановиться до code, Git, Task Manager, ownership и external
writes с `TASK CONTEXT ALARM`.

## 2. Единственный task source

Task Manager является единственным authoritative task source. Не использовать
fallback provider, repository TODO list, plan, Goal, chat transcript или memory
как замену Task Manager scope.

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
| `In Review` | `started` | Result уже предъявлен; проверять candidate, evidence и все связанные duplicates. |
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
→ machine-verified
→ review-ready
→ human-accepted
→ terminal
```

Возврат на доработку:

```text
review-ready
→ changes-requested
→ rework
→ machine-verified
→ review-ready
```

При changes requested вернуть Task из `In Review` в `In Progress`, выполнить
rework и только после повторных checks снова перевести в `In Review`. При
ограниченной capacity сохранять lane за этой review/rework chain до повторного
review или blocker; не переключаться на другую `In Progress` только из-за
смены status.
Переводить `To Do` в `In Progress` только после успешного preflight и получения
write authority. Переводить в `In Review` только exact candidate с passing
required checks и review packet. Переводить в `Done` только после task
acceptance, integration и обязательных effects. `Canceled` использовать только
при подтверждённом canceled outcome. Один status никогда не доказывает другой
evidence layer.

## 5. Preflight disposition

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
reconciliation применимого рабочего scope и остановиться. Не создавать пустой
commit, не повторять дорогой gate и не производить effect только ради свежего
отчёта.

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
- после merge повторяются affected checks, после полного fan-in — aggregate
  gate на exact integrated result.

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
4. Выполнить или повторить targeted checks и проверить changed scope.
5. Перед review прочитать все связанные duplicate Tasks и включить их
   отличающиеся problem statements, acceptance и failure scenarios в checklist.
   Если duplicate описывает материально отдельную проблему, зафиксировать
   finding и запросить scope decision вместо silent closure.
6. Провести independent agent review без mutation authority, если он требуется
   risk class или project policy.
7. Интегрировать result и выполнить integration/aggregate checks.
8. Выполнить только обязательные external effects и независимо проверить exact
   target.
9. Сформировать review packet и обновить Task в `In Review`, если она ещё не в
   этом status и требуется human acceptance.
10. При changes requested вернуть Task в `In Progress` и сохранить за ней
    текущую lane до повторного review или blocker. После explicit acceptance
    обновить её в `Done` и перечитать. При подтверждённом canceled outcome
    завершить через `Canceled` по project policy.

Разделять Task Manager state, source result, checks, human acceptance и external
effects. Успех одного слоя не доказывает остальные.

## 9. Review и reports

Review packet должен содержать:

- Task identifiers и цель batch;
- summary изменений и exact result identity;
- `acceptance criterion → evidence/result`;
- `duplicate scenario → covered evidence/finding` для каждого связанного
  duplicate;
- targeted, integration и aggregate checks;
- dependency/integration picture;
- risks, limitations и unresolved gaps;
- короткий human verification path;
- recommendation: `accept`, `changes requested` или `decision required`.

После changes requested показывать delta: исправленные findings, новый result
identity, повторённые checks и оставшиеся gaps.

Connector не предоставляет append-only comments или отдельный task-report
tool. Не перезаписывать Task description журналом выполнения. До появления
project-defined durable report channel выдавать review packet в текущем
interaction и использовать Task Manager для status projection.

## 10. Defects и recovery

- Автоматически исправлять только defect, который acceptance или project policy
  включает в exact scope.
- Для нового out-of-scope defect остановиться до code и Task Manager writes;
  запросить scope decision.
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
- все duplicate-derived scenarios покрыты evidence либо вынесены как явные
  findings/scope decisions;
- accepted results присутствуют в exact integration state;
- final project checks относятся к exact result;
- обязательные external effects независимо проверены;
- все рабочие и изменённые Tasks перечитаны и их current statuses соответствуют
  фактам; исключённые Backlog и terminal counts отражены отдельно;
- run/Goal/journal state reconciled, когда он применим.

Финальный отчёт отдельно показывает Task Manager projection, source/integration
identity, checks, human acceptance, external effects и gaps.

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
