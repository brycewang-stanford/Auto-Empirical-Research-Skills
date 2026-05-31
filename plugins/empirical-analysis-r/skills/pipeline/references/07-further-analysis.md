# Step 7 — Further Analysis in R (Deep Reference)

Goal: turn the ATT into a story. Three questions:

1. **Heterogeneity**: For whom is the effect strongest?
2. **Mechanism**: Through what channel?
3. **Moderation / Mediation**: Under what conditions?

R's `marginaleffects` ecosystem + `mediation` + `lavaan` + `grf` makes this layer particularly fluent.

## Contents

1. Heterogeneity via formula interactions + Wald test
2. Subgroup estimation + `anova` / `car::linearHypothesis`
3. Triple difference (DDD)
4. Continuous moderator via `marginaleffects::plot_slopes`
5. Subgroup event studies
6. Outcome ladder
7. Mediation — Imai (`mediation::mediate`) + sensitivity
8. Mediation — `lavaan` SEM with bootstrap
9. Moderated mediation
10. Dose-response (splines + `marginaleffects::plot_predictions`)
11. CATE via `grf::causal_forest`
12. Spillover / interference

---

## 1. Heterogeneity via interaction

```r
library(fixest)
library(marginaleffects)

# Binary moderator
het <- feols(log_wage ~ training * female + age + edu | worker_id + year,
             data = df, cluster = ~ worker_id)
summary(het)
# The training:femaleTRUE coefficient is Δ_ATT (female - male).

# margins make by-group effects explicit
avg_slopes(het, variables = "training", by = "female")

# Visualize
plot_slopes(het, variables = "training", condition = "female") +
  labs(x = "Female", y = "Marginal effect of training",
       title = "Marginal effect by gender")
ggsave("figures/het_gender.pdf", width = 6, height = 4)

# Continuous moderator
het_c <- feols(log_wage ~ training * tenure + age + edu | worker_id + year,
               data = df, cluster = ~ worker_id)
plot_slopes(het_c, variables = "training",
            condition = list(tenure = seq(0, 20, by = 1))) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  labs(x = "Tenure (years)", y = "Marginal effect of training",
       title = "How the effect varies with tenure")
ggsave("figures/het_tenure.pdf", width = 6, height = 4)

# Two moderators
het_2 <- feols(log_wage ~ training * female * tenure + age + edu |
               worker_id + year, data = df, cluster = ~ worker_id)
plot_slopes(het_2, variables = "training",
            condition = list(tenure = seq(0, 20, 2), female = c(FALSE, TRUE)))
```

---

## 2. Subgroup estimation + Wald test

When you'd rather run separate regressions per subgroup but still need a formal test:

```r
library(car)

m_male   <- feols(log_wage ~ training + age + edu | worker_id + year,
                  data = df %>% filter(female == 0), cluster = ~ worker_id)
m_female <- feols(log_wage ~ training + age + edu | worker_id + year,
                  data = df %>% filter(female == 1), cluster = ~ worker_id)

# Approximate Wald (independent samples)
b1 <- coef(m_male  )["training"]; se1 <- se(m_male)  ["training"]
b2 <- coef(m_female)["training"]; se2 <- se(m_female)["training"]
delta <- b1 - b2
se    <- sqrt(se1^2 + se2^2)
z     <- delta / se
p     <- 2 * (1 - pnorm(abs(z)))
cat(sprintf("Δ = %.4f   SE = %.4f   z = %.2f   p = %.3f\n", delta, se, z, p))

# Exact — fit a single pooled model with interaction and test the interaction
m_pool <- feols(log_wage ~ training * female + age + edu | worker_id + year,
                data = df, cluster = ~ worker_id)
linearHypothesis(m_pool, "training:femaleTRUE = 0")
```

---

## 3. Triple difference (DDD)

```r
ddd <- feols(log_wage ~ treated * post * high_exposure + age + edu |
             worker_id + year, data = df, cluster = ~ firm_id)
summary(ddd)
# Coefficient on treated:post:high_exposure = differential ATT

# Margins across the third dimension
avg_slopes(ddd, variables = "treated", by = "high_exposure")
```

---

## 4. Continuous moderator via `marginaleffects`

```r
library(marginaleffects)

m <- feols(log_wage ~ training * firm_size + age + edu | worker_id + year,
           data = df, cluster = ~ firm_id)

# Marginal effect along moderator support
fs_seq <- seq(quantile(df$firm_size, 0.05, na.rm = TRUE),
              quantile(df$firm_size, 0.95, na.rm = TRUE), length.out = 40)

plot_slopes(m, variables = "training",
            condition = list(firm_size = fs_seq)) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_rug(data = df, aes(x = firm_size), inherit.aes = FALSE, alpha = 0.1) +
  labs(x = "Firm size", y = "Marginal effect of training")
ggsave("figures/moderation_firmsize.pdf", width = 7, height = 4)
```

---

## 5. Subgroup event studies

