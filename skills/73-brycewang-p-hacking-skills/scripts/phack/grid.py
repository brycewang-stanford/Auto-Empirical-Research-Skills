"""
Enumerate the specification universe ("garden of forking paths") from a design
card, and materialise each specification into an estimable design.

The design card is JSON. Every key is a researcher degree of freedom drawn from
the taxonomy in references/taxonomy.md; leaving a key out collapses that
dimension to a single defensible default, which is how you encode a
pre-registered analysis.
"""
from __future__ import annotations

import itertools, json, hashlib
from dataclasses import dataclass, asdict, fields

import numpy as np
import pandas as pd

from . import core

DEFAULTS = {
    "outcomes": None,            # list[str]; required
    "treatment": None,           # str; required (except rdd)
    "controls_pool": [],
    "control_policy": "nested",  # none | nested | all_subsets | leave_one_out
    "max_controls": None,
    "fixed_effects": [[]],       # list of lists of column names
    "vcov": ["hc1"],             # iid|hc0..hc3|cluster|twoway
    "cluster": [None],           # str, or [str,str] for twoway
    "outcome_transforms": ["level"],
    "treatment_transforms": ["level"],   # includes discretisations, see core.DISCRETIZERS
    "outlier_rules": ["none"],
    "outlier_basis": "outcome",  # outcome | treatment | residual
    "imputation": ["listwise"],
    "subsamples": {},            # name -> pandas query string
    "weights": [None],           # column names; None = unweighted
    "interactions": [[]],        # extra terms, each a list of "a*b" strings
    "lags": [0],                 # shift treatment by k periods (needs panel keys)
    "panel_unit": None,
    "panel_time": None,
    # --- DiD axes (design == "did"); need panel_unit / panel_time
    "did_estimators": ["twfe"],          # twfe | did2s | stacked
    "comparison_groups": ["all"],        # all | drop_never_treated | drop_always_treated
    "cohort": None,                      # documentation only; cohorts are inferred from treatment paths
    "stack_window": [3, 3],              # periods before / after adoption in a stack
    # --- event-study axes (design == "did", estimator twfe); None = static DiD
    "event_windows": None,               # list of [leads, lags], endpoints binned
    "reference_periods": [-1],           # omitted relative period(s)
    "event_estimands": ["avg_post"],     # avg_post | lag0 | lag1 | avg_pre (placebo)
    # --- RDD axes (design == "rdd"); treatment is 1{running >= cutoff}
    "running": None,
    "cutoff": 0.0,
    "bandwidth_selectors": ["rot"],      # rot | ik  (pilot the multipliers scale)
    "bandwidth_multipliers": [1.0],      # multiples of the selected pilot
    "bandwidths": None,                  # absolute bandwidths override the above
    "kernels": ["triangular"],
    "poly_orders": [1],
    "donuts": [0.0],
    "rdd_inference": ["conventional"],   # conventional | bias_corrected | robust
    # --- IV axes (design == "iv")
    "instruments_pool": [],
    "instrument_policy": "all",          # all | nested | all_subsets | leave_one_out
    "iv_estimators": ["2sls"],           # 2sls | liml
}

META_KEYS = {"name", "notes", "design", "seed", "preregistered", "direction"}
REQUIRED = ("outcomes", "treatment")

# Axis names as they appear in Spec, the ledger, and the preregistered block.
AXES = ["outcome", "controls", "fe", "vcov", "cluster", "y_transform", "d_transform",
        "outlier_rule", "imputation", "subsample", "weight", "interactions", "lag",
        "did_estimator", "comparison_group", "ev_window", "ev_ref", "ev_estimand",
        "bandwidth", "bw_selector", "kernel", "poly", "donut", "rdd_inference",
        "instruments", "iv_estimator"]


