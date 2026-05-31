# Step 6 — Robustness Battery in R (Deep Reference)

Goal: a headline coefficient is not credible until you've shown it survives reasonable variations. R has unusually rich tooling here: `modelsummary` for M1–M6 stacks, `clubSandwich` + `fwildclusterboot` for SE families, `ri2` for randomization inference, `bacondecomp` + `HonestDiD` for DID-specific concerns, `robomit` for Oster δ\*.

## Contents

1. Progressive specifications (M1 → M6) with `modelsummary`
2. Alternative cluster levels (multi-way; `clubSandwich`)
3. Wild cluster bootstrap (`fwildclusterboot`)
4. Subsample splits
5. Alternative outcome / treatment definitions
6. Alternative sample restrictions (winsorization, trimming)
7. Placebo — fake timing
8. Placebo — randomization inference (`ri2`)
9. Multiple-testing correction (Romano-Wolf, Westfall-Young)
10. Specification curve (loop + plot)
11. Oster δ\* (`robomit`)
12. TWFE bias diagnosis (`bacondecomp`)
13. HonestDiD parallel-trends sensitivity
14. Influence — leave-one-out, drop top-K Cook's D

---

## 1. Progressive specifications

```r
library(fixest); library(modelsummary)

m1 <- feols(log_wage ~ training, data = df, cluster = ~ firm_id)
m2 <- feols(log_wage ~ training + age + edu, data = df, cluster = ~ firm_id)
m3 <- feols(log_wage ~ training + age + edu + tenure | worker_id, data = df,
            cluster = ~ worker_id)
m4 <- feols(log_wage ~ training + age + edu + tenure | worker_id + year,
            data = df, cluster = ~ worker_id)
m5 <- feols(log_wage ~ training + age + edu + tenure | worker_id + year + region,
            data = df, cluster = ~ worker_id)
m6 <- feols(log_wage ~ training + age + edu + tenure | worker_id + year + industry^year,
            data = df, cluster = ~ worker_id)

modelsummary(
  list("(1)" = m1, "(2)" = m2, "(3)" = m3,
       "(4)" = m4, "(5)" = m5, "(6)" = m6),
  stars = c('*' = .1, '**' = .05, '***' = .01),
  coef_map = c("training" = "Training",
               "age" = "Age", "edu" = "Education", "tenure" = "Tenure"),
  gof_map = list(
    list(raw = "nobs",        clean = "N",        fmt = 0),
    list(raw = "r.squared",   clean = "R²",       fmt = 3),
    list(raw = "adj.r.squared", clean = "Adj. R²", fmt = 3)
  ),
  output = "tables/table_main.tex"
)
```

---

## 2. Alternative cluster levels

```r
library(clubSandwich)

clusters <- c("worker_id", "firm_id", "industry", "state")
out <- map_dfr(clusters, function(cl) {
  fit <- feols(log_wage ~ training | worker_id + year, data = df,
               cluster = as.formula(paste0("~", cl)))
  tibble(cluster = cl,
         estimate = coef(fit)["training"],
         se       = se(fit)["training"],
         t        = estimate / se)
})
print(out)

# Two-way clustering
m_2way <- feols(log_wage ~ training | worker_id + year, data = df,
                cluster = ~ worker_id + firm_id)

# clubSandwich for small-sample correction (CR2)
m_cr2 <- coef_test(lm(log_wage ~ training + age + edu, data = df),
                   vcov = "CR2", cluster = df$state)
```

---

## 3. Wild cluster bootstrap

When clusters < 50, classical CRSE under-cover. `fwildclusterboot` is the gold standard.

```r
library(fwildclusterboot)

m_state <- feols(log_wage ~ training | worker_id + year, data = df,
                 cluster = ~ state)
boot <- boottest(m_state, param = "training", clustid = "state",
                 B = 9999, seed = 42)
summary(boot)

# CI
boot_ci <- boottest(m_state, param = "training", clustid = "state",
                    B = 9999, seed = 42, conf_int = TRUE)
boot_ci$conf_int

# Test specific value
boottest(m_state, param = "training", clustid = "state",
         B = 9999, seed = 42, r = 0.05)        # H0: β = 0.05
```

