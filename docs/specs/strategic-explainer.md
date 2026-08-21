# Strategic Explainer

Статус: current contract, 2026-08-21. Problem-first discovery принято в
[ADR-0014](../decisions/0014-problem-first-bounded-strategic-discovery.md).

Продуктовая цель и implementation-independent инварианты зафиксированы в
[стратегическом видении](../strategic-explainer.md). Эта specification задаёт
нормативный input/output и behavioral contract.

Документ описывает общий skill `$strategic-explainer`, который переводит
локальную техническую ситуацию в ясное объяснение на уровне целей,
пользовательского эффекта, ограничений и следующего понятного шага. Skill не
привязан к ShipTask, Task Manager или конкретному типу проекта.

## 1. Результат и граница

Strategic Explainer получает bounded `Strategic Handoff` от основного агента,
проверяет обязательный `Problem to solve`, самостоятельно восстанавливает
релевантный strategic view через read-only tools и возвращает свободное
стратегическое объяснение ситуации. Это обычный содержательный текст с короткой
source note для parent, а не структурированный result object и не готовый
payload для публикации.

Его задача — связать caller-owned проблему, самостоятельно найденный strategic
context и уже установленные current-state facts. `Lossless-by-relevance`
означает: не потерять факты, которые меняют problem framing, outcome,
impact/risk, действие или confidence, но не переносить process diary.

Skill не является reviewer, incident commander или decision maker. Он:

- не выполняет writes, recovery, release или другие mutations;
- не решает, завершена ли работа, существует ли blocker и какое действие
  разрешено;
- не усиливает confidence и не заменяет current execution evidence; найденные
  документы являются contextual evidence, а не доказательством completion;
- не подменяет основной агент при выборе status, authority boundary или
  следующего действия;
- не публикует ответ пользователю самостоятельно, когда вызван как субагент.

Стратегическое объяснение является интерпретацией, а не новым evidence.
Основной агент принимает решения по исходному состоянию и authority, читает
объяснение как смысловую основу и самостоятельно формулирует окончательное
user-facing сообщение.

## 2. Invocation

Skill можно использовать напрямую через catalog entry текущей distribution для
адаптации технического статуса, результата, ограничения, инцидента или запроса
к пользователю. Другой workflow может вызвать его как отдельного субагента,
когда основной context загрязнён implementation details или когда пользователю
иначе пришлось бы расшифровывать внутреннюю терминологию.

Для orchestration обязателен новый субагент без унаследованной истории
разговора. Ему передаётся только contract skill и один самодостаточный
`Strategic Handoff`. В Codex orchestration это означает точный параметр
`fork_turns="none"`; `fork_turns="all"`, положительное число fork turns или
продолжение старого thread не являются свежим контекстом.

До анализа субагент проверяет context integrity. Допустимы system/developer
instructions, runtime skill и единственный текущий handoff от родительского
агента. Если перед ним видны более ранние user/assistant turns, tool transcript
или другая унаследованная история, субагент ничего не анализирует, не вызывает
tools и возвращает только исправляющий отказ:

```text
CONTEXT_INTEGRITY_ERROR: унаследована история родительского разговора.
Перезапустите новый default subagent с fork_turns="none" и передайте только
самодостаточный Strategic Handoff в первом сообщении.
```

System/developer instructions и сам runtime skill загрязнением не считаются.
Если единственный handoff сам содержит скопированный conversation transcript,
raw tool log или необязательный process diary вместо осознанно подготовленного
brief, действует тот же отказ с просьбой сократить input. Повторный brief после
изменения состояния обрабатывает новый субагент, а не использованный thread.

После context-integrity check субагент проверяет problem gate и только затем
может вызывать bounded read-only tools. Direct invocation следует тому же
порядку. Tool calls не должны выполнять mutations или расширять declared scope.

По умолчанию не вызывать отдельного субагента для тривиального результата,
который основной агент может ясно объяснить одной-двумя фразами. Исключение —
calling workflow, который явно требует independent adaptation для durable
user-facing artifact. Изоляция особенно полезна для:

- material failure, partial result или реального blocker;
- запроса user action, decision или новой authority;
- нескольких независимых ограничений, акторов или проверяемых сценариев;
- terminal report, где technical vocabulary скрывает пользовательский смысл.

## 3. Вход: Strategic Handoff

Handoff содержит три логические части.

### 3.1 Problem to solve

Обязательная содержательная задача включает:

- `Beneficiary` — для кого предназначен результат;
- `Desired outcome` — какое наблюдаемое изменение или capability требуется;
- `Exact scope` — какой конкретный target/ref рассматривается;
- `Why now/current gap` — только когда без него нельзя понять выбор scope.

