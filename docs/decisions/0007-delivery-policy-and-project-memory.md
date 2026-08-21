# 0007: Delivery policy и project memory принадлежат ShipTask

Статус: accepted. Дата: 2026-08-16.

Классификация `Project`/`Release`/bare scope как автоматического `batch` и
обязательный Goal для такого selector заменены
[ADR-0019](0019-goal-only-for-multi-task-implementation.md). Остальные routing и
project-memory boundaries сохраняются.

Формулировка о загрузке user-level skill в последствиях ниже заменена
[ADR-0011](0011-separate-shiptask-plugin-distribution.md). Runtime ShipTask
распространяется отдельным plugin рядом с adapter-only Task Manager plugin.

Уточнение 2026-08-18: implicit invocation требует однозначного Task Manager
delivery anchor; один delivery verb не активирует ShipTask.

## Контекст

Task Manager connector должен оставаться техническим адаптером: подключение,
canonical refs, чтение и запись Tasks, pagination, optimistic concurrency и
read-back. Одновременно delivery workflow должен одинаково работать как при
явном `$ship-tasks`, так и при естественной формулировке вроде «выполни
TM-123» или «доведи выбранный Task Manager release».

Project-specific значения нельзя зашивать ни в adapter, ни в переносимый
delivery skill. Они различаются между проектами и меняются независимо от
общего workflow.

## Решение

Разделить систему на три слоя:

```text
Task Manager skill  -> технический adapter и live task state
ShipTask skill      -> intent routing и business delivery policy
Project Memories    -> current scope и project-specific profile
```

ShipTask активируется явно и неявно. Явный `$ship-tasks` достаточен сам по себе.
Implicit invocation требует одновременно delivery intent и однозначный Task
Manager anchor в текущем запросе/выбранном context: exact существующую Task,
выбранный Task Manager Project/Release/current scope либо явную просьбу создать
ровно одну Task именно в Task Manager и сразу начать её выполнение. Обычная
просьба исправить продукт, код, repository или plugin не проходит этот gate.
Project memory и adapter lookup разрешают уже выбранный scope, но не создают
implicit anchor задним числом. После gate ShipTask классифицирует запрос до
любых мутаций:

- `single` — ровно одна canonical Task; Goal не создаётся. Task может быть
  разрешена из live state либо ровно один раз создана составным
  explicit Task Manager `create-and-deliver` intent и немедленно продолжена в
  том же flow;
- `batch` — Project, Release, несколько Tasks или bare `$ship-tasks`; Goal
  обязателен;
- `memory-maintenance` — явное оформление или обновление project memory;
- `non-delivery` — чтение, статус, планирование и backlog capture. Команда только
  создать/запланировать Task относится сюда; сочетание создания с явным
  execution intent относится к `single`.

Текущий exact selector из запроса имеет приоритет над memory. Bare
`$ship-tasks` берёт `current_scope` из project memory. Memories содержат только
selectors и project profile; Task Manager остаётся authority для текущих
status, version, detail, relations и access.

ShipTask пишет memory только по явной просьбе пользователя. Он может предложить
или оформить context по своей схеме, но delivery-run не меняет memory молча. Отсутствующий,
неоднозначный, устаревший или противоречивый обязательный context до mutation
даёт `TASK CONTEXT ALARM`.

## Последствия

- Natural-language delivery получает ту же policy, что и явный invocation.
- Delivery verbs без Task Manager anchor остаются обычными code/product/plugin
  запросами и не запускают memory lookup, connector discovery или Goal flow.
- Batch остаётся предсказуемым повторяемым сценарием с Goal, а single-task
  delivery не требует orchestration Goal.
- Project memory упрощает выбор scope, но никогда не заменяет live discovery.
- Runtime `SKILL.md` остаётся компактным; схема и процедуры memory вынесены в
  отдельный reference.
- Task Manager skill должен быть сокращён до adapter-only contract отдельным
  согласованным изменением. До этого ShipTask сохраняет минимальные safety
  invariants adapter-вызовов и глобальный routing направляет delivery intent в
  ShipTask.
- Изменения user-level skill и routing становятся видимы только в новой
  сессии, потому что доступные skills и `AGENTS.md` загружаются при старте.

## Не принято

- Хранить business flow в Task Manager skill: это смешивает transport и policy.
- Хранить project-specific refs в ShipTask: это ломает переносимость.
- Использовать Memories как authoritative task database: сохранённый state
  может устареть и не поддерживает безопасные writes.
- Создавать Goal для каждой одиночной Task: это добавляет lifecycle без пользы
  для короткого exact-scope flow.
