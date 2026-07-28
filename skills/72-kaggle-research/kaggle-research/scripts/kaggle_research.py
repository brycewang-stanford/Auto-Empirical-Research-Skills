#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Optional, Sequence

from kaggle_runtime.artifacts import build_audit_record, write_audit
from kaggle_runtime.result import (
    CommandRequest,
    KaggleRuntimeError,
)
from kaggle_runtime.runner import KaggleRunner
from kaggle_runtime.security import redact_text
from kaggle_runtime.smoke import run_readonly_smoke


def _add_executable_options(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--python",
        type=Path,
        help="Python 3.11+ interpreter containing the kaggle package",
    )
    group.add_argument(
        "--executable",
        type=Path,
        help="Kaggle CLI executable",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Safe, auditable wrapper around the official Kaggle CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser(
        "doctor",
        help="Check CLI version and authenticated read access",
    )
    _add_executable_options(doctor)
    doctor.add_argument("--json", action="store_true", dest="as_json")

    run = subparsers.add_parser(
        "run",
        help="Run an official Kaggle command through the safety boundary",
    )
    _add_executable_options(run)
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--allow-write", action="store_true")
    run.add_argument("--allow-delete", action="store_true")
    run.add_argument("--confirm-resource")
    run.add_argument("--output-root", type=Path)
    run.add_argument("--audit", type=Path)
    run.add_argument("--timeout", type=float, default=120.0)
    run.add_argument("kaggle_arguments", nargs=argparse.REMAINDER)

    smoke = subparsers.add_parser(
        "smoke-readonly",
        help="Run real read-only Kaggle verification",
    )
    _add_executable_options(smoke)
    smoke.add_argument("--output-root", type=Path, required=True)
    smoke.add_argument("--report", type=Path)
    smoke.add_argument(
        "--max-dataset-bytes",
        type=int,
        default=250_000,
    )
    return parser


def _strip_separator(arguments: Sequence[str]) -> tuple[str, ...]:
    values = tuple(arguments)
    if values and values[0] == "--":
        return values[1:]
    return values


def request_from_namespace(namespace: argparse.Namespace) -> CommandRequest:
    arguments = _strip_separator(namespace.kaggle_arguments)
    if not arguments:
        raise ValueError("run requires Kaggle arguments after --")
    return CommandRequest(
        arguments=arguments,
        output_root=namespace.output_root,
        timeout_seconds=namespace.timeout,
        allow_write=namespace.allow_write,
        allow_delete=namespace.allow_delete,
        confirm_resource=namespace.confirm_resource,
        dry_run=namespace.dry_run,
    )


def resolve_executable(
    *,
    python: Optional[Path] = None,
    executable: Optional[Path] = None,
) -> tuple[str, ...]:
    if python is not None and executable is not None:
        raise ValueError("--python and --executable are mutually exclusive")
    if python is not None:
        return (str(python), "-m", "kaggle")
    if executable is not None:
        return (str(executable),)

    environment_python = os.environ.get("AERS_KAGGLE_PYTHON")
    if environment_python:
        return (environment_python, "-m", "kaggle")
    environment_executable = os.environ.get("AERS_KAGGLE_EXECUTABLE")
    if environment_executable:
        return (environment_executable,)
    discovered = shutil.which("kaggle")
    if discovered:
        return (discovered,)
    return (sys.executable, "-m", "kaggle")


def build_doctor_commands() -> tuple[tuple[str, ...], ...]:
    return (
        ("--version",),
        ("datasets", "list", "-m", "-v"),
    )


def _runner(namespace: argparse.Namespace) -> KaggleRunner:
    return KaggleRunner(
        executable=resolve_executable(
            python=getattr(namespace, "python", None),
            executable=getattr(namespace, "executable", None),
        )
    )


def _doctor(namespace: argparse.Namespace) -> int:
    runner = _runner(namespace)
    records = []
    for command in build_doctor_commands():
        result = runner.execute(
            CommandRequest(arguments=command, retries=0)
        )
        records.append(build_audit_record(result, capture_limit=2048))
        if not result.ok:
            raise KaggleRuntimeError(
                result.error_category or "command",
                redact_text(result.stderr or result.stdout),
            )
    payload = {
        "status": "passed",
        "checks": {
            "cli_version": True,
            "authenticated_account_list": True,
        },
        "audits": records,
    }
    if namespace.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Kaggle doctor passed: CLI available and account access authenticated.")
    return 0


def _run(namespace: argparse.Namespace) -> int:
    request = request_from_namespace(namespace)
    result = _runner(namespace).execute(request)
    record = build_audit_record(result, capture_limit=request.capture_limit)
    if namespace.audit is not None:
        write_audit(result, namespace.audit, capture_limit=request.capture_limit)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0 if result.ok else 1


def _smoke(namespace: argparse.Namespace) -> int:
    report = run_readonly_smoke(
        _runner(namespace),
        output_root=namespace.output_root,
        max_dataset_bytes=namespace.max_dataset_bytes,
        report_path=namespace.report,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    namespace = parser.parse_args(argv)
    try:
        if namespace.command == "doctor":
            return _doctor(namespace)
        if namespace.command == "run":
            return _run(namespace)
        if namespace.command == "smoke-readonly":
            return _smoke(namespace)
        parser.error(f"unknown command: {namespace.command}")
    except (KaggleRuntimeError, ValueError) as exc:
        category = getattr(exc, "category", "usage")
        payload = {
            "status": "failed",
            "category": category,
            "message": redact_text(str(exc)),
        }
        print(
            json.dumps(payload, ensure_ascii=False, indent=2),
            file=sys.stderr,
        )
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
