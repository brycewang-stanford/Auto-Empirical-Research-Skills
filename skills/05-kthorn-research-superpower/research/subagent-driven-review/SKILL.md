---
name: Subagent-Driven Literature Review
description: Use parallel subagents for large-scale paper screening and deep dive analysis
when_to_use: Large literature searches (50+ papers), parallel paper screening, deep dive analysis on multiple papers, citation network exploration, when main context is getting full
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

# Subagent-Driven Literature Review

## Overview

**Core principle:** Fresh subagent per batch + consolidation between batches = fast parallel screening with quality control

For large literature reviews (50+ papers), dispatching parallel or sequential subagents dramatically speeds up screening while maintaining quality through consolidation checkpoints.

## When to Use

Use subagent-driven approach when:
- **Large searches:** 50+ papers to screen
- **Parallelizable work:** Papers are independent, can be screened separately
- **Deep dive tasks:** Multiple papers need detailed extraction (data tables, methods, datasets)
- **Citation exploration:** Following citation networks recursively
- **Context management:** Main context getting full, need fresh context
- **Time pressure:** Need results faster than sequential screening

**Do NOT use when:**
- Small searches (<20 papers) - overhead not worth it
- Need real-time user visibility into every paper
- Papers require cross-comparison during screening
- Simple, fast screening tasks

## Use Cases

### 1. Parallel Paper Screening (Most Common)

**Scenario:** You have 100 papers from PubMed search to screen for relevance

**Pattern:**
```
Main agent:
1. Splits 100 papers into 5 batches of 20
2. Dispatches 5 subagents IN PARALLEL (single message, multiple Task calls)
3. Each subagent:
   - Fetches abstracts for its batch
   - Scores using rubric
   - Returns JSON with results
4. Main agent consolidates results into papers-reviewed.json

Time savings: 5x faster than sequential!
```

**Prompt template for subagent:**
```
I need you to screen papers 1-20 from this PMID list for relevance to [QUERY].

PMIDs to screen: [PMID list]

Use the evaluating-paper-relevance skill to:
1. Fetch abstract for each PMID
2. Score 0-10 based on:
   - Keywords: [list]
   - Data types needed: [measurements, protocols, datasets, etc.]
3. Return JSON:

{
  "screened_papers": [
    {"pmid": "12345", "score": 8, "status": "relevant", "reason": "..."},
    ...
  ],
  "stats": {"highly_relevant": 3, "relevant": 5, "not_relevant": 12}
}

Do NOT update papers-reviewed.json - return results only.

**Rate limiting (CRITICAL - PubMed limits are SHARED across all parallel subagents):**
- If you are the ONLY subagent running: Use 500ms delays (2 req/sec, safe)
- If running with OTHER parallel subagents: Use longer delays to share capacity
  - You are 1 of 2 parallel: Use 1 second delays
  - You are 1 of 3 parallel: Use 1.5 second delays
  - You are 1 of 5 parallel: Use 2.5 second delays
- If you get HTTP 429 errors: Wait 5 seconds, then use 5-second delays for remaining requests
```

### 2. Deep Dive on Priority Papers

**Scenario:** Initial screening identified 15 highly relevant papers, need detailed data extraction from each

**Pattern:**
```
Main agent:
1. Creates TodoWrite with 15 tasks (one per paper)
2. For each paper, dispatches subagent to:
   - Fetch full text (PMC, Unpaywall)
   - Extract relevant data (tables, figures, methods)
   - Identify key findings
   - Return structured findings
3. Main agent consolidates into SUMMARY.md
4. Reviews and adds to papers-reviewed.json

Can dispatch in parallel (5 at a time) or sequentially
```

**Prompt template for subagent:**
```
Deep dive analysis for paper PMID [12345] / DOI [10.xxxx/yyyy]

Use evaluating-paper-relevance skill to:
1. Check for curated data sources (if applicable to domain)
2. Fetch full text (try PMC, then Unpaywall if paywalled)
3. Extract relevant data based on research domain:
   - Data tables and measurements
   - Methods and protocols
   - Key results and findings
   - Figures with relevant information
4. Return structured JSON:

{
  "pmid": "12345",
  "doi": "10.xxxx/yyyy",
  "full_text_source": "PMC" or "Unpaywall" or "paywalled",
  "data_sources": ["Table 1", "Figure 3", "Supplementary Data"],
  "key_measurements": ["specific values or ranges found"],
  "methods_summary": "Brief description of methods",
  "key_findings": ["Finding 1", "Finding 2", ...],
  "data_availability": "GEO: GSE12345" or "Code: github.com/..." or null
}

Do NOT update papers-reviewed.json - return findings only.
```

### 3. Citation Network Exploration

