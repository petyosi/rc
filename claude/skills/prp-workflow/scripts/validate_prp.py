#!/usr/bin/env python3
"""Validate mechanical PRP structure before semantic review."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


CX_RE = re.compile(r"\bCX-\d+[a-z]?\b", re.IGNORECASE)
TASK_RE = re.compile(r"(?m)^Task\s+\d+[^\n]*:")
HEDGE_RE = re.compile(
    r"\b(where practical|if feasible|when possible|as available|if available|where possible)\b",
    re.IGNORECASE,
)
EXERCISE_ANCHOR_RE = re.compile(
    r"`|\b(run|invoke|open|submit|request|query|render|browser|api|sdk|cli|test|fixture|"
    r"command|build|install|start|call|inspect|exercise|seed|record|upload|download)\b",
    re.IGNORECASE,
)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def section(text: str, heading: str, level: int) -> str:
    marker = "#" * level
    match = re.search(
        rf"(?ms)^{re.escape(marker)}\s+{re.escape(heading)}\s*$\n(.*?)(?=^#{{1,{level}}}\s|\Z)",
        text,
    )
    return match.group(1) if match else ""


def profile(text: str) -> str | None:
    match = re.search(r"(?im)^-\s*\*\*Profile\*\*:\s*(Quick|Standard|Deep)\b", text)
    return match.group(1) if match else None


def acceptance_scenarios(text: str, report: Report) -> list[str]:
    body = section(text, "Acceptance Scenarios", 3)
    if not body:
        report.error("missing `### Acceptance Scenarios` section")
        return []

    found: list[str] = []
    for line in body.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        match = re.fullmatch(r"`?(CX-\d+[a-z]?)`?", cells[0], re.IGNORECASE)
        if not match:
            continue
        scenario = match.group(1).upper()
        found.append(scenario)
        if len(cells) < 6:
            report.error(f"{scenario} acceptance row has {len(cells)} columns; expected 6")
        elif any(not value or value in {"-", "TBD", "TODO"} for value in cells[1:6]):
            report.error(f"{scenario} acceptance row has an empty or placeholder contract cell")
        else:
            exercise = cells[4]
            hedge = HEDGE_RE.search(exercise)
            if hedge:
                report.warn(
                    f"{scenario} exact exercise uses hedged evidence language `{hedge.group(1)}`; "
                    "name a deterministic exercise, explicit conditional gate, or unavailable prerequisite"
                )
            if len(exercise) < 24 or not EXERCISE_ANCHOR_RE.search(exercise):
                report.warn(
                    f"{scenario} exact exercise may not be executable enough; name a command, "
                    "public-boundary action, fixture, and prerequisites"
                )

    if not found:
        report.error("Acceptance Scenarios contains no `CX-N` table rows")
    duplicates = sorted({item for item in found if found.count(item) > 1})
    if duplicates:
        report.error(f"duplicate acceptance scenario IDs: {', '.join(duplicates)}")
    return found


def task_blocks(text: str, report: Report) -> list[tuple[str, str]]:
    blueprint = section(text, "Implementation Blueprint", 2)
    matches = list(TASK_RE.finditer(blueprint))
    if not matches:
        report.error("Implementation Blueprint contains no `Task N:` blocks")
        return []

    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(blueprint)
        blocks.append((match.group(0).rstrip(":"), blueprint[match.start() : end]))
    return blocks


def validate(
    path: Path,
    target_standard_lines: int,
    target_standard_bytes: int,
    max_standard_lines: int,
    max_standard_bytes: int,
    allow_legacy: bool,
    workspace: Path | None,
) -> Report:
    report = Report()
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        report.error(f"cannot read UTF-8 PRP: {exc}")
        return report

    required_headings = (
        "Goal",
        "Success Criteria",
        "Assurance",
        "Consumer Contract",
        "Execution Contract",
        "Implementation Blueprint",
        "Validation",
    )
    for heading in required_headings:
        if not re.search(rf"(?m)^##\s+{re.escape(heading)}\s*$", text):
            message = f"missing required `## {heading}` heading"
            if allow_legacy and heading == "Assurance":
                report.warn(f"legacy PRP: {message}")
            else:
                report.error(message)

    selected_profile = profile(text)
    if selected_profile is None:
        message = "missing Quick, Standard, or Deep `**Profile**` in Assurance"
        (report.warn if allow_legacy else report.error)(f"legacy PRP: {message}" if allow_legacy else message)

    rationale = re.search(r"(?im)^-\s*\*\*Rationale\*\*:\s*(.+)$", text)
    if not rationale or len(rationale.group(1).strip()) < 20:
        message = "Assurance requires a concrete `**Rationale**`"
        (report.warn if allow_legacy else report.error)(f"legacy PRP: {message}" if allow_legacy else message)

    if not re.search(r"(?m)^- \[[ xX]\]\s+\S", section(text, "Success Criteria", 2)):
        report.error("Success Criteria contains no checkable outcomes")

    execution = section(text, "Execution Contract", 2)
    for field_name in ("Planned at commit", "Planning baseline"):
        if not re.search(rf"(?im)^-\s*\*\*{re.escape(field_name)}\*\*:\s*\S", execution):
            report.error(f"Execution Contract missing `**{field_name}**`")

    if workspace is not None:
        expected_workspace = workspace.expanduser().resolve()
        repo_match = re.search(r"(?m)^repo:\s*[`\"']?([^`\"'\n]+)[`\"']?\s*$", text)
        if not repo_match:
            message = "workspace validation requires `repo` frontmatter"
            (report.warn if allow_legacy else report.error)(
                f"legacy PRP: {message}" if allow_legacy else message
            )
        else:
            repo_value = Path(repo_match.group(1).strip()).expanduser()
            if repo_value.is_absolute() and repo_value.resolve() != expected_workspace:
                report.error(
                    f"frontmatter repo `{repo_value}` does not match validator workspace "
                    f"`{expected_workspace}`"
                )
        for raw_path in re.findall(r"(?m)(?:^|[;&|]\s*)cd\s+(/[^\s\\;|&`]+)", text):
            command_path = Path(raw_path.rstrip(".,:)")).expanduser().resolve()
            if command_path != expected_workspace and expected_workspace not in command_path.parents:
                report.error(
                    f"absolute validation path `{command_path}` is outside workspace "
                    f"`{expected_workspace}`; use a workspace-relative command"
                )

    scenarios = acceptance_scenarios(text, report)
    tasks = task_blocks(text, report)
    enabled: set[str] = set()
    parent_refs: set[str] = set()
    for task_name, block in tasks:
        coverage = re.search(r"(?im)^\s*(?:ENABLES|SUPPORTS):\s*(.+)$", block)
        changes_source = bool(re.search(r"(?im)^\s*(?:MODIFY|CREATE|DELETE)\s+\S", block))
        if not coverage and changes_source:
            message = f"{task_name} changes files but is missing `ENABLES:` or `SUPPORTS:`"
            (report.warn if allow_legacy else report.error)(
                f"legacy PRP: {message}" if allow_legacy else message
            )
        elif coverage:
            enabled.update(item.upper() for item in CX_RE.findall(coverage.group(1)))
            parent_refs.update(
                item.upper()
                for item in CX_RE.findall(coverage.group(1))
                if re.search(rf"(?i)parent\s+`?{re.escape(item)}`?", coverage.group(1))
            )
        hedge = HEDGE_RE.search(block)
        if coverage and hedge:
            report.warn(
                f"{task_name} uses hedged evidence language `{hedge.group(1)}` while it owns "
                "consumer scenarios; make the evidence deterministic or add an explicit conditional gate"
            )
        if not re.search(r"(?im)^\s*-?\s*COMMAND:\s*\S", block):
            report.error(f"{task_name} is missing a focused `COMMAND:`")
        if not re.search(r"(?im)^\s*-?\s*EXPECTED:\s*\S", block):
            report.error(f"{task_name} is missing a concrete `EXPECTED:` result")

    missing_task_coverage = sorted(set(scenarios) - enabled)
    if missing_task_coverage:
        report.error(f"acceptance scenarios not enabled by any task: {', '.join(missing_task_coverage)}")
    undefined_task_refs = sorted(enabled - set(scenarios) - parent_refs)
    if undefined_task_refs:
        report.error(f"task `ENABLES` references undefined scenarios: {', '.join(undefined_task_refs)}")

    validation = section(text, "Validation", 2)
    command_lines = [
        line.strip()
        for line in validation.splitlines()
        if line.strip() and not line.lstrip().startswith(("#", "```"))
    ]
    if not command_lines:
        report.error("Validation contains no integrated command or procedure")

    roadmap = section(text, "Roadmap Context", 2)
    if roadmap:
        for field_name in (
            "Parent roadmap",
            "Roadmap step",
            "Satisfied dependencies",
            "Contract produced for later steps",
        ):
            if not re.search(rf"(?im)^-\s*\*\*{re.escape(field_name)}\*\*:\s*\S", roadmap):
                report.error(f"Roadmap Context missing `**{field_name}**`")

    line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
    if selected_profile == "Standard":
        if line_count > target_standard_lines:
            report.warn(
                f"Standard PRP has {line_count} lines (normal target: {target_standard_lines}); "
                "remove repetition before considering the exceptional ceiling"
            )
        if len(raw) > target_standard_bytes:
            report.warn(
                f"Standard PRP is {len(raw)} bytes (normal target: {target_standard_bytes}); "
                "remove repetition before considering the exceptional ceiling"
            )
        if line_count > max_standard_lines:
            report.warn(
                f"Standard PRP exceeds the exceptional {max_standard_lines}-line ceiling; "
                "name the load-bearing reason in Assurance and reapply the roadmap router"
            )
        if len(raw) > max_standard_bytes:
            report.warn(
                f"Standard PRP exceeds the exceptional {max_standard_bytes}-byte ceiling; "
                "name the load-bearing reason in Assurance and reapply the roadmap router"
            )

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prp", type=Path)
    parser.add_argument("--target-standard-lines", type=int, default=300)
    parser.add_argument("--target-standard-bytes", type=int, default=24 * 1024)
    parser.add_argument("--max-standard-lines", type=int, default=400)
    parser.add_argument("--max-standard-bytes", type=int, default=32 * 1024)
    parser.add_argument(
        "--workspace",
        type=Path,
        help="current repository workspace; checks frontmatter and absolute validation paths",
    )
    parser.add_argument(
        "--allow-legacy",
        action="store_true",
        help="downgrade pre-assurance profile/ownership omissions to warnings",
    )
    args = parser.parse_args()

    report = validate(
        args.prp,
        args.target_standard_lines,
        args.target_standard_bytes,
        args.max_standard_lines,
        args.max_standard_bytes,
        args.allow_legacy,
        args.workspace,
    )
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
