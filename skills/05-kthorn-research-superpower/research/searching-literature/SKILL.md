---
name: Searching Scientific Literature
description: PubMed search with keyword optimization, result parsing, and metadata extraction
when_to_use: When starting literature search. When user asks about papers, publications, studies. When need to find scientific articles. When building initial paper list for research question.
version: 1.0.0
---

<!--
  ╔══════════════════════════════════════════════════════════════╗
  ║  本文件为开源 Skill 原始文档，收录仅供学习与研究参考        ║
  ║  CoPaper.AI 收集整理 | https://copaper.ai                  ║
  ╚══════════════════════════════════════════════════════════════╝

  来源仓库: https://github.com/kthorn/research-superpower
  项目名称: research-superpower
  开源协议: MIT License
  收录日期: 2026-04-02

  声明: 本文件版权归原作者所有。此处收录旨在为社会科学实证研究者
  提供 AI Agent Skills 的集中参考。如有侵权，请联系删除。
-->

# Searching Scientific Literature

## Overview

Search PubMed for scientific literature using optimized queries. Extract metadata and prepare papers for relevance evaluation.

**Core principle:** Cast a wide enough net to find relevant papers, but use targeted keywords to keep results manageable.

## When to Use

Use this skill when:
- Starting a new research question
- User asks "find papers about..."
- Need initial paper set for evaluation
- Searching for specific methods, compounds, diseases, techniques

## Search Strategy

### 1. Parse User Query

Extract:
- **Keywords**: Main concepts (e.g., "BTK inhibitor", "selectivity", "kinase")
- **Data types**: What user needs (IC50 values, methods, structures, results)
- **Constraints**: Date ranges, specific journals, author names
- **Synonyms**: Alternative terms (e.g., "Bruton's tyrosine kinase" = "BTK")

### 2. Construct PubMed Query

**Boolean operators:**
- AND - narrow results (must have both terms)
- OR - broaden results (either term)
- NOT - exclude terms

**Example queries:**
```
"BTK inhibitor"[Title/Abstract] AND selectivity[Title/Abstract]

("kinase inhibitor" OR "protein kinase") AND (selectivity OR "off-target")

"ibrutinib"[Title/Abstract] AND ("IC50" OR "inhibitory concentration")
```

**Field tags:**
- `[Title/Abstract]` - search title and abstract only
- `[Title]` - title only (more precise)
- `[Author]` - specific author
- `[Journal]` - specific journal
- `[Date]` - date range

### 3. Execute Search

**API endpoint:**
```bash
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?\
db=pubmed&\
term=YOUR_QUERY&\
retmax=100&\
retmode=json&\
sort=relevance
```

**Parameters:**
- `db=pubmed` - search PubMed database
- `term=` - your query (URL encode spaces and special chars)
- `retmax=100` - max results (start with 100)
- `retmode=json` - return JSON
- `sort=relevance` - most relevant first (or `pub_date` for newest)

**Example bash:**
```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=BTK+inhibitor+selectivity&retmax=100&retmode=json&sort=relevance"
```

**Response format:**
```json
{
  "esearchresult": {
    "count": "156",
    "retmax": "100",
    "idlist": ["12345678", "87654321", ...]
  }
}
```

### 4. Fetch Paper Metadata

**API endpoint:**
```bash
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?\
db=pubmed&\
id=12345678,87654321&\
retmode=json
```

**Extract from response:**
- Title
- Authors (list)
- Journal name
- Publication date
- Abstract (via separate efetch call or use esummary)
- PMID
- DOI (if available in `articleids`)

**Getting DOI from PMID:**
```json
"articleids": [
  {"idtype": "pubmed", "value": "12345678"},
  {"idtype": "doi", "value": "10.1234/example.2023"}
]
```

**If DOI missing:**
- Use PMID as fallback identifier
- Try to resolve DOI via PubMed Central or publisher APIs later

## Output Format

Create list of paper objects:

```json
[
  {
    "pmid": "12345678",
    "doi": "10.1234/example.2023",
    "title": "Selective BTK inhibitors for autoimmune diseases",
    "authors": ["Smith J", "Doe A", "Johnson B"],
    "journal": "Nature Chemical Biology",
    "year": "2023",
    "abstract": "We developed a series of...",
    "source": "pubmed_search"
  }
]
```

## Error Handling

**Rate limits (CRITICAL - shared across all processes/subagents):**
- No API key: 3 requests/second (official limit)
- With API key: 10 requests/second
- **Single agent/script:** Use 500ms delays (2 req/sec, safe margin)
  - 350ms is theoretically sufficient but causes ~20% HTTP 429 errors in practice
- **Multiple parallel subagents:** Use longer delays to share capacity
  - 2 parallel: 1 second each (2 total req/sec)
  - 3 parallel: 1.5 seconds each (2 total req/sec)
  - 5 parallel: 2.5 seconds each (2 total req/sec)
  - Formula: `delay_seconds = (num_parallel / rate_limit) + safety_margin`
- **If you get HTTP 429 errors:** Wait 5 seconds, resume with doubled delays

**Empty results:**
- Try broader terms
- Remove field tags
- Check for typos
- Use OR to add synonyms

**Too many results (>500):**
- Add more specific terms
- Use field tags to narrow
- Add date constraints
- Consider splitting into sub-queries

## Integration with Other Skills

After search completes:
1. **Save results** to research folder as `initial-search-results.json`
2. **For each paper**, call `evaluating-paper-relevance` skill
3. **Track in** `papers-reviewed.json` (use DOI as key, fallback to PMID)

## Quick Reference

| Task | Command |
|------|---------|
| Search PubMed | `curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=QUERY&retmax=100&retmode=json"` |
| Get metadata | `curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=PMID1,PMID2&retmode=json"` |
| URL encode query | Replace spaces with `+`, special chars with `%XX` |
| Narrow results | Use AND, add field tags, more specific terms |
| Broaden results | Use OR, remove field tags, add synonyms |

## Common Mistakes

**Too narrow:** Only 5 results → Use OR, remove constraints
**Too broad:** 5000 results → Add AND terms, use field tags
**Missing abstracts:** Use efetch instead of esummary for full abstract text
**DOI not found:** Many older papers lack DOI - use PMID as fallback
**Rate limiting:** Add 500ms delays (single agent) or longer (parallel subagents sharing rate limit)

## Next Steps

After completing search:
- Announce: "Found N papers matching query"
- Begin evaluation using `skills/research/evaluating-paper-relevance`
- Update user with progress as papers are screened