Один identifier, технический заголовок, error code или формулировка «объяснить
этот результат» недостаточны. Проблема принадлежит caller: Explainer не ищет и
не выбирает её самостоятельно.

Если содержательный `Problem to solve` отсутствует, после context-integrity
check и до любого tool call вернуть только:

```text
PROBLEM_CONTEXT_ERROR: не передана содержательная задача, которую мы решаем.
Передайте, для кого предназначен результат, какой наблюдаемый outcome нужен и
какой exact scope/ref рассматривается. Одного identifier или технического
заголовка недостаточно.
```

Не продолжать частичный анализ и не пытаться восстановить проблему из tool
search.

### 3.2 Current-State Brief

Основной агент передаёт только проверенную и decision-relevant информацию:

- `Reader purpose` — что человек должен понять, решить или суметь сделать после
  чтения;
- `Confirmed outcome` — что фактически работает или завершено;
- `Unfinished or unknown` — что не завершено, не проверено или неизвестно;
- `Observed user impact` — уже подтверждённый эффект без strategic speculation;
- `Evidence and confidence` — основания и уровень уверенности без raw logs;
- `Current capability and attempts` — что основной агент уже может или не
  может сделать самостоятельно;
- `Constraints` — scope, authority, environment, privacy и другие реальные
  границы;
- `Candidate user dependency` — только если evidence уже показывает, что для
  продолжения нужен человек, доступ, решение или внешний state;
- `Next-state contract` — actor, минимальное действие, observable success
  signal и что после него может продолжить основной агент;
- `Decision support request` — optional запрос сравнить несколько допустимых
  способов устранить уже установленный gap, не меняя state или authority;
- `Output language and channel` — язык и ограничения поверхности ответа.

Для material или multi-scenario ситуации brief содержит отдельный ledger:

```text
Scenario:
Expected user-visible behavior:
State: VERIFIED | FAILED | UNVERIFIED | NOT_APPLICABLE
Evidence basis:
Observed user impact:
Needed input:
```

`Needed input` не является разрешением просить пользователя. Он заполняется
только подтверждённой dependency и должен называть actor, минимальное действие,
причину и observable success signal. Независимые сценарии имеют отдельные
ledger entries.

Current-State Brief не должен включать желаемую формулировку, готовый strategic
view, полный process diary или несвязанные детали. Caller определяет current
outcome, report/lifecycle state, evidence, authority и допустимый next action;
Explainer не пересматривает их по найденным design documents.

### 3.3 Strategic discovery anchors

Caller передаёт exact starting anchors, которые уже входят в scope: target/ref,
доступный project/repository context и известные direct links. Он не обязан
находить или пересказывать strategic documents за Explainer.

После problem gate Explainer самостоятельно использует доступные read-only
tools и следует от exact scope к ближайшему materially relevant уровню:
parent/initiative, Epic, Project/Release goal, product vision, high-level design,
current specification и accepted decision record.

Discovery contract:

- различать `current/accepted`, `proposed` и `historical` sources;
- не выдавать plan или historical note за shipped/current behavior;
- остановиться, когда понятны beneficiary, desired capability, ключевые
  constraints/non-goals и вклад exact scope;
- не читать broad logs, conversation history, unrelated files или source code
  по умолчанию;
- technical implementation читать только когда она меняет причинную модель,
  risk, action или confidence;
- отсутствие дополнительного strategic source не считать ошибкой;
- material source conflict или недоступный обязательный context вернуть parent
  как точный gap, не маскируя его уверенным user-facing текстом.

Если входные факты противоречивы или не позволяют честно объяснить impact,
Strategic Explainer сообщает основному агенту точный пробел и не возвращает
частичный user-facing текст.

## 4. Выход: свободное стратегическое объяснение

Результат не имеет обязательных полей, headings, envelope или шаблона. Форму и
глубину адаптировать к ситуации. Объяснение должно дать родительскому агенту
ясную модель:

1. какую проблему и для кого решаем;
2. какой strategic intent, design или constraint определяют смысл;
3. какой результат уже получен и как он продвигает цель;
4. что именно осталось неподтверждённым или недоступным;
5. влияет ли это на пользователя сейчас;
6. требуется ли одно конкретное действие и что произойдёт после него.

Если caller передал `Decision support request`, объяснение дополнительно даёт
2–4 реально различающихся варианта. Для каждого кратко назвать prerequisites,
какой gap он закрывает, основной tradeoff и observable success signal; один
вариант можно рекомендовать с причиной. Explainer не придумывает недоступные
capabilities, не меняет установленный state и не превращает варианты в
выполненные действия или новую authority.

