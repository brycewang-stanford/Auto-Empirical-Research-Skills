#!/usr/bin/env python3
"""Run runnable example demos when their optional dependencies are available.

The repository's normal preflight is intentionally dependency-light: it checks
that demos are registered, documented, syntactically valid, and dependency
declarations are pinned. This smoke runner is the next layer. It executes demo
assertions in an environment that has the optional Python/R stacks installed,
while skipping missing optional dependencies by default.

Usage:
    python3 scripts/run_example_smoke.py
    python3 scripts/run_example_smoke.py --strict-deps
    python3 scripts/run_example_smoke.py --demo shift-share-demo
    python3 scripts/run_example_smoke.py --language python --dry-run
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import validate_repo


ROOT = validate_repo.ROOT
DEFAULT_TIMEOUT_SECONDS = 240


def package_import_names(package: str) -> list[str]:
    """Return top-level Python import names that satisfy a pinned package."""
    mapped = sorted(
        import_name
        for import_name, pinned in validate_repo.PYTHON_IMPORT_PACKAGE_MAP.items()
        if pinned == package
    )
    return mapped or [package.replace("-", "_")]


def missing_python_packages(packages: set[str]) -> list[str]:
    missing: list[str] = []
    for package in sorted(packages):
        import_names = package_import_names(package)
        if not any(importlib.util.find_spec(name) for name in import_names):
            missing.append(package)
    return missing


def r_vector(packages: set[str]) -> str:
    return "c(" + ", ".join(json.dumps(package) for package in sorted(packages)) + ")"


def missing_r_packages(packages: set[str]) -> tuple[list[str], str | None]:
    rscript = shutil.which("Rscript")
    if not rscript:
        return sorted(packages), "Rscript not found"

    expression = (
        f"pkgs <- {r_vector(packages)}; "
        "missing <- pkgs[!vapply(pkgs, requireNamespace, quietly = TRUE, FUN.VALUE = logical(1))]; "
        "if (length(missing)) { cat(paste(missing, collapse=',')); quit(status=42) }"
    )
    result = subprocess.run(
        [rscript, "-e", expression],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode == 0:
        return [], None
    if result.returncode == 42:
        return [item for item in result.stdout.strip().split(",") if item], None
    return sorted(packages), result.stdout.strip() or "R dependency probe failed"


def iter_demo_scripts(selected: set[str] | None, language: str):
    for demo_name, expected_files in sorted(validate_repo.EXPECTED_EXAMPLE_DEMOS.items()):
        if selected is not None and demo_name not in selected:
            continue
        demo_dir = ROOT / "examples" / demo_name
        for script_name in sorted(expected_files):
            suffix = Path(script_name).suffix
            if suffix == ".py" and language in {"all", "python"}:
                yield demo_name, demo_dir / script_name
            elif suffix == ".R" and language in {"all", "r"}:
                yield demo_name, demo_dir / script_name


def command_for(script_path: Path) -> list[str]:
    if script_path.suffix == ".py":
        return [sys.executable, script_path.name]
    if script_path.suffix == ".R":
        rscript = shutil.which("Rscript") or "Rscript"
        return [rscript, script_path.name]
    raise ValueError(f"unsupported script suffix: {script_path}")


def script_dependencies(script_path: Path) -> tuple[set[str], list[str], str | None]:
    declared = set(validate_repo.declared_deps(script_path))
    if script_path.suffix == ".py":
        return declared, missing_python_packages(declared), None
    if script_path.suffix == ".R":
        missing, reason = missing_r_packages(declared)
        return declared, missing, reason
    return declared, [], None


def text_tail(text: str, lines: int = 30) -> str:
    body = text.strip().splitlines()
    if len(body) <= lines:
        return "\n".join(body)
    return "\n".join(["...", *body[-lines:]])


def run_script(script_path: Path, timeout: int, verbose: bool) -> bool:
    command = command_for(script_path)
    env = os.environ.copy()
    env.setdefault("MPLBACKEND", "Agg")
    env.setdefault("PYTHONUNBUFFERED", "1")

    started = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=script_path.parent,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - started
        output = exc.stdout if isinstance(exc.stdout, str) else ""
        print(
            f"FAIL {validate_repo.rel(script_path)} timed out after {elapsed:.1f}s "
            f"(limit {timeout}s)"
        )
        if output:
            print(text_tail(output))
        return False

    elapsed = time.monotonic() - started
    label = validate_repo.rel(script_path)
    if result.returncode == 0:
        print(f"PASS {label} ({elapsed:.1f}s)")
        if verbose and result.stdout.strip():
            print(text_tail(result.stdout))
        return True

    print(f"FAIL {label} exited {result.returncode} ({elapsed:.1f}s)")
    if result.stdout.strip():
        print(text_tail(result.stdout))
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--demo",
        action="append",
        default=[],
        help="Run one registered demo directory; may be supplied more than once.",
    )
    parser.add_argument(
        "--language",
        choices=("all", "python", "r"),
        default="all",
        help="Limit the run to Python or R demos.",
    )
    parser.add_argument(
        "--strict-deps",
        action="store_true",
        help="Fail instead of skipping demos whose optional dependencies are missing.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Seconds allowed per demo script.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List runnable/skipped demos without executing them.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print captured output for passing demos.",
    )
    args = parser.parse_args()

    selected = set(args.demo) if args.demo else None
    unknown = sorted(selected - set(validate_repo.EXPECTED_EXAMPLE_DEMOS)) if selected else []
    if unknown:
        print(f"ERROR: unknown demo(s): {', '.join(unknown)}", file=sys.stderr)
        return 2

    passed = failed = skipped = 0
    scripts = list(iter_demo_scripts(selected, args.language))
    if not scripts:
        print("ERROR: no demo scripts matched the requested filters", file=sys.stderr)
        return 2

    for demo_name, script_path in scripts:
        declared, missing, reason = script_dependencies(script_path)
        deps = ", ".join(sorted(declared)) if declared else "none"
        label = validate_repo.rel(script_path)
        if missing:
            skipped += 1
            why = reason or f"missing optional dependencies: {', '.join(missing)}"
            print(f"SKIP {label} ({why}; declared deps: {deps})")
            if args.strict_deps:
                failed += 1
            continue
        if args.dry_run:
            print(f"WOULD RUN {label} (deps: {deps})")
            continue
        if run_script(script_path, timeout=args.timeout, verbose=args.verbose):
            passed += 1
        else:
            failed += 1

    if args.dry_run:
        print(f"Dry run complete: {len(scripts) - skipped} runnable, {skipped} skipped.")
        return 1 if failed else 0

    print(f"Example smoke summary: {passed} passed, {skipped} skipped, {failed} failed.")
    if failed:
        return 1
    if passed == 0:
        print("ERROR: no demo scripts ran; install optional dependencies or narrow --demo.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
