#!/usr/bin/env python3
"""
Calibrate the calibrator.

The honest p-value is only honest if, on data where the null is true, it is
uniformly distributed -- i.e. a search on a fresh null dataset produces an
honest p below 0.05 about 5% of the time. This script draws K fresh null
datasets from the staggered generator, runs the same (thinned) grid and null
scheme on each, and reports the distribution of honest p across datasets,
for the best spec, the best unflagged spec, and a search procedure.

    python scripts/calibrate_engine.py --datasets 12 --specs 60 --draws 60 --n-jobs 6

A systematic excess of small honest p-values would mean the null scheme does
not reproduce the dependence structure of the data -- the one way the
engine could quietly lie -- and is the first thing to check after changing a
null scheme or an estimator.
"""
import argparse, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from phack import grid, search, procedures
from make_null_data import GENERATORS, EFFECTS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", type=int, default=12)
    ap.add_argument("--specs", type=int, default=60)
    ap.add_argument("--draws", type=int, default=60)
    ap.add_argument("--n-jobs", type=int, default=4, dest="n_jobs")
    ap.add_argument("--card", default=None, help="card JSON; default: the staggered card")
    ap.add_argument("--scheme", default="cluster_permute")
    ap.add_argument("--direction", default="+")
    ap.add_argument("--seed", type=int, default=100)
    ap.add_argument("--design", default="staggered", choices=list(GENERATORS),
                    help="which generator to draw fresh datasets from")
    ap.add_argument("--effect", type=float, default=0.0,
                    help="true effect; 0 measures size (honest p should be uniform), >0 measures power")
    a = ap.parse_args()
    gen = GENERATORS[a.design]
    card = grid.load_card(a.card) if a.card else grid.load_card(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eval", "data", f"null_{a.design}_card.json"))
    card["direction"] = a.direction
    full = grid.enumerate_specs(card)
    pre = grid.resolve_prereg(card, full)
    specs = grid.thin(full, a.specs, keep_keys=[pre])
    rows = []
    t0 = time.time()
    for k in range(a.datasets):
        df = gen(seed=a.seed + k, effect=a.effect)
        led = search.flag_pathologies(search.run(df, card, specs=specs), card)
        # the procedure walks the FULL grid (a path is cheap); the null matrices use the thinned one
        proc = procedures.GreedyCoordinate(start=pre, stop_at_alpha=True, budget=40)
        led_p = search.flag_pathologies(search.run(df, card, specs=full, procedure=proc, seed=k), card)
        nd = search.null_calibration(df, card, B=a.draws, scheme=a.scheme, specs=specs,
                                     keep_keys=[pre], seed=a.seed + 1000 * k, n_jobs=a.n_jobs,
                                     procedure=proc, walk_specs=full)
        au = search.audit(led, null=nd, preregistered_key=pre)
        au_p = search.audit(led_p, null=nd, preregistered_key=pre)
        rows.append({
            "dataset": k,
            "prereg_p": au["preregistered"]["p"],
            "best_p_dir": au["best_spec"].get("p_dir", au["best_spec"]["p"]),
            "honest_p": au["min_p_test"]["honest_p"],
            "honest_p_unflagged": au.get("min_p_test_unflagged", {}).get("honest_p", np.nan),
            "share_sig": au["share_significant"],
            "ssn_share_sig_p": au["ssn_joint"]["share_significant"]["p_value"],
            "greedy_reported_p": au_p["reported_spec"].get("p_dir", au_p["reported_spec"]["p"]),
            "greedy_honest_p": au_p["procedure_test"]["honest_p"],
            "greedy_fpr": au_p["procedure_test"]["null_share_reporting_significant"],
        })
        print(f"  dataset {k}: honest p = {rows[-1]['honest_p']:.3f}  unflagged = {rows[-1]['honest_p_unflagged']:.3f}  "
              f"greedy honest = {rows[-1]['greedy_honest_p']:.3f}  ({time.time()-t0:.0f}s)", flush=True)
    R = pd.DataFrame(rows)
    out = {
        "n_datasets": a.datasets, "n_specs": len(specs), "null_draws": a.draws, "scheme": a.scheme,
        "design": a.design, "true_effect": a.effect,
        "reads_effect": ("with true_effect > 0 the share_*_below_05 numbers are POWER: the honest pipeline should reject "
                         "often when the effect is real, and the pre-registered spec should too") if a.effect else None,
        "share_honest_p_below_05": float((R.honest_p < 0.05).mean()),
        "share_unflagged_honest_p_below_05": float((R.honest_p_unflagged < 0.05).mean()),
        "share_greedy_honest_p_below_05": float((R.greedy_honest_p < 0.05).mean()),
        "share_prereg_p_below_05": float((R.prereg_p < 0.05).mean()),
        "share_best_p_dir_below_05": float((R.best_p_dir < 0.05).mean()),
        "mean_greedy_fpr": float(R.greedy_fpr.mean()),
        "honest_p_quantiles": {q: float(R.honest_p.quantile(q)) for q in (0.1, 0.25, 0.5, 0.75, 0.9)},
        "ks_uniform_p": float(__import__("scipy").stats.kstest(R.honest_p, "uniform").pvalue),
        "reads": ("share_*_below_05 should be near 0.05 for the honest p-values and near 1 for the best "
                  "reported p; ks_uniform_p tests uniformity of honest p across datasets"),
    }
    print(json.dumps(out, indent=2))
    print(R.round(3).to_string())


if __name__ == "__main__":
    main()
