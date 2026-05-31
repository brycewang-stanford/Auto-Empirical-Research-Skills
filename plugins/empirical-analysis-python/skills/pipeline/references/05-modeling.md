# Step 5 — Empirical Modeling (Deep Reference)

Goal: estimate the causal / predictive relationship of interest with the right estimator for the identification strategy. This file is the deep catalog — every classical estimator with its canonical call, kwargs, standard-error family, and diagnostics.

## Contents

1. OLS, WLS, GLS — variants
2. Panel data — FE, RE, between, first-differences, clustered SEs, wild bootstrap
3. Binary / ordinal / count outcomes — logit, probit, ordered logit, Poisson, NegBin
4. Instrumental variables — 2SLS, LIML, GMM, weak-IV robust CIs
5. Difference-in-differences — 2×2, TWFE, event study, CS, SA, BJS, SDiD
6. Regression discontinuity — sharp, fuzzy, kink, multi-cutoff
7. Synthetic control — ADH, SDiD, placebo inference
8. Matching / reweighting — PSM, CEM, entropy balancing, IPW, AIPW
9. Double / debiased ML — partially linear, AIPW, DR-Learner
10. Causal forest — heterogeneous effect estimation
11. Heckman selection
12. Quantile regression

---

## 1. OLS, WLS, GLS

```python
import statsmodels.formula.api as smf
import statsmodels.api as sm

# OLS — default robust SE should be HC3 (Davidson & MacKinnon)
m = smf.ols("log_wage ~ training + age + edu + tenure", data=df).fit(cov_type="HC3")
print(m.summary())

# OLS + clustered SEs (two-way clustering handled via groupby tuple)
m_cl = smf.ols("log_wage ~ training + age + edu", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["firm_id"]})

# WLS (weights as inverse variance if you believe error variance ∝ weight)
wls = smf.wls("log_wage ~ training + age", data=df, weights=1/df["var_hat"]).fit()

# GLS (general covariance structure — niche; FGLS more common)
ar1_res = sm.GLSAR(y, X, rho=1).iterative_fit(maxiter=5)

# Access common quantities
m.params        # coefficients
m.bse           # standard errors
m.pvalues
m.conf_int(0.05)
m.rsquared; m.rsquared_adj
m.nobs
m.resid; m.fittedvalues
```

### Hypothesis tests on coefficients

```python
# Single linear hypothesis: β_training = 0.05
m.t_test("training = 0.05")

# Joint: training = 0 AND age = 0
m.f_test("training = 0, age = 0")

# Equality across coefs
m.t_test("training - female = 0")
```

---

## 2. Panel data

