# Raw facts: comment-idempotency-and-stale-edit

Source project: Task Manager

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Task Manager.

## Publication unit

Нужен один closing comment для вымышленной Task `TM-EVAL-571`. Task проверяет,
что сетевой повтор не дублирует комментарий, устаревшая вкладка не стирает
свежую правку, а высокий Project role не позволяет редактировать текст от имени
его автора.

## User-visible acceptance

### Scenario A — безопасный повтор создания

- Editor отправил комментарий `Ready for review`.
- Ответ на первый запрос потерялся на уровне synthetic client, поэтому client
  повторил отправку с тем же ключом.
- Сервер вернул исходный комментарий с исходным текстом.
- В ветке остался один `Ready for review`; comment count увеличился только один
  раз.

### Scenario B — свежая и устаревшая правки

- Автор открыл комментарий в двух synthetic вкладках.
- В первой вкладке автор сохранил текст `Ready after accessibility check`.
- Вторая вкладка попыталась сохранить старую версию как `Ready`; операция
  получила conflict и не затёрла более новый текст.
- После read-back в комментарии остался `Ready after accessibility check`.

### Scenario C — авторство

- Project Owner попытался отредактировать этот комментарий своим запросом.
- Операция была отклонена: роль Owner не позволяет выдавать свою правку за текст
  другого автора.
- Комментарий и его author attribution не изменились.

## Knowledge and authority boundary

- Проверялись create retry, edit conflict и edit authorship одного native
  comment.
- Owner delete/tombstone, reply normalization и historical comments не
  проверялись.
- Отказы stale edit и Owner edit являются ожидаемой защитой данных, не defects.
- Production не затрагивался; Task пока находится в `In Review`.

## Audit-only evidence

- task ref `tsk_eval_571_f196`;
- comment ref `cmt_eval_571_2a72`;
- create idempotency suffix `idem_eval_571_b901`;
- comment versions `1` и `2`;
- stale request `req_eval_571_tab_b_v1`;
- owner request `req_eval_571_owner_edit_3`;
- comment count snapshots `14/15/15`;
- transaction trace `trace_eval_comment_571_409c`.

## Accepted product source

Comment idempotency, optimistic edit и authorship описаны в read-only sources:

- `/workspace/Task Manager/docs/specs/mvp.md`;
- `/workspace/Task Manager/docs/reference/domain-model.md`;
- `/workspace/Task Manager/docs/specs/agent-api.md`;
- `/workspace/Task Manager/tests/comments-integration.test.ts`.
