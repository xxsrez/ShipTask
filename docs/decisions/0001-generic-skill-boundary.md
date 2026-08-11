# 0001. Универсальный skill без project-specific adapters

Статус: accepted, 2026-08-11.

## Контекст

Repo-local ExampleNotes skill связывал delivery workflow с Linear milestone,
`main`, Sites/UAT, конкретными helpers и project release policy. После
переноса в user scope такое поведение создавало ложные предположения в других
проектах и collision с одноимённым локальным skill.

## Решение

- Использовать имя и explicit trigger `ship-tasks`.
- Оставить в runtime skill только общие execution invariants.
- Получать tasks, acceptance, commands, integration policy, external targets и
  authority из текущего project context.
- Останавливаться с `TASK CONTEXT ALARM`, если критичный факт нельзя
  достоверно установить read-only.
- Хранить provider adapters, project profiles и durable runtime отдельно от
  универсального skill.
- Запретить implicit invocation.

## Последствия

Положительные:

- один skill применим к проектам без Linear, Git или deployment;
- проектные permissions и production policy не протекают между репозиториями;
- collision со старым repo-local именем устранён;
- новые adapters можно развивать независимо от core contract.

Отрицательные:

- skill зависит от качества project context;
- без profile/runtime часть проверок остаётся процедурной, а не машинной;
- установленная user-level копия требует отдельной синхронизации;
- долговременная review queue не может надёжно жить только в Markdown skill.
