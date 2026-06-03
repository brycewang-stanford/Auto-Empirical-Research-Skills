# Cross-Section Methods

Starting-point reference for single-period data — one observation per unit, or repeated cross-sections where panel structure is not used. **Not exhaustive.**

## OLS with Appropriate Standard Errors

**When to use:** Linear relationship between a continuous outcome and one or more covariates.

**Assumptions:**
- Linearity in parameters (transformations of variables are fine)
- Exogeneity: `E[ε | X] = 0`
- No perfect multicollinearity
- Homoskedasticity (relax with robust SEs) and no autocorrelation (relax with clustered SEs)

**Standard errors:**
- **Classical:** Only if homoskedasticity is plausible (rare in practice)
- **Robust (HC1, HC3):** Default for any cross-section
- **Clustered:** When observations are grouped (schools, firms, regions) and the regressor varies at the group level
- **HC3:** More conservative than HC1 in small samples

**Diagnostics:**
- Ramsey RESET test for functional form
- VIF or condition number for multicollinearity
- Residual plots against fitted values and covariates
- Influential observations via Cook's distance, leverage, DFBETAS

**R packages:** `fixest::feols`, `sandwich` + `lmtest` for robust SEs, `car::vif`
**Python packages:** `statsmodels`, `linearmodels`

## Instrumental Variables (2SLS)

**When to use:** Endogenous regressor (OLS inconsistent); valid instrument available.

**Assumptions:**
- **Relevance:** Instrument correlated with endogenous regressor
- **Exclusion:** Instrument affects outcome only through the endogenous regressor
- **Monotonicity (for LATE interpretation):** No defiers

**Diagnostics:**
- **First-stage F-statistic:** Rule of thumb `F > 10`; for single instrument use Montiel-Pflueger or effective F (Andrews-Stock-Sun) in weak IV regimes
- **Stock-Yogo critical values:** For inference under weak instruments
- **Sargan/Hansen test:** For overidentifying restrictions when there are more instruments than endogenous regressors
- **Reduced form:** Always inspect; the reduced form is the total effect of the instrument on the outcome

**Interpretation:** 2SLS identifies the LATE for compliers under monotonicity, not the ATE.

**R packages:** `fixest::feols` with first-stage syntax, `AER::ivreg`, `ivreg`
**Python packages:** `linearmodels.iv`

## Quantile Regression

**When to use:** Interest in heterogeneous effects across the outcome distribution, or robustness to outliers in the outcome.

**Assumptions:**
- Quantile function of the outcome conditional on covariates is linear in parameters at the chosen quantile
- Standard errors: bootstrap or asymptotic

**Diagnostics:** Process plots (coefficient path across quantiles), tests for coefficient constancy across quantiles.

**R packages:** `quantreg`
**Python packages:** `statsmodels.regression.quantile_regression`

## Binary and Count Outcomes

### Logit / Probit

**When to use:** Binary outcome (yes/no, success/failure).

**Assumptions:** Logistic (logit) or normal (probit) CDF for the latent index. Results are similar in practice; logit has the advantage of direct odds-ratio interpretation.

**Reporting:** Report marginal effects at means or average marginal effects, not raw coefficients (which are on the log-odds scale for logit). State which.

### Poisson

**When to use:** Count outcomes, or any nonnegative outcome where a log-linear conditional expectation is plausible (even without count-data assumptions — see Wooldridge 2010 for the "quasi-Poisson" argument).

**Assumptions:** `E[Y | X] = exp(Xβ)`. Strict Poisson (variance = mean) is rarely plausible; use robust SEs or quasi-Poisson.

**Overdispersion:** Variance exceeds mean. Use negative binomial, quasi-Poisson, or robust SEs.

**R packages:** `glm`, `fixest::fepois` for Poisson with fixed effects, `margins` for marginal effects
**Python packages:** `statsmodels.GLM`, `linearmodels`

## Survival Analysis

**When to use:** Outcome is time until an event, with potential censoring.

**Methods:**
- **Kaplan-Meier:** Nonparametric survival curves, good for exploration
- **Cox proportional hazards:** Semiparametric regression, interprets coefficients as log hazard ratios
- **Parametric models:** Weibull, exponential, log-logistic when a specific failure-time distribution is warranted

**Assumptions:**
- **Proportional hazards (Cox):** Hazard ratios constant over time — test with Schoenfeld residuals
- **Noninformative censoring:** Censoring independent of the event time

**R packages:** `survival`, `survminer`
**Python packages:** `lifelines`

## Not in This Reference

Bayesian regression, nonparametric regression (kernel, local polynomial), spatial regression, machine-learning methods (random forests, gradient boosting, neural networks). Use the modeling process from `modeling-process.md` and pick the method that fits the estimand.
