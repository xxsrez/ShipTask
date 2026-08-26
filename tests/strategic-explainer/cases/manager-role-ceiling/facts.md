# Raw facts: manager-role-ceiling

Source project: Task Manager

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Task Manager.

## Publication unit

Нужен один closing comment для вымышленной Task `TM-EVAL-511`. Task проверяет,
что Manager может вести обычный доступ команды, но не может передавать контроль
над Project или создавать равного себе Manager без участия Owner.

## User-visible acceptance

### Scenario A — обычное управление участниками

- Manager добавил уже зарегистрированного пользователя как Viewer.
- Затем Manager повысил этого участника до Editor.
- Пользователь сразу получил права Editor на Project и его Tasks.
- Остальные роли Project не изменились.

### Scenario B — защищённые полномочия владельца

- Manager попытался назначить другого участника Manager; операция была
  отклонена, и тот участник остался Editor.
- Manager попытался передать ему ownership; операция также была отклонена.
- Current Owner, список grants и доступ остальных участников остались без
  изменений после обоих отказов.

### Scenario C — действие владельца

- Owner назначил уже добавленного участника Manager.
- Owner передал ownership другому уже добавленному участнику.
- Новый владелец получил контроль немедленно, прежний Owner стал Manager; второго
  Owner не появилось.

## Knowledge and authority boundary

- Проверялись только Project roles для уже зарегистрированных пользователей.
- Email invitation, standalone Task sharing и global SavedView sharing не
  проверялись.
- Отклонённые Manager operations являются ожидаемой защитной границей.
- Production и реальные пользователи не затрагивались; Task ещё `In Review`.

## Audit-only evidence

- project ref `prj_eval_511_1c63`;
- owner identity projection `usr_eval_owner_511`;
- manager grant `agr_eval_511_mgr_v12`;
- participant grants `agr_eval_511_p1_v4` и `agr_eval_511_p2_v7`;
- ownership command correlation `cmd_eval_511_transfer_02`;
- rejected policy codes `role_ceiling_403` и `owner_only_403`;
- transaction marker `txn_eval_511_71f4`;
- repository snapshot suffix `d209bc`.

## Accepted product source

Принятая модель ролей и ownership transfer описана в read-only sources:

- `/workspace/Task Manager/docs/decisions/0005-project-roles-and-ownership-transfer.md`;
- `/workspace/Task Manager/docs/specs/mvp.md`;
- `/workspace/Task Manager/tests/access.test.ts`;
- `/workspace/Task Manager/tests/repository-integration.test.ts`.
