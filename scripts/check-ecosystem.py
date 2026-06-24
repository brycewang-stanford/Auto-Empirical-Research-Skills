#!/usr/bin/env python3
"""Validate the ecosystem registry and keep docs/ECOSYSTEM.md in sync with it.

Zero external dependencies. Mirrors scripts/validate-repo.py conventions.

Checks:
  * ecosystem/ecosystem.json parses and has the expected schema.
  * Every project has the required fields, a unique id, an https url, and a
    relation/category drawn from the controlled vocabularies.
  * Every interop role references existing projects (by id) and existing AERS
    collections (paths under skills/ that resolve on disk).
  * docs/ECOSYSTEM.md and docs/INTEROP.md exist, and every project name in the
    JSON is mentioned in docs/ECOSYSTEM.md (drift guard).

Internal markdown link existence is intentionally NOT re-checked here; that is
already covered by scripts/validate-repo.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "ecosystem" / "ecosystem.json"
ECOSYSTEM_DOC = ROOT / "docs" / "ECOSYSTEM.md"
INTEROP_DOC = ROOT / "docs" / "INTEROP.md"

ALLOWED_RELATIONS = {"format-peer", "complement", "sibling", "contrast"}
ALLOWED_CATEGORIES = {
    "agent-skills-library",
    "closed-loop-discovery",
    "research-orchestrator",
    "domain-execution-agent",
    "deep-research",
    "data-science-agent",
}
REQUIRED_PROJECT_FIELDS = (
    "id",
    "name",
    "org",
    "url",
    "category",
    "license",
    "star_snapshot",
    "domain",
    "relation",
    "summary",
    "aers_takeaway",
)
REQUIRED_ROLE_FIELDS = ("role", "description", "external", "aers_collections")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def load_registry(errors: list[str]) -> dict | None:
    if not REGISTRY.exists():
        errors.append(f"missing registry: {rel(REGISTRY)}")
        return None
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{rel(REGISTRY)}: invalid JSON: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{rel(REGISTRY)}: top level must be a JSON object")
        return None
    return data


def check_schema(data: dict, errors: list[str], warnings: list[str]) -> None:
    if data.get("schema_version") != 1:
        errors.append(f"{rel(REGISTRY)}: schema_version must be 1")
    if not isinstance(data.get("updated"), str) or not data.get("updated"):
        errors.append(f"{rel(REGISTRY)}: 'updated' must be a non-empty string (YYYY-MM-DD)")
    if not isinstance(data.get("projects"), list) or not data["projects"]:
        errors.append(f"{rel(REGISTRY)}: 'projects' must be a non-empty list")
    if not isinstance(data.get("interop_roles"), list) or not data["interop_roles"]:
        errors.append(f"{rel(REGISTRY)}: 'interop_roles' must be a non-empty list")


def check_projects(data: dict, errors: list[str], warnings: list[str]) -> set[str]:
    ids: set[str] = set()
    for proj in data.get("projects", []) or []:
        if not isinstance(proj, dict):
            errors.append(f"{rel(REGISTRY)}: project entries must be objects")
            continue
        where = f"project {proj.get('id', '<no-id>')!r}"
        for field in REQUIRED_PROJECT_FIELDS:
            if field not in proj:
                errors.append(f"{where}: missing required field {field!r}")
        pid = proj.get("id")
        if isinstance(pid, str) and pid:
            if pid in ids:
                errors.append(f"{where}: duplicate id")
            ids.add(pid)
        url = proj.get("url")
        if not (isinstance(url, str) and url.startswith("https://")):
            errors.append(f"{where}: url must start with https:// (got {url!r})")
        rel_ = proj.get("relation")
        if rel_ not in ALLOWED_RELATIONS:
            errors.append(f"{where}: relation {rel_!r} not in {sorted(ALLOWED_RELATIONS)}")
        cat = proj.get("category")
        if cat not in ALLOWED_CATEGORIES:
            errors.append(f"{where}: category {cat!r} not in {sorted(ALLOWED_CATEGORIES)}")
        star = proj.get("star_snapshot", 0)
        if star is not None and not isinstance(star, int):
            errors.append(f"{where}: star_snapshot must be an integer or null")
    return ids


def check_roles(data: dict, project_ids: set[str], errors: list[str]) -> None:
    for role in data.get("interop_roles", []) or []:
        if not isinstance(role, dict):
            errors.append(f"{rel(REGISTRY)}: interop_role entries must be objects")
            continue
        where = f"role {role.get('role', '<no-role>')!r}"
        for field in REQUIRED_ROLE_FIELDS:
            if field not in role:
                errors.append(f"{where}: missing required field {field!r}")
        for ext in role.get("external", []) or []:
            if ext not in project_ids:
                errors.append(f"{where}: external id {ext!r} is not a known project id")
        collections = role.get("aers_collections", []) or []
        if not collections:
            errors.append(f"{where}: aers_collections must list at least one collection")
        for coll in collections:
            if not isinstance(coll, str) or not coll.startswith("skills/"):
                errors.append(f"{where}: collection {coll!r} must be a path under skills/")
                continue
            if not (ROOT / coll).exists():
                errors.append(f"{where}: collection path does not exist: {coll}")


def check_docs(data: dict, errors: list[str]) -> None:
    for doc in (ECOSYSTEM_DOC, INTEROP_DOC):
        if not doc.exists():
            errors.append(f"missing doc: {rel(doc)}")
    if not ECOSYSTEM_DOC.exists():
        return
    doc_text = ECOSYSTEM_DOC.read_text(encoding="utf-8")
    for proj in data.get("projects", []) or []:
        name = proj.get("name")
        if isinstance(name, str) and name and name not in doc_text:
            errors.append(
                f"{rel(ECOSYSTEM_DOC)}: project {name!r} is in the registry but not "
                f"mentioned in the doc (drift)"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--audit",
        action="store_true",
        help="print warnings as well as errors (non-zero exit only on errors)",
    )
    args = parser.parse_args(argv)

    errors: list[str] = []
    warnings: list[str] = []

    data = load_registry(errors)
    if data is not None:
        check_schema(data, errors, warnings)
        project_ids = check_projects(data, errors, warnings)
        check_roles(data, project_ids, errors)
        check_docs(data, errors)

    if args.audit and warnings:
        print("ecosystem warnings:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print("ecosystem registry validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    n_projects = len(data.get("projects", [])) if data else 0
    n_roles = len(data.get("interop_roles", [])) if data else 0
    print(f"ecosystem registry OK: {n_projects} projects, {n_roles} interop roles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
