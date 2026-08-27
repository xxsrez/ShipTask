# Strategic Explainer: сравнение SOL и Luna

Дата прогона и решения: 2026-08-27.

## Решение

Обычный Strategic Explainer запускает fresh provider-subagent на
`gpt-5.6-luna` с `reasoning_effort="max"`. SOL больше не наследуется от
coordinator-а и не является скрытым fallback. Если exact Luna Max profile
недоступен, caller применяет собственную provider-unavailability policy.

Решение принято пользователем после paired model-forward сравнения и blind
визуального выбора. При указанной пользователем примерно двадцатикратной
разнице стоимости наблюдаемое ухудшение признано допустимым: Luna чаще уступала
в строгом попарном ranking, но сохранила пригодный уровень на большинстве
случаев и несколько раз дала более короткий и естественный результат.

## Метод

На каждом из 20 current fixtures выполнены два отдельных terminal provider
invocation с одинаковыми `fork_turns="none"` и `reasoning_effort="max"`:
один на `gpt-5.6-sol`, второй на `gpt-5.6-luna`. Generator видел только exact
role lock, одну publication task и соответствующий `facts.md`; case rubric,
прошлый candidate и intended wording не передавались.

Отдельный fresh SOL evaluator получал два анонимных candidate, `facts.md`,
case rubric и общий semantic gate. Он давал независимый `PASS | FAIL` каждому
тексту и выбирал более готовый к публикации. Положение Luna в паре A/B
чередовалось. Три показанные пользователю blind-пары дали те же предпочтения,
что evaluators: одна победа SOL и две победы Luna; четвёртая незавершённая
человеческая пара в результат не включена.

## Результаты

| Case | Luna | SOL | Blind preference |
| --- | --- | --- | --- |
| `automatic-capture-safe-boundary` | PASS | PASS | SOL |
| `bulk-cross-project-rollback` | PASS | PASS | Luna |
| `comment-idempotency-and-stale-edit` | PASS | PASS | Luna |
| `concurrent-edit-no-hidden-merge` | PASS | PASS | SOL |
| `green-local-failed-uat` | FAIL | PASS | SOL |
| `hierarchy-cycle-and-stale-guard` | PASS | PASS | Luna |
| `historical-content-current-access` | PASS | PASS | SOL |
| `idempotent-retry-with-authorization` | PASS | PASS | Luna |
| `invitation-reissue-single-pending` | PASS | PASS | Luna |
| `large-file-boundary` | FAIL | FAIL | SOL |
| `manager-role-ceiling` | FAIL | PASS | SOL |
| `mixed-preview-boundary` | PASS | PASS | SOL |
| `ownership-transfer-one-owner` | PASS | PASS | SOL |
| `project-shadow-restore` | PASS | PASS | SOL |
| `redeploy-persistence-failure` | PASS | PASS | SOL |
| `release-delete-membership-boundary` | PASS | PASS | SOL |
| `release-open-tasks-confirmation` | PASS | PASS | SOL |
| `saved-view-base-temporary-separation` | FAIL | FAIL | Luna |
| `viewer-comment-permissions` | PASS | PASS | SOL |
| `write-rebind-fences-prepared-commit` | PASS | PASS | SOL |
| **Итого** | **16/20 PASS; 6 предпочтений** | **18/20 PASS; 14 предпочтений** | **SOL 14 : 6 Luna** |

Два специфичных Luna-дефекта изменили строгий verdict: в UAT blocker
просочился synthetic Task ID, а в role-ceiling case потерялся промежуточный
переход `Viewer → Editor`. В двух других cases провалились обе модели: оба
candidate вынесли version detail в Saved View publication, а large-file
candidate получили разные compression/coverage defects. Катастрофической
потери причинности, новой authority или выдуманного lifecycle effect у Luna в
этом прогоне не было.

## Граница вывода

Это один paired trial на case, а не доказательство долгосрочной частоты ошибок.
Предыдущий отдельный SOL run прошёл 20/20, тогда как свежий control прошёл
18/20, что подтверждает стохастичность wording и строгих verdict. Текущая
регрессия поэтому сохраняет весь 20-case Luna Max gate после material изменения
provider behavior; SOL comparison остаётся исследовательским control, а не
release requirement.
