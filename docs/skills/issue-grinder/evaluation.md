# Issue Grinder: observable evaluation

Статус: current observable evaluation, 2026-09-03. Документ проверяет
компиляцию локальных [Overview](overview.md), [Requirements](requirements.md) и
[Architecture](architecture.md), но не создаёт новый policy contract.

## Слои проверки

1. Static contract связывает каждый `IG-*` с runtime surface и required
   сценарием, проверяет metadata, references и отсутствие незавершённых
   placeholders. Этот слой исполняется repository validators.
2. Детерминированные harness-ы проверяют отдельные внешние решения, mode
   resolver, model-routing receipts, нетерминальный checkpoint, порядок effects
   и механические Git-инварианты writer admission. Они не симулируют reasoning и поэтому
   являются oracle hard invariants, а не полным тестом skill.
3. Model-forward cases должны запускать установленный skill в новой сессии на
   изолированном синтетическом scope; Task Manager effects можно исключить, если
   case измеряет только mode topology и delivery по локальному плану. Generator
   не получает скрытый oracle или expected answer. Полный
   repository-executable harness этого слоя пока отсутствует; доступны узкие
   mode-loading и Solo-topology smoke. Остальные coverage names ниже являются
   обязательным corpus, а не доказанными PASS.
4. Distribution smoke проверяет source → Marketplace → installed cache,
   activation и отсутствие одновременно установленного ShipTask. Его evidence
   относится к конкретному snapshot и не переносится на следующую версию.

## Протокол синтетической настройки режимов

Model-forward tuning не меняет mode contract под имена файлов или частные
особенности одного fixture. Правила оцениваются в два шага: повторяемый tuning
fixture помогает найти дефект orchestration, а перед итоговым выводом
используется не участвовавший в правках holdout с другой предметной формой.

Каждый отдельный прогон имеет единый потолок `3 600` секунд. Значение берётся из
одного поля manifest и одинаково передаётся process runner-у и в rendered
prompt; подготовка обязана остановиться при расхождении. Планового
десятиминутного checkpoint или схемы `600 + 3000` нет. Режимы запускаются
последовательно из одной frozen base, каждый в новом изолированном checkout и
свежей Codex-сессии.

Неблокирующая погрешность не останавливает прогон: она записывается рядом с той
метрикой, которую способна исказить. Дефект, влияющий на весь прогон, отмечается
отдельно и исключает только причинно затронутые сравнения. Минимальный итоговый
набор измерений: terminal outcome, внешний oracle, blind quality review,
валидность mode topology, elapsed time и раздельные Sol/Luna tokens. Улучшение
признаётся общим только если оно сохраняет contract на tuning fixture и не
ухудшает holdout из-за fixture-specific правила.

## Coverage map

Таблица задаёт требуемую трассу и имена observable cases. Наличие строки не
означает, что соответствующий model-forward case уже исполнен.

