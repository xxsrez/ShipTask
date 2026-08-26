# Raw facts: bulk-cross-project-rollback

Source project: Task Manager

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Task Manager.

## Publication unit

Нужен один closing comment для вымышленной Task `TM-EVAL-551`. Task проверяет
атомарный перенос нескольких Tasks между Projects: несовместимое значение не
должно приводить к частичному переносу, а исправленный повтор должен сохранить
идентичность Tasks.

## User-visible acceptance

### Scenario A — весь набор отклонён

- В Project `Source` выбраны две Tasks: `Move invoices` состоит в Release
  `Source 1.0`, а `Update checklist` не назначена в Release.
- Пользователь выбрал Project `Target`, но не указал, что делать с
  несовместимым Release первой Task.
- Система объяснила, что Release нужно явно очистить или заменить, и отклонила
  весь перенос.
- Обе Tasks остались в `Source`, membership первой Task не изменилась, а
  следующий номер Task в `Target` не был израсходован.

### Scenario B — явное решение и успешный перенос

- Пользователь повторил перенос тех же двух Tasks и явно выбрал очистку Release.
- Обе Tasks одной операцией перешли в `Target`; ни одна не осталась в исходном
  Project.
- Их постоянная identity, content, comments и attachments сохранились, Release
  стал пустым.
- Человекочитаемые identifiers сменились с `BS-41`/`BS-42` на следующие номера
  `BT-18`/`BT-19`; поиск по прежним identifiers по-прежнему находит те же Tasks.

## Knowledge and authority boundary

- Проверялся только перенос двух Tasks без parent/subtasks и relations.
- Сценарий не доказывает поведение hierarchy или relation cleanup.
- Первый отказ является ожидаемой защитой от неявной потери Release membership,
  а не defect.
- Все Projects и Tasks синтетические; production не затрагивался; Task пока
  находится в `In Review`.

## Audit-only evidence

- source/target project refs `prj_eval_551_src_42ac` и `prj_eval_551_dst_60df`;
- task public refs `tsk_eval_551_a_27f1` и `tsk_eval_551_b_d108`;
- source release ref `rel_eval_551_src_10`;
- task versions map suffix `vers_eval_551_11_7`;
- target sequence before/after `17/19`;
- rejected transaction `txn_eval_551_abort_84e0`;
- committed transaction `txn_eval_551_apply_84e1`;
- repository trace `trace_eval_bulk_move_551_6b0c`.

## Accepted product source

Атомарный cross-Project move и rollback invalid sets описаны в read-only sources:

- `/workspace/Task Manager/docs/architecture.md`;
- `/workspace/Task Manager/docs/specs/mvp.md`;
- `/workspace/Task Manager/tests/repository-integration.test.ts`.
