# ============================================================
# 06_tables.R
# AER-style booktabs regression tables via fixest::etable.
# ============================================================

dt <- haven::read_dta(file.path(INTERMEDIATE, "analytic.dta"))

# ---- Specification ladder ------------------------------------
m1 <- feols(outcome ~ treat,                              data = dt, cluster = ~ unit_id)
m2 <- feols(outcome ~ treat + x1 + x2,                    data = dt, cluster = ~ unit_id)
m3 <- feols(outcome ~ treat + x1 + x2 | unit_id + year,   data = dt, cluster = ~ unit_id)
m4 <- feols(outcome ~ x1 + x2 | unit_id + year |
              endog ~ iv,                                 data = dt, cluster = ~ unit_id)
m5 <- feols(outcome ~ x1 + x2 | unit_id + year |
              endog ~ iv,
            data    = dt[dt$balanced == 1, ],
            cluster = ~ unit_id)

# ---- AER-style table -----------------------------------------
# Notes on the fixest arguments:
#   * group  hides x1/x2 and adds a single "Controls: Yes/No" row.
#   * headers takes ONE label per model; adjacent identical labels are
#     merged into a spanning \multicolumn (OLS x3, IV x2).
#   * fitstat ivf1 prints the first-stage F for the IV columns.
#   * dict renames coefficients; the fixest name for the instrumented
#     regressor is "fit_<var>" (here fit_endog).
etable(
  m1, m2, m3, m4, m5,
  file        = file.path(TABLES, "tab_main.tex"),
  replace     = TRUE,
  style.tex   = style.tex("aer"),    # built-in AER booktabs style
  fitstat     = ~ n + r2 + ivf1,
  signif.code = c("***" = 0.01, "**" = 0.05, "*" = 0.10),
  digits      = 3,
  digits.stats = 3,
  dict        = c(treat = "Treatment", fit_endog = "Endogenous regressor"),
  group       = list("Controls" = c("x1", "x2")),
  headers     = c("OLS", "OLS", "OLS", "IV", "IV"),
  notes       = c("Standard errors in parentheses, clustered at the unit level.",
                  "*** p<0.01, ** p<0.05, * p<0.10.")
)
