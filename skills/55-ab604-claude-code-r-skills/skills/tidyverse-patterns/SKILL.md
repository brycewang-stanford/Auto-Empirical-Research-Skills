---
name: tidyverse-patterns
description: Modern tidyverse patterns for R including pipes, joins, grouping, purrr, and stringr. Use when writing tidyverse R code.
---

# Modern Tidyverse Patterns

*Best practices for modern tidyverse development with dplyr 1.1+ and R 4.3+*

## Core Principles

1. **Use modern tidyverse patterns** - Prioritize dplyr 1.1+ features, native pipe, and current APIs
2. **Profile before optimizing** - Use profvis and bench to identify real bottlenecks
3. **Write readable code first** - Optimize only when necessary and after profiling
4. **Follow tidyverse style guide** - Consistent naming, spacing, and structure

## Pipe Usage (`|>` not `%>%`)

- **Always use native pipe `|>` instead of magrittr `%>%`**
- R 4.3+ provides all needed features

```r
# Good - Modern native pipe
data |>
  filter(year >= 2020) |>
  summarise(mean_value = mean(value))

# Avoid - Legacy magrittr pipe
data %>%
  filter(year >= 2020) %>%
  summarise(mean_value = mean(value))
```

## Join Syntax (dplyr 1.1+)

- **Use `join_by()` instead of character vectors for joins**
- **Support for inequality, rolling, and overlap joins**

```r
# Good - Modern join syntax
transactions |>
  inner_join(companies, by = join_by(company == id))

# Good - Inequality joins
transactions |>
  inner_join(companies, join_by(company == id, year >= since))

# Good - Rolling joins (closest match)
transactions |>
  inner_join(companies, join_by(company == id, closest(year >= since)))

# Avoid - Old character vector syntax
transactions |>
  inner_join(companies, by = c("company" = "id"))
```

## Join Quality Control

- **Declare cardinality with `relationship` to validate join assumptions**
- **Use `unmatched = "error"` to catch unexpected non-matches**
- **Use `na_matches = "never"` to prevent silent NA joins**
- **Use `tidylog::` prefix interactively to verify join results**

```r
# Validate 1:1 relationship — errors if violated
inner_join(x, y, by = join_by(id),
  relationship = "one-to-one")

# Validate many-to-one (left has duplicates, right does not)
left_join(transactions, companies, by = join_by(company == id),
  relationship = "many-to-one")

# Ensure all rows from left match something in right
inner_join(x, y, by = join_by(id),
  unmatched = "error")

# Prevent NA values from matching each other silently
left_join(x, y, by = join_by(id),
  na_matches = "never")

# Combine for strict joins
inner_join(x, y, by = join_by(id),
  relationship = "one-to-one",
  unmatched = "error",
  na_matches = "never")

# Interactive verification with tidylog
# tidylog prints a summary of rows matched/dropped
tidylog::inner_join(x, y, by = join_by(id))
```

## Data Masking and Tidy Selection

- **Understand the difference between data masking and tidy selection**
- **Use `{{}}` (embrace) for function arguments**
- **Use `.data[[]]` for character vectors**

```r
# Data masking functions: arrange(), filter(), mutate(), summarise()
# Tidy selection functions: select(), relocate(), across()

# Function arguments - embrace with {{}}
my_summary <- function(data, group_var, summary_var) {
  data |>
    group_by({{ group_var }}) |>
    summarise(mean_val = mean({{ summary_var }}))
}

# Character vectors - use .data[[]]
for (var in names(mtcars)) {
  mtcars |> count(.data[[var]]) |> print()
}

# Multiple columns - use across()
data |>
  summarise(across({{ summary_vars }}, ~ mean(.x, na.rm = TRUE)))
```

## Modern Grouping and Column Operations

- **Use `.by` for per-operation grouping (dplyr 1.1+)**
- **Use `pick()` for column selection inside data-masking functions**
- **Use `across()` for applying functions to multiple columns**
- **Use `reframe()` for multi-row summaries**