---

## 4. Subsample splits

```r
splits <- list(
  "Female=0"     = df %>% filter(female == 0),
  "Female=1"     = df %>% filter(female == 1),
  "Young (<40)"  = df %>% filter(age < 40),
  "Old (>=40)"   = df %>% filter(age >= 40),
  "Manuf"        = df %>% filter(industry == "manuf"),
  "Service"      = df %>% filter(industry == "service")
)
sub_fits <- imap(splits, ~ feols(log_wage ~ training | worker_id + year,
                                  data = .x, cluster = ~ worker_id))

modelsummary(sub_fits,
             stars = TRUE,
             coef_map = c("training" = "Training"),
             output = "tables/subsamples.tex")
```

For *testing* heterogeneity (not just estimating subsamples), prefer interaction terms — see `references/07-further-analysis.md`.

---

## 5. Alternative outcome / treatment definitions

```r
# Outcome alternatives
out_y <- map(c("log_wage", "ihs_wage", "wage_w1", "log_wage_real"),
             ~ feols(as.formula(paste(.x, "~ training | worker_id + year")),
                     data = df, cluster = ~ worker_id))
modelsummary(set_names(out_y, c("log_wage","ihs_wage","wage_w1","log_wage_real")),
             stars = TRUE)

# Treatment alternatives
out_t <- map(c("training", "training_ever", "training_hours_log", "training_intense"),
             ~ feols(as.formula(paste("log_wage ~", .x, "| worker_id + year")),
                     data = df, cluster = ~ worker_id))
```

---

## 6. Alternative sample restrictions

```r
# Winsorization sensitivity
out_w <- map(c(0, 1, 5),
             function(p) {
               df_w <- df %>%
                 mutate(log_wage_w = if (p == 0) log_wage else
                        DescTools::Winsorize(log_wage,
                                              probs = c(p/100, 1 - p/100),
                                              na.rm = TRUE))
               feols(log_wage_w ~ training | worker_id + year,
                     data = df_w, cluster = ~ worker_id)
             }) %>%
  set_names(paste0("w", c(0,1,5)))
modelsummary(out_w, stars = TRUE)

# Trim sensitivity
out_t <- map(c(0.01, 0.05),
             function(p) {
               lo <- quantile(df$log_wage, p, na.rm = TRUE)
               hi <- quantile(df$log_wage, 1 - p, na.rm = TRUE)
               feols(log_wage ~ training | worker_id + year,
                     data = df %>% filter(between(log_wage, lo, hi)),
                     cluster = ~ worker_id)
             })
```

---

## 7. Placebo — fake timing

```r
df_placebo <- df %>%
  mutate(fake_first = first_treat - 3,
         fake_post  = year >= fake_first & !is.na(fake_first)) %>%
  filter(year < first_treat)                    # drop real post-period

placebo <- feols(log_wage ~ fake_post | worker_id + year,
                 data = df_placebo, cluster = ~ worker_id)
summary(placebo)                                # expect ≈ 0
```

For event studies: drop real post-period and re-estimate pre-period coefs — all should be ~0.

---

## 8. Randomization inference (`ri2`)

```r
library(ri2)
library(randomizr)

# Permute treatment under sharp null β = 0
ri_out <- conduct_ri(
  formula = log_wage ~ training + age + edu,
  declaration = randomizr::declare_ra(N = nrow(df),
                                       prob = mean(df$training)),
  assignment = "training",
  sharp_hypothesis = 0,
  data = df,
  sims = 1000
)
summary(ri_out)
plot(ri_out) +
  geom_vline(xintercept = ri_out$est$est[2], color = "red", linewidth = 1)
ggsave("figures/ri.pdf", width = 6, height = 4)

# Cluster-level permutation
ri_out_cluster <- conduct_ri(
  formula = log_wage ~ training,
  declaration = randomizr::declare_ra(clusters = df$state,
                                       prob_unit = mean(df$training)),
  assignment = "training",
  sharp_hypothesis = 0,
  data = df,
  sims = 1000
)
```

Manual permutation with `fixest`:

```r
obs_coef <- coef(m6)["training"]
perm_coefs <- replicate(500, {
  df_p <- df %>%
    group_by(worker_id) %>%
    mutate(training_p = sample(training, size = n())) %>%
    ungroup()
  fit <- feols(log_wage ~ training_p | worker_id + year, data = df_p)
  coef(fit)["training_p"]
})
mean(abs(perm_coefs) >= abs(obs_coef))           # permutation p-value

# Plot
ggplot(tibble(b = perm_coefs), aes(b)) +
  geom_histogram(bins = 50, fill = "gray70") +
  geom_vline(xintercept = obs_coef, color = "red", linewidth = 1) +
  labs(x = "Permuted coefficient", y = "Count")
ggsave("figures/permutation.pdf", width = 6, height = 4)
```

---

## 9. Multiple-testing correction

When testing the effect on multiple outcomes (e.g. `employed`, `hours_worked`, `log_wage`), correct for family-wise error.

```r
# Romano-Wolf step-down (manual; or community wrapper)
library(multcomp)
# multcomp focuses on linear hypotheses within a single model;
# Romano-Wolf across models requires bootstrap re-estimation.

# Quick Bonferroni / Holm
ps <- map_dbl(list(m_emp, m_hours, m_wage),
              ~ pvalue(.x)["training"])
p.adjust(ps, method = "holm")
p.adjust(ps, method = "BH")                     # Benjamini-Hochberg FDR

# Westfall-Young — see -multcomp::adjusted-, or use Stata's wyoung via reticulate
```

---

## 10. Specification curve

```r
library(purrr); library(tidyr)

outcomes   <- c("log_wage", "wage_w1")
treatments <- c("training", "training_ever")
controls   <- list(NULL, "age", c("age","edu"), c("age","edu","tenure"))
fes        <- list("worker_id",
                   c("worker_id","year"),
                   c("worker_id","year","industry^year"))

specs <- expand_grid(y = outcomes,
                     t = treatments,
                     c = seq_along(controls),
                     f = seq_along(fes))

run_one <- function(y, t, c, f) {
  rhs <- if (is.null(controls[[c]])) t else paste(c(t, controls[[c]]), collapse = "+")
  fml <- as.formula(paste(y, "~", rhs, "|", paste(fes[[f]], collapse = "+")))
  fit <- feols(fml, data = df, cluster = ~ worker_id)
  tibble(coef = coef(fit)[t], se = se(fit)[t])
}
sc <- specs %>%
  mutate(out = pmap(list(y, t, c, f), run_one)) %>%
  unnest(out) %>%
  arrange(coef) %>%
  mutate(idx = row_number(),
         lower = coef - 1.96*se,
         upper = coef + 1.96*se)

ggplot(sc, aes(idx, coef)) +
  geom_linerange(aes(ymin = lower, ymax = upper), color = "gray70") +
  geom_point(color = "navy") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  labs(x = "Specification (sorted by coefficient)",
       y = "Coefficient on training") +
  theme_classic()
ggsave("figures/spec_curve.pdf", width = 9, height = 4)
```

---

## 11. Oster (2019) δ\*

```r
library(robomit)

# δ test — how big does selection on unobservables need to be?
o_test_out <- o_test(
  y = "log_wage", x = "training",
  con = "age + edu + tenure",                   # observable controls
  id = "worker_id", time = "year",
  data = df, R2max = 1.3 * fitstat(m6, "r2"),
  beta = 0,                                     # treatment effect under H0
  type = "lm"
)
print(o_test_out)
# δ > 1: basic robustness; δ > 2: strong; δ > 4: very strong

# β bound — bias-adjusted estimate under given δ
o_beta_out <- o_beta(
  y = "log_wage", x = "training",
  con = "age + edu + tenure", id = "worker_id", time = "year",
  data = df, R2max = 1.3 * fitstat(m6, "r2"),
  delta = 1, type = "lm"
)
print(o_beta_out)
```

---

## 12. TWFE bias diagnosis

