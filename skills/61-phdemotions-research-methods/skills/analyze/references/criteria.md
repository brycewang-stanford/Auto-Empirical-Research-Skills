# Confirmatory Analysis Checklist

> For each hypothesis: test assumptions, fit model, report fully. No shortcuts.

---

## 1. Pre-Registration Alignment

### 1.1 Hypothesis mapping
- Each pre-registered hypothesis has a corresponding analysis
- IV, DV, mediator, moderator, and covariate specifications match the plan
- Sample and exclusion criteria match the plan

### 1.2 Deviation tracking
- Any change from the pre-registered plan is documented in the decision log
- Deviations are labeled: "justified" (assumption violation, data issue) or "exploratory"
- Post-hoc analyses are clearly separated from confirmatory tests

---

## 2. Assumption Testing by Method

### 2.1 OLS / Linear Regression
- [ ] Linearity: component-residual plots or added-variable plots
- [ ] Normality of residuals: Q-Q plot + Shapiro-Wilk (small N) or visual (large N)
- [ ] Homoscedasticity: Breusch-Pagan test + residual vs. fitted plot
- [ ] Multicollinearity: VIF for all predictors (flag >5, serious >10)
- [ ] Independence: Durbin-Watson if temporal ordering exists
- [ ] Influential observations: Cook's distance (flag > 4/N or > 1)

**If violated:** HC3 robust SEs for heteroscedasticity. Log/sqrt transform for non-normality. Center predictors for multicollinearity. Report both OLS and robust results.

### 2.2 GLM (Logistic, Ordinal, Poisson)
- [ ] Correct link function for the outcome type
- [ ] Logistic: linearity of log-odds (Box-Tidwell test or visual)
- [ ] Poisson: overdispersion test (if significant → negative binomial)
- [ ] Ordinal: proportional odds assumption (Brant test)
- [ ] No perfect separation (logistic) — check for complete/quasi-separation
- [ ] Multicollinearity: VIF

### 2.3 Panel Regression / Fixed Effects (fixest)
- [ ] Within vs. between variation: sufficient within-unit variation in IVs
- [ ] Hausman test: fixed effects vs. random effects (or theoretical justification)
- [ ] Clustered standard errors at appropriate level
- [ ] Serial correlation: test for AR(1) in residuals
- [ ] Time-varying confounders: are fixed effects sufficient?

### 2.4 Mixed / Multilevel Models (lme4)
- [ ] ICC justifies multilevel structure (ICC > .05 or theoretical nesting)
- [ ] Random effects specification: random intercepts? random slopes?
- [ ] Convergence: model converged without warnings
- [ ] Residual normality at each level
- [ ] Sufficient clusters (>20 groups recommended for reliable variance estimates)

### 2.5 SEM / CFA (lavaan)
- [ ] Sample size: N > 200 recommended (or 10:1 parameter ratio)
- [ ] Multivariate normality: Mardia's test (if violated → MLR estimator)
- [ ] Model identification: df > 0, no Heywood cases
- [ ] Fit indices: CFI ≥ .95, TLI ≥ .95, RMSEA ≤ .06, SRMR ≤ .08
- [ ] Modification indices: review but do not apply without theoretical justification
- [ ] Factor loadings: all > .40 (ideally > .60)
- [ ] Discriminant validity: AVE > squared inter-factor correlations

### 2.6 Meta-Analysis (metafor)
- [ ] Effect size metric consistent across studies
- [ ] Heterogeneity: Q-test, I², tau²
- [ ] Random-effects vs. fixed-effects: justified by study heterogeneity
- [ ] Publication bias: funnel plot, Egger's test, trim-and-fill
- [ ] Moderator analyses: pre-registered or exploratory?

---

## 3. Reporting Requirements (All Methods)

### 3.1 Coefficients
- Unstandardized estimates (b) with SEs
- Standardized estimates (beta) where interpretable
- Test statistic (t, z, F, chi-square)
- Exact p-values to three decimal places (p < .001 if below)
- 95% confidence intervals for all key estimates

### 3.2 Effect sizes
- Cohen's d for mean comparisons
- Partial eta-squared for ANOVA effects
- R² and adjusted R² for regression models
- f² for incremental R² (added predictor blocks)
- CFI/RMSEA for SEM model fit
- I² for meta-analysis heterogeneity

### 3.3 Model fit
- Regression: R², adjusted R², F-test, AIC/BIC for model comparison
- SEM: chi-square, df, CFI, TLI, RMSEA (90% CI), SRMR
- Mixed models: ICC, AIC/BIC, likelihood ratio tests for nested models
- Meta-analysis: Q, I², tau², prediction interval

### 3.4 Diagnostic plots
- Residual vs. fitted values
- Q-Q plot of residuals
- Scale-location plot
- Cook's distance / influence plot
- Save to `output/figures/diagnostics/`

---

## 4. Output Artifacts

### 4.1 Tables
- `output/tables/hypothesis-tests.html` + `.docx` — main results
- One table per model family (e.g., all regressions in one table, SEM in another)
- R: `modelsummary::modelsummary()` for regression, `gtsummary` for descriptive comparisons
- Python: `great_tables` for formatted output

### 4.2 Model objects
- R: `output/results/models.rds` — list of fitted model objects
- Python: `output/results/models.pkl` — pickled model objects

### 4.3 Decision log
- `docs/decisions/analysis-decisions.md` — entry for every deviation or post-hoc choice

### 4.4 Analysis script
- R: `R/03_analyze.R` — functions for `targets` pipeline
- Python: `python/03_analyze.py` — functions for Snakemake pipeline
