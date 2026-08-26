# Task Composer

Статус: current Level 2 contract, 2026-08-26. Применимые Level 1 requirements —
`TC-*` в локальных
[требованиях пользователя](requirements.md). Эта architecture описывает
current архитектуру достижения и не может ослаблять Level 1. Архитектурная роль
и distribution зафиксированы в
[ADR-0023](../../decisions/0023-task-composer-as-planning-sibling.md).

## 0. Compilation contract

Эта architecture вместе с локальным `requirements.md` является полным current
source package `$ship-tasks:task-composer`. Runtime `task-composer/SKILL.md` —
производная смысловая компиляция этих двух документов: его можно удалить и
собрать заново, сохранив все `TC-*` и выбранную здесь реализацию примерно
эквивалентными по наблюдаемому поведению. ADR, reports и evaluations дают
rationale и evidence, но не являются параллельным current contract.

Specification описывает Task Manager-only skill `$ship-tasks:task-composer`, который
формулирует, декомпозирует и по явному planning intent создаёт качественные
Tasks. Он не выполняет созданную работу и не управляет delivery lifecycle.

## 1. Назначение и routing

Task Composer превращает требования человека в связную planning-модель:

- одна независимо исполнимая работа остаётся одной Task;
- составной outcome становится Epic — parent Task с несколькими подзадачами;
- Epic сохраняет problem, strategic intent, требования и границы человека;
- подзадачи получают конкретный исполнимый scope, технические детали,
  acceptance criteria и ожидаемое evidence;
- labels, hierarchy и relations отражают фактический смысл, а не формальную
  полноту карточки.

Skill доступен явно через `$ship-tasks:task-composer` и неявно, когда пользователь просит
сформулировать, создать, добавить в backlog или разложить Task Manager работу.
Draft без просьбы о записи остаётся draft. Явная просьба создать/add/capture
разрешает только соответствующие planning mutations.

Task Composer не активируется для implementation, fix, test, delivery,
release, status, audit или простого чтения существующих Tasks. Запрос создать
ровно одну Task и сразу выполнить её относится к ShipTask create-and-deliver,
а не к planning-only Task Composer.

### 1.1 Проверяемая trigger matrix

| Запрос | Task Composer | Результат |
|---|---|---|
| `$ship-tasks:task-composer` | да | сформировать planning model; writes только при явном intent |
| `Сформулируй Task Manager задачу, пока не создавай` | да | read-only draft |
| `Создай Task в Task Manager` | да | одна Task либо Epic с подзадачами по реальному scope |
| `Разбей это на Epic и подзадачи в Task Manager` | да | Epic и достаточные подзадачи |
| `Просто добавь это в backlog` | да | planning-only capture без implementation |
| `Спланируй это в текущем Task Manager Project` | да | compose и create при однозначном Project context |
| `Выполни TM-123` | нет | ShipTask delivery |
| `Создай одну Task и сразу выполни её` | нет | ShipTask create-and-deliver |
| `Покажи статус TM-123` | нет | read-only Task Manager adapter |
| `Проведи аудит TM-123` | нет | read-only Task Manager adapter |
| `Исправь код` | нет | обычная implementation без Task Manager planning anchor |

## 2. Planning boundary

Task Composer создаёт или формулирует planning artifacts, но не:

- меняет существующую implementation Task ради delivery;
- переводит созданные Tasks из `Backlog`;
- реализует, тестирует, выпускает или принимает результат;
- создаёт Goal;
- создаёт, переименовывает или архивирует Label taxonomy;
- придумывает Project, Release, status, label или Task refs;
- переносит secret values, signed URLs или credentials в Task text.

Если пользователь одновременно просит спланировать и выполнить работу,
Task Composer может подготовить Task Manager scope, но дальнейшая delivery
принадлежит ShipTask и его отдельному lifecycle contract.

## 3. Live scope и preflight

Task Manager connector остаётся единственным task adapter. До write skill
разрешает live workspace, exact Project, доступ на запись, workflow statuses,
доступные Labels и candidate duplicates. Memory, repository name и предыдущий
run могут подсказать selector, но не заменяют current read.

Каждая Task требует однозначного Project. Если Project нельзя безопасно
определить, skill запрашивает его и не создаёт orphaned или guessed Task.

Все новые Tasks создаются в canonical status `Backlog`. Если Project не
предоставляет такой status, preflight не пройден: skill не подменяет его
default status и не начинает частичное создание.

