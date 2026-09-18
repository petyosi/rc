from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_prp import validate


def lean_prp(repo: Path) -> str:
    return f"""---
repo: {repo}
status: planned
---

# Ship behavior

## Goal

Ship one bounded behavior.

## Scope

- In: the supported command
- Out: unrelated commands

## Acceptance

### CX-1: The result is visible

- Given: a configured client
- When: it invokes the command
- Then: the result is visible
- Evidence: run the focused test

## Plan

1. Implement the behavior in `src/example.py`.
   - Covers: `CX-1`

## Validation

- Focused: `pytest tests/test_example.py`
- Acceptance: `CX-1` through the command
"""


class ValidatePrpTests(unittest.TestCase):
    def validate_text(self, text: str, workspace: Path):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.md"
            path.write_text(text, encoding="utf-8")
            return validate(path, workspace)

    def test_accepts_lean_prp(self) -> None:
        workspace = Path.cwd().resolve()
        report = self.validate_text(lean_prp(workspace), workspace)

        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])

    def test_requires_acceptance(self) -> None:
        workspace = Path.cwd().resolve()
        report = self.validate_text(
            lean_prp(workspace).replace("## Acceptance", "## Behavior"),
            workspace,
        )

        self.assertIn("missing `## Acceptance`", report.errors)

    def test_rejects_uncovered_scenario(self) -> None:
        workspace = Path.cwd().resolve()
        report = self.validate_text(
            lean_prp(workspace).replace("   - Covers: `CX-1`\n", ""),
            workspace,
        )

        self.assertTrue(any("not referenced" in error for error in report.errors))

    def test_rejects_undefined_plan_reference(self) -> None:
        workspace = Path.cwd().resolve()
        report = self.validate_text(
            lean_prp(workspace).replace("`CX-1`\n\n## Validation", "`CX-1`, `CX-2`\n\n## Validation"),
            workspace,
        )

        self.assertTrue(any("undefined scenarios" in error for error in report.errors))

    def test_rejects_workspace_mismatch(self) -> None:
        workspace = Path.cwd().resolve()
        report = self.validate_text(lean_prp(workspace.parent / "other"), workspace)

        self.assertTrue(any("does not match workspace" in error for error in report.errors))

    def test_accepts_legacy_format(self) -> None:
        workspace = Path.cwd().resolve()
        text = lean_prp(workspace).replace("## Acceptance", "## Consumer Contract").replace(
            "## Plan", "## Implementation Blueprint"
        )
        report = self.validate_text(text, workspace)

        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, ["legacy PRP format accepted; conversion is optional"])


if __name__ == "__main__":
    unittest.main()
