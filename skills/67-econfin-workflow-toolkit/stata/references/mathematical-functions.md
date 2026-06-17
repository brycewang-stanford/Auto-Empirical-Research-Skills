# Mathematical and Statistical Functions in Stata

## Basic Mathematical Functions

```stata
abs(x)           // Absolute value
sign(x)          // -1, 0, or 1
sqrt(x)          // Square root
exp(x)           // e^x
expm1(x)         // exp(x)-1 (accurate when x near 0)
ln(x) / log(x)  // Natural logarithm
log10(x)         // Base-10 logarithm
ln1p(x)          // ln(1+x) (accurate when x near 0)
x^n              // Exponentiation

max(x1, x2, ...) // Maximum (ignores missing unless all missing)
min(x1, x2, ...) // Minimum
mod(x, y)        // Modulus (remainder): x - y*trunc(x/y)
```

**Precision note:** Use `ln1p(x)` instead of `ln(1+x)` and `expm1(x)` instead of `exp(x)-1` when x is close to 0.

---

## Trigonometric Functions

All use radians. Convert: `radians = degrees * _pi / 180`

```stata
sin(x), cos(x), tan(x)        // Basic trig
asin(x), acos(x), atan(x)     // Inverse trig
atan2(y, x)                    // Arctangent using signs for quadrant
sinh(x), cosh(x), tanh(x)     // Hyperbolic
asinh(x), acosh(x), atanh(x)  // Inverse hyperbolic
```

Constant: `_pi` = 3.1415927

---

## Random Number Generation

Always set seed for reproducibility: `set seed 12345`

```stata
runiform()          // Uniform [0,1)
runiform(a, b)      // Uniform [a,b)
runiformint(a, b)   // Uniform integer [a,b] inclusive
rnormal()           // Standard normal (mean=0, sd=1)
rnormal(m, s)       // Normal with mean m, sd s
rbinomial(n, p)     // Binomial
rgamma(a, b)        // Gamma (shape a, scale b)
rbeta(a, b)         // Beta
rchi2(df)           // Chi-squared
rpoisson(m)         // Poisson
rt(df)              // Student's t
rexponential(b)     // Exponential
```

**Gotcha -- SD vs. variance in `rnormal()`:** Mathematical notation writes N(mu, sigma^2) where the second parameter is variance. Stata's `rnormal(m, s)` takes **standard deviation**, not variance. For N(0, 4) errors, use `rnormal(0, 2)` since SD = sqrt(4) = 2.

```stata
// CORRECT: generate N(0, 4) errors — SD = sqrt(4) = 2
generate e = rnormal(0, 2)

// WRONG: this generates N(0, 16) errors, not N(0, 4)
generate e = rnormal(0, 4)
```

**Practical patterns:**
```stata
set seed 1234
gen dice_roll = runiformint(1, 6)
gen test_score = rnormal(75, 10)
gen time_to_event = -ln(runiform()) / hazard_rate   // Exponential
```

---

## Probability Distribution Functions

### Normal Distribution
```stata
normal(z)              // CDF: P(Z <= z)
normalden(z)           // PDF: standard normal density
normalden(x, m, s)     // PDF: normal with mean m, sd s
invnormal(p)           // Inverse CDF: z-score for probability p
```

### Student's t Distribution
```stata
t(df, t)               // CDF
ttail(df, t)           // Upper tail: P(T > t)
invttail(df, p)        // Inverse upper tail
tden(df, t)            // PDF
```

### Chi-squared Distribution
```stata
chi2(df, x)            // CDF
chi2tail(df, x)        // Upper tail
invchi2(df, p)         // Inverse CDF
chi2den(df, x)         // PDF
```

### F Distribution
```stata
F(df1, df2, f)         // CDF
Ftail(df1, df2, f)     // Upper tail
invF(df1, df2, p)      // Inverse CDF
Fden(df1, df2, f)      // PDF
```

### Binomial Distribution
```stata
binomial(n, k, p)      // CDF: P(X <= k)
binomialp(n, k, p)     // PMF: P(X = k)
invbinomial(n, k, p)   // Inverse CDF
```

### Poisson Distribution
```stata
poisson(m, k)          // CDF: P(X <= k)
poissonp(m, k)         // PMF: P(X = k)
invpoisson(m, p)       // Inverse CDF
```

### Beta Distribution
```stata
ibeta(a, b, x)         // CDF (incomplete beta)
invibeta(a, b, p)      // Inverse CDF
betaden(a, b, x)       // PDF
```

