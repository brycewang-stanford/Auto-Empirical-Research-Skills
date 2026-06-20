# Sample Selection Models in Stata

## Table of Contents
1. [Overview](#overview)
2. [The Heckman Selection Model](#the-heckman-selection-model)
3. [Heckman Two-Step Estimator](#heckman-two-step-estimator)
4. [Maximum Likelihood Estimation](#maximum-likelihood-estimation)
5. [The Inverse Mills Ratio](#the-inverse-mills-ratio)
6. [Testing for Selection Bias](#testing-for-selection-bias)
7. [Treatment Effect Models](#treatment-effect-models)
8. [Exclusion Restrictions](#exclusion-restrictions)
9. [Interpretation and Marginal Effects](#interpretation-and-marginal-effects)
10. [Complete Examples](#complete-examples)
11. [Quick Reference](#quick-reference)

---

## Overview

Sample selection models address bias when sample inclusion depends on the outcome variable (incidental truncation).

**Key Stata Commands:**
- `heckman` - Heckman selection model (two-step and MLE)
- `treatreg` - Treatment effects model with endogenous treatment
- `etregress` - Extended treatment effects regression (preferred over `treatreg`)
- `heckprobit` - Heckman selection with probit outcome
- `heckoprobit` - Heckman selection with ordered probit outcome

**Types of Selection:**
- **Incidental Truncation (Type II Tobit):** outcome observed only when selection = 1 (e.g., wages only for employed)
- **Endogenous Treatment Selection:** treatment assignment depends on potential outcomes (e.g., job training)

---

## The Heckman Selection Model

Two equations estimated jointly:

1. **Selection Equation (Probit):** estimated on full sample
2. **Outcome Equation (Linear):** estimated on selected sample only

**Key Parameters:**
- **rho:** Correlation between selection and outcome errors. rho=0 means no selection bias (OLS consistent). rho>0 = positive selection. rho<0 = negative selection.
- **lambda:** Inverse Mills ratio = rho x sigma. The bias correction factor.

**Identification Requirements:**
1. **Exclusion restrictions** (recommended): at least one variable in selection equation not in outcome equation
2. Functional form alone (nonlinearity) provides weak identification -- not recommended
3. Bivariate normality of errors assumed

---

## Heckman Two-Step Estimator

### Basic Syntax

```stata
heckman depvar indepvars [if] [in] [weight], ///
    select(selection_depvar = selection_indepvars) ///
    twostep [options]
```

### Example

```stata
sysuse nlsw88, clear
generate experience = age - grade - 6
generate experience2 = experience^2

heckman wage grade experience experience2, ///
    select(married = grade south) ///
    twostep
```

### Understanding the Output

```stata
heckman wage grade experience, ///
    select(married = grade south children) ///
    twostep

* Output includes:
* 1. Selection Equation (Probit): factors affecting Pr(selected=1)
* 2. Outcome Equation with correction: includes lambda (IMR coefficient)
*    - lambda significant → selection bias present
*    - lambda positive → selected have higher outcomes
* 3. rho, sigma, lambda = rho × sigma
* 4. Test: H0: rho = 0. p < 0.05 → selection bias present
```

### Manual Two-Step (for illustration only)

```stata
* Step 1: Probit on full sample
probit married grade south children
predict imr, mills

* Step 2: OLS on selected sample including IMR
regress wage grade experience imr if married == 1

* WARNING: SEs from manual Step 2 are INCORRECT
* Always use heckman command for correct inference
```

### Options

```stata
heckman wage grade, select(married = grade south) twostep
heckman wage grade, select(married = grade south) twostep vce(robust)
heckman wage grade, select(married = grade south) twostep vce(cluster id)
```

---

## Maximum Likelihood Estimation

Omitting `twostep` invokes MLE (the default). MLE is more efficient but less robust to misspecification.

```stata
* MLE estimation (default)
heckman wage grade south, ///
    select(married = grade south children)

* With robust SEs
heckman wage grade south, ///
    select(married = grade south children) ///
    vce(robust)

* Use difficult option for convergence issues
heckman wage grade south, ///
    select(married = grade south children) ///
    difficult
```

### Comparing Two-Step vs. MLE

```stata
heckman wage grade south, ///
    select(married = grade south children) twostep
estimates store twostep

heckman wage grade south, ///
    select(married = grade south children)
estimates store mle

estimates table twostep mle, b(%9.4f) se(%9.4f) stats(N ll aic)
```

### Starting Values from Two-Step

```stata
heckman wage grade south, ///
    select(married = grade south children) twostep
matrix b_init = e(b)

heckman wage grade south, ///
    select(married = grade south children) ///
    from(b_init, copy)
```

### Constraining rho

```stata
constraint define 1 [athrho]_cons = 0
heckman wage grade south, ///
    select(married = grade south children) ///
    constraints(1)
```

---

## The Inverse Mills Ratio

### Computing IMR

```stata
* After probit
probit employed grade experience children
predict z_hat, xb

generate phi = normalden(z_hat)      // density
generate Phi = normal(z_hat)          // CDF
generate lambda = phi / Phi           // IMR manually

* Or use mills option directly
predict lambda2, mills
```

### IMR in Two-Step

```stata
probit employed grade experience children
predict imr, mills

regress wage grade experience imr if employed == 1

* Coefficient on IMR:
*   Positive & significant → positive selection (workers earn more than random)
*   Negative & significant → negative selection
*   Insignificant → no selection bias, OLS likely fine
```

---

## Testing for Selection Bias

### Test 1: Significance of rho (primary test)

```stata
heckman wage grade experience, ///
    select(employed = grade experience children)

* Reported automatically in output as Wald or LR test of rho=0
* Manual Wald test:
test [athrho]_cons = 0
```

### Test 2: Lambda Significance (two-step)

```stata
heckman wage grade experience, ///
    select(employed = grade experience children) twostep

* Lambda coefficient tested automatically
* Significant lambda → selection bias
```

### Test 3: LR Test via Constraint

```stata
constraint define 1 [athrho]_cons = 0
heckman wage grade experience, ///
    select(employed = grade experience children) constraints(1)
estimates store restricted

heckman wage grade experience, ///
    select(employed = grade experience children)
estimates store unrestricted

lrtest unrestricted restricted
```

### Test 4: Compare OLS vs. Heckman

```stata
regress wage grade experience if employed == 1
estimates store ols

heckman wage grade experience, ///
    select(employed = grade experience children)
estimates store heckman

estimates table ols heckman, b(%9.4f) se stats(N)
hausman heckman ols, equations(1:1)
```

### Complete Testing Protocol

```stata
regress wage grade experience if employed == 1
estimates store ols_model

heckman wage grade experience, ///
    select(employed = grade experience children otherinc)
estimates store heckman_model

test [athrho]_cons = 0
local pvalue_rho = r(p)

estimates table ols_model heckman_model, b(%9.4f) se(%9.4f) stats(N r2)

display "Test of rho = 0: p-value = " %6.4f `pvalue_rho'
if `pvalue_rho' < 0.05 {
    display "Selection bias detected. Use Heckman."
}
else {
    display "No strong evidence of bias. OLS may be adequate."
}
```

---

## Treatment Effect Models

### treatreg

Estimates treatment effects when treatment assignment is endogenous (correlated with outcome errors).

```stata
treatreg depvar indepvars, treat(treatment = instruments) [options]
```

```stata
* Two-step
treatreg wage education age, treat(training = education age distance) twostep

* MLE
treatreg wage education age, treat(training = education age distance) mle

* Robust SEs
treatreg wage education age, treat(training = education age distance) vce(robust)
```

### etregress (preferred over treatreg)

Same underlying model but better post-estimation support, margins integration, and flexible variance structures.

```stata
etregress depvar indepvars, treat(treatment = instruments) [options]
```

```stata
sysuse nlsw88, clear
generate college = (grade >= 16)

* Endogenous treatment model
etregress wage age i.race, treat(college = age i.race south)
```

### Post-Estimation with etregress

```stata
etregress wage age i.race, treat(college = age i.race south)

* Marginal effects
margins, dydx(college)
margins, dydx(age)

* Treatment effects
margins, predict(te)                           // ATE
margins, predict(te) subpop(if college==1)     // ATT
margins, predict(te) subpop(if college==0)     // ATU

* Potential outcomes
margins, predict(yc0)    // outcome if untreated
margins, predict(yc1)    // outcome if treated

* Heterogeneous treatment effects
margins race, predict(te)
marginsplot

margins, at(age=(25(5)55)) predict(te)
marginsplot, title("Treatment Effect by Age")
```

### Calculating Individual Treatment Effects

```stata
treatreg wage education age, treat(training = education age)

predict wage1, yc1      // wage if treated
predict wage0, yc0      // wage if untreated
generate ite = wage1 - wage0

summarize ite                       // ATE
summarize ite if training == 1      // ATT
summarize ite if training == 0      // ATU
```

### Heterogeneous Treatment Effects with Interactions

```stata
etregress wage c.age##i.college i.race, ///
    treat(college = age i.race south c.age#c.age)

margins, at(age=(25(5)55)) predict(te)
marginsplot, title("Treatment Effect of College by Age")

margins race, predict(te)
marginsplot, title("Treatment Effect of College by Race")
```

---

## Exclusion Restrictions

Variables that affect selection/treatment but NOT the outcome directly. Critical for credible identification.

### Why Needed

Without exclusions, identification relies on functional form (nonlinearity) alone -- estimates are unstable and not credible. With exclusions, identification is strong and results are stable.

### Common Exclusion Examples

**Labor/Wage equations:**
- Number of children, non-labor income, spouse income, local unemployment rate

**Education/Training returns:**
- Distance to college, tuition costs, GI Bill eligibility, quarter of birth

**Program evaluation:**
- Geographic proximity, randomized eligibility, administrative barriers

### Testing Instrument Strength

```stata
probit married grade south children otherincome
test children otherincome

* Calculate pseudo-F equivalent
local F_stat = r(chi2) / r(df)
display "First-stage F-statistic: " `F_stat'
* Rule of thumb: F > 10 for strong instruments
```

### Overidentification Test (multiple exclusions)

```stata
heckman wage grade south, ///
    select(married = grade south children otherincome)
estimates store full_model

heckman wage grade south, ///
    select(married = grade south children)
estimates store restricted_model

lrtest full_model restricted_model
* Large p-value → additional instrument appears valid
```

---

## Interpretation and Marginal Effects

### Selection Equation Coefficients

Probit metric -- not directly interpretable as probabilities. Use margins:

```stata
heckman wage grade, select(married = grade children)
margins, dydx(*) predict(psel)
```

### Outcome Equation Coefficients

Effect on outcome CONDITIONAL on being selected. Not the population average effect (unless rho=0).

### rho Interpretation

- rho > 0: Positive selection -- selected observations have higher outcomes
- rho < 0: Negative selection -- selected observations have lower outcomes
- rho = 0: No selection bias

### Marginal Effects

```stata
heckman wage grade experience, ///
    select(married = grade experience children)

* On selection probability
margins, dydx(grade) predict(psel)

* On outcome conditional on selection
margins, dydx(grade) predict(ycond)

* On outcome unconditional
margins, dydx(grade) predict(yexpected)
```

### Prediction Options

```stata
* After heckman:
predict xb, xb              // linear prediction (outcome)
predict xbsel, xbsel        // linear prediction (selection)
predict psel, psel           // Pr(selected)
predict yc, yc               // E(y|selected)
predict ycond, ycond         // E(y|selected) [same as yc]
predict yexpected, yexpected // E(y) unconditional
predict stdp, stdp           // SE of prediction
predict imr, mills           // inverse Mills ratio

* After etregress:
predict te, te               // treatment effect
predict yc0, yc0             // potential outcome if untreated
predict yc1, yc1             // potential outcome if treated
predict ycond, ycond         // conditional mean
```

### Recovering rho from athrho

```stata
* Stata parameterizes rho as athrho (inverse hyperbolic tangent)
nlcom (rho: [athrho]_cons / sqrt(1 + [athrho]_cons^2))
* Or: scalar rho = tanh(b[1, "athrho:_cons"])
```

---

## Complete Examples

### Example 1: Heckman Wage Model

```stata
sysuse nlsw88, clear
generate experience = age - grade - 6
generate experience2 = experience^2

* Step 1: Naive OLS (biased -- only employed women)
regress wage grade experience experience2 if !missing(wage)
estimates store ols_naive

* Step 2: Heckman two-step
heckman wage grade experience experience2, ///
    select(married = grade south age ttl_exp) twostep nolog
estimates store heckman_2step

test lambda

* Step 3: Heckman MLE
heckman wage grade experience experience2, ///
    select(married = grade south age ttl_exp) nolog
estimates store heckman_mle

* Step 4: Compare
estimates table ols_naive heckman_2step heckman_mle, ///
    b(%9.4f) se stats(N ll aic) ///
    keep(grade experience experience2)

* Step 5: Test rho = 0
estimates restore heckman_mle
test [athrho]_cons = 0

* Step 6: Marginal effects
margins, dydx(grade) predict(ycond)      // on wage
margins, dydx(grade) predict(psel)       // on employment
margins, dydx(grade) predict(yexpected)  // unconditional

* Step 7: Predictions
predict wage_fitted, yc
predict prob_married, psel
predict lambda, mills
summarize lambda, detail
```

### Example 2: Treatment Effects (Job Training)

```stata
* etregress with exclusion restrictions
etregress wage education age urban, ///
    treat(training = education age urban distance eligible)
estimates store te_mle

* Test for endogenous treatment
test [athrho]_cons = 0

* Treatment effects
margins, predict(te)                         // ATE
margins if training==1, predict(te)          // ATT
margins if training==0, predict(te)          // ATU

* Heterogeneity
margins, at(education=(8(2)20)) predict(te)
marginsplot, title("Training Effect by Education Level")

* Potential outcomes
predict wage_if_treated, yc1
predict wage_if_untreated, yc0
generate individual_te = wage_if_treated - wage_if_untreated
summarize individual_te
```

### Example 3: Count Outcome with Selection (Workaround)

```stata
* Standard heckman requires continuous outcome
* For count data, two workarounds:

* Approach 1: Manual two-step with Poisson
probit academic phd_quality experience
predict imr if academic == 1, mills
poisson publications phd_quality experience imr if academic == 1
* Significant IMR → selection matters

* Approach 2: Heckman with log transform (approximate)
generate log_pubs = ln(publications + 1) if academic == 1
heckman log_pubs phd_quality experience, ///
    select(academic = phd_quality experience) nolog
```

---

## Quick Reference

### Command Syntax

```stata
*--- Heckman Selection Model ---*
heckman depvar indepvars, select(sel_depvar = sel_indepvars) twostep
heckman depvar indepvars, select(sel_depvar = sel_indepvars)   // MLE

*--- Treatment Effects ---*
treatreg depvar indepvars, treat(treatment = instruments) [twostep|mle]
etregress depvar indepvars, treat(treatment = instruments)     // preferred
```

### Common Options

```stata
twostep                 // two-step estimator (heckman only)
vce(robust)            // robust SEs
vce(cluster clustvar)  // clustered SEs
difficult              // alternative optimization algorithm
from(matname)          // starting values
nolog                  // suppress iteration log
noshowselection        // hide selection equation output
```

### Interpretation Table

| Parameter | Meaning |
|-----------|---------|
| beta (outcome) | Effect on y conditional on selection |
| gamma (selection) | Probit coefficient -- use `margins, predict(psel)` |
| rho > 0 | Positive selection bias |
| rho < 0 | Negative selection bias |
| rho = 0 | No selection bias (OLS OK) |
| lambda | rho x sigma (Mills ratio coefficient) |
| delta (treatment) | Average treatment effect |

### Decision Tree

```
Is sample selection non-random?
  NO  → standard regression
  YES →
    Continuous outcome? → heckman
    Binary outcome? → heckprobit
    Treatment effect problem? → etregress / treatreg

    Have exclusion restrictions?
      YES → strongly identified, proceed
      NO  → weakly identified, interpret cautiously

    Two-step or MLE?
      MLE: more efficient, better inference (default choice)
      Two-step: more robust to distributional misspecification
```

### Common Pitfalls

- Relying on functional form alone without exclusion restrictions
- Interpreting probit coefficients as probabilities (use margins)
- Forgetting to test rho=0 before concluding selection bias exists
- Using weak instruments (F < 10) -- produces unreliable estimates
- Interpreting outcome coefficients as population average effects (they are conditional on selection)
- Not reporting first-stage results and instrument strength

### Reporting Template

```stata
quietly regress wage education experience if working == 1
estimates store m1

quietly heckman wage education experience, ///
    select(working = education experience children) twostep
estimates store m2

quietly heckman wage education experience, ///
    select(working = education experience children)
estimates store m3

esttab m1 m2 m3 using "results.tex", ///
    b(%9.3f) se(%9.3f) ///
    star(* 0.05 ** 0.01 *** 0.001) ///
    stats(N ll rho, labels("Observations" "Log-likelihood" "Rho")) ///
    title("Wage Equation with Selection Correction") ///
    mtitles("OLS" "Heckman-2Step" "Heckman-MLE") ///
    replace
```
