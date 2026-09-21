"""Observable decisions for the four current execution modes."""
from dataclasses import replace
import unittest
from pathlib import Path
from scripts.issue_grinder_mode_harness import (
    ExecutionMode, ScopeSize, Profile, LUNA_MAX, SOL_XHIGH, BALANCE_VERSION,
    resolve_mode, mode_dispatch_policy, decide_mode_switch,
)

class FourModesTest(unittest.TestCase):
    def test_launch_button_does_not_force_a_mode(self):
        p=Path(__file__).resolve().parents[1]/'issue-grinder/agents/openai.yaml'
        prompt=next(x for x in p.read_text().splitlines() if 'default_prompt:' in x)
        self.assertIn('автовыбора',prompt)
        for name in ('Соло','Классический','Экономичный','Баланс'):
            self.assertNotIn(name,prompt)

    def test_default_matrix(self):
        self.assertEqual({m.value for m in ExecutionMode},{'solo','classic','balance','economical'})
        for model in ('gpt-5.6-luna','gpt-5.6-sol','gpt-6-astra','unknown'):
            for effort in (None,'low','high','max','xhigh'):
                for count in (0,1,2,20):
                    with self.subTest(model=model,effort=effort,count=count):
                        p=Profile(model,effort)
                        for size in ScopeSize:
                            record=resolve_mode(
                                p, scope_task_count=count, scope_size=size,
                                scope_assessment_reason='Separate billing and search features with distinct tests; independent review benefits their integration.',
                            )
                            expected='classic' if size is ScopeSize.LARGE else 'solo'
                            self.assertEqual(record.canonical_mode.value,expected)
                            self.assertEqual(record.initial_scope_size,size)

    def test_task_count_alone_never_establishes_large_scope(self):
        for p in (LUNA_MAX,SOL_XHIGH,Profile('gpt-6-astra','high')):
            self.assertEqual(resolve_mode(p,scope_task_count=100).canonical_mode,ExecutionMode.SOLO)

    def test_large_scope_requires_recorded_reason(self):
        for reason in ('', '   '):
            with self.assertRaisesRegex(ValueError,'assessment reason'):
                resolve_mode(SOL_XHIGH,scope_size=ScopeSize.LARGE,scope_assessment_reason=reason)

    def test_explicit_choice_overrides_scope_assessment(self):
        for size in ScopeSize:
            for mode in ExecutionMode:
                record=resolve_mode(LUNA_MAX,scope_size=size,explicit_mode=mode)
                self.assertEqual(record.canonical_mode,mode)

    def test_scope_reassessment_cannot_change_continuation(self):
        for initial, later in ((ScopeSize.LARGE,ScopeSize.SMALL),(ScopeSize.SMALL,ScopeSize.LARGE)):
            record=resolve_mode(SOL_XHIGH,scope_size=initial,scope_assessment_reason='Independent substantial features and integration review.')
            resumed=resolve_mode(LUNA_MAX,scope_size=later,saved_record=record,continuity_proven=True)
            self.assertIs(resumed,record)

    def test_explicit_modes_require_eligible_actual_root(self):
        for p in (LUNA_MAX,SOL_XHIGH,Profile('gpt-5.6-luna','high'),Profile('gpt-5.6-luna',None)):
            for mode in ExecutionMode:
                with self.subTest(p=p,mode=mode):
                    if mode in (ExecutionMode.BALANCE,ExecutionMode.ECONOMICAL) and p!=LUNA_MAX:
                        with self.assertRaisesRegex(ValueError,'main_profile_required'):
                            resolve_mode(p,explicit_mode=mode)
                    else:
                        self.assertEqual(resolve_mode(p,explicit_mode=mode).canonical_mode,mode)

    def test_resume_rechecks_actual_root_without_switching(self):
        for mode in (ExecutionMode.BALANCE,ExecutionMode.ECONOMICAL):
            record=resolve_mode(LUNA_MAX,explicit_mode=mode)
            self.assertIs(resolve_mode(LUNA_MAX,saved_record=record,continuity_proven=True),record)
            for p in (SOL_XHIGH,Profile('gpt-5.6-luna','high'),Profile('gpt-5.6-luna',None)):
                with self.assertRaisesRegex(ValueError,'main_profile_required'):
                    resolve_mode(p,saved_record=record,continuity_proven=True)
                with self.assertRaisesRegex(ValueError,'main_profile_required'):
                    mode_dispatch_policy(record,current_main_profile=p)

    def test_other_continuations_preserve_mode_after_model_change(self):
        for mode in (ExecutionMode.SOLO,ExecutionMode.CLASSIC):
            record=resolve_mode(SOL_XHIGH,explicit_mode=mode)
            self.assertIs(resolve_mode(LUNA_MAX,saved_record=record,continuity_proven=True),record)

    def test_switch_rejects_wrong_or_unknown_current_root(self):
        record=resolve_mode(SOL_XHIGH,explicit_mode=ExecutionMode.SOLO)
        for target in (ExecutionMode.BALANCE,ExecutionMode.ECONOMICAL):
            for p in (None,SOL_XHIGH,Profile('gpt-5.6-luna','low')):
                with self.assertRaises(ValueError):
                    decide_mode_switch(record,target,explicit_request=True,current_main_profile=p)
            waiting=decide_mode_switch(record,target,explicit_request=True,current_main_profile=LUNA_MAX,active_writer_count=1)
            self.assertFalse(waiting.may_apply_next_wave)
            switched=decide_mode_switch(record,target,explicit_request=True,current_main_profile=LUNA_MAX)
            self.assertTrue(switched.may_apply_next_wave)
            self.assertEqual(switched.mode_record.role_profiles.controller,LUNA_MAX)

    def test_legacy_balance_cannot_silently_resume(self):
        current=resolve_mode(LUNA_MAX,explicit_mode=ExecutionMode.BALANCE)
        self.assertEqual(current.mode_contract_version,BALANCE_VERSION)
        old=replace(current,mode_contract_version=None)
        with self.assertRaisesRegex(ValueError,'legacy_balance'):
            resolve_mode(LUNA_MAX,saved_record=old,continuity_proven=True)
        adopted=decide_mode_switch(old,ExecutionMode.BALANCE,explicit_request=True,current_main_profile=LUNA_MAX)
        self.assertTrue(adopted.may_apply_next_wave)
        self.assertEqual(adopted.mode_record.mode_contract_version,BALANCE_VERSION)

    def test_retired_modes_are_rejected(self):
        for name in ('swarm','manager','roy','roi','typo'):
            with self.assertRaises(ValueError):
                resolve_mode(SOL_XHIGH,explicit_mode=name)

    def test_unresolved_count_is_not_guessed(self):
        for count in (None,-1,True,'2'):
            with self.assertRaises(ValueError):
                resolve_mode(Profile('unknown','high'),scope_task_count=count)

    def test_solo_retains_current_profile_and_no_children(self):
        record=resolve_mode(LUNA_MAX,explicit_mode=ExecutionMode.SOLO)
        policy=mode_dispatch_policy(record,current_main_profile=SOL_XHIGH)
        self.assertFalse(policy.issue_grinder_execution_subagents_allowed)
        self.assertEqual(policy.execution_profile,SOL_XHIGH)

if __name__=='__main__':unittest.main()
