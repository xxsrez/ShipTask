# Strategic Explainer Fast: архитектура

Статус: current Level 2, 2026-08-27.

Этот документ описывает один current способ выполнить
[требования `SEF-*`](requirements.md). Он принадлежит только
`$strategic-explainer-fast:strategic-explainer-fast` и не меняет архитектуру
обычного Strategic Explainer.

## 1. Архитектурный выбор

Fast выполняет объяснение текущим агентом в существующем conversation context.
Он не создаёт subagent и не пытается очистить inherited turns. Вместо
контекстной изоляции используется явная смысловая изоляция:

1. выделить одну publication unit и исходный вопрос;
2. разрешить exact scope и read-only anchors;
3. считать authoritative только current sources, а не process diary;
4. построить сообщение заново из evidence map;
5. проверить понимание отдельным in-context pass;
6. вернуть publication body отдельно от source basis.

Это осознанный cost/latency trade-off. Требования к понятности, полноте
значимого смысла, честности и authority не ослабляются, но Fast не заявляет
независимость либо stateless-гарантию обычного provider-subagent.

## 2. Runtime package

Runtime состоит из трёх частей:

- `strategic-explainer-fast/SKILL.md` — trigger, admission, запрет subagent и
  короткий execution protocol;
- `strategic-explainer-fast/references/in-context-contract.md` — полный метод
  discovery, causal reconstruction, language cleanup, source separation и
  comprehension gate;
- `strategic-explainer-fast/agents/openai.yaml` — catalog metadata и qualified
  default prompt.

Progressive disclosure здесь экономит обычный context, а не скрывает expertise
от caller. После admission текущий агент обязан полностью прочитать reference и
сам применить его к одному result.

## 3. Admission и publication unit

Skill принимает один готовящийся человеку comment, Task/scope report, material
state or decision explanation, blocker report, final или явную редактуру.
Routine chat, progress, внутренний draft, mutation и authority decision не
активируют provider.

Admission устанавливает исходный вопрос, exact scope и resolvable read-only
anchors. Смешанные publication units разделяются. Неоднозначный mandatory input
получает честный gap, а не inferred goal. Target text допустим как вход только
при явной задаче редактировать именно его.

## 4. Context firewall без очистки context

Inherited history остаётся физически доступной, поэтому Fast применяет
логический firewall:

- current authoritative source сильнее старого вывода и tool narration;
- candidate, caller summary и remembered state являются locator hints, но не
  evidence;
- proposed, accepted, historical и observed state различаются;
- scope не расширяется найденной стратегией;
- process chronology не попадает в publication только из-за доступности;
- changed facts или scope запускают новый проход из источников.

Этот firewall не называется независимой проверкой. Behavioral evaluation
поэтому отделяет generation от последующей независимой оценки внешним trial,
когда такая оценка требуется для release evidence.

## 5. Discovery и evidence map

Discovery начинается с exact target и поднимается к materially relevant
relations, parent/Epic, Release, Project, product goal, current specification и
accepted decisions. Поиск прекращается, когда следующий слой уже не меняет
problem, outcome, impact/risk, action или confidence.

Во внутренней evidence map фиксируются:

- исходный вопрос, beneficiary и desired observable outcome;
- доказанные, failed, unverified, unknown и not-applicable facts;
- отдельные scenario states, inputs, dependencies и impacts;
- current authority/safety boundary;
- material source refs.

Evidence map не является шаблоном ответа и не публикуется как журнал.

## 6. Reader model и reconstruction

Сначала Fast формулирует без внутренних identifiers одну причинную мысль,
которую должен восстановить читатель. Publication строится из этой reader model,
а не сокращением технического отчёта.

Первый слой отвечает, что получилось или остановилось и почему это важно.
Второй появляется только при необходимости и добавляет material cause, одно
действие, boundary или success signal. Разные сценарии объединяются только без
потери различающихся input, result, state, impact или essential path step.

Редакторский режим сохраняет неизменяемое смысловое ядро: facts, goals,
requirements, exact identifiers, relations, constraints, exceptions,
prohibitions, acceptance, authority/safety/privacy boundaries и uncertainty.
Структура может быть перестроена, смысл — нет.

## 7. Human-language и audit redaction

Внутренние сущности сначала переводятся в человеческие роли. Латиница и exact
names остаются в body только когда читателю нужно увидеть, найти или выбрать
именно их. SHA, deployment/request IDs, внутренние ревизии, gates и технические
статусы по умолчанию уходят в source basis.

Отдельный audit-redaction pass сравнивает publication body с raw facts и
убирает verification-only details. Удаление не должно менять reader model,
decision, action, risk или confidence.

## 8. In-context comprehension gate

Fast повторно читает только исходный вопрос и publication body и пытается без
source basis восстановить:

- что произошло;
- почему это важно;
- что доказано и неизвестно;
- что будет дальше или какое одно действие требуется.

Для materially distinct scenarios дополнительно восстанавливаются их input или
boundary, observed result и state/impact. Если это невозможно, текст строится
заново из evidence map. Этот pass не создаёт subagent и не считается
независимой reader evaluation.

## 9. Output protocol

Result содержит:

1. один самодостаточный publication-ready текст;
2. явно отделённый короткий source basis для factual verification.

Calling workflow проверяет material claims по authoritative sources и публикует
только body без второго editorial rewrite. Factual conflict исправляется через
новый focused pass с current anchors.

## 10. Authority и failure

Fast использует только read-only discovery и не выбирает scope, status,
recovery, release, authority либо mutation. Missing mandatory source,
неоднозначный scope и material conflict называются прямо. Provider failure не
разрешает придумывать facts или заявлять качество, которое не было получено.

## 11. Distribution

Fast распространяется отдельным plugin
`strategic-explainer-fast@srez-marketplace`. Plugin содержит только skill
`$strategic-explainer-fast:strategic-explainer-fast`, не включает connectors и
не встраивается в Ship Tasks, обычный Strategic Explainer или Task Manager.

Repository runtime, Marketplace source и installed cache после изменения
остаются byte-identical. Новый snapshot проверяется в fresh Codex task, потому
что уже открытый task может сохранять прежний catalog.

## 12. Трассировка требований

- `SEF-01`, `SEF-02`, `SEF-04`, `SEF-06`, `SEF-09` → admission, context
  firewall, discovery и evidence map;
- `SEF-03`, `SEF-05`, `SEF-11`, `SEF-14` → reader model, reconstruction,
  language cleanup и comprehension gate;
- `SEF-07`, `SEF-08` → action rule и read-only authority boundary;
- `SEF-10`, `SEF-15`, `SEF-16` → one-unit in-context API, no-subagent
  execution и explicit weaker isolation guarantee;
- `SEF-12` → separate generic plugin distribution;
- `SEF-13` → lossless editorial reconstruction;
- observable evidence → shared 20-case corpus и Fast-specific evaluation
  contract.

