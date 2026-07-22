# Specification-Curve Demo

Runnable simulation showing why reporting a single "preferred" specification can
mislead, and why the honest summary is the whole **specification curve** plus a
**joint permutation test** (Simonsohn-Simmons-Nelson 2020). When a dataset admits
many defensible specs, searching for one that "works" is multiple testing over a
correlated family — it inflates false positives.

## Run

From this directory:

```bash
python3 spec_curve_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy`, `scipy`, and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `spec_curve.pdf`
- `spec_curve.png`

The figure is the iconic specification curve: the treatment estimate under every
subset of the candidate controls, sorted, with the specs that are individually
"significant" highlighted. The repository intentionally does not track those
outputs. Re-run the script to recreate them.

## What To Check

The treatment is randomly assigned (so the sharp null is exchangeable and the
permutation test is exact) and the true effect is KNOWN, so the demo doubles as a
regression test. It exits non-zero unless:

- **Size.** With a true effect of zero, the naive rule "report a spec where the
  effect is significant" rejects far more than 5% of the time, while the
  specification-curve permutation test (re-randomizing treatment, recomputing the
  whole curve, summarized by the median t across specs) holds nominal size.
- **Power.** With a real effect, the permutation test rejects often, so the joint
  test is not merely conservative.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md#6-inference-and-sensitivity-applies-to-all-designs`](../../docs/methods-reference.md)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference lists the per-stack tooling (`speccurve`, `specr`); this
demo is the runnable form of why the curve plus joint inference, not a single
starred coefficient, is the honest report. See `simonsohn_simmons_nelson_2020`
and `romano_wolf_2005` in `../../references.bib`.
