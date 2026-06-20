---


name: mediation-meta-analyst
description: Meta-analysis frameworks and methods for mediation studies


---

# Mediation Meta-Analyst

**Methods for synthesizing mediation effects across multiple studies**

Use this skill when working on: meta-analysis of indirect effects, cross-study effect aggregation, heterogeneity assessment in mediation, individual participant data (IPD) meta-analysis, or systematic reviews of mediation studies.

---

## Meta-Analysis Fundamentals

### Why Meta-Analysis of Mediation is Challenging

| Challenge | Description | Solution Approach |
|-----------|-------------|-------------------|
| Non-normal effects | Product $ab$ is not normally distributed | Use appropriate pooling methods |
| Correlated paths | $a$ and $b$ may be correlated | Model correlation structure |
| Heterogeneity | Effects vary across studies | Random effects models |
| Missing information | Studies report different statistics | Imputation or subset analysis |
| Publication bias | Small studies with null effects unpublished | Sensitivity analysis |

### Effect Size Measures

| Measure | Formula | Use Case |
|---------|---------|----------|
| Unstandardized $ab$ | $a \times b$ | Same scales across studies |
| Partially standardized | $a \times b / SD_Y$ | Standardize by outcome only |
| Fully standardized | $a' \times b'$ (standardized coefficients) | Different scales |
| $R^2_{med}$ | Proportion of effect mediated | Bounded measure |

---

## Aggregate Data Meta-Analysis

### Fixed Effects Model

When assuming homogeneous true effects, the **pooled estimate** is:

$$\hat{\theta}_{FE} = \frac{\sum_i w_i \hat{\theta}_i}{\sum_i w_i}, \quad w_i = \frac{1}{\text{SE}_i^2}$$

This pooled estimate uses inverse-variance weights to optimally combine study-specific estimates.

### Random Effects Model

When true effects vary across studies, the **pooled estimate** incorporates between-study variance:

$$\hat{\theta}_{RE} = \frac{\sum_i w_i^* \hat{\theta}_i}{\sum_i w_i^*}, \quad w_i^* = \frac{1}{\text{SE}_i^2 + \hat{\tau}^2}$$

where $\hat{\tau}^2$ is the between-study variance (tau-squared). The pooled estimate under random effects provides a more generalizable result when heterogeneity is present.

### Heterogeneity Assessment

Key statistics for assessing heterogeneity:

| Statistic | Formula | Interpretation |
|-----------|---------|----------------|
| **Q statistic** | $Q = \sum_i w_i(\hat{\theta}_i - \hat{\theta})^2$ | Test for heterogeneity |
| **I-squared** ($I^2$) | $I^2 = \max(0, \frac{Q - (k-1)}{Q})$ | % variance due to heterogeneity |
| **tau-squared** ($\tau^2$) | Between-study variance | Absolute heterogeneity |
| **H-squared** | $H^2 = Q/(k-1)$ | Relative excess variance |

The **I-squared** statistic ranges from 0-100%: <25% indicates low heterogeneity, 25-75% moderate, and >75% high heterogeneity. The **tau-squared** provides the absolute magnitude of between-study variance.

### R Implementation

