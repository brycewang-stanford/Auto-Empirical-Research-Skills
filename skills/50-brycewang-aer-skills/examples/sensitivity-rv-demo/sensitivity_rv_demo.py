#!/usr/bin/env python3
"""Sensitivity/RV demo: omitted-variable bias reframed as a partial-R^2 budget.

A runnable companion to docs/methods-reference.md and the aer-robustness skill.
It makes the Cinelli and Hazlett (2020) point: coefficient stability under
observed controls does NOT bound omitted-variable bias, and the honest way to
report robustness to an *unobserved* confounder is a partial-R^2 sensitivity
statement, not a hand-wave. Two ingredients summarize how a confounder Z moves a
treatment estimate: how much of the treatment it explains (R^2_{D~Z}) and how
much of the residual outcome it explains (R^2_{Y~Z|D,X}). From those two scalars
the *bias factor* reproduces the confounded estimate exactly, and the
*robustness value* RV reports the single number a referee wants: the partial R^2
(with both treatment and outcome) a confounder must reach to explain the result
away.

This complements the sibling ``oster-ovb-demo``: Oster's delta scales bias by
movement in the coefficient and R^2 as controls are added; Cinelli-Hazlett
instead works directly in the partial-R^2 geometry of a single specification and
needs no assumption about how observed and unobserved confounders relate in
magnitude. Both refuse the fallacy that "the coefficient barely moved" settles
anything.

Every claim is checked by simulation against a known truth. The script asserts,
over a Monte Carlo, that (1) omitting a confounder biases OLS while (2) including
it recovers the truth, that (3) the Cinelli-Hazlett bias factor -- computed from
only the two partial-R^2 scalars -- reproduces the confounded estimate, that
(4) the robustness value equals, to simulation tolerance, the strength of an
equal-partial-R^2 confounder that manufactures a purely spurious effect (true
effect zero), and that (5) a stronger design has a strictly larger robustness
value. It exits non-zero on any failure, so the demo doubles as a regression
test.

Run:  python3 sensitivity_rv_demo.py
Deps: numpy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: cinelli_hazlett_2020 (and oster_2019 for the contrast) in
../../references.bib. See ../../docs/methods-reference.md for the per-stack
tooling (`sensemakr` in R/Stata/Python) and ../../skills/aer-robustness/SKILL.md
for where sensitivity sits in the referee checklist.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")  # headless: write files, never open a window
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _aer_numeric_check import numeric_check  # noqa: E402

SEED = 20260101                       # repository-wide fixed seed
N = 6000                              # sample size per replication
REPS = 200                            # Monte Carlo repetitions
OUT = Path(__file__).resolve().parent / "output"


def ols(y: np.ndarray, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, int]:
    """OLS returning (beta, se, dof) with classical homoskedastic SEs."""
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n, k = X.shape
    dof = n - k
    sigma2 = float(resid @ resid) / dof
    se = np.sqrt(np.diag(sigma2 * np.linalg.inv(X.T @ X)))
    return beta, se, dof


def partial_r2(t: float, dof: int) -> float:
    """Partial R^2 implied by a t-statistic on ``dof`` residual degrees."""
    return t * t / (t * t + dof)


def robustness_value(t: float, dof: int, q: float = 1.0) -> float:
    """Cinelli-Hazlett robustness value: the partial R^2 (with BOTH treatment
    and outcome) a confounder needs to shift the estimate by proportion ``q``.
    Closed form RV_q = 0.5 (sqrt(f^4 + 4 f^2) - f^2) with f = q |t| / sqrt(dof)."""
    f = q * abs(t) / np.sqrt(dof)
    return 0.5 * (np.sqrt(f ** 4 + 4 * f ** 2) - f ** 2)


def bias_factor(r2_dz: float, r2_yz_d: float, dof: int) -> float:
    """Cinelli-Hazlett bias factor in standard-error units: the confounded
    estimate is beta_short -/+ BF * se(beta_short)."""
    return np.sqrt(r2_yz_d * r2_dz / (1.0 - r2_dz)) * np.sqrt(dof)


def _confounded_draw(rng, tau, delta, gamma):
    """One sample of Y = tau D + gamma Z + eY, D = delta Z + eD, with Z the
    confounder to be omitted. Returns short (omit Z) and long (include Z)
    estimates plus the confounder's realized partial R^2 with D and with Y|D."""
    Z = rng.normal(0.0, 1.0, N)
    D = delta * Z + rng.normal(0.0, 1.0, N)
    Y = tau * D + gamma * Z + rng.normal(0.0, 1.0, N)
    one = np.ones(N)
    b_s, se_s, dof_s = ols(Y, np.column_stack([one, D]))       # omit Z
    b_l, se_l, dof_l = ols(Y, np.column_stack([one, D, Z]))    # include Z
    beta_short, se_short, t_short = float(b_s[1]), float(se_s[1]), float(b_s[1] / se_s[1])
    beta_long = float(b_l[1])
    # realized partial R^2 of Z with treatment and with the outcome given D
    b_dz, se_dz, dof_dz = ols(D, np.column_stack([one, Z]))
    r2_dz = partial_r2(float(b_dz[1] / se_dz[1]), dof_dz)
    r2_yz_d = partial_r2(float(b_l[2] / se_l[2]), dof_l)
    return {"beta_short": beta_short, "se_short": se_short, "t_short": t_short,
            "dof_short": dof_s, "beta_long": beta_long,
            "r2_dz": r2_dz, "r2_yz_d": r2_yz_d}


