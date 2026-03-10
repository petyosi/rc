# PRP Template

Use this template when generating PRPs. Adapt sections to the feature — omit sections that don't apply.

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

List the project's validation commands to run after each major step:

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

## Unknowns & Risks

- [Specific uncertainty that could affect implementation]
- [Dependency or assumption that hasn't been verified]

**Confidence: [1-10]** for one-pass implementation success.
