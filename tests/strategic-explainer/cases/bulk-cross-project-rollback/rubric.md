# Evaluation rubric: bulk-cross-project-rollback

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text показывает оба исхода:

- неясное решение о несовместимом Release отклоняет весь набор без перемещения
  любой Task и без расхода номера;
- явная очистка Release позволяет перенести обе Tasks вместе, сохранив их
  identity и доступность по прежним identifiers.

## Factual coverage

- Первый отказ не описан как частичный успех или product defect.
- Ни одна Task не объявлена перенесённой в Scenario A.
- Успешный retry не скрывает проверенную атомарность первоначального отказа.
- Public identity не названа новой только из-за смены human-readable identifier.
- Release очищается явно, а не молча.
- Непроверенные hierarchy/relation paths и production не объявляются прошедшими.

## Human comprehension

Читатель должен понять защищаемый результат: если для одной выбранной Task неясно,
как сохранить совместимость, система не двигает ни одну; после явного решения
обе переезжают без потери истории. UUID, sequence internals, version map и
transaction IDs не нужны для этой мысли.

## Relevance and compression

Пара старых/новых identifiers может сделать результат конкретным, но полный
перечень refs и versions является водой. Каждая фраза должна объяснять действие,
отказ без побочного эффекта, успешный retry или границу. Слова `rollback`,
`transaction` и `identity` допустимы лишь там, где они помогают, а не заменяют
простое русское объяснение.

## Forbidden leakage

Project/Task/Release refs, versions map, raw sequence bookkeeping, transaction IDs
и repository trace не входят в publication text. Они могут находиться только в
отдельно обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Одного сообщения об успешном retry недостаточно,
если потерян факт полного rollback первой попытки.
