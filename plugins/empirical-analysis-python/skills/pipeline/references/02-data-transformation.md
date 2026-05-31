# Step 2 — Variable Construction & Transformation (Deep Reference)

Goal: from a clean DataFrame, produce the exact analysis columns that will enter the models in Step 5 — log transforms, winsorized outcomes, standardized covariates, dummies, interactions, panel operators, deflators. Keep the raw columns untouched; every analysis column is *new*, named with a suffix, and documented.

## Contents

1. Naming convention
2. Log, IHS, Box–Cox (skewed positive vars)
3. Winsorizing vs. trimming
4. Standardization (z-score / min-max / robust)
5. Categorical encoding (dummy / ordinal / target / group-mean)
6. Interaction and polynomial terms
7. Panel / time-series operators (lag, lead, diff, within, rolling)
8. Index construction (composite indicators)
9. Inflation / unit deflation (real vs. nominal)
10. Binning & discretization (quintiles, custom cuts)
11. Per-capita / rate normalization
12. Treatment-timing construction for staggered designs

---

## 1. Naming convention

Keep raw and constructed distinct. Suffixes you'll see in well-written replications:

| Suffix | Meaning |
|--------|---------|
| `_log` | natural log |
| `_ihs` | inverse hyperbolic sine |
| `_w1` | winsorized at 1%/99% |
| `_std` | z-scored |
| `_mm`  | min-max scaled to [0,1] |
| `_l1`, `_l2` | lag 1 / lag 2 |
| `_f1`  | lead 1 |
| `_d`   | first difference |
| `_dm`  | within-unit demeaned |
| `_pc`  | per-capita |
| `_real`| deflated to a base year |

Every engineered column should be one of these, so a reader knows *exactly* what's in it.

---

## 2. Log, IHS, Box–Cox

```python
import numpy as np

# Log — positive variables only; floor at 1 if zeros exist
df["wage_log"] = np.log(df["wage"].clip(lower=1))

# log(1+x) — safe when x>=0 but some are zero
df["grants_log1p"] = np.log1p(df["grants"])

# Inverse hyperbolic sine — handles zero AND negative, behaves like log for large x
df["assets_ihs"] = np.arcsinh(df["assets"])

# Box–Cox — estimate optimal lambda (requires strictly positive)
from scipy.stats import boxcox
bc, lam = boxcox(df["positive_var"].values)
df["var_bc"] = bc
print(f"Box-Cox lambda = {lam:.3f}")

# Yeo–Johnson — Box–Cox variant that accepts zero / negative
from sklearn.preprocessing import PowerTransformer
df["var_yj"] = PowerTransformer(method="yeo-johnson").fit_transform(df[["var"]])
```

**Rule of thumb**: `log` for magnitudes (wages, sales, assets), `ihs` for values that can legitimately be zero or negative (net worth, bank balances, firm profit), `log1p` for non-negative count-like data. Interpret coefficients accordingly (log ≈ elasticity; IHS ≈ log for large |x|, linear near zero).

---

## 3. Winsorizing vs. trimming

Winsorize = clip to the percentile (keep all rows). Trim = delete rows. Prefer winsorize in applied work.

```python
from scipy.stats.mstats import winsorize

# 1%/99% winsorize — most common in accounting / finance
df["wage_w1"] = winsorize(df["wage"], limits=[0.01, 0.01]).data

# Within-group winsorize — e.g. by year (so 2020 outliers clipped to 2020 percentiles)
def winsorize_group(g, col, lo=0.01, hi=0.01):
    q_lo, q_hi = g[col].quantile([lo, 1-hi])
    return g[col].clip(q_lo, q_hi)
df["wage_w1_by_year"] = df.groupby("year", group_keys=False) \
                          .apply(lambda g: winsorize_group(g, "wage"))

# Trim (drop) — only when extreme values are truly spurious
mask = (df["wage"] >= df["wage"].quantile(0.01)) & \
       (df["wage"] <= df["wage"].quantile(0.99))
df_trim = df[mask].copy()
```

Report which approach you used and at what percentile. Prefer symmetric 1/99 or 5/95.

---

## 4. Standardization

