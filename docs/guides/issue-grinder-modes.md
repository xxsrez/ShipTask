# Режимы Issue Grinder

Issue Grinder поддерживает пять режимов. Они меняют распределение работы между
профилями и форму проверки, но не меняют scope, полномочия, Task Manager
lifecycle, запрет Production и требования к доказательствам.

Действующий пользовательский контракт находится в
[Requirements](../skills/issue-grinder/requirements.md), способ исполнения — в
[Architecture](../skills/issue-grinder/architecture.md).

## Короткое сравнение

| Режим | Кто выполняет работу | Проверка | Когда заканчивается |
|---|---|---|---|
| `Соло` | Текущая основная модель последовательно выполняет всю работу без execution-субагентов | Self-review плюс объективные checks | Terminal result или настоящий blocker |
| `Классический` | Основная модель делает почти всё; Luna получает только strict-simple packets | Независимый Luna-review и итоговая приёмка основной моделью | Terminal result или настоящий blocker |
| `Баланс` | Основная модель планирует scope и делает критическую часть; до трёх Luna High параллельно выполняют независимые packets | Общие tool gates и итоговая приёмка основной моделью | Terminal result или настоящий blocker |
| `Менеджер` | Постоянный Luna manager ведёт постоянного Luna implementer-а по крупным последовательным фазам | После `complete` один Luna reviewer проверяет candidate, затем основная модель проводит final gate | Terminal result или настоящий blocker |
| `Экономичный` | Luna выполняет содержательную работу; non-Luna root остаётся transport/authority оболочкой | Independent Luna review нужен для terminal result | Terminal result либо resumable checkpoint |

## Как работает режим по умолчанию

`По умолчанию` — не шестой режим и всегда означает `Соло`. `Классический`,
`Баланс`, `Менеджер` и `Экономичный` включаются только явной просьбой.
Модель, effort, размер scope, число issue, capacity и quota это правило не
меняют. Внутри непрерывного run выбранный mode сохраняется до явного безопасного
переключения.

## `Соло`

Текущая основная модель сама анализирует весь scope, последовательно реализует
по одному dependency-ready issue или packet, интегрирует, проверяет и проводит
self-review. Issue Grinder не создаёт worker, scout, critic, verifier или
отдельного reviewer-а. Service/provider agent не считается исполнителем режима,
пока получает только свой ограниченный semantic request.

## `Классический`

Основная модель изучает весь live scope, принимает продуктовые, архитектурные,
миграционные, security и другие плохо проверяемые решения и делает почти всю
реализацию сама. Luna получает только действительно тривиальные,
самодостаточные, изолированные и объективно проверяемые packets. Exact
интегрированный candidate получает independent Luna review, после чего основная
модель проводит final acceptance.

## `Баланс`

`Баланс` — ускоренный Solo-подобный режим для сложной задачи. Основная модель
одним проходом задаёт архитектуру, dependency graph, acceptance, write surfaces
и integration boundaries. Затем она выделяет от двух до трёх одновременно
готовых независимых packets и одним окном запускает для них Luna High workers.

Каждый packet имеет self-contained inputs, отдельную write surface, стабильный
interface, изолированный candidate и локальный oracle. Workers не создают
descendants, не становятся manager/reviewer и не пишут в integration target.
Если подходящей ширины нет, основная модель продолжает работу последовательно
без искусственного дробления.

Пока Luna работает, основная модель выполняет собственный critical/integration
packet, готовит общий test harness или исследует cross-cutting risk. После
одного collective event-driven wait она механически объединяет handoffs,
проверяет candidate identity и ownership, а затем одним parallel tool batch
запускает долгие общие checks. Финальный exact-diff review, исправления и
acceptance остаются основной модели.

Отдельный independent reviewer не является штатной ролью `Баланса`. Он
добавляется только по явному требованию пользователя, project policy или exact
scope. Одновременно active не больше одной Luna wave и трёх Luna workers.

## `Менеджер`

Основная модель один раз создаёт control brief. Постоянный Luna manager без
source/tool access ведёт постоянного Luna implementer-а по небольшому числу
крупных последовательных фаз одного exact candidate. Coordinator только
механически пересылает phase/evidence packets и сохраняет Goal, Task Manager,
fan-in и external effects.

После manager `complete` один independent Luna reviewer последовательно
проверяет candidate. Material defect возвращается прежнему implementer-у, а
changed candidate — прежнему reviewer-у. Best-of-N, параллельные реализации и
массовые critics не входят в штатную topology.

## `Экономичный`

Luna Max анализирует, реализует, тестирует и критикует, сводя работу к одному
exact candidate. Non-Luna root только хранит Goal/Task Manager authority и
механически выполняет fan-in/publication. Independent Luna review обязателен для
terminal result.

Это единственный режим, где попытка может честно закончиться resumable
checkpoint: с exact candidate, raw checks, known defects, deferred gates,
правдивым active status и точкой продолжения.

## Как выбрать

- Нужна предсказуемость и один текущий исполнитель — `Соло`.
- Нужна максимальная обычная уверенность — `Классический`.
- Нужно ускорить сложную задачу ограниченной параллельной помощью — `Баланс`.
- Большую связанную задачу нужно провести экономичным manager loop — `Менеджер`.
- Нужен максимум прогресса за минимум дефицитной квоты — `Экономичный`.

## Справка без запуска работы

Вопросы о режимах, default и различиях не запускают delivery: Issue Grinder не
обращается к Task Manager, не создаёт Goal, не меняет title и не вызывает
subagents.
