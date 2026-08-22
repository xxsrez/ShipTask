# ShipTask: требования пользователя

Статус: current Level 1, 2026-08-22.

Этот документ — полный пользовательский исходный код только для
`$ship-tasks`. Он не определяет требования к Task Composer или Strategic
Explainer; их использование ниже является локальной dependency ShipTask.

Требования задают обязательный outcome, rationale, observable evidence и
scope/truth/safety/authority boundaries. Architecture и runtime могут
переформулировать и конкретизировать их, но не могут ослабить, заменить или
молча удалить. Изменение смысла Level 1 требует явного решения пользователя.
План, decomposition, tools, число попыток, context и внутренний reasoning
остаются свободными, если точный механизм не назван здесь отдельным инвариантом.

`architecture.md` хранит agent-owned current способ достижения этих требований.
`ship-tasks/SKILL.md` является компактной смысловой компиляцией обоих файлов.
Если runtime удалить и пересобрать из них, новый skill должен быть примерно
эквивалентен по всем требованиям `ST-*` и выбранной архитектуре.

## Требования

### `ST-01` — Exact Task Manager scope

ShipTask доставляет только однозначно выбранный Task Manager scope. Обычная
просьба изменить код или продукт без Task Manager anchor не запускает ShipTask.
Task Manager остаётся единственным authoritative task source; memory, chat,
Goal, Git и планы не заменяют current Task state. Явный `$ship-tasks` и
однозначный natural-language delivery intent используют одну policy; чтение,
status, audit, explanation, planning и backlog capture delivery не запускают.
Если exact selector, обязательная adapter capability или общая authority не
разрешены достаточно для безопасной mutation, ShipTask останавливает writes с
понятным `TASK CONTEXT ALARM`, а не угадывает scope.

### `ST-02` — Полный проверенный результат

ShipTask доводит in-scope работу до фактически доказанного результата либо
оставляет её честно незавершённой с понятной причиной. Он не останавливается на
написанном коде, зелёном тесте, worker report, deploy или status отдельно, если
полный Task outcome и обязательные effects ещё не доказаны.

### `ST-03` — Fresh evidence и правдивое состояние

Scope, acceptance, dependencies, comments, versions, access, result identity и
external effects перечитываются настолько свежо, насколько требует решение.
Прошлый run и сохранённая память не выдаются за current evidence. Task status,
comments и финальный ответ должны соответствовать установленным фактам. Task
Manager, Git candidate, checks, deployment, access policy и другой внешний
effect являются разными proof domains: состояние одного не доказывает другое.

### `ST-04` — Backlog вне delivery

Tasks в `Backlog` являются будущей запланированной работой и не входят в
ShipTask delivery inventory. ShipTask не начинает их реализацию и не переводит
их из `Backlog` без отдельного явного пользовательского решения о начале этой
работы.

### `ST-05` — Evidence важнее выбранного способа

Агент сам выбирает implementation, diagnostics, tools и acceptance method.
Сбой одного средства не делает его обязательным для repair и сам по себе не
доказывает product defect или verification blocker. Acceptance нельзя ослаблять,
а недоступное или непроведённое нельзя называть verified.

### `ST-06` — Правдивый lifecycle и durable comments

Существенное lifecycle решение получает понятный native Task Manager comment,
его read-back и только затем связанный status effect. Ответ в Codex, Goal,
description или внутренний reason code comment не заменяет. Обычный старт
`To Do → In Progress` сам по себе не создаёт комментарий. Report остаётся в
comments и не превращает Task description или другое поле в journal/fallback.
Unknown или failed comment write сначала reconciles; пока обязательный comment
не доказан, зависящий существенный transition не выполнен.

### `ST-07` — Независимое человеческое объяснение

Если пользователь не задал иное применимое topology rule, каждый comment,
который создаёт ShipTask, проходит отдельного независимого Strategic Explainer.
Основной агент сохраняет ответственность за факты и решение, но не подменяет
независимый проход собственной стилистической самооценкой. Пользователь может
свободным языком изменить эту topology, в том числе запретить всех субагентов
или только comment Explainer. При отключённом Explainer основной агент напрямую
применяет тот же quality contract без ложного claim о независимости. Если
effective rule сохраняет Explainer, но он недоступен или непригоден, comment и
зависящий transition остаются незавершёнными, а другая независимая безопасная
работа может продолжаться.

### `ST-08` — Видимый acceptance incident

Доказанный defect, task-contract conflict или невозможность провести приёмку
становятся видимы человеку сразу, сохраняются в Task history и не исчезают из
итогового объяснения после repair. Только прямое нарушение acceptance называется
bug; граница доказательства называется честно. Opening incident сообщается до
repair, unresolved incident остаётся виден в progress и следующем run, а
found-and-resolved incident сохраняется в resolution comment и final ledger —
успешный итог не стирает историю существенной проблемы.

