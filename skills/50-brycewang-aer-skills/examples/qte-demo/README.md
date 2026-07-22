# Quantile-Treatment-Effects Demo

Runnable simulation of the distributional-effects exhibit referees ask for
when the mean is a wash: a randomized treatment leaves the average outcome
exactly unchanged while spreading the distribution — harming the bottom of
the outcome distribution and helping the top. OLS (the ATE) reports a
precise, useless zero; quantile regression of the outcome on the treatment
indicator (Koenker and Bassett 1978,
[`koenker_bassett_1978`](../../references.bib)) traces out the full
quantile-treatment-effect curve the mean averages away.

## Run

From this directory:

```bash
python3 qte_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy`, `matplotlib`, and `statsmodels`.

## What It Produces

The script writes generated files to `output/`:

- `qte_curve.pdf`
- `qte_curve.png`

The figure plots the Monte Carlo mean of the estimated QTE curve with a 95%
band against the analytic QTE line and the flat ATE = 0 line, so the
"the mean hides everything" point is visible at a glance. The repository
intentionally does not track those outputs. Re-run the script to recreate
them.

## What To Check

The data-generating process makes the truth ANALYTIC: treatment is
randomized (so quantile regression on a constant and the treatment dummy
identifies unconditional QTEs), the control outcome is Normal(mu, sigma0^2)
and the treated outcome is Normal(mu, sigma1^2) with sigma1 > sigma0, so the
true ATE is exactly zero while the true QTE curve is
`(sigma1 - sigma0) * Phi^{-1}(tau)`. The demo doubles as a regression test
of the quantile-regression pipeline. It exits non-zero unless:

- the OLS/ATE estimate is (correctly but uselessly) zero;
- **the estimated QTE at tau = 0.9 and tau = 0.1 match their analytic values
  `(sigma1 - sigma0) * Phi^{-1}(tau)`** — the demo's internal correctness
  check of the quantile-regression estimator;
- the median treatment effect is null, as the symmetric spread requires;
- the whole estimated QTE curve stays within tolerance of the analytic curve
  (maximum absolute deviation across the estimated quantiles).

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md`](../../docs/methods-reference.md) and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md);
see [`../../skills/aer-robustness/SKILL.md`](../../skills/aer-robustness/SKILL.md)
for when a distributional exhibit is expected alongside the headline ATE.
The methods reference lists the per-stack tooling (`qreg`, `sqreg`,
`quantreg`, `QuantReg`); this demo shows why the quantile curve, not the
mean, carries the welfare and targeting content when treatment reshapes the
distribution.
