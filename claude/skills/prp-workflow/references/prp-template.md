# PRP Template

Use this template when generating PRPs. Adapt sections to the feature — omit sections that don't apply.

## Template Map

- Goal, value, and success criteria
- Optional parent-roadmap contract
- Consumer Contract and acceptance scenarios
- Research evidence and decisions
- Execution contract and context
- Implementation blueprint and validation
- Risks, confidence, and execution notes

Do not copy this map into the generated PRP.

---

## Goal

[What needs to be built — specific end state]

## Why

- [Business value / user impact]
- [Problems this solves and for whom]

## Success Criteria

- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Specific measurable outcome 3]

## Roadmap Context

Include only when this is a child PRP.

- **Parent roadmap**: `plans/roadmaps/{RRR}-{initiative}.md`
- **Roadmap step**: `R[NN]` — [step outcome]
- **Satisfied dependencies**: [step/evidence or produced contract]
- **Inherited decisions and invariants**: [constraints this PRP must preserve]
- **Contract produced for later steps**: [capability, interface, schema state, or evidence]

## Consumer Contract

Read [consumer-contract.md](consumer-contract.md) before completing this section. Use “consumer” for a person, API client, SDK integrator, CLI user, operator, or downstream system. For a foundational child with no direct end-user behavior, treat the downstream integrator as the immediate consumer and keep the end-to-end scenario in the parent roadmap.

### Consumer and Public Boundary

