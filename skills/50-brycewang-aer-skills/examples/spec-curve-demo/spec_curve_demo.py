#!/usr/bin/env python3
"""Specification-curve demo: why a single "preferred" spec can mislead.

A runnable companion to docs/methods-reference.md section 6 (the
specification-curve row) and the aer-robustness / aer-identification skills. It
makes the Simonsohn-Simmons-Nelson (2020) point: when a dataset admits many
defensible specifications, reporting the one that "works" is specification
search -- it inflates false positives across a correlated family of tests. The
honest summary is the whole specification curve plus a JOINT permutation test
under the sharp null, not a single starred coefficient.

The script demonstrates this with a KNOWN data-generating process. The
treatment is randomly assigned (so the sharp null is exchangeable and the
permutation test is exact), and the researcher's degrees of freedom are which
subset of K control variables to include -- all 2^K specifications.

  1. SIZE. With a true effect of zero, the naive rule "report a spec where the
     effect is significant" rejects far more than 5% of the time, because the
     2^K specs are a correlated multiple-testing family. The specification-curve
     permutation test (re-randomizing treatment, recomputing the whole curve,
     summarized by the median t across specs) keeps its nominal 5% size.
  2. POWER. With a real effect, the permutation test rejects often, so the
     joint test is not merely conservative.

The script asserts the size and power results and exits non-zero if the claim
fails to reproduce, so it doubles as a regression test of the skill stack's
specification-curve advice.

Run:  python3 spec_curve_demo.py
Deps: numpy, scipy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References (keys in ../../references.bib): simonsohn_simmons_nelson_2020
("Specification curve analysis"), romano_wolf_2005 (the permutation/resampling
joint test). See ../../docs/methods-reference.md section 6 for the per-stack
tooling (speccurve, specr) and ../../skills/aer-identification/SKILL.md for the
design context.
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _aer_numeric_check import numeric_check  # noqa: E402

SEED = 20260101
N = 200                  # units
K = 4                    # candidate control variables -> 2^K specifications
N_PERM = 300             # permutations per specification-curve test
SIZE_REPS = 300          # Monte Carlo panels for the size study
POWER_REPS = 200         # Monte Carlo panels for the power study
DELTA = 0.45             # true effect for the power study
ALPHA = 0.05             # nominal level (per-spec and family-wise)
OUT = Path(__file__).resolve().parent / "output"

# every subset of the K controls (including the empty set) is one specification
_SPECS = [list(c) for r in range(K + 1) for c in combinations(range(K), r)]


def _residual_maker(Z: np.ndarray) -> np.ndarray:
    """M = I - Z (Z'Z)^-1 Z', the projector onto the orthogonal complement."""
    ZtZ_inv = np.linalg.inv(Z.T @ Z)
    return np.eye(Z.shape[0]) - Z @ ZtZ_inv @ Z.T


def spec_curve_summary(D_cols: np.ndarray, Y: np.ndarray,
                       X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """For each treatment column, the count of significant specs and median t.

    For every specification S, partial out [1, X_S] from D and Y (Frisch-Waugh)
    and read the treatment coefficient's t-test. The naive p-hacker watches the
    count of significant specs; the honest joint test summarizes the whole curve
    by its median t (a continuous Simonsohn-Simmons-Nelson statistic).
    """
    n, b = D_cols.shape
    counts = np.zeros(b)
    t_stack = np.empty((len(_SPECS), b))
    ones = np.ones((n, 1))
    for si, cols in enumerate(_SPECS):
        Z = ones if not cols else np.hstack([ones, X[:, cols]])
        M = _residual_maker(Z)
        Yt = M @ Y                                   # residualized outcome
        Dt = M @ D_cols                              # residualized treatment(s)
        dtd = (Dt ** 2).sum(0)                       # (b,)
        beta = (Dt * Yt[:, None]).sum(0) / dtd       # (b,)
        resid = Yt[:, None] - beta[None, :] * Dt
        df = n - (Z.shape[1] + 1)
        ssr = (resid ** 2).sum(0)
        se = np.sqrt(ssr / df / dtd)
        t = beta / se
        counts += (2.0 * stats.t.sf(np.abs(t), df) < ALPHA).astype(float)
        t_stack[si] = t
    return counts, np.median(t_stack, axis=0)


def perm_pvalue(D: np.ndarray, Y: np.ndarray, X: np.ndarray,
                rng: np.random.Generator) -> float:
    """Specification-curve permutation p-value under the sharp null.

    The statistic is the median t across the whole curve. The null distribution
    re-randomizes the treatment labels and recomputes the curve; p is the share
    of permutations whose |median t| is at least the observed |median t|.
    """
    _, mt_obs = spec_curve_summary(D[:, None], Y, X)
    mt_obs = float(mt_obs[0])
    Dperm = np.column_stack([rng.permutation(D) for _ in range(N_PERM)])
    _, mt_perm = spec_curve_summary(Dperm, Y, X)
    return float((np.abs(mt_perm) >= abs(mt_obs)).mean())


def _panel(rng: np.random.Generator, delta: float) -> tuple[np.ndarray, ...]:
    # correlated controls; randomized treatment (independent of controls)
    A = rng.normal(size=(K, K))
    cov = A @ A.T / K + np.eye(K)
    X = rng.multivariate_normal(np.zeros(K), cov, size=N)
    D = (rng.random(N) < 0.5).astype(float)
    b = rng.normal(scale=0.7, size=K)
    Y = delta * D + X @ b + rng.normal(size=N)
    return D, Y, X


def naive_any_significant(D: np.ndarray, Y: np.ndarray, X: np.ndarray) -> bool:
    """The p-hacker's rule: is ANY single specification significant?"""
    counts, _ = spec_curve_summary(D[:, None], Y, X)
    return counts[0] > 0


def run_study(reps: int, delta: float, rng: np.random.Generator) -> dict:
    naive = perm = 0
    for _ in range(reps):
        D, Y, X = _panel(rng, delta)
        naive += int(naive_any_significant(D, Y, X))
        perm += int(perm_pvalue(D, Y, X, rng) <= ALPHA)
    return {"naive_reject": naive / reps, "perm_reject": perm / reps}


def make_figure(rng: np.random.Generator) -> Path:
    """Iconic specification curve for one dataset with a real effect."""
    D, Y, X = _panel(rng, DELTA)
    ones = np.ones((N, 1))
    betas, los, his = [], [], []
    for cols in _SPECS:
        Z = ones if not cols else np.hstack([ones, X[:, cols]])
        M = _residual_maker(Z)
        Yt, Dt = M @ Y, M @ D
        dtd = float(Dt @ Dt)
        beta = float(Dt @ Yt) / dtd
        df = N - (Z.shape[1] + 1)
        ssr = float(((Yt - beta * Dt) ** 2).sum())
        se = np.sqrt(ssr / df / dtd)
        crit = stats.t.ppf(1 - ALPHA / 2, df)
        betas.append(beta); los.append(beta - crit * se); his.append(beta + crit * se)
    order = np.argsort(betas)
    betas = np.array(betas)[order]; los = np.array(los)[order]; his = np.array(his)[order]
    sig = los > 0
    x = np.arange(len(betas))

    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.vlines(x[~sig], los[~sig], his[~sig], color="0.7", linewidth=1.2)
    ax.vlines(x[sig], los[sig], his[sig], color="firebrick", linewidth=1.2)
    ax.plot(x, betas, "o", color="black", markersize=3)
    ax.axhline(0, color="grey", linestyle="--", linewidth=0.8)
    ax.axhline(DELTA, color="steelblue", linestyle=":", linewidth=1.0,
               label=f"true effect = {DELTA}")
    ax.set_xlabel("Specification (sorted by estimate)")
    ax.set_ylabel("Treatment effect estimate")
    ax.set_title(f"Specification curve ({len(_SPECS)} specs): each control subset")
    ax.legend(frameon=False)
    fig.tight_layout()
    pdf = OUT / "spec_curve.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "spec_curve.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)
    size = run_study(SIZE_REPS, delta=0.0, rng=rng)
    power = run_study(POWER_REPS, delta=DELTA, rng=rng)
    pdf = make_figure(np.random.default_rng(SEED + 99))

    print("=" * 70)
    print("Specification curve: joint inference beats a single 'preferred' spec")
    print(f"  units N={N}  controls K={K}  specs=2^K={len(_SPECS)}  seed={SEED}")
    print(f"  nominal level alpha={ALPHA}  permutations={N_PERM}")
    print("=" * 70)
    print("SIZE study (true effect = 0):")
    print(f"  naive 'any spec significant' reject = {size['naive_reject']:.3f}"
          f"   (should exceed {ALPHA})")
    print(f"  spec-curve permutation test reject   = {size['perm_reject']:.3f}"
          f"   (should be ~{ALPHA})")
    print()
    print(f"POWER study (true effect = {DELTA}):")
    print(f"  spec-curve permutation test reject   = {power['perm_reject']:.3f}"
          f"   (should be high)")
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    numeric_check("naive any-specification rejection is inflated", size["naive_reject"], lo=0.10)
    numeric_check("permutation test controls size", size["perm_reject"], hi=0.09)
    numeric_check("naive rejects more than the permutation test",
                  size["naive_reject"] - size["perm_reject"], lo=0.0)
    numeric_check("permutation test retains power", power["perm_reject"], lo=0.50)
    print("\nAll assertions passed: specification search inflates false "
          "positives; the\nspecification-curve permutation test holds size and "
          "keeps power.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