**Scenario:** Found one highly relevant paper, need to explore forward and backward citations

**Pattern:**
```
Main agent:
1. Dispatches two subagents IN PARALLEL:
   - Subagent A: Fetch and screen forward citations
   - Subagent B: Fetch and screen backward citations
2. Each returns list of promising PMIDs with scores
3. Main agent:
   - Consolidates results
   - Removes duplicates
   - Adds to screening queue
   - Updates papers-reviewed.json
```

**Prompt template for subagent:**
```
Find and screen forward citations for PMID [12345].

Use traversing-citations skill to:
1. Fetch forward citations from PubMed or OpenCitations
2. Screen abstracts for relevance to [QUERY]
3. Score each citation (0-10)
4. Return JSON with promising papers (score ≥7):

{
  "seed_pmid": "12345",
  "direction": "forward",
  "citations_found": 45,
  "relevant_citations": [
    {"pmid": "67890", "score": 8, "title": "...", "reason": "..."},
    ...
  ]
}

Do NOT update papers-reviewed.json - return results only.
```

### 4. Domain-Specific Extraction

**Examples by domain:**

**Genomics:**
```
Subagent extracts:
- GEO/SRA/ENA accessions
- Sample sizes and conditions
- Sequencing methods (RNA-seq, WGS, etc.)
- Analysis pipelines
- Differential expression results
```

**Computational methods:**
```
Subagent extracts:
- Algorithm descriptions
- Code repositories (GitHub, GitLab, etc.)
- Benchmark datasets used
- Performance metrics
- Implementation details
```

**Clinical research:**
```
Subagent extracts:
- Study design (RCT, cohort, etc.)
- Sample size and demographics
- Intervention details
- Primary outcomes
- Statistical methods
```

**Ecology/Environmental:**
```
Subagent extracts:
- Study sites and coordinates
- Sampling methods
- Species/taxa studied
- Environmental measurements
- Data repositories
```

## Workflow: Parallel Screening

### Step 1: Plan and Split

**Main agent tasks:**
1. Load PMID list from search results
2. Decide on batch size (typically 15-25 papers per subagent)
3. Create TodoWrite with batches
4. Prepare subagent prompts

**Example TodoWrite:**
```
- Screen papers batch 1 (PMIDs 1-20)
- Screen papers batch 2 (PMIDs 21-40)
- Screen papers batch 3 (PMIDs 41-60)
- Screen papers batch 4 (PMIDs 61-80)
- Screen papers batch 5 (PMIDs 81-100)
- Consolidate all subagent results
- Generate SUMMARY.md from consolidated data
```

### Step 2: Dispatch Subagents

**CRITICAL: Dispatch all subagents in PARALLEL using single message with multiple Task calls**

**Example:**
```
I'm dispatching 5 subagents in parallel to screen 100 papers.

[Uses Task tool 5 times in single message]
```

**Why parallel:** 5x speed improvement vs sequential!

### Step 3: Collect Results

**Main agent:**
1. Wait for all subagents to complete
2. Collect JSON results from each
3. Validate format and completeness

**Check for:**
- All PMIDs were screened
- Scoring rubric was applied consistently
- No papers missing

### Step 4: Consolidate

**Main agent:**
1. Merge all subagent results
2. Remove duplicates (if any overlap between batches)
3. Sort by relevance score
4. Add ALL papers to papers-reviewed.json:

```json
{
  "10.1234/example.2023": {
    "pmid": "12345",
    "status": "highly_relevant",
    "score": 9,
    "source": "pubmed_search_batch1",
    "screened_by": "subagent",
    "timestamp": "2025-10-11T14:30:00Z",
    "found_data": ["measurements", "methods", "datasets"]
  }
}
```

**Mark source as "subagent" or "pubmed_search_batch1" etc.**

### Step 5: Review Quality

**Main agent checks:**
- Scoring appears consistent across batches
- No batch has dramatically different hit rate (could indicate problem)
- Highly relevant papers make sense
- Any papers needing manual re-review?

**Red flags:**
- One batch found 10 relevant papers, others found 0-1 (inconsistent scoring?)
- Papers marked "highly relevant" don't match keywords
- Missing expected papers

**If issues found:** Re-screen problematic batch manually or with fresh subagent

### Step 6: Generate Summary

**Main agent:**
1. Create SUMMARY.md with all highly relevant and relevant papers
2. Sort by score
3. Add statistics
4. Note which papers need deep dive

### Step 7: Optional Deep Dive

**For highly relevant papers (score ≥8):**

Option A: Dispatch subagents sequentially
```
For each highly relevant paper:
  - Dispatch one subagent per paper
  - Subagent does deep dive extraction
  - Main agent consolidates findings immediately
  - Updates SUMMARY.md progressively
```

