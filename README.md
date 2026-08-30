# Issue Grinder / ShipTask

Репозиторий содержит current Task Manager delivery skill `$issue-grinder`,
planning-only `$issue-grinder:task-composer`, общий
`$strategic-explainer:strategic-explainer` и legacy source `$ship-tasks`.
Issue Grinder доводит выбранный scope из `To Do`, `In Progress`, `In Review` до
проверенного результата либо, только в `Экономичном` режиме, до честной
возобновляемой контрольной точки. Он создаёт стратегический Goal только для явно
вызванного multi-issue run и использует blocker explanation как обязательную
reflection-точку для автоматического продолжения. Если пути вперёд нет, общий blocker-report
перечисляет все причины, а отдельный ответ по каждой из них объясняет её влияние на
цель, границу самостоятельного устранения и ценность заблокированного шага.

Legacy ShipTask — skill `$ship-tasks`, который через Task Manager
доводит выбранные Tasks, Project или Release до проверенного terminal outcome
при явном invocation и по natural-language delivery intent с однозначным Task
Manager anchor. Один delivery verb или обычная просьба исправить код/продукт/
plugin без такого anchor ShipTask не активирует. Составная команда явно создать
ровно одну Task в Task Manager и сразу выполнить её запускает `single`, а не
backlog capture. Exact одна Task работает в `single` mode без Goal. Goal нужен
только для `batch-implementation`, когда один run реально имплементирует или
возвращает в rework минимум две concrete Tasks. Project/Release/current scope и
bare `$ship-tasks` — только selectors: mode определяется по live inventory.
Release уже подготовленного candidate, включая production, работает без Goal.
Exact Task/явный список refs образуют закрытый selector. Project, Release и
current scope остаются live selectors: стартовый inventory не замораживает
membership, поэтому новая matching non-Backlog Task автоматически входит в run
без повторного approval, а Backlog остаётся вне delivery.
`blocked by` управляет доступностью реализации, а не terminal lifecycle:
dependent Task становится runnable после подтверждённого fan-in нужного upstream
contract в exact integration candidate, даже если blocking Task ещё не `Done`
из-за собственной проверки. Relation и attribution сохраняются; поздний defect
инвалидирует только доказанно затронутые downstream results.

Документация здесь является исходным кодом. Общая модель и разделение
ответственности заданы в [философии проекта](docs/philosophy.md), а source unit —
отдельная entity. В [`docs/skills/<skill>/`](docs/skills/README.md) у неё есть
три независимых source-документа: user-owned `overview.md`, user-owned
`requirements.md` и agent-owned `architecture.md`. Документы четырёх skills не
объединяются. Runtime является компактной стохастической компиляцией локального
source package. Strategic Explainer предоставляет
semantic facade: callers передают только назначение, scope и source anchors,
facade владеет invocation/admission, а provider expertise находится в reference,
который читает только admitted fresh subagent. Удаление и повторная сборка
runtime из source package должны давать примерно эквивалентный по смыслу package.

Current requirements являются конституцией для агентов: они задают outcome,
rationale, observable evidence и authority/safety boundaries, но оставляют
агенту план, декомпозицию, инструменты и внутренний reasoning. Ordinary
Strategic Explainer сохраняет fresh stateless API, но callers видят только
semantic request/result contract; всё внутреннее исполнение принадлежит facade
и не повторяется в вызывающих skills. Другое исключение — execution topology: без явного user
rule ShipTask сам решает, где
субагенты дают реальную пользу, сохраняя одного integration owner. Пользователь
может свободным языком задать exact/relative count, role scope, общий или узкий
запрет и условие вроде «используй субагентов только для работы дольше получаса»;
coordinator обязан сохранить смысл правила, а не вернуть topology к default.
Root agent не входит в явно названное число субагентов. Каждый одновременно
пишущий implementation subagent получает отдельные feature branch и Git
worktree; read-only роли могут работать без worktree.

