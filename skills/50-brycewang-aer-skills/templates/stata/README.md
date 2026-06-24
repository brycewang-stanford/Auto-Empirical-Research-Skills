# Stata Templates

Drop-in scripts for an AEA-compliant Stata pipeline.

## Files

| File | Purpose |
|---|---|
| `run_all.do` | Master script. Runs the full pipeline end-to-end. |
| `00_globals.do` | Project paths, seed, display options. Uses current working directory. |
| `00_install_packages.do` | Install and report user-written package locations. |
| `01_clean.do` | Placeholder cleaning stage; replace with raw-to-analytic code. |
| `02_descriptives.do` | Summary-statistics scaffold. |
| `03_main_did.do` | Staggered DiD with Callaway-Sant'Anna + diagnostics. |
| `04_robustness.do` | Placeholder robustness stage. |
| `05_heterogeneity.do` | Placeholder heterogeneity stage. |
| `06_tables.do` | AER-style 5-column main results table via `esttab`. |
| `07_figures.do` | Placeholder figure stage. |

## Conventions Enforced

- `version 18.0` at the top of every do-file
- Relative paths via `$project`, set from Stata's current working directory
- `set seed 20260101` before any stochastic procedure
- Output goes to `$tables` and `$figures` — never to the project root
- Logs to `$logs/run_all.log` for reproducibility traceability

## How to Adapt to Your Project

1. Run `python3 scripts/scaffold_project.py stata /path/to/project` from the
   AER-skills repository, or copy the contents of `templates/stata/` into your
   replication package root
2. In Stata, change directory to that root
3. Replace `outcome`, `treat`, `$controls`, `unit_id`, `year`, `iv`, `endog`
   with your variable names
4. Run `do run_all.do`

The placeholder stages are intentionally conservative. `01_clean.do` stops with
a clear message until you either write `data/intermediate/analytic.dta` or
replace it with project-specific cleaning code.

## Dependencies

See `00_install_packages.do`. Core: `reghdfe`, `csdid`, `ivreg2`, `weakivtest`,
`rdrobust`, `estout`, `coefplot`, `bacondecomp`, `honestdid`, `boottest`.
For final deposits, record installed package versions in the README and preserve
an `ado/` snapshot if exact SSC package reproduction is required.