- **Consumer(s)**: [who or what uses the capability]
- **Public or supported boundary**: [screen, endpoint, exported API, command, event, file, or stable internal contract]
- **Entry point and prerequisites**: [how the consumer starts, authentication, setup, configuration, or prior state]
- **Current observable behavior**: [vetted baseline, or `New capability`]
- **Observable promise**: [what becomes possible or changes from the consumer's perspective]
- **Must remain compatible with**: [clients, versions, workflows, schemas, or `None`]
- **Not claimed**: [subjective usability or adjacent experience not established by this PRP]

### Acceptance Scenarios

Write observable Given/When/Then outcomes; do not use internal calls or implementation state as the `Then`. Include success plus material error, recovery, retry, cancellation, or compatibility behavior.

| ID | Given | When | Then | Evidence surface | Required evidence |
|---|---|---|---|---|---|
| `CX-1` | [consumer-visible starting state] | [action through public boundary] | [observable result] | [browser/API/SDK/CLI/contract exercise] | DIRECT REQUIRED / PROXY ACCEPTABLE — [rationale] |
| `CX-2` | [failure or edge state] | [public action] | [observable error and recovery] | [exercise] | [grade requirement and rationale] |

## Research Summary

### Vetted Repository Findings

List only facts the main agent confirmed. Include why each fact affects the PRP.

- `path/to/file.ts:42` — [established behavior or pattern] — **PRP impact**: [scope/task/test/constraint]

### External Constraints

Use only when external research applies. Include exact installed version and primary source.

- `[library] [version]` — [applicable API/constraint] — [official documentation URL]

### Settled Decisions and Rejected Alternatives

- **Decision**: [chosen or pre-existing direction] — **Evidence/rationale**: [ADR, code pattern, user decision, or spike]
- **Rejected**: [alternative] — **Reason**: [why it should not be reopened during execution]

### Spike Evidence

- [Spike record path, or `None needed`] — **Question**: [empirical unknown] — **Result/decision**: [outcome] — **Limits**: [what the spike did not establish]

### Validation Baseline

| Command | Status | Observed or expected result |
|---|---|---|
| `[project command]` | Verified / Baseline failing / Discovered but not run / Unavailable | [actual result or reason not run] |

### Research Coverage

- **Depth**: Quick / Standard / Deep
- **Inspected**: [packages, flows, tests, docs]
- **Not inspected**: [areas and why they are outside the research scope]
- **Research confidence**: [HIGH/MED/LOW with concise rationale]

## Execution Contract

- **Planned at commit**: `[git rev-parse --short HEAD]`
- **Planning baseline**: [clean, or list pre-existing changed paths that must be preserved]

### Expected Changes

List the files and systems expected to change. This is a forecast, not a brittle allowlist.

- `path/to/file.ts` — [expected change]
- `path/to/test.ts` — [expected test change]

### Explicitly Out of Scope

- [Adjacent behavior, subsystem, migration, or refactor that must not be included]
- [Public API/schema behavior that must remain unchanged]

### Scope Expansion Rule

Additional files may be changed when necessary to satisfy the PRP without changing its intent or architecture. Record each added file and rationale in Execution Notes. Pause for user direction if expansion materially changes product behavior, architecture, a public API/schema, security posture, migration risk, or agreed scope.

### Pause and Reassess If

Write feature-specific conditions, not generic retry limits. Examples:

- [A critical security, authorization, or data-loss assumption is false]
- [The change requires an unspecified public API or schema change]
- [Implementation would overwrite pre-existing user changes]
- [Validation requires a substantially broader refactor than planned]

## Context

### Key Files

List files relevant to this feature, with WHY each matters:

- `path/to/file.ts` — pattern to follow for X
- `path/to/other.ts` — integration point, will need modification
- `path/to/test.ts` — test pattern to follow

### External References

- [Library docs URL] — specific section/API needed
- [Example/guide URL] — relevant technique

### Gotchas

- [Library/framework] requires [specific setup] — without this, [consequence]
- [API/service] has [constraint] that affects [aspect of implementation]
- [Common pitfall] — do [correct approach] instead

## Implementation Blueprint

### Data Models

[Define core data structures if the feature introduces new ones. Skip if not applicable.]

### Tasks

```yaml
Task 1: [Task Name]
  MODIFY/CREATE [file path]:
    - [Specific action 1]
    - [Specific action 2]
  PATTERN: [Reference to similar code, e.g. path/to/file.ts:42]
  ENABLES: [CX-1, CX-2, or "Downstream contract only"]
  VERIFY:
    - COMMAND: [Focused validation command]
    - EXPECTED: [Concrete success result, including relevant test count/output when useful]

Task 2: [Task Name]
  ...
```

### Integration Points

[Where this feature connects to existing systems. Include file paths and the pattern to follow.]

```yaml
DATABASE:
  - [migration/schema changes]

CONFIG:
  - [config file path] — [what to add]

ROUTES/ENDPOINTS:
  - [router file] — [registration pattern]
```

## Validation

List the project's final validation commands. Task-level gates belong in the blueprint; these commands validate the integrated result:

```bash
# Lint / type check
[project-specific command]

# Tests
[project-specific command]

# Integration / manual verification
[curl commands, CLI invocations, or manual steps]
```

### Required Test Coverage

- [ ] [Happy path scenario]
- [ ] [Key edge case]
- [ ] [Error handling scenario]

### Consumer Verification Plan

Exercise every acceptance scenario outside-in. Internal assertions may support diagnosis but do not satisfy a consumer outcome.

| Scenario | Exercise | Expected observable evidence | Environment and prerequisites |
|---|---|---|---|
| `CX-1` | [exact public-boundary procedure] | [response, rendered state, output, side effect, or artifact] | [runtime, data, credentials, versions] |

If direct evidence is unavailable during verification, record `UNVERIFIED`; do not silently substitute a proxy that the Consumer Contract did not permit.

## Unknowns & Risks

- [Specific uncertainty that could affect implementation]
- [Dependency or assumption that hasn't been verified]

Do not leave a high-impact empirical assumption unresolved unless the user explicitly accepted it. Record the acceptance and add a safe conditional gate under Pause and Reassess If.

**Confidence: [1-10]** for one-pass implementation success.

## Execution Notes

Fill this section during execution. At generation, initialize each subsection with `- None yet.` and replace it when there is something to record.

### Scope Expansions

- [Added file/system] — [why it was necessary and why it remains within intent]

### Deviations

- [Difference from the blueprint] — [reason, impact, and validation]

### Unresolved Risks

- [Remaining risk or follow-up]

## Verification Record

Fill this section in Mode 4. Verification agents remain read-only; the main agent records final reproduced evidence.

### Consumer Acceptance

| Scenario | Grade | Evidence | Limitations |
|---|---|---|---|
| `CX-1` | PENDING, then DIRECTLY VERIFIED / PROXY VERIFIED / FAILED / UNVERIFIED in Mode 4 | [command, observation, screenshot, response, or artifact] | [what the evidence cannot prove, or `None`] |

### Compliance and Engineering Review

- **PRP compliance**: [requirements, gaps, and deviations]
- **Engineering review**: [correctness, regression, security, and maintainability result]
- **Final validation**: [commands and observed outcomes]
