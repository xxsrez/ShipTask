# ShipTask: канонический контракт

Статус: current contract, 2026-08-21. Основан на
[ADR-0018](../decisions/0018-outcomes-not-tool-choreography.md), который уточняет
constitution-first решение ADR-0017.

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
- `batch`: несколько Tasks, Project, Release или bare `$ship-tasks`; используется
  Goal как журнал прогресса всего выбранного scope.
- `memory-maintenance`: project memory меняется только по явной просьбе.
- `non-delivery`: точное чтение или planning mutation без delivery workflow.

Bare `$ship-tasks` берёт `current_scope` из project memory. Prompt selector имеет
приоритет, но не переписывает memory. Task Manager всегда перечитывается: memory
не доказывает текущий status, version, comments, relations или access.

### 1.2 Проверяемая trigger matrix

| Prompt | ShipTask | Результат маршрутизации |
|---|---|---|
| `$ship-tasks` | да | `batch` по memory `current_scope` |
| `Выполни TM-123` | да | `single` для exact существующей Task |
| `Доведи выбранный Task Manager Project Alpha` | да | `batch` выбранного Project |
| `Выпусти выбранный Task Manager Release 0.2` | да | `batch` выбранного Release |
| `Доведи текущий Task Manager scope` | да | `batch` уже выбранного current scope |
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

### 2.3 Доказательство важнее выбранного способа

Агент самостоятельно выбирает инструменты, способы диагностики, реализации и
приёмки. Ни один браузер, test harness или другой технический путь не является
обязательным только потому, что был выбран первым или однажды не сработал.
Агент может исправить его, заменить, объединить несколько источников evidence
или перестроить проверку.

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

### 2.4 Факты определяют исход приёмки

Количество прежних попыток или редакций acceptance ничего само по себе не
доказывает. Текущий контракт Task и текущее наблюдение важнее истории.

### 2.5 Безопасность и полномочия остаются жёсткими

ShipTask не расширяет scope и не разрешает без явного согласия production,
необратимые изменения durable data, secrets/privacy/access-policy changes,
действия с внешними получателями и неограниченные расходы. Обычный нужный
release в dev/test/QA/UAT/staging/preview/sandbox входит в delivery authority,
если target надёжно определён как non-production.

## 3. Источники истины и технический адаптер

Task Manager connector является единственным task-source и отвечает за exact
refs, pagination, detail, comments, optimistic version и read-back. ShipTask
задаёт delivery policy, но не изобретает отсутствующие adapter capabilities.

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

## 5. Четыре исхода `In Review`

Агент выбирает исход по текущим фактам, а не по желанию закрыть Goal.

### 5.1 Противоречие в задаче (`task-contract-conflict`)

Current mandatory requirements противоречат друг другу либо не определяют
наблюдаемый результат. Если одно исправление объективно следует из accepted
source и разрешено, агент исправляет контракт и перечитывает Task. Иначе через
Strategic Explainer формулирует точное противоречие и нужное решение, публикует
и перечитывает comment, оставляет Task в `In Review`.

Длинная история изменений acceptance не является конфликтом.

### 5.2 Доказанный дефект (`verified-failure`)

Exact candidate в совместимой среде прямо нарушает current acceptance. Агент
через Strategic Explainer формулирует, что проверено, что именно не работает,
каково влияние и почему нужен возврат. После comment read-back переводит
`In Review → In Progress`, перечитывает Task и продолжает исправление в том же
run. Сам переход не является завершением ShipTask.

Падение общей batch-проверки без task-level attribution не доказывает дефект
каждой Task. Сначала нужна диагностика, которая разделит причины.

### 5.3 Приёмку нельзя провести (`verification-blocked`)

Выбранные агентом разумные способы не доказывают ни success, ни failure в
текущем scope и полномочиях. Через Strategic Explainer он формулирует:

- что именно нельзя установить и почему;
- что уже доказано;
- 2–4 реально различающихся способа провести приёмку, их предпосылки,
  доказательную силу и краткий trade-off;
- рекомендуемый следующий вариант и наблюдаемый признак успеха.

Комментарий публикуется и перечитывается, Task остаётся `In Review`. Если сломан
сам comment channel, статус не меняется, run сообщает инфраструктурную проблему
прямо и не изображает блокировку документированной в Task.

### 5.4 Доказанный успех (`verified-success`)

Current acceptance, применимые проверки, identity интегрированного result и
обязательные effects доказаны. Агент через Strategic Explainer формулирует
полученный результат, его значение, ключевое evidence и реальные ограничения,
публикует и перечитывает comment, затем переводит `In Review → Done` и
перечитывает Task.

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

## 8. Batch и Goal

Goal создаётся только для batch после exact scope resolution и до первой
non-Goal mutation. Он хранит objective, observable done criteria, verification,
authority и текущий progress. Single Goal не создаёт.

Goal не решает, сколько раз проверять Task, не определяет её status и не
превращает task-local blocker в глобальный. Пока в scope остаются `To Do`,
`In Progress`, `In Review`, rework, незавершённые effects или in-scope defect,
Goal остаётся активным.

Изолированная проблема одной Task не останавливает независимую runnable работу.
Перед ожиданием пользователя batch повторно читает полный inventory; если есть
безопасная runnable работа, агент продолжает её. Глобальный stop допустим только
когда конфликт scope/shared state/authority делает любую оставшуюся mutation
небезопасной.

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
Goal и обязательные external effects. Если есть безопасный in-scope способ
устранить gap, он делает это до handoff.

Run report начинается с результата и простым языком сообщает:

- что получилось и в каком состоянии Task/Goal;
- что доказано, а что не проверено;
- причину незавершённости, если она есть;
- какие исправления уже выполнены;
- одно точное условие или действие для продолжения.

Run report не заменяет Task comments. Batch Goal отмечается complete только
после fresh full inventory без незавершённой in-scope работы. Нельзя объявлять
skill change или distribution завершёнными при частичном выполнении project DoD.

## 11. Проверяемые сценарии

Обязательная decision-level матрица находится в
[проверке lifecycle и приёмки](../reference/shiptask-review-disposition-evaluation.md).
Она является частью current contract и должна выполняться вместе с repository
validator. Исторические ADR и датированные reports не являются fallback policy.