**Default tool**: `pyfixest` (fastest, mirrors R's fixest). **Alternative**: `linearmodels.panel`.

```python
import pyfixest as pf

# Two-way FE + cluster SEs (CRV1 = cluster-robust variance, standard)
fe = pf.feols("log_wage ~ training + age + edu | worker_id + year",
              data=df, vcov={"CRV1": "worker_id"})
fe.summary()

# Multi-way clustering (two-way)
fe2 = pf.feols("log_wage ~ training + age | worker_id + year",
               data=df, vcov={"CRV1": "worker_id+firm_id"})

# High-dimensional FE (industry × year, firm × state, etc.)
fe_hd = pf.feols("log_wage ~ training | worker_id + industry^year",
                 data=df, vcov={"CRV1": "firm_id"})

# Wild cluster bootstrap (when # clusters < 50 — classic SEs under-covered)
fe.wildboottest(param="training", B=9999, seed=42)

# IV with FE — "Y ~ X_exog | fe | X_endog ~ Z"
iv_fe = pf.feols("log_wage ~ age | worker_id + year | training ~ draft_lottery",
                 data=df, vcov={"CRV1": "worker_id"})
```

### `linearmodels.panel` (when you need RE, between, or FD explicitly)

```python
from linearmodels.panel import PanelOLS, RandomEffects, BetweenOLS, FirstDifferenceOLS

dfp = df.set_index(["worker_id","year"])

# Within (FE)
fe = PanelOLS.from_formula(
    "log_wage ~ training + age + edu + EntityEffects + TimeEffects", dfp
).fit(cov_type="clustered", cluster_entity=True)

# Random effects
re = RandomEffects.from_formula("log_wage ~ training + age + edu", dfp).fit(
    cov_type="clustered", cluster_entity=True)

# Between (cross-sectional means)
be = BetweenOLS.from_formula("log_wage ~ training + age + edu", dfp).fit()

# First differences
fd = FirstDifferenceOLS.from_formula("log_wage ~ training + age + edu", dfp).fit(
    cov_type="clustered", cluster_entity=True)
```

---

## 3. Binary / ordinal / count outcomes

```python
# Logit
logit = smf.logit("employed ~ training + age + edu", data=df).fit()
print(logit.summary())
print(logit.get_margeff(at="overall").summary())       # AME — interpretable effect

# Probit
probit = smf.probit("employed ~ training + age + edu", data=df).fit()

# Ordered logit (3+ ordinal outcome) — via statsmodels MNLogit or mord
from statsmodels.miscmodels.ordinal_model import OrderedModel
ord_logit = OrderedModel(df["rating"], df[["training","age","edu"]], distr="logit").fit()

# Multinomial logit
mnl = smf.mnlogit("job_choice ~ training + age + edu", data=df).fit()

# Poisson (count or log-linear) — with FE, use pyfixest
import pyfixest as pf
pois = pf.fepois("citations ~ training + age | firm_id + year",
                 data=df, vcov={"CRV1":"firm_id"})

# Negative binomial (count w/ overdispersion)
from statsmodels.discrete.discrete_model import NegativeBinomial
nb = NegativeBinomial(df["citations"], sm.add_constant(df[["training","age"]])).fit()
```

---

## 4. Instrumental variables

```python
from linearmodels.iv import IV2SLS, IVGMM, IVLIML

# 2SLS with robust or clustered SEs
iv = IV2SLS.from_formula(
    "log_wage ~ 1 + age + edu + [training ~ draft_lottery + policy_exposure]",
    data=df
).fit(cov_type="clustered", clusters=df["firm_id"])
print(iv.summary)

# Key outputs
print(iv.first_stage)            # per-endog first-stage F
print(iv.wu_hausman())           # endogeneity test
print(iv.sargan)                 # overid test (homoskedastic)
print(iv.basmann)                # overid test (small-sample adj)
print(iv.anderson_rubin)         # weak-IV robust CI / test

# LIML — less biased when weak instruments
iv_liml = IVLIML.from_formula(..., data=df).fit()

# GMM — efficient under heteroskedasticity
iv_gmm = IVGMM.from_formula(..., data=df).fit(cov_type="robust")
print(iv_gmm.j_stat)             # Hansen J (overid, heteroskedasticity-robust)

# Anderson-Rubin confidence set (weak-IV robust)
from linearmodels.iv.results import compare
print(compare({"2SLS": iv, "LIML": iv_liml, "GMM": iv_gmm}))
```

### Bartik / shift-share IV

```python
# Z_i = sum_k s_{ik} * g_k   (industry shares × national growth rates)
def bartik(shares, growth):
    return shares @ growth          # shares: (n_units, n_industries); growth: (n_industries,)

df["bartik_z"] = bartik(shares_matrix, national_growth)
iv_bartik = IV2SLS.from_formula("y ~ 1 + controls + [endog ~ bartik_z]", data=df).fit()
```

### Conley spatial HAC SEs (for geographic instruments)

```python
iv_conley = IV2SLS.from_formula(...).fit(cov_type="kernel", bandwidth=5)
```

---

## 5. Difference-in-differences

### 5.1 2×2 DID (two periods, two groups)

```python
did = smf.ols("log_wage ~ treated * post + age + edu", data=df).fit(
    cov_type="cluster", cov_kwds={"groups": df["worker_id"]})
# Coefficient on treated:post IS the ATT
```

### 5.2 TWFE (classic two-way fixed effects; use only with simultaneous treatment)

```python
twfe = pf.feols("log_wage ~ treat_post + age | worker_id + year",
                data=df, vcov={"CRV1":"worker_id"})
```

### 5.3 Event study (dynamic DID)

```python
# Create relative-time variable (negative = pre, positive = post), base = -1
df["rel"] = df["year"] - df["first_treat_year"]
df["rel"] = df["rel"].clip(-5, 5)   # bin tails

es = pf.feols("log_wage ~ i(rel, ref=-1) | worker_id + year",
              data=df, vcov={"CRV1":"worker_id"})
pf.iplot(es)                         # pre/post coefficients plot
```

### 5.4 Staggered DID — modern estimators

For staggered adoption (units treated at different times), **TWFE is biased** (Goodman-Bacon 2021). Use one of:

```python
# --- Callaway–Sant'Anna (CS 2021) via diff-diff or R csdid via rpy2 ---
# diff-diff Python port:
from diff_diff import CS, SA, BJS, SDiD
cs = CS().fit(df, outcome="log_wage", unit="worker_id", time="year",
              cohort="first_treat_year", control_group="never_treated",
              cluster="worker_id")
cs.print_summary()

# --- Sun–Abraham (2021) — interaction-weighted event study ---
sa = SA().fit(df, outcome="log_wage", unit="worker_id", time="year",
              cohort="first_treat_year", cluster="worker_id")

# --- Borusyak–Jaravel–Spiess (2024) — imputation approach ---
bjs = BJS().fit(df, outcome="log_wage", unit="worker_id", time="year",
                cohort="first_treat_year", horizons=range(5), cluster="worker_id")

# --- Synthetic DID (Arkhangelsky et al. 2021) ---
sdid = SDiD().fit(df, outcome="log_wage", treatment="treated",
                  unit="worker_id", time="year", cluster="worker_id")
```

### 5.5 Goodman-Bacon decomposition — diagnose TWFE bias

```python
from diff_diff.diagnostics import GoodmanBaconDecomposition
gb = GoodmanBaconDecomposition().fit(df, outcome="log_wage",
                                      treatment="treated",
                                      unit="worker_id", time="year")
gb.plot()   # weights of each 2×2 comparison — negative = problematic
```

### 5.6 HonestDID (Rambachan–Roth 2023 parallel-trends sensitivity)

```python
# After event study, pass pre/post coefs + covariance to HonestDID
# Either via diff-diff's built-in or R package via rpy2.
# See diff-diff docs. Interpret as: how strong a PT violation is needed to overturn the result?
```

---

## 6. Regression discontinuity

```python
from rdrobust import rdrobust, rdbwselect, rdplot
from rddensity import rddensity

# Sharp RD
res = rdrobust(y=df["outcome"], x=df["running_var"], c=0,
               kernel="triangular", bwselect="mserd", vce="hc1")
print(res)

# Fuzzy RD (takes `fuzzy=` argument)
fuzz = rdrobust(y=df["outcome"], x=df["running_var"], c=0,
                fuzzy=df["treatment"])

# Kink RD (slope discontinuity)
kink = rdrobust(y=df["outcome"], x=df["running_var"], c=0, deriv=1)

# Multi-cutoff
from rdrobust import rdmc
mc = rdmc(y=df["outcome"], x=df["running_var"], cutoffs=[0, 5, 10])

# Bandwidth sensitivity
for h in [0.5, 0.75, 1.0, 1.25, 1.5]:
    r = rdrobust(y=df["outcome"], x=df["running_var"], c=0, h=h*res.bws.iloc[0,0])
    print(f"h={h}: coef={r.coef[0]:.3f}  p={r.pv[2]:.3f}")

# Density test (McCrary / Cattaneo et al.)
den = rddensity(df["running_var"], c=0)
print(den)   # if p < 0.05, manipulation at cutoff — RD invalid

# Covariate smoothness (placebo) — should NOT see jumps in pre-determined covariates
for cov in ["age","edu"]:
    cov_res = rdrobust(y=df[cov], x=df["running_var"], c=0)
    print(f"{cov}: jump={cov_res.coef[0]:.3f}  p={cov_res.pv[2]:.3f}")

# RD plot — visual inspection
rdplot(y=df["outcome"], x=df["running_var"], c=0)
```

---

## 7. Synthetic control

```python
# --- pysynth ---
from pysynth import Synth
sc = Synth()
sc.fit(dataprep={
    "foo_table": df,
    "predictors": ["gdp","trade","invest"],
    "predictors_op": "mean",
    "time_predictors_prior": list(range(1980, 1990)),
    "dependent": "gdp",
    "unit_variable": "country",
    "time_variable": "year",
    "treatment_identifier": "treated_country",
    "controls_identifier": control_country_list,
    "time_optimize_ssr": list(range(1960, 1990)),
    "time_plot": list(range(1960, 1998)),
})
sc.plot(["trends","weights","gaps"])

# --- Manual SC via scipy (full control) ---
from scipy.optimize import minimize
def synth_loss(w, Y_pre_ctrl, Y_pre_trt):
    return np.sum((Y_pre_trt - Y_pre_ctrl @ w)**2)
n_ctrl = Y_pre_ctrl.shape[1]
w0 = np.ones(n_ctrl)/n_ctrl
res = minimize(synth_loss, w0,
               args=(Y_pre_ctrl, Y_pre_trt),
               method="SLSQP",
               bounds=[(0,1)]*n_ctrl,
               constraints=[{"type":"eq","fun": lambda w: w.sum()-1}])
w_opt = res.x

# Post-treatment gap
gap = Y_post_trt - Y_post_ctrl @ w_opt

# RMSPE-ratio inference (placebo in-space)
def rmspe(diff, window): return np.sqrt(np.mean(diff[window]**2))
ratio_trt = rmspe(gap, post_window) / rmspe(gap, pre_window)
# Compare to distribution across placebo control units to compute p-value.
```

---

## 8. Matching / reweighting

```python
# --- Propensity score ---
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

Xc = StandardScaler().fit_transform(df[["age","edu","tenure","female"]])
ps_mod = LogisticRegression(C=1.0, max_iter=1000).fit(Xc, df["training"])
df["pscore"] = ps_mod.predict_proba(Xc)[:,1]

# Check overlap; trim common support
fig, ax = plt.subplots()
ax.hist(df.loc[df.training==1,"pscore"], bins=30, alpha=0.5, label="treated")
ax.hist(df.loc[df.training==0,"pscore"], bins=30, alpha=0.5, label="control")
ax.legend(); plt.savefig("fig_overlap.pdf")

df_trim = df[(df.pscore >= 0.05) & (df.pscore <= 0.95)].copy()

# --- PSM nearest neighbor ---
from causalml.match import NearestNeighborMatch
matcher = NearestNeighborMatch(replace=False, ratio=1, random_state=0)
matched = matcher.match(df_trim, treatment_col="training", score_cols=["pscore"])

# ATT on matched sample
att = matched.query("training==1")["log_wage"].mean() - \
      matched.query("training==0")["log_wage"].mean()

# --- Coarsened Exact Matching ---
# (No mature Python package; use R's `cem` via rpy2 or Stata's `cem`.)

# --- IPW ---
w_att = np.where(df_trim.training==1, 1, df_trim.pscore/(1-df_trim.pscore))
ipw_fit = smf.wls("log_wage ~ training", data=df_trim, weights=w_att).fit(
    cov_type="cluster", cov_kwds={"groups": df_trim["firm_id"]})

# --- AIPW / doubly robust ---
from econml.dr import LinearDRLearner
from sklearn.linear_model import LassoCV, LogisticRegressionCV
dr = LinearDRLearner(
    model_regression=LassoCV(),
    model_propensity=LogisticRegressionCV(),
)
dr.fit(df["log_wage"], df["training"], X=df[["age","edu"]], W=df[["tenure"]])
print(dr.ate(df[["age","edu"]]), dr.ate_interval(df[["age","edu"]]))

# --- Entropy balancing ---
from ebal import ebal
w = ebal(X_control=df.loc[df.training==0, ["age","edu","tenure"]].values,
         X_treated=df.loc[df.training==1, ["age","edu","tenure"]].values,
         moments=1)   # 1=means; 2=means+variances
```

### Balance diagnostics (always report before AND after)

```python
def smd(t, c):
    return (t.mean() - c.mean()) / np.sqrt((t.var()+c.var())/2)

for col in ["age","edu","tenure"]:
    before = smd(df.loc[df.training==1,col],      df.loc[df.training==0,col])
    after  = smd(matched.loc[matched.training==1,col],
                 matched.loc[matched.training==0,col])
    print(f"{col}: SMD before={before:.3f}, after={after:.3f}")
```

---

## 9. Double / debiased ML

```python
from econml.dml import LinearDML, CausalForestDML
from sklearn.ensemble import GradientBoostingRegressor

dml = LinearDML(
    model_y=GradientBoostingRegressor(),
    model_t=GradientBoostingRegressor(),
    discrete_treatment=False,
    cv=5,
)
dml.fit(df["log_wage"], df["training"], X=df[["age","edu"]], W=df[["tenure","firm_size"]])
print(dml.ate_interval(df[["age","edu"]]))
```

---

## 10. Causal forest

```python
cf = CausalForestDML(
    model_y=GradientBoostingRegressor(),
    model_t=GradientBoostingRegressor(),
    n_estimators=1000,
    min_samples_leaf=5,
    discrete_treatment=False,
    cv=5,
)
cf.fit(df["log_wage"], df["training"], X=df[["age","edu","tenure"]])

tau_hat   = cf.effect(df[["age","edu","tenure"]])             # unit-level CATE
lb, ub    = cf.effect_interval(df[["age","edu","tenure"]])
fi        = cf.feature_importances_
blp       = cf.ate_inference(df[["age","edu","tenure"]])
print(blp.summary_frame())
```

---

## 11. Heckman selection

```python
import statsmodels.api as sm

# First step: probit of selection
X_sel = sm.add_constant(df[["age","edu","marital","kids"]])
sel = sm.Probit(df["in_labor_force"], X_sel).fit()

# Compute inverse Mills ratio
from scipy.stats import norm
xb = X_sel @ sel.params
lam = norm.pdf(xb) / norm.cdf(xb)
df["mills"] = lam

# Second step: OLS with Mills ratio
main = smf.ols("log_wage ~ training + age + edu + mills",
               data=df.loc[df.in_labor_force==1]).fit()
# Coefficient on mills > 0 and significant ⇒ selection matters.
```

---

## 12. Quantile regression

```python
# Single quantile
qr50 = smf.quantreg("log_wage ~ training + age + edu", data=df).fit(q=0.5)

# Full quantile process
qrs = {q: smf.quantreg("log_wage ~ training + age + edu", data=df).fit(q=q)
       for q in [0.1,0.25,0.5,0.75,0.9]}

# Plot coefficient across quantiles
qs = list(qrs.keys())
coefs = [qrs[q].params["training"] for q in qs]
ses   = [qrs[q].bse   ["training"] for q in qs]
plt.errorbar(qs, coefs, yerr=1.96*np.array(ses), fmt="o-")
plt.xlabel("Quantile"); plt.ylabel("training coefficient")
plt.savefig("fig_qreg.pdf")
```

---

## Quick estimator → library cheat sheet

| Estimator | Go-to call |
|-----------|-----------|
| OLS, robust SE | `smf.ols(f, df).fit(cov_type="HC3")` |
| OLS, cluster SE | `...fit(cov_type="cluster", cov_kwds={"groups": g})` |
| Panel FE | `pf.feols("y ~ x \| unit+time", df, vcov={"CRV1":"unit"})` |
| Panel IV | `pf.feols("y ~ x \| unit+time \| endog ~ z", df, vcov=...)` |
| Logit | `smf.logit(f, df).fit()` — then `.get_margeff()` |
| Poisson + FE | `pf.fepois(f, df, vcov=...)` |
| 2SLS | `IV2SLS.from_formula("y ~ 1 + exog + [endog ~ z]", df).fit()` |
| 2×2 DID | `smf.ols("y ~ treated*post", df).fit(cov_type="cluster", ...)` |
| Event study | `pf.feols("y ~ i(rel, ref=-1) \| unit+time", df, vcov=...)` |
| CS / SA / BJS | `diff_diff.{CS,SA,BJS}().fit(df, ...)` |
| Sharp RD | `rdrobust(y, x, c=0)` |
| Fuzzy RD | `rdrobust(y, x, c=0, fuzzy=t)` |
| Synthetic control | `pysynth.Synth().fit(dataprep=...)` or manual `scipy.minimize` |
| PSM | `causalml.match.NearestNeighborMatch` |
| IPW | compute weights → `smf.wls(..., weights=w)` |
| AIPW / DR | `econml.dr.LinearDRLearner` |
| DML | `econml.dml.LinearDML` |
| Causal forest | `econml.dml.CausalForestDML` |
| Heckman | manual (probit → Mills → OLS) |
| Quantile reg | `smf.quantreg(f, df).fit(q=...)` |
