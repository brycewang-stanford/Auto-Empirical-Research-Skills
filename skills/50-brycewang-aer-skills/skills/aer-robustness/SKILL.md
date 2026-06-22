---
name: aer-robustness
description: Use when the main empirical results exist but the manuscript lacks the robustness, heterogeneity, mechanism, and placebo checks that AER referees will demand. Apply after aer-identification and before aer-introduction so that the value-added paragraph can reference these tests.
---

# AER Robustness

## Overview

A modern AER referee report contains three predictable demands:

1. **Robustness** — does the result survive specification changes?
2. **Heterogeneity** — where does the effect concentrate, and is that consistent with the proposed channel?
3. **Mechanism** — *why* does X cause Y?

This skill anticipates all three so that the referee finds the answer already in the paper. Skipping this step turns a referee report into a 6-month delay.

## When to Use

- The main result table exists but the rest of the empirical section is thin
- An R&R demands "additional checks" without specifying which
- Drafting the appendix before submission
- Diagnosing why a prior submission drew a "needs more robustness" rejection

## The Referee-Anticipating Battery

Every empirical AER paper should report, at minimum:

### Robustness

1. **Alternative specifications** — drop covariates one at a time; include fixed effects at finer/coarser granularity; weight observations differently
2. **Alternative samples** — drop the largest unit; drop the most influential time period; restrict to balanced panel; restrict to comparable subsets
3. **Alternative outcome definitions** — log vs. level; winsorized at 1% / 5%; alternative deflators
4. **Alternative clustering** — cluster at the next-higher level (e.g., state if main is county); two-way cluster; wild cluster bootstrap if few clusters
5. **Alternative estimators** — if main is OLS, show IV; if main is TWFE, show Callaway-Sant'Anna; if main is RD, show donut and bandwidth grid
6. **Outlier diagnostics** — Cook's distance, leverage; rerun excluding top-1% influential observations

### Heterogeneity

Report heterogeneity that the **theory predicts**, not heterogeneity discovered by mining:

1. By unit characteristics relevant to the mechanism (e.g., effect should be larger in low-credit-access counties if the channel is credit)
2. By time period (early vs. late treatment effects under staggered adoption)
3. By treatment intensity if treatment is continuous
4. Quantile treatment effects if distributional consequences matter
5. Subgroup analysis pre-registered in PAP for field experiments; otherwise label as exploratory

### Mechanism

Distinguish two purposes:

- **Channel evidence** — show auxiliary outcomes consistent with the proposed mechanism. Not causal mediation; just consistency.
- **Ruling out alternatives** — identify the 2-3 most plausible alternative explanations a smart referee will raise, and present evidence against each.

State both explicitly in the manuscript. Do not let the reader infer.

### Placebo

1. **Pre-treatment placebo** — fake the treatment date; the effect should be zero
2. **Cross-unit placebo** — assign treatment to randomly chosen never-treated units; the distribution of placebo effects should bracket zero
3. **Outcome placebo** — apply the design to an outcome that should not respond; null result strengthens the main story

## Specification Curve (Recommended for Contested Results)

If the result is contested or counterintuitive, present a **specification curve** (Simonsohn-Simmons-Nelson 2020) showing the estimate across all reasonable analytic choices. This converts "you chose your specification to get this result" into "the result holds across the entire reasonable choice set."

## Anticipating the Top 5 Referee Comments

For any empirical paper, predict and pre-empt:

| Comment                                                    | Pre-emption                                                  |
|------------------------------------------------------------|--------------------------------------------------------------|
| "The result may be driven by [omitted variable]"           | Include it as a control; show robustness without it          |
| "Standard errors are not clustered correctly"              | Report 2-3 clustering schemes; wild bootstrap if needed      |
| "Pre-trends look suspect"                                  | Formal joint test + honest DiD bounds                        |
| "This is a mechanical effect from [other channel]"         | Direct placebo or sample restriction excluding that channel  |
| "Effect size is implausibly large/small"                   | Sanity-check against existing magnitudes in the literature   |

## Power and Precision

A null result is publishable at AER if and only if:

- The design has demonstrable power to detect the relevant effect size
- The confidence interval is tight enough to rule out economically meaningful magnitudes
- The interpretation does not over-claim "no effect" when the data say "no precisely-estimated effect"

Always report 95% CIs alongside p-values. Many AER editors explicitly prefer effect-size reporting over significance stars.

## Appendix Structure

Keep main-text robustness to **one table** with each row a different specification. Push the deep robustness into the appendix in this order:

1. Additional specifications and clustering
2. Alternative samples and outcome definitions
3. Heterogeneity tables
4. Placebo and falsification tests
5. Mechanism evidence
6. Theoretical extensions / model details
7. Data appendix (sources, cleaning, variable construction)

## What Not to Include

- Robustness checks that confirm what no one would doubt (e.g., "controls for year fixed effects do not change the result" when year FE are already in the main spec)
- Twenty specifications of which two are highlighted; the referee will notice
- "We have additional results available upon request" — at AER this is not credible

## Reporting Discipline

- Every robustness table reports the **same point estimate column** as the main table for direct comparison
- Heterogeneity is reported as interaction coefficients, not as separately-estimated subgroup tables (unless heterogeneity is the point of the paper)
- Magnitude differences are explained in the text, not left to the reader to compute
- Sample-size changes across rows are flagged

## Coverage Gate

The empirical section is referee-ready only when **all** are present and theory-motivated (not mined):

- [ ] Robustness spans specification, sample, outcome definition, clustering, and estimator
- [ ] Heterogeneity is mechanism-predicted (interaction form), labeled pre-specified vs. exploratory
- [ ] Mechanism shows both channel evidence and explicit ruling-out of the 2-3 leading alternatives
- [ ] Placebo / falsification covers pre-treatment, cross-unit, and outcome placebo as applicable
- [ ] Each of the top-5 anticipated referee comments has a visible pre-emption in the paper
- [ ] Any null is reported with demonstrated power and tight CIs, never over-claimed as "no effect"

## Handoff

```text
ROBUSTNESS COVERAGE: <spec / sample / outcome / cluster / estimator>
HETEROGENEITY: <pre-specified / exploratory>
MECHANISM EVIDENCE: <channel / ruling-out / both>
PLACEBO TESTS: <list>
ANTICIPATED REFEREE COMMENTS PRE-EMPTED: <count>
NEXT SKILL: <aer-introduction | aer-tables-figures>
```

## Anti-Patterns

- Adding robustness checks the morning before submission, with no analysis-plan rationale
- Heterogeneity by every demographic — referee will read this as fishing
- Mechanism evidence that contradicts the main effect's sign on a subsample, presented as if it confirms the channel
- A 30-page appendix that adds noise without addressing the obvious counterarguments
