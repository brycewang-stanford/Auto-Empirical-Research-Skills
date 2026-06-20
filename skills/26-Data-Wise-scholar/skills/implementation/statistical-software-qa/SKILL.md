---


name: statistical-software-qa
description: Quality assurance and testing protocols for statistical software


---

# Statistical Software QA

**Quality assurance patterns and testing strategies for statistical R packages**

Use this skill when working on: R package testing, numerical accuracy validation, reference implementation comparison, edge case identification, statistical correctness verification, or software quality assurance for methodology packages.

---

## Testing Philosophy

### Statistical Software is Different

Unlike typical software where "correct output" is clear, statistical software must:

1. **Produce statistically correct results** - Not just bug-free
2. **Handle edge cases gracefully** - Small samples, boundary conditions
3. **Maintain numerical precision** - Floating-point considerations
4. **Match known results** - Verification against published examples
5. **Degrade gracefully** - Informative errors, not crashes

### Testing Pyramid for Statistical Packages

```
                    ▲
                   /│\
                  / │ \
                 /  │  \
                /Manual│\        <- Human review of outputs
               /  Tests │ \
              /─────────────\
             /  Integration  \   <- Cross-function workflows
            /    Tests        \
           /───────────────────\
          /  Statistical Tests  \  <- Correctness verification
         /                       \
        /─────────────────────────\
       /     Reference Tests       \  <- Match known results
      /                             \
     /───────────────────────────────\
    /        Unit Tests               \  <- Individual functions
   /___________________________________\
```

---

## Unit Testing Patterns

### Pattern 1: Known Value Tests

Test against analytically derivable results:

```r
test_that("indirect effect equals a*b for simple mediation", {
  # Create data where we know true values
  set.seed(42)
  n <- 10000
  x <- rnorm(n)
  m <- 0.5 * x + rnorm(n, sd = 0.1)  # a = 0.5
  y <- 0.3 * m + rnorm(n, sd = 0.1)  # b = 0.3

  result <- mediate(y ~ x + m, mediator = "m", data = data.frame(x, m, y))

  # True indirect = 0.5 * 0.3 = 0.15
  expect_equal(result$indirect, 0.15, tolerance = 0.02)
})
```

### Pattern 2: Boundary Condition Tests

```r
test_that("handles minimum sample size", {
  # Minimum viable sample
  small_data <- data.frame(
    x = c(0, 0, 1, 1),
    m = c(0, 1, 1, 2),
    y = c(1, 2, 2, 3)
  )

  # Should work without error

  expect_no_error(mediate(y ~ x + m, mediator = "m", data = small_data))

  # Should warn about low power
  expect_warning(
    mediate(y ~ x + m, mediator = "m", data = small_data),
    "sample size"
  )
})
```

### Pattern 3: Equivalence Tests

```r
test_that("bootstrap CI contains delta method CI asymptotically", {
  set.seed(123)
  data <- simulate_mediation(n = 5000, a = 0.3, b = 0.4)

  boot_result <- mediate(data, method = "bootstrap", R = 2000)
  delta_result <- mediate(data, method = "delta")

  # CIs should be similar for large n
  expect_equal(boot_result$ci, delta_result$ci, tolerance = 0.05)
})
```

---

## Reference Implementation Testing

### Strategy: Compare Against Published Results

```r
test_that("matches Imai et al. (2010) JOBS II example",
  # Load reference data from mediation package
  data("jobs", package = "mediation")

  # Our implementation
  our_result <- our_mediate(
    outcome = job_seek ~ treat + econ_hard + sex + age,
    mediator = job_disc ~ treat + econ_hard + sex + age,
    data = jobs
  )

  # Published results (from paper Table 2)
  expected_acme <- 0.015
  expected_acme_ci <- c(-0.004, 0.035)

  expect_equal(our_result$acme, expected_acme, tolerance = 0.005)
  expect_equal(our_result$acme_ci, expected_acme_ci, tolerance = 0.01)
})
```