| Requirement | Runtime surface | Observable scenarios |
|---|---|---|
| `IG-FLOW-01` | `SKILL.md` §1; `task-.md` | active-status-filter; backlog-rejected |
| `IG-FLOW-02` | `SKILL.md` §2; `task-.md` | all-lifecycle-transitions |
| `IG-FLOW-03` | `SKILL.md` §3; `strategic-explainer.md` | trivial-start; required-comment; astra-native-routing; native-fallback; fresh-facade-per-unit; completed-provider-not-reused |
| `IG-FLOW-04` | `SKILL.md` §3; `strategic-explainer.md` | comment-reveals-work; optional-follow-up |
| `IG-FLOW-05` | `SKILL.md` §2; `task-.md` | integrated-blocked-by; late-reopen-recheck |
| `IG-FLOW-06` | `SKILL.md` §5; `execution-modes.md`; `modes/economical.md`; mode harness | active-scope-prevents-completion; economical-checkpoint-is-nonterminal |
| `IG-GOAL-01` | `run-and-goal.md`; `execution-modes.md`; `modes/economical.md`; trace harness | explicit-multi-create; implicit-no-goal; grow-and-keep; economical-checkpoint-keeps-goal |
| `IG-GOAL-02` | `SKILL.md`; `run-and-goal.md`; `multi-agent-execution.md` | strategic-release-objective; issue-list-rejected; strategic-context-restored; single-issue-parent-context; strategy-does-not-expand-scope |
| `IG-GOAL-03` | `SKILL.md` §5; `run-and-goal.md`; `modes/economical.md`; trace harness | empty-scope-complete; active-scope-continue; checkpoint-goal-not-complete; completed-tasks-with-strategic-gap-still-complete |
| `IG-GOAL-04` | `SKILL.md` §3; blocker harness | explanation-unlocks; true-external-blocker |
| `IG-GOAL-05` | `SKILL.md` §3 | final-reflection-continues; chat-only-final |
| `IG-GOAL-06` | `SKILL.md` §2; `task-.md` | nonmaterial-gap-transparent-by-issue-contract; material-acceptance-gap-blocks |
| `IG-GOAL-07` | `SKILL.md` §3; `strategic-explainer.md`; blocker harness | all-causes-overview; one-separate-answer-per-cause; three-lens-completeness; reason-reflection-unlocks; accepted-blocker-auto-continuation-no-repeat; threshold-goal-effect-only |
| `IG-SCOPE-01` | `run-and-goal.md`; `task-.md` | prompt-selector-precedence |
| `IG-SCOPE-02` | `run-and-goal.md` | explicit-default-release; implicit-missing-selector |
| `IG-SCOPE-03` | `run-and-goal.md`; `task-.md` | late-member; excluded-member; final-refresh |
| `IG-UI-01` | `run-and-goal.md`; `thread-title.md` | fresh-placeholder-renamed; meaningful-title-preserved; ambiguous-candidate-preserved; title-capability-failure-nonblocking |
| `IG-AUTO-01` | `SKILL.md` §4; `run-and-goal.md`; `autonomy-and-environments.md` | explicit-persistence; implicit-no-extra-authority |
| `IG-AUTO-02` | `SKILL.md` §3; `modes/economical.md`; blocker harness | preflight-unlock; explanation-unlock; relevant-signal-resumes; sufficient-economical-checkpoint-stops-boundedly |
| `IG-AUTO-03` | `SKILL.md` §4; environment harness | production-rejected; public-uat-allowed; provider-production-label-does-not-reclassify-uat |
| `IG-AUTO-04` | `SKILL.md` §4; environment harness | default-uat; unknown-uat-before-effect |
| `IG-AUTO-05` | `autonomy-and-environments.md` | security-selector; narrow-always-readback |
| `IG-MODE-01` | `SKILL.md` §1, §5; `execution-modes.md` | four-canonical-modes; mode-does-not-expand-authority |
| `IG-MODE-02` | `SKILL.md` §1; `execution-modes.md`; mode harness | explicit-freeform-wins; default-luna-max-balance; default-sol-xhigh-classic; other-profiles-legacy-default; economical-explicit-only; retired-mode-rejected; mode-persists-after-model-change |
| `IG-MODE-03` | `modes/classic.md`; `multi-agent-execution.md`; mode harness | classic-sol-does-almost-all; classic-luna-trivial-only; classic-high-judgment-owner; classic-simple-independent-review; classic-final-review-terminal |
| `IG-MODE-04` | `modes/balance.md`; mode/routing harness | luna-root-owns-process; bounded-sol-specialist; independent-sol-xhigh-review; no-cheap-quality-bypass |
| `IG-MODE-06` | `SKILL.md` §5; `modes/economical.md`; mode/routing guards; mode harness | economical-all-substantive-luna; wrong-root-refused-before-effects; economical-independent-luna-review; economical-terminal-when-proven; economical-partial-review-checkpoint; economical-resumable-candidate; no-false-done; no-false-blocked |
| `IG-MODE-07` | `SKILL.md` §1; `execution-modes.md`; mode/routing guards | bounded-fork; observed-profile-match; agent-label-neutral; role-override-wins |
| `IG-MODE-08` | `modes/{classic,balance,economical}.md`; `multi-agent-execution.md` | economical-handoff-preserves-evidence; same-retry-rejected |
| `IG-MODE-09` | `modes/{solo,classic,balance,economical}.md` | one-review-candidate; dissent-preserved; finding-disposition-preserved; material-defect-beats-generic-approvals; raw-loop-transcript-not-required; rework-reviewed-again |
| `IG-MODE-10` | `execution-modes.md`; `multi-agent-execution.md`; mode harness | explicit-switch-barrier; automatic-no-switch; switch-preserves-candidates-and-scope |
| `IG-MODE-11` | `SKILL.md` §1-3; `modes/solo.md`; `strategic-explainer.md`; mode/solo-topology harnesses | solo-one-issue; solo-many-issues-sequential; solo-current-profile-after-model-change; solo-no-execution-delegation; solo-provider-allowed; solo-terminal-only |
| `IG-MODE-12` | `execution-modes.md`; `multi-agent-execution.md`; `strategic-explainer.md`; solo-topology harness | outer-controller-not-counted; provider-transport-not-counted; provider-doing-delivery-becomes-execution-agent; explicit-global-opt-out-wins; topology-boundary-all-modes |
| `IG-MODE-19` | `execution-modes.md`; `modes/solo.md` | process-handle-survives-handoff; completed-result-reused; independent-tools-one-solo-packet; unknown-effect-reconciled |
| `IG-MODE-20` | `SKILL.md`; `execution-modes.md`; `main_profile.py`; mode harness | own-latest-turn-profile; no-config-fallback; wrong-model-refused; wrong-effort-refused; unknown-refused; resume-profile-gate; switch-profile-gate; no-wrapper-or-effects; legacy-balance-refused |
| `IG-HELP-01` | `SKILL.md` §0; `mode-help.md` | all-four-modes-brief; default-is-resolver; narrow-difference-answer; help-has-no-task-manager-effects; mixed-help-delivery-preserves-gates |
| `IG-MA-01` | `SKILL.md` §2; `multi-agent-execution.md` | two-independent-packets; useful-critic; intentional-candidate; one-lane-no-filler; solo-delegation-forbidden |
| `IG-MA-02` | `multi-agent-execution.md` | disjoint-surfaces; ordinary-conflicting-surfaces; isolated-intentional-overlap |
| `IG-MA-03` | `multi-agent-execution.md` | dependency-ready-frontier |
| `IG-MA-04` | `multi-agent-execution.md` | adaptive-width; no-filler-packet |
| `IG-MA-05` | `SKILL.md` §2; `multi-agent-execution.md` | coordinator-only-fan-in-and-writes |
| `IG-MA-06` | `multi-agent-execution.md`; `writer_worktree_guard.py` | two-phase-admission; shared-main-rejected; integration-canary; read-only-git-preflight; sequential-patch-return-no-guard-source-read |
| `IG-MA-07` | `multi-agent-execution.md`; `writer_worktree_guard.py` | exclusive-writable-owner; duplicate-branch-and-path-rejected |
| `IG-MA-08` | `multi-agent-execution.md` | read-only-role-no-worktree |
| `IG-MA-09` | `multi-agent-execution.md` | strategic-outcome-and-contribution-in-packet; human-requirements-distinct-from-agent-plan; packet-context-does-not-expand-scope |
| `IG-MA-10` | `SKILL.md` §2; `multi-agent-execution.md` | exact-integrated-verification |
| `IG-MA-11` | `multi-agent-execution.md` | redispatch-after-return-and-scope-change |
| `IG-MA-12` | `SKILL.md` §2; `multi-agent-execution.md`; `writer_worktree_guard.py`; trace harness | startup-inventory-before-fresh-work; branch-only-restored; dirty-checkpoint-resumed; active-owner-rejected; ambiguous-preserved; intentional-candidate-not-replacement |
| `IG-MA-13` | `multi-agent-execution.md` | explicit-profile-preserved |
| `IG-MA-14` | `modes/classic.md`; `multi-agent-execution.md` | classic-simple-luna-max; classic-small-diff-not-simple |
| `IG-MA-15` | `modes/*.md`; `multi-agent-execution.md`; routing guard | solo-current-main-only; classic-material-controller; economical-economical-controller |
| `IG-MA-16` | `modes/{classic,balance,economical}.md`; `multi-agent-execution.md` | luna-uncertainty-evidence-handoff; mode-specific-next-route; same-luna-retry-rejected |
| `IG-MA-17` | `modes/{classic,balance,economical}.md`; `multi-agent-execution.md`; routing guard | selected-profiles-assumed-available; no-automatic-mode-switch-or-profile-substitution; routing-failure-stops-wave |
| `IG-MA-18` | `multi-agent-execution.md`; `strategic-explainer.md` | explainer-outside-worker-routing; worker-evidence-coordinator-facade; nested-facade-no-new-task; solo-provider-outside-execution-topology |
| `IG-MA-19` | `SKILL.md` §2; `execution-modes.md`; `modes/{classic,balance,economical}.md`; `multi-agent-execution.md`; mode harness | capability-aware-direct-stages; one-guard-spawn-per-owner; full-stage-deadline-wait; technical-timeout-no-probe; unchanged-state-polling-rejected; final-response-handoff; economical-deadline-partial-ledger-only |

