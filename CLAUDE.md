# Project Purpose

This is an **RC (Run Commands) configuration repository**. Files in this project are designed to be symlinked to the home directory (`~`) for system-wide use.

**Key points:**

- `claude/skills/` is the portable source of truth for global skills in this repo
- Files in `claude/skills/` → will be linked to `~/.claude/skills/` for Claude Code
- Repo-owned skill directories in `claude/skills/` → will also be linked into `~/.agents/skills/` for profile-level agent discovery
- Files in this repo are configuration templates, not project-specific implementations
- All skills developed here are **global skills** available across all projects
- Installation scripts handle the symlinking to home directory

When documenting or updating skills in this project, always refer to them as **global skills** that work system-wide, not project-specific skills.
