---
name: r-bayes
description: Patterns for Bayesian inference in R using brms, including multilevel models, DAG validation, and marginal effects. Use when performing Bayesian analysis.
---

## Core Packages

```r
library(brms)
library(cmdstanr)
library(dagitty)
library(ggdag)
library(marginaleffects)
library(tidybayes)
library(bayesplot)
```

## Directed Acyclic Graphs (DAGs)

Prior to causal inference, create and validate DAGs with dagitty and ggdag.

### Define DAG Structure

```r
dag <- dagitty('
dag {
  # Node positions for visualization
  exposure [pos="0,1"]
  mediator [pos="1,1"]
  outcome [pos="2,1"]
  confounder [pos="1,0"]

  # Edges (arrows)
  confounder -> exposure
  confounder -> outcome
  exposure -> mediator
  mediator -> outcome
  exposure -> outcome
}
')
```

### Identify Adjustment Sets

```r
# For direct effect
adjustmentSets(dag, exposure = "treatment", outcome = "outcome", effect = "direct")

# For total effect
adjustmentSets(dag, exposure = "treatment", outcome = "outcome", effect = "total")
```

### Validate DAG Against Data

```r
# Get implied conditional independencies
implied_cis <- impliedConditionalIndependencies(dag)

# Test against data
ci_results <- localTests(dag, data = analysis_data, type = "cis")

# Assess validation
ci_df <- as.data.frame(ci_results)
ci_df$independent <- ci_df$p.value > 0.05
pct_supported <- 100 * mean(ci_df$independent, na.rm = TRUE)

cat(sprintf("DAG support: %.1f%% of implied CIs hold\n", pct_supported))
```

### Visualize DAG

```r
dag_tidy <- tidy_dagitty(dag)

ggplot(dag_tidy, aes(x = x, y = y, xend = xend, yend = yend)) +
  geom_dag_edges(edge_colour = "grey50") +
  geom_dag_point(size = 20) +
  geom_dag_text(size = 3.5, color = "black") +
  theme_dag() +
  labs(title = "Causal DAG")
```

## Bayesian Regression with brms

### Standard Configuration

```r
options(mc.cores = 4)

# Standard brms model call
model <- brm(
  formula = outcome ~ predictor1 + predictor2 + (1 | group_id),
  data = model_data,
  family = bernoulli(link = "logit"),  # For binary outcomes
  prior = priors,
  sample_prior = "yes",  # For prior-posterior comparison
  chains = 4,
  cores = 4,
  iter = 4000,
  warmup = 1000,
  control = list(
    adapt_delta = 0.95,
    max_treedepth = 15
  ),
  seed = 123,  # Set seed for reproducibility
  backend = "cmdstanr",
  file = "models/model_name",         # Cache compiled model
  file_refit = "on_change"            # Only refit if formula/data change
)
```

### Priors

Store priors separately and define explicitly:

```r
priors <- c(
  prior(normal(0, 2), class = "Intercept"),
  prior(normal(0, 1), class = "b"),                    # Fixed effects
  prior(exponential(1), class = "sd"),                 # Random effect SD
  prior(lkj(2), class = "cor")                         # Correlation priors
)

# Get default priors for a formula
get_prior(outcome ~ predictor + (1 | id), data = data, family = bernoulli())
```

### Common Families

```r
# Binary outcome
family = bernoulli(link = "logit")

# Count data
family = poisson(link = "log")
family = negbinomial(link = "log")

# Continuous
family = gaussian()
family = student()  # Robust to outliers

# Ordinal
family = cumulative(link = "logit")
```

## Multilevel Models

### Random Intercepts

```r
# Random intercept per participant
outcome ~ predictors + (1 | participant_id)
```

### Random Slopes

```r
# Random intercept and slope for time
outcome ~ time + predictors + (1 + time | participant_id)
```

### Crossed Random Effects

```r
# Participants nested in groups, items crossed
response ~ predictors + (1 | participant_id) + (1 | item_id)
```

## Within-Person Centering

For longitudinal data, separate between-person and within-person effects:

```r
# Create person-centered variables
model_data <- data |>
  group_by(participant_id) |>
  mutate(
    # Between-person means (stable trait)
    predictor_mean = mean(predictor, na.rm = TRUE),

    # Within-person deviations (dynamic change)
    predictor_dev = predictor - predictor_mean,

    # Volatility (person-level SD)
    predictor_sd = sd(predictor, na.rm = TRUE)
  ) |>
  ungroup() |>
  # Standardize
  mutate(
    predictor_mean_z = scale(predictor_mean)[, 1],
    predictor_dev_z = scale(predictor_dev)[, 1]
  )

# Model with both components
model <- brm(
  outcome ~ predictor_mean_z + predictor_dev_z + (1 | participant_id),
  data = model_data,
  family = bernoulli()
)
```

### Lagged Predictors for Temporal Precedence

```r
# Create lagged predictors within person
model_data <- data |>
  group_by(participant_id) |>
  arrange(time) |>
  mutate(
    # Lagged values (from previous timepoint)
    predictor_lag = lag(predictor, order_by = time),
    predictor_dev_lag = lag(predictor_dev, order_by = time)
  ) |>
  ungroup()

# Test if t-1 predicts outcome at t (establishes temporal precedence)
model_lagged <- brm(
  outcome ~ predictor_dev_lag_z + predictor_mean_z + (1 | participant_id),
  ...
)
```

## Extracting and Interpreting Results

### Extract Posterior Samples

