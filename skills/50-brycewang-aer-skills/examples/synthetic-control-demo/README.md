# Synthetic-Control Demo

Runnable simulation showing why a synthetic control that *tracks the treated
unit beautifully in the pre-period* is not evidence of an effect — the
inference comes from the **placebo-in-space permutation distribution**
(Abadie-Diamond-Hainmueller 2010), summarized by the post/pre RMSPE ratio, not
from the eyeball fit.

## Run

From this directory:

```bash
python3 synthetic_control_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy`, `pandas`, `scipy`, and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `synthetic_control.pdf`
- `synthetic_control.png`

The left panel overlays the treated unit's treatment-minus-synthetic gap on the
placebo donors' gaps; the right panel is the permutation distribution of the
post/pre RMSPE ratio with the treated unit marked. The repository intentionally
does not track those outputs. Re-run the script to recreate them.

## What To Check

The data-generating process is a linear factor model with a KNOWN effect, so
the demo doubles as a regression test. It exits non-zero unless:

- **Power.** With a real post-treatment effect, the treated unit's post/pre
  RMSPE ratio is in the extreme tail of the placebo distribution, so the
  permutation p-value is significant.
- **Size.** With no effect, a Monte Carlo over many panels rejects a true null
  at about its nominal rate — the inferential guarantee that "the synthetic
  unit tracks well" cannot give you.
- **Fit is not inference.** Placebo donors routinely match the treated unit's
  pre-period fit; excellent pre-fit is a precondition for synthetic control,
  never a test statistic.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md#5-synthetic-control`](../../docs/methods-reference.md)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference lists the required synthetic-control diagnostics (in-space
and in-time placebo, a permutation / Fisher p-value, and the donor weight
vector); this demo is the runnable form of the first and third.
