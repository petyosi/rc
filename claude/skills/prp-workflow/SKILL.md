---
name: prp-workflow
description: |
  Product Requirements Prompt (PRP) workflow for systematic implementation. Routes work among direct changes, bounded implementation-ready PRPs, and non-executable PRP Roadmaps that decompose large initiatives or execution-heavy single features into just-in-time child PRPs. Includes evidence-first research, consumer contracts, optional empirical spikes, clarification, shared-workspace execution, and outside-in acceptance plus independent engineering verification.

  Use when the user asks to create, generate, clarify, review, execute, or verify a PRP; create or execute a PRP roadmap; break down a large or ambiguous initiative; decide whether work needs direct implementation, one PRP, or multiple PRPs; research or spike an uncertain implementation; or update a roadmap after child delivery. Modes: Roadmapping, Generation, Clarification, Execution, and Verification.
---

# PRP Workflow

Choose a route first:

- **Direct change** -> implement without a PRP
- **Bounded feature** -> **Generation** -> **Clarification** (recommended) -> **Execution** -> **Verification**
- **Large initiative or execution-heavy feature** -> **Roadmapping** -> repeat the child PRP cycle just in time

## Planning Router

Route by execution shape, not by the product label "feature" and not by file count alone:

- **Direct change**: small, local, reversible, with an obvious implementation and validation path.
- **PRP**: one coherent outcome, stable prerequisites, bounded expected changes, and one integrated validation loop.
- **PRP Roadmap**: several dependent outcomes, material decisions, migrations, rollout stages, or validation loops that should not be executed as one plan.

Use a roadmap when any hard trigger applies:

- An earlier result determines the architecture, contract, scope, or design of later work.
- The work cannot be validated meaningfully as one integrated change.
- Safe delivery requires separately controlled migration, compatibility, rollout, or cleanup stages.

Also prefer a roadmap when several softer signals combine: multiple independently risky subsystems, several public-contract or architectural decisions, tasks that are really phases, an ambiguous partial state after interruption, or research that would require designing several implementation plans at once. A single user-facing feature may still require a roadmap.

Reapply this router after reconnaissance. If a requested PRP proves too large, switch to Roadmapping instead of producing an oversized PRP.

**Execution model**: Work in the user's current workspace; do not create a separate worktree. The main agent is the sole repository source-code writer. Subagents may perform bounded read-only research and review. During planning, a designated spike agent may write only inside an isolated scratch directory under the rules in [references/spike-template.md](references/spike-template.md); it must never edit repository source or shared state. Treat “consumer” as any person, API client, SDK integrator, CLI user, operator, or downstream system using a public or supported boundary.

---

## Mode 0: PRP Roadmapping

Create a durable, non-executable coordination artifact whose steps become independently researched PRPs.

### Process

1. **Read the roadmap workflow and template completely**: [references/roadmap-template.md](references/roadmap-template.md). Read [references/research-workflow.md](references/research-workflow.md) for evidence rules, [references/consumer-contract.md](references/consumer-contract.md) for observable acceptance rules, and [references/spike-template.md](references/spike-template.md) when a material empirical uncertainty appears.

2. **Run breadth-first reconnaissance** — establish the end state, consumers, public boundaries, current journeys, relevant subsystems, cross-cutting constraints, intent documents, validation surfaces, migration or rollout needs, and repository baseline. Research enough to discover stable boundaries and dependencies; do not design every child PRP in detail.

3. **Resolve roadmap-level uncertainty** — research or spike questions whose answers could change the decomposition, architecture, ordering, schema, Consumer Contract, public contracts, or cross-step validation. Ask the user only for remaining consequential product, policy, or scope choices. Do not use a spike to invent subjective preferences or claim usability.
   - Before writing the first durable roadmap-level spike record, reserve the next roadmap number and final initiative slug so its research path and roadmap stay aligned.

4. **Decompose around evidence and integration seams**:
   - Prefer a walking skeleton and vertical, independently verifiable capability slices.
   - Use a foundational step only when it produces a stable contract and has meaningful independent validation.
   - Avoid splitting mechanically into database/backend/frontend layers when those layers cannot be validated separately.
   - Split outcomes that have different prerequisites or validation boundaries, such as historical backfill versus runtime propagation, control-plane construction versus operational rollout, or reversible expansion versus destructive contraction.
   - Map every roadmap completion criterion, `CX-N` consumer scenario, and cross-step promise to exactly one producing child and one verification checkpoint. Eliminate orphaned outcomes and duplicate ownership.
   - Define for every step: outcome, dependencies, produced contracts or evidence, consumer impact, invariants, scope boundary, validation boundary, and child PRP status.