## Быстрый mode corpus

`scripts/issue_grinder_mode_harness.py` является исполнимой таблицей только для
механически разрешимых частей mode contract. Он проверяется командой:

```bash
python3 -B -m unittest discover -s tests -p 'test_issue_grinder_mode_harness.py'
```

Corpus доказывает:

- приоритет явного режима; default Luna Max → Balance, Sol xhigh → Classic; прочие профили сохраняют
  прежнее правило; root admission запрещает неправильные и неизвестные профили; Economical только явно;
- `Соло` с current main profile, нулём execution-subagents и одной
  последовательной lane;
- сохранение mode record при доказанной continuity и отсутствие переноса
  старого record в новый run;
- Luna Max baseline рабочих ролей и независимый приоритет role overrides;
- independent-review lifecycle режимов, которые его требуют: один guard/spawn
  на owner-а, event waits, reuse после rework и только economical checkpoint с
  partial deadline ledger;
- полноту resumable checkpoint, запрет ложного `complete`/`blocked` и
  обязательный active Task Manager status/Goal;
- явный switch только после quiescent writers, неизменного integration checkout,
  reconciliation ownership и сохранения evidence.

Harness принимает уже распознанный канонический mode. Он не доказывает качество
понимания свободной пользовательской формулировки, декомпозиции, выбора
полезного агента, code review или фактического
исполнения Markdown runtime. Эти свойства остаются model-forward cases и
наблюдаемым результатом реальных прогонов.

