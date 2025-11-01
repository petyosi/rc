name: "Base PRP Template v3 - Language-Agnostic Context-Rich with Validation Loops"
description: |

## Purpose

Template optimized for AI agents to implement features with sufficient context and self-validation capabilities to achieve working code through iterative refinement. Works across languages by detecting project context.

## Core Principles

1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Project Awareness**: Detect language, package manager, and tooling from project files
6. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## How to Detect Project Context

**CRITICAL: Always detect these from project files - NEVER hardcode:**

### Language Detection

- **TypeScript**: Check for `tsconfig.json` or `package.json` with TypeScript deps
- **Python**: Check for `pyproject.toml`, `setup.py`, or `requirements.txt`
- **Go**: Check for `go.mod`
- **Rust**: Check for `Cargo.toml`

### Package Manager Detection

**TypeScript/JavaScript:**

- `pnpm-lock.yaml` → pnpm
- `yarn.lock` → yarn
- `bun.lockb` → bun
- `package-lock.json` → npm
- No lock file → npm (default)

**Python:**

- `uv.lock` → uv
- `poetry.lock` → poetry
- `Pipfile.lock` → pipenv
- `requirements.txt` only → pip

### Script Detection

1. Read `package.json` → `scripts` section for TypeScript/JavaScript
2. Read `pyproject.toml` → `[tool.hatch.envs.default.scripts]` or `[tool.poe.tasks]` for Python
3. If no scripts defined, use direct tool commands

### Example Detection Process

```bash
# 1. Check for package.json
# 2. Identify lock file (pnpm-lock.yaml → pnpm)
# 3. Read scripts from package.json:
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --fix",
    "typecheck": "tsc --noEmit",
    "test": "vitest"
  }
}
# 4. Use in PRP: "pnpm run lint", "pnpm run typecheck", etc.
```

---

## Goal

[What needs to be built - be specific about the end state and desires]

## Why

- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What

[User-visible behavior and technical requirements]

### Success Criteria

- [ ] [Specific measurable outcomes]

## All Needed Context

### Documentation & References (list all context needed to implement the feature)

```yaml
# MUST READ - Include these in your context window
- url: [Official API docs URL]
  why: [Specific sections/methods you'll need]

- file: [path/to/example.py]
  why: [Pattern to follow, gotchas to avoid]

- doc: [Library documentation URL]
  section: [Specific section about common pitfalls]
  critical: [Key insight that prevents common errors]

- docfile: [PRPs/ai_docs/file.md]
  why: [docs that the user has pasted in to the project]
```

### Project Context & Tooling

```yaml
# Detected from project files - DO NOT HARDCODE
Language: [TypeScript/Python/Go/Rust/etc. - detect from package.json, pyproject.toml, go.mod, etc.]
Package Manager: [npm/pnpm/yarn/bun/uv/pip/poetry - detect from lock files]
Test Runner: [jest/vitest/pytest/go test - detect from package.json scripts or config files]
Linter: [eslint/biome/ruff/pylint - detect from config files]
Type Checker: [tsc/mypy/pyright - detect from config files]
Build Tool: [vite/webpack/tsc/go build - detect from config]

# Package Manager Scripts (read from package.json or pyproject.toml)
Available Scripts:
  - test: [exact command from package.json scripts.test]
  - lint: [exact command from package.json scripts.lint]
  - typecheck: [exact command from package.json scripts.typecheck]
  - build: [exact command from package.json scripts.build]
  - dev: [exact command from package.json scripts.dev]

# If Python project (pyproject.toml exists)
Python Scripts:
  - test: [command from pyproject.toml tool.pytest or tool.hatch.envs]
  - lint: [command from pyproject.toml tool.ruff or scripts]
  - typecheck: [command from pyproject.toml tool.mypy or scripts]

# Example commands will use the detected package manager
Example: {package_manager} run test
Example: {package_manager} run lint
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase

```bash

```

### Desired Codebase tree with files to be added and responsibility of file

```bash

```

### Known Gotchas of our codebase & Library Quirks

```
# CRITICAL: [Library name] requires [specific setup]
# Example: React 18+ requires new JSX transform
# Example: FastAPI requires async functions for endpoints
# Example: This ORM doesn't support batch inserts over 1000 records
# Example: We use TypeScript strict mode
# Example: We use Python 3.11+ features (match/case)
```

## Implementation Blueprint

### Data models and structure

Create the core data models to ensure type safety and consistency.

```typescript
// TypeScript Example:
// - Type definitions (types.ts)
// - Interface definitions
// - Zod schemas for validation
// - Database models (Prisma/TypeORM/Drizzle)

