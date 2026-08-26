# Raw facts: concurrent-edit-no-hidden-merge

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Example Notes.

Source project: ExampleNotes

## Publication unit

Нужен один closing comment перед переводом вымышленной Task `MD-EVAL-501` из
`In Review` в `Done`. Цель Task — убедиться, что одновременные изменения не
затирают друг друга и не объединяются сервером незаметно для пользователя.

## User-visible acceptance

### Scenario A — устаревшая правка остановлена

- Анна открыла revision 28 и подготовила замену `concepts/plan.md`.
- До её сохранения Борис изменил тот же файл; его правка создала revision 29.
- Попытка Анны сохранить изменение поверх revision 28 была отклонена как
  конфликт актуальной версии.
- Сервер не создал частичную revision, не затёр текст Бориса и не попытался
  автоматически объединить оба варианта.

### Scenario B — изменение перестроено на свежих данных

- Анна заново открыла revision 29, увидела изменение Бориса и подготовила новый
  вариант, который сохраняет его абзац и добавляет свой.
- Новое подтверждённое сохранение создало ровно одну revision 30.
- В revision 30 присутствуют оба осознанно объединённых изменения; скрытых
  правок или дублирующего сохранения нет.

## Knowledge and authority boundary

- Проверка выполнена только в synthetic private UAT; production не затрагивался.
- Тест подтверждает отказ при stale base и успешную явную пересборку, но не
  обещает автоматический merge, branches или совместное редактирование в
  реальном времени.
- Comment готовится до status write; Task ещё находится в `In Review`.

## Audit-only evidence

- product candidate `1d582d7768c751a199fda22bb1f7c05b8612d309`;
- CI run `44200410501`;
- Sites version `v-eval-201`;
- deployment `appgdep_eval_501_concurrency`;
- revisions `rev_eval_501_28`, `rev_eval_501_29`, `rev_eval_501_30`;
- write binding `wb_eval_501_07`;
- idempotency suffixes `a16e90` и `c29b11`;
- request correlations `req_eval_501_stale` и `req_eval_501_fresh`.

## Accepted product source

Принятые atomic commit и concurrency semantics описаны в read-only sources:

- `/workspace/ExampleNotes/docs/specs/domain-model.md`;
- `/workspace/ExampleNotes/docs/specs/api.md`.
