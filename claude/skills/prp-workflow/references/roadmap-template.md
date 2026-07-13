# PRP Roadmap Workflow and Template

Use a PRP Roadmap for work that cannot be implemented and validated reliably as one PRP. The roadmap coordinates child PRPs; it is not implementation-ready and must never be executed directly.

## Contents

1. Research and decomposition
2. Child readiness
3. Lifecycle and change control
4. Roadmap template

## 1. Research and Decomposition

Research breadth-first at roadmap time. Establish the target outcome, consumers, public boundaries, current journeys, final Consumer Contract, architectural boundaries, relevant subsystems, cross-cutting constraints, migration and rollout needs, dependency graph, and major risks. Read [consumer-contract.md](consumer-contract.md) completely. Defer exact files, symbols, and task blueprints to just-in-time child PRP research unless they are load-bearing for decomposition.

Run a roadmap-level spike before decomposition when its result could change architecture, step ordering, schema, public contracts, or the roadmap boundaries. Keep implementation-detail spikes inside the affected child PRP.

Decompose by independently verifiable outcomes and integration seams:

- Prefer a walking skeleton, then vertical capability slices, compatibility/migration, hardening, rollout, and cleanup as applicable.
- Permit a foundational child only when it produces a stable contract or evidence consumed by later children and has meaningful independent validation.
- Avoid database/backend/frontend splits when no layer is independently useful or testable.
- Make each dependency point to concrete evidence or a produced contract, not merely another step's completion.
- Assign each end-to-end `CX-N` scenario to one producing child and one integration checkpoint. A foundational child may serve a downstream integrator rather than an end user, but it must produce a stable, independently testable contract that enables a later scenario.

## 2. Child Readiness

Mark a step `READY FOR PRP` only when all conditions hold:

- It has one coherent outcome and a clear exclusion boundary.
- Its prerequisites are satisfied or explicitly part of the step.
- It produces one primary contract, capability, or evidence result; multiple independently verifiable outputs are a split signal.
- Its consumer impact is explicit: it owns bounded `CX-N` scenarios or names the downstream contract and later scenario it enables.
- Required inputs and cross-step contracts are defined.
- No other step claims ownership of the same primary result, and no completion criterion depends on an unowned implementation path.
- It can be implemented without concurrently implementing another step.
- It has an independently runnable validation strategy using repository surfaces or a named available external integration.
- Its required consumer evidence surface, environment, data, credentials, versions, and permitted proxy are known.
- No remaining question can change a public API, schema shape, persistence or concurrency semantics, security boundary, rollback guarantee, or roadmap decomposition.
- Required external inputs such as deployment topology, operators, telemetry, credentials, representative data, and numeric rollout gates are available.
- For migration or compatibility work, the rollback contract covers data created by the new path, not only migrated legacy rows.
- The expected change set appears bounded enough for one implementation cycle.

Otherwise keep it `PROPOSED` or `BLOCKED`, and name the missing evidence or dependency. If child research reveals that the step fails this gate, split it or revise the roadmap rather than expanding the PRP.

## 3. Lifecycle and Change Control

Use these statuses:

`PROPOSED` -> `BLOCKED` or `READY FOR PRP` -> `PRP READY` -> `IN PROGRESS` -> `VERIFIED`

Use `SUPERSEDED` when evidence replaces a step. Record why and what replaced it.

Generate child PRPs just in time. Each child PRP must link to its parent and inherit applicable decisions and invariants, but must research the live repository again. After verification, update the roadmap with actual evidence and reassess only the downstream steps affected by new facts.

Changing a child PRP may not silently change the roadmap outcome, Consumer Contract, `CX-N` scenario, cross-step architecture, public contract, migration posture, or another step's assumptions. Update the roadmap and obtain user direction when the change is consequential.

Treat phrases such as “locate or define,” several independently testable nouns under `Produces`, or a step spanning backfill, runtime behavior, UI, controls, and rollout as decomposition warnings. Split the step or make its missing roadmap-level input explicit. Do not finalize a roadmap while a required cold review is still running.

For compatibility periods, model old and new readers and writers in both directions. State fallback and reconciliation precedence before exposing new behavior. Do not let two children both “own” the same backfill or contract, and do not promise a runtime behavior for which no child creates the necessary write or integration path.

## 4. Roadmap Template