// Python Example:
// - ORM models (SQLAlchemy/Django)
// - Pydantic models
// - Pydantic schemas
// - Pydantic validators

// Go Example:
// - Struct definitions
// - Interface definitions
// - Validation tags

// Rust Example:
// - Struct definitions with derives
// - Enum types
// - Trait implementations
```

### list of tasks to be completed to fullfill the PRP in the order they should be completed

```yaml
Task 1:
MODIFY src/existing_module.py:
  - FIND pattern: "class OldImplementation"
  - INJECT after line containing "def __init__"
  - PRESERVE existing method signatures

CREATE src/new_feature.py:
  - MIRROR pattern from: src/similar_feature.py
  - MODIFY class name and core logic
  - KEEP error handling pattern identical

...(...)

Task N:
...

```

### Per task pseudocode as needed added to each task

Use language-appropriate pseudocode based on detected project language:

```typescript
// TypeScript Example (Task 1)
// Pseudocode with CRITICAL details - don't write entire code
async function newFeature(param: string): Promise<Result> {
  // PATTERN: Always validate input first (see src/validators.ts)
  const validated = validateInput(param); // throws ValidationError

  // GOTCHA: This library requires connection pooling
  await using conn = await getConnection(); // see src/db/pool.ts

  // PATTERN: Use existing retry wrapper
  const result = await retry(
    async () => {
      // CRITICAL: API returns 429 if >10 req/sec
      await rateLimiter.acquire();
      return await externalApi.call(validated);
    },
    { attempts: 3, backoff: "exponential" },
  );

  // PATTERN: Standardized response format
  return formatResponse(result); // see src/utils/responses.ts
}
```

```python
# Python Example (Task 1)
# Pseudocode with CRITICAL details - don't write entire code
async def new_feature(param: str) -> Result:
    # PATTERN: Always validate input first (see src/validators.py)
    validated = validate_input(param)  # raises ValidationError

    # GOTCHA: This library requires connection pooling
    async with get_connection() as conn:  # see src/db/pool.py
        # PATTERN: Use existing retry decorator
        @retry(attempts=3, backoff=exponential)
        async def _inner():
            # CRITICAL: API returns 429 if >10 req/sec
            await rate_limiter.acquire()
            return await external_api.call(validated)

        result = await _inner()

    # PATTERN: Standardized response format
    return format_response(result)  # see src/utils/responses.py
```

### Integration Points

Specify language-appropriate integration patterns:

```yaml
DATABASE:
  # TypeScript (Prisma)
  - migration: "Add column 'featureEnabled' to User model"
  - command: "{package_manager} prisma migrate dev --name add-feature-enabled"

  # TypeScript (Drizzle)
  - migration: "Add column using drizzle-kit"
  - command: "{package_manager} run db:generate && {package_manager} run db:migrate"

  # Python (Alembic/SQLAlchemy)
  - migration: "Add column 'feature_enabled' to users table"
  - command: "alembic revision --autogenerate -m 'add_feature_enabled'"

  # Index creation (language-agnostic SQL)
  - index: "CREATE INDEX idx_feature_lookup ON users(feature_id)"

CONFIG:
  # TypeScript
  - add to: src/config/settings.ts
  - pattern: "export const FEATURE_TIMEOUT = Number(process.env.FEATURE_TIMEOUT ?? 30)"

  # Python
  - add to: config/settings.py
  - pattern: "FEATURE_TIMEOUT = int(os.getenv('FEATURE_TIMEOUT', '30'))"

ROUTES/ENDPOINTS:
  # TypeScript (Express)
  - add to: src/routes/index.ts
  - pattern: "app.use('/feature', featureRouter)"

  # TypeScript (Fastify)
  - add to: src/routes/index.ts
  - pattern: "app.register(featureRoutes, { prefix: '/feature' })"

  # Python (FastAPI)
  - add to: src/api/routes.py
  - pattern: "router.include_router(feature_router, prefix='/feature')"
```

## Validation Loop

**CRITICAL: Use commands detected from Project Context & Tooling section above**

### Level 1: Syntax & Style

Run linting and type checking using the exact commands from package.json or pyproject.toml:

```bash
# TypeScript Projects (use detected package manager from lock files)
{package_manager} run lint           # ESLint/Biome - auto-fix what's possible
{package_manager} run typecheck      # TypeScript compiler (tsc --noEmit)

