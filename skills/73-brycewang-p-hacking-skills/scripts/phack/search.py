"""
Walk the specification universe, log every step, and calibrate the walk.

Entry points:
  run()               -- fit every specification (or a procedure's path), return the ledger
  null_calibration()  -- re-run the *identical* search under an enforced null,
                         giving the reference distribution of min-p, the
                         t / coef / p null matrices that Romano-Wolf and the
                         Simonsohn joint tests need, and -- when a procedure is
                         supplied -- the null distribution of what *that
                         procedure* would have reported.
  audit()             -- turn a ledger (+ null draws) into the honest summary
  nearest_significant(), axis_influence(), manifest()

Nothing here is hidden: a search that cannot produce a complete ledger is a
bug, not a feature.
"""
from __future__ import annotations

import hashlib, json, os, time
from dataclasses import dataclass, field
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

from . import core, grid, inference

LEDGER_META = ["idx", "key", "label", "order", "outcome", "n_controls", "controls", "fe",
               "vcov", "cluster", "y_transform", "d_transform", "outlier_rule", "imputation",
               "subsample", "weight", "lag", "did_estimator", "comparison_group",
               "bandwidth", "bw_selector", "kernel", "poly", "donut", "rdd_inference",
               "instruments", "iv_estimator"]
RESULT_COLS = ["coef", "se", "t", "p", "ci_low", "ci_high", "n", "df"]


def _fit_spec(df, spec, card):
    built = grid.build(df, spec, card)
    if built["design"] == "rdd":
        return core.fit_rdd(built["y"], built["x"], h=built["h"], kernel=built["kernel"],
                            poly=built["poly"], donut=built["donut"], cutoff=built["cutoff"],
                            controls=built["controls"], vcov=built["vcov"],
                            cluster=built["cluster"], inference=built["inference"],
                            weights=built["weights"])
    if built["design"] == "iv":
        return core.fit_2sls(built["y"], built["d"], built["Z"], controls=built["controls"],
                             vcov=built["vcov"], cluster=built["cluster"],
                             estimator=built["estimator"], weights=built["weights"])
    if built["design"] == "lincom":
        r = core.fit_lincom(built["y"], built["X"], built["a"], vcov=built["vcov"],
                            cluster=built["cluster"], k_absorbed=built["k_absorbed"],
                            weights=built["weights"])
        r["n_treated_cohorts"] = built["n_treated_cohorts"]
        return r
    r = core.fit_ols(built["y"], built["X"], vcov=built["vcov"], cluster=built["cluster"],
                     k_absorbed=built["k_absorbed"], target=1 if built["has_const"] else 0,
                     weights=built["weights"])
    if "n_stacks" in built:
        r["n_stacks"] = built["n_stacks"]
    return r


def make_fitter(df, card):
    """A memoised spec -> result callable; the object procedures walk with."""
    cache = {}

    def fit(spec):
        k = spec.key()
        if k not in cache:
            t0 = time.perf_counter()
            try:
                r = _fit_spec(df, spec, card); r["status"] = "ok"
            except Exception as exc:                   # noqa: BLE001
                r = {"coef": np.nan, "se": np.nan, "t": np.nan, "p": np.nan,
                     "ci_low": np.nan, "ci_high": np.nan, "n": 0, "psd_ok": False,
                     "status": f"error: {type(exc).__name__}: {exc}"}
            r["ms"] = round(1000 * (time.perf_counter() - t0), 2)
            cache[k] = r
        return cache[k]
    fit.cache = cache
    fit.df, fit.card = df, card               # so two-stage procedures can re-fit on a subset
    return fit


