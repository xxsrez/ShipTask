# Strategic Explainer

Статус: current agent-owned Architecture, 2026-08-30. Независимые user-owned
входы находятся в [Overview](overview.md), а `SE-*` — в локальных
[Requirements](requirements.md). Эта Architecture является третьим
самостоятельным source-документом: она задаёт дополнительные инструкции и
решения достижения, но не может менять два пользовательских документа.
Problem-first
bounded discovery принято в
[ADR-0014](../../decisions/0014-problem-first-bounded-strategic-discovery.md), а
fresh stateless invocation — в
[ADR-0029](../../decisions/0029-fresh-strategic-explainer-and-blocker-reflection.md),
а самостоятельная plugin distribution — в
[ADR-0031](../../decisions/0031-standalone-strategic-explainer-plugin.md).
Терминальная provider-роль и запрет рекурсивной маршрутизации приняты в
[ADR-0033](../../decisions/0033-terminal-provider-and-optional-shiptask-routing.md).

Общий смысл сущности задаёт пользовательский [Overview](overview.md), а его
agent-owned развитие раскрыто в [стратегическом видении](product-vision.md).
Эта architecture описывает наблюдаемый результат и границы общего skill
`$strategic-explainer`; кроме явно заданного clean-invocation invariant она не
предписывает внутреннюю организацию агента.

## 0. Compilation contract

Локальные `overview.md`, `requirements.md` и `architecture.md` являются тремя
независимыми входами current source package `$strategic-explainer`. Runtime
package — их производная смысловая компиляция; он состоит из публичного semantic
facade и role resolver в `strategic-explainer/SKILL.md`, provider-only admission
`strategic-explainer/references/provider-entrypoint.md` и внутреннего
`strategic-explainer/references/provider-contract.md`. Вместе они являются
компиляцией трёх самостоятельных документов: package можно удалить и собрать заново,
сохранив определённое пользователем назначение, все `SE-*` и выбранную здесь
реализацию примерно эквивалентными по наблюдаемому поведению.
`product-vision.md`, ADR, reports и
evaluations дают локальный design/rationale и evidence, но не становятся
параллельным current contract.

Marketplace компилирует его как самостоятельный package:
`strategic-explainer@srez-marketplace` содержит только source
`strategic-explainer/` и регистрирует qualified skill
`strategic-explainer:strategic-explainer`. Package вызывающего workflow или
adapter не получает provider reference.

## 1. Конституционный принцип

Overview независимо определяет Strategic Explainer как уточнитель общего
назначения для одного универсального технически сильного пользователя. Provider
следует одной product instruction: глубоко разберись, но объясни только главное.
Продукт — понимание читателя, а не отчёт об исследовании; evidence подтверждает
сообщение, но не заменяет его. Технически правильный, но непонятный текст не
проходит contract.

В publication text остаётся только то, что меняет понимание проблемы или
результата, решение, действие, риск либо честную уверенность читателя. Полный
доказательный след сохраняется отдельно в source basis. Поэтому глубина
discovery и объём публикации не связаны: сложное исследование может закончиться
двумя ясными предложениями, а сложная причинная граница может потребовать больше.

Остальные Requirements раскрывают этот принцип, source grounding, read-only
boundary и отсутствие новой authority. `SE-10` и `SE-17` являются явными
исключениями из общей свободы orchestration: direct и delegated client
обращаются к одному semantic facade, а уже facade router создаёт новый built-in
`default` subagent с `fork_turns="none"`; compact task несёт exact role lock,
одну publication unit и resolvable anchors без inherited process state.
Provider после role resolution не оркестрирует agents и не вызывает Strategic
Explainer повторно.

Provider profile является ещё одним внутренним routing invariant: facade router
создаёт subagent на `gpt-5.6-luna` с `reasoning_effort="max"` и не наследует
current model/effort. Если exact profile недоступен, invocation не подменяется
SOL или другой моделью; facade возвращает provider unavailability, после чего
внешний client следует собственной policy.

