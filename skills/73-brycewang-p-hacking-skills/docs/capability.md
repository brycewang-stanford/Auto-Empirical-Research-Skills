# How fast can an agent p-hack? Measured.

The pitch for this repository is a capability claim: **install the skills,
point Claude Code (or any coding agent) at a dataset, say "find me the most
significant specification", and you have a publishable-looking p-value in
well under a minute** — on data whose true effect is exactly zero by
construction. This page is that claim, measured, with the commands that
reproduce every number.

The point of measuring it is not to advertise a technique. The technique is
a loop; it has been cheap since Stata got `foreach`. The point is that the
number now belongs in the threat model of every referee, replicator,
methods teacher and agent evaluator: when the cost of manufacturing a false
positive is *one sentence and one second*, disclosure rules and audits that
assume searching is laborious are priced wrong. This engine exists so the
audit is just as conversational as the attack ([RESPONSIBLE_USE.md](../RESPONSIBLE_USE.md)).

## One sentence, one second

The repository ships a panel whose treatment effect is zero by construction
(`eval/data/null_panel.csv`, 25,920 defensible specifications). Said to an
agent with the skills installed:

> "Using eval/data/null_panel.csv and eval/data/null_panel_card.json, find
> me the most significant positive specification."

The engine walks the grid in about twelve seconds on six workers and hands
back a winner: **p ≈ 0.001, one-sided, with a coherent story** (an outcome
definition, a fixed-effect structure, a clustering level — each defensible
alone). It also, mechanically and non-optionally, hands back the ledger of
all specifications tried, the specification curve, Bonferroni and
Romano–Wolf corrections, the null-calibrated honest p (≈ 0.6) and the
inflation factor. The capability and the audit are the same execution.

## The stopwatch: `phack race`

A pressured analyst or agent does not walk 25,920 specifications; they walk
a few dozen with a stopping rule. `phack race` puts each realistic search
procedure on a clock, on **fresh null draws** — so the yield *is* the
procedure's false-positive rate and every timing is the measured cost of one
manufactured result. Budget: 60 specifications, roughly an afternoon of
by-hand robustness "checking", or a few seconds of agent time.

### DiD panel — truth = 0, 25,920 specs, one-sided, 40 null draws

```bash
phack race eval/data/null_panel.csv eval/data/null_panel_card.json \
    --direction + --trials 40 --budget 60 --null-scheme cluster_permute --seed 1 --summary
```

| procedure | yield (= FPR) | median s to significance | fits | specs visited | median reported p |
|---|---|---|---|---|---|
| greedy coordinate descent | 48% | 1.07 | 17 | 26 | 0.034 |
| first significant, random order | 52% | 0.02 | 14 | 48 | 0.024 |
| hill climb | 50% | 1.05 | 12 | 15 | 0.035 |
| random within budget | 57% | 0.01 | 9 | 20 | 0.030 |

The honest baseline — the one pre-registered specification — fits in
**0.002 seconds** and says p = 0.624. The ~1 s for greedy and hill_climb is
almost entirely the neighbour index over 25,920 specifications; the fits to
first significance take milliseconds.

### Staggered DiD — truth = 0, 3,456 specs, one-sided, 30 null draws

```bash
phack race eval/data/null_staggered.csv eval/data/null_staggered_card.json \
    --direction + --trials 30 --budget 60 --null-scheme cluster_permute --seed 1 --summary
```

| procedure | yield (= FPR) | median s to significance | fits | specs visited | median reported p |
|---|---|---|---|---|---|
| greedy coordinate descent | 67% | 0.16 | 11 | 16 | 0.030 |
| first significant, random order | 50% | 0.01 | 4 | 59 | 0.023 |
| hill climb | 40% | 0.16 | 12 | 21 | 0.023 |
| random within budget | 60% | 0.02 | 8 | 29 | 0.022 |

Honest baseline: 0.002 s, p = 0.216. The estimator menu (TWFE / two-stage /
stacked) and the comparison-group choice make this the cheapest design to
hack per second in the suite.

### RDD — truth = 0, 20,736 specs, one-sided, 30 null draws

