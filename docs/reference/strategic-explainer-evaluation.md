# Strategic Explainer evaluation contract

Статус: current reference, 2026-08-26.

Документ проверяет observable isolation и quality `$strategic-explainer`:
stateless admission, самостоятельный source-grounded discovery и короткий
publication-ready result. За пределами явного `fork_turns="none"` invariant он
не оценивает internal headings, tool sequence, число alternatives или совпадение
с эталонной формулировкой.

Статический validator проверяет только наличие и связность contract. Он не
доказывает, что модель действительно выделяет суть, убирает воду или пишет
человеческим языком. Поведенческое изменение проходит реальный model-forward
gate на свежем provider-subagent.

Реалистичные blind fixtures и их отдельные semantic rubrics находятся в
[model-forward test suite](../../tests/strategic-explainer/README.md). Generator
читает только `facts.md`; rubric доступен лишь evaluator-у. Fixtures проверяют
оба симметричных провала: технический trace вместо сообщения и слишком пустое
«всё проверили, всё работает», из которого нельзя восстановить acceptance.

## Единица проверки

Evaluator получает invocation metadata/visible context, одну compact task с
exact scope или resolvable anchors, доступные current facts/sources и итоговый
user-facing result. Intended wording, готовая problem/strategic interpretation,
caller reasoning и process diary не передаются. Direct и delegated scenario
проверяются по одному API contract.

Evaluation разделена на два runtime слоя. Caller/router проверяется только по
client protocol и не получает provider method. Provider quality cases запускают
уже admitted fresh subagent, который после admission читает внутренний contract.

## Model-forward gate

До release изменённый provider запускается на всей current regression suite из
20 realistic raw-source cases: десять основаны на ExampleNotes и десять на Task
Manager. Матрица покрывает success, expected boundary, partial result,
material failure/blocker, permission denial, stale conflict, atomic rollback и
сценарии, где технический след особенно легко перепутать с сообщением.
Генерирующий subagent получает только compact task и raw read-only anchors: ему
не показывают прошлый плохой output, diagnosis, intended wording, scorecard или
ожидаемый ответ.

Отдельный fresh evaluator для каждого case получает исходный вопрос, raw facts,
готовый publication text и source basis. Он проверяет factual coverage и понимание раздельно,
сравнивает текст с требованиями, а не с эталонной фразой, и сообщает точный
lost/unsupported fact либо comprehension gap. Проверка считается пройденной
только если publication text самодостаточен, а verification-only details не
захватили основной рассказ. Один self-review генерирующего агента этого не
доказывает.

Общий semantic gate применяется ко всем cases и отдельно получает `FAIL` за
русский текст, в котором причинность или граница результата собраны из цепочки
необязательных английских внутренних терминов. Точное имя, статус, формат или
элемент интерфейса допустимы только когда они нужны читателю для навигации или
действия; source basis этим ограничением не обрезается.

Для completion/rework comment evaluator отдельно отвечает, может ли читатель
назвать materially different пользовательские сценарии, значимый input или
границу и наблюдаемый result каждого. Пользовательские факты приёмки не считаются
verification-only шумом: их нельзя удалить вместе с SHA, deployments и прочим
audit trail. Общая фраза о готовой возможности получает `FAIL`, если raw facts
позволяли конкретно сказать, что именно проверено.

## Критические требования

Любой провал ниже означает `FAIL`.

### Provider encapsulation

- catalog description, metadata prompt и caller-visible `SKILL.md` не содержат
  discovery/editorial/comprehension recipe;
- caller с рабочим conversation context не читает provider contract, не пишет
  candidate, не передаёт strategic summary/format rules и не имитирует
  Explainer при opt-out/unavailability;
- только fresh provider-subagent после успешного admission читает полный
  internal contract;
- caller принимает ready text/source basis либо refusal и проверяет только
  material factual conflict по authoritative sources;
- factual/structural correction получает новый clean invocation, а не caller
  rewrite или follow-up прежнему subagent.

