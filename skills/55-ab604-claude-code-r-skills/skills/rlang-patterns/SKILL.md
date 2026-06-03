---
name: rlang-patterns
description: rlang metaprogramming patterns for data-masking, injection operators, and dynamic dots. Use when writing functions that use tidy evaluation.
---

# Modern rlang Patterns for Data-Masking

*Metaprogramming framework that powers tidyverse data-masking*

## Core Concepts

**Data-masking** allows R expressions to refer to data frame columns as if they were variables in the environment. rlang provides the metaprogramming framework that powers tidyverse data-masking.

### Key rlang Tools

- **Embracing `{{}}`** - Forward function arguments to data-masking functions
- **Injection `!!`** - Inject single expressions or values
- **Splicing `!!!`** - Inject multiple arguments from a list
- **Dynamic dots** - Programmable `...` with injection support
- **Pronouns `.data`/`.env`** - Explicit disambiguation between data and environment variables

## Function Argument Patterns

### Forwarding with `{{}}`

**Use `{{}}` to forward function arguments to data-masking functions:**

```r
# Single argument forwarding
my_summarise <- function(data, var) {
  data |> dplyr::summarise(mean = mean({{ var }}))
}

# Works with any data-masking expression
mtcars |> my_summarise(cyl)
mtcars |> my_summarise(cyl * am)
mtcars |> my_summarise(.data$cyl)  # pronoun syntax supported
```

### Forwarding `...` (No Special Syntax Needed)

```r
# Simple dots forwarding
my_group_by <- function(.data, ...) {
  .data |> dplyr::group_by(...)
}

# Works with tidy selections too
my_select <- function(.data, ...) {
  .data |> dplyr::select(...)
}

# For single-argument tidy selections, wrap in c()
my_pivot_longer <- function(.data, ...) {
  .data |> tidyr::pivot_longer(c(...))
}
```

### Names Patterns with `.data`

**Use `.data` pronoun for programmatic column access:**

```r
# Single column by name
my_mean <- function(data, var) {
  data |> dplyr::summarise(mean = mean(.data[[var]]))
}

# Usage - completely insulated from data-masking
mtcars |> my_mean("cyl")  # No ambiguity, works like regular function

# Multiple columns with all_of()
my_select_vars <- function(data, vars) {
  data |> dplyr::select(all_of(vars))
}

mtcars |> my_select_vars(c("cyl", "am"))
```

## Injection Operators

### When to Use Each Operator

| Operator | Use Case | Example |
|----------|----------|---------|
| `{{ }}` | Forward function arguments | `summarise(mean = mean({{ var }}))` |
| `!!` | Inject single expression/value | `summarise(mean = mean(!!sym(var)))` |
| `!!!` | Inject multiple arguments | `group_by(!!!syms(vars))` |
| `.data[[]]` | Access columns by name | `mean(.data[[var]])` |

### Advanced Injection with `!!`

```r
# Create symbols from strings
var <- "cyl"
mtcars |> dplyr::summarise(mean = mean(!!sym(var)))

# Inject values to avoid name collisions
df <- data.frame(x = 1:3)
x <- 100
df |> dplyr::mutate(scaled = x / !!x)  # Uses both data and env x

# Use data_sym() for tidyeval contexts (more robust)
mtcars |> dplyr::summarise(mean = mean(!!data_sym(var)))
```

### Splicing with `!!!`

```r
# Multiple symbols from character vector
vars <- c("cyl", "am")
mtcars |> dplyr::group_by(!!!syms(vars))

# Or use data_syms() for tidy contexts
mtcars |> dplyr::group_by(!!!data_syms(vars))

# Splice lists of arguments
args <- list(na.rm = TRUE, trim = 0.1)
mtcars |> dplyr::summarise(mean = mean(cyl, !!!args))
```

## Dynamic Dots Patterns

### Using `list2()` for Dynamic Dots Support

```r
my_function <- function(...) {
  # Collect with list2() instead of list() for dynamic features
  dots <- list2(...)
  # Process dots...
}

# Enables these features:
my_function(a = 1, b = 2)           # Normal usage
my_function(!!!list(a = 1, b = 2))  # Splice a list
my_function("{name}" := value)      # Name injection
my_function(a = 1, )               # Trailing commas OK
```

### Name Injection with Glue Syntax

```r
# Basic name injection
name <- "result"
list2("{name}" := 1)  # Creates list(result = 1)

# In function arguments with {{
my_mean <- function(data, var) {
  data |> dplyr::summarise("mean_{{ var }}" := mean({{ var }}))
}

mtcars |> my_mean(cyl)        # Creates column "mean_cyl"
mtcars |> my_mean(cyl * am)   # Creates column "mean_cyl * am"

# Allow custom names with englue()
my_mean <- function(data, var, name = englue("mean_{{ var }}")) {
  data |> dplyr::summarise("{name}" := mean({{ var }}))
}

# User can override default
mtcars |> my_mean(cyl, name = "cylinder_mean")
```

