# Raw facts: release-delete-membership-boundary

Source project: Task Manager

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Task Manager.

## Publication unit

Нужен один closing comment для вымышленной Task `TM-EVAL-541`. Цель Task —
проверить, что удаление Release не удаляет его Tasks, а восстановление и
необратимая очистка membership имеют разные последствия.

## User-visible acceptance

### Scenario A — recoverable delete и restore

- Release `0.4` содержал 7 Tasks, а Saved View `0.4 scope` фильтровала Tasks по
  этому Release.
- Editor переместил Release в `Recently deleted`.
- Все 7 Tasks остались доступны в Project и сохранили title, status и content,
  но в обычных карточках Release временно не отображался.
- Saved View не показала эти Tasks, пока Release был удалён.
- После restore тот же Release вернулся, все 7 Tasks снова отобразили прежнюю
  membership, а Saved View снова нашла их.

### Scenario B — permanent purge

- В отдельном повторе Owner после явного подтверждения необратимо удалил такой
  же synthetic Release с 7 Tasks.
- Tasks не были удалены; у них очистилась связь с Release.
- Saved View сохранила исходный фильтр по уже отсутствующему Release, не стала
  шире и вернула пустой результат.
- Восстановить membership после permanent purge через Release restore уже
  нельзя.

## Knowledge and authority boundary

- Два сценария выполнялись на независимых synthetic fixtures, поэтому recoverable
  restore и permanent purge не являются последовательными действиями над одним
  Release.
- Проверялся Release lifecycle, но не удаление Tasks или Saved Views.
- Permanent purge требует Owner и отдельного подтверждения; permission UI вне
  этого пути не проверялся.
- Production не затрагивался; Task ещё находится в `In Review`.

## Audit-only evidence

- recoverable release ref `rel_eval_541_restore_aa31`;
- purge release ref `rel_eval_541_purge_17b2`;
- seven task refs batch suffix `tasks_eval_541_07`;
- Saved View ref `vw_eval_541_release_filter_2e18`;
- deletion tuple revision `del_eval_541_v5`;
- purge job `purge_eval_541_409`;
- filter AST missing ref `qref_eval_541_64cc`;
- repository transactions `txn_eval_541_r_21` и `txn_eval_541_p_22`.

## Accepted product source

Release deletion, membership restore и inert missing filters описаны в read-only
sources:

- `/workspace/Task Manager/docs/reference/domain-model.md`;
- `/workspace/Task Manager/docs/architecture.md`;
- `/workspace/Task Manager/docs/specs/mvp.md`;
- `/workspace/Task Manager/tests/deletion-integration.test.ts`.
