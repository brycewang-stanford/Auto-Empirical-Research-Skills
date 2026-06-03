---
name: r-package-development
description: R package development guide covering dependencies, API design, testing, and documentation. Use when developing R packages.
---

# R Package Development Decision Guide

*Dependencies, API design, testing, documentation, and best practices for R packages*

## Dependency Strategy

### When to Add Dependencies vs Base R

```r
# Add dependency when:
# - Significant functionality gain
# - Maintenance burden reduction
# - User experience improvement
# - Complex implementation (regex, dates, web)

# Use base R when:
# - Simple utility functions
# - Package will be widely used (minimize deps)
# - Dependency is large for small benefit
# - Base R solution is straightforward

# Example decisions:
str_detect(x, "pattern")    # Worth stringr dependency
length(x) > 0              # Don't need purrr for this
parse_dates(x)             # Worth lubridate dependency
x + 1                      # Don't need dplyr for this
```

### Tidyverse Dependency Guidelines

```r
# Core tidyverse (usually worth it):
dplyr     # Complex data manipulation
purrr     # Functional programming, parallel
stringr   # String manipulation
tidyr     # Data reshaping

# Specialized tidyverse (evaluate carefully):
lubridate # If heavy date manipulation
forcats   # If many categorical operations
readr     # If specific file reading needs
ggplot2   # If package creates visualizations

# Heavy dependencies (use sparingly):
tidyverse # Meta-package, very heavy
shiny     # Only for interactive apps
```

### Dependency Specification in DESCRIPTION

```
# Strong dependencies (required)
Imports:
    dplyr (>= 1.1.0),
    rlang (>= 1.0.0)

# Suggested dependencies (optional)
Suggests:
    testthat (>= 3.0.0),
    knitr,
    rmarkdown

# Enhanced functionality (optional but loaded if available)
Enhances:
    data.table
```

## API Design Patterns

### Function Design Strategy

```r
# Modern tidyverse API patterns

# 1. Use .by for per-operation grouping
my_summarise <- function(.data, ..., .by = NULL) {
  # Support modern grouped operations
}

# 2. Use {{ }} for user-provided columns
my_select <- function(.data, cols) {
  .data |> select({{ cols }})
}

# 3. Use ... for flexible arguments
my_mutate <- function(.data, ..., .by = NULL) {
  .data |> mutate(..., .by = {{ .by }})
}

# 4. Return consistent types (tibbles, not data.frames)
my_function <- function(.data) {
  result |> tibble::as_tibble()
}
```

### Input Validation Strategy

```r
# Validation level by function type:

# User-facing functions - comprehensive validation
user_function <- function(x, threshold = 0.5) {
  # Check all inputs thoroughly
  if (!is.numeric(x)) stop("x must be numeric")
  if (!is.numeric(threshold) || length(threshold) != 1) {
    stop("threshold must be a single number")
  }
  # ... function body
}

# Internal functions - minimal validation
.internal_function <- function(x, threshold) {
  # Assume inputs are valid (document assumptions)
  # Only check critical invariants
  # ... function body
}

# Package functions with vctrs - type-stable validation
safe_function <- function(x, y) {
  x <- vec_cast(x, double())
  y <- vec_cast(y, double())
  # Automatic type checking and coercion
}
```

## Error Handling Patterns

```r
# Good error messages - specific and actionable
if (length(x) == 0) {
  cli::cli_abort(
    "Input {.arg x} cannot be empty.",
    "i" = "Provide a non-empty vector."
  )
}

# Include function name in errors
validate_input <- function(x, call = caller_env()) {
  if (!is.numeric(x)) {
    cli::cli_abort("Input must be numeric", call = call)
  }
}

# Use consistent error styling
# cli package for user-friendly messages
# rlang for developer tools
```

### Error Classes

```r
# Custom error classes for programmatic handling
my_error <- function(message, ..., call = caller_env()) {
  cli::cli_abort(
    message,
    ...,
    class = "my_package_error",
    call = call
  )
}

# Specific error types
validation_error <- function(message, ..., call = caller_env()) {
  cli::cli_abort(
    message,
    ...,
    class = c("validation_error", "my_package_error"),
    call = call
  )
}
```

## When to Create Internal vs Exported Functions

### Export Function When

```r
# Export when:
# - Users will call it directly
# - Other packages might want to extend it
# - Part of the core package functionality
# - Stable API that won't change often

# Example: main data processing functions
#' @export
process_data <- function(.data, ...) {
  # Comprehensive input validation
  # Full documentation required
  # Stable API contract
}
```

### Keep Function Internal When

