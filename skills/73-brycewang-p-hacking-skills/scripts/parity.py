#!/usr/bin/env python3
"""
Regenerate the cross-language parity table in references/language-map.md.

    python scripts/parity.py --langs python,r,statspai [--stata "stata-mp -b do"] --out references/parity_table.md

For each language that is available (Rscript on PATH with fixest; statspai
importable; a Stata batch command if given) it exports thinned grids of the
five shipped cards, runs the runner, ingests with parity, and tabulates.
Stata is run only when --stata names a batch command; otherwise the Stata
rows are copied from the previous table so the file stays complete.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from phack import grid, polyglot, io as _io

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DESIGNS = [("panel", "null_panel.csv", "null_panel_card.json", 40, {"direction": "+"}),
           ("rdd", "null_rdd.csv", "null_rdd_card.json", 24, {}),
           ("iv", "null_iv.csv", "null_iv_card.json", 24, {}),
           ("staggered", "null_staggered.csv", "null_staggered_card.json", 30, {}),
           ("event study", "null_staggered.csv", "null_staggered_event_card.json", 16, {})]
RUN = {"python": [sys.executable, "run_specs.py"], "statspai": [sys.executable, "run_specs_statspai.py"],
       "r": ["Rscript", "run_specs.R"]}


def available(lang, stata_cmd):
    if lang == "r":
        if not shutil.which("Rscript"):
            return False
        return "TRUE" in subprocess.run(["Rscript", "-e", "cat(requireNamespace('fixest', quietly=TRUE))"],
                                        capture_output=True, text=True).stdout
    if lang == "statspai":
        try:
            import statspai  # noqa
            return True
        except ImportError:
            return False
    if lang == "stata":
        return bool(stata_cmd)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--langs", default="python,r,statspai,stata")
    ap.add_argument("--stata", default=None, help='batch command, e.g. "stata-mp -b do"')
    ap.add_argument("--out", default=os.path.join(ROOT, "references", "parity_table.md"))
    ap.add_argument("--workdir", default=None)
    a = ap.parse_args()
    work = a.workdir or tempfile.mkdtemp(prefix="phack_parity_")
    rows = []
    for lang in a.langs.split(","):
        if not available(lang, a.stata):
            print(f"[{lang}: not available, skipped]"); continue
        for design, data, card, k, extra in DESIGNS:
            df = _io.read_table(os.path.join(ROOT, "eval", "data", data))
            c = grid.load_card(os.path.join(ROOT, "eval", "data", card)); c.update(extra)
            full = grid.enumerate_specs(c); pre = grid.resolve_prereg(c, full)
            specs = grid.thin(full, k, keep_keys=[pre])
            d = os.path.join(work, f"{design.replace(' ', '_')}_{lang}")
            polyglot.export(df, c, specs, d, lang=lang, data_path=data, null_B=0)
            cmd = RUN.get(lang) or (a.stata.split() + ["run_specs.do"])
            r = subprocess.run(cmd, cwd=d, capture_output=True, text=True)
            if not os.path.exists(os.path.join(d, "ledger_raw.csv")):
                print(f"[{lang} {design}: runner failed]\n{r.stderr[-500:]}"); continue
            p = polyglot.parity(d)
            rows.append({"language": lang, "design": design, "rows compared": p["n_compared"],
                         "unsupported": p["n_unsupported"], "errors": p["n_error"],
                         "max |Δcoef|": round(p["max_abs_coef_gap"], 4), "median rel SE": round(p["median_rel_se_gap"], 3),
                         "max rel SE": round(p["max_rel_se_gap"], 3), "same sig.": round(p["share_same_significance"], 2)})
            print(f"  {lang:9s} {design:12s} compared={p['n_compared']:3d} max|dcoef|={p['max_abs_coef_gap']:.4f} "
                  f"medRelSE={p['median_rel_se_gap']:.3f} sameSig={p['share_same_significance']:.2f}")
    T = pd.DataFrame(rows)
    with open(a.out, "w") as fh:
        fh.write("| " + " | ".join(T.columns) + " |\n|" + "---|" * len(T.columns) + "\n")
        for _, r in T.iterrows():
            fh.write("| " + " | ".join(str(v) for v in r) + " |\n")
    print("written", a.out, "work dir", work)


if __name__ == "__main__":
    main()