```r
# Good - Per-operation grouping (always returns ungrouped)
data |>
  summarise(mean_value = mean(value), .by = category)

# Good - Multiple grouping variables
data |>
  summarise(total = sum(revenue), .by = c(company, year))

# Good - pick() for column selection
data |>
  summarise(
    n_x_cols = ncol(pick(starts_with("x"))),
    n_y_cols = ncol(pick(starts_with("y")))
  )

# Good - across() for applying functions
data |>
  summarise(across(where(is.numeric), mean, .names = "mean_{.col}"), .by = group)

# Good - reframe() for multi-row results
data |>
  reframe(quantiles = quantile(x, c(0.25, 0.5, 0.75)), .by = group)

# Avoid - Old persistent grouping pattern
data |>
  group_by(category) |>
  summarise(mean_value = mean(value)) |>
  ungroup()
```

## NA-Safe Row Filtering

- **Use `filter_out()` instead of negating conditions** — negation (`!condition`) silently drops NAs
- **Use `when_any()` and `when_all()` for multi-column OR/AND filters (dplyr 1.2+)**

```r
# Problem: negation silently drops rows where condition is NA
filter(data, !(value < 0))       # drops rows where value is NA — silent!

# Good - filter_out() passes NAs through safely
filter_out(data, value < 0)      # rows where value is NA are kept

# Good - when_any() for OR across columns (dplyr 1.2+)
filter(data, when_any(x, y, z, \(col) col > 0))  # any column > 0

# Good - when_all() for AND across columns
filter(data, when_all(x, y, z, \(col) !is.na(col)))  # no NAs in any

# Avoid - verbose base patterns
filter(data, !(value < 0) | is.na(value))   # workaround, not idiomatic
```

## Recoding and Conditional Updates

- **Use `replace_when()` for in-place conditional updates** — avoids `case_when()` with `.default = x`
- **Use `case_when()` with `.unmatched = "error"` when all cases should be handled**

```r
# Good - replace_when() for in-place updates (type-stable, NAs unaffected)
mutate(data, status = replace_when(status,
  value < 0  ~ "negative",
  value == 0 ~ "zero"
))

# Avoid - case_when() requires restating the variable in .default
mutate(data, status = case_when(
  value < 0  ~ "negative",
  value == 0 ~ "zero",
  .default   = status    # repetitive
))

# Good - case_when() with strict exhaustiveness check
mutate(data, grade = case_when(
  score >= 90 ~ "A",
  score >= 80 ~ "B",
  score >= 70 ~ "C",
  .unmatched  = "error"  # error if any row falls through
))
```

## Serialization

- **Use `qs2` for fast serialization** — successor to `qs`, not backwards-compatible

```r
# Good - qs2 (use .qs2 extension)
qs2::qs_save(object, "data/results.qs2")
object <- qs2::qs_read("data/results.qs2")

# Avoid - older qs package
qs::qsave(object, "data/results.qs")   # outdated
```

## Modern purrr Patterns

- **Use `map() |> list_rbind()`** instead of superseded `map_dfr()`
- **Use `walk()` for side effects** (file writing, plotting)
- **Use `in_parallel()` for scaling** across cores

```r
# Modern data frame row binding (purrr 1.0+)
models <- data_splits |>
  map(\(split) train_model(split)) |>
  list_rbind()  # Replaces map_dfr()

# Column binding
summaries <- data_list |>
  map(\(df) get_summary_stats(df)) |>
  list_cbind()  # Replaces map_dfc()

# Side effects with walk()
plots <- walk2(data_list, plot_names, \(df, name) {
  p <- ggplot(df, aes(x, y)) + geom_point()
  ggsave(name, p)
})

# Parallel processing (purrr 1.1.0+)
library(mirai)
daemons(4)
results <- large_datasets |>
  map(in_parallel(expensive_computation))
daemons(0)
```

## String Manipulation with stringr

- **Use stringr over base R string functions**
- **Consistent `str_` prefix and string-first argument order**
- **Pipe-friendly and vectorized by design**

