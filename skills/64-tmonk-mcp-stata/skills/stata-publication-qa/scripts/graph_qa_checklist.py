#!/usr/bin/env python3
"""Emit a deterministic graph QA checklist from a graph name and notes."""

from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph-name", default="Graph")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()
    checklist = {
        "graph_name": args.graph_name,
        "checks": [
            "Title and subtitle match the paper narrative",
            "Axis labels are readable and interpretable",
            "Legend labels are publication ready",
            "Scale choices do not hide economically meaningful variation",
            "Notes and sample definitions are complete",
        ],
        "notes": args.notes,
    }
    print(json.dumps(checklist, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
