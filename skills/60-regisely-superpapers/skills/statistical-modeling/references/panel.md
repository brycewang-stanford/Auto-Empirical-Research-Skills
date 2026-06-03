# Panel Methods

Starting-point reference for data with repeated observations on the same units (individuals, firms, countries, etc.) over time. **Not exhaustive.**

## Fixed Effects (Within Estimator)

**When to use:** Unobserved heterogeneity constant over time (or over another dimension) that may be correlated with the regressors.

**Assumptions:**
- **Strict exogeneity conditional on fixed effects:** `E[ε_it | X_i1, ..., X_iT, α_i] = 0` for all t
- No feedback from shocks to future regressors (violated in dynamic panels — use GMM instead)

**Implementation:**
- **Within transformation:** Subtract unit means; fast and memory-efficient for large panels
- **LSDV (dummy variable):** Include a dummy for each unit; equivalent to within transformation, slower for many units
- **Two-way FE:** Include both unit and time fixed effects

**Diagnostics:**
- **Hausman test (FE vs RE):** If rejected, use FE; if not, RE is more efficient
- **Test of joint significance of fixed effects:** F-test that all unit FE equal zero
- **Within R²:** Fraction of within-unit variation explained

**Caveat on two-way FE with heterogeneous treatment effects:** In staggered-adoption settings, two-way FE with a treatment dummy can produce biased estimates due to "forbidden comparisons" (already-treated units used as controls). See `causal-inference.md` for modern alternatives (Callaway-Sant'Anna, de Chaisemartin-D'Haultfoeuille, Borusyak-Jaravel-Spiess).

**R packages:** `fixest::feols`, `plm`
**Python packages:** `linearmodels.PanelOLS`, `pyfixest`

## Random Effects

**When to use:** Unit-specific effects plausibly uncorrelated with regressors. Rare in observational research — the assumption is strong.

**Assumptions:**
- **Orthogonality:** `E[α_i | X_i] = 0`
- Correct specification of the variance structure

**When RE makes sense:**
- Experimental data with random sampling of units from a larger population
- Data where units are exchangeable by design

**When FE is safer:**
- Observational data where unit-specific characteristics plausibly correlate with regressors

**R packages:** `plm`, `lme4` (for mixed-effects framing)
**Python packages:** `linearmodels.RandomEffects`

## Dynamic Panel (GMM)

**When to use:** Lagged outcome variable on the right-hand side of the regression (`y_it = ρ y_{i,t-1} + X_it β + α_i + ε_it`). OLS and FE are both inconsistent due to Nickell bias.

**Methods:**
- **Arellano-Bond (difference GMM):** First-differences the equation, instruments lagged changes with lagged levels
- **Blundell-Bover (system GMM):** Adds levels equation to improve efficiency when persistence is high
- **Arellano-Bover orthogonal deviations:** Alternative transformation useful with unbalanced panels

**Diagnostics:**
- **AR(1) and AR(2) tests (Arellano-Bond):** Expect significant AR(1), non-significant AR(2) in differenced residuals
- **Hansen or Sargan test:** Joint validity of instruments (but Sargan is size-distorted with heteroskedasticity; prefer Hansen)
- **Number of instruments:** Must be less than number of groups; watch for instrument proliferation (rule of thumb: instruments ≤ groups)

**Caveats:**
- Weak identification if persistence is very high (ρ near 1) — system GMM helps but not always
- Sensitive to instrument choice and lag depth

**R packages:** `plm::pgmm`, `pdynmc`
**Python packages:** `linearmodels.DynamicPanelModel`

## Mixed-Effects / Hierarchical Models

**When to use:** Nested or cross-classified structure (students in schools, patients in hospitals, repeated measures within individuals) where partial pooling across groups improves efficiency.

**Components:**
- **Random intercepts:** Group-level shifts
- **Random slopes:** Group-level variation in the effect of covariates
- **Crossed random effects:** Multiple grouping dimensions (students cross-classified with teachers)

**Assumptions:**
- Random effects have a specified distribution (typically normal)
- Random effects are uncorrelated with covariates (as in RE — strong assumption in observational research)

**When to prefer over FE:**
- Small group sizes where full FE are inefficient
- Interest in between-group variation
- Hierarchical data with many groups

**R packages:** `lme4`, `glmmTMB`, `nlme`
**Python packages:** `statsmodels.MixedLM`

## Clustered Standard Errors

**Rule of thumb:** Cluster at the level of treatment assignment or policy variation. Clustering at a finer level underestimates SEs; clustering at a coarser level is conservative but loses power.

**Multi-way clustering:** Possible when there are two (or more) dimensions of dependence (e.g., firm and year). Use when appropriate.

**Wild cluster bootstrap:** For small numbers of clusters (fewer than ~30), standard cluster-robust SEs are unreliable. Use wild cluster bootstrap instead.

**R packages:** `fixest` (built-in), `sandwich::vcovCL`, `clubSandwich`
**Python packages:** `linearmodels`, `statsmodels`

## Not in This Reference

Panel cointegration, panel quantile regression, panel spatial models, Bayesian hierarchical panels. Use the modeling process from `modeling-process.md`.
