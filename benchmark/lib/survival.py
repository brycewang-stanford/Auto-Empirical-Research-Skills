#!/usr/bin/env python3
"""Pure-stdlib survival-analysis (Kaplan-Meier) computations.

Deterministic time-to-event data for a treated and a control group, with
right-censoring that is independent of the latent event time. The latent event
time ships as a column the estimators never read, so the true survival past the
horizon is known. A Kaplan-Meier estimator that handles censoring recovers the
true survival difference, while a naive estimator that treats censored
observations as failures underestimates survival and is biased.
"""

from __future__ import annotations

import csv
from pathlib import Path

PERIODS = 6
HORIZON = 4
BEYOND = PERIODS + 1  # latent event time for units that never fail in-window
N_PER_GROUP = 80
# Number that FAIL at each period (1..HORIZON) per group; the rest survive past
# the horizon. Control fails fast (survival ~0.30); treated slowly (~0.65).
FAILS = {
    0: {1: 20, 2: 16, 3: 12, 4: 8},   # control: 56 fail by H, 24 survive -> 0.30
    1: {1: 10, 2: 8, 3: 6, 4: 4},     # treated: 28 fail by H, 52 survive -> 0.65
}
CENSOR_AT = 2          # units selected for censoring drop out at this period
CENSOR_EVERY = 5       # every Nth unit (deterministic, spread across event times)


def _latent_event_times(group: int) -> list[int]:
    """Multiset of latent event times for the group, interleaved deterministically
    so that the censoring selection is independent of the event time."""
    times: list[int] = []
    for period in range(1, HORIZON + 1):
        times += [period] * FAILS[group][period]
    times += [BEYOND] * (N_PER_GROUP - len(times))
    # Deterministic interleave: stable-sort indices by (i * 7) % N to spread
    # event times across positions without randomness.
    order = sorted(range(N_PER_GROUP), key=lambda i: (i * 7) % N_PER_GROUP)
    return [times[order[i]] for i in range(N_PER_GROUP)]


def generate() -> list[dict]:
    rows: list[dict] = []
    uid = 0
    for group in (0, 1):
        events = _latent_event_times(group)
        for pos, t_event in enumerate(events):
            uid += 1
            censor = CENSOR_AT if (pos % CENSOR_EVERY == 4) else BEYOND + 1
            observed = min(t_event, censor)
            event_flag = 1 if t_event <= censor else 0
            rows.append({
                "id": uid,
                "treat": group,
                "time": observed,
                "event": event_flag,
                "t_event": t_event,  # latent; estimators never read this
            })
    return rows


def write_csv(path: Path) -> None:
    rows = generate()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["id", "treat", "time", "event", "t_event"])
        writer.writeheader()
        writer.writerows(rows)


def load(data_path: Path) -> list[dict]:
    with data_path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(row: dict, key: str) -> float:
    return float(row[key])


def _group(rows: list[dict], group: int) -> list[dict]:
    return [r for r in rows if round(_num(r, "treat")) == group]


def true_survival(rows: list[dict], group: int) -> float:
    """Latent survival past the horizon, from the unread t_event column."""
    g = _group(rows, group)
    survived = sum(1 for r in g if _num(r, "t_event") > HORIZON)
    return survived / len(g)


def km_survival(rows: list[dict], group: int) -> float:
    """Kaplan-Meier survival past the horizon (handles censoring correctly)."""
    g = _group(rows, group)
    n = len(g)
    surv = 1.0
    at_risk = n
    for period in range(1, HORIZON + 1):
        deaths = sum(
            1 for r in g if int(_num(r, "time")) == period and round(_num(r, "event")) == 1
        )
        if at_risk > 0:
            surv *= (1 - deaths / at_risk)
        leaving = sum(1 for r in g if int(_num(r, "time")) == period)
        at_risk -= leaving
    return surv


def naive_survival(rows: list[dict], group: int) -> float:
    """Naive survival: count anyone whose observed time does not exceed the horizon
    as a failure, ignoring censoring -> underestimates survival."""
    g = _group(rows, group)
    survived = sum(1 for r in g if int(_num(r, "time")) > HORIZON)
    return survived / len(g)


def true_diff(rows: list[dict]) -> float:
    return true_survival(rows, 1) - true_survival(rows, 0)


def km_diff(rows: list[dict]) -> float:
    return km_survival(rows, 1) - km_survival(rows, 0)


def naive_diff(rows: list[dict]) -> float:
    return naive_survival(rows, 1) - naive_survival(rows, 0)


if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[1] / "data" / "sim-survival.csv"
    write_csv(data_path)
    print(f"Wrote {data_path}")
