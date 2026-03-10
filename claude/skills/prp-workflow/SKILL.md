---
name: prp-workflow
description: |
  Product Requirements Prompt (PRP) workflow for systematic feature implementation. PRPs are implementation-ready plans with full context, task blueprints, and validation gates.

  This skill should be used when the user wants to implement a complex feature systematically, asks to "create a PRP" or "generate a PRP", mentions "PRP workflow", asks to "clarify" or "review" a PRP for ambiguities, asks to "execute" an existing PRP, or asks to "verify" implementation against a PRP.

  Four modes: Generation (create PRP from requirements), Clarification (resolve ambiguities before execution), Execution (implement from PRP), Verification (validate implementation matches PRP).
---

# PRP Workflow

Four-phase workflow: **Generation** -> **Clarification** (recommended) -> **Execution** -> **Verification**

**Scope check**: PRPs are for features that touch 4+ files, introduce new patterns, or have non-obvious integration points. For smaller changes, skip the PRP and implement directly.

---

## Mode 1: PRP Generation

Generate a PRP from a feature request.

### Process

1. **Launch 2 parallel research agents**:

   **Agent #1 - Codebase** (`subagent_type: "Explore"`): Search for similar features, conventions, test patterns, and architecture. Read key files and return synthesized findings — patterns to follow, naming conventions, relevant abstractions, and how similar features are structured.

   **Agent #2 - External** (`subagent_type: "general-purpose"`): Use context7 MCP tools and web search for library documentation, version-specific APIs, best practices, and known gotchas. Return concrete details: correct API signatures, required config, version constraints.

2. **Clarify with user** using AskUserQuestion for any decisions that emerged from research (patterns to follow, scope boundaries, integration approach)

3. **Generate PRP** using the template in [references/prp-template.md](references/prp-template.md)

4. **Save** to `plans/{XXX}-{feature-name}.md`
   - Auto-increment from highest number in `plans/`
   - Filename: lowercase, hyphens, max 50 chars

5. **Report**: confidence score (1-10), list specific unknowns or risks, then ask user: clarify or execute?

---

## Mode 2: PRP Clarification

Identify and resolve underspecified areas before implementation. Do this in the main context (no sub-agent) — the PRP and taxonomy fit easily, and you need conversational context with the user to formulate good questions.

### Process

1. **Read PRP** and the taxonomy in [references/clarification-taxonomy.md](references/clarification-taxonomy.md)

2. **Analyze** the PRP against relevant taxonomy categories (skip categories that clearly don't apply to this feature's scale). Mark each relevant category as Clear / Partial / Missing. Prioritize gaps by (Impact x Uncertainty).

3. **Present questions** to user via AskUserQuestion (up to 4 per call):
   ```
   AskUserQuestion({
     questions: [
       {
         question: "Which authentication method should the system use?",
         header: "Auth",
         multiSelect: false,
         options: [
           { label: "OAuth 2.0 + JWT", description: "Stateless, scalable" },
           { label: "Session cookies", description: "Traditional, requires storage" }
         ]
       }
     ]
   })
   ```

4. **Integrate answers** into PRP:
   - Add `## Clarifications` section with `### Session YYYY-MM-DD`
   - Record: `- Q: <question> -> A: <answer>`
   - Update relevant PRP sections per the integration table in the taxonomy reference

5. **Report** coverage summary and recommend next step

### Early Exit
- No critical gaps: proceed to execution
- PRP missing: generate first (Mode 1)

---

## Mode 3: PRP Execution

Implement a feature from an existing PRP. Run directly (no sub-agent).

### Process

1. **Read PRP completely** — note success criteria and validation commands

2. **Create task list** from the PRP's implementation blueprint using TodoWrite

3. **Implement** — work through tasks systematically, running validation commands after each major step

4. **If the plan needs updating**: when you discover something that contradicts or isn't covered by the PRP, pause, explain the issue to the user, update the PRP, then continue

5. **Report** completion summary: files modified, validation results, any deviations from PRP

### Session Resumption

If a session ends mid-execution, the next session can resume by reading the PRP and checking TodoWrite + git status for progress.

---

## Mode 4: PRP Verification

Validate that implementation matches the PRP after execution.

### Process

1. **Locate PRP and changes** — identify the PRP file and determine the diff scope (`git diff` for uncommitted, `git diff <base-branch>...HEAD` for a feature branch)

2. **Launch a verification agent** (`subagent_type: "general-purpose"`):

   The agent should:
   - Read the PRP, extracting: success criteria, blueprint tasks, data models, integration points, and validation commands
   - Review all changes via git diff
   - For each PRP requirement, verify corresponding implementation exists
   - Flag significant changes not traceable to PRP requirements
   - Run validation commands from the PRP
   - Return: requirement-to-implementation mapping, coverage percentage, gaps, and deviations

3. **Present findings** in three categories:
   - **Implemented as specified**: requirements fulfilled per PRP
   - **Deviations**: implementation differs from PRP (note if improved or problematic)
   - **Gaps**: PRP requirements missing from implementation

4. **Recommend action**:
   - All green: ready to commit/PR
   - Minor deviations: update PRP to reflect reality, or adjust implementation
   - Gaps: return to execution mode to complete missing work

### Early Exit
- No PRP found: ask user to locate or generate first
- No changes detected: nothing to verify

---

## File Locations
- PRPs: `plans/{XXX}-{feature-name}.md`
- Template: [references/prp-template.md](references/prp-template.md)
- Taxonomy: [references/clarification-taxonomy.md](references/clarification-taxonomy.md)
