# Raw facts: review-completion-duplicate-evidence

Source project: Task Manager

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз Task Manager.

## Publication unit

Нужен один closing comment для вымышленной Task `TM-EVAL-611` перед переходом из
`In Review` в `Done`. В Task уже существует review-ready comment с исходным
результатом и длинным списком локальных проверок. Новый comment должен сохранить
новый material outcome review, а не повторить прежнюю техническую квитанцию.

## User-visible acceptance

### Scenario A — исходный результат уже опубликован

- Ранее опубликованный comment сообщает, что массовое перемещение сначала
  проверяет все выбранные Tasks и при конфликте не переносит ни одну.
- В нём уже перечислены локальная сборка, unit/integration/browser tests и
  отсутствие production release.
- Task после этого была переведена в `In Review`.

### Scenario B — независимая проверка нашла и закрыла дефект

- Reviewer обнаружил, что после конфликта повтор мог использовать устаревший
  список выбранных Tasks.
- Реализацию исправили: перед повтором список теперь читается заново.
- Повторная независимая проверка подтвердила, что конфликт по-прежнему не даёт
  частичного переноса, а после устранения конфликта повтор использует текущий
  список и выполняется один раз.
- Других material findings reviewer не оставил; Task всё ещё `In Review` и
  готовится closing comment перед `Done`.

## Knowledge and authority boundary

- Новый comment должен сохранить факт найденного и исправленного дефекта: это
  material incident, а не внутренний шум.
- Он не должен повторять неизменившийся список команд и проверок из предыдущего
  comment.
- Production не затрагивался; отдельного действия пользователя не требуется.

## Audit-only evidence

- предыдущий comment ref `cmt_tm_eval_611_review_07`;
- reviewer session `review_tm_eval_611_12`;
- initial SHA `4c0ed538864787b0c2fa8c3f3b83af35ee07c624`;
- fixed SHA `bd4a8b51ca325bd86f09d16b7dfd72bb5a246f1e`;
- команда `pnpm test -- bulk-move.retry.test.ts`;
- команда `pnpm playwright test bulk-move-conflict.spec.ts`;
- файлы `src/bulk/retry.ts`, `tests/bulk-move.retry.test.ts` и
  `e2e/bulk-move-conflict.spec.ts`;
- checks `typecheck`, `lint`, `unit 48/48`, `browser 6/6`;
- review disposition `clean-after-fix`.

## Accepted product source

Атомарность массового переноса и правило перечитывания выбора описаны в
read-only sources:

- `/workspace/Task Manager/docs/specs/bulk-move.md`;
- `/workspace/Task Manager/tests/bulk-move.retry.test.ts`;
- `/workspace/Task Manager/AGENTS.md`.