@dataclass
class Spec:
    """One point in the multiverse."""
    idx: int
    outcome: str
    treatment: str
    controls: tuple
    fe: tuple
    vcov: str
    cluster: object
    y_transform: str
    d_transform: str
    outlier_rule: str
    imputation: str
    subsample: str
    weight: object
    interactions: tuple
    lag: int
    did_estimator: str = "twfe"
    comparison_group: str = "all"
    ev_window: object = None      # (leads, lags) or None
    ev_ref: object = None
    ev_estimand: object = None
    bandwidth: object = None      # multiplier (float) or ("abs", value)
    bw_selector: str = "rot"
    kernel: str = "triangular"
    poly: int = 1
    donut: float = 0.0
    rdd_inference: str = "conventional"
    instruments: tuple = ()
    iv_estimator: str = "2sls"

    def label(self) -> str:
        bits = [
            f"y={self.outcome}:{self.y_transform}",
            f"d={self.treatment}:{self.d_transform}",
            f"ctl={len(self.controls)}",
            f"fe={'+'.join(self.fe) or 'none'}",
            f"se={self.vcov}{'/' + str(self.cluster) if self.cluster else ''}",
            f"out={self.outlier_rule}",
            f"imp={self.imputation}",
            f"sub={self.subsample}",
        ]
        if self.lag:
            bits.append(f"lag={self.lag}")
        if self.interactions:
            bits.append("int=" + ",".join(self.interactions))
        if self.weight:
            bits.append(f"w={self.weight}")
        if self.did_estimator != "twfe" or self.comparison_group != "all":
            bits.append(f"did={self.did_estimator}/{self.comparison_group}")
        if self.ev_window is not None:
            bits.append(f"es=w{self.ev_window[0]}/{self.ev_window[1]}/ref{self.ev_ref}/{self.ev_estimand}")
        if self.bandwidth is not None:
            bw = (f"{self.bandwidth[1]:g}abs" if isinstance(self.bandwidth, tuple)
                  else f"{self.bandwidth:g}x{self.bw_selector}")
            bits.append(f"rdd=h{bw}/{self.kernel}/p{self.poly}/donut{self.donut:g}/{self.rdd_inference}")
        if self.instruments:
            bits.append(f"iv={self.iv_estimator}:{'+'.join(self.instruments)}")
        return " | ".join(bits)

    def key(self) -> str:
        return hashlib.sha1(self.label().encode()).hexdigest()[:12]

    def axes(self) -> dict:
        """Axis -> value, hashable, for indexing and for distance computations."""
        d = {}
        for a in AXES:
            v = getattr(self, a)
            if isinstance(v, list):
                v = tuple(v)
            d[a] = v
        return d

    def to_json(self) -> str:
        return json.dumps({k: (list(v) if isinstance(v, tuple) else v)
                           for k, v in asdict(self).items() if k != "idx"}, default=str)


def _control_sets(pool, policy, cap):
    pool = list(pool)
    if policy == "none" or not pool:
        return [tuple()]
    if policy == "nested":
        return [tuple(pool[:i]) for i in range(len(pool) + 1)]
    if policy == "leave_one_out":
        sets = [tuple(pool)]
        sets += [tuple(p for p in pool if p != drop) for drop in pool]
        sets.append(tuple())
        return sets
    if policy == "all_subsets":
        cap = len(pool) if cap is None else min(cap, len(pool))
        out = []
        for r in range(cap + 1):
            out.extend(itertools.combinations(pool, r))
        return out
    raise KeyError(f"unknown control_policy {policy!r}")


def load_card(path_or_dict) -> dict:
    card = dict(DEFAULTS)
    raw = path_or_dict
    if not isinstance(raw, dict):
        with open(raw) as fh:
            raw = json.load(fh)
    unknown = set(raw) - set(DEFAULTS) - META_KEYS
    if unknown:
        raise KeyError(f"unknown design-card keys: {sorted(unknown)}")
    problems = validate_card(raw)
    if problems:
        raise ValueError("design card fails the schema: " + "; ".join(problems[:5]))
    design = raw.get("design", "ols")
    if design == "rdd" and not raw.get("running"):
        raise ValueError("design 'rdd' needs a 'running' column")
    if design == "iv" and not raw.get("instruments_pool"):
        raise ValueError("design 'iv' needs a non-empty 'instruments_pool'")
    if unknown:
        raise KeyError(f"unknown design-card keys: {sorted(unknown)}")
    card.update(raw)
    card.setdefault("design", "ols")
    if card["design"] == "rdd" and not card.get("treatment"):
        card["treatment"] = "__rdd_D__"
    for r in REQUIRED:
        if not card.get(r):
            raise ValueError(f"design card must set {r!r}")
    if isinstance(card["outcomes"], str):
        card["outcomes"] = [card["outcomes"]]
    if card["design"] == "did" and (set(card["did_estimators"]) - {"twfe"} or
                                    set(card["comparison_groups"]) - {"all"}):
        if not (card["panel_unit"] and card["panel_time"]):
            raise ValueError("did_estimators / comparison_groups need panel_unit and panel_time")
    if card.get("direction") not in (None, "+", "-", 1, -1, "pos", "neg"):
        raise ValueError("direction must be '+', '-' or null")
    return card


