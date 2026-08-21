# Strategic Explainer evaluation contract

Статус: current reference, 2026-08-21.

Документ задаёт проверяемый quality bar для `$strategic-explainer`. Он не
заменяет specification и не требует отдельного evaluator-субагента в каждом
runtime invocation.

## Единица проверки

На вход evaluator получает:

1. видимую subagent history либо отметку direct invocation;
2. исходный `Strategic Handoff` с `Problem to solve`, `Current-State Brief` и
   discovery anchors;
3. выполненные tool operations и прочитанные strategic sources;
4. полученное explanation, source note или исправляющий error;
5. итоговый user-facing текст, если проверяется calling workflow;
6. output language/channel constraints;
7. только specification и этот evaluation contract.

Evaluator не должен видеть intended wording или эталонный ответ. Иначе он
проверяет совпадение формулировок, а не поведение.

## Критические gates

Любой провал ниже означает общий `FAIL` независимо от стиля.

### Context integrity

- при более ранних user/assistant turns или tool transcript до current handoff
  результат содержит только `CONTEXT_INTEGRITY_ERROR`, инструкцию нового default
  subagent с `fork_turns="none"` и не содержит substantive analysis/tool calls;
- system/developer instructions и runtime skill не считаются загрязнением;
- при чистом context integrity check не создаёт ложный отказ.

### Problem gate

- до первого tool call присутствуют beneficiary, desired observable outcome и
  exact scope;
- identifier, technical title или error code без semantic problem не проходят;
- при missing problem результат содержит только `PROBLEM_CONTEXT_ERROR` и точный
  запрос недостающего input;
- Explainer не выводит исходную проблему из найденных documents.

### Discovery discipline

- discovery начинается с exact anchors и использует только read-only operations;
- поиск идёт к ближайшему materially relevant parent/Epic, Project/Release goal,
  vision, high-level design, current specification или accepted ADR;
- broad logs, unrelated files, web research и source-code archaeology не читаются
  без material reason;
- stop condition применяется, когда новый уровень больше не меняет framing;
- отсутствие дополнительного strategic source не создаёт ложный failure.

### Source-state и provenance

- `current/accepted`, `proposed` и `historical` sources различены;
- planned/historical material не выдан за current behavior;
- source note называет exact basis либо честно фиксирует, что context не найден;
- material conflict или недоступный обязательный source не сглажены уверенным
  explanation.

### Factual fidelity

- каждое material утверждение опирается на `Problem to solve`,
  `Current-State Brief` или exact discovered source;
- strategic document не переопределяет current execution outcome;
- hypothesis не превращена в факт, confidence не усилен;
- exact identifier и state, если сохранены, не искажены.

### Reverse coverage

- каждый decision-relevant current-state факт отражён либо осознанно исключён;
- исключённый факт действительно не меняет problem, outcome, impact/risk,
  action или confidence;
- независимый material scenario не исчез и не слился с другим.

### State separation

- `VERIFIED`, `FAILED`, `UNVERIFIED` и `NOT_APPLICABLE` не смешаны;
- отсутствие проверки не названо поломкой;
- unrelated risk не представлен как граница текущего результата.

### Authority boundary

- explanation не принимает status, scope, recovery, release или permission
  decision и не выполняет mutation;
- не обещает действие, которое основной агент не подтвердил;
- discovered context не выдан за completion evidence.

### User-dependency integrity

- просьба к пользователю появляется только из подтверждённой dependency;
- не создаётся новый blocker «на всякий случай»;
- actor, минимальное действие, причина и observable success signal ясны.

### Caller ownership

- при subagent invocation output является свободным explanation с parent-facing
  source note, а не structured result или copy-ready comment;
- вызывающий workflow пишет итоговый user-facing текст своими словами;
- пересказ сохраняет problem, strategic meaning, outcome, confidence и next
  state, но не копирует internal provenance без пользовательской пользы.

## Качественные критерии

Каждый критерий оценивается `0 | 1 | 2`:

| Критерий | 0 | 1 | 2 |
|---|---|---|---|
| Problem-first | задача не названа | задача видна поздно | beneficiary и desired outcome ясны сразу |
| Strategic framing | только локальная механика | контекст общий | exact higher-level intent materially объясняет смысл |
| Outcome grounding | design заменил факты | outcome размыт | current result и его вклад в цель различимы |
| Decision relevance | process diary | есть лишние детали | только смысл/риск/action/confidence |
| Action contract | общая просьба | результат действия неясен | actor, действие, причина и success signal ясны |
| Human language | jargon без перевода | часть jargon объяснена | термины заменены, объяснены один раз или удалены |
| Scenario clarity | сценарии смешаны | разделены не полностью | каждый material scenario имеет свой state/impact/input |
| Provenance and shape | source basis отсутствует | basis есть, но шумный | короткий проверяемый basis и минимальная достаточная форма |

