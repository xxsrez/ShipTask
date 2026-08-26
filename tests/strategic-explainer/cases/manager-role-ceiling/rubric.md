# Evaluation rubric: manager-role-ceiling

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text различает три результата:

- Manager может назначать Viewer и Editor для повседневной работы;
- Manager не может назначить Manager или передать ownership, причём отказ ничего
  не меняет;
- Owner может выполнить оба защищённых действия, а при передаче остаётся ровно
  один владелец.

## Factual coverage

- Manager не описан как полный администратор Project.
- Owner-only отказы не названы defect.
- Отклонённые команды не приписывают частичную смену ролей.
- Передача ownership не требует выдуманного подтверждения получателя.
- Прежний Owner после передачи назван Manager или смысловой эквивалент этого
  результата не потерян.
- Publication не распространяет вывод на standalone Tasks, глобальные Views или
  production.

## Human comprehension

Читатель должен понять причинную границу: Manager управляет рабочим доступом, но
контроль над Project остаётся защищённым действием Owner. Таблица
`owner > manager > editor > viewer`, policy codes и transaction internals сами
по себе не объясняют проверенный результат.

## Relevance and compression

Не нужно перечислять всю ролевую модель продукта. Достаточно фактов, которые
показывают разрешённые действия, защищённый отказ без побочного изменения и
успешное Owner-действие. Повторение «всё соответствует матрице доступа» после
конкретных результатов является водой, если не добавляет решения или границы.
Английские названия ролей допустимы, но не заменяют ясную русскую мысль.

## Forbidden leakage

Project/user/grant refs, command correlation, policy codes, transaction marker и
snapshot suffix не входят в publication text. Они допустимы только в отдельно
обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Красивое описание иерархии ролей не компенсирует
потерю защищённой границы ownership.