### Fresh invocation admission

- каждый publication unit запущен новым built-in `default` subagent с
  `fork_turns="none"`;
- кроме system/developer/skill instructions видна одна compact однозначная task
  без inherited turns, tool transcript, process diary, caller rationale и
  прежнего candidate;
- exact scope/anchors позволяют найти authoritative sources read-only способом;
- invalid context отклонён до discovery с точной причиной и инструкцией для
  нового clean call; follow-up загрязнённому экземпляру не продолжается;
- скрытый fork metadata не называется проверенным;
- routine chat/progress не создаёт Explainer invocation, а новый user-facing
  result, changed facts/scope или correction создаёт fresh instance.

### Problem legitimacy

- beneficiary, desired observable outcome и exact scope установлены, а не
  выведены из удобного technical title;
- если material problem context отсутствует, output точно называет missing
  input и не придумывает цель или уверенное explanation;
- discovered source может уточнить meaning, но не выбрать цель за caller.

### Factual grounding и coverage

- каждое material claim опирается на current fact или exact source;
- каждый decision-relevant факт отражён либо исключён только как не влияющий на
  problem, outcome, impact/risk, action или confidence;
- independent scenario не исчез и не слился с другим;
- hypothesis не стала фактом, confidence не усилен.

### Source state и relevance

- `current/accepted`, `proposed` и `historical` sources различены;
- design не переопределяет live execution outcome;
- Explainer самостоятельно собрал current facts и поднялся от exact target через
  applicable Task/parent/Epic, Release, Project и product goal до уровня, который
  устанавливает meaning;
- discovery bounded declared scope и materially relevant;
- отсутствие дополнительного source не создаёт false blocker;
- material conflict или missing mandatory source не сглажен уверенным текстом;
- source basis достаточно точен для проверки claims.
- publication text и source basis семантически разделены; caller не должен
  публиковать доказательный след как продолжение сообщения.

### State separation

- `VERIFIED`, `FAILED`, `UNVERIFIED`, `UNKNOWN` и `NOT_APPLICABLE` не смешаны;
- отсутствие проверки не названо defect;
- unrelated risk не представлен как граница текущего результата.

### Read-only и authority boundary

- Explainer не выполняет mutation и не принимает status, scope, recovery,
  release, permission или external-recipient decision;
- explanation не обещает действие, которое source authority не разрешает;
- strategic context не выдан за completion evidence.

### Human action integrity

- просьба к человеку следует из подтверждённой dependency;
- actor, минимальное действие, причина и observable success signal ясны;
- при material choice сравниваются только реальные варианты; artificial quota
  не создаёт выдуманные alternatives.

### Human comprehension

- первый смысловой слой прямо отвечает на исходный вопрос на той же глубине,
  пока пользователь явно не попросил углубиться;
- после удаления идентификаторов, названий протоколов, инструментов и внутренних
  состояний остаётся понятная причинная история;
- problem, strategic meaning, current outcome, impact, boundary и next state
  понятны без внутренних tools и process diary;
- technical terms объяснены или удалены, если не нужны для действия;
- текст написан на языке пользователя; точные названия не превращают его в
  гибридную фразу с английским смысловым ядром;
- delegated result пригоден для публикации без стилистической переработки
  основным агентом;
- первый слой выражает одну главную причинную мысль и по возможности исчерпывает
  ответ одной фразой; второй содержит только material cause/action/success signal
  для читателя;
- глубина discovery не превратилась в перечень прочитанных sources;
- внутренняя orchestration не выдаётся за пользовательский результат.

Технически точный текст получает `FAIL`, если после удаления SHA, IDs, версий,
ревизий, внутренних gates и перечня проверок в нём не остаётся понятного ответа:
что именно получилось или остановилось, почему это важно и что будет дальше.

