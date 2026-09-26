"""
phack race: how quickly does a search manufacture significance?

"An agent can p-hack in minutes" is a capability claim, and capability claims
deserve measurement, not vibes. This module races the search procedures of
`procedures.py` against the clock on a design card and reports, per procedure:

    - how often it ends up reporting p < alpha            (the yield)
    - the median wall-clock seconds until the first
      significant fit is in hand                          (time to significance)
    - how many model fits and specifications that took    (the effort)
    - what the honest single pre-registered analysis
      costs and says on the same data                     (the contrast)

Run with `null_scheme` set, every trial re-draws treatment under the null
before racing, so the yield IS the false-positive rate of the procedure and
the timings answer the exact question the capability claim raises: *on data
where the true effect is zero, how many seconds of compute separate an honest
analyst from a manufactured p < .05?*

The framing is deliberate. The point of pricing the manufacture is that the
price is trivially low -- a `foreach` loop always made it low, and an agent
makes it conversational. What stays expensive is hiding it: every walk raced
here is the same walk `phack search --procedure` runs under full
instrumentation, where it cannot report a winner without the ledger and the
null-calibrated honest p. A `reported_p` in this module's output is a search
maximum, not a valid p-value; the audit that prices it lives in `search.py`.
"""
from __future__ import annotations

import time

import numpy as np

from . import grid, inference, procedures, search

__all__ = ["race", "summary_lines", "DEFAULT_PROCEDURES"]

DEFAULT_PROCEDURES = ("greedy", "first_significant", "hill_climb", "random")


class _TimedFitter:
    """Wrap a memoised fitter; note the clock when the first significant
    (one-sided, in `direction`) fit comes back."""

    def __init__(self, fit, alpha, direction):
        self._fit, self.alpha, self.direction = fit, alpha, direction
        self.df, self.card, self.cache = fit.df, fit.card, fit.cache
        self.n_fits = 0
        self.t0 = time.perf_counter()
        self.seconds_to_sig = None
        self.fits_to_sig = None

    def __call__(self, spec):
        r = self._fit(spec)
        self.n_fits += 1
        if self.seconds_to_sig is None:
            if procedures._objective(r, self.direction) < self.alpha:
                self.seconds_to_sig = time.perf_counter() - self.t0
                self.fits_to_sig = self.n_fits
        return r


def _make_procedure(name, prereg_key, budget, order):
    if name == "split_sample":
        raise ValueError("race does not run split_sample; race its inner procedure instead")
    if name not in procedures.PROCEDURES:
        raise KeyError(f"unknown procedure {name!r}; known: {sorted(procedures.PROCEDURES)}")
    return procedures.make(
        name,
        start=prereg_key,                    # a search starts where an honest analysis would
        order=order if name == "first_significant" else None,
        stop_at_alpha=True if name in ("greedy", "hill_climb", "random") else None,
        budget=budget)


def _q(xs, q):
    xs = [x for x in xs if x is not None and np.isfinite(x)]
    return float(np.quantile(xs, q)) if xs else None


