# Evaluation rubric: comment-idempotency-and-stale-edit

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text различает три защиты:

- повтор первой отправки возвращает один исходный комментарий без дубликата;
- свежая правка сохраняется, а устаревшая не может её затереть;
- Owner не может редактировать комментарий от имени другого автора.

## Factual coverage

- Retry не назван вторым созданным комментарием.
- Сохранённый итоговый текст соответствует свежей правке, а не stale attempt.
- Conflict не превращён в потерю всего комментария.
- Owner role не описан как право переписывать чужой текст.
- Не приписываются непроверенные delete, replies или historical behavior.
- Publication не утверждает production coverage или уже выполненный status
  transition.

## Human comprehension

Читатель должен понять пользовательский результат: повтор не размножает
сообщение, старая вкладка не стирает новую редакцию, авторство нельзя подменить.
Idempotency keys, optimistic versions, request IDs и count snapshots не должны
быть обязательны для понимания.

## Relevance and compression

Три сценария можно связать одной причинной мыслью о сохранности обсуждения, но
нельзя растворить их в «конфликты обработаны». Технические детали транспорта и
transaction trace являются водой. Умеренные названия role/status допустимы;
основной текст должен звучать естественно по-русски.

## Forbidden leakage

Task/comment refs, idempotency suffix, versions, request IDs, raw count snapshots
и trace не входят в publication text. Они допустимы только в отдельно
обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Упоминание `idempotency` и `version conflict`
без человеческих последствий не является достаточным объяснением.
