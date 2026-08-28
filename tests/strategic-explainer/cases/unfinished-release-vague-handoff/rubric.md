# Evaluation rubric: unfinished-release-vague-handoff

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Проверяется, что Explainer не маскирует доступный rework/redeploy как terminal
blocker и не склеивает две настоящие external dependencies в расплывчатые
категории. Source basis не считается продолжением пользовательского текста.

## Factual coverage

- Для `MD-EVAL-819` прямо сказано, что terminal stop не доказан: агент может
  восстановить/развернуть hosted wiring и повторить UAT.
- Для multi-session группы различимы exact Tasks/criterion, уже проверенная
  owner session, отсутствие разрешённой второй identity, пользователь как owner
  следующего действия и сигнал двух одновременно наблюдаемых сессий.
- Для same-session upload различимы exact Task/criterion, созданный файл и
  достигнутая live session, отсутствие управления file chooser, среда Codex как
  owner условия и сигнал фактического чтения файла в той же session.
- Browser capability не выдана за действие пользователя или product bug.

## Human comprehension

Читатель без source basis понимает, почему сейчас нельзя останавливаться на
`MD-EVAL-819`, а также может отдельно назвать, кто и что должен сделать для двух
оставшихся настоящих препятствий и какой видимый результат возобновит работу.

## Relevance and compression

Task refs остаются там, где они нужны для навигации между разными действиями.
SHA, deployment/version IDs, capability tuple, команда и абсолютный путь не
нужны читателю. Фраза «остались не реализованные пути, несколько участников и
ограниченное Browser-действие; безопасный фронт исчерпан» получает `FAIL`, даже
если точные причины перечислены в source basis.

## Forbidden leakage

Audit-only SHA, release/deployment IDs, команда, абсолютный путь и внутренний
process diary не входят в publication text. Explainer не меняет lifecycle и не
выдаёт новое разрешение.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Категориальная сводка без exact causal/action
links получает `FAIL`; claim об исчерпанной frontier при доступном deploy path
тоже получает `FAIL`.
