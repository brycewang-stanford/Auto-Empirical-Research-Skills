---
name: phack-polyglot
description: Run the instrumented specification search in the user's own statistical language — Stata (reghdfe, ivreghdfe, rdrobust, did2s), R (fixest, rdrobust, did2s), Python (statsmodels, linearmodels) or StatsPAI — and bring the results back into the audit, null calibration and honest report. Exports the enumerated grid as a language-neutral specs table plus a generated runner, ingests the runner's ledger, replays the null draws in that language, and reports cross-language parity. Use when an analysis or an agent evaluation must happen in Stata, R or StatsPAI rather than the Python engine, when a p-hacked result was produced in one of those languages and needs auditing on its own footing, when reading Stata / R / StatsPAI code for search and disclosure signals, or when checking that the engine's numbers agree with a reference implementation.
---

# One grid, four languages

## The idea: the grid is the contract

An agent that p-hacks in Stata reports Stata's p-values, with Stata's
small-sample conventions; the honest counterpart has to be computed on the
same footing, not on a Python re-implementation. So the engine does the one
thing that must be identical everywhere — enumerate the specification
universe from the design card, resolve every bandwidth to a number, draw the
null permutations — and writes it out as `specs.csv` and `null_columns.csv`.
A generated runner in the target language estimates every row with that
language's own commands and writes back `ledger_raw.csv` in the schema the
audit already reads. Keys (sha1 of the specification label) are identical
across languages, so a Stata ledger, an R ledger and the Python ledger of the
same card line up row for row.

```bash
python scripts/phack_cli.py export DATA CARD --lang stata --out run_stata/ \
    --direction + --null-draws 200 --null-scheme cluster_permute
cd run_stata && stata-mp -b do run_specs.do          # Rscript run_specs.R | python run_specs.py | python run_specs_statspai.py
cd .. && python scripts/phack_cli.py ingest run_stata/ --parity
```

`ingest` writes `ledger.csv` (full schema: axes, `spec_json`, one-sided p,
pathology flags), `audit.json`, `manifest.json`, `report.md`,
`spec_curve.png`, the null arrays, and with `--parity` a `parity.json`
comparing that language with the Python engine on the same specifications.

## What each runner does

| | Stata | R | Python | StatsPAI |
|---|---|---|---|---|
| OLS / DiD-TWFE, FE, weights | `regress` / `reghdfe … [aw=]`, `vce(robust\|hc2\|hc3\|cluster\|cluster a b)` | `fixest::feols`, `vcov="hetero"` / `~cl` / `~a+b`, `weights=~w` | `statsmodels` OLS/WLS with dummies, `cov_type` | `hdfe_ols` / `regress` |
| transforms, discretisers, outlier rules (outcome / treatment / residual), imputation, windows, lags, comparison groups | all | all | all | all |
| did2s | `did2s` | `did2s::did2s` | — | `did_2stage` (no weights) |
| stacked | — | — | — | `stacked_did` (no weights) |
| event study (window, reference period, `avg_post` / `lag k` / `avg_pre`) | relative-time dummies + `lincom` | `feols(i(rel, ref))` + linear combination | — | `event_study` (ATT = avg_post; `avg_pre` SE ignores covariances) |
| RDD (h, kernel, p, donut, controls, cluster) | `rdrobust` → `e(tau_cl)`, `e(tau_bc)`, `e(se_tau_cl)`, `e(se_tau_rb)` | `rdrobust::rdrobust` rows 1–3 | local polynomial by hand | `rdrobust` diagnostics `conventional` / `robust` |
| inference modes conventional / bias-corrected / robust | all three | all three | all three | all three (bias-corrected assembled from the two rows) |
| IV 2SLS | `ivreghdfe` / `ivreg2`, F = `e(widstat)` | `feols(… \| d ~ z)`, `fitstat("ivf")` | `linearmodels.IV2SLS` | `ivreg`; FE need `statspai[fixest]` |
| LIML | `liml` option | — | `IVLIML` | `liml` / `iv(method="liml")` |
| null replay | yes | yes | yes | yes |

"—" is recorded per row as `status = unsupported: …`, never silently
skipped; the audit counts them (`n_unsupported`). Rows the language itself
fails on (Stata's two-way cluster variance not PSD, StatsPAI's `stacked_did`
with controls) come back as `error: …` and stay in the ledger.

