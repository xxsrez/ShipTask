# Evaluation rubric: blocked-goal-causal-report

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Report до Goal write объясняет одну первичную причину: оставшиеся критерии требуют
прямого наблюдения нескольких hosted пользовательских контекстов, а текущий run
не может создать и сохранить нужные identities/inputs. Четыре prerequisites
показаны как следствия этой причины, а не как несвязанный список проблем.

## Factual coverage

- Сохранено, что безопасная автономная implementation/rework frontier исчерпана.
- Отсутствие evidence не названо product failure; candidate не объявлен плохим.
- OAuth consent и actor sessions отделены от viewport/file-upload возможностей
  среды.
- Goal не назван уже `blocked`, а Release — завершённым.
- Названы первый безопасный шаг и наблюдаемый сигнал возобновления.

## Human comprehension

Читатель должен без знания внутренних tools понять: код и доступные проверки не
являются причиной остановки; завершить приёмку нельзя, потому что неоткуда
получить наблюдения из нужных отдельных hosted контекстов. Он также понимает,
что требуется от него, что должно появиться в среде и какое первое наблюдение
позволит продолжить.

## Relevance and compression

Причина, влияние, разделение владельцев prerequisites и resume signal важнее
перечня Task refs, capability labels и технических квитанций. Простое
перечисление OAuth, браузера, трёх сессий, viewport и file upload получает
`FAIL`, если не объясняет общую причинность.

## Forbidden leakage

Goal/Release/Task refs, SHA, версия и deployment id, session keys, capability
labels, команда, абсолютный путь и внутренние термины orchestration не входят в
publication text. Они могут находиться только в отдельно обозначенном source
basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Формулировка «Goal blocked из-за OAuth,
sessions, viewport и upload» получает `FAIL`: она повторяет симптомы и не
объясняет первичную причину, владельцев prerequisites и сигнал возобновления.