```r
es_by_group <- map(c(0, 1), function(g) {
  df_g <- df %>% filter(female == g)
  feols(log_wage ~ i(rel_time, ref = -1) | worker_id + year,
        data = df_g %>% filter(!is.na(first_treat)),
        cluster = ~ worker_id)
}) %>% set_names(c("Male","Female"))

# Pull coefficients into a tibble for faceted plotting
es_df <- imap_dfr(es_by_group, function(fit, name) {
  broom::tidy(fit, conf.int = TRUE) %>%
    filter(str_detect(term, "rel_time::")) %>%
    mutate(k = as.integer(str_extract(term, "-?\\d+")),
           group = name)
})

ggplot(es_df, aes(k, estimate, color = group)) +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_vline(xintercept = -0.5, linetype = "dashed", color = "red") +
  geom_line() + geom_point() +
  geom_errorbar(aes(ymin = conf.low, ymax = conf.high), width = 0.1) +
  facet_wrap(~ group) +
  labs(x = "Years relative to treatment", y = "Coefficient (ATT)") +
  theme_classic()
ggsave("figures/es_by_gender.pdf", width = 10, height = 4)
```

---

## 6. Outcome ladder

```r
outcomes <- c("hours_worked", "productivity", "log_wage")
ladder <- map(outcomes, ~ feols(as.formula(paste(.x, "~ training | worker_id + year")),
                                 data = df, cluster = ~ worker_id)) %>%
  set_names(outcomes)

modelsummary(ladder, stars = TRUE,
             coef_map = c("training" = "Training"),
             output = "tables/outcome_ladder.tex")

# Visual coefplot
library(broom)
ladder_df <- imap_dfr(ladder, function(fit, name) {
  broom::tidy(fit, conf.int = TRUE) %>%
    filter(term == "training") %>%
    mutate(outcome = name)
})
ggplot(ladder_df, aes(estimate, outcome)) +
  geom_point(size = 3, color = "navy") +
  geom_errorbar(aes(xmin = conf.low, xmax = conf.high),
                width = 0.2, color = "navy") +
  geom_vline(xintercept = 0, linetype = "dashed") +
  labs(x = "ATT", y = "", title = "Outcome ladder") +
  theme_classic()
ggsave("figures/outcome_ladder.pdf", width = 6, height = 3)
```

---

## 7. Mediation — Imai et al. (2010) via `mediation::mediate`

The gold standard for causal mediation in R. Includes sensitivity analysis for unmeasured M-Y confounding.

```r
library(mediation)

# Step 1: fit M ~ T + X
fit_M <- lm(hours_worked ~ training + age + edu, data = df)

# Step 2: fit Y ~ T + M + X
fit_Y <- lm(log_wage ~ training + hours_worked + age + edu, data = df)

# Step 3: mediate
med <- mediate(fit_M, fit_Y,
               treat = "training", mediator = "hours_worked",
               boot = TRUE, sims = 1000, seed = 42)
summary(med)                                    # ACME, ADE, total, % mediated
plot(med)                                       # coefficient plot

# Sensitivity to unmeasured M-Y confounding (Imai et al. sensitivity)
medsens <- medsens(med, rho.by = 0.05,
                   effect.type = "indirect", sims = 500)
summary(medsens)
plot(medsens)                                   # at what ρ does ACME cross 0?
ggsave("figures/mediation_sens.pdf", width = 7, height = 4)

# For non-linear M or Y (e.g. logit selection into M), just use glm:
fit_M_logit <- glm(M_binary ~ training + age + edu, data = df, family = binomial)
fit_Y       <- lm(log_wage ~ training + M_binary + age + edu, data = df)
med_nl <- mediate(fit_M_logit, fit_Y, treat = "training", mediator = "M_binary",
                  boot = TRUE, sims = 1000)
```

---

## 8. SEM-based mediation with bootstrap

```r
library(lavaan)

mod <- '
  # Outcome equation
  log_wage    ~ b * hours_worked + c_prime * training + age + edu
  # Mediator equation
  hours_worked ~ a * training + age + edu

  # Defined parameters
  indirect := a * b
  total    := a * b + c_prime
  pct_med  := (a * b) / (a * b + c_prime)
'

fit <- sem(mod, data = df,
           se = "bootstrap", bootstrap = 1000,
           fixed.x = FALSE)
summary(fit, standardized = TRUE, fit.measures = TRUE, ci = TRUE)
parameterEstimates(fit, standardized = TRUE, ci = TRUE,
                   boot.ci.type = "bca.simple") %>%
  filter(op %in% c(":=", "~")) %>%
  select(lhs, rhs, est, se, pvalue, ci.lower, ci.upper)
```

---

## 9. Moderated mediation

Test whether the indirect effect differs across levels of a moderator.

```r
# Multi-group mediation in lavaan
mod_group <- '
  log_wage    ~ c(b1, b2) * hours_worked + c(c1, c2) * training + age + edu
  hours_worked ~ c(a1, a2) * training + age + edu

  # Group-specific indirect effects
  indirect_g1 := a1 * b1                 # skilled = 0
  indirect_g2 := a2 * b2                 # skilled = 1
  # Difference
  index_mm   := indirect_g2 - indirect_g1
'
fit_mm <- sem(mod_group, data = df, group = "skilled",
              se = "bootstrap", bootstrap = 1000)
parameterEstimates(fit_mm) %>% filter(op == ":=")

# Or split via mediation::mediate and compare bootstrap CIs manually
```

