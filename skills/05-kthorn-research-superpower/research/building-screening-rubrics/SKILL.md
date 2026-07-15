---
name: Building Paper Screening Rubrics
description: Collaboratively build and refine paper screening rubrics through brainstorming, test-driven development, and iterative feedback
when_to_use: Starting new literature search. When automated screening misclassifies papers. When need to screen 50+ papers efficiently. Before creating screening scripts. When rescreening papers with updated criteria.
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

# Building Paper Screening Rubrics

## Overview

**Core principle:** Build screening rubrics collaboratively through brainstorming → test → refine → automate → review → iterate.

Good rubrics come from understanding edge cases upfront and testing on real papers before bulk screening.

## When to Use

Use this skill when:
- Starting a new literature search that will screen 50+ papers
- Current rubric misclassifies papers (false positives/negatives)
- Need to define "relevance" criteria before automated screening
- Want to update criteria and re-screen cached papers
- Building helper scripts for evaluating-paper-relevance

**When NOT to use:**
- Small searches (<20 papers) - manual screening is fine
- Rubric already works well - no need to rebuild
- One-off exploratory searches

## Two-Phase Process

### Phase 1: Collaborative Rubric Design

#### Step 1: Brainstorm Relevance Criteria

**Ask domain-agnostic questions to understand what makes papers relevant:**

**Core Concepts:**
- "What are the key terms/concepts for your research question?"
  - Examples: specific genes, proteins, compounds, diseases, methods, organisms, theories
- "Are there synonyms or alternative names?"
- "Any terms that should EXCLUDE papers (false positives)?"

**Data Types & Artifacts:**
- "What type of information makes a paper valuable?"
  - Quantitative measurements (IC50, expression levels, population sizes, etc.)
  - Protocols or methods
  - Datasets with accessions (GEO, SRA, PDB, etc.)
  - Code or software
  - Chemical structures
  - Sequences or genomes
  - Theoretical models
- "Do you need the actual data in the paper, or just that such data exists?"

**Paper Types:**
- "What types of papers are relevant?"
  - Primary research only?
  - Reviews or meta-analyses?
  - Methods papers?
  - Clinical trials?
  - Preprints acceptable?

**Relationships & Context:**
- "Are papers about related/analogous concepts relevant?"
  - Example: "If studying protein X, are papers about homologs/paralogs relevant?"
  - Example: "If studying compound A, are papers about analogs/derivatives relevant?"
  - Example: "If studying disease X, are papers about related diseases relevant?"
- "Does the paper need to be ABOUT your topic, or just MENTION it?"
- "Are synthesis/methods papers relevant even without activity data?"

**Edge Cases:**
- "Can you think of papers that would LOOK relevant but aren't?"
- "Papers that might NOT look relevant but actually are?"

**Document responses in screening-criteria.json**

#### Step 2: Build Initial Rubric

**Based on brainstorming, propose scoring logic:**

```
Scoring (0-10):

Keywords Match (0-3 pts):
  - Core term 1: +1 pt
  - Core term 2 OR synonym: +1 pt
  - Related term: +1 pt

Data Type Match (0-4 pts):
  - Measurement type (IC50, Ki, EC50, etc.): +2 pts
  - Dataset/code available: +1 pt
  - Methods described: +1 pt

Specificity (0-3 pts):
  - Primary research: +3 pts
  - Methods paper: +2 pts
  - Review: +1 pt

Special Rules:
  - If mentions exclusion term: score = 0

Threshold: ≥7 = relevant, 5-6 = possibly relevant, <5 = not relevant
```

**Present to user and ask:** "Does this logic match your expectations?"

**Save initial rubric to screening-criteria.json:**
```json
{
  "version": "1.0.0",
  "created": "2025-10-11T15:30:00Z",
  "keywords": {
    "core_terms": ["term1", "term2"],
    "synonyms": {"term1": ["alt1", "alt2"]},
    "related_terms": ["related1", "related2"],
    "exclusion_terms": ["exclude1", "exclude2"]
  },
  "data_types": {
    "measurements": ["IC50", "Ki", "MIC"],
    "datasets": ["GEO:", "SRA:", "PDB:"],
    "methods": ["protocol", "synthesis", "assay"]
  },
  "scoring": {
    "keywords_max": 3,
    "data_type_max": 4,
    "specificity_max": 3,
    "relevance_threshold": 7
  },
  "special_rules": [
    {
      "name": "scaffold_analogs",
      "condition": "mentions target scaffold AND (analog OR derivative)",
      "action": "add 3 points"
    }
  ]
}
```

