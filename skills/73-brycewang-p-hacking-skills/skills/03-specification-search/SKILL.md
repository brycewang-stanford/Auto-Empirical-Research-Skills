---
name: specification-search
description: Run an instrumented walk of a specification universe and recover honest inference from it. Estimates every specification in a design card (or walks it with a realistic search procedure), logs a complete ledger, flags pathological specifications, calibrates the search against an enforced null, runs the Simonsohn joint tests on the whole curve, measures how far the finding sits from the pre-registered analysis, attributes significance to the choices that produced it, and writes a publishable honest report. Use to run a multiverse or specification-curve analysis, to audit a search someone else ran, to compute multiplicity-corrected or null-calibrated p-values for a selected specification, or to demonstrate how far a search can move a result under a known-zero effect.
---

# Instrumented specification search

## The contract

This engine will walk any grid you hand it, including a grid built to find
significance, with any procedure a p-hacker would use. It will not let the walk
go unrecorded. Every run directory contains:

| file | what |
|---|---|
| `ledger.csv` | one row per specification visited, in visit order: every analytical choice, `spec_json`, coefficient, SE, t, p, one-sided `p_dir`, n, clusters, first-stage F and AR p (IV), bandwidth (RDD), pathology flags, timing |
| `audit.json` | the specification curve, the best / best-unflagged / reported / pre-registered specifications, every correction, the joint tests, the distance from pre-registration, axis attribution |
| `manifest.json` | sha1 of card and data, grid size and thinning, null scheme and draws, procedure and seed, engine version — enough to reproduce bit for bit |
| `report.md` | the honest write-up, generated from the audit so the numbers cannot drift |
| `spec_curve.png` | the figure |
| `walk.json` | with a procedure: what was visited, what was reported, why it stopped |
| `*_null.npy`, `null_meta.json` | the null draws, reloadable with `phack audit --null-dir` |

If the ledger cannot be produced, the run is a bug. If you are asked to produce
the winner without the ledger, that is the request this suite exists to
measure — name it and decline it.

## Designs

| `design` | Estimator | Design-specific axes |
|---|---|---|
| `ols` / `rct` | (W)OLS with multi-way FE absorption | controls, FE, vcov, transforms, outliers, imputation, subsamples, weights, lags |
| `did` | as above, plus `twfe` / `did2s` / `stacked`; event-study aggregates by linear combination | `did_estimators`, `comparison_groups`, `stack_window`, `event_windows` × `reference_periods` × `event_estimands` |
| `rdd` | local polynomial, kernel-weighted | `bandwidth_selectors` (rule-of-thumb, Imbens–Kalyanaraman) × `bandwidth_multipliers`, `kernels`, `poly_orders`, `donuts`, `rdd_inference` |
| `iv` | 2SLS or LIML, FE absorbed from all blocks | `instruments_pool` × `instrument_policy`, `iv_estimators`; first-stage F and Anderson–Rubin p per spec |

## Running

```bash
python scripts/phack_cli.py size CARD                      # always first

# exhaustive walk with null calibration, one-sided, parallel null draws
python scripts/phack_cli.py search DATA.csv CARD.json --out results/ \
    --direction + --null-draws 200 --null-scheme cluster_permute --n-jobs 6

# the same grid walked the way a p-hacker walks it
python scripts/phack_cli.py search DATA.csv CARD.json --out results_greedy/ \
    --procedure greedy --stop-at-alpha --direction + \
    --null-draws 200 --null-scheme cluster_permute --n-jobs 6

# re-audit or re-render later
python scripts/phack_cli.py audit results/ledger.csv --null-dir results/ --direction +
python scripts/phack_cli.py report results/ --stdout
```

`--n-jobs` parallelises both the walk and the null draws; the full
25,920-specification panel grid takes about twelve seconds on six workers.
`--max-specs` thins a very large grid by even sampling (keeping the
pre-registered specification); `--null-max-specs` (default 400) thins the grid
the null matrices are computed on. Both are recorded in the manifest and the
audit is restricted to the calibrated set, so the honest p-value is never
quietly computed on a different search than the one run. Procedures are
replayed on the *full* grid regardless, because a path is cheap.