5. **Apply the child readiness gate** — a step is ready for PRP generation only when it has one coherent outcome, satisfied prerequisites, one primary contract or evidence result, consumer impact or a named downstream contract, independent validation, and a plausible bounded change set. The claimed outcome must be testable in the repository or a named available external integration; otherwise narrow it to the testable contract or mark it `BLOCKED`. Its remaining questions must be child-local; none may change public APIs, schema shape, persistence or concurrency semantics, security boundaries, rollback guarantees, the roadmap Consumer Contract, or roadmap decomposition. Required acceptance surfaces, deployment topology, operators, telemetry, credentials, representative data, and numeric rollout gates must already be known or the step stays `BLOCKED`. Split or block steps that fail this gate.

6. **Define integration and rollback checkpoints** — specify where multiple completed children must be validated together through their public boundary, where end-to-end `CX-N` scenarios run, where rollout decisions occur, and which observations can reorder or replace later steps. For migrations or compatibility periods, prove how legacy code handles data created after the new path starts writing; preserving rows alone is not a rollback guarantee.

7. **Generate and vet the roadmap** using [references/roadmap-template.md](references/roadmap-template.md). Re-open load-bearing citations; confirm statuses against the final dependency graph; and check outcome and consumer-scenario coverage, single ownership, evidence surfaces, mixed-version readers/writers, and rollback over newly created data. Cold-review high-risk roadmaps with a fresh-context read-only agent for missing dependencies, consumer promises without verification paths, non-verifiable steps, premature detail, and child PRPs that are still too large. Wait for the review, reproduce important findings, and integrate confirmed gaps before finalizing or reporting; never finish while the reviewer is still running.

8. **Save** to `plans/roadmaps/{RRR}-{initiative-name}.md`
   - Auto-increment from the highest number in `plans/roadmaps/`
   - Filename: lowercase, hyphens, max 50 characters after the number

9. **Report** the decomposition rationale, end-to-end consumer scenarios and evidence surfaces, roadmap-level spike outcomes, ready and blocked steps, integration checkpoints, and confidence; offer to generate the first ready child PRP.

### Roadmap Rule

Never execute a roadmap as though it were a PRP. Generate child PRPs just in time against the repository state produced by completed steps. Do not fully research all children up front; later implementation details will drift.

---

## Mode 1: PRP Generation

Generate a PRP from a feature request.

### Process

1. **Read the research workflow and consumer contract completely**: [references/research-workflow.md](references/research-workflow.md) and [references/consumer-contract.md](references/consumer-contract.md). Read [references/spike-template.md](references/spike-template.md) completely when research identifies an empirical uncertainty that may require a spike. When generating a roadmap child, also read the parent roadmap and [references/roadmap-template.md](references/roadmap-template.md) completely.

2. **Run main-agent reconnaissance** — map repository instructions, stack and exact versions, structure, intent/decision docs, conventions, validation commands, recent relevant history, and working-tree state. For a roadmap child, confirm dependency evidence, inherited invariants, produced contracts, and the step's current readiness. Produce a compact recon brief for subagents.

3. **Reapply the Planning Router** — if reconnaissance reveals multiple dependent outcomes or validation loops, stop PRP generation and switch to Mode 0. For a roadmap child, split or block the step if it fails the child readiness gate.

4. **Choose research depth and launch adaptive parallel lanes**:
   - Implementation path: analogues, architecture, data flow, exact files/symbols, and canonical patterns
   - Consumer contract, blast radius, and verification: actors, public boundaries, current journeys, observable success and failure behavior, compatibility, tests, schemas, migrations, configuration, deployment, and validation baseline
   - External/version-specific research: launch only when external APIs, libraries, protocols, standards, or unstable guidance matter
   - Combine lanes for small PRPs; use up to three agents for substantial work

5. **Require structured evidence** — every agent must cite exact repository locations or primary external sources, distinguish fact from inference, state PRP impact and confidence, and list what it did not inspect. Agents remain read-only during research.

6. **Vet in the main agent** — open every load-bearing citation, confirm version applicability, resolve duplicates and by-design behavior, and run safe validation commands where practical. Record commands as verified, baseline failing, discovered but not run, or unavailable.

