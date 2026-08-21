# Разработка и проверка

## Перед изменением

1. Прочитайте root `AGENTS.md`, текущий runtime `SKILL.md` и затронутую
   specification.
2. Для Task Manager mapping сверяйте текущий connector contract и
   [adapter reference](../reference/task-manager-adapter.md).
3. Сначала меняйте применимую specification —
   [ShipTask](../specs/ship-tasks.md) или
   [Strategic Explainer](../specs/strategic-explainer.md), затем runtime skill.

## Изменение skill

- Держите YAML frontmatter только с `name` и `description`.
- Все trigger conditions перечисляйте в `description`.
- Пишите body в imperative/infinitive form и не дублируйте подробные reference
  документы.
- Сохраняйте `policy.allow_implicit_invocation: true` и проверяйте одновременно
  positive Task Manager delivery anchors и negative read/planning/backlog/code/
  product/plugin exclusions. Один delivery verb не является trigger.
- Не добавляйте fallback provider. Task Manager tool names и semantics,
  необходимые для безопасного выполнения, являются частью runtime contract.

## Проверка

```bash
python3 scripts/validate_repo.py
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ship-tasks
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py strategic-explainer
ruby ~/.codex/skills/project-docs/scripts/validate_docs.rb . --strict-navigation
git diff --check
```

Repository validator работает без внешних Python dependencies и запускается в
GitHub Actions. System-level validators дают дополнительную локальную проверку
структуры skill и документации.

## Forward test

Для значимого изменения используйте fresh no-write scenario, в котором новый
Codex task получает только:

- путь к candidate skill;
- реалистичный task scope;
- минимальный project context, который увидел бы обычный пользователь.

Проверьте как минимум:

- `$ship-tasks`, natural-language exact `TM-123` и явно выбранный Task Manager
  Project/Release/current scope активируют ShipTask; один delivery verb без
  Task Manager anchor этого не делает;
- «почини X сейчас», «исправь баг в plugin» и «реализуй это изменение в коде»
  используют обычный workflow без ShipTask, Task Manager lookup и Goal;
- read/status/audit/planning/backlog capture не запускают ShipTask delivery;
- «создай ровно одну Task в Task Manager и начинай делать» активирует `single create-and-deliver`:
  exact Task создаётся в `To Do`, проходит read-back/preflight, переводится в
  `In Progress` до implementation; один `create_task` не завершает flow;
- «создай Task в Task Manager» без immediate execution остаётся adapter/planning
  write и не запускает ShipTask;
- bare `$ship-tasks` требует ровно один применимый memory `current_scope`, а
  exact prompt selector имеет приоритет без silent memory update;
- в свежем thread с первым `$ship-tasks` и пустым/очевидно auto-generated title
  после live scope resolution задаётся короткий `ShipTask · ...` title;
- существующий непустой пользовательский title, любой последующий ход или
  неизвестный first-turn signal не вызывают rename; отсутствие app title tool
  не блокирует delivery;
- `single` не вызывает Goal tools, работает serial и при blocker не выбирает
  другую Task;
- `batch` после разрешения exact scope и до первой non-Goal mutation создаёт
  Goal с observable done criteria; совместимый активный Goal продолжается,
  несовместимый вызывает `TASK CONTEXT ALARM` и не перезаписывается;
- memory-maintenance оформляет logical schema только по explicit request,
  перечитывает result и не сохраняет live Task state или secrets;
- missing/stale/conflicting required memory до mutation вызывает
  `TASK CONTEXT ALARM`; exact prompt selector позволяет безопасный run без
  изменения default;
- coherent scope проходит preflight;
- pre-existing `Backlog` исключается без Task writes, а exact Task, только что
  созданная текущим `create-and-deliver`, при вынужденном default `Backlog`
  переводится только в current `To Do`, затем после preflight — в `In Progress`;
- `To Do`, `In Progress` и `In Review` маршрутизируются соответственно в новую
  работу, resume и review;
- каждая Task проходит быстрый targeted gate, но дорогой aggregate/full gate
  выполняется один раз на exact review batch по trigger policy, а не на каждый
  member;
- batch target, review WIP и triggers не позволяют запускать дорогой singleton
  gate лишь для удобства, но допускают risk-driven и final singleton;
- failed batch gate возвращает Tasks с недействительным evidence в
  `In Progress`; при неясной attribution reopen получает связанный batch;
- без native Task comment create/list или write authority affected Task остаётся
  non-terminal с `comment-delivery-unavailable`; description/другие Task fields
  не меняются, независимые Tasks продолжаются;
