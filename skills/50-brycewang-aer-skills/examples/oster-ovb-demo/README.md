# Oster-Delta / OVB Demo

Runnable simulation showing why "the coefficient barely moved when I added
controls, so omitted-variable bias is small" is not a valid argument on its own
(Oster 2019). Coefficient movement is only informative when scaled by how much
the R-squared moved: weak controls that barely raise the R-squared cannot certify
robustness no matter how stable the coefficient looks.

## Run

From this directory:

```bash
python3 oster_ovb_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `oster_ovb.pdf`
- `oster_ovb.png`

The figure compares the short (no-controls), controlled (observed X), Oster
bias-adjusted, and infeasible full (observed plus the unobservable W) estimates
against the true effect. The repository intentionally does not track those
outputs. Re-run the script to recreate them.

## What To Check

The data-generating process has a KNOWN true effect of zero and an unobserved
confounder that is exactly as related to the treatment and outcome as the
observed control (proportional selection, delta = 1), so the demo doubles as a
regression test. It exits non-zero unless:

- the full model (controlling the unobservable) recovers the true zero;
- the observed-controls estimate stays biased away from zero;
- **Oster's R-squared-scaled adjustment `beta*(delta=1, R_max=R_full)` recovers
  the true zero** — the demo's internal correctness check of the bounding
  formula;
- the implied delta-for-zero is about 1, as proportional selection requires.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md#6-inference-and-sensitivity-applies-to-all-designs`](../../docs/methods-reference.md)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference lists the per-stack tooling (`psacalc`, `robomit`); this
demo shows why their R-squared-scaled bound, not raw coefficient stability, is
what bounds the bias.
