import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parent.parent


class ReviewRunnerTests(unittest.TestCase):
    def test_reports_are_unique_and_output_path_works(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            mock_bin = root / "bin"
            mock_bin.mkdir()
            for name in ("claude", "codex"):
                mock = mock_bin / name
                mock.write_text("""#!/usr/bin/env python3
import pathlib, sys
prompt = sys.stdin.read()
contract = next(line.removeprefix('Review contract: ') for line in prompt.splitlines() if line.startswith('Review contract: '))
assert pathlib.Path(contract).is_file(), contract
if '--output-last-message' in sys.argv:
    pathlib.Path(sys.argv[sys.argv.index('--output-last-message') + 1]).write_text('mock review')
else:
    print('mock review')
""")
                mock.chmod(0o755)
            env = {**os.environ, "PATH": f"{mock_bin}:{os.environ['PATH']}", "TMPDIR": str(root)}
            for reviewer in ("claude", "codex"):
                reports = []
                for index in range(3):
                    command = ["bash", str(REPO / f"skills/{reviewer}-cold-review/scripts/run-review.sh")]
                    if index == 2:
                        command += ["--output", str(root / f"{reviewer} report.md")]
                    result = subprocess.run(command, cwd=REPO, env=env, text=True, capture_output=True, check=True)
                    report = Path(next(line.removeprefix("REPORT_PATH=") for line in result.stdout.splitlines() if line.startswith("REPORT_PATH=")))
                    self.assertEqual(report.read_text().strip(), "mock review")
                    reports.append(report)
                self.assertEqual(len(set(reports)), 3)
            self.assertEqual(list(root.rglob("prompt.txt")), [])

    def test_agy_runner_hands_over_the_diff_and_reports_failures(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
            git = ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t"]
            (repo / "a.txt").write_text("one\n")
            subprocess.run(git + ["add", "a.txt"], check=True)
            subprocess.run(git + ["commit", "-qm", "base"], check=True)
            subprocess.run(git + ["checkout", "-qb", "work"], check=True)
            (repo / "a.txt").write_text("two\n")
            (repo / "new.txt").write_text("untracked\n")
            mock_bin = root / "bin"
            mock_bin.mkdir()
            mock = mock_bin / "agy"
            mock.write_text("""#!/usr/bin/env python3
import json, os, pathlib, sys
prompt = sys.argv[sys.argv.index('--print') + 1]
value = lambda key: next(l.split(': ', 1)[1] for l in prompt.splitlines() if l.startswith(key))
diff = pathlib.Path(value('Complete diff of the target')).read_text()
assert pathlib.Path(value('Review contract')).is_file()
assert '+two' in diff and '+untracked' in diff, diff
settings = json.loads(sys.argv[sys.argv.index('--settings') + 1])
assert 'write_file(*)' in settings['permissions']['deny']
response = '' if os.environ.get('MOCK_EMPTY') else 'mock review'
print(json.dumps({'event': 'result', 'result': {'status': 'SUCCESS', 'response': response,
      'denied_actions': [{'action': 'command'}] if not response else None, 'usage': {}}}))
""")
            mock.chmod(0o755)
            env = {**os.environ, "PATH": f"{mock_bin}:{os.environ['PATH']}", "TMPDIR": str(root), "HOME": str(root)}
            command = ["bash", str(REPO / "skills/agy-cold-review/scripts/run-review.sh"), "--base", "main"]
            result = subprocess.run(command, cwd=repo, env=env, text=True, capture_output=True, check=True)
            report = Path(next(line.removeprefix("REPORT_PATH=") for line in result.stdout.splitlines() if line.startswith("REPORT_PATH=")))
            self.assertEqual(report.read_text().strip(), "mock review")
            failed = subprocess.run(command, cwd=repo, env={**env, "MOCK_EMPTY": "1"}, text=True, capture_output=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("denied actions", failed.stderr)


if __name__ == "__main__":
    unittest.main()
