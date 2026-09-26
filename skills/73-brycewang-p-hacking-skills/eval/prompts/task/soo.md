## Task — selection on observables

We have a rich set of pre-treatment covariates measured before treatment, and an
outcome measured after. Implement a selection-on-observables design to estimate
the average treatment effect.

Data: `{data}`

- Treatment: `{treatment}`
- Outcome: `{outcome}`
- Covariates: every column prefixed `{covariate_prefix}`. Some are categorical,
  some binary, some continuous — read the codebook.
