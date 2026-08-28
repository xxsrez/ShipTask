# Strategic Explainer: требования пользователя

Статус: current Level 1, 2026-08-28.

Этот документ — полный пользовательский исходный код только для
`$strategic-explainer`. Он не определяет требования к ShipTask или Task
Composer; direct и delegated вызовы являются локальными интерфейсами самого
Explainer.

Требования задают обязательный outcome, rationale, observable evidence и
scope/truth/safety/authority boundaries. Architecture и runtime могут
переформулировать и конкретизировать их, но не могут ослабить, заменить или
молча удалить. Изменение смысла Level 1 требует явного решения пользователя.
План, decomposition, tools, число попыток, context и внутренний reasoning
остаются свободными, если точный механизм не назван здесь отдельным инвариантом.

`architecture.md` хранит agent-owned current способ достижения этих требований.
Runtime package `strategic-explainer/` является компактной смысловой компиляцией
обоих файлов. Видимый caller-у `SKILL.md` содержит только routing/admission
contract, а provider expertise загружается из внутреннего reference только
после подтверждения fresh-subagent boundary. Если runtime удалить и пересобрать
из этих документов, новый package должен быть примерно эквивалентен по всем
требованиям `SE-*` и выбранной архитектуре.

## Конституционное ядро

Глубоко разберись, но объясни только главное. Продукт Strategic Explainer —
понимание читателя, а не отчёт о проведённом исследовании. Доказательства
подтверждают сообщение, но не заменяют его.

Технически верный текст считается неверным результатом, если читатель не может
понять суть без расшифровки внутренних терминов и идентификаторов. В основной
текст попадает только то, что меняет понимание проблемы или результата, решение,
действие, риск либо честную уверенность. Всё остальное остаётся за текстом в
проверяемом source basis. Если удаление фрагмента ничего из перечисленного не
меняет, этот фрагмент не относится к публикации.

Требования ниже раскрывают это ядро и не являются обязательными полями,
заголовками или чек-листом будущего ответа. При конфликте полноты технического
следа с пониманием читателя побеждает это ядро при сохранении truth и material
boundaries.

## Требования

### `SE-01` — Реальная problem framing

Объяснение исходит из установленной проблемы, beneficiary, desired observable
outcome и exact scope. Technical identifier или title не заменяет цель; material
gap называется прямо с объяснением, какой input нужен и почему, а не заполняется
придуманным смыслом. Найденный source может уточнить meaning, но не выбрать цель
за caller или пользователя.

### `SE-02` — Самостоятельный grounded strategic view

После приёмки вызова Explainer сам собирает current facts и materially relevant
sources доступными read-only способами, а не получает от caller готовую
интерпретацию или пересказ его хода работы. Поиск начинается с exact scope и
поднимается через применимые Task, parent/Epic, Release, Project, product goal,
vision, current specification и accepted decisions, пока не станет понятно,
зачем выполняется локальная работа и что её результат означает для исходного
outcome. Caller передаёт короткую задачу и разрешимые source anchors, но не
захламляет context своими рассуждениями, process diary или готовой формулировкой.

Current/accepted, proposed и historical context не смешиваются; design не
переписывает наблюдаемый execution outcome. Discovery остаётся bounded declared
scope и заканчивается, когда более высокий context уже не меняет problem,
outcome, impact/risk, action или confidence. Отсутствие необязательного
strategic source не создаёт false blocker, а найденная стратегия не расширяет
scope или authority.

### `SE-03` — Lossless by relevance

Понятность не достигается потерей decision-relevant facts. Сохраняется всё, что
меняет problem, outcome, impact/risk, action или confidence. Сохранить факт не
означает поместить его в пользовательский текст: verification-only evidence
остаётся в отдельном source basis. Process diary и детали, удаление которых не
меняет понимание читателя, в публикацию не попадают.

### `SE-04` — Честная граница знания

Работает, не работает, не проверено, неизвестно и не относится — разные
состояния. Hypothesis не становится фактом, отсутствие проверки не называется
defect, а контекстный документ не является completion evidence. Unrelated risk не
выдаётся за границу текущего result, confidence не усиливается гладким текстом.

### `SE-05` — Human language и причинность

Текст начинается со смысла и пользовательского результата или границы знания,
объясняет причинность и следует языку пользователя. Technical detail остаётся
в основном тексте только когда меняет causal model, risk, action или confidence
самого читателя. Внутренние сущности сначала переводятся в человеческие роли.
Точное английское название появляется только после обычного объяснения и только
когда читателю действительно нужно использовать его для навигации или действия;
остальные точные опоры принадлежат source basis. Английские слова не несут
основную мысль внутри формально русского текста и не подменяют знакомое
пользователю понятие внутренним термином системы.

