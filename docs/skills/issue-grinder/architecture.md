# Issue Grinder: архитектура

Статус: current Level 2, 2026-08-28. Применимые Level 1 requirements — `IG-*`
в локальных [требованиях пользователя](requirements.md).

Этот документ описывает одно текущее инженерное решение для `$issue-grinder`.
Он является agent-owned: его можно уточнять без изменения Level 1, пока
обязательный результат и пользовательские границы сохраняются. При конфликте
всегда побеждает `requirements.md`.

## 0. Compilation contract

Локальные `requirements.md` и `architecture.md` вместе образуют полный current
source package `$issue-grinder`. Будущий runtime skill должен стать их
компактной смысловой проекцией: удаление runtime и повторная сборка только из
этих двух документов должны давать примерно эквивалентное наблюдаемое
поведение.

Runtime `$issue-grinder` создан в repository как Level 3 compilation. Этот
факт сам по себе ещё не утверждает, что Marketplace package опубликован,
установлен или проверен в fresh Codex session.

## 1. Runtime package и distribution

### 1.1 Минимальная форма plugin

`$issue-grinder` поставляется отдельным plugin `issue-grinder`. Plugin содержит
два независимых runtime skill: одноимённый delivery coordinator и канонический
planning-only `task-composer`. Общий distribution artifact не смешивает их
Requirements: Task Composer сохраняет собственный source package, boundary и
runtime source, но после cutover остаётся доступен без установки старого
ShipTask.

Marketplace package имеет минимальную форму:

```text
plugins/issue-grinder/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    ├── issue-grinder/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── references/
            ├── task-manager-flow.md
            ├── autonomy-and-environments.md
            ├── multi-agent-execution.md
            └── strategic-explainer.md
    └── task-composer/
        ├── SKILL.md
        └── agents/openai.yaml
```

Plugin не содержит собственный MCP server, UI, assets, hooks или runtime
scripts в первой версии. Task Manager уже предоставляет live data,
authentication, authorization и controlled mutations; Issue Grinder остаётся
workflow- и orchestration-слоем вокруг этого adapter-а.

