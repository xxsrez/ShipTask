# Raw facts: unfinished-release-vague-handoff

Source project: ExampleNotes

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз ExampleNotes.

## Publication unit

Нужен один итоговый отчёт вымышленного Release `MD-EVAL-REL-819`. Release ещё не
завершён. Вызов не имеет Goal: это не отменяет обязанность объяснить остановку и
не разрешает скрыть причины в source basis.

## User-visible acceptance

### Scenario A — доступная работа запрещает terminal stop

- Task `MD-EVAL-819` остаётся `In Review`: размещённый маршрут
  `connector-object` не объявлен текущим UAT deployment.
- Fresh capability read-back вернул `not_available/none/none` до provider flow.
- Current Task comment и repository runbook называют следующий шаг внутри
  scope/authority агента: восстановить и развернуть exact hosted wiring, затем
  повторить UAT.
- Это доступная реализация/redeploy frontier, а не доказанная external
  prerequisite. Итог не вправе утверждать, что безопасная автономная работа
  исчерпана; он должен вернуть caller к этой работе.

### Scenario B — два настоящих препятствия нельзя склеить в категории

- `MD-EVAL-844` и `MD-EVAL-854` требуют наблюдения одного сценария в двух
  независимых авторизованных пользовательских сессиях.
- Агент повторно использовал owner session и проверил доступные session/reconnect
  paths, но не имеет полномочий создать вторую внешнюю identity. Следующее
  условие принадлежит пользователю: предоставить вторую тестовую учётную запись.
  Сигнал возобновления — обе identities одновременно видны в своих сессиях.
- `MD-EVAL-863` отдельно требует загрузить синтетический файл в той же
  авторизованной Browser session. Агент создал файл и дошёл до живой вкладки, но
  current in-app Browser не предоставил управление file chooser. Это условие
  принадлежит среде Codex, а не пользователю. Сигнал возобновления — файл выбран
  и прочитан приложением в той же session.
- Причина, владелец действия и resume signal у двух групп различаются. Формулировка
  «нужны несколько участников и ограниченное действие в Browser» теряет эту
  разницу и не является publication-ready.

## Knowledge and authority boundary

- Explainer не меняет статус, не продолжает работу и не решает, что Release
  blocked; он отражает current evidence для caller-а.
- Создавать внешнюю identity или менять access policy нельзя.
- Нельзя объявлять product defect только из-за отсутствия Browser control.
- Нельзя просить пользователя о Browser capability, принадлежащей среде.

## Audit-only evidence

- Release ref `release_md_eval_819_03`;
- candidate SHA `804c9ea3d7f49bbbe377847b38444454e1be352a`;
- UAT version `v819`, deployment `dep_md_eval_819_44`;
- capability tuple `not_available/none/none`;
- command `pnpm test -- terminal-handoff-regression.test.ts`;
- worktree `/Users/eval/.codex/worktrees/md-eval-819/ExampleNotes`.

## Accepted product source

Terminal handoff и причинное покрытие описаны в read-only sources:

- `/workspace/ShipTask/docs/skills/ship-tasks/requirements.md`;
- `/workspace/ShipTask/docs/skills/strategic-explainer/requirements.md`;
- `/workspace/ShipTask/ship-tasks/references/run-report.md`.