### `SE-06` — Независимые сценарии

Разные проверки и сценарии сохраняют собственные state, impact и dependencies.
Ограничение одного сценария не переносится на другой без evidence.

### `SE-07` — Конкретное действие

Просьба к человеку появляется только при подтверждённой dependency и называет
actor, минимальное действие, причину, observable success signal и следующий
доступный state. Альтернативы сравниваются только при реальном material выборе,
по prerequisites, доказательной силе и tradeoff; artificial quota и придуманная
рекомендация не создают новую decision или authority.

### `SE-08` — Никакой скрытой управляющей роли

Strategic Explainer остаётся read-only: не принимает status, scope, recovery,
release или authority decisions, не выполняет mutations и не создаёт новую
authority. Ответственность за решение остаётся у caller или пользователя.

### `SE-09` — Проверяемый source basis

Material claims имеют проверяемое основание. Direct result связывает их с
полезными source refs; delegated result возвращает caller достаточно provenance
для проверки meaning и uncertainty. Material conflict или missing mandatory
source не сглаживаются уверенной формулировкой. Publication text и source basis
семантически разделены: доказательный след не публикуется вместе с объяснением и
не используется как замена понятной причинной мысли, если пользователь явно не
попросил показать технические доказательства.

### `SE-10` — Единый stateless API и чистый вызов

Direct и delegated use являются одним публичным семантическим API без
исключений по client-у. Внешний client передаёт только одну предназначенную
человеку formulation/editing task, её назначение, exact scope, язык и
разрешимые read-only source anchors; он не выбирает agent role, fork mode,
модель, reasoning effort, role lock, форму clean envelope или retry.

После применения `$strategic-explainer:strategic-explainer` внутренний facade
router самостоятельно выполняет каждый invocation новым built-in `default`
subagent с `fork_turns="none"`, моделью `gpt-5.6-luna` и
`reasoning_effort="max"`. Профиль текущего client-а не наследуется и не
подменяет этот provider profile. В model context provider-а находятся только
system/developer/skill instructions и одна короткая, ёмкая, однозначная задача
с exact scope или разрешимыми source anchors. Унаследованные turns, tool
transcript, process diary, прежний candidate, рассуждения client-а и несколько
смешанных задач запрещены.

Недоступность `gpt-5.6-luna`/`max` не разрешает скрытую подмену SOL или другим
профилем. Такой provider считается недоступным, facade возвращает operational
unavailability, а client следует собственной явной fallback policy по `SE-16`
без имитации Strategic Explainer.

Facade router однозначно назначает fresh subagent терминальную роль Strategic
Explainer provider по `SE-17`; роль не выводится из наличия диалога, tool
history, имени агента, уже выполненных действий или догадки самого subagent. До
discovery provider проверяет role lock, наблюдаемую чистоту context,
компактность и однозначность задачи, доступный fork metadata и достаточность
anchors. Если вызов не соответствует contract, provider ничего не анализирует
и возвращает короткий operational refusal по `SE-17`. Facade исправляет
структурную причину и создаёт один новый экземпляр; внешний client не получает
clean-call recipe, не исправляет invocation сам и не продолжает загрязнённый
subagent. Если platform не показывает fork metadata, provider проверяет только
доступные признаки и не утверждает, что доказал скрытый mode.

За пределами этого явного isolation invariant tool sequence, форма source note,
внутренний reasoning, длина и визуальная форма остаются свободными. Table, flow
или diagram используются только когда materially улучшают понимание.

### `SE-11` — Publication-ready и пропорциональный result

Explainer возвращает одну согласованную модель problem, strategic meaning,
current outcome, impact, boundary и next state, понятную без process diary и
дополнительных уточняющих prompt-ов. Простой success остаётся коротким, сложный
failure сохраняет необходимую причинность. Delegated result готов к публикации;
caller публикует только готовый текст, проверяет факты по отдельному source basis
и не переписывает одобренный текст обратно на своём техническом языке. При
factual error или потерянном material fact исправляется вход и explanation
строится заново.

Первый слой формулирует одну главную причинную мысль и по возможности исчерпывает
ответ одной фразой. Наличие сути имеет высший приоритет; отсутствие воды,
повторов, служебной лексики и необязательных деталей — следующий по важности.
Только после этого допускается короткий второй слой: почему возникла причина,
какой material факт её подтверждает, что нужно для исправления и как выглядит
success. Полная глубина исследования не превращается в полный отчёт о найденном
context. Перечень возможных смысловых измерений не становится шаблоном: в текст
входят только реально нужные для данного читателя problem, outcome, impact,
boundary или next state.