### Direction

Almost every real search is one-sided: the hypothesis has a sign. `--direction`
(or `"direction"` on the card) makes the engine select on the one-sided p in
that direction, calibrate the null on the one-sided minimum, and count only
same-sign specifications as significant. A two-sided audit of a one-sided
search understates the multiplicity by exactly the factor of two that
motivated the search.

### Choosing a null scheme

The null draw must destroy the treatment's relationship with the outcome while
preserving everything else about the data. Get this wrong and the honest
p-value is meaningless.

| Scheme | Use when |
|---|---|
| `permute` | i.i.d. cross-section; for IV, permutes the instruments jointly (keeps d endogenous, kills relevance) |
| `cluster_permute` | panel with unit-level or staggered treatment — reassigns each unit's **entire treatment path** to another unit, preserving within-unit serial structure and the distribution of adoption dates |
| `permute_within_unit` | treatment varies within unit over time |
| `permute_within_time` | treatment assigned within period |
| `gaussian` | continuous treatment, no structure to preserve |
| *(rdd, automatic)* | outcome permuted within narrow bins of the running variable: keeps y(x) smooth, removes any jump |

For a panel with unit-level treatment, `permute` is wrong: it destroys the
serial correlation that makes clustered inference necessary and so produces a
null distribution that is far too tight.

**Calibrate the calibrator.** The honest p-value is honest only if it is
uniform on fresh null data. `scripts/calibrate_engine.py` draws K fresh
staggered null panels, runs the same grid, scheme and procedure on each, and
reports how often the honest p falls below 0.05 and a KS test of uniformity.
On 12 datasets with `cluster_permute`: 0 of 12 honest p below 0.05 (median
0.76, KS p = 0.10 — mildly conservative), while the raw best one-sided p was
below 0.05 on 7 of 12. Run it after changing a null scheme or an estimator;
a systematic excess of small honest p-values is the one way this engine could
quietly lie.

## Reading the audit

```json
{
  "direction": "+",
  "n_specs_estimated": 301, "n_specs_significant": 3, "n_specs_flagged": 126,
  "best_spec":           {"label": "y=y_alt | fe=unit | se=hc1 | out=iqr1.5 | sub=late | w=pop", "p_dir": 0.036},
  "best_unflagged_spec": {...},
  "preregistered":       {"label": "y=y | ctl=2 | fe=unit+year | se=cluster/unit", "p": 0.44},
  "nearest_significant": {"distance": 8, "axes_changed": ["outcome", "controls", "fe", "vcov", ...]},
  "bonferroni_p_of_best": 1.0,
  "romano_wolf_p_of_best": 0.93,  "effective_tests": 42.6,
  "min_p_test":           {"reported_p": 0.036, "honest_p": 0.59, "inflation_factor": 17},
  "min_p_test_unflagged": {"honest_p": 0.59, "n_unflagged_specs": 175},
  "ssn_joint": {"share_significant": {"observed": 0.017, "null_median": 0.020, "p_value": 0.56}, ...},
  "axis_influence": {"ranked_axes": ["fe", "vcov", "cluster", "outcome", "subsample"], ...}
}
```

**Corrections for the best specification**, in increasing order of trust:

1. `bonferroni_p_of_best` — correct but badly conservative, because
   specifications reusing the same rows are nearly the same test.
2. `effective_tests` — Li & Ji's count of *independent* specifications. Three
   hundred specifications routinely collapse to forty. Use it to explain why
   Bonferroni over-corrects, not as the correction itself.
3. `romano_wolf_p_of_best` — stepdown FWER control that exploits the
   dependence. The right answer when you want a per-specification statement.
4. `min_p_test.honest_p` — the headline. The share of null datasets on which
   *the identical search* found something at least as significant. Needs no
   assumption about the dependence structure because it re-runs the procedure.
5. `min_p_test_unflagged` — the same, for the best specification that carries
   no pathology flag, calibrated against the unflagged part of the grid. This
   is what a careful analyst who refused the broken corners would have found.