def card_schema() -> dict:
    """JSON Schema (draft 2020-12) for a design card, generated from DEFAULTS
    so it cannot drift from the loader. Published as schema/design-card.schema.json."""
    str_list = {"type": "array", "items": {"type": "string"}}
    nullable_str = {"type": ["string", "null"]}
    props = {
        "name": {"type": "string"}, "notes": {"type": "string"}, "seed": {"type": "integer"},
        "design": {"type": "string", "enum": ["ols", "rct", "did", "rdd", "iv"], "default": "ols"},
        "direction": {"type": ["string", "null"], "enum": ["+", "-", None]},
        "preregistered": {"type": ["object", "string", "null"],
                          "description": "axis -> value (any subset of grid.AXES), a 12-hex key, or a free-text note"},
        "outcomes": {"oneOf": [str_list, {"type": "string"}]}, "treatment": nullable_str,
        "controls_pool": str_list,
        "control_policy": {"type": "string", "enum": ["none", "nested", "all_subsets", "leave_one_out"]},
        "max_controls": {"type": ["integer", "null"]},
        "fixed_effects": {"type": "array", "items": str_list},
        "vcov": {"type": "array", "items": {"type": "string", "enum": ["iid", "hc0", "hc1", "hc2", "hc3", "cluster", "twoway"]}},
        "cluster": {"type": "array", "items": {"oneOf": [nullable_str, str_list]}},
        "outcome_transforms": {"type": "array", "items": {"type": "string", "enum": sorted(core.TRANSFORMS)}},
        "treatment_transforms": {"type": "array", "items": {"type": "string", "enum": sorted(core.TRANSFORMS)}},
        "outlier_rules": {"type": "array", "items": {"type": "string", "enum": sorted(core.OUTLIER_RULES)}},
        "outlier_basis": {"type": "string", "enum": ["outcome", "treatment", "residual"]},
        "imputation": {"type": "array", "items": {"type": "string", "enum": ["listwise", "mean", "median", "zero", "ffill", "interp"]}},
        "subsamples": {"type": "object", "additionalProperties": {"type": "string"}},
        "weights": {"type": "array", "items": nullable_str},
        "interactions": {"type": "array", "items": str_list},
        "lags": {"type": "array", "items": {"type": "integer", "minimum": 0}},
        "panel_unit": nullable_str, "panel_time": nullable_str,
        "did_estimators": {"type": "array", "items": {"type": "string", "enum": ["twfe", "did2s", "stacked"]}},
        "comparison_groups": {"type": "array", "items": {"type": "string", "enum": ["all", "drop_never_treated", "drop_always_treated"]}},
        "cohort": nullable_str,
        "stack_window": {"type": "array", "items": {"type": "integer", "minimum": 0}, "minItems": 2, "maxItems": 2},
        "event_windows": {"type": ["array", "null"], "items": {"type": "array", "items": {"type": "integer", "minimum": 0}, "minItems": 2, "maxItems": 2}},
        "reference_periods": {"type": "array", "items": {"type": "integer"}},
        "event_estimands": {"type": "array", "items": {"type": "string", "pattern": "^(avg_post|avg_pre|lag[0-9]+)$"}},
        "running": nullable_str, "cutoff": {"type": "number"},
        "bandwidth_selectors": {"type": "array", "items": {"type": "string", "enum": ["rot", "ik"]}},
        "bandwidth_multipliers": {"type": "array", "items": {"type": "number", "exclusiveMinimum": 0}},
        "bandwidths": {"type": ["array", "null"], "items": {"type": "number", "exclusiveMinimum": 0}},
        "kernels": {"type": "array", "items": {"type": "string", "enum": sorted(core.KERNELS)}},
        "poly_orders": {"type": "array", "items": {"type": "integer", "minimum": 0, "maximum": 4}},
        "donuts": {"type": "array", "items": {"type": "number", "minimum": 0}},
        "rdd_inference": {"type": "array", "items": {"type": "string", "enum": ["conventional", "bias_corrected", "robust"]}},
        "instruments_pool": str_list,
        "instrument_policy": {"type": "string", "enum": ["all", "nested", "all_subsets", "leave_one_out"]},
        "iv_estimators": {"type": "array", "items": {"type": "string", "enum": ["2sls", "liml"]}},
    }
    return {"$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://github.com/brycewang-stanford/p-hacking-skills/schema/design-card.schema.json",
            "title": "phack design card",
            "description": "One axis per researcher degree of freedom; omit a key to fix that axis at its default. "
                           "Requires `outcomes`, and `treatment` unless design is rdd (then `running`); iv needs `instruments_pool`.",
            "type": "object", "properties": props, "required": ["outcomes"], "additionalProperties": False}


def validate_card(raw: dict) -> list:
    """Return a list of schema violations (empty = valid). Uses jsonschema when
    installed; otherwise only the loader's own checks apply."""
    try:
        import jsonschema
    except ImportError:
        return []
    v = jsonschema.Draft202012Validator(card_schema())
    return [f"{'/'.join(map(str, e.path)) or '<card>'}: {e.message}" for e in v.iter_errors(raw)]


def direction_sign(card_or_value):
    v = card_or_value.get("direction") if isinstance(card_or_value, dict) else card_or_value
    if v in (None, 0, "", "none", "two-sided"):
        return None
    return 1 if v in ("+", 1, "pos", "positive") else -1


def _instrument_sets(pool, policy):
    pool = list(pool)
    if policy == "all":
        return [tuple(pool)]
    sets = _control_sets(pool, policy, None)
    return [z for z in sets if len(z) > 0]


