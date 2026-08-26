# Raw facts: idempotent-retry-with-authorization

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Example Notes.

Source project: ExampleNotes

## Publication unit

Нужен один closing comment для вымышленной Task `MD-EVAL-511`. Task проверяет
безопасное восстановление после потерянного ответа на сохранение: повтор не
должен дублировать изменение, а старый запрос не должен обходить актуальный
доступ.

## User-visible acceptance

### Scenario A — ответ потерян после успешного сохранения

- Editor добавил одну заметку `concepts/retry-note.md`, но соединение оборвалось
  до получения ответа.
- На сервере изменение уже создало revision 41.
- Пока доступ Editor оставался действующим, сверка с тем же запросом и тем же
  ключом вернула исходную revision 41.
- Повтор не создал вторую заметку, дополнительную revision или вторую запись в
  журнале.

### Scenario B — доступ отозван до выяснения результата

- В другой независимой операции соединение оборвалось до ответа, поэтому клиент не
  стал считать сохранение успешным или неуспешным.
- До сверки Owner отозвал Editor membership.
- Сверка и повторный запрос были отклонены после проверки актуального доступа;
  прежний запрос не восстановил права и не создал новый эффект.
- Для выяснения исходного результата сначала требуется снова получить доступ;
  слепой retry с изменённым запросом запрещён.

## Knowledge and authority boundary

- Проверка выполнена только в synthetic private UAT; production не затрагивался.
- Во втором сценарии исход transport-оборванной операции намеренно остаётся
  неизвестным текущему клиенту: отсутствие ответа не доказывает failure.
- Task проверяет безопасное восстановление, но не обещает автоматическое
  возвращение отозванного доступа.
- Comment готовится до отдельного изменения статуса.

## Audit-only evidence

- product candidate `8e76ae8ee887782e1e1c56d6dd3d843621135c87`;
- CI run `44200411739`;
- Sites version `v-eval-202`;
- deployment `appgdep_eval_511_recovery`;
- committed revision `rev_eval_511_41`;
- actor `principal_eval_511_editor`;
- idempotency keys `idem_eval_511_saved` и `idem_eval_511_unknown`;
- request correlations `req_eval_511_timeout_a` и `req_eval_511_timeout_b`.

## Accepted product source

Принятые retry, reconciliation и current-authorization semantics описаны в
read-only sources:

- `/workspace/ExampleNotes/docs/specs/api.md`;
- `/workspace/ExampleNotes/docs/specs/domain-model.md`.
