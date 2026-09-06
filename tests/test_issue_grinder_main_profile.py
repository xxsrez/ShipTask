import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

path=Path(__file__).resolve().parents[1]/'issue-grinder/scripts/main_profile.py'
spec=importlib.util.spec_from_file_location('main_profile',path)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
ID='00000000-0000-4000-8000-6d21e55b1d2f'

class MainProfileTest(unittest.TestCase):
    def test_latest_own_turn_wins_and_incomplete_tail_is_ignored(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'sessions';p.mkdir()
            records=[{'type':'session_meta','payload':{'id':ID}},
                     {'type':'turn_context','payload':{'model':'gpt-5.6-sol','effort':'xhigh'}},
                     {'type':'turn_context','payload':{'model':'gpt-5.6-luna','effort':'max'}}]
            (p/f'rollout-{ID}.jsonl').write_text('\n'.join(json.dumps(x) for x in records)+'\n{')
            r=module.read_profile(Path(d),ID)
            self.assertEqual((r['model'],r['effort']),('gpt-5.6-luna','max'))
    def test_no_config_or_other_session_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'sessions';p.mkdir()
            (Path(d)/'config.toml').write_text('model="gpt-5.6-luna"')
            (p/f'rollout-{ID}.jsonl').write_text(json.dumps({'type':'session_meta','payload':{'id':'other'}})+'\n')
            self.assertEqual(module.read_profile(Path(d),ID)['status'],'unknown')
            self.assertEqual(module.read_profile(Path(d),'../other')['status'],'unknown')
    def test_missing_effort_is_not_max(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'sessions';p.mkdir()
            (p/f'rollout-{ID}.jsonl').write_text(json.dumps({'type':'session_meta','payload':{'id':ID}})+'\n'+json.dumps({'type':'turn_context','payload':{'model':'gpt-5.6-luna'}})+'\n')
            self.assertEqual(module.read_profile(Path(d),ID)['status'],'unknown')
