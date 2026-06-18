---
name: nber-working-papers-api
description: "Access NBER working papers and economic research datasets"
metadata:
  openclaw:
    emoji: "📈"
    category: "domains"
    subcategory: "economics"
    keywords: ["NBER", "working papers", "economics research", "macroeconomics", "economic policy", "recession dating"]
    source: "https://www.nber.org/"
---

# NBER Working Papers and Data API

## Overview

The National Bureau of Economic Research (NBER) is the leading U.S. economics research organization, publishing 1,200+ working papers annually by top economists. NBER papers are among the most cited in economics. The website provides structured JSON API access to working papers and macroeconomic datasets. Free metadata access; some full text requires subscription.

> **API last verified**: 2026-04-23. RSS feeds (`/papers.rss`) and the old query-param API (`?q=...` without `/search` path) are defunct. Use the endpoints below.

## Working Papers Search API

Base URL: `https://www.nber.org/api/v1/working_page_listing/contentType/working_paper`

### Search all papers

```bash
# Search working papers (returns JSON)
curl "https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=20&q=inflation+expectations"

# Get new-this-week papers (omit q for all recent)
curl "https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=20&newThisWeek=true"

# Find a specific paper by number
curl "https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=1&q=w33000"
```

### Filter by program (path segment)

Program names go in the URL path (use `+` for spaces), replacing the two `_/_` placeholders:

```bash
# Labor Studies papers
curl "https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/programs/Labor+Studies/search?page=1&perPage=20"

# Labor Studies + keyword search
curl "https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/programs/Labor+Studies/search?page=1&perPage=20&q=minimum+wage"

# Economic Fluctuations and Growth
curl "https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/programs/Economic+Fluctuations+and+Growth/search?page=1&perPage=20"
```

### API Response Structure

```json
{
  "totalResults": 11711,
  "results": [
    {
      "title": "Paper Title",
      "authors": ["<a href=\"/people/john_doe\">John Doe</a>"],
      "displaydate": "March 2025",
      "abstract": "First ~300 chars of abstract...",
      "url": "/papers/w33000",
      "nid": "767372",
      "type": "working_paper",
      "displaytypename": "Working Paper",
      "newthisweek": false,
      "certifiedrandom": false
    }
  ],
  "facets": [
    {"id": "authorNames", "label": "Author & Editor", ...},
    {"id": "programs", "label": "Programs", ...},
    {"id": "topics", "label": "Topics", ...},
    {"id": "groups", "label": "Working Groups", ...}
  ]
}
```

**Note on `authors` field**: Values contain HTML anchor tags. Strip tags to get plain names:
```python
import re
plain = re.sub(r'<[^>]+>', '', author_html)
```

### Individual Paper Metadata (HTML meta tags)

For richer metadata on a single paper, parse `<meta>` tags from the paper page:

```bash
curl -sL "https://www.nber.org/papers/w33000" | grep 'citation_'
# citation_title, citation_author, citation_doi, citation_publication_date,
# citation_technical_report_number, citation_pdf_url
```

## NBER Data Portal

```bash
# Business cycle dates (JSON, works directly)
curl "https://data.nber.org/data/cycles/business_cycle_dates.json"
# Returns: [{"peak": "2020-02-01", "trough": "2020-04-01"}, ...]

# CPS labor data extracts: https://data.nber.org/cps/
# Macrohistory database: https://data.nber.org/
```

## NBER Programs (full names for API path)

| Program Name (use in API path) | Focus |
|:-------------------------------|:------|
| `Economic Fluctuations and Growth` | Macro, business cycles |
| `Labor Studies` | Employment, wages |
| `Industrial Organization` | Markets, competition |
| `Public Economics` | Taxation, spending |
| `Economics of Health` | Healthcare markets |
| `Development Economics` | Developing countries |
| `International Finance and Macroeconomics` | Exchange rates, capital flows |
| `International Trade and Investment` | Trade policy |
| `Monetary Economics` | Central banking |
| `Corporate Finance` | Firm finance |
| `Asset Pricing` | Financial markets |
| `Economics of Education` | Education economics |
| `Economics of Aging` | Demographics |
| `Children and Families` | Child welfare |
| `Law and Economics` | Legal institutions |
| `Environment and Energy Economics` | Environmental policy |
| `Political Economy` | Political institutions |