## Pronouns for Disambiguation

### `.data` and `.env` Best Practices

```r
# Explicit disambiguation prevents masking issues
cyl <- 1000  # Environment variable

mtcars |> dplyr::summarise(
  data_cyl = mean(.data$cyl),    # Data frame column
  env_cyl = mean(.env$cyl),      # Environment variable
  ambiguous = mean(cyl)          # Could be either (usually data wins)
)

# Use in loops and programmatic contexts
vars <- c("cyl", "am")
for (var in vars) {
  result <- mtcars |> dplyr::summarise(mean = mean(.data[[var]]))
  print(result)
}
```

## Programming Patterns

### Bridge Patterns

**Converting between data-masking and tidy selection behaviors:**

```r
# across() as selection-to-data-mask bridge
my_group_by <- function(data, vars) {
  data |> dplyr::group_by(across({{ vars }}))
}

# Works with tidy selection
mtcars |> my_group_by(starts_with("c"))

# across(all_of()) as names-to-data-mask bridge
my_group_by <- function(data, vars) {
  data |> dplyr::group_by(across(all_of(vars)))
}

mtcars |> my_group_by(c("cyl", "am"))
```

### Transformation Patterns

```r
# Transform single arguments by wrapping
my_mean <- function(data, var) {
  data |> dplyr::summarise(mean = mean({{ var }}, na.rm = TRUE))
}

# Transform dots with across()
my_means <- function(data, ...) {
  data |> dplyr::summarise(across(c(...), ~ mean(.x, na.rm = TRUE)))
}

# Manual transformation (advanced)
my_means_manual <- function(.data, ...) {
  vars <- enquos(..., .named = TRUE)
  vars <- purrr::map(vars, ~ expr(mean(!!.x, na.rm = TRUE)))
  .data |> dplyr::summarise(!!!vars)
}
```

## Error-Prone Patterns to Avoid

### Don't Use These Deprecated/Dangerous Patterns

```r
# Avoid - String parsing and eval (security risk)
var <- "cyl"
code <- paste("mean(", var, ")")
eval(parse(text = code))  # Dangerous!

# Good - Symbol creation and injection
!!sym(var)  # Safe symbol injection

# Avoid - get() in data mask (name collisions)
with(mtcars, mean(get(var)))  # Collision-prone

# Good - Explicit injection or .data
with(mtcars, mean(!!sym(var)))  # Safe
# or
mtcars |> summarise(mean(.data[[var]]))  # Even safer
```

### Common Mistakes

```r
# Don't use {{ }} on non-arguments
my_func <- function(x) {
  x <- force(x)  # x is now a value, not an argument
  quo(mean({{ x }}))  # Wrong! Captures value, not expression
}

# Don't mix injection styles unnecessarily
# Pick one approach and stick with it:
# Either: embrace pattern
my_func <- function(data, var) data |> summarise(mean = mean({{ var }}))
# Or: defuse-and-inject pattern
my_func <- function(data, var) {
  var <- enquo(var)
  data |> summarise(mean = mean(!!var))
}
```

## Package Development with rlang

### Import Strategy

```r
# In DESCRIPTION:
Imports: rlang

# In NAMESPACE, import specific functions:
importFrom(rlang, enquo, enquos, expr, !!!, :=)

# Or import key functions:
#' @importFrom rlang := enquo enquos
```

### Documentation Tags

```r
#' @param var <[`data-masked`][dplyr::dplyr_data_masking]> Column to summarize
#' @param ... <[`dynamic-dots`][rlang::dyn-dots]> Additional grouping variables
#' @param cols <[`tidy-select`][dplyr::dplyr_tidy_select]> Columns to select
```

### Testing rlang Functions

```r
# Test data-masking behavior
test_that("function supports data masking", {
  result <- my_function(mtcars, cyl)
  expect_equal(names(result), "mean_cyl")

  # Test with expressions
  result2 <- my_function(mtcars, cyl * 2)
  expect_true("mean_cyl * 2" %in% names(result2))
})

# Test injection behavior
test_that("function supports injection", {
  var <- "cyl"
  result <- my_function(mtcars, !!sym(var))
  expect_true(nrow(result) > 0)
})
```

This modern rlang approach enables clean, safe metaprogramming while maintaining the intuitive data-masking experience users expect from tidyverse functions.
