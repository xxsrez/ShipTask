# Task Composer: требования пользователя

Статус: current Level 1, 2026-08-27.

Этот документ — полный пользовательский исходный код только для
`$ship-tasks:task-composer`. Он не определяет требования к ShipTask или
Strategic Explainer; их использование ниже является локальной dependency Task
Composer.

Требования задают обязательный outcome, rationale, observable evidence и
scope/truth/safety/authority boundaries. Architecture и runtime могут
переформулировать и конкретизировать их, но не могут ослабить, заменить или
молча удалить. Изменение смысла Level 1 требует явного решения пользователя.
План, decomposition, tools, число попыток, context и внутренний reasoning
остаются свободными, если точный механизм не назван здесь отдельным инвариантом.

`architecture.md` хранит agent-owned current способ достижения этих требований.
`task-composer/SKILL.md` является компактной смысловой компиляцией обоих файлов.
Если runtime удалить и пересобрать из них, новый skill должен быть примерно
эквивалентен по всем требованиям `TC-*` и выбранной архитектуре.

## Требования

### `TC-01` — Planning-only boundary

Task Composer формулирует и по явному intent создаёт Task Manager planning
scope, но не реализует, тестирует, выпускает или принимает работу, не создаёт
Goal и не запускает ShipTask delivery. Просьба только сформулировать или показать
draft не разрешает writes; просьба создать/add/capture разрешает только planning
mutations. Создать ровно одну Task и сразу выполнить её — отдельный ShipTask
create-and-deliver flow, а не обход этой границы.

### `TC-02` — Human intent без придуманного scope

Созданная planning model сохраняет problem, desired outcome, exact scope,
requirements, constraints и non-goals пользователя. Недостающий material выбор
не маскируется гладким текстом и не угадывается из старой памяти.

### `TC-03` — Минимальная полезная decomposition

Один independently deliverable outcome остаётся одной Task. Составной связный
outcome становится Epic только когда нужны несколько самостоятельных
deliverables; подзадачи совместно покрывают его без скрытого остатка,
дублирования ownership и формального дробления ради количества карточек.
Несколько независимых outcomes остаются отдельными Tasks/Epics и не сливаются в
искусственный umbrella Epic. Используется самая мелкая полезная иерархия.

### `TC-04` — Problem-first Epic и исполнимые Tasks

Epic объясняет проблему, beneficiary, цель и cross-cutting boundaries.
Подзадачи содержат конкретный результат, достаточную техническую границу,
acceptance, evidence и реальные dependencies. Tactical detail не вытесняет
смысл, а high-level Epic не оставляет исполнителю технические пробелы.

### `TC-05` — Live Task Manager projection

Project, statuses, Labels, Release, hierarchy, relations и duplicate candidates
разрешаются из current Task Manager. Каждая новая Task получает exact Project и
canonical `Backlog`. Release назначается только когда он явно выбран или
однозначно current; неизвестный Release не угадывается и не блокирует создание.
Если exact Project или canonical `Backlog` отсутствуют, create не начинается и
default не подставляется. Released Release требует отдельного явного выбора, а
последний по номеру или дате не считается current автоматически.

### `TC-06` — Semantic metadata

Labels, hierarchy и relations отражают реальный смысл каждой Task. Task type не
дублируется текстовым префиксом title. Task Composer не создаёт и не изменяет
Label taxonomy без отдельного явного запроса и не выстраивает relations ради
формальной полноты. Missing Label оставляет чистый outcome title и видимый
taxonomy gap, а не текстовый fallback. Exact title, который пользователь явно
потребовал сохранить verbatim, не нормализуется. Parent-child остаётся native
hierarchy; relation type и direction проверяются по реальной dependency, а
независимые подзадачи не связываются искусственной цепочкой.

### `TC-07` — Duplicate safety и write integrity

Перед созданием выполняется bounded duplicate check. Exact duplicate не
создаётся. Writes получают reconciliation и read-back; partial result не
скрывается и не удаляется destructive cleanup без authority. Unknown outcome не
повторяется вслепую: сначала ищется возможный созданный объект. Если multi-Task
write остановился частично, result перечисляет confirmed, unknown и not-created
scope и точное безопасное условие продолжения.

### `TC-08` — Secret-safe planning

