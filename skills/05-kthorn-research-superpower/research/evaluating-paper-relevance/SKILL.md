---
name: Evaluating Paper Relevance
description: Two-stage paper screening - abstract scoring then deep dive for specific data extraction
when_to_use: After literature search returns results. When need to determine if paper contains specific data. When screening papers for relevance. When extracting methods, results, data from papers.
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

# Evaluating Paper Relevance

## Overview

Two-stage screening process: quick abstract scoring followed by deep dive into promising papers.

**Core principle:** Precision over breadth. Find papers that actually contain the specific data/methods user needs, not just topically related papers.

## When to Use

Use this skill when:
- Have list of papers from search
- Need to determine which papers have relevant data
- User asks for specific information (measurements, protocols, datasets, etc.)
- Screening papers one-by-one
- Any research domain (medicinal chemistry, genomics, ecology, computational methods, etc.)

## Choosing Your Approach

**Small searches (<50 papers):**
- Manual screening with progress reporting
- Use papers-reviewed.json + SUMMARY.md only
- No helper scripts needed
- Report progress to user for every paper

**Large searches (50-150 papers):**
- Consider helper scripts (screen_papers.py + deep_dive_papers.py)
- Use Progressive Enhancement Pattern (see Helper Scripts section)
- Create README.md with methodology
- May want TOP_PRIORITY_PAPERS.md for quick reference
- Use richer JSON structure (evaluated-papers.json categorized by relevance)
- Consider using subagent-driven-review skill for parallel screening

**Very large searches (>150 papers):**
- Definitely use helper scripts with Progressive Enhancement Pattern
- Create full auxiliary documentation suite (README.md, TOP_PRIORITY_PAPERS.md)
- Consider citation network analysis
- Plan for multi-week timeline
- Strongly consider subagent-driven-review skill for parallelization
- May need multiple consolidation checkpoints

## Two-Stage Process

### Stage 1: Abstract Screening (Fast)

**Goal:** Quickly identify promising papers

**Score 0-10 based on:**
- **Keywords match (0-3 points)**: Does abstract mention key terms relevant to the query?
- **Data type match (0-4 points)**: Does it mention the specific information user needs?
  - Examples: measurements (IC50, expression levels, population sizes), protocols, datasets, structures, sequences, code
- **Specificity (0-3 points)**: Is it specific to user's question or just general background/review?

**Decision rules:**
- Score < 5: Skip (not relevant)
- Score 5-6: Note in summary as "possibly relevant" but skip for now
- Score ≥ 7: Proceed to Stage 2 (deep dive)

**IMPORTANT: Report to user for EVERY paper:**
```
📄 [N/Total] Screening: "Paper Title"
   Abstract score: 8 → Fetching full text...
```

or

```
📄 [N/Total] Screening: "Paper Title"
   Abstract score: 4 → Skipping (insufficient relevance)
```

**Never screen silently** - user needs to see progress happening

### Stage 2: Deep Dive (Thorough)

**Goal:** Extract specific data/methods from promising papers

#### 1. Check ChEMBL (for medicinal chemistry papers)

**If paper describes medicinal chemistry / SAR data:**

Use `skills/research/checking-chembl` to check if paper is in ChEMBL database:
```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/document.json?doi=$doi"
```

**If found in ChEMBL:**
- Note ChEMBL ID and activity count in SUMMARY.md
- Report to user: "✓ ChEMBL: CHEMBL3870308 (45 data points)"
- Structured SAR data available without PDF parsing

**Continue to full text fetch for context, methods, discussion.**

#### 2. Fetch Full Text

**Try in order:**

**A. PubMed Central (free full text):**
```bash
# Check if available in PMC
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=PMID[PMID]&retmode=json"

# If found, fetch full text XML via API
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=PMCID&rettype=full&retmode=xml"

# Or fetch HTML directly (note: use pmc.ncbi.nlm.nih.gov, not www.ncbi.nlm.nih.gov/pmc)
curl "https://pmc.ncbi.nlm.nih.gov/articles/PMCID/"
```

