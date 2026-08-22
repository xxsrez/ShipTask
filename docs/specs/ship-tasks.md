# ShipTask: канонический контракт

Статус: current contract, 2026-08-22. Основан на
[ADR-0018](../decisions/0018-outcomes-not-tool-choreography.md) и
[ADR-0019](../decisions/0019-goal-only-for-multi-task-implementation.md), а
reporting contract уточнён
[ADR-0020](../decisions/0020-visible-acceptance-incidents-and-required-comments.md).
Эти решения соответственно сохраняют свободу способа, отделяют Goal от release
и делают приёмочные инциденты видимыми во всём run.

## 1. Назначение и запуск

`$ship-tasks` доводит однозначно выбранный scope из Task Manager до результата,
который соответствует фактам: выполнен, возвращён на доработку либо честно
оставлен незавершённым с понятной причиной.

Skill запускается:

- явно через `$ship-tasks`;
- по просьбе выполнить exact существующую Task вроде `TM-123`;
- для уже выбранного Task Manager Project, Release или current scope;
- при явной просьбе создать ровно одну Task в Task Manager и сразу выполнить её.

Обычная просьба исправить код или продукт без Task Manager anchor не запускает
ShipTask. Чтение статуса, аудит, объяснение, планирование и backlog capture также
не являются delivery.

### 1.1 Режимы

- `single`: одна exact Task, включая create-and-deliver; Goal не создаётся.
- `batch-implementation`: в одном run реализуются или возвращаются в rework две
  или больше concrete Tasks; Goal учитывает прогресс этой массовой имплементации.
- `release`: commit/push/publish/deploy/smoke/rollback уже подготовленного
  candidate; Goal не создаётся, в том числе при selector `Project` или `Release`.
- `memory-maintenance`: project memory меняется только по явной просьбе.
- `non-delivery`: точное чтение или planning mutation без delivery workflow.

Project, Release, current scope, несколько Tasks и bare `$ship-tasks` задают
границу discovery, но не mode и не основание для Goal. Mode определяется
фактической работой после live inventory. Чтение, проверка или lifecycle
reconciliation нескольких Tasks не являются массовой имплементацией.

Bare `$ship-tasks` берёт `current_scope` из project memory. Prompt selector имеет
приоритет, но не переписывает memory. Task Manager всегда перечитывается: memory
не доказывает текущий status, version, comments, relations или access.
Unresolved acceptance incidents из materially relevant comments называются в
первом содержательном chat update после scope resolution.

### 1.2 Проверяемая trigger matrix

| Prompt | ShipTask | Результат маршрутизации |
|---|---|---|
| `$ship-tasks` | да | mode по live inventory; Goal только для `batch-implementation` |
| `Выполни TM-123` | да | `single` для exact существующей Task |
| `Доведи выбранный Task Manager Project Alpha` | да | mode по фактической работе; selector не создаёт Goal |
| `Выпусти выбранный Task Manager Release 0.2 на production` | да | `release` без Goal; production authority дана exact запросом |
| `Имплементируй все незавершённые Tasks выбранного Release 0.2` | да | `batch-implementation` с Goal после live inventory |
| `Доведи текущий Task Manager scope` | да | mode по фактической работе; Goal только при имплементации 2+ Tasks |
| `Создай ровно одну Task в Task Manager: исправить импорт, и сразу начни выполнять её` | да | `single create-and-deliver` |
| `Почини X сейчас` | нет | обычная реализация без Task Manager scope |
| `Исправь баг в plugin` | нет | обычная реализация без Task Manager scope |
| `Реализуй это изменение в коде` | нет | обычная реализация без Task Manager scope |
| `Покажи статус TM-123` | нет | read-only Task Manager adapter |
| `Проведи аудит TM-123` | нет | read-only Task Manager adapter |
| `Создай Task в Task Manager` | нет | planning/write через adapter, без delivery flow |
| `Просто добавь это в backlog` | нет | backlog capture, без delivery flow |

## 2. Конституция

Подробный алгоритм не является целью. Агент свободен выбирать инструменты,
порядок работы, способ реализации и достаточные проверки. Свобода ограничена
следующими требованиями.

### 2.1 Пользовательский результат важнее внутренней процедуры

Агент сначала устанавливает, что должна получить Task и что фактически
происходит. Goal, plans, reason codes, report keys и внутренняя оркестрация не
могут подменять реализацию, проверку или понятное объяснение.

### 2.2 Состояние Task должно быть правдивым и объяснённым

Любой существенный переход статуса получает native Task Manager comment,
который опубликован и перечитан до status write. Исключение — очевидный старт
новой работы `To Do → In Progress`.

