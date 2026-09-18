---
name: codex-cold-review
description: Run an independent, read-only review of uncommitted changes, the current branch, or a pull request when asked for a cold, second-opinion, or Codex review. Use Codex only when explicitly requested as the reviewer; otherwise use a fresh subagent or the main agent according to prior session context.
---

# Cold Review

Keep the reviewer independent of prior implementation discussion and conclusions.

## Select the reviewer

1. If the user explicitly asks for Codex as the reviewer, such as "cold Codex review" or "have Codex review this", use the Codex runner below. Merely mentioning Codex as the author or caller does not select it. The skill name `/codex-cold-review` alone does not select Codex either.
2. Otherwise, if this session already contains implementation work, discussion, or review conclusions about the target, start one fresh `general-purpose` subagent with the Agent tool. Give it only the repository path, review scope, and the review instructions below. Do not use `fork`, and do not pass your conclusions or suspected issues.
3. Otherwise, perform the review in the main agent. A fresh Claude session invoked by Codex to review Codex's work belongs here. Receiving the target material in the review request does not by itself require a subagent.

A delegated reviewer must perform the review directly. It must not invoke this skill again, launch Codex, or delegate another review. If a fresh subagent is unavailable, state the independence limit and review directly; do not fall back to Codex.

## Prepare the target

1. Confirm that the current directory is the intended repository.
2. Translate the user's scope into a short target description. Use `current worktree, including committed, staged, unstaged, and untracked changes` by default.
3. For a pull request, include its URL or number. Do not check out another branch unless the user requested it. The runner's read-only sandbox permits `gh pr view` and `gh pr diff`.
4. When delegating, do not pre-review or explain suspected issues to the reviewer. Preserve the independence of the review.

## Review directly or with a fresh subagent

Read applicable repository guidance, the complete diff, and enough surrounding code to check behavior and callers. Include staged, unstaged, and untracked changes when in scope; do not require a commit first. Focus on actionable bugs introduced by the changes, regressions, and violated repository requirements. For each finding, provide severity, file and line references, a concrete failure scenario, and supporting evidence. Exclude speculative concerns and style preferences.

Keep the review read-only. Do not edit files, alter git state, post comments, or update pull requests. Do not run builds, type checks, formatters, or broad test suites. Return findings for assessment below, or state that no actionable issues were found and identify material scope limits.

## Run Codex only when explicitly requested

Execute:

```bash
~/.claude/skills/codex-cold-review/scripts/run-review.sh \
  --target "<target description>"
```

Add `--output /absolute/path/report.md` only when the user requests a durable report. Otherwise, let the runner create a temporary report.

The runner must use Codex `gpt-5.6-sol` (Sol) with `medium` effort by default. Do not weaken this setting without explicit user approval; pass `--model` or `--effort` only when the user asks for a different one. It invokes a non-persistent (`--ephemeral`) session with a `read-only` sandbox and hands Codex the sibling `code-review` global skill as the review contract, so both reviewers follow the same rubric.

If execution fails because Codex is not installed or authenticated, report the exact failure and the required setup. Do not substitute an internal Claude review without saying so.

## Read and assess the findings

1. Read the complete reviewer response. For the Codex runner, read the report at its printed `REPORT_PATH`.
2. Verify each finding against the local diff and cited code before presenting it as confirmed.
3. Separate confirmed findings from findings that are uncertain or false positives.
4. Preserve file and line references. Use clickable `file:line` references in the final response.
5. State the reviewed target and the actual reviewer: Codex Sol at medium effort, a fresh subagent, or the main agent.
6. Do not modify code unless the user also asks for fixes.

Keep the handoff concise. Lead with confirmed findings in severity order. If none survive verification, state that the cold review found no confirmed issues and mention any important residual test or scope limits.
