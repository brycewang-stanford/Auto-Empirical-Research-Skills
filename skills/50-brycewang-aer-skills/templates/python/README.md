# Python Templates

Drop-in scripts for an AEA-compliant Python pipeline. Uses `pyfixest` (the
modern Python equivalent of `fixest`) for high-dim FE OLS and AER-style
`etable` LaTeX output, with pinned packages for DiD, IV, and RDD examples.

## Files

| File | Purpose |
|---|---|
| `run_all.py` | Master script. Runs the full pipeline end-to-end. |
| `setup.py` | Paths, seed, matplotlib defaults, RNG. |
| `clean.py` | Placeholder cleaning stage; replace with raw-to-analytic code. |
| `descriptives.py` | Summary-statistics scaffold. |
| `main_did.py` | Callaway-Sant'Anna DiD via `differences`. |
| `robustness.py` | Placeholder robustness stage. |
| `heterogeneity.py` | Placeholder heterogeneity stage. |
| `tables.py` | AER-style booktabs table via `pyfixest.etable`. |
| `figures.py` | Placeholder figure stage. |
| `requirements.txt` | Pinned exact versions for reproducibility. |

## Conventions Enforced

- `numpy.random.default_rng(seed=20260101)` -- new-style RNG, no global state
- Relative paths via `pathlib.Path` rooted at the project directory
- Output goes to `output/tables` and `output/figures`
- `pdf.fonttype = 42` -- editable text in vector PDFs (required by AER)
- All packages pinned with `==` in `requirements.txt`

## How to Adapt

```bash
cd your-project/
python3 path/to/AER-Skills/scripts/scaffold_project.py python .
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 run_all.py
```

The placeholder stages are intentionally conservative. `clean.py` stops with a
clear message until you either write `data/intermediate/analytic.parquet` or
replace it with project-specific cleaning code.

## Stack

- **pyfixest** -- the Python `fixest`. AER-style tables and event studies.
- **differences** -- Bernardo-Mello implementation of Callaway-Sant'Anna ATT(g,t)
- **linearmodels** -- IV with weak-IV F (Olea-Pflueger), GMM, panel
- **econtools** -- regression helpers in the spirit of Stata `outreg2`
- **statsmodels / scipy** -- general OLS/WLS, diagnostics, simulations
- **rdrobust / rddensity** -- robust bias-corrected RDD and density tests

## Notes on the Python Ecosystem for AER-Track Empirics

Python is a second-class citizen in AEA replication (most papers ship Stata or R).
That is changing. `pyfixest` (2024+) closes most of the table-quality gap with
`fixest`. For Callaway-Sant'Anna, `differences` is the best Python option; for
RDD, `rdrobust` and `rddensity` match the standard Stata/R package family. If
you need wild cluster bootstrap, call into R via `rpy2` -- there is no
production-grade Python alternative yet.
