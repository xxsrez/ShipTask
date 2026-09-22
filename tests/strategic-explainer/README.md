# Model-forward tests Strategic Explainer

Эти fixtures проверяют не совпадение с эталонной фразой, а способность
`$strategic-explainer:strategic-explainer` превратить сырой технический след в
понятный человеку текст. Все продуктовые события здесь синтетические. Текущие
fixtures используют две технические предметные области как сложный материал,
но не задают границу общего skill и не являются утверждением о фактическом
состоянии какой-либо системы.

## Структура case

Каждый case содержит два изолированных входа:

- `facts.md` — единственный fixture, доступный generating subagent;
- `rubric.md` — semantic gate для отдельной оценки готового текста.

Generating subagent не получает rubric, diagnosis, intended wording, прежний
плохой комментарий или candidate другого trial. Он запускается новым built-in
`default` subagent с `fork_turns="none"`, `model="gpt-5.6-luna"` и
`reasoning_effort="max"`; compact task содержит отдельную точную строку
`STRATEGIC_EXPLAINER_PROVIDER_V1`, одну publication task и anchor на один
`facts.md`. Router выбирает terminal provider path, provider-only entrypoint
выполняет admission, после чего subagent возвращает publication text и отдельно
обозначенный source basis.

Это white-box evaluation harness: он намеренно знает внутренний invocation
recipe, чтобы проверить released implementation. Любой delegated или direct
client этих параметров не получает и вызывает только semantic facade.

## Facade topology regression

Отдельный smoke проверяет не качество текста, а способ запуска provider-а.
Основной coordinator с top-level collaboration surface вызывает semantic
facade, после чего orchestration metadata должна показать built-in
child/subagent с parent link и agent path внутри текущей Codex task. В журнале
не должно быть `create_thread`, отдельной projectless task, новой
пользовательской session или нового элемента боковой панели.

`collaboration.spawn_agent` вызывается как прямой top-level tool. Его отсутствие
в `ALL_TOOLS` внутри `functions.exec` не считается отсутствием capability.
Worker trial возвращает coordinator-у только facts/evidence/anchors, после чего
facade вызывает coordinator, а не worker. Если facade запущен внутри built-in
child без namespace `collaboration` или direct child spawn действительно
недоступен, ожидается operational unavailability без app-level fallback,
parent messaging и отдельной task/session.

Evaluator получает исходный `facts.md`, соответствующий `rubric.md`, publication
text, source basis и общий [semantic gate](common-rubric.md). Он отдельно проверяет factual coverage и человеческое
понимание. Формулировка может отличаться между trials; `PASS` требует, чтобы
читатель понял, что именно проверено, при каком значимом входе или границе, что
наблюдалось и готов ли результат к следующему состоянию.

Evaluator — отдельный test-harness agent, а не часть runtime provider-а. Provider
не вызывает evaluator, не создаёт child agents и выполняет только внутренний
comprehension check перед возвратом result.

## Cases

Suite содержит ровно 31 materially different cases. Двадцать пять используют
две реалистичные технические предметные области как сложный материал, а шесть
общих case проверяют текст вне конкретного проекта. Они являются
примерами применения общего контракта, а не специализацией Explainer. Первая
группа покрывает размер и тип файлов, persistence после
переиздания, concurrent edits, idempotent retry, current access к истории,
write rebind, automatic capture, повторную выдачу приглашения и перенос
ownership. Вторая покрывает ACL комментариев, role ceiling, сохранённые и
временные фильтры, recoverable deletion, атомарный массовый перенос, hierarchy
guards, idempotent edits, выпуск с незавершённой работой и
границу между зелёной локальной проверкой и провалившимся UAT. Отдельные
регрессионные cases воспроизводят перегруженный closing comment с командами,
повтор уже опубликованного доказательного следа после review, препятствие без
причинного отчёта, ложный blocker из устаревшего capability state и
остановку незавершённой работы с расплывчатой категоризацией вместо точных
причин и доступного продолжения.

Общий редакторский case воспроизводит отдельный класс сбоя: target text содержит
широкое утверждение, позднюю существенную оговорку, внутренний процесс и
служебные IDs. Он получает `PASS` только когда publication body сохраняет
предметный факт и границу знания рядом, а точный и обезличенный след подготовки
текста остаётся вне публикации.

Два других общих case проверяют объяснительный мост для незнакомого механизма,
масштаба и недоступного графика, а также отрицательную границу: аналогия не
является evidence и не должна удлинять точный экспертный ответ. Ещё три
проверяют выбор наименьшего структурного представления для существенных
отношений, отказ от декоративной визуализации в простом ответе и редакторскую
смену формы без потери порядка, владения и границ.

Матрица намеренно содержит success, expected boundary, partial result,
regression, permission denial, stale conflict, atomic rollback и blocker report.
Это не тридцать одна перефразировка одного closing comment.

## Запуск

Структура fixtures и отсутствие подсказок generator-у проверяются локально:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py'
```

Поведенческий gate выполняется через fresh Codex subagents. Для каждого case
нужен как минимум один blind generation trial и отдельная независимая оценка.
После изменения provider behavior запускаются все cases; нестабильный либо ранее
провалившийся case повторяется новым fresh trial, а не follow-up прежнему агенту.
Изменение facade routing дополнительно требует fresh topology smoke из раздела
выше; provider quality cases его не заменяют.
