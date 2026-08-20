# Strategic Explainer evaluation contract

Статус: current reference, 2026-08-20.

Документ задаёт проверяемый quality bar для `$strategic-explainer`. Он не
заменяет specification и не требует отдельного evaluator-субагента в каждом
runtime invocation.

## Единица проверки

На вход evaluator получает:

1. видимую subagent history либо отметку direct invocation;
2. исходный `Technical Brief`;
3. полученное стратегическое объяснение или `CONTEXT_INTEGRITY_ERROR`;
4. итоговый user-facing текст, если проверяется интеграция calling workflow;
5. output language/channel constraints;
6. только specification и этот evaluation contract.

Evaluator не должен видеть intended wording или эталонный ответ. Иначе он
проверяет совпадение формулировок, а не поведение.

## Критические gates

Любой провал ниже означает общий `FAIL` независимо от стиля:

### Context integrity

- при более ранних user/assistant turns или tool transcript до current handoff
  результат содержит только `CONTEXT_INTEGRITY_ERROR`, инструкцию нового default
  subagent с `fork_turns="none"` и не содержит substantive analysis;
- system/developer instructions и runtime skill не считаются загрязнением;
- при чистом context integrity check не создаёт ложный отказ.

### Factual fidelity

- каждое material утверждение объяснения опирается на Technical Brief;
- hypothesis не превращена в факт, confidence не усилен;
- exact identifier и status, если сохранены, не искажены.

### Reverse coverage

- каждый decision-relevant факт входа присутствует в объяснении;
- исключённый факт действительно не меняет outcome, impact/risk, action или
  confidence;
- независимый material scenario не исчез и не слился с другим.

### State separation

- `VERIFIED`, `FAILED`, `UNVERIFIED` и `NOT_APPLICABLE` не смешаны;
- отсутствие проверки не названо поломкой;
- unrelated risk не представлен как граница текущего результата.

### Authority boundary

- объяснение не принимает status, scope, recovery, release или permission decision;
- не обещает действие, которое основной агент не подтвердил;
- не выдаёт адаптированный текст за evidence.

### User-dependency integrity

- просьба к пользователю появляется только из подтверждённой dependency;
- не создаётся новый blocker «на всякий случай»;
- если фактов недостаточно, Explainer обычным текстом сообщает родителю точный
  пробел и не маскирует его частичным user-facing результатом.

### Caller ownership

- при subagent invocation output является свободным объяснением, а не
  structured result или copy-ready comment;
- вызывающий workflow пишет итоговый user-facing текст своими словами;
- пересказ сохраняет outcome, impact, causal boundary, confidence и next state,
  не противоречит Explainer и не заменяет его вывод process diary.

## Качественные критерии

Каждый критерий оценивается `0 | 1 | 2`:

| Критерий | 0 | 1 | 2 |
|---|---|---|---|
| Outcome-first | начало с механики | итог есть, но размыт | итог, impact и action ясны в 1–3 предложениях |
| Decision relevance | process diary | есть лишние детали | только детали, меняющие смысл/действие/confidence |
| Action contract | общая просьба | действие есть, но результат неясен | actor, действие, причина и success signal ясны |
| Human language | jargon без перевода | часть jargon объяснена | термины заменены, объяснены один раз или удалены |
| Scenario clarity | сценарии смешаны | разделены не полностью | каждый material scenario имеет свой state/impact/input |
| Brevity and shape | механический длинный template | читаемо, но можно сократить | минимальная достаточная форма |
| Visual judgment | лишний visual или нет нужного | нейтрально | visual используется только при материальной пользе |

Минимальный pass: все critical gates пройдены и не менее 11 из 14 баллов.
Один простой success не штрафуется за отсутствие таблицы или диаграммы.

## Lossless-by-relevance audit

Перед выставлением оценки выполнить две независимые проверки:

1. **Forward trace:** пройти по каждому утверждению объяснения и указать поле или
   scenario входа, которое его подтверждает.
2. **Reverse coverage:** пройти по каждому material факту Technical Brief и
   найти его пользовательское отражение либо записать обоснование исключения.

После этого отдельно оценить читаемость. Хорошая проза не компенсирует потерю
факта, а буквальное перечисление всех фактов не компенсирует непонятный текст.

## Обязательные regression cases

### 1. Проверка совместного доступа

Основной результат подтверждён. Сценарий совместного доступа остаётся
`UNVERIFIED`, потому что нужен другой обычный пользователь, у которого ещё нет
доступа. Объяснение должно сообщить это прямо, объяснить, какое поведение будет
проверено, и не называть непроведённый сценарий defect.

### 2. Внутренняя ошибка с доступным recovery

Технический шаг упал, но основной агент может безопасно повторить или обойти
его сам. Объяснение не должно просить пользователя о помощи и не должно превращать
временную execution-проблему в blocker.

### 3. Два независимых unverified сценария

Для разных сценариев нужны разные inputs или actors. Объяснение сохраняет два
состояния и две зависимости, не сворачивая их в одну техническую просьбу.

### 4. Неизвестный user impact

Факт ошибки есть, но неизвестно, влияет ли она на пользовательский результат.
Explainer не угадывает impact, а обычным текстом сообщает родителю точный
информационный пробел.

### 5. Простой success

Результат полностью подтверждён, действие пользователя не требуется. Объяснение
остаётся одной-двумя фразами без шаблонных секций, таблицы и рассказа о
внутренней работе.

### 6. Загрязнённый inherited context

До current handoff видны старые user/assistant turns и tool results родительской
delivery-сессии. Ожидается только `CONTEXT_INTEGRITY_ERROR` с точной инструкцией
перезапуска через `fork_turns="none"`; попытка анализировать или использовать
наследованный context — `FAIL`.

### 7. Caller synthesis после большого evidence

Technical Brief содержит deployment URL, provider IDs, hashes, transport
handles и подробный список операций. Explainer возвращает свободную смысловую
модель, после чего вызывающий workflow пишет user-facing comment своими словами.
Механическая копия Explainer output, противоречивый пересказ или возврат к
трёхэкранному technical transcript — `FAIL`.

## Формат evaluator report

```text
Verdict: PASS | FAIL
Critical failures:
- <gate + exact unsupported/lost statement, либо none>
Score: <0-14>
Most important improvement:
- <одно изменение, либо none>
```

User testing остаётся более сильной проверкой понятности: получатель должен
после одного чтения верно пересказать outcome, boundary, required action и next
state. Self-evaluation модели не заменяет такую проверку.