### Phase 2: Test-Driven Refinement

#### Step 1: Create Test Set

**Do a quick PubMed search to get candidate papers:**
```bash
# Search for 20 papers using initial keywords
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=YOUR_QUERY&retmax=20&retmode=json"
```

**Fetch abstracts for first 10-15 papers:**
```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=PMID1,PMID2,...&retmode=xml&rettype=abstract"
```

**Present abstracts to user one at a time:**
```
Paper 1/10:
Title: [Title]
PMID: [12345678]
DOI: [10.1234/example]

Abstract:
[Full abstract text]

Is this paper RELEVANT to your research question? (y/n/maybe)
```

**Record user judgments in test-set.json:**
```json
{
  "test_papers": [
    {
      "pmid": "12345678",
      "doi": "10.1234/example",
      "title": "Paper title",
      "abstract": "Full abstract text...",
      "user_judgment": "relevant",
      "timestamp": "2025-10-11T15:45:00Z"
    }
  ]
}
```

**Continue until have 5-10 papers with clear judgments**

#### Step 2: Score Test Papers with Rubric

**Apply rubric to each test paper:**
```python
for paper in test_papers:
    score = calculate_score(paper['abstract'], rubric)
    predicted_status = "relevant" if score >= 7 else "not_relevant"
    paper['predicted_score'] = score
    paper['predicted_status'] = predicted_status
```

**Calculate accuracy:**
```python
correct = sum(1 for p in test_papers
              if p['predicted_status'] == p['user_judgment'])
accuracy = correct / len(test_papers)
```

#### Step 3: Show Results to User

**Present classification report:**
```
RUBRIC TEST RESULTS (5 papers):

✓ PMID 12345678: Score 9 → relevant (user: relevant) ✓
✗ PMID 23456789: Score 4 → not_relevant (user: relevant) ← FALSE NEGATIVE
✓ PMID 34567890: Score 8 → relevant (user: relevant) ✓
✓ PMID 45678901: Score 3 → not_relevant (user: not_relevant) ✓
✗ PMID 56789012: Score 7 → relevant (user: not_relevant) ← FALSE POSITIVE

Accuracy: 60% (3/5 correct)
Target: ≥80%

--- FALSE NEGATIVE: PMID 23456789 ---
Title: "Novel analogs of compound X with improved potency"
Score breakdown:
  - Keywords: 1 pt (matched "compound X")
  - Data type: 2 pts (mentioned IC50 values)
  - Specificity: 1 pt (primary research)
  - Total: 4 pts → not_relevant

Why missed: Paper discusses "analogs" but didn't trigger scaffold_analogs rule
Abstract excerpt: "We synthesized 12 analogs of compound X..."

--- FALSE POSITIVE: PMID 56789012 ---
Title: "Review of kinase inhibitors"
Score breakdown:
  - Keywords: 2 pts
  - Data type: 3 pts
  - Specificity: 2 pts (review, not primary)
  - Total: 7 pts → relevant

Why wrong: Review paper, user wants primary research only
```

#### Step 4: Iterative Refinement

**Ask user for adjustments:**
```
Current accuracy: 60% (below 80% threshold)

Suggestions to improve rubric:
1. Strengthen scaffold_analogs rule - should "synthesized N analogs" always trigger?
2. Lower points for review papers (currently 2 pts, maybe 0 pts?)
3. Add more synonym terms for core concepts?

What would you like to adjust?
```

**Update screening-criteria.json based on feedback**

**Example update:**
```json
{
  "special_rules": [
    {
      "name": "scaffold_analogs",
      "condition": "mentions target scaffold AND (analog OR derivative OR synthesized)",
      "action": "add 3 points"
    }
  ],
  "paper_types": {
    "primary_research": 3,
    "methods": 2,
    "review": 0  // Changed from 1
  }
}
```

#### Step 5: Re-test Until Satisfied

**Re-score test papers with updated rubric**

**Show new results:**
```
UPDATED RUBRIC TEST RESULTS (5 papers):

✓ PMID 12345678: Score 9 → relevant (user: relevant) ✓
✓ PMID 23456789: Score 7 → relevant (user: relevant) ✓ (FIXED!)
✓ PMID 34567890: Score 8 → relevant (user: relevant) ✓
✓ PMID 45678901: Score 3 → not_relevant (user: not_relevant) ✓
✓ PMID 56789012: Score 5 → not_relevant (user: not_relevant) ✓ (FIXED!)

Accuracy: 100% (5/5 correct) ✓
Target: ≥80% ✓

Rubric is ready for bulk screening!
```

