#!/usr/bin/env python3
"""
fetch_papers.py - 从经济金融顶刊抓取最新论文
支持RSS和网页抓取两种模式，带去重机制
"""

import argparse
import json
import hashlib
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

try:
    import feedparser
except ImportError:
    print("ERROR: feedparser not installed. Run: pip install feedparser", file=sys.stderr)
    sys.exit(1)

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)


def paper_id(title: str, doi: str = None) -> str:
    """Generate a dedup key from title (normalized) + DOI."""
    norm = title.strip().lower()
    norm = "".join(c for c in norm if c.isalnum() or c == " ")
    norm = " ".join(norm.split())
    if doi:
        return hashlib.md5(f"{norm}|{doi}".encode()).hexdigest()
    return hashlib.md5(norm.encode()).hexdigest()


def load_history(path: str) -> set:
    """Load previously fetched paper IDs."""
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {p.get("id", "") for p in data.get("papers", [])}


def save_history(path: str, new_papers: list, digest_file: str):
    """Append new papers to history file."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"papers": []}

    today = datetime.now().strftime("%Y-%m-%d")
    for p in new_papers:
        data["papers"].append({
            "id": p["id"],
            "title": p["title"],
            "doi": p.get("doi", ""),
            "journal": p["journal"],
            "date_fetched": today,
            "digest_file": digest_file,
        })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Patterns that indicate non-article entries (editorials, front/back matter, etc.)
SKIP_PATTERNS = [
    "frontmatter", "backmatter", "front matter", "back matter",
    "table of contents", "editorial board", "editor's note",
    "election of fellows", "corrigendum", "erratum", "errata",
    "acknowledgment of referees", "referee acknowledgment",
    "volume information", "issue information",
    "forthcoming papers", "books received",
    "turnaround times", "recent referees", "referees for",
    "announcements", "in memoriam", "obituary",
    "letter from the editor", "presidential address",
]


def is_real_article(title: str) -> bool:
    """Filter out non-article entries like front/back matter."""
    t = title.strip().lower()
    return not any(pat in t for pat in SKIP_PATTERNS)


def fetch_rss(journal: dict, cutoff_date: datetime) -> list:
    """Fetch papers from an RSS feed."""
    url = journal.get("rss_url")
    if not url:
        return []

    papers = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6])

            if pub_date and pub_date < cutoff_date:
                continue

            title = entry.get("title", "").strip()
            if not title or not is_real_article(title):
                continue

            doi = ""
            link = entry.get("link", "")
            if "doi.org/" in link:
                doi = link.split("doi.org/")[-1]
            elif hasattr(entry, "prism_doi"):
                doi = entry.prism_doi

            abstract = ""
            if hasattr(entry, "summary"):
                abstract = entry.summary
            elif hasattr(entry, "description"):
                abstract = entry.description

            authors = ""
            if hasattr(entry, "authors"):
                authors = ", ".join(a.get("name", "") for a in entry.authors)
            elif hasattr(entry, "author"):
                authors = entry.author

            papers.append({
                "id": paper_id(title, doi),
                "title": title,
                "doi": doi,
                "authors": authors,
                "abstract": abstract,
                "journal": journal["name"],
                "journal_abbr": journal["abbr"],
                "category": journal["category"],
                "rank": journal["rank"],
                "link": link,
                "pub_date": pub_date.strftime("%Y-%m-%d") if pub_date else "",
                "source": "rss",
            })
    except Exception as e:
        print(f"  WARNING: RSS fetch failed for {journal['name']}: {e}", file=sys.stderr)

    return papers


def fetch_web(journal: dict, cutoff_date: datetime) -> list:
    """Placeholder for web scraping fallback. Returns empty list.
    The actual web scraping should be done by Claude using WebFetch tool,
    as each publisher has different page structures.
    """
    return []


def fetch_crossref(journal: dict, cutoff_date: datetime) -> list:
    """Fetch papers via Crossref API. Works for journals without RSS
    and as a supplement to get abstracts/authors for RSS-fetched papers."""
    issn = journal.get("issn", "")
    if not issn:
        return []

    # Clean ISSN - use print ISSN format for Crossref
    issn = issn.strip()
    from_date = cutoff_date.strftime("%Y-%m-%d")
    url = (
        f"https://api.crossref.org/works?"
        f"filter=issn:{issn},from-pub-date:{from_date}"
        f"&rows=50&select=DOI,title,author,abstract,container-title,published-print,published-online"
    )

    papers = []
    try:
        headers = {"User-Agent": "JournalDigest/1.0 (mailto:research@example.com)"}
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code != 200:
            return []

        data = resp.json()
        for item in data.get("message", {}).get("items", []):
            title = item.get("title", [""])[0].strip()
            if not title or not is_real_article(title):
                continue

            doi = item.get("DOI", "")
            authors = ", ".join(
                f"{a.get('given', '')} {a.get('family', '')}".strip()
                for a in item.get("author", [])
            )

            abstract = item.get("abstract", "")
            # Clean JATS XML tags from abstract
            import re
            abstract = re.sub(r"<[^>]+>", "", abstract).strip()

            pub_date = None
            for date_field in ("published-print", "published-online"):
                if date_field in item:
                    parts = item[date_field].get("date-parts", [[]])[0]
                    if len(parts) >= 3:
                        pub_date = datetime(parts[0], parts[1], parts[2])
                    elif len(parts) >= 2:
                        pub_date = datetime(parts[0], parts[1], 1)
                    elif len(parts) >= 1:
                        pub_date = datetime(parts[0], 1, 1)
                    break

            papers.append({
                "id": paper_id(title, doi),
                "title": title,
                "doi": doi,
                "authors": authors,
                "abstract": abstract,
                "journal": journal["name"],
                "journal_abbr": journal["abbr"],
                "category": journal["category"],
                "rank": journal["rank"],
                "link": f"https://doi.org/{doi}" if doi else "",
                "pub_date": pub_date.strftime("%Y-%m-%d") if pub_date else "",
                "source": "crossref",
            })
    except Exception as e:
        print(f"  WARNING: Crossref fetch failed for {journal['name']}: {e}", file=sys.stderr)

    return papers


def main():
    parser = argparse.ArgumentParser(description="Fetch papers from top journals")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back")
    parser.add_argument("--output", type=str, required=True, help="Output JSON path")
    parser.add_argument("--history", type=str, required=True, help="History JSON path")
    parser.add_argument("--journals", type=str, default=None, help="Path to journals.json")
    parser.add_argument("--enrich", action="store_true", help="Use Crossref to enrich abstracts for RSS papers")
    args = parser.parse_args()

    # Locate journals.json
    if args.journals:
        journals_path = args.journals
    else:
        script_dir = Path(__file__).parent.parent
        journals_path = script_dir / "references" / "journals.json"

    with open(journals_path, "r", encoding="utf-8") as f:
        journals_data = json.load(f)

    cutoff_date = datetime.now() - timedelta(days=args.days)
    history_ids = load_history(args.history)

    all_papers = []
    rss_failed = []
    web_needed = []

    print(f"Fetching papers from {len(journals_data['journals'])} journals...")
    print(f"Cutoff date: {cutoff_date.strftime('%Y-%m-%d')}")
    print(f"History contains {len(history_ids)} previously fetched papers")
    print()

    for journal in journals_data["journals"]:
        name = journal["name"]
        print(f"  [{journal['rank']}] {name}...", end=" ")

        if journal.get("rss_url"):
            papers = fetch_rss(journal, cutoff_date)
            new_papers = [p for p in papers if p["id"] not in history_ids]
            print(f"RSS: {len(papers)} found, {len(new_papers)} new")
            all_papers.extend(new_papers)
        else:
            # Try Crossref API as fallback
            papers = fetch_crossref(journal, cutoff_date)
            new_papers = [p for p in papers if p["id"] not in history_ids]
            if new_papers:
                print(f"Crossref: {len(papers)} found, {len(new_papers)} new")
                all_papers.extend(new_papers)
            else:
                print("No RSS, Crossref returned 0 - needs web scraping")
                web_needed.append(journal)

    # Enrich RSS papers with Crossref abstracts if requested
    if args.enrich:
        import re
        papers_needing_abstract = [p for p in all_papers if not p.get("abstract") or len(p["abstract"]) < 50]
        if papers_needing_abstract:
            print(f"\nEnriching {len(papers_needing_abstract)} papers via Crossref...")
            # Group by DOI for batch lookup
            for p in papers_needing_abstract:
                if not p.get("doi"):
                    continue
                try:
                    url = f"https://api.crossref.org/works/{p['doi']}"
                    headers = {"User-Agent": "JournalDigest/1.0 (mailto:research@example.com)"}
                    resp = requests.get(url, headers=headers, timeout=15)
                    if resp.status_code == 200:
                        item = resp.json().get("message", {})
                        abstract = item.get("abstract", "")
                        abstract = re.sub(r"<[^>]+>", "", abstract).strip()
                        if abstract:
                            p["abstract"] = abstract
                        if not p.get("authors") and item.get("author"):
                            p["authors"] = ", ".join(
                                f"{a.get('given', '')} {a.get('family', '')}".strip()
                                for a in item["author"]
                            )
                except Exception:
                    pass
            print("  Enrichment complete.")

    # Sort by rank priority then journal name
    rank_order = {"A+": 0, "A": 1, "A-": 2, "B+": 3}
    all_papers.sort(key=lambda p: (rank_order.get(p["rank"], 9), p["journal"]))

    result = {
        "fetch_date": datetime.now().strftime("%Y-%m-%d"),
        "cutoff_date": cutoff_date.strftime("%Y-%m-%d"),
        "total_candidates": len(all_papers),
        "papers": all_papers,
        "web_scraping_needed": [j["name"] for j in web_needed],
        "rss_failed": rss_failed,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nDone. {len(all_papers)} new papers saved to {args.output}")
    if web_needed:
        print(f"{len(web_needed)} journals need web scraping: {', '.join(j['name'] for j in web_needed)}")


if __name__ == "__main__":
    main()
