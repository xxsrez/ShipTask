# 0030. Opaque provider boundary для Strategic Explainer

Статус: принято, 2026-08-26.

Уточняет [ADR-0029](0029-fresh-strategic-explainer-and-blocker-reflection.md) и
исправляет оставшуюся утечку между
[Strategic Explainer](../skills/strategic-explainer/requirements.md),
[ShipTask](../skills/ship-tasks/requirements.md) и
[Task Composer](../skills/task-composer/requirements.md).

## Проблема

`fork_turns="none"` очищал conversation нового субагента, но provider method
оставался прямо в catalog-visible `strategic-explainer/SKILL.md`, ShipTask
runtime references и caller requirements. Поэтому coordinating agent видел
правила strategic discovery, структуры объяснения и self-review и начинал сам
сокращать либо улучшать input/output. Независимость была объявлена, но не была
инкапсулирована.

## Решение

- Strategic Explainer runtime становится двухслойным.
- Catalog metadata и `SKILL.md` содержат только router и admission gate.
- Caller с рабочим context не читает provider reference: он создаёт новый
  built-in `default` subagent с `fork_turns="none"` и передаёт одну compact
  user-facing task, exact scope и resolvable read-only anchors.
- Только fresh subagent после успешного admission читает
  `references/provider-contract.md`; там живут discovery, explanation,
  comprehension и editorial expertise.
- ShipTask и Task Composer хранят только opaque client protocol. Они не пишут
  candidate, не передают strategic summary/format rules, не применяют provider
  checklist и не переписывают ready text.
- Invalid invocation и factual/source correction всегда получают новый clean
  subagent. Caller проверяет только material factual conflict по authoritative
  sources.
- User opt-out и provider unavailability не включают self-fallback. Mandatory
  comment/lifecycle effect fail-closed; обязательный final сообщает factual
  state и capability gap по собственному truth contract caller без имитации
  provider.
- Candidate blocker result остаётся reflection input ShipTask. Любой найденный
  путь всё равно проверяется по current sources/acceptance и не расширяет scope
  или authority.

## Проверка

Repository validator требует provider contract внутри Strategic Explainer
package и запрещает provider-method markers в caller runtime/references.
Behavioral evaluations отдельно проверяют router layer, admission-gated provider
load, отсутствие caller-authored candidate и отсутствие self-fallback.

## Последствия

Skill остаётся distribution package и routing surface, но сама экспертиза
исполняется только субагентом. Это согласуется с progressive disclosure skills:
видимый router выбирает роль, а подробный reference загружается только после
доказанной границы context.

## Основание платформы

- [Codex skills](https://learn.chatgpt.com/docs/build-skills) сначала
  обнаруживаются по catalog metadata, а полный instruction package загружается
  при выборе skill; поэтому metadata/router не должны содержать provider method.
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
  создаются для отдельной задачи и используются в том числе для защиты
  основного context от загрязнения; provider expertise привязана к этому fresh
  execution boundary.
