# Scope Reviewer: архитектура

Статус: current agent-owned Architecture, 2026-09-02. Независимые user-owned
источники находятся в локальных [Overview](overview.md) и
[Requirements](requirements.md). Эта Architecture описывает current способ
достижения цели и не может ослаблять, расширять или переопределять их.

Runtime Scope Reviewer скомпилирован в `scope-reviewer/`, а observable contract
находится в [Evaluation](evaluation.md). Installed capability доказывается
отдельно от наличия repository source.

## 0. Compilation contract

Локальные `overview.md`, `requirements.md` и `architecture.md` являются тремя
самостоятельными source-входами Scope Reviewer. Current runtime package должен
быть их компактной смысловой компиляцией и сохранять:

- общий смысл и адресата из Overview;
- все `SR-*` без скрытого ослабления;
- выбранные здесь интерфейсы, integrity guards и orchestration decisions;
- трассу от каждого требования до observable scenario.

Если runtime удалить, из этих трёх входов должно восстанавливаться примерно
эквивалентное наблюдаемое поведение без скрытой policy из implementation или
истории.

Рабочее runtime-имя — `$issue-grinder:scope-reviewer`. Skill логически является
Task Manager-only sibling Task Composer и Issue Grinder и может распространяться
вместе с ними внутри `issue-grinder@srez-marketplace`. Strategic Explainer
остаётся отдельной plugin dependency и не копируется в этот package.

## 1. Роль и границы

Scope Reviewer владеет одним связным циклом:

```text
live scope → multi-lens review → optional plan repair → repeat review →
human-readable plan/release report
```

Он работает в трёх intent-классах:

1. **Plan review** — read-only анализ и понятный отчёт.
2. **Plan improvement** — тот же анализ, автоматическое изменение agent-owned
   planning model и повторная проверка; требует явного mutation intent.
3. **Release review** — всегда read-only обзор текущего delivery scope.

Запрос «покажи план», «объясни, что будем делать», «проверь план», «дай отчёт по
Release» или «что сейчас происходит» сам по себе не разрешает write. Intent
«улучши», «почини», «подготовь план к исполнению» или эквивалентная однозначная
команда включает Plan improvement только для выбранного planning scope.

Task Composer остаётся владельцем исходной постановки, decomposition и записи
согласованных человеком Requirements. Issue Grinder остаётся владельцем
implementation, evidence, Goal и lifecycle. Scope Reviewer не подменяет ни один
из этих workflows.

## 2. Логическая модель planning source

Reviewer различает два независимых слоя:

- **Human Requirements** — user-owned problem, desired outcome, требования,
  ограничения и non-goals;
- **Agent Plan** — agent-owned decomposition, Task scopes, acceptance,
  expected evidence, hierarchy, relations, sequencing и technical detail.

Предпочтительная Task Manager representation предоставляет слоям отдельные
поля, версии и write operations. Каждая Task хранит применимые Requirement IDs
либо другую стабильную связь с каноническим источником, а Agent Plan указывает,
относительно какой Requirements version он построен.

До появления такого adapter contract допустима структурированная representation
в current Task fields только при строгом preservation guard. Reviewer должен
уметь извлечь Human Requirements, сохранить их byte-identical при planning
update и после read-back доказать, что изменён только разрешённый слой. Если
границу нельзя однозначно распознать или сохранить, автоматический repair этой
Task запрещён; проблема возвращается как representation blocker, а не обходится
перезаписью общего description.

Requirement projection в child Task не становится новым source смысла. Она
помогает исполнителю понять применимую часть общей цели, но сверяется с
каноническими Requirements и не разрешает локально изменить их.

## 3. Live scope и согласованный snapshot

До анализа основной agent через Task Manager adapter разрешает exact workspace,
Project и выбранный Project/Release/Epic/Task selector. Relative selector
допустим только когда current context делает его однозначным; максимальный номер,
последняя дата или похожее название не выбирают current Release автоматически.

Для полного scope agent:

1. проходит все страницы inventory до terminal pagination;
2. читает full detail каждой materially relevant Task;
3. разрешает parent/child hierarchy, relations, statuses, Requirements и Agent
   Plan;
4. читает применимые comments и внешние evidence anchors только когда они нужны
   для заявленного состояния;
5. сохраняет snapshot manifest из canonical refs, versions и source anchors.

Lenses анализируют один логический snapshot. До planning writes и до итогового
report coordinator перечитывает version vector. Изменившиеся элементы
инвалидируют только зависимые выводы, но material graph/Requirements change
требует нового согласованного snapshot. Нельзя незаметно соединить старый анализ
с новым состоянием.

## 4. Выбор оптик

Coordinator выводит оптики из problem, состава scope, Requirements, task graph,
execution state и известных рисков. Он не применяет универсальный фиксированный
набор, но для plan review проверяет необходимость как минимум следующих классов:

