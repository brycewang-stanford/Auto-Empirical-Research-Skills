# Step 3 — Descriptive Statistics & Table 1 (Deep Reference)

Goal: before any regression, produce the full set of descriptives a reader needs to understand the sample — size, central tendency, dispersion, comparison across treatment groups, balance, correlations, and key distributions. Every applied paper has these outputs; they are read more carefully than any regression table.

## Contents

1. Full-sample summary (Table 1, column 1)
2. Stratified Table 1 (treated vs. control + SMDs)
3. Weighted descriptives
4. Correlation matrix + heatmap + significance stars
5. Distribution plots (histogram, KDE, ECDF, QQ)
6. Box / violin / strip comparisons across groups
7. Time-series trends (treated vs. control)
8. Panel balance diagnostics visualized
9. Binned means / binscatter (pre-regression visual of y~x)
10. Publication-ready export (LaTeX, Word, Excel)

---

## 1. Full-sample summary (Table 1, column 1)

```python
import pandas as pd
import numpy as np

analysis_vars = ["log_wage","training","age","edu","tenure","female","union"]

tbl = df[analysis_vars].agg(["count","mean","std","min",
                             lambda s: s.quantile(0.25),
                             "median",
                             lambda s: s.quantile(0.75),
                             "max"]).T
tbl.columns = ["N","Mean","SD","Min","P25","Median","P75","Max"]
tbl = tbl.round(3)
print(tbl)
```

For categorical / binary: report the *frequency*, not the mean alone:

```python
for c in ["female","union","industry"]:
    print(df[c].value_counts(dropna=False, normalize=True).round(3))
    print("-"*40)
```

---

## 2. Stratified Table 1 (treated vs. control + SMDs)

This is the single most important descriptive table in an empirical paper.

```python
from scipy import stats as sps

def table1(df, by, cols, paired=False):
    """
    by   : group variable (0/1)
    cols : list of numeric columns
    Returns mean/SD per group, diff, SMD, t-test p-value.
    """
    rows = []
    for c in cols:
        t  = df.loc[df[by]==1, c].dropna()
        ct = df.loc[df[by]==0, c].dropna()
        mean_diff = t.mean() - ct.mean()
        pooled_sd = np.sqrt((t.var() + ct.var()) / 2)
        smd = mean_diff / pooled_sd if pooled_sd > 0 else np.nan
        tt  = sps.ttest_ind(t, ct, equal_var=False) if not paired else sps.ttest_rel(t, ct)
        rows.append({
            "var": c,
            "N_treat": len(t),     "N_ctrl": len(ct),
            "mean_treat": t.mean(),"sd_treat": t.std(),
            "mean_ctrl":  ct.mean(),"sd_ctrl":  ct.std(),
            "diff": mean_diff, "SMD": smd, "p_ttest": tt.pvalue,
        })
    return pd.DataFrame(rows).round(3)

t1 = table1(df, by="training", cols=["log_wage","age","edu","tenure","female"])
print(t1)
```