### `ST-09` — Automatic acceptance по фактам

Доказанно готовая Task автоматически завершается без отдельного ритуала ручной
приёмки. Feedback после завершения возвращается через reopen или новую Task.
Automatic acceptance не расширяет production, destructive, privacy, secrets,
access-policy, external-recipient или cost authority.

### `ST-10` — Независимая работа не простаивает

Изолированная проблема одной Task не останавливает другие безопасные runnable
Tasks. Глобальная остановка допустима только когда scope, shared state или
authority делают любую оставшуюся mutation небезопасной. Пока runnable work
существует, ShipTask не прерывает run серией task-local вопросов: он сохраняет
правдивый handoff конкретной Task, освобождает lane и продолжает. Когда runnable
work исчерпан, человеку даётся одна consolidated decision boundary. Новый
out-of-scope finding не реализуется, не превращается автоматически в Task и не
расширяет текущий Goal.

### `ST-11` — Natural-language topology и automatic default

При нескольких действительно независимых полезных lanes ShipTask по умолчанию
использует доступных субагентов и одного integration owner. Parallelism
ограничивается dependencies, конфликтами ownership, доступной изоляцией и
способностью интегрировать и проверить результат; фиктивные subtasks ради числа
агентов не создаются. Если пользователь не задал topology rule, количество и
роли субагентов ShipTask определяет автоматически по реальной работе и доступной
capacity, не требуя от пользователя настройки scheduler.

Пользователь может свободным языком задать обязательное правило delegation:
точное или относительное количество (`ровно три`, `побольше`), разрешённые или
запрещённые роли, общий opt-out либо условие (`используй субагентов, только если
работа займёт больше получаса`). Coordinator сохраняет смысл такого правила,
комбинирует совместимые ограничения и применяет его к current run; root agent не
входит в число явно названных субагентов. Позднее более конкретное указание
пользователя имеет приоритет над default и прежним правилом того же scope.

Safety, authority, реальная полезность work packets, worktree isolation и
integrability остаются жёсткими границами: coordinator не создаёт фиктивную
работу ради quota и не нарушает изоляцию ради числа. Если обязательное правило
нельзя выполнить из-за конфликта этих границ или недоступной capacity, оно не
подменяется молча — пользователь получает конкретную границу и фактическую
topology. Отчёт не обязан показывать внутренний расчёт target/width; достаточно
правдиво сообщить materially важное применение или невыполнение user rule.

### `ST-12` — Изоляция concurrent writers

Каждый одновременно пишущий implementation subagent работает в собственном Git
worktree и собственной feature branch для своей exact Task. Writable worktree
принадлежит ровно одному implementation writer и не разделяется между
субагентами; writer не пишет в integration target, worktree или branch другой
Task. Read-only scouts, reviewers и comment Explainer отдельного worktree не
требуют. Единственный integration owner делает fan-in и проверяет exact
интегрированный result.

### `ST-13` — Пользователь управляет model profile

Явный выбор пользователем model/effort для всех или отдельных subagents имеет
приоритет и не подменяется молча. Без override дешёвый профиль допустим только
для genuinely simple bounded work без material judgment или risk; uncertainty
возвращается current profile без цикла дешёвых повторов. Автоматический дешёвый
профиль — именно `gpt-5.6-luna`/`max`, а не пониженный effort. Большинство
packets и Strategic Explainer наследуют current profile; ShipTask не повышает
его скрыто до Sol и не заменяет exact unavailable override приблизительным.
Profile allocation и Luna-to-current escalation остаются наблюдаемыми, но не
подменяют evidence результата.

### `ST-14` — Goal только для массовой имплементации

Goal используется для прогресса реальной implementation/rework минимум двух
concrete Tasks. Одна Task и release уже подготовленного candidate работают без
нового Goal независимо от Project/Release selector. Goal не определяет Task
outcome и не превращает task-local blocker в глобальный; он остаётся active,
пока fresh full inventory содержит незавершённую in-scope implementation или
обязательные remnants/effects, и завершается только после Task-level truth.
Release-only run не создаёт, не ретаргетит и не завершает Goal ради самого
release.

### `ST-15` — Release authority

Нужные in-scope non-production effects выполняются и проверяются без лишнего
confirmation ritual после надёжного определения target. Production и другие
sensitive effects требуют явной authority для exact target. Один deploy или
Task Manager state не доказывает другой внешний результат. Environment нельзя
выводить из Task/Release title, прошлого deploy, URL или наличия tool; unknown
или production-like target не считается non-production. Production approval не
разрешает unrelated cleanup, destructive durable-data change, secrets/privacy/
access-policy mutation, external recipient или unbounded cost.

