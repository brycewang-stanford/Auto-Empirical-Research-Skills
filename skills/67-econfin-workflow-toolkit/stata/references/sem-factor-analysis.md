# Structural Equation Modeling and Factor Analysis in Stata

## Table of Contents
1. [The sem Command](#the-sem-command)
2. [Path Diagrams and Model Specification](#path-diagrams-and-model-specification)
3. [Confirmatory Factor Analysis (CFA)](#confirmatory-factor-analysis-cfa)
4. [Measurement Models](#measurement-models)
5. [Structural Models](#structural-models)
6. [Mediation and Indirect Effects](#mediation-and-indirect-effects)
7. [Model Fit Statistics](#model-fit-statistics)
8. [Exploratory Factor Analysis](#exploratory-factor-analysis)
9. [Factor Rotation Methods](#factor-rotation-methods)
10. [Reliability Analysis](#reliability-analysis)
11. [Quick Reference](#quick-reference)

---

## The sem Command

### Basic Syntax

```stata
sem (paths) [if] [in] [weight] [, options]
```

### Path Notation

**Basic Paths:**
```stata
(Y <- X)           // Regression path: Y predicted by X
(Factor -> indicator) // Measurement path: indicator loads on Factor
(X <-> Y)          // Covariance between variables
(X <-> X)          // Variance of variable
```

**Special Symbols:**
```stata
_cons           // Intercept
@value          // Constrain parameter to specific value
@name           // Name a parameter for equality constraints
L.variable      // Lagged variable
*               // Estimate variance/covariance
```

**Examples:**
```stata
// Equivalent to: regress y x1 x2
sem (y <- x1 x2)

// Latent factor F measured by indicators x1, x2, x3
sem (F -> x1 x2 x3)
```

---

## Path Diagrams and Model Specification

```stata
// Estimate model and display path diagram
sem (r_occasp <- f_occasp r_intel f_intel) ///
    (f_occasp <- r_occasp r_intel f_intel)
estat framework

// Standardized path diagram
sem, standardized
estat framework
```

### Model Specification Approaches

```stata
// 1. Command syntax (recommended for reproducibility)
sem (path1) (path2) (path3), options

// 2. SEM Builder (interactive GUI)
sem, builder

// 3. Stored model
estimates store mymodel
estimates restore mymodel
```

---

## Confirmatory Factor Analysis (CFA)

### Single Factor CFA

```stata
webuse sem_2fmm, clear
sem (Ability -> x1 x2 x3 x4), standardized
estat gof, stats(all)
```

**Identification -- need at least 3 indicators per single factor. Fix either factor variance to 1 OR one loading to 1:**
```stata
// Method 1: Fix factor variance to 1 (default)
sem (Ability -> x1 x2 x3 x4), latent(Ability 1)

// Method 2: Fix first loading to 1
sem (Ability -> x1@1 x2 x3 x4)
```

### Multiple Factor CFA

```stata
webuse sem_2fmm, clear

// Two correlated factors (default: factors covary freely)
sem (Visual -> x1 x2 x3) (Textual -> x4 x5 x6)

// Uncorrelated factors
sem (Visual -> x1 x2 x3) (Textual -> x4 x5 x6), ///
    cov(Visual*Textual@0)
```

### Higher-Order Factor Models

```stata
// General intelligence (g) from specific abilities
sem (g -> Verbal Spatial Math) ///
    (Verbal -> vocab reading) ///
    (Spatial -> rotation visualization) ///
    (Math -> arithmetic algebra)
// Second-order factor (g) explains correlations among first-order factors
```

---

## Measurement Models

### Constraints and Standardization

**Parameter Constraints:**
```stata
sem (F -> x1@1 x2 x3)           // Fix x1 loading to 1
sem (F -> x1@a x2@a x3)         // Equality constraint: x1 and x2 loadings equal
sem (F -> x1 x2 x3), var(e.x1@0.5)  // Constrain error variance
sem (F1 -> x1 x2) (F2 -> x3 x4), cov(F1*F2@0)  // Orthogonal factors
```

**Standardized Solutions:**
```stata
sem (...), standardized          // Standardized coefficients
estat stdize: sem                // Post-estimation standardization
```

**Identification rules:**
- t-rule: knowns = p(p+1)/2 >= unknowns (free parameters)
- df = knowns - unknowns >= 0; df > 0 for testable model
- Single factor: min 3 indicators; multiple factors: min 2 per factor
- Must set scale: fix variance=1 OR one loading=1 per factor

---

## Structural Models

### Full SEM Models

```stata
// Measurement + structural: JobSat predicts Performance
sem (JobSat -> sat1 sat2 sat3) ///
    (Performance -> perf1 perf2 perf3) ///
    (Performance <- JobSat), ///
    standardized
```

**Full Example: Theory of Planned Behavior**
```stata
sem (Attitude -> att1 att2 att3) ///
    (Norms -> norm1 norm2 norm3) ///
    (Control -> cont1 cont2 cont3) ///
    (Intention -> int1 int2) ///
    (Behavior <- Intention) ///
    (Intention <- Attitude Norms Control), ///
    standardized method(mlmv)

estat teffects     // All effects (direct, indirect, total)
estat eqgof        // R-squared for endogenous variables
```

### Direct and Indirect Effects

```stata
estat teffects                              // All effects
nlcom (indirect: _b[M:X] * _b[Y:M])       // Specific indirect effect
```

---

## Mediation and Indirect Effects

### Simple Mediation

```stata
// Training -> Motivation -> Performance
sem (motivation <- training) ///
    (performance <- training motivation)

// Test indirect, direct, and total effects
nlcom (indirect: _b[motivation:training] * _b[performance:motivation]) ///
      (direct: _b[performance:training]) ///
      (total: _b[motivation:training] * _b[performance:motivation] + _b[performance:training])
```

**Sobel Test:**
```stata
estat teffects
nlcom (sobel: _b[motivation:training] * _b[performance:motivation]), post
test sobel = 0
```

### Multiple Mediators

```stata
sem (M1 <- X) (M2 <- X) (Y <- X M1 M2)

// Total indirect effect
estat teffects

// Specific indirect effects and their difference
nlcom (via_skills: _b[skills:training] * _b[performance:skills]) ///
      (via_motivation: _b[motivation:training] * _b[performance:motivation]) ///
      (difference: (_b[skills:training] * _b[performance:skills]) - ///
                   (_b[motivation:training] * _b[performance:motivation]))
```

### Bootstrap Confidence Intervals

Bootstrap is preferred for indirect effects (non-normal sampling distribution).

```stata
sem (M <- X) (Y <- X M), vce(bootstrap, reps(1000))
nlcom (indirect: _b[M:X] * _b[Y:M])

// Alternative approach
bootstrap indirect=(_b[M:X]*_b[Y:M]), reps(1000) seed(123): ///
    sem (M <- X) (Y <- X M)
estat bootstrap, percentile
```

---

## Model Fit Statistics

### Understanding Fit Indices

| Index | Good Fit | Acceptable | Description |
|-------|----------|------------|-------------|
| **RMSEA** | < 0.05 | < 0.08 | Root Mean Square Error of Approximation |
| **CFI** | > 0.95 | > 0.90 | Comparative Fit Index |
| **TLI** | > 0.95 | > 0.90 | Tucker-Lewis Index |
| **SRMR** | < 0.05 | < 0.08 | Standardized Root Mean Square Residual |
| **CD** | > 0.95 | > 0.90 | Coefficient of Determination |

```stata
estat gof, stats(all)               // All fit statistics
estat gof, stats(rmsea cfi tli srmr) // Specific indices
```

**Chi-Square caveat:** Almost always significant with large N; rely on fit indices instead.

**AIC/BIC Model Comparison:**
```stata
sem (F -> x1 x2 x3 x4 x5 x6)
estimates store model1

sem (F1 -> x1 x2 x3) (F2 -> x4 x5 x6)
estimates store model2

estimates stats model1 model2
// Difference > 10: strong evidence for better model
```

### Modification Indices

```stata
estat mindices                  // All modification indices
estat mindices, minchi(3.84)    // Only significant (alpha = .05)
estat mindices, minchi(10)      // Only large MIs

// If MI suggests error covariance, add only if theoretically justified:
sem (F -> x1 x2 x3 x4 x5 x6), cov(e.x1*e.x2)
```

---

## Exploratory Factor Analysis

### The factor Command

```stata
factor varlist [, options]
```

**Methods:**
- `pf` (default): Principal factors
- `pcf`: Principal component factors
- `ipf`: Iterated principal factors
- `ml`: Maximum likelihood
- `paf`: Principal axis factoring

```stata
webuse bg2, clear
factor bg2cost1-bg2cost6, factors(2) pcf blanks(0.3)

// Communalities
estat common
// Loading plot
loadingplot, factors(2)
```

### Principal Component Analysis

**PCA vs FA:** PCA explains total variance with linear combinations; FA explains common variance with latent constructs.

```stata
pca varlist

// Example
sysuse auto, clear
foreach v of varlist price mpg weight length {
    egen z_`v' = std(`v')
}
pca z_price z_mpg z_weight z_length

screeplot, yline(1)      // Scree plot with Kaiser line
estat loadings           // Component loadings
predict pc1 pc2, score   // Predict scores for use in regression
```

### Determining Number of Factors

```stata
// 1. Kaiser criterion: keep eigenvalues > 1 (shown in output)
factor varlist

// 2. Scree plot (elbow method)
factor varlist, factors(10)
screeplot

// 3. Parallel analysis (most rigorous)
ssc install paran, replace
paran item1-item10, reps(1000)

// 4. Try multiple and compare interpretability
forvalues k = 1/5 {
    factor varlist, factors(`k') ml
    rotate, promax
    estimates store f`k'
}
```

---

## Factor Rotation Methods

### Orthogonal Rotations

Factors remain uncorrelated after rotation.

```stata
factor varlist, factors(2)
rotate, varimax           // Most common; maximizes variance of squared loadings
rotate, quartimax         // Minimizes factors per variable; may produce general factor
rotate, equamax           // Combination of varimax and quartimax

// blanks(0.3) suppresses small loadings for clarity
rotate, varimax blanks(0.3)
```

### Oblique Rotations

Factors allowed to correlate (more realistic when constructs are related).

```stata
rotate, promax            // Most common oblique
rotate, oblimin           // Direct oblimin

// Compare rotations
estat rotatecompare
```

**Promax produces three matrices:**
- Pattern matrix: unique contribution of each factor
- Structure matrix: total relationship (includes factor correlations)
- Factor correlation matrix

**Choose oblique if:** factors conceptually related or factor correlation > 0.3.

```stata
// Predict factor scores
predict f1 f2 f3, bartlett
regress outcome f1 f2 f3
```

---

## Reliability Analysis

### Cronbach's Alpha

Thresholds: >= 0.70 acceptable, >= 0.80 good, >= 0.90 excellent.

```stata
alpha varlist
```

**Output columns:**
- Item-test correlation: correlation of item with total
- Item-rest correlation: correlation with total excluding that item (preferred)
- Alpha if item deleted: alpha if that item removed

```stata
// Detailed analysis
alpha sat1-sat5, item detail
alpha sat1-sat5, gen(sat_score)   // Generate scale score
alpha sat1-sat5, std              // Standardized alpha (different item scales)
```

### Item Analysis

- Item-rest correlation > 0.30 for good items
- Consider removing items where alpha-if-deleted substantially improves alpha

**Generate Scale Scores:**
```stata
egen satisfaction = rowmean(sat1 sat2 sat4 sat5)
gen sat3_rev = 6 - sat3           // Reverse 5-point scale item
```

**Split-Half Reliability:**
```stata
egen scale1 = rowmean(sat1 sat3 sat5)
egen scale2 = rowmean(sat2 sat4)
corr scale1 scale2
display "Split-half reliability = " 2*r(rho) / (1 + r(rho))
```

**Omega Reliability** (preferred over alpha for ordinal data or unequal loadings):
```stata
ssc install omega, replace
// omega varlist, factors(1)
```

**Multi-Dimensional Scales:**
```stata
alpha extra1-extra5
local alpha_extra = r(alpha)
alpha agree1-agree5
local alpha_agree = r(alpha)
```

---

## Quick Reference

### SEM Commands

```stata
sem (Factor -> x1 x2 x3)                    // CFA
sem (F1 -> x1 x2 x3) (F2 -> x4 x5 x6)     // Multiple factors
sem (Y <- X M) (M <- X)                      // Structural/mediation
nlcom (indirect: _b[M:X] * _b[Y:M])         // Indirect effect
estat gof, stats(all)                         // Fit statistics
estat mindices                                // Modification indices
sem (...), standardized                       // Standardized solution
estat framework                               // Path diagram
```

### Factor Analysis Commands

```stata
factor varlist, factors(k) pcf               // EFA
rotate, varimax                               // Orthogonal rotation
pca varlist                                   // PCA
screeplot                                     // Scree plot
paran varlist                                 // Parallel analysis
predict f1 f2, regression                     // Factor scores
```

### Reliability Commands

```stata
alpha varlist                                 // Cronbach's alpha
alpha varlist, item detail                    // Item analysis
egen scale = rowmean(varlist)                 // Scale score
alpha varlist, gen(scale_score)               // Alpha + generate score
```

### Common Options

```stata
// SEM options
method(ml)           // Maximum likelihood (default)
method(mlmv)         // ML with missing values
vce(robust)          // Robust standard errors
vce(bootstrap)       // Bootstrap SEs
standardized         // Standardized coefficients
cov(e.x1*e.x2)      // Add error covariance

// Factor options
factors(k)           // Number of factors
pcf / ml / ipf       // Extraction method
blanks(0.3)          // Suppress small loadings

// Rotation options
rotate, varimax      // Orthogonal
rotate, promax       // Oblique
```

### Post-Estimation

```stata
// After SEM
estat gof            // Goodness of fit
estat mindices       // Modification indices
estat teffects       // Total/indirect/direct effects
estat eqgof          // Equation-level R-squared
estat framework      // Path diagram

// After factor/pca
estat kmo            // Kaiser-Meyer-Olkin measure
estat anti           // Anti-image correlation matrix
estat common         // Communalities
estat factors        // Factor correlation matrix (oblique)
estat structure      // Structure matrix (oblique)
estat rotatecompare  // Compare rotations
loadingplot          // Plot factor loadings
screeplot            // Scree plot
```

### Best Practices

**SEM:**
1. Start with measurement model (CFA), then add structural paths
2. Check identification before estimation
3. Report multiple fit indices, not just chi-square
4. Use modification indices cautiously -- only add theoretically justified parameters
5. Use bootstrap for mediation analysis

**Factor Analysis:**
1. Sample size: N >= 200 preferred; variable-to-factor ratio >= 5:1
2. Use multiple methods to determine number of factors (parallel analysis preferred)
3. Choose rotation based on theory: oblique if factors likely correlated
4. Examine communalities and cross-loadings

**Reliability:**
1. Report alpha for each scale/subscale
2. Item-rest correlations > 0.30
3. Alpha > 0.90 may indicate item redundancy
4. Alpha assumes tau-equivalence; consider omega for ordinal data

---

## Additional Resources

**User-Written Commands:**
```stata
ssc install paran      // Parallel analysis for factor retention
ssc install polychoric // Polychoric correlations for ordinal data
ssc install omega      // Omega reliability coefficient
```