Fresh subagent и его пустой относительно caller-а context — не заменяемая
техническая подробность, а сам способ управлять context Strategic Explainer.
Цель отдельного subagent состоит не в делегации как таковой: `fork_turns="none"`
исключает унаследованный диалог, tool transcript, process diary, рассуждения и
candidate вызывающего агента. В новый context допускаются только обычные
system/developer/skill instructions и одна короткая задача высокого уровня с
разрешимыми anchors; нужную конкретику provider добывает самостоятельно из
authoritative read-only sources. Поэтому «пустой context» здесь означает
отсутствие унаследованного execution context, а не отсутствие системных правил,
provider contract или самой publication task.

Исполнение provider method в текущем conversational agent, наследование turns,
передача подробного хода работы либо готовой интерпретации считаются
архитектурной регрессией, даже если отдельный текст выглядит удачно. Такие
варианты уничтожают контролируемую границу context, подменяют независимое
понимание редактурой версии caller-а и загружают в provider низкоуровневую
конкретику, от которой эта архитектура его намеренно изолирует.

Профиль `gpt-5.6-luna`/`max` решает две связанные задачи. В принятом
пользовательском слепом сравнении Luna дала для этой роли лучший результат, чем
SOL. Одновременно fresh subagent не использует cache context вызывающего агента
и поэтому создаёт дополнительную стоимость; Luna компенсирует её, а `max`
сохраняет требуемую глубину рассуждения. Предлагать другой профиль или отказаться
от отдельного subagent нельзя как от обычной оптимизации реализации: такое
изменение должно заново обосновать и качество объяснения, и экономику чистого
вызова, не ослабляя context isolation.

За этой границей provider-subagent выбирает tool sequence, форму source note,
внутренний reasoning, длину и визуальную форму. Caller не знает и не применяет
эту часть architecture. Структуры и examples полезны только внутри provider,
если помогают передать смысл; они не заменяют observable result.

### 1.1 Три runtime-слоя и однозначная роль

Внешний client contract живёт только в вызывающем workflow: вызвать qualified
skill с одной semantic formulation/editing task, её целью, exact scope, языком,
material constraints и resolvable read-only anchors, затем принять готовый text
и отдельно обозначенный source basis либо operational unavailability. Agent
topology, fork, profile, role lock, entrypoint и retry в этот contract не входят.

Catalog metadata и `SKILL.md` образуют второй слой — facade router и
детерминированный role resolver. Этот слой знает только invocation/admission
mechanics и не содержит provider method. Facade создаёт новый built-in `default`
subagent с `fork_turns="none"`, `model="gpt-5.6-luna"` и
`reasoning_effort="max"`, затем передаёт отдельной точной строкой
`STRATEGIC_EXPLAINER_PROVIDER_V1`. Отсутствие marker означает facade mode;
наличие marker в compact task означает terminal provider mode. История, tool
calls, parent metadata или имя агента не участвуют в классификации.

Provider никогда не исполняет facade protocol и сразу читает только
`references/provider-entrypoint.md`. Этот слой проверяет роль и invocation по
`SE-10`/`SE-17`; invalid call завершается
`STRATEGIC_EXPLAINER_INVOCATION_ERROR` без domain discovery, source reads или
загрузки expertise. Только admitted provider читает
`references/provider-contract.md`, где находятся discovery, explanation,
внутренний comprehension check и editorial reconstruction. Так conversation
isolation защищает не только входные turns, но и разделение знаний:
coordinating caller не получает метод, ради независимости которого создан
provider.

Третий слой — admitted provider, и только он читает
`references/provider-contract.md` с правилами discovery, причинного объяснения,
редакторской реконструкции, языковой очистки и comprehension check. Ни внешний
client, ни facade router не получают эту методику и не улучшают текст сами.

Facade возвращает publication-ready text и отдельно обозначенный source basis
как opaque result. Внешний client публикует только text, а basis использует для
factual check; не смешивает эти части, не читает provider contract, не формирует
candidate, не запускает внутренний checklist и не переписывает output.
Factual correction приходит новым semantic request. Structural correction и
единственный clean retry выполняются внутри facade. Поведение при opt-out или
недоступности задаёт contract конкретного client-а: он не читает и не имитирует
provider method и не заявляет эквивалентное качество.

### 1.2 Built-in child вместо отдельной Codex task

