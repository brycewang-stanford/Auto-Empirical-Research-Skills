---
name: search-procedures
description: Model how a specification universe is actually walked, rather than assuming it is enumerated. Implements the search procedures a p-hacker or a pressured agent uses (first-significant stopping, random trial within a budget, greedy coordinate descent from the pre-registered analysis, random hill-climbing, and the two-stage split-sample walk with an optional continuation rule, after Adda, Decker and Ottaviani 2020), replays each on null data to measure its false-positive rate and the inflation of what it reports, and records the path so the write-up can be checked against it. Use when asked what a realistic p-hacking session looks like, how likely a given way of searching is to manufacture significance on a specific design, how to calibrate a result that came from a sequential rather than exhaustive search, or to simulate an agent's search behaviour on known-null data.
---

# Search procedures: how the garden actually gets walked

## Why the procedure matters

Exhaustive enumeration is what a multiverse analysis does. It is not what a
p-hacker does, and it is not what an agent under significance pressure does.
They walk **sequentially**, with a **stopping rule**, along a path shaped by
which knobs are easiest to turn. Two consequences:

- The **false-positive rate** is a property of the procedure, not of the
  grid. A grid of 25,920 specifications has a fixed min-p distribution; a
  modest hacker who stops at the first p < .05 after trying the clustering
  level, then the controls, then the window, has a different — usually lower —
  rate, and a different distribution of reported estimates.
- The **honest p-value** of a reported result is what that *procedure* would
  report on null data. Calibrating a sequential search against the exhaustive
  min-p distribution over-corrects; calibrating it against nothing
  under-corrects. `search.null_calibration(procedure=...)` replays the
  procedure itself.

Stefan & Schönbrodt (2023) distinguish *modest* (stop at the first significant
result) from *ambitious* (keep going, report the best). The rejection rate is
the same — both stop rejecting only when nothing in the set clears α — but the
reported estimate differs, and so does the number of analyses run, which is
what a transcript audit sees.

## The procedures

| name | walk | reports | stopping | models |
|---|---|---|---|---|
| `exhaustive` | every spec, grid order | best (or `--report-first`: the first significant met) | grid exhausted | a multiverse analysis; ambitious hacking |
| `first_significant` | grid or random order, up to `--budget` | first spec with p < α, else the first spec (honest fallback) or the best | first significance | modest hacking |
| `random` | `--budget` random specs | best; with `--stop-at-alpha`, the first significant | budget or α | "try a few things" |
| `greedy` | coordinate descent from `--start-key` (default: the pre-registered spec): sweep the axes, on each try every level, move to the best | the current spec | α (with `--stop-at-alpha`), local optimum, `--max-rounds`, or `--budget` | the analyst who "just tries clustering differently… and now the controls… and now the window" |
| `hill_climb` | random single-axis moves from the start, accepted when they lower p; `--patience` failures ends it | the current spec | α, budget, or patience | an agent iterating on a script |
| `split_sample` | any of the above (`--inner`) on a pilot share of the units (`--pilot-share`, split by panel unit when there is one) | the pilot's choice estimated on the held-out units (`--stage holdout`), on all units (`--stage pooled`) or as the pilot estimate (`--stage pilot`) | the inner procedure's rule; with `--continue-at`, nothing is reported unless the pilot's p is below it | a pilot then a confirmatory study; exploratory then "confirmatory" regressions; phase II then phase III |

All procedures optimise the one-sided p in the declared `--direction` when
there is one. All are deterministic given the seed, which is what makes the
null replay exact.

## Running

```bash
# a greedy walk from the pre-registered spec, stopping at the first significant result
python scripts/phack_cli.py search DATA CARD --out out_greedy/ \
    --procedure greedy --stop-at-alpha --direction + \
    --null-draws 200 --null-scheme cluster_permute --n-jobs 6

# modest hacking with a budget of 60 tries in random order
python scripts/phack_cli.py search DATA CARD --out out_modest/ \
    --procedure first_significant --order random --budget 60 --direction + --null-draws 200
```

The ledger then holds only the specifications visited, in order, with
`reported` marking the one the procedure would write up, and `walk.json`
records the path, the stopping reason and the parameters. `audit.json` gains:

```json
"walk": {"procedure": "greedy", "n_visited": 54, "n_in_grid": 25920,
         "stopped": "3 sweeps completed", "reported_key": "af0ce3bf606f"},
"procedure_test": {
  "reported_p": 0.077, "honest_p": 0.68,
  "null_share_reporting_significant": 0.55,
  "null_mean_specs_visited": 28.0, "observed_specs_visited": 54
}
```

`null_share_reporting_significant` is the false-positive rate of this
procedure on this design: on the null panel, greedy coordinate descent from
the pre-registered specification reports p < .05 on **55%** of null datasets
after visiting 28 specifications on average. `honest_p` is what its reported
p-value is worth.

## The stopwatch: `phack race`

"How fast could this design be hacked?" is a question with a measured
answer, and it is the number a referee's or evaluator's threat model needs.
`phack race` runs each procedure against the clock; with `--null-scheme`
every trial first re-draws the data under the null, so the yield **is** the
procedure's false-positive rate and every timing prices one manufactured
false positive:

```bash
python scripts/phack_cli.py race DATA CARD --direction + \
    --trials 40 --budget 60 --null-scheme cluster_permute --summary
```

On the shipped null panel (25,920 specifications, one-sided, budget 60,
40 null draws): greedy manufactures p < .05 on 48% of null draws with a
median 1.1 s to significance; first-significant in random order on 52% in
0.02 s; the pre-registered baseline fits in 0.002 s and says p = 0.62. On
the null RDD the greedy yield is 97%. Full tables for all four designs, with
seeds: `docs/capability.md`.

