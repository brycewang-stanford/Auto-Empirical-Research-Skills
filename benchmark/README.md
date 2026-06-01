# AERS Benchmark

A small, **reproducible, dependency-free** benchmark of empirical-research agent
behavior. Where [`eval-harness/`](../eval-harness/) checks *properties of an agent's prose*,
the benchmark checks *numbers*: given a real dataset with a known answer, does
the pipeline recover it — and does it avoid the trap a naive pipeline falls into?

## Task: `lalonde-recovery`

The LaLonde (1986) / Dehejia–Wahba (1999) data is the canonical observational
causal-inference stress test, already vendored in this repo at
[`demo-notebooks/_lalonde_data.csv`](../demo-notebooks/_lalonde_data.csv)
(185 treated from the NSW experiment, 429 non-experimental CPS controls).

The lesson the benchmark encodes, all reproducible from the data:

| Quantity | Value | Meaning |
|---|---:|---|
| Naive ATT on `re78` | **−$635** | Treated earn *less* than the mismatched CPS controls — the naive comparison misleads. |
| Covariates with \|SMD\| > 0.25 | **5 of 8** | Severe pre-treatment imbalance (black, married, re74, re75, hispan). |
| Regression-adjusted ATT | **+$1,548** | Conditioning on pre-period earnings flips the sign to positive. |
| Experimental benchmark | **≈ +$1,794** | Dehejia–Wahba (1999), from the original randomized NSW experiment. |

A pipeline that handles this correctly **surfaces the imbalance**, **does not
report −$635 as the causal effect**, and after adjustment **recovers a positive
estimate near the experimental benchmark**.

## Task: `card-iv-recovery`

Card (1995) instruments years of schooling with proximity to a 4-year college
(`nearc4`), data vendored at
[`demo-StatsPAI-skill/data/card.csv`](../demo-StatsPAI-skill/data/card.csv)
(3,010 observations). All values reproducible from the data:

| Quantity | Value | Meaning |
|---|---:|---|
| OLS return to schooling | **0.075** | Naive OLS estimate of the wage return. |
| IV return to schooling | **0.131** | 2SLS with `nearc4` — *exceeds* OLS, the canonical surprise. |
| First-stage F (`nearc4`) | **13.3** | Real but only moderately strong instrument; must be reported. |

A pipeline that handles IV correctly recovers a positive OLS return, an IV return
that **exceeds** it, and **reports the first-stage strength** instead of assuming
the instrument is strong.

## What makes the golds trustworthy

The checker **recomputes** the data-derived golds (imbalance count, the true
naive ATT, the true SMD table) from the dataset every run, then compares the
candidate's reported numbers against them. A candidate cannot pass by fabricating
a clean balance table or a flattering effect — the `honest-reported-numbers`
gold cross-checks reported values against the data (see the anti-fabrication test
below). Only the experimental benchmark (~$1,794) is a literature constant, and
its gold is marked non-required and generously toleranced, because observational
methods are genuinely not guaranteed to nail it.

## Run it

```bash
# 1. Produce the reference candidates (pure-stdlib pipelines, one per task)
python3 benchmark/reference_pipeline.py

# 2. Grade all tasks against the golds
python3 benchmark/check_benchmark.py
#    -> lalonde-recovery 15/15, card-iv-recovery 14/14, no required failures

# 3. Grade one task / a real agent run (drop its results.json in a candidate dir)
python3 benchmark/check_benchmark.py --task card-iv-recovery
python3 benchmark/check_benchmark.py --candidate <run-name>
```

### Candidate `results.json` schema

```json
{
  "task": "lalonde-recovery",
  "method": "OLS regression adjustment (full controls incl. re74, re75)",
  "n_treated": 185, "n_control": 429,
  "naive_att": -635.0,
  "adjusted_att": 1548.2,
  "balance": {"age": -0.242, "black": 1.668, "married": -0.719, "...": 0.0}
}
```

Any pipeline (the StatsPAI/Python/R/Stata skills, or an agent run) can emit this
shape; the checker is pipeline-agnostic.

## Files

```
benchmark/
  tasks/lalonde-recovery.toml   # observational DiD/matching recovery task
  tasks/card-iv-recovery.toml   # IV (returns-to-schooling) recovery task
  lib/lalonde.py                # pure-stdlib loaders, SMD, naive ATT, OLS
  lib/card.py                   # pure-stdlib OLS+SE, first-stage F, 2SLS
  reference_pipeline.py         # writes candidates/reference-ols + reference-iv
  check_benchmark.py            # grades all tasks, recomputing data golds
  candidates/reference-*/       # the committed reference candidates
  results/                      # generated scorecards
```

## Anti-fabrication, demonstrated

Tampering with a candidate to claim perfect balance and a positive naive effect
fails four required golds, including the cross-check that recomputes from data:

```
[FAIL]* surfaces-imbalance        0 covariates with |SMD|>0.25 (need >= 3)
[FAIL]* naive-is-negative         naive_att = 2000.0 (want negative)
[FAIL]* adjusted-flips-positive   swing -452, need +1000 & positive
[FAIL]* honest-reported-numbers   naive_att 2000.0 vs true -635.0; SMD[black] 0.01 vs true 1.668
Score: 2/15
```

## Extending

Add a task by dropping a new `tasks/<id>.toml`, a `compute_truth` branch, and any
new gold-check handlers in `check_benchmark.py`. A good next candidate is a
staggered-DiD recovery task on simulated data with a known ATT (verifying a
pipeline recovers the true effect with Callaway–Sant'Anna and not biased TWFE).