### Cross-Package Validation

```r
test_that("matches lavaan for SEM-based mediation", {
  data <- simulate_mediation(n = 1000)

  # Our implementation
  our_result <- our_mediate(data)

  # lavaan implementation
  library(lavaan)
  model <- '
    m ~ a*x
    y ~ b*m + c*x
    indirect := a*b
  '
  lavaan_fit <- sem(model, data = data)
  lavaan_indirect <- parameterEstimates(lavaan_fit)[
    parameterEstimates(lavaan_fit)$label == "indirect", "est"
  ]

  expect_equal(our_result$indirect, lavaan_indirect, tolerance = 0.01)
})
```

---

## Statistical Correctness Tests

### Coverage Probability Tests

Verify confidence intervals achieve nominal coverage:

```r
test_that("95% CI achieves nominal coverage", {
  set.seed(42)
  n_sims <- 1000
  true_indirect <- 0.15
  coverage <- 0

  for (i in 1:n_sims) {
    data <- simulate_mediation(n = 200, a = 0.5, b = 0.3)
    result <- mediate(data, conf.level = 0.95)

    if (result$ci[1] <= true_indirect && true_indirect <= result$ci[2]) {
      coverage <- coverage + 1
    }
  }

  coverage_rate <- coverage / n_sims

  # Coverage should be between 93% and 97% (accounting for MC error)
  expect_gte(coverage_rate, 0.93)
  expect_lte(coverage_rate, 0.97)
})
```

### Bias Tests

```r
test_that("estimator is approximately unbiased", {
  set.seed(123)
  n_sims <- 500
  true_indirect <- 0.2
  estimates <- numeric(n_sims)

  for (i in 1:n_sims) {
    data <- simulate_mediation(n = 500, a = 0.5, b = 0.4)
    estimates[i] <- mediate(data)$indirect
  }

  # Mean should be close to true value
  bias <- mean(estimates) - true_indirect
  expect_lt(abs(bias), 0.02)  # Less than 2% bias
})
```

### Type I Error Tests

```r
test_that("maintains nominal Type I error under null", {
  set.seed(456)
  n_sims <- 1000
  rejections <- 0

  for (i in 1:n_sims) {
    # Null: no indirect effect (a = 0)
    data <- simulate_mediation(n = 200, a = 0, b = 0.5)
    result <- mediate(data, conf.level = 0.95)

    # Reject if CI excludes 0
    if (result$ci[1] > 0 || result$ci[2] < 0) {
      rejections <- rejections + 1
    }
  }

  type1_rate <- rejections / n_sims

  # Should be close to 5%
  expect_lt(type1_rate, 0.07)  # Allow some MC error
})
```

---

## Numerical Precision Testing

### Stability Under Scaling

```r
test_that("results invariant to variable scaling", {
  data <- simulate_mediation(n = 500)

  # Original scale
  result1 <- mediate(data)

  # Scale variables by 1000
  data_scaled <- data
  data_scaled$y <- data$y * 1000
  data_scaled$m <- data$m * 1000
  result2 <- mediate(data_scaled)

  # Standardized effects should match
  expect_equal(
    result1$indirect / (sd(data$y)),
    result2$indirect / (sd(data_scaled$y)),
    tolerance = 1e-10
  )
})
```

### Extreme Values

```r
test_that("handles extreme correlations", {
  set.seed(789)

  # Nearly collinear
  x <- rnorm(100)
  m <- x + rnorm(100, sd = 0.001)  # r ≈ 0.9999
  y <- m + rnorm(100, sd = 0.1)

  data <- data.frame(x, m, y)

  # Should warn about collinearity
  expect_warning(mediate(data), "collinear|singular")
})

test_that("handles near-zero variance", {
  data <- data.frame(
    x = c(rep(0, 99), 1),  # Almost constant
    m = rnorm(100),
    y = rnorm(100)
  )

  # Should handle gracefully
  expect_error(
    mediate(data),
    "variance|constant"
  )
})
```

