# Piecewise Interrupted Time Series

Use `cp.PiecewiseITS` when intervention times are known and the model should estimate explicit level and/or slope changes with `step()` and `ramp()` terms.

## Constructor

```python
cp.PiecewiseITS(
    data,
    formula,
    model=None,
    **kwargs
)
```

## Required Data

- `data`: DataFrame with an outcome and a time variable.
- `formula`: must include at least one `step(time, threshold)` or `ramp(time, threshold)` term.
- `step()`: estimates level changes.
- `ramp()`: estimates slope changes after a threshold.

## Model Guidance

The default backend is `cp.pymc_models.LinearRegression`, and sklearn regressors are supported. Since the model fits the full series, priors on step and ramp coefficients should reflect plausible level and slope changes in the outcome's units.

## Example

```python
import numpy as np
import pandas as pd
import causalpy as cp

rng = np.random.default_rng(42)
t = np.arange(100)
df = pd.DataFrame({"t": t, "y": 1 + 0.05 * t + 2 * (t >= 50) + 0.03 * np.maximum(0, t - 50) + rng.normal(0, 0.2, len(t))})

result = cp.PiecewiseITS(
    data=df,
    formula="y ~ 1 + t + step(t, 50) + ramp(t, 50)",
    model=cp.pymc_models.LinearRegression(sample_kwargs={"target_accept": 0.95}),
)

result.summary()
summary = result.effect_summary(direction="increase")
result.plot()
```

## Interpretation Checks

- Use this when intervention timing is known in advance, not for discovering changepoints.
- Keep formulas interpretable: level-only, slope-only, or level-plus-slope changes.
- Prefer `InterruptedTimeSeries` if the estimand is a post-period forecast gap from a pre-period model.
