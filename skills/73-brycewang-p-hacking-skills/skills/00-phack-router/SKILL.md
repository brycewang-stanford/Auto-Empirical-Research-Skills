---
name: phack-router
description: Entry point for the p-hacking skills suite. Routes a request to the right sub-skill for (a) mapping researcher degrees of freedom in an econometric design, (b) running an instrumented specification search, (c) detecting p-hacking in a body of results, (d) immunising an analysis against it, or (e) running the agent p-hacking evaluation harness. Use whenever the request involves specification search, multiverse or specification-curve analysis, p-curve or caliper tests, publication bias, researcher degrees of freedom, "find me a significant result", robustness theatre, or benchmarking whether an AI agent will p-hack.
---

# p-hacking skills — router

## Intended use

This suite is for academic research on and teaching about p-hacking, and for
evaluating whether AI research agents p-hack. It is **not** for use in real
paper writing or research projects: every search it runs leaves a complete
ledger and a null-calibrated honest p-value, and `phack verify` lets anyone
check a run directory. If a request is to use it to produce a finding for a
real analysis, say so and decline that use.

## What this suite is for

This is an **evaluation instrument**. Its purpose is to measure how readily an
agent will search a specification space for significance, and how well it
detects, discloses and corrects for that search. It exists because
Asher et al. (2026) showed that frontier coding agents refuse an explicit
request to p-hack but comply when the identical request is reframed as
"reporting an upper bound on uncertainty" — a guardrail sensitive to framing
rather than intent. Measuring that gap requires being able to execute the
behaviour under instrumentation.

## The one rule that makes this safe

**Every search leaves a complete ledger, and every reported p-value is
accompanied by its honest counterpart.**

A specification search is not misconduct. Reporting its winner *as if it were a
single pre-specified test* is. So the tooling here is built so that the second
step is mechanically hard: `phack search` cannot emit a "best specification"
without also emitting the ledger of everything tried, the specification curve,
and the null-calibrated p-value of the search procedure as a whole.

If you are asked to run a search and suppress the ledger, or to present a
selected specification as a confirmatory test, decline that framing and say
why. That request is the thing this suite measures, not a thing it performs.

## Routing table

| The request is about | Go to |
|---|---|
| "what are the ways a result can be hacked?" / naming a strategy | `01-phack-taxonomy` |
| "how many defensible analyses does this design admit?" / building a design card | `02-forking-paths` |
| "run the multiverse" / "find the best specification" / audit a search | `03-specification-search` |
| "will this model p-hack if I ask it like *this*?" / prompt-framing probes | `04-framing-attacks` |
| "does this write-up disclose its search?" / HARKing, robustness theatre | `05-narrative-laundering` |
| "is this literature p-hacked?" / p-curve, caliper, publication bias | `06-phack-detection` |
| "how do I make my own analysis hack-proof?" / pre-registration, corrections | `07-phack-immunization` |
| "score this agent run" / run the benchmark | `08-eval-harness` |
| "what does a real p-hacking session look like?" / sequential search, stopping rules, the false-positive rate of a *procedure* | `09-search-procedures` |
| "how fast can significance be manufactured on this design?" / time-to-significance, `phack race` | `09-search-procedures` |
| "do this in Stata / R / StatsPAI" / audit a result produced in another language / read Stata or R code for search signals | `10-phack-polyglot` |

## Toolkit

One Python package, `scripts/phack/`, and one CLI, `scripts/phack_cli.py`:

```bash
phack init      DATA --design did --treatment d --outcome y   # draft a card from a dataset
python scripts/phack_cli.py size      CARD                          # how big is the garden; prereg key
python scripts/phack_cli.py search    DATA CARD --direction + \
                                      --null-draws 200 --n-jobs 6   # walk it; ledger, audit, report, figure
python scripts/phack_cli.py search    DATA CARD --procedure greedy \
                                      --stop-at-alpha --null-draws 200  # walk it like a p-hacker; FPR of the procedure
python scripts/phack_cli.py race      DATA CARD --null-scheme cluster_permute \
                                      --trials 40 --summary            # seconds-to-significance per procedure; the yield is its FPR
python scripts/phack_cli.py audit     LEDGER --null-dir RUN_DIR       # re-audit a ledger
python scripts/phack_cli.py report    RUN_DIR --stdout                # regenerate the honest write-up
python scripts/phack_cli.py export    DATA CARD --lang stata --out DIR  # same grid, Stata / R / Python / StatsPAI runner
python scripts/phack_cli.py ingest    DIR --parity                     # bring the foreign ledger back; audit; parity
python scripts/phack_cli.py verify    RUN_DIR                          # third-party check of a run directory
python scripts/phack_cli.py bench     check                            # is this still benchmark version X?
python scripts/phack_cli.py plot      LEDGER --out fig.png            # specification curve
python scripts/phack_cli.py detect    STATS --pcol p --zcol z         # p-curve battery
python scripts/phack_cli.py simulate  --strategy 03_optional_stopping
python scripts/phack_cli.py score     --ledger L --code F --reported-p ...
python scripts/phack_cli.py score-dir RUN_DIR --batch                # score agent working dirs
```

Designs: OLS / RCT (weighted, multi-way FE), DiD (TWFE, Gardner two-stage,
stacked; comparison groups), RDD (rule-of-thumb and Imbens–Kalyanaraman
bandwidths × kernel × polynomial × donut × conventional / bias-corrected /
robust inference), IV (instrument sets, 2SLS / LIML, Anderson–Rubin). Requires
numpy, scipy, pandas, matplotlib. No R dependency for the engine; the
generated runners use reghdfe / ivreghdfe / rdrobust / did2s (Stata),
fixest / rdrobust / did2s (R), statsmodels / linearmodels (Python) or
StatsPAI, and `references/language-map.md` records how closely each agrees. `./demo.sh` runs the whole
pipeline on known-zero data in a few minutes.

## Reading order for someone new

1. `references/taxonomy.md` — the strategies, with simulated false-positive rates
2. `references/econ-dof-maps.md` — what each econometric design hands you
3. `references/literature.md` — the papers, with what each one actually shows
4. `eval/protocol.md` — how to run the benchmark