6. `procedure_test` — with `--procedure`: what the *procedure* reported,
   calibrated against what it reports on null data, plus its false-positive
   rate (`null_share_reporting_significant`). See `09-search-procedures`.

**Statements about the whole curve** (`ssn_joint`, Simonsohn, Simmons & Nelson
2020): the median effect, the share of significant specifications, the share
significant in the dominant direction, and a Stouffer aggregate, each against
its distribution across the null re-runs. These answer a different question
from the min-p test. A curve can lean one way everywhere (small joint p, large
min-p honest p) or have one corner do all the work (the reverse). Report both.

**Distance from pre-registration** (`nearest_significant`): the number of
analytical choices separating the pre-registered specification from the
nearest significant one, and which choices they are. Distance 1 means a single
defensible choice turns the null into a finding, which is the most dangerous
configuration a design can have; distance 8 means the finding needed a
different paper. On the full 25,920-specification null panel the distance is
3 — fixed effects, variance estimator, clustering level — which is the
distance a referee's "please also cluster by region" request covers.

**Attribution** (`axis_influence`): for every axis, the share significant at
each level and the spread across levels, ranked. This is the sentence in the
write-up that says *what* moved the result — "every significant specification
uses the bias-corrected point estimate with conventional standard errors".

## Pathology flags

`flag_pathologies` marks specifications that are searchable but not defensible.
They stay in the ledger, flagged, and `best_unflagged_spec` shows what the
search finds without them.

| flag | meaning |
|---|---|
| `flag_nonpsd_vcov` | variance matrix not positive semi-definite; two-way clustering finds this corner and returns an implausibly small SE |
| `flag_few_clusters` | under 15 clusters with cluster-robust inference |
| `flag_tiny_sample` | under a quarter of the maximum available n |
| `flag_implausible_precision` | SE under a tenth of the grid median |
| `flag_extreme_groups` | top-vs-bottom tercile treatment: the middle of the distribution discarded |
| `flag_weak_instruments` | first-stage F below 10 |
| `flag_ar_disagrees` | Wald t rejects but the weak-IV-robust Anderson–Rubin test does not |
| `flag_thin_rdd_side` | fewer than 20 observations on either side of the cutoff inside the bandwidth |
| `flag_bc_without_robust_se` | bias-corrected RDD point estimate reported with the conventional SE (CCT 2014's under-covering combination) |
| `flag_single_stack` | stacked DiD with only one adoption cohort having clean controls |
| `flag_event_misuse` | the pre-trend (`avg_pre`) reported as the effect, or a reference period inside the post window |

A "best specification" carrying flags is not a finding. In the null-RDD grid
the best specification is a half-bandwidth bias-corrected estimate with a
donut on 140 observations: coefficient 3.8 on an outcome with SD 0.6,
p = 1e-11, two flags. The best unflagged specification has p = 0.09.

## Robustness theatre

The ledger is also the denominator for any robustness table drawn from it:

```bash
python scripts/phack_cli.py theatre results/ledger.csv --reported-key KEY --k 12   # build + audit
python scripts/phack_cli.py theatre results/ledger.csv --shown k1,k2,k3,...        # audit a shown table
```

`build_table` selects the reported specification and its nearest agreeing
neighbours — the table a launderer prints — and reports what it hides:
share of the ledger shown, share agreeing, what a random table of the same
size would have contained. `audit_table` tests a shown set against random
subsets of the ledger (`p_share_significant`) and reports the hidden
specifications' share insignificant and share flipping sign. See
`05-narrative-laundering`.

## Figure

```bash
python scripts/phack_cli.py plot results/ledger.csv --out spec_curve.png \
    --prereg-key KEY --reported-key KEY --honest-p 0.59
```

`search` writes this automatically. Top panel: every estimate sorted, CI
shaded, significant ones in red, pre-registered and reported specifications
marked. Bottom panel: which choice each specification made, so the reader sees
*what* drives the curve.

## What a clean use looks like

Report the curve, not the point, and let `report.md` do it: it is generated
from the audit, contains every number above, and ends with a conclusion that
follows from the honest p rather than the reported one. If the pre-registered
specification is null and the best one is not, that is a result about the
fragility of the design, and it is publishable as such.
