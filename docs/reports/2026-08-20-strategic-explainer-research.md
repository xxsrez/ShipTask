# Strategic Explainer: исследование подходов

Статус: completed research, 2026-08-20.

## Краткий вывод

Готового компонента с тем же contract не найдено. Существующие решения обычно
покрывают только одну часть задачи: изолируют контекст субагента, упрощают язык,
формируют executive summary или структурируют handoff. Для Strategic Explainer
нужно соединить эти идеи и сохранить более строгую границу: он переводит
подтверждённые факты в пользовательский смысл, но не получает authority,
не принимает решения и не превращает гладкий текст в новое evidence.

Приняты четыре основные идеи:

1. отдельный свежий context для bounded synthesis;
2. один главный вывод в начале и только decision-relevant детали после него;
3. явное разделение сценариев, epistemic state и конкретного следующего шага;
4. независимые проверки factual fidelity и понятности.

## Метод

Исследование охватывало официальную документацию agent platforms, работы о
long-context поведении, стандарты и практики clear communication, медицинские
handoff frameworks, human-AI interaction guidance, академические работы о
переводе технических отчётов и доступные open-source agent skills.

Это landscape review, а не систематический обзор. Наличие существующего
решения проверялось по публичным источникам; отсутствие точного аналога нельзя
считать доказанным исчерпывающе. Выводы применяются как design evidence и
должны подтверждаться собственными regression cases.

## Что подтвердилось

### Свежий bounded context полезен для синтеза

Официальная документация Codex называет накопление нерелевантной истории
`context pollution` / `context rot` и рекомендует выносить шумную работу в
субагентов, которые возвращают компактный результат. OpenAI отдельно отмечает,
что focused context уменьшает interference, а multi-agent pattern стоит
применять для ограниченных самостоятельных задач. Anthropic описывает тот же
паттерн: специализированные субагенты работают в чистом context, а lead agent
синтезирует результат.

Это поддерживает свежий Strategic Explainer, но не доказывает, что отдельный
model run нужен всегда. Для простого результата в одну-две фразы overhead выше
пользы.

Источники:

- [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [OpenAI Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent)
- [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)

### Основной агент должен владеть финальным ответом

OpenAI различает handoff, где specialist принимает разговор, и manager-style
orchestration, где центральный агент вызывает специалиста как bounded tool и
сохраняет контроль над итоговым ответом. Strategic Explainer соответствует
второму варианту: specialist возвращает communication artifact, а основной
агент сверяет его с evidence, принимает решения и отвечает пользователю.

Источник: [OpenAI: Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration).

### Понятность начинается с главного сообщения и действия

CDC Clear Communication Index предлагает определить аудиторию и behavioral
objective, поместить одно главное сообщение в начало, отделять need-to-know от
nice-to-know, объяснять необходимые незнакомые термины и ясно сообщать, что
известно и неизвестно. Это близко к задаче Strategic Explainer, хотя CDC
создавался для public-health материалов, а не для agent handoff.

Отсюда приняты:

- `Reader purpose` во входном brief;
- главный вывод в первых 1–3 предложениях;
- need-to-know filter для каждой детали;
- jargon triage: заменить, один раз объяснить или удалить;
- конкретное действие и наблюдаемый результат, если действие пользователя
  действительно нужно.

Источник: [CDC Clear Communication Index User Guide](https://www.cdc.gov/ccindex/pdf/clear-communication-user-guide.pdf).

Текущая OpenAI model guidance формулирует совместимый concise contract:
сохранять conclusion, evidence, caveat и next action, сокращая вступления,
повторы и background. Она также рекомендует отвечать прямо и признавать
конкретную проблему без generic reassurance. Это дополнительно поддерживает
outcome-first форму и запрет превращать brief в вежливый process diary.

Источник: [OpenAI Model guidance](https://developers.openai.com/api/docs/guides/latest-model).

### Объяснение должно показывать основание и последствия

Microsoft Guidelines for Human-AI Interaction рекомендуют показывать только
контекстно-релевантную информацию, ясно сообщать возможности системы,
объяснять, почему система дала конкретный результат, и делать понятными
последствия действий пользователя. Для Strategic Explainer это не означает
раскрывать внутренний chain of thought. Практический вывод уже уже: назвать
evidence basis на достаточном уровне, объяснить реальную причину user request и
указать observable next state.

Источник: [Microsoft Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf).

ISO 24495-1 подтверждает применимость plain-language principles к большинству
языков и типам документов, включая technical writing. Полный стандарт не был
предоставлен в открытом виде, поэтому этот проект не заявляет соответствие ISO
и использует только доступный общий принцип.

Источник: [ISO 24495-1:2023 Plain language](https://www.iso.org/standard/78907.html).

### Структурированный handoff полезен, но жёсткий шаблон — нет

Clinical handoff frameworks SBAR и I-PASS разделяют ситуацию, assessment,
action list, contingencies и receiver synthesis. Полезная для нас часть —
передавать не process diary, а compact situation model и следующий шаг.
Однако AHRQ отмечает смешанные результаты SBAR и преимущество адаптированных к
контексту инструментов в некоторых сценариях. Поэтому Strategic Explainer не
копирует клинический шаблон и не заполняет секции механически.

Источник: [AHRQ PSNet: Handoffs](https://psnet.ahrq.gov/primer/handoffs).

### Точность и читаемость нужно оценивать отдельно

Работа о patient-friendly medical reports рассматривает близкую трансформацию:
технический отчёт нужно сделать понятным неспециалисту, не потеряв факты. В
небольшом domain-specific исследовании multi-agent/reflection workflow улучшил
accuracy и readability. Размер и предметная область не позволяют переносить
результаты напрямую, но поддерживают архитектурный вывод: красивый текст не
является проверкой factual fidelity.

Отсюда принята двунаправленная проверка:

- forward trace — каждое утверждение User Brief имеет опору во входе;
- reverse coverage — каждый decision-relevant факт входа сохранён либо
  осознанно исключён как не влияющий на понимание, решение или действие.

Источник: [Agentic LLM Workflows for Generating Patient-Friendly Medical Reports](https://arxiv.org/abs/2408.01112).

### Существующие skills подтверждают отдельные паттерны

Open-source skills уже реализуют plain-language rewrite, executive summaries и
stakeholder communication. В них повторяются полезные приёмы: определить
starting knowledge аудитории, найти load-bearing idea, убирать jargon и
технические подробности, не влияющие на решение. AutoGen Society of Mind также
показывает precedent для отдельной стадии подготовки финального ответа после
внутренней multi-agent работы.

Ни один из просмотренных вариантов одновременно не обеспечивает fresh context,
structured evidence input, no-authority boundary, scenario-level epistemic
state, concrete user dependency и parent-owned final answer.

Источники:

- [Plain Language skill](https://github.com/arjunprabhulal/agent-skills/blob/main/skills/docs/plain-language/SKILL.md)
- [Plain Writing skill](https://github.com/docwriter-org/plain-writing-skill)
- [AI for Engineering Leaders](https://github.com/shiphrahx/AI-for-engineering-leaders)
- [AutoGen Society of Mind Agent](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/contrib/society_of_mind_agent/)

## Принятые изменения

### Input contract

- Добавить `Reader purpose`: что человек должен понять или суметь сделать после
  чтения.
- Для material или multi-scenario случаев передавать scenario ledger:
  ожидаемое видимое поведение, состояние `VERIFIED | FAILED | UNVERIFIED |
  NOT_APPLICABLE`, evidence basis, impact и подтверждённый needed input.
- Для пользовательского действия передавать actor, минимальное действие,
  наблюдаемый success signal и причину, почему основной агент не может закрыть
  сценарий сам.
- При полноценном brief запрещать субагенту собирать дополнительный context:
  недостающие факты возвращаются в `PARENT NOTES`.

### Transformation contract

- Сначала найти один load-bearing user message.
- Оставлять detail только если он меняет понимание outcome, impact/risk,
  required action или confidence.
- Разделять failure, unverified и not applicable на уровне каждого сценария.
- Технический термин заменить, один раз объяснить или удалить.
- Не упоминать внутреннюю orchestration и самого Strategic Explainer в
  пользовательском сообщении.

### Output and verification

- Первые 1–3 предложения сообщают итог, impact и наличие действия пользователя.
- Action contract содержит actor, конкретное действие, зачем оно нужно и
  наблюдаемый следующий результат.
- Проверять forward trace и reverse coverage отдельно от readability.
- Закрепить regression cases и критические gates в отдельном
  [evaluation contract](../reference/strategic-explainer-evaluation.md).

## Что сознательно не принято

- **Полная история разговора или execution log.** Она разрушает bounded context
  и переносит tactical framing в новый агент.
- **Жёсткий SBAR/I-PASS output template.** Он полезен как источник полей, но
  механическое заполнение создаёт лишний текст и плохо подходит разным
  пользовательским ситуациям.
- **Отдельный reviewer-subagent на каждый ответ.** Сначала достаточно
  deterministic self-audit и regression evals; второй model run добавится
  только при подтверждённой пользе.
- **Обязательная визуализация.** Она нужна лишь когда несколько акторов,
  сценариев или состояний действительно труднее понять линейно.
- **Plugin-defined native custom agent.** Текущий Codex contract размещает
  custom agents в personal или project configuration, а plugin architecture
  распространяет skills и MCP components. Поэтому переносимый вариант остаётся
  built-in `default` субагентом, который применяет sibling-skill.
- **Самостоятельный ответ Explainer пользователю.** Это превратило бы
  communication helper в decision owner и разорвало проверку с исходным
  evidence.

## Ограничения и следующий шаг

Research sources описывают общие agent и communication patterns, но не
доказывают качество именно этого contract. Следующий уровень evidence —
регрессионные сценарии с независимой оценкой, а затем реальные user tests:
получателю показывают brief один раз и проверяют, может ли он верно назвать
итог, границу, нужное действие и ожидаемое продолжение без дополнительного
уточняющего prompt.
