#!/usr/bin/env python3
"""Validate the small mechanical contract of a PRP."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


CX_RE = re.compile(r"\bCX-\d+[a-z]?\b", re.IGNORECASE)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def section(text: str, *headings: str) -> str:
    alternatives = "|".join(re.escape(heading) for heading in headings)
    match = re.search(
        rf"(?ms)^##\s+(?:{alternatives})\s*$\n(.*?)(?=^##\s|\Z)",
        text,
    )
    return match.group(1) if match else ""


def scenario_ids(body: str) -> list[str]:
    heading_ids = re.findall(r"(?im)^###\s+(CX-\d+[a-z]?)\b", body)
    table_ids = re.findall(r"(?im)^\|\s*`?(CX-\d+[a-z]?)`?\s*\|", body)
    return [item.upper() for item in heading_ids + table_ids]


def validate(path: Path, workspace: Path | None = None) -> Report:
    report = Report()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        report.error(f"cannot read UTF-8 PRP: {exc}")
        return report

    if not re.search(r"(?m)^##\s+Goal\s*$", text):
        report.error("missing `## Goal`")

    acceptance = section(text, "Acceptance")
    plan = section(text, "Plan")
    legacy = False
    if not acceptance or not plan:
        acceptance = section(text, "Consumer Contract")
        plan = section(text, "Implementation Blueprint")
        legacy = bool(acceptance and plan)

    if not acceptance:
        report.error("missing `## Acceptance`")
    if not plan:
        report.error("missing `## Plan`")
    validation = section(text, "Validation")
    if not validation.strip():
        report.error("missing or empty `## Validation`")

    scenarios = scenario_ids(acceptance)
    if not scenarios:
        report.error("acceptance contains no `CX-N` scenarios")
    duplicates = sorted({item for item in scenarios if scenarios.count(item) > 1})
    if duplicates:
        report.error(f"duplicate acceptance scenario IDs: {', '.join(duplicates)}")

    plan_refs = {item.upper() for item in CX_RE.findall(plan)}
    uncovered = sorted(set(scenarios) - plan_refs)
    if uncovered:
        report.error(f"scenarios not referenced by the plan: {', '.join(uncovered)}")

    undefined = sorted(plan_refs - set(scenarios))
    if undefined:
        report.error(f"plan references undefined scenarios: {', '.join(undefined)}")

    if workspace is not None:
        repo_match = re.search(r"(?m)^repo:\s*[`\"']?([^`\"'\n]+)[`\"']?\s*$", text)
        if repo_match:
            declared = Path(repo_match.group(1).strip()).expanduser()
            if declared.is_absolute() and declared.resolve() != workspace.expanduser().resolve():
                report.error(
                    f"frontmatter repo `{declared}` does not match workspace "
                    f"`{workspace.expanduser().resolve()}`"
                )

    if legacy:
        report.warn("legacy PRP format accepted; conversion is optional")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prp", type=Path)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--allow-legacy", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    report = validate(args.prp, args.workspace)
    for message in report.errors:
        print(f"ERROR: {message}")
    for message in report.warnings:
        print(f"WARNING: {message}")
    if report.errors:
        print(f"FAILED: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
        return 1
    print(f"OK: {args.prp} ({len(report.warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
