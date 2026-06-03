# 00_setup.R — Project setup and configuration
#
# This file is sourced by _targets.R and provides:
# - Reproducibility seed
# - Project paths
# - Shared helper functions
#
# All packages are loaded via tar_option_set() in _targets.R,
# NOT here. This keeps dependencies explicit and tracked.

# ── Reproducibility ──────────────────────────────────────────────────

# Set seed for all random operations. Document in decision log if changed.
set.seed(42)

# ── Paths ────────────────────────────────────────────────────────────

# Use here::here() for all paths — never setwd(), never hardcode absolute paths
path_raw       <- here::here("data", "raw")
path_processed <- here::here("data", "processed")
path_codebook  <- here::here("data", "codebook")
path_figures   <- here::here("output", "figures")
path_tables    <- here::here("output", "tables")
path_results   <- here::here("output", "results")

# ── ggplot2 theme ────────────────────────────────────────────────────

# APA 7th-aligned default theme for all figures
theme_apa <- function(base_size = 11) {
  ggplot2::theme_minimal(base_size = base_size) +
    ggplot2::theme(
      # Clean background
      panel.grid.minor = ggplot2::element_blank(),
      panel.grid.major = ggplot2::element_line(color = "grey92"),
      # Axis
      axis.line = ggplot2::element_line(color = "black", linewidth = 0.3),
      axis.ticks = ggplot2::element_line(color = "black", linewidth = 0.3),
      # Text
      plot.title = ggplot2::element_text(face = "bold", hjust = 0),
      plot.subtitle = ggplot2::element_text(color = "grey40"),
      # Legend
      legend.position = "bottom",
      legend.title = ggplot2::element_text(face = "bold"),
      # Strip (facets)
      strip.text = ggplot2::element_text(face = "bold")
    )
}

# Set as default
ggplot2::theme_set(theme_apa())

# Colorblind-safe palette (viridis-based)
scale_color_research <- function(...) {
  ggplot2::scale_color_viridis_d(...)
}
scale_fill_research <- function(...) {
  ggplot2::scale_fill_viridis_d(...)
}

# ── Figure export helper ─────────────────────────────────────────────

save_figure <- function(plot, name, width = 6.5, height = 4.5, dpi = 300) {
  ggplot2::ggsave(
    filename = here::here("output", "figures", paste0(name, ".png")),
    plot = plot,
    width = width,
    height = height,
    dpi = dpi,
    bg = "white"
  )
  ggplot2::ggsave(
    filename = here::here("output", "figures", paste0(name, ".pdf")),
    plot = plot,
    width = width,
    height = height,
    bg = "white"
  )
}

# ── Session info capture ─────────────────────────────────────────────

capture_session_info <- function() {
  info <- sessioninfo::session_info()
  writeLines(
    capture.output(print(info)),
    here::here("output", "session-info.txt")
  )
  invisible(info)
}