def race(df, card, *, procedure_names=DEFAULT_PROCEDURES, trials=20, alpha=0.05,
         seed=0, max_specs=None, budget=None, order="random",
         null_scheme=None, progress=False) -> dict:
    """Race `procedure_names` on (df, card); `trials` runs each.

    With `null_scheme`, each trial first re-draws the data under the null
    (same schemes as `search.null_calibration`), so `share_reporting_significant`
    is the procedure's false-positive rate and every timing is the cost of a
    manufactured result. Without it, the procedures race on the data as given.
    Deterministic given `seed`.
    """
    trials = max(1, int(trials))
    card = dict(card)
    direction = grid.direction_sign(card)
    full = grid.enumerate_specs(card)
    prereg_key = grid.resolve_prereg(card, full)
    specs = grid.thin(full, max_specs, keep_keys=[prereg_key]) if max_specs else full

    # the contrast line: the one analysis an honest analyst runs
    fit0 = search.make_fitter(df, card)
    pre_spec = next(s for s in specs if s.key() == prereg_key)
    r0 = fit0(pre_spec)
    prereg = {
        "key": prereg_key,
        "p": None if not np.isfinite(r0.get("p", np.nan)) else float(r0["p"]),
        "p_dir": (None if direction is None or not np.isfinite(r0.get("p", np.nan))
                  else float(inference.one_sided_p(r0["t"], r0["p"], direction))),
        "coef": None if not np.isfinite(r0.get("coef", np.nan)) else float(r0["coef"]),
        "seconds": r0.get("ms", 0.0) / 1000.0,
    }

    out_procs = {}
    for pi, name in enumerate(procedure_names):
        rows = []
        for t in range(trials):
            rng = np.random.default_rng([seed, pi, t])
            d = search._draw_null(df, card, rng, null_scheme) if null_scheme else df
            proc = _make_procedure(name, prereg_key, budget, order)
            fit = _TimedFitter(search.make_fitter(d, card), alpha, direction)
            t0 = time.perf_counter()
            walk = proc.walk(specs, fit, rng=rng, alpha=alpha, direction=direction)
            total = time.perf_counter() - t0
            rep_o = (procedures._objective(fit(walk.reported), direction)
                     if walk.reported is not None else np.inf)
            sig = bool(rep_o < alpha)
            rows.append({
                "trial": t,
                "significant": sig,
                "seconds_to_significance": (None if fit.seconds_to_sig is None
                                            else round(fit.seconds_to_sig, 4)),
                "fits_to_significance": fit.fits_to_sig,
                "specs_visited": len(walk.visited),
                "total_seconds": round(total, 4),
                "reported_p": None if not np.isfinite(rep_o) else float(rep_o),
                "stopped": walk.stopped,
            })
            if progress:
                print(f"  {name} trial {t + 1}/{trials}: "
                      f"{'sig in %.2fs' % fit.seconds_to_sig if fit.seconds_to_sig else 'no significance'}",
                      flush=True)
        sig_rows = [r for r in rows if r["significant"]]
        out_procs[name] = {
            "share_reporting_significant": round(len(sig_rows) / len(rows), 4),
            "median_seconds_to_significance": _q([r["seconds_to_significance"] for r in sig_rows], 0.5),
            "q90_seconds_to_significance": _q([r["seconds_to_significance"] for r in sig_rows], 0.9),
            "median_fits_to_significance": _q([r["fits_to_significance"] for r in sig_rows], 0.5),
            "median_specs_visited": _q([r["specs_visited"] for r in rows], 0.5),
            "median_total_seconds": _q([r["total_seconds"] for r in rows], 0.5),
            "median_reported_p": _q([r["reported_p"] for r in sig_rows], 0.5),
            "params": proc.params(),
            "trials": rows,
        }

    return {
        "n_specs_in_grid": len(specs),
        "n_specs_in_universe": len(full),
        "n_trials": int(trials),
        "alpha": float(alpha),
        "direction": {1: "+", -1: "-", None: None}[direction],
        "null_scheme": null_scheme,
        "preregistered": prereg,
        "procedures": out_procs,
        "note": (
            "Timings price the manufacture of significance, not evidence. Every "
            "'significant' report above is the maximum of a search; its reported_p is "
            "not a valid p-value. "
            + ("Because null_scheme is set, share_reporting_significant is the "
               "false-positive rate of the procedure on this design. "
               if null_scheme else "")
            + "The same walks run fully instrumented -- ledger, specification curve, "
              "null-calibrated honest p -- under `phack search --procedure`."),
    }


def summary_lines(res) -> str:
    """A human-readable table of a race result."""
    lines = [
        f"grid: {res['n_specs_in_grid']:,} specifications"
        + (f" (thinned from {res['n_specs_in_universe']:,})"
           if res["n_specs_in_grid"] != res["n_specs_in_universe"] else "")
        + f"   trials: {res['n_trials']}   alpha: {res['alpha']}"
        + (f"   null scheme: {res['null_scheme']} (truth = 0 in every trial)"
           if res["null_scheme"] else ""),
        f"honest baseline: the pre-registered spec fits in {res['preregistered']['seconds']:.3f}s"
        + (f" and says p = {res['preregistered']['p_dir']:.3f} (one-sided)"
           if res["preregistered"]["p_dir"] is not None else ""),
        "",
        f"{'procedure':<20}{'yield':>7}{'median s to sig':>17}{'fits':>7}{'specs':>7}{'reported p':>13}",
    ]
    for name, r in res["procedures"].items():
        ms = r["median_seconds_to_significance"]
        lines.append(
            f"{name:<20}"
            f"{100 * r['share_reporting_significant']:>6.0f}%"
            f"{('%.2f' % ms if ms is not None else '--'):>17}"
            f"{('%.0f' % r['median_fits_to_significance'] if r['median_fits_to_significance'] is not None else '--'):>7}"
            f"{r['median_specs_visited']:>7.0f}"
            f"{('%.3f' % r['median_reported_p'] if r['median_reported_p'] is not None else '--'):>13}")
    lines += ["", res["note"]]
    return "\n".join(lines)
