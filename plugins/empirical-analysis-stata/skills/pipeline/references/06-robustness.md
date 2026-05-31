# Step 6 — Robustness Battery in Stata (Deep Reference)

Goal: a headline coefficient is not credible until you've shown it survives reasonable variations. Stata has a particularly rich ecosystem here — `boottest` for wild-cluster bootstrap, `ritest` for randomization inference, `rwolf` for multiple-testing correction, `bacondecomp` for TWFE diagnosis, `honestdid` for parallel-trends sensitivity. Use them.

## Contents

1. Progressive specifications (M1 → M6) with `eststo` + `esttab`
2. Alternative cluster levels (and two-way clustering)
3. Wild cluster bootstrap (`boottest`) — for few clusters
4. Subsample splits
5. Alternative outcome / treatment definitions
6. Alternative sample restrictions (winsorize, trim)
7. Placebo — fake timing
8. Placebo — randomization inference (`ritest`)
9. Multiple-testing correction (`rwolf`, `wyoung`)
10. Specification curve (loop over formulas, plot estimates)
11. Oster (2019) δ\* — `psacalc`
12. TWFE bias diagnosis (`bacondecomp`)
13. HonestDiD — Rambachan–Roth (2023) PT sensitivity
14. Influence diagnostics — leave-one-out, drop top-K Cook's D

---

## 1. Progressive specifications

```stata
eststo clear
eststo m1: qui reg log_wage training, ///
    vce(cluster firm_id)
eststo m2: qui reg log_wage training age edu, ///
    vce(cluster firm_id)
eststo m3: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id) vce(cluster worker_id)
eststo m4: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year) vce(cluster worker_id)
eststo m5: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year region) vce(cluster worker_id)
eststo m6: qui reghdfe log_wage training age edu tenure, ///
    absorb(worker_id year i.industry#i.year) vce(cluster worker_id)

esttab m1 m2 m3 m4 m5 m6 using "tables/table_main.tex", ///
    replace booktabs ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    stats(N r2 r2_a, labels("N" "R²" "Adj. R²")) ///
    label keep(training) ///
    addnotes("All regressions cluster SE by worker_id.")
```

---

## 2. Alternative cluster levels

```stata
foreach c in worker_id firm_id industry state {
    quietly reghdfe log_wage training, ///
        absorb(worker_id year) vce(cluster `c')
    display "cluster=`c'   b=" _b[training] "  se=" _se[training] ///
            "  t=" _b[training]/_se[training]
}

* Two-way clustering
reghdfe log_wage training, absorb(worker_id year) ///
    vce(cluster worker_id firm_id)

* Three-way (rare; supported by reghdfe)
reghdfe log_wage training, absorb(worker_id year) ///
    vce(cluster worker_id firm_id state)
```

---

## 3. Wild cluster bootstrap (`boottest`)

When the number of clusters is small (< 50), classical CRSE under-cover. `boottest` is the gold standard.

```stata
* After reghdfe / reg
quietly reghdfe log_wage training, absorb(worker_id year) ///
    vce(cluster state)
boottest training, cluster(state) reps(9999) seed(42)
boottest training = 0.05, cluster(state) reps(9999)        // test specific value

* Wild restricted ("WCR") and Webb weights
boottest training, weighttype(webb) reps(9999)
boottest training, nograph reps(9999) bootcluster(state worker_id)

* Confidence interval
boottest training, ci level(95) reps(9999)
```

---

## 4. Subsample splits

```stata
foreach mask in "female==0" "female==1" "age<40" "age>=40" ///
                 "industry==1" "industry==2" {
    quietly reghdfe log_wage training if `mask', ///
        absorb(worker_id year) vce(cluster worker_id)
    display "`mask': b=" _b[training] "  se=" _se[training] "  N=" e(N)
}
```

For *testing* heterogeneity (not just estimating subsamples), prefer interaction terms — see references/07.

---

## 5. Alternative outcome / treatment definitions

```stata
* Alternative outcome forms
foreach y in log_wage ihs_wage wage_w1 wage_real_log {
    quietly reghdfe `y' training, absorb(worker_id year) ///
        vce(cluster worker_id)
    display "`y':  b=" _b[training] "  se=" _se[training]
}

