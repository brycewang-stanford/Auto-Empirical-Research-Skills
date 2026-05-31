---


name: sensitivity-analyst
description: Sensitivity analysis frameworks and assumption-testing methods


---

# Sensitivity Analyst

**Comprehensive sensitivity analysis frameworks for causal inference and mediation studies**

Use this skill when working on: unmeasured confounding assessment, E-values, tipping point analysis, measurement error sensitivity, model misspecification checks, Rosenbaum bounds, or any robustness evaluation for causal claims.

---

## Unmeasured Confounding

### The Fundamental Problem

In causal inference, we can never directly test the assumption of no unmeasured confounding. Sensitivity analysis quantifies: "How strong would unmeasured confounding need to be to explain away our findings?"

### Bias Factor Framework

For an unmeasured confounder $U$ affecting both treatment $A$ and outcome $Y$:

$$\text{Bias} = \frac{E[Y \mid A=1, U=1] - E[Y \mid A=1, U=0]}{E[Y \mid A=0, U=1] - E[Y \mid A=0, U=0]} \times \frac{P(U=1 \mid A=1) - P(U=1 \mid A=0)}{1}$$

The observed effect $\hat{\theta}$ relates to the true effect $\theta$ via:

$$\hat{\theta} = \theta \times \text{Bias Factor}$$

### Sensitivity Parameters

| Parameter | Definition | Range |
|-----------|------------|-------|
| $\gamma$ | Odds ratio for U-A association | $[1, \infty)$ |
| $\delta$ | Odds ratio for U-Y association | $[1, \infty)$ |
| $\rho$ | Correlation of U with unmeasured factors | $[-1, 1]$ |

### R Implementation

```r
#' Sensitivity Analysis for Unmeasured Confounding
#'
#' @param estimate Point estimate of causal effect
#' @param se Standard error of estimate
#' @param gamma_range Range of treatment-confounder association
#' @param delta_range Range of outcome-confounder association
#' @return Sensitivity analysis results
sensitivity_unmeasured <- function(estimate, se,
                                    gamma_range = seq(1, 3, 0.25),
                                    delta_range = seq(1, 3, 0.25)) {

  # Create grid of sensitivity parameters
  grid <- expand.grid(gamma = gamma_range, delta = delta_range)

  # Compute bias factor for each combination
  # Using Ding & VanderWeele (2016) bias formula
  grid$bias_factor <- with(grid, (gamma * delta) / (gamma + delta - 1))

  # Adjusted estimates
  grid$adjusted_estimate <- estimate / grid$bias_factor

  # Find tipping point where CI includes 0
  z_crit <- qnorm(0.975)
  ci_lower <- estimate - z_crit * se

  # Tipping point: where adjusted CI lower bound = 0
  tipping_points <- grid[grid$adjusted_estimate - z_crit * se / grid$bias_factor <= 0, ]

  list(
    original = list(estimate = estimate, ci = c(ci_lower, estimate + z_crit * se)),
    sensitivity_grid = grid,
    tipping_points = tipping_points,
    minimum_bias_to_nullify = min(grid$bias_factor[grid$adjusted_estimate <= 0])
  )
}
```

---

## E-Values

### E-Value Definition

The **E-value** (VanderWeele & Ding, 2017) is the minimum strength of association that an unmeasured confounder would need to have with both treatment and outcome to fully explain away the observed effect.

For a risk ratio $RR$:

$$E\text{-value} = RR + \sqrt{RR \times (RR - 1)}$$

For the confidence interval limit:

$$E\text{-value}_{CI} = RR_{lower} + \sqrt{RR_{lower} \times (RR_{lower} - 1)}$$

### Interpretation Guidelines

| E-value | Interpretation |
|---------|----------------|
| < 1.5 | Very weak; easily explained by modest confounding |
| 1.5 - 2.0 | Weak; moderate confounding could explain |
| 2.0 - 3.0 | Moderate; substantial confounding needed |
| 3.0 - 4.0 | Strong; would require strong confounding |
| > 4.0 | Very strong; unlikely to be fully explained |

### E-Value for Different Effect Measures