```r
# Good - stringr (consistent, pipe-friendly)
text |>
  str_to_lower() |>
  str_trim() |>
  str_replace_all("pattern", "replacement") |>
  str_extract("\\d+")

# Common patterns
str_detect(text, "pattern")     # vs grepl("pattern", text)
str_extract(text, "pattern")    # vs complex regmatches()
str_replace_all(text, "a", "b") # vs gsub("a", "b", text)
str_split(text, ",")            # vs strsplit(text, ",")
str_length(text)                # vs nchar(text)
str_sub(text, 1, 5)             # vs substr(text, 1, 5)

# String combination and formatting
str_c("a", "b", "c")            # vs paste0()
str_glue("Hello {name}!")       # templating
str_pad(text, 10, "left")       # padding
str_wrap(text, width = 80)      # text wrapping

# Case conversion
str_to_lower(text)              # vs tolower()
str_to_upper(text)              # vs toupper()
str_to_title(text)              # vs tools::toTitleCase()

# Pattern helpers for clarity
str_detect(text, fixed("$"))    # literal match
str_detect(text, regex("\\d+")) # explicit regex
str_detect(text, coll("e", locale = "fr")) # collation

# Avoid - inconsistent base R functions
grepl("pattern", text)          # argument order varies
regmatches(text, regexpr(...))  # complex extraction
gsub("a", "b", text)           # different arg order
```

## Vectorization and Performance

```r
# Good - vectorized operations
result <- x + y

# Good - Type-stable purrr functions
map_dbl(data, mean)    # always returns double
map_chr(data, class)   # always returns character

# Avoid - Type-unstable base functions
sapply(data, mean)     # might return list or vector

# Avoid - explicit loops for simple operations
result <- numeric(length(x))
for(i in seq_along(x)) {
  result[i] <- x[i] + y[i]
}
```

## Common Anti-Patterns to Avoid

### Legacy Patterns

```r
# Avoid - Old pipe
data %>% function()

# Avoid - Old join syntax
inner_join(x, y, by = c("a" = "b"))

# Avoid - Implicit type conversion
sapply()  # Use map_*() instead

# Avoid - String manipulation in data masking
mutate(data, !!paste0("new_", var) := value)
# Use across() or other approaches instead
```

### Performance Anti-Patterns

```r
# Avoid - Growing objects in loops
result <- c()
for(i in 1:n) {
  result <- c(result, compute(i))  # Slow!
}

# Good - Pre-allocate
result <- vector("list", n)
for(i in 1:n) {
  result[[i]] <- compute(i)
}

# Better - Use purrr
result <- map(1:n, compute)
```

## Migration from Old Patterns

### From Base R to Modern Tidyverse

```r
# Data manipulation
subset(data, condition)          -> filter(data, condition)
data[order(data$x), ]           -> arrange(data, x)
aggregate(x ~ y, data, mean)    -> summarise(data, mean(x), .by = y)

# Functional programming
sapply(x, f)                    -> map(x, f)  # type-stable
lapply(x, f)                    -> map(x, f)

# String manipulation
grepl("pattern", text)          -> str_detect(text, "pattern")
gsub("old", "new", text)        -> str_replace_all(text, "old", "new")
substr(text, 1, 5)              -> str_sub(text, 1, 5)
nchar(text)                     -> str_length(text)
strsplit(text, ",")             -> str_split(text, ",")
paste0(a, b)                    -> str_c(a, b)
tolower(text)                   -> str_to_lower(text)
```

### From Old to New Tidyverse Patterns

```r
# Pipes
data %>% function()             -> data |> function()

# Grouping (dplyr 1.1+)
group_by(data, x) |>
  summarise(mean(y)) |>
  ungroup()                     -> summarise(data, mean(y), .by = x)

# Column selection
across(starts_with("x"))        -> pick(starts_with("x"))  # for selection only

# Joins
by = c("a" = "b")              -> by = join_by(a == b)

# Multi-row summaries
summarise(data, x, .groups = "drop") -> reframe(data, x)

# Data reshaping
gather()/spread()               -> pivot_longer()/pivot_wider()

# String separation (tidyr 1.3+)
separate(col, into = c("a", "b")) -> separate_wider_delim(col, delim = "_", names = c("a", "b"))
extract(col, into = "x", regex)   -> separate_wider_regex(col, patterns = c(x = regex))
```

### Superseded purrr Functions (purrr 1.0+)

```r
map_dfr(x, f)                   -> map(x, f) |> list_rbind()
map_dfc(x, f)                   -> map(x, f) |> list_cbind()
map2_dfr(x, y, f)               -> map2(x, y, f) |> list_rbind()
pmap_dfr(list, f)               -> pmap(list, f) |> list_rbind()
imap_dfr(x, f)                  -> imap(x, f) |> list_rbind()

# For side effects
walk(x, write_file)             # instead of for loops
walk2(data, paths, write_csv)   # multiple arguments
```
