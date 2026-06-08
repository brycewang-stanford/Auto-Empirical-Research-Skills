# R Templates

Drop-in scripts for an AEA-compliant R pipeline using the modern stack
(`fixest`, `did`, `modelsummary`).

## Files

| File | Purpose |
|---|---|
| `run_all.R` | Master script. Runs the full pipeline end-to-end. |
| `00_setup.R` | Paths, packages, seed, plot theme. |
| `01_clean.R` | Placeholder cleaning stage; replace with raw-to-analytic code. |
| `02_descriptives.R` | Summary-statistics scaffold. |
| `03_main_did.R` | Callaway-Sant'Anna DiD + Bacon + Honest DiD. |
| `04_robustness.R` | Placeholder robustness stage. |
| `05_heterogeneity.R` | Placeholder heterogeneity stage. |
| `06_tables.R` | AER-style booktabs table via `fixest::etable`. |
| `07_figures.R` | Placeholder figure stage. |

## Conventions Enforced

- `set.seed(20260101)` in `00_setup.R`
- Relative paths via `PROJECT <- getwd()` and `file.path(...)`
- Output goes to `output/tables` and `output/figures`
- Optional `renv` lock for full package-version pinning
- `cairo_pdf` device for vector figures (publication-ready)

## How to Adapt

1. Run `python3 scripts/scaffold_project.py r /path/to/project` from the
   AER-skills repository, or copy the contents of `templates/r/` into your
   project root
2. Open the project root in RStudio (so `getwd()` is correct)
3. `renv::restore()` if you maintain a lockfile
4. `source("run_all.R")`

The placeholder stages are intentionally conservative. `01_clean.R` stops with a
clear message until you either write `data/intermediate/analytic.dta` or replace
it with project-specific cleaning code.

## Package Stack

- **fixest** — `feols`, `etable`. AER-style tables out of the box.
- **did** — Callaway-Sant'Anna ATT(g,t), aggregations, event study
- **HonestDiD** — Rambachan-Roth pre-trends sensitivity
- **rdrobust** + **rddensity** — modern RDD
- **modelsummary** — flexible table backend (kableExtra / gt / LaTeX)
- **fwildclusterboot** — wild cluster bootstrap for few-cluster inference