Комментарий обязателен, в частности, перед:

- `In Progress → In Review`;
- `In Review → In Progress`;
- `In Review → Done`;
- reopen из `Done` или другого terminal status;
- новым `Canceled`/`Duplicate` либо необычной корректировкой lifecycle.

Если Task остаётся в текущем статусе из-за material blocker, комментарий также
обязателен. Ответ только в Codex не заменяет Task comment. `description` и другие
поля Task не используются как запасной канал.

Current Task Manager adapter предоставляет native comment create/list/read.
ShipTask всегда создаёт и перечитывает обязательный comment. Create reconciles
по adapter contract; пока comment фактически не существует, связанный
существенный transition не завершён.

### 2.3 Приёмочный инцидент виден сразу и остаётся в истории

`verified-failure`, `verification-blocked` и `task-contract-conflict`,
установленные при проверке exact candidate или release scope, являются
приёмочными инцидентами. Только `verified-failure` называется найденным bug.

До repair, status write или blocking handoff агент немедленно сообщает в Codex
chat exact Task/criterion, expected result, observed fact либо границу знания,
impact, установленный outcome и следующий шаг. Для exact Task затем публикуется
и перечитывается opening comment. Resolution/completion comment не стирает
opening: он связывает тот же criterion с cause/confidence, fix/result identity,
повторной проверкой, final state и remaining risk.

Пока инцидент unresolved в active run, chat напоминает о нём при каждом material
state change и, если таких изменений долго нет, примерно каждые 10 минут. Эти
progress updates не дублируются в Task comments. Финальный run report сохраняет
compact ledger всех material incidents, включая найденные и исправленные в том
же run.

Сбой отдельного инструмента, ожидаемая red/green iteration и общий batch failure
без task-level attribution не создают инцидент конкретной Task.

### 2.4 Доказательство важнее выбранного способа

Агент самостоятельно выбирает инструменты, способы диагностики, реализации и
приёмки. Ни один технический путь не является обязательным только потому, что
был выбран первым или однажды не сработал. Агент может исправить его, заменить,
объединить несколько источников evidence или перестроить проверку.

Конституция оценивает результат выбора, а не сам выбор:

- current acceptance не ослаблен ради удобства;
- success/failure подтверждены достаточным evidence;
- недоступное доказательство не названо verified;
- остановка означает, что в текущем scope и полномочиях не найден достаточный
  безопасный способ продолжить.

Нет фиксированного числа попыток, обязательной последовательности repair или
предпочтённого инструмента. Сбой отдельного способа сам по себе не является ни
product defect, ни `verification-blocked`.

Native Task comment остаётся обязательным наблюдаемым результатом существенного
transition. Как обеспечить его создание и read-back, решает агент. Transition
не считается завершённым, пока comment фактически не существует в Task.

### 2.5 Факты определяют исход приёмки

Количество прежних попыток или редакций acceptance ничего само по себе не
доказывает. Текущий контракт Task и текущее наблюдение важнее истории.

### 2.6 Безопасность и полномочия остаются жёсткими

ShipTask не расширяет scope и не разрешает без явного согласия production,
необратимые изменения durable data, secrets/privacy/access-policy changes,
действия с внешними получателями и неограниченные расходы. Обычный нужный
release в dev/test/QA/UAT/staging/preview/sandbox входит в delivery authority,
если target надёжно определён как non-production.

## 3. Источники истины и технический адаптер

Task Manager connector является единственным task-source и отвечает за exact
refs, pagination, detail, native comment create/list/read, optimistic version и
read-back. ShipTask задаёт delivery policy, а adapter гарантирует comment
mechanics, idempotency/reconciliation и current payload contract.

Перед работой агент разрешает полный exact scope и перечитывает live Task state,
acceptance, relations, relevant comments, dependencies и authority. Детали
pagination, optimistic concurrency, write reconciliation и read-back принадлежат
Task Manager adapter, а не business policy ShipTask.

Несовместимый connector, неразрешимый exact scope, чужой активный Goal или
общая authority-конфигурация, делающая любые writes небезопасными, вызывают
`TASK CONTEXT ALARM` до mutation.

## 4. Lifecycle

Базовый поток:

```text
To Do → In Progress → In Review → Done
                            ↘ In Progress при доказанном дефекте
```

- `To Do`: работа не начата.
- `In Progress`: идёт реализация или исправление доказанного дефекта.
- `In Review`: candidate предъявлен, но success/failure ещё не установлен либо
  приёмка объективно заблокирована.
- `Done`: текущий контракт Task доказан и обязательные effects завершены.

