# Step 6 — Robustness Battery (Deep Reference)

Goal: a headline estimate isn't credible until you've shown it survives reasonable variations. A thorough robustness appendix is the difference between a reviewer-approved paper and a desk-rejected one. This file is the standard battery.

## Contents

1. Alternative specifications (progressive controls, M1 → M6)
2. Alternative standard-error families (cluster level, two-way, wild bootstrap)
3. Subsample splits (pre-defined groups)
4. Alternative outcome / treatment definitions
5. Alternative sample restrictions (winsorization, trimming)
6. Placebo — fake timing
7. Placebo — fake treatment / permutation inference
8. Specification curve (all combinations of controls)
9. Oster (2019) δ* — selection-on-unobservables bound
10. Leave-one-out (LOO) sensitivity
11. Influence / leverage re-checks
12. Sensitivity analysis (Rosenbaum bounds, e-value)

---

## 1. Alternative specifications — progressive controls

Run a ladder of specifications; display coefficients side-by-side. Stability across M1 → M6 supports identification.

```python
import pyfixest as pf

specs = [
    # (label, formula)
    ("M1",  "log_wage ~ training"),
    ("M2",  "log_wage ~ training + age + edu"),
    ("M3",  "log_wage ~ training + age + edu + tenure"),
    ("M4",  "log_wage ~ training + age + edu + tenure | worker_id"),
    ("M5",  "log_wage ~ training + age + edu + tenure | worker_id + year"),
    ("M6",  "log_wage ~ training + age + edu + tenure | worker_id + year + industry^year"),
]
results = {name: pf.feols(f, data=df, vcov={"CRV1":"worker_id"}) for name, f in specs}
pf.etable(list(results.values()))          # side-by-side
```

**Report**: the main coefficient, its SE, N, and R² (or within-R²) across all specs. A dramatic change from M3 → M5 suggests omitted variable bias; stability is reassuring.

---

## 2. Alternative standard-error families

Cluster level affects inference more than most authors acknowledge. Report the main result at 3–4 cluster levels:

```python
for cl in ["worker_id", "firm_id", "industry", "state"]:
    r = pf.feols("log_wage ~ training | worker_id + year",
                 data=df, vcov={"CRV1": cl})
    b  = r.coef()["training"]; se = r.se()["training"]
    print(f"cluster={cl:10s}  β={b:.4f}  SE={se:.4f}  t={b/se:.2f}")
```

Two-way clustering (Cameron–Gelbach–Miller):

```python
r2 = pf.feols("log_wage ~ training | worker_id + year",
              data=df, vcov={"CRV1":"worker_id+firm_id"})
```

