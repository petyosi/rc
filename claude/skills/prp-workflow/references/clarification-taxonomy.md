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

### 3. Consumer Experience and Public Contract
- Consumers, supported entry points, and prerequisites
- Primary journeys and observable success
- Error, empty, loading, retry, cancellation, and recovery behavior where applicable
- Input validation and public error contracts
- Compatibility, versioning, discoverability, documentation, and examples
- Outside-in evidence surface for each `CX-N` scenario; proxy limitations when direct evidence is impractical
- Subjective usability claims backed by actual user evidence rather than inferred from code

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

### 8. Empirical Evidence
- Load-bearing assumptions that require observation rather than discussion
- Spike result, decision rule, and representativeness limits
- Inconclusive experiments or explicitly accepted empirical risk

### 9. Roadmap Alignment (child PRPs only)
- Parent step outcome and exclusion boundary
- Satisfied dependency evidence
- Inherited decisions and invariants
- Contract or capability produced for downstream steps

## Prioritization

Generate questions using **(Impact x Uncertainty)** heuristic:
- Highest-impact categories first
- Favor questions that reduce rework risk
- Exclude already-answered questions

## Question Constraints

- Group up to 3 independent high-impact questions in one turn
- Ask one at a time when answers are coupled or change subsequent questions
- Defer reversible implementation details to execution
- Prefer structured options when choices are discrete
- Only ask if the answer materially impacts architecture, data modeling, public behavior, consumer experience, or test design

## PRP Integration Table

After each answer, update the appropriate PRP section:

| Answer Type | Target PRP Section | Action |
|---|---|---|
| Functional scope | Success Criteria / Execution Contract | Add/update capability and explicit exclusions |
| Consumer experience or public contract | Consumer Contract / Success Criteria / Validation | Add or revise consumer, boundary, observable promise, `CX-N` scenarios, and evidence surface |
| Data model | Data Models | Add fields, types, relationships |
| Edge case | Gotchas | Add scenario |
| Non-functional | Success Criteria / Gotchas | Add measurable target |
| Integration | Integration Points / Context / Expected Changes | Add service details, failure modes, and affected systems |
| Constraints | Execution Contract / Unknowns & Risks | Add boundaries, scope-expansion rules, and pause conditions |
| Empirical evidence | Research Summary / Blueprint / Validation | Add spike result, decision, limitations, and derived task gates |
| Roadmap alignment | Roadmap Context / Execution Contract / Validation | Add parent linkage, dependencies, invariants, produced contracts, and independent validation boundary |

## Coverage Summary Template

| Category | Status | Notes |
|---|---|---|
| Functional Scope | Clear/Partial/Missing | |
| Data Model | ... | |
| Consumer Experience and Public Contract | ... | |
| Non-Functional | ... | |
| Integration | ... | |
| Edge Cases | ... | |
| Constraints | ... | |
| Empirical Evidence | ... | |
| Roadmap Alignment | ... | |

**Status values**: Clear (sufficient), Partial (some gaps), Missing (not addressed), Deferred (low impact or better resolved during execution)