| Measure | Formula |
|---------|---------|
| Risk Ratio (RR) | $E = RR + \sqrt{RR(RR-1)}$ |
| Odds Ratio (OR) | Convert to RR approximation first |
| Hazard Ratio (HR) | $E = HR + \sqrt{HR(HR-1)}$ (when rare outcome) |
| Risk Difference | Convert to RR using baseline risk |
| Standardized Mean Difference | $E = \exp(0.91 \times d) + \sqrt{\exp(0.91 \times d)(\exp(0.91 \times d)-1)}$ |

### R Implementation

```r
#' Compute E-value for Causal Effect Estimate
#'
#' @param estimate Effect estimate (RR, OR, HR, or SMD)
#' @param lo Lower confidence limit
#' @param hi Upper confidence limit
#' @param type Type of effect measure
#' @param rare For OR/HR, is outcome rare (<15%)?
#' @return E-value and interpretation
compute_evalue <- function(estimate, lo = NULL, hi = NULL,
                           type = c("RR", "OR", "HR", "SMD"),
                           rare = TRUE) {
  type <- match.arg(type)

  # Convert to RR scale
  rr <- switch(type,
    "RR" = estimate,
    "OR" = if (rare) estimate else sqrt(estimate),  # Rare outcome approximation
    "HR" = if (rare) estimate else sqrt(estimate),
    "SMD" = exp(0.91 * estimate)
  )

  # Ensure RR >= 1 for formula (flip if protective)
  if (rr < 1) rr <- 1/rr

  # E-value formula
  evalue <- rr + sqrt(rr * (rr - 1))

  # E-value for CI
  evalue_ci <- NULL
  if (!is.null(lo)) {
    rr_lo <- switch(type,
      "RR" = lo,
      "OR" = if (rare) lo else sqrt(lo),
      "HR" = if (rare) lo else sqrt(lo),
      "SMD" = exp(0.91 * lo)
    )
    if (rr_lo < 1) rr_lo <- 1/rr_lo
    if (rr_lo >= 1) {
      evalue_ci <- rr_lo + sqrt(rr_lo * (rr_lo - 1))
    } else {
      evalue_ci <- 1
    }
  }

  # Interpretation
  interpretation <- case_when(
    evalue < 1.5 ~ "Very weak evidence; easily explained by modest confounding",
    evalue < 2.0 ~ "Weak evidence; moderate confounding could explain",
    evalue < 3.0 ~ "Moderate evidence; substantial confounding needed",
    evalue < 4.0 ~ "Strong evidence; strong confounding would be required",
    TRUE ~ "Very strong evidence; unlikely explained by confounding alone"
  )

  list(
    evalue_point = evalue,
    evalue_ci = evalue_ci,
    interpretation = interpretation,
    message = sprintf(
      "To explain away the estimate, an unmeasured confounder would need to be associated with both treatment and outcome by RR = %.2f each.",
      evalue
    )
  )
}
```

---

## Tipping Point Analysis

### Concept

Tipping point analysis identifies the specific parameter values at which conclusions would change (e.g., confidence interval includes null, effect reverses sign).

### Tipping Point Types

| Type | Definition | Use Case |
|------|------------|----------|
| **Null tipping point** | Where CI includes 0 | Statistical significance |
| **Clinical tipping point** | Where effect < MCID | Clinical significance |
| **Direction tipping point** | Where effect changes sign | Effect direction |

### Visualization

```r
#' Create Tipping Point Contour Plot
#'
#' @param estimate Point estimate
#' @param se Standard error
#' @param gamma_range Confounder-treatment association range
#' @param delta_range Confounder-outcome association range
#' @return ggplot2 contour plot
plot_tipping_point <- function(estimate, se,
                                gamma_range = seq(1, 5, 0.1),
                                delta_range = seq(1, 5, 0.1)) {
  library(ggplot2)

  grid <- expand.grid(gamma = gamma_range, delta = delta_range)
  grid$bias_factor <- with(grid, (gamma * delta) / (gamma + delta - 1))
  grid$adjusted <- estimate / grid$bias_factor
  grid$significant <- grid$adjusted - 1.96 * se / grid$bias_factor > 0

  ggplot(grid, aes(x = gamma, y = delta, z = adjusted)) +
    geom_contour_filled(breaks = c(-Inf, 0, estimate/2, estimate, Inf)) +
    geom_contour(aes(z = as.numeric(significant)),
                 breaks = 0.5, color = "red", linewidth = 1.5) +
    labs(
      x = "Confounder-Treatment Association (γ)",
      y = "Confounder-Outcome Association (δ)",
      title = "Tipping Point Analysis",
      subtitle = "Red line: boundary of statistical significance"
    ) +
    theme_minimal()
}
```

