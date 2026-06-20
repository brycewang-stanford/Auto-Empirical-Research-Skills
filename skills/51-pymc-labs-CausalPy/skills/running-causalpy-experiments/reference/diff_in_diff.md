# Difference-in-Differences

Use `cp.DifferenceInDifferences` when treated and control groups are observed before and after a single intervention and the causal story rests on parallel trends.

## Constructor

```python
cp.DifferenceInDifferences(
    data,
    formula,
    time_variable_name,
    group_variable_name,
    post_treatment_variable_name="post_treatment",
    model=None,
    **kwargs
)
```

## Required Data

- `data`: long-form DataFrame with an outcome, time variable, group indicator, and post-treatment indicator.
- `formula`: usually includes the group, post indicator, and their interaction, for example `"y ~ 1 + group * post_treatment"`.
- `group_variable_name`: dummy-coded group indicator where one value represents treated and the other control.
- `post_treatment_variable_name`: dummy-coded post-period indicator, defaulting to `"post_treatment"`.

## Model Guidance

The default backend is `cp.pymc_models.LinearRegression`. Sklearn regressors are also supported. If outcomes or continuous covariates are not standardized, use scale-aware priors for the linear model; see [scale-aware custom priors](custom_priors.md).

## Example

```python
import causalpy as cp

df = cp.load_data("did")

result = cp.DifferenceInDifferences(
    df,
    formula="y ~ 1 + group * post_treatment",
    time_variable_name="t",
    group_variable_name="group",
    model=cp.pymc_models.LinearRegression(sample_kwargs={"target_accept": 0.95}),
)

result.summary()
summary = result.effect_summary(direction="increase")
result.plot()
```

## Interpretation Checks

- Inspect whether pre-treatment trends look plausibly parallel before relying on the interaction effect.
- Treat the interaction coefficient and `effect_summary()` as causal only if the control group is a credible counterfactual.
- For staggered adoption, use `StaggeredDifferenceInDifferences` rather than forcing all units into a single post indicator.
