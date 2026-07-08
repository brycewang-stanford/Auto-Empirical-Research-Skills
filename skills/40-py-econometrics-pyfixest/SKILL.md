---
name: pyfixest-reference
description: "Dense, machine-readable API reference for PyFixest — high-dimensional fixed-effects OLS/WLS/IV and Poisson (feols, fepois, feglm), clustered/robust standard errors, R-style formula syntax, and post-estimation. Use when writing or debugging Python fixed-effects regressions with the pyfixest package."
allowed-tools: ["Read", "Write", "Edit", "Bash"]
---

# PyFixest LLM Skill Reference

> Dense, machine-readable reference for LLMs. No prose padding.
> Version: matches latest PyFixest release.

## Package Import

```python
import pyfixest as pf
```

## Core Estimation Functions

### pf.feols() — OLS / WLS / IV with Fixed Effects

```python
pf.feols(
    fml: str,                    # Formula: "Y ~ X1 + X2 | fe1 + fe2" or IV: "Y ~ exog | fe | endog ~ inst"
    data: pd.DataFrame,
    vcov: str | dict = None,     # "iid", "HC1"-"HC3", {"CRV1": "clust"}, {"CRV3": "clust"}, {"CRV1": "c1+c2"}
    weights: str = None,         # Column name for weights
    ssc: dict = None,            # Small sample correction, see pf.ssc()
    fixef_rm: str = "singleton", # "none" or "singleton"
    drop_intercept: bool = False,
    split: str = None,           # Column name to split sample by
    fsplit: str = None,          # Like split but also fits on full sample
    weights_type: str = "aweights",  # "aweights" or "fweights"
    solver: str = "scipy.linalg.solve",
    lean: bool = False,
) -> Feols | FixestMulti
```

Returns `Feols` for single model, `FixestMulti` for multiple estimation syntax.

### pf.fepois() — Poisson Regression with Fixed Effects

```python
pf.fepois(
    fml: str,                    # "Y ~ X1 + X2 | fe1 + fe2"
    data: pd.DataFrame,
    vcov: str | dict = None,
    ssc: dict = None,
    fixef_rm: str = "singleton",
    iwls_tol: float = 1e-08,
    iwls_maxiter: int = 25,
    separation_check: list[str] = None,  # ["fe"] to check for separated FE
    split: str = None,
    fsplit: str = None,
) -> Fepois | FixestMulti
```

### pf.feglm() — GLM (without FE demeaning, WIP)

```python
pf.feglm(
    fml: str,
    data: pd.DataFrame,
    family: str,                 # "gaussian", "logit", "probit"
    vcov: str | dict = None,
    separation_check: list[str] = None,
    split: str = None,
    fsplit: str = None,
) -> Feglm | FixestMulti
```

### pf.quantreg() — Quantile Regression

```python
pf.quantreg(
    fml: str,
    data: pd.DataFrame,
    vcov: str | dict = "nid",
    quantile: float | list[float] = 0.5,  # Single or list of quantiles
    method: str = "fn",          # "fn" (Frisch-Newton)
    split: str = None,
    fsplit: str = None,
) -> Feols | FixestMulti
```

## Formula Syntax

### Basic

```
"Y ~ X1 + X2"                      # OLS
"Y ~ X1 + X2 | fe1"                # OLS + one FE
"Y ~ X1 + X2 | fe1 + fe2"          # OLS + two-way FE
"Y ~ X1 + C(categorical)"          # Categorical variable as dummies
"Y ~ X1 + i(factor, ref=0)"        # Factor variable for event studies
"Y ~ X1 + i(f1, X2)"               # Interaction: factor × continuous
"Y ~ 1 | fe1 | X1 ~ Z1"           # IV: depvar ~ exog | fe | endog ~ inst
"Y ~ 1 | X1 ~ Z1 + Z2"            # IV without FE
"Y ~ X1:X2"                        # Interaction only
"Y ~ X1*X2"                        # X1 + X2 + X1:X2
"Y ~ X1 + I(X1**2)"                # Polynomial term
```

### Multiple Estimation Operators

```
"Y ~ X1 + sw(X2, X3)"              # Stepwise: two models, X2 then X3
"Y ~ X1 + sw0(X2, X3)"             # Stepwise with empty: three models
"Y ~ X1 + csw(X2, X3)"             # Cumulative stepwise: X2, then X2+X3
"Y ~ X1 + csw0(X2, X3)"            # Cumulative with empty: three models
"Y + Y2 ~ X1"                      # Multiple dependent variables
"Y ~ X1 | csw0(fe1, fe2)"          # Stepwise fixed effects
```

### Split Sample

