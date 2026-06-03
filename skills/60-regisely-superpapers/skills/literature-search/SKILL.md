---
name: literature-search
description: Use when the user asks to search for papers, review literature, find references on a topic, verify a paper exists, or build a bibliography. Enforces web verification of every citation via web fetch to prevent hallucinated references.
---

# Literature Search

## Overview

This skill searches academic literature with strict web verification of every result. The primary anti-pattern it prevents is hallucination of citations — plausible-sounding papers that do not exist. Every paper returned must be fetched from the web and confirmed to be real before it enters the output.

## When to Use

- "What does the literature say about X?"
- "Find papers on Y"
- "Who wrote the seminal paper on Z?"
- Building a reference list for a new project
- Verifying that a specific paper exists
- Checking the correct citation details for a paper the user remembers partially

## Modes

This skill operates in two modes. The caller specifies which.

### Gap-check mode
Used during `brainstorm` to verify a research gap exists. Scope: 1-2 targeted queries, 5-8 results maximum, no bibliography file output. Web-verify every result (the anti-hallucination rule still applies). Output the standard markdown table but do not populate `references.bib`.

### Full mode
Used during `execute-plan`'s Literature phase. Run all Mandatory Steps below. Curate 15-30 references, bias toward target journals, populate `references.bib` via `citation-management`, produce literature notes. This is the default when no mode is specified.

## Mandatory Steps

1. **Identify the research field from context.** Resolve `CLAUDE.superpapers.md` by reading it from the current working directory, or walking up parent directories until found. If the file contains a `field` entry, use it. Otherwise infer from the project abstract or ask the user directly. The field determines which databases to prioritize.

2. **Choose databases based on the field:**
   - **Core (any field):** Google Scholar, Web of Science, JSTOR, Semantic Scholar
   - **Economics and finance:** SSRN, NBER, RePEc, ScienceDirect
   - **Health and medicine:** PubMed, Cochrane Library
   - **Political science and sociology:** JSTOR, SAGE Journals
   - **Physical and computer sciences:** arXiv, ACM Digital Library, IEEE Xplore

3. **Search with specific queries, not broad terms.** Include methodology keywords when relevant. For example, prefer `"difference-in-differences" minimum wage employment` over `minimum wage`.

4. **For every candidate paper, web-fetch the landing page.** Confirm title, authors, year, and DOI from the authoritative source. If the paper cannot be fetched and verified, mark it as `[unverified]` and exclude it from the final list.

5. **Output a markdown table** with columns: `Authors (Year)`, `Title`, `Venue`, `DOI`, `Relevance`. Keep the relevance column to a single line of substantive justification.

6. **Curate, do not dump.** Prioritize seminal works, recent papers (last five years), highly cited results, and papers that directly address the user's question. Aim for 8 to 15 results per query unless the user asks for more.

7. **Bias toward the user's target journals.** Use the target journal list resolved from `CLAUDE.superpapers.md` in step 1, or ask the user if the file was absent or the field was unset. Ensure a substantial share of cited references come from those journals or closely related ones in the same field tier. Prioritize very recent publications (last three to five years) in those outlets — reviewers expect to see that the authors know the journal's recent conversation. If a search returns few results from the target journals, widen to journals of similar scope and rank, but flag the gap to the user.

## Output Format

```markdown
| Authors (Year) | Title | Venue | DOI | Relevance |
|---|---|---|---|---|
| Card & Krueger (1994) | Minimum Wages and Employment | American Economic Review | 10.xxxx/xxxxx | Seminal DiD on minimum wage; identifies employment effects |
| Dube et al. (2010) | Minimum Wage Effects Across State Borders | Review of Economics and Statistics | 10.xxxx/xxxxx | Border-pair design, finds no disemployment effect |
```

Replace example DOIs with real verified values. Never leave placeholder DOIs in the final output.

## Anti-Patterns

- **Primary: fabricating a paper that does not exist.** Inventing "Smith (2021), _Some Plausible Title_, Journal of Plausible Results" without verification.
- Citing from memory without web fetch
- Listing 30 papers without curation of relevance
- Including working papers alongside published versions without distinction
- Confusing a journal article with a book chapter or conference paper
- Listing papers outside the user's field
- Returning results without DOIs or stable URLs
- Trusting a paper's existence because a well-known author "probably wrote it"
- Ignoring the target journal list when curating results — the bibliography should reflect the journal's recent conversation

## Verification Before Completion

- [ ] Every paper in the final list was fetched via web in this session
- [ ] Every paper has a verified DOI or stable URL
- [ ] No `[unverified]` entries in the final table
- [ ] Field-appropriate databases were used
- [ ] Relevance column is populated with substantive reasoning
- [ ] Results are curated, not dumped
- [ ] Working papers distinguished from published versions
- [ ] Substantial share of references come from the user's target journals or closely related outlets
- [ ] Recent papers (last 3-5 years) from target journals are well represented