Option B: Dispatch subagents in parallel batches
```
Batch 1: Papers 1-5 (dispatch 5 subagents in parallel)
Wait for completion, consolidate
Batch 2: Papers 6-10 (dispatch 5 subagents in parallel)
Wait for completion, consolidate
...
```

## Workflow: Citation Exploration

### Step 1: Identify Seed Papers

**Find 2-3 highly relevant papers from initial screening**

### Step 2: Dispatch Citation Subagents

**For each seed paper, dispatch TWO subagents in parallel:**
1. Forward citations (who cited this paper?)
2. Backward citations (what did this paper cite?)

**Prompt each subagent with:**
- Seed PMID
- Relevance criteria
- Return only papers scoring ≥7

### Step 3: Consolidate Citations

**Main agent:**
1. Collects all citation results
2. Removes duplicates
3. Removes papers already in papers-reviewed.json
4. Creates new screening queue

### Step 4: Screen New Papers

**Option A:** Dispatch new batch screening subagents for citation results
**Option B:** Main agent screens smaller batch manually

### Step 5: Iterate

**If citation exploration found many new relevant papers:**
- Consider exploring citations from those papers too
- Be careful of exponential growth!
- Set stopping criteria (e.g., max 3 levels deep, max 200 total papers)

## Integration with Other Skills

### Works with:
- **evaluating-paper-relevance**: Subagents use this for individual paper screening
- **traversing-citations**: Subagents use this for citation exploration
- **finding-open-access-papers**: Subagents check Unpaywall for paywalled papers
- **checking-chembl**: Subagents can check curated databases (when applicable)

### Combines with:
- **writing-plans**: Create screening plan before dispatching subagents
- **TodoWrite**: Track batches and consolidation progress

## Consolidation Patterns

### Pattern 1: JSON Aggregation

**Subagents return structured JSON, main agent merges:**

```python
# Pseudo-code for consolidation
all_results = []
for subagent_output in subagent_results:
    results = parse_json(subagent_output)
    all_results.extend(results['screened_papers'])

# Sort by score
all_results.sort(key=lambda x: x['score'], reverse=True)

# Update papers-reviewed.json
for paper in all_results:
    papers_reviewed[paper['doi']] = {
        'pmid': paper['pmid'],
        'status': paper['status'],
        'score': paper['score'],
        'source': f"subagent_batch_{paper['batch_id']}",
        'timestamp': now()
    }
```

### Pattern 2: Progressive Consolidation

**Consolidate after each subagent completes (sequential dispatch):**

```
Dispatch subagent 1 → wait → consolidate → dispatch subagent 2 → wait → consolidate → ...
```

**Advantage:** See progress incrementally
**Disadvantage:** Slower than full parallel

### Pattern 3: Batch Consolidation

**Dispatch N subagents in parallel, consolidate batch, repeat:**

```
Dispatch 5 subagents → wait for all 5 → consolidate → dispatch next 5 → ...
```

**Advantage:** Balance between speed and manageable consolidation
**Disadvantage:** More complex than full parallel or sequential

## Common Mistakes

**Not dispatching in parallel:** Sending Task calls sequentially wastes time → Use single message with multiple Task calls
**Subagents updating tracking files:** Causes conflicts → Subagents return JSON only, main agent updates files
**Inconsistent scoring:** Different subagents use different rubrics → Provide clear rubric in prompt
**No quality review:** Blindly trusting subagent results → Always review consolidated results
**Too many parallel subagents:** Dispatching 20+ at once → Keep to 5-10 parallel max
**Forgetting rate limits:** Subagents hit API limits → Include rate limiting in prompts (500ms for single agent, 2.5 seconds for 5 parallel agents)
**No source tracking:** Can't tell which batch found which papers → Add batch_id or source field
**Duplicate work:** Multiple subagents screen same papers → Carefully split PMID lists with no overlap

## Cost Considerations

**Subagent usage has cost implications:**

**Token usage per subagent:**
- Screening 20 papers: ~10-15K tokens per subagent
- Deep dive 1 paper: ~5-10K tokens per subagent
- Citation exploration: ~8-12K tokens per subagent

**Trade-off:**
- Parallel screening: Higher cost, much faster (5x speed)
- Sequential screening: Lower cost, slower
- Consider for time-sensitive research

**Cost-saving strategies:**
- Use subagents for large batches only (50+ papers)
- Screen manually for small searches (<20 papers)
- Parallel dispatch for initial screening (speed matters)
- Sequential dispatch for deep dive (can review progressively)

## Examples

### Example 1: Screen 80 Papers in Parallel

**Initial state:** Have 80 PMIDs from PubMed search

