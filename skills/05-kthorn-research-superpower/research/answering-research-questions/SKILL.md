---
name: Answering Research Questions
description: Main orchestration workflow for systematic literature research - search, evaluate, traverse, synthesize
when_to_use: When user asks a research question. When user wants to find specific data in literature. When starting comprehensive literature review. When user says "find papers about" or "what is known about".
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

# Answering Research Questions

## Overview

Orchestrate the complete research workflow from query to findings.

**Core principle:** Systematic, trackable, comprehensive. Search → Evaluate → Traverse → Synthesize.

**Announce at start:** "I'm using the Answering Research Questions skill to find [specific data] about [topic]."

## The Process

### Phase 1: Parse Query

Extract from user's request:

**Keywords:**
- Main concepts (e.g., "BTK inhibitor", "selectivity")
- Synonyms and alternatives (e.g., "Bruton tyrosine kinase")
- Related terms (e.g., "off-target", "kinase panel")

**Data types needed:**
- Specific measurements (IC50, KD, EC50, etc.)
- Methods or protocols
- Structures or sequences
- Results or conclusions

**Constraints:**
- Date ranges
- Specific compounds/targets
- Organisms or systems
- Publication types

**Ask clarifying questions if needed:**
- "Are you looking for in vitro or in vivo data?"
- "Any specific time frame?"
- "Which kinases are you most interested in?"
- **"What email address should I use for Unpaywall API requests?"** (Required for finding open access papers)

### Phase 2: Initialize Research Session

**Propose folder name:**
```
research-sessions/YYYY-MM-DD-brief-description/
```

Example: `research-sessions/2025-10-11-btk-inhibitor-selectivity/`

**Show proposal to user:**
```
📁 Creating research folder: research-sessions/2025-10-11-btk-inhibitor-selectivity/
   Proceed? (y/n)
```

**Create folder structure:**
```bash
mkdir -p "research-sessions/YYYY-MM-DD-description"/{papers,citations}
```

**Initialize files:**

**Core files (always create these):**

**papers-reviewed.json:**
```json
{}
```

**citations/citation-graph.json:**
```json
{}
```

**SUMMARY.md:**
```markdown
# Research Query: [User's question]

**Started:** YYYY-MM-DD HH:MM
**Keywords:** keyword1, keyword2, keyword3
**Data types sought:** IC50 values, selectivity data, synthesis methods

---

## Highly Relevant Papers (Score ≥ 8)

Papers scored using `evaluating-paper-relevance` skill:
- Score 0-10 based on: Keywords (0-3) + Data type (0-4) + Specificity (0-3)
- Score ≥ 8: Highly relevant with significant data
- Score 7: Relevant with useful data
- Score 5-6: Possibly relevant
- Score < 5: Not relevant

(Papers will be added here as found)

Example format:
### [Paper Title](https://doi.org/10.1234/example)
**DOI:** [10.1234/example](https://doi.org/10.1234/example) | **PMID:** [12345678](https://pubmed.ncbi.nlm.nih.gov/12345678/)

---

## Relevant Papers (Score 7)

(Papers will be added here as found)

---

## Possibly Relevant Papers (Score 5-6)

(Noted for potential follow-up)

---

## Search Progress

- Initial PubMed search: X results
- Papers reviewed: Y
- Papers with relevant data: Z
- Citations followed: N

---

## Key Findings

(Synthesized findings will be added as research progresses)
```

**CRITICAL: Always use clickable markdown links for DOIs and PMIDs**

**Auxiliary files (for large searches >100 papers):**

See `evaluating-paper-relevance` skill for guidance on when to create:
- **README.md** - Project overview, methodology, file inventory
- **TOP_PRIORITY_PAPERS.md** - Curated priority list organized by tier
- **evaluated-papers.json** - Rich structured data for programmatic access

For small searches (<50 papers), stick to core files only. For large searches (>100 papers), auxiliary files add significant organizational value.

### Phase 3: Search Literature

**Use searching-literature skill:**

1. Construct PubMed query from keywords
2. Execute search (start with 100 results)
3. Save results to `initial-search-results.json`
4. Report: "🔎 Found N papers matching query"

### Phase 4: Evaluate Papers

**Use evaluating-paper-relevance skill:**

For each paper:
1. Check papers-reviewed.json (skip if already processed)
2. Stage 1: Score abstract (0-10)
3. If score ≥ 7: Stage 2 deep dive
4. Extract findings to SUMMARY.md
5. Download PDF and supplementary if available
6. **Update papers-reviewed.json (for ALL papers, even low-scoring ones)**
7. If score ≥ 7: proceed to Phase 5 for this paper

