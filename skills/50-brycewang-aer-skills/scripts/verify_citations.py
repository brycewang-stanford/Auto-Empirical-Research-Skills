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
    "GROUNDED": "ok",
    "BAD_DOI": "fail",
    "FABRICATED": "fail",
    "UNDEFINED_CITATION": "fail",
    "TITLE_MISMATCH": "fail",
    "AUTHOR_MISMATCH": "fail",
    "YEAR_MISMATCH": "fail",
    "PHANTOM_CITATION": "fail",
    "DANGLING_KEY": "fail",
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
# Claim groundedness (no citation from memory, at the prose level)
# --------------------------------------------------------------------------- #
#
# ``verify_entry`` guarantees that every ``references.bib`` entry resolves to a
# real indexed record. Groundedness closes the remaining gap: every *citation in
# the prose* must resolve to such an entry. This is the economics analogue of an
# automated claim-support / anti-hallucination check --- a citation that points
# at nothing is the prose-level signature of a reference written from memory.
#
# Two citation forms are checked:
#   * author-year mentions ("Oster (2019)", "(Callaway and Sant'Anna, 2021)") in
#     skill and reference-doc prose -> must resolve to a bib entry by first-author
#     surname + year (PHANTOM_CITATION on failure);
#   * inline-code bib keys ("`romano_wolf_2005`") anywhere in the repo -> must
#     exist in references.bib (DANGLING_KEY on failure).
#
# Illustrative example *manuscripts* under examples/ deliberately cite the wider
# literature to demonstrate citation style, so they are checked for dangling bib
# keys only, not for author-year groundedness. A line carrying a
# ``<!-- cite-exempt -->`` marker is skipped (use sparingly; it is visible in
# the source and should carry a reason).

# Surfaces scanned. Author-year groundedness is enforced where the repo instructs
# the agent (skills) or documents methods (docs); examples are key-only.
GROUNDEDNESS_AUTHOR_YEAR_DIRS = ("skills", "docs")
GROUNDEDNESS_KEY_ONLY_DIRS = ("examples",)

# Nobiliary particles dropped from surname token sets so "de Chaisemartin"
# matches on "chaisemartin". Hyphenated compounds (Ben-Michael) are kept whole.
_NAME_PARTICLES = {"de", "van", "von", "der", "den", "di", "la", "le", "du",
                   "da", "dos", "del", "della", "ter", "ten"}

# Capitalized words that can precede "(YYYY)" without being an author surname.
_CITATION_STOPWORDS = {
    "table", "figure", "fig", "section", "appendix", "panel", "column", "col",
    "equation", "eq", "note", "notes", "step", "stage", "model", "spec",
    "specification", "theorem", "lemma", "assumption", "footnote", "chapter",
    "part", "box", "exhibit", "row", "line", "page", "version", "item",
    "since", "see", "the", "and", "or", "but", "household", "income", "wave",
    "january", "february", "march", "april", "may", "june", "july", "august",
    "september", "october", "november", "december",
}

_NAME = r"[A-Z][A-Za-z'’.]+(?:-[A-Z][A-Za-z'’.]+)*"
_NAME_CONNECT = r"(?:\s*,\s*(?:and\s+|&\s+)?|\s+(?:and|&)\s+)"
_NAME_GROUP = rf"{_NAME}(?:{_NAME_CONNECT}{_NAME}){{0,3}}(?:\s+et\s+al\.?)?"
_AUTHOR_YEAR_RE = re.compile(rf"\b({_NAME_GROUP})\s*\(\s*((?:19|20)\d{{2}})[a-z]?\s*\)")
_PAREN_CITE_RE = re.compile(rf"\(\s*({_NAME_GROUP}),?\s+((?:19|20)\d{{2}})[a-z]?\s*\)")
_BIB_KEY_TOKEN_RE = re.compile(r"\b([a-z][a-z0-9]*(?:_[a-z0-9]+)*_(?:19|20)\d{2})\b")
_FENCE_RE = re.compile(r"\s*```")
_EXEMPT_RE = re.compile(r"<!--\s*cite-exempt\b[^>]*-->")