**Main agent:**
```
I'll dispatch 4 subagents in parallel to screen these 80 papers.

Batch 1: PMIDs 1-20 [dispatches subagent with prompt]
Batch 2: PMIDs 21-40 [dispatches subagent with prompt]
Batch 3: PMIDs 41-60 [dispatches subagent with prompt]
Batch 4: PMIDs 61-80 [dispatches subagent with prompt]

[Uses Task tool 4 times in single message]

Now waiting for all subagents to complete...
```

**After subagents complete:**
```
All 4 subagents have completed. Consolidating results:

Batch 1: 3 highly relevant, 5 relevant, 12 not relevant
Batch 2: 2 highly relevant, 7 relevant, 11 not relevant
Batch 3: 4 highly relevant, 6 relevant, 10 not relevant
Batch 4: 1 highly relevant, 4 relevant, 15 not relevant

Total: 10 highly relevant, 22 relevant, 48 not relevant

Updating papers-reviewed.json with all 80 papers...
Generating SUMMARY.md with 32 relevant papers...

Next: Deep dive on 10 highly relevant papers?
```

### Example 2: Deep Dive on 12 Papers

**Initial state:** Have 12 highly relevant papers needing data extraction

**Main agent:**
```
I'll dispatch 12 subagents (in 3 batches of 4) to do deep dive analysis.

Batch 1 papers: PMID 12345, 23456, 34567, 45678
[Dispatches 4 subagents in parallel with deep dive prompts]

Waiting for batch 1 to complete...
[Consolidates batch 1 results into SUMMARY.md]

Batch 2 papers: PMID 56789, 67890, 78901, 89012
[Dispatches 4 subagents in parallel]
...
```

**Result:** All 12 papers analyzed with structured data in ~10-15 minutes vs 1-2 hours sequential

### Example 3: Citation Exploration

**Initial state:** Found key paper PMID 12345

**Main agent:**
```
I'll explore citations from this key paper.

Dispatching 2 subagents in parallel:
1. Forward citations (who cited PMID 12345?)
2. Backward citations (what did PMID 12345 cite?)

[Uses Task tool twice in single message]

Waiting for citation exploration...

Forward citations: Found 34 citations, 8 appear relevant
Backward citations: Found 42 references, 6 appear relevant

New papers to screen: 14 (after removing duplicates)

Now dispatching screening subagent for these 14 papers...
```

## Quick Reference

| Task | Subagent Pattern | Parallel? | Consolidation |
|------|-----------------|-----------|---------------|
| Screen 100 papers | 5 batches of 20 | Yes (5 parallel) | Merge JSON, update papers-reviewed.json |
| Deep dive on 15 papers | 15 individual tasks | Yes (batches of 5) | Add findings to SUMMARY.md progressively |
| Citation exploration | 2-3 citation tasks | Yes | Merge, dedupe, add to screening queue |
| Data extraction | 1 per paper | Sequential or batched | Update papers-reviewed.json with findings |

## Decision Tree

```
Have literature review task?
├─ <20 papers?
│  └─ Screen manually (no subagents)
├─ 20-50 papers?
│  ├─ Time-sensitive? → Use subagents (2-3 batches)
│  └─ Not urgent? → Screen manually
└─ 50+ papers?
   ├─ Initial screening → Use parallel subagents (5-10 batches)
   ├─ Deep dive needed? → Use sequential or batched subagents
   └─ Citation exploration? → Use parallel subagents per seed paper
```

## Advanced: Recursive Citation Exploration

**For exhaustive citation network analysis:**

```
Level 0: Seed paper (PMID 12345)
├─ Level 1: Forward + backward citations (dispatch 2 subagents)
│  ├─ Find 12 relevant papers
│  └─ Add to papers-reviewed.json
├─ Level 2: For each of 12 papers, explore citations (dispatch 24 subagents)
│  ├─ Find 43 new relevant papers
│  └─ Add to papers-reviewed.json
└─ Level 3: For top 10 papers from Level 2, explore citations
   ├─ Find 28 new relevant papers
   └─ STOP (reaching diminishing returns)

Total: 83 papers discovered through citation network
```

**Stopping criteria:**
- Max depth (e.g., 3 levels)
- Max total papers (e.g., 200)
- Diminishing returns (fewer relevant papers per level)
- Time/cost budget

## Next Steps After Subagent Review

1. **Review consolidated results** for quality and consistency
2. **Identify gaps** - any expected papers missing?
3. **Deep dive on highly relevant papers** (if not already done)
4. **Generate final summary** with statistics and key findings
5. **Plan next actions** - citation exploration? Specific data extraction?

## See Also

- **evaluating-paper-relevance**: Core screening methodology
- **traversing-citations**: Citation exploration techniques
- **finding-open-access-papers**: Unpaywall integration for paywalled papers
