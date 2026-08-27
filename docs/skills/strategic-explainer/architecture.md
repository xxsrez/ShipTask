# Strategic Explainer

Статус: current Level 2 contract, 2026-08-27. Применимые Level 1 requirements —
`SE-*` в локальных
[требованиях пользователя](requirements.md). Эта architecture описывает
current архитектуру достижения и не может ослаблять Level 1. Problem-first
bounded discovery принято в
[ADR-0014](../../decisions/0014-problem-first-bounded-strategic-discovery.md), а
fresh stateless invocation и blocker reflection — в
[ADR-0029](../../decisions/0029-fresh-strategic-explainer-and-blocker-reflection.md),
а самостоятельная plugin distribution — в
[ADR-0031](../../decisions/0031-standalone-strategic-explainer-plugin.md).
Терминальная provider-роль и запрет рекурсивной маршрутизации приняты в
[ADR-0033](../../decisions/0033-terminal-provider-and-optional-shiptask-routing.md).

Продуктовая архитектура раскрыта в
[стратегическом видении](product-vision.md). Эта architecture описывает
наблюдаемый результат и границы общего skill `$strategic-explainer`; кроме явно
заданного clean-invocation invariant она не предписывает внутреннюю организацию
агента.

## 0. Compilation contract

Эта architecture вместе с локальным `requirements.md` является полным current
source package `$strategic-explainer`. Runtime package — производная смысловая
компиляция требований и architecture; он состоит из публичного semantic
facade и role resolver в `strategic-explainer/SKILL.md`, provider-only admission
`strategic-explainer/references/provider-entrypoint.md` и внутреннего
`strategic-explainer/references/provider-contract.md`. Вместе они являются
компиляцией этих двух документов: package можно удалить и
собрать заново, сохранив все `SE-*` и выбранную здесь реализацию примерно
эквивалентными по наблюдаемому поведению. `product-vision.md`, ADR, reports и
evaluations дают локальный design/rationale и evidence, но не становятся
параллельным current contract.

Marketplace компилирует этот package отдельно от ShipTask:
`strategic-explainer@srez-marketplace` содержит только source
`strategic-explainer/` и регистрирует qualified skill
`strategic-explainer:strategic-explainer`. ShipTask и Task Composer остаются
внешними callers и не получают provider reference в собственный plugin.

## 1. Конституционный принцип

Provider следует одной product instruction: глубоко разберись, но объясни только
главное. Продукт — понимание читателя, а не отчёт об исследовании; evidence
подтверждает сообщение, но не заменяет его. Технически правильный, но непонятный
текст не проходит contract.

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

## 2. Результат и граница роли

Strategic Explainer превращает локальную техническую ситуацию в problem-first
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
`reasoning_effort="max"`. Единственный provider task содержит внутренний role
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
начинается с exact target/session/task и поднимается через применимые relations,
parent/Epic, Release, Project, product goal, vision, current specification и
accepted decisions. Не каждый уровень обязан существовать, но Explainer должен
установить, зачем выполняется локальная работа и что current result означает для
исходного outcome. Поиск ограничен declared scope и заканчивается, когда более
высокий source уже не меняет problem, outcome, impact/risk, action или confidence.

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

Свободная форма даёт читателю одну согласованную модель. Перечень ниже — возможные
смысловые измерения, а не обязательные поля ответа:

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

Если есть реальный material choice, Explainer сравнивает столько доступных
вариантов, сколько нужно для решения: что каждый доказывает, prerequisites,
tradeoff и success signal. Он не придумывает alternatives ради количества и не
выдаёт рекомендацию за принятое действие или новую authority.

Direct и delegated caller получают один publication-ready result contract.
Готовый текст самодостаточен без source basis. Полезные direct links могут стоять
рядом с claim, если помогают самому читателю; delegated source refs возвращаются
после текста отдельной короткой заметкой только для проверки caller-ом.
Фиксированный output envelope не нужен, но caller не должен принять basis за
продолжение publication text.

Один invocation обслуживает один самостоятельный user-facing result: Task
comment/report, material decision/state explanation, blocker report или final.
Routine chat, progress commentary и внутренний draft не являются publication
unit. Новый вопрос, changed facts/scope либо correction получают новый clean
subagent; старый candidate не передаётся как framing.

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

## 8. Completion criteria

Работа завершена, когда:

- admission подтвердил доступные признаки одного compact task и clean context;
- invalid invocation завершился точным отказом до discovery, а не частичным
  explanation;
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
- первый слой передаёт одну главную причинную мысль без необязательной воды, а
  второй существует только при material need;
- publication text самодостаточен, source basis отделён и не опубликован как его
  продолжение;
- result пригоден для публикации без стилистической переработки caller-ом;
- при явной редактуре масштаб правки соответствует состоянию исходника, новая
  структура читается естественно, а обратная проверка подтверждает сохранность
  смыслового ядра без новых решений;
- source basis и material uncertainty остаются проверяемыми.

Regression scenarios проверяются реальным model-forward запуском по observable
behavior в [evaluation contract](../../reference/strategic-explainer-evaluation.md).
Статическая проверка текста contract подтверждает только wiring и не является
доказательством понятности generated result.

Перед completion provider делает отдельный language-normalization pass только
по publication body. Он оставляет латиницу лишь для точного имени, статуса,
формата или элемента интерфейса, который читателю действительно нужно найти или
выбрать; внутренние названия причин, границ и проверок переводятся обычными
словами. Этот pass не задаёт шаблон, длину или список обязательных полей и не
касается отдельно возвращаемого source basis.

После нормализации языка provider делает audit-redaction pass: сравнивает
publication body с raw facts и по умолчанию выносит служебные Task refs, SHA,
run/deployment/request IDs, версии, ревизии, retry keys и внутренние номера в
source basis независимо от исходного раздела fixture. Исключение остаётся только
для точного значения, нужного самому читателю для различения materially distinct
сценария, навигации или действия. Это сохраняет конкретные пользовательские
размеры, имена файлов и видимые статусы, но не превращает их в техническую
квитанцию.
