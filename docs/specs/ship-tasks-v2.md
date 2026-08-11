# Ship Tasks v2

Статус: proposal, 2026-08-11.

Документ описывает следующую версию `$ship-tasks`. Он не утверждает, что
текущий `ship-tasks/SKILL.md` уже реализует review queue или обязательную
human acceptance.

## 1. Результат

Skill должен довести exact task scope от утверждённого planning handoff до
одного проверенного terminal outcome. Машинные проверки, agent review и
человеческая приёмка являются разными слоями evidence.

## 2. Planning handoff

До execution пользователь или authoritative project process должен определить:

- stable identity scope и полный список in-scope tasks;
- acceptance и terminal done criteria;
- dependencies и boundary dependencies;
- разрешённые writes, integration authority и destructive boundaries;
- verification contract и обязательные external effects;
- human acceptance authority;
- execution topology и review WIP limit, когда используется parallel mode.

Skill может read-only найти уже существующие сведения, но не должен
самостоятельно превращать неоднозначное пожелание в writable scope. При
неполном или противоречивом handoff применяется `TASK CONTEXT ALARM`.

## 3. Состояния

Нормативный lifecycle одной task:

```text
planned
→ ready
→ running
→ machine-verified
→ review-ready
→ human-accepted
→ terminal
```

Возврат на доработку:

```text
review-ready
→ changes-requested
→ rework
→ machine-verified
→ review-ready
```

`terminal` разрешён только после human acceptance, выполненной integration,
обязательных external effects и достаточного evidence. Project task state
может иметь другие названия, но adapter должен сохранять эту семантику без
ложного round-trip.

## 4. Preflight dispositions

До мутаций skill должен выбрать ровно одну disposition:

| Disposition | Значение |
|---|---|
| `work-remains` | Есть готовая или потенциально готовая незавершённая работа. |
| `completion-remains` | Код или иной результат существует, но не интегрирован, не принят или не доведён до обязательного effect. |
| `resume` | Найден coherent checkpoint текущего scope и доказана authority продолжения. |
| `no-work` | Scope уже terminal по текущим authoritative sources. |
| `conflict` | Scope, owner, state или evidence неоднозначны либо противоречат друг другу. |

`no-work` не разрешает создавать пустой commit, повторять дорогой gate или
производить внешний effect только ради свежего отчёта.

## 5. Execution topology

Default — serial coordinator без лишних workers и worktrees. Parallel mode
включается только для независимых writable scopes с отдельными execution
surfaces и доказанной coordination authority.

Для `workers=N` skill обязан отдельно показывать:

- `requested_workers`;
- `available_capacity`;
- `active_target`;
- фактически sustained lanes;
- причину idle capacity.

```text
active_target = min(
  requested_workers,
  dependency_ready_tasks,
  isolated_execution_capacity,
  available_review_buffer
)
```

Низкий `active_target` из-за dependency frontier или заполненной review queue
является backpressure, а не скрытым изменением запроса. Если runtime не может
поддержать exact requested topology, skill останавливается до dispatch.

## 6. Layered verification

Каждый candidate проходит три независимых слоя:

1. deterministic checks — tests, lint, typecheck, security и project gates;
2. independent agent review — regressions, scope, architecture и missing tests;
3. human acceptance — продуктовый смысл, архитектурные tradeoffs и решение
   принять либо вернуть.

Agent review не получает mutation authority. Findings исправляет обычный
writer, после чего повторяются затронутые deterministic checks.

## 7. Review-ready queue

Review queue содержит логически цельные candidates, а не сырые worker reports.
Каждый candidate имеет stable identity и связан с exact base/result.

WIP limit задаётся invocation или authoritative project context. Пока он
достигнут:

- новый ordinary dispatch прекращается;
- running work доводится только до безопасной project-defined boundary;
- recovery, reconciliation и urgent in-scope repair остаются возможны;
- свободные worker slots не считаются причиной обходить backpressure.

Skill должен группировать routine tasks по общей product/code surface, но не
скрывать risky или decision-required work внутри большого batch.

## 8. Review packet

Review packet должен помещаться в один компактный экран и содержать:

- exact tasks и candidate identity;
- что изменилось и зачем;
- существенные решения, риски и известные ограничения;
- scope diff;
- deterministic checks и independent review;
- быстрый способ проверить результат;
- recommendation: accept или changes requested.

После `changes-requested` следующий packet показывает delta относительно
предыдущего candidate: исправленные замечания, новый diff, повторённые checks и
оставшиеся gaps. Полный контекст доступен по ссылке, но не повторяется без
необходимости.

## 9. Risk routing

Минимальные классы:

| Класс | Маршрут |
|---|---|
| `routine` | Группировать в связный review batch. |
| `risky` | Отдельный packet и явные risks. |
| `decision-required` | Остановиться до implementation и запросить решение. |
| `mechanically-verifiable` | Не делать отдельный interrupt, но включить в итоговую acceptance. |

Defect автоматически исправляется только когда acceptance или project policy
уже включает его в текущий scope. Иначе требуется scope decision.

## 10. Resume и durability

Текст skill сам по себе не является durable scheduler. Для cross-session queue,
claims, controls и metrics нужен project runtime/helper с:

- stable run/candidate/task identities;
- compare-and-swap либо эквивалентной writer authority;
- idempotent controls и external-effect receipts;
- reconciliation с Git, task source и внешними системами;
- explicit handoff/takeover/fencing semantics.

До появления такого runtime v2 не должна обещать точные долговременные метрики
или background reaction после остановленного model turn.

## 11. Completion

Completion требует:

- zero unfinished in-scope tasks и unresolved in-scope defects;
- zero unaccepted review-ready candidates;
- интегрированные human-accepted results;
- exact final result identity;
- final project checks на exact result;
- independently verified mandatory external effects;
- task-source projection, соответствующую фактам;
- reconciled Goal/run/journal state, когда они применимы.

Финальный отчёт разделяет task state, source/integration identity, checks,
human acceptance, external effects и gaps. Ни один слой не доказывает другой.

## 12. Non-goals

- Не реализовывать в `SKILL.md` полноценную persistent queue или high-load
  scheduler.
- Не зашивать конкретный task manager, Git policy, provider или environment.
- Не устранять human acceptance ради формального terminal status.
- Не максимизировать число активных agents без учёта review throughput.
