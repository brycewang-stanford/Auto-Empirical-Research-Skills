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
5. Optional claim-evidence ledger: each high-level empirical claim maps to an
   exhibit label, citation key, or file and has a closed status.

Usage:
    python3 audit_manuscript.py paper.tex references.bib
    python3 audit_manuscript.py manuscript_dir/ references.bib
    python3 audit_manuscript.py manuscript_dir/ references.bib \
        --claim-ledger docs/claim-evidence-ledger.csv

Exit status is 0 when all checks pass, 1 otherwise, so the script can gate
an agent loop or a Makefile target.
"""

from __future__ import annotations

import argparse
import csv
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
CLAIM_LEDGER_COLUMNS = (
    "claim_id",
    "claim_text",
    "claim_location",
    "evidence_type",
    "evidence_ref",
    "status",
)
CLAIM_LEDGER_CLOSED_STATUSES = {"OK", "PASS"}
CLAIM_LEDGER_OPEN_STATUSES = {"OPEN", "REVISE", "DROP", "NEEDS-EVIDENCE"}
CLAIM_LEDGER_ALLOWED_STATUSES = CLAIM_LEDGER_CLOSED_STATUSES | CLAIM_LEDGER_OPEN_STATUSES
CLAIM_LEDGER_REF_PREFIXES = {"label", "ref", "exhibit", "cite", "citation", "file", "external"}


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


def default_claim_ledger(manuscript: Path) -> Path | None:
    if not manuscript.is_dir():
        return None
    for candidate in (
        manuscript / "docs" / "claim-evidence-ledger.csv",
        manuscript / "claim-evidence-ledger.csv",
    ):
        if candidate.is_file():
            return candidate
    return None


def split_claim_refs(raw: str) -> list[str]:
    return [token.strip() for token in raw.replace("\n", ";").split(";") if token.strip()]


def normalize_status(raw: str) -> str:
    return re.sub(r"\s+", "-", raw.strip().upper())


def validate_claim_reference(
    token: str,
    *,
    ledger_path: Path,
    labels: set[str],
    cited: set[str],
    bib_keys: set[str],
    has_bibliography: bool,
) -> list[str]:
    if ":" not in token:
        return [f"claim ledger evidence {token!r} should be prefix:value"]

    prefix, value = token.split(":", 1)
    prefix = prefix.strip().lower()
    value = value.strip()
    if prefix not in CLAIM_LEDGER_REF_PREFIXES:
        return [f"claim ledger evidence {token!r} has unsupported prefix {prefix!r}"]
    if not value:
        return [f"claim ledger evidence {token!r} has empty value"]

    if prefix in {"label", "ref", "exhibit"}:
        if value not in labels:
            return [f"claim ledger evidence {token!r} points to missing label {value!r}"]
        return []

    if prefix in {"cite", "citation"}:
        if not has_bibliography:
            return [f"claim ledger evidence {token!r} requires a bibliography argument"]
        failures = []
        if value not in bib_keys:
            failures.append(f"claim ledger evidence {token!r} has no BibTeX entry")
        if value not in cited:
            failures.append(f"claim ledger evidence {token!r} is not cited in the manuscript")
        return failures

    if prefix == "file":
        file_part = value.split("#", 1)[0]
        target = (ledger_path.parent / file_part).resolve()
        evidence_root = (
            ledger_path.parent.parent
            if ledger_path.parent.name == "docs"
            else ledger_path.parent
        ).resolve()
        try:
            target.relative_to(evidence_root)
        except ValueError:
            return [f"claim ledger evidence {token!r} escapes the evidence package"]
        if not target.exists():
            return [f"claim ledger evidence {token!r} points to missing file"]
        return []

    return []


def audit_claim_ledger(
    ledger_path: Path,
    *,
    labels: set[str],
    cited: set[str],
    bib_keys: set[str],
    has_bibliography: bool,
    allow_open_claims: bool,
) -> tuple[int, list[str]]:
    failures: list[str] = []
    with ledger_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        missing_columns = [name for name in CLAIM_LEDGER_COLUMNS if name not in fieldnames]
        if missing_columns:
            return 0, [
                "claim ledger missing required columns: "
                + ", ".join(missing_columns)
            ]

        row_count = 0
        seen_claim_ids: set[str] = set()
        for row_number, row in enumerate(reader, start=2):
            if not any((value or "").strip() for value in row.values()):
                continue
            row_count += 1
            claim_id = (row.get("claim_id") or "").strip()
            label = claim_id or f"row {row_number}"

            for column in CLAIM_LEDGER_COLUMNS:
                if not (row.get(column) or "").strip():
                    failures.append(f"claim ledger {label}: missing {column}")

            if claim_id:
                if claim_id in seen_claim_ids:
                    failures.append(f"claim ledger {label}: duplicate claim_id")
                seen_claim_ids.add(claim_id)

            status = normalize_status(row.get("status") or "")
            if status and status not in CLAIM_LEDGER_ALLOWED_STATUSES:
                failures.append(
                    f"claim ledger {label}: status {status!r} should be one of "
                    + ", ".join(sorted(CLAIM_LEDGER_ALLOWED_STATUSES))
                )
            elif status and not allow_open_claims and status not in CLAIM_LEDGER_CLOSED_STATUSES:
                failures.append(
                    f"claim ledger {label}: status {status!r} is not closed; "
                    "use OK/PASS or rerun with --allow-open-claims"
                )

            evidence_refs = split_claim_refs(row.get("evidence_ref") or "")
            if not evidence_refs:
                failures.append(f"claim ledger {label}: evidence_ref lists no evidence")
            for token in evidence_refs:
                for failure in validate_claim_reference(
                    token,
                    ledger_path=ledger_path,
                    labels=labels,
                    cited=cited,
                    bib_keys=bib_keys,
                    has_bibliography=has_bibliography,
                ):
                    failures.append(f"claim ledger {label}: {failure}")

    if row_count == 0:
        failures.append("claim ledger has no claim rows")
    return row_count, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manuscript", type=Path, help=".tex file or directory of .tex files")
    parser.add_argument("bibliography", type=Path, nargs="?", help="references .bib file")
    parser.add_argument(
        "--claim-ledger",
        type=Path,
        help="CSV claim-evidence ledger; auto-detected at docs/claim-evidence-ledger.csv for manuscript directories",
    )
    parser.add_argument(
        "--allow-open-claims",
        action="store_true",
        help="allow OPEN/REVISE/DROP/NEEDS-EVIDENCE rows in the claim ledger",
    )
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

    claim_ledger = args.claim_ledger or default_claim_ledger(args.manuscript)
    if claim_ledger is not None:
        if not claim_ledger.is_file():
            failures.append(f"claim ledger not found: {claim_ledger}")
        else:
            claim_count, claim_failures = audit_claim_ledger(
                claim_ledger,
                labels=set(labels),
                cited=set(cited),
                bib_keys=set(bib_keys),
                has_bibliography=args.bibliography is not None,
                allow_open_claims=args.allow_open_claims,
            )
            print(f"claim-evidence ledger: {claim_count} claim row(s) from {claim_ledger}")
            failures.extend(claim_failures)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"{len(failures)} check(s) failed")
        return 1
    print("all deterministic checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
