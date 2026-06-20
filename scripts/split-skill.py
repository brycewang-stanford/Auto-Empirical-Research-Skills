#!/usr/bin/env python3
"""Propose (or apply) a progressive-disclosure split for an over-length SKILL.md.

Agent-skill guidance is to keep SKILL.md a lean "spine" (~<500 lines) and push
deep detail into a sibling `references/` directory that the agent loads on
demand. This tool reads a SKILL.md, inventories its top-level `##` sections, and
proposes moving the large ones into `references/NN-slug.md`, leaving a short
summary + link in the spine.

It is **read-only by default** and never edits the input. With `--apply OUTDIR`
it writes the proposed split to a fresh directory so you can review it and copy
it into the skill's UPSTREAM repo (editing vendored, auto-synced copies in this
repo would be overwritten by the next sync).

    python3 scripts/split-skill.py skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md
    python3 scripts/split-skill.py <path> --apply /tmp/statspai-split
    python3 scripts/split-skill.py <path> --threshold 60
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:48] or "section"


def split_frontmatter(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    i = 0
    # Keep a leading HTML comment banner with the spine.
    if lines and lines[0].lstrip().startswith("<!--"):
        while i < len(lines) and "-->" not in lines[i]:
            i += 1
        i += 1
    head = i
    if head < len(lines) and lines[head].strip() == "---":
        j = head + 1
        while j < len(lines) and lines[j].strip() != "---":
            j += 1
        front = "\n".join(lines[: j + 1])
        body = "\n".join(lines[j + 1:])
        return front, body
    return "", text


def sections(body: str) -> list[tuple[str, list[str]]]:
    """Split body into (heading, lines) chunks at top-level `## ` headings."""
    out: list[tuple[str, list[str]]] = []
    cur_title = "(preamble)"
    cur: list[str] = []
    for line in body.splitlines():
        if line.startswith("## ") and not line.startswith("###"):
            out.append((cur_title, cur))
            cur_title, cur = line[3:].strip(), [line]
        else:
            cur.append(line)
    out.append((cur_title, cur))
    return [(t, c) for t, c in out if any(x.strip() for x in c)]


def plan(path: Path, threshold: int) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    front, body = split_frontmatter(text)
    secs = sections(body)
    total = len(text.splitlines())
    rows, moved, spine_lines = [], [], len(front.splitlines())
    n = 0
    for title, lines in secs:
        size = len(lines)
        move = size > threshold and title != "(preamble)"
        if move:
            n += 1
            ref = f"references/{n:02d}-{slugify(title)}.md"
            moved.append((ref, title, size, lines))
            spine_lines += 3  # summary + link stub kept in the spine
        else:
            spine_lines += size
        rows.append({"title": title, "lines": size, "action": "move" if move else "keep",
                     "ref": ref if move else ""})
    return {"path": str(path), "total": total, "threshold": threshold,
            "projected_spine": spine_lines, "rows": rows, "moved": moved,
            "front": front, "sections": secs}


def render_plan(p: dict) -> str:
    out = [f"### `{p['path']}`",
           f"- Current: **{p['total']} lines** · projected spine after split: "
           f"**~{p['projected_spine']} lines** · move threshold: {p['threshold']} lines",
           "", "| Section | Lines | Action | Reference file |", "|---|---:|---|---|"]
    for r in p["rows"]:
        out.append(f"| {r['title']} | {r['lines']} | {r['action']} | "
                   f"{('`' + r['ref'] + '`') if r['ref'] else '—'} |")
    out.append("")
    return "\n".join(out)


def apply_split(p: dict, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "references").mkdir(exist_ok=True)
    spine = [p["front"], ""] if p["front"] else []
    moved_by_title = {title: ref for ref, title, _, _ in p["moved"]}
    for title, lines in p["sections"]:
        if title in moved_by_title:
            ref = moved_by_title[title]
            (outdir / ref).write_text("\n".join(lines) + "\n", encoding="utf-8")
            spine.append(f"## {title}")
            spine.append("")
            spine.append(f"See [`{ref}`]({ref}) for details.")
            spine.append("")
        else:
            spine.extend(lines)
    (outdir / "SKILL.md").write_text("\n".join(spine).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote split to {outdir}/ (SKILL.md + {len(p['moved'])} reference files)")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("skill", help="path to a SKILL.md")
    ap.add_argument("--threshold", type=int, default=80, help="move sections larger than N lines")
    ap.add_argument("--apply", metavar="OUTDIR", help="write the split to OUTDIR (does not touch input)")
    args = ap.parse_args(argv)

    path = Path(args.skill)
    if not path.exists():
        print(f"Not found: {path}", file=sys.stderr)
        return 1
    p = plan(path, args.threshold)
    print(render_plan(p))
    if args.apply:
        apply_split(p, Path(args.apply))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
