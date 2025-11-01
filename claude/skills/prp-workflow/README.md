# PRP Workflow Skill

This skill provides comprehensive Product Requirements Prompt (PRP) workflow capabilities for systematic feature implementation with proper context engineering.

## What This Skill Does

This skill combines three powerful workflows into one autonomous capability:

1. **PRP Generation**: Creates comprehensive implementation blueprints from feature requests
2. **PRP Clarification**: Identifies and resolves ambiguities through structured questioning (recommended before execution)
3. **PRP Execution**: Implements features using PRP files with validation loops

## Files in This Skill

- `SKILL.md` - Main skill definition (Claude reads this)
- `prp_template_reference.md` - Base PRP template structure
- `README.md` - This file (human reference)

## How It Works

### Automatic Activation

Claude will automatically activate this skill when you:
- Mention implementing a new feature
- Ask to create a PRP
- Want systematic development approach
- Reference feature files or requirements
- Mention context engineering or PRPs
- Ask to clarify, review, or check a PRP for ambiguities
- Request execution of an existing PRP

### Manual Testing

You can test the skill by asking:
- "What skills are available?"
- "Create a PRP for a REST API endpoint"
- "Help me implement a feature systematically"
- "Clarify the PRP in specs/001-feature.md"
- "Execute the PRP in specs/002-api.md"

## Key Principles

1. **Context is King**: PRPs include all necessary documentation, examples, and patterns
2. **Validation Loops**: Built-in tests allow AI to self-correct
3. **Pattern Following**: References existing code for consistency
4. **One-Pass Success**: Comprehensive context enables working code on first try

## Workflow Overview

This skill operates in three modes for systematic feature implementation:

### Mode 1: PRP Generation
1. Research codebase for similar patterns
2. Search external resources (docs, examples)
3. Clarify initial ambiguities with user
4. Generate comprehensive PRP document
5. Save to `specs/XXX-feature-name.md` with auto-incrementing number
6. Score confidence level (1-10)
7. Recommend clarification phase before execution

### Mode 2: PRP Clarification (Recommended Before Execution)
1. Load existing PRP from `specs/` directory
2. Perform coverage analysis using 10-category taxonomy:
   - Functional Scope & Behavior
   - Domain & Data Model
   - Interaction & UX Flow
   - Non-Functional Quality Attributes
   - Integration & External Dependencies
   - Edge Cases & Failure Handling
   - Constraints & Tradeoffs
   - Terminology & Consistency
   - Completion Signals
   - Misc / Placeholders
3. Generate prioritized question queue (max 5 questions)
4. Ask questions ONE AT A TIME with recommendations
5. Update PRP incrementally after EACH answer
6. Provide coverage summary and next step recommendation

**Purpose**: Identify and resolve underspecified areas BEFORE implementation to reduce downstream rework risk.

### Mode 3: PRP Execution
1. Load and understand complete PRP
2. ULTRATHINK - create detailed plan
3. Execute implementation systematically
4. Validate continuously (tests, linting, type checking)
5. Fix failures and iterate
6. Verify all success criteria met

## Best Practices

- **For Generation**: Be thorough in research, include specific file paths, make validation executable, score confidence honestly
- **For Clarification**: Use recommended answers based on best practices, ask only high-impact questions (max 5), update PRP after each answer, provide coverage summary at end
- **For Execution**: Read entire PRP first, use TodoWrite, follow patterns exactly, validate continuously, fix failures immediately
- **Always**: Over-context rather than under-context, show don't tell, be specific

## Recommended Workflow Sequence

1. **Generate PRP** (Mode 1) - Create comprehensive requirements with context
2. **Clarify PRP** (Mode 2) - Resolve ambiguities before implementation *(optional but recommended to reduce rework risk)*
3. **Execute PRP** (Mode 3) - Implement with validation loops

Users can skip Mode 2 for exploratory work, but should be warned about increased rework risk.

## The Clarification Phase in Detail

### Why Clarify Before Executing?

The clarification phase (Mode 2) reduces downstream rework risk by identifying and resolving ambiguities BEFORE implementation begins. This is especially valuable for:
- Complex features with multiple integration points
- Features requiring non-functional requirements (performance, security, scalability)
- Projects with multiple stakeholders or changing requirements
- When exploring new domains or technologies

### How the Questioning Works

**Interactive Loop:**
1. Claude analyzes the PRP and generates up to 5 high-impact questions
2. Questions are presented ONE AT A TIME (never all at once)
3. Each question includes a recommended answer with reasoning
4. You respond with: option letter, "yes"/"ok" to accept recommendation, or custom answer (≤5 words)
5. Claude updates the PRP immediately after each answer
6. Process continues until 5 questions answered or you signal completion

**Question Format:**

**Multiple-Choice:**
```
**Recommended:** Option B (OAuth 2.0 with JWT) - Standard, secure, scalable

| Option | Description |
|--------|-------------|
| A | Username/password with session cookies |
| B | OAuth 2.0 with JWT tokens |
| C | API key authentication |

Reply with option letter, "yes"/"recommended", or short answer.
```

**Short-Answer:**
```
**Suggested:** <200ms p95 latency - Industry standard for responsive apps

Format: Short answer (≤5 words)
Reply with "yes"/"suggested"/"ok", or your own answer.
```

### Coverage Taxonomy

Questions are generated across 10 categories to ensure comprehensive coverage:

1. **Functional Scope & Behavior** - What the system does, success criteria, out-of-scope items
2. **Domain & Data Model** - Entities, attributes, relationships, lifecycle
3. **Interaction & UX Flow** - User journeys, error states, input validation
4. **Non-Functional Quality** - Performance, scalability, reliability, security
5. **Integration & Dependencies** - External services, APIs, failure modes
6. **Edge Cases & Failures** - Error scenarios, rate limiting, conflict resolution
7. **Constraints & Tradeoffs** - Technical limits, rejected alternatives
8. **Terminology** - Canonical terms, glossary, consistency
9. **Completion Signals** - Acceptance criteria, DoD indicators
10. **Misc / Placeholders** - TODOs, vague adjectives ("fast", "robust")

### PRP Updates

After each answer, the PRP is updated incrementally:
- **Clarifications section** records all Q&A pairs
- **Relevant sections** are updated with specific details
- **Placeholders** are replaced with concrete values
- **Contradictions** are resolved
- **Changes are saved** immediately (atomic updates)

### Coverage Summary

At the end, you receive a coverage table showing:
- **Resolved** - Was unclear, now addressed
- **Clear** - Already sufficient
- **Deferred** - Exceeds 5-question limit OR better for execution phase
- **Outstanding** - Still unclear but low impact

### When to Skip Clarification

You can skip Mode 2 if:
- Doing exploratory/prototyping work
- All requirements are crystal clear
- The PRP confidence score is 9-10
- Time constraints require immediate implementation

However, be warned: skipping clarification increases rework risk, especially for production features.

## Success Metrics

A successful PRP workflow achieves:
- ✅ Working code on first execution pass
- ✅ All tests passing
- ✅ No linting or type errors
- ✅ Follows project conventions
- ✅ Meets all success criteria

## Integration with Projects

If a project has `CLAUDE.md`, the skill will:
1. Read it at session start
2. Follow all project-specific rules
3. Reference it in generated PRPs
4. Ensure alignment with project conventions

## Customization

You can customize this skill by:
1. Editing `SKILL.md` to adjust activation triggers in the description
2. Modifying `prp_template_reference.md` for different template structure
3. Adding additional reference files for specific domains

## Resources

- [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills.md)
- [Context Engineering Best Practices](https://www.philschmid.de/context-engineering)
