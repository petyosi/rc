# PRP Clarification Taxonomy

Analyze the PRP against these categories. **Skip categories that don't apply to the feature's scope and scale.** Mark each relevant category as: **Clear** / **Partial** / **Missing**.

## Coverage Categories

### 1. Functional Scope
- Core user goals and success criteria
- Explicit out-of-scope declarations
- User roles / personas (if applicable)
- Primary workflows

### 2. Data Model
- Entities, attributes, relationships
- Identity and uniqueness rules
- Lifecycle / state transitions

### 3. UX Flow
- Critical user journeys
- Error / empty / loading states
- Input validation rules

### 4. Non-Functional (if applicable)
- Performance targets
- Security and auth requirements
- Observability needs

### 5. Integration & Dependencies
- External services/APIs and failure modes
- Third-party library constraints
- Data formats and protocols

### 6. Edge Cases
- Invalid input and missing data scenarios
- Concurrency and conflict resolution
- Degraded mode behavior

### 7. Constraints
- Technical constraints (language, hosting, compatibility)
- Tradeoffs or rejected alternatives

## Prioritization

Generate questions using **(Impact x Uncertainty)** heuristic:
- Highest-impact categories first
- Favor questions that reduce rework risk
- Exclude already-answered questions

## Question Constraints

- Maximum 8 questions total, up to 4 per AskUserQuestion call
- Prefer structured options via AskUserQuestion when choices are discrete
- Only ask if the answer materially impacts architecture, data modeling, test design, or UX

## PRP Integration Table

After each answer, update the appropriate PRP section:

| Answer Type | Target PRP Section | Action |
|---|---|---|
| Functional scope | Success Criteria | Add/update capability |
| User interaction | Tasks / Integration Points | Add workflow/constraint |
| Data model | Data Models | Add fields, types, relationships |
| Edge case | Gotchas | Add scenario |
| Non-functional | Success Criteria / Gotchas | Add measurable target |
| Integration | Integration Points / Context | Add service details, failure modes |

## Coverage Summary Template

| Category | Status | Notes |
|---|---|---|
| Functional Scope | Clear/Partial/Missing | |
| Data Model | ... | |
| UX Flow | ... | |
| Non-Functional | ... | |
| Integration | ... | |
| Edge Cases | ... | |
| Constraints | ... | |

**Status values**: Clear (sufficient), Partial (some gaps), Missing (not addressed), Deferred (low impact or better resolved during execution)
