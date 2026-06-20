---
name: literature-survey-generator
description: >-
  Generate a complete academic literature survey from scratch using multi-agent
  orchestration. Searches academic databases (OpenAlex, CrossRef, Unpaywall),
  downloads PDFs, builds BibTeX, drafts a LaTeX review, compiles it, reviews for
  quality, and revises based on feedback — all automated. Use this skill whenever
  the user asks to "generate a literature review", "write a survey paper",
  "review recent papers on [topic]", "create a survey of [field]", "综述",
  "文献综述", "survey papers in top journals", or wants a multi-agent pipeline
  to produce a publishable-quality literature review. Also trigger when the user
  wants to search multiple journals for papers on a topic and synthesize findings
  into a structured document. Works for any academic field but optimized for
  economics journals.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - WebFetch
  - WebSearch
  - TaskCreate
  - TaskUpdate
  - TaskList
---

# Literature Survey Generator

A multi-agent, multi-phase pipeline that produces a complete academic literature
survey in LaTeX with BibTeX — from search to final compiled PDF.

## When to Use

- User wants a literature review on a topic across specific journals
- User wants to find and synthesize recent papers in a field
- User asks for a survey of Top 5 / Top Field journals on a topic
- User wants automated paper search → download → review writing

## Overview

The pipeline has 4 phases, each using parallel subagents where possible:

```
Phase 1: SEARCH (parallel per journal)
    ↓ search_{journal}.json files
Phase 2: PROCESS (3 parallel agents)
    ↓ references.bib + paper_summaries.md + pdfs/
Phase 3: DRAFT (1 agent + compilation)
    ↓ survey.tex → survey.pdf
Phase 4: REVIEW & REVISE (sequential)
    ↓ review_report.md → survey_v2.tex → survey_v2.pdf
```

## Execution Instructions

### Step 0: Setup

1. Parse the user's request to extract:
   - **Topic**: The search query (e.g., "networks", "behavioral economics")
   - **Journals**: Which journals to search (default: Top 5 Economics)
   - **Year range**: Publication year(s) (default: current year)
   - **Output format**: LaTeX (default), Markdown, or both

2. Create working directory:
   ```
   agent_tasks/{topic_slug}_{YYYYMMDDHH}/
   ```

3. Write `plan.md` to the working directory documenting the execution plan.

4. Set up task tracking with TaskCreate for the 4 phases.

### Step 1: Phase 1 — Parallel Journal Search

Launch **one subagent per journal** (up to 10 in parallel). Each agent:

1. Queries **OpenAlex API** with the journal's source ID and topic keyword
2. Queries **CrossRef API** with the journal's ISSN and topic keyword
3. Deduplicates results by DOI
4. Saves to `search_{journal_abbrev}.json`

**Agent prompt template:**
```
Search for papers about "{TOPIC}" published in {JOURNAL_NAME} in {YEAR}.

1. OpenAlex API (source ID: {OPENALEX_ID}):
   curl -s "https://api.openalex.org/works?filter=primary_location.source.id:{OPENALEX_ID},default.search:{TOPIC},publication_year:{YEAR}&per_page=50&mailto=xueheng@mail.sysu.edu.cn"

2. CrossRef API (ISSN: {ISSN}):
   curl -s "https://api.crossref.org/journals/{ISSN}/works?query={TOPIC}&filter=from-pub-date:{YEAR}-01-01&rows=50&mailto=xueheng@mail.sysu.edu.cn"

Extract: title, authors, doi, year, cited_by, pdf_urls, abstract (from inverted index), openalex_id.
Deduplicate by DOI. Save to: {WORKDIR}/search_{ABBREV}.json
```

**Key journal identifiers** (verify OpenAlex IDs via API before use):

| Journal | ISSN | OpenAlex ID |
|---------|------|-------------|
| American Economic Review | 0002-8282 | S23254222 |
| Econometrica | 0012-9682 | S95464858 |
| Journal of Political Economy | 0022-3808 | (verify via API) |
| Quarterly Journal of Economics | 0033-5533 | S203860005 |
| Review of Economic Studies | 0034-6527 | (verify via API) |

For non-Top-5 journals, first look up the OpenAlex source ID:
```bash
curl -s "https://api.openalex.org/sources?search={journal+name}&mailto=xueheng@mail.sysu.edu.cn"
```

**Wait for all search agents to complete before proceeding.**

After all agents complete, do a quick tally: read each `search_*.json` and count papers. If total < 3, consider broadening the search terms or year range. If total > 30, the topic may need narrowing — flag this to the user.

### Step 2: Phase 2 — Process (3 Parallel Agents)

Launch these 3 agents simultaneously:

#### Agent A: PDF Downloader
For each paper with a DOI:
1. Query Unpaywall: `https://api.unpaywall.org/v2/{DOI}?email=xueheng@mail.sysu.edu.cn`
2. Check `best_oa_location.url_for_pdf` and all `oa_locations[].url_for_pdf`
3. If PDF URL found, download to `pdfs/{safe_filename}.pdf`
4. Verify each download is a real PDF (file > 10KB, starts with %PDF)
5. Save `pdfs/download_report.md`

#### Agent B: BibTeX Builder
For each DOI:
```bash
curl -sL -H "Accept: application/x-bibtex" "https://doi.org/{DOI}"
```
- Clean citation keys to `{firstauthor}{year}{keyword}` format
- Add foundational references cited in the introduction (if known)
- Save to `references.bib`

