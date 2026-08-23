# 0026. Периодические UAT releases разумными batch-группами

Статус: accepted, 2026-08-23. Это текущее уточнение
[ST-24](../skills/ship-tasks/requirements.md) и архитектурная компенсация
пропущенной при source-package rebuild review-batch семантики; оно не меняет
границу production из [ADR-0004](0004-autonomous-continuation-and-release-authority.md).

## Исходное пользовательское требование

Пользователь явно потребовал дешёвый targeted check на каждую Task и более
тщательное тестирование периодическими batch-группами, а также разрешил обычные
UAT/dev releases без отдельного approval. UAT не является production: в него
можно самостоятельно публиковать разумные накопленные группы изменений, а не
каждый отдельный баг или Task.

## Контекст сбоя

Старый runtime содержал `per-Task targeted gate`, `review-batch gate` и общие
external effects в batch cadence. При перестройке ShipTask из per-skill source
packages этот контракт выпал из текущих Requirements/Architecture и runtime.
Соседний run 2026-08-23 поэтому сделал локальные проверки и read-only UAT probe,
но сообщил, что deployment не выполнялся из-за якобы отсутствующей отдельной
authority. Это противоречит уже принятой non-production UAT boundary.

## Решение

- Каждая Task получает лёгкую проверку, достаточную для её acceptance.
- Совместимые ready candidates объединяются в exact integrated review batch.
- При cadence/trigger — batch target, review WIP, wave/frontier, общий UAT
  effect, acceptance/Done, checkpoint или final flush — выполняется один
  тщательный batch gate и один deploy exact candidate в UAT с verified
  read-back.
- UAT deployment после проверки non-production target входит в standing delivery
  authority и не требует дополнительного вопроса. Неуспешный deploy или smoke
  остаётся честным proof gap/incident, а не поводом объявить deploy выполненным.
- High-risk/coupled Task, явный singleton или final flush могут быть batch из
  одного member. Это не default: исключение не превращает каждую Task в
  singleton и не оправдывает деплой каждой Task.
- Run report обязан назвать batch members, exact SHA, checks, UAT receipt/read-back
  и smoke; Production release и его authority остаются отдельной explicit-
  authority boundary.

## Не является решением

ADR не задаёт универсальный календарный интервал, не разрешает production release,
не превращает Task Manager status в deployment proof и не разрешает destructive,
privacy, secrets, access-policy или unbounded-cost effects.

## Observable evaluation

Regression matrix должна различать targeted per-Task gate и periodic thorough
batch gate, проверять один UAT deploy на batch, отсутствие approval ritual для
обычного UAT и truthful report/read-back exact candidate.
