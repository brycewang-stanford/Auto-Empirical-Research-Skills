# Bunching-at-a-Kink Demo

Runnable simulation of the Saez kink design: when the marginal tax rate rises
at a threshold, workers whose counterfactual earnings would fall just above it
bunch at the kink, and the excess mass — normalized by the counterfactual
density — identifies the earnings elasticity through
`dz*/z* = ((1-t0)/(1-t1))^e - 1`. See `saez_2010` and the survey `kleven_2016`
in [`../../references.bib`](../../references.bib).

The demo separates the two things a referee will ask about: an **oracle** pass
measures the exact bunching mass against the true no-kink density (isolating
the formula and its small-kink approximation), while the **feasible** pass runs
the standard empirical pipeline — bin the earnings, fit a polynomial excluding
a window around the kink, take the fit as the counterfactual. Two
falsification worlds (no kink; a kink with zero elasticity) must show no
excess mass.

## Run

From this directory:

```bash
python3 bunching_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `bunching.pdf`
- `bunching.png`

The figure zooms in on the kink: the observed spike, the true no-kink
counterfactual, the polynomial counterfactual, and the theoretical bunching
segment `dz*`. The repository intentionally does not track those outputs.
Re-run the script to recreate them.

## What To Check

The elasticity (0.5), the kink location, and both tax rates are chosen by us,
so the demo doubles as a regression test. It exits non-zero unless:

- **the oracle excess-mass formula recovers the true elasticity** within the
  small-kink approximation (the counterfactual density is not flat across the
  bunching segment — the estimation caveat catalogued in `kleven_2016`);
- the feasible polynomial pipeline recovers the elasticity within a wider
  tolerance (the extra slack is the price of estimating the counterfactual);
- the same pipeline finds **no** excess mass in a world with no kink;
- a kinked world with zero elasticity shows **no** bunching — the pipeline
  may not invent behavioral responses.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md`](../../docs/methods-reference.md)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
For real projects route the estimation through validated implementations (the
StatsPAI `bunching` / `notch` tools); this demo hand-rolls the pipeline only
so the identification anatomy stays visible.
