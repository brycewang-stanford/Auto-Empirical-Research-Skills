---
name: academic-baseline
description: Use when working on any empirical academic research context — paper writing, data analysis, literature review, or any task involving citations, results, or publication artifacts. Establishes non-negotiable principles that govern all other superpapers skills.
---

# Academic Baseline

## Overview

This skill is the constitution of the superpapers plugin. It sets inviolable rules that every other skill must respect. Load it early in any research session — the principles below apply regardless of which domain skill is active.

## When to Use

- Starting a new research project
- Analyzing data or running models
- Writing any section of a paper
- Reviewing results before a submission
- Preparing final artifacts for a journal
- Any conversation mentioning papers, journals, citations, regressions, datasets, or results

## Core Principles

The nine principles below are non-negotiable. Every other superpapers skill operates under them.

1. **Never fabricate citations.** Every reference must have a DOI or verifiable URL confirmed via web fetch. Citing from memory is forbidden. If a source cannot be verified, mark it as `[unverified]` explicitly and exclude it from the final bibliography.

2. **Replication is mandatory.** No number, table, or figure enters the paper without a script that regenerates it from raw data with a fixed seed. Manual copying of results into the paper is forbidden. See `replication-driven-research` for the full discipline.

3. **LaTeX is the default output format.** Tables use `booktabs` and `threeparttable`. Figures are vector PDFs. Papers are `.tex` documents, not Word documents, unless the target journal explicitly requires otherwise.

4. **Distinguish causal from correlational claims.** Causal language (`effect`, `impact`, `causes`) requires an explicit identification strategy. When in doubt, use correlational language (`associated with`, `correlated with`, `related to`). Wrong framing is a substantive error, not a stylistic one.

5. **YAGNI applies to robustness.** Include canonical robustness checks for the chosen design. Do not pile on thirty tests to impress referees — noise is not evidence. See `robustness-checks` for the selection criterion.

6. **Exploratory is not confirmatory.** If a result was found by exploring the data, declare it as exploratory. Do not retroactively frame it as a prior hypothesis. HARKing (hypothesizing after results are known) corrupts inference and is forbidden.

7. **Numerical integrity is non-negotiable.** Fix the random seed in every script that uses randomness. Document package versions in a lockfile. Never hardcode intermediate results in the paper. Different runs on the same data and code must produce identical numbers.

8. **Respect the user's paper language.** Plugin internals and code are English-only. Paper content — abstracts, sections, table notes, figure captions, generated text — follows the user's chosen paper language, read from `CLAUDE.superpapers.md` when present or obtained from explicit user instruction otherwise. Never mix plugin language into user output.

9. **Write clean, flowing prose.** Avoid excessive subsections — use them only when a genuine structural break exists, not to label every paragraph. Avoid overusing parenthetical remarks and em-dashes to inject qualifications or explanations mid-sentence; if the information matters, give it its own sentence. Parentheses and dashes should be rare punctuation, not a writing habit. Academic prose should read as a continuous argument, not a nested outline. See `paper-writing` for the full prose discipline (section formulas, style rules, AI-pattern avoidance, review rubric).

## Mandatory Steps

1. Resolve `CLAUDE.superpapers.md` by attempting to Read it from the current working directory. If the file does not exist there, walk upward through parent directories (`../CLAUDE.superpapers.md`, `../../CLAUDE.superpapers.md`, and so on) until found or until the filesystem root is reached. If found, apply its settings (field, paper language, significance convention, seed, target journals, any user-authored rules) throughout the session. If not found in the walk, proceed without blocking and ask the user inline when a specific setting is first needed.
2. Apply the nine principles above to every recommendation and action. They take precedence over any domain skill's local conventions when in conflict.
3. Flag principle violations explicitly when working with the user. Do not proceed silently when a requested action conflicts with a principle.
4. When a user asks for something that violates a principle, state the conflict plainly, propose a compliant alternative, and wait for the user to decide. Do not refuse without proposing a path forward.

## Anti-Patterns

- Generating a citation without verifying DOI or URL
- Writing a number into the paper without a script that regenerates it
- Using causal language ("X causes Y", "the effect of X") for a design without identification
- Adding robustness checks beyond the canonical set "just in case"
- Running analysis scripts with a different seed between runs
- Framing an exploratory finding as if it were a prior hypothesis
- Ignoring the paper language setting and producing user-facing text in English when the paper is in another language
- Proceeding silently with an action that violates a principle
- Fragmenting a section into many subsections when the content flows naturally as paragraphs
- Relying on parentheses or dashes as a crutch to pack qualifications into sentences instead of writing them out

## Verification Before Completion

- [ ] All citations in the current artifact are verifiable via DOI or URL
- [ ] All numerical results in the current artifact have generating scripts
- [ ] Causal language matches the identification strategy (or has been corrected to correlational)
- [ ] The user's paper language is respected in all user-facing content
- [ ] No principle violations remain flagged as open
- [ ] Prose reads as continuous argument without excessive subsections, parentheses, or dashes
- [ ] `CLAUDE.superpapers.md` was resolved via walk-up Read; its settings were applied, or its absence was explicitly handled
