---
name: prp-workflow
description: |
  Product Requirements Prompt (PRP) workflow for systematic implementation. Routes work among direct changes, bounded implementation-ready PRPs, and non-executable PRP Roadmaps. Uses risk-tiered research, consumer contracts, optional empirical spikes, clarification, execution, and outside-in verification. Use when the user asks to create, generate, clarify, review, execute, or verify a PRP; create or execute a PRP roadmap; decompose a large initiative; research or spike an uncertain implementation; or update a roadmap after child delivery.
---

# PRP Workflow

Route first, then read only the selected mode reference completely.

**Mode-loading gate**: Before any mode-specific reconnaissance, preflight, artifact read, edit, or verification tool call, read every reference listed for the selected mode completely. Reading this router never substitutes for reading the mode reference. When one request combines modes, such as execution plus verification, finish the first mode, then read the next mode's references before taking its first action.

## Planning Router

- **Direct change**: small, local, reversible, with an obvious implementation and validation path. Implement without a PRP.
- **PRP**: one coherent outcome, stable prerequisites, bounded expected changes, and one integrated validation loop.
- **PRP Roadmap**: dependent outcomes, material decisions, migrations, rollout stages, or validation loops that should not execute as one plan.

Use a roadmap when an earlier result determines later architecture or scope, the work cannot be validated meaningfully as one change, or safe delivery requires separate migration, compatibility, rollout, or cleanup stages. Reapply the router after reconnaissance; do not use file count alone.

## Assurance Profile

Choose once after initial reconnaissance and record it in the PRP or roadmap. Escalate whenever new evidence crosses a trigger.

| Profile | Use when | Research and review budget |
|---|---|---|
| **Quick** | Local, reversible, one boundary, established pattern, high confidence | Main-agent research; no cold review; 1-2 essential `CX-N` scenarios |
| **Standard** (default) | Bounded feature with ordinary integration risk | One combined research lane when useful; one bounded contract audit only when triggered; one combined postimplementation verifier; focused milestone validation |
| **Deep** | A Deep condition below is evidenced | Specialized research lanes; full evidence records; independent verification roles; one conditional cold review |

Use Deep only when at least one condition is evidenced:

- An irreversible or hard-to-rehearse migration, rollback, destructive operation, or mixed-version compatibility boundary
- A material authentication, authorization, privacy, or security-boundary change with high impact if wrong
- Two or more coupled high-risk domains—such as persistence, concurrency, delivery, transactions, deployment, or public compatibility—whose interaction cannot be isolated by Standard research and validation
- Multiple independently affected public consumers with incompatible failure modes or separate validation environments
- An unresolved load-bearing, high-impact uncertainty remains after Standard reconnaissance, or a spike can materially change architecture, decomposition, public contracts, or rollback
- The user explicitly requests maximum assurance

Keep Standard when a risky concern is bounded behind an established pattern, reversible gate, focused test, or single public boundary. Do not escalate for a risk keyword, file count, unfamiliarity alone, cross-package edits with one contract, or reversible implementation details. Record the evidence for each Deep condition; if none applies, remain Standard. A user may explicitly accept a named risk and a safe conditional gate instead.

## Shared Invariants

- Work in the current workspace; do not create a separate worktree.
- Preserve pre-existing user changes. Keep exactly one repository source-code writer active. The main agent writes by default; a fresh-context execution worker may take over only through the sequential milestone handoff in `mode-execution.md`. Delegated research and review remain read-only. A spike may write only to isolated scratch space under the spike rules.
- Give delegated agents compact, self-contained task context. When the host exposes history-fork controls, use no history or the smallest useful window; never fork the full conversation by default. Reviewers receive the artifact, baseline, and review question—not the drafting transcript or intended answer.
- Treat a consumer as a person, API client, SDK integrator, CLI user, operator, or downstream system using a supported boundary.
- Keep `CX-N` scenarios as the single source of truth for observable promises. Reference their IDs from tasks and verification; do not restate them.
- Keep planning cold review, execution self-review, and postimplementation verification distinct. Verification mode exclusively owns the final Verification Record and `VERIFIED` state. A planning review never substitutes for verification of the resulting implementation; Standard and Deep verification require a fresh-context read-only verifier.
- Resolve or explicitly accept high-impact uncertainty before calling a PRP implementation-ready.
- Pause when scope expansion changes product behavior, architecture, a public API/schema, security posture, migration risk, or agreed scope.

## Modes

- **Roadmapping**: read [references/mode-roadmapping.md](references/mode-roadmapping.md), [references/roadmap-template.md](references/roadmap-template.md), [references/research-workflow.md](references/research-workflow.md), and [references/consumer-contract.md](references/consumer-contract.md).
- **Generation**: read [references/mode-generation.md](references/mode-generation.md), [references/research-workflow.md](references/research-workflow.md), [references/consumer-contract.md](references/consumer-contract.md), and [references/prp-template.md](references/prp-template.md).
- **Clarification**: read [references/mode-clarification.md](references/mode-clarification.md) and [references/clarification-taxonomy.md](references/clarification-taxonomy.md).
- **Execution**: read [references/mode-execution.md](references/mode-execution.md) and the PRP before preflight. For a child PRP, also read its parent roadmap.
- **Verification**: read [references/mode-verification.md](references/mode-verification.md), [references/consumer-contract.md](references/consumer-contract.md), and the PRP.
- **Spike**: additionally read [references/spike-template.md](references/spike-template.md) only when a material empirical uncertainty appears.

## File Locations

- Roadmaps: `plans/roadmaps/{RRR}-{initiative-name}.md`
- PRPs: `plans/{XXX}-{feature-name}.md`
- PRP research: `plans/research/{XXX}-{feature-name}/spike-{NN}-{slug}.md`
- Roadmap research: `plans/research/roadmaps/{RRR}-{initiative-name}/spike-{NN}-{slug}.md`
