# 0005. Automatic terminal acceptance

Статус: accepted, 2026-08-16. Заменяет human-acceptance часть ADR-0004.
Порядок обязательного delivery comment перед `Done` уточнён ADR-0006.

## Контекст

ShipTask должен автономно доводить scope до terminal outcome. Реальный run
полностью проверил и выпустил exact result в UAT, но оставил девять Tasks в
`In Review`, трижды потребовал от пользователя фразу о приёмке и затем пометил
Goal `blocked`. Такой gate не добавил evidence: пользователь ожидает проверить
готовый результат позже и при обнаруженном defect reopen-нуть Task либо создать
новую проблему.

После первоначального исправления новый run загрузил уже обновлённый skill, но
также получил более старую memory-запись, требующую explicit acceptance. Он
выбрал historical record, снова запросил фразу для трёх Tasks и после третьего
goal-turn пометил Goal `blocked`. Значит, одного положительного правила
automatic acceptance недостаточно: нужен явный retirement старого контекста.

## Решение

- Считать invocation `$ship-tasks` standing authority для automatic acceptance
  exact result после полного terminal evidence: выполнены Task acceptance
  criteria, targeted gate, applicable review-batch gate, integration и required
  non-production/runtime effects; unresolved in-scope findings отсутствуют.
- Не вызывать `request_user_input`, не задавать финальный вопрос, не создавать
  `acceptance-required`, не удерживать Task в `In Review` и не переводить Goal в
  `blocked` только ради ручной приёмки.
- Считать `In Review` actionable completion stage. После passing evidence
  опубликовать и перечитать обязательный `COMPLETED` report, затем перевести
  Task в `Done`, выполнить Task read-back и продолжить scope.
- При failed/insufficient evidence автоматически выполнить разрешённый
  rework/retest. Defer использовать только для конкретного material decision,
  отсутствующей внешней authority или state change, а не как surrogate ручной
  приёмки.
- Не публиковать `ACCEPTANCE READY`. Batch/review packet остаётся evidence и
  human-readable explanation, но не blocking decision surface.
- После `Done` считать user-initiated reopen authoritative сигналом rework.
  Созданная пользователем новая Task является новым обычным scope. Старые
  reports/checks при следующем запуске являются historical checkpoint, не proof
  текущего состояния.
- Не считать automatic acceptance разрешением на production release,
  destructive durable-data action, secrets/privacy mutation, external-recipient
  action или обязательный approval внешнего approver. Эти границы сохраняют
  собственные reason codes и authority requirements.
- Считать `acceptance criteria` объективными Task completion criteria, а не
  запросом human sign-off. Project/Release/Task context не может настроить
  manual product acceptance для `$ship-tasks`.
- Считать любое прежнее требование human acceptance из memory, rollout summary,
  старого report/Goal/plan или cached project context superseded historical
  evidence. Оно не создаёт current authority, blocker или decision queue.
- При resume старого Goal, заблокированного только ручной приёмкой, отбросить
  retired blocker, повторно проверить exact evidence и автоматически завершить
  passing Tasks. Не повторять blocker threshold для этой причины.

## Последствия

Положительные:

- полностью проверенный scope завершается без холостого user round-trip;
- Goal не зависает и не становится `blocked` после успешной доставки;
- `In Review` перестаёт быть ручной очередью приёмки;
- пользователь сохраняет простой feedback loop через reopen/new Task.
- stale runtime context больше не может вернуть удалённый human gate.

Ограничения:

- automatic acceptance требует всего evidence set, а не только green tests;
- material product ambiguity и настоящая external authority всё ещё могут
  defer-нуть конкретную Task;
- escaped defect после `Done` создаёт новый rework cycle и не переписывает
  прошлое completion evidence задним числом.
