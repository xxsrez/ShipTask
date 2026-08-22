# 0024. Адаптивное multi-agent исполнение по умолчанию

Статус: accepted, 2026-08-22. Частично заменяет
[ADR-0021](0021-requirements-as-agent-constitution.md): topology обычно остаётся
внутренним решением агента, но для ShipTask пользователь явно потребовал
адаптивное использование нескольких субагентов по умолчанию и буквальный
opt-out. Также создаёт узкое исключение из
[ADR-0022](0022-mandatory-independent-strategic-explainer-for-comments.md), когда
пользователь запрещает любые субагенты для текущего run. Выбор model/effort для
этих lanes уточнён [ADR-0025](0025-cost-aware-subagent-profiles.md).

## Контекст

`batch-implementation` уже отличал массовую реализацию от single и release и
получал общий Goal, но не задавал execution topology. Поэтому большой scope мог
последовательно выполняться одним агентом даже при нескольких независимых
runnable Tasks и свободной безопасной capacity.

Фиксированное число workers не решает проблему: ширина меняется с dependencies,
пересечением writable surfaces, доступной изоляцией, стоимостью интеграции и
возможностью независимо проверить результат. Число Tasks или свободных slots
само по себе не доказывает полезный parallelism.

Отдельно фраза «не используй субагентов» должна означать ноль субагентов, а не
скрыто сохранять comment reviewer. Более узкий запрет, например «без субагентов
для реализации», относится только к названной роли.

## Решение

### Default — `subagents=auto`

- Если prompt не ограничивает delegation, ShipTask работает в
  `subagents=auto`.
- После live inventory агент выделяет независимые work packets и поддерживает
  active target, равный наименьшей из реально доступных ширин: dependency-ready
  work, conflict-free ownership/isolation, runtime capacity и способности
  интегрировать, проверить и review-ить результаты. Уменьшить target ниже этого
  значения можно только из-за конкретного observable limiting factor, который
  агент называет пользователю.
- Когда существуют минимум два безопасных полезных независимых packets и
  capacity это позволяет, одновременно работают несколько субагентов. Основной
  агент не поглощает такой frontier последовательно только ради простоты.
- Основной агент является единственным integration owner и владельцем Goal,
  Task Manager comments/status/version writes, сохраняя целостность общего
  candidate и Task attribution. Каждый implementation writer получает bounded
  ownership; пересекающиеся writes не выполняются параллельно.
- При одной безопасной write lane допускается один writer и параллельные
  read-only scouts/reviewers только для реальной независимой работы. Искусственные
  subtasks ради числа агентов не создаются.
- После завершения, blocker или открытия dependency frontier active target
  пересчитывается. Task-local blocker не оставляет другие безопасные lanes
  простаивать.

Эта политика применяется к любому delivery mode с несколькими независимыми work
packets; для `batch-implementation` она является обязательным default. В
сложной `single` или `release` агент использует субагентов, когда декомпозиция
даёт больше одной безопасной полезной lane, но не обязан создавать фиктивный
fan-out.

### Явный opt-out

- Общие формулировки «не используй субагентов», «без субагентов» и эквивалентное
  однозначное указание включают `subagents=off` на весь текущий run. ShipTask не
  запускает implementation, research, review или Strategic Explainer
  субагентов. Goal и lifecycle policy от этого не меняются.
- При `subagents=off` основной агент напрямую применяет quality contract
  Strategic Explainer к обязательному комментарию, проверяет факты и публикует
  его без ложного утверждения о независимом проходе. Это единственный
  no-subagent обход ADR-0022 и действует только из-за прямого указания
  пользователя.
- Узкий запрет относится только к названной роли. Например, «без субагентов для
  реализации» отключает writers/implementers, но сохраняет независимого
  Strategic Explainer для комментариев. Такое состояние сообщается как
  `subagents=auto; implementation=off`, а не как общий `off`.
- Пользователь может явно вернуть `subagents=auto` или задать более узкую
  topology-границу в том же run; последнее однозначное указание имеет приоритет.

Если worker capability технически недоступна, ShipTask снижает active target и
называет `workers=not-available`; это не приравнивается к пользовательскому
opt-out. Отдельная недоступность comment Explainer называется
`comment-explainer=not-available` и по ADR-0022 блокирует только comment-dependent
lifecycle effects.

### Наблюдаемость

Первый содержательный update после live inventory сообщает `subagents=auto` или
`subagents=off`, число ready independent lanes, active target и главный
ограничивающий фактор. Final report кратко сообщает фактически использованную
peak width либо причину coordinator-only исполнения. Это доказательство
применения выбранной политики, а не process diary.

## Проверяемые признаки

- Четыре независимые Tasks с изолированным ownership и достаточной capacity не
  исполняются одним агентом последовательно: одновременно активны несколько
  bounded workers и один integration owner.
- Большой scope с одной safe write lane не получает конфликтующих writers;
  полезные независимые read-only lanes всё ещё могут выполняться параллельно.
- При общем «без субагентов» число запущенных субагентов равно нулю, включая
  comment Explainer; при узком запрете отключены только названные роли.
- Goal, Task lifecycle, acceptance и authority boundaries одинаковы при
  `auto` и `off`.
- Отчёт не выдаёт доступные slots или большое число Tasks за доказательство
  фактически полезного parallelism.

## Последствия

- Большой независимый scope использует доступную multi-agent capacity без
  необходимости каждый раз просить workers вручную.
- Ширина остаётся адаптивной, поэтому shared state и integration backpressure
  естественно уменьшают число writers.
- Пользователь получает буквальный и проверяемый opt-out, включая существующее
  исключение для comment subagent.