- Requirements integrity и согласованность;
- полнота outcome/decomposition и ownership;
- dependencies, sequencing и critical path;
- acceptance, evidence и наблюдаемая готовность;
- risk, authority, review и human-attention boundaries.

По содержанию добавляются domain/product, UX, data/migration, compatibility,
security/privacy, reliability, performance/cost, integration/release или другие
материальные оптики. Два разных названия не оправдывают два subagents, если они
проверят одно и то же решение.

Оптика допускается в wave, если её вывод потенциально способен изменить хотя бы
одно из следующего:

- понимание problem или desired outcome;
- planning repair либо task graph;
- Requirement question;
- acceptance/evidence strategy;
- material risk, dependency или blocker;
- human action/review;
- readiness или confidence.

## 5. Независимые Luna Max reviewers

Каждая выбранная оптика исполняется отдельным built-in `default` subagent через
top-level collaboration surface с:

- `fork_turns="none"`;
- `model="gpt-5.6-luna"`;
- `reasoning_effort="max"`;
- одной compact optic task;
- exact scope/snapshot identity и resolvable read-only anchors;
- явным запретом mutations, orchestration и delegation.

Luna не получает caller reasoning, готовый общий вывод, ответы соседних lenses
или полный process transcript. Это сохраняет независимость оптик и не позволяет
первой интерпретации заранее задать результат остальным.

Каждый lens result содержит не отчёт о процессе, а bounded finding packet:

- краткий человеческий вывод через свою оптику;
- material facts и resolvable evidence anchors;
- влияние на outcome или readiness;
- disposition: `auto-fixable`, `human-requirement-decision`, `risk/observe` либо
  `no-material-finding`;
- предлагаемый repair или вопрос, если он обоснован;
- uncertainty и confidence boundary.

Lens не пишет Tasks, не меняет Requirements, не решает lifecycle и не вызывает
Strategic Explainer. Ошибка или недоступность одной оптики не превращает её
молчание в PASS; coordinator сообщает coverage gap и решает, можно ли честно
завершить review без этой perspective.

## 6. Синтез и disposition findings

Coordinator проверяет каждое material утверждение по snapshot sources. Report
subagent-а является analysis input, но не evidence сам по себе.

Findings проходят disposition:

- `no-material-finding` не попадает в итоговую композицию;
- дубли объединяются с сохранением сильнейшего evidence и существенных
  различий;
- factual conflict возвращается к primary sources;
- genuine disagreement между оптиками остаётся видимым и не разрешается
  редакторским голосованием;
- Requirement issue никогда не переклассифицируется в auto-fix только ради
  продолжения;
- optional improvement не выдаётся за blocker или обязательную работу.

Coordinator строит coverage map `Requirement → Task/plan element → acceptance →
expected evidence` и выявляет скрытый остаток, дублирование ownership и
требование без observable proof. Эта карта является внутренним основанием
readiness, а не обязательной формой пользовательского отчёта.

## 7. Автоматический plan repair

Plan repair выполняется только в Plan improvement. До первой mutation
coordinator подтверждает:

- exact scope и write authority;
- неизменившийся Requirements version и snapshot;
- однозначную границу Human Requirements/Agent Plan;
- что изменяемая Task ещё принадлежит planning surface и её repair не подменяет
  активную delivery/rework;
- что proposed patch не расширяет пользовательский scope.

Auto-fix может уточнить task wording и technical boundary, acceptance, expected
evidence, labels, hierarchy, relations и sequencing, а также перестроить
agent-owned decomposition, если current Task Manager capabilities позволяют
сделать это без destructive deletion и скрытой потери history. Устаревший
элемент предпочтительно supersede/cancel по отдельно разрешённой planning
семантике, а не удалять физически. Если нужная lifecycle operation не входит в
authority или adapter contract, repair остаётся proposed и не имитируется
текстовой пометкой.

Каждый write использует current canonical ref/version, optimistic concurrency и
post-write read-back. Unknown outcome сначала reconciles через reads; blind retry
запрещён. Partial repair перечисляет confirmed, unknown и not-applied changes и
не объявляет план готовым.

Human Requirements до и после repair сравниваются отдельным integrity gate.
Любое неразрешённое отличие отменяет дальнейшие writes и классифицируется как
requirements-integrity failure.

## 8. Requirements discussion loop

Requirements lens формулирует material problem обычным языком и показывает:

- где именно находится противоречие, пробел или выбор;
- как он влияет на outcome, decomposition, acceptance или риск;
- какие варианты действительно следуют из sources и чем отличаются;
- какое минимальное решение требуется от человека.

Scope Reviewer не записывает выбранный вариант в Human Requirements. После
явного решения пользователя owning planning workflow обновляет Requirements и
их version. Reviewer начинает новую итерацию с live reread, обновляет либо
ремонтирует Agent Plan и заново проверяет coverage. Старый зелёный вывод не
переносится через Requirements change.

