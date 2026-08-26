# Raw facts: invitation-reissue-single-pending

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Example Notes.

Source project: ExampleNotes

## Publication unit

Нужен один closing comment для вымышленной Task `MD-EVAL-551`. Task проверяет
повторный выпуск приглашения: у получателя должно остаться одно актуальное
ожидающее приглашение, а доступ появляется только после принятия.

## User-visible acceptance

### Scenario A — просроченное приглашение заменено одним новым

- Зарегистрированному пользователю было выдано приглашение Reader, которое
  истекло до принятия.
- Owner повторно выпустил приглашение; прежнее завершилось, а replacement получил
  новый семидневный срок.
- В интерфейсе адресата отображается ровно одно актуальное pending invitation.
- До принятия membership и доступ к private Mind не появились.
- Попытка принять прежнюю истёкшую ссылку была отклонена и также не добавила
  участника.
- После принятия replacement атомарно появилась одна active Reader membership.

### Scenario B — повтор и конфликт не создают дубликаты

- В отдельном synthetic Mind после потерянного ответа Owner повторил тот же
  reissue request: сервер вернул
  тот же replacement, не создав ещё одного приглашения.
- Конкурентная попытка переиздать уже заменённое приглашение со старой version
  была отклонена.
- Попытка использовать тот же retry key с другой ролью также была отклонена.
- После обеих попыток оставалось одно актуальное pending invitation с исходно
  выбранной ролью; membership не изменилась.

## Knowledge and authority boundary

- Проверка выполнена только в synthetic private UAT; production не затрагивался.
- Invitation адресован уже зарегистрированному пользователю; email delivery и
  приглашение незарегистрированных людей не проверялись.
- Pending invitation не даёт read access и не подходит для ownership transfer.
- Comment готовится до отдельного status write.

## Audit-only evidence

- product candidate `1cc37bd9c067112cd6991f550ac65b2ba8804408`;
- CI run `44200415703`;
- Sites version `v-eval-206`;
- deployment `appgdep_eval_551_invites`;
- invitations `inv_eval_551_old` и `inv_eval_551_replacement`;
- invitation versions `4` и `5`;
- membership `member_eval_551_reader`;
- idempotency suffix `91f2b4`;
- request correlation `req_eval_551_stale_reissue`.

## Accepted product source

Принятые invitation lifecycle и reissue semantics описаны в read-only sources:

- `/workspace/ExampleNotes/docs/specs/domain-model.md`;
- `/workspace/ExampleNotes/docs/specs/api.md`.