```r
#' Meta-Analysis of Indirect Effects
#'
#' @param effects Vector of indirect effect estimates
#' @param se Vector of standard errors
#' @param study_names Optional study identifiers
#' @param method "FE" for fixed effects, "RE" for random effects
#' @return Meta-analysis results
meta_indirect <- function(effects, se, study_names = NULL,
                           method = c("RE", "FE")) {
  method <- match.arg(method)
  k <- length(effects)

  if (is.null(study_names)) {
    study_names <- paste0("Study ", 1:k)
  }

  # Fixed effects weights
  w_fe <- 1 / se^2

  # Q statistic
  theta_fe <- sum(w_fe * effects) / sum(w_fe)
  Q <- sum(w_fe * (effects - theta_fe)^2)
  df <- k - 1

  # Heterogeneity
  I2 <- max(0, (Q - df) / Q)

  # DerSimonian-Laird tau^2 estimate
  c <- sum(w_fe) - sum(w_fe^2) / sum(w_fe)
  tau2 <- max(0, (Q - df) / c)

  if (method == "FE") {
    weights <- w_fe
    pooled <- theta_fe
    se_pooled <- sqrt(1 / sum(w_fe))
  } else {
    # Random effects weights
    weights <- 1 / (se^2 + tau2)
    pooled <- sum(weights * effects) / sum(weights)
    se_pooled <- sqrt(1 / sum(weights))
  }

  # Confidence interval
  ci <- pooled + c(-1.96, 1.96) * se_pooled

  # Test for heterogeneity
  p_het <- 1 - pchisq(Q, df)

  list(
    pooled_effect = pooled,
    se = se_pooled,
    ci = ci,
    z = pooled / se_pooled,
    p_value = 2 * pnorm(-abs(pooled / se_pooled)),
    heterogeneity = list(
      Q = Q,
      df = df,
      p = p_het,
      I2 = I2,
      tau2 = tau2
    ),
    study_data = data.frame(
      study = study_names,
      effect = effects,
      se = se,
      weight = weights / sum(weights)
    ),
    method = method
  )
}
```

---

## Multivariate Meta-Analysis

### Pooling Correlated Effects

When studies report both $a$ and $b$ paths:

$$\begin{pmatrix} \hat{a} \\ \hat{b} \end{pmatrix} \sim N\left(\begin{pmatrix} a \\ b \end{pmatrix}, \Sigma\right)$$

### Two-Stage Approach

**Stage 1**: Extract path coefficients from each study
**Stage 2**: Pool using multivariate random effects

```r
#' Multivariate Meta-Analysis of Mediation Paths
#'
#' @param a_effects Vector of a path estimates
#' @param b_effects Vector of b path estimates
#' @param a_se Standard errors for a
#' @param b_se Standard errors for b
#' @param ab_cor Correlation between a and b estimates (often assumed 0)
#' @return Multivariate meta-analysis results
multivariate_meta_mediation <- function(a_effects, b_effects,
                                         a_se, b_se, ab_cor = 0) {
  library(metafor)

  k <- length(a_effects)

  # Construct variance-covariance matrices for each study
  V_list <- lapply(1:k, function(i) {
    cov_ab <- ab_cor * a_se[i] * b_se[i]
    matrix(c(a_se[i]^2, cov_ab, cov_ab, b_se[i]^2), 2, 2)
  })

  # Stack effects
  yi <- c(rbind(a_effects, b_effects))
  vi <- unlist(lapply(V_list, as.vector))

  # Create V matrix (block diagonal)
  V <- bldiag(V_list)

  # Fit multivariate model
  # Effect type indicator
  effect_type <- rep(c("a", "b"), k)
  study_id <- rep(1:k, each = 2)

  fit <- rma.mv(yi = yi, V = V,
                mods = ~ effect_type - 1,
                random = ~ effect_type | study_id,
                struct = "UN",
                data = data.frame(yi, effect_type, study_id))

  # Extract pooled estimates
  pooled_a <- coef(fit)["effect_typea"]
  pooled_b <- coef(fit)["effect_typeb"]

  # Compute indirect effect and CI via delta method
  vcov_pooled <- vcov(fit)
  indirect <- pooled_a * pooled_b

  # Delta method SE
  grad <- c(pooled_b, pooled_a)
  se_indirect <- sqrt(t(grad) %*% vcov_pooled %*% grad)

  list(
    pooled_a = pooled_a,
    pooled_b = pooled_b,
    pooled_indirect = indirect,
    se_indirect = as.numeric(se_indirect),
    ci_indirect = indirect + c(-1.96, 1.96) * as.numeric(se_indirect),
    model_fit = fit
  )
}
```

---

## Individual Participant Data (IPD) Meta-Analysis

### One-Stage Approach

Pool all data and fit single model with study-level random effects:

