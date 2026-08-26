# 0014. Problem-first и bounded strategic discovery

Статус: partially superseded, 2026-08-26. Problem-first, bounded read-only
discovery, source-state и no-authority boundaries сохраняются; fixed problem
fields/error token остаются historical, а current fresh context и compact
invocation определены
[ADR-0029](0029-fresh-strategic-explainer-and-blocker-reflection.md). Расширяет
[ADR-0012](0012-strategic-explainer-as-portable-subagent-role.md) и
[ADR-0013](0013-strategic-explainer-for-shiptask-report-narratives.md). Заменяет
их no-tools часть; исторически сохраняло fresh context, read-only/no-authority границу и
ответственность основного агента за финальный текст, решения и mutations.
Свобода внутреннего workflow из
[ADR-0021](0021-requirements-as-agent-constitution.md) действует вне явного
clean invocation invariant ADR-0029.

## Контекст

Первоначальный Strategic Explainer получал самодостаточный `Technical Brief` и
не собирал дополнительный context. Это защищало свежий субагент от process
diary и tactical framing, но одновременно делало стратегический уровень
полностью зависимым от того, что основной агент уже поместил во вход.

Такой Explainer хорошо переводит технический outcome на человеческий язык, но
не гарантирует понимания задачи, ради которой выполнялась работа. Parent Task,
Epic, Project/Release goal, product vision, high-level design, accepted
specification или ADR могут materially менять смысл локального результата, хотя
не входят в execution brief. Простое увеличение brief возвращает tactical
framing и заставляет вызывающего агента заранее выполнять стратегическую работу
за Explainer.

Нужна асимметрия ответственности: проблему явно задаёт caller, а релевантный
strategic view Explainer восстанавливает самостоятельно через bounded read-only
discovery.

## Решение

### Обязательный problem gate

- Каждый invocation получает содержательный `Problem to solve`: для кого
  предназначен результат, какой наблюдаемый outcome или capability требуется и
  какой exact scope рассматривается. Один identifier или технический заголовок
  недостаточен.
- Проблема принадлежит caller и не выводится Explainer из найденных документов.
  Discovery может уточнить её контекст или обнаружить противоречие, но не выбрать
  другую проблему.
- После context-integrity check и до любого tool call Explainer проверяет
  `Problem to solve`. При отсутствии содержательной задачи он возвращает только
  `PROBLEM_CONTEXT_ERROR` с точным перечнем недостающего входа.

### Разделённый handoff

Вместо технически центрированного brief caller передаёт bounded `Strategic
Handoff` из трёх частей:

1. обязательный `Problem to solve`;
2. authoritative `Current-State Brief` с уже установленными outcome, state,
   evidence/confidence, constraints, known/unknown scenarios, разрешённым next
   action и dependency;
3. `Strategic discovery anchors`: exact scope/ref, доступный project/repository
   context и ссылки, с которых можно начать read-only поиск.

Caller не передаёт готовый strategic view или желаемый вывод. Explainer не
использует discovery, чтобы заново определять execution outcome, lifecycle state
или authority.

### Bounded strategic discovery

- После problem gate Explainer самостоятельно использует доступные read-only
  tools. Writes, recovery, release, status/Goal decisions и external actions
  запрещены.
- Поиск начинается с exact scope и его связей и идёт к ближайшему materially
  relevant уровню: parent/initiative, Epic, Project/Release goal, product vision,
  high-level design, current specification и accepted decision record.
- Explainer различает `current/accepted`, `proposed` и `historical` источники.
  План или старый документ не выдаётся за текущее состояние.
- Поиск прекращается, когда понятны beneficiary, desired capability, ключевые
  strategic constraints/non-goals и вклад exact scope. Более высокий документ
  не читается, если он уже не меняет интерпретацию.
- Broad logs, execution history, unrelated files и source-code archaeology не
  входят в default discovery. Technical implementation читается только когда
  без неё нельзя понять причинную модель, риск, confidence или следующий шаг.
- Отсутствие дополнительного strategic source не является ошибкой: Explainer
  работает от явно переданной проблемы и честно сообщает parent, что более
  высокий контекст не найден. Material conflict или недоступный обязательный
  source не сглаживается уверенным текстом.

### Два порядка приоритета

Narrative/attention order:

1. какую проблему решаем;
2. какой strategic view и constraint определяют смысл;
3. что current outcome означает относительно цели;
4. technical details только по need-to-know.

Evidence authority order отличается: current execution evidence определяет, что
фактически работает; accepted strategic sources объясняют зачем и в каких
границах это важно; proposed и historical material остаются контекстом. Design
не может переопределить наблюдаемый outcome.

### Provenance и caller ownership

- Каждое strategic утверждение трассируется к exact source. При subagent
  invocation Explainer возвращает свободное объяснение и короткую source note
  для parent: какие источники были использованы и в каком они состоянии.
- Source note не является copy-ready user payload. ShipTask или другой caller
  формулирует финальный текст своими словами и оставляет identifiers только
  когда они помогают навигации или проверке.
- Explainer остаётся manager-style specialist без authority. Он не выбирает
  status, blocker, recovery, permission, release или terminal transition и не
  выполняет mutations.

## Последствия

Положительные:

- explanation начинается с реальной задачи, а не с последнего технического
  события;
- tactical framing вызывающего агента не является единственной стратегической
  оптикой;
- Epic/design/vision используются тогда, когда materially меняют смысл, но не
  превращаются в новый источник execution truth;
- provenance позволяет parent проверить найденный стратегический контекст.

Ограничения:

- invocation требует содержательного problem statement; неполный handoff теперь
  fail-closed до tool calls;
- read-only discovery увеличивает latency и может зависеть от доступности
  project/tracker tooling;
- broad search способен снова загрязнить context, поэтому anchors, source-state
  classification и stop condition являются обязательными;
- существующие regression cases должны отдельно проверять problem gate,
  discovery discipline, source conflict и отсутствие strategic documents.
