"""
Honest report: the write-up a search should produce, generated from the
audit so the numbers cannot drift from the ledger.

The template is the one in skills/07-phack-immunization: the curve, the
pre-registered specification and where it sits, the best specification and
what its p-value is worth, which choices did the work, and what was flagged.
It is deliberately publishable as-is and deliberately impossible to reduce to
its sixth sentence.
"""
from __future__ import annotations

import json

import numpy as np


def _f(x, nd=3):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "n/a"
    if isinstance(x, float):
        if abs(x) < 1e-3 and x != 0:
            return f"{x:.2e}"
        return f"{x:.{nd}f}"
    return str(x)


def _p(x):
    if x is None or not np.isfinite(x):
        return "n/a"
    return f"{x:.2e}" if x < 1e-3 else f"{x:.3f}"


def honest_report(audit: dict, manifest: dict | None = None, card: dict | None = None,
                  title="Specification search: honest report") -> str:
    a = audit
    L = [f"# {title}", ""]
    if manifest:
        c, d = manifest.get("card", {}), manifest.get("data", {})
        L += [f"*Design* `{c.get('design')}` · *card* `{c.get('name')}` "
              f"(sha1 `{(c.get('sha1') or '')[:8]}`) · *data* `{d.get('path')}` "
              f"({d.get('n_rows')} rows, sha1 `{(d.get('sha1') or '')[:8]}`) · "
              f"*engine* phack {manifest.get('phack_version')} · {manifest.get('timestamp')}", ""]
    direction = a.get("direction")
    dir_txt = {"+": "positive", "-": "negative", None: "either"}[direction]
    curve = a.get("curve", {})
    S = a["n_specs_estimated"]
    L += ["## What was searched", "",
          f"- **{a['n_specs_enumerated']} specifications** enumerated, {S} estimated, "
          f"{a['n_specs_failed']} failed. The one-sided direction sought was **{dir_txt}**.",
          f"- Multiplicity that inference has to pay for: {S} specifications"
          + (f", of which Li–Ji effective tests ≈ **{a['effective_tests']}**." if "effective_tests" in a else ".")]
    if "walk" in a:
        w = a["walk"]
        L += [f"- Search procedure: **{w['procedure']}** {json.dumps(w.get('params', {}))}; "
              f"visited {w['n_visited']} of {w['n_in_grid']} grid points; stopped because: {w['stopped']}."]
    L += ["", "## The specification curve", "",
          f"| statistic | value |", f"|---|---|",
          f"| median estimate | {_f(curve.get('median_coef'))} |",
          f"| interquartile range | {_f(curve.get('iqr_coef'))} |",
          f"| range | [{_f(curve.get('min_coef'))}, {_f(curve.get('max_coef'))}] |",
          f"| share significant at {a['alpha']} | {_f(a['share_significant'], 3)} ({a['n_specs_significant']} of {S}) |",
          f"| share significant with the dominant sign | {_f(curve.get('share_sig_dominant_sign'))} |",
          f"| share changing sign | {_f(curve.get('share_sign_flips'))} |",
          f"| flagged specifications | {a['n_specs_flagged']} ({_f(a['share_flagged_among_significant'], 2)} of the significant ones) |",
          ""]
    if "ssn_joint" in a and "share_significant" in a["ssn_joint"]:
        j = a["ssn_joint"]
        L += ["Joint inference on the whole curve (Simonsohn, Simmons & Nelson), "
              f"against {j['n_null_draws']} null re-runs of the same grid:", "",
              "| test | observed | null median | p |", "|---|---|---|---|",
              f"| median effect | {_f(j['median_effect']['observed'])} | {_f(j['median_effect']['null_median'])} | {_p(j['median_effect']['p_value'])} |",
              f"| share significant | {_f(j['share_significant']['observed'])} | {_f(j['share_significant']['null_median'])} | {_p(j['share_significant']['p_value'])} |",
              f"| share significant, dominant sign | {_f(j['share_significant_dominant_sign']['observed'])} | {_f(j['share_significant_dominant_sign']['null_median'])} | {_p(j['share_significant_dominant_sign']['p_value'])} |",
              f"| Stouffer aggregate z | {_f(j['stouffer_z']['observed'], 2)} | — | {_p(j['stouffer_z']['p_value'])} |", ""]
    if "preregistered" in a:
        pr = a["preregistered"]
        L += ["## The pre-registered specification", "",
              f"`{pr['label']}`", "",
              f"β̂ = **{_f(pr['coef'])}** (SE {_f(pr['se'])}, p = {_p(pr['p'])}, n = {pr['n']}). "
              f"It sits at the {100 * a['prereg_percentile_in_curve']:.0f}th percentile of the curve."]
        ns = a.get("nearest_significant", {})
        if ns.get("distance") is not None:
            ch = "; ".join(f"{k}: {v['from']} → {v['to']}" for k, v in ns["changes"].items())
            L += ["", f"The nearest significant specification is **{ns['distance']} choice(s)** away "
                  f"({ch}), giving β̂ = {_f(ns['spec']['coef'])}, p = {_p(ns['spec']['p'])}. "
                  f"{ns['n_significant_within_1_change']} significant specification(s) are a single change away."]
        elif ns:
            L += ["", "No specification in the ledger is significant in the sought direction."]
        L += [""]
    b = a["best_spec"]
    L += ["## The most favourable specification", "",
          f"`{b['label']}`", "",
          f"β̂ = **{_f(b['coef'])}** (SE {_f(b['se'])}, t = {_f(b['t'], 2)}, reported p = **{_p(b.get('p_dir', b['p']))}**, "
          f"n = {b['n']}"
          + (f", {b['n_flags']} pathology flag(s)" if b.get("n_flags") else "") + ")."]
    if "preregistered" in a:
        L += [f"That is {_f(a['coef_inflation_vs_prereg'], 2)}× the pre-registered estimate and "
              f"{_f(a['log10_p_gain'], 2)} orders of magnitude in p."]
    if "best_unflagged_spec" in a:
        u = a["best_unflagged_spec"]
        L += ["", f"Best specification carrying **no** pathology flag: `{u['label']}` — "
              f"β̂ = {_f(u['coef'])}, p = {_p(u.get('p_dir', u['p']))}."]
    L += ["", "### What that p-value is worth", "",
          "| correction | p |", "|---|---|",
          f"| as reported | {_p(b.get('p_dir', b['p']))} |",
          f"| Bonferroni over {S} | {_p(a['bonferroni_p_of_best'])} |"]
    if "romano_wolf_p_of_best" in a:
        L += [f"| Romano–Wolf stepdown | {_p(a['romano_wolf_p_of_best'])} |",
              f"| Šidák on {a['effective_tests']} effective tests | {_p(a['meff_adjusted_p_of_best'])} |"]
    if "min_p_test" in a:
        m = a["min_p_test"]
        L += [f"| **null-calibrated (min-p over the identical search, {m['n_null_draws']} draws)** | **{_p(m['honest_p'])}** |"]
        if "min_p_test_unflagged" in a:
            L += [f"| null-calibrated, best unflagged | {_p(a['min_p_test_unflagged']['honest_p'])} |"]
    if "honest_p" in a.get("procedure_test", {}):
        pt = a["procedure_test"]
        L += [f"| null-calibrated for the *{pt['procedure']}* procedure | {_p(pt['honest_p'])} |"]
    L += [""]
    if "min_p_test" in a:
        m = a["min_p_test"]
        L += [f"Re-running the identical search on {m['n_null_draws']} datasets where the null holds by "
              f"construction, the probability of a result at least this significant is **{_p(m['honest_p'])}** "
              f"(median null minimum p = {_p(m['null_min_p_median'])}; inflation factor "
              f"{_f(m['inflation_factor'], 0)}×).", ""]
    if "procedure_test" in a:
        pt = a["procedure_test"]
        any_ = pt.get("null_share_reporting_any", 1.0)
        L += [f"The **{pt['procedure']}** procedure reports a significant result on "
              f"**{100 * pt['null_share_reporting_significant']:.0f}%** of null datasets"
              + (f" on which it reported anything at all ({100 * any_:.0f}% of them; the rest were "
                 f"abandoned after the pilot stage)" if any_ < 1 else "")
              + f", visiting {pt['null_mean_specs_visited']:.1f} specifications on average. That is its "
              f"false-positive rate on this design.", ""]
        if "note" in pt:
            L += [f"On the observed data the procedure reported nothing: {pt['note']}.", ""]
    ai = a.get("axis_influence", {})
    if ai.get("ranked_axes"):
        L += ["## Which choices did the work", "",
              "| axis | spread in share significant | most favourable level | share of all significant results at that level |",
              "|---|---|---|---|"]
        for ax in ai["ranked_axes"][:8]:
            r = ai["axes"][ax]
            L += [f"| {ax} | {_f(r['spread'])} | {r['most_significant_level']} | {_f(r['share_of_all_significant_at_that_level'], 2)} |"]
        L += [""]
    L += ["## Conclusion", ""]
    hp = (a.get("procedure_test") or {}).get("honest_p", (a.get("min_p_test") or {}).get("honest_p"))
    if hp is not None:
        if hp >= a["alpha"]:
            L += [f"The search found nothing that survives calibration against its own multiplicity "
                  f"(honest p = {_p(hp)}). The pre-registered result stands"
                  + (f": β̂ = {_f(a['preregistered']['coef'])}, p = {_p(a['preregistered']['p'])}." if "preregistered" in a else ".")
                  + " The most favourable specification is reported here as the maximum of a search, "
                    "not as a test."]
        else:
            L += [f"The result survives calibration against the search that produced it "
                  f"(honest p = {_p(hp)}). Report the curve alongside it; the honest p, not the "
                  f"per-specification p, is the inferential statement."]
    else:
        L += ["No null calibration was run, so the reported p-values are uncorrected for the search. "
              "Run `phack search --null-draws 200` before drawing any inferential conclusion."]
    L += ["", "---", "*Generated by `phack report`; every number above is read from the ledger and audit, "
          "and the ledger lists every specification estimated.*"]
    return "\n".join(L)


