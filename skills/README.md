# User skills

This directory contains the actual files for personal and selected third-party skills.
Git records the exact versions used across machines. Langfuse and Linear are excluded.
Built-in, plugin, and Claude-synced skills remain application-managed.

After cloning this repository, run:

```sh
python3 scripts/install-skills.py
```

The installer links each skill into `~/.agents/skills/` for Codex and
`~/.claude/skills/` for Claude. It backs up conflicting copies and retires matching
legacy entries in `~/.codex/skills/`. It preserves and reports unmanaged entries.
Backups remain in `~/.local/state/rc/skill-backups/`. No skill source download is
needed. Python 3 is required; dependencies used by individual skills are separate.

Use `--dry-run` to inspect changes or `--home /path/to/test-home` to test a fresh
installation. Run the installer again after moving the checkout or adding skills.
To remove a skill, remove its links explicitly as well as its repo directory;
the installer deliberately does not delete unmanaged entries.

Edit personal skills here. For third-party updates, download the selected files
into a temporary directory, compare them with the checked-in copy, then apply and
commit the intended changes. Retain license files and update `SOURCES.json`.
Skills.sh may be used for discovery or temporary downloads, but must not manage
these live directories. Its machine-local lock file is not the restore manifest.

`SOURCES.json` records the provenance available at import. Historical folder hashes
are copied from the old installer record; they are not Git commit pins. The files
in this repository, rather than those hashes, define the installed version.
