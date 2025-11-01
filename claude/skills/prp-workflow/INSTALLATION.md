# PRP Workflow Skill - Installation Complete ✓

## Installation Summary

The PRP workflow skill has been successfully installed to your global Claude profile:

```
~/.claude/skills/prp-workflow/
├── SKILL.md                      (Main skill - Claude reads this)
├── prp_template_reference.md     (PRP template structure)
├── README.md                      (Human reference documentation)
└── INSTALLATION.md                (This file)
```

## How to Use

### Automatic Activation

The skill will automatically activate when you say things like:

- "Create a PRP for building a REST API"
- "Help me implement a web scraper systematically"
- "Generate an implementation plan for user authentication"
- "Execute the PRP in PRPs/my-feature.md"
- "I want to build this feature with proper context engineering"

### Verification

Test if the skill is active by asking Claude:

```
"What skills are available?"
```

You should see `prp-workflow` listed.

### Skill Behavior

**Mode 1: PRP Generation**

- Researches your codebase for patterns
- Searches external resources (docs, examples, best practices)
- Generates comprehensive PRP document
- Scores confidence level for success
- Optionally executes the PRP immediately

**Mode 2: PRP Execution**

- Loads and analyzes the PRP
- Creates detailed implementation plan (with TodoWrite)
- Executes systematically with validation loops
- Self-corrects through testing
- Reports completion

## Key Differences from Slash Commands

### Repository Slash Commands (Manual)

- User must type: `/generate-prp INITIAL.md`
- User must type: `/execute-prp PRPs/feature.md`
- Only works in that specific repository
- Requires explicit invocation

### Global Skill (Autonomous)

- Claude decides when to activate based on your request
- Works in ANY directory/project
- Natural language triggers: "help me implement..."
- Single skill handles both generation and execution
- Available system-wide

## Project Integration

### Without CLAUDE.md

The skill works standalone with sensible defaults.

### With CLAUDE.md

If your project has a `CLAUDE.md` file, the skill will:

1. Read it at the start of the session
2. Follow project-specific rules
3. Reference it in generated PRPs
4. Ensure consistency with your conventions

### With PRPs Directory

If your project has a `PRPs/` directory:

- Generated PRPs will be saved there
- The skill will look for existing PRPs in that location

## Customization

### Adjust Activation Triggers

Edit the `description` field in `~/.claude/skills/prp-workflow/SKILL.md`:

```yaml
description: [Add more trigger words that should activate this skill]
```

### Modify PRP Template

Edit `~/.claude/skills/prp-workflow/prp_template_reference.md` to change the structure of generated PRPs.

### Add Domain-Specific References

Place additional reference files in the skill directory:

```
~/.claude/skills/prp-workflow/
├── django_patterns.md
├── react_patterns.md
└── api_design_guide.md
```

Then reference them in SKILL.md.

## Troubleshooting

### Skill Not Activating

1. Check the description field has clear trigger words
2. Try being more explicit: "Use the PRP workflow to..."
3. Ask: "What skills are available?" to verify it's loaded

### Skill Activating Too Often

1. Make the description more specific
2. Add conditions like "only for complex features"

### Want Project-Specific Version

1. Copy the skill to your project: `.claude/skills/prp-workflow/`
2. Customize the SKILL.md for that project
3. Project-level skills take precedence over global skills

## Uninstallation

To remove the skill:

```bash
rm -rf ~/.claude/skills/prp-workflow
```

## Updates

To update the skill:

1. Edit files in `~/.claude/skills/prp-workflow/`
2. Changes take effect in new Claude sessions
3. Restart Claude Code or start new conversation to reload

## Success Indicators

You'll know the skill is working when:

- Claude automatically offers to create PRPs for complex features
- Implementation follows systematic workflow with validation
- Generated PRPs include comprehensive context
- Code works on first pass with passing tests

## Support

- Skill Documentation: ~/.claude/skills/prp-workflow/README.md
- Claude Code Skills: https://docs.claude.com/en/docs/claude-code/skills.md
- Context Engineering: https://github.com/coleam00/Context-Engineering-Intro

## Next Steps

Try the skill in a new conversation:

1. Navigate to any project directory
2. Start a new Claude Code session
3. Say: "Create a PRP for building a CLI tool that processes CSV files"
4. Watch the skill activate and guide you through the workflow

Enjoy systematic, context-rich feature implementation! 🚀
