---
name: code-review
description: Pre-PR code review for branch changes. Use when user wants to review changes before opening a PR, asks to check their branch for issues, or mentions code review. Analyzes diff against base branch for code quality, bugs, security vulnerabilities, logical fallacies, and style/convention violations. Provides detailed analysis with file:line references and improvement suggestions.
---

# Code Review Skill

Review code changes on a local branch before opening a PR. Uses multiple specialized agents with confidence-based scoring to minimize false positives.

## When to Use

Activate when user:

- Asks to review changes before opening a PR
- Wants a code review of their current branch
- Says things like "review my changes", "check my code", "ready for PR"

## Review Process

Follow these steps precisely:

### Step 1: Eligibility Check (Haiku Agent)

Use a Haiku agent to check if the branch is eligible for review:

- Is the branch the same as the base branch (nothing to review)?
- Are there any uncommitted changes that should be committed first?
- Are there any changes at all?

If not eligible, explain why and stop.

### Step 2: Gather CLAUDE.md Files (Haiku Agent)

Use a Haiku agent to find relevant CLAUDE.md files:

- The root CLAUDE.md file (if one exists)
- Any CLAUDE.md files in directories whose files were modified

These files contain project-specific guidelines that should inform the review.

### Step 3: Summarize Changes (Haiku Agent)

Use a Haiku agent to:

1. Run `git diff origin/main...HEAD` (or appropriate base branch)
2. Run `git log --oneline $(git merge-base HEAD origin/main)..HEAD`
3. Return a summary of what these changes do

### Step 4: Launch 5 Parallel Review Agents (Sonnet)

Launch 5 parallel Sonnet agents to independently review the changes. Each returns a list of issues with reasons:

**Agent #1: CLAUDE.md Compliance Audit**

- Audit changes to ensure they comply with CLAUDE.md guidelines
- Note: CLAUDE.md is guidance for writing code, so not all instructions apply during review

**Agent #2: Shallow Bug Scan**

- Read the file changes and do a shallow scan for obvious bugs
- Avoid reading extra context beyond the changes
- Focus on large bugs, avoid small issues and nitpicks
- Ignore likely false positives

**Agent #3: Historical Context Analysis**

- Read git blame and history of modified code
- Identify bugs in light of historical context
- Check what patterns existed before and if changes break them

**Agent #4: Related Code Review**

- Read related files that might be affected by changes
- Check for patterns in sibling files that should be followed
- Look for inconsistencies with existing code

**Agent #5: Code Comment Compliance**

- Read code comments in modified files
- Ensure changes comply with guidance in existing comments
- Check TODOs, FIXMEs, and documentation comments

### Step 5: Confidence Scoring (Parallel Haiku Agents)

For each issue found in Step 4, launch a parallel Haiku agent to score confidence (0-100):

**Scoring Rubric (give to agents verbatim):**

- **0**: Not confident at all. False positive that doesn't stand up to light scrutiny, or pre-existing issue.
- **25**: Somewhat confident. Might be real, but may be false positive. Couldn't verify it's real. Stylistic issues not explicitly in CLAUDE.md.
- **50**: Moderately confident. Verified as real issue, but might be nitpick or rare in practice. Not very important relative to rest of changes.
- **75**: Highly confident. Double-checked and verified as likely real issue that will be hit in practice. Current approach is insufficient. Very important or directly mentioned in CLAUDE.md.
- **100**: Absolutely certain. Double-checked and confirmed as definitely real issue that will happen frequently. Evidence directly confirms this.

For CLAUDE.md issues, the scoring agent must double-check that the CLAUDE.md actually calls out that issue specifically.

### Step 6: Filter by Confidence

Remove any issues with score < 80. If no issues meet this threshold, report that no significant issues were found.

### Step 7: Generate Report

Output the review in this format:

---

## Code Review

**Branch:** `{branch}` -> `{base}`
**Files Changed:** {count} files (+{added}/-{removed} lines)

### Issues Found

{For each issue with score >= 80:}

**{N}. {Brief description}** (Score: {score})

- **Location:** `{file}:{line_start}-{line_end}`
- **Reason:** {CLAUDE.md says "..." / Bug due to ... / Historical context shows ...}
- **Details:** {Explanation of the issue}

```{language}
{Relevant code snippet}
```

**Suggested Fix:**

```{language}
{Improved code}
```

---

Or if no issues found:

---

## Code Review

**Branch:** `{branch}` -> `{base}`
**Files Changed:** {count} files

No significant issues found. Checked for:

- CLAUDE.md compliance
- Obvious bugs
- Historical context violations
- Code comment compliance

---

## False Positives to Ignore

These should NOT be flagged (give to review agents):

- Pre-existing issues not introduced in this branch
- Something that looks like a bug but isn't
- Pedantic nitpicks a senior engineer wouldn't flag
- Issues linters/typecheckers/compilers catch (formatting, types, imports)
- General code quality issues unless explicitly in CLAUDE.md
- Issues called out in CLAUDE.md but silenced with lint ignore comments
- Intentional functionality changes related to the broader change
- Real issues on lines not modified in this branch

## Notes

- Do not check build signal or attempt to build/typecheck - assume CI handles this
- Use git commands to examine changes, not GitHub API
- Make a todo list first
- Cite and link each issue (if referring to CLAUDE.md, reference it)
- Focus on actionable issues that genuinely improve code quality
- The goal is to catch real bugs, not to be pedantic

## Git Commands Reference

```bash
# Get current branch
git branch --show-current

# Get base branch
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main"

# Get diff against base
git diff origin/main...HEAD

# Get changed files
git diff --name-only origin/main...HEAD

# Get diff stats
git diff --stat origin/main...HEAD

# Get commit log for branch
git log --oneline $(git merge-base HEAD origin/main)..HEAD

# Get git blame for a file
git blame {file}

# Get history for a file
git log --oneline -10 -- {file}
```

## Invocation Examples

This skill activates for:

- "Review my changes"
- "Code review before PR"
- "Check my branch for issues"
- "Review this before I open a PR"
- "Pre-PR review"
- "/pre-pr-code-review"
