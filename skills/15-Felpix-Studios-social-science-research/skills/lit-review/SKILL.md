---
name: lit-review
description: >-
  Structured literature review using a parallel fleet of Librarian agents. Searches top journals, working paper repositories (NBER, SSRN, IZA), and traces citation chains from key papers. Make sure to use this skill whenever the user wants to survey existing research on a topic — not to find datasets or write a paper. Triggers include: "review the literature", "find related papers", "what's been done on X", "search for papers on", "do a lit review", "find papers about", "what papers should I cite", "who has written about this", "survey the literature", "find prior work on", or any request to locate and summarize academic publications on a topic.
argument-hint: "[topic, research question, or anchor paper title]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "WebSearch", "WebFetch", "Task", "AskUserQuestion"]
---

# Literature Review

Conduct a systematic literature review using a parallel fleet of Librarian agents, each searching a different angle. Citation chains from anchor papers are the highest-yield search vector and always run when anchor papers are available.

**Input:** `$ARGUMENTS` — a topic, research question, or the title of a known key paper.

---

## Step 1: Orient and Gather Context

1. Read `quality_reports/project_spec_*.md` or `quality_reports/research_*.md` if they exist — extract the research question and identification strategy.
2. Check `references/papers/` — list any PDFs already on hand.
3. Read the project `.bib` file (`Bibliography_base.bib` or any `.bib` at project root) — extract paper titles and authors already known.
4. Read `references/domain-profile.md` if it exists — get the field's journal list and key researchers.
5. Identify **anchor papers**: the 1–3 most central known papers (from existing bib or supporting docs). These seed the citation chain search.

If `references/domain-profile.md` does not exist, use AskUserQuestion to determine the field:
- header: "Field"
- question: "What field is this research in? This determines which journals and repositories the librarian agents search."
- options:
  - label: "Economics", description: "AER, QJE, Econometrica, JPE, ReStud + NBER/IZA"
  - label: "Political Science", description: "APSR, AJPS, JOP, CPS, World Politics"
  - label: "Sociology", description: "ASR, AJS, Social Forces, Demography"
  - label: "Public Health", description: "NEJM, Lancet, JAMA, AJE"

---

## Step 2: Assign Librarians

Dispatch **3–5 Librarian agents** in parallel using `Task`. Each gets a specific search angle, the topic, and the anchor papers (if any).

### Always dispatch (3 minimum):

**Librarian 1 — Top Journals:**
```
Task prompt: "You are a Librarian agent. Topic: [topic]. Search angle: Top Journals.
Field: [field from domain-profile or user answer].
Top journals to search: [list from domain-profile, or infer for field].
Anchor papers (for context only): [list].
Find the 8-12 most relevant published papers from the past 10 years.
For seminal papers, go back further. Follow the Librarian agent instructions."
```

**Librarian 2 — Working Papers (NBER + SSRN + IZA):**
```
Task prompt: "You are a Librarian agent. Topic: [topic]. Search angle: NBER + SSRN + IZA.
Search NBER (site:nber.org), SSRN (site:ssrn.com), and IZA (site:iza.org/publications/dp)
for recent working papers on this topic. Find 6-10 working papers.
Flag all as working papers. Follow the Librarian agent instructions."
```

**Librarian 3 — Secondary Journals + Adjacent Fields:**
```
Task prompt: "You are a Librarian agent. Topic: [topic]. Search angle: Secondary Journals.
Field: [field]. Secondary journals: [list from domain-profile, or search broadly].
Also search adjacent fields that might have relevant methodology or findings.
Find 5-8 papers. Follow the Librarian agent instructions."
```

### Add when anchor papers are available (dispatch 4th and 5th):

**Librarian 4 — Backward Citation Chain:**
```
Task prompt: "You are a Librarian agent. Topic: [topic]. Search angle: Citation Chain — BACKWARD.
Anchor papers: [title, authors, year for each].
For each anchor paper: use Semantic Scholar API to find what it cites.
Extract 8-12 most relevant references from the combined reference lists.
These are the papers the anchor papers build on — the theoretical and empirical foundations.
Follow the Librarian agent instructions for citation chain search."
```

