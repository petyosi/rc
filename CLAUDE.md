# Project Purpose

This is an **RC (Run Commands) configuration repository**. Files in this project are designed to be symlinked to the home directory (`~`) for system-wide use.

**Key points:**

- `skills/` is the portable source of truth for global skills in this repo
- `python3 scripts/install-skills.py` links each skill into `~/.claude/skills/` and `~/.agents/skills/`
- Keep personal skills and selected third-party copies in Git; retain upstream licenses and sources in `skills/SOURCES.json`
- Do not use skills.sh to install or update the live skill directories. Import updates into this repo and review the diff first
- Built-in, plugin, and Claude-synced skills remain application-managed; do not copy their caches into Git
- Files in this repo are configuration templates, not project-specific implementations
- All skills developed here are **global skills** available across all projects
- Installation scripts handle the symlinking to home directory

When documenting or updating skills in this project, always refer to them as **global skills** that work system-wide, not project-specific skills.
