# Survival Analysis in Stata

## Declaring Survival Data (stset)

All survival commands require `stset` first. This creates special variables: `_t0` (interval start), `_t` (interval end), `_d` (failure indicator), `_st` (sample indicator).

```stata
// Basic setup
stset timevar, failure(failvar)

// Specific failure value (e.g., status==1 is death, status==2 is censored)
stset time, failure(status==1)

// Scale time units (days to years)
stset time_days, failure(event) scale(365.25)

// Panel data with subject ID (required for multiple records per subject)
stset time, failure(event) id(patient_id)

// Delayed entry (left truncation)
stset exit_time, failure(died) enter(entry_time) origin(time birth_date)

// Suppress stset banner in subsequent commands
stset time, failure(died) noshow

// Inspect the setup
stdes       // Summary of survival data structure
stsum       // Summary statistics (median survival, etc.)
```

---

## Kaplan-Meier Estimator

### Survival Curves (sts graph)

```stata
webuse drug2, clear
stset studytime, failure(died)

// Basic survival curve
sts graph

// By group
sts graph, by(drug)

// Customized with risk table
sts graph, by(drug) ///
    title("Survival by Treatment Group") ///
    xtitle("Time (days)") ytitle("Survival Probability") ///
    legend(label(1 "Placebo") label(2 "Drug A")) ///
    risktable

// Cumulative hazard plot
sts graph, cumhaz by(drug)

// Hazard function (smoothed)
sts graph, hazard by(drug) kernel(epan2)
```

### Survival Tables (sts list)

```stata
sts list                                  // Full table
sts list, at(0 100 200 300 400 500)       // At specific times
sts list, at(0 to 500 by 100) failure     // Failure probability
sts list, by(drug) ci                     // By group with CIs
```

### Median Survival Time

```stata
stsum               // Overall median survival
stsum, by(drug)     // By group

stci                // Median with CI
stci, by(drug)      // By group
stci, p(25)         // 25th percentile
stci, p(75)         // 75th percentile
```

If median is not reached, more than 50% survived to end of study.

---

## Log-Rank Test (sts test)

Compares survival curves between groups. H0: survival functions are equal.

```stata
sts test drug                      // Log-rank (default)
sts test drug, wilcoxon            // Wilcoxon/Breslow (weights early events)
sts test drug, tware               // Tarone-Ware (intermediate weighting)
sts test drug, peto                // Peto-Peto
sts test drug, fh(1 0)            // Fleming-Harrington (weights early)
sts test drug, fh(0 1)            // Fleming-Harrington (weights late)
sts test drug, strata(age_group)   // Stratified log-rank
sts test dose_level, trend         // Trend test for ordered groups
```

**Which test to use:**
- **Log-rank**: Most powerful when hazards are proportional
- **Wilcoxon**: More sensitive to early differences
- **Fleming-Harrington**: Flexible weighting via fh(p q) parameters

---

## Cox Proportional Hazards Model (stcox)

Semi-parametric model: h(t|X) = h0(t) * exp(b1*X1 + b2*X2 + ...). Baseline hazard h0(t) is unspecified.

```stata
stcox drug                          // Simple model
stcox drug age                      // Multiple covariates
stcox i.drug age                    // Factor notation for categorical
stcox i.drug##c.age                 // Interaction

// Display options
stcox drug age                      // Default: hazard ratios
stcox drug age, nohr                // Coefficients instead

// Standard errors
stcox drug age, vce(robust)         // Robust SE
stcox drug age, vce(cluster hospital_id)  // Clustered SE
```

### Interpreting Hazard Ratios

- **HR = 1**: No effect
- **HR > 1**: Increased hazard (higher risk, shorter survival)
- **HR < 1**: Decreased hazard (lower risk, longer survival)
- **Formula**: % change = (HR - 1) x 100%
- **Continuous vars**: For k-unit increase, HR_k = HR^k (e.g., 10-year age effect: 1.12^10 = 3.11)
- **CI excluding 1**: Statistically significant

```stata
stcox drug age
// drug HR=0.104 → 89.6% reduction in hazard (1 - 0.104)
// age  HR=1.12  → 12% increase in hazard per year
```

### Stratified Cox Models

When PH assumption is violated for a variable, stratification allows different baseline hazards per stratum. The stratifying variable's effect is not estimated.

```stata
stcox drug age, strata(female)
stcox drug age, strata(female hospital)
```

