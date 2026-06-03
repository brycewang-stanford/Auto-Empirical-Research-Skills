---
name: tdd-workflow
description: Test-driven development workflow for R using testthat. Use when writing new features, fixing bugs, or refactoring code. Enforces test-first development with 80%+ coverage.
---

# Test-Driven Development Workflow for R

This skill ensures all R code development follows TDD principles with comprehensive test coverage using testthat.

## When to Activate

- Writing new functions or features
- Fixing bugs or issues
- Refactoring existing code
- Adding new model types
- Creating data processing pipelines
- Building Shiny components

## Getting Started

Initialize testing infrastructure for your package:

```r
# Set up testthat (Edition 3)
usethis::use_testthat(3)

# Create a test file for an existing source file
usethis::use_test("function_name")

# Or create test and source file together
usethis::use_r("function_name")
usethis::use_test("function_name")
```

## Core Principles

### 1. Tests BEFORE Code

ALWAYS write tests first, then implement code to make tests pass.

### 2. Coverage Requirements

- Minimum 80% coverage (unit + integration)
- 100% coverage for statistical calculations
- 100% coverage for data validation
- All edge cases covered
- Error scenarios tested

### 3. Test Types

Tests follow a three-level hierarchy: **File → Test → Expectation**

#### Unit Tests

Individual functions and utilities:

```r
test_that("rescale01 normalizes to [0, 1] range", {
  expect_equal(rescale01(c(0, 5, 10)), c(0, 0.5, 1))
  expect_equal(rescale01(c(-10, 0, 10)), c(0, 0.5, 1))
})

test_that("rescale01 handles edge cases", {
  expect_equal(rescale01(c(5, 5, 5)), c(NaN, NaN, NaN))
  expect_equal(rescale01(numeric(0)), numeric(0))
  expect_equal(rescale01(c(0, NA, 10)), c(0, NA, 1))
})
```

#### Integration Tests

Function interactions and workflows:

```r
test_that("data pipeline produces expected output", {
  raw_data <- read_fixture("sample_input.csv")

  result <- raw_data |>
    clean_data() |>
    transform_features() |>
    summarize_results()

  expect_s3_class(result, "tbl_df")
  expect_named(result, c("group", "mean", "sd", "n"))
  expect_true(all(result$n > 0))
})
```

#### Snapshot Tests

For complex outputs that are hard to specify:

```r
test_that("model summary format is stable", {
  model <- fit_model(test_data)
  expect_snapshot(print(summary(model)))
})

test_that("error messages are informative", {
  expect_snapshot(
    validate_input(invalid_data),
    error = TRUE
  )
})
```

**Snapshot workflow:**
```r
# Review snapshot changes
testthat::snapshot_review("test_name")

# Accept snapshot changes
testthat::snapshot_accept("test_name")
```

Snapshots are stored in `tests/testthat/_snaps/` directory.

#### BDD Alternative (Optional)

For behavior-driven development, use `describe()` and `it()`:

```r
describe("matrix()", {
  it("can be multiplied by a scalar", {
    m1 <- matrix(1:4, 2, 2)
    m2 <- m1 * 2
    expect_equal(matrix(c(2, 4, 6, 8), 2, 2), m2)
  })

  it("can be transposed", {
    m <- matrix(1:4, 2, 2)
    expect_equal(t(m), matrix(c(1, 3, 2, 4), 2, 2))
  })
})
```

**Key distinction:** "describe() verifies you implement the right things, test_that() ensures you do things right."

## Test Design Principles

### Self-Sufficient Tests

Each test should contain all setup, execution, and teardown code. Tests must be independent and runnable in isolation without relying on ambient state or prior test execution.

```r
# GOOD: Self-contained
test_that("function works with specific data", {
  data <- tibble(x = 1:10, y = rnorm(10))  # Setup
  result <- my_function(data)               # Execute
  expect_equal(nrow(result), 10)            # Assert
})

# BAD: Depends on external state
# setup_data <- tibble(...)  # Created outside test
test_that("function works", {
  result <- my_function(setup_data)  # Relies on external data
  expect_equal(nrow(result), 10)
})
```

### Duplication Over Factoring

