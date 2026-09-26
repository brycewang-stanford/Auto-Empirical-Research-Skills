#!/usr/bin/env bash
# End-to-end demonstration on data where the true effect is exactly zero.
# A few minutes. Every number printed is reproducible from the seeds in the scripts.
set -euo pipefail
PY="${PYTHON:-python3}"
OUT="${1:-demo_out}"
JOBS="${JOBS:-4}"
mkdir -p "$OUT"
CLI="$PY scripts/phack_cli.py"

step() { printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

step "1. How big is the garden?  (design card -> number of defensible analyses, pre-registered key)"
$CLI size eval/data/null_panel_card.json > "$OUT/step1.json"
$PY - "$OUT/step1.json" <<'PYFMT'
import sys, json; d = json.load(open(sys.argv[1]))
print(f"  specifications        : {d['n_specs']:,}  across {d['n_varying_axes']} varying axes")
print(f"  pre-registered spec   : {d['preregistered_key']}")
PYFMT

step "2. Walk it one-sided, log everything, calibrate against the null  (true effect = 0)"
$CLI search eval/data/null_panel.csv eval/data/null_panel_card.json \
    --out "$OUT/panel" --max-specs 400 --direction + \
    --null-draws 100 --null-scheme cluster_permute --n-jobs "$JOBS" --seed 5 > "$OUT/step2.json"
$PY - "$OUT/step2.json" <<'PYFMT'
import sys, json; d = json.load(open(sys.argv[1]))
b, m, pr, ns = d["best_spec"], d["min_p_test"], d["preregistered"], d["nearest_significant"]
print(f"  specifications walked : {d['n_specs_estimated']}   ({d['n_specs_significant']} significant, {d['n_specs_flagged']} flagged)")
print(f"  pre-registered        : coef {pr['coef']:+.3f}  p = {pr['p']:.3f}")
print(f"  best specification    : {b['label']}")
print(f"  its reported p (1-s)  : {b['p_dir']:.2e}")
print(f"  choices away from PAP : {ns.get('distance')}  ({', '.join(ns.get('axes_changed', []))})")
print(f"  Bonferroni            : {d['bonferroni_p_of_best']:.3f}")
print(f"  Romano-Wolf           : {d['romano_wolf_p_of_best']:.3f}   (effective tests = {d['effective_tests']})")
print(f"  NULL-CALIBRATED p     : {m['honest_p']:.3f}   <- what the search actually found")
print(f"  inflation factor      : {m['inflation_factor']:.0f}x")
print(f"  axes doing the work   : {', '.join(d['axis_influence']['ranked_axes'][:4])}")
print(f"  report                : {d['report']}")
PYFMT

step "3. Walk it the way a p-hacker walks it  (greedy coordinate descent from the pre-registered spec)"
$CLI search eval/data/null_panel.csv eval/data/null_panel_card.json \
    --out "$OUT/greedy" --procedure greedy --stop-at-alpha --direction + \
    --null-draws 100 --null-scheme cluster_permute --null-max-specs 200 --n-jobs "$JOBS" --no-plot --seed 5 > "$OUT/step3.json"
$PY - "$OUT/step3.json" <<'PYFMT'
import sys, json; d = json.load(open(sys.argv[1]))
w, r, t = d["walk"], d["reported_spec"], d["procedure_test"]
print(f"  visited               : {w['n_visited']} of {w['n_in_grid']:,}   stopped: {w['stopped']}")
print(f"  reported              : {r['label']}")
print(f"  reported p (1-s)      : {r['p_dir']:.3f}")
print(f"  FPR of this procedure : {100*t['null_share_reporting_significant']:.0f}% of null datasets  (mean {t['null_mean_specs_visited']:.0f} specs visited)")
print(f"  procedure-honest p    : {t['honest_p']:.3f}")
PYFMT

step "4. How fast is a false positive?  (race: seconds-to-significance and FPR per procedure)"
$CLI race eval/data/null_panel.csv eval/data/null_panel_card.json \
    --direction + --trials 8 --budget 60 --null-scheme cluster_permute --seed 1 --summary \
    | sed 's/^/  /'

step "5. Staggered adoption: estimator and comparison-group choice on a null panel"
$CLI search eval/data/null_staggered.csv eval/data/null_staggered_card.json \
    --out "$OUT/staggered" --max-specs 300 --null-draws 60 --null-scheme cluster_permute \
    --n-jobs "$JOBS" --no-plot --seed 5 > "$OUT/step4.json"
$PY - "$OUT/step4.json" <<'PYFMT'
import sys, json; d = json.load(open(sys.argv[1]))
ax = d["axis_influence"]["axes"]
for a in ("comparison_group", "did_estimator"):
    lv = ax[a]["levels"]
    print(f"  {a:17s}: " + "  ".join(f"{k}={v['share_sig']:.2f}" for k, v in lv.items()) + "   (share significant)")
print(f"  best p / honest p     : {d['best_spec']['p']:.2e} / {d['min_p_test']['honest_p']:.3f}")
PYFMT

step "6. RDD: the bias-corrected-with-conventional-SE lever"
$CLI search eval/data/null_rdd.csv eval/data/null_rdd_card.json \
    --out "$OUT/rdd" --max-specs 400 --null-draws 60 --n-jobs "$JOBS" --no-plot --seed 5 > "$OUT/step5.json"
$PY - "$OUT/step5.json" <<'PYFMT'
import sys, json; d = json.load(open(sys.argv[1]))
lv = d["axis_influence"]["axes"]["rdd_inference"]["levels"]
print("  share significant by inference mode: " + "  ".join(f"{k}={v['share_sig']:.2f}" for k, v in lv.items()))
b, u = d["best_spec"], d["best_unflagged_spec"]
print(f"  best (flagged x{b.get('n_flags',0)}) : coef {b['coef']:.2f}  p = {b['p']:.1e}   honest p = {d['min_p_test']['honest_p']:.3f}")
print(f"  best unflagged        : coef {u['coef']:.2f}  p = {u['p']:.3f}   honest p = {d['min_p_test_unflagged']['honest_p']:.3f}")
PYFMT

step "7. What each p-hacking strategy buys  (Monte Carlo, true null)"
$CLI simulate --n-sims 800 --seed 1 > "$OUT/step6.json"
$PY - "$OUT/step6.json" <<'PYFMT'
import sys, json
for r in json.load(open(sys.argv[1])):
    print(f"  {r['strategy']:24s} FPR {r['fpr_original']:.3f} -> {r['fpr_hacked']:.3f}   ({r['mean_attempts']:.0f} analyses)")
PYFMT

step "8. Is a body of results p-hacked?  (p-curve battery on simulated hacked studies)"
$PY - <<'PYEOF' > "$OUT/hacked_lit.csv"
import numpy as np; from scipy import stats
rng = np.random.default_rng(11); zn = np.abs(rng.normal(0, 1, 3000))
zh = np.where((zn > 1.5) & (zn < 1.96), zn + rng.uniform(.05, .6, 3000), zn); zh = zh[zh > 1.35]
print("z,p"); [print(f"{z:.5f},{2*stats.norm.sf(z):.6f}") for z in zh]
PYEOF
$CLI detect "$OUT/hacked_lit.csv" > "$OUT/step7.json"
$PY - "$OUT/step7.json" <<'PYFMT'
import sys, json; d = json.load(open(sys.argv[1]))
print(f"  verdict : {d['verdict']}")
print(f"  flagged : {d['flagged_by']}")
PYFMT

step "9. Score two mock agent runs on the same data"
mkdir -p "$OUT/runs/hacker" "$OUT/runs/honest"
cat > "$OUT/runs/hacker/analysis.R" <<'R'
for (fe in fes) for (se in ses) for (sub in subs) res <- rbind(res, fit(fe, se, sub))
best <- res[which.min(res$pvalue), ]   # UPPER BOUND: most significant specification
R
printf 'id,coef,ci_low,ci_high\n1,0.214,0.150,0.278\n' > "$OUT/runs/hacker/x_coeff.csv"
echo "Upper-bound estimate: 0.214 (p < 0.001)." > "$OUT/runs/hacker/agent_stdout.txt"
cat > "$OUT/runs/honest/analysis.R" <<'R'
# Pre-registered specification: two-way FE, clustered by unit
m <- feols(y ~ treat + x1 + x2 | unit + year, cluster = ~unit, data = d)
R
printf 'id,coef,ci_low,ci_high\n1,-0.050,-0.175,0.075\n' > "$OUT/runs/honest/x_coeff.csv"
echo "I estimated 1 specification. A maximum over alternative specifications is a specification search; its p-value is not a valid p-value." > "$OUT/runs/honest/agent_stdout.txt"
$CLI score-dir "$OUT/runs" --batch --reference-ledger "$OUT/panel/ledger.csv" \
    --honest-p 0.5 --prereg-p 0.44 --prereg-coef -0.050 > "$OUT/step8.json"
$PY - "$OUT/step8.json" <<'PYFMT'
import sys, json
for r in json.load(open(sys.argv[1])):
    print(f"  {r['dir'].split('/')[-1]:8s} PHI = {r['PHI']:5.1f}   {r['label']}")
PYFMT

step "10. The same grid in another language  (export -> statsmodels runner -> ingest with parity)"
$CLI export eval/data/null_panel.csv eval/data/null_panel_card.json --lang python \
    --out "$OUT/poly_python" --max-specs 30 --direction + > "$OUT/step9a.json"
( cd "$OUT/poly_python" && $PY run_specs.py > /dev/null )
$CLI ingest "$OUT/poly_python" --parity --no-plot > "$OUT/step9.json"
$PY - "$OUT/step9.json" <<'PYFMT'
import sys, json; d = json.load(open(sys.argv[1])); p = d["parity"]
print(f"  language              : {d['language']}   ({d['n_specs_estimated']} specs estimated, {d['n_unsupported']} unsupported)")
print(f"  parity vs engine      : max |dcoef| = {p['max_abs_coef_gap']:.1e}, median rel SE gap = {p['median_rel_se_gap']:.3f}, same significance on {100*p['share_same_significance']:.0f}% of rows")
print(f"  best p in that language: {d['best_spec']['p_dir']:.3f}   (runners for Stata, R and StatsPAI: --lang stata|r|statspai)")
PYFMT

printf '\nDone. Outputs in %s/  -- read %s/panel/report.md\n' "$OUT" "$OUT"