```python
# Z-score — most common for coefficient interpretation in SD units
df["age_std"] = (df["age"] - df["age"].mean()) / df["age"].std()

# Min-max to [0, 1]
df["age_mm"] = (df["age"] - df["age"].min()) / (df["age"].max() - df["age"].min())

# Robust scaling (median / IQR) — outlier-insensitive
q1, q3 = df["age"].quantile([0.25, 0.75])
df["age_rob"] = (df["age"] - df["age"].median()) / (q3 - q1)

# Scale MULTIPLE columns at once
from sklearn.preprocessing import StandardScaler, RobustScaler
cols = ["age","edu","tenure"]
df[[f"{c}_std" for c in cols]] = StandardScaler().fit_transform(df[cols])

# Within-group standardization (e.g. industry-year-normalized profitability)
df["roa_iy_std"] = df.groupby(["industry","year"])["roa"] \
                     .transform(lambda s: (s - s.mean()) / s.std())
```

---

## 5. Categorical encoding

```python
# One-hot / dummy — drop_first avoids dummy trap
df = pd.get_dummies(df, columns=["region","industry"], prefix=["reg","ind"], drop_first=True)

# Ordinal (integer codes respecting order) — only when order is meaningful
edu_order = ["<HS","HS","Some College","BA","BA+"]
df["edu_ord"] = pd.Categorical(df["education"], categories=edu_order, ordered=True).codes

# Target encoding (group-mean) — careful, leaks info; use leave-one-out in ML contexts
group_mean = df.groupby("industry")["log_wage"].transform("mean")
df["industry_tgt"] = group_mean

# Frequency encoding
df["industry_freq"] = df.groupby("industry")["industry"].transform("count")

# Keep as pandas Categorical (pyfixest, statsmodels formula API will dummy-encode on the fly)
df["industry"] = df["industry"].astype("category")
```

---

## 6. Interaction and polynomial terms

```python
# Explicit columns (useful if you'll inspect / plot them)
df["age_sq"]         = df["age"] ** 2
df["age_cu"]         = df["age"] ** 3
df["training_x_edu"] = df["training"] * df["edu"]
df["trt_x_post"]     = df["treated"] * df["post"]        # 2×2 DID

# Formula-based (statsmodels / pyfixest handle these without explicit columns)
#   "y ~ training * female"    → main + main + interaction
#   "y ~ training + I(age**2)" → polynomial inline
#   "y ~ training + age:edu"   → interaction only, no main
```

---

## 7. Panel / time-series operators

```python
df = df.sort_values(["worker_id","year"])

# Lag / lead (within unit — CRITICAL: groupby().shift, not plain shift)
df["wage_l1"] = df.groupby("worker_id")["log_wage"].shift( 1)
df["wage_l2"] = df.groupby("worker_id")["log_wage"].shift( 2)
df["wage_f1"] = df.groupby("worker_id")["log_wage"].shift(-1)

# First difference
df["d_wage"]  = df.groupby("worker_id")["log_wage"].diff(1)
df["d2_wage"] = df.groupby("worker_id")["log_wage"].diff(2)

# Within-unit demean (useful when not using a FE estimator)
df["wage_dm"] = df.groupby("worker_id")["log_wage"].transform(lambda s: s - s.mean())

# Growth rate
df["wage_growth"] = df.groupby("worker_id")["log_wage"].pct_change()

# Rolling window (3-year moving average)
df["wage_ma3"] = df.groupby("worker_id")["log_wage"] \
                   .transform(lambda s: s.rolling(3, min_periods=1).mean())

# Expanding mean (cumulative average up to year t)
df["wage_cummean"] = df.groupby("worker_id")["log_wage"].expanding().mean().values

# Pre-treatment baseline (useful for DID heterogeneity)
pre_mask = df["year"] < df["first_treat_year"]
df["baseline_wage"] = df[pre_mask].groupby("worker_id")["log_wage"].transform("mean")
df["baseline_wage"] = df.groupby("worker_id")["baseline_wage"].transform("first")  # broadcast
```

**Gotcha**: after `groupby().shift()`, re-sort back if you rely on position. The result is aligned on the original index so `df["wage_l1"]` lines up with `df` — but always verify with a spot check:

```python
df.sort_values(["worker_id","year"]).head(10)[["worker_id","year","log_wage","wage_l1","d_wage"]]
```

---

## 8. Index construction (composite indicators)

When you combine multiple underlying variables into one composite measure (e.g. an ESG index, a financial-constraint index):