Repetition is acceptable in tests—duplicate setup code rather than extracting it elsewhere. Clarity outweighs avoiding duplication.

```r
# GOOD: Duplicated but clear
test_that("clean_data handles missing values", {
  data <- tibble(x = c(1, NA, 3), y = c(4, 5, 6))
  result <- clean_data(data)
  expect_equal(nrow(result), 2)
})

test_that("clean_data handles invalid values", {
  data <- tibble(x = c(1, -999, 3), y = c(4, 5, 6))
  result <- clean_data(data, invalid = -999)
  expect_equal(nrow(result), 2)
})

# ACCEPTABLE: Each test is self-contained and readable
```

### Plan for Failure

Write tests assuming they'll fail and require debugging. Make logic explicit and obvious. Run tests in fresh R sessions independently.

### Use devtools::load_all()

During development, prefer `devtools::load_all()` over `library()`. This:
- Exposes unexported functions for testing
- Automatically attaches testthat
- Eliminates unnecessary `library()` calls in tests
- Simulates package loading without installation

## testthat Edition 3

Edition 3 provides improved snapshot testing, better diffs via waldo, unified condition handling, parallel execution support, and byte-compiled code compatibility for mocking.

### Deprecated Patterns → Modern Alternatives

```r
# DEPRECATED: context() calls
context("Data validation")  # Remove - filename serves this purpose

# DEPRECATED: expect_equivalent()
expect_equivalent(x, y)
# MODERN:
expect_equal(x, y, ignore_attr = TRUE)

# DEPRECATED: with_mock()
with_mock(external_call = function() "mocked", {
  result <- my_function()
})
# MODERN:
local_mocked_bindings(
  external_call = function() "mocked"
)
result <- my_function()

# DEPRECATED: expect_is()
expect_is(x, "data.frame")
# MODERN:
expect_s3_class(x, "data.frame")
```

### Initialize Edition 3

In `DESCRIPTION`, ensure:
```
Config/testthat/edition: 3
```

Or initialize with:
```r
usethis::use_testthat(3)
```

## Essential Expectations Reference

### Equality & Identity

```r
expect_equal(x, y)              # With numeric tolerance
expect_equal(x, y, tolerance = 0.001)
expect_equal(x, y, ignore_attr = TRUE)
expect_identical(x, y)          # Exact match required
expect_all_equal(x)             # Every element equal (v3.3.0+)
```

### Conditions

```r
expect_error(code)
expect_error(code, "pattern")
expect_error(code, class = "validation_error")
expect_warning(code)
expect_no_warning(code)
expect_message(code)
expect_no_message(code)
```

### Collections & Sets

```r
expect_setequal(x, y)          # Same elements, any order
expect_contains(set, element)  # Subset relationship (v3.2.0+)
expect_in(element, set)        # Membership check (v3.2.0+)
expect_disjoint(set1, set2)    # No overlap (v3.3.0+)
expect_named(x, c("a", "b"))   # Named vector/list
```

### Type & Structure

```r
expect_type(x, "double")
expect_s3_class(x, "data.frame")
expect_s4_class(x, "S4Class")
expect_r6_class(x, "R6Class")
expect_shape(matrix, c(2, 3))  # Matrix/array dimensions (v3.3.0+)
expect_length(x, 10)
```

### Logical

```r
expect_true(x)
expect_false(x)
expect_all_true(x)             # Every element TRUE (v3.3.0+)
expect_all_false(x)            # Every element FALSE (v3.3.0+)
```

### Other Useful Expectations

```r
expect_null(x)
expect_invisible(result)
expect_output(print(x), "pattern")
expect_snapshot(complex_output)
```

## File Organization

Tests mirror your package structure:

```
tests/
├── testthat/
│   ├── test-validation.R      # Tests for R/validation.R
│   ├── test-processing.R      # Tests for R/processing.R
│   ├── test-models.R          # Tests for R/models.R
│   ├── test-output.R          # Tests for R/output.R
│   ├── helper-fixtures.R      # Shared functions (sourced before tests)
│   ├── setup-database.R       # Setup code (runs during R CMD check)
│   ├── helper-expectations.R  # Custom expectations
│   └── fixtures/              # Static test data files
│       ├── sample_input.csv
│       └── expected_output.rds
└── testthat.R                 # Test runner
```

