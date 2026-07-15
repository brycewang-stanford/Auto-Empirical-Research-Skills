---
name: Traversing Citation Networks
description: Smart backward and forward citation following via Semantic Scholar, with relevance filtering and deduplication
when_to_use: After finding relevant paper. When need to find related work. When following references or citations. When building citation graph. When exploring paper connections.
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

# Traversing Citation Networks

## Overview

Intelligently follow citations backward (references) and forward (citing papers) using Semantic Scholar API.

**Core principle:** Only follow citations relevant to user's query. Avoid exponential explosion by filtering before traversing.

## When to Use

Use this skill when:
- Found a highly relevant paper (score ≥ 7)
- Need to find related work
- User asks "what papers cite this?"
- Building comprehensive understanding of a topic

**When NOT to use:**
- Paper scored < 7 (not relevant enough to follow)
- Already at 50 papers (check with user first)
- Citations look off-topic from abstract

## Citation Traversal Strategy

### 1. Get Paper ID from Semantic Scholar

**Lookup by DOI:**
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1234/example.2023?fields=paperId,title,year"
```

**Response:**
```json
{
  "paperId": "abc123def456",
  "title": "Paper Title",
  "year": 2023
}
```

**Save paperId** - needed for citations/references queries

### 2. Backward Traversal (References)

**Get references from paper:**
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/abc123def456/references?fields=contexts,intents,title,year,abstract,externalIds&limit=100"
```

**Response format:**
```json
{
  "data": [
    {
      "citedPaper": {
        "paperId": "xyz789",
        "title": "Referenced Paper Title",
        "year": 2020,
        "abstract": "...",
        "externalIds": {
          "DOI": "10.5678/referenced.2020",
          "PubMed": "87654321"
        }
      },
      "contexts": [
        "...as described in previous work [15]...",
        "...we used the method from [15] to..."
      ],
      "intents": ["methodology", "background"]
    }
  ]
}
```

**Filter for relevance:**

For each reference, check:
1. **Context keywords**: Do citation contexts mention user's query terms?
   - Example: If user asks about "IC50 values", look for contexts mentioning "IC50", "activity", "potency"
2. **Title match**: Does title contain relevant keywords?
3. **Intent**: Is intent "methodology" or "result" (more relevant) vs "background" (less relevant)?

**Scoring:**
- Context keywords match: +3 points
- Title keywords match: +2 points
- Intent is methodology/result: +2 points
- Recent (< 5 years old): +1 point

**Only add to queue if score ≥ 5**

### 3. Forward Traversal (Citations)

**Get papers citing this one:**
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/abc123def456/citations?fields=title,year,abstract,externalIds&limit=100"
```

**Response format:**
```json
{
  "data": [
    {
      "citingPaper": {
        "paperId": "def456ghi",
        "title": "Newer Paper Citing This",
        "year": 2024,
        "abstract": "We extended the work of [original paper]...",
        "externalIds": {
          "DOI": "10.9012/citing.2024"
        }
      }
    }
  ]
}
```

**Filter for relevance:**

For each citing paper:
1. **Title match**: Keywords present in title?
2. **Abstract match**: User's query terms in abstract?
3. **Recency**: Newer papers often build on findings (prioritize < 2 years)
4. **Citation count**: If Semantic Scholar provides, highly cited papers more likely relevant

**Scoring:**
- Title keywords match: +3 points
- Abstract keywords match: +2 points
- Recent (< 2 years): +2 points
- Moderate recency (2-5 years): +1 point

**Only add to queue if score ≥ 5**

### 4. Deduplication

**Before adding to queue:**

Check papers-reviewed.json:
```python
doi = paper["externalIds"].get("DOI")
if doi in papers_reviewed:
    skip  # Already processed
else:
    add to queue
