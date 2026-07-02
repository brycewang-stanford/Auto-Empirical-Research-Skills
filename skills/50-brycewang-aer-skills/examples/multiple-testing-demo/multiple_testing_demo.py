#!/usr/bin/env python3
"""Multiple-testing demo: why testing many outcomes needs FWER control.

A runnable companion to docs/methods-reference.md section 6 ("Inference and
sensitivity", the FWER/FDR row) and the aer-identification skill's RCT advice
("multiple-hypothesis correction if more than one primary outcome"). It makes
the point every referee of a many-outcome paper raises: if you test K outcomes
and call the paper a success when *any* one is significant at 5%, your
family-wise error rate (FWER) is far above 5%. A family-wise correction
(Bonferroni, or the step-down Holm 1979 that is never less powerful) pulls it
back to nominal.

The script demonstrates this with a KNOWN data-generating process (a two-group
comparison on K outcomes):

  1. SIZE. With every outcome a true null, the naive "any outcome significant"
     rule rejects far more than 5% of the time. Bonferroni and Holm hold the
     FWER at its nominal level.
  2. POWER. With one outcome carrying a real effect and the rest null, the
     correction still detects the true effect often, while keeping the
     false-positive rate on the null outcomes controlled -- so the correction
     is not merely throwing away discoveries.

The script asserts the size and power results and exits non-zero if the claim
fails to reproduce, so it doubles as a regression test of the skill stack's
multiple-testing advice.

Run:  python3 multiple_testing_demo.py
Deps: numpy, scipy, matplotlib
      (all pinned in ../../templates/python/requirements.txt)

References: Bonferroni; Holm (1979) step-down; Romano-Wolf (2005) resampling
FWER control; Benjamini-Hochberg (1995) for FDR. See
../../docs/methods-reference.md section 6 for the per-stack tooling, and
../../skills/aer-identification/SKILL.md for when a referee will demand it.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEED = 20260101
N = 400                  # units
N_TREAT = 200            # treated units (rest control)
K = 10                   # outcomes tested
SIZE_REPS = 2000         # Monte Carlo panels for the size study
POWER_REPS = 2000        # Monte Carlo panels for the power study
DELTA = 0.4              # true effect on outcome 0 in the power study
ALPHA = 0.05             # nominal family-wise level
OUT = Path(__file__).resolve().parent / "output"

_D = (np.arange(N) < N_TREAT).astype(float)     # fixed group assignment
_DF = N - 2


def outcome_pvalues(Y: np.ndarray) -> np.ndarray:
    """Two-sided pooled-variance two-group t-test p-value for each outcome."""
    yt = Y[_D == 1]
    yc = Y[_D == 0]
    mt, mc = yt.mean(0), yc.mean(0)
    ss = ((yt - mt) ** 2).sum(0) + ((yc - mc) ** 2).sum(0)
    s2 = ss / _DF
    se = np.sqrt(s2 * (1.0 / N_TREAT + 1.0 / (N - N_TREAT)))
    t = (mt - mc) / se
    return 2.0 * stats.t.sf(np.abs(t), _DF)


def holm_reject(pvals: np.ndarray, alpha: float = ALPHA) -> np.ndarray:
    """Holm (1979) step-down rejections; returns a boolean mask over outcomes."""
    k = len(pvals)
    order = np.argsort(pvals)
    reject = np.zeros(k, dtype=bool)
    for step, idx in enumerate(order):
        if pvals[idx] <= alpha / (k - step):
            reject[idx] = True
        else:
            break                          # step-down stops at the first failure
    return reject


def _panel(rng: np.random.Generator, delta_outcome0: float) -> np.ndarray:
    Y = rng.normal(size=(N, K))
    Y[_D == 1, 0] += delta_outcome0        # effect only on outcome 0
    return Y


def run_size(rng: np.random.Generator) -> dict:
    naive = bonf = holm = 0
    for _ in range(SIZE_REPS):
        p = outcome_pvalues(_panel(rng, 0.0))
        naive += int((p < ALPHA).any())
        bonf += int(p.min() < ALPHA / K)
        holm += int(holm_reject(p).any())
    return {"naive": naive / SIZE_REPS, "bonferroni": bonf / SIZE_REPS,
            "holm": holm / SIZE_REPS}


def run_power(rng: np.random.Generator) -> dict:
    naive_det = bonf_det = holm_det = 0
    bonf_fwer_null = holm_fwer_null = 0
    for _ in range(POWER_REPS):
        p = outcome_pvalues(_panel(rng, DELTA))
        # detection of the true effect (outcome 0)
        naive_det += int(p[0] < ALPHA)
        bonf_det += int(p[0] < ALPHA / K)
        holm_det += int(holm_reject(p)[0])
        # false positives among the K-1 true-null outcomes
        bonf_rej = p < ALPHA / K
        holm_rej = holm_reject(p)
        bonf_fwer_null += int(bonf_rej[1:].any())
        holm_fwer_null += int(holm_rej[1:].any())
    n = POWER_REPS
    return {"naive_detect": naive_det / n, "bonf_detect": bonf_det / n,
            "holm_detect": holm_det / n, "bonf_fwer_null": bonf_fwer_null / n,
            "holm_fwer_null": holm_fwer_null / n}


def make_figure(size: dict, power: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2))

    methods = ["naive\n(any sig.)", "Bonferroni", "Holm"]
    fwer = [100 * size["naive"], 100 * size["bonferroni"], 100 * size["holm"]]
    colors = ["firebrick", "black", "0.45"]
    ax1.bar(methods, fwer, color=colors)
    ax1.axhline(100 * ALPHA, linestyle="--", color="grey",
                label=f"nominal {int(100 * ALPHA)}%")
    ax1.set_ylabel("Family-wise error rate (%)")
    ax1.set_title(f"Size: K={K} true nulls")
    ax1.legend(frameon=False)

    det = [100 * power["naive_detect"], 100 * power["bonf_detect"],
           100 * power["holm_detect"]]
    ax2.bar(methods, det, color=colors)
    ax2.set_ylabel("Detection rate of the true effect (%)")
    ax2.set_title(f"Power: one real effect (delta={DELTA})")

    fig.tight_layout()
    pdf = OUT / "multiple_testing.pdf"
    fig.savefig(pdf)
    fig.savefig(OUT / "multiple_testing.png", dpi=150)
    plt.close(fig)
    return pdf


def main() -> int:
    rng = np.random.default_rng(SEED)
    size = run_size(rng)
    power = run_power(rng)

    print("=" * 70)
    print("Multiple testing: family-wise error control across many outcomes")
    print(f"  units N={N} ({N_TREAT} treated)  outcomes K={K}  seed={SEED}")
    print(f"  nominal family-wise level alpha={ALPHA}")
    print("=" * 70)
    print(f"SIZE study ({K} true nulls, family-wise error rate):")
    print(f"  naive 'any outcome significant' = {size['naive']:.3f}"
          f"   (should blow past {ALPHA})")
    print(f"  Bonferroni                      = {size['bonferroni']:.3f}"
          f"   (should be <= {ALPHA})")
    print(f"  Holm step-down                  = {size['holm']:.3f}"
          f"   (should be <= {ALPHA})")
    print()
    print(f"POWER study (one real effect delta={DELTA} on outcome 0):")
    print(f"  detect true effect, naive       = {power['naive_detect']:.3f}")
    print(f"  detect true effect, Bonferroni  = {power['bonf_detect']:.3f}")
    print(f"  detect true effect, Holm        = {power['holm_detect']:.3f}")
    print(f"  false positive on the nulls, Holm = {power['holm_fwer_null']:.3f}"
          f"   (stays controlled)")

    pdf = make_figure(size, power)
    print(f"\nFigure written to {pdf.relative_to(pdf.parents[2])}")

    # ---- assertions: the demo is also a test -------------------------
    assert size["naive"] > 0.25, (
        "testing K outcomes uncorrected should inflate the family-wise error")
    assert size["bonferroni"] <= 0.06, (
        f"Bonferroni should hold FWER <= {ALPHA}, got {size['bonferroni']:.3f}")
    assert size["holm"] <= 0.06, (
        f"Holm should hold FWER <= {ALPHA}, got {size['holm']:.3f}")
    assert power["holm_detect"] >= power["bonf_detect"], (
        "Holm step-down should never detect less often than Bonferroni")
    assert power["holm_detect"] > 0.50, (
        "the correction should retain power against a clear real effect")
    assert power["holm_fwer_null"] <= 0.06, (
        "false positives on the null outcomes should stay controlled under Holm")
    print("\nAll assertions passed: uncorrected multiple testing inflates the "
          "family-wise\nerror; Bonferroni and Holm control it while retaining "
          "power on a real effect.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
