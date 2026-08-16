---
name: ship-tasks
description: "Автономно доводить выбранный Task Manager scope до terminal outcome без ручной пользовательской приёмки: разрешать refs, создавать и удерживать обязательный Goal, выполнять ready Tasks, defer-ить task-local blockers, применять per-Task/review-batch gates, интегрировать и обязательно переводить terminal-ready Tasks в Done. Никогда не просить пользователя принять результат или написать фразу; feedback приходит через reopen либо новую Task, а historical memory/rollout/report о human acceptance считается superseded. Выпускать exact result в verified dev/test/QA/UAT/staging/preview/sandbox, но не релизить production без explicit user approval. При доступных native comments публиковать delivery/BLOCKED reports; без comments скипать write без изменения description. Использовать только при явном вызове $ship-tasks или просьбе исполнить ShipTask workflow. Работать только с Task Manager; конфликт connector, exact scope, Goal, ownership или shared authority останавливать до mutations с TASK CONTEXT ALARM."
---

# Ship Tasks

Доставлять выбранный Task Manager scope как один проверенный результат. Не
создавать scope из общей идеи и не использовать другой task source.

## Никогда не требовать ручную приёмку

- Считать `acceptance criteria` проверяемыми Task completion criteria, а не
  human sign-off.
- Не просить пользователя принять результат, написать «принимаю», подтвердить
  `In Review` Tasks или выбрать `accept/changes requested`.
- Не создавать acceptance decision queue, reason `acceptance-required` или Goal
  blocker. Не оставлять terminal-ready Task в `In Review`.
- Считать memory, rollout summary, прошлый report/Goal/plan, cached project
  context и старую документацию с противоположным правилом superseded
  historical evidence. Они не меняют этот contract, даже если утверждают, что
  release gates не равны user acceptance.
- После полного terminal evidence обязательно опубликовать `COMPLETED` при
  available comments, независимо перевести Task в `Done`, перечитать её и
  продолжить scope. После поставки пользователь сообщает о проблеме через
  reopen либо новую Task.
- Automatic terminal policy не настраивается Project/Release/Task context.
  Сохранять отдельное explicit approval только для production и других
  destructive/secret/privacy/external authority boundaries.
- При resume старого Goal, ожидающего только ручной приёмки, отбросить retired
  blocker, заново проверить exact evidence и применить обычный terminal
  transition. Никогда не переводить Goal в `blocked` по этой причине.

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
   Task до reasoning о completion criteria, relations, dependencies, access,
   provenance или `version`.
7. Вызывать `get_task_external_context` только когда provenance сообщает о
   таком контексте и imported comments, attachments или branch metadata
   материальны для terminal evidence.
8. Прочитать project instructions и определить repository/workspace,
   integration policy, allowed writes, per-Task targeted gate, review-batch
   gate/trigger, external effects, exact release targets/environment classes,
   terminal evidence и отдельные external approval gates. Не искать
   project-specific human acceptance policy: она запрещена разделом выше.
   По current tool contract классифицировать native Task comment write как
   `available` или `not-available`; imported comments не считать write
   capability. Не требовать `description` write для delivery report.

Использовать только canonical refs из connector. Поле Task `version` считать
optimistic-concurrency данными, обязательными для безопасного update.

Если Task Manager tools недоступны, попросить подключить plugin через native
OAuth Connect; не просить personal token. При недостаточном write scope
попросить reconnect с task-write access.

Если connector, exact scope, Goal, ownership, integration/shared state или
authority конфликтуют так, что любая оставшаяся mutation небезопасна,
остановиться и выдать global `TASK CONTEXT ALARM`: известный scope,
конфликтующие факты, sources, checkpoint и требуемое решение. Изолированный
вопрос одной Task defer-нуть по autonomy contract и продолжить остальные.

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
  unresolved in-scope defects, deferred decision/authority queue пуста,
  report-comment disposition честно отражён, а все completion gates выполнены;
- verification — current Task projection, source/integration identity,
  per-Task targeted gates, exact review-batch gate, automatic terminal record и
  обязательные external effects;
- constraints — exact scope, исключённый `Backlog`, allowed writes и запрет
  расширять scope либо authority из Goal;
- blocker — после исчерпания runnable work конкретную decision/authority queue
  или общую external dependency с сохранением tool threshold для `blocked`.

