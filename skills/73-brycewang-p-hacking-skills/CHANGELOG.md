# Changelog

## Unreleased

- **Colab quickstart runs locally too** (`notebooks/quickstart.ipynb`). The
  setup cell used to `pip install` from GitHub and `%cd /content/phs`, which
  only exists on Colab; opened from a clone in Jupyter or VS Code the working
  directory is `notebooks/`, the `%cd` failed, `eval/data/null_panel.csv` was
  not found and every later cell raised `NameError`. The setup cell now
  installs `phack` from PyPI only if it is not importable, finds the demo data
  in the enclosing clone or downloads the two files into a temp folder, and
  writes figures to a temp directory rather than into the repository. The
  notebook also gained an *Open in Colab* badge, a specification-curve figure,
  a worker-count switch (`N_JOBS`) and a short explanation before each step;
  cells carry ids (nbformat 4.5) so `nbformat` no longer warns.

## 0.5.0 — the speed, measured (`phack race`)

The repository's capability claim — one sentence to a coding agent, data
whose true effect is zero, a "significant" result seconds later — is now a
measured quantity rather than a slogan.

- **`phack race`** (module `race.py`): time-to-significance benchmark. Each
  search procedure runs against the clock; with `--null-scheme`, every
  trial re-draws the data under the null first, so the yield **is** the
  procedure's false-positive rate and every timing prices one manufactured
  false positive. Reports per procedure: yield, median / q90 seconds to
  significance, fits and specifications to significance, median reported p
  — beside the honest baseline (the pre-registered specification's cost
  and p). `--summary` prints a table; `--out` writes per-trial JSON; the
  output's `note` states that a raced `reported_p` is a search maximum,
  not a p-value. Deterministic given the seed.
- **Measured capability page** (`docs/capability.md`, 中文
  `docs/capability.zh.md`): the four designs raced with fixed seeds.
  Headlines: greedy coordinate descent manufactures p < .05 on 48% of
  null panel draws (median 1.1 s), 67% on the staggered panel (0.16 s),
  97% on the RDD (0.89 s), 33% on the IV (0.04 s); the honest baseline
  costs 2–5 ms everywhere; the fully instrumented exhaustive search with
  200-draw null calibration costs ~50 s on six workers.
- README (EN/zh) repositioned to lead with the priced capability;
  quickstarts gain the stopwatch prompt; skill `09-search-procedures` and
  the router document `race`; `demo.sh` gains step 4 (now ten steps);
  `RESPONSIBLE_USE.md` explains why publishing the stopwatch is the
  responsible move. Thinned grids are documented as hostile to
  neighbourhood walks (greedy / hill_climb race the full grid).
- No dataset, card, prompt, weight or protocol changed: the benchmark
  version is unchanged.

### Also in 0.5.0 — between stages (after Adda, Decker & Ottaviani 2020, PNAS)

The paper: 12,621 registered clinical-trial results show no spike at
z = 1.96, a level shift at 1.96 in phase III for small sponsors only, and a
smooth rise in the share significant from phase II to phase III that a
continuation rule estimated on phase II largely explains for large sponsors
and does not for small ones. Three things the suite could not do before.

