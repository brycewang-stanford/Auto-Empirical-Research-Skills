"""
Third-party verification of a search run directory.

A run directory is evidence only if someone who did not produce it can check
it. `verify` checks four things and reports each separately:

  hashes      the data and card the manifest names hash to what the manifest says;
              ledger.csv, audit.json and card.json are the files the manifest hashed
  ledger      the audit's headline numbers (grid size, best specification, its p,
              the pre-registered specification) are what the ledger implies
  null        the saved null arrays have the declared shape and reproduce the
              honest p-value in the audit
  report      report.md quotes the audit's honest p and the best specification's p

`recompute=True` additionally re-runs the audit from the ledger and null arrays
and compares every top-level number. It does not re-estimate the ledger; that
is what `phack search` on the same data and card is for, and the hashes make
that re-run comparable.
"""
from __future__ import annotations

import json, os, re

import numpy as np
import pandas as pd

from . import grid, search


def _close(a, b, tol=1e-6):
    try:
        a, b = float(a), float(b)
    except (TypeError, ValueError):
        return a == b
    if np.isnan(a) and np.isnan(b):
        return True
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def verify(run_dir, data_path=None, recompute=True) -> dict:
    checks = []

    def add(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    man_p = os.path.join(run_dir, "manifest.json")
    if not os.path.exists(man_p):
        return {"ok": False, "checks": [{"check": "manifest", "ok": False, "detail": "manifest.json missing"}]}
    man = json.load(open(man_p))
    aud = json.load(open(os.path.join(run_dir, "audit.json")))
    led = pd.read_csv(os.path.join(run_dir, "ledger.csv"))

    # ---- hashes
    for f, h in (man.get("files") or {}).items():
        p = os.path.join(run_dir, f)
        add(f"hash:{f}", os.path.exists(p) and search._sha1_file(p) == h,
            "matches manifest" if os.path.exists(p) and search._sha1_file(p) == h else "file missing or modified after the run")
    dp = data_path or (man.get("data") or {}).get("path")
    if dp and os.path.exists(dp) and (man.get("data") or {}).get("sha1"):
        add("hash:data", search._sha1_file(dp) == man["data"]["sha1"],
            f"{dp} {'matches' if search._sha1_file(dp) == man['data']['sha1'] else 'DIFFERS from'} the data the search used")
    else:
        add("hash:data", False, "data file not found; pass --data to check it")
    card_p = os.path.join(run_dir, "card.json")
    if os.path.exists(card_p):
        card = grid.load_card(card_p)
        import hashlib
        h = hashlib.sha1(json.dumps(card, sort_keys=True, default=str).encode()).hexdigest()
        add("hash:card", h == man["card"]["sha1"], "card.json matches the manifest's card sha1" if h == man["card"]["sha1"] else "card.json differs")
    else:
        card = None
        add("hash:card", False, "card.json missing (runs before v0.4 did not save it)")

    # ---- ledger vs audit
    ok = led[led["status"] == "ok"] if "status" in led else led
    add("ledger:n_specs", aud["n_specs_estimated"] == len(ok) and aud["n_specs_enumerated"] == len(led),
        f"audit says {aud['n_specs_estimated']}/{aud['n_specs_enumerated']}, ledger has {len(ok)}/{len(led)}")
    direction = grid.direction_sign(aud.get("direction"))
    pcol = "p_dir" if direction is not None and "p_dir" in ok else "p"
    if len(ok):
        best = ok.loc[ok[pcol].idxmin()]
        b = aud["best_spec"]
        add("ledger:best_spec", best["key"] == b["key"] and _close(best[pcol], b.get("p_dir", b["p"])),
            f"ledger minimum {pcol} is {best['key']} ({best[pcol]:.3g}); audit reports {b['key']} ({b.get('p_dir', b['p']):.3g})")
        sig = int((ok[pcol] < aud["alpha"]).sum())
        add("ledger:n_significant", sig == aud["n_specs_significant"], f"{sig} vs {aud['n_specs_significant']}")
    if "preregistered" in aud:
        pr = ok[ok["key"] == aud["preregistered"]["key"]]
        add("ledger:preregistered", len(pr) == 1 and _close(pr.iloc[0]["p"], aud["preregistered"]["p"]),
            "pre-registered specification present and its p matches" if len(pr) else "pre-registered key not in ledger")

    # ---- null arrays
    nd = None
    if os.path.exists(os.path.join(run_dir, "null_meta.json")):
        try:
            nd = search.NullDraws.load(run_dir)
            keys = nd.specs if isinstance(nd.specs[0], str) else [s.key() for s in nd.specs]
            shape_ok = nd.t.shape == (nd.B, len(keys)) and nd.p.shape == nd.t.shape
            add("null:shape", shape_ok, f"{nd.B} draws x {len(keys)} specifications")
            if "min_p_test" in aud and len(ok):
                ledk = ok[ok["key"].isin(keys)]
                bp = float(aud["best_spec"].get("p_dir", aud["best_spec"]["p"]))
                ref = nd.min_p if direction is None else nd.min_p_dir
                hp = float((1 + np.sum(ref <= bp)) / (np.isfinite(ref).sum() + 1))
                add("null:honest_p", _close(hp, aud["min_p_test"]["honest_p"], 1e-9),
                    f"recomputed {hp:.4f} vs audit {aud['min_p_test']['honest_p']:.4f}")
        except Exception as exc:                        # noqa: BLE001
            add("null:load", False, f"{type(exc).__name__}: {exc}")
    else:
        add("null:present", "min_p_test" not in aud, "no null arrays saved" + ("" if "min_p_test" not in aud else " but the audit reports a null-calibrated p"))

    # ---- report quotes the audit
    rp = os.path.join(run_dir, "report.md")
    if os.path.exists(rp):
        txt = open(rp).read()
        want = []
        if "min_p_test" in aud:
            hp = aud["min_p_test"]["honest_p"]; want.append(f"{hp:.2e}" if hp < 1e-3 else f"{hp:.3f}")
        bp = aud["best_spec"].get("p_dir", aud["best_spec"]["p"]); want.append(f"{bp:.2e}" if bp < 1e-3 else f"{bp:.3f}")
        add("report:quotes_audit", all(w in txt for w in want), f"looking for {want} in report.md")
    else:
        add("report:present", False, "report.md missing")

    # ---- full recomputation of the audit
    if recompute and card is not None:
        try:
            keys = None
            if nd is not None:
                keys = set(nd.specs if isinstance(nd.specs[0], str) else [s.key() for s in nd.specs])
                if not isinstance(nd.specs[0], str):
                    pass
                else:
                    by = {s.key(): s for s in grid.enumerate_specs(card)}
                    nd.specs = [by[k] for k in nd.specs if k in by]
            # a procedure run is audited on everything it visited (as `phack search`
            # does), an exhaustive run on the specifications the null draws cover
            led_a = led[led["key"].isin(keys)] if (keys and "walk" not in aud) else led
            pre = (aud.get("preregistered") or {}).get("key")
            re_aud = search.audit(led_a, null=nd, preregistered_key=pre, alpha=aud["alpha"], direction=direction)
            diffs = []
            for k in ("n_specs_estimated", "n_specs_significant", "bonferroni_p_of_best", "romano_wolf_p_of_best",
                      "effective_tests", "meff_adjusted_p_of_best"):
                if k in aud and not _close(aud[k], re_aud.get(k), 1e-6):
                    diffs.append(f"{k}: {aud[k]} vs {re_aud.get(k)}")
            if "min_p_test" in aud and not _close(aud["min_p_test"]["honest_p"], re_aud["min_p_test"]["honest_p"], 1e-9):
                diffs.append("honest_p")
            add("recompute:audit", not diffs, "audit reproduced from ledger + null arrays" if not diffs else "; ".join(diffs))
        except Exception as exc:                        # noqa: BLE001
            add("recompute:audit", False, f"{type(exc).__name__}: {exc}")

    return {"ok": all(c["ok"] for c in checks), "run_dir": run_dir, "phack_version": man.get("phack_version"),
            "n_checks": len(checks), "n_failed": sum(not c["ok"] for c in checks), "checks": checks,
            "reads": "ok=true means a third party can rely on the numbers in report.md being the numbers in the ledger, "
                     "for the data and card the manifest names. It does not re-estimate the ledger: "
                     "re-run `phack search` on the same data and card to do that."}
