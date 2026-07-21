from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_prp import validate


def prp_text(repo: Path, *, exercise: str, task_detail: str = "Implement the behavior.") -> str:
    return f"""---
repo: {repo}
---

## Goal

Ship one bounded behavior.

## Success Criteria

- [ ] The public behavior works.

## Assurance

- **Profile**: Standard
- **Rationale**: One reversible public boundary with an established validation path.

## Consumer Contract

### Acceptance Scenarios

| ID | Given | When | Then | Exact exercise and prerequisites | Required evidence |
|---|---|---|---|---|---|
| `CX-1` | A configured client | It invokes the command | The result is visible | {exercise} | DIRECT REQUIRED |

## Execution Contract

- **Planned at commit**: `abc123`
- **Planning baseline**: clean

## Implementation Blueprint

```yaml
Task 1: Implement behavior
  MODIFY src/example.py:
    - {task_detail}
  ENABLES: CX-1
  VERIFY:
    - COMMAND: pytest tests/test_example.py
    - EXPECTED: The focused test passes.
```

## Validation

```bash
pytest tests/test_example.py
```
"""


class ValidatePrpTests(unittest.TestCase):
    def run_validation(self, text: str, workspace: Path):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.md"
            path.write_text(text)
            return validate(
                path,
                target_standard_lines=300,
                target_standard_bytes=24 * 1024,
                max_standard_lines=400,
                max_standard_bytes=32 * 1024,
                allow_legacy=False,
                workspace=workspace,
            )

    def test_accepts_matching_workspace_and_executable_evidence(self) -> None:
        workspace = Path.cwd().resolve()
        report = self.run_validation(
            prp_text(
                workspace,
                exercise="Run `pytest tests/test_example.py` from the configured workspace.",
            ),
            workspace,
        )

        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])

    def test_rejects_stale_workspace_paths(self) -> None:
        workspace = Path.cwd().resolve()
        stale = workspace.parent / "stale-checkout"
        text = prp_text(
            stale,
            exercise="Run `pytest tests/test_example.py` from the configured workspace.",
        ).replace(
            "pytest tests/test_example.py\n```",
            f"cd {stale}\npytest tests/test_example.py\n```",
        )

        report = self.run_validation(text, workspace)

        self.assertTrue(any("frontmatter repo" in error for error in report.errors))
        self.assertTrue(any("outside workspace" in error for error in report.errors))

    def test_requires_repo_frontmatter_for_workspace_validation(self) -> None:
        workspace = Path.cwd().resolve()
        text = prp_text(
            workspace,
            exercise="Run `pytest tests/test_example.py` from the configured workspace.",
        ).replace(f"repo: {workspace}\n", "")

        report = self.run_validation(text, workspace)

        self.assertTrue(any("requires `repo` frontmatter" in error for error in report.errors))

    def test_warns_about_hedged_consumer_evidence(self) -> None:
        workspace = Path.cwd().resolve()
        report = self.run_validation(
            prp_text(
                workspace,
                exercise="Run the browser fixture where practical and inspect the rendered result.",
                task_detail="Seed compatibility fixtures where practical.",
            ),
            workspace,
        )

        self.assertEqual(report.errors, [])
        self.assertTrue(any("CX-1 exact exercise" in warning for warning in report.warnings))
        self.assertTrue(any("Task 1" in warning for warning in report.warnings))


if __name__ == "__main__":
    unittest.main()
