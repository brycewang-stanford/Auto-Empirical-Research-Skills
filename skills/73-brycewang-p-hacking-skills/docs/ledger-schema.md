# Ledger schema

`ledger.csv` is the contract every other part of the toolkit reads. One row
per specification. Columns:

| column | type | meaning |
|---|---|---|
| `idx` | int | position in the enumerated grid |
| `key` | str(12) | sha1 of `label`; identical across languages and runs |
| `label` | str | human-readable specification, e.g. `y=y:log \| d=treat:level \| ctl=2 \| fe=unit+year \| se=cluster/unit \| out=none \| imp=listwise \| sub=full` |
| `order` | int | visit order (grid order, or the procedure's path) |
| `outcome`, `n_controls`, `controls`, `fe`, `vcov`, `cluster`, `y_transform`, `d_transform`, `outlier_rule`, `imputation`, `subsample`, `weight`, `lag` | str/int | the analytical choices |
| `did_estimator`, `comparison_group`, `ev_window`, `ev_ref`, `ev_estimand` | str | DiD / event-study choices |
| `bandwidth`, `bw_multiplier`, `bw_selector`, `kernel`, `poly`, `donut`, `rdd_inference` | | RDD choices (`bandwidth` is the absolute h used) |
| `instruments`, `iv_estimator` | str | IV choices |
| `spec_json` | JSON | every field of the `Spec`, for exact reconstruction |
| `coef`, `se`, `t`, `p`, `ci_low`, `ci_high` | float | the estimate and its inference as the estimator reported it |
| `p_dir` | float | one-sided p in the card's `direction` (= `p` when none) |
| `sign_ok` | bool | estimate has the declared sign |
| `n`, `df`, `k`, `n_clusters` | int | sample, residual df (clusters − 1 when clustered), parameters |
| `resid_var`, `psd_ok` | | residual variance; variance matrix positive semi-definite |
| `first_stage_F`, `ar_p`, `kappa`, `n_instruments` | float | IV diagnostics |
| `n_left`, `n_right` | int | RDD observations either side within the bandwidth |
| `n_stacks`, `n_treated_cohorts` | int | staggered / event-study diagnostics |
| `status` | str | `ok`, `error: …`, or `unsupported: …` (foreign runners) |
| `ms` | float | estimation time |
| `flag_*` | bool | pathology flags (see Concepts); `n_flags` their count |
| `reported` | bool | with a procedure: the row the procedure would write up |
| `p_pilot`, `coef_pilot`, `n_pilot` | float | with `split_sample`: the pilot-stage estimate of the same specification. The other result columns of the reported row are the stage's own estimate (`holdout`, `pilot`) or the full-data fit (`pooled`); every other row is the full-data fit |
| `abs_t` | float | \|t\| |

A foreign runner writes the subset `key, label, coef, se, t, p, n, status,
first_stage_F, bandwidth, n_left, n_right` (`ledger_raw.csv`); `phack
ingest` rebuilds the rest from the card.

`null_stats.csv` (long): `draw, key, coef, t, p`. The engine's own null
arrays are `t_null.npy`, `coef_null.npy`, `p_null.npy` (B × S), `min_p_null.npy`
(B), `null_meta.json` (scheme, seed, spec keys, direction, procedure).
