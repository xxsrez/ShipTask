# Evaluation rubric: hierarchy-cycle-and-stale-guard

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text объясняет два contract-backed результата:

- cycle и parent из другого Project отклоняются, не ломая существующее дерево;
- устаревший повтор создания subtask не создаёт дубликат.

Одновременно текст сохраняет границу: это synthetic contract/local-test
evidence, а не live-release proof.

## Factual coverage

- Успешная исходная parent/subtask связь не объявлена сломанной.
- Cycle и cross-Project отказ не создают промежуточных edges.
- Stale retry не назван вторым успешным созданием.
- Не придумывается coverage для relations.
- Нельзя утверждать, что hierarchy доступна в UAT, production или уже выпущена
  пользователям.
- Нельзя превращать наличие локального теста в completion claim всей функции.

## Human comprehension

Читатель должен понять защищаемое поведение: дерево остаётся непротиворечивым, а
повтор со старым состоянием не создаёт вторую подзадачу. `CAS`, graph guard,
versions, edge IDs и sequence audit не должны нести основную мысль. Также должно
быть очевидно, что речь о контрактной проверке, а не о живом релизе.

## Relevance and compression

Не нужно перечислять все виды graph validation. Нужны только наблюдаемые
результаты, сохранность дерева, отсутствие дубликата и честная evidence boundary.
Технический термин допустим, если без него теряется точность; двуязычный перечень
внутренних механизмов считается шумом.

## Forbidden leakage

Project/Task refs, raw versions, edge path, command correlation, sequence audit и
test shard не входят в publication text. Они допустимы только в отдельно
обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Любой live-release claim является `FAIL`, даже
если guard behavior пересказан верно.