```r
#' IPD Meta-Analysis for Mediation
#'
#' @param data Combined dataset with study indicator
#' @param study_var Name of study variable
#' @param treatment Name of treatment variable
#' @param mediator Name of mediator variable
#' @param outcome Name of outcome variable
#' @return IPD meta-analysis results
ipd_meta_mediation <- function(data, study_var, treatment, mediator, outcome) {
  library(lme4)

  # Mediator model with random slopes
  m_formula <- as.formula(paste(
    mediator, "~", treatment, "+ (1 +", treatment, "|", study_var, ")"
  ))
  m_model <- lmer(m_formula, data = data)

  # Outcome model with random slopes
  y_formula <- as.formula(paste(
    outcome, "~", treatment, "+", mediator,
    "+ (1 +", treatment, "+", mediator, "|", study_var, ")"
  ))
  y_model <- lmer(y_formula, data = data)

  # Extract fixed effects (pooled estimates)
  a <- fixef(m_model)[treatment]
  b <- fixef(y_model)[mediator]
  c_prime <- fixef(y_model)[treatment]

  # Indirect effect
  indirect <- a * b

  # Bootstrap for CI
  boot_indirect <- replicate(1000, {
    boot_idx <- sample(nrow(data), replace = TRUE)
    boot_data <- data[boot_idx, ]

    m_boot <- tryCatch(
      lmer(m_formula, data = boot_data),
      error = function(e) NULL
    )
    y_boot <- tryCatch(
      lmer(y_formula, data = boot_data),
      error = function(e) NULL
    )

    if (is.null(m_boot) || is.null(y_boot)) return(NA)

    fixef(m_boot)[treatment] * fixef(y_boot)[mediator]
  })

  boot_indirect <- boot_indirect[!is.na(boot_indirect)]

  list(
    pooled_a = a,
    pooled_b = b,
    pooled_c_prime = c_prime,
    pooled_indirect = indirect,
    pooled_total = indirect + c_prime,
    se_indirect = sd(boot_indirect),
    ci_indirect = quantile(boot_indirect, c(0.025, 0.975)),
    n_studies = length(unique(data[[study_var]])),
    n_total = nrow(data),
    m_model = m_model,
    y_model = y_model
  )
}
```

### Two-Stage Approach

Estimate effects within each study, then pool:

```r
#' Two-Stage IPD Meta-Analysis
#'
#' @param data Combined dataset
#' @param study_var Study identifier
#' @return Two-stage meta-analysis results
two_stage_ipd <- function(data, study_var, treatment, mediator, outcome) {

  studies <- unique(data[[study_var]])
  k <- length(studies)

  # Stage 1: Study-specific estimates
  study_results <- lapply(studies, function(s) {
    study_data <- data[data[[study_var]] == s, ]

    # Fit models
    m_model <- lm(as.formula(paste(mediator, "~", treatment)), data = study_data)
    y_model <- lm(as.formula(paste(outcome, "~", treatment, "+", mediator)),
                  data = study_data)

    a <- coef(m_model)[treatment]
    b <- coef(y_model)[mediator]

    # Delta method SE for indirect
    se_a <- sqrt(vcov(m_model)[treatment, treatment])
    se_b <- sqrt(vcov(y_model)[mediator, mediator])
    se_indirect <- sqrt(a^2 * se_b^2 + b^2 * se_a^2)

    data.frame(
      study = s,
      n = nrow(study_data),
      a = a,
      b = b,
      indirect = a * b,
      se_a = se_a,
      se_b = se_b,
      se_indirect = se_indirect
    )
  })

  study_df <- do.call(rbind, study_results)

  # Stage 2: Pool indirect effects
  meta_result <- meta_indirect(
    effects = study_df$indirect,
    se = study_df$se_indirect,
    study_names = study_df$study,
    method = "RE"
  )

  list(
    stage1 = study_df,
    stage2 = meta_result,
    pooled_indirect = meta_result$pooled_effect,
    ci = meta_result$ci,
    I2 = meta_result$heterogeneity$I2
  )
}
```

---

## Publication Bias

### Detection Methods

| Method | Description | Limitation |
|--------|-------------|------------|
| Funnel plot | SE vs effect plot | Visual, subjective |
| Egger's test | Regression of effect on SE | Low power |
| Trim-and-fill | Impute missing studies | Assumes specific mechanism |
| PET-PEESE | Conditional regression | Requires assumptions |
| Selection models | Model publication process | Complex, sensitive |