`Built-in subagent` в этой architecture означает дочернего агента текущей Codex
task в её внутреннем team tree. Facade создаёт его прямым top-level вызовом
`collaboration.spawn_agent`. Этот вызов не выполняется через
`functions.exec`: collaboration tools намеренно могут отсутствовать в
`ALL_TOOLS`, доступном вложенному exec-коду, и такой результат не доказывает
отсутствие subagent capability.

Facade должен исполняться агентом, у которого `collaboration.spawn_agent`
реально присутствует в top-level tool surface. Уже созданный built-in child
может видеть только `functions`/`clock` и не иметь права создавать grandchild;
в этом случае facade не ищет transport и возвращает operational unavailability.
Calling workflow, владеющий orchestration, не делегирует facade такому child:
он принимает от рабочих агентов facts/evidence/anchors и вызывает semantic
facade сам. Это сохраняет единый API и fresh provider, не добавляя caller-у
знания provider recipe.

App-level операции с пользовательскими Codex tasks не являются альтернативным
transport. Facade не вызывает `create_thread`, не создаёт projectless task, не
fork-ает и не продолжает отдельную пользовательскую task или session ради
provider-а. Правильный invocation наблюдается как child/subagent с parent link
и agent path внутри текущей task, а не как новый элемент боковой панели или
отдельный рабочий каталог пользователя.

Если прямой `collaboration.spawn_agent` недоступен или завершился ошибкой,
facade возвращает operational unavailability по caller contract. Он не ищет
похожий app tool, не просит parent через app messaging и не подменяет скрытую
внутреннюю делегацию внешне видимой task. Та же граница действует для
единственного clean retry после structural refusal.

## 2. Результат и граница роли

Strategic Explainer превращает локальную ситуацию в problem-first
объяснение на уровне цели, пользовательского эффекта, ограничений, границы
знания и следующего понятного state. По явному запросу на редактуру он также
перестраивает плотный технический или нормативный текст в естественную
профессиональную версию без потери содержания. Результат должен быть понятным
без знания внутренних tools, transport layers, source code и agent lifecycle.

Skill является интерпретационным слоем. Он:

- не выполняет writes, recovery, release, status transition, external action
  или другую mutation;
- не выбирает scope, current outcome, authority или разрешённое действие за
  вызывающий workflow;
- не усиливает confidence и не превращает design document в execution evidence;
- не публикует externally addressed text самостоятельно, если caller оставил
  финальную коммуникацию за собой.

Найденные strategic sources объясняют значение результата, но не доказывают,
что result реализован или проверен.

## 3. Fresh API admission

Direct request и вызов из другого workflow адресуют один semantic API. Client
применяет `$strategic-explainer:strategic-explainer` к одной publication task с
назначением, exact scope, языком, material constraints и resolvable read-only
anchors. После загрузки skill facade router создаёт новый built-in `default`
subagent с `fork_turns="none"`, `model="gpt-5.6-luna"` и
`reasoning_effort="max"` через внутренний child-only transport из раздела 1.2.
Единственный provider task содержит внутренний role
lock `STRATEGIC_EXPLAINER_PROVIDER_V1` и является compact selector, а не brief
или черновиком объяснения. System/developer/skill instructions остаются
нормальной частью context и не считаются загрязнением.

До первого discovery call Explainer проверяет доступные признаки:

- виден ли ровно один compact, ёмкий и непротиворечивый task;
- нет ли inherited conversation, tool transcript, process diary, caller
  rationale, прежнего candidate или нескольких publication units;
- можно ли по exact scope/anchors самостоятельно найти authoritative facts;
- подтверждает ли доступный metadata clean fork; если metadata скрыт, проверка
  не изображает недоступное доказательство.

Invalid invocation возвращает facade-у `STRATEGIC_EXPLAINER_INVOCATION_ERROR`,
точный defect, единственное назначение provider-а и исправимый clean-call
recipe. Discovery и explanation не начинаются. Planning, decomposition,
implementation, mutation, lifecycle/status/authority decision, broad research
без publication unit и orchestration отклоняются тем же способом. Facade
создаёт один новый subagent с исправленной постановкой; внешний client не знает
recipe и не получает промежуточный refusal. Follow-up старому экземпляру
запрещён, а provider не создаёт замену самостоятельно. Explicit editing/review
task может содержать target text, потому что он является предметом, а не
унаследованной формулировкой.

