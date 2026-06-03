---
name: causal-inference-mixtape
description: "'This skill should be used when the user asks to implement a DiD regression, write a causal inference pipeline, set up an event study, implement instrumental variables, run a regression discontinuity design, build a synthetic control model, implement propensity score matching, write parallel trends test, implement Bacon decomposition, or needs code templates for causal inference methods in Python, R, or Stata. Based on Scott Cunningham''s Causal Inference: The Mixtape.'"
version: 1.0.0
---

# Causal Inference: The Mixtape — Code Skill

Practitioner-oriented causal inference skill built from Scott Cunningham's *Causal Inference: The Mixtape* repository. Covers 10 identification strategies with ready-to-run code templates in Python, R, and Stata.

---

## Methods Covered

| Method | Python | R | Stata | Reference |
|--------|--------|---|-------|-----------|
| OLS / Regression | statsmodels | estimatr | reg/reghdfe | `references/method-patterns.md` §1 |
| Difference-in-Differences | statsmodels + C() | lfe/fixest | xtreg/reghdfe | `references/method-patterns.md` §2 |
| Event Study (Dynamic DiD) | manual lead/lag | estimatr | reghdfe | `references/method-patterns.md` §3 |
| Staggered DiD / TWFE | statsmodels | bacondecomp | bacondecomp | `references/method-patterns.md` §4 |
| Regression Discontinuity | statsmodels polynomial | rdrobust | rdplot/rdrobust | `references/method-patterns.md` §5 |
| Instrumental Variables | linearmodels IV2SLS | AER/ivreg | ivregress 2sls | `references/method-patterns.md` §6 |
| Synthetic Control | rpy2 → R Synth | Synth + SCtools | synth | `references/method-patterns.md` §7 |
| Matching / PSM / IPW | manual logit + weights | MatchIt + Zelig | teffects/cem | `references/method-patterns.md` §8 |
| DAGs / Collider Bias | dagitty (conceptual) | dagitty/ggdag | — | `references/method-patterns.md` §9 |
| Randomization Inference | permutation loop | ri2 | ritest | `references/method-patterns.md` §10 |

---

## Core Workflow

### Implement a Causal Method

1. Identify the method from the table above
2. Load the appropriate template from `references/method-patterns.md`
3. Adapt variable names, fixed effects, and clustering to the user's data
4. Add robustness checks (parallel trends for DiD, McCrary for RDD, first-stage F for IV)

### Choose the Right Language

| Scenario | Recommendation |
|----------|---------------|
| ML pipeline integration | Python (statsmodels + linearmodels) |
| Synthetic Control | R (Synth package) or Stata (synth) — Python lacks mature implementation |
| Bacon decomposition | R (bacondecomp) or Stata — no Python equivalent |
| Publication-ready tables | Stata (outreg2/esttab) or R (stargazer/modelsummary) |
| Coarsened Exact Matching | Stata (cem) or R (MatchIt) — no Python equivalent |
| Quick prototyping | Python with statsmodels |

### Cross-Language Equivalents

| Task | Python | R | Stata |
|------|--------|---|-------|
| OLS with robust SE | `smf.ols().fit(cov_type='HC1')` | `lm_robust()` | `reg y x, robust` |
| Cluster SE | `fit(cov_type='cluster', cov_kwds={'groups': g})` | `felm(y ~ x | 0 | 0 | cluster)` | `reg y x, cluster(id)` |
| Two-way FE | `C(id) + C(time)` in formula | `felm(y ~ x | id + time)` | `reghdfe y x, absorb(id time)` |
| IV / 2SLS | `IV2SLS.from_formula('y ~ 1 + exog + [endog ~ inst]')` | `ivreg(y ~ exog | inst)` | `ivregress 2sls y exog (endog = inst)` |
| DiD | `C(treat)*C(post)` | `treat:post` in formula | `did_multiplegt` or interaction |

---

## Key Python Patterns

### DiD with Cluster-Robust SE

```python
import statsmodels.formula.api as smf

model = smf.ols('y ~ C(treated)*C(post) + controls', data=df)
results = model.fit(cov_type='cluster', cov_kwds={'groups': df['firm_id']})
```

### Event Study (Lead/Lag)

```python
# Create relative time dummies
for k in range(-4, 5):
    col = f'rel_{k}' if k >= 0 else f'rel_m{abs(k)}'
    df[col] = (df['relative_time'] == k).astype(int)

# Drop t=-1 as reference
formula = 'y ~ ' + ' + '.join([c for c in rel_cols if c != 'rel_m1']) + ' + C(id) + C(year)'
```

### IV / 2SLS

```python
from linearmodels.iv import IV2SLS

model = IV2SLS.from_formula('y ~ 1 + exog + [endog ~ instrument]', data=df)
results = model.fit(cov_type='clustered', clusters=df['cluster_var'])
```

---

## Robustness Check Patterns

| Method | Required Checks |
|--------|----------------|
| DiD | Parallel trends (event study plot), placebo treatment dates |
| RDD | McCrary density test, bandwidth robustness (half/double IK optimal), polynomial robustness |
| IV | First-stage F > 10, exclusion restriction argument, over-identification test |
| Synthetic Control | Pre-treatment RMSPE, placebo distribution, leave-one-out |
| Matching | Covariate balance table, caliper sensitivity |

---

## Common Pitfalls

1. **TWFE with staggered treatment** — standard two-way FE is biased when treatment timing varies. Use Bacon decomposition or Sun & Abraham / Callaway & Sant'Anna estimators.
2. **Synthetic Control with many treated units** — the Synth package handles one treated unit. For multiple, use augmented synthetic control or stacked approach.
3. **RDD without McCrary test** — always test for manipulation at the cutoff before estimating.
4. **IV weak instruments** — report first-stage F-statistic. Below 10 indicates weak instrument bias.
5. **Python Synth gap** — no mature Python Synth package exists. Use `rpy2` to call R's `Synth` from Python.

---

## Additional Resources

### Reference Files

- **`references/method-patterns.md`** — Detailed code templates for all 10 methods with full examples
- **`references/r-stata-comparison.md`** — Cross-language package comparison and method coverage gaps

### Prompt Files

- **`prompts/01-implement-method.md`** — Copy-paste prompt for implementing any causal method
- **`prompts/02-robustness-checks.md`** — Copy-paste prompt for generating robustness check code
