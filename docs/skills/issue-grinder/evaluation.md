# Issue Grinder: observable evaluation

Статус: current Level 2 evaluation, 2026-08-30. Документ проверяет компиляцию
локальных [Requirements](requirements.md) и [Architecture](architecture.md), но
не создаёт новый policy contract.

## Слои проверки

1. Static contract связывает каждый `IG-*` с runtime surface и required
   сценарием, проверяет metadata, references и отсутствие незавершённых
   placeholders. Этот слой исполняется repository validators.
2. Детерминированные harness-ы проверяют отдельные внешние решения, mode
   resolver, нетерминальный checkpoint, порядок effects и механические
   Git-инварианты writer admission. Они не симулируют reasoning и поэтому
   являются oracle hard invariants, а не полным тестом skill.
3. Model-forward cases должны запускать установленный skill в новой сессии на
   синтетическом Task Manager scope; generator не получает rubric или expected
   answer. Repository-executable harness этого слоя пока отсутствует, поэтому
   coverage names ниже являются обязательным corpus, а не доказанными PASS.
4. Distribution smoke проверяет source → Marketplace → installed cache,
   activation и отсутствие одновременно установленного ShipTask. Его evidence
   относится к конкретному snapshot и не переносится на следующую версию.

## Coverage map

Таблица задаёт требуемую трассу и имена observable cases. Наличие строки не
означает, что соответствующий model-forward case уже исполнен.