После admission Explainer сам устанавливает исходный вопрос, beneficiary,
desired observable outcome, current facts/evidence/confidence, impact,
authority и applicable strategic anchors. Если resolvable source не содержит
material основания, skill ясно называет недостающий факт и почему без него
нельзя честно объяснить результат. Identifier или technical title сами по себе
не заменяют problem framing.

Для нескольких независимых сценариев сохраняются отдельные state, evidence,
impact и dependencies. Форма такого представления выбирается по ситуации.

## 4. Bounded strategic discovery

После admission Explainer обязательно использует доступные read-only sources,
чтобы независимо собрать current facts и проверить strategic meaning. Поиск
начинается с exact target или scope и поднимается через применимые связи,
родительский контекст, текущую цель, продуктовый замысел, current specification
и accepted decisions. Не каждый уровень обязан существовать, но Explainer
должен установить, зачем выполняется локальная работа и что current result
означает для исходного outcome. Поиск ограничен declared scope и заканчивается,
когда более высокий source уже не меняет problem, outcome, impact/risk, action
или confidence.

- `current/accepted`, `proposed` и `historical` sources различаются;
- live execution evidence определяет current outcome, а design объясняет его
  значение;
- отсутствие дополнительного source не создаёт выдуманный blocker;
- material conflict или недоступное обязательное основание явно остаётся gap;
- session history читается только bounded source retrieval, а не наследуется
  целиком в model context;
- unrelated logs, code и broad research не включаются без material relevance.

Specification оценивает relevance и factual grounding discovery, а не порядок
tool calls или количество прочитанных источников.

## 5. Объяснение

Provider сначала строит private evidence map: current facts, границы знания и
точные основания. Из неё он отдельно строит reader model — одну причинную мысль
на уровне исходного вопроса. Publication text создаётся из reader model, а не
путём сокращения технического отчёта. Source basis создаётся из evidence map уже
после текста и не возвращается внутрь публикации.

Когда исходные основания содержат несколько materially distinct пользовательских
сценариев, evidence map включает внутреннюю scenario coverage map. Для каждого
такого сценария она сохраняет проверяемый input или boundary, наблюдаемый result
и относящийся к нему state/impact. Для end-to-end acceptance scenario карта
также сохраняет минимальную пользовательскую цепочку materially checked
переходов или действий, образующих заявленный outcome, а не только последний
result: позднее наблюдение не заменяет более ранний существенный шаг, если целью
является весь путь. Audit-only шаги в эту цепочку не входят, пока не меняют
понимание, решение, риск или уверенность читателя. При построении reader model
сценарии можно объединить только когда эти элементы, существенная цепочка и
вывод для читателя действительно эквивалентны; общая формулировка не должна
поглощать отличающуюся границу, исключение, шаг или результат. Это контроль
смыслового покрытия, а не обязательная структура, заголовки, полная process
chronology или checklist публикации.

Свободная форма даёт читателю одну согласованную модель и прямой ответ, а не
отчётный шаблон. Структура и длина следуют содержанию; заголовки, поля, списки и
таблицы появляются только когда действительно улучшают понимание. Перечень ниже
— возможные смысловые измерения, а не обязательные поля ответа:

- какую проблему и для кого решаем;
- какой strategic intent или constraint определяет смысл;
- что фактически получено и как это влияет на desired outcome;
- что failed, unverified, unknown или не относится к цели;
- требуется ли действие, кто его выполняет, зачем и какой observable signal
  позволит продолжить.

Сначала строится причинная история на уровне исходного вопроса, без внутренних
идентификаторов и названий механизмов. Первый слой выделяет одну главную мысль и
по возможности исчерпывает ответ одной фразой: что получилось или остановилось и
почему. Суть обязательна; отсутствие воды, повторов и необязательных деталей —
второй приоритет. Только после этого короткий второй слой может объяснить
material cause, нужное действие или success signal. Глубина discovery не даёт
деталям собственного сюжета. Если удаление фрагмента не меняет reader model,
decision, action, risk или confidence, этот фрагмент не входит в текст.

