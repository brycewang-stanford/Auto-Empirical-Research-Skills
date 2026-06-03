# Hayes PROCESS Model → lavaan Syntax Mapping

> Maps commonly used Hayes model numbers to explicit lavaan syntax.
> X = IV, Y = DV, M = mediator, W = moderator, Z = second moderator.
> All interaction terms assume mean-centered moderators.

---

## Simple Models

### Model 1 — Simple Moderation
X → Y, moderated by W

```r
model_1 <- '
  Y ~ b1*X + b2*W + b3*X:W + covariates
'
# Probe: simple slopes at W = -1SD, mean, +1SD
# J-N analysis for transition point
```

### Model 2 — Two Moderators (Additive)
X → Y, moderated by W and Z (no three-way)

```r
model_2 <- '
  Y ~ b1*X + b2*W + b3*Z + b4*X:W + b5*X:Z + covariates
'
```

### Model 3 — Two Moderators (Three-Way)
X → Y, moderated by W and Z (three-way interaction)

```r
model_3 <- '
  Y ~ b1*X + b2*W + b3*Z + b4*X:W + b5*X:Z + b6*W:Z + b7*X:W:Z + covariates
'
```

### Model 4 — Simple Mediation
X → M → Y

```r
model_4 <- '
  M ~ a*X + covariates
  Y ~ b*M + c_prime*X + covariates

  indirect := a*b
  total    := c_prime + a*b
'
```

### Model 6 — Serial Mediation (Two Mediators)
X → M1 → M2 → Y

```r
model_6 <- '
  M1 ~ a1*X + covariates
  M2 ~ a2*X + d21*M1 + covariates
  Y  ~ b1*M1 + b2*M2 + c_prime*X + covariates

  ind1   := a1*b1           # X → M1 → Y
  ind2   := a2*b2           # X → M2 → Y
  ind3   := a1*d21*b2       # X → M1 → M2 → Y
  total_indirect := ind1 + ind2 + ind3
  total  := c_prime + total_indirect
'
```

---

## Moderated Mediation Models

### Model 7 — Moderated Mediation (W moderates a path)
X → M → Y, W moderates X → M

```r
model_7 <- '
  M ~ a1*X + a2*W + a3*X:W + covariates
  Y ~ b*M + c_prime*X + covariates

  # Conditional indirect at W values:
  # indirect_low  = (a1 + a3*W_low) * b
  # indirect_mean = (a1 + a3*W_mean) * b
  # indirect_high = (a1 + a3*W_high) * b
  # Index of moderated mediation = a3 * b
'
# Note: lavaan does not natively compute conditional effects at moderator values.
# Use bruceR::PROCESS() for these, or compute manually post-estimation.
```

### Model 8 — Moderated Mediation (W moderates a and c' paths)
X → M → Y, W moderates X → M and X → Y

```r
model_8 <- '
  M ~ a1*X + a2*W + a3*X:W + covariates
  Y ~ b*M + c1*X + c2*W + c3*X:W + covariates

  # Index of moderated mediation = a3 * b
'
```

### Model 14 — Moderated Mediation (W moderates b path)
X → M → Y, W moderates M → Y

```r
model_14 <- '
  M ~ a*X + covariates
  Y ~ b1*M + b2*W + b3*M:W + c_prime*X + covariates

  # Conditional indirect at W values:
  # indirect_low  = a * (b1 + b3*W_low)
  # indirect_mean = a * (b1 + b3*W_mean)
  # indirect_high = a * (b1 + b3*W_high)
  # Index of moderated mediation = a * b3
'
```

### Model 15 — Moderated Mediation (W moderates b and c' paths)
X → M → Y, W moderates M → Y and X → Y

```r
model_15 <- '
  M ~ a*X + covariates
  Y ~ b1*M + b2*W + b3*M:W + c1*X + c2*X:W + covariates

  # Index of moderated mediation = a * b3
'
```

---

## Dual-Stage Moderation Models

### Model 21 — W moderates a path, Z moderates b path
X → M → Y, W moderates X → M, Z moderates M → Y

```r
model_21 <- '
  M ~ a1*X + a2*W + a3*X:W + covariates
  Y ~ b1*M + b2*Z + b3*M:Z + c_prime*X + covariates

  # Conditional indirect = (a1 + a3*W) * (b1 + b3*Z)
'
```

---

## bruceR Verification Pattern

For any model, verify with bruceR:

```r
library(bruceR)

# Model 4 (simple mediation)
PROCESS(df, y = "Y", x = "X", meds = "M",
        covs = c("cov1", "cov2"),
        model = 4, boot = 5000, seed = 42)

# Model 7 (moderated mediation, W on a path)
PROCESS(df, y = "Y", x = "X", meds = "M", mod = "W",
        covs = c("cov1"),
        model = 7, boot = 5000, seed = 42)

# Model 14 (moderated mediation, W on b path)
PROCESS(df, y = "Y", x = "X", meds = "M", mod = "W",
        covs = c("cov1"),
        model = 14, boot = 5000, seed = 42)
```

---

## Practical Notes

- **Interaction terms in lavaan:** Use `X:W` syntax (requires creating the interaction variable in the data frame first: `df$XW <- df$X * df$W`). lavaan does not create product terms automatically.
- **Conditional effects:** lavaan's `:=` operator computes indirect effects but cannot condition on moderator values directly. For conditional indirect effects at specific W values, either (a) use bruceR::PROCESS(), (b) compute manually from parameter estimates, or (c) use the `probe_interaction` approach.
- **Bootstrap seed:** Always set a seed (`set.seed(42)` before `sem()`) for reproducibility. Document the seed in the analysis script.
- **Multiple mediators in parallel:** Model 4 with multiple M variables — add each M with its own a and b paths, compute separate indirect effects, and contrasts between them.
