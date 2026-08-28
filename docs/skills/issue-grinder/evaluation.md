# Issue Grinder: observable evaluation

Статус: current Level 2 evaluation, 2026-08-28. Документ проверяет компиляцию
локальных [Requirements](requirements.md) и [Architecture](architecture.md), но
не создаёт новый policy contract.

## Слои проверки

1. Static contract связывает каждый `IG-*` с runtime surface и сценарием,
   проверяет metadata, references и отсутствие незавершённых placeholders.
2. Детерминированный trace harness наблюдает только внешние решения и порядок
   effects. Он не симулирует reasoning и не становится runtime engine.
3. Model-forward cases запускают установленный skill в новой сессии на
   синтетическом Task Manager scope; generator не получает rubric или expected
   answer.
4. Distribution smoke проверяет source → Marketplace → installed cache,
   activation и отсутствие одновременно установленного ShipTask.

## Coverage map

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
| `IG-SCOPE-01` | `SKILL.md` §1; `task-manager-flow.md` | prompt-selector-precedence |
| `IG-SCOPE-02` | `SKILL.md` §1 | explicit-default-release; implicit-missing-selector |
| `IG-SCOPE-03` | `SKILL.md` §1; `task-manager-flow.md` | late-member; excluded-member; final-refresh |
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
| `IG-MA-06` | `multi-agent-execution.md` | separate-branch-worktree-before-write |
| `IG-MA-07` | `multi-agent-execution.md` | exclusive-writable-owner |
| `IG-MA-08` | `multi-agent-execution.md` | read-only-role-no-worktree |
| `IG-MA-09` | `multi-agent-execution.md` | complete-packet-contract |
| `IG-MA-10` | `SKILL.md` §2; `multi-agent-execution.md` | exact-integrated-verification |
| `IG-MA-11` | `multi-agent-execution.md` | redispatch-after-return-and-scope-change |
| `IG-MA-12` | `multi-agent-execution.md` | quiescent-takeover; active-owner-rejected |
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
- incomplete/raw-error report был опубликован;
- caller error Strategic Explainer превратился в blocker вместо исправления;
- public UAT, синтетический fixture или непроверенная альтернатива были названы
  terminal причиной без попытки самостоятельного продолжения;
- optional improvement создал бесконечную итерацию.

Структурная полнота отчёта проверяется отдельно от качества прозы: stopped work,
primary cause, checkpoint, unverified remainder, impact, user action и resume
condition обязательны. Model-forward evaluator дополнительно проверяет, что
текст естественно объясняет причинную связь и не переносит основной смысл в
внутренние термины.

## Fresh smoke acceptance

После install/upgrade новая Codex-сессия должна:

- видеть `issue-grinder:issue-grinder` и `issue-grinder:task-composer`;
- не видеть установленный `ship-tasks:ship-tasks`;
- видеть Task Manager dependency и optional Strategic Explainer;
- правильно различать explicit delivery, implicit exact selector, implicit
  missing selector и read/status/planning negative prompts;
- на synthetic blocker case продолжить после найденного safe action, а на
  настоящем authority blocker-е дать полный причинный report.

Static, deterministic и registration checks не заменяют этот model-forward
smoke; если live synthetic run не выполнен, это указывается как непроверенная
часть, а не считается автоматически пройденной.