Техническая деталь остаётся в тексте только когда меняет causal model, outcome,
impact/risk, action или confidence читателя. Verification-only identifiers,
версии, SHA, deployment refs, ревизии, названия внутренних gates и перечни
проверок остаются в source basis, если читателю не нужно действовать именно с
ними. Внутренние сущности переводятся в человеческие роли; полезный exact term
можно сохранить после объяснения.
Текст пишется на языке пользователя. Английский термин остаётся только когда он
является точным названием или естественная замена потеряет смысл; русская
грамматическая рамка с английским смысловым ядром не считается понятным
объяснением.

Названия самого Explainer, facade/provider-ролей, admission, orchestration,
gates и других частей процесса подготовки не становятся пользовательским
сюжетом. Если весь claim относится только к созданию текста, отчёта или ответа и
не меняет понимание исходного предмета, он целиком уходит в source basis, а не
обезличивается внутри publication body. Перевод «provider сформировал report» в
«отчёт сформирован» не устраняет утечку: внутренний процесс нужно удалить по
смыслу. Точное название остаётся только когда читателю нужно найти, проверить
или использовать именно его. Так runtime не объясняет собственную работу вместо
исходного предмета.

Перед completion provider применяет к publication body единый фильтр в два
прохода. Language-normalization оставляет латиницу только для точного имени,
статуса, формата или элемента интерфейса, который читателю действительно нужно
найти или выбрать. Затем audit-redaction сопоставляет body с raw facts и по
умолчанию выносит служебные refs, SHA, run/deployment/request IDs, версии,
ревизии, retry keys и внутренние номера в source basis. Исключение действует
только для значения, нужного самому читателю для различения сценария,
навигации или действия. Basis сохраняет доступные точные значения и их смысл
либо даёт точный разрешимый anchor на содержащий их источник, а не подменяет их
общей отметкой об исключении технических деталей. Фильтр не задаёт шаблон,
длину или обязательные поля.

Material limitation, exception или uncertainty ставится рядом с ограничиваемым
утверждением. Общая оговорка в конце не исправляет текст, если предыдущее
предложение без неё звучит шире или увереннее, чем позволяют sources.

Если есть реальный material choice, Explainer сравнивает столько доступных
вариантов, сколько нужно для решения: что каждый доказывает, prerequisites,
tradeoff и success signal. Он не придумывает alternatives ради количества и не
выдаёт рекомендацию за принятое действие или новую authority.

В объяснении препятствия или нужного действия каждая объявленная prerequisite
остаётся material claim. Provider проверяет её по current sources, а не по
старому `not_available`, прежнему report или списку симптомов. Уже существующая
возможность, выполненное условие либо безопасный самостоятельно доступный путь
означают, что заявленная dependency не установлена, вывод об остановке требует
пересчёта, а caller может продолжить доступное действие. Действие человека
называется необходимым только когда evidence подтверждает, что current situation
фактически дошла до соответствующего условия.

Direct и delegated caller получают один publication-ready result contract.
Готовый текст самодостаточен без source basis. Полезные direct links могут стоять
рядом с claim, если помогают самому читателю; delegated source refs возвращаются
после текста отдельной короткой заметкой только для проверки caller-ом.
Фиксированный output envelope не нужен, но caller не должен принять basis за
продолжение publication text.

Один invocation обслуживает один самостоятельный user-facing result: комментарий,
отчёт, объяснение решения, состояния или препятствия, final либо явную редактуру.
Следующая публикация об изменившемся состоянии и итоговое объяснение являются
новыми units, даже если используют те же facts: прежний provider не продолжается,
не переименовывается и не получает новое назначение. Routine chat, progress
commentary и внутренний draft не являются publication unit. Новый вопрос,
changed facts/scope либо correction получают новый clean subagent; старый
candidate не передаётся как framing.

## 6. Проверка понимания

Перед публикацией объяснение проверяется отдельно от проверки фактов. Минимальная
проверка задаёт четыре вопроса:

- отвечает ли первый смысловой слой именно на исходный вопрос и на той же
  глубине;
- можно ли без внутренних названий пересказать, что произошло и почему это
  важно;
- различимы ли установленный результат, граница знания и следующий шаг;
- не требуется ли читателю знать предметную область исполнителя, чтобы понять
  основную причинность.

