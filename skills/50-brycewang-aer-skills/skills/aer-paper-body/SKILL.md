---
name: aer-paper-body
description: Use when drafting or revising the body sections of an AER, AER:Insights, or AEJ manuscript — institutional background, data, empirical strategy, results, mechanisms, and conclusion. Covers equation conventions, results-paragraph narration, magnitude interpretation, and back-of-envelope policy calculations. Apply after the empirics are stable and before or alongside aer-introduction.
---

# AER Paper Body

## Overview

The introduction decides whether the editor sends the paper out; the **body
sections decide what the referees write**. Referees live in Data, Empirical
Strategy, and Results, checking that the estimand is defined, the assumption
stated, the magnitudes interpreted, and the prose matched to the tables. Draft
the body **before** the introduction — the introduction summarizes a paper that
already exists, and writing it first produces promises the body fails to keep.

## When to Use

- The empirics are stable (after `aer-identification` and `aer-robustness`)
  and the manuscript needs full section drafts
- A results section reads like a table walk-through ("Column 1 shows...") and
  needs narration surgery
- A referee called the paper "hard to follow," "under-interpreted," or "reads
  like a report"
- Coefficients are reported but never converted into economic magnitudes
- The conclusion restates the abstract and needs to do real work

## Canonical Section Architecture

A full-length empirical AER paper, after the unlabeled introduction:

```
I.   Background  (or: Institutional Setting; Policy Context)
II.  Data        (sources, sample construction, measurement, summary stats)
III. Empirical Strategy   (estimand, equation, identifying assumption, inference)
IV.  Results     (main estimates, dynamics, robustness pointers)
V.   Mechanisms  (or: Heterogeneity and Mechanisms; Interpretation)
VI.  Conclusion
```

Variants: a **conceptual framework** goes between Background and Data (or
replaces Background for theory-led papers); *AER: Insights* compresses to Data
and Design → Results → Discussion; structural papers add Model and Estimation,
where the rules below bind with more force, not less. One rule binds
everywhere: **every term, dataset, and design feature is defined before first
use** — referees read linearly on the first pass.

## Section I — Background / Institutional Setting

Give exactly the institutional detail needed to (a) locate the identifying
variation and (b) believe the identifying assumption — nothing else.

- Lead with the institution or policy, not the literature. History belongs
  here only if it explains the variation.
- State **who is treated, when, by what rule, and who decided**. If assignment
  is discretionary, say so and explain how the design handles it.
- Length 1.5-3 typeset pages; surplus is almost always literature review in
  disguise — cut it or move it to the intro's antecedents paragraph.
- Cite a **primary source** (statute, agency document, administrative report)
  for every institutional claim, not a secondhand economics paper.

## Optional Section — Conceptual Framework

Include one only if it generates a testable prediction the empirics then test,
defines the estimand's welfare interpretation (a reduced-form coefficient as a
sufficient statistic), or disciplines magnitudes (what effect size theory
permits).

- Keep it **stylized** — two-period, two-type, linear where possible. Push
  derivations to the appendix; state propositions and intuition in the text.
- End with an explicit bridge naming the predictions taken to the data; each
  must reappear, by name, in Results or Mechanisms.
- Do not bolt on a model that re-derives "demand slopes down." Referees read
  decorative theory as padding and say so.

## Section II — Data

Referees check this section against the replication package line by line.

- **Sources.** For each dataset: name, producer, access mode, years, unit of
  observation, and a citation. If access is restricted, say how it was obtained
  (this feeds `aer-replication`).
- **Sample construction** — the most under-written block in rejected papers.
  Report the funnel explicitly with counts (raw file → each drop with its count
  and rationale → analysis sample). Counts must match the replication package
  exactly (`aer-consistency` audits this); flag consequential restrictions the
  robustness section relaxes.
- **Variables and measurement.** Define outcome and treatment precisely, with
  units, in prose (the full variable table lives in the appendix). Discuss
  measurement error where a referee would: self-reports, imputation,
  top-coding, deflators (name the index and base year). State the level of
  aggregation and why it matches the design.
- **Summary statistics.** Narrate Table 1, do not re-read it aloud. Two to four
  facts, each tied to a design decision: is the sample representative, are the
  groups comparable pre-treatment, and what features (skewness, mass points,
  attrition) shape specification choices.

## Section III — Empirical Strategy

The section referees read most carefully. Four mandatory components, in order:
**estimand → equation → identifying assumption → inference**.

**Estimand first**, one sentence before any equation: "Our object of interest
is the average effect of [treatment] on [outcome] among [population],
[horizon]." If the design recovers a local effect (LATE, effect at the cutoff,
ATT for switchers), say so here, not in the conclusion's limitations paragraph.

```latex
Y_{ict} = \beta\, D_{ct} + \alpha_c + \gamma_t + X_{ict}'\delta + \varepsilon_{ict}
```

- **Define every symbol** in the sentence after the equation, every subscript
  included (what each index ranges over; what $D_{ct}$ codes). Keep subscript
  order consistent across equations and tables. Number displayed equations;
  refer to "equation (1)."
- State which coefficient is the object of interest and what variation
  identifies it once controls and fixed effects absorb the rest.
- For modern DiD, write the ATT(g,t) estimand and aggregation explicitly rather
  than pretending the design is equation-(1) TWFE — the estimator choice comes
  from `aer-identification`.
- **Identifying assumption:** state it formally **and** in words, then preview
  the evidence. The unit of writing is "assumption — threat — evidence"; name
  the two or three most plausible violations and point to where each is met.