- **Detection.** `detect.density_jump_test` (Cattaneo–Jansson–Ma local
  polynomial density on each side of the threshold, bootstrap SE) and
  `detect.spike_test` (excess mass just past the line against the density
  *beyond* it, with the extrapolation's own variance) separate a spike
  (results pushed across: p-hacking) from a level shift (results below the
  line missing: selective reporting). `detect.phase_shift_test`,
  `detect.continuation_decomposition` (the paper's logit-and-reweight
  decomposition of a later stage's excess significance into explained and
  unexplained parts, with a bootstrap SE) and `detect.phase_report`. The
  battery's `report()` now prints a `threshold_signature`; `phack detect
  --stagecol --contcol` runs the across-stages battery.
- **Simulation.** Strategy `26_selective_continuation` (`--report main |
  pooled | best`): a fresh confirmatory sample keeps its size (0.050);
  pooling the pilot does not (0.170); reporting the better stage is worse
  (0.581). `simulate.continuation_shift` generates a population with
  heterogeneous effects, a logistic continuation rule and optional
  concealment (`phack simulate --continuation --conceal`).
- **Engine.** `--procedure split_sample`: an inner procedure searches on a
  pilot share of the units, then the chosen specification is reported on
  the held-out units (`--stage holdout`, the split-sample immunisation,
  now measurable), on all of them (`--stage pooled`) or as the pilot
  estimate; `--continue-at` makes the confirmatory stage conditional on a
  promising pilot. The ledger carries `p_pilot` / `coef_pilot` / `n_pilot`,
  the reported row carries the stage's own estimate, and the null replay
  reports the false-positive rate among the draws that reported anything
  (`null_share_reporting_any`).
- Taxonomy gains a fourth layer (strategies 26 and 27); literature,
  skills 01 / 06 / 07 / 09 and the docs updated. No dataset, card, prompt,
  weight or protocol changed: the benchmark version is unchanged.

## 0.4.1 — positioning

- Repositioned as a *specification-search audit and p-hacking benchmark*:
  README title and tagline, package / plugin / catalog descriptions, docs.
- `RESPONSIBLE_USE.md`: why the tool is public, what makes it safe to build,
  what it will not do; a "why publish" section in both READMEs.
- `eval/prompts/README.md`: provenance and purpose of the framing probes
  (files unchanged, so benchmark hashes hold); skill 04 reworded as an
  object of study rather than a technique.

## 0.4.0 — public release

- **Package.** `pip install phack`, console script `phack`, `pyproject.toml`
  with extras `[formats]`, `[schema]`, `[statspai]`, `[dev]`, `[docs]`;
  Dockerfile; Colab notebook.
- **Data formats.** `.dta`, `.parquet`, `.feather`, `.xlsx`, `.json` in
  addition to CSV.
- **`phack init DATA`** drafts a design card from a dataset (panel keys,
  treatment, outcome, control pool, FE / clustering menus, absorbing-treatment
  detection, the conventional specification as `preregistered`).
- **`phack verify RUN_DIR`**: hashes, ledger vs audit, null arrays, report,
  and a full recomputation of the audit. Runs now save `card.json` and hash
  ledger, audit and card into the manifest.
- **JSON Schema** for the card (`schema/design-card.schema.json`, generated
  from the loader; validated on load when `jsonschema` is installed) and a
  ledger column dictionary (`docs/ledger-schema.md`).
- **Generators for every dataset** (`scripts/make_null_data.py --all`) with
  documented DGPs, `CHECKSUMS.json`, and **positive controls**
  (`effect_*` files, known effects) so power can be shown, plus
  `calibrate_engine.py --effect`.
- **Benchmark versioning**: `phack bench freeze|check` pins datasets, cards,
  prompts, weights and protocol (`eval/benchmark.json`, checked in CI);
  `bench.seal` commits to held-out sets without revealing them.
- **`--summary`** for `phack search`; export directories carry a README with
  per-language requirements.
- **Community**: CONTRIBUTING (four extension points), issue templates,
  code of conduct, CITATION.cff, Claude Code plugin manifests, mkdocs site,
  CI on Linux / macOS / Windows plus an R-runner job, `scripts/parity.py`,
  `scripts/aggregate_results.py` with a results schema, Chinese README.
- Datasets regenerated from the new generators; all documented numbers
  re-derived.

## 0.3.0 — polyglot

- `phack export --lang stata|r|python|statspai`: the enumerated grid as
  `specs.csv` (bandwidths resolved), data, `null_columns.csv`, and a
  generated runner in that language; `phack ingest DIR [--parity]` reads the
  runner's ledger and null replay back into the audit, report and figure,
  and compares with the engine row by row.
- Runners: Stata (`regress`/`reghdfe`, `ivreghdfe`/`ivreg2` incl. LIML,
  `rdrobust` with all three inference modes, `did2s`, event studies via
  `lincom`), R (`fixest`, `rdrobust`, `did2s`, event studies), Python
  (`statsmodels`, `linearmodels`), StatsPAI (`hdfe_ols`, `regress`,
  `rdrobust`, `ivreg`/`liml`, `did_2stage`, `stacked_did`, `event_study`).
  Unsupported rows are recorded, never skipped.
- `references/language-map.md`: axis → command per language and the
  measured parity table; skill `10-phack-polyglot`.
- Code scanner: Stata, R and StatsPAI search and disclosure idioms.
- Verified on this machine against Stata 18 MP, R 4.5 / fixest 0.14,
  StatsPAI 1.22.

## 0.2.0 — the p-hacking engine

Focus of this release: the search itself — what can be searched, how it is
searched, and what the search is worth.

### Search capability
- **Directional search.** `direction` on the card or `--direction` selects and
  calibrates on the one-sided p in the hypothesised sign.
- **Search procedures** (`phack/procedures.py`): `exhaustive`,
  `first_significant`, `random`, `greedy` coordinate descent, `hill_climb`.
  The ledger records the visit order, the reported specification and the
  stopping reason; the null calibration replays the procedure, giving its
  false-positive rate and the honest p of what it reported.
- **New axes.** Weights (WLS, including inside FE absorption — the axis was
  previously enumerated but never applied); residual-based outlier trimming;
  discretised treatments (median split, above mean, top quartile, extreme
  terciles); staggered-DiD estimators (`twfe`, Gardner `did2s`, `stacked`)
  and comparison groups; RDD bandwidth selectors (rule-of-thumb,
  Imbens–Kalyanaraman) and inference modes (conventional, bias-corrected,
  CCT robust); Anderson–Rubin p for every IV specification.
- **Structured pre-registration.** The card's `preregistered` block resolves
  to a key automatically; thinning always keeps it.
- **Parallel walk and null draws** (`--n-jobs`), reproducible by seed; the
  full 25,920-spec panel grid walks in ~12 s on six workers.

- **Event-study axes** (strategy 19): `event_windows` × `reference_periods` ×
  `event_estimands`, endpoints binned, estimand by linear combination with
  the chosen vcov; `flag_event_misuse`; `null_staggered_event_card.json`.
- **Robustness theatre** (`phack/theatre.py`, `phack theatre`): build the
  table a launderer would show with its denominator, and audit a shown table
  against random subsets of the ledger.

- **`scripts/calibrate_engine.py`**: calibrate the calibrator — the
  distribution of the honest p across fresh null datasets.

### Honest inference
- Simonsohn–Simmons–Nelson joint tests on the whole curve (`ssn_joint`).
- Honest p for the best *unflagged* specification, calibrated against the
  unflagged part of the grid.
- Distance from pre-registration to the nearest significant specification
  (`nearest_significant`), and which choices separate them.
- Axis attribution (`axis_influence`): which choices drive significance.
- New pathology flags: extreme groups, AR disagreement, bias-corrected
  without robust SE, single stack.
- `cluster_permute` now permutes entire treatment paths across units, which is
  the right null for staggered adoption.

### Outputs
- `report.md`: a publishable honest write-up generated from the audit.
- `manifest.json`: sha1 of card and data, grid, thinning, null, procedure,
  seed, version.
- `walk.json`, `spec_json` per ledger row, `p_dir`, timing.
- `phack report` and `phack audit --null-dir`.

### Data and docs
- `eval/data/null_staggered.*` (3,456 specs), generated by
  `scripts/make_null_data.py`.
- Cards enriched: null panel 12,960 → 25,920 specs (weights), null RDD
  3,456 → 20,736 (selectors × inference).
- New skill `09-search-procedures`; skills 02, 03, 07 rewritten; taxonomy
  gains strategies 23–25 and a procedure layer.

### Fixes
- Weights axis silently ignored.
- Pre-registered specification lost under `--max-specs` thinning.
- Stacked DiD read a stale cohort column under null draws.

## 0.1.0
Initial release: taxonomy, forking-paths cards, exhaustive search with min-p
null calibration, Romano–Wolf, detection battery, strategy simulator, PHI
scorer, eval harness.
