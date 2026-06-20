# Placebo-in-time Analysis

## Overview

The `PlaceboInTime` check (in `causalpy.checks.placebo_in_time`) implements a placebo-in-time sensitivity analysis with a hierarchical Bayesian null model. It shifts the treatment time backward to create placebo folds, extracts posterior cumulative impacts, then fits a hierarchical model to characterise the "status quo" distribution. The actual intervention effect is compared against this learned null. Optionally, Bayesian assurance (operating characteristics) can be computed.

## When to Use

Use `PlaceboInTime` when you want to:

1. **Validate causal claims**: Build a principled model of what "no effect" looks like, then check if your real effect falls outside it
2. **Check model specification**: Verify that your model isn't picking up pre-existing trends
3. **Assess robustness**: Quantify how far the actual effect is from the null distribution (not just pass/fail)
4. **Estimate study power**: Compute Bayesian assurance — the probability of detecting a real effect given your beliefs about effect size

## Core API

`PlaceboInTime` is part of the core library at `causalpy.checks.PlaceboInTime`.

### Constructor

```python
cp.checks.PlaceboInTime(
    n_folds=3,                       # number of placebo folds
    experiment_factory=None,         # (data, treatment_time) -> experiment
    sample_kwargs=None,              # MCMC settings for hierarchical model
    threshold=0.95,                  # P(outside null) cutoff for passed
    prior_scale=1.0,                 # prior width multiplier
    expected_effect_prior=None,      # distribution with .rvs() or numpy array
    rope_half_width=None,            # ROPE half-width (required with prior)
    n_design_replications=None,      # simulation reps for assurance
    random_seed=None,                # RNG seed for assurance
)
```

### Pipeline Usage

```python
import pandas as pd
import causalpy as cp

result = cp.Pipeline(
    data=df,
    steps=[
        cp.EstimateEffect(
            method=cp.InterruptedTimeSeries,
            treatment_time=pd.Timestamp("2020-03-01"),
            formula="y ~ 1 + t",
            model=cp.pymc_models.LinearRegression(
                sample_kwargs={"draws": 1000, "random_seed": 42}
            ),
        ),
        cp.SensitivityAnalysis(
            checks=[cp.checks.PlaceboInTime(n_folds=4)],
        ),
    ],
).run()

placebo_result = result.sensitivity_results[0]
print(placebo_result.text)
```

### Standalone Usage

```python
result = cp.InterruptedTimeSeries(
    data=df,
    treatment_time=pd.Timestamp("2020-03-01"),
    formula="y ~ 1 + t",
    model=cp.pymc_models.LinearRegression(
        sample_kwargs={"draws": 1000, "random_seed": 42}
    ),
)

def my_factory(data, treatment_time):
    return cp.InterruptedTimeSeries(
        data=data,
        treatment_time=treatment_time,
        formula="y ~ 1 + t",
        model=cp.pymc_models.LinearRegression(
            sample_kwargs={"draws": 1000, "random_seed": 42}
        ),
    )

check = cp.checks.PlaceboInTime(n_folds=4, experiment_factory=my_factory)
placebo_result = check.run(experiment=result)
```

## Result Structure

The `CheckResult` metadata contains:

| Key | Type | Description |
|-----|------|-------------|
| `fold_results` | `list[PlaceboFoldResult]` | Per-fold results with posterior samples |
| `status_quo_idata` | `InferenceData` | Hierarchical model trace |
| `null_samples` | `np.ndarray` | Draws from theta_new (the null distribution) |
| `actual_cumulative_mean` | `float` | Actual intervention cumulative effect |
| `p_effect_outside_null` | `float` | P(actual > null) |
| `assurance_result` | `AssuranceResult` | (only if prior provided) Operating characteristics |
| `assurance` | `float` | (only if prior provided) True positive rate |

## Visualization: Null vs Actual

```python
import matplotlib.pyplot as plt
import numpy as np

placebo_result = result.sensitivity_results[0]
null_samples = placebo_result.metadata["null_samples"]
actual = placebo_result.metadata["actual_cumulative_mean"]

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(null_samples, bins=40, density=True, alpha=0.6, label="Status-quo null")
ax.axvline(actual, color="red", ls="--", lw=2, label=f"Actual = {actual:.1f}")
ax.legend()
plt.show()
```

## Visualization: Per-Fold Posteriors

```python
import xarray as xr

fold_results = placebo_result.metadata["fold_results"]
fig, ax = plt.subplots(figsize=(8, 6))

for fr in fold_results:
    samples = fr.cumulative_impact_samples.values
    ax.hist(samples, bins=30, alpha=0.5, density=True,
            label=f"Fold {fr.fold} (mean={fr.fold_mean:.1f})")

ax.hist(null_samples, bins=40, density=True, alpha=0.6, label="θ_new ~ N(μ, τ)")
ax.legend()
plt.show()
```

## Advanced: Bayesian Assurance

Provide an expected-effect prior and ROPE half-width to compute operating characteristics:

```python
import preliz as pz

check = cp.checks.PlaceboInTime(
    n_folds=4,
    experiment_factory=my_factory,
    expected_effect_prior=pz.maxent(pz.Normal(), lower=60, upper=120, mass=0.95),
    rope_half_width=50.0,
    random_seed=42,
)
placebo_result = check.run(experiment=result)

ar = placebo_result.metadata["assurance_result"]
print(f"Assurance (TP rate): {ar.true_positive_rate:.1%}")
print(f"False Positive rate: {ar.false_positive_rate:.1%}")
print(f"True Negative rate:  {ar.true_negative_rate:.1%}")
```

The assurance result contains:

- **true_positive_rate** (assurance): P(detect real effect | real effect exists)
- **false_positive_rate**: P(detect effect | no real effect)
- **true_negative_rate**: P(correctly find null | no real effect)
- **false_negative_rate**: P(miss real effect | real effect exists)
- **null/alt_indeterminate_rate**: P(indeterminate decision)
- **null_decisions / alt_decisions**: Raw decision arrays for custom analysis

### Visualizing Operating Characteristics

```python
import pandas as pd

ar = placebo_result.metadata["assurance_result"]
outcomes = ["positive", "null", "indeterminate"]

null_props = [ar.false_positive_rate, ar.true_negative_rate, ar.null_indeterminate_rate]
alt_props = [ar.true_positive_rate, ar.false_negative_rate, ar.alt_indeterminate_rate]

fig, ax = plt.subplots(figsize=(8, 4))
y_pos = np.arange(len(outcomes))
height = 0.35

ax.barh(y_pos + height / 2, null_props, height, label="Null true", alpha=0.8)
ax.barh(y_pos - height / 2, alt_props, height, label="Alt true", alpha=0.8)
ax.set_yticks(y_pos)
ax.set_yticklabels([o.capitalize() for o in outcomes])
ax.set_xlabel("Probability")
ax.set_title("Bayesian Operating Characteristics")
ax.legend()
plt.show()
```

### ROPE Decision Rule

The `bayesian_rope_decision` static method is available for custom use:

```python
decision = cp.checks.PlaceboInTime.bayesian_rope_decision(
    posterior_samples=my_posterior,
    rope_half_width=50.0,
    threshold=0.95,
)
# Returns: "positive", "null", or "indeterminate"
```
