---
name: prp-workflow
description: Create, review, clarify, execute, or verify concise Product Requirements Prompts (PRPs) and staged PRP roadmaps. Use when the user explicitly asks for a PRP or roadmap, when a feature needs a durable implementation contract before coding, or when existing PRP acceptance evidence must be reviewed. Do not use for small changes with an obvious implementation and validation path.
---

# PRP Workflow

A PRP is a concise implementation contract. It records the outcome, scope, observable acceptance, implementation shape, and validation. It is not a transcript, research report, or operating manual for the coding agent.

## Route

- **Direct change**: Implement without a PRP when the change is local, reversible, and has an obvious validation path.
- **PRP**: Use for one coherent outcome that benefits from a written contract.
- **Roadmap**: Use only when the work has independently deliverable stages, ordering dependencies, or rollout boundaries. Never execute a roadmap as one change.

Follow repository naming conventions. When none exist, use `plans/<date>-<slug>.md` for a PRP and `plans/roadmaps/<date>-<slug>.md` for a roadmap.

Read [artifact-format.md](references/artifact-format.md) when creating or materially restructuring a PRP or roadmap. Existing valid artifacts do not need conversion before execution.

## Create or Review

1. Inspect the request and the relevant repository paths.
2. Resolve only decisions that affect product behavior, public contracts, architecture, scope, or validation. Ask the user only when evidence cannot settle such a decision.
3. For a bug, regression, or unexplained behavior, reproduce the symptom and establish the causal chain before planning the fix. Do not plan from the report's assumed cause, and do not present an unproven cause as an implementation task; an unresolved diagnosis is an Open Decision.
4. Use a short empirical spike only when its result can materially change the plan. Before building, record the hypothesis, the observations that would disprove it, and the verdict boundaries; do not revise them after seeing results. A disproven spike is a successful spike. Keep spike code outside the implementation diff.
5. Write the smallest artifact that makes implementation unambiguous. Cite load-bearing evidence, not the discovery trail.
6. Run the validator:

   `python3 <skill-directory>/scripts/validate_prp.py --workspace <workspace> <prp>`

A review should identify concrete contract gaps or incorrect assumptions. Do not expand a sound PRP merely to make it look more complete.

## Execute

1. Read the PRP and current repository state.
2. Confirm that its assumptions and scope still match the code. Update the PRP only when material drift changes the contract.
3. Implement normally using the repository's existing engineering instructions.
4. Run focused validation while iterating, then one appropriate integrated gate after the implementation stabilizes.
5. Exercise the `CX-N` scenarios through their stated evidence surfaces before declaring the change complete.
6. Record only material deviations, unresolved risks, and final evidence. Do not rerun planning research or add process notes that do not change the contract.

If implementation exposes a material decision that repository evidence and existing user instructions cannot resolve, ask for direction on that decision. Continue authorized work that does not depend on the answer. Destructive actions and scope expansions still require authorization.

## Verify

Verification is required when the user asks for it. Use an independent read-only verifier only when the user requests independent review or the change crosses a high-impact security, privacy, destructive migration, or compatibility boundary.

Verify in this order:

1. Assess each `CX-N` scenario through the supported consumer boundary. Reuse recorded execution evidence when it still applies to the current implementation and environment. Exercise scenarios again when evidence is missing or stale, a failure or unresolved concern warrants it, or the requested independent review requires fresh execution.
2. Check that the implementation matches the PRP scope and plan.
3. Review the diff and affected tests for engineering defects.

When reusing evidence, identify it as reused, name who produced it, and cite the supporting output or artifact in the Verification evidence entry. An independent verifier must assess that evidence's reliability and applicability rather than accept a reported pass alone. Grade the evidence by the boundary exercised, not by who ran the check; reuse alone does not make direct evidence a proxy.

Grade acceptance evidence as:

- `DIRECT`: exercised through the real supported boundary in a representative environment.
- `PROXY`: exercised through an explicitly accepted substitute; state the limitation.
- `FAILED`: observed behavior contradicts the contract.
- `UNVERIFIED`: the required surface or prerequisite was unavailable.

Append a concise Verification section only when verification was requested. Do not repeat passing suites or unaffected review passes after a targeted fix.

## Roadmaps

Keep roadmap steps outcome-oriented. Each step must name its dependencies, produced contract, and validation boundary. Generate or execute one ready child PRP at a time, then update the roadmap with the result needed by later steps.

## Invariants

- Keep one source-code writer active.
- Keep observable promises in `CX-N`; plan steps and validation reference those IDs.
- Preserve unrelated user changes.
- Do not introduce work solely to satisfy the artifact format.
- Prefer a useful incomplete artifact with an explicit open decision over invented certainty.