## Быстрый model-routing corpus

Bundled `issue-grinder/scripts/model_routing_guard.py` и его unit corpus
проверяются командой:

```bash
python3 -B -m unittest discover -s tests -p 'test_model_routing_guard.py'
```

Corpus механически доказывает, что `Экономичный`
принимают mode-specific Luna child только с unique `packet_id`, explicit model/effort,
bounded fork и `issue-grinder/model-routing/v2` fingerprint точных dispatch
args, отвергают inherited Sol, `fork_turns=all` и observed profile mismatch, но
не выводят model/effort из имени либо типа агента. Luna Max обязателен для экономичных ролей. Явный пользовательский role override сохраняется и
сверяется с observed profile. Guard не доказывает честность semantic label,
фактический вызов child или невозможность raw spawn без preflight — это
проверяют model-forward canary и recursive thread-tree telemetry.

## Быстрый blocker corpus

`scripts/issue_grinder_trace_harness.py` моделирует обязательную цепочку:

```text
candidate blocker
  → preflight reflection
  → explanation
  → post-explanation reflection
  → continue | terminal blocker
```

Нулевую терпимость имеют запрещённые эффекты:

- explanation выявила проверенный safe action, но run остановился;
- blocker-report или `update_goal(blocked)` произошли до post-explanation
  reflection;
- platform blocker audit задержал принятый blocker-report пользователю;
- автоматический Goal turn с тем же принятым blocker fingerprint повторил
  browser/profile/account discovery, blocked action, Strategic Explainer,
  blocker-handoff или просьбу пользователю без нового релевантного сигнала;
- достигнутый platform threshold создал новую communication unit вместо
  единственного отсутствующего `update_goal(blocked)`;
- релевантный resume signal или изменившийся primary state не инвалидировал
  прежний blocker checkpoint;