| Requirement | Runtime surface | Observable scenarios |
|---|---|---|
| `IG-FLOW-01` | `SKILL.md` §1; `task-manager-flow.md` | active-status-filter; backlog-rejected |
| `IG-FLOW-02` | `SKILL.md` §2; `task-manager-flow.md` | all-lifecycle-transitions |
| `IG-FLOW-03` | `SKILL.md` §3; `strategic-explainer.md` | trivial-start; required-comment; native-fallback |
| `IG-FLOW-04` | `SKILL.md` §3; `strategic-explainer.md` | comment-reveals-work; optional-follow-up |
| `IG-FLOW-05` | `SKILL.md` §2; `task-manager-flow.md` | integrated-blocked-by; late-reopen-recheck |
| `IG-FLOW-06` | `SKILL.md` §5; `execution-modes.md`; `modes/economical.md`; mode harness | active-scope-prevents-completion; economical-checkpoint-is-nonterminal |
| `IG-GOAL-01` | `run-and-goal.md`; `execution-modes.md`; `modes/economical.md`; trace harness | explicit-multi-create; implicit-no-goal; grow-and-keep; economical-checkpoint-keeps-goal |
| `IG-GOAL-02` | `run-and-goal.md` | strategic-release-objective; issue-list-rejected |
| `IG-GOAL-03` | `SKILL.md` §5; `run-and-goal.md`; `modes/economical.md`; trace harness | empty-scope-complete; active-scope-continue; checkpoint-goal-not-complete |
| `IG-GOAL-04` | `SKILL.md` §3; blocker harness | explanation-unlocks; true-external-blocker |
| `IG-GOAL-05` | `SKILL.md` §3 | final-reflection-continues; chat-only-final |
| `IG-GOAL-06` | `SKILL.md` §2; `task-manager-flow.md` | nonmaterial-gap-transparent; material-gap-blocks |
| `IG-GOAL-07` | `SKILL.md` §3; `strategic-explainer.md`; blocker harness | all-causes-overview; one-separate-answer-per-cause; three-lens-completeness; reason-reflection-unlocks |
| `IG-SCOPE-01` | `run-and-goal.md`; `task-manager-flow.md` | prompt-selector-precedence |
| `IG-SCOPE-02` | `run-and-goal.md` | explicit-default-release; implicit-missing-selector |
| `IG-SCOPE-03` | `run-and-goal.md`; `task-manager-flow.md` | late-member; excluded-member; final-refresh |
| `IG-UI-01` | `run-and-goal.md`; `thread-title.md` | fresh-placeholder-renamed; meaningful-title-preserved; ambiguous-candidate-preserved; title-capability-failure-nonblocking |
| `IG-AUTO-01` | `SKILL.md` §4; `run-and-goal.md`; `autonomy-and-environments.md` | explicit-persistence; implicit-no-extra-authority |
| `IG-AUTO-02` | `SKILL.md` §3; `modes/economical.md`; blocker harness | preflight-unlock; explanation-unlock; sufficient-economical-checkpoint-stops-boundedly |
| `IG-AUTO-03` | `SKILL.md` §4; environment harness | production-rejected; public-uat-allowed |
| `IG-AUTO-04` | `SKILL.md` §4; environment harness | default-uat; unknown-uat-before-effect |
| `IG-AUTO-05` | `autonomy-and-environments.md` | security-selector; narrow-always-readback |
| `IG-MODE-01` | `SKILL.md` §1, §5; `execution-modes.md` | five-canonical-modes; mode-does-not-expand-authority |
| `IG-MODE-02` | `SKILL.md` §1; `execution-modes.md`; mode harness | explicit-freeform-wins; luna-any-effort-economical; non-luna-classic; mode-persists-after-model-change |
| `IG-MODE-03` | `modes/classic.md`; `multi-agent-execution.md` | classic-sol-does-almost-all; classic-luna-trivial-only; classic-high-judgment-owner; classic-final-review-terminal |
| `IG-MODE-04` | `modes/balance.md`; `multi-agent-execution.md` | balance-controller-plans; balance-luna-light-and-medium-first; balance-problem-fallback-to-sol; balance-rework-redispatch; balance-final-gate |
| `IG-MODE-05` | `modes/swarm.md`; `multi-agent-execution.md` | swarm-intentional-candidates; swarm-isolated-overlap; swarm-reduction; swarm-bounded-stop; swarm-final-gate |
| `IG-MODE-06` | `SKILL.md` §5; `modes/economical.md`; mode harness | economical-terminal-when-proven; economical-resumable-candidate; no-false-done; no-false-blocked |
| `IG-MODE-07` | `SKILL.md` §1; `execution-modes.md`; mode harness | luna-profile-collapse; luna-low-root-luna-max-supervisor; non-luna-two-profile; unknown-family-no-guess; role-override-wins |
| `IG-MODE-08` | `modes/{classic,balance,swarm,economical}.md`; `multi-agent-execution.md` | economical-handoff-preserves-evidence; swarm-alternative-approach; same-retry-rejected |
| `IG-MODE-09` | `modes/{balance,swarm,economical}.md` | one-review-candidate; dissent-preserved; raw-swarm-transcript-not-required; rework-reviewed-again |
| `IG-MODE-10` | `execution-modes.md`; `multi-agent-execution.md`; mode harness | explicit-switch-barrier; automatic-no-switch; switch-preserves-candidates-and-scope |
| `IG-MODE-11` | `SKILL.md` §1-3; `modes/solo.md`; `strategic-explainer.md`; mode harness | solo-one-issue; solo-many-issues-sequential; solo-current-profile-after-model-change; solo-zero-subagents; solo-native-publication; solo-terminal-only |
| `IG-HELP-01` | `SKILL.md` §0; `mode-help.md` | all-five-modes-brief; default-is-resolver; narrow-difference-answer; help-has-no-task-manager-goal-title-or-subagents; mixed-help-delivery-preserves-gates |
| `IG-MA-01` | `SKILL.md` §2; `multi-agent-execution.md` | two-independent-packets; useful-critic; intentional-candidate; one-lane-no-filler; solo-delegation-forbidden |
| `IG-MA-02` | `multi-agent-execution.md` | disjoint-surfaces; ordinary-conflicting-surfaces; isolated-intentional-overlap |
| `IG-MA-03` | `multi-agent-execution.md` | dependency-ready-frontier |
| `IG-MA-04` | `multi-agent-execution.md` | adaptive-width; swarm-useful-width; no-filler-packet |
| `IG-MA-05` | `SKILL.md` §2; `multi-agent-execution.md` | coordinator-only-fan-in-and-writes |
| `IG-MA-06` | `multi-agent-execution.md`; `writer_worktree_guard.py` | two-phase-admission; shared-main-rejected; integration-canary |
| `IG-MA-07` | `multi-agent-execution.md`; `writer_worktree_guard.py` | exclusive-writable-owner; duplicate-branch-and-path-rejected |
| `IG-MA-08` | `multi-agent-execution.md` | read-only-role-no-worktree |
| `IG-MA-09` | `multi-agent-execution.md` | complete-packet-contract |
| `IG-MA-10` | `SKILL.md` §2; `multi-agent-execution.md` | exact-integrated-verification |
| `IG-MA-11` | `multi-agent-execution.md` | redispatch-after-return-and-scope-change |
| `IG-MA-12` | `SKILL.md` §2; `multi-agent-execution.md`; `writer_worktree_guard.py`; trace harness | startup-inventory-before-fresh-work; branch-only-restored; dirty-checkpoint-resumed; active-owner-rejected; ambiguous-preserved; intentional-candidate-not-replacement |
| `IG-MA-13` | `multi-agent-execution.md` | explicit-profile-preserved |
| `IG-MA-14` | `modes/classic.md`; `multi-agent-execution.md` | classic-simple-luna-max; classic-small-diff-not-simple |
| `IG-MA-15` | `modes/*.md`; `multi-agent-execution.md` | solo-current-main-only; classic-material-controller; balance-economical-bulk; swarm-economical-waves; economical-economical-controller |
| `IG-MA-16` | `modes/{classic,balance,swarm,economical}.md`; `multi-agent-execution.md` | luna-uncertainty-evidence-handoff; mode-specific-next-route; same-luna-retry-rejected |
| `IG-MA-17` | `modes/{classic,balance,swarm,economical}.md`; `multi-agent-execution.md` | classic-luna-unavailable-controller; economical-fallback-no-silent-expensive-spend |
| `IG-MA-18` | `multi-agent-execution.md`; `strategic-explainer.md` | explainer-outside-worker-routing; worker-evidence-coordinator-facade; nested-facade-no-new-task; solo-native-no-provider |

