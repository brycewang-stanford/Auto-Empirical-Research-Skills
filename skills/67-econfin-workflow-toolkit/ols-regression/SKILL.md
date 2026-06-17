---
name: ols-regression
description: |
  Econometrics skill for OLS regression and linear models. Activates when the user asks about:
  "run OLS", "linear regression", "ordinary least squares", "interpret regression results",
  "heteroskedasticity", "multicollinearity", "regression assumptions", "robust standard errors",
  "GLS", "WLS", "fit a regression model", "check regression diagnostics", "OLS假设",
  "最小二乘法", "线性回归", "回归系数", "残差检验", "异方差", "多重共线性",
  "普通最小二乘", "稳健标准误", "回归诊断"
---

# OLS Regression Skill

This skill provides comprehensive guidance for OLS regression and linear models in empirical research. It covers model specification, assumption testing, diagnostic checks, and result interpretation, with code examples in Python, R, and Stata.

## Core Workflow

When assisting with OLS regression, follow this sequence:

1. **Clarify the research question and data** — understand dependent variable, key regressors, and sample
2. **Specify the model** — choose functional form, control variables, fixed effects if needed
3. **Run the regression** — provide code in the user's preferred language
4. **Check assumptions** — run diagnostics systematically (see references)
5. **Interpret and report** — explain coefficients, significance, fit, and caveats

## Key Concepts

### Model Specification
- Write the regression equation explicitly: Y = β₀ + β₁X₁ + ... + βₖXₖ + ε
- Consider log transformations for skewed variables or elasticity interpretation
- Include relevant controls to reduce omitted variable bias
- Watch for irrelevant variables inflating standard errors

### The Gauss-Markov Assumptions
1. Linearity in parameters
2. Random sampling
3. No perfect multicollinearity
4. Zero conditional mean of errors: E(ε|X) = 0
5. Homoskedasticity: Var(ε|X) = σ²
6. (For inference) Normally distributed errors

Violation of assumptions 4–5 does not bias OLS but affects standard errors. Violation of assumption 4 (endogeneity) biases estimates — recommend IV methods.

### Standard Error Options
- **Default OLS SE**: valid only under homoskedasticity
- **HC robust SE (White)**: use when heteroskedasticity is suspected; always safe for cross-section data
- **Clustered SE**: use when observations are grouped (e.g., by firm, region, year)
- **Newey-West SE**: use for time series with autocorrelation

## Quick Code Templates

### Python (statsmodels)
```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

# With robust standard errors
model = smf.ols('y ~ x1 + x2 + x3', data=df).fit(cov_type='HC3')
print(model.summary())
```

### R
```r
library(lmtest)
library(sandwich)

model <- lm(y ~ x1 + x2 + x3, data = df)
coeftest(model, vcov = vcovHC(model, type = "HC3"))
```

### Stata
```stata
reg y x1 x2 x3, robust
```

## Diagnostics Checklist

Run all diagnostics after fitting. See `references/ols-reference.md` for full test details.

| Issue | Test | Quick Fix |
|-------|------|-----------|
| Heteroskedasticity | Breusch-Pagan, White test | Robust SE |
| Autocorrelation | Durbin-Watson, Breusch-Godfrey | Newey-West SE |
| Multicollinearity | VIF > 10 | Drop/combine variables |
| Non-normality of errors | Jarque-Bera | Check outliers; large N mitigates |
| Omitted variable bias | Ramsey RESET | Respecify model |

## Reporting Standards (Academic)

- Report coefficients with standard errors in parentheses (or t-stats)
- Use asterisks for significance: * p<0.10, ** p<0.05, *** p<0.01
- Always state which standard errors are used (robust, clustered, etc.)
- Report R², adjusted R², N, and F-statistic
- Describe the identification strategy and potential endogeneity concerns

For detailed test formulas, code, and extended examples, see `references/ols-reference.md`.

## Common Pitfalls

- **Claiming causality without identification**: OLS with controls does not establish causality — use IV, DID, or RDD for causal claims
- **Using default SE with clustered data**: Always cluster SE at the group level when observations are grouped
- **Including "bad controls"**: Don't control for post-treatment variables (mediators) — they introduce collider bias
- **Log-transforming variables with zeros**: ln(0) is undefined; use asinh(x) or ln(x+1) with appropriate interpretation
- **Reporting R² as evidence of a good model**: High R² does not mean the model is correctly specified or causal

## Related Skills & Commands

- **panel-data**: If your data has repeated observations on the same units
- **iv-estimation**: If you suspect endogeneity in your key regressor
- **stats**: Generate summary statistics before running regressions
- **/diagnose**: Run comprehensive diagnostic tests on your OLS model
- **/robustness**: Design robustness checks for your specifications
- **/interpret**: Get help interpreting regression output
- **table**: Format regression results for publication