**Practical examples:**
```stata
// Two-tailed p-value for t-test
gen p_value = 2 * ttail(df, abs(t_statistic))

// 95% confidence interval
gen z_crit = invnormal(0.975)
gen lower = mean - z_crit * se
gen upper = mean + z_crit * se

// Use tail functions directly (more accurate than 1 - CDF)
gen p_value = chi2tail(df, chi2_stat)
```

---

## Matrix Functions

```stata
matrix A = (1, 2, 3 \ 4, 5, 6 \ 7, 8, 9)   // Create matrix
matrix I = I(3)                                // Identity matrix
matrix B = A'                                  // Transpose
matrix A_inv = inv(A)                          // Inverse
matrix V_inv = invsym(V)                       // Symmetric inverse (preferred for symmetric matrices)
scalar det_A = det(A)                          // Determinant
scalar tr_A = trace(A)                         // Trace
matrix C = A, B                                // Horizontal join
matrix D = A \ B                               // Vertical join
scalar rows = rowsof(A)
scalar cols = colsof(A)

// Eigenvalues (symmetric)
matrix symeigen X V = A          // X=eigenvalues, V=eigenvectors

// Cholesky decomposition (LL' = A)
matrix L = cholesky(A)

// SVD
matrix svd U w V = A

// Correlation matrix from data
matrix accum R = var1 var2 var3, dev
matrix R = corr(R)
```

**Note:** Use `invsym()` instead of `inv()` for symmetric matrices -- more accurate and handles non-positive-definite matrices via generalized inverse.

---

## Special Functions

```stata
factorial(n)          // n! (max n=167; missing for non-integer/negative)
lnfactorial(n)        // ln(n!) -- handles large n (up to 1e+305)
gamma(z)              // Gamma function (gamma(n) = (n-1)! for integers)
lngamma(z)            // ln(|gamma(z)|) -- use instead of ln(gamma()) for large args
digamma(x)            // d/dx lngamma(x) (x > 0)
trigamma(x)           // d^2/dx^2 lngamma(x) (x > 0)
comb(n, k)            // n choose k = n! / (k!(n-k)!)
```

---

## Rounding Functions

| Function | Description | 5.7 | -5.7 |
|----------|-------------|-----|------|
| `int(x)` / `trunc(x)` | Toward zero | 5 | -5 |
| `floor(x)` | Round down | 5 | -6 |
| `ceil(x)` | Round up | 6 | -5 |
| `round(x)` | Nearest integer | 6 | -6 |

### round(x, y) - Round in Units of y
```stata
round(12.3, 5)     // 10 (nearest multiple of 5)
round(12.3, 0.5)   // 12.5
round(17, 2)       // 18
round(value, 0.01) // Two decimal places
```

**Gotcha:** `round()` uses round-to-even for .5 values:
```stata
display round(2.5, 1)   // 2
display round(3.5, 1)   // 4
```

### Practical Rounding Patterns
```stata
gen price_rounded = 5 * floor(price / 5)      // Nearest multiple of 5 (down)
gen age_group = 10 * ceil(age / 10)            // Age bins (round up)
gen bin = 5 * floor(value / 5)                 // Bins of width 5
```

### Floating-Point Precision Warning
```stata
display int(0.3 / 0.1)   // Returns 2, not 3! (0.3/0.1 stored as 2.999...)
// Workaround:
gen safe_round = floor(value + 0.0000001)
```

---

## Practical Calculation Patterns

### Data Transformations
```stata
// Logit / inverse logit
gen logit = ln(p / (1 - p))
gen prob = 1 / (1 + exp(-logit))

// Box-Cox
gen boxcox = (value^lambda - 1) / lambda if lambda != 0
replace boxcox = ln(value) if lambda == 0

// Min-max normalization
egen min_val = min(value)
egen max_val = max(value)
gen normalized = (value - min_val) / (max_val - min_val)
```

### Financial
```stata
gen future_value = principal * (1 + rate)^years
gen present_value = future_value / (1 + rate)^years
gen continuous_value = principal * exp(rate * years)
```

## Best Practices

1. Use `lngamma()` instead of `ln(gamma())` and `lnfactorial()` instead of `ln(factorial())` for large arguments
2. Always `set seed` before random number generation
3. Use `invsym()` for symmetric matrices
4. Use `round(x, 0.01)` for two decimals, not `round(x*100)/100`
5. Use tail functions (`ttail()`, `chi2tail()`) directly rather than `1 - CDF()`
6. Be aware of floating-point precision with `mod()` and rounding
