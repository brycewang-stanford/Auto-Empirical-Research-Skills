from __future__ import annotations

import os
import re
from collections.abc import Sequence
from pathlib import Path
from typing import Union

from .result import KaggleRuntimeError


REDACTED = "[REDACTED]"

_ENV_SECRET = re.compile(
    r"(?i)\b((?:KAGGLE_(?:API_TOKEN|KEY|USERNAME)|ACCESS_TOKEN|TOKEN)"
    r"\s*=\s*)([^\s,;]+)"
)
_BEARER = re.compile(r"(?i)(Authorization\s*:\s*Bearer\s+)([^\s,;]+)")
_TOKEN_ARGUMENT = re.compile(
    r"(?i)(--?(?:api[-_]?token|token|key)(?:=|\s+))([^\s,;]+)"
)
_SIGNED_QUERY = re.compile(
    r"(?i)([?&](?:X-Goog-Signature|X-Amz-Signature|Signature|"
    r"Access_Token|Token)=)([^&#\s]+)"
)
_KGAT_TOKEN = re.compile(r"\bKGAT_[A-Za-z0-9_-]+\b")
_CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f]")


def redact_text(text: str) -> str:
    value = str(text)
    value = _ENV_SECRET.sub(lambda match: match.group(1) + REDACTED, value)
    value = _BEARER.sub(lambda match: match.group(1) + REDACTED, value)
    value = _TOKEN_ARGUMENT.sub(lambda match: match.group(1) + REDACTED, value)
    value = _SIGNED_QUERY.sub(lambda match: match.group(1) + REDACTED, value)
    value = _KGAT_TOKEN.sub(REDACTED, value)
    return value


def redact_arguments(arguments: Sequence[str]) -> tuple[str, ...]:
    return tuple(redact_text(str(argument)) for argument in arguments)


def _reject_control_characters(value: str, *, label: str) -> None:
    if _CONTROL_CHARACTERS.search(value):
        raise KaggleRuntimeError(
            "path",
            f"{label} cannot contain control characters",
        )


def resolve_output_path(root: Path, candidate: Union[str, Path]) -> Path:
    root_path = Path(root)
    candidate_path = Path(candidate)
    _reject_control_characters(str(root_path), label="Output root")
    _reject_control_characters(str(candidate_path), label="Output path")

    resolved_root = root_path.resolve(strict=False)
    if candidate_path.is_absolute():
        resolved_candidate = candidate_path.resolve(strict=False)
    else:
        resolved_candidate = (resolved_root / candidate_path).resolve(strict=False)

    try:
        common = Path(os.path.commonpath([resolved_root, resolved_candidate]))
    except ValueError as exc:
        raise KaggleRuntimeError(
            "path",
            "Output path is on a different filesystem root",
        ) from exc

    if os.path.normcase(str(common)) != os.path.normcase(str(resolved_root)):
        raise KaggleRuntimeError(
            "path",
            "Output path must remain inside the approved output root",
            details={
                "root": str(resolved_root),
                "candidate": str(resolved_candidate),
            },
        )
    return resolved_candidate
