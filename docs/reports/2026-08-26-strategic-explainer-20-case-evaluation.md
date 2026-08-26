# Strategic Explainer: model-forward evaluation из 20 сценариев

Дата прогона: 2026-08-26.

## Результат

Текущий repository candidate `$strategic-explainer:strategic-explainer` прошёл
20 из 20 независимых blind-reader проверок: 10 сценариев ExampleNotes и 10
сценариев Task Manager. Это проверка поведения модели, а не snapshot exact
wording: каждый generating subagent получал только `SKILL.md` и `facts.md`, а
отдельный judge видел publication body, исходные факты и semantic rubric, но не
ход рассуждений генератора.

## Что изменил первый прогон

Первый кандидатный прогон обнаружил два повторяющихся дефекта:

- в русское объяснение просачивалась гибридная внутренняя терминология вроде
  `synthetic private UAT`;
- publication body повторял audit identifiers: номера revisions и
  синтетические Task refs, хотя они не помогали понять результат.

Provider contract получил две общие, не привязанные к fixture проверки:
нормализацию языка публикации и отдельную redaction-проверку между raw facts и
готовым человеческим слоем. После этого весь набор был сгенерирован заново
fresh subagents и оценён новыми независимыми judges.

## Матрица финального прогона

| Продукт | Сценарий | Результат |
| --- | --- | --- |
| ExampleNotes | `large-file-boundary` | PASS |
| ExampleNotes | `mixed-preview-boundary` | PASS |
| ExampleNotes | `redeploy-persistence-failure` | PASS |
| ExampleNotes | `concurrent-edit-no-hidden-merge` | PASS |
| ExampleNotes | `idempotent-retry-with-authorization` | PASS |
| ExampleNotes | `historical-content-current-access` | PASS |
| ExampleNotes | `write-rebind-fences-prepared-commit` | PASS |
| ExampleNotes | `automatic-capture-safe-boundary` | PASS |
| ExampleNotes | `invitation-reissue-single-pending` | PASS |
| ExampleNotes | `ownership-transfer-one-owner` | PASS |
| Task Manager | `viewer-comment-permissions` | PASS |
| Task Manager | `manager-role-ceiling` | PASS |
| Task Manager | `saved-view-base-temporary-separation` | PASS |
| Task Manager | `project-shadow-restore` | PASS |
| Task Manager | `release-delete-membership-boundary` | PASS |
| Task Manager | `bulk-cross-project-rollback` | PASS |
| Task Manager | `hierarchy-cycle-and-stale-guard` | PASS |
| Task Manager | `comment-idempotency-and-stale-edit` | PASS |
| Task Manager | `release-open-tasks-confirmation` | PASS |
| Task Manager | `green-local-failed-uat` | PASS |

## Граница вывода

PASS означает, что в этом прогоне публикация сохранила существенные факты,
объяснила пользовательский результат простым языком, отделила доказанное от
непроверенного и не превратила audit trail в основной текст. Это не доказывает
детерминированность модели на любых входах и не заменяет повторный полный прогон
после следующего изменения provider behavior.

Сами fixtures и правила воспроизведения находятся в
[`tests/strategic-explainer/`](../../tests/strategic-explainer/).
