#!/usr/bin/env python3
"""Deterministic LaTeX manuscript checks for the aer-consistency skill.

Checks performed (stdlib only, no LaTeX compilation required):

1. Citations two-way: every \\cite-family key has a BibTeX entry, and every
   BibTeX entry is cited at least once.
2. Cross-references two-way: every \\ref/\\autoref/\\eqref/\\cref key has a
   \\label, and every \\label is referenced at least once.
3. Duplicate \\label keys and duplicate BibTeX keys.
4. Abstract word count against the AEA 100-word limit (when an
   abstract environment or \\abstract{} block is found).

Usage:
    python3 audit_manuscript.py paper.tex references.bib
    python3 audit_manuscript.py manuscript_dir/ references.bib

Exit status is 0 when all checks pass, 1 otherwise, so the script can gate
an agent loop or a Makefile target.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CITE_RE = re.compile(r"\\(?:cite|citet|citep|citealt|citealp|citeauthor|citeyearpar|textcite|parencite|autocite)\*?(?:\[[^\]]*\]){0,2}\{([^}]+)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:ref|autoref|eqref|cref|Cref|pageref)\*?\{([^}]+)\}")
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")
ABSTRACT_ENV_RE = re.compile(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", re.DOTALL)
ABSTRACT_CMD_RE = re.compile(r"\\abstract\{((?:[^{}]|\{[^{}]*\})*)\}", re.DOTALL)
COMMENT_RE = re.compile(r"(?<!\\)%.*")
TEX_COMMAND_RE = re.compile(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?")
ABSTRACT_WORD_LIMIT = 100


def strip_comments(text: str) -> str:
    return "\n".join(COMMENT_RE.sub("", line) for line in text.splitlines())


def collect_tex_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(target.rglob("*.tex"))


def split_keys(raw: str) -> list[str]:
    return [key.strip() for key in raw.split(",") if key.strip()]


def abstract_word_count(tex: str) -> int | None:
    match = ABSTRACT_ENV_RE.search(tex) or ABSTRACT_CMD_RE.search(tex)
    if not match:
        return None
    body = TEX_COMMAND_RE.sub(" ", match.group(1))
    body = re.sub(r"[{}~]", " ", body)
    words = [word for word in body.split() if any(ch.isalnum() for ch in word)]
    return len(words)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manuscript", type=Path, help=".tex file or directory of .tex files")
    parser.add_argument("bibliography", type=Path, nargs="?", help="references .bib file")
    args = parser.parse_args()

    tex_files = collect_tex_files(args.manuscript)
    if not tex_files:
        print(f"error: no .tex files found under {args.manuscript}", file=sys.stderr)
        return 1

    cited: list[str] = []
    labels: list[str] = []
    refs: list[str] = []
    abstract_words: int | None = None

    for tex_path in tex_files:
        text = strip_comments(tex_path.read_text(encoding="utf-8", errors="replace"))
        for match in CITE_RE.finditer(text):
            cited.extend(split_keys(match.group(1)))
        labels.extend(LABEL_RE.findall(text))
        for match in REF_RE.finditer(text):
            refs.extend(split_keys(match.group(1)))
        if abstract_words is None:
            abstract_words = abstract_word_count(text)

    failures: list[str] = []

    bib_keys: list[str] = []
    if args.bibliography is not None:
        if not args.bibliography.is_file():
            failures.append(f"bibliography not found: {args.bibliography}")
        else:
            bib_text = args.bibliography.read_text(encoding="utf-8", errors="replace")
            bib_keys = BIB_KEY_RE.findall(bib_text)
            duplicate_bib = sorted({key for key in bib_keys if bib_keys.count(key) > 1})
            for key in duplicate_bib:
                failures.append(f"duplicate BibTeX key: {key}")
            missing_entries = sorted(set(cited) - set(bib_keys))
            for key in missing_entries:
                failures.append(f"cited key has no BibTeX entry: {key}")
            uncited_entries = sorted(set(bib_keys) - set(cited))
            for key in uncited_entries:
                failures.append(f"BibTeX entry never cited: {key}")

    duplicate_labels = sorted({key for key in labels if labels.count(key) > 1})
    for key in duplicate_labels:
        failures.append(f"duplicate label: {key}")
    dangling_refs = sorted(set(refs) - set(labels))
    for key in dangling_refs:
        failures.append(f"reference to missing label: {key}")
    unused_labels = sorted(set(labels) - set(refs))
    for key in unused_labels:
        failures.append(f"label never referenced: {key}")

    if abstract_words is None:
        print("note: no abstract block found; word-count check skipped")
    elif abstract_words > ABSTRACT_WORD_LIMIT:
        failures.append(
            f"abstract is {abstract_words} words; AEA limit is {ABSTRACT_WORD_LIMIT}"
        )
    else:
        print(f"abstract word count: {abstract_words}/{ABSTRACT_WORD_LIMIT}")

    print(
        f"scanned {len(tex_files)} tex file(s): "
        f"{len(set(cited))} cite keys, {len(set(refs))} ref keys, "
        f"{len(set(labels))} labels, {len(set(bib_keys))} bib entries"
    )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"{len(failures)} check(s) failed")
        return 1
    print("all deterministic checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
