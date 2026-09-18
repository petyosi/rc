import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import tempfile
import unittest


REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("install_skills", REPO / "scripts/install-skills.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "relocated checkout"
        shutil.copytree(REPO / "skills", self.repo / "skills")
        self.user_home = self.root / "user home"

    def install(self, dry_run=False):
        with contextlib.redirect_stdout(io.StringIO()):
            installer.install(self.repo, self.user_home, dry_run)

    def test_fresh_restore_and_repeat(self):
        self.install(dry_run=True)
        self.assertFalse(self.user_home.exists())
        self.install()
        skills = [p for p in (self.repo / "skills").iterdir() if (p / "SKILL.md").is_file()]
        self.assertGreater(len(skills), 20)
        for skill in skills:
            for relative in (".agents/skills", ".claude/skills"):
                link = self.user_home / relative / skill.name
                self.assertEqual(link.resolve(), skill)
                self.assertTrue((link / "SKILL.md").is_file())
        self.install()
        self.assertFalse((self.user_home / ".local/state/rc/skill-backups").exists())

    def test_migration_preserves_conflicts_and_unmanaged_content(self):
        old = self.root / "old skills"
        (old / "synced").mkdir(parents=True)
        (old / "synced/local.md").write_text("keep local content")
        (old / "code-review").mkdir()
        (old / "code-review/SKILL.md").write_text("old Claude copy")
        claude = self.user_home / ".claude"
        claude.mkdir(parents=True)
        (claude / "skills").symlink_to(old)
        conflict = self.user_home / ".agents/skills/code-review"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("local edits")
        legacy = self.user_home / ".codex/skills/code-review"
        legacy.mkdir(parents=True)
        (legacy / "SKILL.md").write_text("legacy copy")
        builtin = legacy.parent / ".system"
        builtin.mkdir()
        (builtin / "sentinel").write_text("built-in")
        self.install()
        self.assertFalse(legacy.exists())
        self.assertFalse((claude / "skills").is_symlink())
        self.assertEqual((claude / "skills/synced/local.md").read_text(), "keep local content")
        self.assertEqual((builtin / "sentinel").read_text(), "built-in")
        backup = next((self.user_home / ".local/state/rc/skill-backups").iterdir())
        self.assertEqual((backup / ".agents/skills/code-review/SKILL.md").read_text(), "local edits")
        self.assertEqual((backup / ".codex/skills/code-review/SKILL.md").read_text(), "legacy copy")
        self.assertEqual((backup / ".claude/skills/code-review/SKILL.md").read_text(), "old Claude copy")
        self.install()
        self.assertEqual(len(list(backup.parent.iterdir())), 1)


if __name__ == "__main__":
    unittest.main()
