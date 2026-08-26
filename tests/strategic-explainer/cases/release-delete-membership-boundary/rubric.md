# Evaluation rubric: release-delete-membership-boundary

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text различает два lifecycle outcome:

- recoverable delete скрывает Release membership, не удаляя Tasks, а restore
  возвращает membership;
- permanent purge также сохраняет Tasks, но окончательно очищает их Release
  links, при этом Saved View filter остаётся узким и даёт пустой результат.

## Factual coverage

- Ни в одном сценарии Tasks не названы удалёнными вместе с Release.
- Временно скрытая membership не описана как окончательно очищенная.
- Restore возвращает именно прежнюю membership, а не создаёт новые Tasks.
- После purge Saved View не объявлена удалённой, переписанной или расширенной.
- Два независимых fixtures не превращены в одну невозможную последовательность.
- Owner confirmation и отсутствие production-impact не преувеличены.

## Human comprehension

Читатель должен понять: Release можно временно убрать и вернуть вместе с его
составом; необратимое удаление отвязывает, но не уничтожает Tasks и не превращает
сохранённый фильтр в «показать всё». Tuple, AST и purge job details для этого не
нужны.

## Relevance and compression

Называть все семь Tasks не требуется; count уместен как доказательство сохранения
состава. Реализационные детали inactive projections, missing refs и transactions
не должны вытеснять пользовательское последствие. Английские названия сущностей
допустимы умеренно, но текст остаётся естественным русским.

## Forbidden leakage

Release/Task/View refs, tuple revision, purge job, AST ref и transaction IDs не
входят в publication text. Они могут находиться только в отдельно обозначенном
source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Общая фраза «релиз удаляется и восстанавливается»
не компенсирует потерю судьбы Tasks и сохранённого фильтра.
