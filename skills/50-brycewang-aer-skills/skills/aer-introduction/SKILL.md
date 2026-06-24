---
name: aer-introduction
description: Use when drafting or rewriting the introduction of an economics manuscript targeted at AER, AER:Insights, or an AEJ, or when compressing an abstract to the mandatory 100-word limit. Implements the Keith Head / Bellemare five-paragraph formula and AER-specific formatting conventions. Apply after the body sections exist.
---

# AER Introduction

## Overview

The introduction is the **only** part of the paper most editors read in full. Top-5 desk rejection decisions are typically made on pages 1-3. This skill produces an introduction that survives that filter and an abstract that fits AER's 100-word constraint.

Two non-negotiable AER formatting facts:

1. **No "Introduction" heading.** The introductory section is unlabeled and begins immediately after the title and abstract.
2. **Abstract ≤ 100 words.** Roughly 4-5 sentences. The AER Style Guide states the abstract "must not exceed 100 words"; an over-length abstract is flagged in editorial screening and returned for correction.

## When to Use

- Drafting an introduction from scratch
- Rewriting an introduction that drew a desk rejection
- Compressing a 250-word working-paper abstract to AER's 100-word limit
- The introduction is over 3 typeset pages and needs surgery
- The user has results but cannot explain *why they matter* in one paragraph

## The Five-Paragraph Formula (Keith Head)

Every AER-style introduction has exactly five components, in this order:

### Paragraph 1 — The Hook

Open with one of:

- **Y matters.** Welfare consequences, magnitudes, policy stakes.
- **Y is puzzling.** A stylized fact existing theory cannot explain.
- **Y is controversial.** Two camps disagree; new evidence resolves the question.
- **Y is big.** A first-order phenomenon (the service sector, urban inequality, the trade balance).

Two to three sentences. Cite **one** number that anchors the magnitude. Do not yet name the paper's contribution.

### Paragraph 2 — The Question

State exactly what this paper does:

```
This paper [estimates / documents / characterizes] [the causal effect of X on Y /
the response of Y to shock S / the distribution of Y in setting D].
```

One paragraph. Define the unit of observation, the outcome, and the variation that identifies the answer. Avoid the word "we" if possible; use "this paper."

### Paragraph 3 — The Identification (or the Model)

Empirical papers: name the identification strategy in one sentence, then explain in 1-2 paragraphs what variation drives identification and why the parallel trends / exclusion / smoothness assumption is credible *in this setting*.

Theory papers: name the modeling discipline — what's tractable, what's general, what the comparative statics give you.

This paragraph is where desk rejection happens. Editors check whether the method matches the claim. If you write "we examine the relationship between X and Y" while using OLS with controls, the paper is desk-rejected for methodology mismatch.

### Paragraph 4 — The Antecedents and Value-Added

Often the *single most important paragraph for surviving referee review*. Two halves:

**Antecedents (1-2 paragraphs).** Position the paper relative to its 3-6 closest published predecessors. Be specific: cite by author-year, identify what each did, and what each missed.

**Value-added (1 paragraph or 3 bullet points).** State approximately **three** contributions relative to the antecedents. These are the sentences the referee will quote in their report. Each contribution should make sense only in light of the prior work — otherwise it belongs in the Question paragraph.

Avoid:

- "To the best of our knowledge, this is the first paper to ..." (unverifiable, often false)
- "We contribute to the literature on X" (vacuous unless you say how)
- Padding the contribution list past four items

### Paragraph 5 — The Roadmap

One short paragraph. "Section I describes the data. Section II presents the empirical strategy. Section III reports results. Section IV explores mechanisms. Section V concludes." (AER numbers sections with Roman numerals; the introduction is unnumbered.)

Some AER authors omit the roadmap entirely. Acceptable for short papers (AER: Insights). Required for full-length AER.

## The 100-Word Abstract

AER abstracts are **100 words maximum**, including all numbers. The high-impact pattern allocates word budget as:

| Function                          | Sentences | Words |
|-----------------------------------|-----------|-------|
| Question or setting               | 1         | 15-20 |
| Method / data / identification    | 1         | 15-20 |
| Main quantitative result          | 1-2       | 30-40 |
| Implication                       | 1         | 15-20 |

