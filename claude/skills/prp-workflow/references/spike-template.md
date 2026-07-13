# PRP Spike Workflow and Template

Use a spike to answer one material empirical question before finalizing a PRP or PRP Roadmap. A spike produces evidence and a decision; it is not partial production implementation.

## Discovery Rule

Discover spike candidates during research. Run a spike before planning finalization when its result could change architecture, scope, data model, public contracts, decomposition, task ordering, or the verification strategy.

Good triggers include uncertain runtime/library behavior, integration feasibility, concurrency or transaction semantics, migration compatibility, performance/capacity, public-boundary feasibility, error recovery, old/new client behavior, and any load-bearing claim phrased as “should,” “probably,” or “likely.”

Do not spike incomplete code search, product decisions, established repository patterns, cheap reversible implementation details, or subjective consumer preferences. A spike can establish observable behavior or setup friction, but it cannot establish desirability, comprehension, or usability without representative user evidence.

## Execution Levels

### Read-Only Experiment

Run existing commands or tests without source changes. Proceed during research when safe.

### Scratch Spike

Use an existing ignored scratch location or the OS temporary directory. A designated spike agent may write only inside its dedicated scratch directory and must not edit repository source, shared dependency state, or unrelated artifacts. Independent spikes may run in parallel only when their paths and external state are disjoint.

### In-Repository or External-State Spike

Get explicit user authorization before changing repository source, installing dependencies, using credentials or paid services, mutating data, or changing external systems. Keep the main agent as the sole source writer, run sequentially, preserve pre-existing changes, and do not create a separate worktree.

If a spike requires substantial integration code, infrastructure, representative load/data, or several experiments, create a standalone spike PRP. Its deliverable is a decision with reproducible evidence; finalize the dependent roadmap or feature PRP afterward.

## Spike Record Location

Save child or standalone PRP results under `plans/research/{NNN}-{feature}/spike-{NN}-{slug}.md`. Save roadmap-level results under `plans/research/roadmaps/{RRR}-{initiative}/spike-{NN}-{slug}.md`. Keep disposable code in scratch space and clean it after recording the result unless the user explicitly approves retaining it.

## Spike Record Template

```markdown
# Spike NN: [Question]

## Status

PROPOSED | AUTHORIZATION NEEDED | RUNNING | CONCLUSIVE | INCONCLUSIVE

## Question

[One empirical question, answerable by observation.]

## Why It Blocks Planning

[Which roadmap decomposition, architecture, scope, task, contract, or validation decision depends on it.]

## Hypotheses and Decision Rule

- If [observation], choose [decision].
- If [different observation], choose [alternative].
- If neither is observed, mark inconclusive; do not guess.

## Minimal Experiment

- Environment and exact versions:
- Setup:
- Action:
- Observation to capture:
- Safety and side-effect constraints:

## Evidence

- Commands run:
- Relevant output summary:
- Artifacts or source locations:

## Result

- Outcome: CONCLUSIVE | INCONCLUSIVE
- Observed behavior:
- Decision:
- Rejected alternatives:
- Representativeness limits:

## Planning Impact

- Roadmap or PRP sections/tasks/tests changed by this result:
- Consumer Contract, `CX-N` scenarios, or required evidence grade changed by this result:
- Remaining uncertainty:

## Cleanup

- Disposable artifacts removed:
- Repository and external state checked:
```

## Completion Gate

Finish a spike only when the question is answered conclusively or explicitly marked inconclusive, evidence is reproducible, limitations are stated, scratch artifacts are cleaned, and the result is integrated into the roadmap or PRP.

If inconclusive, narrow or redesign the experiment only when there is a clear next observation. Otherwise surface the remaining uncertainty to the user. Never silently convert an inconclusive spike into an assumption.

Keep a spike as Task 0 during implementation only when either outcome leaves the remaining PRP valid. If it selects between architectures, schemas, or public contracts, run it before PRP finalization.