Runtime provider всегда выполняет comprehension check самостоятельно, без
вызова другого agent: временно откладывает evidence map и проверяет, можно ли из
готового текста восстановить исходный вопрос, причинность, результат, границу и
следующий шаг. При пробеле provider заново строит объяснение из авторитетного
входа. Независимый читатель сохраняется только как внешний model-forward
evaluation harness: он получает исходный вопрос и готовый candidate отдельным
fresh trial, не входит в runtime orchestration и ничего не возвращает provider-у.
Так качество продолжает проверяться независимо, но terminal provider остаётся
единственным агентом своей publication unit.

Фактическая полнота и понятность проверяются раздельно: хороший пересказ не
компенсирует ошибку в фактах, а формально точный перечень не компенсирует
непонятное объяснение.

При наличии scenario coverage map Explainer перед возвратом сверяет с ней
publication text: из естественной формулировки должны восстанавливаться input
или boundary, наблюдаемый result и state/impact каждого materially distinct
сценария, а для заявленного end-to-end outcome — минимальная цепочка его
существенных пользовательских переходов или действий. Эти элементы можно
передать одной фразой или свободной структурой, если различия и этапы результата
не потеряны; наличие полного source basis или позднего наблюдаемого результата
не компенсирует их исчезновение из пользовательского объяснения.

Для объяснения незавершённого результата или невозможности продолжить scenario
coverage map сохраняет фактическое текущее состояние и наблюдаемый result,
primary cause или boundary, оставшееся условие, доступное next action и
observable continuation signal. Существенно разные препятствия объединяются
только без потери разных причин, условий, действий и способов продолжения.
Устойчивое human-facing название или identifier остаётся в publication body
только когда нужно читателю для различения или навигации.

Перед completion provider восстанавливает эти causal links только из готового
publication body и сравнивает с evidence map. Наличие полного source basis не
закрывает пропуск. Объяснение отклоняется, если из него нельзя понять, что
фактически получилось, почему результата пока нет, какое условие осталось и
можно ли продолжить доступным способом. Если evidence map содержит current
repair, retry или self-service path, формулировка об исчерпанной возможности
продолжить также отклоняется; result сообщает caller-у, какой путь ещё доступен,
не принимая решение за него.

## 7. Редакторская реконструкция

Этот режим применяется, когда пользователь или вызывающий агент явно просит
отредактировать, переписать, очеловечить или привести в порядок предназначенный
человеку текст. Обычный запрос объяснить ситуацию сам по себе не требует
переписывать исходный документ целиком.

Сначала определяется масштаб правки:

- локальная редактура подходит тексту с уже ясной логикой, которому мешают
  отдельные тяжёлые фразы, канцелярит или лишний жаргон;
- глубокая реконструкция нужна, когда смысл рассыпан между повторами,
  исключениями, смешанными уровнями детализации или гибридным техническим
  языком и последовательная правка предложений не сделает документ ясным.

До реконструкции фиксируется неизменяемое смысловое ядро исходника:

- точные факты, цели, обязательные результаты, требования и идентификаторы;
- причинные связи, зависимости и отношения между элементами;
- область действия, ограничения, запреты, исключения, приоритеты и явно
  исключённые цели;
- критерии проверки, подтверждения приёмки и границы достоверности;
- границы полномочий, безопасности и конфиденциальности;
- существенная неопределённость, пробел или противоречие.

Это ядро сохраняется во всём двухчастном result contract, а не обязательно
целиком в publication body. Факты, влияющие на понимание, решение, действие,
риск или confidence читателя, остаются в тексте; audit-only identifiers,
служебные статусы и детали внутреннего процесса переходят в source basis.
Перенос точной детали в basis не является содержательной потерей. Наличие
детали в target text само по себе не делает её пользовательски релевантной и не
отменяет language-normalization, audit-redaction или запрет объяснять работу
Explainer вместо исходного предмета.

