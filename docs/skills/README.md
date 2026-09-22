# Skill source packages

Статус: current repository source model, 2026-09-02.

[Философия проекта](../philosophy.md) объясняет, зачем существует эта схема и
кому принадлежат решения. Здесь зафиксирована её техническая структура.

Документация в этом каталоге является исходным кодом runtime skills. Единица
исходного кода — отдельный skill, а не repository целиком. Поэтому Overview,
Requirements и Architecture разных skills не объединяются в общие нормативные
документы.

## Структура

```text
docs/skills/
├── issue-grinder/
│   ├── overview.md
│   ├── requirements.md
│   ├── architecture.md
│   └── evaluation.md
├── scope-reviewer/
│   ├── overview.md
│   ├── requirements.md
│   ├── architecture.md
│   └── evaluation.md
├── task-composer/
│   ├── overview.md
│   ├── requirements.md
│   ├── architecture.md
│   └── evaluation.md
└── strategic-explainer/
    ├── overview.md
    ├── requirements.md
    ├── architecture.md
    └── product-vision.md
```

Канонический source package содержит все три документа. В current tree
пользовательский Overview определён для Issue Grinder, Task Composer, Scope
Reviewer и Strategic Explainer. Overview остальных entities нельзя заполнять из
Requirements, Architecture или реализации: для этого нужно отдельное явное
решение пользователя.

Каждый каталог — независимый source package:

- `overview.md` — самостоятельный user-owned документ об общем смысле сущности:
  что это, для кого, зачем и какую пользу должно давать. Агент не создаёт и не
  восстанавливает отсутствующий Overview без явного разрешения пользователя;
- `requirements.md` — Level 1, полный current-набор требований пользователя
  только к этому skill. Это самостоятельный user-owned документ, который нельзя
  менять без явного разрешения пользователя;
- `architecture.md` — самостоятельный agent-owned документ с дополнительными
  инструкциями, условиями и инженерными решениями, которые помогают достичь
  цели Overview и выполнить Requirements;
- дополнительные локальные документы допустимы, если помогают конкретному
  skill. Они должны быть явно классифицированы как current design, reference,
  evaluation или history и не создавать второй current Requirements или
  Architecture.

## Смысловая компиляция

```text
overview.md     ─┐
requirements.md ├→ <skill>/SKILL.md + runtime references + metadata
architecture.md ┘                         ↓
                              observable behavior and evidence
```

Компилятор здесь стохастический: разные корректные формулировки runtime
допустимы. Но если удалить сгенерированный runtime skill и заново собрать его
из трёх самостоятельных локальных документов, должен получиться примерно тот
же contract — семантически эквивалентный по назначению, обязательным outcomes,
boundaries и выбранным архитектурным решениям.

Overview отвечает на вопросы «что это, для кого и зачем», Requirements — «что
обязательно должно быть истинно», Architecture — «какие дополнительные
инструкции и решения помогут этого достичь». Это три независимых входа, а не
слои одного документа. Runtime package обязан компактно донести исполняющему
агенту применимый смысл каждого. Architecture и runtime не могут противоречить
двум пользовательским документам; конфликт Overview и Requirements разрешает
только пользователь.

Strategic Explainer использует progressive disclosure: внешний client передаёт
только semantic request, `SKILL.md` реализует facade/admission, а полный provider
contract находится в runtime reference и загружается только admitted fresh
subagent. Совокупность этих файлов, а не один `SKILL.md`, является его Level 3.

Только явное поручение пользователя изменить Overview или Requirements
разрешает поменять соответствующий пользовательский документ. Изменение способа
достижения при сохранённых Overview и Requirements меняет локальный
`architecture.md`. После этого пересобираются runtime и применимые evaluations.
Пользовательский смысл или требование нельзя молча удалить ради упрощения
runtime; неумение текущей реализации их выполнить является compilation gap.

## Независимость skills

Каждый source package должен быть понятен и пригоден для пересборки без чтения
Overview или Requirements другого skill. Интеграция с соседним skill
описывается как явный локальный interface или dependency, а не как смешанный
общий contract. Shared ADR, reports и repository references могут объяснять
историю или packaging, но не добавляют скрытой current policy.

Plugin — общий distribution artifact, собранный из независимых runtime skills.
Общие manifest, installation и byte-identity правила допустимы на repository
level, однако plugin packaging не объединяет source contracts и не меняет
границы отдельных skills.

## Current packages

- [`$issue-grinder:consultant`](consultant/overview.md) —
  [Requirements](consultant/requirements.md),
  [Architecture](consultant/architecture.md) и
  [Evaluation](consultant/evaluation.md). Отдельный read-only советчик
  Astra/medium; существующие workflows гриндера его не вызывают.

- [`$issue-grinder`](issue-grinder/overview.md) —
  [Requirements](issue-grinder/requirements.md),
  [Architecture](issue-grinder/architecture.md) и
  [Evaluation](issue-grinder/evaluation.md); source package и repository runtime
  созданы, а installed state доказывается отдельно.
- Архив удалённого `$ship-tasks`: [Requirements](ship-tasks/requirements.md)
  и [Architecture](ship-tasks/architecture.md). Они не являются current source.
- [`$issue-grinder:scope-reviewer`](scope-reviewer/overview.md) —
  [Requirements](scope-reviewer/requirements.md) и
  [Architecture](scope-reviewer/architecture.md),
  [Evaluation](scope-reviewer/evaluation.md); source package, repository runtime
  и observable evaluation созданы, а installed state доказывается отдельно.
- [`$issue-grinder:task-composer`](task-composer/overview.md) —
  [Requirements](task-composer/requirements.md),
  [Architecture](task-composer/architecture.md) и
  [Evaluation](task-composer/evaluation.md).
- [`$strategic-explainer:strategic-explainer`](strategic-explainer/overview.md) —
  [Requirements](strategic-explainer/requirements.md),
  [Architecture](strategic-explainer/architecture.md) и
  [product vision](strategic-explainer/product-vision.md).