7. **Apply the uncertainty gate** — classify each material unknown as further research, empirical spike, user decision, reversible execution detail, or accepted risk. Use `Impact × Uncertainty` to prioritize. Escalate an unknown back to the roadmap if its answer could invalidate downstream decomposition, the Consumer Contract, or other contracts.

8. **Run conditional spikes** under the spike workflow. Safe read-only or scratch spikes may run during generation. Get explicit authorization before repository-source or external-state mutation. Integrate conclusive evidence and limitations; never turn an inconclusive spike into an assumption.
   - Before writing the first durable spike record, reserve the next plan number and final feature slug so the record path and final PRP stay aligned.

9. **Clarify with the user** only for high-impact product, policy, scope, or technical decisions that code, documentation, and authorized spikes cannot resolve. Use the Mode 2 one-question flow.

10. **Capture the final planning baseline** after spike cleanup or any explicitly retained spike changes:
   - Current commit (`git rev-parse --short HEAD`)
   - Pre-existing working-tree changes (`git status --short`)
   - Note user changes that overlap expected implementation files; never assume they can be overwritten

11. **Generate the PRP** using [references/prp-template.md](references/prp-template.md). Include vetted findings, settled decisions, rejected alternatives, spike evidence and limits, a Consumer Contract with `CX-N` scenarios, validation baseline, research coverage, unresolved risks, and confidence rationale. Give each scenario an outside-in evidence surface and trace it to blueprint tasks. For a child PRP, include the parent roadmap link, step ID, satisfied dependencies, inherited invariants, and contracts it must produce.

12. **Cold-review risky drafts** — for high-risk, low-confidence, or spike-dependent PRPs, have one fresh-context read-only agent check evidence traceability, ambiguity, task/criterion and `CX-N` coverage, outside-in testability, proxy justification, and likely scope expansion. Integrate confirmed gaps.

13. **Save** to `plans/{XXX}-{feature-name}.md`
   - Auto-increment from highest number in `plans/`
   - Filename: lowercase, hyphens, max 50 chars

14. **Link a child PRP back to its roadmap** — set the step to `PRP READY`, record the PRP path and planning baseline, and preserve any newly discovered impact on later steps.

15. **Report** research depth and coverage, Consumer Contract and evidence readiness, spike outcomes, validation baseline, confidence score (1-10), and specific unknowns or risks; then ask whether to clarify or execute.

### Finalization Gate

Do not call a PRP implementation-ready while a high-impact empirical assumption remains unresolved, unless the user explicitly accepts the risk and the PRP contains a safe conditional gate. Do not leave an observable consumer promise without an acceptance scenario and achievable evidence surface. If a substantial standalone spike is required, produce that spike PRP first and make the feature PRP depend on its result.

---

## Mode 2: PRP Clarification

Identify and resolve underspecified areas before implementation. Do this in the main context (no sub-agent) — the PRP and taxonomy fit easily, and you need conversational context with the user to formulate good questions.

### Process

1. **Read PRP** and the taxonomy in [references/clarification-taxonomy.md](references/clarification-taxonomy.md)

2. **Analyze** the PRP against relevant taxonomy categories (skip categories that clearly don't apply to this feature's scale). Mark each relevant category as Clear / Partial / Missing. Prioritize gaps by (Impact x Uncertainty).

3. **Present clarification points one by one.** Do not batch multiple unrelated questions unless the user explicitly asks for a compact list. For each point:
   - Name the ambiguity and the taxonomy category it affects.
   - Explain why it matters for implementation, test design, or consumer experience.
   - Cite or summarize the current PRP text that is underspecified.
   - Give a concrete example of how different answers would change the implementation.
   - Recommend a default answer with concise rationale.
   - If the decision has discrete choices, list 2-4 options with tradeoffs and mark the recommended option first.
   - Ask exactly one direct question, then wait for the user's answer before moving to the next point.

   Example:

   ```markdown
   **Clarification 1: Host Crash Behavior**

   The PRP says the terminal host should close sessions if it crashes, but it does not decide whether the gateway should restart the host immediately or wait until the next terminal open. This affects lifecycle code and tests.

   Example: if the host crashes while a terminal is running `pnpm dev`, an immediate restart would bring the host back right away, but the old PTY is still gone either way. A lazy restart avoids restart loops and is simpler.

   Recommendation: Lazy restart. Close active sessions, fail pending opens, and start a fresh host on the next `terminal.open`.

   Choices:
   - Lazy restart (recommended): simpler, avoids restart loops, good enough for local POC.
   - Immediate restart: more available, but needs restart-loop protection.
   - Gateway restart required: simplest, but poor local UX.

   Should the PRP specify lazy restart?
   ```

   Use tool-based user input only if the current environment provides it and it supports this one-question flow. Otherwise ask in plain text.

