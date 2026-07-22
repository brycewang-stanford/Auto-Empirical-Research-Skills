# LP-DiD Demo (Dube-Girardi-Jorda-Taylor)

Runnable simulation showing that under staggered adoption with dynamic,
cohort-heterogeneous treatment effects, the pooled distributed-lag TWFE event
study does not recover the true dynamic path: already-treated units with
still-growing effects enter the implicit control group (the forbidden
comparison), so the lag coefficients are non-convex mixtures of effects at
other horizons and cohorts. LP-DiD (`dube_girardi_jorda_taylor_2023`) fixes
this with the local-projection idea of `jorda_2005` (keys in
[`../../references.bib`](../../references.bib)): for each horizon h, regress
the long difference y(t+h) - y(t-1) on the treatment-switch indicator using
ONLY clean controls (never-treated or not yet treated through t+h), absorbing
period effects. The companion
[`../staggered-did-demo/`](../staggered-did-demo/) shows WHY TWFE fails in the
aggregate; this demo shows the horizon-by-horizon repair.

## Run

From this directory:

```bash
python3 lp_did_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `lp_did.pdf`
- `lp_did.png`

The figure plots, event-study style across horizons h = 0..3, the known true
average dynamic path ATT(h) against the LP-DiD estimates (with the
pre-treatment placebo at h = -2) and the contaminated pooled TWFE event-study
coefficients. The repository intentionally does not track those outputs.
Re-run the script to recreate them.

## What To Check

The data-generating process is fully known: three adoption cohorts plus a
never-treated group, with effects that grow with event time and differ across
cohorts -- exactly the pattern that breaks pooled TWFE. The true ATT(h) is
computed inside the script from the same parameters, weighted the same way the
equally-weighted LP-DiD estimand weights (equally across treated
(unit, event-time-h) observations that enter the estimator), so the demo
doubles as a regression test. Across a 200-rep Monte Carlo it exits non-zero
unless:

- **LP-DiD recovers the true ATT at h = 0** (short horizon);
- **LP-DiD recovers the true ATT at h = 3** (the long horizon, where TWFE
  contamination is worst);
- the pooled distributed-lag TWFE event-study coefficient at h = 3 is
  materially contaminated (far from the truth);
- the LP-DiD pre-treatment placebo -- the long difference y(t-2) - y(t-1) on
  switchers -- is null, as parallel trends in the DGP requires.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md`](../../docs/methods-reference.md) and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference lists the per-stack tooling (`lpdid` in Stata/R); this
demo shows why the clean-control long-difference regression, not the pooled
event study, is what identifies the dynamic path.