**CRITICAL: Add every paper to papers-reviewed.json regardless of score. This prevents re-review and tracks complete search history.**

**Report progress for EVERY paper:**
```
📄 [15/100] Screening: "Paper Title"
   Abstract score: 8 → Fetching full text...
   ✓ Found IC50 data for 8 compounds
   → Added to SUMMARY.md

📄 [16/100] Screening: "Another Paper"
   Abstract score: 3 → Skipping (not relevant)

📄 [17/100] Screening: "Third Paper"
   Abstract score: 7 → Relevant, adding to queue...
```

**Every 10 papers, give summary update**

### Phase 5: Traverse Citations

**Use traversing-citations skill:**

For papers scoring ≥ 7:
1. Get references (backward)
2. Get citations (forward)
3. Filter for relevance (score ≥ 5)
4. Add to processing queue
5. Evaluate queued papers (return to Phase 4)

**Report progress:**
```
🔗 Following citations from highly relevant paper
   → Found 12 relevant references
   → Found 8 relevant citing papers
   → Adding 20 papers to queue
```

### Phase 6: Checkpoint

**Check after:**
- Every 50 papers reviewed
- Every 5 minutes of processing
- Queue exhausted

**Ask user:**
```
⏸️  Checkpoint: Reviewed 50 papers, found 12 relevant
    Papers with data: 7
    Continue searching? (y/n/summary)
```

**Options:**
- `y` - Continue processing
- `n` - Stop and finalize
- `summary` - Show current findings, then decide

### Phase 7: Synthesize Findings

**When stopping (user says no or queue empty):**

**Option A: Manual synthesis (small research sessions)**
1. **Review SUMMARY.md** - Organize by relevance and topic
2. **Extract key findings** - Group by data type
3. **Add synthesis section:**

```markdown
## Key Findings Summary

### IC50 Values for BTK Inhibitors
- Compound A: 12 nM (Smith et al., 2023)
- Compound B: 45 nM (Doe et al., 2024)
- [More compounds...]

### Selectivity Data
- Compound A shows >80-fold selectivity vs other kinases
- Tested against panel of 50 kinases (Jones et al., 2023)

### Synthesis Methods
- Lead compounds synthesized via [method]
- Yields: 30-45%
- Full protocols in [papers]

### Gaps Identified
- No data on selectivity vs [specific kinase]
- Limited in vivo data
- Few papers on resistance mechanisms
```

4. **Update search progress stats**
5. **List all files downloaded**

**Option B: Script-based synthesis (large research sessions >50 papers)**

For large research sessions, consider creating a synthesis script:

**create `generate_summary.py`:**
- Read `evaluated-papers.json` from helper scripts
- Aggregate findings by priority and scaffold type
- Generate comprehensive SUMMARY.md with:
  - Executive summary with statistics
  - Papers grouped by relevance score
  - Priority recommendations for next steps
  - Methodology documentation
- Include timestamps and reproducibility info

**Benefits:**
- Consistent formatting across sessions
- Easy to regenerate as more papers added
- Can customize grouping/filtering logic
- Documents complete methodology

**Final report:**
```
✅ Research complete!

📊 Summary:
   - Papers reviewed: 127
   - Relevant papers: 18
   - Highly relevant: 7
   - Data extracted: IC50 values for 45 compounds, selectivity data, synthesis methods

📁 All findings in: research-sessions/2025-10-11-btk-inhibitor-selectivity/
   - SUMMARY.md (organized findings)
   - papers/ (14 PDFs + supplementary data)
   - papers-reviewed.json (complete tracking)
```

### Phase 8: Final Consolidation

**CRITICAL: Always consolidate findings at the end**

#### 1. Create relevant-papers.json

**Filter papers-reviewed.json to extract only relevant papers (score ≥ 7):**

```python
# Read papers-reviewed.json
with open('papers-reviewed.json') as f:
    all_papers = json.load(f)

# Filter for relevant papers (score >= 7)
relevant_papers = {
    doi: data for doi, data in all_papers.items()
    if data.get('score', 0) >= 7
}

# Save to relevant-papers.json
with open('relevant-papers.json', 'w') as f:
    json.dump(relevant_papers, f, indent=2)
```

**Format:**
```json
{
  "10.1234/example1.2023": {
    "pmid": "12345678",
    "title": "Paper title",
    "status": "highly_relevant",
    "score": 9,
    "source": "pubmed_search",
    "timestamp": "2025-10-11T16:00:00Z",
    "found_data": ["IC50 values", "synthesis methods"],
    "chembl_id": "CHEMBL1234567"
  },
  "10.1234/example2.2023": {
    "pmid": "23456789",
    "title": "Another paper",
    "status": "relevant",
    "score": 7,
    "source": "forward_citation",
    "timestamp": "2025-10-11T16:15:00Z",
    "found_data": ["MIC data"]
  }
}
```

