# Minimum-wage adoption and county employment

Your policy turns on in **different years across counties (2005, 2009, 2012)**,
with a never-treated group. This is a **staggered** adoption design, so a single
two-way fixed-effects (TWFE) coefficient is *not* a trustworthy headline: under
treatment-effect heterogeneity TWFE contaminates the estimate with **forbidden
comparisons** (already-treated counties used as controls).

## Estimating equation and assumption

I estimate group-time average treatment effects ATT(g,t) and aggregate them.
Identifying assumption: **parallel trends** conditional on covariates and **no
anticipation** before adoption.

## Estimator

I use the **Callaway–Sant'Anna** estimator with not-yet-treated controls
(`sp.callaway_santanna(...)`), and cross-check with **Sun–Abraham** event-study
coefficients.

## Diagnostics

1. **Goodman–Bacon decomposition** to show how much weight plain TWFE would put
   on forbidden already-treated comparisons.
2. **Event-study** leads and lags (reference period t = −1) with a formal joint
   **pre-trends** test; report pre-period coefficients with 95% CIs.
3. **Honest DiD** (Rambachan–Roth) bounds for sensitivity to parallel-trends
   violations.

Headline number is the aggregated ATT from Callaway–Sant'Anna, not the TWFE
coefficient.
