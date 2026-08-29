# Issue Grinder: observable evaluation

Статус: current Level 2 evaluation, 2026-08-29. Документ проверяет компиляцию
локальных [Requirements](requirements.md) и [Architecture](architecture.md), но
не создаёт новый policy contract.

## Слои проверки

1. Static contract связывает каждый `IG-*` с runtime surface и required
   сценарием, проверяет metadata, references и отсутствие незавершённых
   placeholders. Этот слой исполняется repository validators.
2. Детерминированные harness-ы проверяют отдельные внешние решения, порядок
   effects и механические Git-инварианты writer admission. Они не симулируют
   reasoning и поэтому являются oracle hard invariants, а не полным тестом skill.
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
| `IG-FLOW-06` | `SKILL.md` §5; trace harness | active-scope-prevents-completion |
| `IG-GOAL-01` | `SKILL.md` §1; trace harness | explicit-multi-create; implicit-no-goal; grow-and-keep |
| `IG-GOAL-02` | `SKILL.md` §1 | strategic-release-objective; issue-list-rejected |
| `IG-GOAL-03` | `SKILL.md` §5; trace harness | empty-scope-complete; active-scope-continue |
| `IG-GOAL-04` | `SKILL.md` §3; blocker harness | explanation-unlocks; true-external-blocker |
| `IG-GOAL-05` | `SKILL.md` §3 | final-reflection-continues; chat-only-final |
| `IG-GOAL-06` | `SKILL.md` §2; `task-manager-flow.md` | nonmaterial-gap-transparent; material-gap-blocks |
| `IG-GOAL-07` | `SKILL.md` §3; `strategic-explainer.md`; blocker harness | all-causes-overview; one-separate-answer-per-cause; three-lens-completeness; reason-reflection-unlocks |
| `IG-SCOPE-01` | `SKILL.md` §1; `task-manager-flow.md` | prompt-selector-precedence |
| `IG-SCOPE-02` | `SKILL.md` §1 | explicit-default-release; implicit-missing-selector |
| `IG-SCOPE-03` | `SKILL.md` §1; `task-manager-flow.md` | late-member; excluded-member; final-refresh |
| `IG-UI-01` | `SKILL.md` §1; `thread-title.md` | fresh-placeholder-renamed; meaningful-title-preserved; ambiguous-candidate-preserved; title-capability-failure-nonblocking |
| `IG-AUTO-01` | `SKILL.md` §4; `autonomy-and-environments.md` | explicit-persistence; implicit-no-extra-authority |
| `IG-AUTO-02` | `SKILL.md` §3; blocker harness | preflight-unlock; explanation-unlock |
| `IG-AUTO-03` | `SKILL.md` §4; environment harness | production-rejected; public-uat-allowed |
| `IG-AUTO-04` | `SKILL.md` §4; environment harness | default-uat; unknown-uat-before-effect |
| `IG-AUTO-05` | `autonomy-and-environments.md` | security-selector; narrow-always-readback |
| `IG-MA-01` | `SKILL.md` §2; `multi-agent-execution.md` | two-independent-packets; one-lane-no-delegation |
| `IG-MA-02` | `multi-agent-execution.md` | disjoint-surfaces; conflicting-surfaces |
| `IG-MA-03` | `multi-agent-execution.md` | dependency-ready-frontier |
| `IG-MA-04` | `multi-agent-execution.md` | adaptive-width; no-filler-packet |
| `IG-MA-05` | `SKILL.md` §2; `multi-agent-execution.md` | coordinator-only-fan-in-and-writes |
| `IG-MA-06` | `multi-agent-execution.md`; `writer_worktree_guard.py` | two-phase-admission; shared-main-rejected; integration-canary |
| `IG-MA-07` | `multi-agent-execution.md`; `writer_worktree_guard.py` | exclusive-writable-owner; duplicate-branch-and-path-rejected |
| `IG-MA-08` | `multi-agent-execution.md` | read-only-role-no-worktree |
| `IG-MA-09` | `multi-agent-execution.md` | complete-packet-contract |
| `IG-MA-10` | `SKILL.md` §2; `multi-agent-execution.md` | exact-integrated-verification |
| `IG-MA-11` | `multi-agent-execution.md` | redispatch-after-return-and-scope-change |
| `IG-MA-12` | `SKILL.md` §2; `multi-agent-execution.md`; `writer_worktree_guard.py`; trace harness | startup-inventory-before-fresh-work; branch-only-restored; dirty-checkpoint-resumed; active-owner-rejected; ambiguous-preserved |
| `IG-MA-13` | `multi-agent-execution.md` | explicit-profile-preserved |
| `IG-MA-14` | `multi-agent-execution.md` | simple-luna-max; small-diff-not-simple |
| `IG-MA-15` | `multi-agent-execution.md` | material-packet-current-profile |
| `IG-MA-16` | `multi-agent-execution.md` | luna-uncertainty-handoff-no-retry |
| `IG-MA-17` | `multi-agent-execution.md` | luna-unavailable-current-profile |
| `IG-MA-18` | `multi-agent-execution.md`; `strategic-explainer.md` | explainer-outside-worker-routing |

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

## Fresh smoke acceptance

После install/upgrade новая Codex-сессия должна:

- видеть `issue-grinder:issue-grinder` и `issue-grinder:task-composer`;
- не видеть установленный `ship-tasks:ship-tasks`;
- видеть Task Manager dependency и optional Strategic Explainer;
- правильно различать explicit delivery, implicit exact selector, implicit
  missing selector и read/status/planning negative prompts;
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