**Allocate the most words to results.** Resist motivation-heavy abstracts — that is what the introduction's first paragraph is for. High-citation AER abstracts dedicate three of four sentences to findings.

### Abstract Template

```
[Setting and question — 1 sentence].
[Data and identification — 1 sentence].
[Main result with magnitude and sign — 1-2 sentences].
[Implication — 1 sentence].
```

### Word-Count Discipline

If the draft is over 100 words:

1. Delete every adjective that does not change the result
2. Replace clauses with semicolons
3. Drop the implication sentence — the introduction handles it
4. Replace "we find that ... " with active "X raises Y by Z%"
5. Numbers count as one word each; don't burn budget on "approximately"

## AER-Specific Formatting

- **No "Introduction" heading.** Begin the introductory material immediately after the abstract.
- **No vertical space markup.** Use `\section` and `\subsection`; do not insert `\vspace` or `\bigskip`.
- **Footnotes, not endnotes.** Inline citations use `\cite{}` (author-year), not numbered references.
- **Style emphasis sparingly.** No `\textbf` for emphasis in body text — italics only, rarely.
- **Sections use Roman numerals.** Per the AER Style Guide, major sections are numbered with Roman numerals (I., II., III.) and subsections with capital letters (A., B., C.). The introduction itself receives **no number and no heading** — the first *numbered* section is the one after it (e.g. "I. Data"). In LaTeX, switch the numbering with `\renewcommand{\thesection}{\Roman{section}}` or use the AEA sample article class, which does this for you.

## Anti-Patterns

- Three-page introduction that never names the identification strategy → desk reject
- Five contributions in the value-added paragraph, one of them weak → referee picks the weak one
- Abstract with 130 words after a "minor tweak" → editor bounces submission
- Hook paragraph that pitches a methods contribution when the paper is empirical (or vice versa)
- Burying the magnitude of the main result until section 4
- Lit review that runs for 2 pages and does not say what *this* paper adds

## Repository Resources

When working from the AER-skills repository or plugin bundle, read `examples/intro-example.md` only when the user asks for a model introduction, a concrete before/after rewrite, or abstract compression. Sentence-level prose rules shared with the body sections live in `docs/style-guide.md`; the antecedents paragraph consumes the map built by `skills/aer-literature/SKILL.md`.

Draft the introduction **after** the body sections exist (`skills/aer-paper-body/SKILL.md`) — the introduction summarizes a paper, it does not promise one.

## Pre-Handoff Gate

Ship the introduction only when **all** are true:

- [ ] Abstract ≤ 100 words by actual word count, with most words spent on the result
- [ ] All five paragraphs present in order — Hook, Question, Identification, Antecedents+Value, Roadmap
- [ ] Identification strategy named within pages 1-3, not deferred to the methods section
- [ ] Exactly three (max four) contributions, each meaningful only against the cited antecedents
- [ ] No "Introduction" heading; the method claim matches the actual estimator
- [ ] No banned phrasing — "to the best of our knowledge, the first to...", vacuous "we contribute to the literature on..."

## Handoff

```text
ABSTRACT WORD COUNT: <n>/100
INTRODUCTION PARAGRAPHS: Hook | Question | Identification | Antecedents+Value | Roadmap
CONTRIBUTIONS LISTED: <n> (target: 3, max 4)
KILL SWITCHES: <list of remaining red flags, or "none">
NEXT SKILL: <aer-tables-figures | aer-consistency>
```

## Reference Pattern

A canonical AER-style intro architecture (paragraph-by-paragraph):

1. **Hook.** "The richest 1% of US households hold X% of wealth. This share has risen by Y percentage points since Z."
2. **Question.** "This paper estimates the causal effect of [policy] on top-wealth concentration using [variation]."
3. **Identification.** "We exploit [quasi-experiment]. The identifying assumption is [...]. We validate this by [pre-trends test / placebo / institutional argument]."
4. **Antecedents + value-added.** "Three prior papers (A 2019, B 2021, C 2023) study related questions. A used [method] but [limitation]. B documented [fact] but did not establish causation. C addressed causation but in [different setting]. This paper makes three contributions: first, [...]; second, [...]; third, [...]."
5. **Roadmap.** "Section I describes [...]. Section II [...]."
