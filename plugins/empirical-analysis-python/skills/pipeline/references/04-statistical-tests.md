# Step 4 — Diagnostic Statistical Tests (Deep Reference)

Goal: before interpreting any coefficient, check the assumptions underlying its standard error and identification. The tests below cover the 5 classical concerns — normality, heteroskedasticity, autocorrelation, multicollinearity, and (for time series) stationarity — plus post-estimation endogeneity / overidentification / Hausman tests specific to IV and panel models.

Each test is presented with: **null → statistic → decision → what to do if rejected**.

## Contents

1. Normality of residuals
2. Heteroskedasticity
3. Autocorrelation (serial correlation)
4. Multicollinearity
5. Stationarity & unit roots (time series)
6. Cointegration (time series)
7. Endogeneity (Hausman / Wu–Hausman / Durbin)
8. Weak instruments (first-stage F, Cragg–Donald, Kleibergen–Paap)
9. Overidentification (Sargan–Hansen J)
10. Panel-specific tests (Hausman FE vs. RE, Breusch–Pagan LM, Chow)
11. Model specification (RESET, link test)
12. Outlier / leverage / influence diagnostics

---

## 1. Normality of residuals

**When it matters**: small-N inference with non-bootstrapped SEs, MLE models. For OLS with N > 200 the CLT usually makes normality a non-issue.

```python
from scipy import stats as sps
from statsmodels.stats.stattools import jarque_bera

resid = ols.resid

# Shapiro-Wilk — most powerful for small samples (N ≤ 5000)
sw_stat, sw_p = sps.shapiro(resid.sample(min(5000, len(resid)), random_state=0))

# Jarque-Bera — asymptotic, based on skew & kurtosis
jb_stat, jb_p, skew, kurt = jarque_bera(resid)

# D'Agostino–Pearson
da_stat, da_p = sps.normaltest(resid)

# Kolmogorov–Smirnov vs. Normal
ks_stat, ks_p = sps.kstest((resid-resid.mean())/resid.std(), "norm")

# Anderson–Darling
ad = sps.anderson(resid, dist="norm")

print(f"Shapiro    p={sw_p:.3f}")
print(f"Jarque-Bera p={jb_p:.3f}  skew={skew:.2f}  kurt={kurt:.2f}")
print(f"D'Agostino p={da_p:.3f}")
print(f"KS         p={ks_p:.3f}")
print(f"Anderson   stat={ad.statistic:.2f}  critical@5%={ad.critical_values[2]:.2f}")
```

**If rejected + small N**: use bootstrap CIs (`fit(cov_type="HC3").bootstrap(...)`) or robust M-estimation (`sm.RLM`).

---

## 2. Heteroskedasticity

**Null**: Var(ε | X) = σ² (homoskedastic). Rejection means SEs without `cov_type="HC3"` (or cluster) are wrong.

```python
from statsmodels.stats.diagnostic import (
    het_breuschpagan, het_white, het_goldfeldquandt
)

# Breusch-Pagan (LM) — assumes linear form of heteroskedasticity
lm, lm_p, f, f_p = het_breuschpagan(ols.resid, ols.model.exog)
print(f"BP  LM={lm:.2f}  p={lm_p:.3f}   F={f:.2f}  p={f_p:.3f}")

# White (general) — includes squares and cross-products
W, W_p, f, f_p = het_white(ols.resid, ols.model.exog)
print(f"White  stat={W:.2f}  p={W_p:.3f}")

# Goldfeld-Quandt (subsample F-test) — for known structural break in variance
gq, gq_p, ord_ = het_goldfeldquandt(ols.model.endog, ols.model.exog)
print(f"GQ F={gq:.2f}  p={gq_p:.3f}")

# Breusch-Pagan via statsmodels helper
import statsmodels.api as sm
print(sm.stats.diagnostic.het_breuschpagan(ols.resid, ols.model.exog))
```

**Rejected? The fix is in the SE family, not the point estimate**:

```python
# Robust SEs (HC3 is default preferred — White-style, Davidson & MacKinnon)
ols_hc3 = ols.get_robustcov_results(cov_type="HC3")

# Cluster SEs when error correlated within group
ols_cl  = ols.get_robustcov_results(cov_type="cluster", groups=df["firm_id"])

# HAC (Newey-West) — heteroskedasticity + autocorrelation consistent (time series)
ols_hac = ols.get_robustcov_results(cov_type="HAC", maxlags=4)
```

---

## 3. Autocorrelation

**When it matters**: time-series, or panel with persistent shocks within unit. Clustered SEs by unit handle it in panel; time series needs HAC.