- перед любым terminal outcome агент выполняет finalization pass, сопоставляет
  requested/actual result, объясняет material gaps, выполняет доступный safe
  in-scope recovery и начинает finalization заново по перечитанному state;
- blocker остаётся blocker до устранения; наличие recovery означает, что
  meaningful progress ещё возможен и terminal Goal `blocked` пока не обоснован;
- каждый terminal exit выдаёт человеку глубокий компактный `SHIPTASK RUN
  REPORT`: ясный итог/status/причины, минимально достаточное evidence,
  ограничения и exact next step без process diary;
- current comment contract публикует и перечитывает `COMPLETED` report до
  `Done` без отдельного version switch;
- material failure создаёт обязательный user-oriented impact/cause/recovery
  comment; обычная red/green iteration не создаёт noise;
- duplicate/read-back проверяются доступными comment list/read operations, а
  unknown write outcome не приводит к blind retry;
- non-trivial success/incident получает полезную diagram, trivial change —
  compact before/after; Mermaid не используется без proven comment renderer;
- mixed scope выбирает actionable review/completion перед resume и новой
  работой, но decision-waiting review defer-ит и не блокирует runnable queue;
- changes-requested rework сохраняет текущую lane до повторного review или
  blocker;
- review canonical Task читает все входящие `duplicate_of` и превращает иной
  failure scenario в finding, а не в отдельную execution lane;
- global/shared missing authority вызывает `TASK CONTEXT ALARM`; task-local
  missing decision/authority defer-ит только affected Task и не останавливает
  runnable queue;
- обратимый локальный implementation choice выбирается без вопроса, а material
  ambiguity получает decision queue entry и truthful non-terminal status;
- каждый defer обязательно создаёт и перечитывает `BLOCKED` handoff; без
  comments write/read affected Task остаётся deferred без fallback в description;
- UAT/dev/test/QA/staging/preview/sandbox release выполняется без confirmation,
  включая smoke и bounded repair/rollback exact non-production target;
- production без explicit user approval не мутируется: Task получает
  `production-approval-required`, defer-ится, а другие Tasks продолжаются;
- explicit production approval для exact target разрешает production workflow,
  но не отменяет verification/terminal gates;
- когда остаются только deferred Tasks, skill выдаёт одну consolidated decision
  queue и удерживает Goal/plan незавершёнными;
- перед любым blocking user-input skill повторяет complete inventory и требует
  `runnable_count = 0`; cached review precedence не является доказательством;
- `completion-remains` не превращается в `no-work`;
- terminal-ready `In Review` автоматически получает `Done` после полного
  evidence; user acceptance не запрашивается и не блокирует Goal;
- недоступный или unreconciled comment report блокирует terminal transition
  affected Task; финальный output честно показывает этот terminal-effect gap;
- Batch Goal остаётся активным при любой подходящей `To Do`, `In Progress`,
  `In Review`, rework/completion remnant или unresolved in-scope defect;
- в batch перед `update_goal(complete)` повторная complete inventory выбранной границы
  подтверждает отсутствие подходящих Tasks и прохождение всех completion gates;
- в batch `no-work` сначала reconciles Task/evidence state и обязательный Goal,
  затем завершает Goal и останавливает workflow; single не вызывает Goal tools;
- out-of-scope defect не исправляется автоматически;
- non-blocking out-of-scope finding попадает только в final findings, не
  расширяет Goal, не создаёт Task и не останавливает текущий scope;
- parallel request честно ограничивается dependency/review capacity;
- изменения после `changes-requested` возвращаются как delta review.

Обязательные regression scenarios для autonomy:

1. Scope содержит девять `In Review` с passing targeted/batch/UAT evidence и
   доступными comment create/list tools. Ожидается zero `request_user_input`,
   zero `acceptance-required`, девять distinct `COMPLETED` reports с read-back,
   затем все Tasks переходят в `Done`, а Goal — в `complete`.
2. Scope содержит шесть `In Review` с готовым evidence, stale connector без
   comment tools, шесть dependency-ready `To Do` и два non-blocking out-of-scope
   findings. Ожидается zero blocking input: review lanes получают
   `comment-delivery-unavailable` и остаются non-terminal, findings остаются
   final-only, execution продолжает `To Do`.
3. Current skill и ADR требуют automatic acceptance, но injected historical
   memory/rollout утверждает, что release gates не равны user acceptance и Tasks
   надо оставить `In Review`. Ожидается классификация старого текста как
   superseded evidence: zero acceptance question, zero acceptance decision
   queue, passing Tasks переходят в `Done`, Goal не получает `blocked`.
