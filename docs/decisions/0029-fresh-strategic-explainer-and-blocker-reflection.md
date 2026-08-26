# 0029. Fresh Strategic Explainer и reflection до blocker

Статус: accepted, 2026-08-26. Уточняет ADR-0012, ADR-0014, ADR-0021 и
ADR-0022. Канонические current requirements остаются в локальных source packages
[Strategic Explainer](../skills/strategic-explainer/requirements.md),
[ShipTask](../skills/ship-tasks/requirements.md) и
[Task Composer](../skills/task-composer/requirements.md).

## Контекст

Explainer должен находить главную причинную мысль независимо от tactical framing
caller-а. Передача предыдущего диалога, tool transcript, process diary, готового
вывода или прежнего candidate заставляет его повторять язык исполнителя и
добавлять лишнюю информацию. Одновременно слишком полный handoff выполняет
стратегическую работу за Explainer и не даёт ему самостоятельно подняться от
локальной задачи к Epic, Release, Project и исходному outcome.

Для blocker report независимый взгляд имеет ещё одну функцию. Если ShipTask
записал ситуацию обычными словами и увидел более общий смысл, он может обнаружить
пропущенный безопасный способ продолжить. Предварительно принятое решение о
блокировке поэтому не должно становиться terminal claim до такой проверки.

## Решение

### Один stateless API

- Direct и delegated use Strategic Explainer имеют один contract.
- Каждый самостоятельный user-facing publication unit получает нового built-in
  `default` subagent с `fork_turns="none"`.
- Caller передаёт одну короткую однозначную задачу, exact scope и resolvable
  read-only anchors. Inherited turns, tool transcript, process diary, caller
  rationale и прежний candidate запрещены.
- Explainer проверяет доступные признаки invocation до discovery. Invalid context
  получает короткий отказ с причиной и способом исправления; caller создаёт
  новый clean invocation, а не продолжает старый.
- Routine chat, progress commentary и внутренний draft не являются publication
  units. Новый Task comment/report, blocker explanation, final, changed facts или
  новый вопрос получают новый invocation.

### Самостоятельное исследование и короткий result

- После admission Explainer сам собирает current facts read-only способом и
  поднимается от exact target через применимые Task/parent/Epic, Release,
  Project, product goal, vision/specification и accepted decisions.
- Поиск останавливается, когда более высокий source не меняет problem, outcome,
  impact/risk, action или confidence. Strategic context не расширяет scope и не
  заменяет execution evidence.
- Первый result layer выражает одну главную причинную мысль и по возможности
  исчерпывает ответ одной фразой. Второй короткий слой появляется только для
  material cause, action, success signal или проверяемой опоры.

### Blocker reflection

- До окончательного blocker claim ShipTask получает fresh candidate explanation
  и читает его/source basis как independent reflection input.
- ShipTask повторно проверяет primary/cascade cause, исходную цель, применимый
  strategic context и безопасную in-scope frontier. Explainer не решает status,
  recovery, scope или authority и не является evidence.
- Найденный путь проверяется по current primary sources и acceptance. Если он
  достаточен и разрешён, blocker не публикуется и работа продолжается; следующий
  user-facing result создаётся новым Explainer.
- Если material incident должен стать видимым немедленно, отдельный fresh
  message сообщает установленный incident и продолжающуюся проверку без
  преждевременного terminal blocker claim.
- Для unchanged blocker state выполняется один reflection pass. Повтор возможен
  после material change либо исправления invalid invocation, но не ради новых
  вариантов wording.

## Последствия

- Clean invocation и retry становятся явными пользовательскими invariants, а не
  свободной implementation detail ADR-0021.
- Strategic Explainer остаётся generic и read-only; ShipTask и Task Composer
  хранят собственные caller obligations в локальных source packages.
- Latency увеличивается только на реальные publication units и candidate blocker
  reflection, а не на routine communication.
- Publication-ready blocker text может быть отброшен после reflection. Это не
  потерянный result: он предотвратил ложную terminal остановку.