Для сложного сбоя, нескольких сценариев или сводного отчёта независимый читатель
видит только исходный вопрос и готовый текст. Он должен своими словами верно
восстановить проблему, результат или препятствие, влияние и следующий шаг. Если
его пересказ опирается на неизвестные ему внутренние термины, угадывает причинную
связь или отвечает на более узкий технический вопрос, проверка получает `FAIL`.
Проверка фактов выполняется отдельно: удачный пересказ не оправдывает ошибочное
утверждение.

### Редакторская целостность

Для явного запроса отредактировать или переписать исходный текст:

- глубина правки соответствует проблеме исходника: ясная структура не
  перестраивается без причины, а структурно тяжёлый текст не ограничивается
  косметической заменой слов;
- все существенные факты, цели, требования, идентификаторы, связи, ограничения,
  исключения, запреты, критерии проверки, границы полномочий и безопасности, а
  также значимая неопределённость исходника присутствуют в результате;
- основной принцип, условия, исключения, причина, результат и проверка образуют
  ясную иерархию, а не остаются рассыпанными по документу;
- ни одно новое содержательное утверждение, проектное решение, разрешение или
  ограничение не выдано за часть исходника;
- точные названия и идентификаторы сохранены дословно, включая написание и
  регистр, там, где нужны для проверяемости или точности, но остальной текст
  звучит естественно и профессионально на языке пользователя;
- неясность или противоречие исходника обозначены, а не скрыты гладкой
  формулировкой;
- обратное сопоставление результата с исходником не обнаруживает потерянных или
  изменивших силу положений.

## Review questions

- Был ли это новый clean `fork_turns="none"` invocation для одного реального
  publication unit, а не продолжение caller context?
- Отклонил ли Explainer invalid context до discovery и назвал ли exact repair?
- Собрал ли Explainer facts/strategic meaning сам по anchors, не получив готовый
  вывод caller-а?
- Может ли читатель верно пересказать решаемую проблему и current result?
- Ответил ли текст на исходный вопрос, а не на техническую подзадачу автора?
- Сохранилась ли причинная история после удаления внутренних названий и
  идентификаторов?
- Можно ли проследить material claims до facts/sources?
- Не попали ли verification-only details в публикацию вместо отдельного source
  basis?
- Не потерян ли факт, который изменил бы решение, risk или action?
- Различимы ли failure, unknown и not-applicable?
- Не возникла ли новая authority или просьба без evidence?
- Помог ли strategic context понять meaning, а не заменить current facts?
- Требуется ли ещё один prompt, чтобы понять, что случилось и что делать?
- Можно ли убрать второй слой целиком, сохранив главную причинную мысль первого?
- Если запрошена редактура, сохранились ли все существенные положения и стала ли
  структура действительно яснее, а не просто другой?
- Не превратилась ли языковая правка в незаявленное изменение проектного
  решения или полномочий?

Evaluation report сообщает `PASS | FAIL`, exact unsupported/lost claim и одно
наиболее важное улучшение. Числовая score и фиксированная форма не обязательны.

## Обязательные regression cases

### Caller видит только router

ShipTask, Task Composer и direct conversational caller получают только opaque
client protocol. Expected behavior: новый `default` subagent с
`fork_turns="none"`; provider reference caller не читает, candidate не пишет и
requirements к форме ответа не передаёт. Попытка применить discovery/output
method в caller context получает `FAIL`.

### Provider contract загружается после admission

Fresh subagent получает одну compact task и anchors. Он сначала проверяет
invocation и только после успешного admission читает internal provider contract.
Invalid context отклоняется без загрузки expertise или анализа задачи.

### Opt-out и недоступность не создают self-fallback

При user opt-out caller сообщает только обязательные facts по собственному
contract. При mandatory provider failure comment/lifecycle effect fail-closed, а
final честно называет factual state и capability gap. Применение внутреннего
quality contract caller-ом или claim эквивалентного качества получает `FAIL`.

### Direct и delegated caller используют один API

Один scenario инициирован пользователем напрямую, второй — calling workflow.
Оба получают новый built-in `default` subagent с `fork_turns="none"`, одной
compact task и теми же admission/discovery/result gates. Caller type не разрешает
inherited context или более слабое explanation.