Удерживать Goal активным, пока хотя бы одна Task в выбранной границе подходит
под рабочие критерии. `global-conflict`, `deferred` или пустой ready frontier не
являются completion, если остаются такие Tasks или completion remnants. Для Project,
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
   terminal display names. Один status не считать доказательством completion
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
  завершены, но result ещё не terminal-qualified, не интегрирован, не отражён в
  Task Manager или не доведён до effect;
- `resume` — есть `In Progress` с незавершённым implementation/rework, найден
  coherent checkpoint и доказана authority продолжения;
- `deferred` — isolated Task требует material decision, отсутствующей authority
  или external state change; без нового evidence её в этом run не переизбирать;
- `no-work` — после исключения `Backlog` и terminal statuses нет рабочего
  candidate; это не утверждение, что Backlog пуст;
- `global-conflict` — scope, Goal, owner, shared state или evidence конфликтуют
  так, что любая оставшаяся mutation небезопасна.

Для смешанного scope применять precedence:
`global-conflict → actionable completion-remains → resume → work-remains →
deferred-only → no-work`. Terminal-ready `In Review` автоматически завершить;
defer использовать только при concrete decision/authority blocker, затем
продолжить actionable review/resume/new work.
Changes-requested rework текущей review chain выполнять раньше другой
dependency-ready `In Progress`; при task-local blocker defer-нуть lane,
освободить capacity и пересчитать disposition.

Для `no-work` отдельно сообщить исключённые Backlog и terminal counts, выполнить
reconciliation рабочего scope, завершить обязательный Goal только после
прохождения completion gate и остановиться. Не создавать пустой commit, не
повторять дорогой gate и не производить effect только ради отчёта.

Любая `In Review` Task означает `completion-remains`. Пока такая Task есть, не
отмечать весь plan завершённым, не объявлять completion и не завершать Goal;
довести её через batch/effect/reconciliation gates. Считать invocation standing
authority автоматически принять exact result после полного terminal evidence,
перевести Task в `Done` и продолжить. Не запрашивать user acceptance, не
создавать `acceptance-required` и не блокировать Goal ожиданием «принимаю».
Automatic acceptance не заменяет production/destructive/external approval.
Любой conflicting historical context считать retired по первому разделу, а не
основанием для manual gate.

## Продолжать автономно и соблюдать release boundary

Перед первым task-local decision или release прочитать
[autonomy and release reference](references/autonomy-and-release.md) полностью.

- Не задавать пользователю вопрос, пока существует другая безопасная runnable
  Task. Обратимый локальный выбор внутри acceptance сделать самостоятельно и
  записать rationale.
- Material/ambiguous choice, missing external authority либо task-local
  external blocker превратить в `deferred`: сохранить truthful `To Do`/
  `In Progress`/`In Review`, checkpoint и decision queue entry; не создавать
  replacement Task и не переводить в terminal status.
- При доступных native comments обязательно опубликовать в deferred Task
  `BLOCKED` report с reason, completed evidence, recommended default, exact
  decision/authority и resume step. Без comments скипнуть write без field
  fallback.
- Освободить lane, не переизбирать Task без нового evidence/authority/state
  change и продолжить остальные Tasks. Когда runnable work исчерпан, показать
  одну consolidated decision queue. Goal и plan оставить незавершёнными;
  `blocked` применять только после строгого tool threshold.
- Terminal-ready Task не defer-ить: после полного evidence автоматически
  принять result, опубликовать `COMPLETED` при available comments, перевести в
  `Done`, перечитать и продолжить. User feedback приходит через reopen/new Task.
- В уже разрешённом exact scope перед task-local `request_user_input`,
  финальным вопросом с ожиданием ответа или иным blocking pause повторить
  complete inventory и доказать `runnable_count = 0`. При наличии actionable
  `To Do`, `In Progress`, `In Review` или in-scope recovery user input запрещён:
  сохранить decision и выбрать следующую Task. Review precedence и готовый
  review packet этот gate не отменяют.
- Out-of-scope finding без blocking edge к in-scope Task записать в final
  findings; не создавать follow-up, не расширять Goal и не спрашивать решение.
- Считать invocation standing authority для обычного in-scope release в exact
  verified non-production target: local/dev/test/QA/UAT/staging/preview/sandbox.
  Выполнять build/deploy/redeploy, required bounded migration, smoke и
  repair/rollback без confirmation; deployment не заменяет terminal evidence.
