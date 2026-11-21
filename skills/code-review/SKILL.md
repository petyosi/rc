---
name: code-review
description: Pre-PR code review for branch changes. Use when user wants to review changes before opening a PR, asks to check their branch for issues, or mentions code review. Finds bugs, regressions, security problems, and violations of repository guidance in the diff against the base branch, and reports each finding with file:line references, a failure scenario, severity, and confidence.
---

# Code Review

Review the changes before a PR is opened. Find defects that the changes introduce or fail to fix. Do not review style or scope; `pr-interrogate` covers scope.

This contract works for any agent (Claude Code, Codex, or another). The cold-review runners in `claude-cold-review` and `codex-cold-review` hand it to their reviewer as-is.

## Scope

- Review the target the user names. By default, review the current branch against its base, plus staged, unstaged, and untracked changes. Do not ask for a commit first.
- Find the base with `git symbolic-ref refs/remotes/origin/HEAD`; fall back to `main` or `master`. Use the merge base (`git diff <base>...HEAD`) for committed changes and `git diff HEAD` plus `git status` for the rest.
- For a pull request, use read-only `gh pr view` and `gh pr diff` when local data is not sufficient.
- Stay read-only. Do not edit files, change git state, post comments, or update the PR. Do not run builds, type checks, formatters, or broad test suites; CI covers them.

## Prepare

1. Read the repository guidance that applies to the changed files: `CLAUDE.md` and `AGENTS.md` at the root and in the changed directories.
2. Read the complete diff, the commit messages, and the PR description when there is one. Write down the **stated intent**: each claim about what the change fixes, keeps, prevents, or adds. This is the specification. Do not accept the code's current behavior as the expected behavior.
3. Scale the depth to the change. For a small, local change, read the diff and its direct callers and callees. For a refactor, a concurrency change, or a parser, read the full changed files, follow callers across files, and check `git log` and `git blame` where earlier behavior matters.

## What to look for

Check the general things (logic errors, wrong conditions, unhandled failures, security problems, resource leaks). Give extra attention to these, which reviews often miss:

- **Claims that do not hold everywhere.** For each claim in the stated intent, trace every path that reaches the affected behavior: other callers, other component or editor instances, focus or selection changes while async work is pending, and repeated or overlapping calls.
- **Incomplete fixes.** When the change fixes a failure, check whether a sibling path still reaches the same failure. Report it even when that path is older than the change, because the change claims to fix it.
- **User expectations.** Where a behavior has an obvious user expectation (a cancelled operation leaves no trace, a retry does not duplicate work, a saved setting survives a reload), compare the result with that expectation. Report a mismatch even when the commit message calls it intended.
- **Ignored signals.** A caller ignores a `false`, `null`, or error return. A promise is not awaited or its rejection is not handled. State that a callee sets asynchronously is read before it is ready. An event is emitted with no listener.
- **Partial coverage of an input space.** Code handles some variants but not all: single quotes but not double quotes, 4xx but not 5xx, two of three union members.
- **Guards that do not match the language.** `typeof x === 'object'` passes for `null` and arrays. `!value` rejects `0` and `""`. `x == null` matches both `null` and `undefined`.
- **Refactoring regressions.** After a split, an extraction, or a moved call site, check that explicit non-default values (props, options, timeouts, limits, thresholds) are still present.
- **Wrong execution scope.** Module-level code that opens connections or starts work for every importer. Subscriptions or timers without cleanup. Code that assumes it runs once but runs repeatedly.
- **Guidance violations.** A change that breaks a specific rule in `CLAUDE.md`, `AGENTS.md`, or an existing code comment. Cite the rule.

## What counts as a finding

Report an issue only when you can give one of these:

- a concrete, reachable failure scenario: the input or sequence of events, and the wrong result, or
- a specific written repository requirement that the change violates.

Judge an issue by whether the change causes it, not by which lines the diff touches. A changed caller that makes an old failure reachable is a finding. An old bug that the change does not affect and does not claim to fix is not.

Do not report:

- issues that linters, type checkers, or compilers catch
- style preferences and general quality remarks that no repository guidance requires
- a missing test on its own. Mention a test gap only as part of a finding, when the gap leaves that specific failure unprotected.
- speculation that you could not trace to a failure scenario

If a possible issue is real but you could not confirm it, report it with low confidence. Do not drop it, and do not raise its confidence.

## Optional delegation

Delegation is optional. Use it only when it adds independent coverage that a single pass would miss, for example a fresh-context agent that checks one high-risk path, or an agent that tries to disprove a finding. Use the session's current model; do not move review work to a weaker model. A small change needs no subagents.

## Report

Rate each finding on two separate scales:

- **Severity**: `high` (data loss, security, crash, or a broken main flow), `medium` (wrong behavior in a real but narrower case), `low` (minor or rare impact).
- **Confidence**: `confirmed` (traced or reproduced), `likely` (strong evidence, one step not verified), `possible` (plausible, not verified).

A rare but confirmed failure is `low` or `medium` severity with `confirmed` confidence. Keep it.

Use this format, with findings sorted by severity:

```markdown
## Code Review

**Target:** `{branch}` -> `{base}` (plus uncommitted changes, if any)
**Files changed:** {count} (+{added}/-{removed})

### Findings

**1. {One-line statement of the defect}** — severity: {high|medium|low}, confidence: {confirmed|likely|possible}

- **Location:** `{file}:{line}`
- **Failure scenario:** {input or sequence} -> {wrong result}
- **Evidence:** {the code path, the guidance rule, or the stated-intent claim it breaks}
- **Fix:** {short direction; add a code snippet only when the fix is not obvious}

### Limits

{What you did not check and why, for example files too large to trace fully or a PR with no description. Omit when there are none.}
```

When there are no findings, say "No actionable issues found", then give the **Limits** section.
