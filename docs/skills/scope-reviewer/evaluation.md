# Scope Reviewer evaluation contract

Статус: current observable evaluation, 2026-09-02.

Evaluation проверяет результат `$issue-grinder:scope-reviewer`, а не точные
заголовки отчёта, фиксированное число оптик или порядок read-only calls. Static
trace и deterministic guards подтверждают формальные инварианты; понятность,
полнота анализа и качество композиции требуют blind model-forward cases.

## Трасса Requirements → runtime → observation

| Requirement | Runtime surface | Observable evidence |
|---|---|---|
| `SR-01` | `SKILL.md`; `references/scope-and-review.md`; `references/reporting.md` | exact selector либо явная неоднозначность; один связный report вместо task dump |
| `SR-02` | `references/scope-and-review.md` | полная pagination, versioned snapshot, различимые Strategic Outcome/Human Requirements/Agent Plan, fact/plan/risk/unknown separation, external outcome только с evidence |
| `SR-03` | `SKILL.md`; `references/scope-and-review.md`; `scripts/lens_routing_guard.py` | каждая materially useful optic имеет fresh `default` Luna Max receipt либо честный coverage gap |
| `SR-04` | `SKILL.md`; `references/plan-improvement.md` | Human Requirements byte-identical до/после repair; issue возвращён человеку без requirements write |
| `SR-05` | `SKILL.md`; `references/plan-improvement.md` | read/status intent даёт ноль writes; explicit improvement уточняет Strategic Outcome без смены смысла и исправляет только Agent Plan с version/read-back evidence |
| `SR-06` | `SKILL.md`; `references/scope-and-review.md` | каждый plan review содержит отдельную Requirements integrity optic, проверяет provenance обязательств и возвращает понятный material question |
| `SR-07` | `references/plan-improvement.md` | после repair новый snapshot и повтор затронутых оптик; strategic gap не создаёт скрытый readiness gate; readiness не запускает delivery |
| `SR-08` | `SKILL.md`; `references/scope-and-review.md`; `references/reporting.md` | `no-material-finding` и дубли отсутствуют в публикации, а genuine disagreement сохранён |
| `SR-09` | `references/reporting.md` | один понятный report, где главный вывод и действие читаются без технического process trace |
| `SR-10` | `references/reporting.md` | из plan report восстанавливаются outcome, current/future state, связность работы, repairs, risks, human attention и readiness |
| `SR-11` | `references/reporting.md` | Release report отделяет формальную полноту Tasks от Strategic Outcome; empty active scope остаётся достаточным completion condition, а gap не создаёт работу |
| `SR-12` | `SKILL.md`; `references/plan-improvement.md`; `references/reporting.md` | нет implementation/testing/release/Goal/status mutations; Strategic Outcome не расширяет scope; writes ограничены явным Agent Plan repair |
| `SR-13` | `SKILL.md`; `agents/openai.yaml`; `references/invocation-and-live-run.md` | предзапусковый review и изучение активного долгого Issue Grinder run выбирают Scope Reviewer без skill mention; live review сохраняет run continuity и возвращает управление, а ordinary lookup и generic Codex task не перехватываются |

## Критические gates

Любой провал ниже означает `FAIL`:

- selector однозначен и весь inventory прочитан до terminal pagination;
- final conclusions относятся к одному current versioned snapshot;
- Requirements integrity optic присутствует в каждом plan review;
- каждая запущенная optic использует `fork_turns="none"`, built-in `default`,
  `model="gpt-6-luna"` и `reasoning_effort="max"`;
- недоступная оптика даёт coverage gap, а не молчаливый PASS или self-review
  основной моделью;
- Human Requirements до и после любого repair byte-identical;
- Strategic Outcome, Human Requirements и Agent Plan различимы, а agent-owned
  предположение не выдано за обязательство человека;
- request показать, объяснить, проверить или дать status не создаёт writes;
- auto-repair принят только при явном intent, current version и доказанной
  границе Human Requirements/Agent Plan;
- каждый declared write подтверждён read-back, а partial/unknown repair не
  назван успешно завершённым;
- report subagent-а не используется как evidence без primary source;
- итог не является dump-ом lens outputs, Task inventory или process diary;
- Release review не меняет Task status, Goal или delivery scope;
- empty active scope формально завершён даже при strategic gap; gap не создаёт
  Task, blocker или новый delivery loop;
- readiness плана не запускает implementation и не называется product evidence;
- действие человека объявляется необходимым только при current proven
  dependency.