Current Issue Grinder имеет пять режимов: `Соло`, `Классический`, `Баланс`,
`Рой` и `Экономичный`. `Соло` последовательно выполняет любой scope текущей
моделью без subagents и отдельного Strategic Explainer. Явный выбор свободным
языком сильнее автоматики; иначе любая
top-level Luna выбирает `Экономичный`, а другая модель — `Классический`.
Resolver срабатывает один раз, и смена модели внутри того же run режим не
меняет; один issue сам по себе не выбирает `Соло`. В `Классическом` Luna Max получает только strict-simple packets,
`Баланс` переносит на неё основную массу ограниченной работы, `Рой` разрешает
изолированные конкурирующие волны, а `Экономичный` может оставить один
непринятый resumable candidate без ложного `Done` или blocker-а.

После ошибки или смены Codex-сессии ShipTask сначала ищет существующий
task-owned checkpoint. Если прежний writer остановлен, незавершённый worktree и
feature branch безопасно переходят новому exclusive owner, и работа продолжается
там, а не начинается с нуля; active или ambiguous ownership не перехватывается.
Профили Issue Grinder нормализуются отдельно от режима: Luna любого effort
схлопывает содержательные controller и worker roles в Luna Max; более сильный
main profile остаётся controller/reviewer, а Luna Max — экономичным worker.
Неизвестное отношение разных семейств не угадывается, а явный role profile
пользователя имеет приоритет. Перед любым существенным status transition сначала
публикуется и перечитывается понятный native Task comment; обычный старт
`To Do → In Progress` комментария не создаёт. Task description и ответ в Codex
комментарий не заменяют. Native comments являются гарантированной частью Task
Manager adapter и всегда используются для material lifecycle reporting.
Если host показывает title capability и ShipTask доказанно является первым
вызовом новой Codex task с catalog placeholder, после live scope resolution
выполняется не более одной best-effort попытки задать имя `ShipTask · ...`;
существующее meaningful название не перезаписывается, а отсутствие или failure
capability не блокируют delivery.

Для каждого comment, Task/scope report, blocker explanation и final ShipTask
использует один communication mode. Live catalog выбирает ordinary
`$strategic-explainer:strategic-explainer`, если он доступен и разрешён, иначе
native ShipTask writing. Ordinary получает terminal clean provider-subagent.
Callers знают только semantic request/result contract и не получают ни recipe
запуска, ни методику улучшения текста; её читает только provider-subagent.
Provider failure переводит run в native. Native не имитирует provider method и
не блокирует comment/status. Routine chat и progress updates publication unit
не создают.

Приёмочный incident сообщается сразу в chat и сохраняется в Task history до
начала repair. Opening comment остаётся видимым после исправления, resolution
comment содержит повторную проверку, а final run report перечисляет material
incidents, включая найденные и исправленные в том же run. Пока incident
unresolved, активный run регулярно напоминает о нём без дублирования Task
comments. Только прямое нарушение acceptance называется bug; невозможность
получить evidence называется verification blocker.

Агент сам выбирает инструменты, способ диагностики и
приёмки; сбой одного средства не навязывает его repair. Acceptance не ослабляется
ради удобства, а непроверенное не называется verified. Единственный явный
fallback — `critical-codebase-accepted`: после fresh inventory без `To Do` и
`In Progress`, когда все оставшиеся `In Review` требуют существенного human
verifier, один fresh-context critic независимо проверяет exact candidate,
code/tests. Grounded approval разрешает weaker `Done` только с обязательным
Strategic Explainer comment о непроведённой functional check и residual risk.
Browser switch допустим как диагностика, но не как repair или причина
отложить уже доказанный product failure, пока безопасная in-scope работа над
продуктом может продолжаться.
До окончательного blocker claim ShipTask перечитывает новый Explainer result как
reflection input и заново проверяет safe frontier. Найденный путь не
принимается на веру: он подтверждается current sources/acceptance; при достаточном
пути stale blocker не публикуется и работа продолжается.
Перед завершением skill сверяет обещанный и фактический результат,
самостоятельно устраняет доступные проблемы внутри выбранной работы и только
затем проводит final publication unit через выбранный Strategic Explainer.
Основной агент проверяет material facts и не переписывает ready text. Если
правило отключает Explainer, caller сообщает обязательные lifecycle
facts по собственному contract без provider method. Explainer не выбирает
статус, полномочия или действие и ничего не меняет; общий router можно
использовать отдельно от ShipTask.
Старые memory, rollout или report записи о ручной приёмке не меняют этот
contract: обычный terminal-ready result закрывается автоматически, а существенная
human verification dependency проходит только строгий critical fallback либо
остаётся честно незавершённой.
Task-local вопросы откладывают только конкретную Task, не прерывая остальные;
для каждой Task делается лёгкий targeted gate, а совместимые изменения
периодически выпускаются в UAT одним exact batch без отдельного approval;
non-production releases выполняются автоматически, а production требует явного
разрешения пользователя. Goal массовой имплементации остаётся активным, пока в
его границе есть незавершённая работа; сам release не создаёт Goal. Project
memory хранит только selectors/profile и изменяется лишь по явной просьбе.

