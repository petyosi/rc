# SEO Skill PRP

## Purpose

This PRP enables the AI to build a Claude Code global skill that audits local HTML files for SEO best practices. The skill will analyze HTML files in a specified directory and provide actionable feedback on technical SEO, content optimization, and accessibility.

## Clarifications

### Session 2025-12-21

- Q: Should the skill analyze a single page per invocation, or crawl multiple pages from a starting URL? → A: Analyze a directory with HTML files (local file system, not HTTP)
- Q: How should the skill handle JavaScript-rendered content (SPAs)? → A: Static HTML only
- Q: Should the skill offer to automatically fix issues it finds? → A: Report only
- Q: Should SEO thresholds adjust based on page type? → A: Fixed thresholds for all pages

## Core Principles

1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Follow all rules in CLAUDE.md (if exists)

---

## Goal

Build a global Claude Code skill named `seo` that:
- Scans a directory for HTML files
- Analyzes each file for SEO issues
- Reports findings with severity levels and actionable fixes
- Covers meta tags, structure, images, links, technical SEO, and content quality

## Why

- Developers need early SEO feedback during development, not after deployment
- Many SEO issues are easy to fix if caught early (missing meta tags, broken heading hierarchy)
- Static file analysis works with any build output (SSG, static sites, pre-rendered pages)
- A local-first approach integrates with the development workflow

## What

A Claude Code skill that when invoked:
1. Takes a directory path containing HTML files (e.g., `./dist`, `./build`, `./public`)
2. Finds all `.html` files in the directory (recursive)
3. Analyzes each file for SEO issues
4. Reports issues organized by file and category with severity ratings
5. Uses fixed thresholds (no page-type context)
6. Report only - does not auto-fix issues

### Success Criteria

- [ ] Skill is installed as a global skill in `~/.claude/skills/`
- [ ] Skill can scan a directory and find all HTML files
- [ ] Analyzes each file for SEO issues across 7 categories
- [ ] Each issue includes severity, file path, description, and fix suggestion
- [ ] Handles common errors (directory not found, no HTML files, permission errors)

## All Needed Context

### Documentation & References

```yaml
- url: https://developers.google.com/search/docs/appearance/core-web-vitals
  why: Official Core Web Vitals thresholds and definitions

- url: https://web.dev/articles/defining-core-web-vitals-thresholds
  why: LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 thresholds

- url: https://developers.google.com/search/docs/appearance/snippet
  why: Official Google guidance on meta descriptions

- file: claude/skills/code-review/SKILL.md
  why: Pattern to follow for skill structure (YAML frontmatter, sections)

- file: claude/skills/prp-workflow/SKILL.md
  why: Advanced skill pattern with multiple modes
```

### Current Codebase Tree

```
/Users/petyo/w/rc/
├── claude/
│   └── skills/
│       ├── code-review/
│       │   └── SKILL.md
│       └── prp-workflow/
│           ├── SKILL.md
│           ├── README.md
│           └── INSTALLATION.md
├── specs/
│   └── seo-skill.md (original requirements)
└── CLAUDE.md
```

### Desired Codebase Tree

```
/Users/petyo/w/rc/
├── claude/
│   └── skills/
│       ├── code-review/
│       │   └── SKILL.md
│       ├── prp-workflow/
│       │   └── ...
│       └── seo/                    # NEW
│           └── SKILL.md            # NEW - Main skill file
└── ...
```

### Known Gotchas & Library Quirks

```markdown
# CRITICAL: Use Glob tool to find HTML files: **/*.html pattern
# CRITICAL: Use Read tool to read file contents (not cat or WebFetch)
# CRITICAL: The skill runs in Claude Code context, has access to all tools
# CRITICAL: Static HTML analysis only - no JavaScript execution
# CRITICAL: Meta tag length limits are approximations (title ~60 chars, description ~160 chars)
# CRITICAL: Handle both absolute and relative directory paths
# CRITICAL: Report file paths relative to the scanned directory for readability
```

## Implementation Blueprint

### SEO Audit Categories

The skill will check the following categories:

#### 1. Meta Tags & Head Elements
| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Title tag | 30-60 chars, unique | >60 or <30 chars | Missing |
| Meta description | 120-160 chars | >160 or <120 chars | Missing |
| Viewport meta | Present | - | Missing |
| Charset | UTF-8 specified | - | Missing |
| Canonical URL | Self-referencing or correct | Different domain | Missing on important pages |
| Open Graph tags | og:title, og:description, og:image | Partial | All missing |
| Twitter Card tags | twitter:card present | - | Missing (suggestion only) |

#### 2. Heading Structure
| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| H1 count | Exactly 1 | 0 or >1 | - |
| Heading hierarchy | Sequential (H1→H2→H3) | Skips levels | H1 missing |
| H1 content | Contains keywords, <70 chars | Too long | Empty or image-only |
| Heading uniqueness | All unique | Duplicates exist | - |

#### 3. Images & Media
| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Alt text | Present, descriptive | Present but empty/generic | Missing on non-decorative images |
| Image dimensions | width/height specified | - | Layout shift risk |
| Lazy loading | loading="lazy" on below-fold | - | Suggestion only |

#### 4. Links & Navigation
| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Internal links | Descriptive anchor text | "click here" style | Broken internal links |
| External links | rel="noopener" on target="_blank" | - | Missing noopener |
| Skip navigation | Skip link present | - | Missing (accessibility) |

#### 5. Technical SEO Signals
| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Language attribute | html lang="" present | - | Missing |
| Robots meta | Appropriate directives | noindex on indexable | Conflicting directives |
| Structured data | JSON-LD present | Partial schema | Invalid JSON-LD |

#### 6. Performance Indicators (Static Analysis)
| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Inline CSS size | <14KB | 14-50KB | >50KB |
| Script placement | defer/async or bottom | Mixed | Render-blocking scripts |
| Resource hints | preconnect/prefetch used | - | Suggestion only |

#### 7. Content Quality
| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Text-to-HTML ratio | >25% | 10-25% | <10% |
| Word count | >300 words | 100-300 words | <100 words |
| Duplicate content | Unique | Similar sections | Large duplicates |

### List of Tasks

```yaml
Task 1: Create skill directory structure
  CREATE claude/skills/seo/SKILL.md:
    - Add YAML frontmatter (name, description)
    - Add "When to Use This Skill" section
  PATTERN: Follow claude/skills/code-review/SKILL.md structure

Task 2: Implement SEO Audit Categories section
  MODIFY claude/skills/seo/SKILL.md:
    - Add all 7 category descriptions
    - Define severity thresholds
    - List specific checks per category
  PATTERN: Structured like code-review's "Review Focus Areas"

Task 3: Implement Audit Process section
  MODIFY claude/skills/seo/SKILL.md:
    - Step 1: Validate URL and fetch page
    - Step 2: Parse HTML and extract elements
    - Step 3: Run category checks
    - Step 4: Generate report
  PATTERN: Follow code-review's "Review Process"

Task 4: Implement Output Format section
  MODIFY claude/skills/seo/SKILL.md:
    - Define report structure
    - Severity definitions (CRITICAL, WARNING, SUGGESTION)
    - Example outputs per category
  PATTERN: code-review's "Output Format" section

Task 5: Add Skill Invocation Examples
  MODIFY claude/skills/seo/SKILL.md:
    - List trigger phrases
    - Add usage examples
    - Add behavior rules
  PATTERN: code-review's "Skill Invocation Examples"
```

### Per Task Pseudocode