Когда skill вызван как субагент, объяснение адресовано родительскому агенту и не
считается copy-ready комментарием. После explanation вернуть короткую source
note: exact strategic sources, их `current/accepted | proposed | historical`
state либо отметку, что дополнительный context не найден. Родитель обязан
проверить meaning и provenance и написать user-facing сообщение своими словами.
При direct invocation skill может сразу отвечать пользователю и размещать source
refs рядом с поддерживаемыми ими утверждениями.

Техническая глубина допустима, когда она помогает понять причинную модель,
impact, confidence или следующий шаг. Не превращать ответ в raw evidence dump,
но и не применять механический лимит длины, число bullets или запрет конкретных
типов identifier: relevance определяется задачей и будущим читателем.

## 5. Правила адаптации

- Начинать с проблемы, strategic meaning текущего outcome и user impact, а не с
  механизма, ошибки или reason code.
- До написания найти одно load-bearing сообщение: минимальный вывод, без
  которого человек неверно поймёт состояние или следующий шаг.
- Применять need-to-know filter: detail остаётся только если меняет понимание
  problem, strategic intent, outcome, impact/risk, required action или confidence.
- Technical details держать на третьем уровне narrative attention. Current
  execution evidence остаётся выше design по factual authority: design не
  переписывает наблюдаемый outcome.
- Заменять внутренние сущности их человеческой ролью. Если точный термин нужен
  для действия или проверяемости, сначала объяснить его обычными словами и
  только затем назвать в скобках.
- Для jargon выбирать одно из трёх: заменить обычными словами, объяснить один
  раз или удалить.
- Явно разделять `работает`, `не работает`, `не проверено` и `не относится к
  текущему результату`. Не превращать отсутствие проверки в defect.
- Отделять `CONFIRMED`, `PROBABLE` и `UNKNOWN`; uncertainty показывать только
  там, где она меняет вывод или следующий шаг.
- Не просить у пользователя внутренний артефакт, account type, environment или
  процедуру без actor, реального проверяемого сценария, причины и observable
  success signal.
- Если нужен другой человек или аккаунт, описать его обычную роль и почему
  текущий агент не может воспроизвести этот сценарий сам.
- Не перечислять tool names, transport paths, raw errors, все checks, Tasks,
  файлы или статусы. Оставлять exact identifier только для полезной навигации.
- Не писать, что пользователь «должен разобраться», «проверить всё вручную» или
  самостоятельно интерпретировать technical evidence.

## 6. Визуализации

Добавлять небольшую таблицу, flow или диаграмму только когда она заметно
упрощает отношения между тремя и более акторами, сценариями, состояниями или
шагами. Визуализация должна отвечать на конкретный пользовательский вопрос и
оставаться понятной без изучения legend или implementation vocabulary.

Не добавлять декоративные картинки и не создавать отдельный media artifact без
явной просьбы основного агента или пользователя. При неизвестных возможностях
renderer использовать plain text или Markdown table. Визуализация не заменяет
краткий outcome-first текст.

## 7. Completion criteria

Strategic Explainer завершил работу, когда:

- context integrity проверен до анализа; загрязнённый subagent invocation
  завершён только `CONTEXT_INTEGRITY_ERROR` с корректной инструкцией перезапуска;
- problem gate пройден до tool calls; отсутствующий problem завершён только
  `PROBLEM_CONTEXT_ERROR` с точным исправлением handoff;
- discovery bounded exact scope, использует только read-only operations,
  различает source state и соблюдает stop condition;
- forward trace пройден: каждое существенное утверждение трассируется к
  `Problem to solve`, `Current-State Brief` или exact discovered source;
- reverse coverage пройден: каждый decision-relevant входной факт сохранён
  либо осознанно исключён как не влияющий на outcome, impact/risk, action или
  confidence;
- outcome, user impact и граница знания различимы;
- подтверждённый user dependency сформулирован одним конкретным действием с
  понятной причиной;
- следующий шаг не содержит решения, которого основной агент ещё не принимал;
- optional `Decision support request` сохранён как 2–4 feasible options с
  prerequisites, tradeoff и success signal без подмены state/authority;
- объяснение можно понять без знания внутренних tools, protocols и source code;
- parent получил короткий проверяемый source basis либо честную отметку, что
  дополнительный strategic context не найден;
- основной агент может использовать ответ как смысловую основу собственного
  сообщения, не как copy-ready payload, evidence или новую authority.

Регрессионные сценарии и pass/fail rubric определены в
[evaluation contract](../reference/strategic-explainer-evaluation.md).
