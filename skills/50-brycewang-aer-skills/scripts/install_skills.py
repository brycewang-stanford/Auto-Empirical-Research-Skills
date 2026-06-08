#!/usr/bin/env python3
"""Install the AER skill directories into Codex or Claude Code."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
PROTECTED_REPO_DESTINATIONS = (
    ROOT,
    ROOT / "skills",
    ROOT / "docs",
    ROOT / "templates",
    ROOT / "examples",
    ROOT / "scripts",
    ROOT / ".github",
    ROOT / ".claude-plugin",
    ROOT / "assets",
)


def default_destination(target: str) -> Path:
    if target == "codex":
        codex_home = os.environ.get("CODEX_HOME")
        if codex_home:
            return Path(codex_home).expanduser() / "skills"
        return Path.home() / ".codex" / "skills"
    if target == "claude":
        return Path.home() / ".claude" / "skills"
    raise ValueError(f"Unsupported target: {target}")


def skill_dirs() -> list[Path]:
    return sorted(path for path in SKILLS_DIR.glob("aer-*") if path.is_dir())


def ensure_destination_not_source(source: Path, destination: Path) -> None:
    source_resolved = source.resolve()
    destination_resolved = destination.expanduser().resolve()
    if destination_resolved == source_resolved or source_resolved in destination_resolved.parents:
        raise RuntimeError(
            f"Refusing to install {source.name} into its source tree: {destination}"
        )


def ensure_destination_root_safe(destination_root: Path) -> None:
    destination_resolved = destination_root.expanduser().resolve()
    for protected in PROTECTED_REPO_DESTINATIONS:
        protected_resolved = protected.resolve()
        overlaps_protected = destination_resolved == protected_resolved
        if protected_resolved != ROOT.resolve():
            overlaps_protected = overlaps_protected or protected_resolved in destination_resolved.parents
        if overlaps_protected:
            raise RuntimeError(
                "Destination overlaps repository source files; use an agent profile "
                f"skills directory instead: {destination_root}"
            )


def install_one(source: Path, destination_root: Path, replace: bool, dry_run: bool) -> str:
    destination = destination_root / source.name
    ensure_destination_not_source(source, destination)
    if destination.exists():
        if not destination.is_dir():
            raise RuntimeError(f"Destination exists and is not a directory: {destination}")
        if not replace:
            return f"skip existing {destination}"
        if dry_run:
            return f"replace {destination}"
        shutil.rmtree(destination)
    else:
        if dry_run:
            return f"install {destination}"

    if not dry_run:
        shutil.copytree(source, destination)
    return f"installed {destination}"


def install(target: str, destination: Path | None, replace: bool, dry_run: bool) -> list[str]:
    destination_root = (destination or default_destination(target)).expanduser()
    sources = skill_dirs()
    if not sources:
        raise RuntimeError(f"No aer-* skill directories found in {SKILLS_DIR}")

    ensure_destination_root_safe(destination_root)

    if not dry_run:
        destination_root.mkdir(parents=True, exist_ok=True)

    results = []
    for source in sources:
        results.append(install_one(source, destination_root, replace=replace, dry_run=dry_run))
    return results


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target",
        choices=("codex", "claude"),
        help="agent profile to install into",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        help="override destination skills directory",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="replace existing installed aer-* directories",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print planned changes without copying files",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        results = install(
            target=args.target,
            destination=args.dest,
            replace=args.replace,
            dry_run=args.dry_run,
        )
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    for result in results:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