---

## Measurement Error Sensitivity

### Types of Measurement Error

| Type | Description | Effect on Estimates |
|------|-------------|---------------------|
| **Non-differential** | Error unrelated to other variables | Usually biases toward null |
| **Differential** | Error depends on treatment/outcome | Can bias in either direction |
| **Systematic** | Consistent over/under-reporting | Shifts estimates |
| **Random** | Noise around true value | Attenuates relationships |

### Measurement Error in Mediation

For mediation with misclassified mediator:

$$\hat{a}\hat{b} = ab \times \text{Attenuation Factor}$$

where:

$$\text{Attenuation} = \frac{\text{Sensitivity} + \text{Specificity} - 1}{1}$$

### R Implementation for Misclassification

```r
#' Sensitivity Analysis for Mediator Misclassification
#'
#' @param indirect_effect Observed indirect effect
#' @param se_indirect Standard error
#' @param sens_range Sensitivity range to explore
#' @param spec_range Specificity range to explore
#' @return Corrected estimates grid
sensitivity_misclassification <- function(indirect_effect, se_indirect,
                                           sens_range = seq(0.7, 1, 0.05),
                                           spec_range = seq(0.7, 1, 0.05)) {

  grid <- expand.grid(sensitivity = sens_range, specificity = spec_range)

  # Attenuation factor
  grid$attenuation <- grid$sensitivity + grid$specificity - 1


  # Corrected indirect effect (assuming non-differential)
  grid$corrected_effect <- indirect_effect / grid$attenuation

  # Corrected SE (approximate)
  grid$corrected_se <- se_indirect / grid$attenuation

  # CI
  grid$ci_lower <- grid$corrected_effect - 1.96 * grid$corrected_se
  grid$ci_upper <- grid$corrected_effect + 1.96 * grid$corrected_se

  # Identify where conclusions change
  original_significant <- (indirect_effect - 1.96 * se_indirect) > 0
  grid$conclusion_change <- (grid$ci_lower > 0) != original_significant

  list(
    original = list(
      effect = indirect_effect,
      se = se_indirect,
      significant = original_significant
    ),
    sensitivity_grid = grid,
    robust_region = grid[!grid$conclusion_change, ],
    vulnerable_region = grid[grid$conclusion_change, ]
  )
}
```

---

## Model Misspecification

### Types of Misspecification

1. **Functional form**: Linear when true relationship is nonlinear
2. **Omitted variables**: Missing important confounders
3. **Incorrect distribution**: Wrong error distribution assumed
4. **Heterogeneity**: Ignoring effect modification

### Specification Curve Analysis

Test how results vary across defensible model specifications:

