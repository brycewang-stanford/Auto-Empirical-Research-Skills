# A taxonomy of p-hacking strategies

Two layers of strategies, then two more. The **base layer** is the
twelve-strategy compendium of Stefan & Schönbrodt (2023), which is the most
complete catalogue in the literature and the only one with matched
simulations. The **econometrics layer** adds the degrees of freedom that
appear in design-based causal work and that the base layer, written for
experimental psychology, does not cover. The **procedure layer** says in what
order the knobs are turned and when the search stops. The **stages layer**,
after Adda, Decker & Ottaviani (2020), covers what happens *between* a pilot
and a confirmatory analysis — which is where a registry of results shows
selection without any p-hacking at all.

Each strategy is described by what the researcher *chooses*, what makes the
choice defensible, and what the choice does to the type I error rate.

---

## Layer 1 — the twelve base strategies

Simulated false-positive rates are produced by `scripts/phack/simulate.py`, a
Python re-implementation of the reference R package `phackR`. Data are
generated under a **true null**, so every rejection is a false positive by
construction, and the nominal rate is 0.05.

"Modest" p-hacking stops at the first significant result. "Ambitious" keeps
searching and reports the *largest* significant effect. Ambitious hacking does
not change the rejection rate — the decision to stop is what does that — but it
changes which estimate reaches print, and so inflates published effect sizes.

| # | strategy | false-positive rate | mean analyses tried |
|---|---|---|---|
| — | *(no p-hacking, nominal α)* | **0.050** | 1 |
| 01 | selective reporting of the DV | 0.166 | 4.6 |
| 02 | selective reporting of the IV | 0.166 | 4.6 |
| 03 | optional stopping | 0.194 | 14.8 |
| 04 | outlier exclusion | 0.126 | 5.5 |
| 05 | controlling for covariates | 0.068 | 7.6 |
| 06 | scale redefinition | 0.165 | 23.2 |
| 07 | variable transformation | **0.250** | 21.1 |
| 08 | discretising a continuous variable | 0.190 | 8.0 |
| 09 | alternative hypothesis tests | 0.072 | 5.7 |
| 10 | favourable imputation | 0.086 | 7.6 |
| 11 | subgroup analysis | **0.214** | 6.3 |
| 12 | incorrect rounding | 0.061 | 1.0 |

4,000 simulations per strategy, α = 0.05, true effect exactly zero. Reproduce
with `python scripts/phack_cli.py simulate --n-sims 4000`. The measured rate
without p-hacking is 0.048 across strategies, which is the calibration check:
the harness recovers the nominal α when nobody cheats.

The rate is *identical* for modest and ambitious hacking, and this is not a bug.
Both stop rejecting only when no analysis in the set clears α, so the rejection
indicator is the same random variable. What ambitious hacking changes is the
published *estimate*: taking the largest significant effect rather than the
first one inflates effect sizes without touching the type I error rate. Pass
`--ambitious` to see the estimate shift while the rate does not.

Two lessons the ranking carries. First, the strategies that move the estimand —
transformation, discretisation, subgrouping — beat the strategies that merely
re-weight it, such as adding covariates or swapping a test. Second, no single
strategy gets near the rates people imagine; getting to a coin flip takes a
*workflow*.

### 1. Selective reporting of the dependent variable
Measure the outcome several ways — a survey index, its subscales, a binary
recode, an alternative data source — and report the one that works. Defensible
because every version is a real measure of the construct. The more correlated
the outcomes, the *less* this buys, because correlated tests are nearly the
same test.

### 2. Selective reporting of the independent variable
The mirror image: several operationalisations of the treatment or the regressor
of interest. In econometrics this is often a choice among instruments, or among
definitions of exposure intensity.

### 3. Optional stopping
Analyse, and if the result is not significant, collect more data and analyse
again. Uniquely dangerous because it is invisible in the final dataset: the
published N looks like a design choice. With enough peeks the rejection rate
approaches 1.

