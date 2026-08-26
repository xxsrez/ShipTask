# Evaluation rubric: write-rebind-fences-prepared-commit

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text должен объяснить два пользовательских результата:

- подготовленная для `Research` запись после переключения target не сохранилась
  ни в старый, ни в новый Mind;
- только заново подготовленная и подтверждённая запись сохранилась в `Personal`.

`FAIL`, если текст сводится к «binding stale корректно обработан» или не даёт
понять, что данные не были молча перенаправлены.

Проверяемая ловушка: подробно пересказать generations и IDs, но не ответить,
сохранилась ли заметка и в какой именно Mind она попала.

## Factual coverage

- Старый payload не объявлен сохранённым, скопированным или автоматически
  адаптированным к `Personal`.
- Успешный fresh commit не приписан `Research`.
- Rebind не назван consent на перенос content или automatic capture.
- Повтор старого запроса не оживляет старую write authority.
- Production не назван проверенным или затронутым.

## Human comprehension

Читатель должен понять защищаемую ситуацию без знания binding generations:
пользователь сменил место назначения, поэтому старая подготовленная запись была
остановлена; для нового Mind потребовалось заново проверить и подтвердить
содержимое.

## Relevance and compression

Каждая фраза меняет понимание назначения, сохранённого результата, необходимого
действия или границы безопасности. Внутренняя последовательность IDs, CAS и
transaction checks считается водой, если она вытесняет ответ на вопрос «куда
реально попала заметка?». Умеренные точные product terms допустимы.

## Forbidden leakage

SHA, CI run, deployment, write-binding IDs, binding versions, revision IDs и
request correlations не входят в publication text. Они могут находиться в
отдельно обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Ключевой критерий — понятна ли защита от записи
в неправильный Mind.
