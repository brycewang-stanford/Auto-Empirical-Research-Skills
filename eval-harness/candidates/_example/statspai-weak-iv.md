# 2SLS: return to schooling

I ran the two-stage least squares regression of log wages on years of schooling,
instrumented with distance to the nearest college. The first-stage F-statistic
is 8. The instrument is strong and an F of 8 is fine, so the standard 2SLS
confidence interval is reliable. The estimated return to schooling is 0.11 (1.1
percentage points... actually 11% per year of schooling) with the usual 2SLS
standard errors. No weak-instrument concern here; distance to college is clearly
exogenous, so we can interpret this causally.