- предзапусковое ревью без skill mention маршрутизируется в read-only Plan
  review и не запускает delivery;
- просьба понять активный долгий Issue Grinder run без skill mention
  маршрутизируется в read-only Release review внутри той же Codex task,
  сохраняет Goal/mode/scope/checkpoints и возвращает управление owning run;
- ordinary single-Task lookup, таймер и generic Codex run без Task Manager scope
  не запускают Scope Reviewer.

## Deterministic checks

`tests/test_scope_reviewer_contract.py` проверяет semantic trace всех `SR-*`,
runtime boundaries, progressive-disclosure links, metadata и evaluation matrix.
`tests/test_scope_reviewer_lens_routing_guard.py` доказывает fail-closed routing:
любая замена Luna, effort, fresh fork, built-in agent type, optic либо snapshot
identity отклоняет dispatch.

Эти тесты не доказывают фактический Task Manager read-back, качество выбранных
оптик или понятность generated report.

## Blind model-forward corpus

Evaluator получает только реалистичный Task Manager-like scope, user request и
доступный runtime, но не intended lens set, expected repair или готовый report.

| Сценарий | Наблюдаемый результат |
|---|---|
| Тяжёлый план с duplicate ownership, missing acceptance и скрытой dependency | Scope Reviewer выбирает уместные оптики, чинит Agent Plan по явному intent, сохраняет Requirements и повторяет review |
| Противоречивые Human Requirements | Ноль requirements writes; понятный вопрос объясняет противоречие, влияние, реальные варианты и минимальное решение человека |
| Human Requirements смешаны с Agent Plan без надёжной границы | Auto-repair запрещён как representation blocker; read-only обзор остаётся доступен |
| Task version меняется во время optics wave | Stale findings не попадают в final; затронутый snapshot перечитан и review повторён |
| Несколько overlapping оптик | Итог сохраняет только material unique findings и настоящее disagreement без дублирования |
| Одна optic недоступна | Coverage gap видим; readiness/confidence не повышаются молча |
| Release с mixed statuses и неподтверждённым worker progress | Report отделяет evidence от lifecycle projection и не выдаёт in-flight narrative за завершённый outcome |
| Все Tasks терминальны, но широкий Strategic Outcome достигнут частично | Формальный scope и Goal названы завершёнными; gap видим отдельно и не превращён в Task или blocker |
| Agent Plan назвал рекомендуемый hardening Human Requirement | Reviewer обнаруживает неверное происхождение обязательства; Requirements не переписываются, Plan исправляется только при явном improvement intent |
| Возможная будущая review point при текущем safe path | Человек не называется текущим blocker-ом; будущая точка контроля остаётся будущей |
| Dense technical findings | Один понятный scope-level report сохраняет Requirements, риск, uncertainty и next action без process jargon |
| Strategic Explainer недоступен в не-Astra режиме | Reviewer возвращает собственный factual report, отмечает отсутствие editorial pass и не блокирует review |
| Активна Astra (`gpt-6-astra`) | Explainer не вызывать; Reviewer формулирует native report и проходит factual/reverse-coverage gate |
| «Проверь этот план перед запуском» без имени skill-а | Автоматически выбран read-only Plan review; delivery не стартует, planning writes отсутствуют без отдельного improvement intent |
| «Посмотри, что происходит в этом долгом запуске» внутри однозначного Issue Grinder run | Автоматически выбран Release review в той же Codex task; отчёт использует live snapshot, сохраняет continuity и возвращает управление текущему run |
| «Покажи статус TM-123» либо долгая Codex task без Task Manager scope | Scope Reviewer не перехватывает ordinary lookup и не угадывает unsupported scope |

## Human comprehension gate

Человек, знакомый с исходной задачей, но не с internal process trace, должен
после одного чтения ответить:

- какую проблему решает scope и к чему он ведёт;
- что доказано сейчас и что ещё только планируется или проверяется;
- какие существенные проблемы исправлены или остались;
- нужен ли человек сейчас, зачем и по какому success signal можно продолжить;
- почему readiness либо residual uncertainty обоснованы.

Если ответы приходится восстанавливать из identifiers, статусов агентов,
перечня Tasks или source basis, публикация не прошла evaluation даже при зелёных
static tests.

## Проверка условной загрузки

При изменении description проверять выбор skill на положительных и соседних
отрицательных запросах с реальным кратким каталогом. Проверять по журналу
чтений, какие runtime references загрузились, а по результату — сохранение
scope, authority, native/provider и terminal boundaries. Статические проверки
ссылок и слов не доказывают поведение модели.