---

## 10. Dose-response (continuous treatment)

```r
library(splines)
library(marginaleffects)

# Natural spline on dose
dr <- feols(log_wage ~ ns(training_hours, df = 4) + age + edu |
            worker_id + year, data = df, cluster = ~ worker_id)

# Predicted Y vs. dose (holding covariates at means)
plot_predictions(dr, condition = "training_hours") +
  labs(x = "Training hours", y = "Predicted log wage")
ggsave("figures/dose_response_spline.pdf", width = 7, height = 4)

# Decile-binned piecewise
df$dose_dec <- ntile(df$training_hours, 10)
dr_dec <- feols(log_wage ~ i(dose_dec, ref = 1) + age + edu |
                worker_id + year, data = df, cluster = ~ worker_id)
iplot(dr_dec, xlab = "Dose decile (ref = 1)",
      ylab = "Coefficient (vs. bottom decile)")
pdf("figures/dose_decile.pdf", width = 7, height = 4); iplot(dr_dec); dev.off()
```

---

## 11. CATE via `grf::causal_forest`

High-dim heterogeneity — let the forest find the moderators.

```r
library(grf)

X <- df %>% select(age, edu, tenure, firm_size) %>% as.matrix()
cf <- causal_forest(X = X, Y = df$log_wage, W = df$training,
                    num.trees = 2000, min.node.size = 5,
                    clusters = df$firm_id, seed = 42)

# ATE
ate <- average_treatment_effect(cf, target.sample = "all")
ate_overlap <- average_treatment_effect(cf, target.sample = "overlap")

# CATE per unit
df$tau_hat <- predict(cf)$predictions

# Variable importance
varimp <- variable_importance(cf)
names(varimp) <- colnames(X)
sort(varimp, decreasing = TRUE)

# Test for heterogeneity (GRF calibration test)
test_calibration(cf)

# Best linear projection of CATE onto covariates
blp <- best_linear_projection(cf, X)
print(blp)

# Plot CATE by a moderator
ggplot(df, aes(tenure, tau_hat)) +
  geom_point(alpha = 0.2) +
  geom_smooth(method = "loess", se = TRUE, color = "navy") +
  geom_hline(yintercept = ate[1], linetype = "dashed") +
  labs(x = "Tenure", y = "Estimated CATE",
       title = "Heterogeneity along tenure")
ggsave("figures/cate_tenure.pdf", width = 7, height = 4)

# Heatmap across two dimensions
grid <- expand_grid(age_g = seq(25, 60, by = 2),
                    tenure_g = seq(0, 20, by = 1))
grid$edu_g <- median(df$edu); grid$firm_size_g <- median(df$firm_size)
grid$tau <- predict(cf, newdata = as.matrix(grid %>%
                   select(age_g, edu_g, tenure_g, firm_size_g)))$predictions
ggplot(grid, aes(age_g, tenure_g, fill = tau)) +
  geom_tile() +
  scale_fill_gradient2(low = "darkred", mid = "white", high = "navy",
                       midpoint = 0) +
  labs(x = "Age", y = "Tenure", fill = "CATE")
ggsave("figures/cate_heatmap.pdf", width = 7, height = 5)
```

---

## 12. Spillover / interference

```r
# Exposure variable: share of treated peers in market-year
df <- df %>%
  group_by(market, year) %>%
  mutate(share_treated_peers = mean(training, na.rm = TRUE)) %>%
  ungroup()

# Main spec with spillover control
spill <- feols(log_wage ~ training + share_treated_peers + age + edu |
               worker_id + year, data = df, cluster = ~ market)
summary(spill)

# Donut-style exclusion (drop controls close to treated units)
df_donut <- df %>%
  filter(!(training == 0 & min_distance_to_treated < 5))
feols(log_wage ~ training + age + edu | worker_id + year,
      data = df_donut, cluster = ~ firm_id)

# Cluster-level randomization — estimate at cluster mean
df_cl <- df %>%
  group_by(cluster_id) %>%
  summarise(across(c(log_wage, training, age, edu), mean, na.rm = TRUE))
feols(log_wage ~ training + age + edu, data = df_cl, vcov = "hetero")
```

---

## What Step 7 typically produces

A solid further-analysis section has, at minimum:

1. **One heterogeneity table** with interaction estimates along 3–5 pre-specified moderators
2. **One `plot_slopes` figure** showing marginal effect along a continuous moderator
3. **One outcome-ladder table** + coefplot
4. **One mediation result** with bootstrap CI + Imai sensitivity plot
5. **One DDD or moderated model** if design supports it
6. If continuous treatment: **one dose-response plot** (spline or decile)
7. **CATE plot** from `grf::causal_forest` + variable-importance table
8. If SUTVA plausibly violated: **one spillover robustness** estimate

All artifacts saved to `tables/` and `figures/` with consistent naming for Step 8 to assemble.