### 4. Outlier exclusion
Apply an outlier rule, and if the result is not significant, apply a different
one. There are many defensible rules — 2/2.5/3 SD, 1.5/3 IQR, MAD, percentile
trims, Cook's distance, studentised residuals — and the researcher need only
report the one used.

### 5. Controlling for covariates
Add, drop, or recombine control variables. Weak per attempt when covariates are
mildly correlated with the outcome, but the *number* of combinations grows as
2^k, so a pool of ten controls is a thousand analyses.

### 6. Scale redefinition
Drop items from a composite index until it "performs". In economics: change
which components enter a welfare index, a governance score, or a poverty
measure.

### 7. Variable transformation
Levels, logs, square roots, ranks, inverses, standardised, winsorised. Each
pairing of an outcome transform with a treatment transform is another test.
Among the strongest single strategies in the simulations, because transforms
change the estimand rather than merely re-weighting the same one.

### 8. Discretising a continuous variable
Median splits, terciles, "high vs low", extreme-group comparisons. Each cutoff
is a fresh test, and the extreme-group split additionally throws away the middle
of the distribution, which raises the apparent effect size. In the grid engine
these are treatment transforms (`median_split`, `above_mean`, `quartile_top`,
`tercile_extremes`); the last is flagged.

### 9. Exploiting alternative hypothesis tests
Student vs Welch, parametric vs rank-based, OLS vs GLM vs quantile, robust vs
clustered vs bootstrap standard errors. Each is defensible; together they are a
menu.

### 10. Favourable imputation
Listwise deletion, mean, median, hot-deck, regression imputation, multiple
imputation with different models. With non-trivial missingness the choice moves
estimates materially, and the choice is rarely reported.

### 11. Subgroup analysis
Run within levels of a moderator. Cheap, unlimited, and the one strategy that
comes with a ready-made narrative ("the effect is concentrated among…").

### 12. Incorrect rounding
Report p = .054 as "p < .05", or as "marginally significant". Small in
isolation — it raises the effective α from .05 to whatever the researcher is
willing to round from — but it applies at *every* stage of any other strategy
and so compounds with all of them.

### Compounding
Applied in sequence, these do not simply add. Marginal returns fall sharply
after the first two or three strategies, because a search that has already
failed on the easy margins has partly exhausted the noise. In our simulation,
a five-strategy workflow on a true null moves the rejection rate from 0.05 to
roughly 0.5. Reproduce with:

```bash
python scripts/phack_cli.py simulate --workflow \
  09_alternative_tests,01_selective_dv,05_covariates,11_subgroup,04_outlier_exclusion
```

---

## Layer 2 — econometrics-specific degrees of freedom

These are not in the psychology compendium, and they are where design-based
empirical economics actually bends. Brodeur, Cook & Heyes (2020) find the
inflation is concentrated in IV and DiD, and is far smaller in RCT and RDD —
consistent with which of these hands the analyst the most knobs.

### 13. Standard-error doctrine
The single largest and most under-policed source of movement in a t-statistic.
Classical, HC0–HC3, cluster at unit / group / region / two-way, Driscoll–Kraay,
Conley spatial, wild cluster bootstrap. Changing the clustering level can move a
p-value by an order of magnitude without touching the point estimate, and
"cluster at the level of treatment assignment" leaves genuine ambiguity when
treatment varies at several levels.

**Failure mode worth naming:** the two-way cluster variance estimator is not
guaranteed positive semi-definite. A search over SE choices will find the
non-PSD corner and return an implausibly small standard error. That is not a
clever specification; it is a broken one. `phack search` flags it
(`flag_nonpsd_vcov`) rather than letting it win.

### 14. Fixed-effect structure
None, unit, time, unit + time, unit × time trends, region × time, industry ×
year. Each is defensible; each changes the identifying variation.

### 15. Sample window and composition
Start year, end year, balanced vs unbalanced panel, dropping crisis years,
dropping small units, dropping never-treated or always-treated units,
restricting to a "clean" control group.