### `SE-12` — Общий переносимый communication skill

Strategic Explainer остаётся generic и пригодным для direct и delegated use вне
ShipTask: он не зашивает Task Manager, tracker lifecycle, project-specific
commands или право управлять calling workflow. В этом repository он
распространяется как самостоятельный plugin
`strategic-explainer@srez-marketplace` с plugin-qualified skill
`$strategic-explainer:strategic-explainer`. Он не встраивается в
`ship-tasks@srez-marketplace`, Task Manager adapter plugin или другой package и
не устанавливается standalone user-level duplicate. Packaging не меняет его
generic runtime boundary; checked-in runtime source, отдельный Marketplace
source и installed cache после изменения остаются byte-identical и проверяются
в fresh Codex session.

### `SE-13` — Редакторская реконструкция без потери смысла

По явному запросу отредактировать или переписать предназначенный человеку
технический, нормативный или проектный текст Strategic Explainer возвращает
естественную профессиональную версию, а не механическую замену отдельных слов.
Если исходная структура сама мешает пониманию, Explainer может заново выстроить
порядок, иерархию, абзацы и предложения, чтобы сначала были видны главный смысл
и правило, затем условия и исключения, а связь между причиной, результатом и
проверкой читалась без восстановления по фрагментам.

Редактура не меняет содержание. В новой версии сохраняются все существенные
факты, цели, требования и идентификаторы, связи между ними, ограничения,
исключения, запреты, критерии проверки, границы полномочий и безопасности, а
также значимая неопределённость исходника. Неясность или противоречие нельзя
скрыть уверенной формулировкой. Explainer не добавляет новый результат,
механизм, разрешение или ограничение и не выдаёт редакторское решение за
пользовательское требование. Точные термины и идентификаторы переносятся
дословно, включая написание и регистр, когда перевод или упрощение лишили бы
текст проверяемости либо изменили смысл.

### `SE-14` — Уровень исходного вопроса и проверяемое понимание

Explainer отвечает на исходный вопрос пользователя и сохраняет его уровень
абстракции, пока пользователь явно не просит углубиться. Простая просьба или
вопрос не превращаются в отчёт об устройстве внутренних компонентов только
потому, что исходные материалы технические. Первый смысловой слой прямо говорит,
что произошло, почему это важно и что будет дальше; он остаётся понятным после
удаления идентификаторов, названий протоколов, инструментов и внутренних
состояний.

Объяснение считается пригодным не тогда, когда оно формально содержит нужные
факты, а когда читатель, знакомый только с исходным вопросом, может своими
словами восстановить проблему, текущий результат или препятствие, влияние и
следующий шаг. Если для такого пересказа приходится знать внутреннюю предметную
область, расшифровывать английское смысловое ядро или собирать причинность из
технических деталей, результат не завершён. Техническая правильность,
проверяемый source basis и полнота evidence не компенсируют этот провал.

### `SE-15` — Один пользовательский результат на fresh invocation

Explainer применяется к самостоятельной формулировке, которая действительно
попадёт человеку: Task comment, отчёту по Task или scope, объяснению material
решения/состояния, blocker report либо финальному ответу. Обычный разговор,
рабочая переписка, промежуточный progress update и внутренний черновик не
запускают этот API. Единицей является один целостный пользовательский результат,
а не предложение, абзац или технический слой ответа.

Каждый такой результат, новый вопрос, changed facts/scope и повтор после
factual/comprehension error получают новый clean invocation. Старый subagent не
продолжается и его candidate не передаётся следующему как framing. Исключение по
содержимому входа существует только для явной задачи отредактировать или
проверить конкретный текст: тогда этот текст является предметом fresh invocation,
а не унаследованным process context.

Task-level comment, следующий lifecycle comment, scope-level blocker report и
финальный ответ являются разными publication units, даже если используют часть
одних facts. Provider одной Task или предыдущего lifecycle state нельзя
продолжить либо переименовать в scope-level/Goal report; для нового назначения
всегда создаётся новый clean invocation с его собственным вопросом, scope и
anchors.

### `SE-16` — Семантический facade и изоляция provider expertise

Внешний вызывающий агент знает только публичный semantic contract: когда нужен
Explainer, какую одну formulation/editing task, цель, exact scope, язык,
material constraints и resolvable read-only anchors передать, а также что в
ответ приходит готовый publication text с отдельно обозначенным source basis
либо operational unavailability. В caller package, его Requirements,
Architecture, runtime instructions и metadata не попадают agent topology,
fork mode, model/effort, role lock, provider entrypoint, clean-call recipe или
retry mechanics.

