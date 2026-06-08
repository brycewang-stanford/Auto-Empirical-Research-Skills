# ============================================================
# 03_main_did.R
# Staggered DiD with modern estimator (Callaway-Sant'Anna).
# Produces main table, event-study figure, Bacon decomposition,
# and Honest DiD sensitivity bounds.
# ============================================================

dt <- haven::read_dta(file.path(INTERMEDIATE, "analytic.dta")) |>
  as.data.table()

# ============================================================
# 1. Naive TWFE (FOR COMPARISON ONLY)
# ============================================================
m_twfe <- feols(
  outcome ~ treat + x1 + x2 | unit_id + year,
  data    = dt,
  cluster = ~ unit_id
)

# ============================================================
# 2. Goodman-Bacon decomposition
# ============================================================
bacon_out <- bacon(outcome ~ treat,
                   data       = as.data.frame(dt),
                   id_var     = "unit_id",
                   time_var   = "year")
saveRDS(bacon_out, file.path(INTERMEDIATE, "bacon_decomp.rds"))

# ============================================================
# 3. Callaway-Sant'Anna ATT(g,t) -- PREFERRED ESTIMATOR
#    base_period = "universal" keeps the e = -1 reference so the
#    event-study coefficients line up with the HonestDiD step below.
# ============================================================
cs_att <- att_gt(
  yname         = "outcome",
  tname         = "year",
  idname        = "unit_id",
  gname         = "treat_year",
  xformla       = ~ x1 + x2,
  data          = as.data.frame(dt),
  est_method    = "dr",            # doubly-robust
  control_group = "notyettreated", # avoids forbidden comparisons
  base_period   = "universal",
  clustervars   = "unit_id"
)

# Aggregations
cs_simple <- aggte(cs_att, type = "simple")
cs_dyn    <- aggte(cs_att, type = "dynamic", min_e = -5, max_e = 5)
cs_group  <- aggte(cs_att, type = "group")

# ============================================================
# 4. Event-study plot
# ============================================================
event_df <- data.frame(
  e        = cs_dyn$egt,
  estimate = cs_dyn$att.egt,
  se       = cs_dyn$se.egt
) |>
  mutate(
    ci_lo = estimate - 1.96 * se,
    ci_hi = estimate + 1.96 * se,
    post  = e >= 0
  )

p_event <- ggplot(event_df, aes(x = e, y = estimate)) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "grey40") +
  geom_vline(xintercept = -0.5, linetype = "dashed", color = "grey40") +
  geom_pointrange(aes(ymin = ci_lo, ymax = ci_hi, color = post)) +
  scale_color_manual(values = c("FALSE" = "grey50", "TRUE" = "black"),
                     guide  = "none") +
  scale_x_continuous(breaks = seq(-5, 5, 1)) +
  labs(x = "Years relative to treatment",
       y = "ATT estimate",
       title = NULL)

ggsave(file.path(FIGURES, "fig_event_study.pdf"),
       p_event, width = 6, height = 4)

# ============================================================
# 5. Honest DiD sensitivity (Rambachan-Roth 2023)
#    honest_did() is the standard did -> HonestDiD bridge from the
#    HonestDiD package vignette: it builds the event-study covariance
#    matrix from the influence function and drops the e = -1 reference
#    period before computing relative-magnitudes robust CIs.
# ============================================================
honest_did <- function(es, e = 0,
                       type = c("relative_magnitude", "smoothness"),
                       Mbarvec = NULL, Mvec = NULL, ...) {
  type <- match.arg(type)
  if (es$type != "dynamic")
    stop("honest_did() requires a dynamic aggte() object")

  # event-study variance-covariance matrix from the influence function
  inf_fn <- es$inf.function$dynamic.inf.func.e
  n      <- nrow(inf_fn)
  Sigma  <- t(inf_fn) %*% inf_fn / n / n
  beta   <- es$att.egt

  # drop the e = -1 reference period
  keep   <- es$egt != -1
  beta   <- beta[keep]
  Sigma  <- Sigma[keep, keep, drop = FALSE]
  n_pre  <- sum(es$egt[keep] <  0)
  n_post <- sum(es$egt[keep] >= 0)
  l_vec  <- HonestDiD::basisVector(e + 1, n_post)

  if (type == "relative_magnitude") {
    robust <- HonestDiD::createSensitivityResults_relativeMagnitudes(
      betahat = beta, sigma = Sigma,
      numPrePeriods = n_pre, numPostPeriods = n_post,
      Mbarvec = Mbarvec, l_vec = l_vec)
  } else {
    robust <- HonestDiD::createSensitivityResults(
      betahat = beta, sigma = Sigma,
      numPrePeriods = n_pre, numPostPeriods = n_post,
      Mvec = Mvec, l_vec = l_vec)
  }
  orig <- HonestDiD::constructOriginalCS(
    betahat = beta, sigma = Sigma,
    numPrePeriods = n_pre, numPostPeriods = n_post, l_vec = l_vec)
  list(robust_ci = robust, orig_ci = orig)
}

honest_out <- honest_did(cs_dyn, e = 0, type = "relative_magnitude",
                         Mbarvec = seq(0.5, 2, by = 0.5))
saveRDS(honest_out, file.path(INTERMEDIATE, "honest_did.rds"))

# ============================================================
# 6. Main results table -- TWFE vs Callaway-Sant'Anna
#    The CS aggregate is not a model object, so wrap it in a
#    modelsummary "list" with the same term name ("treat") used by
#    the TWFE model so the two estimates stack on one row.
# ============================================================
cs_z <- cs_simple$overall.att / cs_simple$overall.se
cs_for_table <- list(
  tidy = data.frame(
    term      = "treat",
    estimate  = cs_simple$overall.att,
    std.error = cs_simple$overall.se,
    statistic = cs_z,
    p.value   = 2 * pnorm(-abs(cs_z))
  ),
  glance = data.frame(nobs = nobs(m_twfe))
)
class(cs_for_table) <- "modelsummary_list"

modelsummary(
  list("TWFE (biased)"      = m_twfe,
       "Callaway-Sant'Anna" = cs_for_table),
  output     = file.path(TABLES, "tab_main_did.tex"),
  stars      = c("*" = 0.1, "**" = 0.05, "***" = 0.01),
  fmt        = 3,
  coef_map   = c("treat" = "Treatment"),
  gof_omit   = "IC|Log|RMSE|Adj|F|Pseudo",
  notes      = c("Standard errors clustered at the unit level.",
                 "TWFE shown for comparison only; Bacon decomposition (Fig A) reports forbidden-comparison weight."),
  booktabs   = TRUE
)
