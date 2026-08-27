# 0025. Cost-aware профили субагентов с эскалацией на current model

Статус: accepted, 2026-08-22; profile routing ordinary Strategic Explainer
частично заменено ADR-0034. Расширяет
[ADR-0024](0024-adaptive-multi-agent-execution-by-default.md) выбором execution
profile для каждого полезного packet и частично заменяет свободу model/effort
из [ADR-0021](0021-requirements-as-agent-constitution.md), потому что
пользователь явно потребовал Luna Max для особо простой работы и эскалацию при
первом material uncertainty.

## Исходное пользовательское требование

- Окончательный выбор primary model/effort остаётся за пользователем.
- Без отдельного profile override genuinely simple packets получают
  `gpt-5.6-luna` с `max`: это дешёвый, но не low-effort lane.
- Большинство packets наследуют current primary profile. В обычном
  пользовательском сценарии это Sol Extra High, но ShipTask не зашивает его как
  универсальный default.
- Для ультрасложного run пользователь может выбрать Sol Ultra как current
  profile; ShipTask не повышает модель до Ultra скрыто или автоматически.
- При первой material ambiguity, непредсказуемом environment/tool state либо
  другой непонятной ситуации Luna останавливается. Тот же packet без повторной
  Luna-попытки принимает основной integration owner на current profile.
- Явное «не используй субагентов» отключает все subagent lanes независимо от
  model policy.

## Контекст

Одинаковая multi-agent topology не требует одинаковой модели во всех lanes.
Стоимость Luna существенно ниже Sol, а высокий effort сохраняет достаточное
качество для простой bounded работы. При этом даже небольшая по объёму задача
может требовать сильного интеллекта из-за неоднозначности, творческого решения,
нестабильного окружения, shared state или высокой цены ошибки.

Обычная эвристика «простая работа — низкий effort» не соответствует выбранному
пользователем quality bar. Предпочтительный дешёвый профиль — именно
`gpt-5.6-luna` с `max`, а не Luna с пониженным effort. Большинство и сложные
packets должны сохранять текущие model/effort основного агента, выбранные
пользователем. Например, это может быть Sol Extra High, а для особо сложного
run — Sol Ultra; примеры не превращаются в зашитый default ShipTask.

## Решение

### Пользовательский выбор первичен

- Текущие model/effort основного агента образуют default profile субагентов.
- Явное указание пользователя о model/effort для всех или отдельных ролей имеет
  приоритет над автоматической классификацией ShipTask.
- Общий `subagents=off` сильнее любой profile policy и означает ноль spawn.
- ShipTask не повышает current profile до Sol Ultra и не заменяет явно выбранный
  профиль молча. Недоступный exact override сообщается как unavailable.

### Luna Max только для genuinely simple packet

Автоматический `gpt-5.6-luna`/`max` допустим, только когда одновременно выполнены
все условия:

- packet self-contained, bounded и имеет disjoint ownership;
- inputs, expected outcome и acceptance достаточно ясны до старта;
- результат объективно и локально проверяем;
- не требуется material creative, product, architectural или cross-task
  judgment;
- нет material production/authority/privacy/security/data-loss risk;
- environment и tool path выглядят обычными и предсказуемыми.

Число строк, файлов или Tasks само по себе не делает packet простым. Внешне
механическая работа с shared evolving state, неоднозначным контрактом или
дорогой ошибкой наследует current model/effort.

Strategic Explainer по умолчанию наследует current profile, поскольку
problem-first user-facing интерпретация требует judgment. Явный profile override
пользователя по-прежнему имеет приоритет.

Model override требует self-contained bounded handoff. Если runtime не может
совместить exact override с ролью, coordinator не подменяет профиль
приблизительным. Он обязан выбрать совместимую bounded форму context; его
собственный выбор incompatible context не делает profile unavailable. Genuine
недоступность auto Luna Max даёт current-profile fallback с
`luna-max=not-available`. Явный user profile не подменяется: сообщается
`<profile>=not-available`, а соответствующая role/capacity считается недоступной.

### Эскалация без Luna retry loop

Luna прекращает packet, если обнаружила хотя бы один material сигнал:

- неоднозначность цели, acceptance или фактов;
- конфликт task contract, context или ownership;
- неожиданное поведение environment, tool или dependency;
- необходимость расширить scope или принять новое решение;
- невозможность уверенно доказать result.

Она не угадывает, не ослабляет acceptance и не делает новых corrective
mutations. Bounded read-only inspection/read-back для точного установления
partial effects и unknown write outcomes остаётся обязательным. Handoff называет
уже выполненное, изменённые surfaces, observed evidence, unknown и точку
остановки. Integration owner reconciles state и сам продолжает packet с текущими
model/effort. Ту же неразрешённую проблему нельзя повторно отправить cheap Luna
lane; это escalation, а не retry. Явное ограничение profile субагентов не меняет
profile основного агента и поэтому не блокирует этот hand-back.

Если current primary сама Luna, replacement Luna subagent не запускается:
integration owner принимает packet с broader context. Если uncertainty остаётся,
он сообщает `luna-escalation=not-available` и не продолжает packet без explicit
stronger-profile override; скрыто подменять user choice на Sol нельзя.

### Наблюдаемость

Если model routing materially повлиял на результат, ShipTask кратко сообщает
использованный profile, недоступный explicit override или Luna-to-current
handoff. Numeric topology accounting и полный profile ledger не требуются. Эти
сведения не заменяют result evidence и не превращаются в process diary.

## Проверяемые признаки

- Ясный bounded packet без material judgment получает Luna Max, если
  пользователь не выбрал иной профиль.
- Неоднозначный, связанный, risky или creative packet сразу наследует current
  model/effort.
- После material uncertainty Luna останавливается, а тот же packet продолжает
  integration owner/current profile без повторного Luna loop.
- Coordinator не создаёт profile unavailability выбором incompatible context, а
  явно выбранный unavailable profile не заменяет молча.
- Явный model/effort пользователя соблюдён, а общий no-subagent prompt запускает
  ноль субагентов.
- Acceptance, authority и integration ownership не меняются из-за выбранной
  модели.

## Последствия

- Дешёвая capacity используется там, где простота доказуема, без снижения effort.
- Сложность и непредвиденное поведение быстро возвращаются current integration
  owner; более сильная модель появляется только когда current profile сильнее.
- ShipTask остаётся переносимым между пользовательскими primary profiles и не
  зашивает Sol Extra High или Sol Ultra как универсальный default.