```r
posterior <- as_draws_df(model)

# Access specific parameter
samples <- posterior$b_predictor_z

# Summary statistics
tibble(
  estimate = median(samples),
  lower_95 = quantile(samples, 0.025),
  upper_95 = quantile(samples, 0.975),
  lower_80 = quantile(samples, 0.10),
  upper_80 = quantile(samples, 0.90),
  prob_negative = mean(samples < 0),
  prob_positive = mean(samples > 0)
)
```

### Odds Ratios (for logistic models)

```r
# Convert log-odds to odds ratios
effects_df <- effects_df |>
  mutate(
    OR = exp(estimate),
    OR_lower = exp(lower_95),
    OR_upper = exp(upper_95)
  )
```

### Posterior Probability of Direction

```r
# P(effect is protective)
prob_protective <- mean(posterior$b_predictor < 0)

# P(effect is harmful)
prob_harmful <- mean(posterior$b_predictor > 0)

# P(|effect| > some threshold)
prob_meaningful <- mean(abs(posterior$b_predictor) > 0.1)
```

### Compare Effect Magnitudes

```r
# Test if within-person effect is larger than between-person
diff <- abs(posterior$b_predictor_dev_z) - abs(posterior$b_predictor_mean_z)
prob_within_larger <- mean(diff > 0)

cat(sprintf("P(|within| > |between|) = %.1f%%\n", 100 * prob_within_larger))
```

## Marginal Effects with marginaleffects

### Average Marginal Effects (AME)

```r
# Change in P(outcome) per 1 unit change in predictor
ame <- avg_slopes(
  model,
  variables = c("predictor1_z", "predictor2_z"),
  type = "response"  # Probability scale
)

print(ame)
```

### Predictions at Specific Values

```r
# Predictions at low (-1 SD), mean (0), and high (+1 SD)
predictions <- predictions(
  model,
  newdata = datagrid(
    model = model,
    predictor_z = c(-1, 0, 1)
  ),
  type = "response",
  re_formula = NA  # Population-level (ignore random effects)
)

as.data.frame(predictions) |>
  select(predictor_z, estimate, conf.low, conf.high)
```

### Marginal Effect Plots

```r
plot_predictions(
  model,
  by = "predictor_z",
  type = "response",
  re_formula = NA
) +
  labs(
    title = "Effect of Predictor on Outcome",
    x = "Predictor (standardized)",
    y = "P(Outcome)"
  ) +
  scale_y_continuous(labels = scales::percent) +
  theme_minimal()
```

### Comparing Slopes Across Models

```r
# Extract AME from multiple models
ame_model1 <- avg_slopes(model1, variables = "predictor_z", type = "response")
ame_model2 <- avg_slopes(model2, variables = "predictor_z", type = "response")

comparison <- bind_rows(
  as.data.frame(ame_model1) |> mutate(model = "Full"),
  as.data.frame(ame_model2) |> mutate(model = "Simple")
)
```

## Model Diagnostics

### Check MCMC Convergence

```r
# Trace plots
mcmc_trace(model, pars = c("b_Intercept", "b_predictor_z"))

# R-hat (should be < 1.01)
summary(model)$fixed$Rhat

# Effective sample size (should be > 400)
summary(model)$fixed$Bulk_ESS
summary(model)$fixed$Tail_ESS
```

### Posterior Predictive Checks

```r
pp_check(model)
pp_check(model, type = "stat", stat = "mean")
pp_check(model, type = "stat_2d", stat = c("mean", "sd"))
```

### Prior-Posterior Comparison

```r
# Requires sample_prior = "yes" in brm()
prior_summary(model)

# Plot prior vs posterior
mcmc_areas(model, pars = "b_predictor_z", prob = 0.95)
```

## tidybayes for Posterior Manipulation

```r
# Extract draws in tidy format
draws <- model |>
  spread_draws(b_predictor1_z, b_predictor2_z) |>
  mutate(
    OR_predictor1 = exp(b_predictor1_z),
    OR_predictor2 = exp(b_predictor2_z)
  )

# Summarize
draws |>
  median_qi(OR_predictor1, OR_predictor2, .width = c(0.80, 0.95))

# Visualize
draws |>
  ggplot(aes(x = OR_predictor1)) +
  stat_halfeye() +
  geom_vline(xintercept = 1, linetype = "dashed") +
  labs(x = "Odds Ratio", y = NULL)
```

## Workflow Summary

1. **Define causal DAG** with dagitty
2. **Validate DAG** against data with `localTests()`
3. **Identify adjustment sets** for target effects
4. **Specify priors** based on domain knowledge
5. **Fit brms model** with random effects for nested data
6. **Check diagnostics** (convergence, PPCs)
7. **Extract posteriors** for inference
8. **Compute marginal effects** on interpretable scale
9. **Visualize** effects with uncertainty

## Anti-Patterns to Avoid

```r
# WRONG: Using contemporaneous predictors when temporal order matters
outcome_t ~ predictor_t  # Shows co-occurrence, not temporal precedence

# CORRECT: Use lagged predictors to establish temporal precedence
outcome_t ~ predictor_t_minus_1

# WRONG: Ignoring clustering
brm(outcome ~ predictor, data = longitudinal_data)

# CORRECT: Account for repeated measures
brm(outcome ~ predictor + (1 | participant_id), data = longitudinal_data)

# WRONG: Interpreting within-person effects from between-person variation
# Using person aggregates when you have time-varying data

# CORRECT: Person-mean centering to separate effects
outcome ~ predictor_mean_z + predictor_dev_z + (1 | id)
```
