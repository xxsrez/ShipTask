# Strategic Explainer evaluation contract

Статус: current reference, 2026-08-22.

Документ проверяет observable quality `$strategic-explainer`. Он не оценивает
agent topology, fork mode, prompt envelope, internal headings, tool sequence,
retry count, число alternatives или совпадение с эталонной формулировкой.

## Единица проверки

Evaluator получает реальную problem framing, доступные current facts и sources,
выполненные read/write effects, explanation и итоговый user-facing text, если
его создаёт calling workflow. Intended wording и внутренний reasoning не
передаются.

Достаточно фактов, позволяющих проверить claims и authority boundary. Context
может иметь любую форму: evaluation не требует специального handoff protocol.

## Критические требования

Любой провал ниже означает `FAIL`.

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
- discovery, если он нужен, bounded declared scope и materially relevant;
- отсутствие дополнительного source не создаёт false blocker;
- material conflict или missing mandatory source не сглажен уверенным текстом;
- source basis достаточно точен для проверки claims.

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

- problem, strategic meaning, current outcome, impact, boundary и next state
  понятны без внутренних tools и process diary;
- technical terms объяснены или удалены, если не нужны для действия;
- внутренняя orchestration не выдаётся за пользовательский результат.

## Review questions

- Может ли читатель верно пересказать решаемую проблему и current result?
- Можно ли проследить material claims до facts/sources?
- Не потерян ли факт, который изменил бы решение, risk или action?
- Различимы ли failure, unknown и not-applicable?
- Не возникла ли новая authority или просьба без evidence?
- Помог ли strategic context понять meaning, а не заменить current facts?
- Требуется ли ещё один prompt, чтобы понять, что случилось и что делать?

Evaluation report сообщает `PASS | FAIL`, exact unsupported/lost claim и одно
наиболее важное улучшение. Числовая score и фиксированная форма не обязательны.

## Обязательные regression cases

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

### Шумный context

Input содержит избыточные logs и implementation details. Explanation сохраняет
material facts, отбрасывает process diary и не требует конкретного механизма
context isolation.

### Read-only boundary

Relevant source доступен только через mutation или access-policy change.
Explainer не выполняет действие и честно сохраняет context gap.

### Реальный выбор способа проверки

Доступно несколько materially разных способов закрыть `UNVERIFIED` gap.
Explanation сравнивает только feasible alternatives по prerequisites,
доказательной силе, tradeoff и success signal; их количество определяется
ситуацией.

Blind forward test сильнее self-review: агент получает realistic problem и raw
facts без diagnosis прошлого run или intended answer. Проверяется outcome,
grounding, понятность и boundaries, а не внутренний путь к результату.
