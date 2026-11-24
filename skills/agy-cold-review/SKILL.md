---
name: agy-cold-review
description: Run a read-only code review of the current branch, uncommitted changes, or a pull request with the Antigravity CLI (agy, Gemini) as an independent second reviewer from another model family. Use when the user asks for an agy, Antigravity, or Gemini review, or for a second opinion from another model. Also use it without being asked, at most once per change, before opening a PR for a risky change (concurrency, cleanup or data deletion, security, parsers) when agy quota allows.
---

# agy Cold Review

agy runs Gemini models, so it catches different things than a Claude reviewer. It cannot run commands or tests to confirm a claim, and it tends to overstate severity. Treat its report as leads to verify, never as findings.

## When to run it

- The user asks for an agy, Antigravity, or Gemini review, or a second-model opinion.
- Without being asked: once per change, before a PR, when the change is risky and a second model family adds coverage. Say in one line that you are running it. Do not run it for small or mechanical changes, and do not rerun it after fixing its findings unless the user asks.
- Check quota first when running it unasked: `agy -p "/usage"` (no model call). Skip it when the Gemini five-hour or weekly limit is below 20%, and say so.

## Run

From inside the repository:

```bash
~/.claude/skills/agy-cold-review/scripts/run-review.sh --target "<short target description>"
```

- Default target: the current branch against `origin/HEAD` (or `--base REF`), plus staged, unstaged, and untracked changes. For a pull request, pass `--pr NUMBER`; the runner fetches its diff and description with `gh`.
- Run it in the background (`run_in_background`); a review takes several minutes. The runner wraps agy in `~/.claude/scripts/agent-watchdog.sh` when it exists.
- The model is `gemini-4-neon-high`. Pass `--model` only when the user names another model or that one is gone (`agy models` lists them).
- Add `--output /absolute/path/report.md` only when the user wants a durable report.

Do not pass your own conclusions or suspected issues in `--target`. Name the scope, and the issue or PR it implements when the diff alone does not show the intent.

## How the runner keeps it read-only

agy in print mode cannot ask for approval, and a refused command ends the turn with an empty response. The runner therefore:

- prepares the diff (and PR description) itself and adds that directory with `--add-dir`;
- hands agy the sibling `code-review` skill as the review contract, so every cold reviewer follows the same rubric;
- runs `--mode plan --sandbox` (no network for commands) with a per-session `--settings` overlay: deny `write_file`, `read_url`, `execute_url`, `mcp`; allow only read-only command prefixes (`git diff/log/show/blame/status/ls-files`, `rg`, `grep`, `ls`, `cat`, `head`, `tail`, `wc`). Allow rules match by literal word prefix, not glob, so `command(rg)` is right and `command(rg *)` is not. Redirects such as `2>/dev/null` and command substitution disable prefix matching;
- prints `REPORT_PATH` and `AGY_LOG`, and fails with the denied actions when agy returns no review.

If the run fails, read the end of `AGY_LOG`. A denied command means agy tried something outside the allow list; report it and do not loosen the rules or use `--dangerously-skip-permissions`.

## Assess the findings

1. Read the whole report.
2. Check every finding against the diff and the cited code. Run a small check (a command, a mutation, a test) when a claim is cheap to test; agy could not.
3. Sort the findings into confirmed, partly right (the issue is real but the scenario or severity is wrong), and wrong. Re-rate severity yourself.
4. Report the reviewer (agy, the model) and its token use, with clickable `file:line` references. Do not change code unless the user asked for fixes.
