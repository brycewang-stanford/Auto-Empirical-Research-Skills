---
name: aer-identification
description: Use when selecting, implementing, or stress-testing the causal identification strategy for an empirical economics manuscript — difference-in-differences (including staggered designs), instrumental variables (including weak-IV-robust inference), regression discontinuity, synthetic control, or shift-share / Bartik. Apply before writing the introduction or results.
---

# AER Identification

## Overview

In AER-track empirical economics, **identification is the paper**. This skill routes among canonical designs, modern defaults, and referee-facing diagnostics.

If the design is fragile, return to `aer-topic-selection`; writing cannot save it.

## When to Use

- Designing the empirical strategy for a new project
- The current strategy is TWFE / first-stage F / naive RDD and the referee will flag it
- A prior submission was rejected on identification grounds and the design needs rebuilding
- Choosing between two candidate identification strategies for the same question

## Master Decision Tree

```
Is treatment assignment plausibly random conditional on observables?
├── Yes, by design (RCT, lottery) → run the RCT analysis; register PAP via AEA RCT Registry
└── No → identification must come from variation
    ├── Sharp threshold in a running variable → RDD (sharp or fuzzy)
    ├── Discrete policy change in some units, not others, over time → DiD
    │     ├── Single treatment date → canonical 2×2 DiD
    │     └── Staggered adoption → Callaway-Sant'Anna or Borusyak-Jaravel-Spiess
    ├── Endogenous regressor + plausibly exogenous shifter → IV
    │     ├── Shifter × pre-existing exposure shares → shift-share / Bartik
    │     └── Single instrument → weak-IV-robust inference if F < 50
    ├── One treated unit / aggregate intervention → synthetic control
    └── None of the above → reconsider the question
```

## Difference-in-Differences

### Canonical 2×2 (single treatment date, two groups)

Use TWFE if and only if:

- Treatment timing is **simultaneous** for all treated units
- The control group is **never treated**
- Treatment-effect heterogeneity is implausible

Otherwise, TWFE produces biased and often sign-flipped estimates.

### Staggered Adoption (most modern applications)

**Do not use TWFE.** Use one of:

- **Callaway and Sant'Anna (2021)** — `csdid` (Stata), `did` (R). Identifies group-time average treatment effects (ATT(g,t)); estimands are doubly robust; supports event-study aggregation.
- **Borusyak, Jaravel, and Spiess (2024)** — imputation estimator.
- **de Chaisemartin and D'Haultfœuille (2020)** — `did_multiplegt`.
- **Sun and Abraham (2021)** — interaction-weighted estimator for event studies.

**Required diagnostics:**

1. Goodman-Bacon decomposition to show the share of weight from "forbidden" comparisons under TWFE
2. Event-study plot with the imputation or Callaway-Sant'Anna estimator
3. Pre-trends test reported as the joint test, not just the visual
4. Heterogeneity by treatment cohort

### Pre-Trends

A flat pre-trend is necessary but not sufficient. Report:

- Visual event-study plot with 95% confidence intervals
- Formal joint test of pre-period coefficients (p-value)
- Honest DiD (Rambachan-Roth 2023) sensitivity bounds for the post-period

## Instrumental Variables

### Weak Instruments

The first-stage F > 10 rule is **obsolete**. Modern conventions:

- Just-identified models: report **Anderson-Rubin (AR) confidence sets** as primary inference; AR keeps size under weak instruments.
- For F < 50: 2SLS confidence intervals are unreliable; AR is required, not optional.
- Stock-Yogo TSLS-bias critical values assume homoskedasticity and rarely fit clustered settings.

Use `weakivtest` (Stata), `ivDiag` (R), or the Olea-Pflueger effective F statistic.

### Exclusion Restriction

The IV's credibility depends on a story, not a test. State the exclusion restriction in **one sentence** in the introduction and defend it with:

- Institutional narrative (one paragraph)
- A placebo regression where the instrument predicts an outcome it should not affect
- Sensitivity analysis: how much exclusion-restriction violation would overturn the result (Conley et al. 2012)

### Shift-Share / Bartik

Two valid sources of identification, with very different implications:

1. **Exogenous shares (Goldsmith-Pinkham, Sorkin, Swift 2020)** — argue that pre-existing exposure shares are conditionally exogenous; report the Rotemberg weights and inspect the top-5 industries driving identification.
2. **Exogenous shocks (Borusyak, Hull, Jaravel 2022; Adão, Kolesár, Morales 2019)** — argue that aggregate shocks are as-good-as-random; report shock-level inference.

Pick one explicitly. Do not hand-wave between the two.

## Regression Discontinuity

### Modern Defaults

- **Local linear regression with a triangular kernel.** Polynomials of order > 1 are discouraged (Gelman-Imbens 2019).
- **MSE-optimal bandwidth (Calonico-Cattaneo-Titiunik 2014)** with the robust bias-corrected confidence interval. Use `rdrobust`.
- **Donut RDD** if bunching near the cutoff is a concern.
- **Covariate adjustment** for efficiency; main result must hold without it.