def enumerate_specs(card: dict) -> list[Spec]:
    ctl_sets = _control_sets(card["controls_pool"], card["control_policy"], card["max_controls"])
    design = card.get("design", "ols")
    if design == "rdd":
        bws = ([(("abs", float(b)), "abs") for b in card["bandwidths"]] if card["bandwidths"]
               else [(float(m), sel) for sel in card["bandwidth_selectors"]
                     for m in card["bandwidth_multipliers"]])
        rdd_axes = list(itertools.product(bws, card["kernels"], card["poly_orders"],
                                          card["donuts"], card["rdd_inference"]))
    else:
        rdd_axes = [((None, "rot"), "triangular", 1, 0.0, "conventional")]
    if design == "iv":
        iv_axes = list(itertools.product(_instrument_sets(card["instruments_pool"], card["instrument_policy"]),
                                         card["iv_estimators"]))
    else:
        iv_axes = [((), "2sls")]
    if design == "did":
        did_axes = list(itertools.product(card["did_estimators"], card["comparison_groups"]))
    else:
        did_axes = [("twfe", "all")]
    ev_axes = [(None, None, None)]          # the static DiD is always one of the specs
    if design == "did" and card["event_windows"]:
        ev_axes += [(tuple(int(v) for v in w), int(r), e)
                    for w in card["event_windows"] for r in card["reference_periods"]
                    for e in card["event_estimands"]]
    subs = card["subsamples"] or {"full": None}
    if "full" not in subs:
        subs = {"full": None, **subs}
    axes = itertools.product(
        card["outcomes"], ctl_sets,
        [tuple(f) for f in card["fixed_effects"]],
        card["vcov"], card["cluster"],
        card["outcome_transforms"], card["treatment_transforms"],
        card["outlier_rules"], card["imputation"],
        list(subs), card["weights"],
        [tuple(i) for i in card["interactions"]], card["lags"],
        did_axes, ev_axes, rdd_axes, iv_axes,
    )
    specs, i = [], 0
    seen = set()
    for (y, ctl, fe, vc, cl, yt, dt, orule, imp, sub, w, ints, lag, dd, ev, rd, iv) in axes:
        if ev[0] is not None and (dd[0] != "twfe" or lag or dt in core.DISCRETIZERS):
            continue                      # event studies: TWFE path only
        if design == "rdd" and (fe or vc == "twoway"):
            continue                      # local polynomial: no FE, no two-way
        if design == "iv" and vc in ("twoway", "hc2", "hc3"):
            continue
        if vc in ("cluster", "twoway") and cl is None:
            continue
        if vc not in ("cluster", "twoway") and cl is not None:
            continue
        if vc == "twoway" and not isinstance(cl, (list, tuple)):
            continue
        if vc == "cluster" and isinstance(cl, (list, tuple)):
            continue
        if dd[0] != "twfe":
            # the estimator fixes its own fixed-effect structure; the FE axis is
            # collapsed so the same estimate is not counted many times over
            fe = (card["panel_unit"], card["panel_time"])
            if vc == "twoway":
                continue
        if dt in core.DISCRETIZERS and (lag or dd[0] != "twfe"):
            continue
        s = Spec(i, y, card["treatment"], ctl, fe, vc,
                 tuple(cl) if isinstance(cl, list) else cl,
                 yt, dt, orule, imp, sub, w, ints, lag,
                 did_estimator=dd[0], comparison_group=dd[1],
                 ev_window=ev[0], ev_ref=ev[1], ev_estimand=ev[2],
                 bandwidth=rd[0][0], bw_selector=rd[0][1], kernel=rd[1], poly=rd[2],
                 donut=rd[3], rdd_inference=rd[4],
                 instruments=tuple(iv[0]), iv_estimator=iv[1])
        if s.key() in seen:
            continue
        seen.add(s.key())
        specs.append(s)
        i += 1
    return specs


def universe_size(card: dict) -> dict:
    """Report the size of the garden before walking it."""
    specs = enumerate_specs(card)
    dims = {}
    for a in AXES:
        vals = {s.axes()[a] for s in specs}
        if len(vals) > 1:
            dims[a] = len(vals)
    return {"n_specs": len(specs), "dimensions": dims,
            "n_varying_axes": len(dims),
            "log10_specs": round(float(np.log10(max(len(specs), 1))), 2)}


# --------------------------------------------------------------------------
# Pre-registration: resolve a structured block on the card to one spec key
# --------------------------------------------------------------------------

def resolve_prereg(card: dict, specs=None):
    """Find the key of the pre-registered specification.

    `card["preregistered"]` may be a 12-hex key, or a dict of axis values
    (any subset of grid.AXES). Missing axes default to the *first* level on
    the card, which is the convention for "the default choice". Returns None
    when the card carries only a free-text note.
    """
    pre = card.get("preregistered")
    if pre is None or isinstance(pre, str) and len(pre) != 12:
        return None
    specs = specs if specs is not None else enumerate_specs(card)
    if isinstance(pre, str):
        return pre if any(s.key() == pre for s in specs) else None
    want = _prereg_axes(card, pre)
    hits = [s for s in specs if all(s.axes()[a] == v for a, v in want.items())]
    if len(hits) != 1:
        raise ValueError(f"preregistered block matches {len(hits)} specifications, need exactly 1; "
                         f"resolved axes = {want}")
    return hits[0].key()


