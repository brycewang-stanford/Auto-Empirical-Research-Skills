#!/usr/bin/env python3
"""Summarize the mcp-stata runtime environment in a deterministic format."""

from __future__ import annotations

import json
import os
import platform
import sys
from pathlib import Path


def main() -> int:
    payload = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cwd": str(Path.cwd()),
        "env": {
            "STATA_PATH": os.environ.get("STATA_PATH", ""),
            "MCP_STATA_STARTUP_DO_FILE": os.environ.get("MCP_STATA_STARTUP_DO_FILE", ""),
            "MCP_STATA_TEMP_DIR": os.environ.get("MCP_STATA_TEMP_DIR", ""),
        },
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