### Required Diagnostics

1. McCrary (2008) / Cattaneo-Jansson-Ma (2020) density test for manipulation of the running variable
2. Balance tests on predetermined covariates at the cutoff
3. Placebo cutoffs away from the true threshold
4. Bandwidth sensitivity — show the estimate across at least three bandwidths
5. Visual RD plot using `rdplot` with the binning method explicitly stated

## Synthetic Control

### When Appropriate

- One (or few) treated units
- Long pre-treatment outcome series (≥ 10 periods)
- A large donor pool of plausibly comparable untreated units
- Aggregate intervention (policy at the country, state, city level)

### Modern Extensions

- **Generalized synthetic control (Xu 2017)** for multiple treated units
- **Augmented synthetic control (Ben-Michael, Feller, Rothstein 2021)** for bias correction
- **Synthetic DiD (Arkhangelsky et al. 2021)** combining SCM and DiD weighting

### Required Diagnostics

1. Placebo (in-time): apply SCM to pre-treatment fake intervention dates
2. Placebo (in-space): apply SCM to every donor as if it were treated; report the distribution of placebo effects
3. Permutation inference / Fisher exact p-value
4. Weight vector reported in the appendix; donors with > 10% weight discussed

## Field Experiments and RCTs

If the paper uses a field experiment:

- **Register with AEA RCT Registry** before the intervention begins. AEA journals require this prior to submission.
- **Pre-analysis plan (PAP)** posted before unblinding. Per Olken and others, keep the PAP moderate in scope — pre-specify primary outcomes and the analysis specification, leave exploratory work clearly labeled as such.
- **Power calculations** in the manuscript or appendix.
- **Multiple-hypothesis correction** if more than one primary outcome.
- **Attrition** documented and tested for differential attrition by treatment arm.

## Mechanism vs. Identification

A common confusion: **identification answers whether X causes Y; mechanism answers why.** Mechanism evidence should not weaken the identification of the main effect. Run:

- Subgroup heterogeneity (does the effect concentrate where theory predicts?)
- Mediation analysis only if the mediator is itself plausibly exogenous (rare)
- Auxiliary outcomes consistent with the proposed channel

## Red Flags for Referees

- TWFE on staggered data with no Goodman-Bacon decomposition
- First-stage F = 12 cited as evidence of instrument strength
- RDD with a polynomial of order 4
- Synthetic control with no placebo inference
- DiD with a "control group" of eventually-treated units
- IV exclusion restriction defended only by "we control for X"
- Quoting an Angrist-Pischke citation as a substitute for showing the diagnostic

## Repository Resources

When working from the repo or plugin bundle, load only the relevant resource:

- Estimator defaults, package calls, diagnostics, and citations: `docs/methods-reference.md`
- Staggered DiD implementation: `templates/stata/03_main_did.do`, `templates/r/03_main_did.R`, or `templates/python/main_did.py`
- Worked empirical examples: `examples/aer-exemplars.md` and `examples/modern-aer-exemplars.md`

Use the methods reference before prose: it fixes the estimand,
diagnostic, inference method, and citation that the manuscript must report.

## Identification Gate

Do not advance to robustness or writing until, for the chosen design, **all** are true:

- [ ] A modern estimator is used — no TWFE on staggered data, no first-stage-F-only IV, no high-order-polynomial RDD
- [ ] Every required diagnostic for the design (see the per-design lists above) is run and reported
- [ ] Inference matches the design — cluster-robust / AR / wild bootstrap / permutation, not default OLS SEs by reflex
- [ ] The identifying assumption is stated in one sentence, ready to drop into the introduction
- [ ] No item in "Red Flags for Referees" is present

### Gate Record Mini-Example

Write the gate decision before routing onward:

```text
STRATEGY: IV
FIRST STAGE: effective F = 7.8; 2SLS CI is not primary
ROBUST INFERENCE: AR 95% CI = [-0.14, 0.52]
PLACEBO: beta = 0.003 (p = 0.71)
DECISION: advance with directional headline only
```

## Handoff

```text
STRATEGY: <DiD | IV | RDD | SCM | shift-share | RCT>
MODERN ESTIMATOR USED: <yes / no / which>
REQUIRED DIAGNOSTICS REPORTED: <list>
INFERENCE METHOD: <robust / cluster-robust / AR / wild bootstrap / permutation>
WEAK-IV / TWFE / POLY-ORDER RED FLAGS: <list or "none">
NEXT SKILL: aer-robustness
```

## Anti-Patterns

- Defending an old design ("the prior literature used TWFE") when modern estimators exist
- Reporting OLS-with-controls as the main specification and IV/RD as "robustness"
- Using more than one identification strategy as if they were independent confirmations when they share identifying variation
- Footnoting the identifying assumption instead of stating it in the introduction
