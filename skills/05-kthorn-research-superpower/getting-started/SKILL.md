---
name: Getting Started with Research Superpowers
description: Introduction to literature search & review skills - systematic paper finding, screening, extraction, and citation traversal
when_to_use: At start of each Claude Code session. When user asks literature search questions. When searching scientific literature. When reviewing papers or citations.
version: 1.1.0
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

# Getting Started with Research Superpowers

Research Superpowers gives Claude Code systematic workflows for **literature searching and review**.

**Focus:** Finding, screening, and extracting data from published papers. NOT for analyzing experimental data or designing experiments.

## What You Can Do

Use these skills for **systematic literature reviews**:

- **Search literature** - PubMed and Semantic Scholar integration
- **Build screening rubrics** - Define and test relevance criteria collaboratively
- **Screen papers** - Two-stage screening (abstract → deep dive) with scoring
- **Extract data** - Find specific methods, results, measurements from papers
- **Traverse citations** - Smart backward/forward citation following
- **Large-scale screening** - Parallel subagent processing for 50+ papers
- **Track findings** - Organized research sessions with summaries, PDFs, and deduplication

## Available Skills

**Literature Search & Review Skills** (`skills/research/`)
- **answering-research-questions** - Main orchestration workflow (search → screen → extract → synthesize)
- **building-screening-rubrics** - Collaborative rubric design with test-driven refinement
- **searching-literature** - PubMed search with keyword optimization
- **evaluating-paper-relevance** - Two-stage screening (abstract → deep dive)
- **subagent-driven-review** - Parallel screening for large searches (50+ papers)
- **checking-chembl** - Check if medicinal chemistry papers have curated SAR data in ChEMBL
- **traversing-citations** - Semantic Scholar citation network traversal
- **finding-open-access-papers** - Unpaywall API to find free versions of paywalled papers
- **cleaning-up-research-sessions** - Safe cleanup of intermediate files after research complete

## Basic Workflow

When user asks a **literature search question**:

1. **Read answering-research-questions skill** - Main orchestration
2. **Announce**: "I'm using the Answering Research Questions skill"
3. **Parse query** - Extract keywords, data types, constraints
4. **Create research folder** - Propose name, initialize tracking
5. **Optional: Build rubric** - For large searches (50+ papers), use building-screening-rubrics skill
6. **Search → Screen → Extract → Traverse** - Follow the workflow
7. **Check in regularly** - Every 10 papers, checkpoint every 50

## Research Session Folders

Each query creates a folder in `research-sessions/`:

```
research-sessions/YYYY-MM-DD-query-description/
├── SUMMARY.md              # Main findings
├── papers-reviewed.json    # Deduplication tracking (DOI → status)
├── papers/                 # Downloaded PDFs and supplementary data
└── citations/              # Citation graph tracking
```

## Core Principles

For **systematic literature review**:

- **Precision over breadth** - Find papers with specific data you need, not just topical matches
- **Test-driven screening** - Build and validate rubrics before bulk processing
- **Smart citation following** - Only traverse relevant citations to avoid exponential explosion
- **Deduplicate aggressively** - Track ALL reviewed papers by DOI (even non-relevant)
- **Cache abstracts** - Save for re-screening when rubrics change
- **Report progress** - Update user every 10 papers as work proceeds
- **Checkpoint frequently** - Ask to continue or stop every 50 papers
- **Reproducible** - Save rubrics, queries, and methodology with research sessions

## API Information

**PubMed E-utilities** (no key required):
- Search: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- Details: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi`
- Full text: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`

**Semantic Scholar** (free tier works, optional key for higher limits):
- Paper: `https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}`
- References: `https://api.semanticscholar.org/graph/v1/paper/{id}/references`
- Citations: `https://api.semanticscholar.org/graph/v1/paper/{id}/citations`

## Finding Skills

Use the find-skills script to search for relevant skills:

```bash
# From project directory
./scripts/find-skills              # List all skills
./scripts/find-skills literature   # Search for "literature"
./scripts/find-skills 'cite|ref'   # Regex search
```

## Remember

- **Always start** by reading the relevant research skill
- **Announce skill usage** when you begin
- **Track everything** in the research folder
- **Check in with user** regularly during long searches
- **Deduplicate** using papers-reviewed.json (DOI as key)