- incomplete/raw-error report был опубликован;
- общий report не перечислил все подтверждённые причины либо для хотя бы
  одной причины нет отдельного ответа;
- reason-specific answer не объяснил, почему причина блокирует обязательный
  результат активного issue, почему Issue Grinder не может устранить её сам или
  зачем заблокированный шаг нужен issue contract и общей цели;
- остановка или `update_goal(blocked)` произошли до публикации общего report и всех
  отдельных ответов;
- caller error Strategic Explainer превратился в blocker вместо исправления;
- завершённый provider-child был продолжен через `followup_task` или
  `send_message` для caller repair либо следующей publication unit;
- public UAT, синтетический fixture или непроверенная альтернатива были названы
  terminal причиной без попытки самостоятельного продолжения;
- optional improvement создал бесконечную итерацию;
- совместимый Goal без доказанной continuity был присвоен новому run;
- одинаковый recovery повторился без нового evidence, изменившегося state или
  bounded fallback;
- сохранённое `Да всегда` не применилось к эквивалентной future operation либо
  расширилось на другую категорию/Production;
- auto-title перезаписал meaningful title, сработал на later turn, передал
  discovery `threadId` в setter, повторил failed setter либо заблокировал
  delivery из-за отсутствующей capability.

Структурная полнота отчёта проверяется отдельно от качества прозы: stopped work,
primary cause, все blocking reasons, checkpoint, unverified remainder, impact, user
action и resume condition обязательны. Для каждой blocking reason harness требует
отдельный answer с тремя непустыми смысловыми полями: blocking effect,
self-resolution boundary и goal value. Model-forward evaluator дополнительно
проверяет, что каждый ответ естественно объясняет эти три связи и не переносит
основной смысл во внутренние термины.

## Проверка экономии организации без ослабления приёмки

Трасса согласованных изменений: `IG-MODE-09` и `IG-MODE-19` → Architecture
§4.4.1 → `execution-modes.md`; `IG-MA-01/04/19` → Classic review;
`IG-MODE-06`, `IG-MA-05/19` → `modes/economical.md`. Overview о надёжной доставке
сложного результата сохраняется: экономия не заменяет обязательные gates.

Для следующей независимой model-forward оценки использовать сценарии:

- Только parser изменён, алгоритмы прежние: сохранить применимые module checks,
  повторить parser и затронутую интеграцию; неизвестная зависимость расширяет gates.
- Долгий процесс ещё работает после handoff: продолжить по сохранённому handle,
  не запустить дубль; завершённый процесс читается из сохранённого raw result.
- Solo запускает независимые проверки одного пакета параллельно, но не начинает
  вторую содержательную задачу и не создаёт рабочего агента.
- Classic оставляет неокупающийся simple packet себе и всё равно получает
  независимый review.
- Luna-root Экономичного реализует сам, затем другой Luna проверяет; автор не
  заменяет независимого reviewer-а, checkpoint не объявляется Done.

Этот корпус задаёт будущую поведенческую проверку, а не утверждает, что она уже
пройдена. Unit tests доказывают решения harness по observations, не фактическую
экономию модели. Новый бенчмарк требуется отдельно для измерения эффекта.

## Быстрый writer-isolation corpus

Узкий Git guard и barrier trace проверяются без модели и Task Manager:

```bash
python3 -B -m unittest discover -s tests -p 'test_writer_worktree_guard.py'
python3 -B -m unittest discover -s tests -p 'test_issue_grinder_trace_harness.py'
```

Corpus доказывает, что:

- два writer packet получают разные locked linked worktree, private Git dir и
  branch от одного exact base;
- admission проходит только из exact `cwd` подготовленного worktree и отвергает
  общий main checkout;
- snapshot integration checkout обнаруживает даже незакоммиченную stray write;
- receipt невозможно записать внутрь Git worktree и тем самым испачкать guard-ом
  защищаемый checkout;
- fresh `prepare` запрещён, пока exact-scope artifact требует reuse, продолжения
  через active owner, takeover либо разрешения ownership;
- branch-only checkpoint восстанавливается как linked worktree той же branch, а
  существующий dirty worktree продолжается только с явным `--allow-dirty` без
  потери diff;
