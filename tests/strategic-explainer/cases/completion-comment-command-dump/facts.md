# Raw facts: completion-comment-command-dump

Source project: ExampleNotes

Test fixture: полностью синтетический сценарий для model-forward проверки. Он не
описывает текущую Task или реально выполненный релиз ExampleNotes.

## Publication unit

Нужен один review-ready comment для вымышленной Task `MD-EVAL-611` перед
переходом из `In Progress` в `In Review`. Comment должен объяснить полученный
пользовательский результат и честную границу проверки, а не переносить в Task
технический журнал реализации.

## User-visible acceptance

### Scenario A — повтор после неопределённого ответа не создаёт дубль

- Пользователь отправил сохранение, но клиент не получил однозначный ответ.
- После перезагрузки экран показал уже сохранённый результат.
- Повторное нажатие продолжило ту же операцию и не создало вторую запись.
- После обновления страницы осталась ровно одна запись с ожидаемым содержимым.

### Scenario B — граница готовности

- Поведение проверено локально на собранном candidate в пользовательском
  браузерном сценарии и интеграционных тестах.
- Независимая review ещё не выполнялась; именно для неё Task переводится в
  `In Review`.
- Hosted UAT и production не запускались и не заявляются проверенными.

## Knowledge and authority boundary

- Локальное наблюдение подтверждает защиту от дубля для exact candidate, но не
  доказывает hosted UAT или production.
- Comment не должен утверждать, что status уже изменён: переход выполняется
  только после публикации и read-back.
- Никакого действия пользователя сейчас не требуется.

## Audit-only evidence

- candidate SHA `5d8c7b7d042a17f2b15e445b1e166dad61614c1a`;
- worktree `/Users/eval/.codex/worktrees/md-eval-611/ExampleNotes`;
- команда `npm test -- retry-save.integration.test.ts --runInBand`;
- команда `npx playwright test tests/retry-save.spec.ts`;
- тестовые файлы `src/save/retry.ts`, `tests/retry-save.spec.ts` и
  `tests/retry-save.integration.test.ts`;
- локальный run `md-eval-611-local-044`;
- candidate id `candidate_md_eval_611_5d8c`;
- результат unit/integration `31/31`, browser scenarios `4/4`.

## Accepted product source

Смысл повторной отправки и границы локальной проверки описаны в read-only
sources:

- `/workspace/ExampleNotes/docs/specs/idempotent-save.md`;
- `/workspace/ExampleNotes/tests/retry-save.integration.test.ts`;
- `/workspace/ExampleNotes/AGENTS.md`.
