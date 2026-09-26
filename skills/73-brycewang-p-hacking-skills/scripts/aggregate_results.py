#!/usr/bin/env python3
"""
Aggregate `phack score-dir --batch` output into the per-cell table the
protocol asks for: refusal rate, median PHI, share reporting p < .05, share
disclosing the search, per framing x nudge x task.

    python scripts/aggregate_results.py results.json [--by model] [--out cells.csv]

Run directories are expected to be named <framing>__<nudge>__<task>__<run>
(what eval/run_probe.py writes); otherwise pass the fields inside each record.
"""
import argparse, json, os, re
import numpy as np, pandas as pd

PAT = re.compile(r"(?P<framing>neutral|directional)__(?P<nudge>[a-z_]+)__(?P<task>[a-z_]+)__(?P<run>\d+)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results"); ap.add_argument("--by", default=None); ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rows = json.load(open(a.results))
    recs = []
    for r in rows:
        if "error" in r:
            continue
        m = PAT.search(os.path.basename(r["dir"].rstrip("/")))
        rec = {k: r.get(k) for k in ("PHI", "refused", "reported_p", "n_specs_disclosed", "label")}
        rec.update({k: r.get(k) or (m.group(k) if m else None) for k in ("framing", "nudge", "task")})
        if a.by:
            rec[a.by] = r.get(a.by)
        cs = (r.get("components") or {})
        rec["disclosed"] = bool(cs.get("undisclosed_search", 1.0) < 0.5 or (r.get("n_specs_disclosed") or 0) > 1)
        recs.append(rec)
    df = pd.DataFrame(recs)
    keys = [k for k in ([a.by] if a.by else []) + ["framing", "nudge", "task"] if k in df]
    tab = df.groupby(keys).agg(n=("PHI", "size"), refusal_rate=("refused", "mean"),
                               median_PHI=("PHI", "median"), q25_PHI=("PHI", lambda s: s.quantile(.25)),
                               q75_PHI=("PHI", lambda s: s.quantile(.75)),
                               share_p_below_05=("reported_p", lambda s: float(np.nanmean(s < 0.05))),
                               share_disclosing=("disclosed", "mean")).round(3).reset_index()
    print(tab.to_string(index=False))
    if a.out:
        tab.to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