Task Composer закрывает соседний planning-only этап: формулирует одну Task либо
Epic с problem-first описанием через Strategic Explainer, конкретными
подзадачами, live Labels и semantic relations, сохраняя применимый strategic
context в каждой child Task. При delivery ShipTask перечитывает current Epic,
но его смысл не расширяет exact child scope. Созданные элементы остаются в
`Backlog`; неизвестный current Release не угадывается и не блокирует создание.

## Структура

- [`issue-grinder/SKILL.md`](issue-grinder/SKILL.md) — current delivery skill.
- [`ship-tasks/SKILL.md`](ship-tasks/SKILL.md) — исполнимый skill.
- [`task-composer/SKILL.md`](task-composer/SKILL.md) — planning-only
  формулировка, декомпозиция и создание Task Manager scope.
- [`strategic-explainer/SKILL.md`](strategic-explainer/SKILL.md) — общий
  semantic facade и deterministic role resolver; terminal provider проходит
  отдельный provider-only admission и только затем загружает внутренний
  text-improvement contract.
- [`docs/skills/README.md`](docs/skills/README.md) — source model и независимые
  Overview/Requirements/Architecture packages для каждого skill; Overview
  появляется только после явного определения пользователем.
- [`docs/skills/issue-grinder/requirements.md`](docs/skills/issue-grinder/requirements.md)
  и [Architecture](docs/skills/issue-grinder/architecture.md) — source
  `$issue-grinder`; [Evaluation](docs/skills/issue-grinder/evaluation.md) хранит
  точную трассировку и быстрый сценарный корпус.
- [`docs/skills/ship-tasks/requirements.md`](docs/skills/ship-tasks/requirements.md)
  и [Architecture](docs/skills/ship-tasks/architecture.md) — source `$ship-tasks`.
- [`docs/skills/task-composer/requirements.md`](docs/skills/task-composer/requirements.md)
  и [Architecture](docs/skills/task-composer/architecture.md) — source Task Composer.
- [`docs/skills/strategic-explainer/overview.md`](docs/skills/strategic-explainer/overview.md),
  [Requirements](docs/skills/strategic-explainer/requirements.md) и
  [Architecture](docs/skills/strategic-explainer/architecture.md) — source
  Strategic Explainer.
- [`ship-tasks/references/project-memory.md`](ship-tasks/references/project-memory.md)
  — runtime contract project scope/profile memory.
- [Документация](docs/README.md) — канонические specifications, Task Manager
  adapter reference, architecture decisions и engineering reports.
- [`scripts/validate_repo.py`](scripts/validate_repo.py) — переносимая
  проверка структуры и project-specific residue.

## Проверка

```bash
python3 scripts/validate_repo.py
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py issue-grinder
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py task-composer
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Current runtime публикуется двумя установленными независимыми plugin:
`issue-grinder@srez-marketplace` содержит Issue Grinder и Task Composer, а
`strategic-explainer@srez-marketplace` — только ordinary Strategic Explainer.
Task Manager connector устанавливается отдельно как adapter-only
`task-manager@srez-marketplace`. Legacy `ship-tasks@srez-marketplace` остаётся
доступным как неустановленный rollback artifact и не устанавливается вместе с
Issue Grinder. Codex manifest не умеет автоматически устанавливать plugin
dependency, поэтому Issue Grinder выбирает ordinary при его наличии и
разрешении, иначе native; Task Composer использует ordinary. Standalone каталоги
`~/.codex/skills/issue-grinder`, `~/.codex/skills/ship-tasks`, `~/.codex/skills/task-composer` и
`~/.codex/skills/strategic-explainer` не устанавливаются: они создают вторые
logical skills рядом с plugin-qualified runtime. Каждый repository source
сверяется со своим Marketplace package и installed plugin cache.
