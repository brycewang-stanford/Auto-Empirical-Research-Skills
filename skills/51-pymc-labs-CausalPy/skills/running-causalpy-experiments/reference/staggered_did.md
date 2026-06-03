# Staggered Difference-in-Differences

Use `cp.StaggeredDifferenceInDifferences` when units adopt treatment at different times and treatment is absorbing.

## Constructor

```python
cp.StaggeredDifferenceInDifferences(
    data,
    formula,
    unit_variable_name,
    time_variable_name,
    treated_variable_name="treated",
    treatment_time_variable_name=None,
    never_treated_value=np.inf,
    model=None,
    event_window=None,
    reference_event_time=-1,
    **kwargs
)
```

## Required Data

- `data`: long unit-time panel.
- `unit_variable_name`: unit identifier.
- `time_variable_name`: time identifier.
- `treated_variable_name`: binary treatment status.
- `treatment_time_variable_name`: optional unit-level first treatment time; if omitted, CausalPy infers timing from the treatment status.
- `formula`: commonly `"y ~ 1 + C(unit) + C(time)"` for unit and time fixed effects.

## Model Guidance

The default backend is `cp.pymc_models.LinearRegression`, and sklearn regressors are supported. The model fits untreated observations and imputes untreated potential outcomes for treated observations. Use scale-aware priors for fixed-effect and covariate coefficients when the outcome is not standardized.

## Example

```python
import numpy as np
import pandas as pd
import causalpy as cp

units = [f"unit_{i}" for i in range(8)]
times = range(8)
treatment_times = {unit: 4 + (i % 2) for i, unit in enumerate(units[:6])}
rng = np.random.default_rng(42)
df = pd.DataFrame(
    [
        {
            "unit": unit,
            "time": time,
            "treatment_time": treatment_times.get(unit, np.inf),
            "treated": int(time >= treatment_times.get(unit, np.inf)),
            "y": rng.normal() + 0.8 * int(time >= treatment_times.get(unit, np.inf)),
        }
        for unit in units
        for time in times
    ]
)

result = cp.StaggeredDifferenceInDifferences(
    data=df,
    formula="y ~ 1 + C(unit) + C(time)",
    unit_variable_name="unit",
    time_variable_name="time",
    treated_variable_name="treated",
    treatment_time_variable_name="treatment_time",
    model=cp.pymc_models.LinearRegression(sample_kwargs={"target_accept": 0.95}),
)

result.summary()
summary = result.effect_summary(direction="increase")
result.plot()
```

## Interpretation Checks

- Treatment must be absorbing: once treated, a unit stays treated.
- Check no-anticipation and parallel-trends assumptions using event-time output.
- Use `cp.checks.PreTreatmentPlaceboCheck()` to inspect pre-treatment event-study effects.
