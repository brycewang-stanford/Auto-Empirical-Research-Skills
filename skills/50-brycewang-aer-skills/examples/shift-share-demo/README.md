# Shift-Share / Bartik Demo

Runnable simulation showing why shift-share inference belongs at the **shock
(industry) level, not the region level** (Adão-Kolesár-Morales 2019;
Borusyak-Hull-Jaravel 2022). Because every region's Bartik regressor is built
from the *same* industry shocks, the regions are not independent observations.
Conventional heteroskedasticity-robust (or region-clustered) standard errors
treat the R regions as R independent draws and are therefore far too small —
the effective number of observations is the number of shocks, not regions.

## Run

From this directory:

```bash
python3 shift_share_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `shift_share.pdf`
- `shift_share.png`

The figure compares region-level HC1 inference against shock-level
randomization inference for both a true-null (size) and a real-effect (power)
panel. The repository intentionally does not track those outputs. Re-run the
script to recreate them.

## What To Check

The data-generating process has a KNOWN coefficient and a shared industry-shock
structure that couples the regional residuals, so the demo doubles as a
regression test. It exits non-zero unless:

- **Size.** Region-level HC1 robust inference rejects a TRUE null far more than
  5% of the time, while shock-level randomization inference (re-drawing the
  industry shocks, holding shares and outcomes fixed — a valid Fisher
  randomization test) keeps its nominal 5% size.
- **Power.** With a real effect, shock-level randomization inference still
  rejects often, so the fix is not merely conservative.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md#3-shift-share--bartik`](../../docs/methods-reference.md)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference makes the choice between an exogenous-shares story
(Rotemberg weights) and an exogenous-shocks story explicit; this demo shows why,
once you commit to the shocks as the source of variation, the inference has to
follow them to the shock level.
