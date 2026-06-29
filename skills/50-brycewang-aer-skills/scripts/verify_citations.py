#!/usr/bin/env python3
"""verify_citations.py --- reproducible citation-integrity verification for AER-Skills.

This operationalizes the design principle *"No citation from memory."* Every
``references.bib`` entry is checked against the Crossref REST API (with an
OpenAlex fallback) by DOI, and the recorded title / authors / year are compared
against the index of record. Fabricated DOIs, mis-attributed entries
(title / author / year drift), and structural defects are reported with a
nonzero exit code.

The tool is offline-by-default for CI hygiene:

* ``--selftest``   runs the bundled economics gold set against recorded index
                   responses (hermetic, no network) --- the regression gate.
* ``--offline``    re-verifies ``references.bib`` against the recorded responses
                   shipped in ``scripts/citation_gold/`` (hermetic).
* ``--online``     performs live Crossref / OpenAlex lookups.
* ``--manuscript`` additionally checks two-way ``\\cite`` <-> bib correspondence.

Examples
--------
    python3 scripts/verify_citations.py --selftest
    python3 scripts/verify_citations.py --offline
    python3 scripts/verify_citations.py --online
    python3 scripts/verify_citations.py --online --manuscript paper.tex --json

The script is standard-library only: it adds no third-party dependency to the
repository and runs under the CI Python (3.12+).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BIB = ROOT / "references.bib"
GOLD_DIR = ROOT / "scripts" / "citation_gold"
RECORDED_RESPONSES = GOLD_DIR / "recorded_responses.json"
GOLD_SET = GOLD_DIR / "gold_set.json"

DEFAULT_MAILTO = "aer-skills@users.noreply.github.com"
USER_AGENT = "AER-Skills-citation-verifier/1.0 (https://github.com/brycewang-stanford/AER-Skills)"

# A DOI is a "10." prefix followed by a registrant code and a suffix.
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
# Explicit "this work predates / has no Crossref DOI" markers in a bib note.
NO_DOI_NOTE_RE = re.compile(r"no\s+(crossref\s+)?doi|jstor|stable url|predates", re.IGNORECASE)

# Matching thresholds. Tuned so the 34 hand-verified references.bib entries all
# pass cleanly online, while catching gross fabrication / mis-attribution.
TITLE_SIM_THRESHOLD = 0.82
YEAR_TOLERANCE = 1  # print year vs online-first year may differ by one.


# --------------------------------------------------------------------------- #
# Verdict model
# --------------------------------------------------------------------------- #

# verdict -> severity. "fail" trips the gate; "warn" is reported but tolerated;
# "ok" is a clean pass.
VERDICT_SEVERITY = {
    "VERIFIED": "ok",
    "STRUCTURAL_OK": "ok",
    "EXEMPT": "ok",
    "MISSING_DOI": "warn",
    "UNRESOLVED": "warn",
    "UNCITED": "warn",
    "BAD_DOI": "fail",
    "FABRICATED": "fail",
    "UNDEFINED_CITATION": "fail",
    "TITLE_MISMATCH": "fail",
    "AUTHOR_MISMATCH": "fail",
    "YEAR_MISMATCH": "fail",
}


@dataclass
class Finding:
    key: str
    verdict: str
    detail: str = ""
    source: str = ""

    @property
    def severity(self) -> str:
        return VERDICT_SEVERITY.get(self.verdict, "fail")


@dataclass
class IndexResponse:
    """Normalized lookup result from a bibliographic index."""

    found: bool
    source: str = ""
    title: str = ""
    surnames: list[str] = field(default_factory=list)
    year: Optional[int] = None
    venue: str = ""
    status: str = ""  # "ok", "not_found", or "error: ..."

    def to_record(self) -> dict:
        return {
            "found": self.found,
            "source": self.source,
            "title": self.title,
            "surnames": self.surnames,
            "year": self.year,
            "venue": self.venue,
            "status": self.status,
        }

    @classmethod
    def from_record(cls, doi: str, record: dict) -> "IndexResponse":
        return cls(
            found=bool(record.get("found")),
            source=record.get("source", "recorded"),
            title=record.get("title", ""),
            surnames=list(record.get("surnames", [])),
            year=record.get("year"),
            venue=record.get("venue", ""),
            status=record.get("status", "ok" if record.get("found") else "not_found"),
        )


# --------------------------------------------------------------------------- #
# Text normalization (LaTeX / Unicode aware)
# --------------------------------------------------------------------------- #

_LATEX_ACCENTS = {
    r"\oe": "oe", r"\OE": "OE", r"\ae": "ae", r"\AE": "AE",
    r"\ss": "ss", r"\o": "o", r"\O": "O", r"\l": "l", r"\L": "L",
    r"\aa": "aa", r"\AA": "AA", r"\i": "i", r"\j": "j",
}

# Unicode letters/ligatures that NFKD does not decompose to ASCII. Folding these
# keeps index-side text (raw Unicode from Crossref/OpenAlex) and bib-side text
# (LaTeX escapes) in agreement so author/title comparison stays stable.
_UNICODE_LETTERS = {
    "œ": "oe", "Œ": "OE", "æ": "ae", "Æ": "AE", "ß": "ss",
    "ø": "o", "Ø": "O", "ł": "l", "Ł": "L", "đ": "d", "Đ": "D",
    "ð": "d", "Ð": "D", "þ": "th", "Þ": "Th", "ı": "i",
    "’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-",
}
_UNICODE_TABLE = {ord(k): v for k, v in _UNICODE_LETTERS.items()}


def latex_to_text(value: str) -> str:
    """Best-effort conversion of a BibTeX field to plain Unicode text."""
    text = value
    # Accent commands with an argument: \'e \"o \~n \v{c} \c{c} \={a} \^o \.z \H{o}
    text = re.sub(r"\\[`'\"~^=.uvHcbdr]\s*\{?([A-Za-z])\}?", r"\1", text)
    # Special letter commands (\oe, \ss, \o, ...).
    for command, repl in _LATEX_ACCENTS.items():
        text = text.replace(command + "{}", repl).replace(command + " ", repl + " ")
        text = text.replace(command, repl)
    # Drop remaining backslash commands.
    text = re.sub(r"\\[A-Za-z]+", " ", text)
    # Strip protective braces and stray backslashes.
    text = text.replace("{", "").replace("}", "").replace("\\", " ")
    # Fold non-decomposing Unicode ligatures, then combining accents, to ASCII.
    text = text.translate(_UNICODE_TABLE)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text


def norm_title(value: str) -> str:
    text = latex_to_text(value).lower()
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def norm_name(value: str) -> str:
    text = latex_to_text(value).lower()
    text = re.sub(r"[^a-z ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def bib_surnames(author_field: str) -> list[str]:
    """Extract author surnames from a BibTeX ``author`` field."""
    surnames: list[str] = []
    for chunk in re.split(r"\s+and\s+", author_field.strip()):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "," in chunk:  # "Surname, Given"
            surname = chunk.split(",", 1)[0]
        else:  # "Given Surname"
            surname = chunk.split()[-1] if chunk.split() else chunk
        surname = norm_name(surname)
        # Keep the most significant token (handles "de Chaisemartin").
        if surname:
            surnames.append(surname.split()[-1])
    return surnames


def _token_set(text: str) -> set[str]:
    return {tok for tok in text.split() if len(tok) > 2}


def title_similarity(a: str, b: str) -> float:
    na, nb = norm_title(a), norm_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    import difflib

    ratio = difflib.SequenceMatcher(None, na, nb).ratio()
    sa, sb = _token_set(na), _token_set(nb)
    jaccard = len(sa & sb) / len(sa | sb) if (sa | sb) else 0.0
    return max(ratio, jaccard)


# --------------------------------------------------------------------------- #
# BibTeX parsing (tolerant; not a full BibTeX engine)
# --------------------------------------------------------------------------- #

@dataclass
class BibEntry:
    key: str
    entry_type: str
    fields: dict[str, str]
    raw: str

    def get(self, name: str) -> str:
        return self.fields.get(name.lower(), "")


def _strip_field_value(value: str) -> str:
    value = value.strip()
    if value.endswith(","):
        value = value[:-1].strip()
    if value and value[0] in "{\"" and value[-1] in "}\"":
        value = value[1:-1]
    return value.strip()


def parse_bib(text: str) -> list[BibEntry]:
    entries: list[BibEntry] = []
    for chunk in re.split(r"\n(?=@)", text):
        header = re.match(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", chunk)
        if not header:
            continue
        entry_type, key = header.group(1).lower(), header.group(2)
        fields: dict[str, str] = {}
        body = chunk[header.end():]
        # Match "name = {balanced}" or "name = \"...\"" or "name = bareword".
        for match in re.finditer(
            r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|[^,\n]+)",
            body,
        ):
            name = match.group(1).lower()
            if name in fields:
                continue
            fields[name] = _strip_field_value(match.group(2))
        entries.append(BibEntry(key=key, entry_type=entry_type, fields=fields, raw=chunk))
    return entries


# --------------------------------------------------------------------------- #
# Index clients (standard library only)
# --------------------------------------------------------------------------- #

def _http_get_json(url: str, timeout: float) -> tuple[Optional[dict], str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8", "replace")
        return json.loads(payload), "ok"
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None, "not_found"
        return None, f"error: HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return None, f"error: {exc.reason}"
    except (TimeoutError, json.JSONDecodeError) as exc:
        return None, f"error: {exc}"


def crossref_lookup(doi: str, mailto: str, timeout: float) -> IndexResponse:
    url = (
        "https://api.crossref.org/works/"
        + urllib.parse.quote(doi, safe="")
        + "?mailto="
        + urllib.parse.quote(mailto)
    )
    data, status = _http_get_json(url, timeout)
    if data is None:
        return IndexResponse(found=False, source="crossref", status=status)
    message = data.get("message", {})
    titles = message.get("title") or [""]
    authors = message.get("author") or []
    surnames = [norm_name(a.get("family", "")).split()[-1]
                for a in authors if norm_name(a.get("family", ""))]
    year = _year_from_crossref(message)
    container = message.get("container-title") or [""]
    return IndexResponse(
        found=True,
        source="crossref",
        title=titles[0],
        surnames=surnames,
        year=year,
        venue=container[0],
        status="ok",
    )


def _year_from_crossref(message: dict) -> Optional[int]:
    for key in ("published-print", "published", "issued"):
        parts = (message.get(key) or {}).get("date-parts") or []
        if parts and parts[0]:
            try:
                return int(parts[0][0])
            except (TypeError, ValueError):
                continue
    return None


def openalex_lookup(doi: str, mailto: str, timeout: float) -> IndexResponse:
    url = (
        "https://api.openalex.org/works/doi:"
        + urllib.parse.quote(doi, safe="")
        + "?mailto="
        + urllib.parse.quote(mailto)
    )
    data, status = _http_get_json(url, timeout)
    if data is None:
        return IndexResponse(found=False, source="openalex", status=status)
    surnames = []
    for authorship in data.get("authorships", []):
        name = norm_name((authorship.get("author") or {}).get("display_name", ""))
        if name:
            surnames.append(name.split()[-1])
    source = (data.get("primary_location") or {}).get("source") or {}
    return IndexResponse(
        found=True,
        source="openalex",
        title=data.get("title") or "",
        surnames=surnames,
        year=data.get("publication_year"),
        venue=source.get("display_name") or "",
        status="ok",
    )


class LiveResolver:
    """Resolve a DOI live: Crossref first, OpenAlex as a fallback."""

    def __init__(self, mailto: str = DEFAULT_MAILTO, timeout: float = 15.0) -> None:
        self.mailto = mailto
        self.timeout = timeout

    def resolve(self, doi: str) -> IndexResponse:
        primary = crossref_lookup(doi, self.mailto, self.timeout)
        if primary.found:
            return primary
        fallback = openalex_lookup(doi, self.mailto, self.timeout)
        if fallback.found:
            return fallback
        # Prefer a definitive "not_found" over a transient network error so a
        # genuinely fabricated DOI is reported even if one index is flaky.
        if primary.status == "not_found" or fallback.status == "not_found":
            return IndexResponse(found=False, source="crossref+openalex", status="not_found")
        return IndexResponse(found=False, source="crossref+openalex", status=primary.status)


class RecordedResolver:
    """Resolve a DOI from a recorded-response fixture (hermetic, offline)."""

    def __init__(self, records: dict[str, dict]) -> None:
        self.records = records

    @classmethod
    def from_file(cls, path: Path = RECORDED_RESPONSES) -> "RecordedResolver":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(data.get("responses", {}))

    def resolve(self, doi: str) -> IndexResponse:
        record = self.records.get(doi)
        if record is None:
            return IndexResponse(found=False, source="recorded", status="not_found")
        return IndexResponse.from_record(doi, record)


# --------------------------------------------------------------------------- #
# Verification core
# --------------------------------------------------------------------------- #

def verify_entry(
    key: str,
    doi: str,
    title: str,
    author: str,
    year: Optional[int],
    note: str,
    resolver,
) -> Finding:
    doi = doi.strip()
    if not doi:
        if NO_DOI_NOTE_RE.search(note or ""):
            return Finding(key, "EXEMPT", "no DOI; documented in note", "")
        return Finding(key, "MISSING_DOI", "no DOI and no no-DOI note", "")

    if not DOI_RE.match(doi):
        return Finding(key, "BAD_DOI", f"malformed DOI {doi!r}", "")

    if resolver is None:
        # No-network structural mode: the DOI is well-formed; metadata is not
        # checked. Use --online or --offline to verify against an index.
        return Finding(key, "STRUCTURAL_OK", "DOI well-formed (metadata not checked)", "structural")

    response = resolver.resolve(doi)
    if not response.found:
        if response.status == "not_found":
            return Finding(key, "FABRICATED", f"DOI {doi} does not resolve in any index", response.source)
        return Finding(key, "UNRESOLVED", f"could not reach index ({response.status})", response.source)

    # Title check.
    if title:
        sim = title_similarity(title, response.title)
        if sim < TITLE_SIM_THRESHOLD:
            return Finding(
                key, "TITLE_MISMATCH",
                f"bib title vs {response.source} title differ (sim={sim:.2f}): "
                f"{response.title!r}",
                response.source,
            )

    # Author check: the first bib surname must appear among index authors.
    bib_names = bib_surnames(author) if author else []
    if bib_names and response.surnames:
        index_names = set(response.surnames)
        if bib_names[0] not in index_names:
            return Finding(
                key, "AUTHOR_MISMATCH",
                f"first author {bib_names[0]!r} absent from {response.source} authors "
                f"{sorted(index_names)}",
                response.source,
            )

    # Year check (tolerate print vs online-first drift).
    if year is not None and response.year is not None:
        if abs(int(year) - int(response.year)) > YEAR_TOLERANCE:
            return Finding(
                key, "YEAR_MISMATCH",
                f"bib year {year} vs {response.source} year {response.year}",
                response.source,
            )

    return Finding(key, "VERIFIED", f"matches {response.source} record", response.source)


def verify_bibliography(entries: Iterable[BibEntry], resolver) -> list[Finding]:
    findings: list[Finding] = []
    for entry in entries:
        if entry.entry_type in {"comment", "string", "preamble"}:
            continue
        year_raw = entry.get("year")
        year = int(year_raw) if year_raw.isdigit() else None
        findings.append(
            verify_entry(
                key=entry.key,
                doi=entry.get("doi"),
                title=entry.get("title"),
                author=entry.get("author") or entry.get("editor"),
                year=year,
                note=entry.get("note"),
                resolver=resolver,
            )
        )
    return findings


# --------------------------------------------------------------------------- #
# Two-way cite <-> bib correspondence
# --------------------------------------------------------------------------- #

CITE_COMMANDS = (
    "cite", "citep", "citet", "citealp", "citealt", "citeauthor", "citeyear",
    "textcite", "parencite", "autocite", "footcite", "fullcite", "cites",
)
_CITE_RE = re.compile(r"\\(?:" + "|".join(CITE_COMMANDS) + r")\*?(?:\[[^\]]*\])*\{([^}]*)\}")
_PANDOC_CITE_RE = re.compile(r"@([A-Za-z][\w:-]+)")


def cited_keys(manuscript_text: str) -> set[str]:
    keys: set[str] = set()
    for match in _CITE_RE.finditer(manuscript_text):
        for key in match.group(1).split(","):
            key = key.strip()
            if key:
                keys.add(key)
    # Pandoc/markdown [@key] style, scoped to bracketed citation contexts.
    for bracket in re.findall(r"\[([^\]]*@[^\]]*)\]", manuscript_text):
        for match in _PANDOC_CITE_RE.finditer(bracket):
            keys.add(match.group(1))
    return keys


def check_two_way(bib_keys: set[str], manuscript_text: str) -> list[Finding]:
    findings: list[Finding] = []
    cited = cited_keys(manuscript_text)
    for key in sorted(cited - bib_keys):
        findings.append(Finding(key, "UNDEFINED_CITATION", "cited in manuscript but absent from references.bib", "manuscript"))
    for key in sorted(bib_keys - cited):
        findings.append(Finding(key, "UNCITED", "defined in references.bib but never cited", "manuscript"))
    return findings


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #

def summarize(findings: list[Finding]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.verdict] = counts.get(finding.verdict, 0) + 1
    return counts


def print_report(findings: list[Finding], *, title: str) -> tuple[int, int]:
    fails = [f for f in findings if f.severity == "fail"]
    warns = [f for f in findings if f.severity == "warn"]
    print(f"== {title} ==")
    counts = summarize(findings)
    ok = sum(c for v, c in counts.items() if VERDICT_SEVERITY.get(v) == "ok")
    print(f"  {len(findings)} entries: {ok} ok, {len(warns)} warn, {len(fails)} fail")
    for finding in fails:
        print(f"  FAIL [{finding.verdict}] {finding.key}: {finding.detail}")
    for finding in warns:
        print(f"  warn [{finding.verdict}] {finding.key}: {finding.detail}")
    return len(fails), len(warns)


# --------------------------------------------------------------------------- #
# Gold-set self-test (hermetic regression gate)
# --------------------------------------------------------------------------- #

def run_selftest() -> int:
    if not GOLD_SET.is_file() or not RECORDED_RESPONSES.is_file():
        print("selftest: gold set or recorded responses missing", file=sys.stderr)
        return 2
    gold = json.loads(GOLD_SET.read_text(encoding="utf-8"))
    resolver = RecordedResolver.from_file()
    failures = 0
    total = 0
    for tuple_case in gold["tuples"]:
        total += 1
        finding = verify_entry(
            key=tuple_case["key"],
            doi=tuple_case.get("doi", ""),
            title=tuple_case.get("title", ""),
            author=tuple_case.get("author", ""),
            year=tuple_case.get("year"),
            note=tuple_case.get("note", ""),
            resolver=resolver,
        )
        expected = tuple_case["expected"]
        if finding.verdict != expected:
            failures += 1
            print(
                f"  FAIL {tuple_case['id']} ({tuple_case['key']}): "
                f"expected {expected}, got {finding.verdict} -- {finding.detail}"
            )
    # Also assert the shipped references.bib verifies clean against recorded data.
    bib_entries = parse_bib(DEFAULT_BIB.read_text(encoding="utf-8"))
    bib_findings = verify_bibliography(bib_entries, resolver)
    bib_fails = [f for f in bib_findings if f.severity == "fail"]
    for finding in bib_fails:
        failures += 1
        print(f"  FAIL references.bib/{finding.key}: {finding.verdict} -- {finding.detail}")

    status = "PASS" if failures == 0 else "FAIL"
    print(
        f"selftest {status}: {total} gold tuples + {len(bib_entries)} bib entries, "
        f"{failures} failure(s)"
    )
    return 0 if failures == 0 else 1


def run_record_from_bib(mailto: str, timeout: float) -> int:
    """Maintenance helper: fetch live index data for every bib DOI and persist
    it as the recorded-response fixture. Run this when references.bib changes."""
    entries = parse_bib(DEFAULT_BIB.read_text(encoding="utf-8"))
    resolver = LiveResolver(mailto=mailto, timeout=timeout)
    responses: dict[str, dict] = {}
    for entry in entries:
        doi = entry.get("doi").strip()
        if not doi:
            continue
        response = resolver.resolve(doi)
        responses[doi] = response.to_record()
        print(f"  recorded {doi}: {'ok' if response.found else response.status}")
    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    existing = {}
    if RECORDED_RESPONSES.is_file():
        existing = json.loads(RECORDED_RESPONSES.read_text(encoding="utf-8"))
    # Preserve any hand-authored fabricated/synthetic fixtures already present.
    merged = dict(existing.get("responses", {}))
    merged.update(responses)
    payload = {
        "_comment": (
            "Recorded Crossref/OpenAlex responses for hermetic offline "
            "verification. Regenerate real entries with "
            "`verify_citations.py --record-from-bib`. Synthetic "
            "fabricated/mismatch fixtures for the gold set are appended by hand."
        ),
        "responses": dict(sorted(merged.items())),
    }
    RECORDED_RESPONSES.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(merged)} recorded responses to {RECORDED_RESPONSES.relative_to(ROOT)}")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify citation integrity for the AER-Skills bibliography.",
    )
    parser.add_argument("--bib", type=Path, default=DEFAULT_BIB, help="path to references.bib")
    parser.add_argument("--manuscript", type=Path, help="manuscript file for two-way cite<->bib check")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--online", action="store_true", help="live Crossref/OpenAlex lookups")
    mode.add_argument("--offline", action="store_true", help="verify against recorded responses (hermetic)")
    mode.add_argument("--selftest", action="store_true", help="run the gold-set regression gate (hermetic)")
    mode.add_argument("--record-from-bib", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--mailto", default=DEFAULT_MAILTO, help="contact email for index polite pools")
    parser.add_argument("--timeout", type=float, default=15.0, help="per-request timeout (seconds)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    if args.selftest:
        return run_selftest()
    if args.record_from_bib:
        return run_record_from_bib(args.mailto, args.timeout)

    if not args.bib.is_file():
        print(f"error: {args.bib} not found", file=sys.stderr)
        return 2
    entries = parse_bib(args.bib.read_text(encoding="utf-8"))

    if args.online:
        resolver: object = LiveResolver(mailto=args.mailto, timeout=args.timeout)
        mode_title = "Bibliography verification (online)"
    elif args.offline:
        resolver = RecordedResolver.from_file()
        mode_title = "Bibliography verification (offline / recorded)"
    else:
        resolver = None
        mode_title = "Bibliography structural check (no network)"

    findings = verify_bibliography(entries, resolver)

    if args.manuscript:
        if not args.manuscript.is_file():
            print(f"error: {args.manuscript} not found", file=sys.stderr)
            return 2
        bib_keys = {entry.key for entry in entries}
        findings += check_two_way(bib_keys, args.manuscript.read_text(encoding="utf-8"))

    if args.json:
        payload = {
            "mode": mode_title,
            "summary": summarize(findings),
            "findings": [
                {"key": f.key, "verdict": f.verdict, "severity": f.severity,
                 "detail": f.detail, "source": f.source}
                for f in findings
            ],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        fails = sum(1 for f in findings if f.severity == "fail")
    else:
        fails, _ = print_report(findings, title=mode_title)

    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