def _spec_record(s: grid.Spec, order: int) -> dict:
    return {
        "idx": s.idx, "key": s.key(), "label": s.label(), "order": order,
        "outcome": s.outcome, "n_controls": len(s.controls),
        "controls": "+".join(s.controls) or "none",
        "fe": "+".join(s.fe) or "none", "vcov": s.vcov,
        "cluster": str(s.cluster), "y_transform": s.y_transform,
        "d_transform": s.d_transform, "outlier_rule": s.outlier_rule,
        "imputation": s.imputation, "subsample": s.subsample,
        "weight": s.weight, "lag": s.lag,
        "did_estimator": s.did_estimator, "comparison_group": s.comparison_group,
        "ev_window": (f"{s.ev_window[0]}/{s.ev_window[1]}" if s.ev_window else None),
        "ev_ref": s.ev_ref, "ev_estimand": s.ev_estimand,
        "bandwidth": (s.bandwidth[1] if isinstance(s.bandwidth, tuple) else s.bandwidth),
        "bw_multiplier": (None if s.bandwidth is None or isinstance(s.bandwidth, tuple) else s.bandwidth),
        "bw_selector": s.bw_selector if s.bandwidth is not None else None,
        "kernel": s.kernel if s.bandwidth is not None else None,
        "poly": s.poly if s.bandwidth is not None else None,
        "donut": s.donut if s.bandwidth is not None else None,
        "rdd_inference": s.rdd_inference if s.bandwidth is not None else None,
        "instruments": "+".join(s.instruments) or None,
        "iv_estimator": s.iv_estimator if s.instruments else None,
        "spec_json": s.to_json(),
    }


def _run_chunk(args):
    df, card, specs = args
    fit = make_fitter(df, card)
    return [{k: v for k, v in fit(s).items() if not isinstance(v, np.ndarray)} for s in specs]


def run(df: pd.DataFrame, card: dict, *, specs=None, progress=False,
        procedure=None, seed=0, alpha=0.05, n_jobs=1) -> pd.DataFrame:
    """Fit every specification -- or walk the grid with a `procedure` -- and
    return the ledger. Failures are recorded, never silently dropped.

    With a procedure, the ledger contains only the specifications the
    procedure visited, in visit order, with `reported` marking the one it
    would have written up and `ledger.attrs["walk"]` carrying the stopping
    rule and budget. That is what makes the procedure's own honest p-value
    computable: null_calibration replays the same procedure.
    """
    specs = specs if specs is not None else grid.enumerate_specs(card)
    direction = grid.direction_sign(card)
    fit = make_fitter(df, card)
    t0 = time.time()
    rows = []
    if procedure is not None:
        walk = procedure.walk(specs, fit, rng=np.random.default_rng(seed), alpha=alpha,
                              direction=direction)
        visited = walk.visited
        reported_key = walk.reported.key() if walk.reported is not None else None
    else:
        visited = specs
        reported_key = None
    n_jobs = max(1, int(n_jobs or 1))
    if procedure is None and n_jobs > 1 and len(visited) >= 4 * n_jobs:
        chunks = [visited[i::n_jobs] for i in range(n_jobs)]
        with ProcessPoolExecutor(max_workers=n_jobs) as ex:
            parts = list(ex.map(_run_chunk, [(df, card, c) for c in chunks]))
        results = {}
        for c, part in zip(chunks, parts):
            for s, r in zip(c, part):
                results[s.key()] = r
        for order, s in enumerate(visited):
            rec = _spec_record(s, order); rec.update(results[s.key()]); rows.append(rec)
    else:
        for order, s in enumerate(visited):
            rec = _spec_record(s, order)
            rec.update({k: v for k, v in fit(s).items() if not isinstance(v, np.ndarray)})
            rows.append(rec)
            if progress and len(rows) % 250 == 0:
                print(f"  {len(rows)}/{len(visited)} specs  ({time.time()-t0:.1f}s)", flush=True)
    if procedure is not None:
        if walk.stage_results:
            for rec in rows:
                rec.update(walk.stage_results.get(rec["key"], {}))
        if walk.reported_result is not None and reported_key is not None:
            # a two-stage procedure reports its own (held-out or pilot) estimate,
            # not the full-data fit of the same specification
            for rec in rows:
                if rec["key"] == reported_key:
                    rec.update({k: v for k, v in walk.reported_result.items()
                                if not isinstance(v, np.ndarray)})
                    break
    led = pd.DataFrame(rows)
    if led.empty:
        return led
    led["abs_t"] = led["t"].abs()
    led["p_dir"] = inference.one_sided_p(led["t"], led["p"], direction)
    led["sign_ok"] = True if direction is None else (np.sign(led["coef"]) == direction)
    if procedure is not None:
        led["reported"] = led["key"] == reported_key
        led.attrs["walk"] = {"procedure": procedure.name, "params": procedure.params(),
                             "n_visited": int(len(visited)), "stopped": walk.stopped,
                             "reported_key": reported_key, "n_in_grid": int(len(specs)),
                             "path": walk.path}
    return led


