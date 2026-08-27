# Model-forward tests Strategic Explainer

Эти fixtures проверяют не совпадение с эталонной фразой, а способность
`$strategic-explainer:strategic-explainer` превратить сырой технический след в понятный
человеку комментарий. Все продуктовые события здесь синтетические: они
опираются на принятые ExampleNotes и Task Manager contracts, но не являются
утверждением о фактическом состоянии Task, UAT или production.

## Структура case

Каждый case содержит два изолированных входа:

- `facts.md` — единственный fixture, доступный generating subagent;
- `rubric.md` — semantic gate для отдельной оценки готового текста.

Generating subagent не получает rubric, diagnosis, intended wording, прежний
плохой комментарий или candidate другого trial. Он запускается новым built-in
`default` subagent с `fork_turns="none"`, `model="gpt-5.6-luna"` и
`reasoning_effort="max"`; compact task содержит отдельную точную строку
`STRATEGIC_EXPLAINER_PROVIDER_V1`, одну publication task и anchor на один
`facts.md`. Router выбирает terminal provider path, provider-only entrypoint
выполняет admission, после чего subagent возвращает publication text и отдельно
обозначенный source basis.

Это white-box evaluation harness: он намеренно знает внутренний invocation
recipe, чтобы проверить released implementation. ShipTask, Task Composer и
обычный direct client этих параметров не получают и вызывают только semantic
facade.

Evaluator получает исходный `facts.md`, соответствующий `rubric.md`, publication
text, source basis и общий [semantic gate](common-rubric.md). Он отдельно проверяет factual coverage и человеческое
понимание. Формулировка может отличаться между trials; `PASS` требует, чтобы
читатель понял, что именно проверено, при каком значимом входе или границе, что
наблюдалось и готов ли результат к следующему состоянию.

Evaluator — отдельный test-harness agent, а не часть runtime provider-а. Provider
не вызывает evaluator, не создаёт child agents и выполняет только внутренний
comprehension check перед возвратом result.

## Cases

Suite содержит ровно 20 materially different cases, поровну из двух соседних
продуктов. ExampleNotes покрывает размер и тип файлов, persistence после
переиздания, concurrent edits, idempotent retry, current access к истории,
write rebind, automatic capture, повторную выдачу приглашения и перенос
ownership. Task Manager покрывает ACL комментариев, role ceiling, сохранённые и
временные фильтры, recoverable deletion Project и Release, атомарный массовый
перенос, hierarchy guards, idempotent comment edits, выпуск с открытыми Tasks и
границу между зелёной локальной проверкой и провалившимся UAT.

Матрица намеренно содержит success, expected boundary, partial result,
regression, permission denial, stale conflict, atomic rollback и blocker report.
Это не двадцать перефразировок одного closing comment.

## Запуск

Структура fixtures и отсутствие подсказок generator-у проверяются локально:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
```

Поведенческий gate выполняется через fresh Codex subagents. Для каждого case
нужен как минимум один blind generation trial и отдельная независимая оценка.
После изменения provider behavior запускаются все cases; нестабильный либо ранее
провалившийся case повторяется новым fresh trial, а не follow-up прежнему агенту.
