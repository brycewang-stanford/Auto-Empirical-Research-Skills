# Inverse Propensity Weighting

Use `cp.InversePropensityWeighting` when treatment is binary, confounders are measured, and overlap is credible enough to estimate treatment effects by propensity weighting.

## Constructor

```python
cp.InversePropensityWeighting(
    data,
    formula,
    outcome_variable,
    weighting_scheme,
    model=None,
    **kwargs
)
```

## Required Data

- `data`: DataFrame with binary treatment, outcome, and confounders.
- `formula`: propensity model formula with treatment on the left-hand side, for example `"trt ~ 1 + age + race"`.
- `outcome_variable`: outcome column to reweight.
- `weighting_scheme`: one of `"raw"`, `"robust"`, `"doubly_robust"`, or `"overlap"`.

## Model Guidance

Only Bayesian PyMC propensity-score models are supported. The default is `cp.pymc_models.PropensityScore`. Standardize continuous confounders or set priors on propensity coefficients so a one-unit covariate change implies a plausible log-odds change.

## Example

```python
import causalpy as cp

df = cp.load_data("nhefs")

result = cp.InversePropensityWeighting(
    df,
    formula="trt ~ 1 + age + race",
    outcome_variable="outcome",
    weighting_scheme="robust",
    model=cp.pymc_models.PropensityScore(sample_kwargs={"target_accept": 0.95}),
)

result.plot_ate()
result.plot_balance_ecdf(covariate="age")
```

## Interpretation Checks

- `plot()` is intentionally not a unified plot; call `plot_ate()` and `plot_balance_ecdf()`.
- `effect_summary()` is not implemented for IPW; inspect the ATE plot and balance diagnostics instead.
- Check overlap and weight stability before interpreting the ATE.
- If important confounders are unmeasured, IPW does not solve the identification problem.
