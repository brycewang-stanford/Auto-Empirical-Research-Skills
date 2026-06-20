# Interrupted Time Series

Use `cp.InterruptedTimeSeries` when a single outcome series has a known intervention time and the counterfactual can be forecast from pre-intervention data.

## Constructor

```python
cp.InterruptedTimeSeries(
    data,
    treatment_time,
    formula,
    model=None,
    treatment_end_time=None,
    **kwargs
)
```

## Required Data

- `data`: DataFrame with a numeric or datetime index. If the index is a `DatetimeIndex`, `treatment_time` must be a `pd.Timestamp`.
- `treatment_time`: first treated time point.
- `treatment_end_time`: optional end of a temporary treatment period, used by persistence analysis.
- `formula`: fit on pre-treatment data, often including time trend, seasonality, or covariates.

## Model Guidance

The default backend is `cp.pymc_models.LinearRegression`, and sklearn regressors are supported. Consider `BayesianBasisExpansionTimeSeries` or `StateSpaceTimeSeries` for more structured time-series models, but note these are experimental. Set priors in the outcome scale or standardize before fitting.

## Example

```python
import causalpy as cp
import pandas as pd

df = cp.load_data("its")
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

treatment_time = pd.to_datetime("2017-01-01")

result = cp.InterruptedTimeSeries(
    df,
    treatment_time,
    formula="y ~ 1 + t + C(month)",
    model=cp.pymc_models.LinearRegression(sample_kwargs={"target_accept": 0.95}),
)

result.summary()
summary = result.effect_summary(direction="increase")
result.plot()
```

## Interpretation Checks

- Verify pre-period fit before interpreting post-period impacts.
- If the intervention is temporary, pass `treatment_end_time` and consider `cp.checks.PersistenceCheck()`.
- For explicit level and slope changes fitted over the whole series, use `PiecewiseITS`.
