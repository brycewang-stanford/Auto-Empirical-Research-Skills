"""
Search procedures: how a specification universe actually gets walked.

Exhaustive enumeration is what a multiverse analysis does. It is not what a
p-hacker does, and it is not what an agent under significance pressure does.
They walk *sequentially*, with a stopping rule, along a path shaped by which
knobs are easiest to turn. The false-positive rate and the inflation of the
reported estimate both depend on that procedure, not just on the grid
(Stefan & Schoenbrodt 2023 section 6; Simonsohn et al. 2020 on "first
significant" versus "most significant").

Each procedure is a pure function of (grid, fitter, rng, alpha, direction) and
returns a Walk: the specifications visited in order, the one it would report,
and why it stopped. Because the walk is deterministic given the rng, the same
procedure can be replayed on null data -- which is how `search.null_calibration`
computes the false-positive rate of the *procedure* rather than of the grid.

    exhaustive         visit everything, report the best (ambitious)
    first_significant  visit in order, stop at the first p < alpha (modest)
    random             sample `budget` specifications, report the best
    greedy             coordinate descent from a start spec, one axis at a time
    hill_climb         random single-axis moves, accepted when they improve p
    split_sample       two stages: search on a pilot share of the units, then report
                       the chosen specification on the held-out share (honest),
                       on all the data (pooled: the pilot's luck is inside the
                       reported test) or as the pilot estimate itself. With
                       `continue_at`, the confirmatory stage is only run after a
                       promising pilot -- selective continuation, after Adda,
                       Decker & Ottaviani (2020).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import grid, inference

__all__ = ["Walk", "Procedure", "Exhaustive", "FirstSignificant", "RandomBudget",
           "GreedyCoordinate", "HillClimb", "SplitSample", "PROCEDURES", "make"]


@dataclass
class Walk:
    visited: list                       # Specs in visit order
    reported: object                    # Spec or None
    stopped: str                        # why the walk ended
    path: list = field(default_factory=list)   # per-step notes, for the ledger / narrative
    reported_result: dict = None        # a fit that overrides the full-data fit of `reported`
                                        # (a held-out or pilot estimate); None = the full-data fit
    stage_results: dict = None          # key -> extra ledger columns (e.g. the pilot-stage p)


def _objective(r, direction):
    """Smaller is better: one-sided p in `direction`, or two-sided p."""
    if r.get("status", "ok") != "ok" or not np.isfinite(r.get("p", np.nan)):
        return np.inf
    if direction is None:
        return float(r["p"])
    return float(inference.one_sided_p(r["t"], r["p"], direction))


class Procedure:
    name = "abstract"

    def params(self) -> dict:
        return {}

    def walk(self, specs, fit, rng, alpha=0.05, direction=None) -> Walk:
        raise NotImplementedError


class Exhaustive(Procedure):
    """The multiverse walk. Reports the best specification (ambitious hacking) --
    or, with report='first', the first significant one it meets in grid order."""
    name = "exhaustive"

    def __init__(self, report="best"):
        self.report = report

    def params(self):
        return {"report": self.report}

    def walk(self, specs, fit, rng, alpha=0.05, direction=None):
        best, best_o, first = None, np.inf, None
        for s in specs:
            o = _objective(fit(s), direction)
            if o < best_o:
                best, best_o = s, o
            if first is None and o < alpha:
                first = s
        rep = first if (self.report == "first" and first is not None) else best
        return Walk(list(specs), rep, "grid exhausted")


class FirstSignificant(Procedure):
    """Modest p-hacking: walk in `order` and stop at the first significant
    specification. `fallback` decides what is reported when none is found:
    'first' (the original analysis, honest failure) or 'best' (still the most
    favourable, which is what the estimate-inflation literature assumes)."""
    name = "first_significant"

    def __init__(self, order="card", budget=None, fallback="first"):
        self.order, self.budget, self.fallback = order, budget, fallback

    def params(self):
        return {"order": self.order, "budget": self.budget, "fallback": self.fallback}

    def walk(self, specs, fit, rng, alpha=0.05, direction=None):
        idx = np.arange(len(specs))
        if self.order == "random":
            idx = rng.permutation(idx)
        if self.budget:
            idx = idx[:self.budget]
        visited, best, best_o = [], None, np.inf
        for i in idx:
            s = specs[i]; visited.append(s)
            o = _objective(fit(s), direction)
            if o < best_o:
                best, best_o = s, o
            if o < alpha:
                return Walk(visited, s, f"first significant after {len(visited)} specs")
        rep = visited[0] if (self.fallback == "first" and visited) else best
        return Walk(visited, rep, "budget exhausted without significance")


class RandomBudget(Procedure):
    """Try `budget` randomly chosen specifications; report the best. With
    stop_at_alpha, stop early -- the modest variant."""
    name = "random"

    def __init__(self, budget=30, stop_at_alpha=False):
        self.budget, self.stop_at_alpha = int(budget), bool(stop_at_alpha)

    def params(self):
        return {"budget": self.budget, "stop_at_alpha": self.stop_at_alpha}

    def walk(self, specs, fit, rng, alpha=0.05, direction=None):
        idx = rng.permutation(len(specs))[:self.budget]
        visited, best, best_o = [], None, np.inf
        for i in idx:
            s = specs[i]; visited.append(s)
            o = _objective(fit(s), direction)
            if o < best_o:
                best, best_o = s, o
            if self.stop_at_alpha and o < alpha:
                return Walk(visited, s, f"stopped at alpha after {len(visited)} specs")
        return Walk(visited, best, "budget exhausted")


def _start(index, specs, start, rng):
    if start in ("first", None):
        return specs[0]
    if start == "random":
        return specs[int(rng.integers(len(specs)))]
    if start in index.by_key:
        return index.by_key[start]
    raise KeyError(f"start {start!r} is neither 'first', 'random' nor a spec key in the grid")


class GreedyCoordinate(Procedure):
    """Coordinate descent: from a start specification, sweep the axes in
    `axis_order` (default: the order the card lists them); on each axis try
    every level holding the others fixed and move to the best. Repeat for
    `max_rounds` sweeps or until nothing improves. This is the search an
    analyst does when they say "let me just try clustering differently...
    and now the controls... and now the window".

    With stop_at_alpha the walk halts as soon as a significant specification
    is met (modest); without it, it runs to a local optimum (ambitious)."""
    name = "greedy"

    def __init__(self, start="first", axis_order=None, max_rounds=3,
                 stop_at_alpha=True, budget=None):
        self.start, self.axis_order = start, axis_order
        self.max_rounds, self.stop_at_alpha, self.budget = int(max_rounds), bool(stop_at_alpha), budget

    def params(self):
        return {"start": self.start, "axis_order": self.axis_order, "max_rounds": self.max_rounds,
                "stop_at_alpha": self.stop_at_alpha, "budget": self.budget}

    def walk(self, specs, fit, rng, alpha=0.05, direction=None):
        index = grid.SpecIndex(specs)
        cur = _start(index, specs, self.start, rng)
        axes = [a for a in (self.axis_order or index.varying) if a in index.varying]
        visited, seen, path = [cur], {cur.key()}, []
        cur_o = _objective(fit(cur), direction)
        if self.stop_at_alpha and cur_o < alpha:
            return Walk(visited, cur, "start specification already significant", path)
        for rnd in range(self.max_rounds):
            improved = False
            for a in axes:
                cand = [(cur, cur_o)]
                for nb in index.neighbours(cur, a):
                    if nb.key() not in seen:
                        visited.append(nb); seen.add(nb.key())
                    o = _objective(fit(nb), direction)
                    cand.append((nb, o))
                    if self.budget and len(visited) >= self.budget:
                        break
                    if self.stop_at_alpha and o < alpha:
                        path.append({"round": rnd, "axis": a, "moved_to": nb.axes()[a], "p": o})
                        return Walk(visited, nb, f"stopped at alpha on axis {a!r} after {len(visited)} specs", path)
                nb, o = min(cand, key=lambda c: c[1])
                if o < cur_o - 1e-12:
                    path.append({"round": rnd, "axis": a, "from": cur.axes()[a],
                                 "moved_to": nb.axes()[a], "p_from": cur_o, "p_to": o})
                    cur, cur_o, improved = nb, o, True
                if self.budget and len(visited) >= self.budget:
                    return Walk(visited, cur, "budget exhausted", path)
            if not improved:
                return Walk(visited, cur, f"local optimum after {rnd + 1} sweeps", path)
        return Walk(visited, cur, f"{self.max_rounds} sweeps completed", path)


class HillClimb(Procedure):
    """Random single-axis moves, accepted when they lower p. The least
    systematic walk here, and the closest to an agent 'trying a few things'.
    `patience` failed moves in a row ends the walk."""
    name = "hill_climb"

    def __init__(self, start="first", budget=40, stop_at_alpha=True, patience=15):
        self.start, self.budget = start, int(budget)
        self.stop_at_alpha, self.patience = bool(stop_at_alpha), int(patience)

    def params(self):
        return {"start": self.start, "budget": self.budget,
                "stop_at_alpha": self.stop_at_alpha, "patience": self.patience}

    def walk(self, specs, fit, rng, alpha=0.05, direction=None):
        index = grid.SpecIndex(specs)
        cur = _start(index, specs, self.start, rng)
        cur_o = _objective(fit(cur), direction)
        visited, seen, path, fails = [cur], {cur.key()}, [], 0
        if self.stop_at_alpha and cur_o < alpha:
            return Walk(visited, cur, "start specification already significant", path)
        while len(visited) < self.budget and fails < self.patience and index.varying:
            a = index.varying[int(rng.integers(len(index.varying)))]
            nbs = index.neighbours(cur, a)
            if not nbs:
                fails += 1; continue
            nb = nbs[int(rng.integers(len(nbs)))]
            if nb.key() not in seen:
                visited.append(nb); seen.add(nb.key())
            o = _objective(fit(nb), direction)
            if o < cur_o:
                path.append({"axis": a, "from": cur.axes()[a], "moved_to": nb.axes()[a],
                             "p_from": cur_o, "p_to": o})
                cur, cur_o, fails = nb, o, 0
                if self.stop_at_alpha and o < alpha:
                    return Walk(visited, cur, f"stopped at alpha after {len(visited)} specs", path)
            else:
                fails += 1
        why = ("budget exhausted" if len(visited) >= self.budget else
               f"no improvement in {self.patience} moves")
        return Walk(visited, cur, why, path)


def _split_mask(df, card, rng, pilot_share):
    """Pilot / holdout split by panel unit when the card has one, else by row."""
    unit = card.get("panel_unit") if isinstance(card, dict) else None
    if unit and unit in df:
        ids = np.asarray(sorted(df[unit].unique(), key=str), dtype=object)
        perm = rng.permutation(len(ids))
        k = max(1, min(len(ids) - 1, int(round(pilot_share * len(ids)))))
        pilot_ids = set(ids[perm[:k]].tolist())
        return df[unit].isin(pilot_ids).to_numpy()
    n = len(df)
    perm = rng.permutation(n)
    k = max(1, min(n - 1, int(round(pilot_share * n))))
    m = np.zeros(n, dtype=bool); m[perm[:k]] = True
    return m


class SplitSample(Procedure):
    """Two stages, after the phase II / phase III structure of a drug trial.

    Stage 1 walks the grid with `inner` (any procedure here) on a pilot share
    of the units and picks a specification. If `continue_at` is set, the
    project continues only when the pilot's chosen p is below it; otherwise
    nothing is reported (the abandoned project) and the null replay counts
    that draw as "did not report". Stage 2 reports the chosen specification:

        stage='holdout'  estimated on the held-out units only. The search was
                         free and the reported test is valid: this is the
                         split-sample immunisation of 07-phack-immunization,
                         and its false-positive rate should be alpha.
        stage='pooled'   estimated on all units. The pilot's favourable draw
                         is inside the reported statistic. This is what
                         "we explored, then confirmed on the full sample" does.
        stage='pilot'    the pilot estimate itself, reported as if confirmatory.

    The ledger rows are always the full-data fits of the specifications the
    pilot visited (so the pooled numbers are visible for every one), with
    `p_pilot` / `coef_pilot` alongside; the reported row carries the
    stage's own estimate.
    """
    name = "split_sample"

    def __init__(self, inner="exhaustive", pilot_share=0.5, stage="pooled", continue_at=None,
                 start="first", report="best", budget=None, stop_at_alpha=None, order="card",
                 max_rounds=None, patience=None):
        if stage not in ("holdout", "pooled", "pilot"):
            raise KeyError(f"stage must be 'holdout', 'pooled' or 'pilot', not {stage!r}")
        if inner == "split_sample":
            raise ValueError("split_sample cannot nest itself")
        self.inner, self.pilot_share, self.stage = inner, float(pilot_share), stage
        self.continue_at = None if continue_at is None else float(continue_at)
        self.start, self.report, self.budget = start, report, budget
        self.stop_at_alpha, self.order, self.max_rounds, self.patience = stop_at_alpha, order, max_rounds, patience

    def params(self):
        return {"inner": self.inner, "pilot_share": self.pilot_share, "stage": self.stage,
                "continue_at": self.continue_at, "start": self.start, "report": self.report,
                "budget": self.budget, "stop_at_alpha": self.stop_at_alpha, "order": self.order,
                "max_rounds": self.max_rounds, "patience": self.patience}

    def _inner(self):
        return make(self.inner, start=self.start, report=self.report, budget=self.budget,
                    stop_at_alpha=self.stop_at_alpha, order=self.order,
                    max_rounds=self.max_rounds, patience=self.patience)

    def walk(self, specs, fit, rng, alpha=0.05, direction=None):
        from . import search                      # local import: search imports this module
        df, card = getattr(fit, "df", None), getattr(fit, "card", None)
        if df is None or card is None:
            raise ValueError("split_sample needs a fitter made by search.make_fitter (it carries df and card)")
        pilot = _split_mask(df, card, rng, self.pilot_share)
        fit_pilot = search.make_fitter(df[pilot].reset_index(drop=True), card)
        inner = self._inner()
        w = inner.walk(specs, fit_pilot, rng, alpha=alpha, direction=direction)
        stage_results = {}
        for s in w.visited:
            r = fit_pilot(s)
            stage_results[s.key()] = {"p_pilot": r.get("p", np.nan), "coef_pilot": r.get("coef", np.nan),
                                      "n_pilot": r.get("n", 0)}
        note = {"stage": "pilot", "inner": inner.name, "inner_stopped": w.stopped,
                "n_pilot_rows": int(pilot.sum()), "n_holdout_rows": int((~pilot).sum()),
                "pilot_share": self.pilot_share}
        if w.reported is None:
            return Walk(w.visited, None, "pilot search reported nothing", [note], None, stage_results)
        p_pilot = _objective(fit_pilot(w.reported), direction)
        note["pilot_p"] = float(p_pilot)
        if self.continue_at is not None and not (p_pilot < self.continue_at):
            note["continued"] = False
            return Walk(w.visited, None,
                        f"pilot p = {p_pilot:.3g} not below continue_at = {self.continue_at}; project abandoned",
                        [note], None, stage_results)
        note["continued"] = True
        if self.stage == "holdout":
            fit_hold = search.make_fitter(df[~pilot].reset_index(drop=True), card)
            override = dict(fit_hold(w.reported))
        elif self.stage == "pilot":
            override = dict(fit_pilot(w.reported))
        else:
            override = None
        note["reported_stage"] = self.stage
        why = f"{self.stage} estimate of the pilot's choice after {len(w.visited)} pilot specs"
        return Walk(w.visited, w.reported, why, [note], override, stage_results)


PROCEDURES = {
    "exhaustive": Exhaustive,
    "first_significant": FirstSignificant,
    "random": RandomBudget,
    "greedy": GreedyCoordinate,
    "hill_climb": HillClimb,
    "split_sample": SplitSample,
}


def make(name, **params) -> Procedure:
    if name not in PROCEDURES:
        raise KeyError(f"unknown procedure {name!r}; known: {sorted(PROCEDURES)}")
    cls = PROCEDURES[name]
    import inspect
    allowed = set(inspect.signature(cls.__init__).parameters) - {"self"}
    return cls(**{k: v for k, v in params.items() if k in allowed and v is not None})