4. **Integrate each answer before asking the next clarification** when practical:
   - Add `## Clarifications` section with `### Session YYYY-MM-DD`
   - Record: `- Q: <question> -> A: <answer>`
   - Update relevant PRP sections per the integration table in the taxonomy reference

5. **Repeat** until the high-impact gaps are resolved, then report the coverage summary and recommend the next step.

### Early Exit
- No critical gaps: proceed to execution
- PRP missing: apply the Planning Router, then generate a roadmap or PRP

---

## Mode 3: PRP Execution

Implement a feature from an existing PRP in the current workspace. The main agent is the sole source-code writer. Do not create a worktree and do not delegate edits to subagents.

If the input is a roadmap, do not execute it wholesale. Select the earliest ready, unblocked step; generate or locate its child PRP; and execute only that PRP. Continue through additional children only when the user explicitly asks to continue the roadmap.

### Process

1. **Read the PRP completely** — extract success criteria, Consumer Contract and `CX-N` scenarios, expected changes, explicit exclusions, task gates, final validation, risks, and pause conditions.

   For a child PRP, also read its parent roadmap. Confirm the step is `PRP READY` or `IN PROGRESS`, dependencies remain satisfied, and inherited contracts still match the live repository.

2. **Run execution preflight**:
   - Capture the current commit, `git status --short`, and the relevant diff before editing
   - Distinguish pre-existing user changes from implementation changes; preserve unrelated edits
   - Re-read key files and confirm referenced paths, symbols, patterns, and assumptions still match live code
   - Treat the planned commit as a drift signal, not sufficient evidence by itself when the planning baseline was dirty
   - If material drift invalidates the blueprint, update the PRP before implementing

3. **Cold-review risky PRPs when useful**: for high-risk, low-confidence, or long-lived PRPs, launch one fresh-context subagent to identify ambiguities, untestable criteria, missing tasks, and likely scope expansion. The subagent must be read-only. Integrate confirmed gaps into the PRP before editing source code. Skip this for straightforward PRPs.

4. **Create a task list** from the implementation blueprint using the available planning/task tool. For a child PRP, set its roadmap step and parent roadmap to `IN PROGRESS` / `ACTIVE` immediately before the first source edit.

5. **Implement sequentially**:
   - Work through tasks in dependency order
   - Run each task's verification command and compare the result with its stated expected outcome before continuing
   - Preserve the scenario-to-task trace and add supported public examples or documentation when the Consumer Contract requires them
   - Use subagents only for bounded, read-only investigation; the main agent applies all edits
   - Do not let source-writing agents operate concurrently in the shared workspace

6. **Control scope expansion**:
   - If an unexpected file is necessary but the feature intent and architecture remain unchanged, document why in the PRP's Execution Notes, update the expected changes, and continue
   - Pause for the user when expansion materially changes product behavior, architecture, a public API/schema, security posture, migration risk, or the agreed scope
   - Honor the PRP's feature-specific Pause and Reassess conditions; do not use arbitrary retry limits as a substitute for diagnosis

7. **Self-review before handoff**:
   - Run final validation
   - Compare the final diff with the preflight baseline and inspect every implementation hunk
   - Confirm every hunk traces to a PRP requirement or a documented deviation
   - Read new or changed tests and confirm they meaningfully assert the intended behavior
   - Confirm each `CX-N` scenario has an executable outside-in verification procedure and that internal assertions are not being used as consumer outcomes
   - Record scope expansions, deviations, and unresolved risks in Execution Notes

8. **Report** files modified, per-task and final validation results, scope expansions, deviations, and unresolved risks. Do not mark a child roadmap step `VERIFIED` until Mode 4 passes.

### Session Resumption

If a session ends mid-execution, resume by reading the PRP and its Execution Notes, checking the task tool and git status, reconstructing the preflight baseline, and verifying the last completed task gate before continuing.

---

## Mode 4: PRP Verification

Validate that implementation matches the PRP after execution.

### Process

1. **Locate the PRP and implementation changes** — identify the PRP, reconstruct the preflight baseline, and determine the diff scope (`git diff` for uncommitted work or `git diff <base-branch>...HEAD` for a feature branch). Exclude unrelated pre-existing user changes from attribution without reverting them.