def _norm(v):
    if isinstance(v, list):
        return tuple(v)
    return v


def _prereg_axes(card, pre):
    first = {
        "outcome": card["outcomes"][0], "controls": tuple(),
        "fe": tuple(card["fixed_effects"][0]), "vcov": card["vcov"][0],
        "cluster": _norm(card["cluster"][0]), "y_transform": card["outcome_transforms"][0],
        "d_transform": card["treatment_transforms"][0], "outlier_rule": card["outlier_rules"][0],
        "imputation": card["imputation"][0], "subsample": "full", "weight": card["weights"][0],
        "interactions": tuple(), "lag": card["lags"][0],
        "did_estimator": card["did_estimators"][0], "comparison_group": card["comparison_groups"][0],
        "ev_window": tuple(card["event_windows"][0]) if card["event_windows"] else None,
        "ev_ref": card["reference_periods"][0] if card["event_windows"] else None,
        "ev_estimand": card["event_estimands"][0] if card["event_windows"] else None,
        "kernel": card["kernels"][0], "poly": card["poly_orders"][0], "donut": card["donuts"][0],
        "rdd_inference": card["rdd_inference"][0], "bw_selector": card["bandwidth_selectors"][0],
        "bandwidth": (("abs", float(card["bandwidths"][0])) if card["bandwidths"]
                      else float(card["bandwidth_multipliers"][0])) if card["design"] == "rdd" else None,
        "instruments": tuple(card["instruments_pool"]) if card["design"] == "iv" else tuple(),
        "iv_estimator": card["iv_estimators"][0],
    }
    unknown = set(pre) - set(AXES)
    if unknown:
        raise KeyError(f"preregistered block has unknown axes {sorted(unknown)}; known: {AXES}")
    out = dict(first)
    for a, v in pre.items():
        v = _norm(v)
        if a == "bandwidth" and isinstance(v, (int, float)):
            v = float(v)
        if a == "controls" and isinstance(v, str):
            v = tuple(v.split("+")) if v not in ("none", "") else tuple()
        if a == "ev_window" and v is not None:
            v = tuple(int(x) for x in v)
        out[a] = v
    return out


def thin(specs, k, keep_keys=()):
    """Evenly thin a grid to k specifications, always keeping `keep_keys`
    (the pre-registered specification above all: thinning must never make the
    honest anchor disappear). Returns the original list when k is falsy or
    not smaller than the grid."""
    specs = list(specs)
    if not k or len(specs) <= k:
        return specs
    keep = {kk for kk in keep_keys if kk}
    pick = set(np.linspace(0, len(specs) - 1, k).astype(int))
    forced = [i for i, s in enumerate(specs) if s.key() in keep]
    pick |= set(forced)
    out = [specs[i] for i in sorted(pick)]
    return out


class SpecIndex:
    """Axis-value lookup over an enumerated grid, for procedures that move one
    axis at a time (coordinate search) rather than walking the whole product."""

    def __init__(self, specs):
        self.specs = list(specs)
        self.by_key = {s.key(): s for s in self.specs}
        self.by_axes = {tuple(sorted(s.axes().items(), key=lambda kv: kv[0])): s for s in self.specs}
        self.levels = {a: sorted({s.axes()[a] for s in self.specs}, key=str) for a in AXES}
        self.varying = [a for a in AXES if len(self.levels[a]) > 1]

    def neighbour(self, spec, axis, value):
        ax = spec.axes(); ax[axis] = value
        return self.by_axes.get(tuple(sorted(ax.items(), key=lambda kv: kv[0])))

    def neighbours(self, spec, axis):
        out = []
        for v in self.levels[axis]:
            if v != spec.axes()[axis]:
                n = self.neighbour(spec, axis, v)
                if n is not None:
                    out.append(n)
        return out


def axis_distance(a: Spec, b: Spec) -> tuple[int, list]:
    """Number of axes on which two specifications differ, and which ones."""
    xa, xb = a.axes(), b.axes()
    diff = [k for k in AXES if xa[k] != xb[k]]
    return len(diff), diff


# --------------------------------------------------------------------------
# Materialisation: Spec -> estimable design
# --------------------------------------------------------------------------

def _apply_comparison_group(d, spec, card):
    if spec.comparison_group == "all":
        return d
    unit, t = card["panel_unit"], spec.treatment
    ever = d.groupby(unit)[t].transform("max")
    always = d.groupby(unit)[t].transform("min")
    if spec.comparison_group == "drop_never_treated":
        return d[ever > 0]
    if spec.comparison_group == "drop_always_treated":
        return d[always < 1]
    raise KeyError(f"unknown comparison_group {spec.comparison_group!r}")


