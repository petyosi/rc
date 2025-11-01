# PRP Workflow Skill - Installation Guide

## Installation Summary

The PRP workflow skill is a **global skill** that will be available system-wide once installed to your home directory:

**Source location** (this repository):

```
<rc-repo>/claude/skills/prp-workflow/
├── SKILL.md                      (Main skill - Claude reads this)
├── prp_template_reference.md     (PRP template structure)
├── README.md                      (Feature reference documentation)
└── INSTALLATION.md                (This file)
```

**Installed location** (after symlinking):

```
~/.claude/skills/prp-workflow/
```

## What This Skill Does

This skill provides a comprehensive three-phase workflow for systematic feature implementation:

**Mode 1: PRP Generation**

- Researches your codebase for patterns and conventions
- Searches external resources (docs, examples, best practices)
- Generates comprehensive PRP document in `specs/XXX-feature-name.md`
- Scores confidence level for implementation success
- Recommends clarification before execution

**Mode 2: PRP Clarification**

- Analyzes existing PRP for ambiguities and gaps
- Uses 10-category coverage taxonomy
- Asks up to 5 high-impact questions ONE AT A TIME
- Updates PRP incrementally after each answer
- Provides coverage summary and next step recommendation

**Mode 3: PRP Execution**

- Loads and analyzes the PRP
- Creates detailed implementation plan with TodoWrite
- Executes systematically with validation loops
- Self-corrects through testing
- Reports completion status

## How to Use

This is a **global skill** - it works automatically in ANY project or directory once installed to `~/.claude/skills/prp-workflow/`.

### Automatic Activation

Claude automatically activates this skill when you say things like:

**For Generation:**

- "Create a PRP for building a REST API"
- "Help me implement user authentication systematically"
- "Generate an implementation plan for a web scraper"
- "I want to build this feature with proper context engineering"

**For Clarification:**

- "Clarify the PRP in specs/002-api.md"
- "Review specs/003-feature.md for ambiguities"
- "Check if the requirements in specs/001-auth.md are clear"
- "What's missing from specs/004-integration.md?"

**For Execution:**

- "Execute the PRP in specs/002-api.md"
- "Implement the feature described in specs/003-scraper.md"
- "Build from specs/001-auth.md"

### Verification

Test if the skill is active by asking Claude:

```
"What skills are available?"
```

You should see `prp-workflow` listed.

### Manual Invocation

If the skill doesn't activate automatically, you can invoke it explicitly:

```
"Use the prp-workflow skill to implement [feature]"
```

## Recommended Workflow

For best results, follow this sequence:

1. **Generate PRP** (Mode 1)
   - Create comprehensive requirements with full context
   - Research codebase patterns and external resources
   - Save to `specs/XXX-feature-name.md` with auto-incrementing number

2. **Clarify PRP** (Mode 2) - Optional but recommended
   - Resolve ambiguities before implementation
   - Reduces downstream rework risk
   - Skip only for exploratory/prototyping work

3. **Execute PRP** (Mode 3)
   - Implement with validation loops
   - Self-correct through testing
   - Achieve working code on first pass

## Project Integration

### specs/ Directory

PRPs are automatically saved to `specs/` directory with auto-incrementing naming:

- `specs/001-feature-name.md`
- `specs/002-another-feature.md`
- `specs/003-third-feature.md`

The skill will:

- Create the directory if it doesn't exist
- Find the next available number automatically
- Generate kebab-case filenames from feature names

### CLAUDE.md Integration

If your project has a `CLAUDE.md` file, the skill will:

1. Read it at the start of the session
2. Follow all project-specific rules
3. Reference it in generated PRPs
4. Ensure alignment with project conventions

### Project Context Detection

The skill automatically detects your project setup:

- **Language**: TypeScript, Python, Go, Rust (from config files)
- **Package Manager**: npm, pnpm, yarn, bun, uv, pip, poetry (from lock files)
- **Testing Framework**: jest, vitest, pytest (from config/scripts)
- **Linting/Type Checking**: ESLint, ruff, mypy, tsc (from config)

