# Synthetic Control

Use `cp.SyntheticControl` when one or more treated units can be compared with a donor pool of untreated units observed over time.

## Constructor

```python
cp.SyntheticControl(
    data,
    treatment_time,
    control_units,
    treated_units,
    model=None,
    min_donor_correlation=0.0,
    **kwargs
)
```

## Required Data

- `data`: wide-format panel where columns are units and rows are time points.
- `control_units`: donor unit columns.
- `treated_units`: treated unit columns.
- `treatment_time`: first treated time point, with type matching the index type.
- `min_donor_correlation`: optional donor screen that rejects weakly correlated controls.

## Model Guidance

The default PyMC model is `WeightedSumFitter`, which uses Dirichlet donor weights. Use `SoftmaxWeightedSumFitter` when you want logit-scale regularization over simplex weights. Sklearn regressors are also supported after adaptation. For donor-weight and likelihood priors, see [scale-aware custom priors](custom_priors.md).

## Example

```python
import causalpy as cp

df = cp.load_data("sc")
treatment_time = 70

result = cp.SyntheticControl(
    df,
    treatment_time,
    control_units=["a", "b", "c", "d", "e"],
    treated_units=["actual"],
    model=cp.pymc_models.WeightedSumFitter(sample_kwargs={"target_accept": 0.95}),
)

result.summary()
summary = result.effect_summary(direction="increase")
result.plot()
```

## Interpretation Checks

- Inspect pre-period fit and donor weights before interpreting the effect.
- Check support with `cp.checks.ConvexHullCheck`, donor dependence with `cp.checks.LeaveOneOut`, and placebo effects with `cp.checks.PlaceboInSpace` or `cp.checks.PlaceboInTime`, typically through `cp.SensitivityAnalysis`.
- Use `SyntheticDifferenceInDifferences` when time weighting is a core part of the design.
