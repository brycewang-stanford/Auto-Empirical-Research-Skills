# Multiple-Testing Demo

Runnable simulation showing why testing many outcomes and calling the paper a
success when *any* one is significant inflates the **family-wise error rate
(FWER)** far above 5% — and why a family-wise correction (Bonferroni, or the
step-down Holm 1979 that is never less powerful) pulls it back to nominal
without throwing away real discoveries.

## Run

From this directory:

```bash
python3 multiple_testing_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy`, `scipy`, and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `multiple_testing.pdf`
- `multiple_testing.png`

The left panel is the family-wise error rate of the naive, Bonferroni, and Holm
rules under a complete null; the right panel is each rule's power to detect a
single real effect. The repository intentionally does not track those outputs.
Re-run the script to recreate them.

## What To Check

The data-generating process has a KNOWN structure (K outcomes, two groups), so
the demo doubles as a regression test. It exits non-zero unless:

- **Size.** With every outcome a true null, the naive "any outcome significant"
  rule rejects far more than 5% of the time (about `1 - 0.95^K`), while
  Bonferroni and Holm hold the FWER at its nominal level.
- **Power.** With one outcome carrying a real effect and the rest null, the
  correction still detects the true effect often (Holm never below Bonferroni)
  while keeping the false-positive rate on the null outcomes controlled.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md#6-inference-and-sensitivity-applies-to-all-designs`](../../docs/methods-reference.md)
and
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference lists the per-stack FWER/FDR tooling (`wyoung`,
`multcomp`, `statsmodels` `multipletests`); the aer-identification RCT advice
calls for a multiple-hypothesis correction whenever there is more than one
primary outcome. Romano-Wolf (2005) resampling and Benjamini-Hochberg (1995)
FDR are the less conservative alternatives when the outcomes are correlated.
