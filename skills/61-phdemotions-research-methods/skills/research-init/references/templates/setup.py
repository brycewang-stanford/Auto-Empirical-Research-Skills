"""
00_setup.py — Project setup and configuration

Provides:
- Reproducibility seed
- Project paths
- Shared helper functions
- Visualization defaults

All packages are managed via uv (pyproject.toml + uv.lock).
"""

from pathlib import Path

import numpy as np

# ── Reproducibility ──────────────────────────────────────────────────

# Set seed for all random operations. Document in decision log if changed.
SEED = 42
np.random.seed(SEED)

# ── Paths ────────────────────────────────────────────────────────────

# Project root is wherever this file lives (python/ -> parent)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

PATH_RAW = PROJECT_ROOT / "data" / "raw"
PATH_PROCESSED = PROJECT_ROOT / "data" / "processed"
PATH_CODEBOOK = PROJECT_ROOT / "data" / "codebook"
PATH_FIGURES = PROJECT_ROOT / "output" / "figures"
PATH_TABLES = PROJECT_ROOT / "output" / "tables"
PATH_RESULTS = PROJECT_ROOT / "output" / "results"


# ── Visualization defaults ───────────────────────────────────────────

def setup_matplotlib():
    """Configure matplotlib for APA-style publication figures."""
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "figure.figsize": (6.5, 4.5),
        "figure.dpi": 300,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.grid": True,
        "axes.grid.which": "major",
        "grid.alpha": 0.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
    })


def save_figure(fig, name: str, width: float = 6.5, height: float = 4.5, dpi: int = 300):
    """Save a figure in PNG and PDF formats to output/figures/."""
    fig.set_size_inches(width, height)
    fig.savefig(PATH_FIGURES / f"{name}.png", dpi=dpi, bbox_inches="tight", facecolor="white")
    fig.savefig(PATH_FIGURES / f"{name}.pdf", bbox_inches="tight", facecolor="white")


# ── Session info ─────────────────────────────────────────────────────

def capture_session_info():
    """Capture Python environment info for reproducibility."""
    try:
        import watermark
        info = watermark.watermark(packages="polars,pandas,numpy,scipy,statsmodels,matplotlib,seaborn")
    except ImportError:
        import sys
        info = f"Python {sys.version}\nInstall watermark for full session info."

    (PROJECT_ROOT / "output" / "session-info.txt").write_text(info)
    return info