#### 2. Enhance SUMMARY.md with Methodology Section

**Add these sections to the TOP of existing SUMMARY.md (before paper listings):**

```markdown
# Research Query: [User's question]

**Date:** 2025-10-11
**Duration:** 2h 15m
**Status:** Complete

---

## Search Strategy

**Keywords:** BTK, Bruton tyrosine kinase, inhibitor, selectivity, off-target, kinase panel, IC50
**Data types sought:** IC50 values, selectivity data, kinase panel screening
**Constraints:** None (open date range)

**PubMed Query:**
```
("BTK" OR "Bruton tyrosine kinase") AND (inhibitor OR "kinase inhibitor") AND (selectivity OR "off-target")
```

---

## Screening Methodology

**Rubric:** Abstract scoring (0-10)
- Key terms: +3 pts each (or Keywords 0-3, Data type 0-4, Specificity 0-3 if using old rubric)
- Relevant terms: +1 pt each
- Threshold: ≥7 = relevant

**Sources:**
- Initial PubMed search
- Forward/backward citations via Semantic Scholar

---

## Results Statistics

**Papers Screened:**
- Total reviewed: 127 papers
- Highly relevant (≥8): 12 papers
- Relevant (7): 18 papers
- Possibly relevant (5-6): 23 papers
- Not relevant (<5): 74 papers

**Data Extracted:**
- IC50 values: 45 compounds across 12 papers
- Selectivity data: 8 papers with kinase panel screening
- Full text obtained: 18/30 relevant papers (60%)

**Citation Traversal:**
- Papers with citations followed: 7
- References screened: 45 papers
- Citing papers screened: 38 papers
- Relevant papers found via citations: 8 papers

---

## Key Findings Summary

### IC50 Values for BTK Inhibitors
- Ibrutinib: 0.5 nM (Smith et al., 2023)
- Acalabrutinib: 3 nM (Doe et al., 2024)
- [Additional findings synthesized from papers below]

### Selectivity Patterns
- Most inhibitors show >50-fold selectivity vs other kinases
- Common off-targets: TEC, BMX (other TEC family kinases)

### Gaps Identified
- Limited data on selectivity vs JAK/SYK
- Few papers on resistance mechanisms
- No in vivo selectivity data found

---

## File Inventory

- `SUMMARY.md` - This file (methodology + findings)
- `relevant-papers.json` - 30 relevant papers (score ≥7)
- `papers-reviewed.json` - All 127 papers screened
- `papers/` - 18 PDFs + 5 supplementary files
- `citations/citation-graph.json` - Citation relationships

---

## Reproducibility

**To reproduce:**
1. Use PubMed query above
2. Apply screening rubric (threshold ≥7)
3. Follow citations from highly relevant papers (≥8)
4. Check Unpaywall for paywalled papers

**Software:** Research Superpowers skills v2025-10-11

---

[Existing paper listings follow below...]

## Highly Relevant Papers (Score ≥ 8)

### [Paper Title]...
```

**Report to user:**
```
✅ Research session complete!

📄 Consolidation complete:
   1. SUMMARY.md - Enhanced with methodology, statistics, and findings
   2. relevant-papers.json - 30 relevant papers (score ≥7) in JSON format

📁 All files in: research-sessions/2025-10-11-btk-inhibitor-selectivity/
   - SUMMARY.md (complete: methodology + paper-by-paper findings)
   - relevant-papers.json (30 relevant papers for programmatic access)
   - papers-reviewed.json (127 total papers screened)
   - papers/ (18 PDFs)

🔍 Quick access:
   - Open SUMMARY.md for complete findings and methodology
   - Use relevant-papers.json for programmatic access

💡 Optional: Clean up intermediate files?
   → Use cleaning-up-research-sessions skill to safely remove temporary files
```

## Workflow Checklist

**Use TodoWrite to track these steps:**

- [ ] Parse user query (keywords, data types, constraints)
- [ ] Propose and create research folder
- [ ] Initialize tracking files (SUMMARY.md, papers-reviewed.json, citation-graph.json)
- [ ] Search PubMed using searching-literature skill
- [ ] For each paper: evaluate using evaluating-paper-relevance skill
- [ ] For relevant papers (≥7): traverse citations using traversing-citations skill
- [ ] Report progress regularly
- [ ] Checkpoint every 50 papers or 5 minutes
- [ ] When done: synthesize findings and enhance SUMMARY.md with methodology
- [ ] Create relevant-papers.json (filtered JSON for programmatic access)
- [ ] Final report with stats and file locations