2. **Stop source editing, read [references/consumer-contract.md](references/consumer-contract.md), then launch read-only verification**. Keep consumer acceptance, PRP compliance, and engineering review as distinct passes. For substantial or high-risk PRPs, use up to three parallel fresh-context agents; for smaller PRPs, one agent may cover multiple roles but must run the outside-in acceptance pass first. Verification agents must not edit source files. They may run the PRP's safe validation commands even if those commands create normal ignored test/build artifacts.

   **Agent A — consumer acceptance**:
   - Read the Consumer Contract, prerequisites, and permitted evidence surfaces before reading the implementation diff
   - Exercise every `CX-N` scenario through the supported public boundary as a representative consumer
   - Grade each scenario `DIRECTLY VERIFIED`, `PROXY VERIFIED`, `FAILED`, or `UNVERIFIED`; state evidence and environment limitations
   - Do not present proxy or unavailable evidence as a pass, and do not claim subjective usability without actual user evidence

   **Agent B — PRP compliance**:
   - Read the PRP, extracting: success criteria, blueprint tasks, data models, integration points, and validation commands
   - Map each requirement to concrete implementation and tests
   - Confirm every `CX-N` scenario traces to enabling tasks and a verification result
   - Check expected changes, explicit exclusions, scope expansions, and documented deviations
   - Run validation commands from the PRP
   - Return a requirement-to-implementation mapping, validation evidence, gaps, and deviations

   **Agent C — engineering review**:
   - Read the full implementation diff and relevant surrounding code
   - Check correctness, regressions, security, error handling, repository conventions, and maintainability
   - Inspect changed tests for meaningful assertions and missing edge cases
   - Flag unsupported claims, suspicious out-of-scope changes, and validation that was skipped or inconclusive

3. **Reproduce and resolve findings in the main agent**:
   - Verify important reviewer claims against the live diff and actual tool results
   - Fix confirmed issues in the main agent; verification agents remain read-only
   - Rerun affected task gates and final validation
   - Repeat affected outside-in scenarios and record their final evidence grades in the PRP
   - Replace every `PENDING` consumer result; no scenario may remain ungraded after Mode 4
   - Repeat review when changes are material, until criteria pass or a genuine blocker requires user input

4. **Present findings** in three categories:
   - **Implemented as specified**: requirements fulfilled per PRP
   - **Deviations**: implementation differs from PRP (note if improved or problematic)
   - **Gaps**: PRP requirements missing from implementation

   Include a `CX-N` acceptance table with its grade and evidence. Treat `FAILED` as a gap and `UNVERIFIED` as a blocker or explicitly accepted limitation, not as all green.

5. **Recommend action**:
   - All green: ready to commit/PR only when every required `CX-N` scenario is directly verified or uses an explicitly accepted proxy
   - Minor deviations: update PRP to reflect reality, or adjust implementation
   - Gaps: return to execution mode to complete missing work

6. **Update the parent roadmap after successful child verification**:
   - Set the step to `VERIFIED` and record the implementation/validation evidence
   - Capture newly settled decisions, produced contracts, and deviations
   - Reassess downstream dependencies and readiness when the implementation changed an assumed boundary
   - Identify the next ready step, but generate its PRP only just in time
   - Mark the roadmap `COMPLETE` only after all required steps, end-to-end consumer scenarios, roadmap completion criteria, and integration checkpoints pass

### Early Exit
- No PRP found: ask user to locate or generate first
- No changes detected: nothing to verify

---

## File Locations
- PRP Roadmaps: `plans/roadmaps/{RRR}-{initiative-name}.md`
- PRPs: `plans/{XXX}-{feature-name}.md`
- Spike records: `plans/research/{XXX}-{feature-name}/spike-{NN}-{slug}.md`
- Roadmap spike records: `plans/research/roadmaps/{RRR}-{initiative-name}/spike-{NN}-{slug}.md`
- Roadmap workflow and template: [references/roadmap-template.md](references/roadmap-template.md)
- Template: [references/prp-template.md](references/prp-template.md)
- Research workflow: [references/research-workflow.md](references/research-workflow.md)
- Consumer contract and outside-in verification: [references/consumer-contract.md](references/consumer-contract.md)
- Spike workflow and template: [references/spike-template.md](references/spike-template.md)
- Taxonomy: [references/clarification-taxonomy.md](references/clarification-taxonomy.md)