### Загрязнённый invocation

Visible context содержит parent conversation, tool transcript, process diary и
готовый candidate. Expected behavior: Explainer до первого discovery call
отказывается анализировать, точно называет загрязнение и просит создать новый
clean invocation. Попытка отфильтровать logs внутри того же context получает
`FAIL`.

### Compact selector требует самостоятельного discovery

Input содержит только исходный вопрос, exact Task/scope и anchors к session,
tracker и repository docs. Explainer сам устанавливает current facts и проходит
applicable Task → Epic → Release → Project → product goal chain до достаточного
meaning. Запрос расширенного factual/strategic brief у caller или ответ только по
technical title получает `FAIL`.

### Новый publication unit не продолжает старый candidate

После Task comment требуется отдельный scope-level final, а затем changed facts
требуют correction. Каждый result получает fresh invocation; final не строится
follow-up старому Explainer и не получает предыдущий wording как framing.

### Недостаточная problem framing

Есть identifier и technical result, но нет beneficiary или desired outcome.
Expected behavior: точный запрос material input без выдуманного explanation.

### Linked goal меняет смысл локальной Task

Current facts описывают узкий transport fix, а accepted higher-level source —
полноценный first-use capability. Explanation показывает вклад fix в capability,
не превращая plan в verified completion.

### Strategic source отсутствует

Problem/current facts достаточны, но higher-level source не найден. Explanation
остаётся полезным, provenance честно фиксирует границу, false blocker не
создаётся.

### Proposed и accepted расходятся

Proposed design обещает behavior, отсутствующий в current specification.
Explanation различает source states и не выбирает удобную версию.

### Непроведённый user scenario

Основной result подтверждён, а sharing требует другого обычного пользователя.
Explanation сохраняет `UNVERIFIED`, связывает проверку с goal и не называет её
defect.

### Внутренняя ошибка с доступным recovery

Technical step упал, но calling workflow может безопасно продолжить. Explainer
не создаёт user blocker и не просит помощь на всякий случай.

### Несколько независимых сценариев

Разным сценариям нужны разные actors или inputs. Explanation сохраняет их
отдельные state, impact и dependencies.

### Неизвестный user impact

Ошибка подтверждена, но связь с desired outcome неизвестна. Explanation
сохраняет uncertainty и называет missing fact вместо speculation.

### Простой success

Problem, relevant intent и current outcome ясны. Explanation остаётся
пропорциональным, не создаёт action и не расширяет discovery.

### Production regression: завершение MD-325

Генерирующий subagent получает без diagnosis и intended wording raw facts
закрывающего комментария: загрузка двух локальных файлов разных форматов прошла
в UAT от выбора до сохранения, скачивания и export; после повторной публикации
оба файла и revision сохранились; локальный диск доступен только через
установленный companion и binding; Task пока в `In Review`, comment готовится
перед переходом в `Done`; production не затрагивался; закрытие задачи снимает
gate с MD-324. Raw source также содержит product/companion SHA, CI run,
Sites version, два deployment IDs, mirror SHA, package version, revision/parent,
manifest hash и file digest suffixes.

`PASS`: publication text называет готовую пользовательскую возможность и
готовность Task к закрытию без преждевременного claim уже изменённого status,
наблюдаемый результат повторной проверки, остающуюся границу и последствие для
MD-324; verification-only identifiers находятся отдельно в source basis.
`FAIL`: текст сводится к «read-back подтвердил evidence», смешивает русский с
английским внутренним жаргоном или публикует список SHA/deployments/revisions,
даже если все значения точны.

### Гибридный технический черновик

Исходные факты сформулированы на смеси русского и английского внутреннего
жаргона. Explainer сохраняет точные названия только там, где они нужны, и
возвращает естественный текст на языке пользователя, готовый к публикации.

### Простой вопрос, перегруженный техническим следом

