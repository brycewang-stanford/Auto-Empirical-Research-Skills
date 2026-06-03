---
name: statistical-modeling
description: Use when estimating a statistical or econometric model, running a regression, specifying an identification strategy, testing a hypothesis, or fitting any model to empirical data. Guides the process (assumptions, estimation, reporting, diagnostics) without forcing a fixed method list.
---

# Statistical Modeling

## Overview

This skill defines the process for statistical modeling in empirical research. It is method-agnostic and field-agnostic — the appropriate method for a research question comes from the data and the estimand, not from a fixed list. Reference files organized by method family (cross-section, panel, causal inference, time series) offer starting points, but they are not exhaustive and not a boundary. Bayesian methods, machine learning, spatial models, and any other approach can be used as long as the modeling process below is followed.

## When to Use

- Estimating any regression or model
- Designing an identification strategy for a causal question
- Testing a hypothesis
- Fitting a time-series model
- "Run a DiD for me"
- "Fit a VAR"
- "Is this the right model for the data?"
- Diagnosing a model after estimation

## Mandatory Steps

Every estimation follows the six-phase modeling process below. Each phase is mandatory — skipping one corrupts inference downstream.

1. Define the estimand
2. Verify assumptions match the data
3. Choose the method
4. Estimate
5. Diagnose
6. Report

Each phase is expanded below.

### 1. Define the Estimand

What parameter do you want to learn? Is it causal or descriptive? What population does it apply to? Without a clear estimand, method choice is premature. Write the estimand down in one sentence before touching the data.

### 2. Verify Assumptions Match the Data

Every method has assumptions — exogeneity, stationarity, parallel trends, common support, no interference, proportional hazards, and so on. Check the ones that apply to your method. Document which assumptions are plausible given the context and which are weak. Weak assumptions force either a different method or a robustness discussion.

### 3. Choose the Method

Pick the simplest method that identifies the estimand under plausible assumptions. More complex methods should be justified by the estimand, the data structure, or a specific identification concern, not by novelty or sophistication signaling. When in doubt, simpler wins.

### 4. Estimate

**Before estimating, document every variable in the model.** For each variable, state: (a) its role — outcome, treatment, control, instrument, heterogeneity moderator; (b) its expected sign or direction and the theoretical or empirical basis for inclusion; (c) its scale — log, levels, percentage, standardized, index. If control variables are numerous, group them by rationale (e.g., "demographic controls," "macroeconomic conditions") and justify each group. The paper text must include this documentation — a reader should understand why every regressor is present.

**Verify scale consistency across all variables.** If some variables are in percentage points while others are in log scale, or some are in levels while others are standardized, the coefficients will not be directly comparable. Check that scales are intentional and documented. When mixing scales (e.g., log-level, log-log, percentage-level), state the implied interpretation of each coefficient explicitly. Flag any variable whose scale does not match the rest and either transform it or justify the discrepancy.

Run the model. Use standard errors appropriate to the design — clustered at the level of treatment assignment or policy variation, robust where heteroskedasticity is a concern, bootstrap where standard asymptotics are suspect. Report coefficients with standard errors and the SE type.

### 5. Diagnose

Run post-estimation checks. Does the model fit? Are residuals well-behaved? Are there influential observations driving the result? Are the testable implications of the identification assumption supported (pre-trends for DiD, balance for matching, first-stage F for IV)?

### 6. Report

Produce a publication-quality results table with coefficient, standard error (in parentheses), significance markers with the convention documented in a table note, sample size, R² or equivalent where applicable. Notes must include the SE type, the sample, and the data source.

## Reference Files

The `references/` directory has starting-point files organized by method family:

- **`modeling-process.md`** — Detailed walkthrough of the six phases above, applicable to any method
- **`cross-section.md`** — OLS, GLS, IV/2SLS, quantile regression, logit/probit, Poisson, survival, and similar single-period methods
- **`panel.md`** — Fixed effects, random effects, dynamic panel (GMM), mixed-effects and hierarchical models
- **`causal-inference.md`** — DiD (canonical and staggered), regression discontinuity (sharp and fuzzy), synthetic control, matching, inverse probability weighting
- **`time-series.md`** — ARIMA, VAR, VECM, GARCH, state-space, structural breaks, cointegration

**The reference files are starting points, not boundaries.** If a method not listed is appropriate for the research question — Bayesian hierarchical models, double machine learning, spatial autoregressive models, network regression, neural networks, synthetic DiD, anything — use it. The modeling process above applies regardless of method.

## Integration with Other Skills

- Invoke `replication-driven-research` before declaring any result final — the estimation script must reproduce the result end-to-end.
- After a main specification produces a result, signal that `robustness-checks` should be invoked.
- Use `tables-and-figures` to format the output for the paper.
- Use `academic-baseline` to enforce the causal-versus-correlational distinction in reporting.

## Anti-Patterns

- Estimating without stating the estimand
- Skipping assumption checks
- Using causal language (`effect`, `impact`) without an identification strategy
- Reporting coefficients without specifying the standard error type
- Picking the method by the significance of the result
- Choosing a complex method when a simpler one identifies the estimand
- Treating p-values as the probability the null is true
- Hiding failures of post-estimation diagnostics
- Including control variables without stating why they belong in the model
- Mixing variable scales (log, percentage, levels) without documenting the implied interpretation of coefficients
- Using a variable in levels when the relationship is log-linear, or vice versa, without justification

## Verification Before Completion

- [ ] Estimand defined explicitly in one sentence
- [ ] Assumptions checked and documented, including which are weak
- [ ] Method choice justified by the estimand and data
- [ ] Standard error type specified and appropriate for the design
- [ ] Post-estimation diagnostics run and reported
- [ ] Results generated by a script under `code/` (see `replication-driven-research`)
- [ ] Every variable has a documented role, expected direction, scale, and justification for inclusion
- [ ] Variable scales (log, percentage, levels, standardized) verified consistent or discrepancies justified
- [ ] Control variable rationale included in the paper text (individually or by logical group)
- [ ] Signal sent to invoke `robustness-checks` when the main result is produced