Wild cluster bootstrap (essential when # clusters < 50; cluster robust SEs under-cover):

```python
r = pf.feols("log_wage ~ training | worker_id + year", data=df, vcov={"CRV1":"state"})
r.wildboottest(param="training", B=9999, seed=42)
```

Newey–West / HAC (time-series):

```python
import statsmodels.formula.api as smf
ols_hac = smf.ols("y ~ x", data=ts).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
```

---

## 3. Subsample splits

```python
splits = {
    "female=0": df["female"]==0, "female=1": df["female"]==1,
    "young"   : df["age"] < 40,  "old"     : df["age"] >= 40,
    "manuf"   : df["industry"]=="manuf",
    "service" : df["industry"]=="service",
}

for name, mask in splits.items():
    r = pf.feols("log_wage ~ training | worker_id + year",
                 data=df[mask], vcov={"CRV1":"worker_id"})
    print(f"{name:10s}  β={r.coef()['training']:.4f}  SE={r.se()['training']:.4f}  N={int(r._N)}")
```

For heterogeneity *testing* (not just estimation), do a full-sample interaction — see `07-further-analysis.md`.

---

## 4. Alternative outcome / treatment definitions

```python
# Alternative outcome transformations
for y in ["log_wage", "ihs_wage", "wage_w1", "wage_real_log"]:
    r = pf.feols(f"{y} ~ training | worker_id + year", data=df)
    print(y, r.coef()["training"], r.se()["training"])

# Alternative treatment definitions
for t in ["training_ever", "training_hours", "training_completed", "training_intense"]:
    r = pf.feols(f"log_wage ~ {t} | worker_id + year", data=df)
    print(t, r.coef()[t], r.se()[t])
```

If the main effect only shows up under one specific definition → suspicious.

---

## 5. Alternative sample restrictions

```python
# Winsorization sensitivity
for lo, hi in [(0.00,0.00), (0.01,0.01), (0.05,0.05)]:
    y = winsorize(df["log_wage"], limits=[lo, hi]).data
    d2 = df.assign(y=y)
    r = pf.feols("y ~ training | worker_id + year", data=d2)
    print(f"winsorize {lo*100:.0f}%/{(1-hi)*100:.0f}%: β={r.coef()['training']:.4f}")

# Trim sensitivity
for trim in [0.01, 0.05]:
    lo = df["log_wage"].quantile(trim); hi = df["log_wage"].quantile(1-trim)
    mask = (df["log_wage"] >= lo) & (df["log_wage"] <= hi)
    r = pf.feols("log_wage ~ training | worker_id + year", data=df[mask])
    print(f"trim {trim*100:.0f}%: β={r.coef()['training']:.4f}")
```

---

## 6. Placebo — fake timing

Shift the "treatment" backward in time to a period before the real policy. The placebo coefficient should be ~0.

```python
# Fake treatment 3 years earlier
df["fake_first_treat"] = df["first_treat_year"] - 3
df["fake_post"] = (df["year"] >= df["fake_first_treat"]).astype(int)

# Drop the true post-period so the placebo isn't contaminated by the real effect
df_placebo = df[df["year"] < df["first_treat_year"]].copy()
r_placebo = pf.feols("log_wage ~ fake_post | worker_id + year",
                     data=df_placebo, vcov={"CRV1":"worker_id"})
r_placebo.summary()       # expect insignificant coefficient
```

For event studies, drop the real post period and re-estimate pre-period coefficients: all should be indistinguishable from zero.

---

## 7. Placebo — fake treatment / permutation inference

Shuffle treatment across units; re-estimate many times; compare observed coefficient to permutation distribution.

```python
obs_coef = pf.feols("log_wage ~ training | worker_id + year",
                    data=df, vcov={"CRV1":"worker_id"}).coef()["training"]

# Unit-level permutation (preserves within-unit trajectory; randomizes who gets treated)
unit_treat = df.groupby("worker_id")["training"].max()        # whether unit ever treated
perm_coefs = []
for s in range(1000):
    new_order = unit_treat.sample(frac=1, random_state=s).values
    mapping = dict(zip(unit_treat.index, new_order))
    df["training_perm"] = df["worker_id"].map(mapping) * df["training"].groupby(df["worker_id"]) \
                                                                        .transform(lambda g: (g>0).astype(int))
    r = pf.feols("log_wage ~ training_perm | worker_id + year", data=df)
    perm_coefs.append(r.coef()["training_perm"])

p_perm = np.mean(np.abs(perm_coefs) >= abs(obs_coef))
print(f"Permutation p = {p_perm:.3f}")

# Plot the distribution
plt.hist(perm_coefs, bins=50, alpha=0.7)
plt.axvline(obs_coef, color="red", lw=2, label=f"observed = {obs_coef:.3f}")
plt.legend(); plt.xlabel("Permuted coefficient")
plt.savefig("fig_permutation.pdf")
```

---

## 8. Specification curve

Fit the model across every combination of controls / fixed effects / outcome / treatment definitions, and plot the distribution of estimates.

```python
import itertools

outcomes     = ["log_wage", "wage_w1"]
treatments   = ["training", "training_ever"]
controls_opt = [[], ["age"], ["age","edu"], ["age","edu","tenure"]]
fe_opt       = ["", "worker_id", "worker_id + year", "worker_id + year + industry^year"]

rows = []
for y, t, ctrls, fe in itertools.product(outcomes, treatments, controls_opt, fe_opt):
    rhs = [t] + ctrls
    fml = f"{y} ~ {'+'.join(rhs)}"
    if fe: fml += f" | {fe}"
    try:
        r = pf.feols(fml, data=df, vcov={"CRV1":"worker_id"})
        rows.append({"y":y, "t":t, "ctrls": ",".join(ctrls) or "none",
                     "fe": fe or "none",
                     "coef": r.coef()[t], "se": r.se()[t]})
    except Exception as e:
        pass

sc = pd.DataFrame(rows).sort_values("coef").reset_index(drop=True)
sc["lb"] = sc["coef"] - 1.96*sc["se"]; sc["ub"] = sc["coef"] + 1.96*sc["se"]

# Plot — the classic specification curve
fig, ax = plt.subplots(figsize=(10,4))
ax.scatter(range(len(sc)), sc["coef"], s=10)
ax.vlines(range(len(sc)), sc["lb"], sc["ub"], color="gray", alpha=0.3)
ax.axhline(0, color="k", ls="--")
ax.set_xlabel("Specification (ordered by coefficient)")
ax.set_ylabel("Coefficient on treatment")
plt.savefig("fig_spec_curve.pdf")

print(f"Median coef: {sc.coef.median():.3f}   # positive sig: {((sc.coef-1.96*sc.se)>0).sum()}/{len(sc)}")
```

---

## 9. Oster (2019) δ* — selection on unobservables

Given R² in a "short" and "long" regression, derive the bias-adjusted coefficient and how strong selection on unobservables would need to be (relative to observables) to null the effect.

```python
def oster_delta(beta_short, beta_long, R2_short, R2_long, R_max=None):
    """
    Oster (2019) delta*, assuming linear selection.
    R_max = hypothetical R^2 if ALL confounders observed (commonly 1.3*R2_long, capped at 1).
    Returns delta* (if >1, selection on unobs must exceed selection on obs to eliminate the effect).
    """
    if R_max is None: R_max = min(1.3*R2_long, 1.0)
    num   = (beta_long) * (R2_long - R2_short)
    denom = (beta_short - beta_long) * (R_max - R2_long)
    return num / denom if denom != 0 else np.nan

r_s = pf.feols("log_wage ~ training", data=df).fit()
r_l = pf.feols("log_wage ~ training + age + edu + tenure + female | worker_id + year", data=df)
print(f"δ* = {oster_delta(r_s.coef()['training'], r_l.coef()['training'], r_s._R2, r_l._R2):.2f}")
# |δ*| > 1 = basic robustness; |δ*| > 2 = strong robustness to unobservables.
```

---

## 10. Leave-one-out sensitivity

```python
units = df["worker_id"].unique()
loo_coefs = []
for u in np.random.choice(units, size=min(500, len(units)), replace=False):
    r = pf.feols("log_wage ~ training | worker_id + year",
                 data=df[df.worker_id != u])
    loo_coefs.append(r.coef()["training"])

plt.hist(loo_coefs, bins=50)
plt.axvline(obs_coef, color="red", lw=2)
plt.title("Leave-one-unit-out coefficient distribution")
plt.savefig("fig_loo.pdf")
```

For panel papers, also try leaving out entire years, entire cohorts, or entire geographic regions.

---

## 11. Influence / leverage re-checks

```python
# See 04-statistical-tests.md §12 for the full OLSInfluence recipe.
# For the robustness section: drop the top 1% most influential obs and rerun.
from statsmodels.stats.outliers_influence import OLSInfluence
ols_full = smf.ols("log_wage ~ training + age + edu + tenure", data=df).fit()
inf = OLSInfluence(ols_full)
cd  = inf.cooks_distance[0]

mask = cd < np.quantile(cd, 0.99)
r_drop = pf.feols("log_wage ~ training | worker_id + year",
                  data=df.loc[mask], vcov={"CRV1":"worker_id"})
print("Main:", obs_coef, "Drop top 1% Cook's D:", r_drop.coef()["training"])
```

---

## 12. Sensitivity — Rosenbaum bounds / e-value

### Rosenbaum bounds (for matched-pair studies)

Asks: how strong would an unobserved confounder have to be (in odds ratio) to nullify the significance of the effect?

```python
# Use pysensemakr or hand-roll via matched-pair signed-rank test over Gamma in [1, 1.5, 2, 3]
# See Rosenbaum (2002) for formula.
```

### E-value (VanderWeele & Ding 2017)

```python
def evalue(rr):
    """E-value for a risk ratio (point estimate only; extend to CI lb for conservative)."""
    if rr < 1: rr = 1/rr
    return rr + np.sqrt(rr*(rr-1))

# Convert OLS coefficient to approximate RR (when outcome is not too rare)
# For continuous outcomes, convert via Cohen's d or another mapping; see literature.
```

---

## What a strong robustness appendix contains

A paper that will pass review has, at minimum:

1. **Progressive specs table** (M1–M6) with the main coefficient across all columns
2. **Cluster-level sensitivity** table (main coef at 3–4 cluster levels, + wild bootstrap if few clusters)
3. **Placebo (fake timing)** — event study on pre-period; placebo coef should be ~0
4. **Placebo (permutation)** — histogram with observed coef vs. null distribution
5. **Specification curve** — main coef across dozens of valid specs, plotted
6. **Oster δ\*** — reported for short→long spec
7. **Subsample splits** — main coef across 4–6 pre-defined subsamples
8. **Alternative outcome / treatment definitions** — main coef at 2–3 alternatives each
9. For DID: Goodman-Bacon weights + HonestDID sensitivity
10. For IV: weak-IV robust AR CI, overid test, Conley SEs if geographic
11. For RD: bandwidth sensitivity (0.5h / h / 2h), density test, covariate smoothness
12. For PSM: SMD table before/after, common-support trimmed result, entropy-balance version
