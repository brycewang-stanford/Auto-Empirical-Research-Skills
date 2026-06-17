# Limited Dependent Variable Models in Stata

## Binary Outcome Models

### Logit and Logistic

- `logit` reports coefficients (log-odds)
- `logistic` reports odds ratios (exponentiated coefficients)

```stata
logit union age grade south
logit, or                           // Redisplay as odds ratios
logistic union age grade south      // Directly reports odds ratios

// Factor variable notation for interactions
logit union c.age##i.south grade

// Robust and clustered SEs
logit union age grade south, robust
logit union age grade south, cluster(industry)
```

**Interpreting odds ratios:** OR > 1 increases odds; OR < 1 decreases odds; (OR - 1) * 100 = percentage change in odds.

### Probit

```stata
probit union age grade south
```

**Logit vs Probit:** Logit coefficients are roughly 1.6-1.8x larger than probit. Both give similar predicted probabilities. Logit has fatter tails. Use logit unless field conventions dictate otherwise.

---

## Censored and Truncated Models

### Tobit Regression

For censored continuous outcomes (values at a boundary are observed but capped).

```stata
tobit hours age grade south, ll(0)          // Left-censored at 0
tobit test_score age education, ll(0) ul(100)  // Both sides
```

**Gotcha:** Tobit coefficients represent effects on the **latent variable**, not the observed outcome. Use `margins` for interpretable effects.

```stata
tobit hours age grade south, ll(0)
predict ystar, xb                           // Predicted latent variable
predict yexp, ystar(0,.)                    // Expected value of censored DV
predict prob_positive, pr(0,.)              // Pr(uncensored)
margins, dydx(*) predict(ystar(0,.))        // Marginal effects on E[Y|Y>0]
```

---

## Ordered Outcome Models

For naturally ordered categories with unknown distances between levels.

### Ordered Logit (ologit) / Ordered Probit (oprobit)

```stata
ologit health age grade i.race
ologit health age grade i.race, or          // Odds ratios

oprobit health age grade i.race
```

**Cut points** divide the latent continuous variable into ordered categories. The **proportional odds assumption** means same coefficients apply across all category comparisons.

```stata
// Test proportional odds assumption
ssc install omodel
omodel logit health age grade
// If violated, consider mlogit or gologit2
```

---

## Multinomial Outcome Models

### Multinomial Logit (mlogit)

For unordered categorical outcomes. **Do not use for ordered outcomes.**

```stata
mlogit occ_cat age grade i.race, baseoutcome(1)
mlogit occ_cat age grade i.race, rrr base(1)  // Relative risk ratios

// Predicted probabilities
predict prob_prof prob_tech prob_service, pr
```

**IIA assumption** (Independence of Irrelevant Alternatives): relative odds between any two alternatives don't depend on other alternatives.

```stata
// Hausman test for IIA
mlogit occ_cat age grade
estimates store full
mlogit occ_cat age grade if occ_cat != 2
hausman full ., alleqs constant
// If violated, consider multinomial probit, nested logit, or mixed logit
```

---

## Count Data Models

### Poisson Regression

Assumes mean = variance (equidispersion). Use `irr` option for incidence rate ratios.

```stata
poisson doctor_visits age grade i.married, irr

// Exposure variable (when observation periods differ)
poisson num_events age education, exposure(months_observed)

// Test for overdispersion
estat gof
// If Prob > chi2 is very small: evidence of overdispersion
```

### Negative Binomial Regression

Handles overdispersion by adding parameter alpha. When alpha = 0, reduces to Poisson.

```stata
nbreg doctor_visits age grade i.married, irr

// Test Poisson vs Negative Binomial
poisson doctor_visits age grade
estimates store m_pois
nbreg doctor_visits age grade
estimates store m_nbreg
lrtest m_pois m_nbreg
// p < 0.05: use Negative Binomial
```

### Zero-Inflated Models

For excess zeros beyond what Poisson/NB predict:

```stata
zip depvar indepvars, inflate(predictors_of_zeros)
zinb depvar indepvars, inflate(predictors_of_zeros)
```

---

## Post-Estimation and Interpretation

### The margins Command

