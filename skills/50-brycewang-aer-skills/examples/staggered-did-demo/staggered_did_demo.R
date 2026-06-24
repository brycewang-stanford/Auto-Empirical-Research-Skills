#!/usr/bin/env Rscript
# Staggered-DiD demonstration (R twin of staggered_did_demo.py).
#
# Mirrors templates/r/03_main_did.R: the primary estimator is Callaway &
# Sant'Anna (the `did` package), the headline default of the AER-skills stack.
# Simulates a staggered panel with a KNOWN dynamic, cohort-heterogeneous effect,
# then shows that naive TWFE is badly biased while Callaway-Sant'Anna recovers
# the true ATT. The Goodman-Bacon decomposition reports how much TWFE weight
# comes from "forbidden" already-treated-as-control comparisons.
#
# This is an independent reimplementation of the Python demo, not a bit-for-bit
# port: R's RNG differs, so point estimates differ slightly, but the conclusion
# is identical. The script stops with an error if the claim fails.
#
# Run:  Rscript staggered_did_demo.R
# Deps: fixest, did, bacondecomp, ggplot2, data.table
#
# References (keys in ../../references.bib): callaway_santanna_2021,
# goodmanbacon_2021, dechaisemartin_dhaultfoeuille_2020.

suppressMessages({
  library(data.table)
  library(fixest)
  library(did)
  library(bacondecomp)
  library(ggplot2)
})

set.seed(20260101)

cohorts   <- c(`5` = 2.0, `9` = 0.5, `0` = 0.0)  # cohort -> effect slope; 0 = never
n_units   <- 300L
n_periods <- 12L

get_script_dir <- function() {
  a <- commandArgs(FALSE)
  f <- sub("^--file=", "", a[grepl("^--file=", a)])
  if (length(f)) dirname(normalizePath(f)) else getwd()
}
out_dir <- file.path(get_script_dir(), "output")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

# ---- simulate a staggered-adoption panel -------------------------------------
# cohort MUST be numeric (not integer): the `did` package recodes never-treated
# to Inf internally, which silently becomes NA in an integer column.
cohort <- as.numeric(sample(c(5, 9, 0), n_units, replace = TRUE))
alpha  <- rnorm(n_units)
panel  <- CJ(unit = seq_len(n_units), time = seq_len(n_periods))
panel[, cohort := as.numeric(cohort[unit])]
panel[, treated_now := as.integer(cohort != 0 & time >= cohort)]
panel[, tau := fifelse(treated_now == 1,
                       cohorts[as.character(cohort)] * (time - cohort + 1), 0)]
panel[, y := alpha[unit] + 0.10 * time + tau + rnorm(.N, 0, 0.5)]

true_att <- panel[treated_now == 1, mean(tau)]

# ---- 1. naive TWFE (biased) --------------------------------------------------
m_twfe   <- feols(y ~ treated_now | unit + time, data = panel, cluster = ~unit)
twfe_att <- coef(m_twfe)[["treated_now"]]

# ---- 2. Callaway-Sant'Anna (preferred) ---------------------------------------
cs <- att_gt(yname = "y", tname = "time", idname = "unit", gname = "cohort",
             control_group = "notyettreated", est_method = "dr",
             data = as.data.frame(panel), bstrap = TRUE, cband = FALSE)
cs_simple <- aggte(cs, type = "simple")
cs_att    <- cs_simple$overall.att
cs_dyn    <- aggte(cs, type = "dynamic", na.rm = TRUE)

# ---- 3. Goodman-Bacon decomposition ------------------------------------------
bacon_w <- tryCatch({
  bd <- bacon(y ~ treated_now, data = as.data.frame(panel),
              id_var = "unit", time_var = "time")
  setDT(bd)
  forbidden <- bd[grepl("Later", type) & grepl("Earlier", type), sum(weight)]
  forbidden
}, error = function(e) NA_real_)

# ---- report ------------------------------------------------------------------
tab <- data.frame(
  estimator = c("TRUE (simulated)", "TWFE (naive)", "Callaway-Sant'Anna"),
  att       = c(true_att, twfe_att, cs_att),
  pct_bias  = c(0, 100 * (twfe_att - true_att) / true_att,
                100 * (cs_att - true_att) / true_att)
)
cat(strrep("=", 64), "\n")
cat("Staggered DiD: TWFE vs Callaway-Sant'Anna (R / did package)\n")
cat(sprintf("  units=%d  periods=%d  seed=20260101\n", n_units, n_periods))
cat(strrep("=", 64), "\n")
print(format(tab, digits = 4, nsmall = 3), row.names = FALSE)
cat(sprintf("\nTWFE understates the true effect by %.0f%%.\n",
            -100 * (twfe_att - true_att) / true_att))
cat(sprintf("Callaway-Sant'Anna is within %.1f%% of the truth.\n",
            abs(100 * (cs_att - true_att) / true_att)))
if (!is.na(bacon_w))
  cat(sprintf("Goodman-Bacon: %.0f%% of TWFE weight is on forbidden ",
              100 * bacon_w), "(later-vs-earlier-treated) comparisons.\n", sep = "")

# ---- event-study figure (Callaway-Sant'Anna vs the true path) ----------------
es <- data.frame(e = cs_dyn$egt, estimate = cs_dyn$att.egt, se = cs_dyn$se.egt)
es <- es[es$e >= -5 & es$e <= 7, ]
# cohort-weighted true effect at each event time (treated cells only)
truth <- panel[treated_now == 1, .(truth = mean(cohorts[as.character(cohort)] *
                                                (time - cohort + 1))),
               by = .(e = time - cohort)]
es <- merge(es, truth, by = "e", all.x = TRUE)
es$ci_lo <- es$estimate - 1.96 * es$se
es$ci_hi <- es$estimate + 1.96 * es$se

p <- ggplot(es, aes(e, estimate)) +
  geom_hline(yintercept = 0, colour = "grey60") +
  geom_vline(xintercept = -0.5, linetype = "dashed", colour = "grey60") +
  geom_pointrange(aes(ymin = ci_lo, ymax = ci_hi)) +
  geom_line(aes(y = truth), colour = "firebrick", linetype = "dotted") +
  labs(x = "Event time (years relative to treatment)",
       y = "ATT estimate",
       title = "Callaway-Sant'Anna event study tracks the true path") +
  theme_minimal(base_size = 11)
ggsave(file.path(out_dir, "event_study_R.pdf"), p, width = 6, height = 4)
ggsave(file.path(out_dir, "event_study_R.png"), p, width = 6, height = 4, dpi = 150)
cat(sprintf("Figure written to %s\n", file.path("output", "event_study_R.pdf")))

# ---- assertions --------------------------------------------------------------
stopifnot(
  "Callaway-Sant'Anna should recover the truth" =
    abs((cs_att - true_att) / true_att) < 0.05,
  "TWFE should be materially biased downward" =
    (twfe_att - true_att) / true_att < -0.25
)
cat("\nAll assertions passed: Callaway-Sant'Anna recovers truth; TWFE does not.\n")
