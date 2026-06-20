---
name: event-study
description: >
  Use this skill whenever the user wants to conduct an event study, create event study plots,
  test for parallel trends, implement difference-in-differences designs, or work with any
  panel data estimation that involves pre/post treatment comparisons. Trigger on phrases like
  "event study", "parallel trends", "pre-trends", "dynamic treatment effects", "leads and lags",
  "TWFE", "two-way fixed effects", "staggered adoption", "staggered treatment",
  "difference-in-differences", "DiD", "Sun and Abraham", "Callaway and Sant'Anna",
  "de Chaisemartin", "Borusyak", "did_multiplegt", "fixest", "did2s", "bacon decomposition",
  or any reference to plotting coefficients around a treatment event. Also trigger when the user
  uploads panel data and wants to estimate treatment effects with variation in treatment timing.
  All code is in R.
---

# Event Study Skill

This skill covers everything needed to conduct event studies in R - from the traditional
two-way fixed effects (TWFE) approach through modern robust estimators that handle
staggered treatment timing and heterogeneous treatment effects.

## When to Use This Skill

Use this skill when the user wants to:
- Create event study plots (coefficient plots around a treatment event)
- Test for parallel pre-trends in a difference-in-differences design
- Estimate dynamic treatment effects
- Work with staggered treatment adoption (units treated at different times)
- Implement any of the modern DiD estimators (Callaway & Sant'Anna, Sun & Abraham, etc.)
- Diagnose problems with TWFE under treatment effect heterogeneity

## Quick Decision Tree

Before writing any code, determine the user's situation:

1. **Is treatment timing the same for all treated units?**
   - Yes → Traditional TWFE event study is fine. See `traditional-event-study.md`
   - No (staggered) → Go to step 2.

2. **Is there reason to expect heterogeneous treatment effects across cohorts or over time?**
   - No strong reason → Traditional TWFE may still be OK, but consider robust alternatives.
   - Yes or unsure → Use a robust estimator. See `modern-extensions.md`

3. **What is the user's goal?**
   - Quick visualization of pre-trends → Traditional approach, fast and familiar.
   - Publication-quality estimation → Recommend a robust estimator + traditional as comparison.
   - Diagnostic check → Bacon decomposition to understand TWFE weights.

## Core Concepts (Brief)

An event study plot displays estimated coefficients for leads (pre-treatment periods) and lags
(post-treatment periods) relative to a baseline period (typically one period before treatment).
The key elements are:

- **Relative time**: Time reindexed so that treatment occurs at period 0 for each unit.
- **Baseline/reference period**: Usually t = -1 (omitted from regression, normalized to zero).
- **Pre-trend coefficients**: Periods before treatment. If these are close to zero, it supports
  the parallel trends assumption.
- **Post-treatment coefficients**: These capture the dynamic treatment effect over time.

The parallel trends assumption states that, absent treatment, treated and control units would
have followed the same trajectory. Pre-trend coefficients near zero are necessary (but not
sufficient) evidence for this.

## Workflow

For any event study request, follow this general workflow:

1. **Understand the data**: Identify the panel structure (unit ID, time variable, treatment
   indicator, outcome). Ask the user if not clear.
2. **Determine treatment timing**: Is it uniform or staggered?
3. **Choose the estimator**: Use the decision tree above.
4. **Estimate the model**: Follow the relevant reference file.
5. **Create the plot**: Always produce a clean, publication-ready event study plot.
6. **Interpret results**: Discuss pre-trends, post-treatment dynamics, and any concerns.

## Reference Files

Read these as needed based on the user's situation:

- `traditional-event-study.md` - Traditional TWFE event study with `fixest`.
  Read this for any event study request. It covers the baseline approach, plotting,
  and the assumptions behind it.

- `modern-extensions.md` - Modern robust estimators for staggered designs.
  Read this when treatment timing varies across units or when the user asks about
  heterogeneous treatment effects, or any of the newer DiD methods.

- `diagnostics-and-testing.md` - Pre-trend testing, placebo checks,
  Bacon decomposition, sensitivity analysis. Read this when the user wants to
  validate their design or when you spot potential issues.

## Key R Packages

| Package | Purpose | When to use |
|---------|---------|-------------|
| `fixest` | TWFE event studies, Sun & Abraham | Default starting point |
| `did` | Callaway & Sant'Anna estimator | Staggered treatment, heterogeneous effects |
| `did2s` | Gardner (2022) two-stage DiD | Staggered treatment, clean decomposition |
| `DIDmultiplegt` | de Chaisemartin & D'Haultfoeuille | Staggered, robust to heterogeneity |
| `bacondecomp` | Bacon decomposition | Diagnosing TWFE problems |
| `HonestDiD` | Sensitivity analysis for pre-trends | Robustness checks on parallel trends |
| `ggplot2` | Plotting | Always |
| `modelsummary` | Regression tables | When user needs tables |

## Plotting Standards

All event study plots should follow these defaults (user can override):

- Use `ggplot2` with `theme_minimal()` or a clean custom theme
- Include a vertical dashed line at t = 0 (treatment onset)
- Include a horizontal dashed line at y = 0 (null effect)
- **IMPORTANT: Use discrete point estimates with vertical error bars (`geom_point` + `geom_errorbar`),
  NOT connected lines with shaded ribbons (`geom_line` + `geom_ribbon`).** Each period `t` should
  show an individual point with its own error bar. This is the standard format in economics journals.
- Show 95% confidence intervals as error bars (vertical lines at each point)
- Label axes clearly: "Periods Relative to Treatment" (x) and the outcome name (y)
- Normalize the reference period coefficient to 0 explicitly
- Use colorblind-friendly palettes when comparing multiple groups
- If comparing estimators, use facets or distinct colors/shapes with a legend

## Common Pitfalls to Watch For

- **Forgetting to set the reference period**: Always drop one pre-treatment period.
- **Binning endpoint periods**: With limited pre/post periods, bin the endpoints
  (e.g., "-5+" and "5+") to avoid small-sample noise.
- **Not-yet-treated as controls**: In staggered settings, TWFE uses not-yet-treated
  units as controls, which can introduce bias if treatment effects are heterogeneous.
- **Interpreting pre-trends as proof of parallel trends**: Pre-trends being zero is
  necessary but not sufficient. Absence of evidence is not evidence of absence.
- **Unbalanced panels**: Missing observations can distort event study estimates,
  especially at the endpoints.
