---
name: r-style-guide
description: R style guide covering naming conventions, spacing, layout, and function design best practices. Use when writing R code.
---

# R Style Guide & Function Writing Best Practices

*Consistent naming, spacing, structure, and function design for R code*

## Function Writing Best Practices

### Structure and Style

```r
# Good function structure
rescale01 <- function(x) {
  rng <- range(x, na.rm = TRUE, finite = TRUE)
  (x - rng[1]) / (rng[2] - rng[1])
}

# Use type-stable outputs
map_dbl()   # returns numeric vector
map_chr()   # returns character vector
map_lgl()   # returns logical vector
```

### Naming and Arguments

```r
# Good naming: snake_case for variables/functions
calculate_mean_score <- function(data, score_col) {
  # Function body
}

# Prefix non-standard arguments with .
my_function <- function(.data, ...) {
  # Reduces argument conflicts
}
```

## Style Guide Essentials

### Object Names

- **Use snake_case for all names**
- **Variable names = nouns, function names = verbs**
- **Avoid dots except for S3 methods**

```r
# Good
day_one
calculate_mean
user_data

# Avoid
DayOne
calculate.mean
userData
```

### Spacing and Layout

```r
# Good spacing
x[, 1]
mean(x, na.rm = TRUE)
if (condition) {
  action()
}

# Pipe formatting
data |>
  filter(year >= 2020) |>
  group_by(category) |>
  summarise(
    mean_value = mean(value),
    count = n()
  )
```

### Assignment

```r
# Good - Use <- for assignment
x <- 5

# Avoid - = for assignment (use only for function arguments)
x = 5  # Less clear intent
```

### Indentation and Line Length

- Use 2 spaces for indentation (never tabs)
- Keep lines under 80 characters when possible
- For long function calls, put each argument on its own line

```r
# Good - Long function call
do_something_complicated(
  data = my_data,
  arg_one = value_one,
  arg_two = value_two,
  arg_three = value_three
)

# Good - Long pipe chain
result <- data |>
  filter(year >= 2020) |>
  mutate(
    new_var = old_var * 2,
    another_var = str_to_lower(text_var)
  ) |>
  summarise(
    mean_value = mean(value),
    .by = category
  )
```

### Comments

```r
# Good - Comments explain WHY, not WHAT
# Calculate running average to smooth noise in sensor data
running_avg <- zoo::rollmean(values, k = 5)

# Avoid - Comments that just repeat the code
# Add 1 to x
x <- x + 1
```

### File Organization

```r
# 1. Load packages at the top
library(dplyr)
library(ggplot2)

# 2. Source any helper files
source("R/helpers.R")

# 3. Define constants
MAX_ITERATIONS <- 1000
DEFAULT_THRESHOLD <- 0.05

# 4. Define functions
process_data <- function(data) {
  # ...
}

# 5. Main script logic (if not a package)
main <- function() {
  data <- read_csv("data/input.csv")
  result <- process_data(data)
  write_csv(result, "data/output.csv")
}
```

## Function Design Guidelines

### Single Responsibility

```r
# Good - Each function does one thing
read_and_validate <- function(path) {
  data <- read_csv(path)
  validate_columns(data)
  data
}

validate_columns <- function(data) {
  required <- c("id", "value", "date")
  missing <- setdiff(required, names(data))
  if (length(missing) > 0) {
    stop("Missing columns: ", paste(missing, collapse = ", "))
  }
}

# Avoid - Function does too many things
do_everything <- function(path, output_path, ...) {
  # Reads, validates, transforms, models, plots, writes...
}
```

### Return Values

```r
# Good - Explicit return for complex functions
calculate_metrics <- function(data) {
  metrics <- list(
    mean = mean(data$value),
    sd = sd(data$value),
    n = nrow(data)
  )
  return(metrics)
}

# Good - Implicit return for simple functions
square <- function(x) {
  x^2
}

# Avoid - Return in the middle without good reason
process <- function(x) {
  if (is.null(x)) return(NULL)  # OK - early exit
  # ... more code
  result  # Implicit return at end
}
```

### Error Handling

Prefer `cli::cli_abort()` over `stop()` for user-facing errors. Structure messages as a problem statement followed by context bullets.

```r
# Good - cli::cli_abort() with structured bullets
# Bullet types: x = error detail, i = info/hint, ! = warning
validate_input <- function(x, threshold = 0) {
  if (!is.numeric(x)) {
    cli::cli_abort(c(
      "{.arg x} must be numeric.",
      x = "You supplied {.cls {class(x)}}.",
      i = "Convert with {.fn as.numeric} first."
    ))
  }
  if (any(x < threshold)) {
    cli::cli_abort(c(
      "{.arg x} must be >= {threshold}.",
      x = "{sum(x < threshold)} value{?s} below threshold.",
      i = "Set {.arg threshold} to adjust the lower bound."
    ))
  }
}

# Good - reference argument names, functions, and classes with inline markup
cli::cli_abort(c(
  "{.fn my_func} requires a data frame.",
  x = "{.arg data} is {.cls {class(data)}}, not {.cls data.frame}.",
  i = "Did you mean to call {.fn as.data.frame}?"
))

# Avoid - stop() with string concatenation
stop("`x` must be numeric, not ", typeof(x), call. = FALSE)
```

**Inline markup tokens:**
- `{.arg x}` — argument name (backtick-formatted)
- `{.fn foo}` — function name
- `{.cls {class(x)}}` — class name
- `{.val {value}}` — literal value
- `{?s}` — pluralisation (`value{?s}` → "value" or "values")

### Default Arguments

```r
# Good - Sensible defaults
summarise_data <- function(data, na.rm = TRUE, digits = 2) {
  # ...
}

# Good - NULL default for optional arguments
filter_data <- function(data, min_value = NULL, max_value = NULL) {
  if (!is.null(min_value)) {
    data <- filter(data, value >= min_value)
  }
  if (!is.null(max_value)) {
    data <- filter(data, value <= max_value)
  }
  data
}
```

## Tidyverse API Conventions

### Data-First Argument

```r
# Good - Data as first argument for piping
my_transform <- function(data, var, threshold = 0.5) {
  data |>
    filter({{ var }} > threshold)
}

# Usage
data |> my_transform(value, threshold = 0.8)
```

### Prefixed Non-Standard Arguments

```r
# Good - Prefix with . to avoid conflicts
group_summary <- function(.data, ..., .by = NULL) {
  .data |>
    summarise(..., .by = {{ .by }})
}
```

### Consistent Return Types

```r
# Good - Always return tibble
my_function <- function(data) {
  result <- data |>
    # processing...
    filter(!is.na(value))

  tibble::as_tibble(result)
}
```

## Common Style Mistakes

### Avoid These Patterns

```r
# Avoid - Inconsistent spacing
x<-1+2  # No spaces
x <- 1 + 2  # Correct

# Avoid - Unnecessary parentheses
if ((x > 0)) {}  # Extra parens
if (x > 0) {}    # Correct

# Avoid - Using T/F instead of TRUE/FALSE
if (x == T) {}     # T can be overwritten
if (x == TRUE) {}  # Correct

# Avoid - Semicolons to separate statements
x <- 1; y <- 2  # Hard to read
x <- 1          # Correct
y <- 2

# Avoid - attach() - creates ambiguity
attach(mtcars)
mean(mpg)  # Which mpg?
detach(mtcars)

# Correct - Be explicit
mean(mtcars$mpg)
# or
with(mtcars, mean(mpg))
# or
mtcars |> pull(mpg) |> mean()
```