### File Types

- **`test-*.R`** - Actual test files (paired with source files)
- **`helper-*.R`** - Shared utility functions, sourced before tests run
- **`setup-*.R`** - Setup code that runs only during `R CMD check`
- **`fixtures/`** - Static test data, accessed via `test_path("fixtures/file")`

Access fixtures:
```r
test_path("fixtures", "sample_data.csv")
```

## TDD Workflow Steps

### Step 1: Define Expected Behavior

Document what the function should do:

```r
# Function: calculate_ci
# Purpose: Calculate bootstrap confidence intervals
# Inputs:
#   - data: numeric vector
#   - conf_level: confidence level (default 0.95)
#   - n_boot: number of bootstrap samples (default 1000)
# Outputs:
#   - Named numeric vector with lower and upper bounds
# Edge cases:
#   - Handle NA values
#   - Error on non-numeric input
#   - Error on empty input
```

### Step 2: Write Failing Tests

```r
# tests/testthat/test-calculate_ci.R
library(testthat)

test_that("calculate_ci returns correct structure", {
  set.seed(123)
  result <- calculate_ci(1:100)

  expect_type(result, "double")
  expect_named(result, c("lower", "upper"))
  expect_true(result["lower"] < result["upper"])
})

test_that("calculate_ci respects confidence level", {
  set.seed(123)
  ci_95 <- calculate_ci(1:100, conf_level = 0.95)
  ci_99 <- calculate_ci(1:100, conf_level = 0.99)

  # 99% CI should be wider
  expect_true(ci_99["upper"] - ci_99["lower"] > ci_95["upper"] - ci_95["lower"])
})

test_that("calculate_ci handles NA values", {
  set.seed(123)
  result <- calculate_ci(c(1:100, NA, NA))

  expect_false(any(is.na(result)))
})

test_that("calculate_ci validates inputs", {
  expect_error(calculate_ci("not numeric"), class = "validation_error")
  expect_error(calculate_ci(numeric(0)), class = "validation_error")
  expect_error(calculate_ci(1:10, conf_level = 1.5), class = "validation_error")
})
```

### Step 3: Run Tests (They Should Fail)

```r
devtools::test()
# ✖ calculate_ci returns correct structure
# ✖ calculate_ci respects confidence level
# ✖ calculate_ci handles NA values
# ✖ calculate_ci validates inputs
```

### Step 4: Implement Minimal Code

```r
# R/calculate_ci.R

#' Calculate Bootstrap Confidence Interval
#'
#' @param x Numeric vector
#' @param conf_level Confidence level (default 0.95)
#' @param n_boot Number of bootstrap samples (default 1000)
#' @return Named numeric vector with lower and upper bounds
#' @export
calculate_ci <- function(x, conf_level = 0.95, n_boot = 1000) {
  # Validate inputs
  if (!is.numeric(x)) {
    cli::cli_abort("{.arg x} must be numeric", class = "validation_error")
  }
  if (length(x) == 0) {
    cli::cli_abort("{.arg x} cannot be empty", class = "validation_error")
  }
  if (conf_level <= 0 || conf_level >= 1) {
    cli::cli_abort("{.arg conf_level} must be between 0 and 1", class = "validation_error")
  }

  # Remove NA values
  x <- x[!is.na(x)]

  # Bootstrap
  boot_means <- replicate(n_boot, mean(sample(x, replace = TRUE)))

  # Calculate quantiles
  alpha <- 1 - conf_level
  c(
    lower = unname(quantile(boot_means, alpha / 2)),
    upper = unname(quantile(boot_means, 1 - alpha / 2))
  )
}
```

### Step 5: Run Tests Again

```r
devtools::test()
# ✔ calculate_ci returns correct structure
# ✔ calculate_ci respects confidence level
# ✔ calculate_ci handles NA values
# ✔ calculate_ci validates inputs
```

### Step 6: Refactor

Improve while keeping tests green:

```r
# Extract validation to helper
validate_ci_inputs <- function(x, conf_level) {
  if (!is.numeric(x)) {
    cli::cli_abort("{.arg x} must be numeric", class = "validation_error")
  }
  if (length(x) == 0) {
    cli::cli_abort("{.arg x} cannot be empty", class = "validation_error")
  }
  if (conf_level <= 0 || conf_level >= 1) {
    cli::cli_abort("{.arg conf_level} must be between 0 and 1", class = "validation_error")
  }
}

calculate_ci <- function(x, conf_level = 0.95, n_boot = 1000) {
  validate_ci_inputs(x, conf_level)

  x <- x[!is.na(x)]
  boot_means <- replicate(n_boot, mean(sample(x, replace = TRUE)))

  alpha <- 1 - conf_level
  c(
    lower = unname(quantile(boot_means, alpha / 2)),
    upper = unname(quantile(boot_means, 1 - alpha / 2))
  )
}
```

### Step 7: Verify Coverage

```r
covr::package_coverage()
# calculate_ci.R: 100%
```

## Testing Patterns

### Testing Data Transformations

```r
test_that("clean_data removes invalid rows", {
  input <- tibble(
    id = 1:4,
    value = c(1, NA, 3, -999)
  )

  result <- clean_data(input, invalid_value = -999)

  expect_equal(nrow(result), 2)
  expect_equal(result$id, c(1, 3))
  expect_false(anyNA(result$value))
})
```

### Testing Statistical Functions

```r
test_that("weighted_mean matches manual calculation", {
  x <- c(1, 2, 3)
  w <- c(1, 2, 1)

  result <- weighted_mean(x, w)
  expected <- sum(x * w) / sum(w)  # (1 + 4 + 3) / 4 = 2

  expect_equal(result, expected)
})
```

### Testing with Fixtures

```r
# helper-fixtures.R
read_fixture <- function(name) {
  path <- testthat::test_path("fixtures", name)
  readr::read_csv(path, show_col_types = FALSE)
}

# test-pipeline.R
test_that("pipeline handles real data", {
  input <- read_fixture("sample_data.csv")
  result <- process_pipeline(input)

  expect_snapshot(result)
})
```

### Mocking External Dependencies

```r
test_that("fetch_data handles API errors", {
  # Mock the API call
  local_mocked_bindings(
    httr2_request = function(...) {
      stop("API unavailable")
    }
  )

  expect_error(
    fetch_data("endpoint"),
    "API unavailable"
  )
})
```

### Using withr for Cleanup

Use `withr` functions to manage temporary state with automatic restoration:

```r
test_that("function respects options", {
  # Temporarily set options
  withr::local_options(list(digits = 2))

  result <- format_number(3.14159)
  expect_equal(result, "3.14")
})

test_that("function writes to temp file", {
  # Create temp file that's automatically cleaned up
  tmp <- withr::local_tempfile(lines = c("line 1", "line 2"))

  result <- process_file(tmp)
  expect_equal(result$n_lines, 2)
})

test_that("function uses custom environment variable", {
  # Temporarily set env var
  withr::local_envvar(MY_VAR = "test_value")

  result <- get_config()
  expect_equal(result$my_var, "test_value")
})
```

## Test Data Strategies

Choose the appropriate approach for your testing needs:

### 1. Constructor Functions

Create data on-demand with helper functions:

```r
# helper-data.R
make_sample_data <- function(n = 100) {
  tibble(
    id = 1:n,
    group = sample(c("A", "B"), n, replace = TRUE),
    value = rnorm(n)
  )
}

# test-analysis.R
test_that("analysis handles grouped data", {
  data <- make_sample_data(n = 50)
  result <- analyze_groups(data)
  expect_s3_class(result, "tbl_df")
})
```

### 2. Local Functions with Cleanup

Handle side effects using withr:

```r
test_that("function reads CSV correctly", {
  # Create temp file with cleanup
  tmp <- withr::local_tempfile(fileext = ".csv")
  write.csv(mtcars, tmp, row.names = FALSE)

  result <- read_and_process(tmp)
  expect_equal(nrow(result), 32)
})
```

### 3. Static Fixtures

Store data files in `fixtures/` directory:

```r
# Store in: tests/testthat/fixtures/sample_data.csv

test_that("function handles real data format", {
  path <- test_path("fixtures", "sample_data.csv")
  data <- read_csv(path)
  result <- process_data(data)
  expect_true(all(result$valid))
})
```

