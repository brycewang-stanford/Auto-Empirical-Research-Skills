---
name: phack-detection
description: Test whether a body of reported results shows p-hacking, selective reporting or selection between stages, using the p-curve battery and the threshold and across-stages tests of Adda, Decker and Ottaviani (2020). Implements the binomial, Fisher, Stouffer and least-concave-majorant monotonicity tests of Elliott, Kudrin and Wuethrich (2022); threshold-bunching tests calibrated against a smooth counterfactual density; a Cattaneo-Jansson-Ma density-jump test and a right-side spike test that tell a level shift (results withheld) from a spike (results pushed across); the phase II vs phase III comparison and the selective-continuation decomposition; and Simonsohn's p-curve power estimate. Use when asked whether a literature, a journal, a research design, an author, a registry or a set of agent runs shows evidence of p-hacking, publication bias or selective continuation.
---

# Detecting p-hacking in a collection of results

## What can and cannot be established

Every test here is a test on the **distribution across many results**. None of
them can establish that any individual paper was p-hacked, and the report says
so on every run. Treat a flag as a reason to look, never as a finding about a
person.

## The theory in one paragraph

Elliott, Kudrin & Wüthrich (2022) show that in the absence of p-hacking the
density of p-values across studies is **non-increasing** on (0, α), and for
tests based on asymptotically normal statistics it is also **continuous** and
bounded above. p-hacking breaks these: it moves mass from just above the
threshold to just below, producing a hump, a discontinuity, or a
non-monotonicity. Each testable implication gives a test.

## Running

```bash
python scripts/phack_cli.py detect stats.csv --pcol p --zcol z
```

Input is one row per reported result. Supply p-values, z-statistics, or both;
whichever is missing is derived.

## The battery

**Shape tests** — clean nulls, trust these:

| Test | Null | Small p-value means |
|---|---|---|
| `binomial` | ≥ half of significant p-values fall below α/2 | left-skewed p-curve; no evidential value |
| `fisher` | p-curve is uniform or right-skewed | left skew |
| `stouffer` | as Fisher, normal aggregation | left skew |
| `lcm_monotonicity` | density non-increasing on (0, α) | the curve humps; bootstrapped against the least favourable null |

**Bunching tests** — weaker, read with care:

| Test | What it compares |
|---|---|
| `discontinuity` | mass just below p = .05 against a Poisson log-linear counterfactual fitted outside a donut |
| `caliper` | mass just above z = 1.96 against the same kind of counterfactual |

**Why the counterfactual matters.** The classical caliper test asks whether more
than half the statistics in a window around 1.96 lie above it. That null is
right only when the density is locally *flat*. When a real effect is present the
density of |z| is *rising* through 1.96, so an honest literature fails the naive
test. On simulated honest data with a true effect, the naive caliper reports 65%
above and p = .011 — a false positive. The counterfactual version reports
p = .11 and correctly declines to flag. Both are printed; `naive_share_above` is
kept for comparability with the published literature, but `p_value` is the
counterfactual one.

**Threshold signatures** — Adda, Decker & Ottaviani (2020) on 12,621
registered clinical-trial p-values found *no* spike past z = 1.96 anywhere,
but a discontinuity at 1.96 in phase III for small industry sponsors. Those
are different things, and two tests separate them:

| Test | Counterfactual | Small p-value means |
|---|---|---|
| `density_jump` | local polynomial density of \|z\| on each side of 1.96 (Cattaneo, Jansson & Ma 2020), bootstrap SE | the density is higher just past the line than just before it |
| `spike` | log-linear Poisson fit on [1.96 + 0.2, 1.96 + 0.8] extrapolated over the caliper, with the extrapolation's own variance | mass just past the line is out of line with the density *beyond* it |

Read them together. A **spike** with or without a jump is results pushed
across the line: p-hacking. A **jump without a spike** is a level shift: the
results below the line are missing, not moved — selective reporting, the
small-sponsor pattern in the paper. Neither, with a rising share significant
between stages of a project, is **selection between stages**, which no
threshold test can see. `report()` prints this reading as
`threshold_signature`. The classical `caliper` fits its counterfactual
*through* the threshold and so flags any discontinuity alike; it is kept for
comparability.

