# Обзор ShipTask

## Назначение

`$ship-tasks` — явно вызываемый универсальный workflow для доставки уже
определённого task scope. Skill отвечает за способ выполнения: read-only
preflight, authority, dependencies, изоляцию параллельных lanes, интеграцию,
verification, внешние эффекты и честное terminal evidence.

Конкретные задачи, команды, ветки, task manager, environments и права
определяются текущим project context. Если критичный факт нельзя установить
достоверно, skill обязан остановиться с `TASK CONTEXT ALARM` до первой
мутации.

## Текущий статус

- `ship-tasks/SKILL.md` — текущий исполнимый baseline v1.
- [Ship Tasks v2](specs/ship-tasks-v2.md) — proposal, а не реализованный
  runtime contract.
- Cross-session scheduler, durable review queue и provider adapters пока не
  реализованы.
- User-level установленная копия существует отдельно и не синхронизируется с
  репозиторием автоматически.

## Происхождение

Репозиторий создан после сессии Codex
`00000000-0000-4000-8000-3bd4623c02c1`. В ней repo-local
`ship-linear-release` сначала был обобщён и переименован в `ship-tasks`, а
затем сопоставлен с идеями управления человеческой review-нагрузкой.

Документация предыдущего поколения была изучена в ExampleNotes. Универсальные
инварианты перенесены в этот проект, а Linear, Sites/UAT, ветка `main`,
ExampleNotes commands и запрет production оставлены за пределами runtime skill.
Точная карта источников находится в
[reference-документе](reference/minddiary-predecessor.md).

## Целевой продуктовый поток

```text
user planning
→ dependency-ready execution
→ deterministic verification
→ independent agent review
→ bounded review-ready queue
→ human acceptance
→ integration/external effects
→ terminal evidence
```

Главная цель v2 — не заменить человеческую приёмку, а уменьшить число
обращений к пользователю и стоимость каждого переключения контекста.

## Границы

- Skill не создаёт scope из неопределённого пожелания.
- Skill не получает внешние полномочия из одного факта invocation.
- Skill не навязывает Git, tracker, workers или deployment проекту, где они
  неприменимы.
- Skill не превращает failed check в разрешение на unrelated cleanup.
- Skill не называет plan, worker report, commit, test или deploy достаточным
  доказательством completion другого слоя.