## Common Testing Mistakes to Avoid

### WRONG: Testing Implementation Details

```r
# Don't test internal state
expect_equal(obj$internal_cache, expected_cache)
```

### CORRECT: Test Behavior

```r
# Test observable behavior
expect_equal(get_result(obj), expected_result)
```

### WRONG: Brittle Tests

```r
# Breaks on any output change
expect_equal(as.character(result), "Mean: 5.234567890")
```

### CORRECT: Flexible Assertions

```r
# Robust to formatting changes
expect_equal(result$mean, 5.23, tolerance = 0.01)
```

### WRONG: Dependent Tests

```r
test_that("creates data", { global_data <<- create() })
test_that("uses data", { process(global_data) })  # Depends on previous!
```

### CORRECT: Independent Tests

```r
test_that("creates and uses data", {
  data <- create()
  result <- process(data)
  expect_true(is_valid(result))
})
```

### WRONG: Modifying Tests to Pass

```r
# When a test fails, don't change the test (unless it's wrong)
test_that("function returns 42", {
  expect_equal(my_function(), 42)  # Test fails
})

# DON'T DO THIS:
test_that("function returns 41", {
  expect_equal(my_function(), 41)  # Changed to pass - WRONG!
})
```

### CORRECT: Fix the Implementation

```r
# Fix the code to match expected behavior
test_that("function returns 42", {
  expect_equal(my_function(), 42)  # Test fails
})

# Fix my_function() implementation instead
```

## When Tests Fail

1. **Do NOT modify tests** to make them pass (unless the test is wrong)
2. **Fix the implementation** to match expected behavior
3. **Add more tests** if the failure reveals missing coverage
4. **Update snapshots** only if the change is intentional

```r
# Review and accept snapshot changes
testthat::snapshot_review("test_name")
testthat::snapshot_accept("test_name")
```

## Coverage Verification

```r
# Run coverage report
covr::package_coverage()

# Interactive HTML report
covr::report()

# Check specific thresholds
cov <- covr::package_coverage()
pct <- covr::percent_coverage(cov)
if (pct < 80) {
  stop("Coverage below 80%: ", round(pct, 1), "%")
}

# In testthat.R or as a coverage check
covr::package_coverage(
  type = "all",
  line_coverage = 0.80,
  function_coverage = 0.80
)
```

## Debugging & Development

### Running Tests at Different Scales

```r
# Micro: Interactive development
devtools::load_all()
expect_equal(my_function(1), 1)  # Direct expectation

# Mezzo: Single file
testthat::test_file("tests/testthat/test-validation.R")
# RStudio: Ctrl/Cmd+Shift+T

# Macro: Full suite
devtools::test()
devtools::check()  # Full package validation
```

### Test Reporters

```r
# Find slow tests
devtools::test(reporter = "slow")

# Progress reporter (verbose)
devtools::test(reporter = "progress")

# Test execution order independence
devtools::test(shuffle = TRUE)
```

### Continuous Testing

```r
# Watch mode - auto-run on file changes
testthat::auto_test_package()
```

### Parallel Execution (Edition 3)

Edition 3 supports parallel test execution for faster runs on multi-core systems.

## Running Tests

```r
# All tests
devtools::test()

# All tests (keyboard shortcut)
# RStudio: Ctrl/Cmd+Shift+T

# With coverage
covr::package_coverage()

# Specific file
testthat::test_file("tests/testthat/test-validation.R")

# Watch mode
testthat::auto_test_package()

# Verbose output
devtools::test(reporter = "progress")

# Find slow tests
devtools::test(reporter = "slow")

# Test independence
devtools::test(shuffle = TRUE)

# Full package check
devtools::check()
```

## Success Metrics

- 80%+ code coverage achieved
- All tests passing
- No skipped tests
- Fast execution (< 30s for unit tests)
- Tests catch bugs before production
- Confident refactoring enabled
- Tests run independently in any order
- Clear, descriptive test names
- Each test validates one concept

---

**Remember**: Tests are not optional. They are the safety net that enables confident refactoring, rapid development, and production reliability. Write them FIRST.
