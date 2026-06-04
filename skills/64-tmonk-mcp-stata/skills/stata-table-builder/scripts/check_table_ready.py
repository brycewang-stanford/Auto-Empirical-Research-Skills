#!/usr/bin/env python3
"""Check a simple table payload for missing presentation essentials."""

from __future__ import annotations

import json
import sys


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("usage: check_table_ready.py table.json", file=sys.stderr)
        return 1
    with open(argv[0], "r") as handle:
        payload = json.load(handle)
    findings = []
    for required in ("title", "columns", "notes"):
        if not payload.get(required):
            findings.append(f"missing_{required}")
    print(json.dumps({"ready": not findings, "findings": findings}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
