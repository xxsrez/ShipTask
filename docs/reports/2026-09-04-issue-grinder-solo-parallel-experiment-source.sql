-- Source snapshot for the portable report. Values are transcribed from the
-- saved run.json, acceptance.json, thread-tree.json and gate receipts listed in
-- docs/tasks/issue-grinder-solo-parallel-experiment.md.
WITH benchmark_runs(
  run_order, run_id, label, scheme, wall_seconds, raw_passed, adjusted_passed,
  sol_tokens, luna_tokens, total_tokens, api_equivalent_usd,
  gate_start_spread_ms, gate_finish_spread_ms, outcome
) AS (
  VALUES
    (1, 'S1', 'S1 Solo', 'Solo', 562.143, 19, 21, 1247531, 0, 1247531, 1.006278, NULL, NULL, 'valid control'),
    (2, 'E1', 'E1 parallel v0', 'parallel v0', 684.787, 21, 21, 1303608, 1950721, 3254329, 1.037318, NULL, NULL, 'rejected: slower'),
    (3, 'E2', 'E2 parallel v1', 'parallel v1', 468.899, 19, 21, 1196426, 823187, 2019613, 0.913293, NULL, NULL, 'valid predecessor'),
    (4, 'S2', 'S2 Solo', 'Solo', 755.154, 21, 21, 1672261, 0, 1672261, 1.243095, NULL, NULL, 'valid control'),
    (5, 'E4', 'E4 parallel v2', 'parallel v2', 449.758, 18, 21, 1335425, 450290, 1785715, 1.036007, 9, 6, 'valid final prototype')
)
SELECT * FROM benchmark_runs ORDER BY run_order;

WITH sol_categories(category_order, category, solo_tokens, experimental_tokens) AS (
  VALUES
    (1, 'Реализация поверхностей', 974191, 91342),
    (2, 'Понимание и планирование', 108766, 283555),
    (3, 'Dispatch, ожидание и fan-in', 0, 692284),
    (4, 'Финальная проверка и review', 376940, 268244),
    (5, 'Всего Sol', 1459896, 1335425)
)
SELECT
  category_order,
  category,
  solo_tokens,
  experimental_tokens,
  experimental_tokens - solo_tokens AS delta_tokens
FROM sol_categories
ORDER BY category_order;
