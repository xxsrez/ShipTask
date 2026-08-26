# Raw facts: project-shadow-restore

Source project: Task Manager

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Task Manager.

## Publication unit

Нужен один closing comment для вымышленной Task `TM-EVAL-531`. Task проверяет
восстанавливаемое удаление Project: удаление Project временно скрывает весь его
состав, но восстановление не должно оживлять child, который был удалён отдельно.

## User-visible acceptance

### Scenario A — отдельное удаление и Project shadow

- В Project `Spring cleanup` было 6 Tasks, 2 Releases и 1 project-scoped Saved
  View.
- Task `Remove legacy flag` сначала отдельно переместили в `Recently deleted`.
- Затем Editor удалил Project. Project и весь его оставшийся состав исчезли из
  обычных списков, поиска и навигации.
- У пяти остальных Tasks, обоих Releases и Saved View не появились собственные
  deletion timestamps: их скрывал Project shadow.
- Отдельно удалённая Task сохранила собственное состояние удаления.

### Scenario B — восстановление Project

- Editor восстановил Project до истечения срока хранения.
- Project, пять обычных Tasks, оба Releases и Saved View снова появились с теми
  же данными и связями.
- Отдельно удалённая `Remove legacy flag` не вернулась в Project lists и осталась
  в `Recently deleted`, где её можно восстановить отдельным действием.
- Восстановление Project не создало копий Tasks или Releases.

## Knowledge and authority boundary

- Проверялись recoverable delete и restore, но не permanent purge.
- Comment не должен обещать точный wall-clock момент будущей физической очистки.
- Все records синтетические; production и реальные пользовательские данные не
  затрагивались.
- Task пока находится в `In Review`; status write выполняется отдельно.

## Audit-only evidence

- project ref `prj_eval_531_44fd`;
- independently deleted task ref `tsk_eval_531_deleted_72a1`;
- Project deletion tuple suffix `del_eval_531_09`;
- child tuple scan `scan_eval_531_all_null_5_2_1`;
- restore transaction `txn_eval_531_restore_6bc2`;
- retention cutoff `2026-10-01T12:00:00Z`;
- sync cursor before/after `sync_eval_531_9021/9034`;
- repository trace `trace_eval_shadow_531_12c8`.

## Accepted product source

Project shadow и точный restore deletion state описаны в read-only sources:

- `/workspace/Task Manager/docs/reference/domain-model.md`;
- `/workspace/Task Manager/docs/architecture.md`;
- `/workspace/Task Manager/docs/specs/interface.md`;
- `/workspace/Task Manager/docs/decisions/0007-project-backup.md`;
- `/workspace/Task Manager/tests/deletion-integration.test.ts`.
