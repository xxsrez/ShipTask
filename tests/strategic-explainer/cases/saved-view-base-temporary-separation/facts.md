# Raw facts: saved-view-base-temporary-separation

Source project: Task Manager

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Task Manager.

## Publication unit

Нужен один closing comment для вымышленной Task `TM-EVAL-521`. Цель Task —
проверить, что временное уточнение списка не переписывает сохранённое
представление, а явное создание нового представления сохраняет именно видимый
результат.

## User-visible acceptance

### Scenario A — временное уточнение и очистка

- Исходная Saved View `Release candidates` хранит базовый фильтр по Release
  `0.3` и показывает 18 Tasks.
- Пользователь добавил временный фильтр `priority = High`; список сузился до 5
  Tasks, а интерфейс показал сохранённый и временный слои отдельно.
- `Clear temporary` вернул исходные 18 Tasks.
- Базовый фильтр Saved View остался фильтром только по Release `0.3`; version
  исходной View не изменилась.

### Scenario B — явное сохранение видимого результата

- Пользователь снова применил временный `priority = High` поверх исходной View и
  выбрал `Save as`.
- Новая Saved View `High-priority 0.3` сохранила оба условия, соединённые через
  `AND`, и при повторном открытии показала те же 5 Tasks.
- Исходная `Release candidates` осталась отдельной View с теми же 18 Tasks и
  прежней базовой формулой.
- Никакие Tasks не были изменены или скопированы.

## Knowledge and authority boundary

- Проверялись base query, temporary URL/session layer, `Clear temporary` и
  `Save as` для одной синтетической Project-scoped Saved View.
- `Edit view → Save changes`, sharing и global Saved Views не проверялись.
- Counts относятся только к подготовленным synthetic Tasks.
- Production не затрагивался; Task пока находится в `In Review`.

## Audit-only evidence

- source view ref `vw_eval_521_base_18e4`;
- derived view ref `vw_eval_521_saved_as_902c`;
- source version `27`, derived version `1`;
- Release ref `rel_eval_521_03`;
- query AST nodes `q_eval_release_44` и `q_eval_priority_61`;
- URL state digest `url_eval_521_732a`;
- executor snapshot `exec_eval_521_5f21`;
- sync cursor `sync_eval_521_000184`.

## Accepted product source

Разделение сохранённого и временного фильтров описано в read-only sources:

- `/workspace/Task Manager/docs/specs/mvp.md`;
- `/workspace/Task Manager/docs/specs/interface.md`;
- `/workspace/Task Manager/docs/reference/domain-model.md`;
- `/workspace/Task Manager/tests/saved-view-lifecycle.test.ts`.
