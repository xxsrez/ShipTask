# Evaluation rubric: saved-view-base-temporary-separation

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text объясняет два materially different действия:

- временный фильтр применяется поверх сохранённого и может быть очищен без
  изменения исходной View;
- `Save as` создаёт новую View из совместного результата, не меняя исходную.

Нельзя заменить это общей фразой «фильтры и сохранение работают».

## Factual coverage

- Temporary filter не назван заменой или скрытым изменением base query.
- `Clear temporary` не приписано удаление сохранённого Release filter.
- Новая View содержит оба условия через `AND`, а не только priority.
- Исходная View остаётся неизменной после `Save as`.
- Saved View не описана как копия Tasks и не получает право менять Tasks.
- Publication не распространяет вывод на непроверенные global/sharing paths или
  production.

## Human comprehension

Читатель должен понять простую модель: временное уточнение влияет только на
текущий просмотр; отдельное явное сохранение создаёт новый повторяемый список.
Query AST, versions, URL digest и sync cursor не должны быть нужны для этого
понимания.

## Relevance and compression

Counts могут помочь показать разницу результатов, но внутренние механизмы
executor/query storage и пересказ всей системы фильтров не нужны. Каждая фраза
должна добавлять действие, наблюдаемый результат, границу или решение. Английские
названия UI actions и сущностей допустимы умеренно; смешанная техническая каша —
нет.

## Forbidden leakage

View/Release refs, versions, AST node IDs, URL digest, executor snapshot и sync
cursor не входят в publication text. Они могут находиться только в отдельно
обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Точный пересказ counts не компенсирует ложное
впечатление, что temporary layer переписал исходную View.
