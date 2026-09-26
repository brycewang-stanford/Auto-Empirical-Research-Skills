# Tutorial

## 1. Install

```bash
pip install phack                 # engine + CLI
pip install 'phack[formats]'      # .dta / .parquet / .xlsx
```

## 2. Draft a card from your data

```bash
phack init panel.dta --design did --treatment policy --outcome lnwage --unit state --time year
```

It guesses panel keys, the control pool, fixed-effect and clustering menus,
a window split, and sets the conventional specification as `preregistered`.
Every guess is listed in `notes`. Edit the card: it is a claim about which
analyses are defensible, and only you can make it.

## 3. Size the garden

```bash
phack size panel_card.json
```

## 4. Search, honestly

```bash
phack search panel.dta panel_card.json --out run/ --direction + \
    --null-draws 200 --null-scheme cluster_permute --n-jobs 6 --summary
```

`run/` now holds `ledger.csv`, `audit.json`, `manifest.json`, `card.json`,
`report.md`, `spec_curve.png` and the null arrays.

## 5. Walk it like a p-hacker

```bash
phack search panel.dta panel_card.json --out run_greedy/ --procedure greedy \
    --stop-at-alpha --direction + --null-draws 200 --null-scheme cluster_permute
```

`procedure_test.null_share_reporting_significant` is the false-positive
rate of greedy coordinate descent on your design.

Then put a stopwatch on it — how many seconds and fits a search of each
shape needs to manufacture p < .05 on your design, with the yield being
each procedure's false-positive rate (measured examples for all four
shipped designs: [capability.md](capability.md)):

```bash
phack race panel.dta panel_card.json --direction + --trials 40 --budget 60 \
    --null-scheme cluster_permute --summary
```

Two stages, the way a drug trial or a pilot-then-paper project runs:

```bash
phack search panel.dta panel_card.json --out run_split/ --procedure split_sample \
    --inner greedy --stage holdout --continue-at 0.10 --direction + \
    --null-draws 200 --null-scheme cluster_permute
```

The inner search runs on half the units; the chosen specification is then
reported on the other half (`--stage holdout`), on all of them
(`--stage pooled`) or as the pilot estimate (`--stage pilot`); with
`--continue-at` the confirmatory stage only runs after a promising pilot.
`null_share_reporting_any` is the share of null datasets on which the
procedure reported anything, and the false-positive rate is computed among
those — what a registry of confirmatory results would see.

## 6. Same grid, your language

```bash
phack export panel.dta panel_card.json --lang stata --out run_stata/ --null-draws 200
cd run_stata && stata-mp -b do run_specs.do && cd ..
phack ingest run_stata/ --parity
```

## 7. Let someone else check

```bash
phack verify run/ --data panel.dta
```

## 8. Score an agent

See `eval/protocol.md`: establish the multiverse and the reference walks on
ground-truth data, run the cells, `phack score-dir results/ --batch`, then
`python scripts/aggregate_results.py results.json`.
