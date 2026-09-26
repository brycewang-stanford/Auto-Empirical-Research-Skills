# Python API

```python
from phack import grid, search, procedures, race, report, polyglot, verify, bench, init_card, io
```

| function | does |
|---|---|
| `io.read_table(path)` | CSV / TSV / .dta / parquet / feather / Excel / JSON |
| `init_card.draft_card(df, ...)` | draft a design card from a table |
| `grid.load_card(path_or_dict)` | validate (JSON Schema) and fill defaults |
| `grid.enumerate_specs(card)` / `grid.universe_size(card)` | the grid and its size |
| `grid.resolve_prereg(card, specs)` | the pre-registered key |
| `grid.thin(specs, k, keep_keys)` | even thinning that keeps the anchor |
| `search.run(df, card, specs=, procedure=, n_jobs=)` | the ledger |
| `search.flag_pathologies(ledger, card)` | the flags |
| `search.null_calibration(df, card, B=, scheme=, procedure=, n_jobs=)` | `NullDraws` |
| `search.audit(ledger, null=, preregistered_key=, direction=)` | the audit dict |
| `search.nearest_significant`, `search.axis_influence`, `search.manifest` | diagnostics, manifest |
| `procedures.make(name, **params)` | `exhaustive`, `first_significant`, `random`, `greedy`, `hill_climb`, `split_sample` (two stages: `inner`, `pilot_share`, `stage=holdout|pooled|pilot`, `continue_at`) |
| `race.race(df, card, procedure_names=, trials=, budget=, null_scheme=)` / `race.summary_lines(res)` | time-to-significance benchmark: yield (= FPR under a null scheme), seconds / fits / specs to p < α, honest baseline |
| `report.honest_report(audit, manifest, card)` / `report.summary_lines(audit)` | Markdown / terminal |
| `theatre.build_table`, `theatre.audit_table` | robustness theatre |
| `polyglot.export(df, card, specs, dir, lang=, null_B=)` / `polyglot.ingest(dir)` / `polyglot.parity(dir)` | other languages |
| `verify.verify(run_dir)` | third-party check |
| `bench.freeze`, `bench.check`, `bench.seal` | benchmark versions, held-out commitments |
| `detect.report(pvals=, zstats=)` | p-curve battery |
| `simulate.sweep`, `simulate.workflow` | Stefan–Schönbrodt strategies |
| `score.score_run(...)`, `rundir.score_dir(dir)` | PHI |

Every function has a docstring; `python -c "import phack, pydoc; help(phack.search)"`.
