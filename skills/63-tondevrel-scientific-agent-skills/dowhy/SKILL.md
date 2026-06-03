---
name: dowhy
description: Causal inference framework for answering "does X cause Y?" beyond correlation. DoWhy (Microsoft Research) provides the identify-estimate-refute loop: define a causal graph (DAG), identify the causal effect using backdoor/frontdoor/instrumental variable criteria, estimate treatment effects with multiple estimators, and validate results with automated refutation tests. Use when: distinguishing causation from correlation, estimating treatment effects (ATE, ATT, CATE), designing and analyzing A/B tests with confounders, using instrumental variables, performing counterfactual reasoning ("what would have happened if..."), validating causal claims with sensitivity analysis, working with observational data where randomization is impossible, or any analysis where the question is "what is the CAUSAL effect of X on Y" rather than just "how do X and Y relate?"
version: 0.11.0
license: MIT
---

# DoWhy — Causal Inference

DoWhy answers the question every analyst actually wants answered: **"Does X cause Y, or is it just correlated?"** Correlation is everywhere. Causation requires structure — a causal graph that encodes which variables influence which. DoWhy's workflow is three steps: **Identify** (is the effect estimable from this graph?) → **Estimate** (compute the effect) → **Refute** (is this estimate robust?).

## Core Mental Model

```
CORRELATION:  X and Y move together. Could be:
                X → Y          (X causes Y)
                Y → X          (Y causes X)
                X ← C → Y     (C confounds both — spurious!)

CAUSATION:    We need to know WHY they move together.
              A causal graph (DAG) encodes our assumptions.
              Then math tells us: "Given this graph,
              CAN we estimate the causal effect from data?"
              → If yes: which variables to control for?
              → If no: what additional data do we need?
```

## When to Use

