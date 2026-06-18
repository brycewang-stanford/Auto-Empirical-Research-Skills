---
name: academic-paper-search
description: >-
  This skill should be used when the user asks to "search for academic papers",
  "find working papers on SSRN", "look up a DOI", "download paper PDF",
  "check open access availability", "search NBER papers", "find arXiv preprints",
  or "search CrossRef". Provides unified search, metadata retrieval,
  and PDF download across arXiv, NBER, SSRN, CrossRef, OpenAlex, Unpaywall,
  and Semantic Scholar. Covers economics, finance, social science, CS/AI,
  and all academic disciplines.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - Agent
---

# Academic Paper Search

A unified toolkit for discovering, retrieving metadata, and downloading academic papers
across all major sources. The right API depends on the task — this skill routes to the best source.

## Decision Tree: Which API to Use

```
What is needed?
│
├─ SEARCH for papers on a topic
│  ├─ arXiv preprints (CS/AI/Physics/Econ) ──→ arXiv API
│  ├─ NBER working papers (economics) ───────→ NBER API
│  ├─ SSRN working papers (social science) ──→ OpenAlex (primary) + CrossRef prefix:10.2139
│  ├─ Published journal articles ────────────→ CrossRef API or OpenAlex
│  └─ Broad multi-source search ─────────────→ OpenAlex API
│
├─ GET METADATA for a known paper
│  ├─ Have DOI ──→ CrossRef (structured) or OpenAlex (richer)
│  ├─ Have arXiv ID ──→ arXiv API
│  ├─ Have NBER number ──→ NBER API
│  └─ Have SSRN abstract ID ──→ OpenAlex DOI lookup (DOI = 10.2139/ssrn.{id})
│
├─ FIND/DOWNLOAD PDF
│  ├─ Have DOI ──→ Unpaywall API (check OA) → OpenAlex (alt PDF links)
│  ├─ arXiv paper ──→ Direct: https://arxiv.org/pdf/{id}
│  ├─ NBER paper ──→ Direct: https://www.nber.org/system/files/working_papers/w{n}/w{n}.pdf
│  └─ SSRN paper ──→ Unpaywall (~30%) or institutional repos (EconStor, IZA)
│
└─ IMPORT TO ZOTERO
   └─ Always use zotero_add_by_doi (best metadata + auto PDF via Unpaywall cascade)
```

---

## 1. OpenAlex API (Best All-Round)

Free, no API key needed. Covers 250M+ works including SSRN, NBER, arXiv, all journals.
Add `mailto=your@email.com` for polite pool (faster responses).

### Search by Source

```bash
# SSRN papers (source ID: S4210172589, NOT S4306400806 which is Europe PMC)
curl -s "https://api.openalex.org/works?filter=primary_location.source.id:S4210172589,default.search:social+preferences,publication_year:2024-2026&per_page=25&mailto=you@university.edu"

# NBER papers
curl -s "https://api.openalex.org/works?filter=primary_location.source.id:S4210174556,default.search:behavioral+economics&per_page=25&mailto=you@university.edu"
```

### Search by Topic (All Sources)

```bash
curl -s "https://api.openalex.org/works?search=network+formation+game+theory&filter=publication_year:2024-2026&per_page=25&sort=cited_by_count:desc&mailto=you@university.edu"
```

### DOI Lookup

```bash
curl -s "https://api.openalex.org/works/doi:10.2139/ssrn.4812743?mailto=you@university.edu"
```

### Python Pattern

```python
import requests

def openalex_search(query, source_id=None, year_from=2024, year_to=2026, per_page=25):
    """Search OpenAlex. source_id: S4210172589 (SSRN), S4210174556 (NBER), etc."""
    filters = [f"default.search:{query}", f"publication_year:{year_from}-{year_to}"]
    if source_id:
        filters.insert(0, f"primary_location.source.id:{source_id}")
    params = {
        "filter": ",".join(filters),
        "per_page": per_page,
        "mailto": "you@university.edu"
    }
    data = requests.get("https://api.openalex.org/works", params=params).json()
    results = []
    for w in data.get("results", []):
        pdf_urls = [loc["pdf_url"] for loc in w.get("locations", []) if loc.get("pdf_url")]
        results.append({
            "title": w["title"],
            "doi": w.get("doi", "").replace("https://doi.org/", ""),
            "year": w.get("publication_year"),
            "authors": [a["author"]["display_name"] for a in w.get("authorships", [])],
            "cited_by": w.get("cited_by_count", 0),
            "pdf_urls": pdf_urls,
            "landing_url": (w.get("primary_location") or {}).get("landing_page_url", ""),
        })
    return {"total": data.get("meta", {}).get("count", 0), "results": results}
```

### Key Source IDs

> **Full reference**: See `references/journal_identifiers.md` for a comprehensive table of 77 verified
> OpenAlex Source IDs and CrossRef ISSNs covering Top 5 economics, AEA journals, finance, management,
> marketing, accounting, IS, and 15+ field journal categories.

