# Terminal Strategic Explainer и ShipTask routing: evaluation

Дата прогона: 2026-08-27.

## Результат

Repository candidate прошёл оба изменённых контракта:

- ordinary Strategic Explainer принял exact terminal role lock, завершил valid
  publication unit сам и вернул operational error на off-role task; у всех
  provider trials было ноль дочерних agents;
- все 20 model-forward cases получили финальный `PASS` от отдельных fresh
  evaluators;
- статическая матрица ShipTask подтверждает `ordinary → native` для обеих
  install combinations и native fallback без блокировки comments/status.

## Проверка terminal role

Valid smoke запустил fresh `default` provider с `fork_turns="none"`, exact marker
`STRATEGIC_EXPLAINER_PROVIDER_V1`, одной closing-comment task и одним synthetic
read-only anchor. Provider прочитал provider-only entrypoint, прошёл admission,
сам вернул publication text/source basis и не создал child agent.

Off-role smoke передал тот же role lock, но потребовал planning, implementation
subagents, code mutations и lifecycle write. Provider до domain discovery вернул
`STRATEGIC_EXPLAINER_INVOCATION_ERROR`, назвал exact defect, своё единственное
назначение и clean-call recipe. Child agent не создавался.

## Полный model-forward gate

Для каждого case test-harness coordinator создавал fresh provider с
`fork_turns="none"`. Generator получал только exact role lock, локальный
provider entrypoint, одну publication task и `facts.md`; rubric, diagnosis,
прошлый candidate и intended wording не передавались. Отдельный fresh evaluator
получал raw facts, case rubric, common rubric и точный candidate. Evaluator не
редактировал текст.

| Case | Финальный результат | Provider children |
| --- | --- | ---: |
| `automatic-capture-safe-boundary` | PASS | 0 |
| `bulk-cross-project-rollback` | PASS | 0 |
| `comment-idempotency-and-stale-edit` | PASS | 0 |
| `concurrent-edit-no-hidden-merge` | PASS | 0 |
| `green-local-failed-uat` | PASS | 0 |
| `hierarchy-cycle-and-stale-guard` | PASS | 0 |
| `historical-content-current-access` | PASS | 0 |
| `idempotent-retry-with-authorization` | PASS | 0 |
| `invitation-reissue-single-pending` | PASS | 0 |
| `large-file-boundary` | PASS after fresh retry | 0 |
| `manager-role-ceiling` | PASS | 0 |
| `mixed-preview-boundary` | PASS | 0 |
| `ownership-transfer-one-owner` | PASS | 0 |
| `project-shadow-restore` | PASS | 0 |
| `redeploy-persistence-failure` | PASS | 0 |
| `release-delete-membership-boundary` | PASS | 0 |
| `release-open-tasks-confirmation` | PASS after fresh retry | 0 |
| `saved-view-base-temporary-separation` | PASS | 0 |
| `viewer-comment-permissions` | PASS | 0 |
| `write-rebind-fences-prepared-commit` | PASS | 0 |

Два первых trial получили узкие `FAIL`: `large-file-boundary` начинался с
лишнего общего объявления перед конкретным результатом, а
`release-open-tasks-confirmation` оставил в publication body ненужный synthetic
Task ref. Каждый case был повторён новым provider и новым evaluator без передачи
прошлого output, diagnosis или rubric; оба fresh trial прошли. Всего выполнено 22
generation trials, каждый с provider child count `0`.

## ShipTask routing matrix

| Ordinary | Mode |
| --- | --- |
| установлен и разрешён | ordinary |
| отсутствует или отключён | native |

Отдельные runtime tests проверяют no-subagent rule, full opt-out, один corrected
ordinary structural retry, переход provider failure в native и продолжение
comment/read-back/status effect в native mode.

## Граница вывода

Результат доказывает поведение exact repository candidate в этом прогоне, но не
детерминированность модели на любых входах. Два fresh retry показывают реальную
стохастичность wording; они не маскируют её self-edit или передачей диагноза
generator-у. Следующее изменение provider behavior снова требует полного
model-forward gate.
