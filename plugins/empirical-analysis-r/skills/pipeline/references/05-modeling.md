# Step 5 — Empirical Modeling in R (Deep Reference)

Goal: estimate the causal / predictive relationship with the right R command for the identification strategy. `fixest` is the workhorse (panel, IV, GLM, all under one umbrella, multi-way clusters, multi-FE, fast). For specialized estimators, R has the deepest open-source ecosystem of any language for econometrics.

## Contents

1. OLS, robust / cluster / multi-way SEs (`feols`, `lm` + `sandwich` + `clubSandwich`)
2. Panel — within / FD / RE / between (`feols`, `plm`)
3. Binary / count / GLM (`feglm`, `fepois`, `glm`)
4. IV — `feols(... | endog ~ z)`, `AER::ivreg`, `ivmodel`
5. Difference-in-differences — `feols`, `did::att_gt`, `fixest::sunab`, `didimputation`, `synthdid`, `DIDmultiplegtDYN`
6. Regression discontinuity — `rdrobust`, `rddensity`, `rdmulti`
7. Synthetic control — `Synth`, `gsynth`, `tidysynth`, `synthdid`
8. Matching & weighting — `MatchIt`, `WeightIt`, `cobalt`, `ebal`, `cem`
9. ML causal — `grf::causal_forest`, `DoubleML`
10. Heckman selection
11. Quantile regression (`quantreg`)
12. SEM / mediation — `lavaan`, `mediation`

---

## 1. OLS

```r
library(fixest)
library(sandwich); library(lmtest); library(clubSandwich)

# Default — feols
ols <- feols(log_wage ~ training + age + edu + tenure, data = df,
             cluster = ~ firm_id)
summary(ols)

# Multi-way clustering
ols2 <- feols(log_wage ~ training + age + edu + tenure, data = df,
              cluster = ~ worker_id + firm_id)

# Robust SE families via lm + sandwich
fit <- lm(log_wage ~ training + age + edu + tenure, data = df)
coeftest(fit, vcov. = vcovHC(fit, type = "HC3"))     # White / Davidson-MacKinnon
coeftest(fit, vcov. = vcovCL(fit, cluster = ~ firm_id))
# Or clubSandwich (small-sample cluster correction, recommended)
coef_test(fit, vcov = "CR2", cluster = df$firm_id)

# Bootstrap
library(boot)
boot_fit <- Boot(fit, R = 999, ncores = 4)
confint(boot_fit, type = "perc")

# Tests on coefficients
library(car)
linearHypothesis(fit, "training = 0.05")
linearHypothesis(fit, c("training = 0", "age = 0"))
```

### `marginaleffects` for any post-estimation query

```r
library(marginaleffects)
avg_slopes(ols)                                # average marginal effect of every var
avg_slopes(ols, variables = "training")
avg_predictions(ols, by = "training")
plot_slopes(ols, variables = "training",
            condition = list(tenure = seq(0, 20, 2)))
```

---

## 2. Panel data

`fixest::feols` is the modern primary; `plm` is the alternative for RE / FD / between.

```r
library(fixest)

# Two-way FE
fe <- feols(log_wage ~ training + age + edu + tenure | worker_id + year,
            data = df, cluster = ~ worker_id)
summary(fe)

# Multi-way clustering
fe_mw <- feols(log_wage ~ training | worker_id + year,
               data = df, cluster = ~ worker_id + firm_id)

# High-dim interaction FE
fe_hd <- feols(log_wage ~ training | worker_id + industry^year,
               data = df, cluster = ~ firm_id)

# Save residuals / fitted values
df$resid_fe <- residuals(fe)
df$fitted_fe <- fitted(fe)

# Multiple LHS (one fit per outcome)
multi <- feols(c(log_wage, hours_worked) ~ training | worker_id + year,
               data = df, cluster = ~ worker_id)
```

### `plm` for RE / FD / between

