---
name: prp-workflow
description: |
  Product Requirements Prompt (PRP) workflow for systematic feature implementation. PRPs are PRDs engineered for AI - they include complete context, implementation blueprints, and validation gates for one-pass success.

  Use when user: (1) wants to implement a complex feature systematically, (2) asks to "create/generate a PRP", (3) mentions "PRP workflow" or "context engineering", (4) has a feature file to implement, (5) asks to "clarify" or "review" a PRP for ambiguities, (6) asks to "execute" an existing PRP, (7) asks to "verify" implementation against a PRP.

  Four modes: Generation (create PRP from requirements), Clarification (resolve ambiguities before execution), Execution (implement from PRP with validation loops), Verification (validate implementation matches PRP).
---

# PRP Workflow

Four-phase workflow: **Generation** -> **Clarification** (recommended) -> **Execution** -> **Verification**

---

## Mode 1: PRP Generation

Generate a comprehensive PRP from a feature request.

### Process

1. **Launch 2 parallel Opus agents** for research:

   **Agent #1 - Codebase Research**: Search for similar features/patterns in the codebase. Identify conventions (imports, naming, structure), test patterns, and architecture. Return a summary of patterns found and a list of 5-10 key files to read.

   **Agent #2 - External Research**: Search the web for library documentation, implementation examples, best practices, and known gotchas. Return URLs, version-specific details, and recommendations.

2. **Read key files** identified by agents to build deep understanding

3. **Clarify with user** (if needed) using AskUserQuestion for patterns to follow, integration requirements, constraints

4. **Generate PRP** using the template in [references/prp-template.md](references/prp-template.md)

5. **Save** to `plans/{XXX}-{feature-name}.md`
   - Auto-increment from highest number in `plans/`
   - Filename: lowercase, hyphens, max 50 chars

6. **Report** confidence score (1-10) and ask: clarify or execute?

---

## Mode 2: PRP Clarification

Identify and resolve underspecified areas BEFORE implementation.

### Process

1. **Locate PRP** - Ask user or search `plans/*.md`

2. **Launch an Opus agent** to analyze the PRP for ambiguities:

   The agent should analyze the PRP against the coverage taxonomy in [references/clarification-taxonomy.md](references/clarification-taxonomy.md). Mark each category (Functional Scope, Data Model, UX Flow, Non-Functional, Integration, Edge Cases, Constraints, Terminology, Completion Signals) as Clear/Partial/Missing. Return a coverage summary table and up to 5 recommended clarification questions prioritized by (Impact × Uncertainty).

3. **Present questions** to user using AskUserQuestion (max 5, up to 4 per batch):
   ```typescript
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
   - Record: `- Q: <question> → A: <answer>`
   - Update relevant PRP sections per integration table in taxonomy reference

5. **Report** coverage summary and recommend next step

### Early Exit
- No critical gaps: proceed to execution
- PRP missing: generate first (Mode 1)

---

## Mode 3: PRP Execution

Implement a feature using an existing PRP. Run directly (no sub-agent).

### Process

1. **Load PRP** - Read completely, note success criteria and validation gates

2. **Create task list** from the PRP's implementation blueprint using TodoWrite

3. **Implement** - Work through tasks systematically:
   - Keep ONE task in_progress at a time
   - Follow patterns from PRP exactly (don't introduce new patterns)
   - Run validation commands after each major step
   - Fix failures immediately (don't accumulate)

4. **Report** completion summary: files modified, validation results, any deviations from PRP

### Validation Philosophy

If validation fails:
1. Read error carefully
2. Understand root cause
3. Fix underlying issue (don't patch)
4. Re-run validation
5. Repeat until passing

---

## Mode 4: PRP Verification

Validate that implementation matches the PRP after execution completes.

### Process

1. **Locate PRP and changes** - Identify the PRP file and gather the git diff of changes made during execution

2. **Launch an Opus agent** to perform verification:

   The agent should:
   - Read the PRP completely, extracting: success criteria, implementation blueprint tasks, data models, integration points, and validation checklist
   - Run `git diff` (or `git diff <base-branch>...HEAD` if on a feature branch) to get all changes
   - For each PRP requirement, verify it has a corresponding implementation in the diff
   - For each change in the diff, verify it traces back to a PRP requirement (no undocumented additions)
   - Check that validation commands from the PRP pass
   - Return: verification matrix (requirement → implementation mapping), coverage percentage, any gaps or deviations, any extra changes not in PRP

3. **Present findings** with three categories:
   - **Implemented as specified**: Requirements fulfilled per PRP
   - **Deviations**: Implementation differs from PRP (note if intentional/improved or problematic)
   - **Gaps**: PRP requirements missing from implementation

4. **Recommend action**:
   - All green: Ready to commit/PR
   - Minor deviations: Update PRP to reflect reality or adjust implementation
   - Gaps: Return to execution mode to complete missing work

### Verification Checklist

The agent verifies against these PRP sections:
- [ ] Success criteria met
- [ ] All blueprint tasks completed
- [ ] Data models match specification
- [ ] Integration points connected correctly
- [ ] Validation loop commands pass
- [ ] No undocumented changes introduced

### Early Exit
- No PRP found: Ask user to locate or generate first
- No changes detected: Nothing to verify

---

## Quick Reference

### File Locations
- PRPs: `plans/{XXX}-{feature-name}.md`
- Template: [references/prp-template.md](references/prp-template.md)
- Taxonomy: [references/clarification-taxonomy.md](references/clarification-taxonomy.md)

### Agent Summary
| Phase | Agents | Model |
|-------|--------|-------|
| Generation | 2 parallel (codebase + external research) | Opus |
| Clarification | 1 (coverage analysis) | Opus |
| Execution | direct (no sub-agent) | — |
| Verification | 1 (plan-vs-diff analysis) | Opus |

### Key Constraints
- Clarification: max 5 questions, 4 per AskUserQuestion batch
- Execution: one task in_progress at a time
- Validate after each major step
- If CLAUDE.md exists, follow its rules

### Anti-Patterns
- Skipping research to save time
- Implementing without reading full PRP
- Ignoring validation failures
- Creating new patterns instead of following existing ones
- Skipping verification after execution
- Marking gaps as "minor" without user confirmation