`In Review` не означает ни успех, ни дефект. `Done` не ставится в ожидании
ручного подтверждения пользователя: invocation разрешает automatic acceptance,
когда result действительно доказан.

### 4.1 Комментарий при переходе

Комментарий должен простым языком объяснять:

- что установлено сейчас;
- почему Task меняет статус или остаётся незавершённой;
- какое наблюдение поддерживает вывод;
- что это означает для пользователя;
- что произойдёт дальше или что нужно для продолжения.

Не нужен формальный шаблон, внутренний журнал или длинный перечень инструментов.
Достаточен текст, после которого человек понимает решение без чтения сессии.
Комментарий пишется на языке пользователя; внутренние reason codes, смесь
жаргона и отчёт о процессе объяснением не являются.
Status меняется только после comment read-back; затем Task также перечитывается.

### 4.2 Переход в review

Когда целостный candidate реализован и необходимые текущие проверки пройдены,
агент публикует понятный comment о готовом результате и проведённой проверке,
перечитывает его, переводит `In Progress → In Review` и сразу проводит
приёмку. `In Review` не является местом ожидания человека.

## 5. Исходы приёмки

Агент выбирает исход по текущим фактам, а не по желанию закрыть Goal. Матрица
применяется к exact candidate в `In Review` и к release verification уже
подготовленного scope. Status effects выполняются только для точно attributed
Tasks.

### 5.1 Противоречие в задаче (`task-contract-conflict`)

Current mandatory requirements противоречат друг другу либо не определяют
наблюдаемый результат. Агент немедленно называет конфликт в chat и публикует
opening comment. Если одно исправление объективно следует из accepted source и
разрешено, он исправляет контракт, перечитывает Task и оставляет resolution
comment. Иначе Task остаётся `In Review` с рекомендованным решением.

Длинная история изменений acceptance не является конфликтом.

### 5.2 Доказанный дефект (`verified-failure`)

Exact candidate в совместимой среде прямо нарушает current acceptance. Агент
до repair сообщает инцидент в chat и через Strategic Explainer формулирует
opening comment: что ожидалось, что наблюдается, каково влияние, чем это доказано
и почему нужен возврат. После comment read-back переводит `In Review → In
Progress`, перечитывает Task и продолжает исправление в том же run. Сам переход
не является завершением ShipTask.

После repair агент публикует material progress в chat, повторяет достаточную
приёмку и в resolution/completion comment связывает тот же criterion с cause,
fix/result identity и retest evidence. Найденный defect остаётся в final incident
ledger даже при последующем `verified-success`.

Падение общей batch-проверки без task-level attribution не доказывает дефект
каждой Task. Сначала нужна диагностика, которая разделит причины.

### 5.3 Приёмку нельзя провести (`verification-blocked`)

Выбранные агентом разумные способы не доказывают ни success, ни failure в
текущем scope и полномочиях. Через Strategic Explainer он формулирует:

- что именно нельзя установить и почему;
- что уже доказано;
- рекомендуемый feasible способ получить достаточное evidence, его предпосылки
  и наблюдаемый признак успеха;
- альтернативы только когда реальный выбор materially меняет authority, risk,
  cost или доказательную силу.

Агент немедленно сообщает, что приёмка не завершена и product bug не установлен,
публикует и перечитывает opening/blocker comment; Task остаётся `In Review`.

### 5.4 Доказанный успех (`verified-success`)

Current acceptance, применимые проверки, identity интегрированного result и
обязательные effects доказаны. Агент через Strategic Explainer формулирует
полученный результат, его значение, ключевое evidence и реальные ограничения,
публикует и перечитывает comment, затем переводит `In Review → Done` и
перечитывает Task. Если в этом run был приёмочный инцидент, comment также
закрывает его или прямо указывает, что он остаётся unresolved.

### 5.5 Attribution за пределами одной Task

Падение общего batch gate без task-level attribution создаёт scope-level chat и
final-report finding, но не defect comments во всех Tasks. После separating
evidence opening comment и lifecycle effects получает только exact affected
Task. Если release verification обнаружила defect в terminal Task, opening
comment предшествует reopen, после чего обычный rework lifecycle продолжается.

## 6. Strategic Explainer

Strategic Explainer помогает написать человеческое объяснение, но не выбирает
факты, статус, scope, authority, способ исправления или terminal outcome.

Он используется для каждого обязательного lifecycle/blocker comment. ShipTask
передаёт содержательную проблему, current facts, известное/неизвестное, влияние
и ближайшие strategic anchors. Конкретный способ вызова и организации контекста
агент выбирает сам; discovery остаётся bounded и read-only.

