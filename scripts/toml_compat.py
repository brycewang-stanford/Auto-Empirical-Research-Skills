#!/usr/bin/env python3
"""Tiny TOML loading compatibility layer for AERS tooling.

Python 3.11+ ships ``tomllib``. The repo's local gate also needs to run on the
macOS system Python 3.9 without third-party dependencies, so this module falls
back to a deliberately small parser for the TOML subset used by benchmark tasks
and eval scenarios:

- top-level key/value pairs
- ``[[array_of_tables]]`` sections
- strings, multiline strings, booleans, integers, floats
- arrays of primitive values, including multiline arrays

It is not a general-purpose TOML implementation.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any, BinaryIO, TextIO

try:  # Python 3.11+
    import tomllib as _tomllib  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - exercised on Python < 3.11
    _tomllib = None

try:  # Optional when available; not required by the repo.
    import tomli as _tomli  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - dependency-free fallback
    _tomli = None


class TomlCompatError(ValueError):
    """Raised when fallback parsing sees unsupported TOML."""


def load(fp: BinaryIO | TextIO) -> dict[str, Any]:
    """Load TOML from a file object."""
    raw = fp.read()
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    return loads(text)


def load_path(path: str | Path) -> dict[str, Any]:
    """Load TOML from a filesystem path."""
    with Path(path).open("rb") as fh:
        return load(fh)


def loads(text: str) -> dict[str, Any]:
    """Load TOML from a string, using stdlib/``tomli`` when available."""
    if _tomllib is not None:
        return _tomllib.loads(text)
    if _tomli is not None:
        return _tomli.loads(text)
    return _loads_fallback(text)


def _loads_fallback(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    current: dict[str, Any] = root
    pending_key: str | None = None
    pending_value_lines: list[str] = []
    pending_bracket_depth = 0

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        i += 1
        if not line or line.startswith("#"):
            continue

        if pending_key is not None:
            pending_value_lines.append(raw)
            pending_bracket_depth += _bracket_delta(_strip_comment(raw))
            if pending_bracket_depth <= 0:
                current[pending_key] = _parse_value("\n".join(pending_value_lines).strip())
                pending_key = None
                pending_value_lines = []
            continue

        if line.startswith("[[") and line.endswith("]]"):
            section = line[2:-2].strip()
            if not re.fullmatch(r"[A-Za-z0-9_-]+", section):
                raise TomlCompatError(f"unsupported array-of-tables section: {line}")
            item: dict[str, Any] = {}
            root.setdefault(section, []).append(item)
            current = item
            continue

        if line.startswith("["):
            raise TomlCompatError(f"unsupported TOML table header: {line}")

        key, sep, value = raw.partition("=")
        if not sep:
            raise TomlCompatError(f"expected key/value assignment: {raw}")
        key = key.strip()
        value = value.strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]+", key):
            raise TomlCompatError(f"unsupported key syntax: {key}")

        if value.startswith('"""') and not _triple_string_closed(value):
            block = [value]
            while i < len(lines):
                block.append(lines[i])
                if '"""' in lines[i]:
                    i += 1
                    break
                i += 1
            current[key] = _parse_multiline_basic("\n".join(block))
            continue

        if value.startswith("[") and _bracket_delta(_strip_comment(value)) > 0:
            pending_key = key
            pending_value_lines = [value]
            pending_bracket_depth = _bracket_delta(_strip_comment(value))
            continue

        current[key] = _parse_value(_strip_comment(value).strip())

    if pending_key is not None:
        raise TomlCompatError(f"unterminated array for key: {pending_key}")
    return root


def _strip_comment(text: str) -> str:
    """Strip a TOML ``#`` comment outside quoted strings."""
    quote: str | None = None
    escaped = False
    for idx, ch in enumerate(text):
        if quote == '"':
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quote = None
        elif quote == "'":
            if ch == "'":
                quote = None
        else:
            if ch in {"'", '"'}:
                quote = ch
            elif ch == "#":
                return text[:idx].rstrip()
    return text.rstrip()


def _triple_string_closed(value: str) -> bool:
    return value.count('"""') >= 2


def _parse_multiline_basic(value: str) -> str:
    if not (value.startswith('"""') and value.endswith('"""')):
        raise TomlCompatError("unterminated multiline string")
    inner = value[3:-3]
    if inner.startswith("\n"):
        inner = inner[1:]
    return inner


def _bracket_delta(text: str) -> int:
    """Return net square-bracket depth outside strings."""
    quote: str | None = None
    escaped = False
    depth = 0
    for ch in text:
        if quote == '"':
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quote = None
        elif quote == "'":
            if ch == "'":
                quote = None
        else:
            if ch in {"'", '"'}:
                quote = ch
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
    return depth


def _parse_value(value: str) -> Any:
    if value == "true":
        return True
    if value == "false":
        return False
    if value.startswith('"""'):
        return _parse_multiline_basic(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith('"') and value.endswith('"'):
        return ast.literal_eval(value)
    if value.startswith("[") and value.endswith("]"):
        return _parse_array(value)
    if re.fullmatch(r"[+-]?\d+", value):
        return int(value)
    float_re = r"[+-]?(\d+\.\d*|\d*\.\d+)([eE][+-]?\d+)?"
    exponent_re = r"[+-]?\d+[eE][+-]?\d+"
    if re.fullmatch(float_re, value) or re.fullmatch(exponent_re, value):
        return float(value)
    raise TomlCompatError(f"unsupported TOML value: {value!r}")


def _parse_array(value: str) -> list[Any]:
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [_parse_value(part.strip()) for part in _split_array(inner) if part.strip()]


def _split_array(inner: str) -> list[str]:
    parts: list[str] = []
    quote: str | None = None
    escaped = False
    start = 0
    for idx, ch in enumerate(inner):
        if quote == '"':
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quote = None
        elif quote == "'":
            if ch == "'":
                quote = None
        else:
            if ch in {"'", '"'}:
                quote = ch
            elif ch == ",":
                parts.append(_strip_comment(inner[start:idx]).strip())
                start = idx + 1
    parts.append(_strip_comment(inner[start:]).strip())
    return parts