---

## Testing Proportional Hazards Assumption

### Schoenfeld Residuals

```stata
stcox drug age
estat phtest              // Global test
estat phtest, detail      // Per-variable test

// p > 0.05 → PH assumption reasonable
// rho = correlation between residuals and time

// Plot residuals against time
estat phtest, plot(drug)
estat phtest, plot(age)
```

**If PH is violated:**
- Stratify: `stcox x1, strata(x2)`
- Include time interaction: `stcox x1, tvc(x1) texp(_t)`
- Use parametric model with time-varying effects

### Graphical Assessment

```stata
// Log-log plots (should be parallel if PH holds)
sts graph, by(drug) gwood

// Observed KM vs Cox-predicted survival
stcox drug age
stcurve, survival at1(drug=0) at2(drug=1)
```

---

## Parametric Survival Models (streg)

Unlike Cox, these specify the baseline hazard distribution. Two metrics:
- **Proportional hazards (PH)**: Reports hazard ratios (default)
- **Accelerated failure time (AFT)**: Reports time ratios (option `time`)

### Available Distributions

```stata
streg x1 x2, distribution(exponential)     // Constant hazard
streg x1 x2, distribution(weibull)         // Monotone hazard (increasing or decreasing)
streg x1 x2, distribution(gompertz)        // Exponentially changing hazard
streg x1 x2, distribution(lognormal)       // Non-monotone hazard (AFT only)
streg x1 x2, distribution(loglogistic)     // Non-monotone hazard (AFT only)
streg x1 x2, distribution(ggamma)          // Generalized gamma (nests exp, Weibull, lognormal)
```

### PH vs AFT Metric

```stata
// PH metric (hazard ratios)
streg drug age, distribution(weibull)
// HR=0.10 → drug reduces hazard by 90%

// AFT metric (time ratios)
streg drug age, distribution(weibull) time
// TR=10.1 → drug multiplies survival time by 10.1

// Coefficients (log scale)
streg drug age, distribution(weibull) nohr
```

### Weibull Shape Parameter

```stata
streg drug age, distribution(weibull)
di "p (shape) = " exp(_b[/ln_p])
// p < 1: hazard decreases over time
// p = 1: constant hazard (reduces to exponential)
// p > 1: hazard increases over time
```

### Frailty (Random Effects)

```stata
streg drug age, distribution(weibull) frailty(gamma) shared(hospital_id)
```

### Model Comparison

```stata
streg drug age, distribution(exponential)
estimates store exp_model

streg drug age, distribution(weibull)
estimates store weib_model

streg drug age, distribution(lognormal)
estimates store lnorm_model

streg drug age, distribution(loglogistic)
estimates store llogistic_model

// AIC/BIC comparison (lower is better)
estimates stats exp_model weib_model lnorm_model llogistic_model

// LR test: exponential nested in Weibull (test p=1)
streg drug age, distribution(weibull)
test [/]ln_p = 0
```

---

## Time-Varying Covariates

### Using stsplit

Splits each subject's record into multiple time intervals for time-varying analysis.

```stata
webuse drugtr, clear
stset studytime, failure(died)

// Split at specific times
stsplit period, at(0 100 200 300)

// Split into equal intervals
stsplit interval, every(50)

// Inspect split data
list studytime died _t0 _t period in 1/20, sepby(studytime)

// Create time-varying covariate
gen age_current = age + _t/365.25
```

### Cox Model with Time-Varying Covariates

```stata
// Manual approach: split then create TVC
stset studytime, failure(died) id(id)
stsplit month, every(30)
gen time_on_drug = _t
gen drug_time = drug * time_on_drug
stcox drug drug_time age
// drug: HR at time 0
// drug_time: change in log(HR) per unit time

// Built-in tvc() option (equivalent, no splitting needed)
stcox drug age, tvc(drug) texp(_t)
// Negative tvc coefficient → effect becomes more protective over time
// Non-significant → PH assumption holds for that variable
```

### Treatment Switching Example

```stata
stset failure_time, failure(died) id(patient_id)
stsplit switch, at(switch_time)
gen current_treatment = (switch_time != . & _t >= switch_time)
stcox current_treatment age baseline_severity
```

---

## Competing Risks

When subjects can experience multiple event types (e.g., death from cancer vs. death from other causes).

### Cumulative Incidence Function (CIF)

