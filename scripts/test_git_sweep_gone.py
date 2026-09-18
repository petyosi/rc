import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parent.parent / "bin/git-sweep-gone"


class SweepTests(unittest.TestCase):
    def test_missing_origin_head_protects_custom_default_or_stops(self):
        for lookup_succeeds in (True, False):
            with self.subTest(lookup_succeeds=lookup_succeeds), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                repo = root / "repo"
                repo.mkdir()
                real_git = shutil.which("git")

                def git(*args):
                    return subprocess.run([real_git, *args], cwd=repo, check=True, capture_output=True, text=True).stdout

                git("init", "-b", "main")
                git("-c", "user.name=Test", "-c", "user.email=test@example.com", "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-m", "initial")
                git("remote", "add", "origin", "https://github.com/example/test.git")
                git("update-ref", "refs/remotes/origin/main", "HEAD")
                git("branch", "develop")
                git("branch", "topic")
                mock_bin = root / "bin"
                mock_bin.mkdir()
                wrapper = mock_bin / "git"
                wrapper.write_text(f'#!/bin/sh\n[ "$1" = fetch ] && exit 0\nexec {shlex.quote(real_git)} "$@"\n')
                wrapper.chmod(0o755)
                gh = mock_bin / "gh"
                gh.write_text("#!/bin/sh\nprintf 'develop\\n'\n" if lookup_succeeds else "#!/bin/sh\nexit 1\n")
                gh.chmod(0o755)
                result = subprocess.run(["bash", str(SCRIPT), "--apply"], cwd=repo, env={**os.environ, "PATH": f"{mock_bin}:{os.environ['PATH']}"}, text=True, capture_output=True)
                branches = git("branch", "--format=%(refname:short)").splitlines()
                self.assertIn("develop", branches)
                self.assertIn("main", branches)
                if lookup_succeeds:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertNotIn("topic", branches)
                else:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("topic", branches)
                    self.assertIn("nothing was removed", result.stderr)


if __name__ == "__main__":
    unittest.main()
