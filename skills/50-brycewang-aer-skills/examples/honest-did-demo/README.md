# Honest-DiD Demo

Runnable simulation showing why a flat-looking pre-trend does not license the
parallel-trends assumption (Rambachan-Roth 2023). A difference-in-differences
event study whose pre-period coefficients are individually small can still hide a
differential trend that continues into the post period and biases the effect.
Naive parallel-trends inference — a confidence interval that assumes the trend
stops at treatment — then under-covers the truth; **honest DiD** reports a
confidence set valid under the relative-magnitudes restriction (the post-period
violation is at most M times the pre-period violation).

## Run

From this directory:

```bash
python3 honest_did_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy`, `scipy`, and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `honest_did.pdf`
- `honest_did.png`

The figure plots coverage of the true effect against the relative-magnitudes
bound M: the naive CI (M = 0) sits far below 95%, and coverage crosses the
nominal line by M = 1, the true relative magnitude. The repository intentionally
does not track those outputs. Re-run the script to recreate them.

## What To Check

The data-generating process has a KNOWN linear differential trend that continues
at the same rate after treatment (so M = 1 is exactly true) plus a real effect.
Framed as a coverage experiment — the natural self-test for a confidence set — it
exits non-zero unless:

- the naive parallel-trends CI covers the true effect far below 95%;
- the relative-magnitudes honest CI reaches >= 95% coverage by M = 1;
- coverage is non-decreasing in M and the M = 0 honest CI coincides with the
  naive CI.

This is the single-coefficient relative-magnitudes case (one pre-period violation
bounds one post-period bias); the general multi-period FLCI is in the HonestDiD
package, but the intuition and coverage behavior are identical.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md#1-difference-in-differences-staggered-adoption`](../../docs/methods-reference.md)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference prescribes Honest DiD sensitivity bounds alongside the joint
pre-trends test; this demo shows why the pre-test alone is not enough.