```r
# Keep internal when:
# - Implementation detail that may change
# - Only used within package
# - Complex implementation helpers
# - Would clutter user-facing API

# Example: helper functions (no @export)
.validate_input <- function(x, y) {
  # Minimal documentation
  # Can change without breaking users
  # Assume inputs are pre-validated
}

# Naming convention: prefix with . for internal functions
.compute_metrics <- function(data) { ... }
```

## Testing and Documentation Strategy

### Testing Levels

```r
# Unit tests - individual functions
test_that("function handles edge cases", {
  expect_equal(my_func(c()), expected_empty_result)
  expect_error(my_func(NULL), class = "my_error_class")
})

# Integration tests - workflow combinations
test_that("pipeline works end-to-end", {
  result <- data |>
    step1() |>
    step2() |>
    step3()
  expect_s3_class(result, "expected_class")
})

# Property-based tests for package functions
test_that("function properties hold", {
  # Test invariants across many inputs
})
```

### Test File Organization

```
tests/
  testthat/
    test-validation.R      # Input validation tests
    test-processing.R      # Core processing tests
    test-output.R          # Output format tests
    test-integration.R     # End-to-end tests
    helper-fixtures.R      # Shared test fixtures
  testthat.R              # Test runner
```

### Snapshot Testing

```r
# For complex outputs that are hard to specify exactly
test_that("summary output is correct", {
  expect_snapshot(summary(my_object))
})

# For error messages
test_that("errors are informative",
  expect_snapshot(my_function(bad_input), error = TRUE)
})
```

### Documentation Priorities

```r
# Must document:
# - All exported functions
# - Complex algorithms or formulas
# - Non-obvious parameter interactions
# - Examples of typical usage

# Can skip documentation:
# - Simple internal helpers
# - Obvious parameter meanings
# - Functions that just call other functions
```

### roxygen2 Documentation

```r
#' Process and summarize data
#'
#' @description
#' Takes a data frame and computes summary statistics
#' for specified variables.
#'
#' @param data A data frame or tibble.
#' @param vars <[`tidy-select`][dplyr::dplyr_tidy_select]> Columns to summarize.
#' @param .by <[`data-masking`][dplyr::dplyr_data_masking]> Optional grouping variable.
#'
#' @return A tibble with summary statistics.
#'
#' @examples
#' mtcars |> process_data(mpg, .by = cyl)
#'
#' @export
process_data <- function(data, vars, .by = NULL) {
  # ...
}
```

## Package Structure

### Recommended Directory Layout

```
mypackage/
  DESCRIPTION
  NAMESPACE
  LICENSE
  README.md
  R/
    utils.R           # Internal utilities
    validation.R      # Input validation
    core.R            # Core functionality
    methods.R         # S3/S7 methods
    zzz.R             # .onLoad, .onAttach
  man/                # Generated by roxygen2
  tests/
    testthat/
    testthat.R
  vignettes/
    getting-started.Rmd
  inst/
    extdata/          # Example data files
  data/               # Package data (lazy-loaded)
  data-raw/           # Scripts to create package data
```

### DESCRIPTION Best Practices

```
Package: mypackage
Title: What The Package Does (One Line)
Version: 0.1.0
Authors@R:
    person("First", "Last", email = "email@example.com",
           role = c("aut", "cre"))
Description: A longer description that spans multiple lines.
    Use four spaces for continuation lines.
License: MIT + file LICENSE
Encoding: UTF-8
Roxygen: list(markdown = TRUE)
RoxygenNote: 7.2.3
Imports:
    dplyr (>= 1.1.0),
    rlang (>= 1.0.0)
Suggests:
    testthat (>= 3.0.0)
Config/testthat/edition: 3
```

## Release Checklist

```r
# Before release:
devtools::check()         # Must pass with 0 errors, warnings, notes
devtools::test()          # All tests pass
devtools::document()      # Documentation up to date
urlchecker::url_check()   # All URLs valid
spelling::spell_check_package()  # No typos

# Update version
usethis::use_version("minor")  # or "major", "patch"

# Update NEWS.md with changes

# Final checks
devtools::check(remote = TRUE, manual = TRUE)
```

## Common Package Development Mistakes

```r
# Avoid - Using library() in package code
library(dplyr)  # Never in package code!

# Good - Use namespace qualification
dplyr::filter(data, x > 0)

# Or import in NAMESPACE via roxygen2
#' @importFrom dplyr filter mutate

# Avoid - Modifying global state
options(my_option = TRUE)  # Side effect!

# Good - Restore state if you must modify
old_opts <- options(my_option = TRUE)
on.exit(options(old_opts), add = TRUE)

# Avoid - Hardcoded paths
read.csv("/home/user/data.csv")

# Good - Use system.file for package data
system.file("extdata", "data.csv", package = "mypackage")
```
