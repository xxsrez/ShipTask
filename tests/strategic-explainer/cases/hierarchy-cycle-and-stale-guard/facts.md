# Raw facts: hierarchy-cycle-and-stale-guard

Source project: Task Manager

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Task Manager.

Этот case является contract-backed synthetic evaluation. Он проверяет смысл
принятой спецификации и repository test behavior, но не является live UAT,
production или доказательством того, что hierarchy уже выпущена пользователям.

## Publication unit

Нужен один evaluation comment для вымышленной Task `TM-EVAL-561`. Comment должен
объяснить, какие повреждения и дубликаты предотвращает hierarchy contract, не
выдавая contract-level проверку за завершённый релиз функции.

## User-visible acceptance

### Scenario A — допустимая связь и запрещённые parents

- В одном synthetic Project Task `Child` была успешно назначена дочерней для
  Task `Root`.
- Попытка затем назначить `Child` родителем для `Root` была отклонена как цикл.
- Попытка назначить для `Root` parent из другого Project также была отклонена.
- После обоих отказов исходная связь `Root → Child` осталась единственной и не
  изменилась.

### Scenario B — устаревший повтор создания subtask

- Для `Root` была создана новая subtask `Retry-safe child`.
- Повтор команды с прежней version parent был отклонён.
- В Project осталась ровно одна `Retry-safe child`; identifier sequence не
  создал второй номер для дубликата.
- Уже существующая `Child` не была отсоединена или изменена.

## Knowledge and authority boundary

- Evidence ограничено current accepted contract и локальным repository test;
  live release state не проверялся.
- Корневой Task Manager `AGENTS.md` по-прежнему предупреждает, что hierarchy не
  следует описывать как реализованную без отдельного актуального доказательства.
- Нельзя утверждать UAT/production availability, пользовательский rollout или
  release completion.
- Relations `blocks`, `related` и `duplicate_of` не проверялись.

## Audit-only evidence

- project refs `prj_eval_561_main_b415` и `prj_eval_561_other_9dd0`;
- task refs `tsk_eval_561_root_1a` и `tsk_eval_561_child_1b`;
- parent versions `12` и `13`;
- rejected cycle path `edge_eval_561_1b_to_1a`;
- cross-project target `tsk_eval_561_foreign_2c`;
- stale command correlation `cmd_eval_561_subtask_retry_04`;
- sequence reservation audit `seq_eval_561_73_only`;
- local test shard `tm-hierarchy-contract-02`.

## Accepted product source

Принятый hierarchy contract и его local repository evidence находятся в
read-only sources:

- `/workspace/Task Manager/AGENTS.md`;
- `/workspace/Task Manager/docs/specs/mvp.md`;
- `/workspace/Task Manager/docs/architecture.md`;
- `/workspace/Task Manager/tests/task-hierarchy.test.ts`.