```python
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, acorr_ljungbox

# Durbin-Watson — detects AR(1); 2 = no autocorrelation, <1.5 or >2.5 red flag
dw = durbin_watson(ols.resid)
print(f"Durbin-Watson = {dw:.2f}")

# Breusch-Godfrey — detects AR(p) up to nlags
bg_stat, bg_p, f, f_p = acorr_breusch_godfrey(ols, nlags=4)
print(f"BG  stat={bg_stat:.2f}  p={bg_p:.3f}")

# Ljung-Box — portmanteau test of overall autocorrelation up to lag h
lb = acorr_ljungbox(ols.resid, lags=[4, 8, 12], return_df=True)
print(lb)
```

**Fix**: HAC / Newey-West SEs, or add lagged dependent variable, or model AR(1) residuals via GLS.

---

## 4. Multicollinearity

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

X = ols.model.exog   # includes constant
vif = pd.DataFrame({
    "var":  ols.model.exog_names,
    "VIF":  [variance_inflation_factor(X, i) for i in range(X.shape[1])]
})
print(vif)

# Condition number (of scaled X)
Xs = (X - X.mean(0)) / X.std(0)
print(f"Condition number (scaled): {np.linalg.cond(Xs):.1f}")
```

**Rules of thumb**:
- `VIF < 5`: fine
- `5 ≤ VIF < 10`: watch
- `VIF ≥ 10`: serious; drop / combine / ridge
- Condition number > 30: warning; > 100: severe

**Fixes**: drop one of the collinear variables; use a composite index (PCA); ridge/lasso regularization; or accept that individual coefficients will be unstable but joint hypotheses are fine.

---

## 5. Stationarity (time series)

Two complementary tests — run both. Decision = intersection of both.

```python
from statsmodels.tsa.stattools import adfuller, kpss

# ADF — Null: unit root (non-stationary). Reject (p<0.05) = stationary.
adf_stat, adf_p, *_ = adfuller(y, autolag="AIC")

# KPSS — Null: stationary. FAIL to reject (p>0.05) = stationary.
kpss_stat, kpss_p, *_ = kpss(y, regression="c", nlags="auto")

print(f"ADF  p={adf_p:.3f}   KPSS p={kpss_p:.3f}")
```

**Decision table**:

| ADF | KPSS | Conclusion |
|-----|------|------------|
| reject | fail to reject | **stationary** (use levels) |
| fail to reject | reject | **non-stationary** (first-difference or cointegrate) |
| reject | reject | inconclusive (try structural-break test) |
| fail to reject | fail to reject | insufficient info (small sample) |

**Phillips–Perron** (robust to serial correlation; use `arch` package):

```python
from arch.unitroot import PhillipsPerron, DFGLS, ZivotAndrews
print(PhillipsPerron(y).summary())
print(DFGLS(y).summary())                # more power than ADF
print(ZivotAndrews(y).summary())         # allows one structural break
```

---

## 6. Cointegration (time series)

When levels are non-stationary but a linear combination is stationary → levels can be regressed on levels without spurious results.

```python
from statsmodels.tsa.stattools import coint

score, p, crit = coint(y1, y2)           # Engle-Granger two-step
print(f"Cointegration p={p:.3f}")

# Johansen for vector / multi-variable
from statsmodels.tsa.vector_ar.vecm import coint_johansen
jres = coint_johansen(df[["y1","y2","y3"]].dropna(), det_order=0, k_ar_diff=1)
print(jres.lr1)     # trace statistics
print(jres.cvt)     # critical values
```

---

## 7. Endogeneity (Hausman / Wu–Hausman / Durbin)

**Null**: OLS is consistent (i.e., the suspect regressor is exogenous). Rejection → use IV.

```python
from linearmodels.iv import IV2SLS

iv = IV2SLS.from_formula("y ~ 1 + x_exog + [x_endog ~ z1 + z2]", data=df).fit()

print(iv.wu_hausman())         # H0: OLS consistent; rejecting ⇒ IV needed
print(iv.durbin())             # equivalent under conditional homoskedasticity
```

Output: if `p < 0.05`, OLS is inconsistent, IV is preferred (at the cost of efficiency).

---

## 8. Weak instruments

```python
# linearmodels exposes first-stage regressions directly
print(iv.first_stage)
# First-stage F for each endogenous var — target ≥ 104 (Lee et al. 2022), ≥10 rule-of-thumb
```

Cragg–Donald, Kleibergen–Paap (for multiple endogenous variables), and Stock–Yogo critical values are in `iv.diagnostics`:

```python
print(iv.diagnostics)
# Anderson-Rubin confidence set (weak-instrument robust)
print(iv.anderson_rubin)
```

---

## 9. Overidentification (Sargan–Hansen J)

**Null**: all instruments are valid (uncorrelated with error). Requires more instruments than endogenous regressors.

```python
print(iv.sargan)          # homoskedastic form
print(iv.basmann)
# For heteroskedasticity-robust version, use IVGMM:
from linearmodels.iv import IVGMM
iv_gmm = IVGMM.from_formula(...).fit()
print(iv_gmm.j_stat)      # Hansen J
```

**Interpretation**: if `p > 0.1`, cannot reject instrument validity. If `p < 0.05`, at least one instrument is invalid — the exclusion restriction probably fails.

---

## 10. Panel-specific tests

```python
from linearmodels.panel import PanelOLS, RandomEffects, compare

