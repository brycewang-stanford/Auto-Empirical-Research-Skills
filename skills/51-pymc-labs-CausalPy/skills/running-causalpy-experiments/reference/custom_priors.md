# Scale-Aware Custom Priors

Use custom priors whenever CausalPy is fitting a PyMC model to predictors and outcomes that are not already on comparable, interpretable scales. Defaults are useful for examples, but a default such as `Normal(0, 50)` on coefficients or `HalfNormal(1)` on outcome noise can be too weak, too tight, or simply mismatched when outcomes are revenue, deaths, log-sales, percentages, or standardized scores.

## Basic Workflow

1. Inspect scales before fitting: summarize the outcome, treatment indicators, running variables, donor units, and continuous covariates.
2. Decide whether to standardize. Standardizing continuous predictors often makes coefficient priors easier; standardizing the outcome helps when effect interpretation can later be transformed back.
3. If you do not standardize the outcome, set priors on coefficients and likelihood noise in the outcome's units.
4. Use `sample_kwargs` for computational behavior and `priors=...` for model assumptions. Keep these separate.
5. After fitting, inspect posterior diagnostics, prior/posterior predictive reasonableness, pre-period fit, coefficient magnitudes, and sensitivity to plausible prior alternatives.

## LinearRegression Priors

`cp.pymc_models.LinearRegression` accepts `priors=...` with `pymc_extras.prior.Prior` objects. Match dims to the model: coefficients use `["treated_units", "coeffs"]`, and likelihood noise usually uses `["treated_units"]`.

```python
import causalpy as cp
from pymc_extras.prior import Prior

model = cp.pymc_models.LinearRegression(
    sample_kwargs={"target_accept": 0.95, "random_seed": 42},
    priors={
        "beta": Prior("Normal", mu=0, sigma=2.5, dims=["treated_units", "coeffs"]),
        "y_hat": Prior(
            "Normal",
            sigma=Prior("HalfNormal", sigma=10, dims=["treated_units"]),
            dims=["obs_ind", "treated_units"],
        ),
    },
)
```

If predictors are standardized and the outcome is standardized, coefficient priors such as `Normal(0, 1)` or `Normal(0, 2.5)` are usually easier to reason about. If the outcome remains in original units, set the `y_hat` noise prior in those units.

## Synthetic-Control Weight Priors

`WeightedSumFitter` uses Dirichlet weights. Lower concentration encourages sparse donor weights; higher concentration encourages more uniform donor weights.

```python
from pymc_extras.prior import Prior

model = cp.pymc_models.WeightedSumFitter(
    priors={
        "beta": Prior("Dirichlet", a=[1, 1, 1, 1], dims=["treated_units", "coeffs"]),
        "y_hat": Prior(
            "Normal",
            sigma=Prior("HalfNormal", sigma=5, dims=["treated_units"]),
            dims=["obs_ind", "treated_units"],
        ),
    }
)
```

`SoftmaxWeightedSumFitter` controls regularization through the scale of `beta_raw`. Smaller `sigma` pulls weights toward uniform; larger `sigma` lets weights concentrate on better-matching donors.

```python
model = cp.pymc_models.SoftmaxWeightedSumFitter(
    priors={
        "beta_raw": Prior("Normal", mu=0, sigma=0.5, dims=["treated_units", "coeffs_raw"])
    }
)
```

`SyntheticDifferenceInDifferencesWeightFitter` uses `omega_raw` for unit weights and `lam_raw` for time weights. Tighten these when weights are implausibly concentrated or loosen them when the fit is overly uniform and misses the pre-period pattern.

## PropensityScore Priors

For `InversePropensityWeighting`, the propensity model is logistic. Standardize continuous covariates before fitting or choose priors that imply plausible log-odds shifts.

```python
model = cp.pymc_models.PropensityScore(
    sample_kwargs={"target_accept": 0.95, "random_seed": 42},
    priors={"b": Prior("Normal", mu=0, sigma=1, dims="coeffs")},
)
```

Very large propensity-score coefficients can imply near-zero or near-one treatment probabilities, producing unstable weights. Inspect overlap and use `plot_balance_ecdf()` after fitting.

## InstrumentalVariableRegression Priors

`InstrumentalVariable` accepts a `priors=...` dictionary at the experiment level. The `mus` and `sigmas` entries cover the treatment-stage and outcome-stage coefficients. Set these based on the scales of instruments, treatment, covariates, and outcome.

```python
result = cp.InstrumentalVariable(
    instruments_data=instruments_data,
    data=data,
    instruments_formula="t ~ 1 + z",
    formula="y ~ 1 + t + x",
    model=cp.pymc_models.InstrumentalVariableRegression(
        sample_kwargs={"target_accept": 0.95, "random_seed": 42}
    ),
    priors={
        "mus": [[0, 0], [0, 0, 0]],
        "sigmas": [2, 5],
        "eta": 2,
        "lkj_sd": 1,
    },
)
```

For weak instruments or many instruments, consider variable-selection priors through `vs_prior_type` and `vs_hyperparams`, then report the sensitivity of the causal estimate to prior choices.
