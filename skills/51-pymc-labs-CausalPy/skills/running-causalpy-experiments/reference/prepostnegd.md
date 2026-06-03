# PrePostNEGD

Use `cp.PrePostNEGD` for pretest/posttest nonequivalent group designs where a baseline outcome is used to adjust post-treatment group comparisons.

## Constructor

```python
cp.PrePostNEGD(
    data,
    formula,
    group_variable_name,
    pretreatment_variable_name,
    model=None,
    **kwargs
)
```

## Required Data

- `data`: DataFrame with post-treatment outcome, pretreatment outcome, and group indicator.
- `formula`: usually post outcome on group and pre outcome, for example `"post ~ 1 + C(group) + pre"`.
- `group_variable_name`: binary or boolean group column.
- `pretreatment_variable_name`: baseline outcome column.

## Model Guidance

Only Bayesian PyMC models are supported. The default model is `cp.pymc_models.LinearRegression`. Because pre and post outcomes may have natural units, set priors for coefficients and noise to match those units or standardize both before fitting.

## Example

```python
import causalpy as cp

df = cp.load_data("anova1")

result = cp.PrePostNEGD(
    df,
    formula="post ~ 1 + C(group) + pre",
    group_variable_name="group",
    pretreatment_variable_name="pre",
    model=cp.pymc_models.LinearRegression(sample_kwargs={"target_accept": 0.95}),
)

result.summary()
summary = result.effect_summary(direction="increase")
result.plot()
```

## Interpretation Checks

- The baseline outcome must be a credible adjustment for pre-existing group differences.
- Use DiD when repeated pre/post time structure is available and parallel trends can be assessed.