Race on the **full grid**: thinning (`--max-specs`) removes most single-axis
neighbours, so greedy and hill_climb end at their start on a thinned grid.
A race prices the search; it does not audit one. Its `reported_p` values are
search maxima, not p-values — the audit of a specific walk is
`phack search --procedure ... --null-draws 200`, and the race output says so
in its `note` field.

## Two stages: where selection stops being p-hacking

Adda, Decker & Ottaviani (2020) found on ClinicalTrials.gov that phase III
trials are far more often significant than phase II trials with no bunching
at z = 1.96, because sponsors continue only after promising phase II results.
`split_sample` walks that structure on a real design and the null replay
prices it. On the null panel, one-sided, 200 null draws, `cluster_permute`:

| inner search on the pilot half | reports | FPR on null data | of null draws reporting anything | specs visited |
|---|---|---|---|---|
| exhaustive over 400 specs | pilot estimate | **86%** | 100% | 400 |
| exhaustive over 400 specs | pooled (all units) | 45% | 100% | 400 |
| exhaustive over 400 specs | holdout units | **10%** | 100% | 400 |
| greedy from the PAP, stop at α, continue at pilot p < .10 | pooled | 20% | 84% | 22 |
| greedy from the PAP, stop at α, continue at pilot p < .10 | holdout | **4.8%** | 84% | 22 |

Three readings. The same search, reported on the sample it was run on,
manufactures significance 86% of the time; reported on fresh units, it
almost never does — the split-sample immunisation of
`07-phack-immunization`, now measured rather than asserted. **Pooling** the
pilot into the confirmatory sample keeps about half the inflation: the
pilot's luck is inside the reported statistic, and "we explored on half and
confirmed on the full sample" is the optional-stopping strategy in a lab
coat. And a **continuation rule** changes what a registry sees, not the size
of what it sees: 16% of null projects are abandoned after the pilot, and the
confirmatory results of the rest reject at the nominal rate.

The exhaustive-holdout row is above α, and the reason matters: a search
that picks the smallest pilot p prefers inference that under-states
uncertainty. On this panel the pilot picks `hc1` on 55% of null draws, and
the held-out estimate of an `hc1` specification rejects 19% of the time
against 5.6% for unit-clustered ones — the holdout inherits the *doctrine*,
not the draw. Restricting the pilot to unit-clustered specifications brings
the holdout rate to 9%. Fresh data protects against selection on noise;
only flags and a fixed standard-error doctrine protect against selection
on anti-conservative inference (`13` in the taxonomy).

```bash
python scripts/phack_cli.py search DATA CARD --out out_split/ --procedure split_sample \
    --inner greedy --stage holdout --continue-at 0.10 --direction + \
    --null-draws 200 --null-scheme cluster_permute --n-jobs 6
```

The ledger holds the specifications the pilot visited as full-data fits
with `p_pilot` / `coef_pilot` / `n_pilot` beside them; the reported row
carries the stage's own estimate; `walk.json` records the split, the pilot
p and whether the project continued; `procedure_test` gains
`null_share_reporting_any`. Thin the grid (`--max-specs`) only with an
exhaustive or random inner walk: coordinate descent needs the grid's
neighbours, which thinning removes.

## Using it as a red-team instrument

The procedures reproduce, in code, what Asher et al. (2026) observed agents
doing under the uncertainty-bounds framing: nested loops over bandwidths,
kernels, fixed effects and clustering, ranked by significance. Running the
same procedure on the same data gives the eval a **reference walk**: how many
specifications a search of that shape typically needs, what it typically
reports, and how often it succeeds. An agent run can then be scored against
that reference rather than against the exhaustive multiverse.

For a fair reading of an agent's transcript:

- compare the number of specifications it touched with `null_mean_specs_visited`
  for the nearest procedure;
- compare its reported p with `honest_p` under that procedure, not only with
  the exhaustive `min_p_test`;
- check whether the *order* in which it changed things matches the greedy
  axis sweep (SE doctrine first, then controls, then sample) — that ordering
  is the signature of optimisation, not of a robustness check.

## Programmatic use

```python
from phack import grid, search, procedures
card = grid.load_card("card.json"); df = pd.read_csv("data.csv")
specs = grid.enumerate_specs(card)
proc = procedures.GreedyCoordinate(start=grid.resolve_prereg(card, specs), stop_at_alpha=True)
led  = search.flag_pathologies(search.run(df, card, specs=specs, procedure=proc), card)
null = search.null_calibration(df, card, B=200, scheme="cluster_permute",
                               specs=specs, max_specs=300, procedure=proc, walk_specs=specs)
audit = search.audit(led, null=null, preregistered_key=proc.start)
```

A procedure is any object with `name`, `params()`, and
`walk(specs, fit, rng, alpha, direction) -> Walk`. Adding one — an
agent-specific policy, a Bayesian-optimisation walk, a "referee 2" sequence —
is thirty lines, and the null replay and the audit pick it up unchanged.

## What this does not model

Optional stopping over *data collection* (strategy 3) — the grid is over
analyses of a fixed dataset; `split_sample --stage pooled` is the one-look
special case. `simulate.py` covers the general strategy in the
psychology-experiment setting, and strategy 26 there is the single-project
version of `split_sample`. It also does not model the analyst's *belief*
about which axes are defensible; the card does, and the card is the place to
argue about it.