#### Agent C: Summary Extractor
For each paper:
1. Read abstracts from `search_*.json` files
2. For missing/truncated abstracts, query OpenAlex for full inverted abstract
3. As fallback, query Semantic Scholar (with 3s sleep between calls)
4. Save `paper_summaries.md` with per-paper sections:
   - Title, Authors, Journal, DOI, Citations, Full Abstract, Key Themes
5. Save `all_papers.json` (consolidated, enriched metadata)

**Wait for all 3 agents to complete before proceeding.**

### Step 3: Phase 3 — Draft LaTeX Survey

Launch 1 agent to write the survey. The agent reads:
- `paper_summaries.md` (content source)
- `references.bib` (citation keys)

**Survey structure** (adapt based on paper count and topics):

```latex
\documentclass[12pt]{article}
\usepackage{amsmath,amssymb,natbib,geometry,hyperref,booktabs,setspace,array}
\bibliographystyle{plainnat}

1. Title, Author, Abstract (150-200 words)
2. Introduction
   - Motivation for the topic
   - Selection methodology (how papers were found)
   - Brief overview of themes
   - Positioning relative to existing surveys
3. Summary Table (booktabs: Authors, Journal, Title, Type, Key Aspect)
4-6. Thematic Sections (group papers by theme, not by journal)
   - Each paper: 2+ paragraphs of substantive discussion
   - Critical engagement: limitations, open questions
   - Cross-references between papers where relevant
7. Methodological Advances (compare approaches across papers)
8. Conclusion (synthesis, gaps, future directions)
```

**Important instructions for the drafting agent:**
- Use `\citet{}` for in-text citations, `\citep{}` for parenthetical
- Be transparent about papers with tangential relevance to the topic
- Add critical engagement (limitations, open questions) for at least 3 papers
- Verify all `\cite` keys match entries in `references.bib`
- Target 8-15 pages when compiled

After the agent saves `survey.tex`, **compile it**:
```bash
cd {WORKDIR}
pdflatex -interaction=nonstopmode survey.tex
bibtex survey
pdflatex -interaction=nonstopmode survey.tex
pdflatex -interaction=nonstopmode survey.tex
```

Check for errors. Fix any compilation issues before proceeding.

### Step 4: Phase 4 — Review & Revise

#### 4a: Review Agent
Reads `survey.tex`, `paper_summaries.md`, `references.bib`.
Writes `review_report.md` covering:

1. **Content Accuracy**: Does each paper description match its abstract?
2. **Structure**: Is the grouping logical? Are transitions smooth?
3. **Writing Quality**: Academic tone, citation style consistency
4. **Completeness**: Are all papers discussed substantively?
5. **Specific Revisions**: 5-10 actionable changes with priority (HIGH/MEDIUM/LOW)
6. **Overall Score**: X/10 with top 3 strengths and weaknesses

#### 4b: Revision Agent
Reads `review_report.md`, `survey.tex`, `paper_summaries.md`.
Implements ALL revision suggestions. Saves to `survey_v2.tex`.

**Final compilation:**
```bash
cd {WORKDIR}
pdflatex -interaction=nonstopmode survey_v2.tex
bibtex survey_v2
pdflatex -interaction=nonstopmode survey_v2.tex
pdflatex -interaction=nonstopmode survey_v2.tex
```

Verify zero errors in the final PDF.

### Step 5: Deliver

Report to the user:
- Total papers found per journal
- PDF download success rate
- Review score and key improvements made
- Final PDF page count and location
- List all deliverables in the working directory

## Critical Rules

1. **File handoff, not context handoff**: Every agent saves its output to a file.
   Never pass large content back to the main agent. Agents return only a status
   summary (paper count, success/failure, file paths).

2. **Parallel where possible, sequential where required**: Phases 1 and 2 are
   parallel internally. Phase 3 depends on Phase 2 outputs. Phase 4 is sequential
   (review before revision).

3. **All agents get `mode: auto`**: Subagents need Bash, Read, Write, Edit access
   to do their work without permission prompts.

4. **Verify before proceeding**: Always compile LaTeX and check for errors between
   phases. Don't hand broken output to the next phase.

5. **Be transparent about relevance**: Not every paper returned by keyword search
   is centrally about the topic. The survey should acknowledge varying degrees of
   relevance rather than force-fitting papers into the narrative.

6. **Respect API rate limits**: OpenAlex (add mailto), CrossRef (add mailto),
   Semantic Scholar (3s between calls), arXiv (3s between calls).

## Customization Points

- **Different journals**: Change the journal table. For any journal, look up its
  OpenAlex source ID first.
- **Different output format**: Swap LaTeX template for Markdown if user prefers.
- **Broader search**: Add NBER, SSRN, arXiv searches in Phase 1 using the
  `academic-paper-search` skill's API patterns.
- **Deeper review**: Add a second review-revise cycle if the first review score < 7.
- **Zotero import**: After Phase 2, optionally import all papers via `zotero_add_by_doi`.

## File Structure (Final)

```
agent_tasks/{topic}_{timestamp}/
├── plan.md                  # Execution plan
├── search_aer.json          # Per-journal search results
├── search_ecma.json
├── search_jpe.json
├── search_qje.json
├── search_restud.json
├── all_papers.json           # Consolidated metadata
├── paper_summaries.md        # Full abstracts + key themes
├── references.bib            # Complete BibTeX database
├── pdfs/                     # Downloaded open-access PDFs
│   ├── *.pdf
│   └── download_report.md
├── survey.tex                # Initial draft
├── survey.pdf                # Initial compilation
├── review_report.md          # Quality review
├── survey_v2.tex             # Revised draft
└── survey_v2.pdf             # Final PDF (deliverable)
```
