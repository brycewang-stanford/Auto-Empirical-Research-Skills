# OLS / GLM Regression Template

> Linear regression, logistic regression, ordinal, Poisson/negative binomial.

---

## R Pattern

```r
# --- OLS Regression ---
library(easystats)  # parameters, performance, effectsize, report
library(modelsummary)

# Fit model
model_h1 <- lm(dv ~ iv + moderator + covariate, data = df)

# Assumption checks
check_model(model_h1)  # visual diagnostic panel
check_normality(model_h1)
check_heteroscedasticity(model_h1)
check_collinearity(model_h1)  # VIF

# If heteroscedasticity detected:
library(sandwich)
model_h1_robust <- coeftest(model_h1, vcov = vcovHC(model_h1, type = "HC3"))

# Results
model_parameters(model_h1, standardize = "refit")  # coefficients + CIs
effectsize(model_h1)  # standardized effect sizes
r2(model_h1)  # R-squared variants

# Publication table
modelsummary(
  list("H1: Main Effect" = model_h1),
  stars = c("*" = .05, "**" = .01, "***" = .001),
  gof_map = c("r.squared", "adj.r.squared", "nobs", "F", "aic"),
  output = "output/tables/regression-results.docx"
)

# APA text
report(model_h1)


# --- Logistic Regression ---
model_logit <- glm(binary_dv ~ iv + covariate, data = df, family = binomial)

# Assumption checks
check_collinearity(model_logit)
performance_hosmer(model_logit)  # Hosmer-Lemeshow

# Odds ratios
model_parameters(model_logit, exponentiate = TRUE)


# --- Poisson / Negative Binomial ---
model_pois <- glm(count_dv ~ iv + covariate, data = df, family = poisson)
check_overdispersion(model_pois)  # if significant → negative binomial

library(MASS)
model_nb <- glm.nb(count_dv ~ iv + covariate, data = df)
```

## Python Pattern

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

# OLS
model_h1 = smf.ols("dv ~ iv + moderator + covariate", data=df).fit()

# Assumption checks
_, bp_pval, _, _ = het_breuschpagan(model_h1.resid, model_h1.model.exog)
vif = [variance_inflation_factor(model_h1.model.exog, i)
       for i in range(model_h1.model.exog.shape[1])]

# Robust SEs if needed
model_h1_robust = smf.ols("dv ~ iv + moderator + covariate", data=df).fit(
    cov_type="HC3"
)

# Logistic
model_logit = smf.logit("binary_dv ~ iv + covariate", data=df).fit()

# Poisson / Negative Binomial
model_pois = smf.poisson("count_dv ~ iv + covariate", data=df).fit()
model_nb = smf.negativebinomial("count_dv ~ iv + covariate", data=df).fit()
```