```python
# Z-score and average (simplest, transparent)
components = ["leverage","cash_ratio","current_ratio"]
for c in components:
    df[f"{c}_z"] = (df[c] - df[c].mean()) / df[c].std()
df["fin_constraint_idx"] = df[[f"{c}_z" for c in components]].mean(axis=1)

# Principal component (first PC as the index)
from sklearn.decomposition import PCA
pca = PCA(n_components=1)
df["fin_constraint_pc1"] = pca.fit_transform(df[components].fillna(0))
print("Explained variance:", pca.explained_variance_ratio_)
print("Loadings:", dict(zip(components, pca.components_[0])))

# Inverse-covariance weighting (Anderson 2008; downweights correlated signals)
# See the `GlobalEffects` package or hand-roll via block-diagonal inverse of Σ.
```

Always report (a) which components, (b) which weights/method, (c) alternative versions (simple mean vs. PCA) in a robustness appendix.

---

## 9. Deflation (real vs. nominal)

```python
# Given a CPI series (base year = 2010)
cpi = pd.read_csv("cpi.csv")        # cols: year, cpi
df = df.merge(cpi, on="year", how="left")

base = cpi.loc[cpi["year"]==2010, "cpi"].iloc[0]
df["wage_real"]     = df["wage"]    * base / df["cpi"]
df["wage_real_log"] = np.log(df["wage_real"].clip(lower=1))

# Within-country deflation for cross-country panels (use country-specific CPI/PPP)
df["y_real_ppp"] = df["y_nom"] * df["ppp_factor"]
```

---

## 10. Binning & discretization

```python
# Equal-width
df["age_bin5"] = pd.cut(df["age"], bins=5, labels=["q1","q2","q3","q4","q5"])

# Equal-frequency (quintiles)
df["wage_quint"] = pd.qcut(df["wage"], q=5, labels=[1,2,3,4,5])

# Custom cutoffs (policy thresholds)
df["age_cat"] = pd.cut(df["age"],
                       bins=[0,18,30,45,65,200],
                       labels=["minor","young","mid","senior","retire"])
```

---

## 11. Per-capita / rate normalization

```python
# Per-capita: always divide by appropriate denominator BEFORE taking logs
df["gdp_pc"]      = df["gdp"] / df["population"]
df["gdp_pc_log"]  = np.log(df["gdp_pc"])

# Rate / ratio
df["crime_rate"]  = df["crimes"] / df["population"] * 100_000  # per 100k

# Share (bounded 0–1) → use logistic if building a regression outcome
df["mkt_share"]       = df["firm_rev"] / df.groupby(["industry","year"])["firm_rev"].transform("sum")
df["mkt_share_logit"] = np.log(df["mkt_share"] / (1 - df["mkt_share"] + 1e-9))
```

---

## 12. Treatment-timing construction for staggered DID

This is fiddly enough to deserve its own recipe. Assume each unit is treated at most once.

```python
# Treatment status by (unit, year)
df["treated_now"] = (df["year"] >= df["policy_year"]).astype(int)

# First treatment year (NaN = never treated)
df["first_treat_year"] = df.groupby("worker_id")["treated_now"] \
    .transform(lambda s: df.loc[s.index, "year"][s.values.astype(bool)].min()
                         if s.any() else np.nan)

# Relative event time (for event studies)
df["rel_time"] = df["year"] - df["first_treat_year"]            # negative = pre

# Never-treated indicator (clean control group)
df["never_treated"] = df["first_treat_year"].isna().astype(int)

# Not-yet-treated indicator (for CS / SA control groups)
df["not_yet_treated"] = ((df["first_treat_year"].isna()) |
                         (df["year"] < df["first_treat_year"])).astype(int)

# Event-time dummies (binned: pre -4, -3, -2, -1|ref, 0, +1, ..., +5, post)
def bin_rel_time(k):
    if pd.isna(k): return "never"
    if k <= -5:    return "pre_5plus"
    if k >=  5:    return "post_5plus"
    return f"k_{int(k)}"
df["rt_bin"] = df["rel_time"].apply(bin_rel_time).astype("category")
```

Double-check with a crosstab:

```python
pd.crosstab(df["first_treat_year"].fillna("never"), df["treated_now"])
```

---

## Final checklist before Step 3

- [ ] Every engineered column has a documented suffix (`_log`, `_w1`, etc.)
- [ ] No silent floor at zero when taking logs (check `(wage <= 0).sum()` first)
- [ ] Panel operators use `groupby(unit).shift()` / `.diff()`, never plain `shift()`
- [ ] All interactions / polynomials either inlined in formulas or stored with clear names
- [ ] Dummies created with `drop_first=True` to avoid dummy trap in manual matrices
- [ ] Nominal variables deflated to a clearly-stated base year
- [ ] Raw columns preserved so you can reproduce / revise transformations later