- **Inference:** one paragraph — clustering level and why it matches the
  design's variation, number of clusters, and any small-cluster correction
  (wild cluster bootstrap) or design-specific inference (AR confidence sets,
  randomization inference). Never leave inference to the table notes alone.

## Section IV — Results

### The narration discipline

One paragraph per claim, not per table. Each results paragraph:

1. **Finding first.** The opening sentence states the economic finding with its
   magnitude, not the table's existence: "The reform raises earnings by 4.2
   percent (Table 3, column 4)," never "Table 3 presents the results."
2. **Evidence.** Where the number comes from and how it moves across
   specifications (added controls, finer fixed effects, alternative samples).
3. **Interpretation.** Convert the coefficient into economic units and
   benchmark it.

Column-by-column narration without a finding-first sentence is the most
reliable marker of a weak results section.

### Magnitude interpretation

Every headline coefficient gets three conversions: (1) **native units** —
log-outcome coefficients are *log points*; use the exact 100·(e^β − 1) whenever
|β| > 0.10, and never confuse **percent** with **percentage points**; (2)
**relative to the sample** — against the dependent variable's mean or SD; (3)
**relative to the literature or a policy lever**. Report the baseline rate next
to every binary marginal effect. If the implied magnitude is implausible, say
so and investigate before a referee does. Worked conversions:
`examples/results-section-example.md`; the percent/percentage-point table lives
in `aer-consistency`.

### Precision and back-of-envelope

- Quote point estimates and standard errors **exactly** as the table shows
  them. "Significant at the 5 percent level," never "almost significant." For
  nulls, report the CI and what it rules out, distinguishing a precise zero
  from an uninformative one. Line-level rules: `docs/style-guide.md`.
- Close a high-impact results section with **one** disciplined aggregate
  calculation: every input and its source stated, multiplied through in one
  visible chain, rounded honestly — not a cascade of unsourced products. If it
  needs more than a paragraph, it becomes its own short section. Worked
  example: `examples/results-section-example.md`.

### Robustness pointers

The results section **cites** robustness, it does not contain it: one paragraph
summarizing the `aer-robustness` battery ("stable across clustering, sample,
and specification variants; Appendix B reports the full set") plus the single
most important check shown inline.

## Section V — Mechanisms

Organize by **candidate explanation**, not by table:

1. Name the two or three channels consistent with the main result, including
   the ones you will rule out.
2. For the favored channel, present the theory-predicted heterogeneity and
   auxiliary outcomes ("if the channel is skill-biased adoption, effects should
   concentrate in tradeable services — they do, Table 5").
3. For each alternative, state the sharpest version of the referee's objection,
   then the evidence against it. Steelman first, then answer.
4. Close with calibrated language ("most consistent with [channel]," not "we
   prove the mechanism"). Mechanism evidence is consistency evidence; only the
   main effect carries design-based identification (see `aer-identification`).

## Section VI — Conclusion

Short (half a page to one page), doing four things:

1. Restate the question and the headline magnitude in fresh words — no abstract
   sentences copied verbatim (`aer-consistency` flags duplication).
2. State the external-validity boundary: population, period, policy margin, and
   the complier/locality caveat if the design implies one.
3. Draw the one policy or theory implication the evidence supports — one step
   beyond the results, never three.
4. At most two sentences on specific open questions this paper makes
   answerable, not "more research is needed."

No new results, no new citations, no new caveats that belong in Results.

## Cross-Section Consistency Rules

- The introduction's promises (contributions, magnitudes, evidence) map
  one-to-one onto body sections; nothing promised is undelivered and nothing
  major appears unannounced.
- Numbers, sample sizes, and specification labels match the tables exactly
  everywhere — `aer-consistency` audits this before submission.
- Tense: present for what the paper does and finds; past for data collection
  and historical events.
- Prose follows `docs/style-guide.md` — finding-first sentences, no filler
  transitions, no AI-pattern tics.

## Repository Resources

Load only the relevant resource:

- Worked results-section narration (same fictional paper as the intro example):
  `examples/results-section-example.md`
- Sentence- and paragraph-level prose rules: `docs/style-guide.md`
- Estimator, diagnostic, and citation defaults for Section III:
  `docs/methods-reference.md`
- Model introduction the body must stay consistent with:
  `examples/intro-example.md`
- Code that should produce every number quoted in Results: `templates/stata/`,
  `templates/r/`, or `templates/python/`

## Handoff

```text
SECTIONS DRAFTED: <Background | Framework | Data | Strategy | Results | Mechanisms | Conclusion>
ESTIMAND STATED: <yes / no — sentence>
SAMPLE FUNNEL REPORTED: <yes / no>
HEADLINE MAGNITUDE CONVERSIONS: <log-points / percent / vs-mean / vs-literature>
BACK-OF-ENVELOPE CALCULATION: <present / not applicable>
MECHANISM CHANNELS: <favored + ruled-out list>
NEXT SKILL: <aer-introduction | aer-tables-figures | aer-consistency>
```

## Anti-Patterns

- Writing the introduction first and forcing the body to keep its promises
- Narrating tables instead of findings ("Table 4 shows the results. Column 1
  reports...")
- Reporting a 0.31 log-point effect as "31 percent" (it is 36 percent), or
  never benchmarking the magnitude at all
- The estimand defined nowhere — "the effect" means three populations in three
  sections
- The sample funnel absent, so the referee reconstructs (and mistrusts) the Ns
- A conceptual framework added after the results to decorate them
- Mechanisms organized as "more regressions," or claimed with the confidence of
  the identified main effect
- A two-page conclusion introducing limitations Results hid, or paragraphs
  recycled verbatim into the abstract
- Institutional background with no source for any factual claim
