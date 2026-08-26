# Strategic Explainer

Статус: current Level 2 contract, 2026-08-26. Применимые Level 1 requirements —
`SE-*` в локальных
[требованиях пользователя](requirements.md). Эта architecture описывает
current архитектуру достижения и не может ослаблять Level 1. Problem-first
bounded discovery принято в
[ADR-0014](../../decisions/0014-problem-first-bounded-strategic-discovery.md), а
fresh stateless invocation и blocker reflection — в
[ADR-0029](../../decisions/0029-fresh-strategic-explainer-and-blocker-reflection.md).

Продуктовая архитектура раскрыта в
[стратегическом видении](product-vision.md). Эта architecture описывает
наблюдаемый результат и границы общего skill `$strategic-explainer`; кроме явно
заданного clean-invocation invariant она не предписывает внутреннюю организацию
агента.

## 0. Compilation contract

Эта architecture вместе с локальным `requirements.md` является полным current
source package `$strategic-explainer`. Runtime package — производная смысловая
компиляция требований и architecture; он состоит из публичного
routing/admission layer `strategic-explainer/SKILL.md` и внутреннего
`strategic-explainer/references/provider-contract.md`. Вместе они являются
компиляцией этих двух документов: package можно удалить и
собрать заново, сохранив все `SE-*` и выбранную здесь реализацию примерно
эквивалентными по наблюдаемому поведению. `product-vision.md`, ADR, reports и
evaluations дают локальный design/rationale и evidence, но не становятся
параллельным current contract.

## 1. Конституционный принцип

Requirements определяют проблему, качество объяснения, source grounding,
read-only boundary и отсутствие новой authority. `SE-10` является явным
исключением из общей свободы orchestration: direct и delegated use проходят один
stateless API, новый built-in `default` subagent и `fork_turns="none"`; контекст
допускает одну compact task и resolvable anchors без inherited process state.

За этой границей provider-subagent выбирает tool sequence, форму source note,
внутренний reasoning, длину и визуальную форму. Caller не знает и не применяет
эту часть architecture. Структуры и examples полезны только внутри provider,
если помогают передать смысл; они не заменяют observable result.

### 1.1 Два runtime-слоя

Catalog metadata и `SKILL.md` видны routing agent, поэтому они содержат только
client protocol и admission gate. Если текущий agent уже несёт рабочий диалог,
ход задачи или собственные рассуждения, router запрещает читать внутренний
provider contract и требует создать новый built-in `default` subagent с
`fork_turns="none"`.

Новый subagent сначала проверяет invocation по `SE-10`. Invalid call завершается
refusal без загрузки expertise. Только после успешного admission он читает
`references/provider-contract.md`, где находятся discovery, explanation,
comprehension и editorial reconstruction. Так conversation isolation защищает
не только входные turns, но и разделение знаний: coordinating caller не получает
метод, ради независимости которого создан provider.

Caller принимает готовый текст и source basis как opaque result. Он проверяет
material facts по authoritative sources, но не читает provider contract, не
формирует candidate, не запускает внутренний checklist и не переписывает output.
Factual/structural correction всегда получает новый clean invocation. При
mandatory unavailability caller fail-closed для comment/lifecycle publication и
честно сообщает capability failure в обязательном final без имитации provider.

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

Direct request и вызов из другого workflow адресуют один API: caller создаёт
новый built-in `default` subagent с `fork_turns="none"`. Единственный user/task
message является compact selector, а не brief или черновиком объяснения. Он
называет один исходный вопрос, exact scope либо resolvable source anchors и
назначение user-facing result. System/developer/skill instructions остаются
нормальной частью context и не считаются загрязнением.

До первого discovery call Explainer проверяет доступные признаки:

- виден ли ровно один compact, ёмкий и непротиворечивый task;
- нет ли inherited conversation, tool transcript, process diary, caller
  rationale, прежнего candidate или нескольких publication units;
- можно ли по exact scope/anchors самостоятельно найти authoritative facts;
- подтверждает ли доступный metadata clean fork; если metadata скрыт, проверка
  не изображает недоступное доказательство.

Invalid invocation возвращает только короткую operational correction: какой
признак нарушен и какой clean call нужен. Discovery и explanation не начинаются.
Caller создаёт новый subagent с исправленной постановкой; follow-up старому
экземпляру запрещён. Explicit editing/review task может содержать target text,
потому что он является предметом, а не унаследованной формулировкой.

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

Свободная форма должна дать читателю одну согласованную модель:

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
material cause, нужное действие, success signal или точную техническую опору.
Глубина discovery не даёт деталям собственного сюжета.

Техническая деталь остаётся только когда меняет causal model, outcome,
impact/risk, action или confidence. Внутренние сущности переводятся в
человеческие роли; полезный exact term можно сохранить после объяснения.
Текст пишется на языке пользователя. Английский термин остаётся только когда он
является точным названием или естественная замена потеряет смысл; русская
грамматическая рамка с английским смысловым ядром не считается понятным
объяснением.

Если есть реальный material choice, Explainer сравнивает столько доступных
вариантов, сколько нужно для решения: что каждый доказывает, prerequisites,
tradeoff и success signal. Он не придумывает alternatives ради количества и не
выдаёт рекомендацию за принятое действие или новую authority.

Direct и delegated caller получают один publication-ready result contract.
Source refs размещаются рядом с claims либо возвращаются коротким source basis,
чтобы caller мог проверить смысл, факты и provenance. Фиксированный output
envelope не нужен.

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

Для сложного сбоя, нескольких независимых сценариев, существенного препятствия
или сводного отчёта current архитектура использует независимого читателя. Он
получает только исходный вопрос и готовый кандидат, не видит технический журнал,
намерение автора или эталонную формулировку и возвращает свой краткий пересказ
либо точный пробел понимания. Читатель не исправляет текст, не добавляет факты и
не принимает решение. При провале Explainer заново строит объяснение из
авторитетного входа с учётом найденного пробела. Простому однозначному результату
достаточно той же проверки внутри Explainer, если причинная модель очевидна.

Фактическая полнота и понятность проверяются раздельно: хороший пересказ не
компенсирует ошибку в фактах, а формально точный перечень не компенсирует
непонятное объяснение.

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
- result пригоден для публикации без стилистической переработки caller-ом;
- при явной редактуре масштаб правки соответствует состоянию исходника, новая
  структура читается естественно, а обратная проверка подтверждает сохранность
  смыслового ядра без новых решений;
- source basis и material uncertainty остаются проверяемыми.

Regression scenarios проверяются по observable behavior в
[evaluation contract](../../reference/strategic-explainer-evaluation.md).
