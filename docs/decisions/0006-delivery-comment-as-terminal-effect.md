# 0006. Delivery comment как обязательный terminal effect

Статус: accepted, 2026-08-16. Заменяет capability-optional часть
[ADR-0003](0003-delivery-reports-as-task-comments.md); запрет fallback в Task
fields и формат отчёта из ADR-0003 сохраняются. Обработка unavailable channel
до/после mutations уточнена
[ADR-0009](0009-terminal-report-capability-preflight.md).

## Контекст

ADR-0003 разрешал завершать Task без delivery comment, потому что проверенный
тогда Task Manager connector не предоставлял native comment write. На
2026-08-16 live `tools/list` существующего Task Manager UAT уже публикует
`list_task_comments`, `get_task_thread`, `add_task_comment` и связанные native
comment tools. Пользователь отдельно потребовал, чтобы выполненная или
остановившаяся работа всегда оставляла понятный durable отчёт прямо в Task.

Optional policy приводила к невидимому разрыву: source result и status могли
стать terminal, но review context оставался только в чате Codex. После закрытия
Task пользователю было невозможно восстановить, что сделано, как устроено и чем
проверено, не находя исходный run.

## Решение

- Для каждой изменённой рабочей Task `COMPLETED` native comment является
  обязательным terminal effect. Публиковать и перечитывать его после полного
  result/evidence/external-effect gate и до перехода Task в `Done`.
- При material rework, failure или defer публиковать `REWORK REQUIRED`, `FAILED`
  или `BLOCKED` comment с impact, checkpoint, evidence, cause/confidence,
  recovery, remaining risk и точным resume/decision step.
- Report остаётся task-specific, idempotent и comments-only. Использовать
  стабильный report key/idempotency key, искать эквивалентный report перед
  повтором и выполнять read-back после write. Никогда не менять `description`,
  acceptance, status text или другой Task field ради отчёта.
- Если comment create/list/read отсутствует на preflight, остановить delivery до
  Goal и mutations по ADR-0009. Если channel потерян или write нельзя
  reconciliate через read-back уже после mutation, сохранить truthful
  non-terminal statuses, прекратить новый dispatch и явно показать
  `comment-delivery-unavailable`/`write-outcome-unknown` в scope-wide blocker
  ledger.
- Automatic acceptance остаётся автоматической, но последовательность теперь
  фиксирована: terminal evidence → published/read-back `COMPLETED` → `Done` →
  Task reread. Отдельная пользовательская приёмка по-прежнему не нужна.
- Для non-trivial/cross-component результата включать одну-две полезные
  text/Markdown diagrams; для trivial change использовать compact before/after.
  Mermaid допустим только при доказанной поддержке renderer.
- Standing authority на verified non-production release из ADR-0004 не
  меняется. Production и destructive/secret/privacy/external boundaries
  остаются отдельными approval gates.

## Последствия

Положительные:

- Task становится самодостаточной review surface с результатом, техническим
  объяснением, evidence и ограничениями;
- ShipTask больше не может молча закрыть Task при stale plugin/tool snapshot;
- статус и durable delivery context reconciliate как два обязательных слоя.

Ограничения:

- устаревшая сессия Codex без comment tools должна оставить Task non-terminal и
  продолжить после refresh/reconnect, даже если code/effect уже готовы;
- comment write и status update остаются неатомарными, поэтому между ними нужен
  явный read-back и recovery;
- это решение не backfill-ит старые terminal Tasks без отдельного запроса.