Commands in generated PRPs will match your detected tooling.

## Customization

### Adjust Activation Triggers

Edit the `description` field in `~/.claude/skills/prp-workflow/SKILL.md` to add more trigger words.

### Modify PRP Template

Edit `~/.claude/skills/prp-workflow/prp_template_reference.md` to customize the structure of generated PRPs.

### Add Domain-Specific References

Place additional reference files in the skill directory:

```
~/.claude/skills/prp-workflow/
├── django_patterns.md
├── react_patterns.md
└── api_design_guide.md
```

Then reference them in `SKILL.md`.

**Note**: If you modify files in the source repository, re-run your installation script to sync changes to `~/.claude/skills/`.

## Troubleshooting

### Skill Not Activating

1. Check the description field has clear trigger words
2. Try being more explicit: "Use the PRP workflow to..."
3. Ask: "What skills are available?" to verify it's loaded
4. Ensure you're in a new conversation (skills load at session start)

### Skill Activating Too Often

1. Make the description more specific in `SKILL.md`
2. Add conditions like "only for complex features"
3. Be more explicit about when NOT to use it

### PRPs Not Saving to specs/

1. Check that the `specs/` directory exists (skill creates it if missing)
2. Verify write permissions in your project directory
3. Check for file system errors in Claude's output

### Clarification Mode Not Working

1. Ensure the PRP file exists in `specs/` directory
2. Provide full path to PRP file if not in `specs/`
3. Verify PRP has valid markdown structure

## Success Indicators

You'll know the skill is working when:

- Claude automatically offers to create PRPs for complex features
- Implementation follows systematic workflow with validation
- Generated PRPs include comprehensive context with file paths
- Code works on first pass with passing tests
- Validation loops catch and fix errors automatically

## Key Differences

### Global Skills (This Skill)

- **Scope**: Works in ANY project or directory system-wide
- **Location**: `~/.claude/skills/prp-workflow/`
- **Activation**: Claude decides automatically based on natural language
- **Setup**: Install once, use everywhere
- **Triggers**: "Create a PRP...", "Clarify the requirements...", etc.

### Project-Level Skills

- **Scope**: Only works in specific project directory
- **Location**: `<project>/.claude/skills/skill-name/`
- **Activation**: Same automatic activation as global skills
- **Setup**: Configured per-project
- **Priority**: Takes precedence over global skills with same name

### Slash Commands

- **Scope**: Project-specific
- **Location**: `<project>/.claude/commands/`
- **Activation**: Manual invocation (e.g., `/generate-prp`)
- **Setup**: Must define each command separately
- **Triggers**: Explicit command syntax only

## Support Resources

- **Skill Documentation**: `~/.claude/skills/prp-workflow/README.md`
- **Template Reference**: `~/.claude/skills/prp-workflow/prp_template_reference.md`
- **Claude Code Skills**: <https://docs.claude.com/en/docs/claude-code/skills.md>
- **Context Engineering**: <https://www.philschmid.de/context-engineering>

## Updating the Skill

To update:

1. Edit files in the source repository (where you manage your dotfiles)
2. Re-run your installation/symlinking script to sync to `~/.claude/skills/`
3. Start a new Claude Code conversation to reload the skill

**Or** edit directly in `~/.claude/skills/prp-workflow/` for quick changes (will be overwritten on next sync).

## Removal

To remove the skill:

```bash
rm -rf ~/.claude/skills/prp-workflow
```

Then remove the symlink from your installation script if you want permanent removal.

## Next Steps

Try the skill now:

1. Start a new conversation with Claude Code
2. Say: "Create a PRP for building a CLI tool that processes CSV files"
3. Watch the skill activate and guide you through the workflow
4. Follow with: "Clarify the PRP in specs/001-cli-tool.md"
5. Then: "Execute the PRP in specs/001-cli-tool.md"

Enjoy systematic, context-rich feature implementation!