### R Implementation

```r
#' Publication Bias Assessment for Mediation Meta-Analysis
#'
#' @param effects Indirect effect estimates
#' @param se Standard errors
#' @return Publication bias diagnostics
publication_bias_mediation <- function(effects, se) {
  library(metafor)

  # Fit random effects model
  res <- rma(yi = effects, sei = se, method = "REML")

  # Funnel plot data
  funnel_data <- data.frame(
    effect = effects,
    se = se,
    precision = 1/se
  )

  # Egger's test
  egger <- regtest(res, model = "lm")

  # Trim and fill
  tf <- trimfill(res)

  # PET-PEESE (if significant, use PEESE; otherwise PET)
  pet <- lm(effects ~ se, weights = 1/se^2)
  peese <- lm(effects ~ I(se^2), weights = 1/se^2)

  pet_est <- coef(pet)[1]
  peese_est <- coef(peese)[1]

  # Use PEESE if PET significant, else PET
  if (coef(summary(pet))[2, 4] < 0.10) {
    adjusted_estimate <- peese_est
    method_used <- "PEESE"
  } else {
    adjusted_estimate <- pet_est
    method_used <- "PET"
  }

  list(
    original_estimate = coef(res),
    egger_test = list(
      z = egger$zval,
      p = egger$pval,
      interpretation = ifelse(egger$pval < 0.10,
                              "Evidence of funnel asymmetry",
                              "No strong evidence of asymmetry")
    ),
    trim_fill = list(
      original_k = res$k,
      imputed_k = tf$k0,
      adjusted_estimate = coef(tf),
      adjusted_ci = c(tf$ci.lb, tf$ci.ub)
    ),
    pet_peese = list(
      pet_estimate = pet_est,
      peese_estimate = peese_est,
      method_used = method_used,
      adjusted_estimate = adjusted_estimate
    ),
    funnel_data = funnel_data
  )
}
```

---

## Moderator Analysis

### Meta-Regression

Test whether study-level characteristics explain heterogeneity:

```r
#' Meta-Regression for Mediation Effects
#'
#' @param effects Indirect effect estimates
#' @param se Standard errors
#' @param moderators Data frame of moderator variables
#' @return Meta-regression results
meta_regression_mediation <- function(effects, se, moderators) {
  library(metafor)

  # Build formula from moderator names
  mod_formula <- as.formula(paste("~", paste(names(moderators), collapse = " + ")))

  # Fit mixed-effects meta-regression
  res <- rma(yi = effects, sei = se,
             mods = mod_formula,
             data = moderators,
             method = "REML")

  # R^2 analog
  res_null <- rma(yi = effects, sei = se, method = "REML")
  R2 <- max(0, (res_null$tau2 - res$tau2) / res_null$tau2)

  # Test for residual heterogeneity
  QE_test <- list(
    QE = res$QE,
    df = res$k - res$p,
    p = res$QEp
  )

  list(
    coefficients = coef(summary(res)),
    tau2_residual = res$tau2,
    I2_residual = res$I2,
    R2 = R2,
    residual_heterogeneity = QE_test,
    model = res
  )
}
```

### Subgroup Analysis