Tasks могут ссылаться на имя credential, secret store или target, но не
содержат secret values, signed URLs или private runtime material.

### `TC-09` — Strategic Explainer для каждого Epic

Problem-first описание каждого Epic проходит sibling Strategic Explainer,
который является opaque provider и не выбирает decomposition, metadata, writes
или authority. Task Composer остаётся ответственным за factual accuracy и
полное покрытие. Если grounded provider result недоступен, Epic create не
начинается; независимо допустимая single Task от этого не блокируется.

Каждый Epic description является отдельным пользовательским результатом и
получает новый clean built-in `default` subagent с `fork_turns="none"`. Task
Composer передаёт короткую задачу, exact planning scope и разрешимые source
anchors без предыдущего диалога, process diary, собственного strategic view или
готового candidate. Он не читает provider-internal contract, не передаёт
требования к форме description, не пишет explanation draft и не применяет
методику Explainer самостоятельно. Готовый text проверяется только на material
factual conflict с authoritative planning sources. Если Explainer отклоняет
invocation либо source/anchor нужно исправить, Task Composer автоматически
вызывает новый экземпляр; старый context не продолжается, result самостоятельно
не улучшается и обязательная независимость не обходится.

### `TC-10` — Независимая planning distribution

Task Composer остаётся отдельным planning-only runtime skill внутри
`ship-tasks@srez-marketplace` и использует отдельно установленный Task Manager
только как adapter. Для `TC-09` он использует отдельно установленный
`$strategic-explainer:strategic-explainer`; копия provider-а в ShipTask package
не встраивается. Он не переносится в adapter plugin, не получает скрытый
delivery lifecycle и не устанавливается standalone user-level duplicate.
Checked-in runtime source, Marketplace source и installed cache после изменения
должны быть byte-identical, а plugin-qualified skill проверяется в fresh Codex
session.

### `TC-11` — Стратегическая преемственность от Epic к Task

Когда план или крупная цель требуют Epic, Task Composer сохраняет стратегическое
видение не только в parent Task, но и доводит его применимую часть до каждой
подзадачи. Native hierarchy указывает на полный контекст Epic, а description
подзадачи содержит компактную самодостаточную проекцию: какую часть общего
результата она даёт, какие parent requirements, ограничения и non-goals к ней
относятся и какой локальный результат должен быть доказан. Исполнитель не должен
восстанавливать этот смысл из технического title или догадываться, чем нельзя
пожертвовать ради локально удобного решения.

Шаги исходного плана не превращаются в Tasks механически: decomposition следует
независимо проверяемым outcomes, реальным dependencies и целостному покрытию
Epic. Стратегический контекст направляет выбор решения и планку качества, но не
расширяет exact scope или полномочия дочерней Task. Material противоречие между
Epic и подзадачей остаётся видимым и не сглаживается уверенной формулировкой.

### `TC-12` — Уместные attachments из bug report

Если пользователь просит создать Task по сообщению о баге и передал attachment,
Task Composer оценивает его уместность по содержанию и роли в конкретной Task.
Уместный материал напрямую связан с описанной проблемой и помогает исполнителю
увидеть её проявление, воспроизвести, локализовать, понять релевантный контекст
либо проверить исправление. Тип или формат attachment, включая screenshot, сам
по себе не делает материал ни уместным, ни неуместным. Уместный attachment
сохраняется как native attachment той создаваемой Task, для которой он является
evidence.

Уместный attachment не заменяется пересказом, локальным путём, временной или
защищённой ссылкой и не пропускается молча. Явно нерелевантный, случайный,
избыточный либо нарушающий `TC-08` материал не добавляется, а его disposition
остаётся видимым. Создание считается полным только когда read-back подтверждает
каждый обязательный attachment на правильной Task. Если доступный source нельзя
провести через native attachment transport, Task Composer не объявляет scope
успешно созданным: result честно различает not-created и partial scope, называет
missing attachment и безопасное условие продолжения.

## Изменение Level 1

Новый запрос меняет этот файл только если пользователь меняет обязательный Task
Composer result, invariant или boundary. Просьба улучшить architecture,
упростить процесс, сменить tool или найти лучший способ достижения сохраняет
Level 1 и относится к `architecture.md`.
