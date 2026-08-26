# Raw facts: historical-content-current-access

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Example Notes.

Source project: ExampleNotes

## Publication unit

Нужен один closing comment для вымышленной Task `MD-EVAL-521`. Task проверяет,
что история остаётся привязана к точной старой версии, но сама ссылка на историю
не заменяет актуальное право чтения Mind.

## User-visible acceptance

### Scenario A — старая версия доступна действующему Reader

- Reader открыл запись `concepts/retrospective.md` из revision 12.
- В текущей HEAD revision 15 эта запись уже удалена.
- Пока membership Reader действует, выданный historical locator продолжает
  возвращать содержимое именно revision 12, а не подмешивает текущую HEAD.
- Чтение истории не восстановило удалённую запись и не изменило Mind.

### Scenario B — прежняя ссылка не переживает потерю доступа

- Тот же Reader заранее получил locator revision 12 и ссылку на готовый export.
- После отзыва membership повторное чтение locator и скачивание export были
  остановлены до выдачи содержимого.
- Ответ не раскрыл название Mind, состав старой revision или bytes архива.
- Старый locator и download URL не дали обойти отзыв доступа; после
  восстановления membership потребовалась новая авторизованная ссылка на
  скачивание.

## Knowledge and authority boundary

- Проверка выполнена только в synthetic private UAT; production не затрагивался.
- Историческая revision immutable и read-only, но доступ к ней проверяется заново
  при чтении; наличие старой ссылки не является самостоятельным разрешением.
- Сценарий не утверждает, что отзыв доступа удаляет историю для остальных
  текущих участников.
- Comment готовится до отдельного status write.

## Audit-only evidence

- product candidate `0bd7f87730dcf4d3c42ee2684515f6ec7a56cd53`;
- CI run `44200412980`;
- Sites version `v-eval-203`;
- deployment `appgdep_eval_521_history`;
- revisions `rev_eval_521_12` и `rev_eval_521_15`;
- locator `mdl2_eval_521_history`;
- export job `export_eval_521_09`;
- grant suffix `f2d9aa`;
- request correlation `req_eval_521_revoked_fetch`.

## Accepted product source

Принятые exact-revision и current-access semantics описаны в read-only sources:

- `/workspace/ExampleNotes/docs/specs/api.md`;
- `/workspace/ExampleNotes/docs/specs/domain-model.md`.