Такая форма следует принципу минимального plugin из
[официальной архитектуры OpenAI](https://developers.openai.com/plugins/concepts/plugins):
plugin может содержать только skills, а MCP server, UI и lifecycle extensions
добавляются позднее без изменения его назначения.

### 1.2 Внутреннее устройство skill

`SKILL.md` остаётся компактным исполнимым entrypoint. В нём находятся:

- trigger и граница между явным и неявным invocation;
- стратегический смысл и обязательные terminal conditions;
- основной scope/Goal/delivery loop;
- routing к условным references;
- жёсткие authority и truth boundaries, которые нельзя потерять при
  progressive disclosure.

Подробности загружаются только тогда, когда меняют текущие решения:

- `task-manager-flow.md` — live scope, lifecycle, blocked-by, comment/status
  transaction, read-back и recovery;
- `autonomy-and-environments.md` — только для явно вызванного автономного run и
  действий со средами;
- `multi-agent-execution.md` — только когда существует полезная независимая
  работа или явное topology rule пользователя;
- `strategic-explainer.md` — перед comment, blocker-report или финальным
  пользовательским текстом.

Reference не создаёт собственную политику и не становится параллельным
Requirements или Architecture. Весь применимый смысл `IG-*` должен оставаться
восстановимым из `SKILL.md` и адресно подключаемых references. Такой способ
разделения соответствует
[официальной модели skills](https://developers.openai.com/plugins/build/skills),
где `SKILL.md` задаёт workflow, а supporting resources выносят только нужную
условную детализацию.

### 1.3 Metadata, activation и внешние зависимости

`agents/openai.yaml` задаёт:

- `display_name: Issue Grinder` и короткое описание доставки Task Manager
  scope до terminal результата;
- `allow_implicit_invocation: true`, потому что архитектура различает
  автоматическую загрузку и явный `$issue-grinder`;
- MCP dependency `task-manager` с `streamable_http` transport;
- default prompt, который объясняет выбранный scope, но не подменяет текущий
  пользовательский prompt.

Skill description должна привлекать запросы реализовать, исправить, проверить
или доставить существующий Task Manager scope. Read/status/audit и
planning-only запросы не должны маршрутизироваться в Issue Grinder.

Task Manager остаётся отдельно установленным adapter plugin и не копируется в
Issue Grinder package. Task Composer копируется только из канонического
repository source `task-composer/`; его planning-only lifecycle не расширяется
правами Issue Grinder. Strategic Explainer также остаётся отдельным plugin:
при доступности вызывается его semantic facade, при отсутствии применяется
native writing по `IG-FLOW-03`. Жёсткая plugin-to-plugin dependency для него не
моделируется.

### 1.4 Почему в первой версии нет scripts и hooks

Runtime script добавляется только для повторяемой детерминированной операции,
которую существующие tools и инструкции не выполняют надёжно. Scope resolution,
Goal, lifecycle, verification, reflection и multi-agent dispatch зависят от
живого контекста и остаются решениями coordinator-а. Выносить их во второй
скрытый orchestration engine нельзя.

Build- и evaluation-скрипты допустимы на уровне repository: semantic coverage
Level 1/Level 2, behavioural scenarios, сборка Marketplace package и проверка
byte identity. Они проверяют runtime, но не участвуют в пользовательском run и
не входят в skill только ради удобства разработки.

Hooks являются plugin/Codex lifecycle-механизмом, а не внутренним шагом skill.
Они могут выполняться вместе с hooks из других источников, требуют отдельного
trust review и срабатывают по общим lifecycle events. Поэтому основной цикл,
Production boundary, Goal completion и blocker reflection не реализуются через
hooks. Plugin-bundled hook появится только после доказанного случая чисто
механического cross-cutting инварианта, который нельзя надёжно обеспечить
обычным skill workflow. Текущая архитектура такого случая не содержит. Это
соответствует [официальной модели Codex hooks](https://learn.chatgpt.com/docs/hooks).

### 1.5 Repository source и установка

Когда начнётся runtime implementation, канонический source появится в этом
repository:

```text
issue-grinder/
├── SKILL.md
├── agents/openai.yaml
└── references/...
```

После проверки `issue-grinder/` и `task-composer/` копируются в отдельный
Marketplace plugin соответственно как `skills/issue-grinder/` и
`skills/task-composer/`. Каждая пара repository source, Marketplace source и
installed cache должна быть byte-identical. Изменение runtime payload требует
новой manifest version, публикации Marketplace commit, переустановки plugin и
проверки свежего snapshot в новой Codex-сессии.

Standalone user-level duplicate не создаётся. Source package документации,
runtime source, Marketplace package и installed cache имеют разные роли и не
смешиваются в один writable каталог.

### 1.6 Переключение с ShipTask

Во время разработки Issue Grinder тестируется явным вызовом либо в изолированной
сессии, где конкурирующая автоматическая маршрутизация исключена. Cutover
устанавливает `issue-grinder@srez-marketplace`, затем удаляет локально
`ship-tasks@srez-marketplace`: Issue Grinder становится единственной
установленной неявной delivery authority, а Task Composer продолжает работать
как `$issue-grinder:task-composer` из нового package.

Старый Marketplace package можно сохранить как неустановленный rollback
artifact, но одновременно устанавливать его с Issue Grinder нельзя: это вернёт
конкурирующий ShipTask и дублирует logical Task Composer. Миграция не объявляется
завершённой, пока fresh skill discovery не показывает
`issue-grinder:issue-grinder`, `issue-grinder:task-composer` и отсутствие
установленного `ship-tasks:ship-tasks`.

## 2. Роль и зависимости

`$issue-grinder` — Task Manager-only coordinator доставки выбранного scope. Он
владеет общей стратегией, Goal, решениями о lifecycle issue, интеграцией кода,
окончательной проверкой и итоговым ответом пользователю.

Внешние интерфейсы разделены так:

- Task Manager adapter разрешает canonical refs, читает live issue, Release и
  связи, выполняет status/comment mutations и подтверждает их read-back;
- Strategic Explainer формулирует отдельные публикационные тексты, но не
  принимает решения о scope, статусе, полномочиях или продолжении работы;
- Goal хранит стратегическую цель и состояние длинного явно вызванного прогона;
- Git worktree и feature branches изолируют одновременно пишущих исполнителей;
- project context и project memory помогают найти Release, UAT и устойчивые
  разрешения, но не заменяют live Task Manager или фактическое состояние среды.

Ни одна зависимость не добавляет `$issue-grinder` полномочия сверх
`requirements.md` и текущего запроса пользователя.

Task Manager adapter является обязательной capability: без canonical reads и
versioned writes Issue Grinder не подменяет его локальным списком, другим
tracker-ом или памятью. Недоступность adapter-а обнаруживается до delivery
mutations и выдаётся как точная technical/context failure. Strategic Explainer,
напротив, остаётся optional communication dependency с native path.

Dependency declaration делает adapter доступным, но не заменяет его current wire
contract. Перед первой Task Manager mutation coordinator сверяет доступные tool
schemas и использует только реально объявленные операции и поля; названия,
idempotency и conflict shape не угадываются и не копируются в Issue Grinder как
вторая быстро устаревающая схема. Если обязательная semantic capability —
pagination, versioned write, comment/read-back или Goal operation — отсутствует,
это exact capability failure до соответствующего write. Механический guard,
если он нужен, принадлежит Task Manager adapter-у, а Issue Grinder сохраняет
собственные lifecycle и authority decisions.

## 3. Режим прогона и ранний context gate

В начале нового run coordinator фиксирует два разных факта:

- `explicit invocation` — пользователь назвал `$issue-grinder` в prompt,
  запустившем именно этот run;
- `run mode` — является ли уже начатый run явно вызванным и поэтому автономным.

Прошлый `$issue-grinder` не разрешает начинать новый явный run или новый Goal.
Однако `run mode` не теряется посреди того же незавершённого прогона из-за
следующего turn, compaction, автоматического продолжения или восстановления
контекста. Непрерывность доказывается не одним совпадением selector-а: checkpoint
связывает origin `explicit|implicit`, identity Project/selector, terminal flag,
Goal ref при его наличии и task-owned implementation/effect receipts. Для
single-issue run отсутствие Goal не уничтожает origin: тот же thread lineage и
согласованные checkpoints сохраняют его отдельно. Совместимый активный Goal
является одним из anchors, но сам по себе не доказывает тот же run и не переносит
autonomy в новый implicit request. При отсутствии доказанной непрерывности старый
explicit marker не восстанавливается по догадке. Terminal result либо явная
отмена, замена или существенная смена текущего прогона пользователем закрывают
этот режим.

До изменяющих действий coordinator разрешает:

1. явные уточнения scope и среды из текущего prompt;
2. canonical Project, Release и status refs через live Task Manager;
3. repository/project context и project memory как указатели на текущий Release,
   repository, команды и UAT;
4. фактическое подтверждение, что выбранная среда не является Production.

Устаревающая память используется только как locator и перепроверяется в живом
источнике. Неоднозначный default Release останавливает run до Task Manager
mutations. В явно вызванном автономном run неизвестный UAT также останавливает
работу до environment mutations; Production не используется как fallback.

Default Release разрешается только явному запуску без selector-а. Неявно
активированный skill должен получить однозначный issue, Release, Project или
иной ограниченный selector из текущего запроса и разрешимого непосредственного
контекста. Если такого selector-а нет, coordinator выполняет только безопасное
разрешение контекста и просит уточнение до любых mutations; remembered current
Release не подставляется как скрытое расширение scope.

При неявной загрузке Goal и дополнительные полномочия автономного режима не
создаются. Само исполнение разрешённого пользователем запроса и обычная
делегация независимой работы при этом могут продолжаться только в пределах
обычной authority текущего prompt и действующих платформенных ограничений.

Issue Grinder сам не создаёт routine approval prompt, запрещённый автономным
режимом. Если confirmation технически навязывает платформа или tool policy,
coordinator не выдаёт его за собственную продуктовую неопределённость и после
получения результата продолжает run; обойти платформенный gate скрытым способом
он не пытается.

## 4. Scope и стратегическая модель

Scope хранится как правило отбора, а не как замороженный список issue. Его
runtime-представление содержит источник выбора, canonical Project/Release или
явные issue refs, применимые статусы и последний подтверждённый снимок. Каждый
full inventory дочитывает Task Manager pagination до `hasMore=false` или
эквивалентного подтверждённого конца; первая страница не является полным scope.
Названия `To Do`, `In Progress` и `In Review` разрешаются в canonical status
refs текущего workspace/project, а не сравниваются как неподтверждённые строки.
Отсутствующий или неоднозначный обязательный status ref останавливает lifecycle
mutations до разрешения контекста.

Coordinator перечитывает scope:

- перед первой диспетчеризацией;
- после обнаруженного изменения Release, relations или статуса;
- после завершения либо блокировки рабочего пакета;
- перед новой волной параллельной работы;
- перед финальным выводом о завершении.

Непрерывный polling не нужен. Если issue исключено из scope, coordinator
перестаёт управлять его Task Manager lifecycle, сохраняет уже созданный
восстановимый checkpoint и решает судьбу локальной реализации по её фактической
полезности для оставшегося scope. Автоматический rollback или включение такой
работы в интеграцию только по инерции не выполняется.

### 4.1 Создание Goal

После live scope resolution coordinator изучает весь текущий фронт, общие
требования и связи issue и формулирует проблему верхнего уровня. Goal objective
содержит:

- ключевой стратегический outcome;
- текущее правило scope;
- обязательство довести все входящие issue из трёх рабочих статусов до выхода
  из них;
- существенные ограничения, включая запрет Production;
- наблюдаемое условие завершения.

Goal создаётся только при выполнении `IG-GOAL-01`. До `create_goal` coordinator
читает текущий Goal. Совместимый незавершённый Goal переиспользуется только при
доказанной continuity текущего run; совпадения selector-а и objective для этого
недостаточно. Его сохранённый selector сверяется с live scope без ложного
обещания переписать objective через недоступный интерфейс. Новый implicit run не
присваивает даже совместимый Goal и не наследует из него explicit autonomy.
Несовместимый либо не принадлежащий доказанно текущему run Goal не
перезаписывается и не завершается ради Issue Grinder. Если платформа не позволяет
завести второй Goal, coordinator сохраняет найденный безопасный frontier как
read-only checkpoint и сообщает несовместимость как точное препятствие Goal
lifecycle; он не начинает требующую Goal изменяющую работу без обязательного
Goal и не присваивает чужую цель.

Если явный run начался с одного issue, coordinator работает без Goal и создаёт
его лишь после роста scope. После создания Goal уменьшение scope не уничтожает
накопленный контекст. Признак явно запущенного run сохраняется отдельно от
самого факта наличия Goal, поэтому одно issue и временно недоступный Goal не
выключают автономность уже начатого прогона.

Стратегический outcome не остаётся одноразовым текстом при создании Goal. Перед
новой dispatch wave, существенным integration/review решением и финальной
reflection coordinator заново соотносит frontier с этим outcome. Каждый worker
packet получает только применимую к нему проекцию общей цели вместе с exact
issue contract; стратегический контекст не расширяет owned scope.

## 5. Основной delivery loop

Одна итерация цикла состоит из следующих смысловых фаз; конкретные tool calls
могут объединяться или переставляться, если сохраняются инварианты:

1. Перечитать live scope и фактические статусы.
2. Определить dependency-ready frontier и выбрать следующий issue или
   независимые рабочие пакеты.
3. Перевести начинаемое `To Do` в `In Progress` и подтвердить изменение.
4. Реализовать результат локально либо через изолированных субагентов.
5. Проверить точную интегрированную версию пропорционально изменению и
   acceptance issue.
6. Подготовить объяснение следующего нетривиального status transition и пройти
   reflection gate.
7. Опубликовать комментарий, изменить статус и перечитать issue.
8. Заново оценить scope, frontier и необходимость следующей итерации.

Issue, уже находящееся в `In Progress` или `In Review`, сначала проходит
recovery фактической target branch, task-owned implementation и доступного
evidence. Один старый status не доказывает наличие реализации или успешной
проверки. Неполный `In Review` возвращается в `In Progress` только через
обязательный причинный comment и повторный delivery loop.

Связь `blocked by` оценивается по наличию требуемой реализации в exact commit,
от которого реально будет выполняться зависимое issue, а не только по статусу
карточки или наличию кода в постороннем worker branch. Если реализация уже
доступна либо сначала безопасно интегрируется в эту base, зависимое issue
допускается в frontier; поздний reopen блокирующего issue добавляет повторную
проверку затронутой части, но не восстанавливает блокировку автоматически.

## 6. Комментарий и status transition как публикационная операция

Для каждого перехода, кроме `To Do → In Progress`, coordinator сначала собирает
проверенные факты и формирует semantic request к доступному
`$strategic-explainer:strategic-explainer`. В запрос входят назначение текста,
исходная ситуация, exact scope, язык, существенные ограничения и разрешимые
read-only anchors. Внутреннюю методику provider-а coordinator не воспроизводит.

Тот же communication route применяется к любому другому Task Manager comment,
который Issue Grinder решает опубликовать, а также к blocker- и final-report по
правилам Level 1. Routine progress journal в Task Manager по умолчанию не
создаётся: дополнительный comment должен иметь самостоятельную пользовательскую
ценность, но его наличие не обходит Strategic Explainer/native contract.

Полученный либо самостоятельно написанный native text проходит reflection:
объясняет ли он честно фактическое состояние и не обнаруживает ли доступную
существенную незавершённую работу текущего scope. Существенной считается работа,
которая нужна для acceptance issue, стратегического результата, исправления
ложного evidence/status, обработки нового участника dynamic scope или снятия
настоящего blocker-а. Необязательное улучшение, новый возможный feature либо
косметический hardening не удерживают текущий run открытым. Ready result не
переписывается ради стилистической вариативности. Если обнаружен существенный
пробел, status transition отменяется и issue возвращается в delivery loop.

После reflection публикационная последовательность такова:

1. опубликовать человекопонятный комментарий;
2. подтвердить его read-back;
3. изменить статус с optimistic concurrency;
4. перечитать итоговое состояние issue.

Если статус не изменился после уже опубликованного правдивого комментария,
coordinator сначала reconciles live state и повторяет только недостающий
эффект. Он не дублирует комментарий вслепую. Для тривиального
`To Do → In Progress` выполняются только status mutation и read-back.

Комментарий описывает уже подтверждённые факты, готовность к целевому статусу и
причину перехода, но не утверждает, что mutation уже состоялась. Поэтому
частичный результат `comment committed / status failed` остаётся правдивым и
восстановимым. Unknown comment outcome сначала разрешается чтением thread;
unknown status outcome — повторным чтением issue. Повторная запись допустима
только после доказательства отсутствующего эффекта.

Publication checkpoint сохраняет доступную identity операции: returned comment
ref или idempotency key adapter-а, exact target issue/version и digest готового
текста. Если adapter не предоставляет operation identity, coordinator не
изобретает поле, а reconciles bounded thread window по фактическому результату.
Одинаковая повторная проверка без изменения live state не создаёт нового права
на запись.

Если Strategic Explainer отсутствует, сразу используется native writing. Если
установленный facade вернул caller error, coordinator исправляет semantic call
по сообщённой причине. Настоящая техническая ошибка provider-а раскрывается как
таковая и не переименовывается в caller error. По умолчанию coordinator
продолжает через native writing, когда проверенные факты позволяют выполнить
тот же communication contract. Допустимый `IG-FLOW-03` ранний stop применяется
только если provider failure одновременно лишил run возможности безопасно
подготовить обязательную публикацию либо выявил более широкую техническую
неисправность, которая реально препятствует продолжению.

## 7. Verification и прозрачное исключение

Обычный путь в `Done` требует evidence по acceptance issue на точной
интегрированной версии. Размер diff или успешный отчёт отдельного субагента не
заменяют эту проверку.

Исключение `IG-GOAL-06` применяется только когда недоступная проверка относится
к детали, которая не меняет достигнутый стратегический outcome и не ставит под
сомнение основной acceptance, целостность данных, безопасность или identity
проверяемой версии. Если такой вывод нельзя обосновать имеющимися evidence,
проверка не считается несущественной.

При применении исключения coordinator сохраняет в issue comment точный
непроверенный фрагмент, причину, основание non-blocking решения и остаточный
риск. Тот же факт переносится в финальный ответ и, при наличии Goal, в его
финальный комментарий. Формулировка «проверено успешно» для пропущенной проверки
запрещена.

## 8. Blocker reflection и завершение

Candidate blocker сначала становится входом новой итерации осознанности:
coordinator перечитывает scope, зависимости, доступные инструменты, локальные
checkpoints и безопасные действия в пределах имеющихся полномочий. Объяснение
через Strategic Explainer готовится только после этой проверки.

Этот reflection и human blocker-report применяются к любому run, включая один
issue без Goal. Наличие Goal меняет только его lifecycle effect; оно не является
условием честного объяснения или поиска самостоятельного продолжения.

Если при формулировании blocker-report обнаружен реальный существенный шаг
текущего scope, публикация blocker-а отменяется и delivery loop продолжается.
Полученный текст и его source basis обязательно проходят отдельную
`post-explanation reflection` по current primary sources: объяснение не является
доказательством собственной блокировки.
Отсутствие frontier сначала фиксируется как candidate blocker. После принятой
post-explanation reflection полный blocker-report показывается пользователю и
текущая попытка останавливается с точным resume condition независимо от наличия
Goal. Goal получает terminal `blocked` только когда дальнейшее продвижение
действительно требует пользовательского решения или новой authority и выполнен
действующий платформенный blocker audit. Пока платформа ещё не разрешает
terminal `blocked`, Goal остаётся активным, а report честно называет это
расхождение; audit не задерживает объяснение пользователю и не запускает
внутренний бесконечный цикл.

Каждая recovery-ветка имеет наблюдаемую границу прогресса. Coordinator сравнивает
scope/frontier, object versions, attempted effect, result/error class, available
authority и новый evidence. Повтор допустим, когда изменился хотя бы один из этих
входов либо выбран другой существенный action. Та же комбинация без нового
evidence не считается продвижением: caller error переходит к исправленному
semantic call, повторившаяся provider failure — к native path, unknown write — к
live reconciliation, а исчерпанный safe path — к candidate blocker. Это не
универсальный лимит попыток, а bounded recovery конкретного effect.

Завершение использует fresh full inventory выбранного scope. Отсутствие issue в
`To Do`, `In Progress` и `In Review` является достаточным предметным критерием;
стратегический outcome не превращается во второй независимый terminal gate.
Финальный текст ещё раз проверяется на изменение scope, скрытый существенный
остаток и доступное обязательное действие текущего run. Новая идея или
необязательное улучшение могут попасть в итоговый отчёт, но не создают новый
цикл сами по себе. Только после чистой переоценки Goal завершается, а
пользователь получает причинный итоговый отчёт.

## 9. Автономность и среды

В явно вызванном run coordinator самостоятельно выполняет все доступные действия
в scope. Target по умолчанию — подтверждённый UAT; staging и другие доказанно
непроизводственные среды также допустимы. Публичность UAT не повышает действие
до approval gate.

Production отклоняется всегда: Issue Grinder не подключается к production
endpoint, не читает production logs/data, не выполняет smoke и не создаёт там
mutation или deployment. Локальное чтение project metadata, необходимое лишь
для классификации target как Production и отказа от него, не считается работой
с самой средой.

Task Manager lifecycle является отдельным control plane Issue Grinder и не
считается product Production deployment только потому, что сам Task Manager
доступен как hosted service. Его writes всё равно ограничены exact scope,
canonical refs, optimistic concurrency и read-back.

Исключительный security prompt допустим для действий с очень высоким риском:
раскрытие или ротация secrets, расширение access policy, необратимое изменение
общих durable data, работа с реальными чувствительными данными, воздействие на
реальных внешних получателей, реальный платёж либо потенциально неограниченная
стоимость. Сам факт deployment, публичного URL или обычного синтетического
тестового состояния UAT к этой категории не относится. Когда acceptance можно
доказать synthetic/ephemeral fixtures без реальных данных и получателей,
coordinator выбирает такой путь самостоятельно.

Если prompt необходим, UI selector предлагает `Да`, `Нет` и `Да всегда`. Если
специализированная selector capability недоступна, coordinator показывает те же
три взаимоисключающих варианта обычным структурированным вопросом и ждёт явного
выбора; отсутствие UI не считается согласием.
Категория `Да всегда` строится из типа действия, класса данных, среды и
ограниченного resource scope, чтобы не стать безграничным разрешением. После
выбора она сохраняется в project memory и в дальнейшем, включая будущие run,
применяется только к эквивалентным операциям этого проекта. Сохранённое
разрешение не превращает implicit run в explicit, не разрешает Production и не
расширяет соседние action/data/environment/resource категории. Persistence
подтверждается read-back. Если project memory недоступна, текущее `Да` остаётся
действительным для exact action, но coordinator честно сообщает, что обещание
`Да всегда` не удалось сохранить, и не симулирует постоянное разрешение.

`Нет` запрещает exact action и эквивалентные попытки обойти отказ. Coordinator
заново ищет безопасный путь в пределах прежних полномочий и блокируется только
если такого пути действительно нет. `Да` не расширяется на соседние категории
или следующий run.

UAT target определяется и подтверждается перед первым environment effect, а не
превращается в обязательный preflight для работы, которой среда вообще не
нужна. До environment mutation target должен быть однозначно подтверждён как
UAT либо другая непроизводственная среда; неизвестный target не угадывается.

## 10. Multi-agent orchestration

Делегация применяется при наличии минимум двух независимых полезных пакетов
независимо от явного или неявного способа загрузки skill. Это решение не
включает максимальную автономность в неявном run и не расширяет authority.
Если subagent capability или изолированная writable capacity недоступны,
coordinator выполняет frontier последовательно на текущем профиле. Отсутствие
multi-agent surface само по себе не является blocker-ом.

Явное правило пользователя о topology — точное или относительное число
субагентов, роли, условие делегации либо opt-out — имеет приоритет. Основной
coordinator не входит в названное число субагентов. Общий opt-out worker
delegation не отключает отдельный Strategic Explainer interface, если
пользователь прямо не запретил и его.

Без user override coordinator:

1. разрешает live integration target и не подменяет его текущей случайной
   веткой либо dirty root checkout;
2. строит dependency graph и карту поверхностей записи;
3. выделяет только conflict-free dependency-ready packets;
4. создаёт branches от подтверждённой integration base и выдаёт каждому writer
   отдельные feature branch и Git worktree;
5. оставляет read-only исследователей без worktree;
6. запускает столько пакетов, сколько оправдано шириной frontier;
7. принимает отчёты, но сам объединяет изменения;
8. проверяет exact integrated result;
9. после каждого результата или изменения scope пересчитывает frontier.

Каждый packet содержит exact scope, owned surfaces, исходные данные,
ограничения, ожидаемый результат и способ проверки. Сохранившийся task-owned
worktree является checkpoint: после доказанной остановки прежнего владельца он
передаётся новому exclusive writer, а не дублируется.

Изоляция writer-а подтверждается фактическими `git worktree` и branch refs до
первой записи. Указание пути только в prompt субагента не является evidence.
Coordinator не интегрирует исключённый из dynamic scope packet по инерции:
такой checkpoint попадает в fan-in лишь когда его результат независимо нужен
оставшемуся scope, что подтверждено повторной оценкой поверхностей и acceptance.

`gpt-5.6-luna` с `max` получает только строго простые пакеты по `IG-MA-14`.
Material uncertainty немедленно возвращает тот же checkpoint coordinator-у,
который продолжает его на current profile без Luna retry loop. Остальные
пакеты сразу наследуют текущий профиль. Недоступность Luna означает обычное
выполнение на current profile, а не blocker.

## 11. Integrity и восстановление

Каждая Task Manager mutation использует текущую версию объекта, а её результат
подтверждается read-back. Unknown write outcome сначала reconciles через live
read; повторять mutation вслепую нельзя.

Run checkpoint хранит только проверяемую continuity: origin, Project/selector
identity, terminal state, Goal ref при наличии, task-owned Git identity,
publication/status receipts и незавершённые effects. Формат и место хранения
выбираются по доступной platform capability; Architecture не требует
несуществующий durable store. Возобновление сверяет checkpoint с live state и не
принимает совместимый Goal либо тот же Release за достаточную lineage.

Git integration принимает только task-owned изменения с понятным происхождением.
Чужие или пользовательские изменения не очищаются, не reset-ятся и не
присваиваются run. При interruption сохраняются ветки, worktree, результаты
проверок и незавершённые эффекты Task Manager, достаточные для безопасного
возобновления.

Явная отмена пользователем немедленно прекращает новые изменяющие действия
этого run. Coordinator сохраняет проверяемые checkpoints и фактическое
состояние, но не выдаёт отменённый run за `complete` или `blocked` и не меняет
Task Manager cancellation statuses от имени Issue Grinder.

## 12. Трассировка и наблюдаемая проверка

| Level 1 | Архитектурный механизм | Наблюдаемое evidence |
|---|---|---|
| `IG-FLOW-*` | delivery loop, publication transaction, live read-back | корректная последовательность статусов и причинные комментарии без ложного completion |
| `IG-GOAL-*` | strategic synthesis, Goal lifecycle, blocker/final reflection | Goal отражает общую проблему и завершается только после fresh empty active scope |
| `IG-SCOPE-*` | selector-as-predicate и контрольные refresh points | новые и исключённые issue учитываются до terminal result |
| `IG-AUTO-*` | explicit-mode gate, UAT resolver и узкий security selector | нет Production access; разрешённая UAT работа не ждёт рутинного approval |
| `IG-MA-*` | dependency-ready packets, isolated writers, integration owner и profile routing | параллельные writers изолированы, а acceptance относится к объединённой версии |

Группированная таблица является только обзором. Точная coverage map связывает
каждый отдельный `IG-*` как минимум с одним runtime surface и одним наблюдаемым
evaluation scenario.
Отсутствующий exact ID считается пробелом компиляции, но совпадение текста или
ID само по себе не доказывает поведение.

Целевой release gate состоит из четырёх слоёв; их текущий фактический статус
фиксируется в `evaluation.md`, а описание слоя не считается доказательством его
исполнения:

1. **Static contract.** Проверяет frontmatter, manifest, ссылки, уникальность и
   полноту `IG-*`, разрешимость references, отсутствие скрытой второй policy и
   byte identity source → Marketplace → installed cache.
2. **Deterministic trace harness.** Получает синтетическое начальное состояние,
   scripted tool results и fault injection, затем проверяет required/forbidden
   decisions и их порядок. Текущий harness является oracle отдельных hard
   invariants и не доказывает, что Markdown runtime вызовет те же effects.
3. **Independent model-forward evaluation.** Запускает реальный skill на
   синтетическом Task Manager и временном Git repository. Детерминированные
   assertions проверяют effects, а отдельный evaluator — стратегический смысл,
   фактологичность и понятность публикационного текста. Generator не получает
   expected answer или rubric с подсказкой нужного решения.
4. **Fresh installed-plugin smoke.** После упаковки plugin проверяется в новой
   Codex-сессии с live synthetic UAT: activation, dependencies, полный workflow,
   Marketplace/cache identity и отсутствие второй implicit delivery authority.

Минимальный fault/scenario corpus включает:

- direct explicit, indirect implicit с selector-ом, implicit без selector-а,
  follow-up, negative routing и boundary prompts;
- zero/one/multiple issue, рост и сокращение scope, late matching issue,
  pagination и concurrent status change;
- недоступный Task Manager adapter и навязанный платформой approval, который не
  превращается во внутренний permission loop;
- совместимый и несовместимый активный Goal, доказанная continuity против одного
  совпадения selector-а, single-issue explicit checkpoint и новый implicit run;
- платформенный blocker audit, включая принятый report при отложенной Goal
  mutation;
- каждый lifecycle transition, `comment committed / status failed`, оба
  unknown outcomes, version conflict и защита от duplicate comment;
- реализацию `blocked by` в integration base, код только в постороннем worker
  branch, поздний reopen и targeted recheck;
- отсутствующий Explainer, caller error, technical failure, reflection finding
  и native continuation;
- non-material verification gap и соседний material gap, где исключение
  запрещено;
- public UAT, неизвестный target, Production alias, попытку production read и
  узкий `Да всегда` с успешным/неуспешным memory read-back, future equivalent
  operation и несовпадающую категорию;
- synthetic substitute для real data/recipient и настоящий high-risk внешний
  effect, требующий selector-а;
- независимые и конфликтующие writer surfaces, недоступных subagents, worker
  interruption, Luna return и exact integrated verification;
- optional improvement при финальной reflection, который попадает в отчёт, но
  не создаёт бесконечный run;
- повтор recovery с тем же progress fingerprint, changed-input retry, доступный
  fallback и переход к candidate blocker после исчерпания safe path.

Hard invariants — отсутствие Production access и Backlog mutations, корректный
Goal gate, обязательный comment, exclusive writable worktree, отсутствие blind
retry и task lifecycle только от coordinator-а — имеют нулевую терпимость.
Semantic quality оценивается отдельно и не может компенсировать нарушение hard
invariant. Проверка наличия терминов в файлах не заменяет model-forward run.
