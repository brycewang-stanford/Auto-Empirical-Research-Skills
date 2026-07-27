from __future__ import annotations

import csv
import io
import json
import re
import tempfile
from pathlib import Path
from typing import Any, Optional, Sequence

from .artifacts import build_artifact_manifest, build_audit_record
from .result import CommandRequest, CommandResult, KaggleRuntimeError
from .security import redact_text


SMOKE_SCHEMA_VERSION = "aers.kaggle.live-smoke/v1"
_VERSION = re.compile(r"(?i)Kaggle\s+CLI\s+(\d+)\.(\d+)(?:\.(\d+))?")


def _require_ok(result: CommandResult, label: str) -> None:
    if result.ok:
        return
    category = result.error_category or "command"
    detail = redact_text(result.stderr or result.stdout).strip()
    message = f"{label} failed"
    if detail:
        message += f": {detail}"
    raise KaggleRuntimeError(category, message)


def _parse_supported_version(output: str) -> tuple[int, int, int]:
    match = _VERSION.search(output)
    if not match:
        raise KaggleRuntimeError(
            "prerequisite",
            "Could not parse the Kaggle CLI version",
        )
    version = tuple(int(part or 0) for part in match.groups())
    if not ((2, 2, 0) <= version < (3, 0, 0)):
        raise KaggleRuntimeError(
            "prerequisite",
            (
                "Kaggle CLI version is unsupported; "
                "expected >=2.2,<3, observed "
                + ".".join(str(part) for part in version)
            ),
        )
    return version


def _csv_rows(output: str) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(output.lstrip("\ufeff")))
    rows: list[dict[str, str]] = []
    for raw in reader:
        rows.append(
            {
                str(key or "").strip().lower(): str(value or "").strip()
                for key, value in raw.items()
            }
        )
    return rows


def _integer(value: str) -> Optional[int]:
    normalized = value.replace(",", "").strip()
    if normalized.isdigit():
        return int(normalized)
    return None


def _dataset_candidates(
    output: str,
    max_dataset_bytes: int,
) -> list[str]:
    candidates: list[str] = []
    for row in _csv_rows(output):
        reference = row.get("ref") or row.get("reference") or ""
        size = _integer(
            row.get("totalbytes")
            or row.get("size")
            or row.get("bytes")
            or ""
        )
        if reference and (size is None or size <= max_dataset_bytes):
            candidates.append(reference)
    if not candidates:
        raise KaggleRuntimeError(
            "parse",
            "Dataset search returned no downloadable result under the size limit",
        )
    return candidates


def _write_report(report: dict[str, Any], destination: Path) -> None:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    try:
        temporary.write_text(
            json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def run_readonly_smoke(
    runner: Any,
    *,
    output_root: Path,
    max_dataset_bytes: int = 250_000,
    report_path: Optional[Path] = None,
) -> dict[str, Any]:
    if max_dataset_bytes <= 0:
        raise ValueError("max_dataset_bytes must be positive")
    root = Path(output_root).resolve(strict=False)
    root.mkdir(parents=True, exist_ok=True)

    checks: dict[str, bool] = {}
    audit_records: list[dict[str, Any]] = []

    def execute(
        arguments: Sequence[str],
        *,
        label: str,
        download_root: Optional[Path] = None,
    ) -> CommandResult:
        result = runner.execute(
            CommandRequest(
                arguments=tuple(arguments),
                output_root=download_root,
                timeout_seconds=120.0,
                retries=1,
            )
        )
        audit_records.append(build_audit_record(result, capture_limit=2048))
        _require_ok(result, label)
        return result

    version_result = execute(("--version",), label="Kaggle CLI version check")
    version = _parse_supported_version(version_result.stdout)
    checks["supported_cli_version"] = True

    execute(
        ("datasets", "list", "-m", "-v"),
        label="Authenticated account dataset listing",
    )
    checks["authenticated_account_list"] = True

    search_result = execute(
        (
            "datasets",
            "list",
            "-s",
            "iris",
            "--file-type",
            "csv",
            "--max-size",
            str(max_dataset_bytes),
            "-v",
        ),
        label="Public dataset search",
    )
    candidates = _dataset_candidates(
        search_result.stdout,
        max_dataset_bytes,
    )
    checks["dataset_search"] = True

    execute(
        ("competitions", "list", "--page-size", "1", "-v"),
        label="Competition listing",
    )
    checks["competitions_list"] = True

    execute(
        ("kernels", "list", "-m", "--page-size", "1", "-v"),
        label="Kernel listing",
    )
    checks["kernels_list"] = True

    execute(
        ("models", "list", "--page-size", "1", "-v"),
        label="Model listing",
    )
    checks["models_list"] = True

    artifacts: list[dict[str, Any]] = []
    downloaded_ref: Optional[str] = None
    with tempfile.TemporaryDirectory(
        prefix="aers-kaggle-smoke-",
        dir=str(root),
    ) as temporary:
        download_root = Path(temporary)
        failures: list[str] = []
        for reference in candidates[:5]:
            result = runner.execute(
                CommandRequest(
                    arguments=(
                        "datasets",
                        "download",
                        "-d",
                        reference,
                    ),
                    output_root=download_root,
                    timeout_seconds=180.0,
                    retries=1,
                )
            )
            audit_records.append(
                build_audit_record(result, capture_limit=2048)
            )
            if not result.ok:
                failures.append(
                    f"{reference}: "
                    + redact_text(result.stderr or result.stdout).strip()
                )
                continue
            artifacts = build_artifact_manifest(
                download_root,
                max_total_bytes=max_dataset_bytes * 2,
            )
            if artifacts and all(entry["size"] > 0 for entry in artifacts):
                downloaded_ref = reference
                break
            failures.append(f"{reference}: no non-empty artifact")

        if downloaded_ref is None:
            raise KaggleRuntimeError(
                "artifact",
                "No candidate dataset produced a valid small artifact: "
                + "; ".join(failures),
            )

    checks["dataset_download"] = True
    checks["artifact_integrity"] = bool(artifacts)

    report: dict[str, Any] = {
        "schema_version": SMOKE_SCHEMA_VERSION,
        "status": "passed",
        "cli_version": ".".join(str(part) for part in version),
        "dataset_ref": downloaded_ref,
        "checks": checks,
        "artifacts": artifacts,
        "audits": audit_records,
    }
    encoded = json.dumps(report, ensure_ascii=False, sort_keys=True)
    checks["report_redacted"] = redact_text(encoded) == encoded
    if not checks["report_redacted"]:
        raise KaggleRuntimeError(
            "artifact",
            "Live smoke report still contains sensitive text",
        )
    if report_path is not None:
        _write_report(report, report_path)
    return report