```r
library(bacondecomp)
bacon_out <- bacon(log_wage ~ training,
                   data = df,
                   id_var = "worker_id", time_var = "year")

# Examine the components — negative weights on "Later vs. Earlier Treated"
# are the classic forbidden-comparison problem
print(bacon_out)
sum(bacon_out$weight * bacon_out$estimate)      # = TWFE coefficient

# Plot
ggplot(bacon_out, aes(weight, estimate, color = factor(type))) +
  geom_hline(yintercept = sum(bacon_out$weight * bacon_out$estimate),
             linetype = "dashed", color = "red") +
  geom_point(size = 3) +
  labs(x = "Weight", y = "2×2 DID estimate",
       color = "Comparison type") +
  theme_classic()
ggsave("figures/bacon.pdf", width = 7, height = 4)
```

---

## 13. HonestDiD — Rambachan-Roth (2023)

```r
library(HonestDiD)

# After event study (es is a feols object on i(rel_time, ref=-1)):
betas <- coef(es)
sigma <- vcov(es)

# Index — need numPrePeriods + numPostPeriods (excluding the omitted base = -1)
# (the package's vignette walks through extracting these correctly)

# Smoothness restriction — bound on second derivative of pre-trend
honest_smooth <- createSensitivityResults(
  betahat        = betas,
  sigma          = sigma,
  numPrePeriods  = 5,
  numPostPeriods = 5,
  Mbarvec        = seq(0, 0.5, by = 0.05),
  method         = "FLCI"
)
createSensitivityPlot(honest_smooth,
                      originalResults = honest_smooth$mainResult)
ggsave("figures/honestdid_smooth.pdf", width = 6, height = 4)

# Relative-magnitudes restriction
honest_rm <- createSensitivityResults_relativeMagnitudes(
  betahat = betas, sigma = sigma,
  numPrePeriods = 5, numPostPeriods = 5,
  Mbarvec = c(0.5, 1, 1.5, 2),
  bound = "deviation from parallel trends"
)
createSensitivityPlot_relativeMagnitudes(honest_rm,
                                          originalResults = honest_rm$mainResult)
```

---

## 14. Influence — leave-one-out

```r
units <- unique(df$worker_id)
sample_units <- sample(units, min(500, length(units)))

obs_coef <- coef(m4)["training"]

loo_coefs <- map_dbl(sample_units, function(u) {
  fit <- feols(log_wage ~ training | worker_id + year,
               data = df %>% filter(worker_id != u),
               cluster = ~ worker_id)
  coef(fit)["training"]
})

ggplot(tibble(b = loo_coefs), aes(b)) +
  geom_histogram(bins = 50, fill = "gray70") +
  geom_vline(xintercept = obs_coef, color = "red", linewidth = 1) +
  labs(x = "LOO coefficient", y = "Count",
       title = "Leave-one-unit-out distribution")
ggsave("figures/loo.pdf", width = 6, height = 4)

# Drop top 1% Cook's D and re-fit
ols <- lm(log_wage ~ training + age + edu + tenure, data = df)
cd  <- cooks.distance(ols)
cutoff <- quantile(cd, 0.99, na.rm = TRUE)
m_clean <- feols(log_wage ~ training | worker_id + year,
                 data = df %>% slice(which(cd <= cutoff)),
                 cluster = ~ worker_id)
modelsummary(list("Full" = m4, "Drop top 1% Cook" = m_clean), stars = TRUE)
```

---

## What a strong robustness appendix contains

A paper that survives review should include, at minimum:

1. **Progressive specs** (M1–M6) → `tables/table_main.tex` via `modelsummary`
2. **Cluster sensitivity** at 3–4 levels + `fwildclusterboot::boottest` if few clusters
3. **Placebo (fake timing)** event-study estimates ≈ 0 in pre-period
4. **Randomization inference** distribution + observed coefficient
5. **Specification curve** of all valid combinations
6. **Oster δ\*** computed via `robomit::o_test`
7. **Subsample splits** at 4–6 pre-defined dimensions
8. **Alternative outcome / treatment definitions** (≥ 2–3 each)
9. For DID: `bacondecomp` + `HonestDiD` plots
10. For IV: KP rk Wald, AR weak-IV-robust CI, Hansen J overid
11. For RD: bandwidth sensitivity (×0.5/1/2), `rddensity`, covariate smoothness
12. For PSM/IPW: `cobalt::love.plot` SMDs before/after, common-support trimmed re-estimate, entropy-balanced version
