# Model-forward tests Strategic Explainer Fast

Fast использует canonical 20-case corpus из
[`../strategic-explainer/`](../strategic-explainer/), чтобы A/B не расходился по
fixtures. Его generation protocol отличается:

- один case является одной publication unit;
- текущий agent уже может иметь рабочий conversation context;
- authoritative input ограничен соответствующим `facts.md`;
- `rubric.md`, `common-rubric.md`, intended wording, candidate и verdict скрыты
  до фиксации publication text и source basis;
- `$strategic-explainer-fast:strategic-explainer-fast` полностью читает свой
  in-context contract и не создаёт subagent;
- process diary и inherited conclusions не считаются evidence.

После фиксации результата отдельный independent evaluator получает raw facts,
case rubric, common rubric, publication text и source basis. Этот evaluator —
часть test harness, не Fast runtime. Self-review или batching нескольких cases
должны быть обозначены как feasibility trial и не называются blind independent
evaluation.

Static structure запускается вместе со всем suite:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
```

