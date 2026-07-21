# PRP Template

Use this template when generating PRPs. Adapt sections to the feature — omit sections that don't apply.

## Template Map

- Goal, value, and success criteria
- Assurance profile
- Optional parent-roadmap contract
- Consumer Contract and acceptance scenarios
- Research evidence and decisions
- Execution contract and context
- Implementation blueprint and validation
- Risks, confidence, and execution notes

Do not copy this map into the generated PRP.

For Standard, normally target about 300 lines and 24 KiB. Treat 400 lines or 32 KiB as an exceptional ceiling, not a completeness gate; when approaching it, state the load-bearing reason in the Assurance rationale and consider whether the router should produce a roadmap. Define each observable promise once in `CX-N`; tasks and validation reference scenario IDs instead of repeating the behavior. Prefer compact citations over narrative repository tours.

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

## Assurance

- **Profile**: Quick / Standard / Deep
- **Rationale**: [risk and blast-radius evidence; name any Deep trigger]

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

Keep the scenario set minimal: the primary success path plus only material error, recovery, or compatibility promises. Quick PRPs normally need 1-2 scenarios.

| ID | Given | When | Then | Exact exercise and prerequisites | Required evidence |
|---|---|---|---|---|---|
| `CX-1` | [consumer-visible starting state] | [action through public boundary] | [observable result] | [browser/API/SDK/CLI procedure, environment, setup] | DIRECT REQUIRED / PROXY ACCEPTABLE — [rationale] |
| `CX-2` | [material failure or compatibility state] | [public action] | [observable error/recovery] | [procedure and setup] | [grade requirement and rationale] |

## Research Summary

### Vetted Repository Findings

List only load-bearing facts the main agent confirmed. Use compact records for Quick and Standard; add expanded evidence fields only for Deep or contested claims.

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

Required consumer evidence must be deterministic. Do not qualify a `CX-N` exercise with "where practical", "if feasible", "as available", or similar language. Name the exact exercise, an explicit conditional gate, or the prerequisite whose absence makes the scenario `UNVERIFIED`.

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
    - FAILURE-LOCAL: [For a composite gate, direct command or phase selector for each expensive phase; omit for a single-stage gate]
    - PROCESS-LIFECYCLE: [For started services/browsers, success and failure terminal signals, progress signal, and cleanup owner; omit when no process is started]

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

For a composite task or final gate, list one clean integrated command and the failure-local commands or phase selectors that avoid replaying already passing setup/build/install phases. If phase isolation is unsafe or impossible, state why and name the cheapest direct diagnosis path. Any gate that starts services or browsers must define both success and failure terminal states plus cleanup for process groups, ports, sessions, and scratch state.

## Validation

List the project's final validation commands. Task-level gates belong in the blueprint; these commands validate the integrated result:

Prefer commands relative to the current workspace. If an absolute workspace path is unavoidable, it must match the `repo` frontmatter and planning baseline exactly.

```bash
# Lint / type check
[project-specific command]

# Tests
[project-specific command]

# Integration / manual verification
[curl commands, CLI invocations, or manual steps]
```

The `CX-N` table is the authoritative consumer verification plan. Tasks reference scenario IDs, while focused tests may cover internal edge cases that support those scenarios. Internal assertions do not replace the observable `Then`. If direct evidence is unavailable, record `UNVERIFIED`; do not silently substitute an unapproved proxy.

## Unknowns & Risks

- [Specific uncertainty that could affect implementation]
- [Dependency or assumption that hasn't been verified]

Do not leave a high-impact empirical assumption unresolved unless the user explicitly accepted it. Record the acceptance and add a safe conditional gate under Pause and Reassess If.

**Confidence: [1-10]** for one-pass implementation success.

## Execution Notes

Omit this section during generation. Add it during execution only when at least one subsection has content.

### Scope Expansions

- [Added file/system] — [why it was necessary and why it remains within intent]

### Deviations

- [Difference from the blueprint] — [reason, impact, and validation]

### Unresolved Risks

- [Remaining risk or follow-up]

## Verification Record

Omit this section until Mode 4. Verification agents remain read-only; the main agent appends final reproduced evidence.

### Consumer Acceptance

| Scenario | Grade | Evidence | Limitations |
|---|---|---|---|
| `CX-1` | DIRECTLY VERIFIED / PROXY VERIFIED / FAILED / UNVERIFIED | [command, observation, screenshot, response, or artifact] | [what the evidence cannot prove, or `None`] |

### Compliance and Engineering Review

- **PRP compliance**: [requirements, gaps, and deviations]
- **Engineering review**: [correctness, regression, security, and maintainability result]
- **Final validation**: [commands and observed outcomes]
