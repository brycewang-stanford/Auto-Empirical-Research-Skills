# ============================================================
# 00_setup.R
# Paths, packages, seed.
# ============================================================

# ---- Paths ---------------------------------------------------
PROJECT      <- getwd()
DATA         <- file.path(PROJECT, "data")
RAW          <- file.path(DATA, "raw")
INTERMEDIATE <- file.path(DATA, "intermediate")
CODE         <- PROJECT
OUTPUT       <- file.path(PROJECT, "output")
TABLES       <- file.path(OUTPUT, "tables")
FIGURES      <- file.path(OUTPUT, "figures")
LOGS         <- file.path(PROJECT, "logs")

dir.create(RAW,          showWarnings = FALSE, recursive = TRUE)
dir.create(INTERMEDIATE, showWarnings = FALSE, recursive = TRUE)
dir.create(TABLES,       showWarnings = FALSE, recursive = TRUE)
dir.create(FIGURES,      showWarnings = FALSE, recursive = TRUE)
dir.create(LOGS,         showWarnings = FALSE, recursive = TRUE)

# ---- Reproducibility -----------------------------------------
set.seed(20260101)

# ---- Required packages ---------------------------------------
required_pkgs <- c(
  # Data manipulation
  "data.table", "tidyverse", "haven", "readr",
  # Identification
  "fixest",         # high-dim FE OLS, IV, event studies
  "did",            # Callaway-Sant'Anna
  "didimputation",  # Borusyak-Jaravel-Spiess
  "DIDmultiplegt",  # de Chaisemartin-D'Haultfoeuille
  "bacondecomp",    # Goodman-Bacon
  "HonestDiD",      # Rambachan-Roth sensitivity
  "rdrobust",       # Calonico-Cattaneo-Titiunik RDD
  "rddensity",      # Cattaneo-Jansson-Ma density test
  "Synth", "tidysynth", "augsynth",
  "ivDiag",         # weak-IV diagnostics
  "AER",            # ivreg with diagnostics
  # Tables & figures
  "modelsummary", "kableExtra", "gt",
  "ggplot2", "ggthemes", "scales", "patchwork", "viridis",
  # Inference
  "sandwich", "lmtest", "fwildclusterboot", "clubSandwich"
)

missing <- setdiff(required_pkgs, rownames(installed.packages()))
if (length(missing) > 0) {
  install.packages(missing, repos = "https://cloud.r-project.org")
}
invisible(lapply(required_pkgs, library, character.only = TRUE))

# ---- Plot theme ----------------------------------------------
theme_set(theme_minimal(base_family = "Helvetica", base_size = 11) +
            theme(panel.grid.minor = element_blank(),
                  plot.title = element_text(face = "plain")))
