# Sensitivity / Robustness-Value Demo (Cinelli-Hazlett)

Runnable simulation showing that coefficient stability under observed controls
does **not** bound omitted-variable bias, and that the honest way to report
robustness to an *unobserved* confounder is a partial-R² sensitivity statement.
Cinelli and Hazlett (2020) (`cinelli_hazlett_2020` in
[`../../references.bib`](../../references.bib)) summarize how any confounder Z
moves a treatment estimate with two scalars -- how much of the treatment it
explains (`R²_{D~Z}`) and how much of the residual outcome it explains
(`R²_{Y~Z|D,X}`). From those two numbers the *bias factor* reproduces the
confounded estimate exactly, and the *robustness value* RV reports the single
number a referee wants: the partial R² (with both treatment and outcome) a
confounder must reach to explain the result away.

This complements [`../oster-ovb-demo/`](../oster-ovb-demo/). Oster's δ scales
bias by how the coefficient and R² move as controls are added; Cinelli-Hazlett
works directly in the partial-R² geometry of a single specification and needs no
assumption about how observed and unobserved confounders compare in magnitude.
Both refuse the fallacy that "the coefficient barely moved" settles anything.

## Run

From this directory:

```bash
python3 sensitivity_rv_demo.py
```

Use the pinned Python stack in
[`../../templates/python/requirements.txt`](../../templates/python/requirements.txt).
The script depends only on `numpy` and `matplotlib`.

## What It Produces

The script writes generated files to `output/`:

- `sensitivity_rv.pdf`
- `sensitivity_rv.png`

The figure contrasts the robustness value of a strong and a fragile design
against a benchmark confounder of partial R² = 0.30: the strong design's RV sits
above the benchmark (survives it), the fragile design's below (is overturned by
it). The repository intentionally does not track those outputs. Re-run the
script to recreate them.

## What To Check

Every claim is checked by simulation against a known truth. The main
data-generating process has a true effect of 1.0 and a genuine omitted
confounder; two auxiliary designs isolate the robustness value. Across a 200-rep
Monte Carlo the demo exits non-zero unless:

- **omitting the confounder biases the short regression** while **including it
  recovers the truth** -- ordinary OVB;
- the **Cinelli-Hazlett bias factor reproduces the confounded estimate** from
  only the two partial-R² scalars -- the bias-factor-adjusted short estimate
  lands on the long (truth-recovering) estimate;
- the **robustness value equals the strength of an equal-partial-R² confounder
  that manufactures a purely spurious effect** -- with a true effect of zero, a
  confounder of partial R² = 0.30 with both treatment and outcome produces an
  estimate whose RV is 0.30, so the RV literally reads back the confounding that
  created the result;
- a **strong design survives the benchmark confounder (RV > 0.30)** while a
  **fragile design is overturned by the same benchmark (RV < 0.10)** -- a larger
  t-statistic buys a larger partial-R² cushion.

Use this demo as a teaching artifact next to
[`../../docs/methods-reference.md`](../../docs/methods-reference.md),
[`../../skills/aer-robustness/SKILL.md`](../../skills/aer-robustness/SKILL.md),
and the design context in
[`../../skills/aer-identification/SKILL.md`](../../skills/aer-identification/SKILL.md).
The methods reference lists the per-stack tooling (`sensemakr` in R, Stata, and
Python); this demo shows why a partial-R² robustness value, benchmarked against
observed covariates, is the sensitivity statement to report -- not a table of
coefficients that "hardly change."