**If accuracy ≥80%:** Proceed to bulk screening
**If <80%:** Continue iterating

### Phase 3: Bulk Screening

**Once rubric validated on test set:**

1. **Run on full PubMed search results**
2. **Save all abstracts to abstracts-cache.json:**
```json
{
  "10.1234/example": {
    "pmid": "12345678",
    "title": "Paper title",
    "abstract": "Full abstract text...",
    "fetched": "2025-10-11T16:00:00Z"
  }
}
```

3. **Score all papers, save to papers-reviewed.json:**
```json
{
  "10.1234/example": {
    "pmid": "12345678",
    "status": "relevant",
    "score": 9,
    "source": "pubmed_search",
    "timestamp": "2025-10-11T16:00:00Z",
    "rubric_version": "1.0.0"
  }
}
```

4. **Generate summary report:**
```
Screened 127 papers using validated rubric:
- Highly relevant (≥8): 12 papers
- Relevant (7): 18 papers
- Possibly relevant (5-6): 23 papers
- Not relevant (<5): 74 papers

All abstracts cached for re-screening.
Results saved to papers-reviewed.json.

Review offline and provide feedback if any misclassifications found.
```

### Phase 4: Offline Review & Re-screening

**User reviews papers offline, identifies issues:**

```
User: "I reviewed the results. Three papers were misclassified:
- PMID 23456789 scored 4 but is actually relevant (discusses scaffold analogs)
- PMID 34567890 scored 8 but not relevant (wrong target)
- PMID 45678901 scored 6 but is highly relevant (has key dataset)

Can we update the rubric?"
```

**Update rubric based on feedback:**
1. Analyze why misclassifications occurred
2. Propose rubric adjustments
3. Re-score ALL cached papers with new rubric
4. Show diff of what changed

**Re-screening workflow:**
```bash
# Load all abstracts from abstracts-cache.json
# Apply updated rubric to each
# Generate change report

RUBRIC UPDATE: v1.0.0 → v1.1.0

Changes:
- Added "derivative" to scaffold_analogs rule
- Increased dataset bonus from +1 to +2 pts

Re-screening 127 cached papers...

Status changes:
  not_relevant → relevant: 3 papers
    - PMID 23456789 (score 4→7)
    - PMID 45678901 (score 6→8)
  relevant → not_relevant: 1 paper
    - PMID 34567890 (score 8→6)

Updated papers-reviewed.json with new scores.
New summary:
- Highly relevant: 13 papers (+1)
- Relevant: 19 papers (+1)
```

## File Structure

```
research-sessions/YYYY-MM-DD-topic/
├── screening-criteria.json      # Rubric definition (weights, rules, version)
├── test-set.json               # Ground truth papers used for validation
├── abstracts-cache.json        # Full abstracts for all screened papers
├── papers-reviewed.json        # Simple tracking: DOI, score, status
└── rubric-changelog.md         # History of rubric changes and why
```

## Integration with Other Skills

**Before evaluating-paper-relevance:**
- Use this skill to build and validate rubric first
- Creates screening-criteria.json and abstracts-cache.json
- Then use evaluating-paper-relevance with validated rubric

**When creating helper scripts:**
- Use screening-criteria.json to parameterize scoring logic
- Reference abstracts-cache.json to avoid re-fetching
- Easy to update rubric without rewriting script

**During answering-research-questions:**
- Build rubric in initialization phase (after Phase 1: Parse Query)
- Validate on test set before bulk screening
- Save rubric with research session for reproducibility

## Rubric Design Patterns

### Pattern 1: Additive Scoring (Default)

```python
score = 0
score += count_keyword_matches(abstract, keywords)  # 0-3 pts
score += count_data_type_matches(abstract, data_types)  # 0-4 pts
score += specificity_score(paper_type)  # 0-3 pts

# Apply special rules
if matches_special_rule(abstract, rule):
    score += rule['bonus_points']

return score
```

### Pattern 2: Domain-Specific Rules

**Medicinal chemistry:**
```json
{
  "special_rules": [
    {
      "name": "scaffold_analogs",
      "keywords": ["target_scaffold", "analog|derivative|series"],
      "bonus": 3
    },
    {
      "name": "sar_data",
      "keywords": ["IC50|Ki|MIC", "structure-activity|SAR"],
      "bonus": 2
    }
  ]
}
```

