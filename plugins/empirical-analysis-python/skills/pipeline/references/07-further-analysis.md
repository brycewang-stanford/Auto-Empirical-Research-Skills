# Step 7 — Further Analysis (Deep Reference)

Goal: deepen the story beyond the average treatment effect. A strong empirical paper answers three additional questions:

1. **For whom does the effect exist?** → heterogeneity
2. **Through what channel does it operate?** → mechanism
3. **Under what conditions does it strengthen or weaken?** → moderation

This file covers the classical tools for each.

## Contents

1. Heterogeneity — interaction terms, subgroup estimation, Wald test of equality
2. Heterogeneity — triple difference (DDD)
3. Heterogeneity — CATE via causal forest (high-dim moderators)
4. Heterogeneity — event studies by subgroup
5. Mechanism — outcome ladder (short / intermediate / final)
6. Mechanism — mediation (Baron–Kenny and Imai)
7. Mechanism — decomposition of channels (share of total effect)
8. Moderation — single moderator with margins plot
9. Moderated mediation
10. Dose-response (continuous treatment)
11. Spillover / general-equilibrium effects

---

## 1. Heterogeneity via interaction (preferred: tests the heterogeneity directly)

```python
import pyfixest as pf

# Clean interaction form — the interaction coefficient IS the heterogeneity test
het = pf.feols(
    "log_wage ~ training + training:female + age + edu | worker_id + year",
    data=df, vcov={"CRV1":"worker_id"}
)
het.summary()
# Coefficient on 'training:female' is the difference in ATT between female and male.

# Continuous moderator — add both interaction and main effect
het_c = pf.feols(
    "log_wage ~ training + training:tenure + age + edu | worker_id + year",
    data=df, vcov={"CRV1":"worker_id"}
)
# Marginal effect at tenure = t: β_training + β_training×tenure * t
```

---

## 2. Subgroup estimation + Wald test of equality

When you'd rather run separate regressions per group but still want a formal test of coefficient equality:

```python
male_r   = pf.feols("log_wage ~ training | worker_id + year",
                    data=df[df.female==0], vcov={"CRV1":"worker_id"})
female_r = pf.feols("log_wage ~ training | worker_id + year",
                    data=df[df.female==1], vcov={"CRV1":"worker_id"})

b1, se1 = male_r.coef()["training"],   male_r.se()["training"]
b2, se2 = female_r.coef()["training"], female_r.se()["training"]
# Independent-samples assumption — OK if covariance across splits is 0
diff = b1 - b2
se   = np.sqrt(se1**2 + se2**2)
z    = diff/se
from scipy.stats import norm
p    = 2*(1 - norm.cdf(abs(z)))
print(f"Δ = {diff:.4f}   SE={se:.4f}   z={z:.2f}   p={p:.3f}")
```

Forest plot of subgroup estimates — see `08-tables-plots.md §8.6`.

---

## 3. Triple-difference (DDD)

Compares the DID estimate across two levels of a third variable — crisp interpretation as "the causal effect of treatment is X units larger among high-exposure firms than low-exposure ones."

```python
# DDD with unit + year FE
ddd = pf.feols(
    "log_wage ~ treated*post*high_exposure | worker_id + year",
    data=df, vcov={"CRV1":"firm_id"}
)
# Coefficient on treated:post:high_exposure is the "differential DID"
```

---

## 4. Heterogeneous treatment effects via causal forest

When you have many candidate moderators and want to let the data discover heterogeneity:

```python
from econml.dml import CausalForestDML
from sklearn.ensemble import GradientBoostingRegressor

cf = CausalForestDML(
    model_y=GradientBoostingRegressor(),
    model_t=GradientBoostingRegressor(),
    n_estimators=1000,
    min_samples_leaf=5,
    cv=5,
)
cf.fit(df["log_wage"], df["training"], X=df[["age","edu","tenure","firm_size"]])

tau = cf.effect(df[["age","edu","tenure","firm_size"]])
lb, ub = cf.effect_interval(df[["age","edu","tenure","firm_size"]])

# Which X drives heterogeneity?
imp = pd.Series(cf.feature_importances_, index=["age","edu","tenure","firm_size"])
print(imp.sort_values(ascending=False))

# Best Linear Predictor of CATE — parametric summary of heterogeneity
blp = cf.ate_inference(df[["age","edu","tenure","firm_size"]])
print(blp.summary_frame())

# CATE by subgroup — binned
import matplotlib.pyplot as plt
df["tau_hat"] = tau
df["tenure_bin"] = pd.qcut(df["tenure"], 10)
cate_by_bin = df.groupby("tenure_bin")["tau_hat"].mean()
cate_by_bin.plot(kind="bar"); plt.ylabel("Average CATE")
plt.savefig("fig_cate_by_tenure.pdf")
```