# FE
fe = PanelOLS.from_formula("y ~ x1 + x2 + EntityEffects + TimeEffects", df.set_index(["id","year"])).fit()
# RE
re = RandomEffects.from_formula("y ~ x1 + x2", df.set_index(["id","year"])).fit()

# Hausman (FE vs. RE) — H0: RE consistent (use RE); reject ⇒ use FE
b_diff = fe.params - re.params
v_diff = fe.cov - re.cov
hausman = b_diff @ np.linalg.pinv(v_diff) @ b_diff
p = 1 - sps.chi2.cdf(hausman, df=len(b_diff))
print(f"Hausman = {hausman:.2f},  p = {p:.3f}")

# Breusch-Pagan LM test — H0: RE not needed (pooled OLS fine)
# Test whether variance of unit effects is zero
# See linearmodels.panel.IVSystemGMM or hand-roll from residuals

# Chow test — structural break (pre/post) with known break
import statsmodels.api as sm
def chow_test(y, X, split_idx):
    r  = sm.OLS(y, X).fit()
    r1 = sm.OLS(y[:split_idx], X[:split_idx]).fit()
    r2 = sm.OLS(y[split_idx:], X[split_idx:]).fit()
    SSR_p, SSR_1, SSR_2 = r.ssr, r1.ssr, r2.ssr
    k, n = X.shape[1], len(y)
    F = ((SSR_p - SSR_1 - SSR_2)/k) / ((SSR_1+SSR_2)/(n-2*k))
    p = 1 - sps.f.cdf(F, k, n-2*k)
    return F, p
```

---

## 11. Model specification

```python
from statsmodels.stats.diagnostic import linear_reset
reset = linear_reset(ols, power=[2,3], test_type="fitted")
print(reset)   # H0: no functional-form misspecification; reject ⇒ add polynomial / log
```

Stata-style `linktest` (manual):

```python
# Regress y on yhat and yhat^2; if yhat^2 significant, specification is wrong
yhat = ols.fittedvalues
aux = sm.OLS(df["y"], sm.add_constant(np.column_stack([yhat, yhat**2]))).fit()
print(aux.summary())
```

---

## 12. Outlier / leverage / influence

```python
from statsmodels.stats.outliers_influence import OLSInfluence
inf = OLSInfluence(ols)

cooks_d      = inf.cooks_distance[0]
leverage     = inf.hat_matrix_diag
std_resid    = inf.resid_studentized_internal
dffits       = inf.dffits[0]

# Flags
high_cooks    = cooks_d    > 4/len(df)             # rule of thumb
high_leverage = leverage   > 2*X.shape[1]/len(df)
high_resid    = np.abs(std_resid) > 3
high_dffits   = np.abs(dffits) > 2*np.sqrt(X.shape[1]/len(df))

print(f"Cook's D flagged:   {high_cooks.sum()}")
print(f"High leverage:      {high_leverage.sum()}")
print(f"|stud resid| > 3:   {high_resid.sum()}")
print(f"|DFFITS| > threshold: {high_dffits.sum()}")

# Plot
fig, ax = plt.subplots(figsize=(7,5))
ax.scatter(leverage, std_resid, s=30*cooks_d/cooks_d.max()+5, alpha=0.5)
ax.axhline( 3, ls="--", color="red"); ax.axhline(-3, ls="--", color="red")
ax.set_xlabel("Leverage"); ax.set_ylabel("Studentized residual")
plt.savefig("fig_influence.pdf")
```

Refit without the top-K influential observations and report whether the main coefficient survives.

---

## A standard Step-4 deliverable

Before moving to Step 5, produce a **diagnostics report**:

```text
=== Diagnostics: baseline spec log_wage ~ training + age + edu + tenure ===
[Normality]    JB p=0.12  SW p=0.08  → OK (N=5432, CLT dominates anyway)
[Hetero]       BP p=0.003  White p=0.002  → USE HC3 / cluster SEs
[Autocorr]     DW=1.6  BG p=0.01        → CLUSTER by worker_id
[Multicoll]    max VIF=3.4  condN=14     → OK
[Stationarity] ADF p=0.04  KPSS p=0.07   → stationary in levels
[Influence]    2 observations flagged (Cook>4/N); rerun without → main coef stable
```

Store this report alongside the regression so later readers can reproduce the choice of SE family.
