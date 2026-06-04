#!/usr/bin/env python3
"""Compare two regression result payloads deterministically."""

from __future__ import annotations

import json
import sys


def _load(path: str) -> dict:
    with open(path, "r") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 2:
        print("usage: compare_specs.py baseline.json variant.json", file=sys.stderr)
        return 1
    baseline = _load(argv[0])
    variant = _load(argv[1])
    result = {}
    for key, value in baseline.items():
        other = variant.get(key)
        if isinstance(value, (int, float)) and isinstance(other, (int, float)):
            result[key] = {
                "baseline": value,
                "variant": other,
                "delta": other - value,
            }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