```r
#' Subgroup Analysis for Mediation Meta-Analysis
#'
#' @param effects Indirect effect estimates
#' @param se Standard errors
#' @param subgroup Factor variable defining subgroups
#' @return Subgroup analysis results
subgroup_analysis <- function(effects, se, subgroup) {

  groups <- unique(subgroup)

  # Within-group estimates
  group_results <- lapply(groups, function(g) {
    idx <- subgroup == g
    meta_indirect(effects[idx], se[idx], method = "RE")
  })
  names(group_results) <- groups

  # Extract pooled estimates
  group_effects <- sapply(group_results, function(x) x$pooled_effect)
  group_se <- sapply(group_results, function(x) x$se)
  group_k <- sapply(group_results, function(x) length(x$study_data$effect))

  # Test for subgroup differences
  # Q_between = Q_total - sum(Q_within)
  overall <- meta_indirect(effects, se, method = "RE")
  Q_total <- overall$heterogeneity$Q

  Q_within <- sapply(group_results, function(x) x$heterogeneity$Q)
  Q_between <- Q_total - sum(Q_within)
  df_between <- length(groups) - 1
  p_between <- 1 - pchisq(Q_between, df_between)

  list(
    subgroup_estimates = data.frame(
      subgroup = groups,
      k = group_k,
      effect = group_effects,
      se = group_se,
      ci_lower = group_effects - 1.96 * group_se,
      ci_upper = group_effects + 1.96 * group_se
    ),
    test_for_differences = list(
      Q_between = Q_between,
      df = df_between,
      p = p_between,
      interpretation = ifelse(p_between < 0.05,
                              "Significant subgroup differences",
                              "No significant subgroup differences")
    ),
    group_results = group_results
  )
}
```

---

## Reporting Checklist

### PRISMA for Mediation Meta-Analysis

- [ ] Search strategy documented
- [ ] Inclusion/exclusion criteria specified
- [ ] Effect measure defined (standardized vs. unstandardized)
- [ ] Method for extracting/computing indirect effects stated
- [ ] Heterogeneity statistics reported ($I^2$, $\tau^2$, $Q$)
- [ ] Forest plot included
- [ ] Publication bias assessed
- [ ] Sensitivity analyses conducted
- [ ] GRADE assessment for certainty

### Forest Plot Template

```r
#' Create Forest Plot for Mediation Meta-Analysis
#'
#' @param meta_result Result from meta_indirect()
#' @return ggplot2 forest plot
forest_plot_mediation <- function(meta_result) {
  library(ggplot2)

  df <- meta_result$study_data
  df$ci_lower <- df$effect - 1.96 * df$se
  df$ci_upper <- df$effect + 1.96 * df$se

  # Add pooled estimate
  pooled <- data.frame(
    study = "Pooled",
    effect = meta_result$pooled_effect,
    se = meta_result$se,
    weight = NA,
    ci_lower = meta_result$ci[1],
    ci_upper = meta_result$ci[2]
  )
  df <- rbind(df, pooled)
  df$study <- factor(df$study, levels = rev(df$study))

  ggplot(df, aes(x = effect, y = study)) +
    geom_vline(xintercept = 0, linetype = "dashed", color = "gray50") +
    geom_point(aes(size = weight)) +
    geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper), height = 0.2) +
    geom_point(data = df[df$study == "Pooled", ],
               shape = 18, size = 5, color = "darkred") +
    labs(
      x = "Indirect Effect",
      y = "",
      title = "Forest Plot: Meta-Analysis of Indirect Effects",
      subtitle = sprintf("I² = %.1f%%, τ² = %.4f",
                         meta_result$heterogeneity$I2 * 100,
                         meta_result$heterogeneity$tau2)
    ) +
    theme_minimal() +
    theme(legend.position = "none")
}
```

---

## References

### Meta-Analysis Methods

- Borenstein, M., et al. (2009). *Introduction to Meta-Analysis*
- Higgins, J. P., & Green, S. (2011). *Cochrane Handbook for Systematic Reviews*

### Mediation Meta-Analysis

- Cheung, M. W. L. (2015). *Meta-Analysis: A Structural Equation Modeling Approach*
- MacKinnon, D. P. (2008). *Introduction to Statistical Mediation Analysis*

### Publication Bias

- Rothstein, H. R., et al. (2005). *Publication Bias in Meta-Analysis*
- Stanley, T. D., & Doucouliagos, H. (2014). Meta-regression approximations

### Software

- Viechtbauer, W. (2010). Conducting meta-analyses in R with the metafor package
- Cheung, M. W. L. (2015). metaSEM: Meta-analysis using structural equation modeling

---

**Version**: 1.0.0
**Created**: 2025-12-09
**Domain**: Meta-analysis of mediation effects
**Applications**: Systematic reviews, research synthesis, evidence aggregation