```r
#' Specification Curve Analysis
#'
#' @param data Dataset
#' @param outcome Outcome variable name
#' @param treatment Treatment variable name
#' @param mediator Mediator variable name
#' @param covariate_sets List of covariate sets to try
#' @param model_types Vector of model types to try
#' @return Specification curve results
specification_curve <- function(data, outcome, treatment, mediator,
                                 covariate_sets,
                                 model_types = c("linear", "logistic")) {

  results <- list()
  spec_id <- 1

  for (covs in covariate_sets) {
    for (model_type in model_types) {

      # Fit mediator model
      m_formula <- as.formula(paste(mediator, "~", treatment, "+",
                                     paste(covs, collapse = "+")))

      # Fit outcome model
      y_formula <- as.formula(paste(outcome, "~", treatment, "+", mediator, "+",
                                     paste(covs, collapse = "+")))

      if (model_type == "linear") {
        m_model <- lm(m_formula, data = data)
        y_model <- lm(y_formula, data = data)
      } else {
        m_model <- glm(m_formula, data = data, family = binomial)
        y_model <- glm(y_formula, data = data, family = binomial)
      }

      # Extract coefficients
      a <- coef(m_model)[treatment]
      b <- coef(y_model)[mediator]
      indirect <- a * b

      results[[spec_id]] <- data.frame(
        spec_id = spec_id,
        covariates = paste(covs, collapse = ", "),
        model_type = model_type,
        a_path = a,
        b_path = b,
        indirect_effect = indirect,
        n_covariates = length(covs)
      )

      spec_id <- spec_id + 1
    }
  }

  results_df <- do.call(rbind, results)

  # Summary statistics
  list(
    specifications = results_df,
    summary = data.frame(
      median_effect = median(results_df$indirect_effect),
      mean_effect = mean(results_df$indirect_effect),
      sd_effect = sd(results_df$indirect_effect),
      min_effect = min(results_df$indirect_effect),
      max_effect = max(results_df$indirect_effect),
      prop_positive = mean(results_df$indirect_effect > 0),
      prop_significant = NA
    ),
    n_specifications = nrow(results_df)
  )
}
```

---

## Rosenbaum Bounds

### Framework

Rosenbaum bounds quantify how sensitive causal conclusions are to hidden bias in observational studies using matched designs.

### Sensitivity Parameter Γ

$\Gamma$ represents the maximum ratio of odds of treatment for two matched subjects:

$$\frac{1}{\Gamma} \leq \frac{P(A_i = 1 \mid X_i)}{P(A_j = 1 \mid X_j)} \times \frac{1 - P(A_j = 1 \mid X_j)}{1 - P(A_i = 1 \mid X_i)} \leq \Gamma$$

### Interpretation

| Γ Value | Interpretation |
|---------|----------------|
| 1.0 | No hidden bias (randomization) |
| 1.1 - 1.3 | Sensitive to small hidden bias |
| 1.3 - 2.0 | Moderately robust |
| 2.0 - 3.0 | Robust to substantial bias |
| > 3.0 | Very robust |

### R Implementation

```r
#' Rosenbaum Bounds for Matched Study
#'
#' @param outcome_diff Vector of within-pair outcome differences
#' @param gamma_range Range of sensitivity parameter
#' @return Bounds on p-values
rosenbaum_bounds <- function(outcome_diff, gamma_range = seq(1, 3, 0.1)) {

  n <- length(outcome_diff)

  # Signed rank statistic
  ranks <- rank(abs(outcome_diff))
  W_obs <- sum(ranks[outcome_diff > 0])

  results <- data.frame(gamma = gamma_range)
  results$p_upper <- NA
  results$p_lower <- NA

  for (i in seq_along(gamma_range)) {
    gamma <- gamma_range[i]

    # Upper bound: worst case p-value
    # Uses hypergeometric distribution approximation
    p_treat <- gamma / (1 + gamma)

    # Expected value and variance under gamma
    E_W <- sum(ranks) * p_treat
    V_W <- sum(ranks^2) * p_treat * (1 - p_treat)

    # Normal approximation
    z_upper <- (W_obs - E_W) / sqrt(V_W)
    results$p_upper[i] <- 1 - pnorm(z_upper)

    # Lower bound
    p_treat_low <- 1 / (1 + gamma)
    E_W_low <- sum(ranks) * p_treat_low
    V_W_low <- sum(ranks^2) * p_treat_low * (1 - p_treat_low)
    z_lower <- (W_obs - E_W_low) / sqrt(V_W_low)
    results$p_lower[i] <- 1 - pnorm(z_lower)
  }

  # Find critical gamma
  results$significant_upper <- results$p_upper < 0.05
  critical_gamma <- min(results$gamma[!results$significant_upper], na.rm = TRUE)

  list(
    bounds = results,
    critical_gamma = critical_gamma,
    interpretation = sprintf(
      "Results would be sensitive to hidden bias if Γ > %.2f",
      critical_gamma
    )
  )
}
```

