---
name: prp-workflow
description: |
  Product Requirements Prompt (PRP) workflow for systematic feature implementation. PRPs are PRDs engineered for AI - they include complete context, implementation blueprints, and validation gates for one-pass success.

  Use when user: (1) wants to implement a complex feature systematically, (2) asks to "create/generate a PRP", (3) mentions "PRP workflow" or "context engineering", (4) has a feature file to implement, (5) asks to "clarify" or "review" a PRP for ambiguities, (6) asks to "execute" an existing PRP.

  Three modes: Generation (create PRP from requirements), Clarification (resolve ambiguities before execution), Execution (implement from PRP with validation loops).
---

# PRP Workflow

Three-phase workflow: **Generation** -> **Clarification** (recommended) -> **Execution**

## Mode 1: PRP Generation

Generate a comprehensive PRP from a feature request.

### Input

User provides: feature description (file or inline), examples to follow, documentation references, constraints/gotchas.

### Research Process

1. **Codebase Analysis**
   - Search for similar patterns using Grep/Glob
   - Identify files to reference (imports, structure, naming conventions)
   - Check test patterns for validation approach
   - Run `tree` to understand project structure

2. **External Research**
   - WebSearch for library docs, implementation examples, best practices
   - Include specific URLs and version-specific gotchas

3. **Clarification** - Use AskUserQuestion for:
   - Patterns to mirror
   - Integration requirements
   - Auth/config needs
   - Performance requirements

### Generate PRP

Use the template in [references/prp-template.md](references/prp-template.md).

**Save location:** `plans/{XXX}-{feature-name}.md`
- Auto-increment: find highest number in `plans/`, add 1
- Filename: lowercase, hyphens, max 50 chars (e.g., `plans/003-user-authentication.md`)

### Output

1. Announce what you're generating
2. Show research findings
3. Present PRP location
4. Score confidence (1-10)
5. Ask: clarify or execute?

---

## Mode 2: PRP Clarification

Identify and resolve underspecified areas BEFORE implementation to reduce rework risk.

### Process

1. **Locate PRP** - Ask user or search `plans/*.md`

2. **Coverage Analysis** - Analyze PRP against taxonomy in [references/clarification-taxonomy.md](references/clarification-taxonomy.md). Mark each category: Clear / Partial / Missing.

3. **Generate Questions** - Create prioritized queue (max 5 total):
   - Use (Impact × Uncertainty) heuristic
   - Each question: multiple-choice (2-4 options) or short phrase
   - Only include if materially impacts architecture, data model, tests, or UX

4. **Ask Questions** - Use AskUserQuestion tool:
   ```typescript
   AskUserQuestion({
     questions: [
       {
         question: "Which authentication method should the system use?",
         header: "Auth",  // max 12 chars
         multiSelect: false,
         options: [
           { label: "OAuth 2.0 + JWT", description: "Stateless, scalable for web/mobile" },
           { label: "Session cookies", description: "Traditional, requires session storage" },
           { label: "API keys", description: "Simple, for service-to-service only" }
         ]
       }
     ]
   })
   ```
   - Batch up to 4 questions per call
   - Max 5 questions total across all batches

5. **Integrate Answers** - After each batch:
   - Add `## Clarifications` section with `### Session YYYY-MM-DD`
   - Record: `- Q: <question> → A: <answer>`
   - Update appropriate PRP sections (see integration table in taxonomy reference)
   - Remove contradictions, don't duplicate

6. **Report** - Provide coverage summary table and recommend next step

### Early Exit Conditions

- No ambiguities: "No critical ambiguities detected" -> proceed to execution
- PRP missing: instruct to generate first (Mode 1)

---

## Mode 3: PRP Execution

Implement a feature using an existing PRP.

### Process

1. **Load PRP** - Read completely, note success criteria and validation gates

2. **Plan** - Create TodoWrite task list:
   - Break complex tasks into steps
   - Identify patterns from existing code
   - Plan validation for each component

3. **Research** (if needed) - Web searches, codebase exploration, AskUserQuestion

4. **Execute**
   - Work through tasks systematically
   - Update TodoWrite status as you progress
   - Keep exactly ONE task in_progress at a time
   - Follow patterns from PRP and existing code

5. **Validate Continuously**
   - Run validation commands after each major step
   - Fix failures immediately (don't accumulate)
   - Don't proceed if validation fails

6. **Final Validation**
   - Run complete validation suite
   - Verify all success criteria met
   - Re-read PRP to confirm everything implemented

7. **Report** - Mark tasks complete, summarize what was built, note any deviations

### Validation Philosophy

If validation fails:
1. Read error carefully
2. Understand root cause
3. Fix underlying issue (don't patch)
4. Re-run validation
5. Repeat until passing

---

## Quick Reference

### File Locations
- PRPs: `plans/{XXX}-{feature-name}.md`
- Template: [references/prp-template.md](references/prp-template.md)
- Taxonomy: [references/clarification-taxonomy.md](references/clarification-taxonomy.md)

### Key Constraints
- Clarification: max 5 questions, 4 per batch
- Always use TodoWrite during execution
- One task in_progress at a time
- Validate after each major step
- If CLAUDE.md exists, follow its rules

### Anti-Patterns
- Skipping research to save time
- Implementing without reading full PRP
- Ignoring validation failures
- Creating new patterns instead of following existing ones
- Batching validation at the end