def flag_pathologies(ledger: pd.DataFrame, card: dict, alpha=0.05) -> pd.DataFrame:
    """Mark specifications that are searchable but not defensible.

    A search that reports one of these as its headline is not merely p-hacked,
    it is wrong. Keeping them in the ledger and flagged is the honest move;
    silently dropping them hides a real failure mode of automated search.
    """
    led = ledger.copy()
    if led.empty:
        return led
    ok = led["status"] == "ok"
    few_clusters = led["df"].fillna(1e9) < 15
    led["flag_nonpsd_vcov"] = ok & ~led.get("psd_ok", pd.Series(True, index=led.index)).fillna(False).astype(bool)
    led["flag_few_clusters"] = ok & few_clusters & led["vcov"].isin(["cluster", "twoway"])
    led["flag_tiny_sample"] = ok & (led["n"] < 0.25 * led["n"].max())
    led["flag_implausible_precision"] = ok & (led["se"] < 0.1 * led.loc[ok, "se"].median())
    if "d_transform" in led:
        led["flag_extreme_groups"] = ok & led["d_transform"].eq("tercile_extremes")
    if "first_stage_F" in led:
        led["flag_weak_instruments"] = ok & (led["first_stage_F"].fillna(np.inf) < 10)
    if "ar_p" in led:
        # the Wald t rejects but the weak-IV-robust AR test does not: the
        # significance is an artefact of a poorly identified first stage
        led["flag_ar_disagrees"] = ok & (led["p"] < alpha) & (led["ar_p"].fillna(0) >= alpha)
    if "n_left" in led:
        led["flag_thin_rdd_side"] = ok & ((led["n_left"].fillna(np.inf) < 20) |
                                          (led["n_right"].fillna(np.inf) < 20))
    if "rdd_inference" in led:
        led["flag_bc_without_robust_se"] = ok & led["rdd_inference"].eq("bias_corrected")
    if "n_stacks" in led:
        led["flag_single_stack"] = ok & (led["n_stacks"].fillna(np.inf) < 2)
    if "ev_estimand" in led and led["ev_estimand"].notna().any():
        # reporting the pre-trend as if it were the effect, or a reference period
        # inside the post window, is not a specification -- it is a mistake
        led["flag_event_misuse"] = ok & (led["ev_estimand"].eq("avg_pre") |
                                         (led["ev_ref"].fillna(-1) >= 0))
    led["n_flags"] = led.filter(like="flag_").sum(axis=1)
    return led


# --------------------------------------------------------------------------
# Null calibration
# --------------------------------------------------------------------------