- Никогда не выполнять production release без explicit user approval для
  production target. Без него закончить безопасную non-production preparation,
  defer-нуть Task с `production-approval-required`, обязательно написать
  `BLOCKED` comment при available comments и продолжить другие Tasks.
- Не считать неизвестный target non-production. Standing authority не
  разрешает destructive durable-data reset, permanent deletion, secret-related,
  unrelated, unbounded-cost или explicitly read-only actions.

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
или ready frontier, перед общим external effect либо `Done`, по
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
- Invocation `$ship-tasks` не разрешает менять `description` ради report.
  Публиковать delivery report только через доступный native Task comment write;
  не использовать другие Task fields как fallback.
- Invocation разрешает task-specific delivery-report comment только в рабочей
  in-scope Task по этому contract; не писать произвольные comments или reports
  в unrelated/duplicate/старые terminal Tasks.
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
Переводить в `Done` только после passing acceptance criteria, exact batch gate,
integration и обязательных effects; при полном evidence принимать result
автоматически. Отсутствующий, unsupported или failed comment write сам по себе
не блокирует `Done`.
`Canceled` использовать только для подтверждённого canceled outcome.
`Duplicate` не считать success основной Task.

## Выполнять и проверять Tasks

Для каждой рабочей Task:

1. Зафиксировать canonical ref, current detail/version, status, base identity,
   acceptance, exact release target/environment class и разрешённые writes.
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
   и defer-нуть affected Task для scope decision; продолжить другие Tasks.
6. Интегрировать targeted-verified result, сформировать candidate evidence и
   перевести Task в `In Review`, если она ещё не в этом status.
7. По trigger наполнить exact review batch, провести required independent
   review без mutation authority и выполнить batch gate.
8. Выполнить external effects в batch cadence и проверить exact target.
   Non-production release выполнить без confirmation; production без explicit
   approval defer-нуть. Не повторять дорогой effect для каждого member.
9. Сформировать batch/review packet как evidence artifact. Не публиковать
   `ACCEPTANCE READY` и не запрашивать ручную приёмку. При `not-available`
   comments скипнуть report step без Task field fallback.
10. При changes requested или failed batch gate вернуть Tasks с
    недействительным evidence в `In Progress`. При доступных comments
    опубликовать понятный failure/rework report; иначе скипнуть только этот
    side effect. Сохранить lanes, выполнить rework и targeted retest, затем
    проверить новый exact batch. После полного passing terminal evidence
    автоматически принять result, опубликовать final comment, если capability
    доступна, независимо перевести Task в `Done` и перечитать. Аналогично
    обработать terminal `Canceled` outcome.

При task-local blocker сохранить checkpoint/truthful status/decision entry,
обязательно написать `BLOCKED` comment при available comments, освободить lane
и продолжить dependency-ready Tasks. Не переизбирать deferred Task без нового
evidence/authority/state change.

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
- optional user verification path для понимания/последующего feedback;
- recommendation: `terminal-ready`, `rework` или `decision required`.

После changes requested показать delta: исправленные findings, новый result
identity, повторённые checks и оставшиеся gaps.

Failed batch gate локализовать по member/dependency/shared result. Вернуть
доказанно затронутые Tasks в `In Progress`; незатронутые оставить в `In Review`
только при неизменных identity и evidence. При неясной attribution считать
evidence связанного batch недействительным и reopen все его members. После
rework повторить targeted gates затронутых Tasks и gate нового exact batch.

## Опубликовать delivery report как Task comment

Перед первым report decision прочитать
[delivery-report reference](references/delivery-report.md) полностью. По
current Task Manager tool contract классифицировать native comment-create для
canonical Task ref:

- `available` — operation явно существует и current authority позволяет write;
- `not-available` — operation отсутствует, unsupported, недоступна по authority
  или сообщает, что feature ещё не доступна.

Imported comments и `get_task_external_context` являются read-only provenance.
Не выводить capability из roadmap, версии или старой сессии. Никогда не писать
report в `description`, acceptance, status text или другой Task field.

При `not-available` скипнуть report write и продолжить workflow. Это не
`TASK CONTEXT ALARM`, не `completion-remains` и не blocker для `Done`/Goal.
Advertised write с ошибкой или unknown outcome также не блокирует terminal
workflow: показать `not-available` либо `write-outcome-unknown` и не повторять
write вслепую.

