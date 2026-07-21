# PRP Verification

Validate observable consumer behavior, PRP compliance, and engineering quality as distinct passes with effort proportional to risk.

Verification mode exclusively owns the final Verification Record, child `VERIFIED` state, and downstream unblocking. Treat execution-authored verification claims or records as provisional evidence to reproduce, not as completed verification. A planning cold review evaluates the plan before implementation and never satisfies postimplementation verification.

Before any verification tool call, confirm that `mode-verification.md`, `consumer-contract.md`, and the PRP were read completely in the current context. This remains mandatory when verification follows execution in the same user request.

## Process

1. Locate the PRP, reconstruct its preflight baseline, and isolate the implementation diff from unrelated user changes.
2. Run `python3 <skill-directory>/scripts/validate_prp.py --allow-legacy --workspace <current-workspace> <prp-path>` from the current workspace and resolve structural or stale-workspace errors before semantic verification. The flag downgrades only pre-assurance profile and task-ownership omissions. Compactness and legacy warnings do not block verification of an already executed PRP and must never cause removal of research, decisions, risks, execution notes, or evidence.
3. Select verification shape from the recorded assurance profile:
   - Quick: the main agent performs the three passes; use a reviewer only when a concrete concern appears.
   - Standard: one fresh-context read-only verifier performs the passes sequentially and reports separate results.
   - Deep: begin with one fresh-context read-only verifier covering the three passes. Split into at most three specialists only when the PRP records genuinely independent high-risk evidence surfaces that one verifier cannot exercise faithfully.
   Give every verifier the PRP, isolated diff/baseline, validation evidence, and its review question without inherited conversation history. For Standard and Deep, the execution writer cannot serve as this verifier even if it already ran every listed gate.
   Use the host's supported collaboration/verifier mechanism. Do not shell out to a nested Codex process as an improvised substitute unless the user explicitly requested that CLI workflow. If the required fresh verifier is unavailable or authorization is denied, do not retry through another wrapper: record the independent passes and affected `CX-N` grades as `UNVERIFIED`, name the missing verifier capability, and stop without marking the PRP verified.
4. Consumer acceptance comes first. Read the Consumer Contract before the diff, exercise every `CX-N` scenario through its supported boundary, and grade it `DIRECTLY VERIFIED`, `PROXY VERIFIED`, `FAILED`, or `UNVERIFIED` with evidence and limitations.
5. PRP compliance maps success criteria and tasks to implementation and tests, checks exclusions and deviations, and reuses recorded validation results when the code and environment are unchanged.
6. Engineering review inspects the complete diff and relevant surrounding code for correctness, regression, security, error handling, conventions, maintainability, and meaningful tests.
7. The main agent reproduces important findings and fixes confirmed issues. Rerun only affected focused gates and any final suite invalidated by code or environment changes. Repeat an affected acceptance scenario after its implementation changes; do not automatically repeat unaffected review passes or launch a general second verifier. Use a targeted follow-up only for a specific unresolved finding or failed validation.
8. Append the Verification Record to the PRP only now. Assign a final grade to every `CX-N` scenario, replacing any legacy `PENDING` entries, and report implemented requirements, deviations, gaps, and an evidence table.
9. Recommend ready only when every required scenario is directly verified or uses an explicitly accepted proxy. Treat `FAILED` as a gap and `UNVERIFIED` as a blocker or named accepted limitation.
10. After successful child verification, update the parent step to `VERIFIED`, record produced contracts and evidence, reassess downstream readiness, and identify—but do not generate—the next ready child.

## Early Exit

- No PRP: locate or generate it first.
- No implementation changes: nothing to verify.