# Python Projects (detect from pyproject.toml)
{package_manager} run lint           # ruff check . --fix (if using ruff)
{package_manager} run typecheck      # mypy . (if using mypy)

# Alternative direct commands if no scripts defined:
# TypeScript: npx eslint src/ --fix && npx tsc --noEmit
# Python: ruff check . --fix && mypy .

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests

Create test files using existing project patterns. Use the testing framework available in the project, consult with CLAUDE.md for details.

```typescript
// TypeScript Example (Jest/Vitest)
// CREATE: src/__tests__/newFeature.test.ts or src/newFeature.test.ts

describe("newFeature", () => {
  it("should handle valid input successfully", async () => {
    const result = await newFeature("valid_input");
    expect(result.status).toBe("success");
  });

  it("should throw ValidationError for invalid input", async () => {
    await expect(newFeature("")).rejects.toThrow(ValidationError);
  });

  it("should handle timeouts gracefully", async () => {
    vi.spyOn(externalApi, "call").mockRejectedValue(new TimeoutError());
    const result = await newFeature("valid");
    expect(result.status).toBe("error");
    expect(result.message).toContain("timeout");
  });
});
```

```python
# Python Example (pytest)
# CREATE: tests/test_new_feature.py

def test_happy_path():
    """Basic functionality works"""
    result = new_feature("valid_input")
    assert result.status == "success"

def test_validation_error():
    """Invalid input raises ValidationError"""
    with pytest.raises(ValidationError):
        new_feature("")

def test_external_api_timeout():
    """Handles timeouts gracefully"""
    with mock.patch('external_api.call', side_effect=TimeoutError):
        result = new_feature("valid")
        assert result.status == "error"
        assert "timeout" in result.message
```

```bash
# Run using detected test command from package.json/pyproject.toml
{package_manager} run test           # Runs all tests
{package_manager} run test -- path/to/test/file  # Run specific test file

# Alternative direct commands:
# TypeScript: npx jest src/newFeature.test.ts or npx vitest run src/newFeature.test.ts
# Python: pytest tests/test_new_feature.py -v

# If failing: Read error, understand root cause, fix code, re-run (never mock to pass)
```

### Level 3: Integration Test

Use language-appropriate commands to start the service and test:

```bash
# TypeScript - Start the dev server (use detected command)
{package_manager} run dev

# Test the endpoint (same for all languages)
curl -X POST http://localhost:3000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# Expected: {"status": "success", "data": {...}}
# If error: Check browser console or terminal logs
```

```bash
# Python - Start the service (use detected command)
{package_manager} run dev  # or: uvicorn src.main:app --reload

# Test the endpoint
curl -X POST http://localhost:8000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# Expected: {"status": "success", "data": {...}}
# If error: Check logs at logs/app.log or terminal output
```

## Final validation Checklist

Use the detected commands from Project Context & Tooling section:

```bash
# Use exact commands from package.json/pyproject.toml scripts
- [ ] All tests pass: `{package_manager} run test`
- [ ] No linting errors: `{package_manager} run lint`
- [ ] No type errors: `{package_manager} run typecheck`
- [ ] Build succeeds: `{package_manager} run build` (if applicable)
- [ ] Manual test successful: [specific curl/command from Level 3]
- [ ] Error cases handled gracefully
- [ ] Logs are informative but not verbose
- [ ] Documentation updated if needed

# Examples based on detected project:
# TypeScript: npm run test && npm run lint && npm run typecheck && npm run build
# Python: uv run pytest tests/ -v && uv run ruff check . && uv run mypy .
```

---

## Anti-Patterns to Avoid

Language-agnostic:

- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"
- ❌ Don't ignore failing tests - fix them
- ❌ Don't delete failing tests without understanding why it failed
- ❌ Don't hardcode values that should be config
- ❌ Don't hardcode package manager or commands - detect from project files

TypeScript-specific:

- ❌ Don't use `any` type - use proper types or `unknown`
- ❌ Don't ignore TypeScript errors with `@ts-ignore` without good reason
- ❌ Don't mix Promise patterns (use async/await consistently)
- ❌ Don't mutate state directly in React/Vue

Python-specific:

- ❌ Don't use sync functions in async context
- ❌ Don't catch all exceptions with bare `except:` - be specific
- ❌ Don't ignore type hints in strict typing projects