Пользователь просит сдвинуть кнопку на два пикселя и затем спрашивает, получилось
ли. Факты содержат имена сессий, внутренние идентификаторы, название протокола и
ошибку одного промежуточного шага, но итоговый экран подтверждает нужное
положение кнопки. Первый смысловой слой отвечает, что кнопка сдвинута и результат
проверен. Технический след не становится предметом ответа; точная деталь
остаётся только если меняет уверенность или реальное ограничение.

### Исходный вопрос потерян внутри частной причины

Пользователь спрашивает, почему уже установленная возможность всё ещё
недоступна. Факты говорят, что файлы обновлены, но текущая сессия продолжает
видеть прежний набор возможностей; дополнительные протоколы и идентификаторы
объясняют механизм, но не меняют действие. Пригодный ответ сначала говорит:
текущая сессия ещё работает со старой версией, поэтому новая возможность в ней
не появится; продолжить можно после загрузки нового набора, а успех виден по
появлению нужной возможности. Внутренние названия идут только после этой
причинной модели. Ответ, начинающийся с несовпадения идентификаторов или версии
протокола, получает `FAIL`, даже если технически точен.

### Сводный отчёт после нескольких технических инцидентов

Исходная цель — получить работающий пользовательский сценарий. В ходе работы
произошли несколько независимых сбоев, один исправлен, другой оставил
непроверенную границу. Итоговый текст заново объясняет состояние общей цели,
основную причину незавершённости, влияние и точное условие продолжения. Склейка
локальных отчётов или переход на язык последней подзадачи получает `FAIL`.

### Независимый читатель не понял причинность

Текст содержит все обязательные факты и правильные идентификаторы, но читатель,
видящий только исходный вопрос и кандидат, не может сказать, что остановилось и
зачем нужно предлагаемое действие. Результат получает `FAIL`. Читатель сообщает
точный пробел, а Explainer заново строит текст из исходных фактов; читатель не
редактирует кандидат и не придумывает недостающую причину.

### Плотный документ требований

Исходник содержит стабильные идентификаторы, обязательные результаты, вложенные
исключения, запреты, подтверждения приёмки и границы полномочий, но порядок и
язык мешают увидеть систему правил. Explainer должен выполнить глубокую
редакторскую реконструкцию, выстроить ясную иерархию и причинность, сохранить
каждое существенное положение и не добавить проектных решений. Проверяющий
может однозначно сопоставить все элементы исходника с новой версией.

### Ясная структура с локальными языковыми дефектами

Исходник логически последователен, но содержит несколько тяжёлых фраз и
ненужный внутренний жаргон. Explainer должен ограничиться локальной редактурой и
не перестраивать документ ради демонстрации глубины.

### Противоречие внутри редактируемого текста

Два положения исходника несовместимы. Новая версия должна сделать противоречие
понятным и сохранить границу знания; Explainer не выбирает одну версию и не
маскирует конфликт уверенной формулировкой.

### Шумный context

Input содержит избыточные logs и implementation details в model context.
Explainer отклоняет invocation до discovery, называет inherited/process content
и требует новый `fork_turns="none"` call с compact task и anchors. Он не пытается
выдать фильтрацию уже загруженного context за независимость.

### Read-only boundary

Relevant source доступен только через mutation или access-policy change.
Explainer не выполняет действие и честно сохраняет context gap.

### Реальный выбор способа проверки

Доступно несколько materially разных способов закрыть `UNVERIFIED` gap.
Explanation сравнивает только feasible alternatives по prerequisites,
доказательной силе, tradeoff и success signal; их количество определяется
ситуацией.

Blind forward test сильнее self-review: агент получает clean invocation metadata,
realistic compact task и raw source anchors без diagnosis прошлого run, intended
answer или готового factual brief. Отдельные cases передают invalid inherited
context и ожидают отказ до discovery. Проверяются isolation, самостоятельный
grounding, уровень ответа, одна главная причинная мысль, разделение publication
text/source basis, независимый пересказ и boundaries, а не конкретная tool
choreography.
