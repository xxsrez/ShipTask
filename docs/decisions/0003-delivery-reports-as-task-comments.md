# 0003. Delivery reports только как Task comments

Статус: accepted, 2026-08-16. Заменяет
[ADR-0002](0002-managed-delivery-report-in-task.md). Capability-optional часть
этого решения заменена [ADR-0006](0006-delivery-comment-as-terminal-effect.md),
а current гарантия native comments закреплена
[ADR-0020](0020-visible-acceptance-incidents-and-required-comments.md).

## Контекст

Пользователь ожидает, что человекочитаемые ShipTask delivery reports будут
обычными комментариями Task Manager. Task `description` принадлежит постановке
задачи и не должен становиться storage, journal или fallback для отчётов.

На момент решения current Task Manager source
`06f19e807bf24829ca47106791eca662f4b36dcf` предоставляет только чтение
imported comments через external context. Native tool для создания Task
comments отсутствует. Эта capability планируется отдельно и может появиться
без одновременного изменения ShipTask.

## Решение

- Публиковать delivery report только через native Task Manager capability
  создания комментария для exact Task. Никогда не писать report в
  `description` и не использовать другой Task field как fallback.
- Явный ShipTask invocation разрешает только task-specific report comments в
  рабочих in-scope Tasks. Он не разрешает arbitrary discussion comments,
  unrelated Tasks, duplicates или backfill старых terminal Tasks.
- На каждом запуске определять capability по текущему доступному tool contract,
  а не по версии, дате, ожиданию roadmap или сохранённому флагу. Как только
  connector действительно предоставляет подходящий write tool и authority,
  skill начинает использовать comments без отдельной migration Task.
- Считать capability `available`, только если доступный Task Manager tool явно
  создаёт native comment для canonical Task ref. Imported comments и
  `get_task_external_context` являются read-only provenance, а не этой
  capability.
- Если tool отсутствует, не поддерживается фактическим connector, недоступен по
  authority или возвращает feature-not-available, классифицировать report step
  как `not-available` и скипать. Это не `TASK CONTEXT ALARM`, не
  `completion-remains` и не препятствие для `Done` или Goal completion.
- Когда comments доступны, писать user-facing report при terminal completion и
  при material failure/rework/blocker, который важно объяснить пользователю.
  Не писать `ACCEPTANCE READY`: passing terminal evidence автоматически ведёт
  к `COMPLETED`. Не комментировать каждую внутреннюю red/green итерацию.
- Перед созданием комментария использовать read/list capability, если она есть,
  чтобы не дублировать тот же `Task + state + exact result`. После write
  проверить созданный comment, когда connector даёт read-back. При unknown
  outcome не повторять write вслепую.
- Сохранять outcome-first, blameless и task-specific формат ADR-0002: полезные
  flow/causal diagrams, evidence, limitations и confidence там, где они
  действительно нужны. Выбирать plain text или Markdown по доказанному
  renderer contract; Mermaid использовать только при подтверждённой поддержке.
- В финальном interaction report явно показывать disposition для comments:
  `published`, `not-available` либо `write-outcome-unknown`. Не выдавать
  скипнутый report за опубликованный.

Точный runtime reference удалён вместе с legacy `$ship-tasks`; это решение
сохранено как историческое.

## Последствия

Положительные:

- requirements в `description` остаются неизменными;
- report появляется в предназначенной для discussion истории Task;
- ShipTask автоматически использует новую connector capability после её
  фактического появления;
- отсутствие ещё не выпущенной feature не блокирует доставку основной Task.

Ограничения:

- до появления native comment write отчёт остаётся только в review/interaction
  output и не сохраняется внутри Task;
- comment create и status transition могут быть неатомарны; при частичном
  outcome skill обязан честно reconciliate оба слоя;
- без comment list/read tool невозможно доказать отсутствие duplicate после
  неизвестного network outcome, поэтому blind retry запрещён.
