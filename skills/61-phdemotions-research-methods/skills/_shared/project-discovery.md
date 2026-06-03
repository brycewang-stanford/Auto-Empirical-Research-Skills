# Project Discovery

> How to find and read the research project context. Every skill reads this first.

## Locating the research project

1. **Check CWD** — if there's a `_targets.R`, `Snakefile`, or `data/raw/` directory, you're in a research project.
2. **Check argument** — if the user passed a path or project name, use that.
3. **Check parent directories** — walk up from CWD looking for the project root markers.

## Project root markers (any of these)

- `_targets.R` (R pipeline)
- `Snakefile` (Python pipeline)
- `data/raw/` directory
- `renv.lock` + research-style directory structure
- `reports/manuscript.qmd`

## What to read (in order)

Once you find the project root, read these files to understand context:

1. **`data/codebook/`** — variable definitions, types, scales, measurement info
2. **`docs/pre-registration.md`** — planned hypotheses and analyses
3. **`docs/decisions/`** — prior subjective choices and rationale
4. **`README.md`** — project overview, data sources
5. **Pipeline definition** — `_targets.R` or `Snakefile` to understand what's been built

## What to check for existing data

- `data/raw/` — original data files (.csv, .xlsx, .sav, .dta, .parquet)
- `data/processed/` — already-cleaned data
- `output/results/` — prior analysis output
- `output/figures/` — existing figures
- `output/tables/` — existing tables

## Language detection

- If `_targets.R` exists → R project (primary)
- If `Snakefile` exists → Python project (primary)
- If both → dual-language project
- If neither but `.R` files in `R/` → R project
- If neither but `.py` files in `python/` → Python project
- Ask the user if ambiguous
