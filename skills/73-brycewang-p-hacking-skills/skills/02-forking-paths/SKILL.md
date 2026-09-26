---
name: forking-paths
description: Map the garden of forking paths for a concrete econometric design and turn it into a machine-readable design card that the specification-search engine can walk. Use when asked how many defensible analyses a dataset or research design admits, to enumerate researcher degrees of freedom for a specific DiD, IV, RDD, staggered-adoption, panel or cross-sectional study, to build or validate a design card, to encode a pre-registered specification, or to size a multiverse before running it.
---

# Mapping the garden

Before anything is estimated, work out how large the space of defensible
analyses is. That number is the multiplicity that honest inference has to pay
for, and it is almost always larger than researchers expect.

## Step 1 — read the design-specific map

`references/econ-dof-maps.md` lists, per design, the choices a referee would
accept without comment. Take only the ones that are genuinely defensible **for
this dataset**: a bandwidth grid is real for an RDD and meaningless for an RCT.

## Step 2 — write a design card

`phack init DATA [--design …] [--treatment …] [--outcome …]` drafts one:
panel keys, the treatment, a control pool, fixed-effect and clustering
menus, a window split, staggered-adoption axes when the treatment is
absorbing, and the conventional specification as `preregistered`. Every
guess is listed in its `notes`; the draft is a starting point, not a card.
`schema/design-card.schema.json` is the formal schema and the loader
validates against it when `jsonschema` is installed (`phack schema` prints it).

A design card is JSON. Each key is one axis of the grid; omitting a key
collapses that axis to a single default, which is how a pre-registered analysis
is encoded.

```json
{
  "name": "example-did",
  "design": "did",
  "direction": "+",
  "outcomes": ["y", "y_alt"],
  "treatment": "treat",
  "controls_pool": ["x1", "x2", "x3", "x4"],
  "control_policy": "all_subsets",
  "fixed_effects": [[], ["unit"], ["unit", "year"], ["region", "year"]],
  "vcov": ["hc1", "cluster", "twoway"],
  "cluster": [null, "unit", "region", ["unit", "year"]],
  "outcome_transforms": ["level", "log", "std"],
  "outlier_rules": ["none", "sd3", "iqr1.5"],
  "outlier_basis": "residual",
  "imputation": ["listwise", "mean"],
  "subsamples": {"early": "year < 2010", "late": "year >= 2010"},
  "weights": [null, "pop"],
  "did_estimators": ["twfe", "did2s", "stacked"],
  "comparison_groups": ["all", "drop_never_treated"],
  "panel_unit": "unit",
  "panel_time": "year",
  "preregistered": {
    "outcome": "y", "controls": ["x1", "x2"], "fe": ["unit", "year"],
    "vcov": "cluster", "cluster": "unit", "y_transform": "level",
    "outlier_rule": "none", "imputation": "listwise", "subsample": "full",
    "weight": null, "did_estimator": "twfe", "comparison_group": "all"
  }
}
```

Full key reference: `grid.DEFAULTS` in `scripts/phack/grid.py`. The loader
rejects unknown keys rather than silently ignoring them, because a typo that
quietly drops an axis makes the multiplicity count wrong.

### Axes by design

| Axis | Card key | Applies to | Notes |
|---|---|---|---|
| outcome definition | `outcomes` | all | strategy 1 |
| control set | `controls_pool` × `control_policy` (`none` / `nested` / `leave_one_out` / `all_subsets`) | all | strategy 5; `all_subsets` is 2^k |
| fixed effects | `fixed_effects` | ols / did / iv | strategy 14 |
| SE doctrine | `vcov` × `cluster` | all | strategy 13; a cluster variable only pairs with a clustered vcov, two-way only with a pair |
| transforms | `outcome_transforms`, `treatment_transforms` | all | strategy 7; treatment transforms include the discretisers `median_split`, `above_mean`, `quartile_top`, `tercile_extremes` (strategy 8) |
| outliers | `outlier_rules`, `outlier_basis` (`outcome` / `treatment` / `residual`) | all | strategy 4; `residual` trims on studentised residuals |
| missing data | `imputation` | all | strategy 10 |
| sample | `subsamples` (name → pandas query) | all | strategy 15 |
| weights | `weights` (column names, `null` = unweighted) | all | strategy 21; applied as WLS, including inside FE absorption |
| timing | `lags` | panel | strategy 22 |
| interactions | `interactions` | all | extra `"a*b"` regressors |
| DiD estimator | `did_estimators`: `twfe` / `did2s` (Gardner two-stage) / `stacked` (Cengiz et al.) | did | strategy 18; non-TWFE estimators fix their own FE and collapse the FE axis |
| comparison group | `comparison_groups`: `all` / `drop_never_treated` / `drop_always_treated` | did | strategy 15; the "forbidden comparison" lever |
| stack window | `stack_window` `[pre, post]` | did / stacked | periods around adoption |
| event study | `event_windows` `[[leads, lags], ...]` × `reference_periods` × `event_estimands` (`avg_post` / `lag0` / `lag1` / `avg_pre`) | did / twfe | strategy 19; endpoints binned, reference period omitted; `avg_pre` is the placebo and is flagged when reported as the effect |
| bandwidth | `bandwidth_selectors` (`rot` / `ik`) × `bandwidth_multipliers`, or absolute `bandwidths` | rdd | strategy 16 |
| kernel / polynomial / donut | `kernels`, `poly_orders`, `donuts` | rdd | strategy 16 |
| RDD inference | `rdd_inference`: `conventional` / `bias_corrected` / `robust` | rdd | strategy 23; `bias_corrected` is the under-covering combination and is flagged |
| instruments | `instruments_pool` × `instrument_policy` | iv | strategy 17 |
| IV estimator | `iv_estimators`: `2sls` / `liml` | iv | strategy 17; Anderson–Rubin p recorded per spec |
| direction | `direction`: `"+"` / `"-"` / null | all | the one-sided sign the search is after; changes which spec is "best" and the calibration |

