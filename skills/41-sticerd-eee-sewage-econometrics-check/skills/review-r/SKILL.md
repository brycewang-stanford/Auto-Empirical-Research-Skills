---
name: review-r
description: "R code review for the sewage project. Checks script structure, reproducibility, function design, figure quality, and professional polish against project conventions (here::here, arrow/parquet, fixest, modelsummary, native pipe). This skill should be used when asked to review the code, check my script, or code review."
argument-hint: "[filename, directory, or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Agent"]
---

# Review R Code

Run a code quality review on R scripts in the sewage project. Produces a report — does NOT edit source files.

**Input:** `$ARGUMENTS` — a `.R` filename, directory path, or `all`.

---

## Project-Specific Conventions

### Script Structure

**Pipeline scripts (layers 01-06):**
```
Header block (########) → roxygen description → initialise_environment() → setup_logging() → CONFIG list → functions → main() → conditional execution (sys.nframe() == 0)
```

**Analysis scripts (09_analysis):**
```
Numbered sections with # === separators, inline package loading, direct execution (no main() wrapper)
```

### Required Conventions
- **Paths:** `here::here()` — never relative paths or `setwd()`
- **Data formats:** `arrow` (parquet) for intermediate/final; DuckDB for large joins
- **Pipe:** Native R pipe `|>` (not `%>%`)
- **Naming:** `snake_case` for functions/variables, `UPPER_SNAKE_CASE` for constants
- **Econometrics:** `fixest::feols()` for regressions
- **Tables:** `modelsummary` → LaTeX with `tabularray` format
- **SE:** `vcov = "hetero"` for heteroskedasticity-robust
- **Factors:** `forcats::as_factor()` / `forcats::fct_drop()`

### Key Files
- Scripts: `scripts/R/01_data_ingestion/` through `scripts/R/09_analysis/`
- Utilities: `scripts/R/utils/`
- Output: `output/{figures,tables,html_plots,regs,log}/`

---

## Workflow

### Step 1: Identify Scripts

- If `$ARGUMENTS` is a specific `.R` file: review that file
- If `$ARGUMENTS` is a directory: review all `.R` files in that directory
- If `$ARGUMENTS` is `all`: review all scripts in `scripts/R/`
- If no argument: ask which scripts to review

### Step 2: Review Each Script (9 Categories)

#### Category 1: Script Structure
- Pipeline scripts: header block, roxygen, `initialise_environment()`, `CONFIG` list, `main()`, conditional execution
- Analysis scripts: numbered sections with `# ===` separators
- Clear separation of concerns

#### Category 2: Console Hygiene
- No unnecessary `print()` / `cat()` pollution
- Logging via `setup_logging()` in pipeline scripts
- Clean output — only meaningful messages

#### Category 3: Reproducibility
- `set.seed()` where randomness is involved
- All paths via `here::here()` — no `setwd()`, no relative paths, no hardcoded absolute paths
- No hardcoded values that should be in CONFIG

#### Category 4: Function Design
- DRY — no duplicated code blocks
- Functions at appropriate abstraction level
- Shared utilities in `scripts/R/utils/` where reuse is needed

#### Category 5: Figure Quality
- Axis labels present and readable
- Appropriate dimensions (not too wide/narrow)
- Consistent theme across plots
- Alpha transparency for overlapping points
- Saved to `output/figures/` via `here::here()`

#### Category 6: Data Persistence
- Intermediate results saved as parquet (`arrow::write_parquet()`)
- `saveRDS()` for R-specific objects
- No orphaned temporary files

#### Category 7: Comments
- Explain *why*, not *what*
- Section headers for navigation
- No commented-out dead code

#### Category 8: Error Handling
- Graceful failures with informative messages in pipeline scripts
- File existence checks before reading
- Data validation where appropriate

#### Category 9: Polish
- Consistent style (indentation, spacing)
- No dead code or unused imports
- Clean namespace — `library()` calls at top
- Native pipe `|>` (not magrittr `%>%`)

### Step 3: Present Summary

```markdown
## Code Review: [filename/directory]
**Date:** YYYY-MM-DD
**Scripts reviewed:** N

### Issues by Severity
| Script | Critical | Major | Minor |
|--------|----------|-------|-------|
| ... | ... | ... | ... |

### Top 3 Critical Issues
1. ...
2. ...
3. ...

### Conventions Compliance
- [ ] here::here() for all paths
- [ ] Native pipe |>
- [ ] arrow/parquet for data
- [ ] fixest for regressions
- [ ] modelsummary for tables

### Score: XX / 100
```

Save report to `output/log/code_review_[target].md`.

### Step 4: IMPORTANT

**Do NOT edit any source files.** Only produce reports. Fixes are applied after user review.

---

## Principles

- **Report only, never edit.** The reviewer is a critic, not a creator.
- **Project conventions matter.** Flag deviations from the conventions above, not personal preferences.
- **Proportional severity.** A missing `set.seed()` is Major. A missing comment is Minor. Using `setwd()` is Critical.
- **Language-specific.** Check R idioms — vectorised operations over loops, tidyverse patterns, proper use of factors.
- **Pipeline vs analysis distinction.** Different structure expectations for pipeline scripts vs analysis scripts.
