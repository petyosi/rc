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


if __name__ == "__main__":
    unittest.main()
