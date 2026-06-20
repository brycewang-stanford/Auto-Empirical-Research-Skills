# R Coding Standards for Research

> Every R skill in this suite follows these standards.

## Style

- **tidyverse style guide** — snake_case, pipe operator, consistent spacing
- Use the native pipe `|>` (R 4.1+) unless a package requires magrittr `%>%`
- Maximum line length: 80 characters (for readability in Quarto documents)

## Package Management

- All packages loaded via `renv` — never install.packages() in analysis scripts
- Package loading happens in `R/00_setup.R` or in the `_targets.R` pipeline definition
- Use `library()` not `require()` — fail loudly if a package is missing
- Never use `library(tidyverse)` in production code — load specific packages: `library(dplyr)`, `library(ggplot2)`, etc.

## Reproducibility

- **Set seed** at the top of any script that uses randomization: `set.seed(42)` (or project-specific seed documented in decision log)
- **Session info** captured at end of every pipeline run
- **renv::snapshot()** after any package change
- **No hardcoded paths** — use `here::here()` for project-relative paths
- **No setwd()** — ever

## Function Design (for targets pipeline)

- Each analysis step is a **function** that takes input and returns output
- Functions live in `R/` directory, organized by pipeline stage
- Functions are **pure** where possible (same input → same output)
- Side effects (file writing) happen in dedicated write functions, not analysis functions
- Every function has a clear, descriptive name: `clean_survey_data()` not `clean()`

## Data Handling

- Raw data read from `data/raw/` using `readr::read_csv()`, `haven::read_sav()`, `readxl::read_excel()`, etc.
- Processed data saved to `data/processed/` as `.rds` (R-native) or `.csv` (interoperable)
- Large intermediate results cached by `targets` — don't manually save/load
- Use `tibble` not `data.frame`

## Variable Naming in Analysis Code

- Use construct names from the codebook, not generic names
- `brand_authenticity` not `x1`
- `purchase_intention` not `dv`
- Factor levels should be meaningful: `c("low", "medium", "high")` not `c(1, 2, 3)`
- Prefix computed variables: `z_` for standardized, `log_` for log-transformed, `c_` for centered

## Commenting

- **Why, not what.** The code shows what; comments explain why.
- Every analysis choice that could be questioned gets a comment with rationale
- Reference hypotheses: `# H2: Brand authenticity → purchase intention via perceived value`
- Reference pre-registration: `# Per pre-registration: listwise deletion for missing data`
- Reference codebook: `# brand_auth: 5-item scale, alpha = .89, see codebook`

## Error Handling

- Use `stopifnot()` or `assertthat::assert_that()` for data validation assertions
- Fail fast and loud — don't silently produce wrong results
- Check dimensions after merges: `stopifnot(nrow(merged) == expected_n)`

## targets Pipeline Pattern

```r
# _targets.R
library(targets)
tar_option_set(packages = c("dplyr", "ggplot2", "lavaan", ...))

list(
  tar_target(raw_data, read_raw_data("data/raw/survey.csv")),
  tar_target(validated_data, validate_data(raw_data)),
  tar_target(clean_data, clean_data(validated_data)),
  tar_target(descriptives, compute_descriptives(clean_data)),
  tar_target(h1_model, test_hypothesis_1(clean_data)),
  tar_target(h2_model, test_hypothesis_2(clean_data)),
  ...
)
```
