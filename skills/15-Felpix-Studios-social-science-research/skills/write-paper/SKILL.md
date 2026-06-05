---
name: write-paper
description: >-
  Draft a full academic paper manuscript from analysis outputs, project spec, and lit review. Make sure to use this skill whenever the user wants to turn completed analysis into a written paper — not to run analysis or review existing writing. Triggers include: "write the paper", "draft the manuscript", "write up the results", "start the paper", "turn my results into a paper", "write the introduction", "draft the empirics section", "I have my results, now write the paper", "help me write this up", "write the abstract", or any request to produce academic prose from existing research outputs.
argument-hint: "[paper title, research question, or 'from spec']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Task"]
---

# Write Paper Draft

Draft an academic manuscript from existing analysis outputs. Follows propose-first — the outline is always shown for approval before writing begins.

**Input:** `$ARGUMENTS` — a paper title, research question, or `from spec` to read from `quality_reports/specs/`.

---

## Step 1: Orient

Read project context:
- `CLAUDE.md` — project name, author, institution
- Most recent file in `quality_reports/specs/` — research question and identification strategy
- Most recent file in `quality_reports/lit_review_*.md` — related literature (if it exists)
- Most recent file in `quality_reports/research_ideation_*.md` — hypotheses (if it exists)

If no spec exists, ask the user for the core research question before proceeding.

---

## Step 2: Inventory Analysis Outputs

Glob for available outputs:
- `output/tables/**/*.tex` — regression tables
- `output/tables/**/*.html` — HTML table versions
- `output/figures/**/*.pdf`, `output/figures/**/*.png` — figures
- `output/**/*.rds`, `output/**/*.pkl`, `output/**/*.parquet` — saved objects

List what exists. Note any gaps (e.g., "no summary statistics table found").

---

## Step 3: Propose Outline (WAIT FOR APPROVAL)

Draft a paper outline using standard social science structure:

```
1. Abstract
2. Introduction
3. Related Literature
4. Data and Institutional Background
5. Empirical Strategy
6. Results
7. Robustness and Extensions
8. Conclusion
References
```

Present the outline with a one-sentence description of each section's content, linking specific output files to each section (e.g., "Table 2 → Section 6, Results"). **Do NOT start writing until the user approves the outline or requests changes.**

---

## Step 4: Draft Section by Section

Write in this order (minimizes backtracking):

1. **Data section** — describe the dataset, summary statistics. Reference `output/tables/summary_stats.tex` if it exists.
2. **Empirical Strategy** — describe the identification approach from the research spec.
3. **Results** — one paragraph per main finding. Reference each table/figure with `\input{}` or `\includegraphics{}` — do NOT copy table content inline.
4. **Robustness** — brief description of robustness checks, referencing additional output files.
5. **Literature** — synthesize from the lit review document if one exists.
6. **Introduction** — write after results are known. State the question, preview the findings, and map the paper.
7. **Abstract** — write last: one sentence each for motivation, question, method, finding, and implication.
8. **Conclusion** — summarize and state limitations and next steps.

---

## Step 5: Save the Draft

Save to `manuscripts/[project-name]-draft.tex` (or `.qmd` if the user prefers Quarto).

Create `manuscripts/` directory if it does not exist.

Use `\input{}` for tables and `\includegraphics{}` for figures — reference the actual files in `output/`, do not embed content directly.

---

## Step 6: Run Domain Review

After saving the draft, launch the `domain-reviewer` agent via Task:

Task prompt: "Review the draft at manuscripts/[filename] for argument structure, identification assumptions, and citation fidelity. Check that the identification strategy is clearly stated, assumptions are explicit, and all cited tables/figures exist in output/."
Task agent: domain-reviewer

Wait for the review to complete, then present the findings to the user.

---

## Step 7: Recommend Next Steps

Inform the user:
- **`/review-paper`** — for a full top-journal-style review of the manuscript
- **`/validate-bib`** — to check all citations are in the bibliography
- **`/quality-gate`** — to verify every claim in the paper is backed by an output file

---

## Key Rules

- **Propose outline first.** Never start writing without outline approval.
- **Reference, don't embed.** Tables and figures go in `output/`; the paper references them by path.
- **No fabrication.** Only write results that exist in output files. If a number isn't in `output/`, flag it rather than guessing.
- **Report only.** The domain-reviewer agent proposes fixes; you apply them only after user approval.