On simulated ground truth: withholding half the non-significant results
gives a density jump with p < 0.001 and a clean spike test; pushing half the
results in [1.6, 1.96) to just past 1.96 gives a spike with p < 0.001. Over
30 draws of a half-normal with n = 3,000 and of a null/effect mixture with
n = 1,800, the spike test rejects at 5% on 3% and 3% of draws; the jump test
on 30 draws of the rising-density literature above rejects on 5%.

**`pcurve_power`** estimates the average power behind the significant results.
A value near α means the significant findings carry no evidential value at all.

## Across stages: selection is not manipulation

The paper's central finding is that the share of significant primary outcomes
rises from 45.7% in phase II to 70.6% in phase III for industry sponsors (34.7%
to 34.8% for non-industry), with a **smooth** phase III distribution. Sponsors
continue to phase III after promising phase II results; the later stage
inherits the selection. That is rational, possibly socially desirable, and
invisible to every test above. Three functions handle it:

```bash
# stats.csv: one row per result, a column with two stage labels, and on the
# early-stage rows a 0/1 column saying whether the project continued
python scripts/phack_cli.py detect stats.csv --zcol z --stagecol phase --contcol continued
```

- `phase_shift_test(z_early, z_late)` — share significant by stage, a
  two-proportion test, and a one-sided KS test that the later stage
  stochastically dominates.
- `continuation_decomposition(z_early, continued, z_late)` — the paper's
  method: a logit of continuation on the early-stage |z|, the early-stage
  distribution reweighted by the fitted continuation probabilities, and the
  later stage's excess split into the part the continuation rule **explains**
  and the part it leaves **unexplained**, with a bootstrap SE on the latter.
  In the paper the rule explains ≈ 85% of the phase III excess for the ten
  largest sponsors and ≈ 29% for small ones; the unexplained 18 points for
  small sponsors is what is left for selective reporting.
- `phase_report(...)` runs both stages through the threshold tests, the
  phase shift and the decomposition and prints a `signature`.

The decomposition's identifying assumption is the paper's: conditional on
continuing, the expected later-stage z equals the earlier-stage z. It holds
when the sponsor's decision uses information of which the registered z is a
noisy reflection, and it fails when continuation is a deterministic function
of the registered z itself (the logit separates; the function says so).
`simulate.continuation_shift` generates a population that satisfies it —
heterogeneous true effects, a logistic continuation rule on the sponsor's own
read of the pilot, an optional probability `conceal` of withholding a
non-significant confirmatory result — and is what the battery is validated
on: with no concealment the rule explains 90–100% of the phase III excess and
the later stage shows no threshold signature; with half the null confirmatory
results withheld, 19 points are left unexplained (p < 0.001) and the later
stage shows a density jump with no spike.

```bash
python scripts/phack_cli.py simulate --continuation --n-sims 6000 --conceal 0.5
```

## Reading the verdict

The verdict weights shape tests above bunching tests, because only the shape
tests have clean nulls:

- **strong evidence** — two or more shape tests flag
- **moderate** — one shape test plus bunching
- **weak / ambiguous — bunching only** — this is the interesting case. It is
  what a *mixed* literature looks like: genuine effects dilute the shape tests
  while threshold-seeking still leaves a bunching signature. In simulation, a
  literature that is 5/6 null with mild threshold-pushing shows excess mass of
  2.3× at the caliper while every shape test comes back clean.
- **no distributional evidence** — the tests found nothing; this is not proof of
  absence, particularly with few results

## Validation

The battery is calibrated on simulated data with known ground truth:

| Data | Shape tests | Bunching | Estimated power | Verdict |
|---|---|---|---|---|
| honest, real effect | clean | clean | 0.80 | no evidence |
| p-hacked, true null | all four flag | both flag | 0.05 | strong evidence |
| mixed | clean | both flag | 0.30 | weak / ambiguous |

Reproduce from `tests/test_detect.py`.

## Sample-size guidance

The shape tests need at least ~15 significant results and are underpowered
below ~50. The bunching tests need enough mass near the threshold to fit a
counterfactual and return a note rather than a p-value when they do not; the
density-jump test wants ≥ 30 statistics within its bandwidth on each side,
and the decomposition ≥ 30 early-stage projects with variation in continuation. Elliott
et al. and the follow-up work on when p-hacking is detectable are clear that
none of these tests has much power against *mild* hacking; a clean report from a
small collection means very little.