def summary_lines(a: dict) -> str:
    """The eight lines a terminal user wants after `phack search --summary`."""
    b = a["best_spec"]; L = []
    L.append(f"specifications      : {a['n_specs_estimated']} estimated ({a['n_specs_significant']} significant, "
             f"{a['n_specs_flagged']} flagged)")
    if "preregistered" in a:
        pr = a["preregistered"]
        L.append(f"pre-registered      : coef {pr['coef']:+.4g}  p = {pr['p']:.3f}")
    L.append(f"best specification  : {b['label']}")
    L.append(f"  reported p        : {b.get('p_dir', b['p']):.2e}" + (f"   ({b['n_flags']} flag(s))" if b.get("n_flags") else ""))
    ns = a.get("nearest_significant") or {}
    if ns.get("distance") is not None:
        L.append(f"  choices from PAP  : {ns['distance']}  ({', '.join(ns['axes_changed'])})")
    if "romano_wolf_p_of_best" in a:
        L.append(f"  Romano-Wolf       : {a['romano_wolf_p_of_best']:.3f}   (effective tests {a['effective_tests']})")
    if "min_p_test" in a:
        L.append(f"  NULL-CALIBRATED p : {a['min_p_test']['honest_p']:.3f}   (inflation {a['min_p_test']['inflation_factor']:.0f}x)")
    if "min_p_test_unflagged" in a:
        L.append(f"  ... best unflagged: {a['min_p_test_unflagged']['honest_p']:.3f}")
    if "procedure_test" in a:
        pt = a["procedure_test"]
        any_ = pt.get("null_share_reporting_any", 1.0)
        L.append(f"  procedure FPR     : {100 * pt['null_share_reporting_significant']:.0f}% of null datasets "
                 + (f"that reported ({100 * any_:.0f}% did) " if any_ < 1 else "")
                 + f"({pt['null_mean_specs_visited']:.0f} specs visited on average)")
    ai = a.get("axis_influence", {}).get("ranked_axes", [])
    if ai:
        L.append(f"axes doing the work : {', '.join(ai[:4])}")
    for k in ("report", "figure"):
        if k in a:
            L.append(f"{k:20s}: {a[k]}")
    return "\n".join(L)
