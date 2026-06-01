#!/usr/bin/env python3
"""Validate AERS repository structure without external dependencies."""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _skip_leading_comment(lines: list[str]) -> list[str]:
    """Drop a leading HTML comment banner (vendored CoPaper.AI provenance banner)
    plus surrounding blank lines, so frontmatter after the banner is detected."""
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].lstrip().startswith("<!--"):
        while i < len(lines) and "-->" not in lines[i]:
            i += 1
        i += 1  # move past the line containing -->
        while i < len(lines) and not lines[i].strip():
            i += 1
    return lines[i:]


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = _skip_leading_comment(text.splitlines())
    if not lines or lines[0].strip() != "---":
        return {}

    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return {}

    data: dict[str, str] = {}
    i = 1
    while i < end:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t", "-")):
            i += 1
            continue

        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            i += 1
            continue

        key, value = match.group(1), (match.group(2) or "").strip()
        if value and value[0] in {"|", ">"} and set(value[1:]).issubset({"-", "+"}):
            block: list[str] = []
            i += 1
            while i < end and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            data[key] = " ".join(part for part in block if part).strip()
            continue

        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        data[key] = value
        i += 1

    return data


def iter_skill_files() -> list[Path]:
    """Return exact-case SKILL.md files for cross-platform determinism."""

    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(SKILLS_DIR):
        dirnames[:] = [name for name in dirnames if name not in {".git", "__pycache__"}]
        for filename in filenames:
            if filename == "SKILL.md":
                paths.append(Path(dirpath) / filename)
    return sorted(paths)


def iter_nonstandard_skill_files() -> list[Path]:
    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(SKILLS_DIR):
        dirnames[:] = [name for name in dirnames if name not in {".git", "__pycache__"}]
        for filename in filenames:
            if filename.lower() == "skill.md" and filename != "SKILL.md":
                paths.append(Path(dirpath) / filename)
    return sorted(paths)


def normalize_markdown_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if not target:
        return None
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split()[0]

    target = target.strip()
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return None
    if target.startswith("//"):
        return None
    return unquote(target.split("#", 1)[0])


def iter_project_markdown() -> list[Path]:
    """Markdown maintained by AERS, excluding partial upstream vendor docs."""

    paths: list[Path] = []
    paths.extend(ROOT.glob("*.md"))
    if (ROOT / "docs").exists():
        paths.extend((ROOT / "docs").rglob("*.md"))
    if (ROOT / ".github").exists():
        paths.extend((ROOT / ".github").rglob("*.md"))
    return sorted(set(paths))


def validate_markdown_links() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for md_path in iter_project_markdown():
        text = read_text(md_path)
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = normalize_markdown_target(match.group(1))
            if target is None:
                continue

            resolved = (md_path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                warnings.append(f"{rel(md_path)} links outside repo: {target}")
                continue

            if not resolved.exists():
                line_no = text.count("\n", 0, match.start()) + 1
                errors.append(f"{rel(md_path)}:{line_no} missing local link: {target}")

    return errors, warnings


def validate_skill_frontmatter() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    names: Counter[str] = Counter()
    missing_frontmatter: list[str] = []
    missing_name: list[str] = []
    missing_description: list[str] = []
    oversized: list[str] = []
    unusual_names: list[str] = []

    skill_paths = iter_skill_files() if SKILLS_DIR.exists() else []
    if not skill_paths:
        errors.append("No SKILL.md files found under skills/")
        return errors, warnings

    for skill_path in skill_paths:
        text = read_text(skill_path)
        line_count = len(text.splitlines())
        if line_count > 500:
            oversized.append(f"{rel(skill_path)} ({line_count} lines)")

        frontmatter = parse_frontmatter(text)
        if not frontmatter:
            missing_frontmatter.append(rel(skill_path))
            continue

        name = frontmatter.get("name", "").strip()
        description = frontmatter.get("description", "").strip()
        if not name:
            missing_name.append(rel(skill_path))
        else:
            names[name] += 1
            if not re.match(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$", name):
                unusual_names.append(f"{rel(skill_path)} ({name})")
        if not description:
            missing_description.append(rel(skill_path))

    if missing_frontmatter:
        warnings.append(
            f"{len(missing_frontmatter)} vendored SKILL.md files missing YAML frontmatter; "
            f"first examples: {', '.join(missing_frontmatter[:8])}"
        )
    if missing_name:
        warnings.append(
            f"{len(missing_name)} SKILL.md files missing frontmatter field `name`; "
            f"first examples: {', '.join(missing_name[:8])}"
        )
    if missing_description:
        warnings.append(
            f"{len(missing_description)} SKILL.md files missing frontmatter field `description`; "
            f"first examples: {', '.join(missing_description[:8])}"
        )
    if oversized:
        warnings.append(
            f"{len(oversized)} SKILL.md files exceed 500 lines; first examples: {', '.join(oversized[:8])}"
        )
    if unusual_names:
        warnings.append(
            f"{len(unusual_names)} skill names use non-portable characters; first examples: {', '.join(unusual_names[:8])}"
        )

    duplicates = [(name, count) for name, count in names.most_common() if count > 1]
    if duplicates:
        preview = ", ".join(f"{name} x{count}" for name, count in duplicates[:12])
        warnings.append(f"{len(duplicates)} duplicate skill names found across vendored packs: {preview}")

    nonstandard = iter_nonstandard_skill_files() if SKILLS_DIR.exists() else []
    if nonstandard:
        warnings.append(
            f"{len(nonstandard)} files look like skills but are not exact-case `SKILL.md`; "
            f"first examples: {', '.join(rel(path) for path in nonstandard[:8])}"
        )

    return errors, warnings


def validate_required_files() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required = [
        "README.md",
        "README-zh.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "LICENSE",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "CITATION.cff",
        ".github/workflows/check-external-links.yml",
        "catalog/skills.json",
        "catalog/provenance.json",
        "catalog/skill-audit.json",
        "docs/COMPETITIVE_LANDSCAPE.md",
        "docs/LICENSE_AUDIT.md",
        "docs/RELEASE.md",
        "docs/SKILL_AUDIT.md",
        "docs/SKILL_CATALOG.md",
        "docs/GOLDEN_WORKFLOWS.md",
        "docs/INSTALL.md",
        "docs/SKILL_SUBMISSION_GUIDE.md",
        "docs/demos/README.md",
        "docs/search.html",
    ]
    for item in required:
        if not (ROOT / item).exists():
            errors.append(f"missing required project file: {item}")
    if not (ROOT / ".github" / "workflows").exists():
        warnings.append("missing .github/workflows directory")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--audit", action="store_true", help="print non-blocking vendored-skill audit warnings")
    args = parser.parse_args()

    checks = [
        validate_required_files,
        validate_skill_frontmatter,
        validate_markdown_links,
    ]

    errors: list[str] = []
    warnings: list[str] = []
    for check in checks:
        check_errors, check_warnings = check()
        errors.extend(check_errors)
        warnings.extend(check_warnings)

    if args.audit or args.strict:
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    if args.audit or args.strict:
        print(
            f"Validation complete: {len(errors)} error(s), {len(warnings)} warning(s).",
            file=sys.stderr,
        )
    else:
        print(f"Validation complete: {len(errors)} error(s).", file=sys.stderr)
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
