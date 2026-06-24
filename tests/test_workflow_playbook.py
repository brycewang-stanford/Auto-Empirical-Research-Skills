#!/usr/bin/env python3
"""Integrity gate for the 10-stage Chinese research-workflow playbook.

The numbered stage guides under ``docs/01-*.md`` … ``docs/10-*.md`` are the
narrative spine that turns a large vendored skill library into an end-to-end
empirical-research workflow. Their long-standing weakness was that they pointed
*out* to upstream GitHub repos and third-party registries instead of *in* to the
skills this repository actually vendors — so a reader could not click from a
stage to the local skill that implements it, and nothing stopped the prose from
drifting away from what the repo ships.

``scripts/validate-repo.py`` already fails on any *broken* local link, so this
suite does not re-check link existence in general. It locks in the property that
``validate-repo`` cannot express: every stage guide must stay *connected to the
vendored library* — each one references at least ``MIN_COLLECTIONS_PER_STAGE``
distinct top-level ``skills/<NN-collection>/`` folders that genuinely exist.

The checks are intentionally structural (resolve + count), not semantic: editors
own which skills belong in a stage. The gate only guarantees the wiring exists
and never silently rots back into a bare link collection.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
SKILLS_DIR = ROOT / "skills"

# Each guide must wire to at least this many distinct vendored collections.
MIN_COLLECTIONS_PER_STAGE = 3

# Matches the numbered stage guides docs/01-*.md … docs/10-*.md (any title).
STAGE_DOC_RE = re.compile(r"^(0[1-9]|10)-.+\.md$")

# Markdown links that point into the vendored skills tree from docs/, e.g.
# `[...](../skills/00-Full-empirical-analysis-skill_StatsPAI/)` or a deep
# `.../SKILL.md`. Group 1 is the top-level collection directory name.
SKILL_LINK_RE = re.compile(r"\]\(\.\./skills/([^/)#]+)[/)#]")

# Code fences are skipped so that example snippets do not count as live links.
FENCE_RE = re.compile(r"^\s*```")


def _stage_docs() -> list[Path]:
    return sorted(p for p in DOCS_DIR.glob("*.md") if STAGE_DOC_RE.match(p.name))


def _outside_code_fences(text: str) -> str:
    """Return the document text with fenced code blocks blanked out."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def _vendored_collections_in(doc: Path) -> set[str]:
    body = _outside_code_fences(doc.read_text(encoding="utf-8"))
    return set(SKILL_LINK_RE.findall(body))


class StagePlaybookWiringTest(unittest.TestCase):
    def test_exactly_ten_stage_docs_present(self) -> None:
        names = sorted(p.name[:2] for p in _stage_docs())
        self.assertEqual(
            names,
            [f"{i:02d}" for i in range(1, 11)],
            "expected exactly the ten numbered stage guides docs/01..10",
        )

    def test_each_stage_links_to_real_vendored_collections(self) -> None:
        problems: list[str] = []
        for doc in _stage_docs():
            collections = _vendored_collections_in(doc)
            missing = sorted(c for c in collections if not (SKILLS_DIR / c).is_dir())
            if missing:
                problems.append(
                    f"{doc.name}: links to non-existent vendored collection(s): "
                    + ", ".join(missing)
                )
            if len(collections) < MIN_COLLECTIONS_PER_STAGE:
                problems.append(
                    f"{doc.name}: references {len(collections)} vendored collection(s); "
                    f"need >= {MIN_COLLECTIONS_PER_STAGE}. The stage guide must link "
                    f"into the vendored skills/ library, not only to external sources."
                )
        self.assertEqual([], problems, "\n" + "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
