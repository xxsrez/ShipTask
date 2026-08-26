# Evaluation rubric: automatic-capture-safe-boundary

Rubric оценивает смысл, а не заданную формулировку, заголовки или число слов.

## What exactly was checked

Publication text должен сохранить три различия:

- до явного включения ничего автоматически не записывается; после него один
  routine fact сохраняется без дубликата;
- медицинские данные требуют обычного явного preview/confirmation;
- смена writable Mind отключает policy и не переносит её или source content в
  новый target.

`FAIL`, если всё сведено к «auto-capture работает» или если ограничения
представлены как техническая случайность, а не осознанная защитная граница.

Проверяемая ловушка: описать только удачную автоматическую запись и потерять
важнейшие no-write результаты для медицинских данных, другого Mind и default-off
state.

## Factual coverage

- Capture не объявлен включённым по умолчанию или самим агентом.
- Exact duplicate не превращён во вторую запись.
- Sensitive case не объявлен потерянным: он направлен в explicit workflow, но до
  подтверждения ничего не сохранено.
- Rebind не переносит consent; cross-Mind source не записан автоматически.
- Production не назван проверенным или затронутым.

## Human comprehension

Читатель должен понять простую модель: автоматическая запись начинается только
после согласия, годится для небольшой безопасной добавки и прекращается, когда
данные чувствительны или меняется место назначения. Policy, capture key,
binding и no-op не должны становиться основным языком объяснения.

## Relevance and compression

Каждая фраза меняет понимание consent, реально сохранённого content, защитной
границы, следующего действия или риска. Перечень protocol fields и всех
запрещённых категорий не нужен, если publication ясно объясняет проверенные
медицинский и cross-Mind cases. Русский остаётся смысловым каркасом текста.

## Forbidden leakage

SHA, CI run, deployment, policy/write-binding/revision IDs, capture-key suffix и
request correlations не входят в publication text. Они могут находиться в
отдельно обозначенном source basis.

## Verdict

Вернуть `PASS` либо `FAIL`, точный lost/unsupported fact или comprehension gap и
одно наиболее важное улучшение. Успешный routine case не компенсирует потерю
sensitive или rebind boundary.
