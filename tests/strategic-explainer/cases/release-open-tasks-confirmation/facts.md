# Raw facts: release-open-tasks-confirmation

Source project: Task Manager

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Task Manager.

## Publication unit

Нужен один closing comment для вымышленной Task `TM-EVAL-581`. Task проверяет
преднамеренный выпуск Release с открытой работой: система должна потребовать
явное подтверждение, но не должна автоматически закрывать Tasks.

## User-visible acceptance

### Scenario A — выпуск без подтверждения

- Release `1.0` находился в активном состоянии и содержал одну открытую Task
  `Finalize translations`.
- Editor попытался перевести Release в `Released` без подтверждения открытой
  работы.
- Система показала, что внутри остаётся 1 открытая Task, и отклонила переход.
- Release остался активным, дата выпуска не появилась, а Task не изменилась.

### Scenario B — осознанный выпуск

- Editor повторил переход и явно подтвердил, что Release выпускается с одной
  открытой Task.
- Release стал `Released` и получил дату выпуска.
- `Finalize translations` осталась открытой в том же статусе; система не
  перевела её в `Done` автоматически.
- Состав Release не изменился.

### Scenario C — устаревшее следующее изменение

- Вкладка со старым состоянием попыталась сразу перевести тот же Release в
  `Canceled`.
- Операция получила conflict и не изменила выпущенный Release, дату или Task.
- После read-back Release по-прежнему был `Released`, а Task — открытой.

## Knowledge and authority boundary

- Проверялись terminal transition, explicit confirmation и stale update одного
  synthetic Release.
- Comment не утверждает, что открытая Task завершена или что её можно игнорировать.
- Изменение состава уже выпущенного Release и production deploy не проверялись.
- Product-data lifecycle этого fixture не является Sites release; Task пока
  находится в `In Review`.

## Audit-only evidence

- project ref `prj_eval_581_c420`;
- release ref `rel_eval_581_10_12bd`;
- open task ref `tsk_eval_581_i18n_903c`;
- release versions `8` и `9`;
- confirmation request `cmd_eval_581_confirm_open_1`;
- released timestamp `2026-08-26T19:14:22Z`;
- stale request correlation `req_eval_581_cancel_v8`;
- sync cursor `sync_eval_581_001972`.

## Accepted product source

Release terminal confirmation и version guard описаны в read-only sources:

- `/workspace/Task Manager/docs/reference/domain-model.md`;
- `/workspace/Task Manager/docs/architecture.md`;
- `/workspace/Task Manager/docs/specs/mvp.md`;
- `/workspace/Task Manager/tests/release-lifecycle.test.ts`.