## Python Usage

```python
import re
import requests


SEARCH_BASE = (
    "https://www.nber.org/api/v1/working_page_listing"
    "/contentType/working_paper"
)


def _strip_html(text: str) -> str:
    """Remove HTML tags from a string."""
    return re.sub(r'<[^>]+>', '', text)


def _extract_paper_number(url: str) -> str:
    """Extract paper number from URL like /papers/w33000."""
    return url.rsplit("/", 1)[-1] if url else ""


def search_papers(query: str = "", program: str = "",
                  page: int = 1, per_page: int = 20,
                  new_this_week: bool = False) -> dict:
    """Search NBER working papers.

    Args:
        query: Search keywords (optional).
        program: Full program name, e.g. "Labor Studies" (optional).
        page: Page number (1-indexed).
        per_page: Results per page (max ~100).
        new_this_week: If True, return only new-this-week papers.

    Returns:
        Dict with 'total' count and 'papers' list.
    """
    if program:
        url = f"{SEARCH_BASE}/programs/{program}/search"
    else:
        url = f"{SEARCH_BASE}/_/_/search"

    params = {"page": page, "perPage": per_page}
    if query:
        params["q"] = query
    if new_this_week:
        params["newThisWeek"] = "true"

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    papers = []
    for item in data.get("results", []):
        number = _extract_paper_number(item.get("url", ""))
        papers.append({
            "title": item.get("title", ""),
            "authors": [_strip_html(a) for a in item.get("authors", [])],
            "number": number,
            "date": item.get("displaydate", ""),
            "url": f"https://www.nber.org{item['url']}" if item.get("url") else "",
            "pdf_url": f"https://www.nber.org/system/files/working_papers/{number}/{number}.pdf" if number else "",
            "abstract": item.get("abstract", ""),
            "new_this_week": item.get("newthisweek", False),
        })
    return {"total": data.get("totalResults", 0), "papers": papers}


def get_paper_metadata(paper_number: str) -> dict:
    """Get metadata for a specific paper (e.g. 'w33000') via citation meta tags."""
    resp = requests.get(
        f"https://www.nber.org/papers/{paper_number}", timeout=30
    )
    resp.raise_for_status()

    meta = {}
    for match in re.finditer(
        r'<meta\s+name="citation_(\w+)"\s+content="([^"]*)"', resp.text
    ):
        key, val = match.group(1), match.group(2)
        if key == "author":
            meta.setdefault("authors", []).append(val)
        else:
            meta[key] = val
    return meta


def get_business_cycle_dates() -> list:
    """Get NBER official business cycle dates."""
    resp = requests.get(
        "https://data.nber.org/data/cycles/business_cycle_dates.json",
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


# === Examples ===

# Search for AI economics papers
results = search_papers("artificial intelligence labor market")
print(f"Found {results['total']} papers")
for p in results["papers"][:3]:
    print(f"[{p['number']}] {p['title']} ({p['date']})")
    print(f"  Authors: {', '.join(p['authors'])}")

# New papers this week
new = search_papers(new_this_week=True, per_page=5)
for p in new["papers"]:
    print(f"[NEW] {p['title']}")

# Papers in a specific program
labor = search_papers(query="minimum wage", program="Labor Studies", per_page=5)
for p in labor["papers"]:
    print(f"[{p['number']}] {p['title']}")

# Get detailed metadata for a specific paper
meta = get_paper_metadata("w33000")
print(f"Title: {meta.get('title')}")
print(f"DOI: {meta.get('doi')}")
print(f"PDF: {meta.get('pdf_url', 'N/A')}")

# Recession dates
cycles = get_business_cycle_dates()
for c in cycles[-3:]:
    print(f"Peak: {c.get('peak')} → Trough: {c.get('trough')}")
```

## Key Datasets

| Dataset | Description |
|---------|-------------|
| Business Cycle Dates | Official US recession start/end dates |
| CPS Extracts | Current Population Survey labor data |
| Macrohistory Database | 150 years of macro indicators |
| Patent Data | Patent citation and classification |
| Trade Data | Bilateral trade statistics |

## References

- [NBER](https://www.nber.org/)
- [NBER Working Papers](https://www.nber.org/papers)
- [NBER Data](https://data.nber.org/)
- [NBER Programs](https://www.nber.org/programs-projects/programs-working-groups)
