# 0035. Semantic facade владеет invocation Strategic Explainer

Статус: принято, 2026-08-27.

Частично заменяет caller-visible invocation recipe в
[ADR-0029](0029-fresh-strategic-explainer-and-blocker-reflection.md),
[ADR-0030](0030-opaque-strategic-explainer-provider-boundary.md),
[ADR-0033](0033-terminal-provider-and-optional-shiptask-routing.md) и
[ADR-0034](0034-luna-max-for-ordinary-strategic-explainer.md). Fresh isolation,
terminal provider role, Luna Max profile, opaque provider expertise и
caller-specific fallback policies сохраняются.

## Контекст

Ordinary Strategic Explainer уже имел собственный routing skill, но ShipTask и
Task Composer всё равно повторяли способ его реализации: topology, fork,
provider profile, role lock, clean envelope и retry. Поэтому изменение provider
invocation требовало синхронных правок каждого caller-а, а смысловая dependency
выглядела как распределённый protocol вместо функции «semantic request → готовый
текст».

Отдельная опасность — методика анализа и улучшения текста. Она нужна только
независимому provider-subagent. Если эти инструкции видит вызывающий workflow
или facade router, clean fork уже не обеспечивает независимого взгляда: caller
может подготовить candidate, навязать структуру либо переписать готовый result.

## Решение

Strategic Explainer предоставляет один semantic facade
`$strategic-explainer:strategic-explainer`.

Внешний client передаёт только:

- назначение и исходный пользовательский вопрос;
- одну formulation либо explicit editing task;
- exact или однозначно bounded scope;
- язык и material constraints;
- resolvable read-only source anchors.

Внешний client не знает и не задаёт agent topology, fork mode, model/effort,
role lock, provider entrypoint, clean envelope или retry mechanics. Эти детали
существуют только в facade implementation Strategic Explainer. ShipTask, Task
Composer и другие callers не копируют их в Requirements, Architecture, runtime
skills или metadata.

Runtime разделён на три слоя:

1. Client вызывает qualified skill с semantic request и получает готовый text,
   отдельно обозначенный source basis либо operational unavailability.
2. Facade router внутри `strategic-explainer/SKILL.md` владеет clean invocation,
   provider profile, admission и единственным corrected structural retry. Он не
   читает provider contract и не улучшает текст.
3. Только admitted terminal provider читает
   `strategic-explainer/references/provider-contract.md` и знает правила
   discovery, причинного объяснения, редакторской реконструкции, языковой
   очистки и comprehension check.

Factual correction приходит новым semantic request с исправленными anchors.
Operational failure facade возвращается вызывающему workflow; ShipTask после
него использует native writing, а Task Composer сохраняет свою отдельную policy
не начинать Epic create без grounded description. Facade не выбирает fallback
за client и не переносит provider method в native path.

## Последствия

- Изменение модели, fork или admission затрагивает только Strategic Explainer.
- Callers становятся устойчивыми к внутренней эволюции provider-а.
- Вызов остаётся function-like semantic API, хотя Codex skill является
  instruction facade, а не детерминированной математической функцией.
- Provider expertise не попадает ни во внешний client context, ни в facade
  router instructions до terminal admission.
- Отсутствие plugin-а и user opt-out сохраняют policies конкретного caller-а.

## Проверка

- repository validator запрещает invocation markers во всех caller contracts;
- тот же validator запрещает provider-method markers и в callers, и в facade;
- runtime tests подтверждают, что только Strategic Explainer package содержит
  invocation recipe, а только provider contract содержит text-improvement
  method;
- behavioral smoke даёт агенту только semantic request и наблюдает fresh
  terminal provider с готовым result без ручных invocation parameters;
- source, Marketplace package и installed cache проверяются на byte identity, а
  новый snapshot — в fresh Codex session.