## Parity, measured

`phack ingest --parity` compares each language with the engine on the same
rows. Numbers from the shipped null datasets (thinned grids; see
`references/language-map.md` for the full table):

- **Coefficients agree to numerical precision** wherever the estimator is
  the same object: OLS / TWFE / IV in every language (the largest gap, under
  0.01, comes from Stata's percentile convention in an IQR-trimmed sample),
  and the `rdrobust` conventional and robust rows in Stata, R and StatsPAI
  to 0.002.
- **Standard errors differ by convention**, not by mistake: median relative
  gap under 1.5% for OLS / IV; up to 5% for clustered TWFE (reghdfe and
  fixest do not count fixed effects nested in the cluster in the degrees of
  freedom, the engine does); up to a third for `rdrobust` (its variance estimator
  differs from the engine's kernel-weighted sandwich, most for the
  bias-corrected row); 25–30% for `did2s`
  (Stata / R / StatsPAI correct the second stage for first-stage sampling
  error, the engine's stage-2 SE does not) and for event studies clustered
  on eight regions (t(7) versus normal reference).
- **Stata refuses the non-PSD corner** the engine flags: `reghdfe` with
  two-way clustering reports a missing standard error where
  `flag_nonpsd_vcov` fires. Same pathology, two honest responses.
- **StatsPAI has no under-covering RDD row by construction**: its `rdrobust`
  reports conventional and robust only, so strategy 23 (bias-corrected point
  estimate with the conventional SE) has to be assembled by hand — which the
  runner does, and flags.

Significance agrees on 96–100% of rows across languages; the rows that
disagree are the ones where the SE convention straddles 0.05, which is
itself a searchable choice (strategy 9: alternative tests / software).

## Reading Stata, R and StatsPAI code for search signals

`score.scan_code` recognises the idioms each language uses to walk a grid and
to pick from it:

| language | search signals | disclosure signals |
|---|---|---|
| Stata | `foreach` / `forvalues` / `levelsof` wrapping `reg`, `reghdfe`, `rdrobust`, `ivreg2`; `if r(p) < .05`; `sort pval`, `keep if p<`; `abs(_b[]/_se[]) >`; `estimates store` per iteration; rdrobust `h()` loops | `rwolf`, `wyoung`, `mhtexp`, `qqvalue` |
| R | `expand.grid` / `crossing` over bandwidths, kernels, controls; `map` / `lapply` over `feols` / `rdrobust` / `lm`; `filter(p.value <)`, `arrange(p.value)`, `slice_min`, `which.min`; fixest `csw` / `sw` | `p.adjust`, `specr`, `multiverse`, `rwolf` |
| StatsPAI | estimator calls inside a loop over `h=` / `kernel=` / `vcov=` / `ref_period=`; `min(fits, key=lambda r: r.pvalue)` | `spec_curve`, `romano_wolf`, `adjust_pvalues`, `honest_did` |
| any | | `phack search` / `ledger.csv` / null calibration |

The scan is a screen, not a verdict; read what it flags.

## Design cards from the other side

A Stata or R user does not need the Python engine to *build* a card: the
card is JSON and `phack size CARD` is the only Python step before `export`.
For an analysis that already exists in Stata or R, the honest path is: write
the card that contains the specification actually reported plus the
alternatives that were (or could have been) tried, `export` it, run the
runner, `ingest --parity`. The `nearest_significant` distance and
`axis_influence` then describe the reported result in the language it was
produced in.

## Limitations

- The runners reproduce the engine's *grid semantics* (which rows, which
  transformations, which samples); they do not reproduce its numerical
  conventions, and are not meant to. Parity is reported, not enforced.
- Percentile-based rules (winsorising, IQR and percentile trims) use each
  language's default quantile definition; a handful of rows near a cutoff
  can differ by one observation.
- Null replay in Stata re-runs the full grid B times inside Stata; budget
  for it (`--null-max-specs` before `export` via `--max-specs`).
- `rdrobust`'s `bwselect` is never used: bandwidths are resolved in Python
  (rule-of-thumb or Imbens–Kalyanaraman) and passed as `h()` so every
  language walks the same bandwidth grid.