### 16. Bandwidth and kernel (RDD)
Bandwidth (IK, CCT, manual multiples of an optimal choice), kernel
(triangular / uniform / epanechnikov), polynomial order, donut radius, whether
to bias-correct, whether to use robust confidence intervals. The Cartesian
product runs to hundreds of specifications, all citable. This is the design the
Stanford agent evaluation found most susceptible after selection-on-observables.

### 17. Instrument set and first-stage specification (IV)
Which instruments, how many, interacted with what, included vs excluded
controls, LIML vs 2SLS vs JIVE, whether to report weak-instrument-robust
inference. Weak instruments make the second stage extraordinarily sensitive, and
the first-stage F is itself a searchable object.

### 18. Estimator choice under staggered treatment (DiD)
TWFE, Callaway–Sant'Anna, Sun–Abraham, Borusyak–Jaravel–Spiess, de
Chaisemartin–D'Haultfœuille, stacked, imputation. These genuinely differ under
heterogeneous effects, which is exactly what makes choosing among them *after*
seeing results so effective.

### 19. Event-window and reference-period choice (event study)
How many leads and lags, which period is omitted, whether to bin endpoints.
Moving the reference period alone can flip the sign of a pre-trend. The
engine walks `event_windows` × `reference_periods` × `event_estimands`
(average post-period effect, a single lag, or the pre-trend as a placebo)
with binned endpoints; `eval/data/null_staggered_event_card.json` is the
ground-truth grid, and reporting the pre-trend as the effect is flagged.

### 20. Donor pool and pre-period (synthetic control)
Which units are eligible donors, how long the pre-period is, which predictors
are matched, how they are weighted.

### 21. Weighting
Unweighted, population weights, inverse-probability weights, survey weights,
trimmed weights. Rarely pre-specified, frequently decisive.

### 22. Outcome timing and aggregation
Contemporaneous vs lagged vs cumulative outcome, monthly vs quarterly vs annual
aggregation, level vs growth rate. In panel work this is a large and largely
undisclosed space.

### 23. Inference mode mismatch (RDD)
Calonico, Cattaneo & Titiunik (2014) showed that the conventional local-linear
confidence interval under-covers because the bias is first-order, and proposed
bias-correcting the point estimate *and* inflating the variance to account for
the correction. Reporting the bias-corrected point estimate with the
**conventional** standard error takes the estimate shift without the variance
penalty. It is citable — "we bias-correct following CCT" — and it is the
single most productive lever in the null-RDD grid: every significant
specification in `eval/data/null_rdd` uses it. `rdd_inference:
bias_corrected` is in the grid and carries `flag_bc_without_robust_se`.

### 24. First-stage screening (IV)
Report only specifications whose first-stage F clears 10 — or choose the
instrument subset by its F. Conditioning on the first stage invalidates the
second-stage inference that is then reported (Andrews, Stock & Sun 2019). The
Anderson–Rubin test is the weak-instrument-robust statement that a search
cannot inflate by conditioning on the first stage; the engine records it per
specification and flags specifications where Wald rejects but AR does not
(`flag_ar_disagrees`).

### 25. Comparison-group composition (staggered DiD)
Dropping never-treated units ("we focus on adopters"), dropping always-treated
units, or restricting to not-yet-treated controls. Each changes which 2×2
comparisons enter the estimate; under heterogeneous dynamics they disagree by
construction (Goodman-Bacon 2021). `comparison_groups` is an axis, and in the
staggered null grid it has the largest spread of any axis.

---

---

## Layer 3 — the procedure

