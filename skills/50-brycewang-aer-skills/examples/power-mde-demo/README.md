# Power / MDE Demo (ex-ante design and the underpowered-study trap)

Runnable simulation for the two design questions a pre-analysis plan must settle
*before* any data are collected. First, the minimum detectable effect (MDE)
formula for a two-arm trial,

```
MDE = (z_power + z_{1 - alpha/2}) * sigma * sqrt(1 / (p (1 - p) N)),
```

is not folklore: it is exactly the true effect at which the design attains its
target power, and a Monte Carlo confirms it to the third decimal. Second -- and
this is why AEA referees care -- an *underpowered* design is not merely "less
likely to find the effect." Conditional on reaching significance, its estimates
are inflated: the Type-M (exaggeration) ratio. A study powered at 29% does not
just miss most of the time; when it "wins," it overstates the effect by nearly
2x. Honest power calculations and pre-registration exist to keep that winner's
curse out of the published record (`mckenzie_2012`,
`duflo_glennerster_kremer_2007` in
[`../../references.bib`](../../references.bib)).

Unlike the identification demos, nothing here is estimated wrong -- the test is
correctly sized throughout. The failure this demo dramatizes is a *design*
failure: collecting too small a sample and then reading a significant,
exaggerated estimate as if it were news.

## Run

From this directory:

```bash
python3 power_mde_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends on `numpy`, `scipy`, and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `power_mde.pdf`
- `power_mde.png`

The figure plots simulated power against the true effect (expressed as a
multiple of the MDE), with reference lines at the 80% power target, at the MDE,
and at the nominal size under the null. The power curve crosses 80% exactly at
the MDE. The repository intentionally does not track those outputs. Re-run the
script to recreate them.

## What To Check

Every claim is checked by simulation against the analytic target. Across a
4,000-rep Monte Carlo the demo exits non-zero unless:

- the **analytic MDE delivers the target 80% power** -- the closed-form design
  number is the real operating characteristic, not an approximation to
  apologize for;
- a **design at half the MDE is badly underpowered** (power near 29%);
- the **test holds its nominal 5% size under the null** -- the exaggeration
  below is not a broken test;
- the **underpowered design exaggerates the effect** among significant
  replications (Type-M ratio near 1.9x) while the **well-powered design barely
  does** (about 1.1x).

Use this demo as a teaching artifact next to
[`../../skills/aer-preregistration/SKILL.md`](../../skills/aer-preregistration/SKILL.md),
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md),
and [`../../docs/methods-reference.md`](../../docs/methods-reference.md). It is
the quantitative backbone of the pre-analysis-plan power section: state the MDE,
justify the sample size, and refuse to run -- or over-interpret -- a design whose
only significant findings would be inflated.
