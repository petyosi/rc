# Global Codex Instructions

## Working Style

- Prefer surgical edits over rewrites or large, sweeping changes.

## Communication Style

- Apply ASD-STE100 principles to all responses.
- Keep each response concise, complete, and easy to understand.
- Remove information that does not help the user.
- Let the completed work show the result.
- Format according to the user's needs.
- Include all necessary context.
- Keep post-task summaries concise: state what was done and the important outcomes.
- Do not use flattery, self-congratulation, emojis, or emoticons.
- Skip detailed explanations unless they help the user make a decision, verify the result, or address a problem.

## Code Comments

- Write comments to explain why, constraints, or non-obvious contracts. Do not restate what the code already expresses.
- Avoid section labels, step numbers, and comments that repeat assignments or conditionals.

## NPM Package Installation

- Before installing a new npm package, use `npm info <package> version` or `pnpm info <package> version` to determine the current version.
- Follow existing version constraints when the package manifest, lockfile, or peer dependencies require a specific version.

## Commit and PR Guidelines

- When creating a Git branch, prefix its name with the GitHub username `petyosi/`.
- When creating pull requests, do not prefix PR titles with `[codex]`.
- Unless asked to, always open pull requests as ready to review, not draft.
- Do not co-sign commits or PRs with Codex, and do not add AI-attribution footers.
- Do not include testing checklists in PR descriptions.
- Do not assign reviewers or labels unless asked.
- Write commit messages and PR titles and descriptions to convey the intent and motivation of the change. Mention implementation details only when they clarify the result.
- Write PR titles and descriptions for a human reviewer who does not already know the implementation.
- Use a short, plain-language PR title that states the user-visible or operational outcome. Prefer an active result such as "Make Logfire app startup failures visible" over an implementation label such as "Add bootstrap telemetry".
- Lead the PR description with the problem and why it matters. Then explain the observable behavior, how a person or system will use the result, and any important limits, privacy boundaries, rollout constraints, or unresolved follow-up work.
- Describe implementation details only after the human outcome is clear, and only when they help a reviewer assess behavior, risk, or tradeoffs.
- Use concrete domain language. Define or replace internal terms that a product, engineering, or operations reader would not understand immediately.
- Keep PR descriptions easy to scan. Use descriptive sections when they help, such as `Why`, `What changes`, `How to use it`, and `Limits`. Do not include a section only to satisfy a template.
- State what the change deliberately does not do when that boundary prevents a likely misunderstanding.