A strategy says *which* knob is turned. A procedure says *in what order, and
when to stop*. Both matter for the false-positive rate and for what gets
reported (Stefan & Schönbrodt, section 6; Simonsohn et al. 2020 on "first
significant" vs "most significant"):

| procedure | what it models | on the null panel (25,920 specs, one-sided) |
|---|---|---|
| exhaustive | a multiverse; ambitious hacking | min-p over 400 specs: median null p ≈ 0.02 |
| first significant | modest hacking: stop at the first p < α | FPR ≈ the share of null datasets with any significant spec in the first *budget* tried |
| greedy coordinate descent | "try the clustering… now the controls… now the window", from the pre-registered spec | reports p < .05 on ≈ 55% of null datasets after ≈ 28 specifications |
| hill climb | an agent iterating on a script | see `phack search --procedure hill_climb` |

The procedures are implemented in `scripts/phack/procedures.py` and replayed
on null data by `search.null_calibration`; `09-search-procedures` explains
how to read the result.

## Layer 4 — between stages: continuation and concealment

Research runs in stages: a pilot and a confirmatory study; an exploratory
regression and the one in the paper; phase II and phase III. Adda, Decker &
Ottaviani (2020) show on 12,621 registered clinical-trial results that the
share significant rises from 46% to 71% between phases for industry sponsors
with **no** discontinuity at z = 1.96 in the earlier stage, because sponsors
continue only after promising early results. Two strategies live here, and
only one of them is p-hacking.

### 26. Selective continuation
Run the pilot; continue to the confirmatory stage only if the pilot is
promising. With a **fresh** confirmatory sample the confirmatory test keeps
its size — the false-positive rate stays at α among the projects that
continue — and the population of confirmatory results is nonetheless shifted
toward significance, because true effects are heterogeneous and the rule
selects on them. That is selection, not manipulation, and it is invisible to
every threshold test. It becomes p-hacking the moment the pilot is **pooled**
into the confirmatory test (the favourable pilot draw is inside the reported
statistic: optional stopping with one lenient look), or the **better** of the
stages is reported.

| `26_selective_continuation --report` | false-positive rate | pilots run per continued project |
|---|---|---|
| `main` (confirmatory sample alone) | **0.050** | 9.9 |
| `pooled` (pilot folded into the confirmatory test) | 0.170 | 9.9 |
| `best` (the better of pilot, confirmatory, pooled) | 0.581 | 9.9 |

4,000 simulations, pilot n = 50 per arm, confirmatory n = 100 per arm,
continuation at pilot p < 0.10, true effect zero, conditional on continuation.
`simulate.continuation_shift` is the population version with heterogeneous
effects; the engine walks the same structure on a real design as the
`split_sample` procedure (`09-search-procedures`), whose `holdout` stage is
the split-sample immunisation of `07-phack-immunization` and whose `pooled`
stage is its failure mode.

### 27. Selective reporting between stages
Run the confirmatory stage and register it only when it is significant. In
the paper this is what is left after continuation is accounted for: about 18
points of excess significance for small industry sponsors, with a
discontinuity of the phase III density at 1.96 that is a **level shift, not
a spike** — the results below the line are missing, not moved. Distinct from
strategy 12 (rounding) and from the base-layer strategies, all of which leave
a spike. `detect.density_jump_test` sees it; `detect.spike_test` tells it
from p-hacking; `detect.continuation_decomposition` quantifies it.

## How to use this taxonomy

- **To build a design card** (`02-forking-paths`): each strategy that plausibly
  applies becomes one axis of the grid.
- **To audit a paper** (`05-narrative-laundering`): each strategy is a question
  — "was this choice pre-specified, or arrived at?"
- **To score an agent** (`08-eval-harness`): which strategies did it reach for,
  and did it say so?

## Sources

Stefan, A. M. & Schönbrodt, F. D. (2023). Big little lies: a compendium and
simulation of p-hacking strategies. *Royal Society Open Science* 10:220346.
Reference implementation: `astefan1/phacking_compendium`.

Adda, J., Decker, C. & Ottaviani, M. (2020). P-hacking in clinical trials and
how incentives shape the distribution of results across phases. *PNAS*
117(24):13386–13392.

Simmons, Nelson & Simonsohn (2011); Gelman & Loken (2013); Brodeur, Cook &
Heyes (2020); Cameron, Gelbach & Miller (2011) on two-way clustering. Full list
in `references/literature.md`.