- replacement для уже checked-out branch и молчаливое присвоение ambiguous
  artifact отвергаются;
- implementation dispatch разрешается только после всех valid admission
  receipts; missing/failed admission, изменившийся integration checkout и
  отсутствующий task-owned commit запрещают fan-in и lifecycle effect.

Это проверка enforcement-механизма, а не решения coordinator-а разделить работу,
не полнота packet contract и не качество fan-in. Эти части остаются предметом
fresh model-forward smoke.

## Обратная связь из реальных прогонов

Реальный запуск Issue Grinder является основным дешёвым источником поведенческих
сигналов, но не превращает случайный результат одного стохастического прогона в
новое универсальное правило. Подтверждённый дефект сначала сводится к
минимальному синтетическому примеру:

- если решение механическое и не требует reasoning, пример добавляется в
  соответствующий deterministic harness;
- если дефект относится к пониманию запроса, стратегии, делегированию, review
  или качеству текста, он добавляется в model-forward corpus с наблюдаемым
  outcome и минимальным source fixture;
- приватные production-данные, реальные recipients и подписанные URLs в fixture
  не копируются.

Так feedback постепенно увеличивает покрытие доказанных failure modes, не
создавая тяжёлый fake Task Manager и не закрепляя случайные формулировки output.

## Fresh smoke acceptance

После install/upgrade новая Codex-сессия должна:

- видеть `issue-grinder:issue-grinder`, `issue-grinder:task-composer` и
  `issue-grinder:scope-reviewer`;
- не видеть установленный `ship-tasks:ship-tasks`;
- видеть Task Manager dependency и optional Strategic Explainer;
- на чистый вопрос о режимах/default/различиях дать краткую справку о четырёх
  режимах без Task Manager, Goal, title mutation, delivery loop и subagents;
- правильно различать explicit delivery, implicit exact selector, implicit
  missing selector и read/status/planning negative prompts;
- на новых synthetic runs проверить default: non-Luna + несколько задач → Classic,
  иначе Solo; Economical только явно;
  любой явно выбранный канонический режим должен победить default rule, а продолжение
  после смены модели — сохранить ранее выбранный mode;
- при активной модели Astra (`gpt-6-astra`) для каждой автоматической
  publication unit не вызывать Strategic Explainer и сформулировать native
  текст самой Astra, даже если provider установлен и предыдущий mode был
  `ordinary`;
- наблюдаемо различить режимы: в `Классическом` Sol/controller делает почти
   всё, а Luna получает только тривиальные packets; `Соло` сохраняет current
  model, ноль Issue Grinder execution-subagents и в не-Astra ветке допускает
  отдельный Strategic Explainer provider для одного и нескольких issue;
  `Экономичный` выполняет весь substantive packet и review на Luna Max, оставляя
  non-Luna root только transport/authority shell, и сохраняет один resumable
  candidate без ложного `Done`/Goal completion;
- для всех mode-specific Luna child в `Классическом` и `Экономичном` сохранить packet-bound
  pre-dispatch и observed `issue-grinder/model-routing/v2` receipts с
  совпадающими dispatch fingerprints; ни один substantive child не наследует
  несовместимый profile, а agent name/type не используется как источник
  model/effort policy; пропущенный receipt либо raw Sol/GPT-5.4 ordinary spawn
  закрывает валидность выбранного cost-aware mode;
- на scope с двумя независимыми write packets сначала получить от каждого
  admission-only receipt отдельного linked worktree, разрешить implementation
  только follow-up turn-ом и сохранить integration checkout неизменным до
  fan-in; admission mismatch должен закрыть wave до implementation dispatch, а
  stray Git-visible write в общем checkout — до fan-in и lifecycle effects с
  сохранением неизвестного diff;
- в доказанной первой task с catalog placeholder и canonical scope сделать не
  более одной best-effort попытки `Issue Grinder · ...`, сохранив meaningful
  title и продолжив при отсутствии capability;
- на synthetic blocker case продолжить после найденного safe action, а на
  настоящем authority blocker-е дать полный общий причинный report и отдельный
  трёхчастный ответ по каждой причине; в двух следующих автоматических Goal
  turns с тем же fingerprint не повторять blocked proof, facade, handoff и user
  request, а на platform threshold выполнить только Goal mutation; новый
  релевантный signal обязан возобновить live reconciliation;