## 9. Итерация и readiness

После repair coordinator создаёт новый snapshot и повторно запускает затронутые
оптики. Полный task graph либо Requirements change требует полного materially
applicable review; узкая текстовая правка может повторить только зависимые lenses
и общие integrity gates.

Итерация останавливается, когда:

- план готов по критериям ниже;
- остались только Requirement decisions человека;
- безопасный repair невозможен из-за authority/capability/conflict;
- новый проход не приносит нового evidence или materially different action.

Повтор той же генерации без changed source, repair или конкретного quality gap не
является прогрессом.

Ready означает одновременно:

- Human Requirements однозначны для текущего scope либо явно согласованы с
  известными boundaries;
- coverage map не содержит скрытого обязательного остатка;
- Task decomposition, ownership и dependencies внутренне согласованы;
- acceptance и expected evidence позволяют наблюдать каждый обязательный
  outcome;
- material auto-fix findings устранены и подтверждены read-back;
- незакрытые риски, review points и действия человека названы и не выданы за
  уже выполненные;
- final snapshot остаётся current.

Readiness не переводит Tasks из `Backlog`, не запускает Issue Grinder и не
является evidence реализации.

## 10. Human-readable report

Coordinator сначала создаёт factual synthesis из accepted findings и current
snapshot. Он включает только material content: problem, current/future state,
целостную модель работы, repairs, Requirements questions, risks/dependencies,
review/human attention и readiness. Lens transcripts и process diary в draft не
копируются.

Затем coordinator передаёт этот factual target text отдельному
`$strategic-explainer:strategic-explainer` как explicit editing task с exact
scope, языком и resolvable anchors. Strategic Explainer отвечает только за
publication-ready редакторскую реконструкцию и не получает право менять
findings, planning decisions или Task Manager state.

Coordinator проверяет ready text на material factual conflict и reverse
coverage. Он не переписывает результат ради вкуса. Потерянный факт или ошибка
исправляются новым clean editing invocation с корректным target/source. Если
Strategic Explainer недоступен, Scope Reviewer возвращает собственный factual
report и явно отмечает отсутствие независимого editorial pass, не заявляя
эквивалентное качество.

Publication — один целостный ответ. Возможные смысловые вопросы `SR-10` и
`SR-11` не становятся обязательными заголовками; главный вывод и требуемое
действие должны быть видны раньше поддерживающих деталей.

## 11. Release review

Release review всегда read-only. Coordinator строит current snapshot из Task
Manager и доступных primary evidence. Если review вызывается внутри активного
Issue Grinder run, тот может предоставить factual run snapshot и resolvable
anchors на current candidate/checks; неподтверждённый worker narrative остаётся
in-flight state, а не completion evidence.

Отчёт разделяет:

- фактически доказанный product/release outcome;
- current Task Manager lifecycle projection;
- известную незавершённую или in-flight работу;
- critical path и следующий observable state;
- current blockers и лишь возможные будущие risks;
- действие человека, необходимое сейчас, будущую review point и отсутствие
  human dependency.

Task count и status percentage могут быть supporting context, но не заменяют
оценку относительно общей цели Release. Scope Reviewer не публикует Task
comments, не меняет status/Goal и не запускает repair delivery scope.

## 12. Observable evaluation

Runtime получает отдельный evaluation contract с тремя слоями:

1. **Static trace:** каждый `SR-*` связан с runtime surface и observable case.
2. **Deterministic integrity:** exact Luna profile receipts, отсутствие writes в
   Plan review/Release review, stable snapshot/version gates, byte-preservation
   Requirements, optimistic write/read-back и partial-result truthfulness.
3. **Blind model-forward cases:** реальный Task Manager-like scope без intended
   lens set или expected report.

Минимальный model-forward corpus включает:

- тяжёлый многозадачный план с дублированием, missing acceptance и скрытой
  dependency, который автоматически исправляется без изменения Requirements;
- противоречивые Requirements, которые дают понятный human decision и ноль
  requirements writes;
- concurrent version change во время optics wave, который инвалидирует stale
  findings;
- несколько overlapping lenses, из которых итог сохраняет только material
  unique findings и настоящее disagreement;
- Release с mixed statuses, in-flight work и неподтверждённым completion, где
  отчёт не строит ложный progress;
- current safe path, при котором возможная human dependency не называется
  blocker-ом;
- dense technical lens outputs, превращённые в понятный scope-level report без
  потери Requirements, риска и next action.

Статический validator не доказывает качество оптик или понятность generated
report. Эти свойства подтверждаются только blind model-forward результатом и
проверкой человеком, знакомым с исходным вопросом, но не с внутренним process
trace.
