# Custom Instructions for Claude Code

## Communication Style

- Keep summaries after task completion very concise - just the key facts without
  elaboration
- Avoid flattery, self-congratulation, or unnecessary politeness
- don't use emojis or emoticons
- Focus on what was done and any important outcomes
- Skip verbose explanations unless something went wrong or requires user attention
- Current year is 2026, use this whenever relevant (e.g. web searches, etc.)

## Code Comments

Write comments only when they explain _why_, not _what_. Do not add comments that restate what the code already expresses:

- No comments describing what a function does if the name is clear
- No comments labeling code sections (e.g., "// Calculate X", "// Handle Y case")
- No step numbers (e.g., "// 1. First do X", "// 2. Then do Y")
- No comments restating variable assignments or conditionals
- No format examples in comments when types/signatures are clear

Good: `// Tolerance for floating point comparison due to browser rounding`
Bad: `// Check if values are equal within tolerance`

## NPM Package Installation

When installing new npm packages, use `npm info <package> version` or `pnpm info <package> version` to determine the latest version. Do not rely on training data or web searches for package versions - they become stale quickly.

Exception: Follow existing version constraints when a project's package.json, lockfile, or peer dependencies require specific versions.

# Commit and PR Guidelines

- Don't co-sign commits or PRs with Claude.
- Don't include testing check lists in the PR description.
- Don't assign reviewers or labels to PRs, I'll handle that.
- Never add "Generated with Claude Code" or similar attribution footers to PR descriptions.
