# Regression Kink

Use `cp.RegressionKink` when treatment intensity or incentives change slope at a known kink point in a running variable.

## Constructor

```python
cp.RegressionKink(
    data,
    formula,
    kink_point,
    model=None,
    running_variable_name="x",
    epsilon=0.001,
    bandwidth=np.inf,
    **kwargs
)
```

## Required Data

- `data`: DataFrame with outcome, running variable, and a dummy-coded `treated` column indicating observations at or above the kink point.
- `kink_point`: threshold where the slope changes.
- `running_variable_name`: running variable column, defaulting to `"x"`.
- `formula`: must include `treated` and terms that encode the slope change, such as `I((x - kink_point) * treated)`.
- `bandwidth`: optional local window around the kink.

## Model Guidance

Only Bayesian PyMC models are supported. The default is `cp.pymc_models.LinearRegression`. Scale the running variable around the kink and use priors that make the implied slope changes plausible in the outcome units.

## Example

```python
import numpy as np
import pandas as pd
import causalpy as cp

kink_point = 0.0
rng = np.random.default_rng(42)
x = np.linspace(-1, 1, 100)
df = pd.DataFrame({"x": x})
df["treated"] = (df["x"] >= kink_point).astype(int)
df["y"] = 1 + 0.5 * df["x"] + 2 * (df["x"] - kink_point) * df["treated"] + rng.normal(0, 0.1, len(df))

result = cp.RegressionKink(
    data=df,
    formula=f"y ~ 1 + x + I((x - {kink_point}) * treated)",
    kink_point=kink_point,
    running_variable_name="x",
    bandwidth=1.0,
    model=cp.pymc_models.LinearRegression(sample_kwargs={"target_accept": 0.95}),
)

result.summary()
summary = result.effect_summary(direction="increase")
result.plot()
```

## Interpretation Checks

- Use `cp.checks.BandwidthSensitivity` through `cp.SensitivityAnalysis` to assess whether the estimate depends on the local window.
- Use `RegressionDiscontinuity` instead if the outcome or treatment probability jumps at the cutoff.
- Check that the running variable is not manipulated near the kink.
