#!/usr/bin/env python3
"""
Citation Checker — Multi-Source Verification for Academic Reports.

Prevents AI-hallucinated citations from reaching submission.
Uses a cascading verification pipeline: CrossRef → Semantic Scholar → OpenAlex.

Background:
- 6-55% of AI-generated citations are fabricated (varies by model/domain)
- 100+ hallucinated refs found in NeurIPS 2025 accepted papers
- Universities increasingly treat fake citations as academic misconduct
- Three hallucination types: fully fabricated, chimeric (blended), modified real

Usage:
    # Check a single .bib file
    python citation_checker.py references.bib

    # Check all .bib files in a directory
    python citation_checker.py path/to/report/

    # Output as JSON (for CI pipelines)
    python citation_checker.py references.bib --json

    # Verbose mode (show API responses)
    python citation_checker.py references.bib --verbose

Dependencies:
    pip install requests

No API keys required — uses free tiers of CrossRef, Semantic Scholar, and OpenAlex.
"""

import re
import sys
import json
import time
import urllib.parse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: pip install requests")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class BibEntry:
    key: str
    entry_type: str
    title: str
    authors: str
    year: str
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    raw: str = ""
    line_number: int = 0
    file_path: str = ""


@dataclass
class VerificationResult:
    entry: BibEntry
    status: str  # "verified", "suspicious", "not_found", "error"
    confidence: float  # 0.0 - 1.0
    sources_checked: list[str] = field(default_factory=list)
    sources_found: list[str] = field(default_factory=list)
    best_match_title: Optional[str] = None
    best_match_similarity: float = 0.0
    notes: list[str] = field(default_factory=list)
    red_flags: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# BibTeX Parser
# ---------------------------------------------------------------------------

def parse_bib_file(filepath: Path) -> list[BibEntry]:
    """Parse a .bib file and extract entries."""
    entries = []
    content = filepath.read_text(encoding="utf-8", errors="replace")
    # Match @type{key, ... }
    entry_pattern = re.compile(
        r"@(\w+)\{([^,\s]+)\s*,(.+?)\n\}",
        re.DOTALL,
    )

    for match in entry_pattern.finditer(content):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        body = match.group(3)
        line_number = content[: match.start()].count("\n") + 1

        # Skip @comment, @string, @preamble
        if entry_type in ("comment", "string", "preamble"):
            continue

        title = _extract_field(body, "title")
        authors = _extract_field(body, "author")
        year = _extract_field(body, "year")
        doi = _extract_field(body, "doi")
        arxiv_id = _extract_field(body, "eprint") or _extract_field(
            body, "arxiv"
        )

        if not title:
            continue  # Can't verify without title

        entries.append(
            BibEntry(
                key=key,
                entry_type=entry_type,
                title=_clean_latex(title),
                authors=_clean_latex(authors) if authors else "",
                year=year or "",
                doi=doi,
                arxiv_id=arxiv_id,
                raw=match.group(0),
                line_number=line_number,
                file_path=str(filepath),
            )
        )

    return entries


