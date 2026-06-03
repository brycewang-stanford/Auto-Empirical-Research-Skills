#!/usr/bin/env python3
"""Validate AERS repository structure without external dependencies."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
CATALOG_JSON = ROOT / "catalog" / "skills.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def display_path(path: Path) -> str:
    try:
        return rel(path)
    except ValueError:
        return str(path)


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


def parse_markdown_target(raw_target: str) -> tuple[str, str] | None:
    target = raw_target.strip()
    if not target:
        return None
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split()[0]

    target = target.strip()
    if not target:
        return None
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return None
    if target.startswith("//"):
        return None
    path, _, fragment = target.partition("#")
    if not path and not fragment:
        return None
    return unquote(path), unquote(fragment)


def normalize_markdown_target(raw_target: str) -> str | None:
    parsed = parse_markdown_target(raw_target)
    if parsed is None:
        return None
    path, _fragment = parsed
    return path


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
    anchors_by_path: dict[Path, set[str]] = {}
    repo_root = ROOT.resolve()

    for md_path in iter_project_markdown():
        text = read_text(md_path)
        for match in MARKDOWN_LINK_RE.finditer(text):
            if is_in_fenced_code(text, match.start()):
                continue
            parsed = parse_markdown_target(match.group(1))
            if parsed is None:
                continue
            target, fragment = parsed

            resolved = md_path.resolve() if not target else (md_path.parent / target).resolve()
            try:
                resolved.relative_to(repo_root)
            except ValueError:
                warnings.append(f"{rel(md_path)} links outside repo: {target}")
                continue

            if not resolved.exists():
                line_no = text.count("\n", 0, match.start()) + 1
                errors.append(f"{rel(md_path)}:{line_no} missing local link: {target}")
                continue

            if fragment and resolved.suffix.lower() in {".md", ".markdown"}:
                anchors = anchors_by_path.setdefault(resolved, markdown_anchors(read_text(resolved)))
                if normalize_anchor_fragment(fragment) not in anchors:
                    line_no = text.count("\n", 0, match.start()) + 1
                    errors.append(
                        f"{rel(md_path)}:{line_no} missing markdown anchor: "
                        f"{target or rel(md_path)}#{fragment}"
                    )

    return errors, warnings


def normalize_anchor_fragment(fragment: str) -> str:
    return fragment.strip().lstrip("#").lower()


def github_heading_slug(heading: str) -> str:
    text = heading.strip()
    text = re.sub(r"\s+#+\s*$", "", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[([^\]]*)]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower()

    chars: list[str] = []
    for char in text:
        category = unicodedata.category(char)
        if category.startswith("M"):
            continue
        if char.isspace():
            chars.append("-")
        elif category[0] in {"P", "S"} and char not in {"-", "_"}:
            continue
        else:
            chars.append(char)
    return "".join(chars)


def markdown_anchors(text: str) -> set[str]:
    anchors = {"top"}
    seen: Counter[str] = Counter()
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        base = github_heading_slug(match.group(2))
        count = seen[base]
        seen[base] += 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def is_in_fenced_code(text: str, offset: int) -> bool:
    in_fence = False
    for line in text[:offset].splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
    return in_fence


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
        "README-en.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "LICENSE",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "CITATION.cff",
        ".github/dependabot.yml",
        ".github/workflows/check-external-links.yml",
        ".github/workflows/scorecard.yml",
        "benchmark/README.md",
        "benchmark/schema/candidate.schema.json",
        "benchmark/schema/task.schema.json",
        "catalog/skills.json",
        "catalog/provenance.json",
        "catalog/skill-audit.json",
        "docs/AGENT_COORDINATION.md",
        "docs/COMPETITIVE_LANDSCAPE.md",
        "docs/LICENSE_AUDIT.md",
        "docs/MAINTAINER_PLAYBOOK.md",
        "docs/RELEASE.md",
        "docs/SKILL_AUDIT.md",
        "docs/SKILL_CATALOG.md",
        "docs/GOLDEN_WORKFLOWS.md",
        "docs/EVALS.md",
        "docs/INSTALL.md",
        "docs/SKILL_SUBMISSION_GUIDE.md",
        "evals/flagship-evals.json",
        "docs/demos/README.md",
        "docs/search.html",
        "eval-harness/README.md",
        "eval-harness/schema/scenario.schema.json",
        "scripts/check-repo-hygiene.py",
    ]
    for item in required:
        if not (ROOT / item).exists():
            errors.append(f"missing required project file: {item}")
    if not (ROOT / ".github" / "workflows").exists():
        warnings.append("missing .github/workflows directory")
    return errors, warnings


def validate_catalog_snapshot(catalog_path: Path = CATALOG_JSON) -> tuple[list[str], list[str]]:
    """Fast consistency check between the committed catalog summary and skills/.

    The full builders still own deterministic freshness. This cheap check catches
    the common multi-agent failure mode where skill directories are added or
    removed but the catalog has not been regenerated yet.
    """

    errors: list[str] = []
    warnings: list[str] = []
    if not catalog_path.exists():
        return errors, warnings

    try:
        payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{display_path(catalog_path)} is not valid JSON: {exc.msg}"], warnings

    summary = payload.get("summary", {})
    skills = payload.get("skills", [])
    collections = payload.get("collections", [])
    skill_paths = iter_skill_files() if SKILLS_DIR.exists() else []
    collection_ids = {
        path.relative_to(SKILLS_DIR).parts[0]
        for path in skill_paths
        if path.relative_to(SKILLS_DIR).parts
    }

    expected = {
        "skill_files": len(skill_paths),
        "top_level_collections": len(collection_ids),
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(
                f"{display_path(catalog_path)} summary `{key}`={summary.get(key)!r} "
                f"does not match skills/ ({value})"
            )

    if isinstance(skills, list) and len(skills) != len(skill_paths):
        errors.append(
            f"{display_path(catalog_path)} has {len(skills)} skill records but skills/ has {len(skill_paths)} SKILL.md files"
        )
    if isinstance(collections, list) and len(collections) != len(collection_ids):
        errors.append(
            f"{display_path(catalog_path)} has {len(collections)} collection records but skills/ has {len(collection_ids)} collections"
        )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--audit", action="store_true", help="print non-blocking vendored-skill audit warnings")
    args = parser.parse_args()

    checks = [
        validate_required_files,
        validate_catalog_snapshot,
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
