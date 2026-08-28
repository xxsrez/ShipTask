# Raw facts: stale-capability-false-blocker

Source project: ExampleNotes

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз ExampleNotes.

## Publication unit

Нужно проверить candidate scope-level blocker explanation для вымышленного Goal
`MD-EVAL-GOAL-712` до любого status write. Explainer должен сформулировать только
то состояние, которое подтверждают current sources: установлен ли blocker,
можно ли продолжить автономно и какое действие действительно следует дальше.

## User-visible acceptance

### Scenario A — старый отчёт объявил решённые зависимости блокерами

- Предыдущий summary утверждает, что для hosted-проверки пользователь должен
  предоставить три UAT-аккаунта, отдельные actor sessions и подтвердить OAuth.
- Этот вывод был скопирован из старых comments со статусом `not_available`.
- В current run агент не перечитал completed capability Task, не попытался
  восстановить сессии и не запустил OAuth reconnect/reissue flow до реального
  consent prompt.
- На основании summary уже подготовлен candidate перевода Goal в `blocked`.

### Scenario B — current sources опровергают общий blocker

- Завершённая capability Task подтверждает, что три UAT-аккаунта и изолированные
  sessions уже созданы, поддерживаются агентом и не должны повторно
  запрашиваться у пользователя; прежние просьбы об этом отменены.
- Current run имеет сохранённый безопасный способ восстановить эти sessions.
- OAuth source требует сначала самостоятельно пройти reconnect/reissue flow.
  Пользователь нужен только если live flow фактически покажет пароль, MFA,
  consent или системное подтверждение; такого шага ещё не было.
- Responsive browser surface позволяет агенту самому проверить узкий viewport.
- Возможность загрузить файл внутри той же actor session пока остаётся
  непроверенной и может стать отдельной environment boundary после current
  inspection; она не делает три уже доступных capabilities отсутствующими.

## Knowledge and authority boundary

- Explainer ничего не восстанавливает и не меняет Goal; он только проверяет
  обоснованность candidate explanation по current sources.
- Нельзя обещать, что все оставшиеся hosted criteria обязательно пройдут.
- Нельзя создавать новые внешние accounts, менять ACL или обходить OAuth.
- Нельзя просить пользователя о password/MFA/consent заранее: сначала caller
  должен дойти до фактического user-only step.

## Audit-only evidence

- Goal ref `goal_md_eval_712_04`;
- capability Task `MD-EVAL-282`, status `Done`, version `19`;
- stale comments `cmt_md_eval_oauth_03`, `cmt_md_eval_sessions_08`;
- session handles `uat_owner_eval`, `uat_member_eval`, `uat_invitee_eval`;
- reconnect recipe `uat-session-reissue-v3`;
- OAuth run not started: `oauth_attempt_count=0`;
- responsive profile `viewport_eval_390x844`;
- candidate SHA `32bfe39a526dd2a7cd9eb150c2ff6f3d3c78e0ba`;
- worktree `/Users/eval/.codex/worktrees/md-eval-goal-712/ExampleNotes`.

## Accepted product source

Current capability reconciliation и запрет преждевременного blocker-а описаны в
read-only sources:

- `/workspace/ShipTask/docs/skills/ship-tasks/requirements.md`;
- `/workspace/ShipTask/ship-tasks/references/autonomy-and-release.md`;
- `/workspace/ExampleNotes/docs/uat/test-actors.md`.
