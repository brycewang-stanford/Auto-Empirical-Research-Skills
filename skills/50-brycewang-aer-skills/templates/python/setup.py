"""
setup.py
Paths, seed, and shared utilities for the AER-compliant Python pipeline.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np

# ---- Paths ---------------------------------------------------------
ROOT         = Path(__file__).resolve().parent
DATA         = ROOT / "data"
RAW          = DATA / "raw"
INTERMEDIATE = DATA / "intermediate"
OUTPUT       = ROOT / "output"
TABLES       = OUTPUT / "tables"
FIGURES      = OUTPUT / "figures"
LOGS         = ROOT / "logs"

for d in (RAW, INTERMEDIATE, TABLES, FIGURES, LOGS):
    d.mkdir(parents=True, exist_ok=True)

# ---- Reproducibility -----------------------------------------------
SEED = 20260101
RNG  = np.random.default_rng(SEED)   # new-style RNG; pass to any stochastic call

# ---- Plot defaults -------------------------------------------------
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family":     "Helvetica",
    "font.size":       10,
    "axes.titlesize":  11,
    "axes.labelsize":  10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi":      150,
    "savefig.dpi":     300,
    "savefig.bbox":    "tight",
    "savefig.format":  "pdf",
    "pdf.fonttype":    42,            # editable text in PDF
    "axes.grid":       True,
    "grid.alpha":      0.25,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})
