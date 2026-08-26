# Evaluation rubric: project-shadow-restore

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text различает:

- Project delete, который временно скрывает обычный subtree как единое целое;
- Project restore, который возвращает обычный subtree, но оставляет отдельно
  удалённую Task в `Recently deleted`.

Фраза «проект и все данные восстановлены» является фактической потерей главной
границы сценария.

## Factual coverage

- Project shadow не описан как отдельное удаление каждого child.
- Пять обычных Tasks, Releases и Saved View после restore названы вернувшимися
  либо этот результат передан без двусмысленности.
- Отдельно удалённая Task не объявлена восстановленной или потерянной навсегда.
- Не выдумывается permanent purge или точный момент очистки.
- Отсутствие дублей не превращается в claim о любых возможных restore paths.
- Publication не утверждает работу с production или реальными данными.

## Human comprehension

Читатель должен понять разницу между «Project временно скрыл состав» и «эта Task
сама лежит в корзине». Термины deletion tuple, shadow implementation, transaction
и sync cursor не должны быть нужны для восстановления этой мысли.

## Relevance and compression

Counts уместны, когда помогают показать, что именно вернулось. Детали timestamps,
tuple scans и repository trace являются audit noise. Короткий итог готовности к
закрытию допустим, но не заменяет важное исключение для отдельно удалённой Task.
Английские product names можно оставить, технический двуязычный каркас — нет.

## Forbidden leakage

Project/Task refs, tuple/transaction IDs, retention timestamp, sync cursors и
trace не входят в publication text. Они допустимы в отдельно обозначенном source
basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Удачный короткий текст не проходит, если
создаёт впечатление восстановления отдельно удалённой Task.