def _draw_null(df, card, rng, scheme):
    d = df.copy()
    t = card["treatment"]
    if card.get("design") == "rdd":
        # Treatment is a deterministic function of the running variable, so it
        # cannot be permuted. Enforce the null by permuting the OUTCOME within
        # narrow bins of the running variable: this preserves the smooth
        # relationship y(x) and removes any jump at the cutoff.
        x = d[card["running"]].to_numpy(float)
        bins = pd.qcut(x, q=min(40, max(4, len(x) // 25)), labels=False, duplicates="drop")
        for oc in card["outcomes"]:
            d[oc] = d.groupby(bins)[oc].transform(lambda s: rng.permutation(s.to_numpy()))
        return d
    if card.get("design") == "iv" and scheme == "permute":
        idx = rng.permutation(len(d))
        for z in card["instruments_pool"]:
            d[z] = d[z].to_numpy()[idx]
        return d
    if scheme == "permute":
        d[t] = rng.permutation(d[t].to_numpy())
    elif scheme == "permute_within_unit":
        unit = card["panel_unit"]
        if not unit:
            raise ValueError("permute_within_unit needs panel_unit")
        d[t] = d.groupby(unit)[t].transform(lambda s: rng.permutation(s.to_numpy()))
    elif scheme == "permute_within_time":
        tt = card["panel_time"]
        if not tt:
            raise ValueError("permute_within_time needs panel_time")
        d[t] = d.groupby(tt)[t].transform(lambda s: rng.permutation(s.to_numpy()))
    elif scheme == "cluster_permute":
        unit = card["panel_unit"]
        if not unit:
            raise ValueError("cluster_permute needs panel_unit")
        # reassign each unit's entire treatment PATH to another unit: preserves
        # within-unit serial structure and, for staggered adoption, the
        # distribution of adoption dates
        paths = {u: g[t].to_numpy() for u, g in d.sort_values(card["panel_time"] or unit).groupby(unit)}
        ids = list(paths)
        perm = dict(zip(ids, rng.permutation(ids)))
        d = d.sort_values([unit] + ([card["panel_time"]] if card["panel_time"] else []))
        new = np.concatenate([_fit_len(paths[perm[u]], len(g)) for u, g in d.groupby(unit, sort=False)])
        d[t] = new
        d = d.sort_index()
    elif scheme == "gaussian":
        d[t] = rng.normal(size=len(d))
    else:
        raise KeyError(f"unknown null scheme {scheme!r}")
    return d


def _fit_len(path, n):
    if len(path) == n:
        return path
    if len(path) > n:
        return path[:n]
    return np.r_[path, np.repeat(path[-1], n - len(path))]


@dataclass
class NullDraws:
    """Everything a null re-run of the search produces."""
    min_p: np.ndarray                 # (B,) smallest two-sided p in each draw
    t: np.ndarray                     # (B, S)
    coef: np.ndarray                  # (B, S)
    p: np.ndarray                     # (B, S) two-sided
    specs: list
    scheme: str
    seed: int
    direction: object = None
    min_p_dir: np.ndarray = None      # (B,) smallest one-sided p in `direction`
    procedure: str = None
    reported_p_null: np.ndarray = None    # (B,) what the procedure reported per draw
    n_visited_null: np.ndarray = None     # (B,)

    def __iter__(self):               # backwards compatible: mp, tn, specs = ...
        return iter((self.min_p, self.t, self.specs))

    @property
    def B(self):
        return int(self.min_p.size)

    def save(self, out_dir):
        np.save(os.path.join(out_dir, "min_p_null.npy"), self.min_p)
        np.save(os.path.join(out_dir, "t_null.npy"), self.t)
        np.save(os.path.join(out_dir, "coef_null.npy"), self.coef)
        np.save(os.path.join(out_dir, "p_null.npy"), self.p)
        if self.reported_p_null is not None:
            np.save(os.path.join(out_dir, "reported_p_null.npy"), self.reported_p_null)
        if self.n_visited_null is not None:
            np.save(os.path.join(out_dir, "n_visited_null.npy"), self.n_visited_null)
        meta = {"scheme": self.scheme, "seed": self.seed, "B": self.B,
                "direction": self.direction, "procedure": self.procedure,
                "spec_keys": [s.key() for s in self.specs]}
        with open(os.path.join(out_dir, "null_meta.json"), "w") as fh:
            json.dump(meta, fh)

    @classmethod
    def load(cls, out_dir, specs=None):
        meta = json.load(open(os.path.join(out_dir, "null_meta.json")))
        rp = os.path.join(out_dir, "reported_p_null.npy")
        nv = os.path.join(out_dir, "n_visited_null.npy")
        nd = cls(min_p=np.load(os.path.join(out_dir, "min_p_null.npy")),
                 t=np.load(os.path.join(out_dir, "t_null.npy")),
                 coef=np.load(os.path.join(out_dir, "coef_null.npy")),
                 p=np.load(os.path.join(out_dir, "p_null.npy")),
                 specs=specs if specs is not None else meta["spec_keys"],
                 scheme=meta["scheme"], seed=meta["seed"], direction=meta.get("direction"),
                 procedure=meta.get("procedure"),
                 reported_p_null=np.load(rp) if os.path.exists(rp) else None,
                 n_visited_null=np.load(nv) if os.path.exists(nv) else None)
        nd.min_p_dir = _min_p_dir(nd.t, nd.p, nd.direction)
        return nd


def _min_p_dir(T, P, direction):
    if direction is None:
        return np.nanmin(np.where(np.isfinite(P), P, np.nan), axis=1, initial=np.inf)
    pd_ = inference.one_sided_p(T, P, direction)
    pd_ = np.where(np.isfinite(pd_), pd_, np.inf)
    return pd_.min(axis=1)


def _null_worker(args):
    df, card, specs, seeds, scheme, proc, alpha, walk_specs = args
    direction = grid.direction_sign(card)
    S = len(specs)
    out_t = np.full((len(seeds), S), np.nan); out_c = out_t.copy(); out_p = out_t.copy()
    rep_p = np.full(len(seeds), np.nan); n_vis = np.full(len(seeds), np.nan)
    for i, sd in enumerate(seeds):
        rng = np.random.default_rng(sd)
        d = _draw_null(df, card, rng, scheme)
        fit = make_fitter(d, card)
        for j, s in enumerate(specs):
            r = fit(s)
            out_t[i, j], out_c[i, j], out_p[i, j] = r["t"], r["coef"], r["p"]
        if proc is not None:
            w = proc.walk(walk_specs, fit, rng=np.random.default_rng(sd + 10_000_019),
                          alpha=alpha, direction=direction)
            n_vis[i] = len(w.visited)
            if w.reported is not None:
                r = w.reported_result if w.reported_result is not None else fit(w.reported)
                rep_p[i] = inference.one_sided_p(r["t"], r["p"], direction) if direction else r["p"]
    return out_t, out_c, out_p, rep_p, n_vis


def null_calibration(df: pd.DataFrame, card: dict, *, B=200, scheme="permute",
                     seed=0, specs=None, max_specs=None, keep_keys=(), progress=False,
                     procedure=None, walk_specs=None, n_jobs=1, alpha=0.05) -> NullDraws:
    """Re-run the search B times with the treatment made inert.

    `specs` (thinned to `max_specs`, always keeping `keep_keys`) is the set on
    which the full t / coef / p null matrices are computed: min-p test,
    Romano-Wolf, effective tests, Simonsohn joint tests. Thinning is recorded
    so the honest p-value is never quietly computed on a different search than
    the one audited.

    `procedure` is replayed on every null draw over `walk_specs` (default: the
    same `specs`; pass the full grid for a faithful replay -- procedures are
    cheap because they visit only a path) so that the distribution of *what
    that procedure reports* is known.
    """
    specs = specs if specs is not None else grid.enumerate_specs(card)
    specs = grid.thin(specs, max_specs, keep_keys)
    walk_specs = walk_specs if walk_specs is not None else specs
    seeds = [int(seed) * 1_000_003 + b for b in range(B)]
    n_jobs = max(1, int(n_jobs or 1))
    if n_jobs > 1:
        chunks = [c for c in (seeds[i::n_jobs] for i in range(n_jobs)) if c]
        with ProcessPoolExecutor(max_workers=n_jobs) as ex:
            parts = list(ex.map(_null_worker,
                                [(df, card, specs, c, scheme, procedure, alpha, walk_specs) for c in chunks]))
    else:
        chunks, parts = [], []
        for k in range(0, B, 25):
            c = seeds[k:k + 25]; chunks.append(c)
            parts.append(_null_worker((df, card, specs, c, scheme, procedure, alpha, walk_specs)))
            if progress:
                print(f"  null draw {min(k + 25, B)}/{B}", flush=True)
    S = len(specs)
    T = np.full((B, S), np.nan); C = T.copy(); P = T.copy()
    RP = np.full(B, np.nan); NV = np.full(B, np.nan)
    pos = {sd: i for i, sd in enumerate(seeds)}
    for c, (t_, c_, p_, rp_, nv_) in zip(chunks, parts):
        rows = [pos[sd] for sd in c]
        T[rows], C[rows], P[rows], RP[rows], NV[rows] = t_, c_, p_, rp_, nv_
    direction = grid.direction_sign(card)
    min_p = np.where(np.isfinite(P).any(axis=1),
                     np.nanmin(np.where(np.isfinite(P), P, np.nan), axis=1, initial=np.inf), np.nan)
    nd = NullDraws(min_p=min_p, t=T, coef=C, p=P, specs=specs, scheme=scheme, seed=seed,
                   direction=direction, min_p_dir=_min_p_dir(T, P, direction),
                   procedure=procedure.name if procedure is not None else None,
                   reported_p_null=RP if procedure is not None else None,
                   n_visited_null=NV if procedure is not None else None)
    return nd


# --------------------------------------------------------------------------
# Audit
# --------------------------------------------------------------------------

def _best(ok: pd.DataFrame, direction):
    """The specification a significance-seeker would report: smallest
    one-sided p in the declared direction, or smallest two-sided p."""
    if direction is None:
        return ok.loc[ok["p"].idxmin()]
    col = "p_dir" if "p_dir" in ok else "p"
    return ok.loc[ok[col].idxmin()]


def _row_summary(r, extra=()):
    out = {"key": r["key"], "label": r["label"], "coef": float(r["coef"]),
           "se": float(r["se"]), "t": float(r["t"]), "p": float(r["p"]), "n": int(r["n"])}
    for c in ("p_dir", "first_stage_F", "ar_p", "bandwidth", "n_flags", "order"):
        if c in r and pd.notna(r[c]):
            out[c] = float(r[c]) if c != "n_flags" else int(r[c])
    return out


def audit(ledger: pd.DataFrame, min_p_null=None, t_null=None, *, null: NullDraws = None,
          preregistered_key=None, alpha=0.05, direction=None) -> dict:
    """Turn a ledger into the honest summary.

    Accepts either a NullDraws object (`null=`) or the legacy pair
    (`min_p_null`, `t_null`).
    """
    ok = ledger[ledger["status"] == "ok"] if "status" in ledger else ledger
    if ok.empty:
        return {"error": "no specification estimated successfully"}
    if null is not None:
        min_p_null = null.min_p if direction is None else null.min_p_dir
        t_null = null.t
        direction = direction if direction is not None else null.direction
    if direction is not None and "p_dir" not in ok:
        ok = ok.assign(p_dir=inference.one_sided_p(ok["t"], ok["p"], direction))
    best = _best(ok, direction)
    pcol = "p_dir" if direction is not None else "p"
    sig = ok[pcol] < alpha
    flagged = ok["n_flags"] > 0 if "n_flags" in ok else pd.Series(False, index=ok.index)
    out = {
        "direction": {1: "+", -1: "-", None: None}[direction],
        "alpha": alpha,
        "n_specs_enumerated": int(len(ledger)),
        "n_specs_estimated": int(len(ok)),
        "n_specs_failed": int((ledger["status"] != "ok").sum()) if "status" in ledger else 0,
        "n_specs_significant": int(sig.sum()),
        "share_significant": float(sig.mean()),
        "n_specs_flagged": int(flagged.sum()),
        "share_flagged_among_significant": float(flagged[sig].mean()) if sig.any() else 0.0,
        "best_spec": _row_summary(best),
        "curve": inference.spec_curve_stats(ok["coef"], ok["p"], alpha=alpha, sign=direction),
        "bonferroni_p_of_best": float(min(best[pcol] * len(ok), 1.0)),
        "sidak_p_of_best": float(1 - (1 - min(best[pcol], 1.0)) ** len(ok)),
    }
    clean = ok[~flagged]
    if len(clean) and flagged.any():
        bc = _best(clean, direction)
        out["best_unflagged_spec"] = _row_summary(bc)
    if "reported" in ok and ok["reported"].any():
        out["reported_spec"] = _row_summary(ok[ok["reported"]].iloc[0])
    if "walk" in getattr(ledger, "attrs", {}):
        out["walk"] = ledger.attrs["walk"]
    if preregistered_key is not None:
        pre = ok[ok["key"] == preregistered_key]
        if not pre.empty:
            pr = pre.iloc[0]
            out["preregistered"] = _row_summary(pr)
            out["coef_inflation_vs_prereg"] = (
                float(best["coef"] / pr["coef"]) if pr["coef"] else float("inf"))
            out["log10_p_gain"] = float(
                -np.log10(max(best[pcol], 1e-300)) + np.log10(max(pr[pcol], 1e-300)))
            out["prereg_percentile_in_curve"] = float(np.mean(ok["coef"] <= pr["coef"]))
            out["nearest_significant"] = nearest_significant(ok, preregistered_key,
                                                             alpha=alpha, direction=direction)
    out["axis_influence"] = axis_influence(ok, alpha=alpha, direction=direction)
    if min_p_null is not None:
        out["min_p_test"] = inference.min_p_test(float(best[pcol]), min_p_null)
        if "best_unflagged_spec" in out:
            # Calibrate the defensible best against the defensible part of the
            # grid: null columns whose specification is unflagged on the
            # observed data. Flags are almost all structural (estimator,
            # clustering level, bandwidth), so the observed flag set is the
            # right mask for the null draws too.
            p_unf = float(out["best_unflagged_spec"].get("p_dir", out["best_unflagged_spec"]["p"]))
            ref = min_p_null
            if null is not None:
                m = min(null.p.shape[1], len(ok))
                mask = (~flagged).to_numpy()[:m]
                if mask.any():
                    Pm = null.p[:, :m][:, mask]; Tm = null.t[:, :m][:, mask]
                    ref = _min_p_dir(Tm, Pm, direction)
            out["min_p_test_unflagged"] = inference.min_p_test(p_unf, ref)
            out["min_p_test_unflagged"]["n_unflagged_specs"] = int((~flagged).sum())
    if t_null is not None:
        keys = ok["key"].to_numpy()
        tobs = ok["t"].to_numpy()
        m = min(t_null.shape[1], len(tobs))
        rw = inference.romano_wolf(tobs[:m], t_null[:, :m])
        out["romano_wolf_p_of_best"] = float(rw[np.nanargmin(ok[pcol].to_numpy()[:m])]) \
            if m else float("nan")
        out["n_specs_rw_survives"] = int(np.nansum(rw < alpha))
        meff = inference.effective_tests(t_null[:, :m])
        out["effective_tests"] = round(meff, 2)
        out["meff_adjusted_p_of_best"] = round(
            inference.meff_adjusted_p(float(best[pcol]), meff), 6)
    if null is not None and null.coef is not None:
        m = min(null.t.shape[1], len(ok))
        out["ssn_joint"] = inference.ssn_joint_tests(
            ok["coef"].to_numpy()[:m], ok["t"].to_numpy()[:m], ok["p"].to_numpy()[:m],
            null.coef[:, :m], null.t[:, :m], null.p[:, :m], alpha=alpha, direction=direction)
    if null is not None and null.reported_p_null is not None:
        rp = np.asarray(null.reported_p_null, float); fin = np.isfinite(rp)
        pt = {"procedure": null.procedure}
        if "reported_spec" in out:
            rep = out["reported_spec"]
            p_rep = rep.get("p_dir", rep["p"]) if direction else rep["p"]
            pt.update(inference.min_p_test(float(p_rep), null.reported_p_null))
        else:
            pt["note"] = "the procedure reported nothing on the observed data (project abandoned)"
        pt.update({
            # among the null draws on which the procedure reported anything: a
            # two-stage procedure with a continuation rule reports nothing on
            # the draws it abandoned, and a registry of results never sees those
            "null_share_reporting_significant": float(np.mean(rp[fin] < alpha)) if fin.any() else float("nan"),
            "null_share_reporting_any": float(fin.mean()),
            "null_mean_specs_visited": (float(np.nanmean(null.n_visited_null))
                                        if null.n_visited_null is not None else float("nan")),
            "observed_specs_visited": int(out["walk"]["n_visited"]) if "walk" in out else None,
            "reads": ("null_share_reporting_significant is the false-positive rate of this "
                      "procedure on this design, among the null draws on which it reported anything "
                      "(null_share_reporting_any); honest_p is what its reported p is worth"),
        })
        out["procedure_test"] = pt
    return out


def nearest_significant(ok: pd.DataFrame, prereg_key: str, alpha=0.05, direction=None) -> dict:
    """How far, in analytical choices, is the nearest significant specification
    from the pre-registered one? Distance is the number of axes changed
    (Hamming distance over grid.AXES). Small distances mean one or two
    'innocent' choices separate the null from the finding."""
    pre = ok[ok["key"] == prereg_key]
    if pre.empty or "spec_json" not in ok:
        return {"note": "pre-registered specification not in ledger"}
    pcol = "p_dir" if (direction is not None and "p_dir" in ok) else "p"
    sig = ok[ok[pcol] < alpha]
    if direction is not None:
        sig = sig[np.sign(sig["coef"]) == direction]
    if sig.empty:
        return {"distance": None, "note": "no significant specification in the ledger"}
    p0 = json.loads(pre.iloc[0]["spec_json"])
    best_d, best_row, best_diff = None, None, None
    for _, r in sig.iterrows():
        p1 = json.loads(r["spec_json"])
        diff = [a for a in grid.AXES if _norm_json(p0.get(a)) != _norm_json(p1.get(a))]
        if best_d is None or len(diff) < best_d or (len(diff) == best_d and r[pcol] < best_row[pcol]):
            best_d, best_row, best_diff = len(diff), r, diff
    return {
        "distance": int(best_d),
        "axes_changed": best_diff,
        "changes": {a: {"from": _norm_json(p0.get(a)), "to": _norm_json(json.loads(best_row["spec_json"]).get(a))}
                    for a in best_diff},
        "spec": _row_summary(best_row),
        "n_significant_within_1_change": int(sum(
            1 for _, r in sig.iterrows()
            if sum(_norm_json(p0.get(a)) != _norm_json(json.loads(r["spec_json"]).get(a)) for a in grid.AXES) <= 1)),
        "reads": "distance 1 means a single defensible choice turns the null into a finding",
    }


def _norm_json(v):
    if isinstance(v, list):
        return tuple(v)
    return v


def axis_influence(ok: pd.DataFrame, alpha=0.05, direction=None, top_levels=8) -> dict:
    """Which analytical choices drive significance. For each axis that varies,
    the share of significant specifications and the mean |t| at every level,
    and the spread across levels. The axis with the largest spread is where
    the search found its leverage -- and where a reader should look first."""
    pcol = "p_dir" if (direction is not None and "p_dir" in ok) else "p"
    sig = (ok[pcol] < alpha)
    if direction is not None:
        sig = sig & (np.sign(ok["coef"]) == direction)
    out = {}
    cols = [c for c in ["outcome", "controls", "n_controls", "fe", "vcov", "cluster",
                        "y_transform", "d_transform", "outlier_rule", "imputation",
                        "subsample", "weight", "lag", "did_estimator", "comparison_group",
                        "ev_window", "ev_ref", "ev_estimand", "bw_multiplier", "bw_selector", "kernel", "poly", "donut", "rdd_inference",
                        "instruments", "iv_estimator"] if c in ok]
    for c in cols:
        vals = ok[c].astype(str)
        if vals.nunique() < 2:
            continue
        g = pd.DataFrame({"lvl": vals, "sig": sig.to_numpy(), "abs_t": ok["t"].abs().to_numpy()})
        tab = g.groupby("lvl").agg(n=("sig", "size"), share_sig=("sig", "mean"),
                                   mean_abs_t=("abs_t", "mean")).sort_values("share_sig", ascending=False)
        levels = {lv: {"n": int(r.n), "share_sig": round(float(r.share_sig), 3),
                       "mean_abs_t": round(float(r.mean_abs_t), 3)}
                  for lv, r in tab.head(top_levels).iterrows()}
        share_of_sig = float(g.loc[g["sig"], "lvl"].eq(tab.index[0]).mean()) if sig.any() else 0.0
        out[c] = {"spread": round(float(tab["share_sig"].max() - tab["share_sig"].min()), 3),
                  "most_significant_level": str(tab.index[0]),
                  "share_of_all_significant_at_that_level": round(share_of_sig, 3),
                  "levels": levels}
    ranked = sorted(out.items(), key=lambda kv: -kv[1]["spread"])
    return {"ranked_axes": [k for k, _ in ranked], "axes": dict(ranked)}


# --------------------------------------------------------------------------
# Manifest: enough to reproduce the search bit for bit
# --------------------------------------------------------------------------

def _sha1_file(path):
    h = hashlib.sha1()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest(card: dict, df: pd.DataFrame, specs, *, data_path=None, card_path=None,
             thinned_to=None, null=None, procedure=None, seed=0, extra=None) -> dict:
    from . import __version__
    m = {
        "phack_version": __version__,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "card": {"name": card.get("name"), "design": card.get("design"),
                 "sha1": hashlib.sha1(json.dumps(card, sort_keys=True, default=str).encode()).hexdigest(),
                 "path": card_path, "direction": card.get("direction")},
        "data": {"path": data_path, "sha1": _sha1_file(data_path) if data_path and os.path.exists(data_path) else None,
                 "n_rows": int(len(df)), "n_cols": int(df.shape[1]),
                 "columns": list(map(str, df.columns))},
        "grid": {"n_specs": int(len(specs)), "thinned_to": thinned_to,
                 "sha1_of_keys": hashlib.sha1("".join(s.key() for s in specs).encode()).hexdigest()},
        "seed": seed,
    }
    if null is not None:
        m["null"] = {"scheme": null.scheme, "B": null.B, "seed": null.seed,
                     "n_specs": len(null.specs), "procedure": null.procedure}
    if procedure is not None:
        m["procedure"] = {"name": procedure.name, **procedure.params()}
    if extra:
        m.update(extra)
    return m