```r
library(plm)
pdata <- pdata.frame(df, index = c("worker_id","year"))

# Random effects
re <- plm(log_wage ~ training + age + edu, data = pdata, model = "random")

# Between
be <- plm(log_wage ~ training + age + edu, data = pdata, model = "between")

# First differences
fd <- plm(log_wage ~ training + age + edu, data = pdata, model = "fd")

# All clustered
coeftest(re, vcov. = vcovHC(re, type = "HC1", cluster = "group"))
```

---

## 3. Binary / count / GLM

```r
# Logit + AME via marginaleffects
logit <- glm(employed ~ training + age + edu, data = df, family = binomial)
avg_slopes(logit)                              # AME on every var
avg_slopes(logit, variables = "training", by = "female")

# Logit with HD FE — feglm
logit_fe <- feglm(employed ~ training + age + edu | firm_id + year,
                  data = df, family = binomial("logit"),
                  cluster = ~ firm_id)
avg_slopes(logit_fe)

# Probit
probit <- glm(employed ~ training + age + edu, data = df,
              family = binomial(link = "probit"))

# Poisson + HD FE — fepois
pois <- fepois(citations ~ training + age | firm_id + year,
               data = df, cluster = ~ firm_id)

# Negative binomial (overdispersion)
library(MASS)
nb <- glm.nb(citations ~ training + age + edu, data = df)
AIC(pois, nb)                                  # compare

# Zero-inflated count
library(pscl)
zinb <- zeroinfl(citations ~ training + age | training, data = df, dist = "negbin")

# Ordered logit
library(MASS)
olog <- polr(rating ~ training + age + edu, data = df, method = "logistic", Hess = TRUE)

# Multinomial logit
library(nnet)
mlog <- multinom(job_choice ~ training + age + edu, data = df)
```

---

## 4. Instrumental variables

`fixest::feols` syntax: `Y ~ exog | FE | endog ~ z`.

```r
library(fixest)

iv <- feols(log_wage ~ age + edu | worker_id + year |
            training ~ draft_lottery + z2,
            data = df, cluster = ~ firm_id)
summary(iv, stage = 1)                         # first-stage
summary(iv, stage = 2)
fitstat(iv, ~ ivf + ivf1 + ivwald + sargan + endo)

# AER::ivreg — alternative
library(AER)
iv_aer <- ivreg(log_wage ~ training + age + edu |
                draft_lottery + z2 + age + edu, data = df)
summary(iv_aer, vcov. = sandwich, diagnostics = TRUE)

# ivreg::ivreg (tidymodels-friendly successor)
library(ivreg)
iv2 <- ivreg(log_wage ~ training + age + edu |
             . - training + draft_lottery + z2, data = df)
summary(iv2, vcov. = sandwich)

# Anderson-Rubin / weak-IV-robust
library(ivmodel)
ivm <- ivmodel(Y = df$log_wage, D = df$training,
               Z = df %>% select(draft_lottery, z2) %>% as.matrix(),
               X = df %>% select(age, edu) %>% as.matrix())
AR.test(ivm)
CLR(ivm)
```

### Bartik / shift-share

```r
# Construct the instrument:
# bartik_z = sum_k(industry_share_ik * national_growth_k)
df$bartik_z <- as.numeric(industry_shares %*% national_growth)
iv_bartik <- feols(log_wage ~ age + edu | worker_id + year |
                   training ~ bartik_z, data = df, cluster = ~ firm_id)
```

---

## 5. Difference-in-differences

### 5.1 2×2 DID

```r
library(fixest)
did22 <- feols(log_wage ~ i(treated, post, ref = 0) + age + edu | worker_id + year,
               data = df, cluster = ~ worker_id)
# i(treated, post, ref=0) creates the treated × post interaction with control = reference.
```

### 5.2 TWFE — only with simultaneous treatment

```r
twfe <- feols(log_wage ~ I(treated * post) | worker_id + year,
              data = df, cluster = ~ worker_id)
```

### 5.3 Event study (dynamic DID)

```r
es <- feols(log_wage ~ i(rel_time, ref = -1) | worker_id + year,
            data = df %>% filter(!is.na(first_treat)),
            cluster = ~ worker_id)
iplot(es,
      xlab = "Years relative to treatment",
      main = "Event study", drop = "[-99]")    # drop -99 placeholder if you have one
```