Затем текст строится заново вокруг одной главной мысли на смысловой блок.
Доминирующее правило и его пользовательский смысл появляются раньше частных
условий; исключение находится рядом с правилом, которое оно ограничивает;
причина, ожидаемый результат и способ проверки связаны явно. Заголовки,
порядок, длина абзацев и синтаксис можно менять свободно. Точные названия
протоколов, состояний, инструментов и технологий, а также идентификаторы
сохраняются дословно, включая написание и регистр, когда они нужны для
проверяемости, навигации или точности; остальной внутренний жаргон переводится
в естественный язык пользователя.

После правки выполняется обратная проверка покрытия: каждый элемент
неизменяемого смыслового ядра должен иметь однозначное место в новой версии, а
каждое новое содержательное утверждение — основание в исходнике. Потеря
исключения, ослабление запрета, усиление уверенности или добавление нового
решения являются содержательной ошибкой, даже если текст стал легче читать.
Неясность исходника сохраняется явно, а не маскируется редактурой.

Эта обратная проверка охватывает весь двухчастный result: каждый точный факт,
убранный из body как нерелевантный читателю, остаётся в basis самим значением
либо точным разрешимым anchor. Общая ссылка на документ или отметка об
исключённых деталях не подтверждает сохранность.

Затем единый фильтр публикации из раздела 5 выполняется заново независимо от
исходной формы. После удаления exact names provider повторно проверяет смысл
оставшейся фразы: обезличенное сообщение о создании отчёта или ответа тоже
удаляется, если не относится к исходному предмету. Просьба сохранить факты не
считается просьбой опубликовать audit trail.

## 8. Completion criteria

Работа завершена, когда:

- admission подтвердил доступные признаки одного compact task и clean context;
- invalid invocation завершился точным отказом до discovery, а не частичным
  explanation;
- provider invocation наблюдается как child/subagent текущей Codex task, а не
  отдельная пользовательская task/session; недоступность прямого child spawn
  завершилась operational unavailability без `create_thread` или app-level
  замены;
- проблема и desired outcome не выдуманы;
- каждое material утверждение опирается на current facts или exact source;
- каждый decision-relevant факт сохранён либо исключён только как не влияющий
  на problem, outcome, impact/risk, action или confidence;
- fact, interpretation, failure, unknown и not-applicable различимы;
- discovery самостоятельно собрал нужные facts и strategic context, остался
  bounded и read-only;
- explanation не создаёт status, permission или action, которого источник не
  устанавливал;
- первый смысловой слой отвечает на исходный вопрос на его уровне абстракции и
  остаётся понятным без идентификаторов и внутренней терминологии;
- читатель может своими словами восстановить проблему, результат или
  препятствие, влияние и следующий шаг без process diary;
- названия Explainer, agents, ролей, маршрутизации и процесса подготовки не
  подменяют объяснение исходного предмета;
- material limitation, exception и uncertainty находятся рядом с ограничиваемым
  утверждением;
- explanation нужного действия не просит человека повторить уже выполненное
  условие и не превращает старый `not_available` или ещё не достигнутый шаг в
  current dependency;
- первый слой передаёт одну главную причинную мысль без необязательной воды, а
  второй существует только при material need;
- если пользователь прямо не запросил audit trail, publication body не содержит
  raw shell/test commands, абсолютные пути, полный список тестовых файлов,
  неприменимые SHA/IDs или другую техническую квитанцию; эти сведения остаются в
  source basis;
- новая публикация об изменившемся состоянии сообщает material delta и не повторяет
  неизменившиеся доказательства из предыдущего пользовательского сообщения;
  исправленный incident, новая граница либо новое действие при этом не теряются;
- publication text самодостаточен, source basis отделён и не опубликован как его
  продолжение;
- result пригоден для публикации без стилистической переработки caller-ом;
- при явной редактуре масштаб правки соответствует состоянию исходника, новая
  структура читается естественно, а обратная проверка подтверждает сохранность
  смыслового ядра без новых решений;
- source basis и material uncertainty остаются проверяемыми.
- объяснение незавершённого результата сохраняет причинные различия между
  препятствиями и не заявляет исчерпанную возможность продолжить при наличии
  current runnable path.

Regression scenarios проверяются реальным model-forward запуском по observable
behavior в [evaluation contract](../../reference/strategic-explainer-evaluation.md).
Статическая проверка текста contract подтверждает только wiring и не является
доказательством понятности generated result.
