# Strategic Explainer: требования пользователя

Статус: current Level 1, 2026-08-24.

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
`strategic-explainer/SKILL.md` является компактной смысловой компиляцией обоих
файлов. Если runtime удалить и пересобрать из них, новый skill должен быть
примерно эквивалентен по всем требованиям `SE-*` и выбранной архитектуре.

## Требования

### `SE-01` — Реальная problem framing

Объяснение исходит из установленной проблемы, beneficiary, desired observable
outcome и exact scope. Technical identifier или title не заменяет цель; material
gap называется прямо с объяснением, какой input нужен и почему, а не заполняется
придуманным смыслом. Найденный source может уточнить meaning, но не выбрать цель
за caller или пользователя.

### `SE-02` — Grounded strategic view

Current facts и materially relevant sources образуют основание объяснения.
Current/accepted, proposed и historical context не смешиваются; design не
переписывает наблюдаемый execution outcome. Discovery остаётся bounded declared
scope и заканчивается, когда дополнительный context больше не меняет meaning;
отсутствие необязательного strategic source не создаёт false blocker.

### `SE-03` — Lossless by relevance

Понятность не достигается потерей decision-relevant facts. Сохраняется всё, что
меняет problem, outcome, impact/risk, action или confidence; process diary и
нерелевантные детали можно удалить.

### `SE-04` — Честная граница знания

Работает, не работает, не проверено, неизвестно и не относится — разные
состояния. Hypothesis не становится фактом, отсутствие проверки не называется
defect, а контекстный документ не является completion evidence. Unrelated risk не
выдаётся за границу текущего result, confidence не усиливается гладким текстом.

### `SE-05` — Human language и причинность

Текст начинается со смысла и пользовательского результата или границы знания,
объясняет причинность и следует языку пользователя. Technical detail остаётся
только когда меняет causal model, risk, action, confidence или помогает
проверить результат. Внутренние сущности сначала переводятся в человеческие
роли; точные английские названия сохраняются только когда перевод потеряет
смысл, а не образуют технический гибрид вместо естественного текста.

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
source не сглаживаются уверенной формулировкой.

### `SE-10` — Свобода формы

Direct/delegated invocation, agent topology, context envelope, tool sequence,
retry count, длина и визуальная форма не являются требованиями сами по себе.
Table, flow или diagram используются только когда materially улучшают понимание.
Проверяется независимость meaning, grounding и result, а не конкретный
`fork_turns`, поля handoff или служебные error tokens.

### `SE-11` — Publication-ready и пропорциональный result

Explainer возвращает одну согласованную модель problem, strategic meaning,
current outcome, impact, boundary и next state, понятную без process diary и
дополнительных уточняющих prompt-ов. Простой success остаётся коротким, сложный
failure сохраняет необходимую причинность. Delegated result готов к публикации;
caller проверяет факты, но не переписывает одобренный текст обратно на своём
техническом языке. При factual error или потерянном material fact исправляется
вход и explanation строится заново.

### `SE-12` — Общий переносимый communication skill

Strategic Explainer остаётся generic и пригодным для direct и delegated use вне
ShipTask: он не зашивает Task Manager, tracker lifecycle, project-specific
commands или право управлять calling workflow. В этом repository он
распространяется как sibling `ship-tasks:strategic-explainer` внутри
`ship-tasks@srez-marketplace`, не переносится в Task Manager adapter plugin и не
устанавливается standalone user-level duplicate. Packaging не меняет его
generic runtime boundary; checked-in runtime source, Marketplace source и
installed cache после изменения остаются byte-identical и проверяются в fresh
Codex session.

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

## Изменение Level 1

Новый запрос меняет этот файл только если пользователь меняет обязательный
Strategic Explainer result, invariant или boundary. Просьба улучшить
architecture, упростить процесс, сменить tool или найти лучший способ достижения
сохраняет Level 1 и относится к `architecture.md`.