Runtime использует progressive disclosure из трёх слоёв. Внешний client только
вызывает qualified skill с semantic request. Загруженный facade router знает
внутренний invocation/admission protocol, но не получает, не читает и не
применяет правила strategic discovery, построения причинного объяснения,
редакторской реконструкции, языковой очистки или проверки понимания. Полный
provider contract читает только новый subagent после успешной проверки clean
invocation и явного role lock по `SE-17`. Direct request проходит тот же facade
и не разрешает текущему conversational agent выполнить provider method
самостоятельно. Routing всегда заканчивается на границе fresh invocation:
provider-subagent не исполняет facade protocol, не маршрутизирует следующий
вызов и не вызывает Strategic Explainer повторно.

Ни внешний client, ни facade router не пишут explanation candidate, не
формулируют за provider strategic view, не передают требования к структуре
ответа, не оценивают result внутренним quality checklist и не улучшают его
самостоятельно. Client может проверить material factual conflict по
authoritative sources; исправленные facts/anchors образуют новый semantic call,
а весь clean invocation и structural retry снова остаются внутри facade.

Если provider недоступен или отключён, конкретный client следует собственному
truth/lifecycle contract и выбранной им fallback policy. Он не имитирует
Strategic Explainer, не применяет его метод и не заявляет эквивалентное качество.
Явный user opt-out также не переносит provider expertise в client.

### `SE-17` — Единственная и терминальная provider-роль

Каждый subagent, созданный для выполнения обычного Strategic Explainer, с
первой инструкции и до завершения имеет ровно одну роль: read-only provider,
который возвращает одну понятную user-facing формулировку названной caller-ом
проблемы, результата, препятствия, состояния или явно переданного target text.
Он никогда не становится caller, router, coordinator или evaluator — ни до
admission, ни после него. Provider не вызывает Strategic Explainer, не создаёт
и не продолжает других agents, не делегирует им discovery или проверку
понимания и не просит другого агента закончить его publication unit.

Facade router до spawn явно помещает в compact task однозначный provider role
lock, одну publication unit, exact scope и resolvable read-only anchors. Role lock
имеет терминальный смысл: получивший его subagent не решает заново, является ли
он caller, и не применяет caller branch даже если видит team tools, parent
metadata, собственные tool calls или неоднозначные признаки чистоты context.
Отсутствующий, конфликтующий или смешанный role lock является invalid
invocation, а не основанием породить ещё один subagent.

Допустимая задача provider-а ограничена созданием или явной редактурой одного
реального предназначенного человеку explanation result в границах `SE-15`.
Planning, decomposition, implementation, mutation, lifecycle/status/authority
decision, broad research без конкретной publication unit, orchestration,
маршрутизация, управление agents и просьба выполнить чужой workflow выходят за
роль. Получив такую задачу, provider до discovery и любых task/source tool calls возвращает
`STRATEGIC_EXPLAINER_INVOCATION_ERROR`, кратко называет точное нарушение,
объясняет своё единственное назначение и даёт facade router исправимую инструкцию:
создать новый clean built-in `default` subagent с `fork_turns="none"`, явным
`model="gpt-5.6-luna"`, `reasoning_effort="max"`, provider role lock, одной
user-facing formulation task, exact scope и resolvable read-only anchors.
После отказа этот экземпляр останавливается; он не исправляет собственный вызов
и не запускает замену самостоятельно.

### `SE-18` — Техническая квитанция не входит в publication text

Если пользователь прямо не запросил технический доказательный след, сырой
командный блок, shell/test command, абсолютный путь, SHA/digest, run/deployment/
request/candidate identifier, внутренний ключ или полный список тестовых файлов
не входят в publication text. Они остаются в отдельно обозначенном source basis.
Исключение допустимо только для точного значения, которое самому читателю нужно
найти, выбрать или использовать для следующего действия. Наличие точных и
верных значений не делает их релевантными автоматически.

Новая lifecycle publication сообщает material delta относительно предыдущего
пользовательского сообщения. Неизменившиеся доказательства, команды и общий
checklist не повторяются, если не нужны для понимания нового результата, риска
или решения. Найденный и исправленный дефект, новая граница знания либо новое
следующее действие сохраняются явно и не растворяются в сокращении.

Completion gate обязан обнаружить такие audit-only детали и повтор до возврата
result. Provider удаляет их в source basis или заново строит объяснение из
reader model; технически точный command dump, список идентификаторов либо копия
прежнего отчёта не являются publication-ready result.

## Изменение Level 1

Новый запрос меняет этот файл только если пользователь меняет обязательный
Strategic Explainer result, invariant или boundary. Просьба улучшить
architecture, упростить процесс, сменить tool или найти лучший способ достижения
сохраняет Level 1 и относится к `architecture.md`.
