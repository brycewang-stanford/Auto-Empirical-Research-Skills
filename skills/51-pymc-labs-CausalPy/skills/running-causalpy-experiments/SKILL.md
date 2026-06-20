---
name: running-causalpy-experiments
description: Fit, summarize, plot, and interpret a chosen CausalPy experiment. Use after the causal method has been selected, including when configuring PyMC/sklearn models and scale-aware custom priors.
---

# Running CausalPy Experiments

Use this skill when the CausalPy experiment class is already known or has just been selected by `choosing-causalpy-methods`. This skill is for execution: preparing data, instantiating the experiment, choosing a model backend, setting sane priors, inspecting outputs, plotting, and communicating results.

## Workflow

1. Load and validate a pandas `DataFrame` with the data layout required by the chosen experiment.
2. Choose a backend: PyMC models for posterior uncertainty and priors, or sklearn-compatible regressors where the experiment supports OLS/sklearn.
3. Configure the model before construction. For PyMC, set `sample_kwargs` and scale-aware `priors` when predictors or outcomes are not standardized.
4. Instantiate the experiment. CausalPy experiments fit during initialization.
5. Inspect outputs with `summary()`, `effect_summary()`, `print_coefficients()`, and `plot()` only where the chosen experiment supports them.
6. Run relevant sensitivity checks through `cp.Pipeline`, `cp.EstimateEffect`, and `cp.SensitivityAnalysis` when robustness matters.

## Model And Prior Guardrails

- Do not blindly accept diffuse default priors when predictors and outcomes are on very different scales. Either standardize the modeling variables or pass scale-aware priors to the PyMC model.
- For `cp.pymc_models.LinearRegression`, configure priors for `beta` and the observation noise inside `y_hat`.
- For synthetic-control weight models, priors control donor-weight regularization and outcome noise; see `WeightedSumFitter`, `SoftmaxWeightedSumFitter`, and `SyntheticDifferenceInDifferencesWeightFitter`.
- For `PropensityScore`, standardize continuous confounders or use coefficient priors that imply plausible log-odds shifts.
- For `InstrumentalVariableRegression`, priors are passed at the experiment level through `priors=...` and should reflect the scale of both the treatment-stage and outcome-stage regressions.
- Always check posterior diagnostics, prior predictive plausibility when available, coefficient magnitudes, counterfactual fit in the pre-period, and whether effect summaries are stable under reasonable prior alternatives.

## Common Output Methods

- `experiment.summary()`: Prints a method-specific summary where implemented.
- `experiment.effect_summary()`: Returns a decision-ready structured effect summary where implemented.
- `experiment.plot()`: Visualizes fitted values, counterfactuals, effects, or diagnostics where implemented.
- `experiment.print_coefficients()`: Shows model coefficients for model-backed experiments.
- `result = cp.Pipeline(...).run()`: Runs estimation, sensitivity checks, and report generation as a reproducible workflow.

## Important Exceptions

- `InversePropensityWeighting.plot()` is intentionally a stub. Use `plot_ate()` and `plot_balance_ecdf()` instead.
- `InversePropensityWeighting.effect_summary()` is not implemented. Inspect ATE draws, overlap, balance, and weight stability instead.
- `InstrumentalVariable.plot()`, `summary()`, and `effect_summary()` are not implemented, so inspect model outputs and first-stage/second-stage diagnostics directly.
- `PanelRegression.effect_summary()` is not implemented because panel fixed-effects models report coefficient-level estimates rather than time-window impacts. Use `summary()`, `print_coefficients()`, and `plot()` or `plot_coefficients()`.

## References

- [Scale-aware custom priors](reference/custom_priors.md)
- [Difference-in-Differences](reference/diff_in_diff.md)
- [Interrupted Time Series](reference/interrupted_time_series.md)
- [Piecewise Interrupted Time Series](reference/piecewise_its.md)
- [Synthetic Control](reference/synthetic_control.md)
- [Synthetic Difference-in-Differences](reference/synthetic_difference_in_differences.md)
- [Panel Regression](reference/panel_regression.md)
- [PrePostNEGD](reference/prepostnegd.md)
- [Regression Discontinuity](reference/regression_discontinuity.md)
- [Regression Kink](reference/regression_kink.md)
- [Staggered Difference-in-Differences](reference/staggered_did.md)
- [Instrumental Variable](reference/instrumental_variable.md)
- [Inverse Propensity Weighting](reference/inverse_propensity_weighting.md)
