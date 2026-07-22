# Matrix-Completion Counterfactual Demo

Runnable simulation of the interactive-fixed-effects setting of
`athey_etal_2021` and `xu_2017` (see
[`../../references.bib`](../../references.bib)): control outcomes follow a
low-rank factor structure and treated units load more heavily on a trending
factor, so parallel trends fails **by construction** and two-way-FE DiD is
structurally biased. Treating the treated-by-post block of the outcome matrix
as missing and imputing it from the observed low-rank structure (hard-impute:
truncated SVD alternated with re-imputation, initialized from a two-way FE
fit) recovers the known treatment effect.

The demo also shows the method's practical failure mode instead of hiding it:
a rank-sensitivity printout demonstrates how an over-set rank lets the
alternating imputation drift in the missing corner — the reason regularized,
cross-validated variants (MC-NNM) exist.

## Run

From this directory:

```bash
python3 matrix_completion_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `matrix_completion.pdf`
- `matrix_completion.png`

The figure shows the treated units' observed mean path, the imputed
counterfactual tracking it until treatment and then splitting off by the
treatment effect, and the control mean for contrast. The repository
intentionally does not track those outputs. Re-run the script to recreate
them.

## What To Check

The treatment effect (1.0), the factor structure, and the loading shift are
all chosen by us, so the demo doubles as a regression test. It exits non-zero
unless:

- two-way FE DiD is biased upward by at least 0.40 — the factor confounding
  is structural, not sampling noise;
- **the matrix-completion imputation recovers the true effect within ±0.08**;
- a placebo world with no treatment shows an imputed effect of ~0;
- the imputation removes most of the DiD bias (the bias gap exceeds 0.40).

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md`](../../docs/methods-reference.md)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
For real projects route the estimation through validated implementations —
the StatsPAI `gsynth`, `matrix_completion`, and `interactive_fe` tools, or
`gsynth`/`fect` in R — rather than hand-rolling the imputation; this demo
hand-rolls it only so the mechanics (and the rank-sensitivity caveat) stay
visible.
