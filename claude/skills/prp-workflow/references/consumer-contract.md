# PRP Consumer Contract and Outside-In Verification

Use a Consumer Contract to pin the observable experience promised to a person, API client, SDK integrator, CLI user, operator, or downstream system. Apply it throughout research, planning, execution, and verification; do not add it only as a final checklist.

## Planning Contract

Identify the consumer, public boundary, entry point, prerequisites, current behavior, intended observable promise, failure and recovery behavior, and compatibility constraints. Derive these from user requirements, repository evidence, published contracts, and explicit clarification. Do not infer subjective preferences from code or claim usability without real user evidence.

Write acceptance scenarios as `CX-N` Given/When/Then statements:

- `Given` describes consumer-visible starting state and prerequisites.
- `When` uses the public surface rather than an internal call.
- `Then` describes an observable result, error, recovery path, or compatibility behavior.
- `Evidence surface` names how Mode 4 can exercise the behavior.
- `Required evidence` is `DIRECT REQUIRED` or `PROXY ACCEPTABLE`, with rationale for any proxy.

Do not write internal assertions such as “the service method is called” as consumer outcomes. Trace every scenario to one or more blueprint tasks and to a verification procedure. For a purely foundational child PRP, name the downstream integrator as its immediate consumer and describe the stable contract it produces; keep the end-to-end scenario in the parent roadmap.

## Evidence Grades

Do not assign a grade before Mode 4. If an existing PRP already contains a scaffolded `PENDING` record, Mode 4 must replace it. Final grades are:

- `DIRECTLY VERIFIED`: exercised through the real public boundary in a representative environment.
- `PROXY VERIFIED`: exercised through a contract, integration harness, fake, or non-representative environment that the PRP explicitly allowed. State what the proxy cannot prove.
- `FAILED`: observed behavior contradicts the Consumer Contract.
- `UNVERIFIED`: required surface, environment, data, credentials, or integration was unavailable.

Do not collapse proxy or unavailable evidence into “passed.” A PRP is all green only when every required scenario is directly verified or has an explicitly accepted proxy. Automated evidence is preferred when it faithfully crosses the public boundary; a manual journey is valid when automation is impractical and the exact observations are recorded.

Use supported local, test, or sandbox environments and disposable data where practical. Obtain explicit authorization before mutating external or production state. If the required environment cannot be used safely, grade the scenario `UNVERIFIED` and name the missing prerequisite.

## Surface-Specific Exercises

- **UI**: perform the journey in the running product, including relevant loading, empty, error, keyboard, and recovery states.
- **API**: call the published endpoint as a real client and inspect status, schema, headers, errors, and side effects.
- **SDK/library**: build a minimal scratch consumer using only documented exports and supported setup.
- **CLI**: invoke the built or installed command and inspect exit status, stdout/stderr, files, and repeat behavior.
- **Events/protocols**: exercise the documented producer/consumer contract, delivery semantics, and malformed or duplicate input behavior.
- **Compatibility/migration**: exercise relevant old/new reader and writer combinations and rollback behavior over newly created data.

## Outside-In Verification Sequence

1. Read the Consumer Contract, prerequisites, and permitted evidence surface before reading implementation details.
2. Set up a representative consumer through supported entry points.
3. Execute every `CX-N` scenario and capture commands, observations, screenshots, responses, or artifacts as appropriate.
4. Grade each scenario independently and state environment limitations.
5. Only then inspect implementation and tests to diagnose failures or map supporting evidence.

Keep this acceptance pass distinct from PRP compliance and engineering review even when one verifier performs multiple roles. Consumer verification establishes observable conformance, not subjective desirability; obtain actual user research when preference, comprehension, or usability is the claim.
