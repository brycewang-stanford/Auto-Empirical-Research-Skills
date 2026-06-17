# OLS Regression — Detailed Reference

## Assumption Tests: Code and Interpretation

### 1. Heteroskedasticity

**Breusch-Pagan Test** (H₀: homoskedasticity)

```python
# Python
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(model.resid, model.model.exog)
print(f"LM stat: {bp_test[0]:.4f}, p-value: {bp_test[1]:.4f}")
# Reject H₀ → use robust SE
```

```r
# R
library(lmtest)
bptest(model)
# p < 0.05 → heteroskedasticity present
```

```stata
* Stata
estat hettest
* Significant result → use robust
```

**White Test** (more general, detects non-linear forms)

```python
from statsmodels.stats.diagnostic import het_white
white_test = het_white(model.resid, model.model.exog)
```

### 2. Autocorrelation

**Durbin-Watson** (tests first-order autocorrelation only)
- DW ≈ 2: no autocorrelation
- DW < 1.5: positive autocorrelation
- DW > 2.5: negative autocorrelation

**Breusch-Godfrey** (preferred; tests higher-order autocorrelation)

```python
from statsmodels.stats.diagnostic import acorr_breusch_godfrey
bg_test = acorr_breusch_godfrey(model, nlags=4)
print(f"LM stat: {bg_test[0]:.4f}, p-value: {bg_test[1]:.4f}")
```

```r
bgtest(model, order = 4)
```

### 3. Multicollinearity

**VIF (Variance Inflation Factor)**
- VIF < 5: acceptable
- VIF 5–10: moderate concern
- VIF > 10: serious multicollinearity

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd

X = model.model.exog
vif_data = pd.DataFrame({
    "Variable": model.model.exog_names,
    "VIF": [variance_inflation_factor(X, i) for i in range(X.shape[1])]
})
print(vif_data)
```

```r
library(car)
vif(model)
```

```stata
estat vif
```

### 4. Normality of Residuals

**Jarque-Bera Test**

```python
from scipy import stats
jb_stat, jb_pval = stats.jarque_bera(model.resid)
print(f"JB stat: {jb_stat:.4f}, p-value: {jb_pval:.4f}")
```

```r
library(tseries)
jarque.bera.test(residuals(model))
```

**Note**: With large N (n > 100), normality matters less due to CLT. Focus on outliers.

### 5. Functional Form Misspecification

**Ramsey RESET Test**

```python
from statsmodels.stats.diagnostic import linear_reset
reset_test = linear_reset(model, power=3, use_f=True)
print(reset_test)
```

```r
library(lmtest)
resettest(model, power = 2:3, type = "fitted")
```

## Standard Error Types — Full Guide

```python
# Python — all SE options
model_ols   = smf.ols('y ~ x1 + x2', data=df).fit()                    # default
model_hc1   = smf.ols('y ~ x1 + x2', data=df).fit(cov_type='HC1')      # degrees-of-freedom corrected
model_hc3   = smf.ols('y ~ x1 + x2', data=df).fit(cov_type='HC3')      # recommended for small samples
model_clust = smf.ols('y ~ x1 + x2', data=df).fit(
    cov_type='cluster', cov_kwds={'groups': df['cluster_var']})          # clustered
```

```r
# R — clustered SE
library(sandwich); library(lmtest)
coeftest(model, vcov = vcovCL(model, cluster = ~cluster_var))
```

```stata
* Stata — clustered
reg y x1 x2, cluster(cluster_var)
```

## Coefficient Interpretation Guide

| Model Form | Coefficient β₁ Interpretation |
|-----------|-------------------------------|
| Level-Level: Y = β₀ + β₁X | ΔX=1 → ΔY=β₁ (units) |
| Log-Level: ln(Y) = β₀ + β₁X | ΔX=1 → ΔY≈β₁×100% |
| Level-Log: Y = β₀ + β₁ln(X) | ΔX=1% → ΔY≈β₁/100 (units) |
| Log-Log: ln(Y) = β₀ + β₁ln(X) | ΔX=1% → ΔY≈β₁% (elasticity) |
| Interaction: β₁X₁ + β₃X₁X₂ | Marginal effect of X₁ = β₁ + β₃X₂ |
| Quadratic: β₁X + β₂X² | Marginal effect = β₁ + 2β₂X |

## Regression Table Template (LaTeX)

```latex
\begin{table}[htbp]
\centering
\caption{OLS Regression Results}
\begin{tabular}{lcc}
\hline\hline
 & (1) & (2) \\
 & Baseline & With Controls \\
\hline
X1 & 0.234*** & 0.198** \\
   & (0.045)  & (0.062) \\
X2 &          & 0.102*  \\
   &          & (0.053) \\
Constant & 1.234*** & 0.987*** \\
         & (0.123)  & (0.145) \\
\hline
Observations & 500 & 500 \\
R-squared & 0.234 & 0.278 \\
\hline\hline
\multicolumn{3}{l}{\textit{Note: HC3 robust SE in parentheses.}} \\
\multicolumn{3}{l}{* p<0.10, ** p<0.05, *** p<0.01} \\
\end{tabular}
\end{table}
```

## Python: Full Regression Report

```python
import statsmodels.formula.api as smf
import pandas as pd

def run_ols_report(formula, data, cov_type='HC3', cluster=None):
    """Run OLS with full diagnostics."""
    if cluster:
        model = smf.ols(formula, data=data).fit(
            cov_type='cluster', cov_kwds={'groups': data[cluster]})
    else:
        model = smf.ols(formula, data=data).fit(cov_type=cov_type)

    print(model.summary())

    # VIF
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    X = model.model.exog
    vifs = [variance_inflation_factor(X, i) for i in range(X.shape[1])]
    print("\nVIF:")
    for name, vif in zip(model.model.exog_names, vifs):
        print(f"  {name}: {vif:.2f}")

    # Breusch-Pagan
    from statsmodels.stats.diagnostic import het_breuschpagan
    bp = het_breuschpagan(model.resid, model.model.exog)
    print(f"\nBreusch-Pagan p-value: {bp[1]:.4f} ({'heteroskedastic' if bp[1]<0.05 else 'homoskedastic'})")

    return model
```