**B. DOI resolution:**
```bash
# Try publisher link
curl -L "https://doi.org/10.1234/example.2023"
# May hit paywall - check response
```

**C. Unpaywall (MANDATORY if paywalled):**
**CRITICAL: If step B hits a paywall, you MUST immediately try Unpaywall before giving up.**

Use `skills/research/finding-open-access-papers` to find free OA version:
```bash
curl "https://api.unpaywall.org/v2/DOI?email=USER_EMAIL"
# Often finds versions in repositories, preprint servers, author copies
# IMPORTANT: Ask user for their email if not already provided - do NOT use claude@anthropic.com
```

Report to user:
```
⚠️  Paper behind paywall, checking Unpaywall...
✓ Found open access version at [repository/preprint server]
```

or

```
⚠️  Paper behind paywall, checking Unpaywall...
✗ No open access version available - continuing with abstract only
```

**D. Preprints (direct):**
- Check bioRxiv: `https://www.biorxiv.org/content/10.1101/{doi}`
- Check arXiv (for computational papers)

**If full text unavailable AFTER trying Unpaywall:**
- Note in SUMMARY.md: "⚠️ Full text behind paywall - no OA version found via Unpaywall"
- Continue with abstract-only evaluation (limited)

**CRITICAL: Do NOT skip Unpaywall check. Many paywalled papers have free versions in repositories.**

#### 2. Scan for Relevant Content

**Focus on sections:**
- **Methods**: Experimental procedures, protocols
- **Results**: Data tables, figures, measurements
- **Tables/Figures**: Often contain the specific data user needs
- **Supplementary Information**: Additional data, extended methods

**What to look for (adapt to research domain):**
- Specific data user requested
  - **Medicinal chemistry**: IC50 values, compound structures, SAR data
  - **Genomics**: Gene expression levels, sequences, variant data
  - **Ecology**: Population measurements, species counts, environmental parameters
  - **Computational**: Algorithms, code availability, performance benchmarks
  - **Clinical**: Patient outcomes, treatment protocols, sample sizes
- Methods/protocols described in detail
- Statistical analysis and significance
- Data availability statements
- Code/data repositories mentioned

**Use grep/text search (adapt search terms):**
```bash
# Examples for different domains
grep -i "IC50\|Ki\|MIC" paper.xml                    # Medicinal chemistry
grep -i "expression\|FPKM\|RNA-seq" paper.xml        # Genomics
grep -i "abundance\|population\|sampling" paper.xml  # Ecology
grep -i "algorithm\|github\|code" paper.xml          # Computational
```

#### 3. Extract Findings

**Create structured extraction (adapt to research domain):**

**Example 1: Medicinal chemistry**
```json
{
  "doi": "10.1234/medchem.2023",
  "title": "Novel kinase inhibitors...",
  "relevance_score": 9,
  "findings": {
    "data_found": [
      "IC50 values for compounds 1-12 (Table 2)",
      "Selectivity data (Figure 3)",
      "Synthesis route (Scheme 1)"
    ],
    "key_results": [
      "Compound 7: IC50 = 12 nM",
      "10-step synthesis, 34% yield"
    ]
  }
}
```

**Example 2: Genomics**
```json
{
  "doi": "10.1234/genomics.2023",
  "title": "Gene expression in disease...",
  "relevance_score": 8,
  "findings": {
    "data_found": [
      "RNA-seq data for 50 samples (GEO: GSE12345)",
      "Differential expression results (Table 1)",
      "Gene set enrichment analysis (Figure 4)"
    ],
    "key_results": [
      "123 genes upregulated (FDR < 0.05)",
      "Pathway enrichment: immune response"
    ]
  }
}
```

**Example 3: Computational methods**
```json
{
  "doi": "10.1234/compbio.2023",
  "title": "Novel alignment algorithm...",
  "relevance_score": 9,
  "findings": {
    "data_found": [
      "Algorithm pseudocode (Methods)",
      "Code repository (github.com/user/tool)",
      "Benchmark results (Table 2)"
    ],
    "key_results": [
      "10x faster than BLAST",
      "98% accuracy on test dataset"
    ]
  }
}
```