### 5.4 Staggered DID — modern estimators

```r
# --- Callaway–Sant'Anna (2021) ---
library(did)
cs <- att_gt(yname = "log_wage", tname = "year", idname = "worker_id",
             gname = "first_treat", data = df,
             control_group = "nevertreated",     # or "notyettreated"
             est_method = "dr",                  # doubly robust
             clustervars = "firm_id",
             panel = TRUE)
ggdid(cs)                                       # event-study plot

# Aggregations
agg_simple   <- aggte(cs, type = "simple")      # overall ATT
agg_event    <- aggte(cs, type = "dynamic")     # event study
agg_group    <- aggte(cs, type = "group")       # ATT(g)
agg_calendar <- aggte(cs, type = "calendar")    # ATT(t)
ggdid(agg_event)

# --- Sun & Abraham (2021) — fixest::sunab ---
sa <- feols(log_wage ~ sunab(first_treat, year) | worker_id + year,
            data = df, cluster = ~ worker_id)
iplot(sa, sub.title = "Sun-Abraham (2021)")
summary(sa, agg = "att")                        # aggregate ATT

# --- Borusyak–Jaravel–Spiess (2024) imputation ---
library(didimputation)
bjs <- did_imputation(data = df, yname = "log_wage", gname = "first_treat",
                      tname = "year", idname = "worker_id",
                      horizon = 0:5, pretrends = -5:-1,
                      cluster_var = "worker_id")
print(bjs)

# --- Synthetic DID (Arkhangelsky et al. 2021) ---
library(synthdid)
setup <- panel.matrices(df, unit = "worker_id", time = "year",
                        outcome = "log_wage", treatment = "training")
sdid_fit <- synthdid_estimate(setup$Y, setup$N0, setup$T0)
plot(sdid_fit)
summary(sdid_fit)
sdid_se <- sqrt(synthdid_se(sdid_fit, method = "placebo")^2)

# --- de Chaisemartin & D'Haultfœuille ---
library(DIDmultiplegtDYN)
dcdh <- did_multiplegt_dyn(df = df,
                           outcome = "log_wage",
                           group = "worker_id",
                           time = "year",
                           treatment = "training",
                           effects = 5,
                           placebo = 3,
                           cluster = "worker_id")
```

### 5.5 Goodman-Bacon decomposition (TWFE bias diagnosis)

```r
library(bacondecomp)
bacon_out <- bacon(log_wage ~ training,
                   data = df, id_var = "worker_id", time_var = "year")
ggplot(bacon_out, aes(weight, estimate, color = factor(type))) +
  geom_point(size = 2) +
  geom_hline(yintercept = sum(bacon_out$weight * bacon_out$estimate),
             linetype = "dashed") +
  labs(x = "Weight", y = "Estimate", color = "Comparison type")
ggsave("figures/bacon.pdf", width = 7, height = 4)
```

### 5.6 HonestDiD — Rambachan-Roth (2023)

```r
library(HonestDiD)
# After event study, extract betas + Sigma:
betas <- coef(es)
sigma <- vcov(es)

# Index pre / post coefficients (depends on your model)
honest_smooth <- createSensitivityResults(betahat = betas,
                                          sigma   = sigma,
                                          numPrePeriods = 5,
                                          numPostPeriods = 5,
                                          Mbarvec = seq(0, 0.5, by = 0.05),
                                          method = "FLCI")
createSensitivityPlot(honest_smooth, originalResults = honest_smooth$mainResult)
ggsave("figures/honestdid.pdf", width = 6, height = 4)
```

### 5.7 Continuous treatment

```r
# Decile bins
df$dose <- ntile(df$training_hours, 10)
dr <- feols(log_wage ~ i(dose, ref = 1) | worker_id + year,
            data = df, cluster = ~ worker_id)
iplot(dr)

# Continuous DID — see -did_continuous- (community R port)
```

---

## 6. Regression discontinuity