def _infer_cohort(d, unit, time, treat):
    """First period with treat == 1 per unit; +inf for never-treated."""
    first = d[d[treat] > 0].groupby(unit)[time].min()
    return d[unit].map(first).fillna(np.inf).to_numpy(float)


def _stack(d, spec, card, ycol, dcol, ctl_cols, wcol):
    """Stacked DiD (Cengiz et al. 2019): one clean 2x2 per adoption cohort."""
    unit, time = card["panel_unit"], card["panel_time"]
    pre, post = card["stack_window"]
    # Cohorts are always inferred from the treatment paths, never read from a
    # column: a null draw permutes the paths, and a stale cohort column would
    # silently misalign the stacks. `card["cohort"]` is documentation only.
    cohort = _infer_cohort(d, unit, time, dcol)
    d = d.assign(__cohort=cohort)
    tt = d[time].to_numpy(float)
    blocks = []
    for g in sorted({c for c in cohort if np.isfinite(c)}):
        win = (tt >= g - pre) & (tt <= g + post)
        clean = (d["__cohort"].to_numpy() > g + post)          # never / not-yet treated
        treated = d["__cohort"].to_numpy() == g
        sel = win & (clean | treated)
        if sel.sum() < 10 or treated[sel].sum() == 0 or clean[sel].sum() == 0:
            continue
        b = d.loc[sel].copy()
        b["__stack"] = g
        blocks.append(b)
    if not blocks:
        raise ValueError("stacked DiD: no cohort has both treated units and clean controls")
    s = pd.concat(blocks, ignore_index=True)
    s["__unit_stack"] = s[unit].astype(str) + "@" + s["__stack"].astype(str)
    s["__time_stack"] = s[time].astype(str) + "@" + s["__stack"].astype(str)
    return s


def _did2s_residualise(d, spec, card, ycol, dcol, ctl_cols, wcol):
    """Gardner (2022) two-stage DiD: fit unit and time effects (and controls)
    on untreated observations only, remove them from every observation, then
    regress the residual on treatment. Stage-2 SEs ignore stage-1 sampling
    error, which is the standard implementation's known simplification."""
    unit, time = card["panel_unit"], card["panel_time"]
    y = d[ycol].to_numpy(float); t = d[dcol].to_numpy(float)
    untreated = t == 0
    if untreated.sum() < 10:
        raise ValueError("did2s: too few untreated observations for stage 1")
    w = None if wcol is None else d[wcol].to_numpy(float)
    C = np.column_stack([d[c].to_numpy(float) for c in ctl_cols]) if ctl_cols else None
    ui = pd.factorize(d[unit])[0]; ti = pd.factorize(d[time])[0]
    beta = np.zeros(0)
    if C is not None:
        M, _ = core.absorb(np.column_stack([y[untreated], C[untreated]]),
                           [ui[untreated], ti[untreated]],
                           weights=None if w is None else w[untreated])
        beta = np.linalg.lstsq(M[:, 1:], M[:, 0], rcond=None)[0]
    yc = y - (C @ beta if C is not None else 0.0)
    alpha = np.zeros(ui.max() + 1); lam = np.zeros(ti.max() + 1)
    ww = np.ones(y.size) if w is None else w
    for _ in range(500):
        a_old = alpha.copy()
        r = yc - lam[ti]
        num = np.bincount(ui[untreated], weights=(ww * r)[untreated], minlength=alpha.size)
        den = np.bincount(ui[untreated], weights=ww[untreated], minlength=alpha.size)
        alpha = np.where(den > 0, num / np.clip(den, 1e-12, None), np.nan)
        r = yc - np.nan_to_num(alpha)[ui]
        num = np.bincount(ti[untreated], weights=(ww * r)[untreated], minlength=lam.size)
        den = np.bincount(ti[untreated], weights=ww[untreated], minlength=lam.size)
        lam = np.where(den > 0, num / np.clip(den, 1e-12, None), np.nan)
        if np.nanmax(np.abs(alpha - a_old)) < 1e-9:
            break
    ytil = yc - alpha[ui] - lam[ti]
    keep = np.isfinite(ytil)                     # always-treated units drop out
    return ytil, keep