```python
pf.feols("Y ~ X1 | fe1", data=data, split="group_var")   # Separate by group
pf.feols("Y ~ X1 | fe1", data=data, fsplit="group_var")  # Separate + full sample
```

## Post-Estimation Methods (Feols object)

### Extracting Results

```python
fit.summary()             # Print summary
fit.tidy(alpha=0.05)      # pd.DataFrame: Estimate, Std. Error, t value, Pr(>|t|), CI
fit.coef()                # pd.Series of coefficients
fit.se()                  # pd.Series of standard errors
fit.tstat()               # pd.Series of t-statistics
fit.pvalue()              # pd.Series of p-values
fit.confint(alpha=0.05)   # pd.DataFrame of confidence intervals
fit.confint(joint=True)   # Simultaneous confidence bands (multiplier bootstrap)
```

### Changing Inference

```python
fit.vcov("iid")                      # IID standard errors
fit.vcov("HC1")                      # Heteroskedasticity-robust
fit.vcov({"CRV1": "cluster_var"})    # One-way cluster-robust
fit.vcov({"CRV3": "cluster_var"})    # CRV3 cluster-robust
fit.vcov({"CRV1": "c1 + c2"})       # Two-way clustering
```

Returns self — chainable: `fit.vcov("HC1").summary()`.

### Visualization

```python
fit.coefplot()                                # Coefficient plot
pf.coefplot([fit1, fit2], keep="X1")         # Compare models
pf.iplot([fit1, fit2], coord_flip=False)     # Event study plot (for i() vars)
pf.qplot(fit_qr)                             # Quantile regression plot
```

### Prediction

```python
fit.predict()                        # In-sample predictions
fit.predict(newdata=df_new)          # Out-of-sample
fit.predict(type="response")         # Response scale (GLMs)
fit.predict(type="link")             # Link scale (GLMs)
```

### Inference Methods

```python
# Wild cluster bootstrap
fit.wildboottest(param="X1", reps=999, cluster="clust_var")

# Randomization inference
fit.ritest(resampvar="X1=0", reps=1000, cluster="group_id")

# Causal cluster variance estimator (Abadie et al. 2023)
fit.ccv(treatment="treat_var", pk=0.05, n_splits=2, seed=42)

# Wald test: H0: beta = 0
fit.wald_test(R=np.eye(k))
# Wald test: H0: R @ beta = q
fit.wald_test(R=R_matrix, q=q_vector)
```

### IV Diagnostics (Feiv objects)

```python
fit_iv._model_1st_stage          # First stage Feols object
fit_iv._f_stat_1st_stage         # First stage F-statistic
fit_iv.IV_Diag()                 # Run IV diagnostics
fit_iv._eff_F                    # Effective F-stat (Olea & Pflueger 2013)
```

### Online Learning

```python
fit.update(X_new, y_new)         # Sherman-Morrison coefficient update
```

## Reporting Functions

### pf.etable() — Regression Tables

```python
pf.etable(
    models,                        # Feols, list[Feols], or FixestMulti
    type: str = "gt",              # "gt" (Great Tables), "tex" (LaTeX), "md" (markdown), "df" (DataFrame)
    signif_code: list = None,      # e.g. [0.001, 0.01, 0.05]
    coef_fmt: str = "b \n (se)",   # Format: b=coef, se=SE, p=pval, t=tstat, ci_l, ci_u
    keep: str | list = None,       # Regex pattern(s) to keep
    drop: str | list = None,       # Regex pattern(s) to drop
    labels: dict = None,           # {"old_name": "New Label"}
    felabels: dict = None,         # {"fe_var": "FE Label"}
    show_fe: bool = True,
    show_se_type: bool = True,
    notes: str = "",
    model_heads: list = None,      # Custom column headers
    caption: str = None,           # Via kwargs
    file_name: str = None,         # Save to file (.tex, .html)
)
```

### pf.summary() — Print Results

```python
pf.summary(models, digits=3)      # models: Feols, list, or FixestMulti
```

### pf.dtable() — Descriptive Statistics

```python
pf.dtable(
    df: pd.DataFrame,
    vars: list,                    # Column names
    stats: list = None,            # ["count", "mean", "std", "min", "max", "median"]
    bycol: list[str] = None,       # Group columns (shown as separate column groups)
    byrow: str = None,             # Group variable (shown as row sections)
    type: str = "gt",              # "gt", "tex", "md", "df"
    labels: dict = None,
    digits: int = 2,
)
```

## Multiple Testing Corrections