#### 4. Download Materials

**PDFs:**
```bash
# If PDF available
curl -L -o "papers/$(echo $doi | tr '/' '_').pdf" "https://doi.org/$doi"
```

**Supplementary data:**
```bash
# Download SI files if URLs found
curl -o "papers/${doi}_supp.zip" "https://publisher.com/supp/file.zip"
```

#### 5. Update Tracking Files

**CRITICAL: Use ONLY papers-reviewed.json and SUMMARY.md. Do NOT create custom tracking files.**

**CRITICAL: Add EVERY paper to papers-reviewed.json, regardless of score. This prevents re-reviewing papers and tracks complete search history.**

**Add to papers-reviewed.json:**

**For relevant papers (score ≥7):**
```json
{
  "10.1234/example.2023": {
    "pmid": "12345678",
    "status": "relevant",
    "score": 9,
    "source": "pubmed_search",
    "timestamp": "2025-10-11T10:30:00Z",
    "found_data": ["IC50 values", "synthesis methods"],
    "has_full_text": true,
    "chembl_id": "CHEMBL1234567"
  }
}
```

**For not-relevant papers (score <7):**
```json
{
  "10.1234/another.2023": {
    "pmid": "12345679",
    "status": "not_relevant",
    "score": 4,
    "source": "pubmed_search",
    "timestamp": "2025-10-11T10:31:00Z",
    "reason": "no activity data, review paper"
  }
}
```

**Always add papers even if skipped** - this prevents re-processing and documents what was already checked.

**Add to SUMMARY.md (examples for different domains):**

**Medicinal chemistry example:**
```markdown
### [Novel kinase inhibitors with improved selectivity](https://doi.org/10.1234/medchem.2023) (Score: 9)

**DOI:** [10.1234/medchem.2023](https://doi.org/10.1234/medchem.2023)
**PMID:** [12345678](https://pubmed.ncbi.nlm.nih.gov/12345678/)
**ChEMBL:** [CHEMBL1234567](https://www.ebi.ac.uk/chembl/document_report_card/CHEMBL1234567/)

**Key Findings:**
- IC50 values for 12 inhibitors (Table 2)
- Compound 7: IC50 = 12 nM, >80-fold selectivity
- Synthesis route (Scheme 1, page 4)

**Files:** PDF, supplementary data
```

**Genomics example:**
```markdown
### [Transcriptomic analysis of disease progression](https://doi.org/10.1234/genomics.2023) (Score: 8)

**DOI:** [10.1234/genomics.2023](https://doi.org/10.1234/genomics.2023)
**PMID:** [23456789](https://pubmed.ncbi.nlm.nih.gov/23456789/)
**Data:** [GEO: GSE12345](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE12345)

**Key Findings:**
- RNA-seq data: 50 samples, 3 conditions
- 123 differentially expressed genes (FDR < 0.05)
- Immune pathway enrichment (Figure 3)

**Files:** PDF, supplementary tables with gene lists
```

**Computational methods example:**
```markdown
### [Fast sequence alignment with novel algorithm](https://doi.org/10.1234/compbio.2023) (Score: 9)

**DOI:** [10.1234/compbio.2023](https://doi.org/10.1234/compbio.2023)
**Code:** [github.com/user/tool](https://github.com/user/tool)

**Key Findings:**
- New alignment algorithm (pseudocode in Methods)
- 10x faster than BLAST, 98% accuracy
- Benchmark datasets available

**Files:** PDF, code repository linked
```

**IMPORTANT: Always make DOIs and PMIDs clickable links:**
- DOI format: `[10.1234/example.2023](https://doi.org/10.1234/example.2023)`
- PMID format: `[12345678](https://pubmed.ncbi.nlm.nih.gov/12345678/)`
- Makes papers easy to access directly from SUMMARY.md

## Progress Reporting