Release назначается только когда пользователь явно его выбрал либо current
Project context однозначно определяет текущий unreleased Release. Последний по
номеру, имени или дате Release сам по себе не является current. Если current
Release неизвестен или неоднозначен, `releaseRef` опускается, создание
продолжается и отсутствие Release сообщается. Добавление в уже released
Release требует отдельного явного подтверждения.

Перед write выполняется bounded duplicate search по Project и materially
relevant title/problem terms. Exact duplicate не создаётся. Material overlap
сначала изучается; существующую Task можно reuse, изменить или связать только
когда это соответствует явному intent пользователя.

## 4. Композиция задачи

Сначала формируется целая candidate-модель без writes: Project/Release/status,
parent, children, descriptions, labels и relation graph. Модель должна покрыть
требования человека без придуманного scope и без технических пробелов между
подзадачами.

Исходный план является материалом для понимания цели и зависимостей, а не
готовым списком карточек. Task Composer строит outcome graph: отделяет
independently verifiable results от действий и промежуточных шагов, а порядок
фиксирует relation только там, где одна часть действительно требует результат
другой.

Не объединяй независимые desired outcomes в искусственный umbrella Epic. Один
связный outcome получает одну standalone Task или один Epic; несколько
независимых outcomes сохраняются отдельными Tasks/Epics и связываются только
при реальной relation.

Title кратко называет ожидаемый результат и объект изменения. Epic title
отражает strategic outcome, subtask title — конкретный deliverable. Избегай
служебных заголовков про работу агента и расплывчатых формул, которые нельзя
отличить от соседней Task. Форма description свободна, если смысл, requirements
и проверяемость сохраняются.

Task type и другая classification metadata выражаются native Labels и
hierarchy, а не дублируются в title. Если live catalog содержит `Bug`, `Epic`,
`Feature`, `Improvement`, `Spike`, `Release blocker` или другой применимый
classification Label, title не получает соответствующий префикс/суффикс:
`BUG:`, `EPIC:`, `[Bug]`, `Epic —`, `Feature:` и локализованные эквиваленты
запрещены. Если подходящего Label нет, textual prefix не является fallback:
Task создаётся с чистым outcome title, а taxonomy gap сообщается отдельно.
Исключение — только exact title, который пользователь явно потребовал сохранить
verbatim.

Duplicate search сравнивает outcome title также после удаления известных
legacy classification prefixes. `BUG: Исправить X` и `Исправить X` являются
одним title candidate и требуют проверки описания до любого create.

### 4.1 Одна Task

Оставляй одну Task, когда работа имеет один independently deliverable outcome
и не требует нескольких самостоятельных acceptance результатов. Не создавай
Epic с единственной формальной подзадачей и не дроби работу только ради
количества карточек.

Одиночная Task содержит:

- problem и ожидаемый observable outcome;
- exact scope и material constraints человека;
- достаточную техническую конкретику для исполнения;
- objective acceptance criteria и ожидаемое evidence;
- явно названные non-goals или dependencies, если они меняют решение.

### 4.2 Epic и подзадачи

Создавай Epic, когда desired outcome требует нескольких независимо исполнимых
частей, разных проверяемых результатов или настоящих dependencies. Используй
самую мелкую полезную иерархию; дополнительный уровень вложенности нужен только
когда он действительно улучшает самостоятельность и проверяемость работы.

Epic объясняет:

- какую проблему, для кого и зачем решаем;
- desired observable outcome и strategic intent;
- exact scope, требования и ограничения, данные человеком;
- cross-cutting acceptance и non-goals;
- как подзадачи вместе дают целостный результат.

Epic не становится свалкой tactical instructions. Техническая деталь остаётся
в нём только когда является явным cross-cutting требованием человека или
меняет смысл всего решения.

Каждая подзадача содержит:

- один конкретный independently deliverable result;
- собственный вклад в desired outcome Epic;
- точную границу изменения и materially relevant technical details;
- применимые parent requirements и dependencies;
- проверяемые acceptance criteria и evidence;
- secret-safe operational references: имя credential/secret store и target,
  но никогда не secret value.

Подзадачи совместно покрывают Epic без скрытого остатка и без дублирования
ownership. Requirement, влияющий на несколько подзадач, остаётся видимым в
Epic и отражается в каждой применимой подзадаче.

### 4.3 Стратегическая преемственность

Epic остаётся каноническим полным источником общей проблемы, desired outcome и
cross-cutting boundaries. Native parent-child hierarchy даёт исполнителю путь к
этому источнику, но одной ссылки недостаточно: description каждой подзадачи
содержит короткую самодостаточную проекцию релевантного смысла. Она прямо
объясняет вклад Task в Epic, применимые стратегические требования, ограничения и
non-goals, а также качества, которыми нельзя пожертвовать ради локального
упрощения. Полный текст Epic при этом не копируется в каждую карточку.