**Interpretation rules**:
- `|SMD| < 0.1`: well-balanced covariate (the PSM / matching literature's default threshold)
- `|SMD| 0.1–0.25`: modest imbalance; control explicitly in regression
- `|SMD| > 0.25`: severe imbalance; consider matching / IPW

**Categorical version** (uses chi-square):

```python
def table1_cat(df, by, cols):
    rows = []
    for c in cols:
        ct = pd.crosstab(df[c], df[by])
        chi2, p, *_ = sps.chi2_contingency(ct)
        props = ct / ct.sum(axis=0)
        for lvl, row in props.iterrows():
            rows.append({"var": c, "level": lvl,
                         "p_ctrl": row[0], "p_treat": row[1],
                         "chi2_p": p})
    return pd.DataFrame(rows).round(3)

print(table1_cat(df, by="training", cols=["female","union","region"]))
```

**Third-party shortcut**: the `tableone` package gives publication-ready HTML / LaTeX output:

```python
from tableone import TableOne
t1 = TableOne(df,
              columns=["log_wage","age","edu","tenure","female","union"],
              categorical=["female","union"],
              groupby="training", pval=True, smd=True)
print(t1.tabulate(tablefmt="latex_booktabs"))
```

---

## 3. Weighted descriptives

If the sample uses survey weights or inverse-probability weights:

```python
def w_mean(x, w):
    w = np.asarray(w); x = np.asarray(x)
    m = np.isfinite(x) & np.isfinite(w)
    return (x[m] * w[m]).sum() / w[m].sum()

def w_var(x, w):
    mu = w_mean(x, w)
    w = np.asarray(w); x = np.asarray(x)
    m = np.isfinite(x) & np.isfinite(w)
    return (w[m] * (x[m]-mu)**2).sum() / w[m].sum()

# Or use statsmodels DescrStatsW for weighted mean/var/quantile/CI
from statsmodels.stats.weightstats import DescrStatsW
d = DescrStatsW(df["wage"], weights=df["svy_weight"])
print(d.mean, d.std, d.quantile([0.25,0.5,0.75]))
```

---

## 4. Correlation matrix + heatmap + significance stars

```python
import seaborn as sns, matplotlib.pyplot as plt

cols = ["log_wage","age","edu","tenure","training"]
corr = df[cols].corr(method="pearson")     # or "spearman" for rank-based
print(corr.round(3))

# Heatmap
plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, vmin=-1, vmax=1, square=True)
plt.tight_layout(); plt.savefig("fig_corr_heatmap.pdf")

# Correlations with p-values
def corr_pvals(df, cols):
    pvals = pd.DataFrame(np.nan, index=cols, columns=cols)
    for i in cols:
        for j in cols:
            if i != j:
                x, y = df[[i,j]].dropna().values.T
                _, p = sps.pearsonr(x, y)
                pvals.loc[i,j] = p
    return pvals

pvals = corr_pvals(df, cols)
# Star-annotated matrix
stars = pvals.applymap(lambda p: "***" if p<0.01 else "**" if p<0.05 else "*" if p<0.1 else "")
annot = corr.round(3).astype(str) + stars
print(annot)
```

---

## 5. Distribution plots

```python
fig, axes = plt.subplots(2, 2, figsize=(10,7))

# Histogram
axes[0,0].hist(df["wage"], bins=50, edgecolor="k", alpha=0.7)
axes[0,0].set_title("Histogram — wage"); axes[0,0].set_xlabel("wage")

# KDE by group
for g, sub in df.groupby("training"):
    sub["log_wage"].plot.kde(ax=axes[0,1], label=f"training={g}")
axes[0,1].set_title("KDE — log wage by treatment"); axes[0,1].legend()

# ECDF
for g, sub in df.groupby("training"):
    sorted_y = np.sort(sub["log_wage"].dropna())
    axes[1,0].plot(sorted_y, np.arange(len(sorted_y))/len(sorted_y),
                   label=f"training={g}")
axes[1,0].set_title("ECDF — log wage by treatment"); axes[1,0].legend()

# QQ vs. Normal
sps.probplot(df["log_wage"].dropna(), dist="norm", plot=axes[1,1])
axes[1,1].set_title("QQ — log wage vs. Normal")

plt.tight_layout(); plt.savefig("fig_distributions.pdf")
```

Two-group Kolmogorov–Smirnov test (non-parametric comparison of distributions):

```python
a = df.loc[df["training"]==1, "log_wage"].dropna()
b = df.loc[df["training"]==0, "log_wage"].dropna()
ks = sps.ks_2samp(a, b)
print(f"KS stat={ks.statistic:.3f}  p={ks.pvalue:.3f}")
```

---

## 6. Box / violin / strip comparisons

```python
import seaborn as sns
fig, axes = plt.subplots(1, 3, figsize=(13,4), sharey=True)
sns.boxplot   (data=df, x="training", y="log_wage", ax=axes[0]).set_title("Box")
sns.violinplot(data=df, x="training", y="log_wage", ax=axes[1]).set_title("Violin")
sns.stripplot (data=df, x="training", y="log_wage", ax=axes[2],
               alpha=0.3, jitter=0.3).set_title("Strip")
plt.tight_layout(); plt.savefig("fig_group_compare.pdf")
```

---

## 7. Time-series trends (the DID motivation plot)

```python
trend = (df.groupby(["year","training"])["log_wage"].mean()
           .unstack().rename(columns={0:"control", 1:"treated"}))

fig, ax = plt.subplots(figsize=(7,4))
trend.plot(marker="o", ax=ax)
ax.axvline(policy_year, ls="--", color="gray", label="policy")
ax.set_ylabel("mean log wage"); ax.set_title("Pre/post trends")
ax.legend(); plt.tight_layout(); plt.savefig("fig_did_motivation.pdf")
```

Also plot **difference** (treated − control) by year — the pre-period should hug zero:

```python
diff = trend["treated"] - trend["control"]
diff.plot(marker="o"); plt.axhline(0, ls="--", color="k")
plt.axvline(policy_year, ls="--", color="gray")
plt.ylabel("Δ log wage (treated − control)")
plt.savefig("fig_did_diff.pdf")
```

---

## 8. Panel balance diagnostics

```python
# 8a. Units per year
units_per_year = df.groupby("year")["worker_id"].nunique()
units_per_year.plot(kind="bar"); plt.ylabel("# unique workers")
plt.savefig("fig_panel_count.pdf")

# 8b. Observations per unit
obs_per_unit = df.groupby("worker_id")["year"].count()
obs_per_unit.hist(bins=30); plt.xlabel("# years observed")
plt.savefig("fig_panel_hist.pdf")

# 8c. Treatment-cohort sizes (staggered DID)
cohort_sizes = df.groupby("first_treat_year")["worker_id"].nunique()
cohort_sizes.plot(kind="bar"); plt.ylabel("# units treated")
plt.savefig("fig_cohort_sizes.pdf")

# 8d. Heatmap of observations (unit × year)
obs_matrix = df.assign(obs=1).pivot_table(index="worker_id", columns="year",
                                          values="obs", fill_value=0)
sns.heatmap(obs_matrix, cmap="Greys", cbar=False)
plt.title("Observed (black) vs. missing (white)")
plt.savefig("fig_obs_heatmap.pdf")
```

---

## 9. Binned means / binscatter

Gives a pre-regression eye-check of the shape of y~x.

```python
# Manual binscatter
df["tenure_bin"] = pd.qcut(df["tenure"], 20, duplicates="drop")
bs = df.groupby("tenure_bin").agg(x=("tenure","mean"),
                                  y=("log_wage","mean"),
                                  n=("log_wage","count"))
plt.errorbar(bs["x"], bs["y"], yerr=bs["y"].std()/np.sqrt(bs["n"]),
             fmt="o", capsize=3)
plt.xlabel("tenure (bin mean)"); plt.ylabel("log wage (bin mean)")
plt.savefig("fig_binscatter_tenure.pdf")

# With controls residualized out — use `binsreg`
from binsreg import binsreg
binsreg(y=df["log_wage"], x=df["tenure"], w=df[["age","edu","female"]], nbins=20)
```

---

## 10. Publication export

```python
# LaTeX via pandas — simple and robust
tbl.to_latex("table1.tex", float_format="%.3f", escape=False,
             column_format="lcccccccc")

# Word — via python-docx or stargazer's HTML (copy-paste into Word)
t1.to_excel("table1.xlsx")

# Stargazer output for a list of statsmodels-style regressions (we'll revisit in Step 8)
from stargazer.stargazer import Stargazer
# ...
```

---

## A standard Step-3 deliverable

For every empirical paper, produce these 6 artifacts in Step 3:

1. `table1_full.tex` — full-sample summary
2. `table1_stratified.tex` — treated vs. control with SMDs
3. `fig_corr_heatmap.pdf`
4. `fig_distributions.pdf` (hist + KDE + ECDF + QQ, 2×2 panel)
5. `fig_did_motivation.pdf` (time trends by group, with policy line)
6. `fig_panel_coverage.pdf` (units-per-year or obs-heatmap)

When those 6 exist, you can move to Step 4 with confidence you understand the sample.
