# Raw facts: blocked-goal-causal-report

Source project: ExampleNotes

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз ExampleNotes.

## Publication unit

Нужен один scope-level blocker report для вымышленного Goal
`MD-EVAL-GOAL-611`. Report готовится после полного чтения Release и до записи
Goal status `blocked`. Он должен объяснить, почему весь текущий объём нельзя
честно завершить сейчас и при каком наблюдаемом условии работа возобновится.

## User-visible acceptance

### Scenario A — автономная работа исчерпана

- В синтетическом Release восемь Tasks: четыре завершены, четыре остаются в
  `In Review`; runnable implementation и rework больше нет.
- Exact candidate собран, интегрирован, выпущен в закрытую hosted UAT и прошёл
  доступные автоматические проверки.
- Для четырёх оставшихся критериев нужно прямое наблюдение поведения в разных
  hosted пользовательских контекстах; локальная проверка и code review не
  доказывают эти критерии.
- Дефект продукта не установлен. Известна только граница доказательства.

### Scenario B — внешние prerequisites разделены по владельцу

- Пользователь может подтвердить повторное OAuth consent и предоставить три
  независимые тестовые actor sessions.
- Текущая среда выполнения должна отдельно дать управляемый узкий viewport и
  загрузку файла внутри той же авторизованной actor session.
- Перечень из четырёх prerequisites является следствием одной причины: запуск
  не может создать и наблюдать требуемые разные hosted контексты с сохранением
  их identity и input, поэтому оставшаяся пользовательская приёмка сейчас не
  доказуема.
- После появления этих контекстов первый безопасный шаг — повторить один
  representative hosted scenario; видимый корректный результат в нужной actor
  session является сигналом возобновления полного acceptance pass.

## Knowledge and authority boundary

- Report не должен утверждать, что Goal уже `blocked`: status write выполняется
  только после готового report и factual check.
- Отсутствие hosted evidence нельзя назвать product failure или неготовностью
  candidate.
- Не все prerequisites являются действием пользователя; viewport и file upload
  принадлежат возможностям среды выполнения.
- Нельзя обещать завершение Release до фактической hosted проверки.

## Audit-only evidence

- Goal ref `goal_md_eval_611_77`;
- Release ref `release_md_eval_611_03`;
- remaining Task refs `MD-EVAL-701`, `MD-EVAL-702`, `MD-EVAL-703`,
  `MD-EVAL-704`;
- candidate SHA `7f4b1f2020bf837cab2666874c0289287aa5474e`;
- UAT version `v611`, deployment `dep_md_eval_611_44`;
- actor session keys `actor_eval_owner`, `actor_eval_member`,
  `actor_eval_invitee`;
- внутренние capability labels `oauth-reconsent`, `multi-actor-session`,
  `narrow-viewport-control`, `same-session-file-upload`;
- команда проверки `pnpm test -- hosted-acceptance-boundary.test.ts`;
- worktree `/Users/eval/.codex/worktrees/md-eval-goal-611/ExampleNotes`.

## Accepted product source

Причинный blocker-report и граница hosted acceptance описаны в read-only
sources:

- `/workspace/ShipTask/docs/skills/ship-tasks/requirements.md`;
- `/workspace/ShipTask/ship-tasks/references/run-report.md`;
- `/workspace/ExampleNotes/AGENTS.md`.
