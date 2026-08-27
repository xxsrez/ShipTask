# Skill source packages

Статус: current repository source model, 2026-08-27.

Документация в этом каталоге является исходным кодом runtime skills. Единица
исходного кода — отдельный skill, а не repository целиком. Поэтому требования и
архитектура разных skills не объединяются в общие нормативные документы.

## Структура

```text
docs/skills/
├── ship-tasks/
│   ├── requirements.md
│   └── architecture.md
├── task-composer/
│   ├── requirements.md
│   └── architecture.md
└── strategic-explainer/
    ├── requirements.md
    ├── architecture.md
    └── product-vision.md
```

Каждый каталог — независимый source package:

- `requirements.md` — Level 1, полный current-набор требований пользователя
  только к этому skill. Это обязательная конституция, которую нельзя ослабить
  архитектурой или runtime;
- `architecture.md` — Level 2, current инженерное решение, как именно выполнить
  локальные requirements. Это agent-owned инерционная память: её можно
  развивать и менять без пользовательского решения, пока Level 1 остаётся
  выполнен;
- дополнительные локальные документы допустимы, если помогают конкретному
  skill. Они должны быть явно классифицированы как current design, reference,
  evaluation или history и не создавать второй current Requirements или
  Architecture.

## Смысловая компиляция

```text
docs/skills/<skill>/requirements.md
                     +
docs/skills/<skill>/architecture.md
                     ↓
 <skill>/SKILL.md + runtime references + metadata
                     ↓
        observable behavior and evidence
```

Компилятор здесь стохастический: разные корректные формулировки runtime
допустимы. Но если удалить сгенерированный runtime skill и заново собрать его
только из локальных Requirements и Architecture, должен получиться примерно тот
же contract — семантически эквивалентный по обязательным outcomes, boundaries и
выбранным архитектурным решениям.

Level 1 отвечает на вопрос «что обязательно должно быть истинно». Level 2 —
«как мы сейчас это обеспечиваем». Runtime package обязан компактно донести
исполняющему агенту оба уровня, но при конфликте Requirements всегда сильнее
Architecture и runtime.

Strategic Explainer использует progressive disclosure: внешний client передаёт
только semantic request, `SKILL.md` реализует facade/admission, а полный provider
contract находится в runtime reference и загружается только admitted fresh
subagent. Совокупность этих файлов, а не один `SKILL.md`, является его Level 3.

Изменение цели, инварианта или пользовательской границы сначала меняет локальный
`requirements.md`. Изменение способа достижения при сохранённой цели меняет
локальный `architecture.md`. После этого пересобираются runtime и применимые
evaluations. Требование нельзя молча удалить ради упрощения runtime; неумение
текущей реализации его выполнить является compilation gap.

## Независимость skills

Каждый source package должен быть понятен и пригоден для пересборки без чтения
Requirements другого skill. Интеграция с соседним skill описывается как явный
локальный interface или dependency, а не как смешанный общий contract. Shared
ADR, reports и repository references могут объяснять историю или packaging, но
не добавляют скрытых current требований.

Plugin — общий distribution artifact, собранный из независимых runtime skills.
Общие manifest, installation и byte-identity правила допустимы на repository
level, однако plugin packaging не объединяет source contracts и не меняет
границы отдельных skills.

## Current packages

- [`$ship-tasks`](ship-tasks/requirements.md) —
  [Architecture](ship-tasks/architecture.md).
- [`$ship-tasks:task-composer`](task-composer/requirements.md) —
  [Architecture](task-composer/architecture.md).
- [`$strategic-explainer:strategic-explainer`](strategic-explainer/requirements.md) —
  [Architecture](strategic-explainer/architecture.md) и
  [product vision](strategic-explainer/product-vision.md).