До create candidate-модель проверяется с позиции нового исполнителя, который
видит подзадачу и её parent: он должен суметь назвать общий outcome, собственный
вклад, exact change boundary и применимую планку качества без догадки. Context
Epic помогает выбирать решение внутри этой границы, но не разрешает выполнять
соседние подзадачи или расширять scope. Material gap либо противоречие между
Epic и child остаётся явным и требует исправления planning model до write.

## 5. Strategic Explainer

Перед созданием каждого Epic его problem-first описание составляется с помощью
sibling `$ship-tasks:strategic-explainer`. Каждый Epic description является
отдельным publication unit: Task Composer создаёт новый built-in `default`
subagent с `fork_turns="none"` и передаёт одну compact task, exact planning scope
и resolvable read-only anchors. Унаследованный диалог, tool transcript, process
diary, готовый strategic view и прежний candidate не передаются. Explainer
остаётся opaque provider и не выбирает Project, decomposition, status, labels,
relations или write authority. Task Composer не читает provider-internal
contract, не пишет description candidate и не передаёт требования к тому, как
provider должен анализировать или формулировать result.

Если Explainer отклоняет invocation, Task Composer исправляет указанную причину
и создаёт новый clean subagent; follow-up старому экземпляру не используется.
Готовый text проверяется только на material factual conflict с authoritative
planning sources. Factual correction также получает новый clean invocation;
caller не читает internal quality checklist и не улучшает text самостоятельно.

Основной Task Composer остаётся ответственным за factual accuracy, полноту
coverage и соответствие подготовленной hierarchy. Если Strategic Explainer
выявил material context gap, write не маскирует его гладкой формулировкой. Если
Explainer недоступен или не может подготовить grounded Epic description,
создание Epic не начинается; single Task, которой Epic не нужен, от этого не
блокируется.

## 6. Labels, hierarchy и relations

Labels выбираются только из live active catalog и назначаются каждой Task по
её собственному смыслу. Skill не предполагает наследование label от Epic и не
добавляет label ради того, чтобы поле было непустым. Если подходящего label
нет, Task создаётся без label, а missing taxonomy coverage явно перечисляется
в результате. Создание нового Label не разрешено этим workflow. Label и
hierarchy остаются canonical classification metadata; их смысл не повторяется
в title.

Parent-child hierarchy задаётся native Task Manager relationship. Она не
дублируется relation `related`.

Native relations создаются только для реальной семантики:

- `blocks` — выполнение одной Task фактически необходимо другой;
- `related` — связь полезна для понимания, но не задаёт порядок.

`duplicate_of` не создаётся для нового planning set: exact duplicate вообще не
создаётся. Изменение lifecycle существующей Task как duplicate требует
отдельного явного запроса и не маскируется под композицию нового scope.

Не выстраивай все подзадачи в цепочку по умолчанию. Direction каждого `blocks`
проверяется в человеческой формулировке до write. Relations не могут связывать
Tasks из разных Projects, если current adapter этого не поддерживает.

## 7. Write integrity и completion

После полного preflight parent/standalone Task создаётся с canonical Project,
`Backlog`, необязательным confirmed Release и resolved existing labels. Для
Epic подзадачи создаются native subtask operation с current parent version;
после каждой mutation authoritative state перечитывается. Relations создаются
после существования обоих endpoints с caller-stable idempotency key.

Unknown write outcome сначала reconciles через reads и duplicate search; write
не повторяется вслепую. Поскольку multi-Task create не является транзакцией,
ошибка после частичного результата не скрывается и не вызывает destructive
cleanup без authority: skill перечисляет созданные, подтверждённые и
несозданные элементы и безопасное условие продолжения.

Работа завершена, когда read-back подтверждает для каждого созданного элемента:

- canonical Task/Project identity и `Backlog`;
- Release либо честно зафиксированное отсутствие current Release;
- parent-child hierarchy;
- фактически назначенные labels и известные label gaps;
- отсутствие classification prefix/suffix в title, кроме explicit verbatim
  user title;
- созданные relation types и direction;
- description, сохраняющий intended strategic/technical split.

Финальный ответ перечисляет созданный scope, duplicate disposition, Release,
status, hierarchy, labels/label gaps, relations и любой unreconciled outcome.
Task Manager read-back доказывает только planning projection, а не
implementation или delivery.