Cohorts for the staggered estimators are inferred from each unit's treatment
path, never read from a column, so a null draw that permutes paths stays
internally consistent.

Constraints the enumerator enforces for you: cluster / vcov pairing, no fixed
effects or two-way clustering in a local-polynomial RDD, no HC2/HC3 in IV,
discretised treatments only with the plain TWFE path, and duplicate
specifications collapsed by content hash.

## Step 3 — size it before you walk it

```bash
python scripts/phack_cli.py size CARD
```

```json
{"n_specs": 25920, "dimensions": {"outcome": 3, "controls": 16, "fe": 4, "vcov": 3, ...},
 "n_varying_axes": 10, "log10_specs": 4.41, "preregistered_key": "e88cbfc3e0e7"}
```

Sizing is the deliverable on its own. A design admitting 25,920 defensible
analyses cannot support a 0.05 threshold on any single one of them: under the
null the smallest of that many correlated p-values is routinely below 0.001.
Say that number out loud before estimating anything.

## Step 4 — mark the pre-registered path

Write the `preregistered` block as a dict of axis values (any subset of
`grid.AXES`; unpinned axes default to the **first** level listed on the card,
which is the convention for "the default choice"). `size` resolves it to a
12-character key and refuses if it matches zero or several specifications.
Every later command — `search`, `audit`, `report` — reads the anchor from the
card, so there is no key to copy by hand.

Without this anchor there is no way to distinguish a search from an analysis:
`prereg_departure`, `nearest_significant` and the honest report all hang off
it.

## Thinning

`--max-specs K` walks an evenly spaced subset of a very large grid. Thinning
**always keeps the pre-registered specification** and is recorded in
`manifest.json`; the honest p-value is then computed on the grid that was
actually walked, never on a different one.

## Honest defaults when building a card

- **Include the ugly options.** A grid containing only the specifications you
  like understates multiplicity and overstates robustness.
- **Exclude the indefensible ones.** A grid padded with analyses no referee
  would accept inflates the correction and lets a weak result hide behind a
  large denominator. Both directions are cheating. The pathology flags exist
  for the options that are *citable but wrong* — non-PSD two-way clustering,
  bias-corrected RDD estimates with conventional SEs, weak-instrument
  specifications — which belong in the grid and in the ledger, flagged.
- **Weighting, timing, comparison group and aggregation are axes too.** They
  are the most commonly forgotten and among the most consequential.
- **Declare the direction.** A one-sided search is a smaller and more
  dangerous object than a two-sided one; the card should say which it is.

## Ground-truth cards that ship

| card | design | specs | what it exercises |
|---|---|---|---|
| `eval/data/null_panel_card.json` | did (within-unit treatment) | 25,920 | controls, FE, SE doctrine, transforms, outliers, imputation, windows, weights |
| `eval/data/null_staggered_card.json` | did (staggered adoption) | 3,456 | estimator choice, comparison groups, weights, windows |
| `eval/data/null_staggered_event_card.json` | did (event study) | 1,200 | event window, reference period, estimand, comparison group |
| `eval/data/null_rdd_card.json` | rdd | 20,736 | bandwidth selector × multiplier, kernel, polynomial, donut, inference mode |
| `eval/data/null_iv_card.json` | iv | 672 | instrument subsets, 2SLS / LIML, controls, FE, AR test |

All four have a true effect of exactly zero. `scripts/make_null_data.py`
regenerates the staggered panel; the other three are fixed so documented
numbers stay reproducible.
