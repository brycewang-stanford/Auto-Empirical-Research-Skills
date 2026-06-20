#!/usr/bin/env python3
"""Build a deterministic catalog of vendored AERS skills."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DEFAULT_JSON = ROOT / "catalog" / "skills.json"
DEFAULT_MARKDOWN = ROOT / "docs" / "SKILL_CATALOG.md"
DEFAULT_PROVENANCE = ROOT / "catalog" / "provenance.json"


@dataclass(frozen=True)
class SkillEntry:
    name: str
    description: str
    path: str
    collection: str
    line_count: int
    frontmatter_fields: list[str]
    has_frontmatter: bool
    has_name: bool
    has_description: bool


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _skip_leading_comment(lines: list[str]) -> list[str]:
    """Drop a leading HTML comment banner plus surrounding blank lines.

    Vendored snapshots prepend a CoPaper.AI provenance banner (`<!-- ... -->`)
    before the YAML frontmatter, which would otherwise hide the frontmatter from
    a parser that requires `---` on the first line.
    """
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
    """Parse the simple YAML frontmatter shape used by SKILL.md files.

    This intentionally avoids a PyYAML dependency. It supports scalar values and
    block scalars, which covers the fields the catalog needs: name/description.
    """

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


def first_sentence(text: str, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def markdown_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def collect_skills() -> list[SkillEntry]:
    entries: list[SkillEntry] = []
    if not SKILLS_DIR.exists():
        return entries

    for skill_path in iter_skill_files():
        text = read_text(skill_path)
        frontmatter = parse_frontmatter(text)
        name = frontmatter.get("name", "").strip()
        description = frontmatter.get("description", "").strip()
        collection = skill_path.relative_to(SKILLS_DIR).parts[0]
        entries.append(
            SkillEntry(
                name=name or skill_path.parent.name,
                description=description,
                path=rel(skill_path),
                collection=collection,
                line_count=len(text.splitlines()),
                frontmatter_fields=sorted(frontmatter.keys()),
                has_frontmatter=bool(frontmatter),
                has_name=bool(name),
                has_description=bool(description),
            )
        )
    return entries


def iter_skill_files() -> list[Path]:
    """Return exact-case SKILL.md files for cross-platform determinism."""

    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(SKILLS_DIR):
        dirnames[:] = [name for name in dirnames if name not in {".git", "__pycache__"}]
        for filename in filenames:
            if filename == "SKILL.md":
                paths.append(Path(dirpath) / filename)
    return sorted(paths)


def collection_records(entries: Iterable[SkillEntry]) -> list[dict[str, object]]:
    provenance = load_provenance()
    by_collection: dict[str, list[SkillEntry]] = {}
    for entry in entries:
        by_collection.setdefault(entry.collection, []).append(entry)

    records: list[dict[str, object]] = []
    for collection in sorted(by_collection):
        collection_path = SKILLS_DIR / collection
        skill_entries = sorted(by_collection[collection], key=lambda item: item.path)
        primary = next(
            (item for item in skill_entries if Path(item.path).parent == Path("skills") / collection),
            skill_entries[0],
        )
        record = {
            "id": collection,
            "path": rel(collection_path),
            "skill_count": len(skill_entries),
            "primary_skill": {
                "name": primary.name,
                "path": primary.path,
                "description": primary.description,
            },
            "has_readme": any(
                (collection_path / name).exists()
                for name in ("README.md", "README-original.md", "CLAUDE.md")
            ),
            "has_license": any(
                (collection_path / name).exists()
                for name in ("LICENSE", "LICENSE.md", "COPYING")
            ),
        }
        if collection in provenance:
            record["source_url"] = provenance[collection].get("source_url")
            record["license"] = provenance[collection].get("license")
            record["commercial_use"] = provenance[collection].get("commercial_use")
            record["source_confidence"] = provenance[collection].get("source_confidence")
            record["sync"] = provenance[collection].get("sync")
        records.append(record)
    return records


def load_provenance(path: Path = DEFAULT_PROVENANCE) -> dict[str, dict[str, object]]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {record["id"]: record for record in data.get("collections", [])}


def build_payload() -> dict[str, object]:
    entries = collect_skills()
    records = collection_records(entries)
    oversized = [entry for entry in entries if entry.line_count > 500]
    missing_frontmatter = [entry for entry in entries if not entry.has_frontmatter]
    missing_description = [entry for entry in entries if not entry.has_description]
    missing_name = [entry for entry in entries if not entry.has_name]

    return {
        "schema_version": "1.0",
        "generated_by": "scripts/build-catalog.py",
        "summary": {
            "top_level_collections": len(records),
            "skill_files": len(entries),
            "oversized_skill_files_over_500_lines": len(oversized),
            "missing_frontmatter": len(missing_frontmatter),
            "missing_name": len(missing_name),
            "missing_description": len(missing_description),
        },
        "collections": records,
        "skills": [
            {
                "name": entry.name,
                "description": entry.description,
                "path": entry.path,
                "collection": entry.collection,
                "line_count": entry.line_count,
                "frontmatter_fields": entry.frontmatter_fields,
                "has_frontmatter": entry.has_frontmatter,
                "has_name": entry.has_name,
                "has_description": entry.has_description,
            }
            for entry in entries
        ],
    }


def render_markdown(payload: dict[str, object]) -> str:
    summary = payload["summary"]
    collections = payload["collections"]
    skills = payload["skills"]

    lines = [
        "# AERS Local Skill Catalog",
        "",
        "This file is generated by `scripts/build-catalog.py`. Do not edit it by hand; run `make catalog` after adding, removing, or moving skills.",
        "",
        "## Snapshot",
        "",
        f"- Top-level collections: {summary['top_level_collections']}",
        f"- `SKILL.md` files: {summary['skill_files']}",
        f"- `SKILL.md` files over 500 lines: {summary['oversized_skill_files_over_500_lines']}",
        f"- Missing YAML frontmatter: {summary['missing_frontmatter']}",
        f"- Missing `name` frontmatter: {summary['missing_name']}",
        f"- Missing `description` frontmatter: {summary['missing_description']}",
        "",
        "## How To Use",
        "",
        "- Start with the top-level collection table when choosing a source repository.",
        "- Open the local `SKILL.md` path when you want the exact agent instructions.",
        "- Use `catalog/skills.json` for search UIs, docs tooling, or downstream package indexes.",
        "",
        "## Top-Level Collections",
        "",
        "| # | Collection | Skills | License | Source | Primary skill | Description |",
        "|---:|---|---:|---|---|---|---|",
    ]

    for index, collection in enumerate(collections, start=1):
        primary = collection["primary_skill"]
        lines.append(
            "| {index} | [`{collection_id}`](../{path}/) | {count} | {license} | {source} | [`{name}`](../{skill_path}) | {description} |".format(
                index=index,
                collection_id=markdown_escape(collection["id"]),
                path=collection["path"],
                count=collection["skill_count"],
                license=markdown_escape(collection.get("license", "")),
                source=(
                    f"[source]({collection['source_url']})"
                    if collection.get("source_url")
                    else "UNKNOWN"
                ),
                name=markdown_escape(primary["name"]),
                skill_path=primary["path"],
                description=markdown_escape(first_sentence(primary["description"])),
            )
        )

    lines.extend(["", "## All SKILL.md Entries", ""])

    skills_by_collection: dict[str, list[dict[str, object]]] = {}
    for skill in skills:
        skills_by_collection.setdefault(skill["collection"], []).append(skill)

    for collection in sorted(skills_by_collection):
        collection_skills = sorted(skills_by_collection[collection], key=lambda item: item["path"])
        lines.extend(
            [
                f"<details>",
                f"<summary><code>{markdown_escape(collection)}</code> ({len(collection_skills)} skills)</summary>",
                "",
                "| Name | Lines | Path | Description |",
                "|---|---:|---|---|",
            ]
        )
        for skill in collection_skills:
            lines.append(
                "| `{name}` | {lines_count} | [`SKILL.md`](../{path}) | {description} |".format(
                    name=markdown_escape(skill["name"]),
                    lines_count=skill["line_count"],
                    path=skill["path"],
                    description=markdown_escape(first_sentence(skill["description"], limit=180)),
                )
            )
        lines.extend(["", "</details>", ""])

    return "\n".join(lines).rstrip() + "\n"


def write_outputs(payload: dict[str, object], json_path: Path, markdown_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")


def check_outputs(payload: dict[str, object], json_path: Path, markdown_path: Path) -> int:
    expected_json = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    expected_markdown = render_markdown(payload)
    failures: list[str] = []

    if not json_path.exists() or json_path.read_text(encoding="utf-8") != expected_json:
        failures.append(str(json_path.relative_to(ROOT)))
    if not markdown_path.exists() or markdown_path.read_text(encoding="utf-8") != expected_markdown:
        failures.append(str(markdown_path.relative_to(ROOT)))

    if failures:
        print("Catalog is stale. Regenerate with `make catalog`.", file=sys.stderr)
        for failure in failures:
            print(f"stale: {failure}", file=sys.stderr)
        return 1
    print("Catalog is current.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--check", action="store_true", help="fail if generated outputs are stale")
    args = parser.parse_args()

    payload = build_payload()
    if args.check:
        return check_outputs(payload, args.json, args.markdown)

    write_outputs(payload, args.json, args.markdown)
    print(f"Wrote {args.json.relative_to(ROOT)}")
    print(f"Wrote {args.markdown.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
