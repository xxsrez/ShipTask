# 0002. Managed delivery report внутри Task

Статус: superseded by
[ADR-0003](0003-delivery-reports-as-task-comments.md), 2026-08-16.

## Контекст

Пользователю нужен долговечный, человекочитаемый отчёт прямо в каждой
выполненной Task: при success — объяснение результата и устройства feature, при
material failure — понятное описание impact, причины, recovery и remaining
risk. Review packet только в chat не остаётся рядом с Task.

Current Task Manager connector не предоставляет append-only comments или
отдельный report resource, но `update_task` умеет атомарно менять `description`
и status с optimistic `version`. Поле принимает до 100 000 characters. Current
UI показывает description как plain text/textarea с сохранением line breaks;
Markdown и Mermaid там не рендерятся.

В предыдущем ShipTask analysis уже был предложен task-type-aware decision
surface: outcome, exact identity, acceptance evidence, impact map, risks и
короткий human path вместо сырого worker log. Это решение делает такой report
частью current runtime contract.

## Решение

Это решение описывает прежний runtime contract и сохранено как история.
Текущий contract определён ADR-0003: delivery report не записывается в
`description` и публикуется только через native Task comments, когда эта
capability доступна.

- Хранить в `description` каждой выполненной in-scope Task ровно один видимый
  managed delivery-report block с точными start/end sentinels.
- Сохранять исходный user-authored description без изменений; append для первого
  report, replace-in-place для rework и completion. Не вести append-only журнал.
- Писать `ACCEPTANCE READY` report после passing exact batch gate, material
  failure report при reopen/blocker и финальный `COMPLETED` report вместе с
  переходом в `Done`, когда current tool позволяет один atomic update.
- Считать report обязательным evidence surface: failed/missing/unverified write
  удерживает Task и Goal незавершёнными.
- Использовать plain-text-first format. Для non-trivial feature или incident
  включать одну-две содержательные text diagrams; для trivial change выбирать
  compact before/after вместо декоративной схемы.
- Адаптировать report к task type. Success объясняет user outcome, main flow,
  implementation decisions, evidence и limitations. Material failure объясняет
  impact, detection, trigger/root cause с confidence, recovery, prevention и
  remaining risk.
- Писать blameless, отделять evidence от inference, не вставлять raw logs и не
  создавать follow-up Tasks без отдельной authority.

Этот historical contract больше не является runtime format. Текущий reference
по ссылке из ADR-0003 описывает comments-only поведение.

## Рассмотренные варианты

### Только review packet в chat

Отклонён: report теряется отдельно от canonical Task и плохо поддерживает
возврат к решению после сессии.

### Append-only история в description

Отклонена: быстро раздувает поле, смешивает исходные requirements с execution
log и делает актуальное состояние трудно различимым.

### Markdown/Mermaid report

Не принят как current baseline: Task Manager сейчас показывает plain text.
Mermaid остаётся возможной будущей опцией только после проверки реального
renderer support. Text diagrams сохраняют читаемость в текущем UI.

### Отдельный report/comment resource

Предпочтительнее как future product capability, но сейчас отсутствует в
connector. При его появлении потребуется отдельное решение о migration; skill
не должен изображать эту capability заранее.

## Последствия

Положительные:

- acceptance и последующая диагностика видят explanation рядом с Task;
- один replaceable block остаётся idempotent и не превращает description в log;
- failure report нацелен на impact и prevention, а не на оправдание агента;
- plain-text diagrams работают в текущем UI без дополнительного renderer.

Ограничения:

- description становится совместным user/ShipTask storage и требует строгого
  preservation/concurrency contract;
- report нельзя безопасно записать при malformed markers, field overflow или
  отсутствии write authority — это блокирует terminal transition;
- rich visual assets, rendered Mermaid и append-only discussion остаются вне
  текущих capabilities.

## Основания формата

- [Google SRE: Postmortem Culture](https://sre.google/workbook/postmortem-culture/)
  — impact, root-cause depth, concrete action items и blameless writing.
- [C4 model: Diagrams](https://c4model.com/diagrams) — выбирать только уровень
  diagram, который действительно добавляет ценность читателю.
- [Mermaid flowcharts](https://mermaid.js.org/syntax/flowchart) — возможный
  text-defined rich renderer после появления и проверки поддержки в Task
  Manager, но не current storage baseline.