| Source | OpenAlex ID | CrossRef ISSN |
|--------|-------------|---------------|
| SSRN Electronic Journal | S4210172589 | 1556-5068 |
| NBER Working Papers | S2809516038 | N/A |
| American Economic Review | S23254222 | 0002-8282 |
| Quarterly Journal of Economics | S203860005 | 0033-5533 |
| Econometrica | S95464858 | 0012-9682 |

**Warning**: OpenAlex source IDs are opaque and not guessable. Always verify
via `https://api.openalex.org/sources?search=journal+name` before using a new ID.
For verified IDs of 77 journals, consult `references/journal_identifiers.md`.

### PDF from OpenAlex

`primary_location.pdf_url` is null for SSRN papers (Elsevier blocks it).
Check `locations[].pdf_url` for third-party repos — ~24% of SSRN papers have PDFs
via EconStor, IZA, MPRA, etc. These are real, downloadable PDFs.

---

## 2. CrossRef API (Best for DOI Metadata)

Free, no key needed. Add `mailto=` for 50 req/sec (vs 1 req/sec without).

### Search with SSRN DOI Prefix

```bash
# All SSRN papers matching a query
curl -s "https://api.crossref.org/works?query=%22social+preferences%22&filter=prefix:10.2139,from-pub-date:2024-01-01&rows=25&sort=relevance&mailto=you@university.edu"
```

### Search within a Journal

```bash
# See references/journal_identifiers.md for 77 verified ISSNs
# AER: 0002-8282, QJE: 0033-5533, JPE: 0022-3808, Econometrica: 0012-9682, REStud: 0034-6527
curl -s "https://api.crossref.org/journals/0002-8282/works?query=auction+mechanism&rows=10&mailto=you@university.edu"
```

### DOI Lookup

```bash
curl -s "https://api.crossref.org/works/10.1257/aer.20171330?mailto=you@university.edu"
```

### DOI Construction Rules

| Source | DOI Format | Example |
|--------|-----------|---------|
| SSRN | `10.2139/ssrn.{abstract_id}` | 10.2139/ssrn.4812743 |
| NBER | `10.3386/w{number}` | 10.3386/w34297 |

These predictable DOI formats allow constructing DOIs from paper IDs
without making extra API calls.

### Limitations

