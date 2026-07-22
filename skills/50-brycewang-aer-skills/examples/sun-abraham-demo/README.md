# Sun-Abraham Demo (interaction-weighted event study)

Runnable simulation showing that under staggered adoption with
cohort-heterogeneous dynamic treatment effects, the *dynamic* two-way
fixed-effects event study -- outcome on unit fixed effects, period fixed
effects, and a full set of relative-time indicators -- does not recover the
average dynamic path. Each relative-time coefficient is a contaminated weighted
sum of cohort-specific effects (CATT) at that *and other* relative times,
because already-treated cohorts whose effects are still growing enter the
implicit comparison group. Sun and Abraham (2021) (`sun_abraham_2021` in
[`../../references.bib`](../../references.bib)) repair this *inside one saturated
regression*: fully interact the relative-time indicators with cohort dummies to
estimate each `CATT(e, l)` against a clean never-treated control, then aggregate
to the horizon-`l` average using the interaction WEIGHTS -- the sample share of
each cohort among units observed at relative time `l`. That weighted average is
the true `ATT(l)`.

This is a different repair from its siblings. The companion
[`../staggered-did-demo/`](../staggered-did-demo/) shows WHY pooled TWFE fails
(the Goodman-Bacon forbidden comparison); [`../lp-did-demo/`](../lp-did-demo/)
repairs the path horizon-by-horizon with clean-control local projections;
Sun-Abraham instead repairs it in a single interaction-weighted regression --
the estimator AER referees now request by name alongside Callaway-Sant'Anna.

## Run

From this directory:

```bash
python3 sun_abraham_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `sun_abraham.pdf`
- `sun_abraham.png`

The figure plots, event-study style across horizons l = 0..3 (with the
pre-treatment placebo at l = -2), the known true average dynamic path ATT(l)
against the Sun-Abraham interaction-weighted estimates and the contaminated
naive dynamic TWFE event-study coefficients. The repository intentionally does
not track those outputs. Re-run the script to recreate them.

## What To Check

The data-generating process is fully known: three adoption cohorts plus a small
(10%) never-treated group, with a common dynamic shape `BASE(l) = 1 + 0.5 l`
scaled by a cohort multiplier so effects grow with event time and differ across
cohorts -- exactly the pattern that breaks the naive dynamic TWFE event study,
made worse by the thin never-treated anchor. The true ATT(l) is computed inside
the script from the same parameters, weighted the same way the
interaction-weighted estimand weights (each cohort's share of the units observed
at relative time l), so the demo doubles as a regression test. Across a 300-rep
Monte Carlo it exits non-zero unless:

- **Sun-Abraham recovers the true ATT at l = 0** (short horizon);
- **Sun-Abraham recovers the true ATT at l = 3** (the long horizon, where TWFE
  contamination is worst);
- the naive dynamic TWFE event-study coefficient at l = 3 is materially
  contaminated (far from the truth -- roughly 60% of the true effect in this
  DGP);
- the Sun-Abraham pre-treatment placebo at l = -2 is null, as parallel trends
  in the DGP requires.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md`](../../docs/methods-reference.md) and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference lists the per-stack tooling (`eventstudyinteract` in
Stata, `sunab` inside `fixest` in R); this demo shows why the interaction
weights, not the pooled relative-time coefficients, are what identify the
dynamic path.
