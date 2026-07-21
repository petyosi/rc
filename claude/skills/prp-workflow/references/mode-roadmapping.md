# PRP Roadmapping

Create a durable, non-executable coordination artifact whose steps become independently researched PRPs.

## Process

1. Run breadth-first reconnaissance: establish the end state, consumers, public boundaries, current journeys, subsystems, cross-cutting constraints, intent documents, validation surfaces, migration or rollout needs, and repository baseline. Discover stable boundaries; do not design every child in detail.
2. Resolve roadmap-level uncertainty that could change decomposition, architecture, ordering, schema, public contracts, or cross-step validation. Spike only objective empirical questions. Before the first durable spike record, reserve the roadmap number and slug.
3. Decompose around evidence and integration seams:
   - Prefer a walking skeleton and vertical, independently verifiable capability slices.
   - Use a foundational step only when it produces a stable contract with meaningful independent validation.
   - Separate outcomes with different prerequisites or validation boundaries; do not split mechanically by technical layer.
   - Map each completion criterion and `CX-N` scenario to one producing child and one verification checkpoint.
   - Define each step's outcome, dependencies, produced contract/evidence, consumer impact, invariants, exclusions, validation boundary, and status.
4. Apply the child readiness gate. A ready step has one coherent outcome, satisfied prerequisites, one primary produced contract/evidence result, bounded changes, and independent validation. Remaining questions must be child-local. Require deployment topology, telemetry, credentials, representative data, or numeric rollout gates only when that child's claimed validation depends on them. Otherwise mark the specific validation or rollout step `BLOCKED`, not unrelated implementation work.
5. Define integration, compatibility, and rollback checkpoints. For migrations, prove how legacy code handles data produced after the new writer starts; preserved rows alone are not rollback evidence.
6. Generate the roadmap from the template. Re-open evidence that controls decomposition, public contracts, schema, security, compatibility, or rollback. Under Standard, use one combined cold reviewer only when confidence is low or the dependency graph is nontrivial. Under Deep, use one fresh-context read-only cold reviewer only when self-review leaves a concrete high-risk question. Give it the roadmap, baseline, and focused criteria without conversation history. Reproduce confirmed findings in the main agent. Use a targeted follow-up—not a new general review—only for a specific unresolved contract, failed validation, or a revision that materially changes decomposition, public schema/API behavior, security, migration/rollback semantics, or the evidence strategy.
7. Save to `plans/roadmaps/{RRR}-{initiative-name}.md`, auto-incrementing the number. Keep the slug lowercase, hyphenated, and at most 50 characters.
8. Report decomposition rationale, consumer scenarios, ready and blocked steps, integration checkpoints, spike outcomes, assurance profile, and confidence. Offer the first ready child PRP.

## Rule

Never execute a roadmap as a PRP. Generate child PRPs just in time against the repository state produced by completed children. Execute additional children only when the user explicitly requests continuation.