```r
library(rdrobust); library(rddensity); library(rdmulti)

# Sharp RD
rd <- rdrobust(y = df$outcome, x = df$running_var, c = 0,
               kernel = "triangular", bwselect = "mserd",
               vce = "hc1")
summary(rd)
rdplot(y = df$outcome, x = df$running_var, c = 0,
       p = 1, binselect = "esmv",
       title = "RD plot",
       y.label = "Outcome", x.label = "Running variable")

# Bandwidth alone
rdbwselect(y = df$outcome, x = df$running_var, c = 0, bwselect = "mserd")

# Fuzzy RD
rd_fuzzy <- rdrobust(y = df$outcome, x = df$running_var, c = 0,
                     fuzzy = df$treatment)

# Kink RD (slope discontinuity)
rd_kink <- rdrobust(y = df$outcome, x = df$running_var, c = 0, deriv = 1)

# Multi-cutoff
rdmc(y = df$outcome, x = df$running_var, c = df$cutoff_var)

# Density (manipulation) test
rdd <- rddensity(X = df$running_var, c = 0)
summary(rdd)
plot(rdd)

# Covariate smoothness placebos
for (cv in c("age","edu","female")) {
  r <- rdrobust(y = df[[cv]], x = df$running_var, c = 0)
  cat(cv, "  coef =", r$coef[1, "Robust"], "  p =", r$pv[3, "Robust"], "\n")
}

# Bandwidth sensitivity
for (mult in c(0.5, 0.75, 1.0, 1.25, 1.5)) {
  h <- mult * rd$bws[1, "left"]
  r <- rdrobust(y = df$outcome, x = df$running_var, c = 0, h = h)
  cat("h =", round(h,3), "  coef =", r$coef[1, "Robust"], "\n")
}

# Local randomization
library(rdlocrand)
rdrandinf(y = df$outcome, x = df$running_var, cutoff = 0,
          wl = -0.5, wr = 0.5, seed = 42)
```

---

## 7. Synthetic control

```r
# --- tidysynth — modern tidyverse interface ---
library(tidysynth)

sc <- df %>%
  synthetic_control(outcome = log_wage, unit = country, time = year,
                    i_unit = "treated_country", i_time = 2001, generate_placebos = TRUE) %>%
  generate_predictor(time_window = 1990:2000,
                     gdp = mean(gdp, na.rm = TRUE),
                     trade = mean(trade, na.rm = TRUE)) %>%
  generate_predictor(time_window = 1985, gdp_85 = gdp) %>%
  generate_predictor(time_window = 1988, gdp_88 = gdp) %>%
  generate_weights(optimization_window = 1985:2000) %>%
  generate_control()

sc %>% plot_trends()
sc %>% plot_differences()
sc %>% plot_weights()
sc %>% plot_placebos()
sc %>% grab_significance()                     # placebo p-values

# --- gsynth — generalized SC with multiple treated, IFE ---
library(gsynth)
gs <- gsynth(log_wage ~ training, data = df,
             index = c("worker_id", "year"),
             force = "two-way", CV = TRUE, r = c(0, 5),
             se = TRUE, inference = "parametric", nboots = 500,
             parallel = FALSE)
plot(gs, type = "gap")
plot(gs, type = "counterfactual")

# --- Synth (classic Abadie–Diamond–Hainmueller) ---
library(Synth)
# verbose dataprep + synth() call; see Synth vignette.

# --- synthdid (Arkhangelsky et al. 2021) — already in §5.4 ---
```

---

## 8. Matching & weighting

### MatchIt (PSM, exact, mahalanobis, full, optimal)