```markdown
# Task 1: Skill structure
Create SKILL.md with:
---
name: seo
description: SEO audit for local HTML files. Use when user wants to check SEO,
analyze files for search optimization, or mentions SEO review/audit. Scans a
directory for HTML files and analyzes meta tags, heading structure, images,
links, and technical SEO signals.
---

# SEO Audit Skill
[Introduction paragraph]

## When to Use This Skill
[Trigger conditions - user mentions SEO, audit, directory path]

# Task 2: Categories
## SEO Audit Categories
### 1. Meta Tags & Head Elements
[Table of checks with thresholds]
...continue for all 7 categories

# Task 3: Process
## Audit Process
### Step 1: Find HTML Files
- Validate directory path exists
- Use Glob tool with **/*.html pattern
- Handle errors (directory not found, no HTML files)

### Step 2: Analyze Each File
- Use Read tool to get file contents
- Extract <head> elements
- Extract heading hierarchy
- Extract images with src/alt
- Extract links with href/text
- Extract structured data

### Step 3: Run Checks
- For each category, evaluate against fixed thresholds
- Collect issues with severity per file

### Step 4: Generate Report
- Summary with file count and issue totals
- Group issues by file, then by category
- Format with markdown
- Include fix suggestions with file:line references

# Task 4: Output format
## Output Format
### Summary Section
- Files scanned: N
- Critical issues: N
- Warnings: N
- Suggestions: N

### Findings by File
For each file with issues:
- File path (relative)
- Issues grouped by category

### Severity Definitions
- CRITICAL: Blocks indexing or severely hurts rankings
- WARNING: Negatively impacts SEO/UX
- SUGGESTION: Optimization opportunity

# Task 5: Invocation
## Skill Invocation Examples
- "Run SEO audit on ./dist"
- "Check SEO for the build folder"
- "Analyze ./public for SEO issues"
- "SEO check my HTML files in ./out"
```

### Integration Points

```yaml
SKILL REGISTRATION:
  - File: claude/skills/seo/SKILL.md
  - Will be symlinked to: ~/.claude/skills/seo/SKILL.md
  - Pattern: Same as existing skills in claude/skills/

TOOL USAGE:
  - Glob: Find all HTML files with **/*.html pattern
  - Read: Read each HTML file contents
  - Output: Markdown report to user terminal
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# Verify markdown is valid
# Check YAML frontmatter format
cat claude/skills/seo/SKILL.md | head -20
```

### Level 2: Structure Verification

```bash
# Verify all required sections exist
grep -E "^## |^### " claude/skills/seo/SKILL.md
```

### Level 3: Manual Test

```bash
# Test the skill by:
# 1. Start a local dev server
# 2. Invoke the SEO skill in Claude Code
# 3. Verify it produces expected output
```

## Final Validation Checklist

- [ ] SKILL.md has valid YAML frontmatter (name, description)
- [ ] All 7 SEO categories documented with checks and thresholds
- [ ] Audit process is step-by-step with clear instructions
- [ ] Output format defined with examples
- [ ] Invocation examples listed
- [ ] Skill handles error cases (no server, invalid URL)
- [ ] Follows pattern of existing skills (code-review)

---

## Anti-Patterns to Avoid

- ❌ Don't claim to measure runtime metrics (LCP, CLS) - these require browser execution
- ❌ Don't analyze non-HTML files (skip .js, .css, etc.)
- ❌ Don't generate overly long reports - prioritize critical issues first
- ❌ Don't try to auto-fix issues - report only
- ❌ Don't skip error handling (missing directory, no HTML files, permission errors)
- ❌ Don't use Bash cat/grep - use Read and Glob tools

## Confidence Score

**9/10** - High confidence because:
- Clear pattern to follow (existing skills)
- Well-defined SEO requirements from research
- Simple skill (single mode, clear input/output)
- File-based analysis is straightforward with Glob/Read tools
- All key ambiguities resolved in clarification session

Potential gaps:
- May need user testing to refine severity thresholds
- Structured data (JSON-LD) validation may need refinement

## Research Sources

- [Core Web Vitals - Google Developers](https://developers.google.com/search/docs/appearance/core-web-vitals)
- [Core Web Vitals Thresholds - web.dev](https://web.dev/articles/defining-core-web-vitals-thresholds)
- [Meta Descriptions - Google](https://developers.google.com/search/docs/appearance/snippet)
- [Technical SEO Checklist - Backlinko](https://backlinko.com/seo-site-audit)
- [Headings for SEO - Yoast](https://yoast.com/how-to-use-headings-on-your-site/)
- [Alt Text Optimization - Yoast](https://yoast.com/image-seo-alt-tag-and-title-tag-optimization/)
