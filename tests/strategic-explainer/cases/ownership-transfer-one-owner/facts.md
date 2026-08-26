# Raw facts: ownership-transfer-one-owner

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Example Notes.

Source project: ExampleNotes

## Publication unit

Нужен один closing comment для вымышленной Task `MD-EVAL-561`. Task проверяет,
что ownership ordinary Mind передаётся атомарно только действующему участнику и
ни на мгновение не оставляет Mind без владельца или с двумя владельцами.

## User-visible acceptance

### Scenario A — передача существующему участнику

- У private Mind `Team Notes` был один Owner и active Editor Мария.
- Текущий Owner явно подтвердил передачу ownership Марии.
- Одна операция сделала Марию единственным Owner, а прежнего Owner — Admin.
- Content, история и memberships остальных участников не изменились.
- После операции только Мария смогла выполнить owner-only изменение visibility;
  прежний владелец с ролью Admin не смог.

### Scenario B — неподходящие цели не меняют роли

- В отдельном ordinary Mind Алексей имел только pending invitation и ещё не стал
  active participant.
- Попытка передать ownership Алексею была отклонена; роли текущего Owner и
  active Editor Елены не изменились.
- Отдельная попытка назначить второго Owner обычным изменением роли также была
  отклонена.
- После обеих попыток у Mind по-прежнему был ровно один Owner; ownerless и
  dual-owner state не возникли.

## Knowledge and authority boundary

- Проверка выполнена только в synthetic private UAT; production не затрагивался.
- Сценарий относится к ordinary Mind. Personal Mind не передаётся вообще.
- Target transfer должен быть existing active participant; pending invitation
  недостаточно.
- Comment готовится до отдельного status write.

## Audit-only evidence

- product candidate `2fd2a696aa406ca577952dbd45e60f3e860eb56f`;
- CI run `44200416855`;
- Sites version `v-eval-207`;
- deployment `appgdep_eval_561_owner`;
- metadata versions `12` и `13`;
- source membership `member_eval_561_source_owner`;
- target membership `member_eval_561_maria`;
- pending invitation `inv_eval_561_alexey`;
- request correlations `req_eval_561_transfer` и `req_eval_561_pending_denied`.

## Accepted product source

Принятые single-owner и transfer semantics описаны в read-only sources:

- `/workspace/ExampleNotes/docs/specs/domain-model.md`;
- `/workspace/ExampleNotes/docs/specs/api.md`.
