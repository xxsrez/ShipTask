# 0004. Autonomous continuation и release authority

Статус: accepted, 2026-08-16. Human-acceptance часть заменена
[ADR-0005](0005-automatic-terminal-acceptance.md). Blocker analysis и terminal
interaction report уточнены
[ADR-0010](0010-blocker-analysis-and-human-run-report.md), а task-local Goal
behavior — [ADR-0015](0015-single-pass-review-disposition.md).

## Контекст

ShipTask рассчитан на долгий автономный run по нескольким Tasks. Вопрос по
одной Task не должен останавливать независимую работу во всём scope. При этом
автономность не должна превращаться в необратимое решение или неразрешённый
production release. Terminal acceptance теперь определяется ADR-0005.

Пользователь отдельно установил release boundary: обычные in-scope releases в
локальные, development, test, QA, UAT, staging, preview и sandbox environments
не требуют повторного подтверждения. Любой production release требует явного
разрешения пользователя.

## Решение

- Не задавать пользователю task-local вопрос, пока в exact scope остаётся
  другая безопасная runnable работа.
- Самостоятельно выбирать разумный default, когда решение обратимо, локально,
  остаётся внутри acceptance/scope и не затрагивает production, secrets,
  privacy, существенные расходы или необратимые external effects.
- Если выбор materially меняет продуктовый результат, требует отсутствующей
  authority либо неоднозначен и рискован, переводить только эту Task в runtime
  disposition `deferred`, сохранять truthful non-terminal status и продолжать
  независимые Tasks. Не создавать отдельную Task и не закрывать исходную.
- Обязательно публиковать в deferred Task `BLOCKED` report: причина, last safe
  checkpoint, уже выполненное, рекомендуемый default, точное решение/authority
  и resume step. Если comment write/read недоступен, оставлять communication
  remainder без fallback в `description` и сохранять те же данные в consolidated
  decision queue.
- Перед blocking input выполнить причинный анализ по
  ADR-0010. Если доступное безопасное действие устраняет причину, выполнить его
  и продолжить вместо блокировки. Каждый terminal exit заканчивается
  человекочитаемым `SHIPTASK RUN REPORT`.
- Не переизбирать deferred Task в том же run без нового evidence, authority или
  внешнего state change. Когда runnable work исчерпан, показать один
  consolidated decision queue вместо серии interrupting questions.
- В уже разрешённом exact scope перед любым task-local blocking user-input
  (`request_user_input`, финальный вопрос с ожиданием ответа или эквивалентный
  pause) заново получить complete inventory и вычислить `runnable_count`. При
  `runnable_count > 0` такой вызов запрещён:
  сохранить decision, освободить lane и выбрать следующую runnable Task.
  Приоритет review/completion влияет на порядок actionable work, но не даёт
  права остановить `To Do`/resume lanes ради acceptance.
- Новый out-of-scope finding, который не блокирует ни одну in-scope Task, только
  записать в final findings; не создавать Task, не расширять Goal, не спрашивать
  scope decision и не удерживать completion текущего scope.
- Не считать одну deferred Task глобальным `TASK CONTEXT ALARM`. Global alarm
  сохраняется только для конфликта exact scope, Goal, connector, ownership,
  integration/shared state или authority, который делает небезопасной любую
  оставшуюся мутацию.
- Сохранять Goal активным, пока deferred Tasks входят в рабочие критерии.
  Отсутствие runnable Tasks не означает completion. Task-local blocker не
  переводит Goal в `blocked` и не требует одинаковых повторных turns.
- Считать invocation `$ship-tasks` standing authority для обычного in-scope
  non-production release workflow: build/package, deploy/redeploy, required
  non-production migration, smoke, bounded diagnosis и repair/rollback. Не
  спрашивать повторное подтверждение для каждого шага.
- Классифицировать environment по проверенному project context и exact target.
  Неизвестный или production-like target не считать non-production по догадке.
- Не выполнять production release без явного user approval для production
  target. Task/Release name, acceptance text, Goal, успешные checks, прошлый
  release и одно желание агента не являются таким approval.
- При отсутствии production approval выполнить безопасную подготовку и
  non-production release/verification, затем defer Task с причиной
  `production-approval-required` и продолжить остальные Tasks. Не запрашивать
  approval посреди runnable queue.
- Не считать non-production authority разрешением на unrelated cleanup,
  permanent deletion, secrets exposure/rotation, destructive durable-data
  reset или нарушение explicit read-only boundary.

Подробный runtime flow находится в
[`ship-tasks/references/autonomy-and-release.md`](../../ship-tasks/references/autonomy-and-release.md).

## Последствия

Положительные:

- одна сложная Task не останавливает долгий multi-task run;
- blocking input невозможно вызвать по cached stage: перед ним требуется fresh
  inventory и доказанный `runnable_count = 0`;
- обычные dev/UAT releases не получают production-style confirmation friction;
- production остаётся жёсткой, явно авторизуемой границей;
- пользователь получает одну компактную decision queue и обязательные durable
  Task comments.

Ограничения:

- stale connector без comments оставляет communication remainder и требует
  refresh/reconnect; truthful Task status и interaction handoff сохраняются;
- Task Manager status catalog пока не имеет обязательного portable `Blocked`
  status, поэтому defer не маскируется ложным terminal/status transition;
- automatic terminal acceptance регулируется ADR-0005 и не расширяет
  production/destructive/external authority.