---

## Edge Case Identification

### Edge Case Checklist

- [ ] **Sample size**: n = 3, 4, 10, 30, 100, 1000, 10000
- [ ] **Effect sizes**: 0, very small (0.01), medium (0.3), large (0.8), 1.0
- [ ] **Correlations**: 0, near-zero, high (>0.9), perfect (1.0)
- [ ] **Missing data**: None, 1%, 10%, 50%
- [ ] **Outliers**: None, 1 extreme, 5%
- [ ] **Variable types**: Continuous, binary, categorical
- [ ] **Model fit**: Perfect, good, poor

### Systematic Edge Case Generation

```r
#' Generate Edge Case Test Suite
#'
#' @return List of edge case datasets
generate_edge_cases <- function() {
  list(
    # Minimal sample
    minimal = data.frame(
      x = c(0, 1, 0, 1),
      m = c(0, 0.5, 0.5, 1),
      y = c(0, 0.3, 0.3, 0.6)
    ),

    # Zero effect
    null_effect = {
      set.seed(1)
      n <- 100
      data.frame(
        x = rnorm(n),
        m = rnorm(n),  # No relationship with x
        y = rnorm(n)   # No relationship with m
      )
    },

    # Perfect mediation
    perfect = {
      x <- c(0, 0, 1, 1, 2, 2)
      m <- x  # Perfect a path
      y <- m  # Perfect b path
      data.frame(x, m, y)
    },

    # High collinearity
    collinear = {
      set.seed(2)
      x <- rnorm(100)
      m <- x + rnorm(100, sd = 0.01)
      y <- m + rnorm(100)
      data.frame(x, m, y)
    },

    # Outliers
    with_outliers = {
      set.seed(3)
      n <- 100
      x <- c(rnorm(n-2), 10, -10)
      m <- 0.5 * x + c(rnorm(n-2), 20, -20)
      y <- 0.3 * m + rnorm(n)
      data.frame(x, m, y)
    },

    # Missing data
    with_missing = {
      set.seed(4)
      n <- 100
      x <- rnorm(n)
      m <- 0.5 * x + rnorm(n)
      y <- 0.3 * m + rnorm(n)
      # Introduce 10% missing
      m[sample(n, 10)] <- NA
      y[sample(n, 10)] <- NA
      data.frame(x, m, y)
    }
  )
}

# Run all edge cases
test_that("handles all edge cases", {
  edge_cases <- generate_edge_cases()

  for (name in names(edge_cases)) {
    expect_no_error(
      tryCatch(
        mediate(edge_cases[[name]]),
        warning = function(w) NULL  # Warnings OK
      ),
      info = paste("Edge case:", name)
    )
  }
})
```

---

## Performance Testing

### Benchmarking

```r
test_that("meets performance requirements", {
  skip_on_cran()  # Skip during CRAN checks

  data <- simulate_mediation(n = 1000)

  # Point estimate should be fast
  time_point <- system.time({
    mediate(data, method = "delta")
  })["elapsed"]
  expect_lt(time_point, 0.1)  # < 100ms

  # Bootstrap should be reasonable
  time_boot <- system.time({
    mediate(data, method = "bootstrap", R = 1000)
  })["elapsed"]
  expect_lt(time_boot, 10)  # < 10s for 1000 bootstraps
})
```

### Memory Testing

```r
test_that("memory usage is reasonable", {
  skip_on_cran()

  # Large dataset
  data <- simulate_mediation(n = 100000)

  mem_before <- pryr::mem_used()
  result <- mediate(data)
  mem_after <- pryr::mem_used()

  mem_increase <- as.numeric(mem_after - mem_before) / 1e6  # MB
  expect_lt(mem_increase, 100)  # Less than 100MB increase
})
```

---

## Test Organization