**Always use `margins` for interpretation of limited DV models.** Raw coefficients are not directly interpretable as marginal effects.

```stata
// Average marginal effects (AME)
logit union age grade south
margins, dydx(*)                      // Do NOT add 'post' unless you need to test margins

// At specific values
margins, dydx(*) at(age=30 grade=12)
margins, dydx(*) at(age=(20 30 40 50))

// For factor variables
logit union age grade i.south i.race
margins, dydx(race)

// After ordered logit: predicted probabilities per outcome
ologit health age grade
margins, predict(outcome(1))
margins, predict(outcome(4))
margins, at(age=(30 40 50 60)) predict(outcome(4))
marginsplot

// After count models
poisson doctor_visits age grade i.married, irr
margins, dydx(*)
margins, at(age=(30 40 50 60) married=(0 1))
```

### Predicted Probabilities

```stata
// Binary
logit union age grade south
predict pr_union, pr
generate predicted = (pr_union > 0.5)
tabulate union predicted              // Confusion matrix

// Ordered
ologit health age grade
predict pr1 pr2 pr3 pr4, pr

// Multinomial
mlogit occ_cat age grade
predict pr_prof pr_tech pr_service, pr

// Count: probability of specific counts
poisson doctor_visits age grade
predict lambda, n                     // Expected count
predict pr0, pr(0)                    // Pr(Y=0)
predict pr_ge3, pr(3,.)              // Pr(Y>=3)
```

---

## Model Diagnostics and Testing

```stata
// Logit/Probit goodness of fit
logit union age grade south
estat gof, group(10)                  // Hosmer-Lemeshow (p > 0.05 = good fit)
estat classification                  // Sensitivity, specificity
lroc                                  // AUC (0.7-0.8 acceptable, >0.9 outstanding)

// Model comparison
logit union age grade
estimates store restricted
logit union age grade south i.race i.married
estimates store full
lrtest restricted full                // LR test (p < 0.05: use full model)

// Information criteria
estimates table model1 model2 model3, stats(N ll aic bic)

// Residuals
predict pearson, rstandard
predict deviance, deviance
list if abs(pearson) > 3              // Outliers
```

---

## Quick Reference

| Outcome Type | Command | Reports |
|---|---|---|
| Binary | `logit` / `logistic` / `probit` | Log-odds / Odds ratios / Normal CDF |
| Censored continuous | `tobit` | Latent variable coefficients |
| Ordered categories | `ologit` / `oprobit` | Log-odds / Normal CDF |
| Unordered categories | `mlogit` | Log relative risk |
| Count | `poisson` / `nbreg` | Log count coefficients |

### Common Options

```stata
command ..., robust                   // Robust SEs
command ..., cluster(varname)         // Clustered SEs
logit ..., or                         // Odds ratios
poisson ..., irr                      // Incidence rate ratios
mlogit ..., rrr                       // Relative risk ratios
mlogit ..., baseoutcome(#)            // Set base category
tobit ..., ll(#) ul(#)               // Censoring limits
```

### Post-Estimation

```stata
margins, dydx(*)                      // Average marginal effects
margins, at(var=(values))             // Predicted at values
marginsplot                           // Visualize
estat ic                              // AIC, BIC
estat gof                             // Goodness of fit
lrtest model1 model2                  // Likelihood ratio test
```

### Common Mistakes

- Using OLS for binary, count, or ordered outcomes
- Interpreting logit/probit coefficients as marginal effects
- Ignoring overdispersion in count models
- Using mlogit for ordered outcomes
- Forgetting `ll()` in tobit when censored at 0
- Using `margins, post` unnecessarily — `post` replaces `e()` with margins results, forcing re-estimation before any further post-estimation (`estat`, `lroc`, `predict`, or another `margins` call). Only use `post` when you need to run `test` or `lincom` on the margins themselves.

### Useful User-Written Commands

```stata
ssc install estout       // Publication tables
ssc install omodel       // Test ordered model assumptions
ssc install gologit2     // Generalized ordered logit
ssc install countfit     // Compare count models
ssc install listcoef     // Coefficient interpretation
ssc install fitstat      // Model fit statistics
```
