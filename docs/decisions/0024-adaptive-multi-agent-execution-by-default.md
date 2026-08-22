# 0024. Automatic delegation и natural-language topology rules

Статус: accepted, уточнён 2026-08-22 по current Level 1. Частично заменяет
[ADR-0021](0021-requirements-as-agent-constitution.md): topology обычно остаётся
внутренним решением агента, но ShipTask имеет automatic default и обязан
исполнять однозначные пользовательские delegation rules свободным языком.
Topology rule может также изменить обязательность comment Explainer из
[ADR-0022](0022-mandatory-independent-strategic-explainer-for-comments.md).
Выбор model/effort уточнён
[ADR-0025](0025-cost-aware-subagent-profiles.md).

## Контекст

Когда пользователь ничего не задаёт, заранее выбранное постоянное число workers
не имеет устойчивого смысла: полезная ширина зависит от dependencies, mutable
surfaces, изоляции, runtime capacity и стоимости fan-in. Поэтому default должен
оставаться автоматическим.

Однако automatic default не отменяет пользовательское управление. Пользователь
может естественным языком задать точное число, попросить больше или меньше
субагентов, ограничить конкретную роль либо сформулировать условие по ожидаемой
длительности, сложности или другому наблюдаемому признаку. Coordinator обязан
сохранить смысл правила, а не свести любое указание к `auto` или только к
глобальному `off`.

Независимо от topology concurrent writers нельзя помещать в общий writable
checkout: каждому нужны собственные branch и worktree, а объединяет результат
один integration owner.

## Решение

### Default без user rule

- Если current prompt и применимый conversation context не задают topology
  rule, ShipTask сам определяет, где delegation полезна и сколько субагентов
  использовать.
- Число Tasks и свободных slots само по себе не создаёт useful work packet.
  Связанные writes и shared mutable state остаются последовательными;
  искусственные subtasks ради fan-out не создаются.
- Основной агент является единственным integration owner и владельцем Goal,
  Task Manager comments/status/version writes, целостного candidate и Task
  attribution.

### User topology rule

Однозначное правило пользователя имеет приоритет над automatic default. Оно
может выражаться любым естественным способом, например:

- exact count: «используй ровно три субагента»;
- relative direction: «используй побольше субагентов»;
- role scope: «без implementation-субагентов, но с reviewer»;
- condition: «используй субагентов, только если работа займёт больше получаса»;
- общий opt-out: «не используй субагентов».

Coordinator извлекает смысл, область действия и condition, комбинирует
совместимые правила и применяет их к current run. Root/coordinator не входит в
число, явно названное как количество субагентов. Позднее более конкретное
указание пользователя заменяет прежнее правило того же scope; независимые
constraints продолжают действовать.

Exact count является обязательным count, а не ceiling или пожеланием.
Qualitative direction исполняется по смыслу: например, «побольше» сдвигает
выбор к большему числу реально полезных lanes относительно automatic baseline,
но не создаёт фиктивную работу. Conditional rule применяется к той оценке или
наблюдаемому сигналу, который назвал пользователь; coordinator не заменяет
условие собственной другой метрикой.

Safety, authority, useful ownership, worktree isolation и возможность fan-in
сильнее topology preference. Если обязательное rule нельзя выполнить из-за
этих границ или runtime capacity, coordinator не подменяет его молча: он
называет конфликт, фактическую topology и влияние на result.

### Writer isolation

- Каждый одновременно пишущий implementation subagent до первой writable
  mutation получает собственную feature branch и собственный Git worktree для
  своей exact Task.
- Writable worktree принадлежит одному writer и не разделяется с другим
  implementation subagent. Writer не пишет в integration target, чужую branch
  или чужой worktree.
- Если writer/session остановились до fan-in, branch и worktree остаются
  task-owned checkpoint. После доказанной quiescence следующий writer или
  integration owner принимает тот же artifact; при active/unknown ownership
  параллельный takeover запрещён.
- Read-only scouts, reviewers и comment Explainer отдельного worktree не
  требуют.
- Только integration owner делает fan-in и проверяет exact объединённый
  candidate. Проверка isolated worktree не доказывает интегрированный result.

### Comment Explainer

Без применимого user rule каждый ShipTask comment проходит отдельного Strategic
Explainer. Общий opt-out отключает все subagents; role-scoped rule может
отключить только Explainer или, наоборот, сохранить его при запрете
implementation workers. Когда Explainer отключён пользователем, основной агент
применяет тот же quality contract напрямую и не заявляет независимую проверку.

### Наблюдаемость без scheduler-бухгалтерии

ShipTask сообщает effective user rule, когда оно задано, и честно показывает
material deviation или невозможность его выполнить. При automatic default
достаточно назвать materially важное использование delegation или limitation.
Внутренняя формула выбора, ready width и peak-width telemetry не обязательны.

## Проверяемые признаки

- Без user rule coordinator выбирает полезную delegation автоматически и не
  просит обязательную настройку scheduler.
- «Ровно три субагента» означает три subagents сверх root, если это возможно без
  нарушения жёстких границ; невозможность не скрывается.
- «Побольше субагентов» и conditional rule materially меняют default decision,
  а не игнорируются как неформальные слова.
- Role-scoped rule влияет только на названные роли; общий «не используй
  субагентов» запускает ноль subagents.
- Каждый concurrent implementation writer имеет уникальные branch и worktree;
  два writers не разделяют writable checkout.
- Отчёт подтверждает соблюдение или честное невыполнение user rule, но не
  превращается в обязательную numeric scheduler telemetry.

## Последствия

- Пользователь может управлять delegation теми словами и на той детализации,
  которые удобны в конкретном run.
- Automatic default остаётся удобным, когда пользователь topology не задаёт.
- Worktree isolation остаётся жёстким инвариантом для concurrent writes, не
  превращаясь в требование для read-only ролей.