- на completed Task scope с известным strategic gap завершить Goal, раскрыть gap
  в отчёте и не создать новую Task, blocker или delivery iteration;
- перед implementation и после simulated resume восстановить Strategic Outcome,
  Human Requirements, вклад issue и exact Agent Plan, не расширяя scope.

Static, deterministic и registration checks не заменяют этот model-forward
smoke; если live synthetic run не выполнен, это указывается как непроверенная
часть, а не считается автоматически пройденной.

Узкий smoke прогрессивной загрузки запускается отдельно:

```bash
python3 scripts/issue_grinder_mode_loading_smoke.py \
  --model gpt-5.6-luna \
  --reasoning-effort max
```

Runner создаёт по одной fresh ephemeral read-only Codex-сессии для каждого из
четырёх explicit mode. По наблюдаемым command-execution events case проходит,
только если агент полностью открыл installed `SKILL.md`, общий
`execution-modes.md` и ровно один выбранный файл из `references/modes/`.
Открытие соседнего mode-файла, broad access ко всему каталогу, отсутствие
обязательного чтения или расходящийся итоговый receipt закрывают case. Этот
smoke проверяет progressive disclosure, но не доказывает соблюдение model
routing и topology во время полноценной delivery.

Отдельный synthetic Solo topology smoke запускается после установки plugin:

```bash
python3 scripts/issue_grinder_solo_topology_smoke.py \
  --model gpt-5.6-sol \
  --reasoning-effort low
```

Runner создаёт временный локальный scope с анализом, реализацией, проверкой и
self-review, запускает fresh explicit `Соло` без Task Manager и внешних
publication units и проверяет root trace. Case проходит, только если exact
result создан и проверен основной сессией, загружен ровно `solo.md`, а
`spawn_agent`, `create_thread`, `fork_thread` или иной execution-child dispatch
не наблюдался. В этом synthetic scope provider не нужен, поэтому любой child
означает рабочую делегацию Issue Grinder. Разрешение отдельного Strategic
Explainer provider и его исключение из mode topology проверяются
детерминированным mode corpus и contract tests; provider, которому передали
delivery source/tests/review, должен считаться execution-agent и закрывать
соответствующий model-forward case.

## Исторические замеры

Замеры удалённых режимов сохранены в датированных reports и не являются
действующей политикой или подтверждением поведения четырёх текущих режимов.
Новый автовыбор проверяется матрицей profiles × число live задач, явным выбором,
продолжением после изменения модели/числа задач и отклонением удалённых modes.
Одинарная синтетика остаётся базовым протоколом; изменение маршрутизации само
по себе не доказывает изменения стоимости и не требует переписывать старые цифры.

## Проверка установленного Баланса 2026-09-06

[Полный отчёт](../../reports/2026-09-06-issue-grinder-balance-installed.md) и
[данные](../../reports/2026-09-06-issue-grinder-balance-installed.json) фиксируют
пять fresh profile cases и одинарные S1/C1/B1/E1 установленного payload.
Все четыре результата проходят 21/21 и исходные 45-second gates. Отказы
на Sol xhigh и Luna high наблюдены без writes/children; default resolver
выбирает Balance для Luna Max и Classic для Sol xhigh. Первая версия ошиблась
на Luna high; обязательный session-backed admission исправлен и перепроверен.
Баланс снизил стоимость относительно текущих Соло/Классического, но ухудшил
КПД относительно LC1; это regression evidence, не подтверждение отсутствия
регрессии. Полный Task Manager lifecycle этим локальным опытом не проверен.

Пересчёт подписочной метрики: [отчёт 07.09.2026](../../reports/2026-09-07-issue-grinder-weekly-pool.md).
Проверка изменения единицы измерения: прежние токены каждого run совпадают,
сумма недельных процентов run равна объединённому дереву, API price отдельно
суммируется по категориям/моделям и не выдаётся за подписочный счётчик. Калибровка принадлежит
счётчику; отсутствие счётчика не блокирует delivery и не разрешает выдумывать проценты.