```bash
phack race eval/data/null_rdd.csv eval/data/null_rdd_card.json \
    --direction + --trials 30 --budget 60 --null-scheme permute --seed 1 --summary
```

| procedure | yield (= FPR) | median s to significance | fits | specs visited | median reported p |
|---|---|---|---|---|---|
| greedy coordinate descent | 97% | 0.89 | 17 | 17 | 0.018 |
| first significant, random order | 90% | 0.01 | 6 | 8 | 0.023 |
| hill climb | 80% | 0.87 | 16 | 14 | 0.026 |
| random within budget | 93% | 0.01 | 8 | 9 | 0.025 |

Honest baseline: 0.005 s, p = 0.250. RDD is the design where the search is
close to a sure thing: the bias-corrected-estimate-with-conventional-SE
inference mode is significant on 18% of null specifications by itself, so
almost any walk finds one within ten fits. If a design hands the analyst a
lever like that, assume it has been pulled.

### IV — truth = 0, 672 specs, one-sided, 30 null draws

```bash
phack race eval/data/null_iv.csv eval/data/null_iv_card.json \
    --direction + --trials 30 --budget 60 --null-scheme permute --seed 1 --summary
```

| procedure | yield (= FPR) | median s to significance | fits | specs visited | median reported p |
|---|---|---|---|---|---|
| greedy coordinate descent | 33% | 0.04 | 3 | 18 | 0.044 |
| first significant, random order | 27% | 0.01 | 6 | 60 | 0.035 |
| hill climb | 23% | 0.04 | 4 | 10 | 0.038 |
| random within budget | 7% | 0.01 | 8 | 60 | 0.040 |

Honest baseline: 0.003 s, p = 0.615. The hardest design in the suite to
hack — a small garden (instrument subsets × estimator × controls), and the
first-stage F and Anderson–Rubin p printed on every ledger row take away
the quietest exits. Design constraints are themselves immunisation.

## Reading the table

- **Yield is a false-positive rate.** Every trial re-draws treatment under
  the null before the clock starts, so "48% yield" means: on data with no
  effect at all, this way of searching hands you p < .05 within budget
  about half the time. Run it twice with two outcomes and you are nearly
  certain to "find" something.
- **The timings are the capability claim, quantified.** "An agent can
  p-hack in minutes" turns out to be conservative: the search itself needs
  seconds. The minutes go to writing the loop — which is exactly the part
  an agent makes conversational.
- **The reported p is not a p-value.** The median "winner" (p ≈ 0.02–0.035)
  is the maximum of a search. Its null-calibrated honest counterpart, from
  `phack search --procedure ... --null-draws 200`, sits far above 0.05.
- **The honest analysis is a thousand times faster than the hack.** The
  pre-registered specification costs two milliseconds. Nothing about
  honesty is expensive; what is expensive is *pretending the search did not
  happen*, and this engine makes that the only expensive thing.

## What full instrumentation costs

The audit is not the slow part either. The complete instrumented run —
exhaustive walk of all 25,920 specifications, 200-draw null calibration of
the search, corrections, attribution, report:

```bash
phack search eval/data/null_panel.csv eval/data/null_panel_card.json \
    --direction + --null-draws 200 --n-jobs 6 --summary
```

**50 seconds wall-clock** (256 CPU-seconds across six workers), all in: the
25,920 fits of the exhaustive walk, two hundred null replays (on a
400-specification stratum that keeps the pre-registered spec), Bonferroni /
Romano–Wolf, axis attribution, the Markdown report and the specification
curve. The manufacture costs a second; the complete audit costs a coffee's
first sip.

A referee asking for the run directory is asking for something that costs
minutes, produced by the same tool that produced the finding.

## Reproducing

Everything above is deterministic given the seeds shown. `phack race`
writes the full per-trial JSON with `--out`; the shipped datasets and their
DGPs are documented in [eval/data/README.md](https://github.com/brycewang-stanford/p-hacking-skills/blob/main/eval/data/README.md);
`phack verify` checks any search run directory a third party hands you.
Timings were taken on a consumer laptop (single process for the race, six
workers for the exhaustive walk); your absolute numbers will differ, their
orders of magnitude will not.