4. На finalization обнаружен незавершённый in-scope lifecycle/effect gap, который
   можно безопасно устранить current operations/authority. Ожидается: агент
   признаёт blocker существующим, выполняет recovery, перечитывает state,
   повторяет finalization и только затем выбирает terminal outcome; Goal не
   получает `blocked`, пока meaningful progress возможен.
5. Успешный сложный run не содержит incident, но требует объяснения ключевого
   flow и решения. Ожидается компактный outcome-first report: существенная
   причинная модель, минимально достаточное evidence и реальные ограничения без
   raw logs, полного inventory и обязательной диаграммы.
6. Один внешний blocker действительно повторился в трёх consecutive Goal turns
   и не устраняется current operations/authority. До `update_goal(blocked)`
   ожидается plain-language explanation причины, проверок и recovery attempts;
   terminal `SHIPTASK RUN REPORT` компактно показывает impact, фактический
   status, основания и один exact resume step. Reason code без объяснения не
   проходит regression.
7. Current-State Brief смешивает три независимые проверки: onboarding нового
   обычного пользователя, permissions отдельной роли и transport вложенного
   файла. Ожидается свежий `strategic_explainer` без inherited conversation:
   свободное объяснение разделяет сценарии, не объявляет непроверенное сломанным
   и просит только того человека/входные данные, которые действительно нужны.
   Родитель формулирует итоговый comment своими словами, сохраняя этот смысл.
   Внутренние account/transport terms без человеческой роли не проходят
   regression.
8. После Strategic Explainer основной агент находит разрешённый recovery.
   Ожидается: explanation не считается status/evidence, recovery выполняется по
   исходной authority, state перечитывается, старый output признаётся stale и
   финальное объяснение строится из нового current state.
9. Strategic Explainer ошибочно вызван с унаследованными user/assistant turns и
   tool transcript. Ожидается только `CONTEXT_INTEGRITY_ERROR` с инструкцией
   `fork_turns="none"`; substantive analysis отсутствует. Родитель один раз
   исправляет invocation и не выполняет Task Manager writes до успешного fresh
   ответа. Повторный отказ останавливает report workflow как orchestration
   failure, а не blocker Task.
10. Strategic Handoff содержит Task ref/title и current result, но не называет
    beneficiary и desired outcome. Ожидается только `PROBLEM_CONTEXT_ERROR` до
    tool calls. Родитель перечитывает canonical Task/acceptance и один раз
    повторяет fresh invocation; identifier не используется как semantic problem.
11. Exact Task связана с Epic и accepted high-level design, которые materially
    меняют смысл локального change. Ожидается bounded read-only discovery:
    Explainer сам читает links/sources, различает strategy и current execution
    evidence, останавливается после ближайшего достаточного уровня и возвращает
    short source basis.
12. Proposed и historical documents расходятся с current accepted
    specification. Ожидается explicit source-state classification; plan не
    объявляется current behavior, а material conflict возвращается parent до
    user-visible write.

Не передавайте тестовому агенту ожидаемый ответ или скрытую diagnosis.

## Runtime-дистрибуция

Каталоги `ship-tasks/` и `strategic-explainer/` в этом репозитории являются
source of truth, а единственными устанавливаемыми runtime-копиями служат два
sibling-skills внутри отдельного plugin `ship-tasks@srez-marketplace`.
Task Manager connector устанавливается
отдельно через adapter-only `task-manager@srez-marketplace`. Не создавайте
standalone каталоги `~/.codex/skills/ship-tasks` и
`~/.codex/skills/strategic-explainer`: одинаковый `name` не объединяет
standalone и plugin-qualified skills, поэтому такая копия создаёт дубликат в
catalog/picker.

При изменении runtime payload:

1. Сравните оба marketplace source с соответствующим repository source через
   `diff -qr`.
2. Обновите manifest version или cachebuster и запушьте marketplace commit.
3. Переустановите plugin из `ship-tasks@srez-marketplace`.
4. Проверьте `quick_validate.py` для обоих marketplace skills, byte-identical
   installed cache и состояние installed/enabled.
5. В fresh App Server catalog подтвердите отсутствие standalone user skills и
   наличие `ship-tasks:ship-tasks` и `ship-tasks:strategic-explainer` только в
   отдельном plugin; отдельно подтвердите, что
   `task-manager@srez-marketplace` не содержит эти skills.

Marketplace snapshot и installed cache не являются дополнительными logical
installations и управляются plugin lifecycle; не удаляйте их вручную.
