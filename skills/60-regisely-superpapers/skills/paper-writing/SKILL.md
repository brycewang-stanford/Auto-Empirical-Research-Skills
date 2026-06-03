---
name: paper-writing
description: Use when drafting, rewriting, reviewing, or auditing prose for any section of an empirical academic paper (Abstract, Introduction, Methods, Data, Results, Discussion, Conclusion) or specialized output (job market paper, grant proposal, policy brief, referee response).
---

# Paper Writing

## Overview

Applies writing discipline to paper prose. Operates under `academic-baseline` — its nine principles bind every step below. Defers non-prose work to sibling skills: `tables-and-figures` for tables and figures, `citation-management` for `.bib` entries, `compile-latex` for LaTeX builds, `replication-driven-research` for reproducibility, `robustness-checks` for which checks to run, `journal-guidelines` for journal-specific formatting.

Deep material lives in `references/`; load a reference file when the task calls for it:

- `section-formulas.md` — structures for Abstract, Introduction, Methods, Data, Results, Discussion, Conclusion, and specialized outputs (JMP, grant, policy brief, referee response).
- `style-rules.md` — sentence structure, phrases to delete, word choice, voice, paragraph discipline, AI-pattern avoidance, five-pass self-check.
- `research-design-narratives.md` — how to write Methods for RCT, DiD, IV, RDD, event study, synthetic control, ML, descriptive, bunching, shift-share, structural.
- `review-checklist.md` — 3-reviewer simulation and 100-point rubric.

## When to Use

- Drafting or rewriting a section of a paper.
- Reviewing or auditing a draft with the 3-reviewer rubric.
- Writing a job market paper, grant proposal, policy brief, op-ed, or referee response.
- Tightening a working paper into a journal version.
- Removing AI-generated writing patterns from a draft.
- Any Writing-phase task dispatched by `execute-plan`.

## Mandatory Steps

1. Invoke `academic-baseline` first. Its walk-up Read loads `CLAUDE.superpapers.md`; the nine principles (especially 4, 8, 9) bind every step below.
2. Identify the task type: drafting, rewriting, reviewing, or specialized output.
3. Identify the paper type from the design spec in `docs/superpapers/specs/` when present: applied empirical, theory, mixed, structural, or descriptive. Ask the user if absent.
4. Identify the target section; load the matching formula from `references/section-formulas.md`. For Methods sections, also load `research-design-narratives.md`.
5. Apply the seven core principles below.
6. Apply the style rules in `references/style-rules.md`. Run the five-pass self-check before declaring the output done.
7. Mark author-input gaps with `[AUTHOR: description]`. Never invent numbers, citations, dataset names, institutional details, or dates.
8. Use causal language only when the design supports it; otherwise correlational. (Academic-baseline principle 4.)
9. Produce output in `paper_language` from `CLAUDE.superpapers.md`. (Academic-baseline principle 8.)
10. Defer non-prose work to the sibling skills listed in the Overview.

## The Seven Core Principles

1. **Reader First.** Write for PhD-level researchers in your discipline, not subfield specialists. Readers skim; make it easy to find the basic result fast.
2. **Triangular Style.** Most important information first, then details. No punchline endings.
3. **One Central Contribution.** State it in a paragraph. Every piece of the paper serves this one contribution.
4. **Concrete.** Say what you find, with magnitudes. "A 10% increase in X reduces Y by 3 percentage points (SE = 0.8)", not "I find interesting effects".
5. **Every Word Counts.** Cut ruthlessly. Target 30–45 pages (adapt to field and journal).
6. **Active Voice, Present Tense.** "I find…", "Smith (2019) finds…". Passive acceptable in methods descriptions and captions only.
7. **Simple > Complex.** "Use" not "utilize". "But" not "however". Simpler estimation is better than complex for the same identification.

## Field Adaptation

Read `field` from `CLAUDE.superpapers.md`:

- Economics, political science, public administration: apply all rules directly.
- Epidemiology, public health, medicine: follow CONSORT for RCTs, STROBE for observational studies; pre-registration norms (ClinicalTrials.gov, PROSPERO); defer to ICMJE via `journal-guidelines`.
- Sociology, education, psychology: some field journals expect a standalone Literature Review section; adapt the introduction formula to the target journal.
- Other fields: apply the seven principles and formulas; consult the user when a convention should override.

If `field` is unset, ask the user inline before applying field-specific advice.

## Anti-Patterns

- Inventing coefficients, sample sizes, F-statistics, hazard ratios, citations, or institutional details. Mark gaps with `[AUTHOR: …]`.
- Producing output in English when `paper_language` is another language.
- Throat-clearing openings: "It is important to note that…", "Researchers have long wondered…", "The literature has long been interested in…".
- Burying the lead. The main result must appear by paragraph 3 of the introduction.
- Literature review written as an annotated bibliography ("Smith found X. Jones found Y.") rather than a story with a "however".
- Literature review placed as a separate section when the journal expects it integrated into the introduction.
- Passive voice as the default in body prose. (Acceptable only in methods descriptions and captions.)
- Adjectives describing the author's own work: "striking", "novel", "important contribution".
- Causal language without an identification strategy.
- Excessive subsections, or parentheses / em-dashes used as a crutch. (Academic-baseline principle 9.)
- A separate "Limitations" subsection in the conclusion. Limitations belong near the analysis they qualify.
- Conclusion that copy-pastes the abstract or introduction. Each phrases the same findings differently.
- Declaring output done without running the five-pass self-check from `references/style-rules.md`.
- Replicating content already in sibling skills (tables, figures, `.bib`, LaTeX commands, replication standards).

## Verification Before Completion

- [ ] `academic-baseline` was invoked; `CLAUDE.superpapers.md` was resolved.
- [ ] Paper type and target section identified; matching formula applied.
- [ ] Seven core principles respected line by line.
- [ ] Five-pass self-check from `references/style-rules.md` run.
- [ ] No invented numbers, citations, or institutional details. Gaps marked `[AUTHOR: …]`.
- [ ] Causal / correlational language matches the design.
- [ ] Output in the user's paper language.
- [ ] No AI-pattern banned words in the final text.
- [ ] When reviewing: 3-reviewer perspectives applied and 100-point rubric scored.
- [ ] Non-prose work deferred to sibling skills.
