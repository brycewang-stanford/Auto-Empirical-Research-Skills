#!/usr/bin/env python3
"""Validate GitHub Actions workflow policy without external dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = ROOT / ".github" / "workflows"
CHECKOUT_RE = re.compile(r"^\s*-\s+uses:\s+actions/checkout@")
USES_RE = re.compile(r"^\s*(?:-\s+)?uses:\s+([^#\s]+)")
FLOATING_REFS = {"HEAD", "latest", "main", "master", "trunk"}
WRITE_PERMISSIONS = {
    "actions",
    "checks",
    "contents",
    "deployments",
    "id-token",
    "issues",
    "packages",
    "pull-requests",
    "security-events",
    "statuses",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def workflow_paths() -> list[Path]:
    if not WORKFLOWS_DIR.exists():
        return []
    paths = list(WORKFLOWS_DIR.glob("*.yml"))
    paths.extend(WORKFLOWS_DIR.glob("*.yaml"))
    return sorted(paths)


def has_top_level_key(lines: list[str], key: str) -> bool:
    prefix = f"{key}:"
    return any(line.startswith(prefix) for line in lines)


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0].rstrip()


def top_level_block(lines: list[str], key: str) -> list[str]:
    block: list[str] = []
    start = None
    prefix = f"{key}:"
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            start = index
            block.append(line)
            break
    if start is None:
        return []
    for line in lines[start + 1 :]:
        if (
            line
            and not line.startswith((" ", "\t"))
            and re.match(r"^[A-Za-z_-][A-Za-z0-9_-]*:", line)
        ):
            break
        block.append(line)
    return block


def workflow_has_event(lines: list[str], event: str) -> bool:
    block = top_level_block(lines, "on")
    if not block:
        return False
    event_re = re.compile(rf"(^|[\s,\[]){re.escape(event)}($|[\s,\]:])")
    first = strip_comment(block[0])
    if event_re.search(first.split(":", 1)[1] if ":" in first else first):
        return True
    for line in block[1:]:
        stripped = strip_comment(line).strip()
        if not stripped:
            continue
        if event_re.search(stripped):
            return True
    return False


def iter_permission_blocks(lines: list[str]) -> list[tuple[int, list[tuple[int, str]]]]:
    blocks: list[tuple[int, list[tuple[int, str]]]] = []
    for index, line in enumerate(lines):
        match = re.match(r"^(\s*)permissions:\s*(.*)$", strip_comment(line))
        if not match:
            continue
        base_indent = len(match.group(1))
        entries = [(index + 1, match.group(2).strip())]
        for offset, child in enumerate(lines[index + 1 :], start=index + 2):
            stripped = strip_comment(child)
            if not stripped.strip():
                entries.append((offset, stripped.strip()))
                continue
            child_indent = len(stripped) - len(stripped.lstrip(" "))
            if child_indent <= base_indent:
                break
            entries.append((offset, stripped.strip()))
        blocks.append((index + 1, entries))
    return blocks


def validate_pr_permissions(path: Path, lines: list[str]) -> list[str]:
    errors: list[str] = []
    if not workflow_has_event(lines, "pull_request"):
        return errors

    for start_line, entries in iter_permission_blocks(lines):
        for line_no, entry in entries:
            if not entry:
                continue
            if entry == "write-all":
                errors.append(
                    f"{rel(path)}:{line_no} pull_request workflows must not use permissions: write-all"
                )
                continue
            match = re.match(r"^([A-Za-z-]+):\s*write\b", entry)
            if match and match.group(1) in WRITE_PERMISSIONS:
                errors.append(
                    f"{rel(path)}:{line_no} pull_request workflow grants write permission: {entry}"
                )
        # Empty permissions blocks are allowed by GitHub but ambiguous for this
        # repo; keep requiring explicit read-only entries in PR workflows.
        if len(entries) == 1 and not entries[0][1]:
            errors.append(f"{rel(path)}:{start_line} pull_request workflow has empty permissions")
    return errors


def validate_checkout_credentials(path: Path, lines: list[str]) -> list[str]:
    errors: list[str] = []
    for index, line in enumerate(lines):
        if not CHECKOUT_RE.match(line):
            continue

        window = lines[index + 1 : index + 9]
        if not any("persist-credentials: false" in item for item in window):
            errors.append(
                f"{rel(path)}:{index + 1} actions/checkout must set persist-credentials: false"
            )
    return errors


def validate_action_refs(path: Path, lines: list[str]) -> list[str]:
    errors: list[str] = []
    for index, line in enumerate(lines):
        match = USES_RE.match(strip_comment(line))
        if not match:
            continue
        target = match.group(1).strip("'\"")
        if target.startswith(("./", "../", "docker://")):
            continue
        if "@" not in target:
            errors.append(f"{rel(path)}:{index + 1} external action must pin a ref: {target}")
            continue
        ref = target.rsplit("@", 1)[1]
        if ref in FLOATING_REFS:
            errors.append(f"{rel(path)}:{index + 1} external action uses floating ref: {target}")
    return errors


def validate_workflow(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    errors: list[str] = []

    if "pull_request_target:" in text:
        errors.append(f"{rel(path)} uses pull_request_target; avoid privileged untrusted PR runs")
    if re.search(r"(curl|wget)\b[^\n|]*\|\s*(bash|sh)\b", text):
        errors.append(f"{rel(path)} pipes downloaded content into a shell")
    if not has_top_level_key(lines, "permissions"):
        errors.append(f"{rel(path)} is missing an explicit top-level permissions block")

    errors.extend(validate_pr_permissions(path, lines))
    errors.extend(validate_checkout_credentials(path, lines))
    errors.extend(validate_action_refs(path, lines))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)

    paths = workflow_paths()
    if not paths:
        print("error: no GitHub Actions workflows found", file=sys.stderr)
        return 1

    errors: list[str] = []
    for path in paths:
        errors.extend(validate_workflow(path))

    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        return 1

    print(f"Workflow policy validation passed for {len(paths)} workflow(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
