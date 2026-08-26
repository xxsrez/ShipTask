# Evaluation rubric: release-open-tasks-confirmation

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text позволяет восстановить три результата:

- выпуск с открытой Task без явного подтверждения не происходит;
- после подтверждения Release становится выпущенным, но Task намеренно остаётся
  открытой;
- устаревшее следующее изменение не перезаписывает новое состояние.

## Factual coverage

- Первый отказ не назван defect или успешным release transition.
- Наличие даты выпуска не превращено в claim, что все Tasks завершены.
- Открытая Task не объявлена автоматически переведённой в `Done`.
- Explicit confirmation не описано как закрытие или отмена Task.
- Stale update не приписывает частичную смену статуса/date.
- Не утверждается изменение released composition или production deployment.

## Human comprehension

Главная мысль для читателя: выпуск с незавершённой работой возможен только как
осознанное решение, и это решение не маскирует Task как выполненную. Versions,
confirm flags, timestamps и sync cursors не должны заменять эту причинную модель.

## Relevance and compression

Техническое перечисление lifecycle states не нужно, если не объясняет судьбу
открытой Task. Дата может быть агрегирована как «зафиксирована дата выпуска».
Короткий вывод готовности Task к закрытию допустим только после конкретных
результатов. Русский текст может умеренно использовать названия Release/Task и
статусов, но не строиться из API-терминов.

## Forbidden leakage

Project/Release/Task refs, raw versions, confirmation request, exact timestamp,
request correlation и sync cursor не входят в publication text. Они могут быть
в отдельно обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Текст `Release успешно закрыт` без явного факта,
что Task осталась открытой, является `FAIL`.