```stata
// failure_type: 1=relapse, 2=death in remission, 0=censored
stset time_months, failure(failure_type==1) id(id)

// CIF for cause 1, with cause 2 as competing event
stcompet CIF_relapse = ci, compet1(2)

// CIF by group
stcompet CIF = ci, compet1(2) by(treatment)
```

### Fine-Gray Subdistribution Hazards (stcrreg)

```stata
// Fine-Gray model for cause 1
stcrreg i.treatment age, compete(failure_type==2)
// Subdistribution HR: interpretation similar to Cox HR but accounts for competing events

// Model for each cause
stset time_months, failure(failure_type==1)
stcrreg i.treatment age, compete(failure_type==2)
estimates store cause1

stset time_months, failure(failure_type==2)
stcrreg i.treatment age, compete(failure_type==1)
estimates store cause2

estimates table cause1 cause2, eform
```

### CIF Predictions After Fine-Gray

```stata
stcrreg i.treatment age, compete(failure_type==2)
stcurve, cif at1(treatment=1 age=40) at2(treatment=2 age=40)
```

---

## Survival Predictions

### After Cox Model

```stata
stcox drug age

// Predicted curves at specific covariate values
stcurve, survival at1(drug=0 age=50) at2(drug=1 age=50)
stcurve, cumhaz at1(drug=0 age=50) at2(drug=1 age=50)
stcurve, hazard at1(drug=0 age=50) at2(drug=1 age=50)

// Individual-level predictions
predict xb, xb                  // Linear predictor
predict hr, hr                  // Relative hazard (exp(xb))
predict basehaz, basehazard     // Baseline cumulative hazard
predict basesurv, basesurv      // Baseline survival
```

### After Parametric Model

```stata
streg drug age, distribution(weibull) time

predict median_t, median time          // Median survival time
predict mean_t, mean time              // Mean survival time
predict S_at_100, surv time at(100)    // S(t=100)
predict h_at_100, hazard time at(100)  // h(t=100)
```

### Marginal Effects

```stata
stcox drug i.stage age female

// Marginal survival at specific times
margins drug, predict(surv time(100))
margins drug, predict(surv time(200))

// Plot marginal effects
margins, at(drug=(0 1) age=(40 50 60)) predict(surv time(200))
marginsplot

// Pairwise comparisons of categorical groups
stcox i.treatment_group age
contrast treatment_group, effects
```

---

## Model Diagnostics

```stata
estat concordance                   // Harrell's C statistic
predict cs, csnell                  // Cox-Snell residuals
predict mg, mgale                   // Martingale residuals
predict dev, deviance               // Deviance residuals
predict sch*, scaledsch             // Scaled Schoenfeld residuals
predict dfb*, dfbeta                // DFbeta influence
predict lmax, lmax                  // Likelihood displacement
```

---

## Quick Reference

### stset Options

| Option | Purpose |
|---|---|
| `failure(failvar)` | Failure indicator variable |
| `failure(status==1)` | Specific failure value |
| `id(subject_id)` | Subject identifier (multi-record data) |
| `enter(time t0)` | Delayed entry / left truncation |
| `origin(time birthdate)` | Origin for time scale |
| `scale(365.25)` | Scale time (e.g., days to years) |
| `noshow` | Suppress stset banner |

### Hazard Ratio Quick Interpretation

| HR | Interpretation |
|---|---|
| 1.0 | No effect |
| 1.5 | 50% increase in hazard |
| 2.0 | Doubled hazard |
| 0.5 | 50% decrease in hazard |
| 0.25 | 75% decrease in hazard |

### streg Distributions

| Distribution | Hazard Shape | Metrics Available |
|---|---|---|
| `exponential` | Constant | PH, AFT |
| `weibull` | Monotone | PH, AFT |
| `gompertz` | Exponential change | PH |
| `lognormal` | Non-monotone (hump) | AFT only |
| `loglogistic` | Non-monotone (hump) | AFT only |
| `ggamma` | Flexible (nests above) | AFT only |

### sts test Variants

| Test | When to Use |
|---|---|
| `sts test x` (log-rank) | Proportional hazards |
| `sts test x, wilcoxon` | Early differences |
| `sts test x, tware` | Intermediate |
| `sts test x, fh(p q)` | Custom weighting |
| `sts test x, trend` | Ordered groups |
| `sts test x, strata(z)` | Adjusted comparison |