**Librarian 5 — Forward Citation Chain:**
```
Task prompt: "You are a Librarian agent. Topic: [topic]. Search angle: Citation Chain — FORWARD.
Anchor papers: [title, authors, year for each].
For each anchor paper: use Semantic Scholar API to find who cites it.
Focus on papers published in the last 3 years — these represent the active research frontier.
Find 8-12 most relevant papers that cite the anchor papers.
Follow the Librarian agent instructions for citation chain search."
```

> **Why citation chains beat keyword search:** The papers that cite your anchor papers are by definition working on the same problem. The papers your anchor papers cite are the foundations your paper must engage with. These vectors find papers that keyword searches miss entirely.

---

## Step 3: Consolidate and Deduplicate

After all Librarians complete:

1. Merge all paper lists from all Librarians.
2. Deduplicate: if the same paper appears from multiple sources, keep one entry and note "Found via: [multiple sources]" — cross-source confirmation increases confidence.
3. Flag any papers marked `FLAG` by a Librarian — do not include in final BibTeX without manual verification.
4. Total target: 20–40 papers (quality over quantity).

---

## Step 4: Organize Thematically

Sort papers into these categories:

- **Theoretical Contributions** — models, mechanisms, frameworks
- **Empirical Findings** — key results, effect sizes, data used
- **Methodological Innovations** — estimators, identification strategies, inference
- **Open Debates** — unresolved disagreements, conflicting findings

For each category, write a 2–3 paragraph synthesis (not just a list).

---

## Step 5: Identify Gaps

List 3–5 specific gaps the reviewed literature leaves open:
- Questions not asked
- Populations or contexts not studied
- Data limitations that constrained prior work
- Methodological assumptions no one has relaxed
- Conflicting findings that need resolution

For each gap: *"No paper has examined X in context Y using method Z. This matters because..."*

---

## Step 6: Save Report

Save to `quality_reports/lit_review_[sanitized_topic].md`:

```markdown
# Literature Review: [Topic]

**Date:** [YYYY-MM-DD]
**Search strategy:** [N Librarians — journals, NBER/SSRN/IZA, citation chains from: [anchor papers]]
**Papers reviewed:** N total (M published, K working papers)

## Summary

[3-paragraph overview of the state of the literature]

## Key Papers

### [Author(s) (Year)] — [Short Title]
- **Venue:** [Journal / NBER wXXXX / IZA DP XXXX]
- **Method:** [Identification strategy + data]
- **Key finding:** [Result with effect size]
- **Relevance:** [Why it matters for our question]
- **Found via:** [Librarian source]

[Repeat for all papers, ordered by relevance]

---

## Thematic Organization

### Theoretical Contributions
[Synthesis paragraph(s)]

### Empirical Findings
[Synthesis comparing results across studies]

### Methodological Innovations
[Methods relevant to our research question]

### Open Debates
[Conflicting findings and unresolved questions]

---

## Gaps and Opportunities

1. [Gap 1 — specific and actionable]
2. [Gap 2]
3. [Gap 3]

---

## Suggested Next Steps

- Papers to read in full: [list 3-5 highest priority]
- `/data-finder [topic]` — identify datasets for the priority research question
- `/validate-bib` after incorporating new citations into the manuscript

---

## BibTeX Entries

```bibtex
[all verified entries]
```

---

## Flagged Papers (Unverified — Manual Check Required)

[Papers Librarians marked FLAG — verify before citing]
```

---

## Important

- **Working papers change.** Note the date retrieved for all working papers.
- **Do not include flagged papers in the BibTeX block.** Move them to the Flagged section.
- **Citation chains are the most productive vector.** Librarians 4 and 5 often find the most important missing papers — always dispatch them when anchor papers are available.
- **Recommend `/validate-bib`** after the user incorporates new citations into the manuscript.