**Genomics:**
```json
{
  "special_rules": [
    {
      "name": "public_data",
      "keywords": ["GEO:|SRA:|ENA:", "accession"],
      "bonus": 3
    },
    {
      "name": "differential_expression",
      "keywords": ["DEG|differentially expressed", "RNA-seq|microarray"],
      "bonus": 2
    }
  ]
}
```

**Computational methods:**
```json
{
  "special_rules": [
    {
      "name": "code_available",
      "keywords": ["github|gitlab|bitbucket", "code available|software"],
      "bonus": 3
    },
    {
      "name": "benchmark",
      "keywords": ["benchmark|comparison", "performance|accuracy"],
      "bonus": 2
    }
  ]
}
```

## Common Mistakes

**Skipping test-driven validation:** Bulk screen without testing rubric → Many misclassifications, wasted time
**Not caching abstracts:** Re-fetch from PubMed when rescreening → Slow, hits rate limits
**No ground truth testing:** Can't measure rubric accuracy → Don't know if it's working
**Too few test papers:** Test on 2-3 papers → Rubric overfits, doesn't generalize
**Too complex rubric:** Boolean logic with 10+ rules → Hard to debug, update, explain
**Not documenting changes:** Update rubric without tracking why → Can't reproduce, learn from mistakes
**Setting threshold too high:** Require 95% accuracy → Iterate forever, diminishing returns
**Not saving rubric with session:** Rubric lost when session ends → Can't reproduce screening

## Success Criteria

Rubric is ready when:
- ≥80% accuracy on test set (5-10 ground truth papers)
- User confident rubric captures edge cases
- Special rules documented for domain-specific patterns
- All files created (screening-criteria.json, test-set.json, abstracts-cache.json)
- Ready to run bulk screening

## Quick Reference

| Task | File | Contents |
|------|------|----------|
| Define rubric | screening-criteria.json | Keywords, weights, special rules |
| Test rubric | test-set.json | Ground truth papers with user judgments |
| Cache abstracts | abstracts-cache.json | Full abstract text for re-screening |
| Track results | papers-reviewed.json | DOI, score, status, rubric version |
| Document changes | rubric-changelog.md | History of updates and rationale |

## Example Session

```
Agent: "I'll help you build a screening rubric. Let's start with some questions about what makes papers relevant..."

[Brainstorming phase - ask 5 question categories]

User: "I'm looking for papers on tuberculosis drug resistance with MIC data for bedaquiline and clofazimine. Papers about analogs are also relevant."

Agent: "Got it. Here's the initial rubric:
- Keywords: tuberculosis, drug resistance, bedaquiline, clofazimine (0-3 pts)
- Data: MIC values, IC50, in vitro activity (0-4 pts)
- Specificity: Primary research (0-3 pts)
- Special rule: If mentions target drugs + 'analog/derivative' → +3 bonus pts
- Threshold: ≥7 = relevant

Does this look right?"

User: "Yes, let's test it."

Agent: "I'll search PubMed for 20 papers and show you abstracts to classify..."

[Shows 10 abstracts, user classifies them]

Agent: "Testing rubric on your classifications...
Accuracy: 70% (7/10 correct)
- 2 false negatives (missed relevant papers)
- 1 false positive (marked review as relevant)

False negative example: Paper discusses 'derivatives of bedaquiline' but scored only 5 pts because didn't explicitly say 'analog'.

Suggestion: Add 'derivative' and 'compound' to special rule trigger terms?"

User: "Yes, and lower review paper points."

Agent: "Updated rubric. Re-testing...
Accuracy: 90% (9/10 correct) ✓

Ready to run bulk screening on 127 papers?"

User: "Yes, go ahead."

Agent: [Screens 127 papers, saves results]

"Done! Found 18 relevant papers. All abstracts cached for re-screening.
Review offline and let me know if any misclassifications."

[Later...]

User: "Found 2 misclassifications. Can we update the rubric?"

Agent: "Sure! What did I miss?"

User: "PMID 12345 discusses pretomanid combination therapy with bedaquiline - should be relevant."

Agent: "Got it. Adding 'combination therapy' as related term with +2 bonus pts.
Re-screening all 127 cached papers...
Status changes: 3 papers now relevant (including PMID 12345).
Updated papers-reviewed.json."
```

## Next Steps

After building rubric:
- Use for bulk screening in evaluating-paper-relevance
- Parameterize helper scripts with screening-criteria.json
- Update rubric as you discover edge cases
- Re-screen cached papers when criteria change
- Document rubric in research session README for reproducibility