## Integration Points

**Skills used:**
1. `searching-literature` - Initial PubMed search
2. `evaluating-paper-relevance` - Score and extract from papers
3. `traversing-citations` - Follow citation networks

**All skills coordinate through:**
- Shared `papers-reviewed.json` (deduplication)
- Shared `SUMMARY.md` (findings accumulation)
- Shared `citation-graph.json` (relationship tracking)

**File organization:**
- **Small searches (<50 papers):** Core files only (papers-reviewed.json, SUMMARY.md, citation-graph.json)
- **All searches:** Create relevant-papers.json at end; enhance SUMMARY.md with methodology
- **Large searches (>100 papers):** May add auxiliary files (README.md, TOP_PRIORITY_PAPERS.md, evaluated-papers.json) for better organization

## Error Handling

**No results found:**
- Try broader keywords
- Remove constraints
- Check spelling
- Try different synonyms

**API rate limiting:**
- Report to user: "⏸️ Rate limited, waiting..."
- Wait required time
- Resume automatically

**Full text unavailable:**
- Note in SUMMARY.md
- Continue with abstract-only evaluation
- Flag for manual retrieval if highly relevant

**Too many results (>500):**
- Suggest narrowing query
- Process first 100, ask if continue
- Focus on most recent or most cited

## Quick Reference

| Phase | Skill | Output |
|-------|-------|--------|
| Parse | (built-in) | Keywords, data types, constraints |
| Initialize | (built-in) | Folder, SUMMARY.md, tracking files |
| Search | searching-literature | List of papers with metadata |
| Evaluate | evaluating-paper-relevance | Scored papers, extracted findings |
| Traverse | traversing-citations | Additional papers from citations |
| Synthesize | (built-in) | Enhanced SUMMARY.md with methodology + findings |
| Consolidate | (built-in) | relevant-papers.json (filtered to score ≥7) |

## Common Mistakes

**Not tracking all papers:** Only adding relevant papers to papers-reviewed.json → Add EVERY paper to prevent re-review, track complete history
**Creating unnecessary auxiliary files for small searches:** For <50 papers, stick to core files (papers-reviewed.json, SUMMARY.md, citation-graph.json). For large searches (>100 papers), auxiliary files like README.md and TOP_PRIORITY_PAPERS.md add value.
**Silent work:** User can't see progress → Report EVERY paper, give updates every 10
**Non-clickable identifiers:** Plain text DOIs/PMIDs → Always use markdown links
**Jumping to evaluation without good search:** Too narrow results → Optimize search first
**Not tracking papers:** Re-reviewing same papers → Always use papers-reviewed.json
**Following all citations:** Exponential explosion → Filter before traversing
**No checkpoints:** User loses context → Report and ask every 50 papers
**Poor synthesis:** Just list papers → Group by data type, extract key findings
**Batch reporting:** Reporting 20 papers at once → Report each one as you go

## User Communication (CRITICAL)

**NEVER work silently! User needs continuous feedback.**

**Report frequency:**
- **Every paper:** Brief status as you screen (`📄 [N/Total] Title... Score: X`)
- **Every 5-10 papers:** Progress summary with counts
- **Every finding:** Immediately report what data you found
- **Every decision point:** Ask before changing direction

**Be specific in progress reports:**
- ✅ "Found IC50 = 12 nM for compound 7 (Table 2)"
- ❌ "Found data"
- ✅ "Screening paper 25/127: Not relevant (score 3)"
- ❌ Silently skip papers

**Ask for clarification when needed:**
- ✅ "Are you looking for in vitro or in vivo IC50 values?"
- ❌ Assume and potentially waste time

**Report blockers immediately:**
- ✅ "⚠️ Paper behind paywall - evaluating from abstract only"
- ❌ Silently skip without mentioning

**Periodic summaries (every 10-15 papers):**
```
📊 Progress update:
   - Reviewed: 30/127 papers
   - Highly relevant: 3 (scores 8-10)
   - Relevant: 5 (score 7)
   - Currently: Screening paper 31...
```

**Why:** User can course-correct early, knows work is happening, can stop if needed

## Success Criteria

Research session successful when:
- All relevant papers found and evaluated
- Specific data extracted and organized
- Citations followed systematically
- No duplicate processing
- Clear SUMMARY.md with actionable findings
- User questions answered with evidence

## Next Steps

After completing research:
- User reviews SUMMARY.md and relevant-papers.json
- **Optional**: Run cleaning-up-research-sessions skill to remove intermediate files
- May request deeper dive into specific papers
- May request follow-up searches with refined keywords
- May archive or share research session folder