```

**CRITICAL: After evaluating any paper from citation traversal, add it to papers-reviewed.json regardless of score. This prevents re-processing the same paper from multiple sources.**

**Track citation relationship** in citations/citation-graph.json:
```json
{
  "10.1234/example.2023": {
    "references": ["10.5678/ref1.2020", "10.5678/ref2.2021"],
    "cited_by": ["10.9012/cite1.2024", "10.9012/cite2.2024"]
  }
}
```

**CRITICAL: Use ONLY citation-graph.json for citation tracking. Do NOT create custom files like forward_citation_pmids.txt or citation_analysis.md. All findings go in SUMMARY.md.**

### 5. Process Queue

**Add relevant citations to processing queue:**
```json
{
  "doi": "10.5678/referenced.2020",
  "title": "Referenced Paper",
  "relevance_score": 7,
  "source": "backward_from:10.1234/example.2023",
  "context": "Method citation - describes IC50 measurement protocol"
}
```

**Then:**
- Evaluate using `evaluating-paper-relevance` skill
- If relevant, extract data and potentially traverse its citations too

## Smart Traversal Limits

**To avoid explosion:**
- Only traverse papers scoring ≥ 7 in initial evaluation
- Only follow citations scoring ≥ 5 in relevance filtering
- Limit traversal depth to 2 levels (original → references → references of references)
- Check with user after every 50 papers total

**Breadth-first strategy:**
1. Get all references + citations for current paper
2. Filter and score them
3. Add high-scoring ones to queue
4. Process next paper in queue
5. Repeat until queue empty or hit limit

## Progress Reporting

**Report as you traverse:**
```
🔗 Analyzing citations for: "Original Paper Title"
   → Found 45 references, 12 look relevant
   → Found 23 citing papers, 8 look relevant
   → Adding 20 papers to queue

📄 [51/127] Following reference: "Method for measuring IC50"
   Source: Referenced by original paper in Methods section
   Abstract score: 7 → Fetching full text...
```

## API Rate Limiting

**Semantic Scholar limits:**
- Free tier: 100 requests per 5 minutes
- With API key: 1000 requests per 5 minutes

**Be efficient:**
- Request multiple fields in one call (`?fields=title,abstract,externalIds,year`)
- Use `limit=100` to get more results per request
- Cache responses - don't re-fetch same paper

**If rate limited:**
- Wait 5 minutes
- Report to user: "⏸️ Rate limited by Semantic Scholar API. Waiting 5 minutes..."
- Consider getting API key for higher limits

## Integration with Other Skills

**After traversing citations:**
1. Queue now has N new papers to evaluate
2. For each, use `evaluating-paper-relevance` skill
3. If relevant, extract to SUMMARY.md
4. If highly relevant (≥9), traverse its citations too
5. Update citation-graph.json to track relationships

## Quick Reference

| Task | API Endpoint |
|------|--------------|
| Get paper by DOI | `GET /graph/v1/paper/DOI:{doi}?fields=paperId,title` |
| Get references | `GET /graph/v1/paper/{paperId}/references?fields=contexts,title,abstract,externalIds` |
| Get citations | `GET /graph/v1/paper/{paperId}/citations?fields=title,abstract,externalIds` |
| Check if processed | Look up DOI in papers-reviewed.json |
| Filter relevance | Score based on context/title/intent/recency |

## Relevance Filtering Checklist

Before adding citation to queue:
- [ ] Check if already in papers-reviewed.json (skip if yes)
- [ ] Score based on context/title keywords (need ≥ 5)
- [ ] Verify external ID (DOI or PMID) exists
- [ ] Add source tracking ("backward_from:DOI" or "forward_from:DOI")
- [ ] Add to queue with metadata

## Common Mistakes

**Not tracking all evaluated papers:** Only adding relevant papers to papers-reviewed.json → Add EVERY paper after evaluation to prevent re-review
**Creating custom analysis files:** Making forward_citation_pmids.txt, CITATION_ANALYSIS.md, etc. → Use ONLY citation-graph.json and SUMMARY.md
**Following all citations:** Exponential explosion → Filter before adding to queue
**Ignoring context:** Citation might be tangential → Read context strings
**Not deduplicating:** Re-process same papers → Always check papers-reviewed.json before and after evaluation
**Too deep:** Following 5+ levels → Limit to 2 levels, check with user
**Missing forward citations:** Only checking references → Use both backward and forward
**No rate limiting awareness:** API blocks you → Add delays, handle 429 errors

## Example Workflow

```
1. User asks: "Find selectivity data for BTK inhibitors"
2. Search finds Paper A (score: 9, has great IC50 data)
3. Traverse citations for Paper A:
   - References: 45 total, 12 relevant (mention "selectivity", "IC50")
   - Citations: 23 total, 8 relevant (newer papers on BTK)
4. Add 20 papers to queue
5. Evaluate first queued paper (score: 8)
6. Extract data, traverse its citations (add 5 more)
7. Continue until queue empty or user says stop
```

## Next Steps

After traversing citations:
- Process queued papers with `evaluating-paper-relevance`
- Update SUMMARY.md with new findings
- Check if reached checkpoint (50 papers or 5 minutes)
- If checkpoint: ask user to continue or stop
