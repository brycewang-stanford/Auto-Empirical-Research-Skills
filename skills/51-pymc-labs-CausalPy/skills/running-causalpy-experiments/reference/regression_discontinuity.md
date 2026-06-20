# Regression Discontinuity

Use `cp.RegressionDiscontinuity` when treatment assignment changes discontinuously at a known cutoff in a running variable.

## Constructor

```python
cp.RegressionDiscontinuity(
    data,
    formula,
    treatment_threshold,
    model=None,
    running_variable_name="x",
    epsilon=0.001,
    bandwidth=np.inf,
    donut_hole=0.0,
    **kwargs
)
```

## Required Data

- `data`: DataFrame with outcome, running variable, and treatment indicator or formula terms that encode treatment.
- `running_variable_name`: assignment variable, defaulting to `"x"`.
- `treatment_threshold`: cutoff where assignment changes.
- `formula`: include enough terms to model both sides of the cutoff, for example `"y ~ 1 + age + treated + age:treated"`.
- `bandwidth`: optional local window around the cutoff.
- `donut_hole`: optional exclusion region around the cutoff for robustness.

## Model Guidance

The default backend is `cp.pymc_models.LinearRegression`, and sklearn regressors are supported. Scale the running variable around the cutoff or use priors that match the units of the running variable and outcome.

## Example

```python
import causalpy as cp

df = cp.load_data("drinking")
df = df.rename(columns={"agecell": "age"}).assign(treated=lambda d: d.age > 21)

result = cp.RegressionDiscontinuity(
    df,
    formula="all ~ 1 + age + treated + age:treated",
    running_variable_name="age",
    treatment_threshold=21,
    model=cp.pymc_models.LinearRegression(sample_kwargs={"target_accept": 0.95}),
)

result.summary()
summary = result.effect_summary(direction="increase")
result.plot()
```

## Interpretation Checks

- Check whether units can manipulate the running variable near the threshold.
- Use `cp.checks.BandwidthSensitivity` and `cp.checks.McCraryDensityTest` through `cp.SensitivityAnalysis` for robustness.
- Use `RegressionKink` when the causal estimand is a slope change rather than a jump.