### `ST-16` — Переносимый общий skill

Generic ShipTask не зашивает repository path, Project/Release refs, provider,
environment, URL, команды или project-specific production policy. Такой context
берётся из current project sources. Project memory хранит selectors/profile и
меняется только по явной просьбе; она не хранит live Task state, не создаёт
implicit anchor задним числом и не является approval. Prompt selector имеет
приоритет только для current run и не переписывает memory молча.

### `ST-17` — Безопасное имя новой Codex task

Если ShipTask доказанно является первым запросом новой Codex task с catalog
placeholder, она получает короткое содержательное имя после live scope
resolution. Meaningful или уже изменённое название не перезаписывается, а
неуверенная identity не угадывается. Failure rename не блокирует delivery.

### `ST-18` — Outcome-first handoff

После failure или незавершённого результата человек без дополнительных
уточняющих запросов получает понятную причинную картину: что остановилось,
первичную и каскадные причины, что уже сделано и не проверено, влияние,
необходимое действие и точное условие продолжения. Любой terminal exit, включая
success и no-work, начинается с observable outcome и отделяет факты от
inference; reason codes, tools и process diary остаются только когда помогают
понять или проверить вывод.

### `ST-19` — Lifecycle priority и duplicate context

`Backlog`, `To Do`, `In Progress`, `In Review` и terminal statuses сохраняют
разный смысл. В пределах одной safe lane незавершённый `In Progress` и готовый
к completion `In Review` reconciliate раньше новой `To Do`, но это не запрещает
параллельно начинать независимую работу. `Duplicate` не выполняется отдельно:
исходящая canonical relation и входящие duplicates читаются как полный контекст
проблемы и приёмки, чтобы не потерять другой её аспект.

### `ST-20` — Bounded scope и сохранность чужого состояния

ShipTask изменяет только in-scope surfaces и сохраняет unrelated пользовательские
изменения, Tasks и внешнее состояние. Он не превращает delivery authority в
право на unrelated cleanup, не выдаёт worker report или isolated-worktree check
за integrated result и проверяет exact candidate после fan-in. Частичный или
unknown effect сначала reconciles и сообщается честно, а не скрывается rollback,
blind retry или destructive cleanup без authority.

### `ST-21` — Resume-first и подхватывание начатой работы

После ошибки, остановки агента, прерывания run или перехода в новую Codex-сессию
ShipTask по возможности продолжает уже начатую in-scope работу до финального
результата, а не начинает её заново. Перед созданием новой implementation
surface он reconciles current Task/comments/status, partial effects и доступные
task-owned Git artifacts. Смена сессии или coordinator не стирает доказанные
commits, незакоммиченные изменения, branch, worktree, evidence history или
незавершённый lifecycle; freshness evidence обновляется настолько, насколько
этого требует current решение.

Если для exact Task уже существует доказанно связанная feature branch и Git
worktree с незавершённой работой, а прежний writer остановлен и concurrent
ownership отсутствует, ShipTask принимает эксклюзивное владение этим же
worktree и продолжает работу в нём. Он не бросает или дублирует такой worktree
только из-за новой сессии, ошибки прежнего агента или смены исполнителя. Если
сохранилась branch без доступного worktree, ShipTask по возможности безопасно
восстанавливает рабочий checkout из неё и продолжает с существующего state.

Подхватывание не разрешает двум writers одновременно менять один worktree, не
позволяет присвоить чужие или неоднозначные изменения и не отменяет fresh
проверку scope, ownership, current acceptance и partial/unknown effects. Пока
эксклюзивность или связь artifacts с Task не доказана, ShipTask сначала
reconciles состояние и не делает destructive cleanup; независимая безопасная
работа может продолжаться. Terminal Task, изменившийся scope или явное решение
пользователя отказаться от прежнего candidate имеют приоритет над resume.

### `ST-22` — Независимая plugin distribution

ShipTask распространяется только в отдельном `ship-tasks@srez-marketplace`, а
Task Manager connector — отдельным adapter-only plugin без delivery policy.
Checked-in runtime source, Marketplace source и installed cache после
behavioral изменения должны быть byte-identical; standalone user-level
duplicates не создаются, а новый snapshot проверяется в fresh Codex session.

## Изменение Level 1

Новый запрос меняет этот файл только если пользователь меняет обязательный
ShipTask result, invariant или boundary. Просьба улучшить architecture,
упростить процесс, сменить tool или найти лучший способ достижения сохраняет
Level 1 и относится к `architecture.md`.
