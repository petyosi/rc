#!/usr/bin/env python3
"""Link repo-owned user skills, preserving local conflicts in a dated backup."""

import argparse
from pathlib import Path
import shutil
import tempfile


def install(repo: Path, user_home: Path, dry_run: bool = False) -> None:
    repo = repo.resolve()
    user_home = user_home.resolve()
    skills = sorted(path for path in (repo / "skills").iterdir() if (path / "SKILL.md").is_file())
    names = {path.name for path in skills}
    backup_root = None

    def backup_path(path: Path) -> Path:
        nonlocal backup_root
        if backup_root is None:
            base = user_home / ".local/state/rc/skill-backups"
            base.mkdir(parents=True, exist_ok=True)
            backup_root = Path(tempfile.mkdtemp(prefix="migration-", dir=base))
        target = backup_root / path.relative_to(user_home)
        target.parent.mkdir(parents=True, exist_ok=True)
        return target

    def backup(path: Path) -> None:
        target = backup_path(path)
        shutil.move(str(path), str(target))
        print(f"BACKUP {path} -> {target}")

    for relative in (".agents/skills", ".claude/skills"):
        directory = user_home / relative
        if directory.is_symlink():
            print(f"MATERIALIZE {directory}")
            if not dry_run:
                source = directory.resolve(strict=True)
                target = backup_path(directory)
                # Preserve the contents, not a link that may point at the old checkout layout.
                shutil.copytree(source, target, symlinks=True)
                directory.unlink()
                directory.mkdir()
                for entry in source.iterdir():
                    if entry.name in names:
                        continue
                    destination = directory / entry.name
                    if entry.is_symlink():
                        destination.symlink_to(entry.resolve())
                    elif entry.is_dir():
                        shutil.copytree(entry, destination, symlinks=True)
                    else:
                        shutil.copy2(entry, destination)
                print(f"BACKUP {directory} contents -> {target}")
        elif directory.exists() and not directory.is_dir():
            raise RuntimeError(f"Expected a directory: {directory}")
        if not dry_run:
            directory.mkdir(parents=True, exist_ok=True)

        for source in skills:
            target = directory / source.name
            if target.is_symlink() and target.resolve() == source:
                continue
            print(f"LINK {target} -> {source}")
            if not dry_run:
                if target.exists() or target.is_symlink():
                    backup(target)
                target.symlink_to(source, target_is_directory=True)

    # Codex discovers .agents/skills; retire only matching legacy copies.
    for source in skills:
        legacy = user_home / ".codex/skills" / source.name
        if legacy.exists() or legacy.is_symlink():
            print(f"RETIRE {legacy} (available through .agents/skills)")
            if not dry_run:
                backup(legacy)

    for relative in (".agents/skills", ".claude/skills", ".codex/skills"):
        directory = user_home / relative
        if directory.is_dir():
            for entry in sorted(directory.iterdir()):
                if entry.name not in names and entry.name != ".system":
                    print(f"UNMANAGED {entry}")
    if backup_root:
        print(f"Backups retained at {backup_root}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(), help="Alternate home for restore checks")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    install(Path(__file__).resolve().parent.parent, args.home.expanduser().resolve(), args.dry_run)
