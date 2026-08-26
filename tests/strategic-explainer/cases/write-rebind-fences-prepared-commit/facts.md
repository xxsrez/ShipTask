# Raw facts: write-rebind-fences-prepared-commit

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Example Notes.

Source project: ExampleNotes

## Publication unit

Нужен один closing comment для вымышленной Task `MD-EVAL-531`. Task проверяет,
что подготовленное изменение не уезжает в другой Mind, если writable target
сменился до сохранения.

## User-visible acceptance

### Scenario A — старое изменение остановлено после rebind

- Writable target был `Research`; для него подготовили добавление
  `concepts/interview.md` на текущей revision 7.
- До commit пользователь явно переключил writable target на `Personal`.
- Попытка отправить ранее подготовленное изменение со старым write binding была
  отклонена.
- Ни `Research`, ни `Personal` не получили новую запись или новую revision;
  payload не был автоматически перенаправлен в новый target.

### Scenario B — свежая правка попала только в новый target

- После переключения клиент перечитал current binding и HEAD `Personal`, заново
  показал пользователю точное назначение и подготовил отдельную заметку
  `concepts/personal-follow-up.md`.
- Подтверждённое сохранение создало одну новую revision только в `Personal`.
- Повтор старого запроса для `Research` снова был отклонён; прежний binding ID не
  ожил и не пересёк новую generation.

## Knowledge and authority boundary

- Проверка выполнена только в synthetic private UAT; production не затрагивался.
- Rebind выбирает destination, но не переносит consent или уже подготовленный
  content между Minds.
- Сценарий не проверяет автоматический capture или cross-Mind copy.
- Comment готовится до отдельного изменения статуса.

## Audit-only evidence

- product candidate `64da50637430a3c5a16ee9d90f4a891b76dd0ac8`;
- CI run `44200413812`;
- Sites version `v-eval-204`;
- deployment `appgdep_eval_531_rebind`;
- previous write binding `wb_eval_531_research_03`;
- current write binding `wb_eval_531_personal_04`;
- binding versions `17` и `18`;
- revisions `rev_eval_531_research_7` и `rev_eval_531_personal_22`;
- request correlations `req_eval_531_stale` и `req_eval_531_fresh`.

## Accepted product source

Принятые rebind и commit-fencing semantics описаны в read-only sources:

- `/workspace/ExampleNotes/docs/specs/mind-bindings.md`;
- `/workspace/ExampleNotes/docs/specs/api.md`.
