# Strategic Explainer Fast: product vision

Статус: current product vision, 2026-08-27.

Нормативный контракт находится в [Requirements](requirements.md), способ
достижения — в [Architecture](architecture.md). Этот документ объясняет, зачем
Fast существует как отдельный продукт.

## Проблема

Обычный Strategic Explainer даёт сильную clean-context гарантию: каждый текст
строит новый stateless subagent. Практические тесты показали резкий рост
понятности, но отдельный agent invocation заметно увеличивает token cost и
latency даже тогда, когда текущий агент уже имеет все факты и способен
сфокусироваться на одном publication result.

Нужен честный способ проверить более дешёвую гипотезу, не ослабляя обычный
provider и не подменяя эксперимент скрытым изменением его контракта.

## Product bet

Те же требования к user-facing outcome можно попытаться выполнить в текущем
context, если skill явно:

- отделяет current sources от process history;
- строит reader model заново, а не редактирует старый technical candidate;
- выполняет language и audit-redaction passes;
- проверяет понимание по готовому body;
- не выдаёт self-review за независимую оценку.

Fast делает именно этот bet. Его ценность — похожая понятность с меньшими
расходами на orchestration и context replay.

## Почему отдельный plugin

Fast не является «режимом» обычного Explainer. Их isolation guarantees
несовместимы: обычный provider обязан быть fresh и opaque, Fast обязан работать
in-context без subagent. Отдельные skills, Requirements, Architecture,
evaluation и Marketplace packages позволяют пользователю выбрать вариант
установкой и сравнивать их без скрытой конфигурации.

Обычный Strategic Explainer остаётся контрольным вариантом и не меняется.

## Обещание пользователю

Fast стремится дать тот же observable результат:

- главная мысль понятна без внутренних IDs и англоязычного смыслового каркаса;
- material facts и различия сценариев не потеряны;
- граница знания честна;
- действие конкретно только при реальной dependency;
- publication body отделён от source basis;
- skill ничего не решает и не изменяет за calling workflow.

Fast не обещает независимость от caller framing, stateless context или слепую
reader-проверку. Эти различия должны оставаться видимыми в документации и
evaluation reports.

## Выбор и rollback

Пользователь выбирает Fast установкой отдельного plugin. Интегрированный caller
может предпочесть Fast по live catalog и использовать обычный Explainer только
когда Fast отсутствует. Для одного текста нельзя незаметно прогонять оба
варианта: иначе стоимость и интерпретация эксперимента становятся ложными.

Rollback прост и наблюдаем: отключить или удалить Fast plugin. Обычный
Strategic Explainer продолжает существовать независимо.

## Success criteria

Гипотеза считается перспективной, если Fast:

1. проходит тот же semantic 20-case portfolio без case-specific hints;
2. не допускает material factual loss, hybrid language и audit leakage;
3. не создаёт subagent во время generation и self-review;
4. показывает materially меньший token cost/latency на сопоставимых trials;
5. не меняет ordinary provider и позволяет чистый availability-based rollback.

Предварительный self-review может подтвердить feasibility, но release-quality
сравнение требует blind generation и независимой оценки, отделённой от Fast
runtime.