```python
pf.bonferroni(models, param="X1")                            # Bonferroni adjusted p-values
pf.rwolf(models, param="X1", reps=9999, seed=42)             # Romano-Wolf
pf.wyoung(models, param="X1", reps=9999, seed=42)            # Westfall-Young
```

## Difference-in-Differences

### pf.event_study() — Unified Event Study API

```python
pf.event_study(
    data: pd.DataFrame,
    yname: str,              # Outcome column
    idname: str,             # Unit ID column
    tname: str,              # Time column
    gname: str,              # Group (first treatment period) column
    xfml: str = None,        # Additional covariates formula
    cluster: str = None,     # Cluster variable
    estimator: str = "twfe", # "twfe" or "did2s"
    att: bool = True,
)
```

### pf.did2s() — Gardner's Two-Stage DID

```python
pf.did2s(
    data: pd.DataFrame,
    yname: str,
    first_stage: str,        # "~ covariates | fe1 + fe2"
    second_stage: str,       # "~ i(rel_year, ref=-1.0)"
    treatment: str,          # Treatment indicator column
    cluster: str,
    weights: str = None,
)
```

### pf.lpdid() — Local Projections DID

```python
pf.lpdid(
    data: pd.DataFrame,
    yname: str,
    idname: str,
    tname: str,
    gname: str,
    vcov: str | dict = None,
    pre_window: int = None,
    post_window: int = None,
    never_treated: int = 0,
    att: bool = True,
    xfml: str = None,
)
```

### pf.panelview() — Treatment Visualization

```python
pf.panelview(data, unit="unit_col", time="time_col", treat="treat_col")
```

## Small Sample Correction

```python
pf.ssc(
    k_adj: bool = True,        # Adjust for number of estimated parameters
    k_fixef: str = "nonnested", # "nonnested" or "nested" FE adjustment
    G_adj: bool = True,         # Adjust for number of clusters
    G_df: str = "min",          # "min" or "conventional"
)
# Usage:
pf.feols("Y ~ X1 | fe1", data=data, ssc=pf.ssc(k_adj=True))
```

## Data Generators

```python
pf.get_data(N=1000, seed=1234, model="Feols")   # Synthetic data: "Feols" or "Fepois"
pf.get_twin_data(N_pairs=500, seed=42)           # Twin study data (returns to education)
pf.get_worker_panel(N_workers=500, N_firms=50, N_years=11, seed=42)  # Worker-firm panel
```

## Variance-Covariance Options

| vcov | Description |
|---|---|
| `"iid"` | Spherical errors (homoskedastic, uncorrelated) |
| `"HC1"` | Heteroskedasticity-robust (White) |
| `"HC2"` | HC2 robust |
| `"HC3"` | HC3 robust (jackknife-like) |
| `{"CRV1": "var"}` | One-way cluster-robust |
| `{"CRV3": "var"}` | CRV3 cluster-robust |
| `{"CRV1": "v1 + v2"}` | Two-way clustering |

Default: CRV1 clustered by first FE variable (if FE present), else "iid".

## Common Patterns

```python
# Basic OLS with FE and clustering
fit = pf.feols("Y ~ X1 + X2 | fe1 + fe2", data=df, vcov={"CRV1": "fe1"})

# IV regression
fit_iv = pf.feols("Y ~ exog | fe1 | endog ~ instrument", data=df)

# Multiple specifications at once
fits = pf.feols("Y ~ X1 | csw0(fe1, fe2, fe3)", data=df)
fits.etable()

# Poisson with FE
fit_pois = pf.fepois("count ~ X1 + X2 | fe1", data=df)

# Event study
fit_es = pf.feols("Y ~ i(rel_time, ref=-1) | unit + time", data=df)
pf.iplot(fit_es)

# Publication table
pf.etable([fit1, fit2, fit3], type="tex", file_name="table1.tex",
           labels={"X1": "Treatment"}, felabels={"fe1": "Unit FE"})

# Adjust SE after estimation
fit.vcov({"CRV1": "cluster"}).summary()

# Compare R fixest syntax → PyFixest
# R:     feols(Y ~ X1 | fe1, data, cluster = ~fe1)
# Py: pf.feols("Y ~ X1 | fe1", data=data, vcov={"CRV1": "fe1"})
```

## FixestMulti Methods

When multiple estimation syntax is used, returns `FixestMulti`:

```python
multi = pf.feols("Y + Y2 ~ X1 | csw0(fe1, fe2)", data=df)
multi.etable()                           # Table of all models
multi.summary()                          # Print all summaries
multi.coefplot()                         # Plot all models
multi.vcov("HC1")                        # Update all models' inference
multi.fetch_model(0)                     # Get first Feols object
multi.all_fitted_models["Y~X1"]          # Access by formula key
```