**CRITICAL: Report to user as you work - never work silently!**

**For every paper, report:**
1. **Start screening:** `📄 [N/Total] Screening: "Title..."`
2. **Abstract score:** `Abstract score: X/10`
3. **Decision:** What you're doing next (fetching full text / skipping / etc)

**For relevant papers, report findings immediately (adapt to domain):**

**Medicinal chemistry example:**
```
📄 [15/127] Screening: "Selective BTK inhibitors..."
   Abstract score: 8 → Fetching full text...
   ✓ Found IC50 data for 8 compounds (Table 2)
   ✓ Selectivity data vs 50 kinases (Figure 3)
   → Added to SUMMARY.md
```

**Genomics example:**
```
📄 [23/89] Screening: "Gene expression in liver disease..."
   Abstract score: 9 → Fetching full text...
   ✓ RNA-seq data available (GEO: GSE12345)
   ✓ 123 DEGs identified (Table 1, FDR < 0.05)
   → Added to SUMMARY.md
```

**Computational methods example:**
```
📄 [7/45] Screening: "Novel phylogenetic algorithm..."
   Abstract score: 8 → Fetching full text...
   ✓ Code available (github.com/user/tool)
   ✓ Benchmark results (10x faster, Table 2)
   → Added to SUMMARY.md
```

**Update user every 5-10 papers with summary:**
```
📊 Progress: Reviewed 30/127 papers
   - Highly relevant: 3
   - Relevant: 5
   - Currently screening paper 31...
```

**Why this matters:** User needs to see work happening and provide feedback/corrections early

## Integration with Other Skills

**For medicinal chemistry papers:**
- **Use `skills/research/checking-chembl`** to find curated SAR data
- Check BEFORE attempting to parse activity tables from PDFs
- ~30-40% of medicinal chemistry papers have ChEMBL data

**During full text fetching:**
- **If paywalled: MANDATORY to use `skills/research/finding-open-access-papers` (Unpaywall)**
- Do NOT skip this step - Unpaywall finds ~50% of paywalled papers for free

**After finding relevant paper:**
1. **Check ChEMBL** (if medicinal chemistry)
2. **Extract findings** to SUMMARY.md
3. **Download files** to papers/ folder
4. **Call traversing-citations skill** to find related papers
5. **Update papers-reviewed.json** to avoid re-processing

## Scoring Rubric

| Score | Meaning | Action |
|-------|---------|--------|
| 0-4 | Not relevant | Skip, brief note in summary |
| 5-6 | Possibly relevant | Note for later, skip deep dive for now |
| 7-8 | Relevant | Deep dive, extract data, add to summary |
| 9-10 | Highly relevant | Deep dive, extract data, follow citations, highlight in summary |

## Helper Scripts (Optional)

**When screening many papers (>20), consider creating a helper script:**

**Benefits:**
- Batch processing with rate limiting
- Consistent scoring logic
- Save intermediate results
- Resume after interruption

**Create in research session folder:**
```python
# research-sessions/YYYY-MM-DD-query/screen_papers.py
```

**Key components:**
1. **Fetch abstracts** - PubMed efetch with error handling
2. **Score abstracts** - Implement scoring rubric (0-10)
3. **Rate limiting** - 500ms delay between API calls (or longer if running parallel subagents)
4. **Save results** - JSON with scored papers categorized by relevance
5. **Progress reporting** - Print status as it runs

### Progressive Enhancement Pattern (Recommended for 50+ papers)

**For large-scale screening, use two-script pattern:**

**Script 1: Abstract Screening** (`screen_papers.py`)
- Batch fetch abstracts
- Score using rubric (0-10)
- Categorize by relevance
- Output: `evaluated-papers.json` with basic metadata

**Script 2: Deep Dive** (`deep_dive_papers.py`)
- Read Script 1 output
- Fetch full text for highly relevant papers (score ≥8)
- Extract domain-specific data (measurements, protocols, datasets, etc.)
- Update same JSON file with enhanced metadata