---

## Sensitivity Analysis for Mediation

### Sequential Ignorability Sensitivity

For natural indirect effects, sensitivity to violation of sequential ignorability:

```r
#' Mediation Sensitivity Analysis
#'
#' Following Imai, Keele, & Yamamoto (2010)
#'
#' @param mediation_result Result from mediation analysis
#' @param rho_range Correlation between M and Y errors
#' @return Sensitivity results
sensitivity_mediation <- function(a_coef, b_coef, indirect_effect,
                                   se_indirect,
                                   rho_range = seq(-0.5, 0.5, 0.05)) {

  results <- data.frame(rho = rho_range)

  # Bias from correlation
  # Approximate bias formula from Imai et al.
  results$adjusted_indirect <- indirect_effect * (1 - rho_range^2)

  # Adjusted inference
  results$ci_lower <- results$adjusted_indirect - 1.96 * se_indirect
  results$ci_upper <- results$adjusted_indirect + 1.96 * se_indirect
  results$significant <- results$ci_lower > 0 | results$ci_upper < 0

  # Find critical rho
  original_sign <- sign(indirect_effect)
  critical_rho <- min(abs(rho_range[sign(results$adjusted_indirect) != original_sign]))

  list(
    sensitivity_grid = results,
    critical_rho = critical_rho,
    interpretation = sprintf(
      "Indirect effect sign would change if |ρ| > %.2f",
      critical_rho
    ),
    robust_range = results[results$significant, "rho"]
  )
}
```

---

## Sensitivity Analysis Checklist

### Pre-Analysis Planning

- [ ] Identify key assumptions being made
- [ ] Determine which assumptions are most uncertain
- [ ] Select appropriate sensitivity analysis methods
- [ ] Define tipping points of interest
- [ ] Plan visualization strategy

### Analysis Execution

- [ ] Compute E-values for main effects
- [ ] Conduct unmeasured confounding analysis
- [ ] Test sensitivity to measurement error (if applicable)
- [ ] Run specification curve analysis
- [ ] Compute Rosenbaum bounds (if matched design)

### Reporting Template

```markdown
## Sensitivity Analysis

### Unmeasured Confounding

The E-value for our main finding (RR = X.XX) is E = X.XX, indicating that
an unmeasured confounder would need to be associated with both treatment
and outcome by a risk ratio of at least X.XX each to fully explain away
the observed effect. This represents [interpretation] confounding.

### Tipping Point Analysis

Figure X shows the sensitivity of our conclusions to unmeasured confounding.
The observed effect would be nullified if [specific conditions].

### Measurement Error

Under the assumption of [non-differential/differential] measurement error,
our results remain significant for mediator sensitivity values above X%
and specificity above X%.

### Robustness to Model Specification

Across [N] alternative model specifications varying [covariates/functional
forms/etc.], the median indirect effect was X.XX (range: X.XX to X.XX).
[XX%] of specifications yielded statistically significant positive effects.
```

---

## References

### Foundational Papers

- VanderWeele, T. J., & Ding, P. (2017). Sensitivity analysis in observational research: Introducing the E-value. *Annals of Internal Medicine*
- Rosenbaum, P. R. (2002). *Observational Studies*
- Ding, P., & VanderWeele, T. J. (2016). Sensitivity analysis without assumptions. *Epidemiology*

### Mediation-Specific

- Imai, K., Keele, L., & Yamamoto, T. (2010). Identification, inference and sensitivity analysis for causal mediation effects. *Statistical Science*
- VanderWeele, T. J. (2010). Bias formulas for sensitivity analysis for direct and indirect effects. *Epidemiology*

### Measurement Error

- Carroll, R. J., et al. (2006). *Measurement Error in Nonlinear Models*
- Buonaccorsi, J. P. (2010). *Measurement Error: Models, Methods, and Applications*

---

**Version**: 1.0.0
**Created**: 2025-12-08
**Domain**: Sensitivity analysis for causal inference
**Applications**: Mediation analysis, observational studies, matched designs
