# Evaluation contract Strategic Explainer Fast

Статус: current, 2026-08-27.

Этот contract проверяет observable requirements
[`SEF-*`](../skills/strategic-explainer-fast/requirements.md). Fast использует тот
же сложный 20-case portfolio, что и обычный Strategic Explainer, чтобы варианты
можно было сравнивать по одинаковому смысловому материалу.

## Corpus

Canonical raw facts, case rubrics и common gate остаются в
[`tests/strategic-explainer/`](../../tests/strategic-explainer/). Fast-specific
protocol находится в
[`tests/strategic-explainer-fast/README.md`](../../tests/strategic-explainer-fast/README.md).
Fixtures не копируются: расходящиеся дубликаты сделали бы A/B несопоставимым.

## Generation trial

Один trial выполняет `$strategic-explainer-fast:strategic-explainer-fast` в
реалистичном уже существующем conversation context. Генератор получает только:

- исходный пользовательский вопрос из `facts.md`;
- один exact case и его `facts.md` как authoritative anchor;
- runtime Fast skill.

До фиксации publication text и source basis генератор не читает case
`rubric.md`, common rubric, intended wording, предыдущий candidate или verdict.
Он не создаёт subagent. Один production-like trial обслуживает одну publication
unit; batching разрешён только как отдельный feasibility experiment и должен
быть явно назван.

## Evaluation trial

Release verdict отделён от Fast generation. Независимый evaluator получает
`facts.md`, case `rubric.md`, common rubric, зафиксированные publication text и
source basis. Evaluator не переписывает candidate и ставит PASS только когда:

- сохранены все material facts и отдельные scenario boundaries;
- works, failed, unverified, unknown и not-applicable не смешаны;
- source basis подтверждает claims, но не заменяет понятный body;
- reader без внутренней предметной области понимает problem, outcome, impact и
  next state;
- audit IDs, verification diary и англоязычный смысловой каркас не утекли в
  publication;
- Fast не присвоил authority и не заявил clean/independent guarantee.

Независимый evaluator относится к test harness, а не к Fast runtime. Runtime
Fast никогда не создаёт subagent для generation или self-review.

## Comparative measurements

Сравнение с обычным Strategic Explainer использует одинаковые facts, model
profile и publication unit. Отдельно фиксируются:

- semantic PASS и comprehension defects;
- material omissions и forbidden leakage;
- input, cached input и output tokens;
- latency и число model invocations;
- наличие batching, retries и coordinator cost.

Метрика стоимости не заменяет quality gate. Self-review и batched run являются
feasibility evidence, но не независимым A/B verdict.

## Release gate

Behavioral change Fast готов к публикации только после static validation и
полного blind portfolio. Новый plugin допускается как явный экспериментальный
вариант после честно обозначенного feasibility result, если обычный Explainer
остаётся доступен и rollback определяется одной установкой. Заявление о parity
требует независимого полного A/B, а не только self-review.