def _event_study_design(d, spec, card, yv, X, wts):
    """Relative-time dummies with binned endpoints and an omitted reference
    period; the estimand is a linear combination of the dummy coefficients.
    Moving the reference period or the window changes the estimate without
    touching a single data point -- strategy 19."""
    unit, time = card["panel_unit"], card["panel_time"]
    leads, lags = spec.ev_window
    tt = d[time].to_numpy(float)
    cohort = _infer_cohort(d.assign(__d=X[:, 0]), unit, time, "__d")
    rel = np.where(np.isfinite(cohort), tt - cohort, np.nan)
    rel_b = np.clip(rel, -leads, lags)                       # bin the endpoints
    periods = [r for r in range(-leads, lags + 1) if r != spec.ev_ref]
    if spec.ev_ref < -leads or spec.ev_ref > lags:
        raise ValueError(f"reference period {spec.ev_ref} outside window [-{leads}, {lags}]")
    D = np.column_stack([(np.nan_to_num(rel_b, nan=np.inf) == r).astype(float) for r in periods])
    if D.sum(axis=0).min() == 0:
        raise ValueError("an event-time dummy has no support in this sample")
    Xe = np.column_stack([D, X[:, 1:]]) if X.shape[1] > 1 else D
    post = [j for j, r in enumerate(periods) if r >= 0]
    pre = [j for j, r in enumerate(periods) if r < 0]
    a = np.zeros(Xe.shape[1])
    if spec.ev_estimand == "avg_post":
        a[post] = 1.0 / len(post)
    elif spec.ev_estimand == "avg_pre":
        a[pre] = 1.0 / len(pre)
    elif spec.ev_estimand.startswith("lag"):
        k = int(spec.ev_estimand[3:])
        j = [j for j, r in enumerate(periods) if r == k]
        if not j:
            raise ValueError(f"lag {k} is the reference period or outside the window")
        a[j[0]] = 1.0
    else:
        raise KeyError(f"unknown event estimand {spec.ev_estimand!r}")
    groups = [d[f].to_numpy() for f in spec.fe]
    if groups:
        M, ka = core.absorb(np.column_stack([yv, Xe]), groups, weights=wts)
        return {"design": "lincom", "y": M[:, 0], "X": M[:, 1:], "cluster": _cl(d, spec),
                "k_absorbed": ka, "has_const": False, "weights": wts, "vcov": spec.vcov, "a": a,
                "n_treated_cohorts": int(np.unique(cohort[np.isfinite(cohort)]).size)}
    return {"design": "lincom", "y": yv, "X": np.column_stack([np.ones(len(yv)), Xe]),
            "cluster": _cl(d, spec), "k_absorbed": 0, "has_const": True, "weights": wts,
            "vcov": spec.vcov, "a": np.r_[0.0, a],
            "n_treated_cohorts": int(np.unique(cohort[np.isfinite(cohort)]).size)}


