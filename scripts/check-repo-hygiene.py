#!/usr/bin/env python3
"""Check tracked-file hygiene for local artifacts that should never ship."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_BASENAMES = {
    ".DS_Store",
    "Thumbs.db",
}
FORBIDDEN_PARTS = {
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
}
FORBIDDEN_SUFFIXES = {
    ".pyc",
    ".pyo",
}


def is_forbidden_artifact(path: str) -> bool:
    parts = path.replace("\\", "/").split("/")
    name = parts[-1] if parts else path
    return (
        name in FORBIDDEN_BASENAMES
        or any(part in FORBIDDEN_PARTS for part in parts)
        or any(name.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES)
    )


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return [item.decode("utf-8", errors="replace") for item in result.stdout.split(b"\0") if item]


def ignored_local_artifacts() -> list[str]:
    """Return ignored/untracked artifacts matching the same denylist.

    This is audit-only because local caches can exist harmlessly while developing.
    """

    tracked = set(tracked_files())
    matches: list[str] = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        try:
            repo_path = path.relative_to(ROOT).as_posix()
        except ValueError:
            continue
        if is_forbidden_artifact(repo_path) and repo_path not in tracked:
            matches.append(repo_path)
    return sorted(matches)


def forbidden_tracked_files(paths: list[str]) -> list[str]:
    return sorted(path for path in paths if is_forbidden_artifact(path))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--audit-local",
        action="store_true",
        help="also print ignored local artifacts; this does not fail the check",
    )
    args = parser.parse_args(argv)

    bad = forbidden_tracked_files(tracked_files())
    if bad:
        print("Tracked local/cache artifacts found:", file=sys.stderr)
        for path in bad:
            print(f"  - {path}", file=sys.stderr)
        print("Remove them from git and keep them ignored.", file=sys.stderr)
        return 1

    print("Tracked-file hygiene passed.")
    if args.audit_local:
        local = ignored_local_artifacts()
        if local:
            print(f"Ignored local artifacts present: {len(local)}")
            for path in local[:40]:
                print(f"  - {path}")
            if len(local) > 40:
                print(f"  ... and {len(local) - 40} more")
        else:
            print("No ignored local artifacts found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