### Recommended Test Structure

```
tests/
├── testthat/
│   ├── test-mediate.R           # Main function tests
│   ├── test-mediate-bootstrap.R # Bootstrap-specific
│   ├── test-mediate-delta.R     # Delta method-specific
│   ├── test-numerical.R         # Numerical precision
│   ├── test-edge-cases.R        # Edge cases
│   ├── test-reference.R         # Reference implementation
│   ├── test-coverage.R          # Statistical coverage
│   └── helper-simulate.R        # Test helpers
├── testthat.R
└── reference-results/           # Saved reference results
    ├── jobs-example.rds
    └── known-values.rds
```

### Test Tagging

```r
test_that("coverage probability (slow)", {
  skip_on_cran()
  skip_if_not(Sys.getenv("RUN_SLOW_TESTS") == "true")

  # ... slow coverage test ...
})
```

---

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/R-CMD-check.yaml
name: R-CMD-check

on: [push, pull_request]

jobs:
  R-CMD-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: r-lib/actions/setup-r@v2
      - uses: r-lib/actions/setup-r-dependencies@v2
      - uses: r-lib/actions/check-r-package@v2

  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: r-lib/actions/setup-r@v2
      - uses: r-lib/actions/setup-r-dependencies@v2
      - name: Test coverage
        run: covr::codecov()
        shell: Rscript {0}

  slow-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - uses: r-lib/actions/setup-r@v2
      - uses: r-lib/actions/setup-r-dependencies@v2
      - name: Run slow tests
        run: |
          Sys.setenv(RUN_SLOW_TESTS = "true")
          testthat::test_local()
        shell: Rscript {0}
```

---

## QA Checklist

### Pre-Release Checklist

- [ ] All unit tests pass
- [ ] Reference tests match published results
- [ ] Coverage > 80%
- [ ] No R CMD check warnings
- [ ] Edge cases handled gracefully
- [ ] Performance benchmarks met
- [ ] Documentation examples run
- [ ] Vignette builds without error
- [ ] NEWS.md updated
- [ ] Version number incremented

### Statistical Validation Template

```markdown
## Statistical Validation Report

**Package**: [name] v[version]
**Date**: [date]
**Validator**: [name]

### Coverage Probability (95% CI)

| Scenario | N | True Effect | Observed Coverage | Pass |
|----------|---|-------------|-------------------|------|
| Small sample | 50 | 0.15 | 94.2% | Yes |
| Medium sample | 200 | 0.15 | 95.1% | Yes |
| Large sample | 1000 | 0.15 | 94.8% | Yes |
| Null effect | 200 | 0 | 95.3% | Yes |

### Bias Assessment

| Scenario | True | Mean Estimate | Bias | Pass |
|----------|------|---------------|------|------|
| a=0.5, b=0.3 | 0.15 | 0.151 | 0.001 | Yes |
| a=0.1, b=0.1 | 0.01 | 0.012 | 0.002 | Yes |

### Reference Comparison

| Reference | Our Result | Difference | Pass |
|-----------|------------|------------|------|
| Imai et al. Table 2 | Match | <0.001 | Yes |
| lavaan output | Match | <0.001 | Yes |
```

---

## References

### R Package Testing

- Wickham, H. (2011). testthat: Get started with testing. *The R Journal*
- Wickham, H., & Bryan, J. (2023). *R Packages* (Testing chapter)

### Statistical Software Validation

- FDA Guidance for Industry: Statistical Software Validation
- Altman, M., et al. (2004). Numerical Issues in Statistical Computing

### Quality Assurance

- McCullough, B. D. (1999). Assessing the reliability of statistical software
- Keeling, K. B., & Pavur, R. J. (2007). Statistical accuracy of spreadsheet software

---

**Version**: 1.0.0
**Created**: 2025-12-09
**Domain**: Quality assurance for statistical R packages
**Target**: MediationVerse ecosystem and similar methodology packages