```r
library(MatchIt)
library(cobalt)

# Nearest-neighbor 1:1 PSM
m_out <- matchit(training ~ age + edu + tenure + female,
                 data = df, method = "nearest", ratio = 1,
                 caliper = 0.05, replace = FALSE,
                 distance = "glm")
summary(m_out)
matched_df <- match.data(m_out)

# Balance check
bal.tab(m_out, un = TRUE, m.threshold = 0.1)
love.plot(m_out, threshold = 0.1, abs = TRUE)
ggsave("figures/loveplot.pdf", width = 6, height = 4)

# ATT on matched sample
fit_att <- feols(log_wage ~ training + age + edu + tenure + female,
                 data = matched_df, weights = matched_df$weights,
                 cluster = ~ subclass)
summary(fit_att)

# Other methods:
m_cem    <- matchit(training ~ age + edu + tenure, data = df, method = "cem")
m_full   <- matchit(training ~ age + edu + tenure, data = df, method = "full")
m_optimal<- matchit(training ~ age + edu + tenure, data = df, method = "optimal", ratio = 2)
```

### WeightIt (IPW / IPWRA / AIPW)

```r
library(WeightIt)
library(cobalt)

w_out <- weightit(training ~ age + edu + tenure + female,
                  data = df, method = "ps", estimand = "ATT")
df$ipw_weight <- w_out$weights

bal.tab(w_out, un = TRUE)
love.plot(w_out, threshold = 0.1)

# Outcome regression with weights
fit_ipw <- feols(log_wage ~ training + age + edu, data = df,
                 weights = ~ ipw_weight, cluster = ~ firm_id)
```

### Entropy balancing

```r
library(ebal)
eb_out <- ebalance(Treatment = df$training,
                   X = df %>% select(age, edu, tenure, female) %>% as.matrix())
df$ebal_weight <- 1
df$ebal_weight[df$training == 0] <- eb_out$w
fit_ebal <- feols(log_wage ~ training, data = df, weights = ~ ebal_weight,
                  cluster = ~ firm_id)

# Or via WeightIt
w_eb <- weightit(training ~ age + edu + tenure, data = df,
                 method = "ebal", estimand = "ATT")
```

---

## 9. ML causal

```r
# Causal forest — grf
library(grf)
X <- df %>% select(age, edu, tenure, firm_size) %>% as.matrix()
cf <- causal_forest(X = X, Y = df$log_wage, W = df$training,
                    num.trees = 2000, min.node.size = 5)

# ATE / CATE
ate <- average_treatment_effect(cf, target.sample = "all")
df$tau_hat <- predict(cf)$predictions
varimp <- variable_importance(cf)
test_calibration(cf)                            # GRF test for heterogeneity

# Best-linear-projection
blp <- best_linear_projection(cf, X)

# Plot CATE by moderator
library(ggplot2)
ggplot(df, aes(tenure, tau_hat)) +
  geom_smooth(method = "loess", se = TRUE, color = "navy") +
  geom_hline(yintercept = ate[1], linetype = "dashed") +
  labs(x = "Tenure", y = "Estimated CATE")

# DoubleML
library(DoubleML)
library(mlr3); library(mlr3learners)

dml_data <- DoubleMLData$new(df,
                             y_col = "log_wage",
                             d_cols = "training",
                             x_cols = c("age","edu","tenure","firm_size"))

learner_g <- lrn("regr.ranger")
learner_m <- lrn("regr.ranger")
dml <- DoubleMLPLR$new(dml_data, ml_g = learner_g, ml_m = learner_m,
                       n_folds = 5, n_rep = 1)
dml$fit()
dml$confint()
```

---

## 10. Heckman selection

```r
library(sampleSelection)

# Two-step
heck2 <- heckit(selection = in_labor_force ~ age + edu + marital + kids,
                outcome   = log_wage         ~ age + edu + training,
                data = df, method = "2step")
summary(heck2)

# Maximum likelihood
heck_ml <- heckit(selection = in_labor_force ~ age + edu + marital + kids,
                  outcome   = log_wage         ~ age + edu + training,
                  data = df, method = "ml")
summary(heck_ml)
```

---

## 11. Quantile regression

