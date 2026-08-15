---
name: ship-tasks
description: "Доводить уже созданный и выбранный scope Tasks, Project или Release из Task Manager до проверенного terminal outcome: разрешать canonical refs через Task Manager connector, читать полный Task detail и dependencies, выполнять ready Tasks, безопасно интегрировать результаты, проводить проверки и human review, обновлять Task statuses с optimistic concurrency и сверять обязательные внешние эффекты. Использовать только при явном вызове $ship-tasks или явной просьбе исполнить ShipTask workflow. Работать только с Task Manager; если connector, exact scope, acceptance, authority или обязательная capability недоступны либо неоднозначны, остановиться до мутаций с TASK CONTEXT ALARM."
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
   integration policy, allowed writes, required checks, external effects и
   human acceptance authority.

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

## Выполнить read-only preflight

1. Перечитать in-scope Task details и связанные boundary Tasks.
2. Отделить `backlog`, `unstarted`, `started`, `completed` и `canceled` Tasks;
   один status не считать доказательством acceptance или результата.
3. Построить dependency-ready frontier по relations и current statuses. Не
   угадывать смысл неоднозначной relation.
4. Проверить workspace, Git, branches, worktrees, uncommitted changes и
   provenance существующей работы. Сохранить пользовательские и чужие edits.
5. Проверить active run, writer ownership, claims/coordination records и уже
   выполненные external effects. Без доказанной authority оставаться observer.
6. Построить integration-conflict graph для paths, schema, API, migrations,
   generated artifacts, mutable dependencies, caches, runtime state и
   environments.
7. Определить verification, integration и review capacity.

Выбрать ровно одну disposition:

- `work-remains` — есть ready или потенциально ready Tasks;
- `completion-remains` — result существует, но не интегрирован, не принят, не
  отражён в Task Manager или не доведён до обязательного effect;
- `resume` — найден coherent checkpoint и доказана authority продолжения;
- `no-work` — весь scope terminal и reconciled;
- `conflict` — scope, owner, Task state или evidence противоречат друг другу.

Для `no-work` выполнить reconciliation и остановиться. Не создавать пустой
commit, не повторять дорогой gate и не производить effect только ради отчёта.

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
  defect Task. Invocation `$ship-tasks` само по себе этого не разрешает.

Переводить Task в started status только после успешного preflight. Переводить
в review status только для exact candidate с passing required checks и review
packet. Переводить в completed status только после acceptance, integration и
обязательных effects. Canceled/duplicate outcome не считать success без явной
project policy.

## Выполнять и проверять Tasks

Для каждой ready Task:

1. Зафиксировать canonical ref, current detail/version, base identity,
   acceptance и разрешённые writes.
2. При необходимости обновить Task в started status и перечитать projection.
3. Реализовать минимальный целостный result без unrelated cleanup.
4. Выполнить targeted checks и проверить changed scope.
5. Провести independent review без mutation authority, если его требует risk
   или project policy.
6. Интегрировать result. После каждого risk-relevant merge повторить affected
   checks; после fan-in выполнить aggregate gate на exact integrated result.
7. Выполнить только обязательные external effects и независимо проверить exact
   target.
8. Сформировать review packet и обновить Task в review status, если нужна human
   acceptance.
9. После explicit acceptance обновить Task в completed status и перечитать её.

Merge conflict, semantic conflict или aggregate regression возвращает Task в
rework. Не маскировать конфликт незапланированной правкой integration owner.

## Провести review

Сформировать компактный packet:

- Task identifiers и цель batch;
- summary и exact result identity;
- `acceptance criterion → evidence/result`;
- targeted, integration и aggregate checks;
- dependency/integration picture;
- risks, limitations и gaps;
- короткий human verification path;
- recommendation: `accept`, `changes requested` или `decision required`.

После changes requested показать delta: исправленные findings, новый result
identity, повторённые checks и оставшиеся gaps.

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
- При resume перечитать Tasks и сверить их с workspace, Git, checks и external
  states. Старый report — checkpoint, не proof.
- При competing owner, unexplained drift или dirty state остановить lane. Не
  выполнять automatic reset, clean, stash, force-push, takeover или удаление
  чужой worktree/branch.

## Завершить

До completion проверить:

- zero unfinished in-scope Tasks и unresolved in-scope defects;
- zero unaccepted review-ready candidates;
- accepted results присутствуют в exact integration state;
- final checks относятся к exact result;
- обязательные external effects независимо проверены;
- все in-scope Tasks перечитаны и current statuses соответствуют фактам;
- Goal/run/journal state reconciled, когда применим.

В финальном отчёте отдельно указать Task Manager projection,
source/integration identity, checks, human acceptance, external effects и gaps.
Не объявлять completion при отсутствующем evidence любого обязательного слоя.