**Benefits:**
- **Can run steps independently** - Score abstracts once, re-run deep dive multiple times
- **Resume if interrupted** - No need to re-fetch abstracts if deep dive fails
- **Re-run deep dive without re-scoring abstracts** - Adjust extraction logic, keep scores
- **Consistent and reproducible** - Same scoring logic applied to all papers
- **Save API calls** - Abstract screening happens once, deep dive only on relevant papers

**Script design:**
- Parameterize keywords and data types for specific query
- Progressive enhancement - add detail to same JSON file
- Include rate limiting (500ms between API calls for single script, longer if parallel)
- Keep scripts with research session for reproducibility

**When NOT to create helper script:**
- Few papers (<20)
- One-off quick searches
- Manual screening is faster

## Common Mistakes

**Not tracking all papers:** Only adding relevant papers to papers-reviewed.json → Add EVERY paper regardless of score to prevent re-review
**Skipping Unpaywall:** Hitting paywall and giving up → ALWAYS check Unpaywall first, many papers have free versions
**Creating unnecessary files for small searches:** For <50 papers, use ONLY papers-reviewed.json and SUMMARY.md. For large searches (>100 papers), structured evaluated-papers.json and auxiliary files (README.md, TOP_PRIORITY_PAPERS.md) add significant value and should be used.
**Too strict:** Skipping papers that mention data indirectly → Re-read abstract carefully
**Too lenient:** Deep diving into tangentially related papers → Focus on specific data user needs
**Missing supplementary data:** Many papers hide key data in SI → Always check for supplementary files
**Silent screening:** User can't see progress → Report EVERY paper as you screen it
**No periodic summaries:** User loses big picture → Update every 5-10 papers
**Non-clickable DOIs/PMIDs:** Plain text identifiers → Always use markdown links
**Re-reviewing papers:** Wastes time → Always check papers-reviewed.json first
**Not using helper scripts:** Manually screening 100+ papers → Consider batch script

## Quick Reference

| Task | Action |
|------|--------|
| Check if reviewed | Look up DOI in papers-reviewed.json |
| Score abstract | Keywords (0-3) + Data type (0-4) + Specificity (0-3) |
| Get full text | Try PMC → DOI → Unpaywall → Preprints |
| Find data | Grep for terms, focus on Methods/Results/Tables |
| Download PDF | `curl -L -o papers/FILE.pdf URL` |
| Update tracking | Add to papers-reviewed.json + SUMMARY.md |

## Next Steps

After evaluating paper:
- If score ≥ 7: Call `skills/research/traversing-citations`
- Continue to next paper in search results
- Check if reached 50 papers or 5 minutes → ask user to continue or stop

## Auxiliary Files (for large searches >100 papers)

### README.md Template

**Use this structure for research projects with 100+ papers:**

1. **Project Overview**
   - Query description
   - Target molecules/topics
   - Date completed

2. **Quick Start Guide**
   - Where to start reading
   - Priority lists

3. **File Inventory**
   - Description of each file
   - What each is used for

4. **Key Findings Summary**
   - Statistics
   - Top findings
   - Coverage by category

5. **Methodology**
   - Scoring rubric
   - Decision rules
   - Data sources

6. **Next Steps**
   - Recommended actions
   - Priority order

### TOP_PRIORITY_PAPERS.md Template

**For datasets with >50 relevant papers, create curated priority list:**

- Organized by tier (Tier 1: Must-read, Tier 2: High-value, etc.)
- Include score, DOI, key findings summary
- Note full text availability
- Suggest reading order

**Example structure:**
```markdown
# Top Priority Papers

## Tier 1: Must-Read (Score 10)

### [Paper Title](https://doi.org/10.xxxx/yyyy) (Score: 10)

**DOI:** [10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy)
**PMID:** [12345678](https://pubmed.ncbi.nlm.nih.gov/12345678/)
**Full text:** ✓ PMC12345678

**Key Findings:**
- Finding 1
- Finding 2

---

## Tier 2: High-Value (Score 8-9)

[Additional papers organized by priority...]
```