```r
library(quantreg)

# Single quantile
q50 <- rq(log_wage ~ training + age + edu, data = df, tau = 0.5)
summary(q50, se = "boot", R = 500)

# Multiple quantiles
qrs <- rq(log_wage ~ training + age + edu, data = df,
          tau = c(0.1, 0.25, 0.5, 0.75, 0.9))

# Plot coefficient across quantiles
plot(summary(qrs, se = "boot", R = 500))

# ggplot version
library(ggplot2)
qr_summary <- summary(qrs, se = "boot", R = 500)
coef_df <- map_dfr(seq_along(qr_summary), function(i) {
  s <- qr_summary[[i]]$coefficients["training", ]
  tibble(tau   = qr_summary[[i]]$tau,
         coef  = s["coefficients"],
         lower = s["lower bd"],
         upper = s["upper bd"])
})
ggplot(coef_df, aes(tau, coef)) +
  geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.2) +
  geom_line(linewidth = 1) +
  geom_hline(yintercept = coef(lm(log_wage ~ training + age + edu, data = df))["training"],
             linetype = "dashed", color = "red") +
  labs(x = "Quantile", y = "Coefficient on training")
ggsave("figures/qreg.pdf", width = 6, height = 4)
```

---

## 12. SEM / mediation

```r
library(lavaan)

# Linear SEM with mediator
mod <- '
  log_wage    ~ b * hours_worked + c_prime * training + age + edu
  hours_worked~ a * training + age + edu
  indirect := a * b
  total    := a * b + c_prime
'
fit <- sem(mod, data = df, se = "bootstrap", bootstrap = 1000)
summary(fit, standardized = TRUE, fit.measures = TRUE)
parameterEstimates(fit, standardized = TRUE)

# Imai et al. mediation with sensitivity
library(mediation)
fit_M <- lm(hours_worked ~ training + age + edu, data = df)
fit_Y <- lm(log_wage ~ training + hours_worked + age + edu, data = df)
med   <- mediate(fit_M, fit_Y, treat = "training", mediator = "hours_worked",
                 boot = TRUE, sims = 1000)
summary(med); plot(med)

# Sensitivity to unmeasured M-Y confounder
medsens <- medsens(med, rho.by = 0.05, effect.type = "indirect", sims = 500)
plot(medsens)
```

---

## Quick command → estimator cheat sheet

| Estimator | Canonical R command |
|-----------|---------------------|
| OLS robust | `feols(y ~ x, data, cluster = ~ id)` |
| Panel FE | `feols(y ~ x \| unit + time, data, cluster = ~ unit)` |
| Multi-way cluster | `feols(..., cluster = ~ unit + firm)` |
| HD interaction FE | `feols(y ~ x \| unit + ind^year, ...)` |
| Logit + AME | `glm(y ~ x, family=binomial)` then `avg_slopes(.)` |
| Logit + HD FE | `feglm(y ~ x \| fe, family=binomial)` |
| Poisson + HD FE | `fepois(y ~ x \| fe)` |
| 2SLS | `feols(y ~ exog \| fe \| endog ~ z)` or `AER::ivreg` |
| 2×2 DID | `feols(y ~ i(treated, post, ref=0) \| unit + time)` |
| Event study | `feols(y ~ i(rel, ref = -1) \| unit + time)` |
| CS 2021 | `did::att_gt(yname, tname, idname, gname, data)` |
| SA 2021 | `feols(y ~ sunab(first_treat, year) \| unit + time)` |
| BJS 2024 | `didimputation::did_imputation(data, yname, gname, tname, idname)` |
| SDID | `synthdid::synthdid_estimate` |
| Sharp RD | `rdrobust(y, x, c=0)` |
| Density | `rddensity(X, c=0)` |
| SCM | `tidysynth` pipeline / `gsynth::gsynth` |
| PSM | `MatchIt::matchit(treat ~ X, method = "nearest")` |
| IPW | `WeightIt::weightit(treat ~ X, method = "ps")` |
| Entropy bal | `ebal::ebalance(treat, X)` or `WeightIt::weightit(method="ebal")` |
| Causal forest | `grf::causal_forest(X, Y, W)` |
| DML | `DoubleML::DoubleMLPLR` |
| Heckman | `sampleSelection::heckit` |
| Quantile reg | `quantreg::rq(y ~ x, tau = 0.5)` |
| SEM | `lavaan::sem` |
| Mediation w/ sensitivity | `mediation::mediate` + `medsens` |
