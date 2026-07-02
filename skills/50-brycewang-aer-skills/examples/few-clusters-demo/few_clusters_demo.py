#!/usr/bin/env python3
"""Few-clusters demo: why cluster-robust t-tests need the wild bootstrap.

A runnable companion to docs/methods-reference.md section 6 ("Inference and
sensitivity") and the aer-robustness skill. It makes the point that
Cameron-Gelbach-Miller (2008) and MacKinnon-Webb (2017) insist on: with a
small number of clusters and treatment assigned at the cluster level, the
conventional cluster-robust (CRVE) t-test rejects a TRUE null far too often.
The wild cluster bootstrap, imposing the null with cluster-level Rademacher
weights, restores nominal size.

The script demonstrates this with a KNOWN data-generating process (a
cluster random-effects model with the true coefficient set to zero):

  1. SIZE. With few clusters, the CRVE t-test compared against +/-1.96 rejects
     a true null well above 5%. The wild cluster bootstrap keeps its nominal
     size.
  2. POWER. With a real effect, the wild cluster bootstrap still rejects often,
     so the fix is not merely conservative.

The script asserts the size and power results and exits non-zero if the claim
fails to reproduce, so it doubles as a regression test of the skill stack's
few-clusters advice.

Run:  python3 few_clusters_demo.py
Deps: numpy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References (keys in ../../references.bib): cameron_gelbach_miller_2008,
mackinnon_webb_2017.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEED = 20260101
G = 10                   # number of clusters (few)
G_TREATED = 5            # treated clusters (treatment is assigned at cluster level)
N_PER = 30               # observations per cluster
SIGMA_ALPHA = 0.5        # cluster random effect (intra-cluster correlation)
SIGMA_EPS = 1.0          # idiosyncratic error
B_BOOT = 399             # wild-bootstrap re-draws per test
SIZE_REPS = 600          # Monte Carlo panels for the size study
POWER_REPS = 400         # Monte Carlo panels for the power study
DELTA = 1.0              # true effect for the power study
ALPHA = 0.05             # nominal level
OUT = Path(__file__).resolve().parent / "output"

# fixed design: cluster ids and a cluster-level treatment dummy
_G_IDX = np.repeat(np.arange(G), N_PER)
_TREAT_CLUSTER = (np.arange(G) < G_TREATED).astype(float)
_D = _TREAT_CLUSTER[_G_IDX]
_DC = _D - _D.mean()
_SXX = float(_DC @ _DC)
# G x N cluster-sum indicator, for vectorized CRVE scores
_M = (_G_IDX[None, :] == np.arange(G)[:, None]).astype(float)


def _crve_t(y: np.ndarray) -> tuple[float, float]:
    """Slope and cluster-robust t-stat for y on [1, D] (H0: slope = 0)."""
    beta = float(_DC @ (y - y.mean())) / _SXX
    resid = (y - y.mean()) - beta * _DC
    scores = _M @ (_DC * resid)                 # per-cluster score sums
    var = float(scores @ scores) / _SXX ** 2
    return beta, beta / np.sqrt(var)


def _wild_bootstrap_p(y: np.ndarray, t_obs: float,
                      rng: np.random.Generator) -> float:
    """Wild cluster bootstrap p-value (restricted: null imposed).

    Under H0 the restricted fit is the intercept, so the restricted residuals
    are the demeaned outcome. Each bootstrap re-draw multiplies every cluster's
    residuals by an independent Rademacher (+/-1) weight, regenerates the
    outcome, and recomputes the CRVE t-stat -- fully vectorized over draws.
    """
    e = y - y.mean()                            # restricted residuals (H0: slope=0)
    W = rng.choice((-1.0, 1.0), size=(G, B_BOOT))
    Wn = W[_G_IDX]                              # N x B cluster weights
    ystar = Wn * e[:, None]                     # constant intercept drops out
    ystar = ystar - ystar.mean(axis=0, keepdims=True)
    beta_b = (_DC[:, None] * ystar).sum(axis=0) / _SXX        # (B,)
    resid_b = ystar - beta_b[None, :] * _DC[:, None]          # N x B
    scores_b = _M @ (_DC[:, None] * resid_b)                  # G x B
    var_b = (scores_b ** 2).sum(axis=0) / _SXX ** 2
    t_b = beta_b / np.sqrt(var_b)
    return float((np.abs(t_b) >= np.abs(t_obs)).mean())


def _panel(rng: np.random.Generator, delta: float) -> np.ndarray:
    alpha = rng.normal(scale=SIGMA_ALPHA, size=G)[_G_IDX]    # cluster effect
    eps = rng.normal(scale=SIGMA_EPS, size=G * N_PER)
    return delta * _D + alpha + eps


def run_study(reps: int, delta: float, rng: np.random.Generator) -> dict:
    crve_rej = wild_rej = 0
    for _ in range(reps):
        y = _panel(rng, delta)
        _beta, t = _crve_t(y)
        crve_rej += int(abs(t) > 1.96)
        wild_rej += int(_wild_bootstrap_p(y, t, rng) <= ALPHA)
    return {"crve_reject_rate": crve_rej / reps,
            "wild_reject_rate": wild_rej / reps}


def make_figure(size: dict, power: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    labels = ["Size\n(true effect = 0)", f"Power\n(true effect = {DELTA})"]
    x = np.arange(len(labels))
    width = 0.38
    crve = [100 * size["crve_reject_rate"], 100 * power["crve_reject_rate"]]
    wild = [100 * size["wild_reject_rate"], 100 * power["wild_reject_rate"]]
    ax.bar(x - width / 2, crve, width, color="firebrick",
           label="Cluster-robust t-test (|t| > 1.96)")
    ax.bar(x + width / 2, wild, width, color="black",
           label="Wild cluster bootstrap")
    ax.axhline(100 * ALPHA, linestyle="--", color="grey",
               label=f"nominal {int(100 * ALPHA)}%")
    ax.set_ylabel("Rejection rate (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title(f"Few clusters (G={G}): CRVE over-rejects; wild bootstrap is honest")
    ax.legend(frameon=False)
    fig.tight_layout()
    pdf = OUT / "few_clusters.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "few_clusters.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)
    size = run_study(SIZE_REPS, delta=0.0, rng=rng)
    power = run_study(POWER_REPS, delta=DELTA, rng=rng)

    print("=" * 70)
    print("Few clusters: cluster-robust t-test vs wild cluster bootstrap")
    print(f"  clusters G={G} ({G_TREATED} treated)  obs/cluster={N_PER}"
          f"  seed={SEED}")
    print(f"  nominal level alpha={ALPHA}  bootstrap draws={B_BOOT}")
    print("=" * 70)
    print("SIZE study (true effect = 0):")
    print(f"  cluster-robust t-test reject rate = {size['crve_reject_rate']:.3f}"
          f"   (should exceed {ALPHA})")
    print(f"  wild cluster bootstrap reject      = {size['wild_reject_rate']:.3f}"
          f"   (should be ~{ALPHA})")
    print()
    print(f"POWER study (true effect = {DELTA}):")
    print(f"  cluster-robust t-test reject rate = {power['crve_reject_rate']:.3f}")
    print(f"  wild cluster bootstrap reject      = {power['wild_reject_rate']:.3f}"
          f"   (should be high)")

    pdf = make_figure(size, power)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    assert size["crve_reject_rate"] > 0.09, (
        "cluster-robust t-test should over-reject with few clusters")
    assert size["wild_reject_rate"] <= 0.075, (
        f"wild cluster bootstrap should hold ~{ALPHA} size, "
        f"got {size['wild_reject_rate']:.3f}")
    assert size["crve_reject_rate"] > size["wild_reject_rate"], (
        "CRVE should reject a true null more often than the wild bootstrap")
    assert power["wild_reject_rate"] > 0.40, (
        "wild cluster bootstrap should still have power against a real effect")
    print("\nAll assertions passed: with few clusters the cluster-robust t-test "
          "over-rejects,\nwhile the wild cluster bootstrap holds size and keeps "
          "power.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