* Alternative treatment definitions
foreach t in training training_ever training_hours_log training_intense {
    quietly reghdfe log_wage `t', absorb(worker_id year) ///
        vce(cluster worker_id)
    display "`t':  b=" _b[`t'] "  se=" _se[`t']
}
```

---

## 6. Alternative sample restrictions

```stata
* Winsorization sensitivity
foreach lvl in 0 1 5 {
    preserve
        if `lvl' > 0 {
            winsor2 log_wage, cuts(`lvl' `=100-`lvl'') replace
        }
        quietly reghdfe log_wage training, absorb(worker_id year) ///
            vce(cluster worker_id)
        display "winsor `lvl'/`=100-`lvl'':  b=" _b[training] ///
                "  se=" _se[training]
    restore
}

* Trim sensitivity
foreach trim in 0.01 0.05 {
    preserve
        quietly sum log_wage, detail
        local lo = r(p`=`trim'*100')
        local hi = r(p`=100-`trim'*100')
        keep if log_wage >= `lo' & log_wage <= `hi'
        quietly reghdfe log_wage training, absorb(worker_id year)
        display "trim `=`trim'*100'%:  b=" _b[training]
    restore
}
```

---

## 7. Placebo — fake timing

```stata
* Shift treatment 3 years earlier; should produce ~0
gen fake_first = first_treat - 3
gen fake_post  = (year >= fake_first) if !missing(fake_first)
replace fake_post = 0 if missing(fake_first)

preserve
    keep if year < first_treat                            // drop real post period
    reghdfe log_wage fake_post, absorb(worker_id year) ///
        vce(cluster worker_id)
restore

* For event studies: drop real post period, re-estimate pre-period coefs.
* All pre-period coefficients should be ~0.
```

---

## 8. Randomization inference (`ritest`)

Permutation-based inference — re-shuffles treatment under the null, gives an exact p-value. Especially valuable when:
- Few clusters
- Treatment assignment was randomized
- You want a non-parametric placebo distribution

```stata
* After your headline regression, permute treatment and re-estimate
ritest training _b[training], reps(1000) seed(42) ///
    strata(industry):  reghdfe log_wage training, ///
    absorb(worker_id year) vce(cluster worker_id)

* Two-tailed p-value, plus full distribution
ritest training _b[training], reps(1000) seed(42) ///
    saving("logs/ritest_dist.dta", replace): ///
    reghdfe log_wage training, absorb(worker_id year) ///
    vce(cluster worker_id)

* Plot the null distribution
preserve
    use "logs/ritest_dist.dta", clear
    histogram _b_training, bin(50) ///
        xtitle("Permuted coefficient") ///
        addplot(scatteri 0 `=_b_training_obs', mcolor(red))
    graph export "figures/ritest_dist.pdf", replace
restore

* Permute *within* clusters (preserves cluster structure)
ritest training _b[training], reps(1000) cluster(state) seed(42): ///
    reghdfe log_wage training, absorb(worker_id year) ///
    vce(cluster state)
```

---

## 9. Multiple-testing correction

When you test the effect on multiple outcomes (e.g. employed, hours_worked, log_wage), the family-wise error rate balloons. Correct it:

```stata
* Romano-Wolf step-down
rwolf employed hours_worked log_wage, ///
    indepvar(training) ///
    controls(age edu) ///
    reps(500) seed(42) ///
    method(reghdfe) ///
    fe(worker_id year) ///
    cluster(worker_id) ///
    bl(0.05)

* Westfall–Young
ssc install wyoung, replace
wyoung, cmd("reghdfe employed training age edu, absorb(worker_id year)" ///
            "reghdfe hours_worked training age edu, absorb(worker_id year)" ///
            "reghdfe log_wage training age edu, absorb(worker_id year)") ///
    family("training") ///
    bootstraps(500) seed(42) cluster(worker_id)
```

---

## 10. Specification curve

Run the model across every combination of controls / FE / outcomes / treatments, plot the distribution.

```stata
* Loop and collect estimates
tempname M
postfile `M' str30 spec float(b se) using "logs/spec_curve.dta", replace

local outcomes "log_wage wage_w1"
local treatments "training training_ever"
local control_sets `""""    ""age""    ""age edu""    ""age edu tenure"""'
local fe_sets `""worker_id"  "worker_id year"  "worker_id year industry^year""'

local s = 0
foreach y of local outcomes {
    foreach t of local treatments {
        foreach c of local control_sets {
            foreach fe of local fe_sets {
                local ++s
                local rhs = trim("`t' `c'")
                quietly reghdfe `y' `rhs', absorb(`fe') vce(cluster worker_id)
                if e(N) > 0 {
                    post `M' ("`y'|`t'|`c'|`fe'") (_b[`t']) (_se[`t'])
                }
            }
        }
    }
}
postclose `M'

* Plot
preserve
    use "logs/spec_curve.dta", clear
    sort b
    gen idx = _n
    gen lb = b - 1.96*se
    gen ub = b + 1.96*se
    twoway (rcap lb ub idx, lcolor(gs10)) ///
           (scatter b idx, mcolor(navy) msize(small)), ///
        yline(0, lpattern(dash)) ///
        xtitle("Specification (sorted by coefficient)") ///
        ytitle("Coefficient on training") legend(off)
    graph export "figures/spec_curve.pdf", replace
restore
```

---

## 11. Oster (2019) δ\*

Tests how strong selection on unobservables (relative to observables) would need to be to nullify the effect.

```stata
ssc install psacalc, replace

* Long regression (all observable controls)
quietly reghdfe log_wage training age edu tenure female, ///
    absorb(worker_id year) vce(cluster worker_id)
psacalc delta training, mcontrol(age edu tenure female) rmax(1.3*e(r2))
* δ* > 1   ⇒ basic robustness
* δ* > 2   ⇒ strong robustness
* |δ*| > 4 ⇒ very strong (used in JOE / AER)

* Bound the bias-adjusted β
psacalc beta training, mcontrol(age edu tenure female) rmax(1.3*e(r2)) delta(1)
```

---

## 12. TWFE bias diagnosis (`bacondecomp`)

```stata
xtset worker_id year
bacondecomp log_wage training, ///
    ddetail ///                                          // print the 2×2 components
    nograph
* Reports 4 categories of comparisons + their weights:
*   - Earlier vs. later (treated)
*   - Later vs. earlier (treated)        ← negative-weight problem
*   - Treated vs. never-treated
*   - Treated vs. always-treated
* If "Later vs. earlier (treated)" weights are non-trivial, TWFE is biased.

* Visualize
bacondecomp log_wage training
graph export "figures/bacon.pdf", replace
```

---

## 13. HonestDiD — parallel-trends sensitivity

After estimating an event study, ask: "How big a violation of parallel trends would be needed to change my conclusion?"

```stata
* After eventstudyinteract / reghdfe with relative-time dummies,
* save the b and V matrices:
matrix b = e(b)
matrix V = e(V)

* HonestDiD using smoothness-restriction
honestdid, pre(1/4) post(5/9) mvec(0(0.05)0.5) ///
    coefplot
graph export "figures/honestdid.pdf", replace

* Bound on M (smoothness budget) at which significance disappears
honestdid, pre(1/4) post(5/9) mvec(0(0.05)0.5) ///
    delta(rm) breakdown
```

---

## 14. Influence — leave-one-out

```stata
quietly reghdfe log_wage training, absorb(worker_id year) ///
    vce(cluster worker_id)
local b_full = _b[training]

levelsof worker_id, local(units)
local n_units : word count `units'

* For tractability, sample 500 units to drop
local sample : list shuffle units
gettoken first rest : sample, parse(" ")
local i = 0

tempname L
postfile `L' float(b_loo) using "logs/loo.dta", replace
foreach u of local units {
    local ++i
    if `i' > 500 continue, break
    quietly reghdfe log_wage training if worker_id != `u', ///
        absorb(worker_id year) vce(cluster worker_id)
    post `L' (_b[training])
}
postclose `L'

preserve
    use "logs/loo.dta", clear
    histogram b_loo, bin(50) ///
        addplot(scatteri 0 `b_full', mcolor(red))
    graph export "figures/loo.pdf", replace
restore

* Drop top 1% Cook's D
quietly reg log_wage training age edu tenure
predict cd, cooksd
sum cd, detail
preserve
    drop if cd > r(p99)
    reghdfe log_wage training, absorb(worker_id year) vce(cluster worker_id)
restore
```

---

## What a strong robustness appendix contains

A paper that survives review should include, at minimum:

1. **Progressive specs** (M1–M6) → `tables/table_main.tex`
2. **Cluster sensitivity** at 3–4 levels + `boottest` if few clusters
3. **Placebo (fake timing)** event-study estimates ~0 in pre-period
4. **Randomization inference** histogram with observed coef vs. null distribution
5. **Specification curve** of all valid combinations
6. **Oster δ\*** computed via `psacalc`
7. **Subsample splits** at 4–6 pre-defined dimensions
8. **Alternative outcome / treatment definitions** (≥ 2–3 each)
9. For DID: `bacondecomp` weights + `honestdid` sensitivity
10. For IV: weak-IV stats (KP rk Wald, AR), overid (Hansen J), Conley if geographic
11. For RD: bandwidth sensitivity (×0.5/1/2), `rddensity`, covariate smoothness placebos
12. For PSM/IPW: `pstest` / `tebalance` SMDs before/after, common-support trimmed re-estimate, entropy-balance version
