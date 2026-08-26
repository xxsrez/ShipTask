# Raw facts: viewer-comment-permissions

Source project: Task Manager

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Task Manager.

## Publication unit

Нужен один closing comment перед переводом вымышленной Task `TM-EVAL-501` из
`In Review` в `Done`. Цель Task — подтвердить понятную границу доступа к
обсуждениям: участник с правом чтения видит разговор, но не может менять его, а
участник с правом редактирования может безопасно продолжить ветку.

## User-visible acceptance

### Scenario A — участник с правом чтения

- Viewer открыл Task и прочитал корневой комментарий вместе с двумя ответами.
- Попытка Viewer добавить новый комментарий была отклонена.
- Попытка Viewer поставить реакцию также была отклонена.
- В ветке не появилось нового текста или реакции; существующие комментарии не
  изменились.

### Scenario B — участник с правом редактирования

- Та же ветка до действия Editor была отмечена как закрытая.
- Editor отправил ответ; ответ появился один раз, а ветка снова стала открытой.
- Повтор той же отправки с тем же ключом вернул исходный ответ и не создал
  дубликат.
- Viewer после этого увидел обновлённую ветку, но по-прежнему не получил права
  её менять.

## Knowledge and authority boundary

- Проверялись только чтение и обычные comment/reaction mutations внутри одной
  синтетической Project Task.
- Sharing, изменение ролей, удаление комментариев и production не проверялись.
- Task пока находится в `In Review`; status write выполняется отдельно.
- Отказ Viewer является ожидаемой permission boundary, а не defect.

## Audit-only evidence

- synthetic task ref `tsk_eval_501_8f17b3`;
- root comment ref `cmt_eval_501_root_09`;
- reply ref `cmt_eval_501_reply_14`;
- Viewer grant revision `agr_eval_501_viewer_v6`;
- Editor grant revision `agr_eval_501_editor_v3`;
- idempotency key suffix `idem_501_a91c`;
- Task versions `41` и `42`;
- repository trace `trace_eval_comments_501_772e`;
- test worker shard `tm-comments-eval-03`.

## Accepted product source

Принятые границы ролей и comment behavior описаны в read-only sources:

- `/workspace/Task Manager/docs/specs/mvp.md`;
- `/workspace/Task Manager/tests/comments-integration.test.ts`;
- `/workspace/Task Manager/tests/repository-integration.test.ts`.
