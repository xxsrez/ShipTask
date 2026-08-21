# 0019. Goal только для массовой имплементации Tasks

Статус: accepted, 2026-08-21. Заменяет selector-based Goal policy из ADR-0007 и
ADR-0017, уточняя Goal/release части текущего ShipTask contract.

## Контекст

Текущий runtime автоматически относил любой Project, Release, current scope или
bare `$ship-tasks` к `batch` и создавал Goal. Поэтому операционная просьба
выпустить уже подготовленный candidate, в том числе в production, разворачивала
Goal на весь inventory Release. Тип selector оказался ошибочно принят за тип
работы.

Goal полезен, когда один run координирует длительную реализацию или rework
нескольких Tasks. Для commit/push/deploy/smoke готового candidate он создаёт
лишний lifecycle, расширяет objective до чужих Tasks и мешает точно завершить
release-only запрос.

## Решение

- `batch-implementation` означает, что current run реально реализует или
  возвращает в rework минимум две concrete Tasks. Только этот mode создаёт Goal.
- Одна Task всегда выполняется без Goal, даже если она выбрана через parent
  Project или Release.
- Project, Release, current scope, список Tasks и bare invocation являются
  selectors для discovery. Они не определяют mode и не разрешают Goal сами по
  себе.
- Чтение, проверка, приёмка или lifecycle reconciliation нескольких Tasks не
  являются массовой имплементацией.
- `release` означает commit, push, publish, deploy, smoke и при необходимости
  bounded repair/rollback уже подготовленного candidate. Release-only не создаёт,
  не переиспользует, не ретаргетит и не завершает Goal только ради release.
- Production отличается дополнительной authority boundary, а не Goal policy.
  Явный production approval не является основанием создать Goal.
- Release может быть done criterion уже активного совместимого Goal только если
  Goal был создан для массовой имплементации и release входил в её исходный
  observable outcome. Сам release новый Goal не создаёт.
- Если release обнаруживает defect, одна локальная доработка не создаёт Goal.
  Переход к `batch-implementation` допустим только когда current authority
  действительно охватывает implementation/rework минимум двух exact Tasks.

## Последствия

- Goal отражает координационную сложность работы, а не размер inventory.
- Production release готового candidate остаётся точным release-only run без
  скрытого расширения на весь Project/Release.
- Bare invocation требует live inventory и классификации фактической работы до
  решения о Goal.
- Evals отдельно проверяют массовую имплементацию с Goal и release-only без Goal.

## Не принято

- Создавать Goal для любого selector, содержащего больше одной Task.
- Создавать Goal для любого Project или Release независимо от requested outcome.
- Считать commit/push/deploy/smoke массовой имплементацией Tasks.
- Создавать Goal «на всякий случай», если release может обнаружить дефект.
