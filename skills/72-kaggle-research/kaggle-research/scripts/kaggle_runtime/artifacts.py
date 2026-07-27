from __future__ import annotations

import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import Any

from .result import CommandResult, KaggleRuntimeError
from .security import redact_arguments, redact_text, resolve_output_path


AUDIT_SCHEMA_VERSION = "aers.kaggle.audit/v1"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _captured_stream(value: str, capture_limit: int) -> dict[str, Any]:
    raw = value.encode("utf-8", errors="replace")
    redacted = redact_text(value)
    truncated = len(redacted) > capture_limit
    return {
        "text": redacted[:capture_limit],
        "truncated": truncated,
        "bytes": len(raw),
        "sha256": _sha256_bytes(raw),
    }


def build_audit_record(
    result: CommandResult,
    *,
    capture_limit: int = 16_384,
) -> dict[str, Any]:
    if capture_limit < 0:
        raise ValueError("capture_limit cannot be negative")
    return {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "operation_id": str(uuid.uuid4()),
        "started_at": result.started_at,
        "finished_at": result.finished_at,
        "duration_seconds": result.duration_seconds,
        "operation": result.operation.value,
        "executable": list(redact_arguments(result.executable)),
        "arguments": list(redact_arguments(result.arguments)),
        "returncode": result.returncode,
        "ok": result.ok,
        "attempts": result.attempts,
        "dry_run": result.dry_run,
        "error_category": result.error_category,
        "stdout": _captured_stream(result.stdout, capture_limit),
        "stderr": _captured_stream(result.stderr, capture_limit),
        "artifacts": [dict(entry) for entry in result.artifacts],
    }


def write_audit(
    result: CommandResult,
    destination: Path,
    *,
    capture_limit: int = 16_384,
) -> Path:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    payload = build_audit_record(result, capture_limit=capture_limit)
    try:
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return path


def build_artifact_manifest(
    root: Path,
    *,
    max_total_bytes: int,
) -> list[dict[str, Any]]:
    if max_total_bytes < 0:
        raise ValueError("max_total_bytes cannot be negative")
    resolved_root = Path(root).resolve(strict=False)
    if not resolved_root.is_dir():
        raise KaggleRuntimeError(
            "artifact",
            f"Artifact root is not a directory: {resolved_root}",
        )

    files = sorted(
        (path for path in resolved_root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(resolved_root).parts,
    )
    total = 0
    manifest: list[dict[str, Any]] = []
    for path in files:
        resolved_path = path.resolve(strict=True)
        resolve_output_path(resolved_root, resolved_path)
        size = resolved_path.stat().st_size
        total += size
        if total > max_total_bytes:
            raise KaggleRuntimeError(
                "artifact",
                (
                    "Artifact total exceeds configured limit "
                    f"of {max_total_bytes} bytes"
                ),
                details={"observed_bytes": total},
            )
        manifest.append(
            {
                "path": path.relative_to(resolved_root).as_posix(),
                "size": size,
                "sha256": _sha256_file(resolved_path),
            }
        )
    return manifest