def surname_tokens(surname_part: str) -> set[str]:
    """Tokenize a surname into comparable parts, dropping nobiliary particles."""
    toks = {t for t in norm_name(surname_part).split() if len(t) >= 2}
    core = {t for t in toks if t not in _NAME_PARTICLES}
    return core or toks


def entry_surname_tokens(author_field: str) -> set[str]:
    """All surname tokens across every author of a bib ``author`` field."""
    tokens: set[str] = set()
    for chunk in re.split(r"\s+and\s+", (author_field or "").strip()):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "," in chunk:  # "Surname, Given"
            surname_part = chunk.split(",", 1)[0]
        else:  # "Given Surname"
            parts = chunk.split()
            surname_part = parts[-1] if parts else chunk
        tokens |= surname_tokens(surname_part)
    return tokens


def first_author_tokens(name_group: str) -> set[str]:
    """Surname tokens of the *first* author named in a prose citation group."""
    cleaned = re.sub(r"\bet\s+al\.?", "", name_group)
    first = re.split(r"\s*,\s*|\s+(?:and|&)\s+", cleaned.strip())[0]
    return surname_tokens(first)


@dataclass
class BibIndex:
    """Resolution index over references.bib for prose-level grounding."""

    keys: set[str]
    entries: list  # list[tuple[set[str], Optional[int], str]] = (surnames, year, key)

    @classmethod
    def from_entries(cls, entries: Iterable[BibEntry]) -> "BibIndex":
        keys: set[str] = set()
        index: list = []
        for entry in entries:
            if entry.entry_type in {"comment", "string", "preamble"}:
                continue
            keys.add(entry.key)
            author = entry.get("author") or entry.get("editor")
            year_raw = entry.get("year")
            year = int(year_raw) if year_raw.isdigit() else None
            index.append((entry_surname_tokens(author), year, entry.key))
        return cls(keys=keys, entries=index)

    def resolve_author_year(self, author_tokens: set[str], year: int) -> Optional[str]:
        """Return a matching bib key (shared first-author token, year within
        ``YEAR_TOLERANCE``) or ``None`` if the citation grounds nowhere."""
        if not author_tokens:
            return None
        for tokens, entry_year, key in self.entries:
            if entry_year is None:
                continue
            if abs(entry_year - year) <= YEAR_TOLERANCE and (author_tokens & tokens):
                return key
        return None


def _strip_code_fences(text: str) -> str:
    """Blank out fenced ``` code blocks while preserving line numbers."""
    out: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            out.append("")
        else:
            out.append("" if in_fence else line)
    return "\n".join(out)


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _inline_code_spans(text: str) -> list:
    """Yield (content_offset, content) for each inline code span, following the
    CommonMark rule: a run of N backticks is closed only by a run of exactly N.
    Robust to documents that *display* backticks via doubled/quadrupled runs."""
    spans: list = []
    i, n = 0, len(text)
    while i < n:
        if text[i] != "`":
            i += 1
            continue
        j = i
        while j < n and text[j] == "`":
            j += 1
        run = j - i  # opening backtick-run length
        k = j
        closed = False
        while k < n:
            if text[k] == "`":
                m = k
                while m < n and text[m] == "`":
                    m += 1
                if m - k == run:  # matching closing run
                    spans.append((j, text[j:k]))
                    i, closed = m, True
                    break
                k = m
            else:
                k += 1
        if not closed:  # unterminated run: not a code span
            i = j
    return spans


def _exempt_lines(text: str) -> set[int]:
    return {_line_of(text, m.start()) for m in _EXEMPT_RE.finditer(text)}


