# PRP Artifact Format

Use these formats as shapes, not forms. Omit optional sections that add no decision or evidence.

## PRP

```markdown
---
repo: /absolute/path/to/current/workspace
status: planned
---

# <Outcome-oriented title>

## Goal

State the user-visible or operational result and why it matters.

## Scope

- In: <behavior or boundary included>
- Out: <likely misunderstanding that is deliberately excluded>

## Acceptance

### CX-1: <observable promise>

- Given: <consumer-visible starting state>
- When: <action through a supported boundary>
- Then: <observable result or recovery behavior>
- Evidence: <specific command, journey, fixture, or environment>

Add only scenarios needed to define the outcome and material failure behavior.

## Plan

1. <Coherent implementation outcome>
   - Likely paths or symbols: `<path>`
   - Covers: `CX-1`
2. <Next outcome, if needed>
   - Covers: `CX-1`, `CX-2`

Describe intent, ownership, and integration points. Do not prescribe obvious line-by-line edits.

## Validation

- Focused: `<cheap command or procedure used while iterating>`
- Integrated: `<final repository gate appropriate to the change>`
- Acceptance: `CX-1` through <evidence surface>

## Open Decisions

- <Only unresolved decisions that can materially change the implementation>

## Risks

- <Only material failure modes or compatibility limits>
```

During execution, optionally add:

```markdown
## Outcome

- Material deviations: none
- Evidence: <commands and concise results>
- Remaining risks: none
```

When verification was requested, add:

```markdown
## Verification

| Scenario | Grade | Evidence | Limitation |
|---|---|---|---|
| `CX-1` | `DIRECT` | <observation> | None |

Verdict: <ready, gap, or blocked>
```

## Roadmap

```markdown
---
repo: /absolute/path/to/current/workspace
status: planned
---

# <Initiative title>

## Goal

State the end result and why one PRP cannot deliver it safely.

## Constraints

- <Ordering, rollout, migration, or compatibility constraint>

## Steps

| Step | Outcome | Depends on | Produces | Validation | Status |
|---|---|---|---|---|---|
| 1 | <bounded outcome> | None | <contract or evidence> | <boundary> | `PENDING` |
| 2 | <bounded outcome> | Step 1 | <contract or evidence> | <boundary> | `BLOCKED` |

## Decisions

- <Only decisions shared across multiple steps>

## Risks

- <Only initiative-level risks>
```

Create a child PRP only when its dependencies are satisfied. Keep implementation detail in the child, not the roadmap.