def build(df: pd.DataFrame, spec: Spec, card: dict):
    d = df
    if spec.subsample != "full":
        q = (card["subsamples"] or {})[spec.subsample]
        d = d.query(q)
    design = card.get("design", "ols")
    needed = [spec.outcome, *spec.controls, *spec.fe]
    if design == "rdd":
        needed.append(card["running"])
    else:
        needed.append(spec.treatment)
    needed += list(spec.instruments)
    if spec.cluster:
        needed += list(spec.cluster) if isinstance(spec.cluster, tuple) else [spec.cluster]
    if spec.weight:
        needed.append(spec.weight)
    for term in spec.interactions:
        needed.extend(term.split("*"))
    if design == "did":
        needed += [card["panel_unit"], card["panel_time"]]
        if card.get("cohort"):
            needed.append(card["cohort"])
    needed = [c for c in dict.fromkeys(needed) if c is not None]
    missing = [c for c in needed if c not in d.columns]
    if missing:
        raise KeyError(f"spec {spec.idx} references absent columns {missing}")
    d = d.loc[:, needed]

    if design == "rdd":
        d = d.assign(**{spec.treatment: (d[card["running"]] >= card["cutoff"]).astype(float)})
    numeric = [c for c in (spec.outcome, spec.treatment, *spec.controls, *spec.instruments) if c in d]
    d = core.impute(d, numeric, spec.imputation)

    if spec.lag:
        if not (card["panel_unit"] and card["panel_time"]):
            raise ValueError("lags require panel_unit and panel_time on the card")
        base = df.sort_values([card["panel_unit"], card["panel_time"]])
        lagged = base.groupby(card["panel_unit"])[spec.treatment].shift(spec.lag)
        d = d.assign(**{spec.treatment: lagged.reindex(d.index)})

    if design == "did":
        d = _apply_comparison_group(d, spec, card)

    d = d.dropna()
    if len(d) < 10:
        raise ValueError(f"spec {spec.idx} left {len(d)} rows")

    y = core.apply_transform(d[spec.outcome], spec.y_transform)
    dd = core.apply_transform(d[spec.treatment], spec.d_transform)
    ok = np.isfinite(y.to_numpy()) & np.isfinite(dd.to_numpy())
    y, dd, d = y[ok], dd[ok], d.loc[ok]

    if card["outlier_basis"] == "residual" and spec.outlier_rule != "none":
        Xr = np.column_stack([np.ones(len(d)), dd.to_numpy(float)] +
                             [d[c].to_numpy(float) for c in spec.controls])
        basis = core.studentized_residuals(y.to_numpy(float), Xr,
                                           None if spec.weight is None else d[spec.weight])
    else:
        basis = {"outcome": y, "treatment": dd}.get(card["outlier_basis"], y)
    keep = ~core.flag_outliers(basis, spec.outlier_rule)
    y, dd, d = y[keep], dd[keep], d.loc[keep]

    wts = None if spec.weight is None else d[spec.weight].to_numpy(float)
    cols = [dd.to_numpy(dtype=float)]
    for c in spec.controls:
        cols.append(d[c].to_numpy(dtype=float))
    for term in spec.interactions:
        a, b = term.split("*")
        cols.append(d[a].to_numpy(dtype=float) * d[b].to_numpy(dtype=float))
    X = np.column_stack(cols)
    yv = y.to_numpy(dtype=float)

    if design == "rdd":
        x = d[card["running"]].to_numpy(dtype=float)
        if isinstance(spec.bandwidth, tuple):
            h = spec.bandwidth[1]
        else:
            pilot = (core.ik_bandwidth(yv, x, card["cutoff"]) if spec.bw_selector == "ik"
                     else core.rot_bandwidth(x - card["cutoff"]))
            h = spec.bandwidth * pilot
        ctl = X[:, 1:] if X.shape[1] > 1 else None
        return {"design": "rdd", "y": yv, "x": x, "h": h, "controls": ctl,
                "cluster": _cl(d, spec), "kernel": spec.kernel, "poly": spec.poly,
                "donut": spec.donut, "cutoff": card["cutoff"], "vcov": spec.vcov,
                "inference": spec.rdd_inference, "weights": wts}
    if design == "iv":
        Z = np.column_stack([d[z].to_numpy(dtype=float) for z in spec.instruments])
        ctl = X[:, 1:] if X.shape[1] > 1 else None
        if spec.fe:
            blocks = [yv[:, None], X, Z]
            M, ka = core.absorb(np.column_stack(blocks), [d[f].to_numpy() for f in spec.fe],
                                weights=wts)
            yv, X, Z = M[:, 0], M[:, 1:1 + X.shape[1]], M[:, 1 + X.shape[1]:]
            ctl = X[:, 1:] if X.shape[1] > 1 else None
        return {"design": "iv", "y": yv, "d": X[:, 0], "Z": Z, "controls": ctl,
                "cluster": _cl(d, spec), "vcov": spec.vcov, "estimator": spec.iv_estimator,
                "weights": wts}

    if design == "did" and spec.ev_window is not None:
        return _event_study_design(d, spec, card, yv, X, wts)
    if design == "did" and spec.did_estimator == "did2s":
        dtmp = d.assign(__y=yv, __d=X[:, 0])
        ytil, keep2 = _did2s_residualise(dtmp, spec, card, "__y", "__d", list(spec.controls), spec.weight)
        Xs = np.column_stack([np.ones(keep2.sum()), X[keep2, 0]])
        return {"design": "ols", "y": ytil[keep2], "X": Xs, "cluster": _cl(d.loc[keep2], spec),
                "k_absorbed": 0, "has_const": True, "weights": None if wts is None else wts[keep2],
                "vcov": spec.vcov}
    if design == "did" and spec.did_estimator == "stacked":
        dtmp = d.assign(__y=yv, __d=X[:, 0])
        for j, c in enumerate(spec.controls):
            dtmp[f"__c{j}"] = X[:, 1 + j]
        s = _stack(dtmp, spec, card, "__y", "__d", list(spec.controls), spec.weight)
        Xs = np.column_stack([s["__d"].to_numpy(float)] +
                             [s[f"__c{j}"].to_numpy(float) for j in range(len(spec.controls))])
        ws = None if wts is None else s[spec.weight].to_numpy(float)
        M, ka = core.absorb(np.column_stack([s["__y"].to_numpy(float), Xs]),
                            [s["__unit_stack"].to_numpy(), s["__time_stack"].to_numpy()], weights=ws)
        return {"design": "ols", "y": M[:, 0], "X": M[:, 1:], "cluster": _cl(s, spec),
                "k_absorbed": ka, "has_const": False, "weights": ws, "vcov": spec.vcov,
                "n_stacks": int(s["__stack"].nunique())}

    groups = [d[f].to_numpy() for f in spec.fe]
    if groups:
        M, ka = core.absorb(np.column_stack([yv, X]), groups, weights=wts)
        return {"design": "ols", "y": M[:, 0], "X": M[:, 1:], "cluster": _cl(d, spec),
                "k_absorbed": ka, "has_const": False, "weights": wts, "vcov": spec.vcov}
    X = np.column_stack([np.ones(len(yv)), X])
    return {"design": "ols", "y": yv, "X": X, "cluster": _cl(d, spec),
            "k_absorbed": 0, "has_const": True, "weights": wts, "vcov": spec.vcov}


def _cl(d, spec):
    if spec.cluster is None:
        return None
    if isinstance(spec.cluster, tuple):
        return (d[spec.cluster[0]].to_numpy(), d[spec.cluster[1]].to_numpy())
    return d[spec.cluster].to_numpy()
