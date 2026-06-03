# Instrumental Variable

Use `cp.InstrumentalVariable` when treatment is endogenous and there is a credible instrument for treatment.

## Constructor

```python
cp.InstrumentalVariable(
    instruments_data,
    data,
    instruments_formula,
    formula,
    model=None,
    priors=None,
    vs_prior_type=None,
    vs_hyperparams=None,
    binary_treatment=False,
    **kwargs
)
```

## Required Data

- `instruments_data`: DataFrame containing the treatment variable and instrument columns.
- `data`: DataFrame containing the outcome, treatment, and outcome-stage covariates.
- `instruments_formula`: first-stage formula, for example `"t ~ 1 + z"`.
- `formula`: outcome-stage formula, for example `"y ~ 1 + t + x"`.
- `binary_treatment`: set to `True` for binary endogenous treatment.

## Model Guidance

Only Bayesian PyMC models are supported. The default is `cp.pymc_models.InstrumentalVariableRegression`. Priors are passed to `cp.InstrumentalVariable(..., priors=...)`, not to the model constructor, and should match the scale of the treatment-stage and outcome-stage regressions. Variable-selection priors are available through `vs_prior_type` and `vs_hyperparams`.

## Example

```python
import numpy as np
import pandas as pd
import causalpy as cp

rng = np.random.default_rng(42)
n = 100
z = rng.normal(size=n)
x = rng.normal(size=n)
unobserved = rng.normal(size=n)
t = 0.8 * z + 0.5 * x + unobserved + rng.normal(size=n)
y = 1.5 * t + 0.5 * x + unobserved + rng.normal(size=n)
df = pd.DataFrame({"y": y, "t": t, "x": x, "z": z})

result = cp.InstrumentalVariable(
    instruments_data=df[["t", "z"]],
    data=df[["y", "t", "x"]],
    instruments_formula="t ~ 1 + z",
    formula="y ~ 1 + t + x",
    model=cp.pymc_models.InstrumentalVariableRegression(
        sample_kwargs={"target_accept": 0.95}
    ),
    priors={
        "mus": [[0, 0], [0, 0, 0]],
        "sigmas": [2, 5],
        "eta": 2,
        "lkj_sd": 1,
    },
)
```

## Interpretation Checks

- `plot()`, `summary()`, and `effect_summary()` are not implemented for this experiment.
- Check instrument relevance, exclusion restriction plausibility, and weak-instrument sensitivity before using causal language.
- Use variable-selection priors cautiously and report whether conclusions depend on them.
