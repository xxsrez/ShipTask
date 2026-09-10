"""Regression guards for mandatory Goal-stop advice versus ordinary publication."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


class BlockerConsultantContract(unittest.TestCase):
    def test_goal_branch_has_priority_over_ordinary_skip_rules(self):
        routing = read('issue-grinder/references/consultant.md')
        ordinary, blocker = routing.split('## Перед остановкой из-за блокировки Goal')
        self.assertIn('Astra или unknown profile автоматического вызова нет', ordinary)
        self.assertIn('имеет приоритет', blocker)
        self.assertIn('включая\nunknown profile', blocker)
        self.assertIn('Astra сама проверяет', blocker)
        self.assertIn('отдельного Консультанта не вызывает', blocker)
        self.assertIn('не зависит от', blocker)

    def test_blocker_is_not_routed_back_through_explainer(self):
        entry = read('issue-grinder/SKILL.md')
        routing = read('issue-grinder/references/strategic-explainer.md')
        self.assertIn('blocker-report без Goal', entry)
        self.assertIn('Strategic Explainer здесь не вызывается', entry)
        self.assertIn('включая редактуру полученного вывода', ' '.join(routing.split()))
        self.assertIn('одним запросом Консультанту', routing)

    def test_unavailable_advice_cannot_become_accepted_blocker(self):
        routing = read('issue-grinder/references/consultant.md')
        self.assertIn('не является принятым blocker fingerprint', routing)
        self.assertIn('не разрешает\n`update_goal(blocked)`', routing)
        self.assertIn('Не обходи запрет на субагентов', routing)
        self.assertIn('не вызывает\nновую консультацию', routing)

    def test_advice_keeps_repair_and_decision_with_caller(self):
        routing = read('issue-grinder/references/consultant.md')
        self.assertIn('выполни его, проверь результат и продолжи delivery', routing)
        self.assertIn('решение и записи остаются у coordinator', routing)
        self.assertIn('не передавай execution/review пакет', routing.lower())
        solo = read('issue-grinder/references/modes/solo.md')
        self.assertIn('Он не получает execution packet', solo)

    def test_consultant_honors_required_workflow_without_profile_substitution(self):
        skill = read('consultant/SKILL.md')
        self.assertIn('обязательный запрос явно применимого workflow', skill)
        self.assertIn('не отменяет исключение для подтверждённой Astra', skill)
        self.assertIn('fork_turns="none"', skill)
        self.assertIn('reasoning_effort="medium"', skill)
        self.assertIn('не подменяй модель', skill)


if __name__ == '__main__':
    unittest.main()