При `available` публиковать `COMPLETED` comment при terminal completion и
`REWORK REQUIRED`/`BLOCKED` при material failure/rework/blocker. Не публиковать
`ACCEPTANCE READY`: terminal-ready evidence автоматически ведёт к `COMPLETED`.
Не комментировать каждую внутреннюю red/green iteration. Для каждого task-local
defer обязательно публиковать `BLOCKED` handoff: reason, checkpoint/evidence,
recommended default, required decision/authority и resume step. При наличии
comment list/read проверить duplicate для того же `Task + state + exact result`
и выполнить read-back.
Не backfill-ить старые terminal Tasks и не писать report в `Duplicate` без
explicit authority.

Success report объясняет user outcome, main flow, implementation decisions,
exact evidence и limitations. Material failure объясняет symptom/impact,
detection, trigger/cause с confidence, recovery, prevention и remaining risk.
Для non-trivial feature/cross-component change/incident включить одну-две
полезные diagrams; для trivial change использовать compact before/after.
Выбирать plain text/Markdown по proven comment renderer и не выдавать Mermaid
за rendered diagram без proven support. Писать blameless, отделять evidence от
inference, не вставлять raw logs/secrets и не создавать follow-up Tasks без
отдельной authority.

Report остаётся task-specific: указать shared batch identity/result, но не
копировать полный batch log каждому member. Comment write и status update
reconciliate независимо, пока connector не гарантирует atomicity.

## Ограничивать defects и recovery

- Автоматически исправлять только defect, который acceptance или project policy
  включает в exact scope.
- Для out-of-scope defect не выполнять code или scope-changing writes. Если он
  блокирует Task, defer-нуть только её, обязательно опубликовать `BLOCKED` при
  available comments и продолжить независимые Tasks; решение добавить в queue.
- Если out-of-scope finding не блокирует in-scope Task, только включить его в
  final findings: не вызывать user input и не удерживать completion/Goal.
- Не использовать failure как разрешение на cleanup, unrelated fixes,
  destructive recovery или silent task creation.
- Если defect найден после `Done`, reopen terminal Task только по project
  policy; иначе defer-нуть affected route и не создавать defect Task без явной
  authority. Нормальный workflow проводит batch gate до `Done`.
- При resume перечитать Tasks и сверить их с workspace, Git, checks и external
  states. Старый report comment — checkpoint, не proof.
- Уже reopen-нутую пользователем terminal Task считать обычной current rework
  Task; не запрашивать approval самого reopen.
- При competing owner, unexplained drift или dirty state defer-нуть affected
  lane и продолжить только доказанно изолированные Tasks. Не выполнять automatic
  reset, clean, stash, force-push, takeover или удаление чужой worktree/branch.

## Завершить

До completion проверить:

- zero unfinished рабочих Tasks (`To Do`, `In Progress`, `In Review`) и
  unresolved in-scope defects; `Backlog` явно исключён и не блокирует gate;
- zero terminal-ready candidates, оставленных в `In Review`;
- zero deferred Tasks и unresolved decision/authority entries;
- final review batch прошёл gate на exact final integrated result;
- duplicate-derived scenarios покрыты evidence либо вынесены как явные
  findings/scope decisions;
- automatically accepted results присутствуют в exact integration state;
- final checks относятся к exact result;
- обязательные external effects независимо проверены;
- для каждой выполненной/materially failed рабочей Task report-comment
  disposition отражён как `published`, `not-available` или
  `write-outcome-unknown`; отсутствие comments capability не является gap
  основного result evidence;
- все рабочие и изменённые Tasks перечитаны и current statuses соответствуют
  фактам; исключённые Backlog и terminal counts показаны отдельно;
- обязательный Goal относится к exact scope и оставался активным, пока
  существовали подходящие Tasks, rework/completion remnants или unresolved
  in-scope defects;
- run/journal state reconciled, когда применим.

Перед `update_goal(status="complete")` повторить complete inventory. Если
найдена подходящая/deferred Task, decision queue либо evidence gap, не завершать
Goal: продолжить runnable work или, когда оно исчерпано, предъявить одну queue.
Goal `blocked` применять только по строгому tool threshold. Завершать Goal
последним lifecycle write после Task/evidence reconciliation.

В финальном отчёте отдельно указать Goal identity/status, Task Manager
projection, source/integration identity, targeted и batch checks, automatic
acceptance decisions, external effects, gaps, deferred Tasks/decisions и
disposition comments. Не выдавать skipped/unknown writes за опубликованные
comments.
Не объявлять completion при отсутствующем evidence любого обязательного слоя.