- "Does this ad campaign actually increase sales, or do people who see ads already buy more?"
- "Does smoking cause cancer?" (observational data, can't randomize)
- "What would revenue have been if we hadn't changed the pricing?" (counterfactual)
- Any analysis where confounders exist and you have a theory about the causal structure.

**When NOT to use:** Pure prediction (use sklearn). Randomized controlled trials with no confounders (simple A/B test suffices). When you have no theory about the causal structure — you need at least a hypothesis about the DAG.

## Reference Documentation

**DoWhy docs**: https://dowhy.readthedocs.io/en/latest/  
**GitHub**: https://github.com/py-why/dowhy  
**Causal graph tutorials**: https://dowhy.readthedocs.io/en/latest/tutorials.html  
**Search patterns**: `CausalModel`, `identify_effect`, `estimate_effect`, `refute_estimate`

## Core Principles

### The Causal Graph (DAG)
A Directed Acyclic Graph where arrows mean "causes". `A → B` means A is a cause of B. This is your **assumptions** about the world — not learned from data. You draw it based on domain knowledge. The graph is what makes causal inference possible.

### The Identify-Estimate-Refute Loop
1. **Identify**: Given the DAG, is the causal effect of treatment on outcome *estimable* from observational data? Which variables must be controlled? (Backdoor criterion, frontdoor criterion, instrumental variables.)
2. **Estimate**: Compute the effect using the identified strategy and a statistical method.
3. **Refute**: Test robustness — would the estimate survive if our assumptions were wrong?

### Confounders Are the Enemy
A confounder C is a common cause of both treatment and outcome: `T ← C → Y`. It creates spurious correlation. The entire point of causal inference is to block these backdoor paths.

### Treatment Effect Types
- **ATE** (Average Treatment Effect): Effect across the whole population.
- **ATT** (Average Treatment Effect on the Treated): Effect on those who actually received treatment.
- **CATE** (Conditional ATE): Effect varies by subgroup — heterogeneous treatment effects.

## Quick Reference

### Installation

```python
pip install dowhy networkx matplotlib pandas scikit-learn
```

### Standard Imports

```python
import dowhy
from dowhy import CausalModel
import pandas as pd
import numpy as np
```

### Basic Pattern — Full Causal Pipeline

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel

# 1. Simulate data with a known causal structure:
#    Confounder C → Treatment T, C → Outcome Y, T → Y (true effect = 2.0)
np.random.seed(42)
n = 2000
C = np.random.randn(n)                        # Confounder
T = (C + np.random.randn(n) > 0).astype(int)  # Treatment influenced by C
Y = 2.0 * T + 1.5 * C + np.random.randn(n)   # Outcome: true causal effect of T is 2.0

data = pd.DataFrame({'T': T, 'Y': Y, 'C': C})

# 2. Define the causal graph (YOUR ASSUMPTIONS)
graph = """
    digraph {
        C -> T;
        C -> Y;
        T -> Y;
    }
"""

# 3. Create causal model
model = CausalModel(
    data=data,
    treatment=['T'],
    outcome='Y',
    graph=graph
)

# 4. IDENTIFY: Can we estimate the effect? How?
identified_effect = model.identify_effect()
print(identified_effect)
# → Backdoor criterion: control for C

# 5. ESTIMATE: Compute the causal effect
estimate = model.estimate_effect(
    identified_effect,
    estimation_method='backdoor.linear_regression'
)
print(f"Estimated causal effect of T on Y: {estimate.value:.3f}")
# → Should be close to 2.0 (the true effect we simulated)

# 6. REFUTE: Is this estimate robust?
refutation = model.refute_estimate(
    estimate,
    refutation_method='refute_placebo_treatment'
)
print(refutation)
# → Placebo effect should be ~0. If it is, our estimate is credible.
```

## Critical Rules

### ✅ DO

- **Draw the graph BEFORE looking at data** — The DAG encodes your causal assumptions. It must come from domain knowledge, not from data patterns. Drawing it after seeing correlations defeats the purpose.
- **Include ALL known confounders in the graph** — Missing a confounder = biased estimate. When in doubt, include it.
- **Always run at least 2 refutation tests** — Placebo treatment + random common cause is the minimum. A single estimate without refutation is untrustworthy.
- **Use multiple estimators and compare** — If backdoor.linear_regression and backdoor.propensity_score give wildly different answers, your model assumptions may be wrong.
- **Check positivity (overlap)** — Propensity score methods fail if treatment and control groups don't overlap in covariate space. Visualize distributions.
- **Report confidence intervals, not just point estimates** — Use `estimate.get_confidence_intervals()`.
- **Interpret ATE in context** — An ATE of 0.5 means nothing without knowing the scale of Y.

### ❌ DON'T

- **Don't assume correlation = causation and skip the graph** — This is the entire reason DoWhy exists.
- **Don't use DoWhy without a causal hypothesis** — If you have no theory about why X might cause Y, you cannot draw a valid DAG. Go do qualitative research first.
- **Don't ignore refutation failures** — If placebo treatment gives a non-zero effect, your estimate is suspect. Investigate, don't just report.
- **Don't confuse "not statistically significant" with "no causal effect"** — Underpowered studies fail to detect real effects. Sample size matters.
- **Don't use backdoor adjustment when backdoor criterion isn't satisfied** — `identify_effect()` tells you which strategy is valid. Trust it.
- **Don't assume linearity** — `backdoor.linear_regression` assumes linear relationships. If the truth is nonlinear, use `backdoor.propensity_score_weighting` or `backdoor.propensity_score_matching`.

## Anti-Patterns (NEVER)

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel

# ❌ BAD: No graph — just "estimate" the effect (this is regression, not causal inference)
data = pd.DataFrame({'T': [0,1,0,1], 'Y': [1,3,2,4], 'C': [0.5,1.2,0.8,1.5]})

# This is NOT causal inference — it's just OLS regression. No confounders controlled.
# model = CausalModel(data=data, treatment=['T'], outcome='Y', graph=None)  # ← WRONG

# ✅ GOOD: Explicit graph with confounders
graph = "digraph { C -> T; C -> Y; T -> Y; }"
model = CausalModel(data=data, treatment=['T'], outcome='Y', graph=graph)

# ─────────────────────────────────────────────────────────────

# ❌ BAD: Graph drawn AFTER looking at data correlations
# "T and C correlate strongly, so let's put C → T"
# "Y and C correlate, so C → Y"
# This is data-driven graph construction — circular reasoning!
# The graph must come from DOMAIN KNOWLEDGE.

# ✅ GOOD: Graph from theory
# "We know from epidemiology that smoking history (C) affects both
#  whether someone enrolls in the program (T) and health outcomes (Y)"
# THEN encode: C -> T; C -> Y; T -> Y

# ─────────────────────────────────────────────────────────────

# ❌ BAD: Single estimator, no refutation — "done"
identified = model.identify_effect()
estimate   = model.estimate_effect(identified, estimation_method='backdoor.linear_regression')
print(f"Effect = {estimate.value}")   # And that's it. Trust this number? Why?

# ✅ GOOD: Multiple estimators + refutation battery
est_lr  = model.estimate_effect(identified, estimation_method='backdoor.linear_regression')
est_psm = model.estimate_effect(identified, estimation_method='backdoor.propensity_score_matching')
est_psw = model.estimate_effect(identified, estimation_method='backdoor.propensity_score_weighting')

print(f"Linear Regression:     {est_lr.value:.3f}")
print(f"Propensity Matching:   {est_psm.value:.3f}")
print(f"Propensity Weighting:  {est_psw.value:.3f}")
# If all three agree → high confidence. If they diverge → investigate.

# Refutation battery
model.refute_estimate(est_lr, refutation_method='refute_placebo_treatment')
model.refute_estimate(est_lr, refutation_method='refute_random_common_cause')
model.refute_estimate(est_lr, refutation_method='refute_data_subset')

# ─────────────────────────────────────────────────────────────

# ❌ BAD: Ignoring the identification result
identified = model.identify_effect()
# identified says: "Backdoor criterion NOT satisfied with these variables"
# But we proceed anyway with backdoor adjustment → biased estimate!

# ✅ GOOD: Check identification, switch strategy if needed
identified = model.identify_effect()
if identified.get_backdoor_variables():
    estimate = model.estimate_effect(identified, estimation_method='backdoor.linear_regression')
elif identified.get_instrumental_variables():
    estimate = model.estimate_effect(identified, estimation_method='iv.instrumental_variable')
else:
    print("Effect is NOT identifiable from this graph. Need more data or stronger assumptions.")
```

## Causal Graphs — Building Blocks

### DAG Syntax

```python
from dowhy import CausalModel

# Arrows: A -> B means "A causes B"
# Multiple paths: C -> T and C -> Y means C confounds T and Y

# Simple: treatment, outcome, one confounder
graph_simple = """
    digraph {
        C -> T;
        C -> Y;
        T -> Y;
    }
"""

# Multiple confounders
graph_multi = """
    digraph {
        C1 -> T;  C1 -> Y;
        C2 -> T;  C2 -> Y;
        C3 -> Y;
        T  -> Y;
    }
"""
# C1, C2 confound. C3 affects only Y (not a confounder, but still important).

# Mediator: T → M → Y (T affects Y *through* M)
graph_mediator = """
    digraph {
        T -> M;
        M -> Y;
        T -> Y;
        C -> T;  C -> Y;
    }
"""
# Total effect of T on Y = direct (T→Y) + indirect (T→M→Y)

# Collider: T → S ← Y (S is caused by BOTH T and Y)
# NEVER condition on a collider — it opens a spurious path!
graph_collider = """
    digraph {
        T -> S;
        Y -> S;
        T -> Y;
    }
"""

# Instrumental Variable: Z → T → Y, Z does NOT directly affect Y
graph_iv = """
    digraph {
        Z -> T;
        T -> Y;
        C -> T;  C -> Y;
    }
"""
# Z is valid instrument if: (1) Z affects T, (2) Z affects Y ONLY through T
```

### Graph Visualization

```python
from dowhy import CausalModel
import pandas as pd
import numpy as np

data = pd.DataFrame({'T': [0,1]*100, 'Y': np.random.randn(200),
                     'C': np.random.randn(200), 'Z': np.random.randn(200)})

graph = "digraph { C -> T; C -> Y; Z -> T; T -> Y; }"

model = CausalModel(data=data, treatment=['T'], outcome='Y', graph=graph)
model.view_graph()   # Renders the DAG — opens in browser or saves .png
```

## Identification Strategies

### Backdoor Criterion — Control for Confounders

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel

np.random.seed(0)
n = 3000

# Data generating process:
# C1, C2 are confounders. True effect of T on Y = 3.0
C1 = np.random.randn(n)
C2 = np.random.randn(n)
T  = (0.5*C1 + 0.3*C2 + np.random.randn(n) > 0).astype(int)
Y  = 3.0*T + 1.0*C1 - 0.5*C2 + np.random.randn(n)

data = pd.DataFrame({'T': T, 'Y': Y, 'C1': C1, 'C2': C2})

graph = "digraph { C1 -> T; C1 -> Y; C2 -> T; C2 -> Y; T -> Y; }"

model = CausalModel(data=data, treatment=['T'], outcome='Y', graph=graph)

# Identify: DoWhy finds which variables satisfy the backdoor criterion
identified = model.identify_effect()
print("Backdoor variables:", identified.get_backdoor_variables())
# → ['C1', 'C2'] — control for both confounders

# Estimate with backdoor adjustment
estimate = model.estimate_effect(
    identified,
    estimation_method='backdoor.linear_regression'
)
print(f"Causal effect (backdoor): {estimate.value:.3f}")   # ≈ 3.0
print(f"95% CI: {estimate.get_confidence_intervals()}")
```

### Frontdoor Criterion — When You Can't Control Confounders

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel

np.random.seed(42)
n = 5000

# Frontdoor structure: T → M → Y, with unobserved confounder U
# U affects both T and Y, but we DON'T observe U
# M (mediator) is observed and fully mediates T's effect on Y
U = np.random.randn(n)                            # UNOBSERVED
T = (U + np.random.randn(n) > 0).astype(int)      # U confounds T
M = 2.0 * T + np.random.randn(n)                  # T causes M (effect = 2.0)
Y = 1.5 * M + U + np.random.randn(n)              # M causes Y (effect = 1.5)
# True total effect of T on Y = 2.0 * 1.5 = 3.0

data = pd.DataFrame({'T': T, 'Y': Y, 'M': M})
# Note: U is NOT in data — we can't control for it directly

# Graph includes U as unobserved
graph = """
    digraph {
        U -> T;
        U -> Y;
        T -> M;
        M -> Y;
    }
"""

model = CausalModel(data=data, treatment=['T'], outcome='Y', graph=graph)
identified = model.identify_effect()
print("Frontdoor variables:", identified.get_frontdoor_variables())
# → ['M'] — the mediator satisfies frontdoor criterion

estimate = model.estimate_effect(
    identified,
    estimation_method='frontdoor.two_stage_linear_regression'
)
print(f"Causal effect (frontdoor): {estimate.value:.3f}")   # ≈ 3.0
```

### Instrumental Variables — Exogenous Variation

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel

np.random.seed(42)
n = 5000

# IV structure: Z (instrument) → T → Y
# Unobserved confounder U affects T and Y
# Z affects Y ONLY through T
Z = np.random.randn(n)                            # Instrument (e.g., random assignment)
U = np.random.randn(n)                            # Unobserved confounder
T = 1.0*Z + 0.8*U + np.random.randn(n)           # T affected by Z and U
Y = 2.5*T + 1.2*U + np.random.randn(n)           # True causal effect of T = 2.5

data = pd.DataFrame({'T': T, 'Y': Y, 'Z': Z})
# U is unobserved — not in data

graph = """
    digraph {
        Z -> T;
        U -> T;
        U -> Y;
        T -> Y;
    }
"""

model = CausalModel(data=data, treatment=['T'], outcome='Y', graph=graph)
identified = model.identify_effect()
print("Instrumental variables:", identified.get_instrumental_variables())
# → ['Z']

estimate = model.estimate_effect(
    identified,
    estimation_method='iv.instrumental_variable',
    method_params={'instrument_variables': ['Z']}
)
print(f"Causal effect (IV): {estimate.value:.3f}")   # ≈ 2.5
```

## Estimation Methods

```python
from dowhy import CausalModel

# After identification, choose an estimator based on assumptions:

# ─── LINEAR: Fast, interpretable, assumes linearity ───
est = model.estimate_effect(identified, estimation_method='backdoor.linear_regression')

# ─── PROPENSITY SCORE MATCHING: Pairs similar treated/control units ───
# Better when treatment assignment is non-random but depends on observables
est = model.estimate_effect(identified, estimation_method='backdoor.propensity_score_matching')

# ─── PROPENSITY SCORE WEIGHTING (IPW): Re-weights population ───
# Creates a "pseudo-population" where T is independent of confounders
est = model.estimate_effect(identified, estimation_method='backdoor.propensity_score_weighting')

# ─── INSTRUMENTAL VARIABLES: When backdoor is blocked ───
est = model.estimate_effect(identified, estimation_method='iv.instrumental_variable',
                            method_params={'instrument_variables': ['Z']})

# ─── COMPARISON: Run all valid estimators and compare ───
def compare_estimators(model, identified, methods):
    """Run multiple estimators, return comparison table."""
    import pandas as pd
    results = []
    for method in methods:
        try:
            est = model.estimate_effect(identified, estimation_method=method)
            ci  = est.get_confidence_intervals()
            results.append({
                'method':    method.split('.')[-1],
                'estimate':  round(est.value, 4),
                'ci_lower':  round(ci[0][0], 4) if ci else None,
                'ci_upper':  round(ci[0][1], 4) if ci else None,
            })
        except Exception as e:
            results.append({'method': method.split('.')[-1], 'error': str(e)})
    return pd.DataFrame(results)

# methods = ['backdoor.linear_regression',
#            'backdoor.propensity_score_matching',
#            'backdoor.propensity_score_weighting']
# comparison = compare_estimators(model, identified, methods)
# print(comparison)
```

## Refutation Tests — Validating Estimates

Refutation is the third pillar. Each test asks: "Would our estimate survive if assumption X were wrong?"

```python
from dowhy import CausalModel

# ─── 1. PLACEBO TREATMENT ───
# Replace treatment with random noise. Effect should vanish → ~0.
# If it doesn't → our estimate is capturing something spurious.
refute_placebo = model.refute_estimate(
    estimate,
    refutation_method='refute_placebo_treatment'
)
print(refute_placebo)
# Expected: "Refutation effect ≈ 0, original effect ≈ 3.0 → PASSED"

# ─── 2. RANDOM COMMON CAUSE ───
# Add a random variable as an unobserved confounder.
# If our estimate changes a lot → we're sensitive to hidden confounders.
refute_random = model.refute_estimate(
    estimate,
    refutation_method='refute_random_common_cause',
    method_params={
        'num_simulations': 100,        # Number of random confounders to try
        'confidence_level': 0.95
    }
)
print(refute_random)
# Expected: estimate stays stable across simulations → PASSED

# ─── 3. DATA SUBSET ───
# Estimate on random subsets of data. Should be stable (bootstrap-like).
refute_subset = model.refute_estimate(
    estimate,
    refutation_method='refute_data_subset',
    method_params={
        'fraction_removed': 0.2,       # Remove 20% of data each time
        'num_simulations': 50
    }
)
print(refute_subset)

# ─── 4. CHOOSE RANDOM TREATMENT ───
# Replace treatment with a random variable. Effect should be ~0.
refute_random_treat = model.refute_estimate(
    estimate,
    refutation_method='refute_treatment_regression_discontinuity'
)

# ─── INTERPRETATION GUIDE ───
# PASSED: Refutation effect ≈ 0 (placebo) or estimate is stable (subset/random cause)
# FAILED: Refutation effect ≠ 0 or estimate is unstable
#         → Your causal model may be wrong. Revisit the DAG.
```

## Counterfactual Reasoning

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel

# "What would Y have been if T had been different?"

np.random.seed(42)
n = 1000
C = np.random.randn(n)
T = (C + np.random.randn(n) > 0).astype(int)
Y = 2.0 * T + 1.5 * C + np.random.randn(n)

data = pd.DataFrame({'T': T, 'Y': Y, 'C': C})
graph = "digraph { C -> T; C -> Y; T -> Y; }"

model = CausalModel(data=data, treatment=['T'], outcome='Y', graph=graph)
identified = model.identify_effect()
estimate   = model.estimate_effect(identified, estimation_method='backdoor.linear_regression')

# Counterfactual: for treated units (T=1), what would Y have been if T=0?
treated_mask   = data['T'] == 1
Y_factual      = data.loc[treated_mask, 'Y']
# Counterfactual Y = Y_factual - (causal_effect × change_in_T)
Y_counterfactual = Y_factual - estimate.value * 1   # T goes from 1 → 0

# Individual treatment effect for each treated unit
individual_effect = Y_factual.values - Y_counterfactual.values

print(f"Average Treatment Effect on Treated (ATT): {individual_effect.mean():.3f}")
print(f"ATT std across treated units:               {individual_effect.std():.3f}")
print(f"Min / Max individual effect:                {individual_effect.min():.3f} / {individual_effect.max():.3f}")

# Scenario: "Revenue if ALL users had been treated"
Y_all_treated = data['Y'] + estimate.value * (1 - data['T'])  # Treat the untreated
revenue_lift  = Y_all_treated.mean() - data['Y'].mean()
print(f"\nEstimated revenue lift from universal treatment: {revenue_lift:.3f}")
```

## Heterogeneous Treatment Effects (CATE)

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel
from sklearn.tree import DecisionTreeRegressor

np.random.seed(42)
n = 3000

# Treatment effect VARIES by subgroup:
# Effect = 5.0 for age > 40, effect = 1.0 for age <= 40
age = np.random.uniform(18, 70, n)
C   = np.random.randn(n)
T   = (C + np.random.randn(n) > 0).astype(int)
true_effect = np.where(age > 40, 5.0, 1.0)
Y   = true_effect * T + 1.5 * C + np.random.randn(n)

data = pd.DataFrame({'T': T, 'Y': Y, 'C': C, 'age': age})
graph = "digraph { C -> T; C -> Y; T -> Y; age -> Y; }"

model = CausalModel(data=data, treatment=['T'], outcome='Y', graph=graph)
identified = model.identify_effect()

# Estimate CATE using a meta-learner approach:
# 1. Estimate Y under T=1 for everyone
# 2. Estimate Y under T=0 for everyone
# 3. CATE = E[Y|T=1, X] - E[Y|T=0, X]

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_predict

features = ['C', 'age']
X = data[features].values

# Outcome model for treated
treated_mask = data['T'] == 1
model_1 = GradientBoostingRegressor(random_state=42)
model_0 = GradientBoostingRegressor(random_state=42)

model_1.fit(X[treated_mask],  data.loc[treated_mask, 'Y'])
model_0.fit(X[~treated_mask], data.loc[~treated_mask, 'Y'])

# CATE for each unit
Y_hat_1 = model_1.predict(X)
Y_hat_0 = model_0.predict(X)
CATE    = Y_hat_1 - Y_hat_0

data['CATE'] = CATE

# Analyze: who benefits most?
print("CATE by age group:")
print(data.groupby(pd.cut(data['age'], bins=[18, 30, 40, 50, 60, 70]))['CATE'].mean())
# Should show jump at age 40 (effect goes from 1.0 to 5.0)

# Target the high-CATE subgroup
top_quartile = data.nlargest(int(0.25 * n), 'CATE')
print(f"\nTop 25% CATE: mean effect = {top_quartile['CATE'].mean():.2f}")
print(f"Bottom 75% CATE: mean effect = {data.nsmallest(int(0.75*n), 'CATE')['CATE'].mean():.2f}")
```

## Practical Workflows

### 1. Full Causal Analysis — Marketing Attribution

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel

def causal_marketing_analysis(data: pd.DataFrame,
                              treatment: str,
                              outcome: str,
                              confounders: list[str],
                              graph: str) -> dict:
    """
    Full causal pipeline for marketing:
    identify → estimate (3 methods) → refute (3 tests) → report.
    """
    model = CausalModel(data=data, treatment=[treatment], outcome=outcome, graph=graph)

    # IDENTIFY
    identified = model.identify_effect()
    print(f"Backdoor variables: {identified.get_backdoor_variables()}")

    # ESTIMATE — three methods
    methods = [
        'backdoor.linear_regression',
        'backdoor.propensity_score_matching',
        'backdoor.propensity_score_weighting'
    ]
    estimates = {}
    for method in methods:
        est = model.estimate_effect(identified, estimation_method=method)
        name = method.split('.')[-1]
        ci = est.get_confidence_intervals()
        estimates[name] = {
            'value': round(est.value, 4),
            'ci':    (round(ci[0][0], 4), round(ci[0][1], 4)) if ci else None
        }
        print(f"  {name:35s} effect = {est.value:.4f}")

    # Use linear regression estimate as primary for refutation
    primary_est = model.estimate_effect(identified, estimation_method='backdoor.linear_regression')

    # REFUTE — three tests
    print("\nRefutation tests:")
    refutations = {}

    ref_placebo = model.refute_estimate(primary_est, refutation_method='refute_placebo_treatment')
    refutations['placebo'] = ref_placebo
    print(f"  Placebo treatment: {ref_placebo}")

    ref_random  = model.refute_estimate(primary_est, refutation_method='refute_random_common_cause',
                                        method_params={'num_simulations': 50})
    refutations['random_cause'] = ref_random
    print(f"  Random common cause: {ref_random}")

    ref_subset  = model.refute_estimate(primary_est, refutation_method='refute_data_subset',
                                        method_params={'fraction_removed': 0.2, 'num_simulations': 30})
    refutations['data_subset'] = ref_subset
    print(f"  Data subset: {ref_subset}")

    # REPORT
    effect = primary_est.value
    ci     = primary_est.get_confidence_intervals()

    print(f"\n{'='*60}")
    print(f"  CAUSAL EFFECT OF {treatment} ON {outcome}")
    print(f"{'='*60}")
    print(f"  Estimate:  {effect:.4f}")
    if ci: print(f"  95% CI:    [{ci[0][0]:.4f}, {ci[0][1]:.4f}]")
    print(f"  Direction: {'Positive ↑' if effect > 0 else 'Negative ↓'}")
    agreement = len(set(round(v['value'], 1) for v in estimates.values())) == 1
    print(f"  Estimator agreement: {'✅ All methods agree' if agreement else '⚠️  Methods disagree — investigate'}")

    return {
        'effect':       effect,
        'ci':           ci,
        'estimates':    estimates,
        'refutations':  refutations,
        'model':        model
    }

# ─── Usage ───
# np.random.seed(42)
# n = 2000
# age = np.random.uniform(18, 65, n)
# income = np.random.randn(n) * 30000 + 50000
# T = ((age/65 + income/100000 + np.random.randn(n)) > 1.5).astype(int)
# Y = 15.0 * T + 0.0002 * income + 0.1 * age + np.random.randn(n) * 5
# data = pd.DataFrame({'campaign': T, 'revenue': Y, 'age': age, 'income': income})
# graph = "digraph { age -> campaign; income -> campaign; age -> revenue; income -> revenue; campaign -> revenue; }"
# result = causal_marketing_analysis(data, 'campaign', 'revenue', ['age', 'income'], graph)
```

### 2. A/B Test with Confounders

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel

def causal_ab_test(data: pd.DataFrame,
                   variant_col: str,         # 'A' or 'B'
                   outcome_col: str,
                   confounders: list[str],
                   graph: str) -> dict:
    """
    A/B test where assignment was NOT perfectly random —
    e.g., users self-selected, or assignment leaked through confounders.
    Standard A/B test would be biased. Causal adjustment fixes it.
    """
    # Encode variant as binary treatment
    data = data.copy()
    data['T'] = (data[variant_col] == 'B').astype(int)

    model = CausalModel(data=data, treatment=['T'], outcome=outcome_col, graph=graph)
    identified = model.identify_effect()

    # Estimate: causal vs naive
    naive_diff = data.groupby('T')[outcome_col].mean()
    naive_effect = naive_diff[1] - naive_diff[0]

    causal_est = model.estimate_effect(identified, estimation_method='backdoor.propensity_score_weighting')

    print(f"Naive A/B difference (biased):   {naive_effect:.4f}")
    print(f"Causal effect (adjusted):        {causal_est.value:.4f}")
    print(f"Bias from confounding:           {naive_effect - causal_est.value:.4f}")

    # Refute
    model.refute_estimate(causal_est, refutation_method='refute_placebo_treatment')

    return {
        'naive_effect':  naive_effect,
        'causal_effect': causal_est.value,
        'bias':          naive_effect - causal_est.value
    }

# ─── Usage ───
# result = causal_ab_test(df, variant_col='group', outcome_col='conversion',
#                         confounders=['age', 'tenure'],
#                         graph="digraph { age -> T; tenure -> T; age -> conversion; tenure -> conversion; T -> conversion; }")
```

### 3. Instrumental Variable — Natural Experiment

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel

def iv_analysis(data: pd.DataFrame,
                treatment: str,
                outcome: str,
                instrument: str,
                graph: str) -> dict:
    """
    IV analysis for when confounders are unobserved.
    Classic example: "Does education cause higher income?"
    Instrument: distance to nearest university (affects education, not income directly)
    """
    model = CausalModel(data=data, treatment=[treatment], outcome=outcome, graph=graph)
    identified = model.identify_effect()

    iv_vars = identified.get_instrumental_variables()
    print(f"Identified instruments: {iv_vars}")

    if not iv_vars:
        print("ERROR: No valid instrument found. Check the graph.")
        return None

    # IV estimate
    estimate = model.estimate_effect(
        identified,
        estimation_method='iv.instrumental_variable',
        method_params={'instrument_variables': iv_vars}
    )

    print(f"\nIV Causal Effect of {treatment} on {outcome}: {estimate.value:.4f}")

    # Validate instrument strength: first stage F-test
    # Weak instrument (F < 10) → IV estimates are unreliable
    from sklearn.linear_model import LinearRegression
    import numpy as np

    first_stage = LinearRegression()
    first_stage.fit(data[[instrument]], data[treatment])
    r2 = first_stage.score(data[[instrument]], data[treatment])
    print(f"First stage R²: {r2:.4f} ({'Strong' if r2 > 0.1 else 'WEAK — estimates unreliable'})")

    # Refute
    model.refute_estimate(estimate, refutation_method='refute_placebo_treatment')

    return {'effect': estimate.value, 'first_stage_r2': r2}

# ─── Usage ───
# np.random.seed(42)
# n = 2000
# Z = np.random.uniform(0, 100, n)          # Distance to university (km)
# U = np.random.randn(n)                     # Unobserved ability
# education = 0.03 * Z + 0.5 * U + np.random.randn(n)  # Years of education
# income    = 5000 * education + 10000 * U + np.random.randn(n) * 8000
# df = pd.DataFrame({'education': education, 'income': income, 'distance': Z})
# graph = "digraph { distance -> education; U -> education; U -> income; education -> income; }"
# result = iv_analysis(df, 'education', 'income', 'distance', graph)
```

### 4. Sensitivity Analysis — How Robust Is the Estimate?

```python
import numpy as np
import pandas as pd
from dowhy import CausalModel

def sensitivity_analysis(data: pd.DataFrame,
                         treatment: str,
                         outcome: str,
                         graph: str,
                         n_simulations: int = 100) -> pd.DataFrame:
    """
    Systematic sensitivity analysis:
    How much would a hidden confounder need to bias our estimate to zero?
    """
    model = CausalModel(data=data, treatment=[treatment], outcome=outcome, graph=graph)
    identified = model.identify_effect()
    estimate   = model.estimate_effect(identified, estimation_method='backdoor.linear_regression')

    original_effect = estimate.value
    print(f"Original causal estimate: {original_effect:.4f}")

    # 1. Random common cause — varying strength
    print("\n1. Sensitivity to unobserved confounders:")
    ref = model.refute_estimate(
        estimate,
        refutation_method='refute_random_common_cause',
        method_params={
            'num_simulations': n_simulations,
            'confidence_level': 0.95
        }
    )
    print(f"   {ref}")

    # 2. Data subset stability
    print("\n2. Stability across data subsets:")
    ref_sub = model.refute_estimate(
        estimate,
        refutation_method='refute_data_subset',
        method_params={
            'fraction_removed': 0.3,
            'num_simulations': 50
        }
    )
    print(f"   {ref_sub}")

    # 3. Placebo battery — test with multiple random treatments
    print("\n3. Placebo treatment test:")
    ref_placebo = model.refute_estimate(
        estimate,
        refutation_method='refute_placebo_treatment',
        method_params={'num_simulations': 50}
    )
    print(f"   {ref_placebo}")

    # Summary
    print(f"\n{'='*50}")
    print(f"  SENSITIVITY SUMMARY")
    print(f"  Original effect: {original_effect:.4f}")
    print(f"  If all refutations PASS → estimate is robust")
    print(f"  If any FAIL → revisit causal assumptions")

    return {'original_effect': original_effect, 'model': model}

# ─── Usage ───
# result = sensitivity_analysis(data, 'T', 'Y', graph)
```

## Common Pitfalls and Solutions

### Collider Bias — Conditioning Opens Bad Paths

```python
# The most dangerous mistake in causal inference.

# DAG: T → S ← Y  (S is a collider)
# T and Y are INDEPENDENT — no causal relationship.
# But if you condition on S (e.g., "among people who applied"),
# T and Y become CORRELATED. This is spurious!

# Real example: "Among admitted students, SAT scores and GPA are negatively
# correlated" — but in the general population they're positively correlated.
# Conditioning on admission (collider) creates bias.

# ❌ BAD: Include collider as confounder
graph_bad = "digraph { T -> S; Y -> S; T -> Y; }"
# If you add S to backdoor adjustment → you OPEN the path T ← S → Y

# ✅ GOOD: Never condition on a collider. Identify it in the graph.
# DoWhy's identify_effect() handles this automatically IF your graph is correct.
# The graph is the key — get it right.
```

### Graph Specification Errors

```python
# ❌ COMMON ERROR: Bidirectional arrow (not valid in DAG)
graph_bad = "digraph { T <-> Y; }"   # Syntax error or wrong meaning

# ✅ GOOD: Model bidirectional influence as shared unobserved cause
graph_good = "digraph { U -> T; U -> Y; T -> Y; }"
# U is the unobserved common cause. This is how you encode "T and Y influence each other"
# in a DAG framework.

# ❌ COMMON ERROR: Missing confounder
# You know age affects both treatment enrollment and outcome,
# but you forget to include it.
graph_bad  = "digraph { T -> Y; }"                    # Biased — age confounds!
graph_good = "digraph { age -> T; age -> Y; T -> Y; }"  # Correct
```

### Effect Not Identifiable

```python
from dowhy import CausalModel

# When DoWhy says "effect not identifiable" — it means:
# Given THIS graph, there is NO statistical method that can recover
# the true causal effect from observational data.

# This happens when all backdoor paths are blocked by unobserved variables
# AND no frontdoor or IV path exists.

graph = "digraph { U -> T; U -> Y; T -> Y; }"
# U is unobserved, no instrument, no mediator
# → Effect is NOT identifiable

# Solutions:
# 1. Find an instrument (natural experiment, randomization)
# 2. Find a mediator (frontdoor)
# 3. Make stronger assumptions (e.g., assume linearity → bounds)
# 4. Collect data on U (measure the confounder)
# 5. Run an RCT (gold standard — randomization breaks confounding)
```

---

DoWhy's power is the **structure**: you don't just throw data at a model and hope. You articulate your causal assumptions as a graph, let the math tell you whether the effect is identifiable, estimate it with the right method, and then systematically test whether your answer would survive if your assumptions were wrong. The identify → estimate → refute loop is the closest thing science has to a rigorous protocol for extracting causation from observational data.