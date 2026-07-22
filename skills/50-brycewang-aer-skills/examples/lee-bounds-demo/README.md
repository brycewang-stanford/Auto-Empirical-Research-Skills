# Lee Bounds Demo (partial identification under differential attrition)

Runnable simulation showing that when a randomized treatment changes who is
*observed* -- differential attrition, or selection into employment in Lee's
training-program setting -- the naive contrast of observed outcomes across arms
is biased for any causal effect. Randomization balances the arms at assignment,
not among survivors, so once selection differs by arm the observed samples are
no longer comparable. Lee (2009) (`lee_2009` in
[`../../references.bib`](../../references.bib)) answers with *partial*
identification: under a monotonicity assumption -- treatment moves selection in
one direction only, leaving a well-defined "always-selected" subpopulation
observed in both arms -- the effect on that subpopulation is bounded. Trim the
excess-selection fraction from one tail of the higher-selection arm (low tail for
the upper bound, high tail for the lower bound) and difference against the other
arm. The interval width is the honest price of the attrition.

Most of the repo's demos contrast a broken point estimate with a fixed one; this
one is different in kind. It shows a design where the right answer is an
*interval*, not a number -- the partial-identification move an AER referee
expects whenever attrition is differential and cannot be assumed away.

## Run

From this directory:

```bash
python3 lee_bounds_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `lee_bounds.pdf`
- `lee_bounds.png`

The figure draws the Lee interval `[LB, UB]` as a horizontal bar, the true
always-taker effect as a vertical reference line inside it, and the naive
observed-outcome contrast as a marker sitting well outside the interval. The
repository intentionally does not track those outputs. Re-run the script to
recreate them.

## What To Check

The data-generating process is fully known: always-takers (observed regardless
of assignment) with a true treatment effect of 2.0, plus low-outcome marginal
units that appear *only* under treatment, so the treated-arm sample is
contaminated downward. The true always-taker effect is computed from the
parameters, and across a 300-rep Monte Carlo the demo exits non-zero unless:

- the **Lee lower bound sits at or below** the true effect, and the **upper
  bound at or above** it -- the interval covers the truth;
- the **naive observed-outcome contrast misses the truth** by a wide margin
  (about one full unit of bias here);
- the **interval has strictly positive width** -- this is partial, not point,
  identification, and reporting a single number would be dishonest;
- a **placebo world with symmetric attrition** (no marginal units) collapses the
  interval to a small fraction of its width, recovering point identification --
  the trim fraction is what the attrition costs you.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md`](../../docs/methods-reference.md),
[`../../skills/aer-robustness/SKILL.md`](../../skills/aer-robustness/SKILL.md),
and the design context in
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference lists the per-stack tooling (`leebounds` in Stata); this
demo shows why differential attrition demands an identified *interval* and a
trimming argument, not a footnote promising the attrition is "balanced."
