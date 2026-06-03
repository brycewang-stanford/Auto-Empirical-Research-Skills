# Causal Inference Methods

Starting-point reference for methods designed to identify causal effects from observational data. **Not exhaustive.**

## Difference-in-Differences (Canonical 2x2)

**When to use:** A treatment is applied to some units at a specific point in time, leaving untreated units as a control group, and parallel pre-trends between groups are plausible.

**Assumptions:**
- **Parallel trends:** In the absence of treatment, treated and control units would have followed parallel paths on the outcome
- **No anticipation:** Treated units do not change behavior before the treatment actually occurs
- **SUTVA:** No spillovers between treated and untreated units

**Diagnostics:**
- **Event-study plot:** Estimate the treatment effect at each pre- and post-treatment period, check that pre-period coefficients are near zero
- **Pre-trend test:** Formally test that pre-period coefficients are jointly zero
- **Triple-diff (DDD):** When a third dimension distinguishes affected from unaffected subgroups of the treated
- **Alternative comparison groups:** Results should be robust across reasonable control-group choices

**Implementation:**
- For a single treatment timing, standard two-way FE with treatment dummy works
- For aggregated event studies, use binned endpoints to avoid "open-ended" comparisons

**R packages:** `fixest`, `did`, `bacondecomp`
**Python packages:** `differences`, `linearmodels`, `pyfixest`

## Staggered DiD (Modern Estimators)

**When to use:** Treatment adopted at different times by different units, with potentially heterogeneous effects over time and across cohorts.

**Problem with two-way FE:** Under heterogeneous effects and staggered timing, two-way FE can be biased because already-treated units serve as controls for later-treated units ("forbidden comparisons"). See Goodman-Bacon (2021) for the decomposition.

**Modern estimators:**

- **Callaway and Sant'Anna (CS):** Group-time average treatment effects, aggregated by cohort or time
- **de Chaisemartin and D'Haultfoeuille (dCDH):** Average effects without forbidden comparisons, with placebo tests
- **Borusyak, Jaravel, and Spiess (BJS):** Imputation estimator using only never-treated or not-yet-treated as controls
- **Sun and Abraham:** Interaction-weighted estimator for event studies

**Choice:**
- CS is the most widely used; good default for reporting group-time effects
- BJS is efficient when pre-trends are good
- dCDH is flexible; good for multiple treatments and dynamic effects

**R packages:** `did` (CS), `DIDmultiplegt` (dCDH), `didimputation` (BJS), `fixest::sunab`
**Python packages:** `differences`, `csdid`

## Regression Discontinuity

**When to use:** Treatment assignment follows a cutoff rule on a continuous running variable (exam scores, vote shares, income thresholds, ages).

### Sharp RD

**Assumption:** Treatment is a deterministic function of the running variable — everyone above the cutoff is treated, everyone below is not.

**Identification:** Continuity of potential outcomes at the cutoff. Formally, `lim E[Y(0) | X=c+] = lim E[Y(0) | X=c-]` and similarly for `Y(1)`.

### Fuzzy RD

**When to use:** The cutoff affects the probability of treatment but does not fully determine it.

**Identification:** Same continuity assumption, plus monotonicity. Estimand is a LATE for compliers at the cutoff.

### Diagnostics

- **McCrary density test:** Check for manipulation of the running variable around the cutoff
- **Covariate balance:** Pre-determined covariates should be continuous at the cutoff
- **Bandwidth sensitivity:** Results should be stable across a reasonable range of bandwidths
- **Polynomial order:** Avoid high-order polynomials (Gelman-Imbens warning); prefer local linear or local quadratic with robust-bias-corrected inference
- **Donut RD:** Drop observations very close to the cutoff as a robustness check

**R packages:** `rdrobust`, `rddensity`, `rdlocrand`
**Python packages:** `rdrobust`

## Synthetic Control

**When to use:** A single (or a few) treated unit(s) and many potential control units, with a pre-treatment period long enough to match the treated unit's trajectory.

**Assumptions:**
- **Pre-treatment fit:** The synthetic control (weighted combination of donors) closely matches the treated unit before treatment
- **No interference:** Donors are not affected by the treatment
- **Invariant donor pool:** Donors are comparable units that could plausibly have been treated

**Diagnostics:**
- **Pre-treatment RMSPE:** Should be small
- **Placebo tests in space:** Apply the method to each donor as if it were treated; rank the treated unit's effect against placebo distribution
- **Placebo tests in time:** Move the treatment date back, check for "effects" where none should exist
- **Leave-one-out:** Drop each donor and re-estimate; the weight on any single donor should not drive the result
- **MSPE ratios:** Ratio of post-period to pre-period MSPE, compared to placebo distribution

**Extensions:**
- **Augmented SC:** Combines SC with outcome regression for bias correction
- **Synthetic DiD:** Combines SC weighting with DiD structure, useful with multiple treated units

**R packages:** `Synth`, `tidysynth`, `augsynth`, `synthdid`
**Python packages:** `pysyncon`

## Matching and Inverse Probability Weighting

**When to use:** Selection on observables is plausible (no unobserved confounders after conditioning on covariates).

**Methods:**
- **Propensity score matching:** Match treated and control units on estimated propensity to be treated
- **Coarsened exact matching (CEM):** Discretize covariates and match within bins
- **Entropy balancing:** Reweight controls to match treated units' covariate moments
- **Inverse probability weighting (IPW):** Weight observations by inverse of the propensity score

**Diagnostics:**
- **Covariate balance:** Standardized mean differences before and after matching (rule of thumb: |SMD| < 0.1)
- **Common support:** Distribution of propensity scores should overlap between treated and control
- **Sensitivity analysis:** Rosenbaum bounds for hidden bias

**Caveats:**
- Propensity score matching discards unmatched observations, changing the estimand
- IPW is sensitive to extreme weights; consider trimming or stabilization

**R packages:** `MatchIt`, `WeightIt`, `cobalt`, `sensemakr`
**Python packages:** `causalml`, `dowhy`

## IV for Causal Effects

See `cross-section.md` for IV mechanics. For causal interpretation, focus on:

- **Plausibility of the exclusion restriction:** Can you tell a convincing story that the instrument affects the outcome *only* through the endogenous regressor?
- **LATE interpretation:** 2SLS identifies the effect for compliers under monotonicity
- **Heterogeneous effects:** The estimand is local; do not extrapolate

## Sensitivity Analysis

- **Rosenbaum bounds (matching):** How much hidden bias in treatment assignment would it take to nullify the result?
- **Oster bounds (OLS):** Uses the relationship between coefficient stability and R² changes to bound the treatment effect under unobserved confounding
- **Cinelli-Hazlett:** Robustness value for omitted variable bias

Use sensitivity analysis when the main result relies on selection on observables.

## Not in This Reference

Bayesian causal inference, double machine learning, structural causal models, interference and spillover methods, mediation analysis. Use the modeling process from `modeling-process.md`.
