# Example — Five-Paragraph Introduction

A worked example of the Keith Head / Bellemare five-paragraph introduction
formula, written to AER house style. Topic is fictional but the architecture
is real. Read this alongside `skills/aer-introduction/SKILL.md`.

The example assumes a paper titled:

> *Broadband Expansion and Local Wage Inequality:
>  Evidence from the FCC's Connect America Fund*

---

## Abstract (97 words)

> We estimate the causal effect of high-speed broadband deployment on
> local wage inequality using the staggered rollout of the FCC's Connect
> America Fund Phase II auction. Combining ZIP-code-level coverage maps
> with American Community Survey wage data, we identify treatment effects
> from a Callaway-Sant'Anna event study. Broadband expansion raises the
> 90/10 wage ratio by 4.2 log points (s.e. 1.1) over six years, driven
> by gains at the top of the distribution. The effect concentrates in
> tradeable-services occupations and is absent in retail and
> construction, consistent with skill-biased technology adoption.

*Word count: 97 / 100. Each result reported with a magnitude. Sells
findings, not motivation.*

---

## Introduction

### Paragraph 1 — Hook

> Between 2010 and 2024, US rural counties received \$84 billion in
> federal broadband subsidies, an investment justified by the premise
> that high-speed connectivity narrows place-based economic gaps. Yet
> the within-county distribution of who benefits is poorly understood:
> if broadband disproportionately raises top-decile wages, federal
> investment may widen, not narrow, local inequality.

*The hook anchors on a number (\$84 billion), establishes that the
phenomenon is large, and frames a puzzle worth resolving. Two sentences.
Does not yet name what the paper does.*

### Paragraph 2 — Question

> This paper estimates the causal effect of high-speed broadband
> deployment on local wage inequality. The unit of observation is the
> US ZIP code; the outcome is the within-ZIP-code 90/10 log wage ratio,
> measured annually from 2010 to 2024 using the American Community
> Survey. Identification exploits the staggered geographic rollout of
> the FCC's Connect America Fund Phase II reverse auction, which
> assigned broadband subsidies based on engineering-cost criteria
> uncorrelated with pre-period wage trends.

*One paragraph. Names the outcome, the unit of observation, and the
source of identifying variation in a single sentence. The reader knows
the entire empirical strategy by line 4.*

### Paragraph 3 — Identification

> We implement the Callaway and Sant'Anna (2021) doubly-robust
> estimator for group-time average treatment effects, aggregating to
> simple and event-study ATTs. The identifying assumption is parallel
> pre-trends in 90/10 wage ratios between auction-funded ZIP codes and
> not-yet-funded ZIP codes within the same commuting zone. We support
> this assumption with three pieces of evidence: (i) a formal joint
> test of pre-period coefficients fails to reject parallel trends
> (p = 0.71); (ii) the Goodman-Bacon decomposition shows that 94% of
> the implicit weight comes from valid comparisons; and (iii) Honest
> DiD sensitivity bounds (Rambachan and Roth 2023) imply our post-
> period estimates remain economically meaningful under pre-trend
> violations up to 0.3 standard deviations.

*This is the paragraph that determines desk-reject vs. desk-pass. The
identifying assumption is stated as one sentence and defended with three
explicit pieces of evidence. The modern estimator (Callaway-Sant'Anna)
and modern sensitivity tools (Honest DiD) are named explicitly.*

### Paragraph 4 — Antecedents and Value-Added

> A growing literature studies the labor-market effects of broadband
> infrastructure. Akerman, Gaarder and Mogstad (2015) document
> productivity gains from Norwegian broadband rollout but do not study
> distributional incidence. Hjort and Poulsen (2019) estimate
> employment effects of African submarine cables, finding aggregate
> gains concentrated in skilled occupations. Closest to our setting,
> Bauernschuster, Falck and Heblich (2014) examine German DSL
> diffusion but rely on a cross-sectional IV that cannot trace
> distributional dynamics over time.
>
> This paper contributes to this literature in three ways. First, we
> provide the first design-based causal estimates of broadband's effect
> on within-area wage inequality, using a staggered estimator robust to
> heterogeneous treatment effects. Second, we quantify the
> distributional incidence by occupation, showing that gains
> concentrate in tradeable services consistent with skill-biased
> technology channels. Third, we provide a benefit-cost framework that
> allows policymakers to weigh aggregate productivity gains against
> distributional consequences within a single welfare metric.

*Two paragraphs: first names 3-4 antecedents with what each did and what
each missed; second lists exactly three contributions in order of
importance. Each contribution is meaningful only in light of the
antecedents.*

### Paragraph 5 — Roadmap

> Section I describes the Connect America Fund auction mechanism and
> our data sources. Section II presents the empirical strategy.
> Section III reports main results. Section IV explores heterogeneity by
> occupation and tests the skill-biased technology mechanism. Section V
> presents a calibrated benefit-cost framework. Section VI concludes.

*One paragraph, terse. Six numbered sections (AER house style numbers
them with Roman numerals; the introduction is unnumbered), each serving
one purpose. Some AER papers omit the roadmap entirely — acceptable for
short papers.*

---

## What This Example Demonstrates

| Element | Choice made | Why |
|---|---|---|
| Abstract length | 97 words | Under the 100-word cap with margin for safety |
| Hook anchor | \$84 billion | One number; magnitude makes the question matter |
| Identification | Named in paragraph 2, defended in paragraph 3 | Editor knows the design by page 1 |
| Estimator | Callaway-Sant'Anna | Modern default; TWFE on staggered data is desk-reject bait |
| Robustness tools | Bacon, Honest DiD | Named in the intro, not buried in §6 |
| Value-added bullets | Exactly 3 | Easy for referees to quote in their reports |
| No "Introduction" heading | (LaTeX convention) | AER house style |

---

## Counterexample — What Not to Write

The same paper, written badly:

> **(Bad) Hook.** "In recent years, broadband has become an important
> infrastructure investment in many countries around the world.
> Researchers have studied many aspects of broadband but few have
> looked at within-area inequality."

What's wrong:
- No number anchors the magnitude
- "In recent years" is filler
- The hook is actually a literature-gap claim, not a hook
- No puzzle, no stake

> **(Bad) Identification.** "We use a difference-in-differences design
> exploiting the fact that some areas got broadband before others.
> Pre-trends look parallel (see Figure 5)."

What's wrong:
- "Some areas got broadband before others" is not an identification
  strategy — it's a description of the data
- "Pre-trends look parallel" requires the reader to leaf to Figure 5
- No modern estimator named; no Goodman-Bacon, no sensitivity bounds
- Desk reject in 5 minutes

---

## Word-Count Discipline

A common failure mode: an introduction creeps to 4 typeset pages because
each section feels essential. AER editors explicitly penalize this. The
five-paragraph formula is a *length budget*, not just a structure:

| Paragraph | Target words | Hard cap |
|---|---|---|
| Hook | 60-100 | 150 |
| Question | 80-120 | 180 |
| Identification | 150-220 | 300 |
| Antecedents + value-added | 250-400 | 500 |
| Roadmap | 50-80 | 100 |
| **Total** | **600-900** | **~1,200** |

That keeps the intro to roughly 2 typeset pages. If your draft is 4
pages, half of it should move to the literature review section or be
deleted entirely.
