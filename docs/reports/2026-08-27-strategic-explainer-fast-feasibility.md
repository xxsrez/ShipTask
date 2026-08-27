# Strategic Explainer Fast: feasibility experiment

Дата: 2026-08-27.

## Результат

In-context prototype прошёл 20 из 20 существующих semantic cases по
самопроверке. Весь run выполнен одним агентом в уже загрязнённом рабочем
context без subagent. В publication bodies не найдено служебных identifiers.

Это подтверждает осуществимость отдельного Fast plugin, но не доказывает parity
с обычным Strategic Explainer: генератор и evaluator были одним агентом, а cases
обрабатывались группами по пять.

## Protocol

- Временный неустановленный skill считал один `facts.md` authoritative input, а
  inherited conversation и tool diary — недоверенным process context.
- Case rubric не открывался до фиксации candidates соответствующей группы.
- Skill сохранял scenario map, reader model, language cleanup, audit redaction,
  truth/authority boundaries и отдельный source basis.
- Task Manager, Marketplace, installed plugins, environments и Git не
  изменялись.

## Observed checks

| Check | Result |
| --- | ---: |
| Semantic cases, self-review | 20/20 PASS |
| Audit identifiers in publication bodies | 0 |
| Structural fixture tests at experiment time | 6/6 PASS |
| Temporary skill quick validation | PASS |

## Token telemetry

Оба измерения использовали local `last_token_usage` для `gpt-5.6-sol`; публичная
API price для модели не заявлялась, поэтому сравнение ограничено tokens.

| Category | Ordinary final run | In-context prototype | Difference |
| --- | ---: | ---: | ---: |
| Cached input | 8,292,608 | 2,892,032 | -65.13% |
| Uncached input | 738,271 | 69,401 | -90.60% |
| Output | 86,274 | 16,159 | -81.27% |
| Total | 9,117,153 | 2,977,592 | -67.34% |
| Model events with tokens | 227 | 19 | -91.63% |

Ordinary interval: 2026-08-26 21:18–21:29 UTC, 40 final generator/evaluator
logs; coordinator and earlier failed trials excluded. Prototype interval:
2026-08-27 12:58–13:04 UTC, one dirty context including skill creation,
generation, self-review and static checks. Batching benefits Fast, while omitted
coordinator cost benefits ordinary, so this is directional rather than
like-for-like telemetry.

## Decision

Не заменять ordinary provider. Создать Strategic Explainer Fast как отдельный
explicitly installable experiment with independent Requirements, Architecture,
runtime and evaluation. ShipTask may prefer it by live availability and return
to ordinary behavior when the Fast plugin is absent. Claims of quality parity
remain pending a blind one-unit-at-a-time A/B with independent evaluators.
