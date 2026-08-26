# 0023. Task Composer как planning sibling-skill

Статус: accepted, 2026-08-22. Первоначально расширял состав отдельного
`ship-tasks@srez-marketplace`, первоначально заданный
[ADR-0011](0011-separate-shiptask-plugin-distribution.md) и
[ADR-0012](0012-strategic-explainer-as-portable-subagent-role.md). Совместная
упаковка Strategic Explainer заменена
[ADR-0031](0031-standalone-strategic-explainer-plugin.md); Task Composer остаётся
в ShipTask plugin.

## Контекст

Task Manager adapter умеет безопасно создавать Tasks, hierarchy, Labels и
relations, но намеренно не определяет business-правила качественной постановки.
ShipTask начинает delivery уже выбранного scope и не должен превращать каждую
просьбу добавить работу в backlog в implementation run. Strategic Explainer
помогает раскрыть problem и смысл, но остаётся read-only и не владеет
decomposition или Task Manager writes.

Нужен отдельный workflow между человеческим требованием и delivery: он должен
выбирать одну Task либо Epic, сохранять стратегический смысл на уровне Epic,
переносить tactical details в подзадачи и создавать согласованный planning
graph в Task Manager.

## Решение

- Добавить sibling-skill `task-composer` в репозиторий ShipTask и тот же plugin
  `ship-tasks@srez-marketplace`.
- Разрешить explicit invocation и implicit routing для формулировки,
  декомпозиции и planning/backlog capture с Task Manager intent.
- Оставить Task Composer planning-only: он не реализует, не выпускает, не
  принимает созданную работу, не создаёт Goal и не выводит Tasks из `Backlog`.
- Использовать `$ship-tasks:strategic-explainer` для problem-first описания
  каждого Epic, сохраняя за Task Composer решения о scope, decomposition,
  metadata и writes.
- Считать parent Task с несколькими independently deliverable children Epic;
  не вводить отдельный скрытый task type или формальный Epic для одной Task.
- Назначать только live existing Labels. Если подходящего Label нет, создавать
  Task без него и сообщать taxonomy gap; автоматически taxonomy не расширять.
- Назначать однозначный current или explicit Release. Неизвестный Release не
  блокирует create и не заменяется guess.
- Создавать native hierarchy и только semantic relations; duplicate search и
  post-write read-back обязательны для целостности planning projection.
- Task Manager plugin остаётся adapter-only и не получает Task Composer.

## Последствия

- Planning capture и delivery получают разные routing и authority boundaries.
- Epic остаётся понятным человеку, а подзадачи — исполнимыми и проверяемыми.
- Одна установка Ship Tasks предоставляет композицию, delivery и общий
  Strategic Explainer, но Task Manager connector по-прежнему устанавливается
  отдельно.
- Missing Release или Label не маскируется выдуманным ref; пользователю виден
  точный metadata gap.
- Multi-Task create не становится транзакционным: частичный outcome требует
  reconciliation и явного handoff, а не автоматического destructive cleanup.
