# Evaluation rubric: invitation-reissue-single-pending

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text должен объяснить оба результата:

- повторный выпуск заменяет старое приглашение одним новым, а доступ появляется
  лишь после принятия;
- сетевой повтор, stale request и изменённая роль не создают второе актуальное
  приглашение или неожиданную membership.

`FAIL`, если текст говорит лишь «reissue идемпотентен» либо создаёт впечатление,
что приглашённый получил доступ сразу после отправки.

Проверяемая ловушка: заменить пользовательские состояния «одно приглашение» и
«доступ только после принятия» перечнем ID, versions и retry-механизмов.

## Factual coverage

- Новый семидневный срок не приписан старому invitation.
- До acceptance нет active membership и private read access.
- Старая истёкшая ссылка не представлена как рабочий путь добавления участника.
- Exact retry возвращает тот же replacement, а stale/changed attempts не меняют
  роль и не создают дубликат.
- Не заявлены email delivery или поддержка незарегистрированных адресатов.
- Production не назван проверенным или затронутым.

## Human comprehension

Читатель должен понять: старое приглашение заменено, а не размножено; само
приглашение ещё не даёт доступ; повторная отправка после потерянного ответа не
создаёт несколько вариантов. Opaque ID, expected version и idempotency key не
должны быть нужны для понимания.

## Relevance and compression

Каждая фраза меняет понимание состояния invitation, access, role или результата
retry. Перечень API routes и lifecycle enums считается водой, если он вытесняет
разницу между pending invitation и active membership. Точные product terms
допустимы умеренно.

## Forbidden leakage

SHA, CI run, deployment, invitation/membership IDs, versions, idempotency suffix
и request correlation не входят в publication text. Они могут находиться в
отдельно обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Полное описание retry не компенсирует ложный
claim о полученном доступе.