CrossRef returns title, authors, DOI, date, journal — but **no abstracts** for SSRN papers
(Elsevier doesn't submit them to CrossRef). Use OpenAlex for richer metadata.

---

## 3. arXiv API (Preprints — CS/AI/Physics/Math/Econ)

Free, no key needed. Returns Atom XML. Rate limit: ~1 request per 3 seconds.

```bash
curl -s "https://export.arxiv.org/api/query?search_query=abs:social+preferences+AND+(cat:econ.TH+OR+cat:econ.GN)&max_results=20&sortBy=submittedDate&sortOrder=descending"
```

### Search Prefixes

`all:` (full text), `ti:` (title), `au:` (author), `abs:` (abstract), `cat:` (category).
Boolean: `AND`, `OR`, `ANDNOT`. Exact phrase: `%22social+preferences%22`.

### Economics Categories

`econ.TH` (Theory), `econ.GN` (General), `econ.EM` (Econometrics).

**Caveat**: The `cat:` filter in `search_query` does not always reliably restrict results
to specified categories — arXiv may still return papers from other fields.
Verify category matches in results and filter client-side if needed.

### Direct PDF

```
https://arxiv.org/pdf/{id}          # e.g. https://arxiv.org/pdf/2401.12345
https://arxiv.org/abs/{id}          # abstract page
```

---

## 4. NBER API (Economics Working Papers)

Free, no key needed. Returns JSON.

```bash
# Search
curl -s "https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=20&q=social+preferences"

# Filter by Program (replace _/_ with programs/{name})
curl -s "https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/programs/Labor+Studies/search?page=1&perPage=20&q=minimum+wage"

# New this week
curl -s "https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=20&newThisWeek=true"
```

### Programs

Labor Studies, Economic Fluctuations and Growth, Industrial Organization,
Public Economics, Development Economics, International Finance and Macroeconomics,
Corporate Finance, Asset Pricing, Health Economics, etc.

### Response Processing

Authors field contains HTML `<a>` tags — strip with: `re.sub(r'<[^>]+>', '', text)`

No built-in date filter — API sorts by relevance. Filter client-side by `displaydate`.

### Direct PDF

```
https://www.nber.org/system/files/working_papers/w{number}/w{number}.pdf
```

---

## 5. Unpaywall API (Open Access PDF Finder)

Free, no key needed. Email as query param. 100,000 requests/day.

```bash
curl -s "https://api.unpaywall.org/v2/10.2139/ssrn.4812743?email=you@university.edu" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'OA: {d[\"is_oa\"]} ({d[\"oa_status\"]})')
pdf = (d.get('best_oa_location') or {}).get('url_for_pdf')
print(f'PDF: {pdf or \"none\"}')
# Check all locations for alternative PDFs
for loc in d.get('oa_locations', []):
    if loc.get('url_for_pdf'):
        print(f'Alt PDF: {loc[\"url_for_pdf\"]} ({loc[\"host_type\"]})')
"
```

### OA Status Values

| Status | Meaning |
|--------|---------|
| `gold` | Published OA by publisher |
| `green` | Free copy in a repository |
| `hybrid` | OA article in subscription journal |
| `bronze` | Free to read on publisher site |
| `closed` | No free version found |

### Platform-Specific PDF Availability

| Source | Unpaywall PDF Rate | Why |
|--------|-------------------|-----|
| arXiv | ~100% | Native OA, direct PDF links |
| NBER | ~97% | Green OA via author/institution repos |
| SSRN | ~30% | Cloudflare blocks Unpaywall; only finds institutional repo mirrors |

For SSRN papers where Unpaywall returns `url_for_pdf=null`, check `oa_locations[]`
for institutional repositories (EconStor, university repos) — follow their landing pages
to find PDF links.

---

## 6. Semantic Scholar API (Citations & Impact)

Free, no key needed. Rate limit: 100 requests per 5 minutes.
**Warning**: As of 2026, Semantic Scholar may return 429 errors frequently.
Consider registering for an API key at https://www.semanticscholar.org/product/api
for higher limits. Add header: `x-api-key: YOUR_KEY`.

```bash
# Search
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=social+preferences+experiment&fields=title,year,authors,citationCount,externalIds,venue&limit=20&year=2024-2026"

# DOI lookup
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1257/aer.20171330?fields=title,year,authors,citationCount,abstract"
```

### Field of Study Filter

`fieldsOfStudy=Economics,Sociology,Political+Science,Business,Psychology`

Warning: The `Economics` filter is very strict and may return 0 results.
Often better to search without it and filter manually.

### When to Use

Best for: citation counts, finding related papers, author impact metrics.
Not best for: SSRN-specific search (poor coverage), bulk downloading.

---

## 7. Tavily Search (Fallback for Any Source)

When APIs do not cover the need, Tavily can search any academic site.
Particularly useful for SSRN (no public API) and as a fallback for any source.

```python
# Via MCP tool
mcp__tavily__tavily-search({
    "query": 'site:ssrn.com "social preferences" economics 2024 2025',
    "search_depth": "advanced",
    "max_results": 20,
    "include_domains": ["ssrn.com", "papers.ssrn.com"]
})

# Also works for NBER, RePEc, etc.
mcp__tavily__tavily-search({
    "query": 'site:nber.org "network formation" working paper',
    "include_domains": ["nber.org"]
})
```

---

## Recommended Workflows

### Workflow A: Comprehensive Topic Search

For finding all recent papers on a topic across multiple sources:

```
1. OpenAlex: broad search (all sources, richest metadata)
2. CrossRef prefix:10.2139: catch SSRN papers OpenAlex might miss
3. NBER API: NBER-specific search with program filtering
4. arXiv API: preprints in CS/AI/Physics/Econ
5. Tavily: sweep for anything the APIs missed
6. Deduplicate by DOI
```

### Workflow B: SSRN Paper Search

SSRN has no public API. Use this cascade:

```
1. OpenAlex (filter: source.id:S4210172589) — best: 1 API call, rich metadata
2. CrossRef (filter: prefix:10.2139) — backup: structured DOI search
3. Tavily (include_domains: ssrn.com) — catches papers not yet in OpenAlex/CrossRef
```

### Workflow C: PDF Download Pipeline

Try sources in this order (most reliable first):

```
1. arXiv direct: https://arxiv.org/pdf/{id}
2. NBER direct: https://www.nber.org/system/files/working_papers/w{n}/w{n}.pdf
3. Unpaywall: check best_oa_location.url_for_pdf via DOI
4. OpenAlex: check locations[].pdf_url for third-party repo PDFs
5. Institutional repos: follow Unpaywall oa_locations landing pages
6. SSRN direct: construct Delivery.cfm URL (may be Cloudflare-blocked)
```

### Workflow D: Zotero Import

Always prefer `zotero_add_by_doi` over `zotero_add_by_url`:
- Better metadata (correct entry types, complete fields)
- Higher PDF download success (Zotero uses Unpaywall → arXiv → S2 → PMC cascade)
- DOI can be constructed for SSRN (`10.2139/ssrn.{id}`) and NBER (`10.3386/w{number}`)

---

## Rate Limits & Best Practices

| API | Rate Limit | Best Practice |
|-----|-----------|---------------|
| OpenAlex | 10 req/sec (polite pool) | Add `mailto=` parameter |
| CrossRef | 50 req/sec with `mailto=`, 1/sec without | Always add `mailto=` |
| Unpaywall | 100K/day | Burst OK, no throttling needed |
| arXiv | ~1 req/3sec | Add `time.sleep(3)` between requests |
| NBER | No documented limit | Be polite, ~1 req/sec |
| Semantic Scholar | 100 req/5min | Add `time.sleep(3)` or use API key for higher limit |
| Tavily | Per plan | Use `search_depth: "basic"` when possible |