```markdown
# PRP Roadmap: [Initiative]

## Status

- **Roadmap status**: PLANNING | ACTIVE | BLOCKED | COMPLETE
- **Created at commit**: `[short commit]`
- **Planning baseline**: [pre-artifact state: clean or pre-existing paths to preserve; exclude this newly created roadmap]
- **Last updated**: YYYY-MM-DD

## Outcome

[The final user-visible or system end state.]

## Why

- [Value and affected users]
- [Problem this initiative resolves]

## Roadmap Completion Criteria

- [ ] [End-to-end measurable result]
- [ ] [Compatibility, migration, or rollout result]
- [ ] [Integrated validation result]

## Explicitly Out of Scope

- [Adjacent capability or refactor]

## Consumer Contract

- **Consumer(s)**: [person, API client, SDK integrator, CLI user, operator, downstream system]
- **Public or supported boundaries**: [screens, endpoints, exports, commands, events, or stable integration contracts]
- **Current journey**: [vetted baseline, or `New capability`]
- **Final observable promise**: [end-to-end capability]
- **Compatibility promise**: [clients, versions, workflows, or `None`]
- **Not claimed**: [subjective usability or adjacent experience not established by the roadmap]

### End-to-End Acceptance Scenarios

| ID | Given | When | Then | Evidence surface | Required evidence |
|---|---|---|---|---|---|
| `CX-1` | [consumer-visible start] | [action through public boundary] | [observable result] | [outside-in exercise] | DIRECT REQUIRED / PROXY ACCEPTABLE — [rationale] |

## Evidence and Decisions

### Vetted Findings

- `path/file:line` — [fact] — **Roadmap impact**: [boundary/order/contract/risk]

### Settled Decisions and Invariants

- **Decision/invariant**: [what children must preserve] — **Evidence**: [source or user decision]

### Roadmap-Level Spikes

- [Record path or `None`] — **Result**: [decision] — **Limits**: [what remains unknown]

### Compatibility and Rollback Contract

Include when migrations, staged enablement, or legacy readers/writers apply.

- **Reversible boundary**: [last state where old and new paths remain safe]
- **New data under rollback**: [how legacy code represents and serves data created by the new path]
- **Mixed-version behavior**: [old/new reader and writer combinations, fallback precedence, and reconciliation timing]
- **Destructive boundary**: [what removes easy rollback and which evidence authorizes it]

### Validation Baseline

| Surface or command | Status | Observed result |
|---|---|---|
| `[command]` | Verified / Baseline failing / Discovered but not run / Unavailable | [result] |

## Decomposition Strategy

[Why these steps are the smallest stable, independently verifiable outcomes and why they are ordered this way.]

## Dependency Map

- `R1` -> `R2`: [concrete evidence or contract R1 produces for R2]

## Outcome Coverage

Map each completion criterion, `CX-N` scenario, and cross-step contract to one owner and one checkpoint. No row may be unowned; avoid multiple producing steps for the same result.

| Required outcome, `CX-N`, or contract | Producing step | Verification checkpoint |
|---|---|---|
| [measurable roadmap result] | R[...] | [checkpoint] |

## Steps

### R1: [Outcome-oriented step name]

- **Status**: PROPOSED | BLOCKED | READY FOR PRP | PRP READY | IN PROGRESS | VERIFIED | SUPERSEDED
- **Outcome**: [one observable result]
- **Why separate**: [risk, contract, or validation boundary]
- **Depends on**: [step plus concrete evidence, or `None`]
- **Produces**: [contract, capability, migration state, or decision consumed later]
- **Consumer impact**: [`CX-N` scenarios owned, or downstream integrator and later scenario enabled]
- **External readiness inputs**: [topology, operator, telemetry, credentials, representative data, thresholds, or `None`]
- **Must preserve**: [roadmap invariants and compatibility]
- **In scope**: [bounded capability]
- **Out of scope**: [work reserved for later children]
- **Validation boundary**: [how this step can pass independently]
- **Remaining questions**: [child-local research only, or `None`; move contract/decomposition questions to roadmap decisions]
- **Child PRP**: [path, or `Not generated`]
- **Completion evidence**: [implementation and validation evidence, or `Pending`]

### R2: [Next step]

[Repeat the same fields.]

## Integration Checkpoints

### After R[...]

- **Integrated behavior to validate**: [cross-child scenario]
- **Consumer scenarios**: [`CX-N` exercised through the public boundary, or `None`]
- **Commands or observation**: [validation]
- **Evidence requirement**: [DIRECT REQUIRED or accepted proxy and limitation]
- **Decision enabled**: [rollout/reordering/next stage]

## Risks and Replanning Triggers

- [Observation that requires revising decomposition, contracts, or order]

## Progress Log

### YYYY-MM-DD

- [Status change, evidence, decision, or downstream impact]
```
