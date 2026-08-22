# Strategic Explainer

Статус: current Level 2 contract, 2026-08-22. Применимые Level 1 requirements —
`SE-*` в локальных
[требованиях пользователя](requirements.md). Эта architecture описывает
current архитектуру достижения и не может ослаблять Level 1. Problem-first
bounded discovery принято в
[ADR-0014](../../decisions/0014-problem-first-bounded-strategic-discovery.md), а
implementation-specific orchestration заменена
[ADR-0021](../../decisions/0021-requirements-as-agent-constitution.md).

Продуктовая архитектура раскрыта в
[стратегическом видении](product-vision.md). Эта architecture описывает
наблюдаемый результат и границы общего skill `$strategic-explainer`; она не
задаёт внутреннюю архитектуру агента.

## 0. Compilation contract

Эта architecture вместе с локальным `requirements.md` является полным current
source package `$strategic-explainer`. Runtime `strategic-explainer/SKILL.md` —
производная смысловая компиляция этих двух документов: его можно удалить и
собрать заново, сохранив все `SE-*` и выбранную здесь реализацию примерно
эквивалентными по наблюдаемому поведению. `product-vision.md`, ADR, reports и
evaluations дают локальный design/rationale и evidence, но не становятся
параллельным current contract.

## 1. Конституционный принцип

Requirements определяют проблему, качество объяснения, source grounding,
read-only boundary и отсутствие новой authority. Они не предписывают direct или
delegated invocation, тип или число агентов, fork mode, форму handoff, названия
полей, error tokens, tool sequence, retry count, длину ответа или квоту
alternatives.

Caller или сам агент выбирает организацию работы. Структуры и examples полезны,
только если помогают передать смысл; они не являются protocol. Проверяется
итоговое объяснение, использованные основания и соблюдение границ.

## 2. Результат и граница роли

Strategic Explainer превращает локальную техническую ситуацию в problem-first
объяснение на уровне цели, пользовательского эффекта, ограничений, границы
знания и следующего понятного state. Объяснение должно быть понятным без знания
внутренних tools, transport layers, source code и agent lifecycle.

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

## 3. Достаточный вход

До уверенного объяснения должны быть установлены три смысловых основания:

- реальная проблема: beneficiary, desired observable outcome и exact scope;
- current facts: что доказано, failed, unverified или not applicable, какое
  evidence и confidence это поддерживает, каков фактический impact и authority;
- доступные anchors: exact target и ближайшие relevant product, design,
  specification или decision sources, если они нужны для понимания смысла.

Эти основания могут находиться в prompt, current conversation, task context,
документах или быть безопасно найдены read-only способом. Exact envelope не
требуется. Identifier или технический заголовок сами по себе не определяют
проблему.

Если material основания не хватает, skill ясно называет, какой факт нужен и
почему без него нельзя честно объяснить результат. Он не угадывает цель,
пользовательский impact или permission и не скрывает противоречие гладким
текстом.

Для нескольких независимых сценариев сохраняются их отдельные state, evidence,
impact и dependencies. Форма такого представления выбирается по ситуации.

## 4. Bounded strategic discovery

Когда ближайший strategic context materially меняет смысл, Explainer может
использовать доступные read-only sources. Поиск ограничен declared scope и
заканчивается, когда понятны beneficiary, desired capability, ключевые
constraints/non-goals и вклад current result.

- `current/accepted`, `proposed` и `historical` sources различаются;
- live execution evidence определяет current outcome, а design объясняет его
  значение;
- отсутствие дополнительного source не создаёт выдуманный blocker;
- material conflict или недоступное обязательное основание явно остаётся gap;
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

При direct invocation source refs размещаются рядом с поддерживаемыми claims.
При delegated use Explainer возвращает готовый пользовательский текст и
достаточно короткий source basis, чтобы parent проверил смысл, факты и
provenance. Никакой фиксированный output envelope не нужен.

## 6. Completion criteria

Работа завершена, когда:

- проблема и desired outcome не выдуманы;
- каждое material утверждение опирается на current facts или exact source;
- каждый decision-relevant факт сохранён либо исключён только как не влияющий
  на problem, outcome, impact/risk, action или confidence;
- fact, interpretation, failure, unknown и not-applicable различимы;
- discovery, если он был, остался bounded и read-only;
- explanation не создаёт status, permission или action, которого источник не
  устанавливал;
- пользователь понимает смысл и следующий state без process diary;
- delegated result пригоден для публикации без стилистической переработки
  основным агентом;
- source basis и material uncertainty остаются проверяемыми.

Regression scenarios проверяются по observable behavior в
[evaluation contract](../../reference/strategic-explainer-evaluation.md).
