#!/usr/bin/env python3
"""Shift-share demo: why inference is at the shock level, not the region level.

A runnable companion to docs/methods-reference.md section 3 ("Shift-share /
Bartik") and the aer-identification skill. It makes the single point that
Adao-Kolesar-Morales (2019) and Borusyak-Hull-Jaravel (2022) insist on:
because every region's Bartik regressor is built from the SAME industry
shocks, the regional observations are not independent. Conventional
heteroskedasticity-robust (or region-clustered) standard errors treat the R
regions as R independent draws and are therefore far too small -- the
effective number of observations is the number of SHOCKS, not regions.

The script demonstrates this with a KNOWN data-generating process where the
true coefficient is zero and a shared industry-shock structure couples the
regional residuals:

  1. SIZE. Conventional region-level robust inference rejects a TRUE null far
     more than 5% of the time. Shock-level randomization inference (re-drawing
     the industry shocks, holding shares and outcomes fixed -- a valid Fisher
     randomization test) keeps its nominal 5% size.
  2. POWER. With a real effect, shock-level randomization inference still
     rejects often, so the fix is not merely conservative.

The script asserts the size and power results and exits non-zero if the claim
fails to reproduce, so it doubles as a regression test of the skill stack's
shift-share advice.

Run:  python3 shift_share_demo.py
Deps: numpy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References (keys in ../../references.bib): adao_kolesar_morales_2019,
borusyak_hull_jaravel_2022, goldsmithpinkham_sorkin_swift_2020.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEED = 20260101
R = 300                  # regions
N = 20                   # industries (= number of shocks: the real n)
CONC = 0.35              # Dirichlet concentration -> concentrated exposure
SIGMA_ETA = 1.0          # industry-level residual component (couples regions)
SIGMA_NU = 0.5           # idiosyncratic region residual
N_RAND = 400             # shock re-draws per randomization test
SIZE_REPS = 300          # Monte Carlo panels for the size study
POWER_REPS = 200         # Monte Carlo panels for the power study
DELTA = 1.00             # true effect for the power study
ALPHA = 0.05             # nominal level
OUT = Path(__file__).resolve().parent / "output"


def draw_shares(rng: np.random.Generator, r: int = R, n: int = N) -> np.ndarray:
    """Region x industry exposure shares; each row is on the simplex."""
    return rng.dirichlet(np.full(n, CONC), size=r)


def bartik(shares: np.ndarray, shocks: np.ndarray) -> np.ndarray:
    """Bartik regressor B_r = sum_n share_rn * shock_n."""
    return shares @ shocks


def ols_beta(x: np.ndarray, y: np.ndarray) -> tuple[float, np.ndarray]:
    """Univariate OLS slope (with intercept) and residuals."""
    xc = x - x.mean()
    yc = y - y.mean()
    sxx = float(xc @ xc)
    beta = float(xc @ yc) / sxx
    resid = yc - beta * xc
    return beta, resid


def hc1_t(x: np.ndarray, y: np.ndarray) -> float:
    """Conventional region-level HC1-robust t-statistic for H0: beta = 0."""
    beta, resid = ols_beta(x, y)
    xc = x - x.mean()
    sxx = float(xc @ xc)
    # HC1 sandwich variance, treating the R regions as independent units
    meat = float((xc ** 2) @ (resid ** 2))
    var = meat / sxx ** 2 * (len(x) / (len(x) - 2))
    return beta / np.sqrt(var)


def shock_level_p(shares: np.ndarray, y: np.ndarray, beta_obs: float,
                  rng: np.random.Generator, n_rand: int = N_RAND) -> float:
    """Shock-level randomization p-value for H0: y unrelated to the shocks.

    Hold shares and outcomes fixed; re-draw the N industry shocks from their
    distribution and recompute the slope. Because the observed shocks and the
    re-drawn shocks are identically distributed and y is fixed, the observed
    slope is exchangeable with the re-draws under the null, so the test has
    exact size. This is the design-based, shock-level reference distribution
    that region-level standard errors fail to reproduce.
    """
    yc = y - y.mean()
    G = rng.normal(size=(N, n_rand))               # N shocks x draws
    B = shares @ G                                  # R x draws
    Bc = B - B.mean(axis=0, keepdims=True)
    betas = (Bc * yc[:, None]).sum(axis=0) / (Bc ** 2).sum(axis=0)
    return float((np.abs(betas) >= np.abs(beta_obs)).mean())


def one_panel(rng: np.random.Generator, delta: float) -> tuple[float, float]:
    """Generate one shift-share panel; return (HC1 t-stat, shock-level p)."""
    shares = draw_shares(rng)
    eta = rng.normal(scale=SIGMA_ETA, size=N)       # industry-level residual
    nu = rng.normal(scale=SIGMA_NU, size=R)         # idiosyncratic residual
    eps = shares @ eta + nu                         # coupled regional residual
    shocks = rng.normal(size=N)                     # realized industry shocks
    B = bartik(shares, shocks)
    y = delta * B + eps
    beta_obs, _ = ols_beta(B, y)
    t = hc1_t(B, y)
    p = shock_level_p(shares, y, beta_obs, rng)
    return t, p


def run_study(reps: int, delta: float, rng: np.random.Generator) -> dict:
    hc1_rej = shock_rej = 0
    for _ in range(reps):
        t, p = one_panel(rng, delta)
        hc1_rej += int(abs(t) > 1.96)
        shock_rej += int(p <= ALPHA)
    return {"hc1_reject_rate": hc1_rej / reps,
            "shock_reject_rate": shock_rej / reps}


def make_figure(size: dict, power: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    labels = ["Size\n(true effect = 0)", f"Power\n(true effect = {DELTA})"]
    x = np.arange(len(labels))
    width = 0.38
    hc1 = [100 * size["hc1_reject_rate"], 100 * power["hc1_reject_rate"]]
    shock = [100 * size["shock_reject_rate"], 100 * power["shock_reject_rate"]]
    ax.bar(x - width / 2, hc1, width, color="firebrick",
           label="Region-level HC1 t-test")
    ax.bar(x + width / 2, shock, width, color="black",
           label="Shock-level randomization")
    ax.axhline(100 * ALPHA, linestyle="--", color="grey",
               label=f"nominal {int(100 * ALPHA)}%")
    ax.set_ylabel("Rejection rate (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_title("Shift-share: region-level SEs over-reject; shock-level is honest")
    ax.legend(frameon=False)
    fig.tight_layout()
    pdf = OUT / "shift_share.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "shift_share.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)
    size = run_study(SIZE_REPS, delta=0.0, rng=rng)
    power = run_study(POWER_REPS, delta=DELTA, rng=rng)

    print("=" * 70)
    print("Shift-share: shock-level vs region-level inference")
    print(f"  regions R={R}  industries (shocks) N={N}  seed={SEED}")
    print(f"  nominal level alpha={ALPHA}  randomization draws={N_RAND}")
    print("=" * 70)
    print("SIZE study (true effect = 0):")
    print(f"  region-level HC1 t-test reject rate = {size['hc1_reject_rate']:.3f}"
          f"   (should blow past {ALPHA})")
    print(f"  shock-level randomization reject     = {size['shock_reject_rate']:.3f}"
          f"   (should be ~{ALPHA})")
    print()
    print(f"POWER study (true effect = {DELTA}):")
    print(f"  region-level HC1 t-test reject rate = {power['hc1_reject_rate']:.3f}")
    print(f"  shock-level randomization reject     = {power['shock_reject_rate']:.3f}"
          f"   (should be high)")

    pdf = make_figure(size, power)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    assert size["hc1_reject_rate"] > 0.15, (
        "region-level HC1 should over-reject under shared industry shocks")
    assert size["shock_reject_rate"] <= 0.10, (
        f"shock-level randomization should hold ~{ALPHA} size, "
        f"got {size['shock_reject_rate']:.3f}")
    assert size["hc1_reject_rate"] > 2 * size["shock_reject_rate"], (
        "region-level inference should reject far more often than shock-level")
    assert power["shock_reject_rate"] > 0.50, (
        "shock-level randomization should still have power against a real effect")
    print("\nAll assertions passed: region-level SEs over-reject; shock-level "
          "randomization\nholds size and keeps power. Inference belongs at the "
          "shock level.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
