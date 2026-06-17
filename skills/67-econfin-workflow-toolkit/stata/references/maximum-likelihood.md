# Maximum Likelihood Estimation in Stata

## Table of Contents
1. [The ml Command Framework](#the-ml-command-framework)
2. [ML Evaluator Methods](#ml-evaluator-methods)
3. [Writing Likelihood Functions](#writing-likelihood-functions)
4. [Starting Values](#starting-values)
5. [Constrained Optimization](#constrained-optimization)
6. [Standard Errors and Variance-Covariance](#standard-errors-and-variance-covariance)
7. [Likelihood Ratio Tests](#likelihood-ratio-tests)
8. [Post-Estimation and ml display](#post-estimation-and-ml-display)
9. [Complete Examples](#complete-examples)
10. [Best Practices and Troubleshooting](#best-practices-and-troubleshooting)

---

## The ml Command Framework

### Basic Workflow

```stata
* Step 1: Define the model
ml model method program_name (equation specifications)

* Step 2: Set starting values (optional)
ml init parameter_values

* Step 3: Maximize
ml maximize

* Step 4: Display results
ml display
```

### ML Model Syntax

```stata
ml model method prog_name (eq_name: depvar = indepvars) ///
                         (eq_name: indepvars) ///
                         [if] [in] [weight], [options]
```

**Components:**
- `method`: Evaluator type (lf, lf0, lf1, lf2, d0, d1, d2)
- `prog_name`: Your likelihood evaluator program
- `eq_name`: Optional equation names
- `depvar`: Dependent variable
- `indepvars`: Independent variables

**Common Options:**
- `maximize`: Combine ml model and ml maximize in one step
- `difficult`: More robust (slower) optimization technique
- `trace`: Show iteration log
- `gradient`: Show gradient vector
- `hessian`: Show Hessian matrix
- `search`: Search for better starting values

---

## ML Evaluator Methods

| Method | You Provide | Stata Computes | Speed | Difficulty |
|--------|-------------|----------------|-------|------------|
| `lf` | ln L_i for each obs | Derivatives numerically | Fastest | Easiest |
| `lf0` | ln L overall | Derivatives numerically | Fast | Easy |
| `lf1` | ln L and gradient | Hessian numerically | Medium | Medium |
| `lf2` | ln L, gradient, Hessian | Nothing | Faster | Hard |
| `d0` | ln L overall | Derivatives numerically | Slow | Easy |
| `d1` | ln L and gradient | Hessian numerically | Medium | Medium |
| `d2` | ln L, gradient, Hessian | Nothing | Fast | Hard |

### Method lf (Linear Form) -- Most Common

Requirements: return ln L_i per observation; must be "linear form" where ln L_i = f(x_i'beta).

```stata
program define myprog
    version 18
    args lnf theta1 theta2 ...
    quietly replace `lnf' = log-likelihood expression
end
```

### Method lf0 (Linear Form, Scalar)

Returns a single scalar; uses `mleval` and `mlsum` utilities.

```stata
program define myprog
    version 18
    args todo b lnf
    tempvar theta1 theta2
    mleval `theta1' = `b', eq(1)
    mleval `theta2' = `b', eq(2)
    mlsum `lnf' = log-likelihood expression
end
```

### Method lf1 (With Gradient)

```stata
program define myprog
    version 18
    args todo b lnf g
    mlsum `lnf' = log-likelihood expression
    if (`todo' == 0) exit
    tempname d1 d2
    mlvecsum `lnf' `d1' = derivative w.r.t. theta1
    mlvecsum `lnf' `d2' = derivative w.r.t. theta2
    matrix `g' = (`d1', `d2')
end
```

### Method d0, d1, d2 (General Form)

More general than lf -- allows panel data, time series, observation interdependence.

```stata
program define myprog
    version 18
    args todo b lnf
    tempvar theta1 theta2
    mleval `theta1' = `b', eq(1)
    mleval `theta2' = `b', eq(2)
    quietly {
        tempvar lnf_i
        generate double `lnf_i' = log-likelihood expression
        mlsum `lnf' = `lnf_i'
    }
end
```

---

## Writing Likelihood Functions

### General Structure

```stata
program define myml
    version 18
    args lnf xb [other parameters]
    quietly {
        tempvar y
        generate double `y' = $ML_y1
        replace `lnf' = log-likelihood formula
    }
end
```

### Common Likelihood Functions

#### Normal Distribution (linear regression)
```stata
quietly replace `lnf' = ln(normalden(`y', `xb', `sigma'))
* Or equivalently:
quietly replace `lnf' = -0.5 * (ln(2*_pi) + ln(`sigma'^2) + ///
                                ((`y' - `xb')^2 / `sigma'^2))
```

#### Bernoulli (binary outcome)
```stata
tempvar p
generate double `p' = normal(`xb')    // Probit
* or: generate double `p' = invlogit(`xb')  // Logit
quietly replace `lnf' = `y' * ln(`p') + (1 - `y') * ln(1 - `p')
```

#### Poisson (count data)
```stata
tempvar mu
generate double `mu' = exp(`xb')
quietly replace `lnf' = -`mu' + `y' * ln(`mu') - lnfactorial(`y')
```

#### Exponential (duration data)
```stata
tempvar lambda
generate double `lambda' = exp(`xb')
quietly replace `lnf' = ln(`lambda') - `lambda' * `y'
```

### ML Utility Commands

```stata
* mleval -- extract equation values
mleval `xb' = `b', eq(1)
mleval `sigma' = `b', eq(2)

* mlsum -- sum to create log-likelihood
mlsum `lnf' = `lnf_i'

* mlvecsum -- create gradient vector
mlvecsum `lnf' `g1' = derivative_expression, eq(1)

* mlmatsum -- create Hessian matrix
mlmatsum `lnf' `H' = second_derivative_expression
```

---

## Starting Values

### Setting Starting Values

```stata
ml init b0:_cons = 1          // Set constant in equation b0
ml init 0                      // All parameters to 0

* From matrix
matrix b0 = (1, 2, 3, 0.5)
ml init b0, copy

* From another estimator
quietly regress y x1 x2 x3
matrix b_ols = e(b)
ml init b_ols, copy
```

### Search for Starting Values

```stata
ml model lf myprog (y = x1 x2 x3)
ml search                       // Search for good starting values
ml search repeat(100)           // More thorough search
ml maximize
```

### Strategies

```stata
* 1. Use related estimators (e.g., OLS for probit, scaled by ~0.4)
quietly regress y x1 x2
matrix b0 = e(b) * 0.4
ml init b0

* 2. Use sample statistics for variance parameters
quietly summarize y
ml init lnsigma:_cons = ln(`r(sd)')

* 3. Grid search
forvalues p = -2(0.5)2 {
    capture ml model lf myprog (y = x1 x2)
    ml init b0:_cons = `p'
    ml maximize
    if _rc == 0 {
        continue, break
    }
}
```

---

## Constrained Optimization

### Parameter Constraints

```stata
* Equality constraints
constraint 1 x1 = x2
constraint 2 _cons = 0
ml model lf myprog (y = x1 x2), constraints(1 2)

* Linear constraints
constraint 1 x1 + x2 = 1
constraint 2 2*x1 - x2 = 0
```

### Inequality Constraints via Transformation

For theta > 0, estimate ln(theta); for 0 < theta < 1, estimate logit(theta).

```stata
program define myprog
    args lnf xb lnsigma
    tempvar sigma
    generate double `sigma' = exp(`lnsigma')
    // Use `sigma' in likelihood
end

* After estimation, transform back:
nlcom (sigma: exp([lnsigma]_cons))
```

### Constrained vs Unconstrained for LR Tests

```stata
constraint define 1 x1 = x2

ml model lf myprog (y = x1 x2)
ml maximize
estimates store unrestricted

ml model lf myprog (y = x1 x2), constraints(1)
ml maximize
estimates store restricted

lrtest unrestricted restricted
```

---

## Standard Errors and Variance-Covariance

### Accessing Results

```stata
matrix V = e(V)          // Variance-covariance matrix
matrix list V
```

### Robust and Cluster Standard Errors

```stata
ml model lf myprog (y = x1 x2), vce(robust)
ml model lf myprog (y = x1 x2), vce(cluster clustervar)
```

### Bootstrap Standard Errors

```stata
program define myboot, rclass
    ml model lf myprog (y = x1 x2)
    ml maximize
    matrix b = e(b)
    return matrix b = b
end
bootstrap, reps(1000): myboot
```

### Delta Method for Nonlinear Functions

```stata
ml maximize
nlcom (ratio: [eq1]x1 / [eq1]x2)
nlcom (elasticity: [eq1]x1 * (mean_x1/mean_y))
```

---

## Likelihood Ratio Tests

### Using lrtest

```stata
ml model lf myprog (y = x1 x2 x3 x4)
ml maximize
estimates store unrest

ml model lf myprog (y = x1 x2)
ml maximize
estimates store rest

lrtest unrest rest
```

### Manual Calculation

```stata
quietly ml maximize
scalar ll_unrest = e(ll)
scalar df_unrest = e(df_m)

* ... estimate restricted model ...
scalar ll_rest = e(ll)
scalar df_rest = e(df_m)

scalar LR = 2 * (ll_unrest - ll_rest)
scalar df = df_unrest - df_rest
scalar pvalue = chi2tail(df, LR)
display "LR chi2(" df ") = " LR
display "Prob > chi2 = " pvalue
```

### Model Comparison (Non-nested)

```stata
ml maximize
estat ic
estimates stats model1 model2 model3
```

---

## Post-Estimation and ml display

### ml display

```stata
ml display                 // Standard display
ml display, level(99)     // 99% confidence intervals
ml display, eform         // Exponentiated coefficients
```

### Post-Estimation Statistics

```stata
estat ic                   // Information criteria
estat vce                  // Variance-covariance matrix
estat vce, correlation     // Correlation matrix
estat summarize            // Summary statistics
estat classification       // Classification table (binary models)
```

### Storing and Comparing

```stata
estimates store model1
estimates table model1 model2
estimates stats model1 model2
estimates restore model1
```

### Predictions

```stata
predict xb, xb             // Linear prediction
predict pr, pr              // Probability (binary models)
predict resid, residuals    // Residuals
predictnl sigma = exp([lnsigma]_cons), se(sigma_se)  // Custom
```

### Saved Results After ml maximize

```stata
* Key scalars
e(ll)          // Log-likelihood
e(N)           // Number of observations
e(k)           // Number of parameters
e(k_eq)        // Number of equations
e(df_m)        // Model degrees of freedom
e(chi2)        // chi-squared statistic
e(converged)   // 1 if converged

* Key macros
e(cmd)         // Command name
e(depvar)      // Dependent variable
e(vce)         // Variance type

* Key matrices
e(b)           // Coefficient vector
e(V)           // Variance-covariance matrix
e(gradient)    // Gradient vector

* Functions
e(sample)      // Marks estimation sample
```

---

## Complete Examples

### Linear Regression via ML

```stata
capture program drop myols
program define myols
    version 18
    args lnf xb lnsigma
    quietly {
        tempvar y sigma
        generate double `y' = $ML_y1
        generate double `sigma' = exp(`lnsigma')
        replace `lnf' = -0.5 * (ln(2*_pi) + 2*`lnsigma' + ///
                                ((`y' - `xb')/`sigma')^2)
    }
end

sysuse auto, clear

* Use OLS for starting values
quietly regress price mpg weight foreign
matrix b_start = e(b)
summarize price
scalar sigma_start = r(sd)

ml model lf myols (price = mpg weight foreign) (lnsigma:)
ml init lnsigma:_cons = ln(`=sigma_start')
ml maximize

* Transform sigma back from log scale
nlcom (sigma: exp([lnsigma]_cons))

* Compare with built-in
regress price mpg weight foreign
```

### Probit via ML

```stata
capture program drop myprobit
program define myprobit
    version 18
    args lnf xb
    quietly {
        tempvar y p
        generate double `y' = $ML_y1
        generate double `p' = normal(`xb')
        replace `lnf' = `y' * ln(`p') + (1 - `y') * ln(1 - `p')
    }
end

sysuse auto, clear
generate expensive = (price > 6000)

ml model lf myprobit (expensive = mpg weight foreign)
ml maximize

* Compare with built-in
probit expensive mpg weight foreign
```

### Probit with Analytical Gradient (lf1)

```stata
capture program drop myprobit_d1
program define myprobit_d1
    version 18
    args todo b lnf g
    tempvar y xb p phi
    mleval `xb' = `b'
    quietly {
        generate double `y' = $ML_y1
        generate double `p' = normal(`xb')
        generate double `phi' = normalden(`xb')

        tempvar lnf_i
        generate double `lnf_i' = `y' * ln(`p') + (1 - `y') * ln(1 - `p')
        mlsum `lnf' = `lnf_i'

        if (`todo' == 0) exit

        tempvar g_i
        generate double `g_i' = `y' * (`phi'/`p') - ///
                                (1 - `y') * (`phi'/(1 - `p'))
        mlvecsum `lnf' `g' = `g_i'
    }
end

ml model lf1 myprobit_d1 (expensive = mpg weight foreign)
ml maximize
```

### Tobit (Censored Regression)

```stata
capture program drop mytobit
program define mytobit
    version 18
    args lnf xb lnsigma
    quietly {
        tempvar y sigma z
        generate double `y' = $ML_y1
        generate double `sigma' = exp(`lnsigma')
        generate double `z' = (`y' - `xb') / `sigma'

        * Censored at 0: ln(Phi(-xb/sigma)); Uncensored: normal density
        replace `lnf' = ln(normal(-`xb'/`sigma')) if `y' == 0
        replace `lnf' = -0.5 * (ln(2*_pi) + 2*`lnsigma' + `z'^2) if `y' > 0
    }
end

sysuse auto, clear
replace price = 0 if price < 4000

ml model lf mytobit (price = mpg weight) (lnsigma:)
ml maximize

* Compare: tobit price mpg weight, ll(0)
```

### Poisson Regression

```stata
capture program drop mypoisson
program define mypoisson
    version 18
    args lnf xb
    quietly {
        tempvar y mu
        generate double `y' = $ML_y1
        generate double `mu' = exp(`xb')
        replace `lnf' = -`mu' + `y' * `xb' - lnfactorial(`y')
    }
end

webuse dollhill3, clear
ml model lf mypoisson (deaths = smokes)
ml maximize

* Compare: poisson deaths smokes
```

### Negative Binomial

```stata
capture program drop mynbreg
program define mynbreg
    version 18
    args lnf xb lnalpha
    quietly {
        tempvar y mu alpha m
        generate double `y' = $ML_y1
        generate double `mu' = exp(`xb')
        generate double `alpha' = exp(`lnalpha')
        generate double `m' = 1/`alpha'

        replace `lnf' = lngamma(`m' + `y') - lngamma(`m') - ///
                        lnfactorial(`y') + ///
                        `m' * ln(`m') + `y' * ln(`mu') - ///
                        (`m' + `y') * ln(`m' + `mu')
    }
end

webuse recid, clear
ml model lf mynbreg (arrests = property person male) (lnalpha:)
ml maximize
nlcom (alpha: exp([lnalpha]_cons))

* Compare: nbreg arrests property person male
```

### Heckman Selection Model

```stata
capture program drop myheckman
program define myheckman
    version 18
    args lnf xb1 xb2 lnsigma athrho
    quietly {
        tempvar y1 y2 sigma rho
        generate double `y1' = $ML_y1      // Selection equation
        generate double `y2' = $ML_y2      // Outcome equation
        generate double `sigma' = exp(`lnsigma')
        generate double `rho' = tanh(`athrho')

        tempvar z2 z3
        generate double `z2' = (`y2' - `xb2') / `sigma'
        generate double `z3' = (`xb1' - `rho'*`z2') / sqrt(1-`rho'^2)

        * Selected (y1=1, y2 observed)
        replace `lnf' = -0.5*ln(2*_pi) - `lnsigma' - 0.5*`z2'^2 + ///
                        ln(normal(`z3')) if `y1' == 1
        * Not selected (y1=0)
        replace `lnf' = ln(1 - normal(`xb1')) if `y1' == 0
    }
end
```

---

## Best Practices and Troubleshooting

### Debugging

```stata
* Test with small dataset first
preserve
keep in 1/10
ml model lf myprog (y = x1 x2)
ml check                    // Check gradient numerically
ml maximize
restore

* Trace execution
ml model lf myprog (y = x1 x2), trace gradient
```

### Numerical Stability

```stata
* Use log-scale for positive parameters (sigma > 0 -> estimate lnsigma)
* Stable log-sum-exp: ln(exp(a)+exp(b)) = max(a,b) + ln(1+exp(-abs(a-b)))
* Guard against overflow:
replace `lnf' = . if missing(`xb') | abs(`xb') > 700
```

### Common Errors and Fixes

**"flat or discontinuous region"** -- Poor starting values.
```stata
ml search
ml init b0, copy
```

**"could not calculate numerical derivatives"** -- Likelihood returns missing/infinite.
```stata
* Add bounds checking:
replace `lnf' = . if missing(`lnf') | `lnf' >= .
replace `lnf' = . if abs(`lnf') > 1e10
```

**"Hessian is not negative semidefinite"** -- Not at maximum or identification issues.
```stata
ml maximize, difficult
* Check collinearity, rescale variables
```

**"convergence not achieved"**
```stata
ml maximize, iterate(100)    // More iterations
ml search                    // Better starting values
* Do NOT relax tolerance unless you understand the tradeoff
```

---

## Quick Reference

### Common ml Commands

```stata
ml model       // Define model
ml init        // Set starting values
ml search      // Search for starting values
ml maximize    // Maximize likelihood
ml display     // Display results
ml check       // Check derivatives numerically
ml plot        // Plot likelihood
ml query       // Query current model
ml count       // Count evaluations
```

### Useful ml Options

```stata
vce(robust)        // Robust standard errors
vce(cluster var)   // Cluster-robust SE
constraints(#)     // Apply constraints
difficult          // Alternative algorithm
trace              // Show trace
iterate(#)         // Max iterations
tolerance(#)       // Convergence tolerance
```

### Help Files

```stata
help ml            // Main ml help
help mleval        // Parsing utilities
help mlsum         // ML sum functions
help mlvecsum      // Gradient functions
help mlmatsum      // Hessian functions
```

### Key References

- Gould, Pitblado, Poi: *Maximum Likelihood Estimation in Stata*
- Cameron & Trivedi (2022): *Microeconometrics Using Stata*
