# Step 7 — Further Analysis in Stata (Deep Reference)

Goal: deepen the headline ATT into a story. Three classical questions:

1. **Heterogeneity**: For whom is the effect strongest?
2. **Mechanism**: Through what channel does it operate?
3. **Moderation / Mediation**: Under what conditions?

Stata's `factor variables` + `margins` + `marginsplot` is unusually well-suited to this layer; this file is the playbook.

## Contents

1. Heterogeneity via factor-variable interactions + Wald test
2. Subgroup estimation + `suest` cross-equation Wald
3. Triple difference (DDD)
4. Continuous moderator + `marginsplot`
5. Subgroup event studies
6. Outcome ladder
7. Mediation — Baron–Kenny manual
8. Mediation — `medsem` / `khb` / SEM
9. Moderated mediation
10. Dose-response (continuous treatment)
11. CATE — falling back to Python `econml` via Stata-Python bridge
12. Spillover / interference

---

## 1. Heterogeneity via factor-variable interactions

The cleanest approach — the interaction coefficient *is* the heterogeneity test.

```stata
* Binary moderator
reghdfe log_wage c.training##i.female age edu, ///
    absorb(worker_id year) vce(cluster worker_id)

* The coefficient on c.training#1.female is Δ_ATT (female - male).
* margins makes the effect by group explicit:
margins, dydx(training) at(female=(0 1))
marginsplot, recast(connected) ///
    title("Marginal effect of training, by gender") ///
    ytitle("dY/d(training)")
graph export "figures/het_gender.pdf", replace

* Continuous moderator
reghdfe log_wage c.training##c.tenure age edu, ///
    absorb(worker_id year) vce(cluster worker_id)
margins, dydx(training) at(tenure=(0(2)20))
marginsplot, recast(connected) ///
    title("Marginal effect of training along tenure") ///
    ytitle("dY/d(training)")
graph export "figures/het_tenure.pdf", replace

* Two moderators at once
reghdfe log_wage c.training##i.female##c.tenure age edu, ///
    absorb(worker_id year) vce(cluster worker_id)
margins, dydx(training) at(female=(0 1) tenure=(0 5 10 20))
marginsplot, recast(connected) by(female)
```

---

## 2. Subgroup estimation + `suest`

If you'd rather run separate regressions per subgroup but need a formal Wald test of equality:

```stata
eststo clear
eststo male:   qui reghdfe log_wage training age edu if female==0, ///
    absorb(worker_id year) vce(cluster worker_id)
eststo female: qui reghdfe log_wage training age edu if female==1, ///
    absorb(worker_id year) vce(cluster worker_id)

* suest combines covariance matrices across equations
suest male female

* Test equality of training coefficient across subgroups
test [male_mean]training = [female_mean]training
```

**Caveat**: `suest` does not support `reghdfe`'s absorbed FEs natively. Re-fit with `xtreg, fe` or use the Wald approximation:

```stata
local b1 = _b[training] in m1; local se1 = _se[training] in m1
local b2 = _b[training] in m2; local se2 = _se[training] in m2
local diff = `b1' - `b2'
local se   = sqrt(`se1'^2 + `se2'^2)
local z    = `diff'/`se'
display "Δ=" `diff' "  SE=" `se' "  z=" `z' "  p=" 2*(1-normal(abs(`z')))
```

---

## 3. Triple difference (DDD)

```stata
* Differential DID across a third dimension
reghdfe log_wage c.treated##c.post##c.high_exposure age edu, ///
    absorb(worker_id year) vce(cluster firm_id)

* The coefficient on treated#post#high_exposure is the differential ATT
* (effect of treatment among high-exposure minus low-exposure firms).
margins, dydx(treated) at(post=1 high_exposure=(0 1))
```

---

## 4. Continuous moderator with margins plot

```stata
reghdfe log_wage c.training##c.firm_size age edu, ///
    absorb(worker_id year) vce(cluster firm_id)

* Marginal effect of training along the support of firm_size
margins, dydx(training) ///
    at(firm_size=(`=`firm_p5'(`=`firm_step')'`firm_p95''))

marginsplot, recast(line) ///
    recastci(rarea) ciopts(fcolor(navy%20) lcolor(none)) ///
    yline(0, lpattern(dash)) ///
    title("Marginal effect of training along firm size") ///
    xtitle("Firm size") ytitle("dY/d(training)")
graph export "figures/marginsplot_firmsize.pdf", replace
```

---

## 5. Subgroup event studies

```stata
* Stack subgroup event studies side-by-side
foreach g in 0 1 {
    local lab = cond(`g'==0, "Male", "Female")
    quietly eventstudyinteract log_wage rel_p_*  if female==`g', ///
        cohort(first_treat) control_cohort(never_treated) ///
        absorb(i.worker_id i.year) vce(cluster worker_id)
    coefplot, keep(rel_p_*) vertical omitted ///
        yline(0) ///
        title("`lab'") ///
        saving(figures/es_`g', replace)
}
graph combine "figures/es_0.gph" "figures/es_1.gph", ///
    title("Event study by gender")
graph export "figures/es_by_gender.pdf", replace
```

---

## 6. Outcome ladder

Run the same treatment regression on a sequence of outcomes (proximate → distal). The effect should propagate down the chain if the mechanism is real.

```stata
eststo clear
local outs "hours_worked productivity log_wage"
foreach y of local outs {
    eststo `y': qui reghdfe `y' training age edu, ///
        absorb(worker_id year) vce(cluster worker_id)
}
esttab `outs' using "tables/outcome_ladder.tex", ///
    replace booktabs ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label keep(training) ///
    addnotes("Same regressors and FE across outcomes.")

* Visual coefplot
coefplot (hours_worked, label("Proximate: hours")) ///
         (productivity,  label("Intermediate: productivity")) ///
         (log_wage,      label("Distal: log wage")), ///
    keep(training) vertical xline(0) ///
    title("Outcome ladder")
graph export "figures/outcome_ladder.pdf", replace
```

---

## 7. Mediation — Baron-Kenny (manual)

Linear, naive mediation. OK as a first pass; insufficient for serious causal claims.

```stata
* Step 1: Total effect (c)
quietly reghdfe log_wage training age edu, ///
    absorb(worker_id year) vce(cluster worker_id)
scalar c_path = _b[training]

* Step 2: T → M (a)
quietly reghdfe hours_worked training age edu, ///
    absorb(worker_id year) vce(cluster worker_id)
scalar a_path = _b[training]

* Step 3: T + M → Y (gives c' direct and b mediator coef)
quietly reghdfe log_wage training hours_worked age edu, ///
    absorb(worker_id year) vce(cluster worker_id)
scalar cprime = _b[training]
scalar b_path = _b[hours_worked]

scalar indirect = a_path * b_path
scalar pct_med  = 100*indirect/c_path

display "Total c    = " %7.4f c_path
display "Direct c'  = " %7.4f cprime
display "Indirect ab = " %7.4f indirect "  (" %4.1f pct_med "% of total)"
```

### Bootstrap CI for the indirect effect

```stata
program drop _all
program define mediation_bk, rclass
    quietly reghdfe hours_worked training age edu, absorb(worker_id year)
    scalar a = _b[training]
    quietly reghdfe log_wage training hours_worked age edu, absorb(worker_id year)
    scalar b = _b[hours_worked]
    return scalar indirect = a*b
end

bootstrap r(indirect), reps(1000) seed(42) cluster(worker_id): mediation_bk
```

---

## 8. Mediation — `medsem` / `khb` / SEM

```stata
* medsem — uses sem with bootstrap
ssc install medsem, replace
medsem, indep(training) med(hours_worked) dep(log_wage) ///
    mcreps(1000) zlc                                       // 1000 bootstrap reps

* khb — Karlson-Holm-Breen for non-linear mediation (logit / probit)
ssc install khb, replace
khb logit employed training || hours_worked, ///
    summary

* sem — full path model
sem (log_wage  <- training age edu hours_worked) ///
    (hours_worked <- training age edu)
estat teffects                                            // direct, indirect, total

* gsem — non-linear mediation (e.g. employment → wage)
gsem (employed     <- training age edu, logit) ///
     (log_wage     <- training age edu employed), ///
     vce(cluster firm_id)
estat teffects
```

Imai sensitivity (`mediation` package via `rsource` or rpy2-style bridge): no native Stata implementation; for serious causal mediation, fall back to R's `mediation` or Python `causalml`.

---

## 9. Moderated mediation

```stata
* Hypothesis: training → hours → wage, stronger for skilled workers.
* Approach: run mediation analysis separately by skill level.
foreach s in 0 1 {
    display _newline "===== skilled = `s' ====="
    medsem if skilled == `s', ///
        indep(training) med(hours_worked) dep(log_wage) ///
        mcreps(1000)
}

* For Hayes' Index of Moderated Mediation, see -hayesmacro- (older) or
* hand-roll via SEM with multi-group constraints:
sem (log_wage <- training@a hours_worked@b age edu) ///
    (hours_worked <- training@d age edu), ///
    group(skilled) ginvariant(none)
* Then test: a:_b[skilled@1] * d:_b[skilled@1] = a:_b[skilled@0] * d:_b[skilled@0]
```

---

## 10. Dose-response (continuous treatment)

```stata
* Decile-based piecewise-linear dose response
xtile dose10 = training_hours, nq(10)
reghdfe log_wage i.dose10 age edu, ///
    absorb(worker_id year) vce(cluster worker_id)
margins i.dose10
marginsplot, recast(connected) ///
    xtitle("Training-hours decile") ///
    ytitle("Predicted log wage")
graph export "figures/dose_decile.pdf", replace

* Spline-based smooth dose response
ssc install bspline, replace
bspline, xvar(training_hours) gen(bs_) knots(0(20)100) p(3)
reghdfe log_wage bs_* age edu, absorb(worker_id year) vce(cluster worker_id)

* Linear extrapolation (predict on a grid)
preserve
    keep if _n <= 100
    replace age = `=mean_age'
    replace edu = `=mean_edu'
    replace training_hours = (_n - 1) * 1                      // 0..99
    foreach v of varlist bs_* {
        replace `v' = .                                          // recompute
    }
    bspline, xvar(training_hours) gen(bs_) knots(0(20)100) p(3) replace
    predict y_hat, xb
    twoway line y_hat training_hours
    graph export "figures/dose_spline.pdf", replace
restore

* Continuous DID — see -did_continuous- (community) or fall back to Python
```

---

## 11. CATE — Stata–Python bridge to `econml`

Stata 16+ supports Python integration. For high-dimensional CATE estimation (causal forest, DR-Learner) use Python's `econml` from inside Stata:

```stata
* In Stata
python:
import pandas as pd
from econml.dml import CausalForestDML
from sklearn.ensemble import GradientBoostingRegressor

# Pull the Stata data into Python
from sfi import Data
y = Data.get("log_wage")
t = Data.get("training")
X = Data.get(["age", "edu", "tenure", "firm_size"])

cf = CausalForestDML(
    model_y=GradientBoostingRegressor(),
    model_t=GradientBoostingRegressor(),
    n_estimators=1000,
    min_samples_leaf=5,
    cv=5,
)
cf.fit(y, t, X=X)

tau = cf.effect(X)
# Push CATE back into Stata
Data.addVarFloat("tau_hat")
Data.store("tau_hat", None, tau.tolist())
end

* Now `tau_hat` is in your Stata dataset
sum tau_hat, detail
xtile tau_quint = tau_hat, nq(5)
tabstat age edu tenure firm_size, by(tau_quint) stat(mean)
```

Plot CATE binned by a moderator:

```stata
binscatter tau_hat tenure, nquantiles(20) ///
    xtitle("Tenure") ytitle("Estimated CATE")
graph export "figures/cate_by_tenure.pdf", replace
```

---

## 12. Spillover / interference

When SUTVA is questionable — e.g. treating one firm in a market may affect competitors:

```stata
* 12a. Exposure variable: share of treated peers in the market-year
bysort market year: egen share_treated_peers = mean(training)

* Re-estimate controlling for (and separately estimating effect of) exposure
reghdfe log_wage training share_treated_peers age edu, ///
    absorb(worker_id year) vce(cluster market)
* Coefficient on share_treated_peers captures spillover.

* 12b. Donut-style exclusion of close neighbors
preserve
    drop if min_distance_to_treated < 5  & training == 0   // controls within 5 km dropped
    reghdfe log_wage training age edu, ///
        absorb(worker_id year) vce(cluster firm_id)
restore

* 12c. Cluster-level randomization → estimate at cluster mean
collapse (mean) log_wage training age edu, by(cluster_id)
reg log_wage training age edu, vce(robust)
```

---

## What Step 7 typically produces

A solid further-analysis section has, at minimum:

1. **One heterogeneity table** with interaction estimates along 3–5 pre-specified moderators
2. **One marginsplot** showing dY/dT along a continuous moderator
3. **One outcome-ladder table** (`tables/outcome_ladder.tex`) + corresponding coefplot
4. **One mediation estimate** with bootstrap CI + a paragraph on the no-confounders assumption
5. **One DDD or moderated regression** if the design supports it
6. If treatment is continuous: **one dose-response plot** (`figures/dose_decile.pdf`)
7. **CATE results** if heterogeneity is high-dimensional (use Stata–Python bridge to `econml`)
8. If SUTVA is plausibly violated: **one spillover robustness** estimate

Each artifact lives in `tables/` or `figures/` with consistent naming, ready for Step 8 to assemble.
