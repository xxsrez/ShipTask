# Evaluation rubric: green-local-failed-uat

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Blocker report объясняет два разных evidence layers:

- локальный candidate прошёл проверки, но UAT deployment failed до live smoke;
- успешный read через production plugin не является проверкой UAT candidate и
  не разрешает production release.

Главный вывод — поставка не готова, пока UAT не достиг terminal success и не
пройден authenticated smoke.

## Factual coverage

- Green local checks не названы доказательством hosted UAT behavior.
- Failed deploy не смягчён до «осталось только посмотреть деплой».
- Отсутствующие smoke/migration/error checks не объявлены пройденными.
- Plugin response правильно отнесён к production endpoint и не использован как
  UAT substitute.
- Не выдумывается root cause provider failure.
- Следующий шаг остаётся в UAT; production не объявлен затронутым или разрешённым.

## Human comprehension

Читатель должен сразу понять blocker: код локально выглядит исправным, но новая
версия не запустилась в тестовой среде, поэтому реальную работу приложения ещё
не проверили. SHA, Sites version, deployment ID, provider event и binding internals
не должны быть нужны для этой мысли.

## Relevance and compression

Достаточно назвать прошедший локальный слой агрегированно и конкретно указать,
какого hosted результата нет. Полный список команд, идентификаторов и provider
trace является водой. Следующий шаг должен быть наблюдаемым и не расширять
authority. Умеренные `UAT`, `production`, `deploy` допустимы, если объяснены
человеческим языком и не образуют двуязычную кашу.

## Forbidden leakage

SHA, run/version/deployment/project IDs, event correlation, previous version и
plugin request ID не входят в publication text. Они могут находиться только в
отдельно обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Текст «всё проверено, кроме деплоя» является
`FAIL`, поскольку скрывает отсутствие самой hosted проверки.