## Быстрый mode corpus

`scripts/issue_grinder_mode_harness.py` является исполнимой таблицей только для
механически разрешимых частей mode contract. Он проверяется командой:

```bash
python3 -B -m unittest discover -s tests -p 'test_issue_grinder_mode_harness.py'
```

Corpus доказывает:

- приоритет явного канонического режима над automatic rule;
- `Соло` как явный пятый mode, который использует фактически current main
  profile каждого turn, запрещает subagents и ограничивает исполнение одной
  последовательной lane;
- `Экономичный` для exact `gpt-5.6-luna` при каждом доступном effort и
  `Классический` для другого family identity без fuzzy match;
- сохранение mode record при доказанной continuity и отсутствие переноса
  старого record в новый run;
- схлопывание Luna-профилей в Luna Max, сохранение non-Luna controller-а и
  независимый приоритет role overrides;
- полноту resumable checkpoint, запрет ложного `complete`/`blocked` и
  обязательный активный Task Manager status/Goal;
- явный switch только после quiescent writers, неизменного integration checkout,
  reconciliation ownership и сохранения evidence.

Harness принимает уже распознанный канонический mode. Он не доказывает качество
понимания свободной пользовательской формулировки, декомпозиции, выбора
полезного агента, различия подходов `Роя`, code review или фактического
исполнения Markdown runtime. Эти свойства остаются model-forward cases и
наблюдаемым результатом реальных прогонов.

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
- incomplete/raw-error report был опубликован;
- общий report не перечислил все подтверждённые причины либо для хотя бы
  одной причины нет отдельного ответа;
- reason-specific answer не объяснил, почему причина блокирует цель, почему
  Issue Grinder не может устранить её сам или зачем нужен заблокированный шаг для цели;
- остановка или `update_goal(blocked)` произошли до публикации общего report и всех
  отдельных ответов;
- caller error Strategic Explainer превратился в blocker вместо исправления;
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

- видеть `issue-grinder:issue-grinder` и `issue-grinder:task-composer`;
- не видеть установленный `ship-tasks:ship-tasks`;
- видеть Task Manager dependency и optional Strategic Explainer;
- на чистый вопрос о режимах/default/различиях дать краткую справку о пяти
  режимах без Task Manager, Goal, title mutation, delivery loop и subagents;
- правильно различать explicit delivery, implicit exact selector, implicit
  missing selector и read/status/planning negative prompts;
- на новых synthetic runs выбрать `Экономичный` для Luna при `none`, `low`,
  `medium`, `high`, `xhigh` и `max`, а для non-Luna — `Классический`; любой явно
  выбранный канонический режим должен победить automatic rule, а продолжение
  после смены модели — сохранить ранее выбранный mode;
- наблюдаемо различить режимы: в `Классическом` Sol/controller делает почти
  всё, а Luna получает только тривиальные packets; `Соло` сохраняет current
  model, ноль subagents и native publication для одного и нескольких issue; в
  `Балансе` Luna сначала пытается выполнить лёгкие и средние bounded tasks и при
  существенной проблеме возвращает evidence fallback Sol/controller-у; `Рой`
  создаёт isolated intentional candidates и сокращает их до одного; `Экономичный`
  сохраняет один resumable candidate без ложного `Done`/Goal completion;
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
  трёхчастный ответ по каждой причине.

Static, deterministic и registration checks не заменяют этот model-forward
smoke; если live synthetic run не выполнен, это указывается как непроверенная
часть, а не считается автоматически пройденной.

Узкий smoke прогрессивной загрузки запускается отдельно:

```bash
python3 scripts/issue_grinder_mode_loading_smoke.py \
  --model gpt-5.6-luna \
  --reasoning-effort low
```

Runner создаёт по одной fresh ephemeral read-only Codex-сессии для каждого из
пяти explicit mode. По наблюдаемым command-execution events case проходит,
только если агент полностью открыл installed `SKILL.md`, общий
`execution-modes.md` и ровно один выбранный файл из `references/modes/`.
Открытие соседнего mode-файла, broad access ко всему каталогу, отсутствие
обязательного чтения или расходящийся итоговый receipt закрывают case. Этот
smoke проверяет progressive disclosure, но не доказывает соблюдение model
routing и topology во время полноценной delivery.
