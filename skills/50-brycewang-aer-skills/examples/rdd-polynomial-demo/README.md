# RDD Polynomial Demo

Runnable simulation showing why high-order global polynomials are not the
default for regression discontinuity designs, and why local-linear `rdrobust`
with robust bias-corrected inference is safer at the cutoff.

## Run

From this directory:

```bash
python3 rdd_polynomial_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends on `numpy`, `pandas`, `statsmodels`, `rdrobust`, and
`matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `rd_fit.pdf`
- `rd_fit.png`

The repository intentionally does not track those outputs. Re-run the script to
recreate them.

## What To Check

The simulation has a known jump at the cutoff. It exits non-zero unless:

- the fourth-order global polynomial is materially biased
- the global-polynomial confidence interval badly under-covers
- `rdrobust` recovers the jump
- the robust bias-corrected interval covers near nominal size

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md#4-regression-discontinuity`](../../docs/methods-reference.md#4-regression-discontinuity)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
