---
name: code-review
description: Pre-PR code review for branch changes. Use when user wants to review changes before opening a PR, asks to check their branch for issues, or mentions code review. Analyzes diff against base branch for code quality, bugs, security vulnerabilities, logical fallacies, and style/convention violations. Provides detailed analysis with file:line references and improvement suggestions.
---

# Code Review Skill

Review code changes on a branch before opening a PR. Provides detailed analysis of diffs against the base branch.

## When to Use This Skill

Activate this skill when the user:

- Asks to review changes before opening a PR
- Wants a code review of their current branch
- Asks to check for issues in their changes
- Mentions reviewing their work before submitting
- Says things like "review my changes", "check my code", "ready for PR"

## Review Focus Areas

### 1. Code Quality & Bugs

- Logic errors and potential bugs
- Null/undefined handling issues
- Off-by-one errors, boundary conditions
- Resource leaks (unclosed handles, missing cleanup)
- Race conditions and concurrency issues
- Error handling gaps
- Code complexity (deeply nested logic, long functions)
- Dead code or unreachable branches

### 2. Security Vulnerabilities

- Injection risks (SQL, command, XSS)
- Authentication/authorization issues
- Sensitive data exposure (secrets, PII in logs)
- Insecure cryptographic practices
- Path traversal vulnerabilities
- CSRF, SSRF risks
- Unsafe deserialization
- Hardcoded credentials or secrets

### 3. Logical Fallacies & Reasoning Errors

- Incorrect assumptions in conditionals
- Flawed boolean logic (De Morgan violations)
- Incomplete state handling
- Missing edge cases
- Incorrect operator precedence assumptions
- Type coercion pitfalls
- Temporal coupling issues
- Invalid invariant assumptions

### 4. Style & Conventions

- Naming consistency (variables, functions, files)
- Project pattern adherence
- Import organization
- Code formatting issues
- Inconsistent error handling patterns
- Deviation from existing codebase conventions
- Missing or excessive comments

## Review Process

### Step 1: Identify Branch Context

```bash
# Get current branch name
git branch --show-current

# Get base branch (usually main or master)
git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'

# Get commit history for this branch
git log --oneline $(git merge-base HEAD origin/main)..HEAD
```

### Step 2: Gather Changes

```bash
# Get full diff against base branch
git diff origin/main...HEAD

# Get list of changed files
git diff --name-only origin/main...HEAD

# Get diff stats
git diff --stat origin/main...HEAD
```

### Step 3: Understand Context

For each changed file:

1. Read the full file (not just the diff) to understand context
2. Identify the purpose of the changes
3. Look for related files that might be affected
4. Check for existing patterns in the codebase

### Step 4: Analyze Changes

For each category, systematically review:

#### Code Quality Analysis

- Trace execution paths through new/modified code
- Check error handling completeness
- Verify resource management
- Look for complexity that could be simplified
- Check for potential null/undefined access

#### Security Analysis

- Identify all user input entry points
- Trace data flow from input to output
- Check for proper sanitization/validation
- Verify authentication/authorization checks
- Look for sensitive data handling

#### Logic Analysis

- Verify boolean conditions are correct
- Check edge cases are handled
- Validate state transitions
- Confirm loop termination conditions
- Check type handling

#### Style Analysis

- Compare against existing codebase patterns
- Check naming conventions match project
- Verify import organization
- Look for formatting inconsistencies

### Step 5: Generate Report

Structure findings by severity and category.

## Output Format

### Summary Section

```markdown
## Code Review Summary

**Branch:** `feature/xyz` -> `main`
**Files Changed:** N files (+X/-Y lines)
**Commits:** N commits

### Overview
[1-2 sentence summary of what these changes do]

### Risk Assessment
- **Critical Issues:** N
- **Warnings:** N
- **Suggestions:** N
```

### Findings Section

For each issue found, provide:

```markdown
### [CRITICAL/WARNING/SUGGESTION] Category: Brief Description

**Location:** `path/to/file.ts:123-145`

**Issue:**
[Detailed explanation of what the problem is and why it matters]

**Code:**
```language
[relevant code snippet]
```

**Suggested Fix:**
```language
[improved code or approach]
```

**Rationale:**
[Why this fix is better, what it prevents]
```

### Severity Definitions

- **CRITICAL**: Must fix before merge. Security vulnerabilities, data loss risks, breaking bugs.
- **WARNING**: Should fix. Bugs that may occur under certain conditions, significant code quality issues.
- **SUGGESTION**: Consider fixing. Style issues, minor improvements, optional enhancements.

### Positive Findings

Also note well-done aspects:

```markdown
## What's Done Well

- [Positive observation about the changes]
- [Good patterns followed]
- [Effective solutions]
```

### Final Checklist

```markdown
## Pre-PR Checklist

- [ ] All critical issues addressed
- [ ] Tests added/updated for changes
- [ ] No secrets or credentials in code
- [ ] Error handling is complete
- [ ] Documentation updated if needed
```

## Review Behavior Rules

### Always

- Read full files, not just diffs, to understand context
- Provide specific file:line references
- Explain WHY something is an issue, not just WHAT
- Suggest concrete fixes with code examples
- Consider the broader impact of changes
- Acknowledge good patterns and solutions

### Never

- Flag issues that don't exist in the diff (unless security-critical)
- Suggest purely stylistic changes that contradict project conventions
- Recommend over-engineering simple code
- Miss obvious security vulnerabilities
- Provide vague feedback without actionable suggestions

### Calibration

- Be thorough but not pedantic
- Focus on issues that matter
- Adjust depth based on change size (small fix vs large feature)
- Consider the experience level implied by the code

## Example Review Scenarios

### Scenario 1: Simple Bug Fix

```
User: "Review my changes before I open a PR"

AI: [Activates skill]
    1. Identifies branch and base
    2. Gets diff (small, focused change)
    3. Reviews the specific fix
    4. Checks for regression risks
    5. Provides concise review focused on the fix
```

### Scenario 2: New Feature

```
User: "Can you do a code review of this branch?"

AI: [Activates skill]
    1. Identifies branch context
    2. Gets full diff (multiple files)
    3. Understands feature purpose from commits/code
    4. Deep review of each category
    5. Comprehensive report with all findings
```

### Scenario 3: Security-Sensitive Changes

```
User: "Review my auth changes before PR"

AI: [Activates skill]
    1. Identifies auth-related changes
    2. Prioritizes security analysis
    3. Traces all auth flows
    4. Checks for common auth vulnerabilities
    5. Detailed security-focused report
```

## Integration with Git Workflow

After review is complete, suggest next steps:

```markdown
## Next Steps

1. Address critical issues (if any)
2. Consider warnings based on priority
3. Run tests: `npm test` / `pytest` / etc.
4. Create PR when ready: `gh pr create`
```

## Skill Invocation Examples

This skill should activate when user says:

- "Review my changes"
- "Code review before PR"
- "Check my branch for issues"
- "Review this before I open a PR"
- "Can you review my code?"
- "What issues do you see in my changes?"
- "Pre-PR review"
- "Review the diff"

## Notes

- This skill focuses on changes only, not the entire codebase
- It assumes the base branch is clean/correct
- Security issues are always flagged regardless of severity threshold
- The review adapts depth based on change size and complexity
- When in doubt, flag it - better to over-communicate than miss issues
