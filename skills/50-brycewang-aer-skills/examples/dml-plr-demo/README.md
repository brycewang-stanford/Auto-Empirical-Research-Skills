# Double Machine Learning (Partially Linear) Demo

Runnable simulation showing why flexible prediction alone is not causal
inference. In a partially linear model with a KNOWN effect, three estimators
run on the same Monte Carlo panels: OLS with linear controls (misspecifies the
nonlinear nuisance, biased upward by design), a naive ML plug-in (learns
E[Y|X] with a flexible learner but regresses the outcome residual on the raw
treatment — a non-orthogonal moment, attenuated by the predictable share of
the treatment), and DML partialling-out (residualize BOTH outcome and
treatment under cross-fitting, then residual-on-residual OLS — the
Neyman-orthogonal moment), which recovers the truth with honest coverage.

The design keys: the plug-in's attenuation is not sampling noise. Ignoring the
treatment equation scales the estimand by var(v)/var(D) ≈ 0.64 here, so the
plug-in converges to roughly 0.32 when the truth is 0.5 — no sample size fixes
a wrong moment condition. See `chernozhukov_etal_2018` and `robinson_1988` in
[`../../references.bib`](../../references.bib).

## Run

From this directory:

```bash
python3 dml_plr_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `dml_plr.pdf`
- `dml_plr.png`

The figure overlays the Monte Carlo distributions of the three estimators
against the true effect. The repository intentionally does not track those
outputs. Re-run the script to recreate them.

## What To Check

The data-generating process has a KNOWN effect of 0.5 with nonlinear nuisances
shared between the outcome and treatment equations, so the demo doubles as a
regression test. It exits non-zero unless:

- the linear-controls OLS estimate is biased upward by at least 0.10;
- the naive plug-in lands on its KNOWN attenuation target
  `var(v)/var(D) * theta` within ±0.05 — and stays at least 0.10 below the
  truth (the bias is structural, not noise);
- **DML partialling-out with 5-fold cross-fitting recovers the truth within
  ±0.02** — the demo's internal correctness check of the orthogonal moment;
- the DML 95% confidence interval covers the truth in 90–99% of panels.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md`](../../docs/methods-reference.md)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
For real projects, route the estimation through validated implementations —
the StatsPAI `dml` tool, or the DoubleML packages in R/Python — rather than
hand-rolling the cross-fitting; this demo hand-rolls it only so the bias
anatomy stays visible in ~200 lines of `numpy`.
