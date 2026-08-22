# 0021. Требования являются конституцией для агентов

Статус: accepted, 2026-08-22. Уточняет ADR-0017 и ADR-0018 для всех current
requirements ShipTask и Strategic Explainer. Заменяет обязательную agent
topology, fixed context isolation, exact handoff envelope, error tokens, retry
scheme и option quota из ADR-0012, ADR-0013 и ADR-0014. Также заменяет
требование обязательно вызывать Strategic Explainer для каждого comment:
обязательным остаётся качество объяснения, а не внутренний исполнитель.

## Контекст

После перехода ShipTask к constitution-first contract часть старой
оркестрации осталась нормативной. Strategic Explainer всё ещё требовал
конкретный тип свежего субагента, точный `fork_turns`, один формат handoff,
служебные error codes, специальный отказ при унаследованном context и
фиксированное число вариантов. ShipTask, в свою очередь, требовал использовать
этот механизм для каждого обязательного comment.

Эти правила описывают внутреннее устройство одного решения. Они не определяют
пользовательский результат, доказательную силу или safety boundary и мешают
агенту выбрать более подходящий способ работы при другой модели, платформе или
форме задачи.

## Решение

### Current requirements — конституция

Каждое нормативное требование должно объяснять:

- какой пользовательский или системный результат обязателен;
- почему он важен;
- по каким наблюдаемым фактам он считается достигнутым;
- какие scope, truth, safety и authority boundaries нельзя нарушать.

Агент самостоятельно выбирает план, декомпозицию, инструменты, порядок
диагностики, число попыток, делегирование, форму context и текст ответа. Examples,
reason codes и удобные структуры могут помогать, но не становятся обязательными
только потому, что однажды сработали.

### Когда допустима точность механизма

Жёсткий порядок или точный protocol остаётся только при доказуемом инварианте
целостности, безопасности или внешнего эффекта. В current contract это, в
частности:

- evidence предшествует claim о verification;
- native comment существует и перечитан до связанного существенного status
  transition;
- current version и read-back защищают Task Manager writes от потерянных или
  продублированных effects;
- explicit authority предшествует production и другим sensitive actions.

Это границы корректности внешнего состояния, а не управление тем, сколько
агентов использовать, какие tools вызвать или как организовать reasoning.
Технический adapter может описывать protocol, необходимый для безопасной работы
API, но delivery policy не превращает этот protocol в универсальный agent
script.

### Strategic Explainer определяется результатом

Strategic Explainer получает или восстанавливает достаточную постановку
реальной проблемы и current facts, при необходимости читает bounded relevant
sources без mutations и даёт problem-first объяснение. Оно сохраняет
существенные факты, различает факт, интерпретацию и unknown, показывает
пользовательский смысл и не создаёт новую authority.

Skill можно использовать напрямую, делегировать или применять его принципы в
основном workflow. Не обязательны конкретный subagent type, fresh-thread
механизм, `fork_turns`, exact handoff fields, служебный error token, число
attempts или число alternatives. Если входа недостаточно, агент ясно называет
material gap и необходимый input, не придумывая цель или факты.

ShipTask обязан получить понятный problem-first comment и run report,
соответствующие этому quality contract. Вызов sibling skill является доступным
способом улучшить результат, но не обязательным внутренним ритуалом.

### Evals проверяют наблюдаемое поведение

Current evals проверяют factual grounding, evidence, state separation,
read-only/authority boundary, понятность, incident visibility и external
effects. Они не оценивают agent topology, fork mode, точный prompt envelope,
названия внутренних этапов, tool sequence, число попыток, фиксированное число
вариантов или совпадение с эталонной формулировкой.

## Последствия

- Requirements остаются достаточно точными для проверки, но не подменяют
  инженерное решение бюрократической процедурой.
- Strategic Explainer сохраняет problem-first, grounded и read-only результат
  без зависимости от одной orchestration implementation.
- ShipTask сохраняет обязательные comments, evidence и reporting, но может
  добиться их качества подходящим способом.
- Исторические ADR и reports сохраняют прежние механизмы как историю; current
  specification, runtime skill и evaluation contract не используют их как
  fallback policy.