def _extract_field(body: str, field_name: str) -> Optional[str]:
    """Extract a field value from BibTeX body."""
    pattern = re.compile(
        rf"{field_name}\s*=\s*[\{{\"](.+?)[\}}\"]",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(body)
    if match:
        value = match.group(1).strip()
        # Handle nested braces
        value = re.sub(r"\{([^}]*)\}", r"\1", value)
        return value
    return None


def _clean_latex(text: str) -> str:
    """Remove LaTeX commands from text."""
    text = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", text)
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"\\.", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------------------------------------------------
# Similarity
# ---------------------------------------------------------------------------

def title_similarity(a: str, b: str) -> float:
    """Compute normalized token-overlap similarity between two titles."""
    if not a or not b:
        return 0.0
    tokens_a = set(a.lower().split())
    tokens_b = set(b.lower().split())
    # Remove common stop words
    stop = {"the", "a", "an", "of", "for", "in", "on", "to", "and", "with", "by", "from", "is", "are", "at"}
    tokens_a -= stop
    tokens_b -= stop
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


def author_overlap(entry_authors: str, found_authors: str) -> float:
    """Check if author last names overlap between BibTeX entry and API result."""
    if not entry_authors or not found_authors:
        return 0.0

    def extract_last_names(text: str) -> set[str]:
        lower = text.lower().strip()
        names = set()

        if re.search(r"\band\b", lower):
            # BibTeX format: "Last, First and Last, First"
            people = re.split(r"\band\b", lower)
            for person in people:
                person = person.strip()
                if not person:
                    continue
                if "," in person:
                    # "Last, First" → take before comma
                    last = person.split(",")[0].strip().split()[-1]
                    names.add(last)
                else:
                    # "First Last" → take last word
                    words = person.split()
                    if words:
                        names.add(words[-1])
        else:
            # API format: "First Last, First Last" (comma-separated)
            people = lower.split(",")
            for person in people:
                person = person.strip()
                if not person:
                    continue
                words = person.split()
                if len(words) >= 2:
                    names.add(words[-1])
                elif words:
                    names.add(words[0])

        return names

    entry_names = extract_last_names(entry_authors)
    found_names = extract_last_names(found_authors)

    if not entry_names or not found_names:
        return 0.0

    overlap = entry_names & found_names
    return len(overlap) / max(len(entry_names), 1)


# ---------------------------------------------------------------------------
# API Clients (Cascading: CrossRef → Semantic Scholar → OpenAlex)
# ---------------------------------------------------------------------------

HEADERS = {
    "User-Agent": "citation-checker/1.0 (academic-report-verification)"
}


def check_crossref(entry: BibEntry, verbose: bool = False) -> Optional[dict]:
    """Search CrossRef for a matching paper. Covers 140M+ DOI-registered works."""
    try:
        # If DOI is provided, verify directly
        if entry.doi:
            url = f"https://api.crossref.org/works/{entry.doi}"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json()["message"]
                title = data.get("title", [""])[0]
                authors_raw = data.get("author", [])
                authors = ", ".join(
                    f"{a.get('given', '')} {a.get('family', '')}"
                    for a in authors_raw
                )
                return {
                    "source": "CrossRef",
                    "title": title,
                    "authors": authors,
                    "doi": entry.doi,
                    "year": str(
                        data.get("published-print", data.get("published-online", {}))
                        .get("date-parts", [[""]])[0][0]
                    ),
                }

        # Title search — try full title, then subtitle if colon present
        search_titles = [entry.title]
        if ":" in entry.title:
            subtitle = entry.title.split(":", 1)[1].strip()
            if len(subtitle.split()) >= 4:
                search_titles.append(subtitle)

        for search_title in search_titles:
            query = urllib.parse.quote(search_title)
            url = f"https://api.crossref.org/works?query.title={query}&rows=5"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                items = resp.json().get("message", {}).get("items", [])
                for item in items:
                    found_title = item.get("title", [""])[0]
                    sim = title_similarity(entry.title, found_title)
                    if sim > 0.6:
                        authors_raw = item.get("author", [])
                        authors = ", ".join(
                            f"{a.get('given', '')} {a.get('family', '')}"
                            for a in authors_raw
                        )
                        return {
                            "source": "CrossRef",
                            "title": found_title,
                            "authors": authors,
                            "doi": item.get("DOI", ""),
                            "year": str(
                                item.get("published-print", item.get("published-online", {}))
                                .get("date-parts", [[""]])[0][0]
                            ),
                            "similarity": sim,
                        }
    except Exception as e:
        if verbose:
            print(f"  CrossRef error for '{entry.key}': {e}")
    return None


def check_semantic_scholar(
    entry: BibEntry, verbose: bool = False
) -> Optional[dict]:
    """Search Semantic Scholar. Covers 200M+ papers with author disambiguation."""
    query = urllib.parse.quote(entry.title)
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=3&fields=title,authors,year,externalIds"

    for attempt in range(2):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                papers = resp.json().get("data", [])
                for paper in papers:
                    found_title = paper.get("title", "")
                    sim = title_similarity(entry.title, found_title)
                    if sim > 0.6:
                        authors = ", ".join(
                            a.get("name", "") for a in paper.get("authors", [])
                        )
                        ext_ids = paper.get("externalIds", {})
                        return {
                            "source": "Semantic Scholar",
                            "title": found_title,
                            "authors": authors,
                            "doi": ext_ids.get("DOI", ""),
                            "arxiv": ext_ids.get("ArXiv", ""),
                            "year": str(paper.get("year", "")),
                            "similarity": sim,
                        }
                return None  # Got 200 but no match
            elif resp.status_code == 429:
                wait = 5 if attempt == 0 else 10
                if verbose:
                    print(f"  Semantic Scholar rate limited, waiting {wait}s (attempt {attempt + 1})...")
                time.sleep(wait)
                continue
            else:
                return None
        except Exception as e:
            if verbose:
                print(f"  Semantic Scholar error for '{entry.key}': {e}")
            return None
    return None


def check_openalex(entry: BibEntry, verbose: bool = False) -> Optional[dict]:
    """Search OpenAlex. Fully open, broadest coverage (240M+ works)."""
    # Try full title, then subtitle if colon present
    search_titles = [entry.title]
    if ":" in entry.title:
        subtitle = entry.title.split(":", 1)[1].strip()
        if len(subtitle.split()) >= 4:
            search_titles.append(subtitle)

    for search_title in search_titles:
        try:
            query = urllib.parse.quote(search_title)
            url = f"https://api.openalex.org/works?filter=title.search:{query}&per_page=5"
            resp = requests.get(
                url,
                headers={**HEADERS, "Accept": "application/json"},
                timeout=15,
            )
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                for work in results:
                    found_title = work.get("title", "")
                    sim = title_similarity(entry.title, found_title)
                    if sim > 0.6:
                        authors = ", ".join(
                            a.get("author", {}).get("display_name", "")
                            for a in work.get("authorships", [])
                        )
                        return {
                            "source": "OpenAlex",
                            "title": found_title,
                            "authors": authors,
                            "doi": (work.get("doi") or "").replace(
                                "https://doi.org/", ""
                            ),
                            "year": str(work.get("publication_year", "")),
                            "similarity": sim,
                        }
        except Exception as e:
            if verbose:
                print(f"  OpenAlex error for '{entry.key}': {e}")
    return None


# ---------------------------------------------------------------------------
# Red Flag Detection
# ---------------------------------------------------------------------------

def detect_red_flags(entry: BibEntry) -> list[str]:
    """Detect markers that suggest a citation may be AI-hallucinated."""
    flags = []

    # 1. DOI format check
    if entry.doi:
        if not re.match(r"10\.\d{4,}/", entry.doi):
            flags.append(f"Invalid DOI format: '{entry.doi}'")

    # 2. Suspiciously generic title
    generic_patterns = [
        r"^a (?:comprehensive |novel |survey)",
        r"^towards ",
        r"(?:comprehensive|systematic) (?:survey|review|study|analysis)",
    ]
    for pattern in generic_patterns:
        if re.search(pattern, entry.title.lower()):
            flags.append(
                "Title matches common AI-hallucination pattern (overly generic)"
            )
            break

    # 3. Missing key fields
    if not entry.authors:
        flags.append("Missing author field")
    if not entry.year:
        flags.append("Missing year field")

    # 4. Future year
    if entry.year and entry.year.isdigit():
        if int(entry.year) > 2026:
            flags.append(f"Future year: {entry.year}")

    # 5. Author name patterns — split by "and" (BibTeX convention), not comma
    if entry.authors:
        author_parts = re.split(r"\band\b", entry.authors)
        for part in author_parts:
            stripped = part.strip().strip(",").strip()
            if stripped and len(stripped.split()) == 1 and len(stripped) > 2:
                flags.append(
                    f"Single-word author name: '{stripped}' (may be incomplete)"
                )

    return flags


# ---------------------------------------------------------------------------
# Verification Engine
# ---------------------------------------------------------------------------

def verify_entry(entry: BibEntry, verbose: bool = False) -> VerificationResult:
    """Verify a single BibTeX entry using cascading multi-source lookup."""
    result = VerificationResult(entry=entry, status="not_found", confidence=0.0)
    result.red_flags = detect_red_flags(entry)

    # Cascade: CrossRef → Semantic Scholar → OpenAlex
    checkers = [
        ("CrossRef", check_crossref),
        ("Semantic Scholar", check_semantic_scholar),
        ("OpenAlex", check_openalex),
    ]

    matches = []

    for source_name, checker in checkers:
        result.sources_checked.append(source_name)
        if verbose:
            print(f"  Checking {source_name} for '{entry.key}'...")

        match = checker(entry, verbose=verbose)
        if match:
            result.sources_found.append(source_name)
            matches.append(match)

            # Store best match
            sim = match.get("similarity", 1.0)
            if sim > result.best_match_similarity:
                result.best_match_similarity = sim
                result.best_match_title = match.get("title", "")

        # Rate limiting between APIs (Semantic Scholar needs ~1s between requests)
        time.sleep(1.0)

    # Compute confidence
    if len(result.sources_found) >= 2:
        result.status = "verified"
        result.confidence = min(0.95, 0.5 + 0.2 * len(result.sources_found))

        # Boost confidence if title similarity is high
        if result.best_match_similarity > 0.85:
            result.confidence = min(1.0, result.confidence + 0.1)

        # Check author overlap for best match
        if matches:
            best = max(matches, key=lambda m: m.get("similarity", 0))
            ao = author_overlap(entry.authors, best.get("authors", ""))
            if ao > 0.3:
                result.confidence = min(1.0, result.confidence + 0.1)
                result.notes.append(f"Author overlap: {ao:.0%}")
            elif ao == 0 and entry.authors:
                # Zero author overlap = likely chimeric (real title, wrong authors)
                result.notes.append("WARNING: No author overlap with best match")
                result.confidence -= 0.3
                result.red_flags.append(
                    "Title matches but authors don't — possible chimeric hallucination"
                )
                result.status = "suspicious"

    elif len(result.sources_found) == 1:
        result.status = "suspicious"
        result.confidence = 0.4 + (result.best_match_similarity * 0.2)
        result.notes.append("Found in only 1 source — verify manually")

    else:
        result.status = "not_found"
        result.confidence = 0.0
        result.notes.append("NOT FOUND in any database — likely hallucinated")

    # Red flags reduce confidence
    if result.red_flags:
        result.confidence = max(0.0, result.confidence - 0.1 * len(result.red_flags))

    return result


def verify_all(
    entries: list[BibEntry], verbose: bool = False
) -> list[VerificationResult]:
    """Verify all entries with progress reporting."""
    results = []
    total = len(entries)

    for i, entry in enumerate(entries, 1):
        if not verbose:
            print(f"  [{i}/{total}] Checking: {entry.key}", end="", flush=True)

        result = verify_entry(entry, verbose=verbose)

        if not verbose:
            status_icon = {
                "verified": " ✓",
                "suspicious": " ?",
                "not_found": " ✗",
                "error": " !",
            }
            print(status_icon.get(result.status, " ?"))

        results.append(result)

        # Rate limiting between entries
        time.sleep(1.0)

    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(results: list[VerificationResult]) -> None:
    """Print formatted verification report."""
    verified = [r for r in results if r.status == "verified"]
    suspicious = [r for r in results if r.status == "suspicious"]
    not_found = [r for r in results if r.status == "not_found"]
    with_flags = [r for r in results if r.red_flags]

    print("\n" + "=" * 65)
    print("  CITATION VERIFICATION REPORT")
    print("=" * 65)

    print(f"\n  Total citations: {len(results)}")
    print(f"  Verified (2+ sources): {len(verified)}")
    print(f"  Suspicious (1 source):  {len(suspicious)}")
    print(f"  NOT FOUND (0 sources):  {len(not_found)}")
    print(f"  With red flags:         {len(with_flags)}")

    if not_found:
        print(f"\n  {'='*60}")
        print("  CITATIONS NOT FOUND — LIKELY HALLUCINATED")
        print(f"  {'='*60}")
        for r in not_found:
            print(f"\n  [{r.entry.key}] {r.entry.file_path}:{r.entry.line_number}")
            print(f"    Title:   {r.entry.title}")
            print(f"    Authors: {r.entry.authors}")
            print(f"    Year:    {r.entry.year}")
            if r.red_flags:
                for flag in r.red_flags:
                    print(f"    FLAG: {flag}")

    if suspicious:
        print(f"\n  {'-'*60}")
        print("  SUSPICIOUS — FOUND IN ONLY 1 SOURCE (verify manually)")
        print(f"  {'-'*60}")
        for r in suspicious:
            print(f"\n  [{r.entry.key}] confidence={r.confidence:.0%}")
            print(f"    Title:      {r.entry.title}")
            print(f"    Best match: {r.best_match_title}")
            print(f"    Similarity: {r.best_match_similarity:.0%}")
            print(f"    Found in:   {', '.join(r.sources_found)}")
            for note in r.notes:
                print(f"    Note: {note}")
            if r.red_flags:
                for flag in r.red_flags:
                    print(f"    FLAG: {flag}")

    if with_flags and not not_found and not suspicious:
        print(f"\n  {'-'*60}")
        print("  RED FLAGS ON VERIFIED CITATIONS")
        print(f"  {'-'*60}")
        for r in with_flags:
            if r.status == "verified":
                print(f"\n  [{r.entry.key}]")
                for flag in r.red_flags:
                    print(f"    FLAG: {flag}")

    # Summary
    print("\n" + "=" * 65)
    if not_found:
        print(
            f"  RESULT: {len(not_found)} UNFOUND CITATION(S) — "
            "remove or replace before submission"
        )
    elif suspicious:
        print(
            f"  RESULT: {len(suspicious)} SUSPICIOUS — "
            "manually verify these citations"
        )
    else:
        print("  RESULT: All citations verified in 2+ sources")
    print("=" * 65 + "\n")


def json_report(results: list[VerificationResult]) -> str:
    """Generate JSON report."""
    output = {
        "summary": {
            "total": len(results),
            "verified": sum(1 for r in results if r.status == "verified"),
            "suspicious": sum(1 for r in results if r.status == "suspicious"),
            "not_found": sum(1 for r in results if r.status == "not_found"),
        },
        "citations": [],
    }
    for r in results:
        output["citations"].append(
            {
                "key": r.entry.key,
                "title": r.entry.title,
                "status": r.status,
                "confidence": round(r.confidence, 2),
                "sources_found": r.sources_found,
                "best_match_title": r.best_match_title,
                "best_match_similarity": round(r.best_match_similarity, 2),
                "red_flags": r.red_flags,
                "notes": r.notes,
            }
        )
    return json.dumps(output, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify academic citations against CrossRef, Semantic Scholar, and OpenAlex"
    )
    parser.add_argument(
        "path", help="Path to .bib file or directory containing .bib files"
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    target = Path(args.path)
    bib_files = []
    if target.is_file() and target.suffix == ".bib":
        bib_files = [target]
    elif target.is_dir():
        bib_files = sorted(target.rglob("*.bib"))
    else:
        print(f"Error: {target} is not a .bib file or directory", file=sys.stderr)
        sys.exit(1)

    if not bib_files:
        print(f"No .bib files found in {target}", file=sys.stderr)
        sys.exit(1)

    # Parse all entries
    all_entries = []
    for bib_file in bib_files:
        entries = parse_bib_file(bib_file)
        all_entries.extend(entries)
        if not args.json:
            print(f"Parsed {len(entries)} entries from {bib_file}")

    if not all_entries:
        print("No BibTeX entries found")
        sys.exit(0)

    if not args.json:
        print(f"\nVerifying {len(all_entries)} citations across 3 databases...\n")

    # Verify
    results = verify_all(all_entries, verbose=args.verbose)

    # Report
    if args.json:
        print(json_report(results))
    else:
        print_report(results)

    # Exit code: 1 if any not_found, 2 if suspicious only, 0 if all verified
    not_found = sum(1 for r in results if r.status == "not_found")
    suspicious = sum(1 for r in results if r.status == "suspicious")
    if not_found:
        sys.exit(1)
    elif suspicious:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