---

## 5. Event studies by subgroup

```python
# Stack subgroup event studies side-by-side
fig, axes = plt.subplots(1, 2, figsize=(12,4), sharey=True)

for ax, (name, mask) in zip(axes, [("Male", df.female==0), ("Female", df.female==1)]):
    es = pf.feols("log_wage ~ i(rel, ref=-1) | worker_id + year",
                  data=df[mask], vcov={"CRV1":"worker_id"})
    coefs = es.coef().filter(like="rel::").reset_index()
    coefs.columns = ["term","coef"]
    coefs["k"]  = coefs["term"].str.extract(r"rel::(-?\d+)").astype(int)
    coefs["se"] = es.se().filter(like="rel::").values
    ax.errorbar(coefs["k"], coefs["coef"], yerr=1.96*coefs["se"], fmt="o-")
    ax.axhline(0, ls="--", color="gray"); ax.axvline(-0.5, ls="--", color="red")
    ax.set_title(name)
plt.tight_layout(); plt.savefig("fig_es_by_gender.pdf")
```

---

## 6. Mechanism — outcome ladder

Run the same treatment regression on a sequence of outcomes from proximate to distal. The effect should propagate along the chain if the mechanism is correct.

```python
outcomes = [
    ("hours_worked",   "proximate — intensive margin"),
    ("productivity",   "intermediate — output per hour"),
    ("log_wage",       "distal — total compensation"),
]

rows = []
for y, label in outcomes:
    r = pf.feols(f"{y} ~ training | worker_id + year",
                 data=df, vcov={"CRV1":"worker_id"})
    rows.append({"outcome": y, "label": label,
                 "β": r.coef()["training"], "SE": r.se()["training"],
                 "p": r.pvalue()["training"], "N": int(r._N)})
out = pd.DataFrame(rows).round(4)
print(out)
```

If the proximate outcome moves but the distal one doesn't → the mechanism exists but is too weak to affect final outcomes. If the distal moves but not the proximate → the hypothesized channel is wrong.

---

## 7. Mediation — Baron–Kenny (linear, naive)

```python
import statsmodels.formula.api as smf

# Total effect c
c = smf.ols("log_wage ~ training + age + edu", data=df).fit().params["training"]

# Path a: T → M
a = smf.ols("hours_worked ~ training + age + edu", data=df).fit().params["training"]

# Path b (and direct c'): T + M → Y
fit_med = smf.ols("log_wage ~ training + hours_worked + age + edu", data=df).fit()
b       = fit_med.params["hours_worked"]
c_prime = fit_med.params["training"]

indirect = a * b
print(f"Total effect c       = {c:.4f}")
print(f"Direct effect c'     = {c_prime:.4f}")
print(f"Indirect effect a*b  = {indirect:.4f}   ({100*indirect/c:.1f}% of total)")
```

**Limitations**: Baron–Kenny assumes no unobserved confounders of M → Y and linearity. For serious causal mediation, use Imai–Keele–Tingley:

### Imai–Keele–Tingley (via `pingouin` or manual bootstrap)

```python
from pingouin import mediation_analysis

med = mediation_analysis(
    data=df, x="training", m="hours_worked", y="log_wage",
    covar=["age","edu"], n_boot=1000, seed=0
)
print(med)
# Reports ACME (average causal mediation effect) and ADE (direct) with bootstrap CIs.
```

### Sensitivity to unmeasured M↔Y confounders (Imai sensitivity)

```python
# No mainstream Python implementation; use R's `mediation` package via rpy2.
# The key quantity is the correlation rho between residuals of M and Y equations
# at which ACME crosses zero — the smaller |rho|, the more fragile the mediation result.
```

---

## 8. Mechanism — decomposition

When you believe multiple mediators operate simultaneously:

```python
# Multi-mediator model (sequential ignorability — strong assumption)
mediators = ["hours_worked", "skill_index", "experience"]

# Fit total and direct
total  = smf.ols("log_wage ~ training + age + edu", data=df).fit().params["training"]
direct = smf.ols(f"log_wage ~ training + {' + '.join(mediators)} + age + edu",
                 data=df).fit().params["training"]
print(f"Total = {total:.4f}, Direct = {direct:.4f}")
print(f"Total mediated = {total-direct:.4f} ({100*(total-direct)/total:.1f}%)")

# Share via each mediator (approximate — Baron–Kenny style per mediator)
for m in mediators:
    a = smf.ols(f"{m} ~ training + age + edu", data=df).fit().params["training"]
    b = smf.ols(f"log_wage ~ training + {' + '.join(mediators)} + age + edu",
                data=df).fit().params[m]
    print(f"  {m}: a*b = {a*b:.4f}  ({100*a*b/total:.1f}% of total)")
```