def _signal_t(rng, tau, sigma):
    """No confounder: Y = tau D + N(0, sigma). Returns (t, dof) of the reported
    treatment coefficient, isolating how signal strength alone drives the
    robustness value."""
    D = rng.normal(0.0, 1.0, N)
    Y = tau * D + rng.normal(0.0, sigma, N)
    b, se, dof = ols(Y, np.column_stack([np.ones(N), D]))
    return float(b[1] / se[1]), dof


def _spurious_rv(rng, r_star):
    """True effect ZERO; a confounder with equal partial R^2 = r_star with both
    treatment and outcome manufactures a spurious estimate. Analytic scaling:
    delta = sqrt(r/(1-r)), gamma = sqrt(r)/(1-r) hit both partial-R^2 targets.
    Returns the robustness value RV(q=1) of the spurious short regression, which
    should equal r_star."""
    delta = np.sqrt(r_star / (1.0 - r_star))
    gamma = np.sqrt(r_star) / (1.0 - r_star)
    Z = rng.normal(0.0, 1.0, N)
    D = delta * Z + rng.normal(0.0, 1.0, N)
    Y = gamma * Z + rng.normal(0.0, 1.0, N)              # tau = 0
    one = np.ones(N)
    b_s, se_s, dof_s = ols(Y, np.column_stack([one, D]))
    t = float(b_s[1] / se_s[1])
    return robustness_value(t, dof_s)