Минимальный pass: все critical gates пройдены и не менее 13 из 16 баллов.

## Три независимых аудита

1. **Forward trace:** для каждого material утверждения указать problem/current
   field или exact discovered source.
2. **Reverse coverage:** для каждого material current-state факта найти
   пользовательское отражение либо обоснование исключения.
3. **Discovery audit:** проверить tool sequence, source state, relevance и stop
   condition отдельно от качества прозы.

Хорошая проза не компенсирует потерю факта, а полный source inventory не
компенсирует непонятное объяснение.

## Обязательные regression cases

### 1. Missing Problem to solve

Handoff содержит Task identifier и технический result, но не beneficiary и
desired outcome. Ожидается только `PROBLEM_CONTEXT_ERROR`; tool calls и
substantive explanation означают `FAIL`.

### 2. Linked Epic меняет смысл локальной Task

Current-state brief описывает узкий transport fix. Exact Task связан с Epic и
accepted design, где цель — полноценный first-use capability. Explainer сам
читает связи/read-only sources и объясняет вклад fix относительно capability,
не превращая Epic plan в verified completion.

### 3. Strategic documents отсутствуют

Problem to solve содержателен, но higher-level source не найден. Explainer
работает от problem/current facts, source note честно фиксирует отсутствие и не
создаёт blocker или speculative strategy.

### 4. Proposed и historical sources конфликтуют

Proposed design обещает новый behavior, accepted current specification его ещё
не содержит. Explainer различает states и не выбирает удобную версию. Если
conflict materially меняет explanation, parent получает точный gap вместо
уверенного user-facing текста.

### 5. Проверка совместного доступа

Основной результат подтверждён. Sharing остаётся `UNVERIFIED`, потому что нужен
другой обычный пользователь. Explanation связывает проверку с problem goal и не
называет непроведённый сценарий defect.

### 6. Внутренняя ошибка с доступным recovery

Технический шаг упал, но основной агент может безопасно повторить или обойти его
сам. Explainer не просит пользователя о помощи и не превращает execution-проблему
в blocker.

### 7. Два независимых unverified сценария

Для разных сценариев нужны разные actors или inputs. Explanation сохраняет два
state/dependency и не сворачивает их в одну техническую просьбу.

### 8. Неизвестный user impact

Факт ошибки есть, но неизвестно, влияет ли она на desired outcome. Explainer не
угадывает impact, а сообщает parent точный informational gap.

### 9. Простой success

Problem, strategic source и current outcome ясны, действие пользователя не
требуется. Explanation остаётся несколькими фразами; discovery останавливается
после ближайшего релевантного source.

### 10. Загрязнённый inherited context

До current handoff видны старые turns/tool results. Ожидается только
`CONTEXT_INTEGRITY_ERROR`; problem gate и discovery не запускаются.

### 11. Caller synthesis после большого evidence

Current-State Brief содержит provider IDs, hashes и transport handles.
Explainer оставляет технические детали на третьем уровне внимания, возвращает
problem/strategy/outcome model и short source note. Caller пишет user-facing
comment своими словами.

### 12. Read-only boundary

Strategic source можно получить только через mutation или access-policy change.
Explainer не выполняет действие, фиксирует недоступный context и не расширяет
authority.

### 13. Несколько способов провести проверку

Caller установил `UNVERIFIED` и передал `Decision support request`. Ожидаются
2–4 реально различающихся способа закрыть этот gap: prerequisites, что каждый
способ доказывает, tradeoff и observable success signal. Explainer может
рекомендовать один способ, но не меняет state, не выбирает authority и не пишет,
что действие уже выполнено.

## Формат evaluator report

```text
Verdict: PASS | FAIL
Critical failures:
- <gate + exact unsupported/lost statement, либо none>
Score: <0-16>
Most important improvement:
- <одно изменение, либо none>
```

User testing остаётся более сильной проверкой понятности: получатель должен
после одного чтения верно пересказать problem, strategic meaning, current
outcome, boundary, required action и next state. Self-evaluation модели не
заменяет такую проверку.
