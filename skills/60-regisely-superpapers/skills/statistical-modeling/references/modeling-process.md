# The Empirical Modeling Process

This reference expands the six-phase modeling process from `statistical-modeling/SKILL.md`. It applies to any statistical model in empirical research, regardless of discipline or method family.

## 1. Define the Estimand

An estimand is the parameter you want to learn about the world. It is distinct from the estimator (the method) and from the estimate (the number you compute). A good estimand answers:

- **What parameter?** A mean, a difference in means, a slope, an elasticity, a quantile, a hazard ratio, a treatment effect at a specific margin.
- **For what population?** The full population, a subpopulation, a local population (e.g., at a discontinuity), the treated, the untreated.
- **Causal or descriptive?** Causal estimands require counterfactual reasoning. Descriptive estimands characterize observed variation without claiming interventions would move them.
- **Aggregation?** If the estimand is heterogeneous (e.g., different effects across groups), what weights aggregate it into a single number?

Examples across fields:

- *Economics (causal):* "The average treatment effect on the treated of receiving Bolsa Família on child school enrollment in Brazilian municipalities between 2003 and 2015."
- *Political science (descriptive):* "The average ideological distance between winning and losing parties in European parliamentary elections since 1990."
- *Epidemiology (causal):* "The effect of mandatory face masks on hospitalization rates during the first three months of the COVID-19 pandemic in US counties."

Write the estimand in one sentence before touching the data. If you cannot write it clearly, the research question is not ready for estimation.

## 2. Verify Assumptions Match the Data

Every method's identification and inference depend on assumptions. Some assumptions are fundamental (e.g., ignorability, strict exogeneity, parallel trends); others are technical (e.g., homoskedasticity, stationarity). Distinguish them.

**Fundamental assumptions** must be plausible a priori, given knowledge of the data generating process. No statistical test can verify them — at best, tests can probe their testable implications.

**Technical assumptions** often have formal tests. Failing a test is a signal to use a more robust method or to explicitly adjust (robust SE, bootstrap, correction factor).

Document every assumption as one of:

- **Plausible by design** (e.g., random assignment in an experiment)
- **Plausible by argument** (with reasoning stated)
- **Weak** (with plan for robustness or acknowledgment of limitation)
- **Violated** (method must change, or the result must be reframed)

If a core assumption is violated, do not proceed with the method. Change methods or change the estimand.

## 3. Choose the Method

Apply the simplicity principle: pick the simplest method that identifies the estimand under plausible assumptions. Simpler methods are:

- Easier to interpret
- Easier to replicate
- Less prone to specification error
- More robust to unmodeled heterogeneity

More complex methods are justified when:

- The estimand itself is complex (e.g., heterogeneous treatment effects across a distribution)
- Data structure forces it (e.g., clustered, nested, time series with dependence)
- A specific identification concern requires it (e.g., endogeneity, selection, measurement error)

Avoid method choice based on:

- Novelty of the approach
- Signaling sophistication to referees
- Matching what someone else used in a "similar" paper

When in doubt, the simpler method wins.

## 4. Estimate

Run the model. A few principles:

- **Standard errors should match the design.** Cluster at the level of treatment assignment or policy variation. Use robust SEs when heteroskedasticity is plausible. Bootstrap when asymptotics are suspect (small samples, near-boundary parameters, nonstandard statistics).
- **Document numerical details.** Convergence criteria, optimizer, starting values, and any numerical tricks. Users re-running the code must see the same numbers.
- **Handle missing data explicitly.** Complete-case deletion, multiple imputation, inverse probability weighting — each implies a different estimand. Do not ignore missingness.
- **Use well-tested packages.** Stable, popular packages are audited by the community. Home-rolled implementations are a source of bugs.

## 5. Diagnose

Post-estimation diagnostics test whether the model is behaving reasonably and whether the identification assumptions are supported where testable.

Universal checks (apply to any model):

- **Residuals:** Distribution, patterns against fitted values, patterns against covariates
- **Influential observations:** Leverage, Cook's distance, DFBETAS — especially in small samples
- **Sensitivity to observations:** Leave-one-out for clusters, groups, or time periods
- **Fit statistics:** R², pseudo-R², AIC/BIC, deviance, log-likelihood — report what is standard for the method

Method-specific checks:

- **Parallel trends (DiD):** Pre-period event study, placebo periods
- **First stage (IV):** F-statistic, partial R², weak-IV critical values
- **Balance (matching/RD):** Pre-treatment covariate balance, common support
- **Stationarity (time series):** Unit root tests, differencing diagnostics

When diagnostics fail, say so. Do not silently accept a model that does not pass its own tests.

## 6. Report

A publication-quality results table contains:

- **Coefficient** (or other parameter) with appropriate precision (2-3 decimals for coefficients, 0 for sample sizes)
- **Standard error** in parentheses below the coefficient (or confidence interval as an alternative)
- **Significance markers** with the convention explicitly documented in the table note
- **Sample size** for each column
- **Fit statistics** appropriate to the method (R², pseudo-R², log-likelihood)
- **Notes** identifying the SE type, the sample, the data source, the sample period, and any non-obvious specification choices

Avoid:

- Decorations that obscure the numbers (colored cells, gradients)
- Unstated significance thresholds
- Stars without a note
- Hiding the standard error type
- Mixing multiple conventions in the same table

## Common Pitfalls

- **Confusing the estimand with the estimator.** A difference-in-differences *estimator* can target multiple *estimands* depending on aggregation. Be specific.
- **Treating p-values as probabilities of the null.** A p-value is the probability of data at least as extreme under the null, not the probability that the null is true.
- **Over-interpreting R².** High R² does not imply correct identification; low R² does not imply a useless model.
- **Ignoring dependence structure.** Clustered data with OLS SEs produces undersized confidence intervals and false discoveries.
- **Running many specifications and reporting only the best.** This is p-hacking, even when unconscious. Pre-commit to a main specification.
- **Hiding model failures.** Diagnostics that fail are information about the world. Report them.
