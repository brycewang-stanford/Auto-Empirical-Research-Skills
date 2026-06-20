#!/usr/bin/env python3
"""Summarize a replication log with deterministic heuristics."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("usage: summarize_log.py /path/to/log", file=sys.stderr)
        return 1
    text = Path(argv[0]).read_text()
    lines = text.splitlines()
    payload = {
        "line_count": len(lines),
        "has_error": any("r(" in line or "error" in line.lower() for line in lines),
        "tail": lines[-10:],
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
