# _targets.R — Pipeline definition for {{PROJECT_NAME}}
#
# This file defines the reproducible analysis pipeline using the {targets}
# package. Each target is a step in the analysis — from raw data to final
# manuscript. Targets automatically tracks dependencies and skips steps
# whose inputs haven't changed.
#
# Run the full pipeline:    tar_make()
# Visualize the pipeline:   tar_visnetwork()
# Check what's outdated:    tar_outdated()
# Read a target's value:    tar_read(target_name)
#
# Learn more: https://books.ropensci.org/targets/

library(targets)

# Load all functions in R/ directory
tar_source()

# Set packages used across the pipeline
tar_option_set(
  packages = c(
    # Data wrangling
    "dplyr", "tidyr", "readr", "stringr", "forcats", "purrr",
    # Visualization
    "ggplot2", "patchwork", "scales",
    # Tables
    "gt", "gtsummary", "modelsummary",
    # Statistics
    "parameters", "performance", "effectsize", "report",
    # Add project-specific packages below:
    NULL
  )
)

# Define the pipeline
list(

  # ── Stage 1: Read raw data ──────────────────────────────────────────
  # tar_target(raw_data, read_raw_data("data/raw/YOUR_FILE.csv")),

  # ── Stage 2: Validate ──────────────────────────────────────────────
  # tar_target(validation_report, validate_data(raw_data)),

  # ── Stage 3: Clean ─────────────────────────────────────────────────
  # tar_target(clean_data, clean_data(raw_data)),

  # ── Stage 4: EDA ───────────────────────────────────────────────────
  # tar_target(descriptives, compute_descriptives(clean_data)),
  # tar_target(table1, create_table1(clean_data)),
  # tar_target(correlation_matrix, compute_correlations(clean_data)),

  # ── Stage 5: Confirmatory analysis ─────────────────────────────────
  # tar_target(h1_model, test_hypothesis_1(clean_data)),
  # tar_target(h2_model, test_hypothesis_2(clean_data)),

  # ── Stage 6: Robustness ────────────────────────────────────────────
  # tar_target(robustness_h1, robustness_checks(h1_model, clean_data)),

  # ── Stage 7: Figures ───────────────────────────────────────────────
  # tar_target(fig_main, create_main_figure(h1_model, clean_data)),

  # ── Stage 8: Tables ────────────────────────────────────────────────
  # tar_target(results_table, create_results_table(h1_model, h2_model)),

  # ── Stage 9: Manuscript ────────────────────────────────────────────
  # tar_target(manuscript, tar_quarto_render("reports/manuscript.qmd")),

  # Placeholder — remove when adding real targets above
  tar_target(pipeline_ready, TRUE)
)