---

## 9. Moderation — single moderator with margins plot

Goal: show how the treatment effect varies along a continuous moderator, with a CI band.

```python
import numpy as np, matplotlib.pyplot as plt

# Fit with interaction
m = smf.ols("log_wage ~ training * tenure + age + edu",
            data=df).fit(cov_type="cluster", cov_kwds={"groups": df["worker_id"]})

# Compute marginal effect of training at each level of tenure
tenures = np.linspace(df["tenure"].quantile(0.05),
                      df["tenure"].quantile(0.95), 50)
# ∂Y/∂training = β_training + β_interaction * tenure
b_t  = m.params["training"]
b_tx = m.params["training:tenure"]
V    = m.cov_params()
var_me = (V.loc["training","training"]
          + 2*tenures*V.loc["training","training:tenure"]
          + tenures**2 * V.loc["training:tenure","training:tenure"])
me     = b_t + b_tx * tenures
se     = np.sqrt(var_me)

fig, ax = plt.subplots(figsize=(6,4))
ax.plot(tenures, me, color="steelblue")
ax.fill_between(tenures, me-1.96*se, me+1.96*se, alpha=0.3)
ax.axhline(0, ls="--", color="k")
ax.set_xlabel("Tenure (years)"); ax.set_ylabel("Marginal effect of training on log wage")
plt.tight_layout(); plt.savefig("fig_marginal_effect.pdf")
```

---

## 10. Moderated mediation

Test whether the *indirect* effect differs across levels of a moderator:

```python
# Example hypothesis: training → hours → wage, stronger for skilled workers
# Approach: run two mediation analyses, one per moderator level
for level in [0, 1]:
    sub = df[df.skilled == level]
    med = mediation_analysis(data=sub, x="training", m="hours_worked", y="log_wage",
                             covar=["age","edu"], n_boot=1000, seed=0)
    print(f"skilled={level}:")
    print(med[["path","coef","CI[2.5%]","CI[97.5%]"]])
```

More rigorously: Hayes' index of moderated mediation (requires careful bootstrap).

---

## 11. Dose-response (continuous treatment)

When treatment intensity matters (hours of training, dollars of subsidy):

```python
# Piecewise-linear by deciles
df["dose_dec"] = pd.qcut(df["training_hours"], 10, labels=False)
pw = pf.feols("log_wage ~ C(dose_dec) + age + edu | worker_id + year",
              data=df, vcov={"CRV1":"worker_id"})
pf.iplot(pw)

# Smooth dose-response via spline
import patsy
df2 = df.copy()
df2["spline"] = patsy.dmatrix("bs(training_hours, df=4)", df,
                              return_type="dataframe")
# Then fit and plot the predicted outcome vs. dose holding covariates at means.

# Continuous DID (Callaway, Goodman-Bacon, Sant'Anna 2024)
# — requires the `did` R package via rpy2; Python: see sp.continuous_did in StatsPAI
```

---

## 12. Spillover / general equilibrium

When SUTVA is questionable — e.g. treating one firm in a market may affect competitors:

```python
# 12a. Control-unit proximity ("intensity of exposure" to treatment)
df["share_treated_in_mkt"] = df.groupby(["market","year"])["training"].transform("mean")

# Rerun main spec controlling for (or separately estimating effect of) exposure
sp = pf.feols(
    "log_wage ~ training + share_treated_in_mkt | worker_id + year",
    data=df, vcov={"CRV1":"market"}
)
# Coefficient on share_treated_in_mkt captures spillover.

# 12b. Doughnut exclusion — drop controls close to treated units; compare to main estimate
# 12c. Randomization at cluster level; estimate ATE via cluster-level regression
```

---

## What Step 7 typically produces

A solid further-analysis section has, at minimum:

1. **One heterogeneity table**: interaction estimates along 3–5 pre-specified moderators with Wald tests
2. **One CATE plot** from a causal forest (or subgroup CATEs with CIs)
3. **One outcome-ladder table**: treatment coefficient along 3 sequential outcomes
4. **One mediation estimate** with bootstrap CI, plus a one-paragraph discussion of the no-unmeasured-M↔Y-confounder assumption
5. **One margins plot** showing how the treatment effect varies along a continuous moderator
6. If treatment is continuous: **one dose-response curve** (spline or decile bins)
7. If SUTVA is plausibly violated: **one spillover robustness** estimate or discussion

Store each result under `tables/` and `figures/` with consistent naming so Step 8 can assemble them into the final manuscript.
