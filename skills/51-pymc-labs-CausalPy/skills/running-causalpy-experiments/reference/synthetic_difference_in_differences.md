# Synthetic Difference-in-Differences

Use `cp.SyntheticDifferenceInDifferences` when a synthetic-control setting should also weight pre-treatment time periods, combining donor-unit balance with time balance.

## Constructor

```python
cp.SyntheticDifferenceInDifferences(
    data,
    treatment_time,
    control_units,
    treated_units,
    model=None,
    **kwargs
)
```

## Required Data

- `data`: wide-format panel where columns are units and rows are time points.
- `control_units`: donor unit columns.
- `treated_units`: treated unit columns.
- `treatment_time`: first treated time point.

## Model Guidance

The default PyMC model is `SyntheticDifferenceInDifferencesWeightFitter`. It fits unit weights and time weights; the treatment effect is computed analytically from those weight posteriors. Tune `omega_raw`, `lam_raw`, intercept, and noise priors when weights are too concentrated, too uniform, or when the outcome scale is far from the defaults.

## Example

```python
import causalpy as cp

df = cp.load_data("sc")

result = cp.SyntheticDifferenceInDifferences(
    df,
    treatment_time=70,
    control_units=["a", "b", "c", "d", "e", "f", "g"],
    treated_units=["actual"],
    model=cp.pymc_models.SyntheticDifferenceInDifferencesWeightFitter(
        sample_kwargs={"target_accept": 0.95}
    ),
)

result.summary()
summary = result.effect_summary(direction="increase")
result.plot()
```

## Interpretation Checks

- Compare against `SyntheticControl` when the time-weighting assumption is not central.
- Inspect pre-period fit, unit weights, and time weights.
- Report the double-difference estimand clearly; the treatment effect is not a direct regression coefficient inside the PyMC model.