def groundedness_findings(
    text: str,
    bib_index: BibIndex,
    *,
    label: str,
    check_author_year: bool,
) -> list[Finding]:
    """Findings for one document. ``GROUNDED`` for resolved citations,
    ``PHANTOM_CITATION`` / ``DANGLING_KEY`` for unresolved ones."""
    findings: list[Finding] = []
    body = _strip_code_fences(text)
    exempt = _exempt_lines(text)

    # Check A: inline-code bib keys must exist in references.bib.
    for span_start, content in _inline_code_spans(body):
        for key_match in _BIB_KEY_TOKEN_RE.finditer(content):
            key = key_match.group(1)
            line = _line_of(body, span_start)
            if line in exempt:
                continue
            if key in bib_index.keys:
                findings.append(Finding(f"{label}:{line}", "GROUNDED",
                                        f"`{key}` in references.bib", "groundedness"))
            else:
                findings.append(Finding(f"{label}:{line}", "DANGLING_KEY",
                                        f"`{key}` cited but absent from references.bib", "groundedness"))

    # Check B: author-year mentions must resolve to a references.bib entry.
    if check_author_year:
        seen: set[tuple[int, int]] = set()
        for regex in (_AUTHOR_YEAR_RE, _PAREN_CITE_RE):
            for match in regex.finditer(body):
                key_span = (match.start(), match.end())
                if key_span in seen:
                    continue
                seen.add(key_span)
                name_group, year = match.group(1), int(match.group(2))
                tokens = first_author_tokens(name_group)
                if not tokens or (len(tokens) == 1 and next(iter(tokens)) in _CITATION_STOPWORDS):
                    continue
                line = _line_of(body, match.start())
                if line in exempt:
                    continue
                resolved = bib_index.resolve_author_year(tokens, year)
                citation = f"{' '.join(name_group.split())} ({year})"
                if resolved:
                    findings.append(Finding(f"{label}:{line}", "GROUNDED",
                                            f"{citation} -> {resolved}", "groundedness"))
                else:
                    findings.append(Finding(f"{label}:{line}", "PHANTOM_CITATION",
                                            f"{citation} resolves to no references.bib entry", "groundedness"))
    return findings


def check_groundedness(bib_index: BibIndex, root: Path = ROOT) -> list[Finding]:
    """Scan the repository's prose surfaces for citation groundedness."""
    findings: list[Finding] = []
    for subdir in GROUNDEDNESS_AUTHOR_YEAR_DIRS:
        for path in sorted((root / subdir).rglob("*.md")):
            findings += groundedness_findings(
                path.read_text(encoding="utf-8"), bib_index,
                label=str(path.relative_to(root)), check_author_year=True)
    for subdir in GROUNDEDNESS_KEY_ONLY_DIRS:
        for path in sorted((root / subdir).rglob("*.md")):
            findings += groundedness_findings(
                path.read_text(encoding="utf-8"), bib_index,
                label=str(path.relative_to(root)), check_author_year=False)
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

    # Groundedness regression: labeled snippet cases + a live "repo scans clean".
    bib_index = BibIndex.from_entries(bib_entries)
    ground_cases = gold.get("groundedness_cases", [])
    for case in ground_cases:
        total += 1
        case_findings = groundedness_findings(
            case["text"], bib_index, label=case["id"],
            check_author_year=case.get("check_author_year", True),
        )
        verdicts = {f.verdict for f in case_findings}
        expected = case["expected"]
        if expected == "NONE":
            passed = not any(VERDICT_SEVERITY.get(v) == "fail" for v in verdicts)
        else:
            passed = expected in verdicts
        if not passed:
            failures += 1
            print(
                f"  FAIL {case['id']}: expected {expected}, "
                f"got {sorted(verdicts) or ['<none>']}"
            )
    repo_ground = check_groundedness(bib_index)
    repo_ground_fails = [f for f in repo_ground if f.severity == "fail"]
    for finding in repo_ground_fails:
        failures += 1
        print(f"  FAIL groundedness/{finding.key}: {finding.verdict} -- {finding.detail}")
    repo_ground_ok = sum(1 for f in repo_ground if f.verdict == "GROUNDED")

    status = "PASS" if failures == 0 else "FAIL"
    print(
        f"selftest {status}: {total} gold tuples + {len(bib_entries)} bib entries "
        f"+ {len(ground_cases)} groundedness cases + {repo_ground_ok} repo citations, "
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
    mode.add_argument("--groundedness", action="store_true",
                      help="check that every prose citation grounds in references.bib (hermetic)")
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

    if args.groundedness:
        findings = check_groundedness(BibIndex.from_entries(entries))
        if args.json:
            payload = {
                "mode": "Citation groundedness (prose -> references.bib)",
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
            fails, _ = print_report(findings, title="Citation groundedness (prose -> references.bib)")
        return 1 if fails else 0

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
