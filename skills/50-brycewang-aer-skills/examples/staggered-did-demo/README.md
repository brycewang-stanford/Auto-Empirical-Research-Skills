# Staggered DiD Demo

Runnable simulation showing why naive TWFE can fail under staggered adoption
with heterogeneous dynamic treatment effects, and why a heterogeneity-robust
event-study estimator is the safer default.

## Run

From this directory, run either implementation:

```bash
python3 staggered_did_demo.py
Rscript staggered_did_demo.R
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends on `numpy`, `pandas`, `pyfixest`, and `matplotlib`.

For R, use the packages listed in
[`../../templates/r/00_setup.R`](../../templates/r/00_setup.R): `data.table`,
`fixest`, `did`, `bacondecomp`, and `ggplot2`.

## What It Produces

The script writes generated files to `output/`:

- `results.csv`
- `event_study.pdf`
- `event_study.png`
- `event_study_R.pdf`
- `event_study_R.png`

The repository intentionally does not track those outputs. Re-run the script to
recreate them.

## What To Check

The simulation has a known true treatment effect. It exits non-zero unless:

- `did2s` (Python) or Callaway-Sant'Anna (R) recovers the true aggregate ATT
  within a tight tolerance
- TWFE is materially biased downward
- pre-treatment event-study coefficients are near zero

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md`](../../docs/methods-reference.md) and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
