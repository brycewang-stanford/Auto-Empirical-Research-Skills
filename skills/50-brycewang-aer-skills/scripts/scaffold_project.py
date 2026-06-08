#!/usr/bin/env python3
"""Scaffold an AER replication project from bundled templates."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "stata": ROOT / "templates" / "stata",
    "r": ROOT / "templates" / "r",
    "python": ROOT / "templates" / "python",
    "skeleton": ROOT / "examples" / "replication-package-skeleton",
}


def ensure_safe_destination(source: Path, destination: Path, replace: bool) -> None:
    source_resolved = source.resolve()
    destination_resolved = destination.expanduser().resolve()
    repo_resolved = ROOT.resolve()
    if (
        destination_resolved == source_resolved
        or source_resolved in destination_resolved.parents
        or destination_resolved in source_resolved.parents
    ):
        raise RuntimeError(
            "Destination must be outside the template source tree and its parents: "
            f"{destination}"
        )

    if destination_resolved == repo_resolved or repo_resolved in destination_resolved.parents:
        raise RuntimeError(f"Refusing to scaffold inside this repository: {destination}")

    protected = {
        Path("/").resolve(),
        Path.home().resolve(),
        Path.cwd().resolve(),
        repo_resolved,
        repo_resolved.parent,
    }
    if replace and destination_resolved in protected:
        raise RuntimeError(f"Refusing to replace protected destination: {destination}")


def copy_tree_contents(source: Path, destination: Path, replace: bool, dry_run: bool) -> list[str]:
    if not source.is_dir():
        raise RuntimeError(f"Template source does not exist: {source}")
    ensure_safe_destination(source, destination, replace=replace)
    if destination.exists() and not destination.is_dir():
        raise RuntimeError(f"Destination exists and is not a directory: {destination}")
    if destination.exists() and any(destination.iterdir()) and not replace:
        raise RuntimeError(
            f"Destination is not empty: {destination}. Use --replace to overwrite it."
        )

    actions: list[str] = []
    for item in sorted(source.iterdir()):
        target = destination / item.name
        actions.append(f"copy {item.relative_to(ROOT)} -> {target}")

    if dry_run:
        return actions

    if destination.exists() and replace:
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for item in sorted(source.iterdir()):
        target = destination / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)
    return actions


def scaffold(kind: str, destination: Path, replace: bool, dry_run: bool) -> list[str]:
    source = SOURCES[kind]
    return copy_tree_contents(
        source=source,
        destination=destination.expanduser(),
        replace=replace,
        dry_run=dry_run,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=sorted(SOURCES), help="template to copy")
    parser.add_argument("destination", type=Path, help="directory to create or populate")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="delete and recreate the destination if it already has files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print planned copies without writing files",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        actions = scaffold(
            kind=args.kind,
            destination=args.destination,
            replace=args.replace,
            dry_run=args.dry_run,
        )
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for action in actions:
        print(action)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