def main() -> int:
    t0 = time.time()
    rng = np.random.default_rng(SEED)

    TAU = 1.0                          # true treatment effect
    DELTA, GAMMA = 0.8, 1.2            # confounder -> D and -> Y strengths
    R_STAR = 0.30                      # equal-strength spurious confounder

    short, long_, adj = [], [], []
    r2d, r2y = [], []
    for _ in range(REPS):
        d = _confounded_draw(rng, TAU, DELTA, GAMMA)
        bf = bias_factor(d["r2_dz"], d["r2_yz_d"], d["dof_short"])
        beta_adj = d["beta_short"] - np.sign(d["beta_short"]) * bf * d["se_short"]
        short.append(d["beta_short"]); long_.append(d["beta_long"])
        adj.append(beta_adj); r2d.append(d["r2_dz"]); r2y.append(d["r2_yz_d"])
    beta_short = float(np.mean(short)); beta_long = float(np.mean(long_))
    beta_adj = float(np.mean(adj))
    r2_dz = float(np.mean(r2d)); r2_yz_d = float(np.mean(r2y))

    # RV validation: RV of an equal-strength spurious confounder ~ r_star.
    rv_spurious = float(np.mean([_spurious_rv(rng, R_STAR) for _ in range(REPS)]))

    # Robust vs fragile: signal strength alone (no confounder), calibrated so
    # the r=0.30 benchmark confounder overturns the fragile design but not the
    # robust one.
    rv_strong, rv_fragile = [], []
    for _ in range(REPS):
        t_s, dof_s = _signal_t(rng, 0.52, 1.0)                 # strong signal
        t_f, dof_f = _signal_t(rng, 0.045, 1.0)                # weak signal
        rv_strong.append(robustness_value(t_s, dof_s))
        rv_fragile.append(robustness_value(t_f, dof_f))
    rv_strong_m = float(np.mean(rv_strong)); rv_fragile_m = float(np.mean(rv_fragile))

    print("=" * 70)
    print("Cinelli-Hazlett sensitivity: OVB as a partial-R^2 budget")
    print(f"  N={N}  reps={REPS}  seed={SEED}  true effect tau={TAU}")
    print("=" * 70)
    print(f"  Short regression (omits confounder) : beta = {beta_short:.3f}  "
          f"(bias {beta_short - TAU:+.3f})")
    print(f"  Long regression  (includes it)      : beta = {beta_long:.3f}  "
          f"(truth {TAU:.2f})")
    print(f"  Confounder partial R^2: with D = {r2_dz:.3f}, with Y|D = {r2_yz_d:.3f}")
    print(f"  Bias-factor-adjusted short estimate : beta = {beta_adj:.3f}  "
          f"(matches the long estimate)")
    print()
    print(f"  RV of an equal-strength (r={R_STAR}) spurious confounder : "
          f"{rv_spurious:.3f}")
    print(f"    -> the robustness value recovers the confounding strength that")
    print(f"       manufactured a purely spurious effect.")
    print()
    print(f"  Robustness value, strong design  : {rv_strong_m:.3f}  "
          f"(survives an r={R_STAR} confounder)")
    print(f"  Robustness value, fragile design : {rv_fragile_m:.3f}  "
          f"(overturned by an r={R_STAR} confounder)")
    print("    -> a bigger t-statistic buys a larger partial-R^2 cushion.")

    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    labels = ["strong\ndesign", "fragile\ndesign"]
    vals = [rv_strong_m, rv_fragile_m]
    bars = ax.bar(labels, vals, color=["#2b6f39", "#c25a1c"], width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.01, f"RV={v:.2f}",
                ha="center", fontsize=10)
    ax.axhline(R_STAR, color="grey", linestyle="--", linewidth=0.9)
    ax.text(1.35, R_STAR + 0.01, f"benchmark confounder r={R_STAR}",
            ha="right", fontsize=8, color="grey")
    ax.set_ylabel("Robustness value RV$_{q=1}$ (partial $R^2$ to nullify)")
    ax.set_ylim(0, max(vals) * 1.25)
    ax.set_title("A stronger design tolerates a stronger unobserved confounder")
    fig.tight_layout()
    pdf = OUT / "sensitivity_rv.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "sensitivity_rv.png", dpi=150)
    plt.close(fig)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    numeric_check("omitting the confounder biases the short regression",
                  abs(beta_short - TAU), lo=0.3)
    numeric_check("including the confounder recovers the truth",
                  beta_long, target=TAU, tol=0.05)
    numeric_check("Cinelli-Hazlett bias factor reproduces the confounded estimate",
                  abs(beta_adj - beta_long), hi=0.02)
    numeric_check("robustness value equals the equal-strength confounder that "
                  "nullifies a spurious effect",
                  rv_spurious, target=R_STAR, tol=0.02)
    numeric_check("robust design survives the benchmark confounder (RV > 0.30)",
                  rv_strong_m, lo=R_STAR)
    numeric_check("fragile design is overturned by the same benchmark (RV < 0.10)",
                  rv_fragile_m, hi=0.10)
    print(f"\nAll assertions passed in {time.time() - t0:.1f}s: omitted-variable "
          "bias reduces to a\npartial-R^2 budget, and the robustness value "
          "reports how large a confounder would overturn the result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