ShipTask проверяет результат, сам пишет окончательный comment и не упоминает в
нём внутреннюю orchestration. Конституция требует применить Strategic Explainer
и получить понятный comment, но не задаёт конкретный способ invocation,
диагностики или восстановления.

Подробный handoff: [runtime reference](../../ship-tasks/references/strategic-explainer.md).

## 7. Реализация и проверка

Агент самостоятельно выбирает минимальный целостный способ выполнить Task.
Обычно он:

- проверяет repository/project instructions и dirty worktree;
- реализует только in-scope result;
- выполняет подходящие targeted checks и необходимые aggregate/runtime checks;
- устанавливает exact result identity;
- выполняет необходимые разрешённые non-production effects и проверяет их;
- устраняет найденные in-scope проблемы, пока остаётся безопасный полезный шаг.

Не все Tasks обязаны проходить одинаковые команды. Проверка должна доказывать
конкретный контракт, а не соответствие универсальному ритуалу. Недоступное
доказательство называется `not-available`, а не verified.

Out-of-scope finding не исправляется и не превращается автоматически в новую
Task. Если он не блокирует текущий result, он кратко попадает в final report.

## 8. Массовая имплементация и Goal

Goal создаётся только для `batch-implementation`: после exact scope resolution и
live inventory установлено, что current run действительно реализует или
возвращает в rework минимум две concrete Tasks. Goal создаётся до первой
implementation mutation и хранит objective, observable done criteria,
verification, authority и progress именно этой массовой имплементации.

Ни selector `Project`/`Release`/current scope, ни bare `$ship-tasks`, ни чтение,
проверка, приёмка или reconciliation нескольких Tasks сами по себе не разрешают
Goal. `single` и `release` Goal не создают. Commit, push, publish, deploy, smoke,
bounded repair/rollback и production release уже подготовленного candidate —
release effects, а не массовая имплементация Tasks.

Release-only run не создаёт, не переиспользует, не ретаргетит и не завершает Goal
только ради release. Если release является исходным done criterion уже активного
совместимого Goal массовой имплементации, run может продолжить этот Goal, но сам
release никогда не является основанием создать новый.

Goal не решает, сколько раз проверять Task, не определяет её status и не
превращает task-local blocker в глобальный. Пока в scope массовой имплементации
остаются `To Do`, `In Progress`, `In Review`, rework, незавершённые effects или
in-scope defect, Goal остаётся активным.

Изолированная проблема одной Task не останавливает независимую runnable работу.
Перед ожиданием пользователя `batch-implementation` повторно читает полный
inventory; если есть безопасная runnable работа, агент продолжает её. Глобальный
stop допустим только когда конфликт scope/shared state/authority делает любую
оставшуюся mutation небезопасной.

## 9. Release authority

Нужный для Task release в local/dev/test/QA/UAT/staging/preview/sandbox можно
выполнить без дополнительного вопроса после проверки target. Сюда входят
build/publish/deploy, smoke и bounded repair/rollback затронутого
non-production surface.

Production требует явного approval для exact target. Такое approval не отменяет
verification, comments и read-back. При отсутствии approval Task получает
понятный comment и остаётся в правдивом non-terminal status; другие Tasks могут
продолжаться.

## 10. Завершение run

Перед финальным ответом агент перечитывает affected Tasks, comments, statuses,
применимый Goal и обязательные external effects. Если есть безопасный in-scope
способ устранить gap, он делает это до handoff.

Run report начинается с результата и простым языком сообщает:

- что получилось и в каком состоянии Task/Goal;
- что доказано, а что не проверено;
- какие material acceptance incidents обнаружены, включая уже исправленные;
- для каждого incident — Task/criterion, cause/confidence, fix, retest evidence
  и final state;
- причину незавершённости, если она есть;
- какие исправления уже выполнены;
- одно точное условие или действие для продолжения.

Unresolved incident располагается рядом с общим result и не допускает
clean-success формулировку для affected Task. Compact incident ledger не
является process diary и не исчезает после успешного repair. Run report не
заменяет Task comments. Goal `batch-implementation` отмечается
complete только после fresh full inventory без незавершённой in-scope работы.
Release-only run не создаёт и не финализирует Goal. Нельзя объявлять skill change
или distribution завершёнными при частичном выполнении project DoD.

## 11. Проверяемые сценарии

Обязательная decision-level матрица находится в
[проверке lifecycle и приёмки](../reference/shiptask-review-disposition-evaluation.md).
Она является частью current contract и должна выполняться вместе с repository
validator. Исторические ADR и датированные reports не являются fallback policy.
