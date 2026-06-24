# Glossary

Precise, one-paragraph definitions of the identification, inference, and
editorial terms used across AER-skills. Where a term has a canonical reference,
the bib key into [`../references.bib`](../references.bib) is given in
parentheses. Command-level usage is in the
[methods reference](./methods-reference.md).

The point of this page is disambiguation: many of these terms are used loosely
in seminars and precisely by referees. The referee's meaning is the one below.

---

### Anderson-Rubin (AR) confidence set
A confidence set for the IV coefficient obtained by inverting the AR test. It has
correct coverage *regardless of instrument strength*, so it is the recommended
primary inference for just-identified models instead of the 2SLS `t`-interval,
which over-rejects when instruments are weak (`andrews_stock_sun_2019`).

### Antecedents map
The table of the 3-6 closest prior papers — question, data, identification,
finding, and what each does not do — built before the introduction is drafted.
It is the evidence base for the value-added claim and the checklist a field
referee will run. See [`aer-literature`](../skills/aer-literature/SKILL.md).

### ATT(g,t) — group-time average treatment effect
The average treatment effect at calendar time `t` for the cohort first treated at
time `g`. Modern staggered-DiD estimators report ATT(g,t) and then *aggregate*
(simple, dynamic/event-study, or by group) rather than estimating a single
pooled coefficient (`callaway_santanna_2021`).

### Augmented synthetic control (ASCM)
A synthetic control that adds an outcome-model bias correction (e.g. ridge) so it
can be used even when the pre-treatment fit is imperfect, relaxing the strict
convex-hull requirement of classic SCM (`benmichael_feller_rothstein_2021`).

### Bartik / shift-share instrument
An instrument built as the inner product of pre-period exposure *shares* and
aggregate *shocks* (e.g. national industry growth × local industry mix).
Identification can rest on the shares or on the shocks being exogenous — see
*exogenous shares vs. exogenous shocks*.

### booktabs
The LaTeX table style (top/mid/bottom rules, **no vertical lines**) that is the
AER house convention. Captions go *above* tables and *below* figures. See
[`aer-tables-figures`](../skills/aer-tables-figures/SKILL.md).

### Citation integrity ledger
The per-reference verification record (existence, field accuracy, claim
accuracy, version, date checked) maintained alongside the bibliography. A
manuscript ships only when every row is all-yes; unverifiable entries are
removed, never kept on probability. The protocol exists because language
models fabricate plausible citations and misattribute findings to real
papers. See [`aer-literature`](../skills/aer-literature/SKILL.md).

### Claim-evidence map
The audit table pairing every empirical claim in the abstract, introduction,
and conclusion with the exhibit or citation that supports it. Claims with no
evidence pointer are rewritten or deleted; mechanism claims must be worded as
consistency, not identification. See
[`aer-consistency`](../skills/aer-consistency/SKILL.md).

### Cluster-robust standard errors (CRVE)
Standard errors that allow arbitrary within-cluster correlation. They are
asymptotically valid in the number of *clusters*, not observations, and are
anti-conservative (too small) when clusters are few or very unequal in size — use
the *wild cluster bootstrap* there (`cameron_gelbach_miller_2008`).

### Cross-subfield interest
The actual AER acceptance bar: whether economists *outside* the author's subfield
will read and cite the paper. Technical quality alone routes a paper to a field
journal or the AEJ family. See [`design-principles`](./design-principles.md).

### Data and Code Availability Policy (DCAP)
The AEA policy, enforced by the **AEA Data Editor**, requiring a deposited
replication package (data or access route, code, and a README that runs) before
publication. See [`aer-replication`](../skills/aer-replication/SKILL.md).

### Desk rejection
Rejection by the editor without external review, typically within days. At AER it
is common; at AER: Insights roughly 45% of submissions. The first three pages and
the identification strategy decide it.

### Desk screen
The simulated version of the editor's first pass — ten minutes, first three
pages, main tables, bibliography — run internally before submission as Stage 1
of [`aer-referee-sim`](../skills/aer-referee-sim/SKILL.md). A failed desk
screen ends the run; referee reports are only simulated for drafts that pass.

### Donut RDD
A regression discontinuity that drops observations in a small window *exactly* at
the cutoff, to test whether the estimate is driven by bunching or manipulation
right at the threshold.

### Doubly robust (DR)
An estimator combining an outcome model and a propensity/weighting model that is
consistent if *either* model is correctly specified. The default `est_method`
for Callaway-Sant'Anna DiD (`callaway_santanna_2021`).

### Effective F (Montiel Olea-Pflueger)
A weak-instrument test statistic valid under heteroskedastic, clustered, or
autocorrelated errors — unlike the classic first-stage `F` and Stock-Yogo
critical values, which assume homoskedasticity (`montielolea_pflueger_2013`).

### Event-study plot
A plot of dynamic treatment-effect coefficients against time-relative-to-
treatment, with the period before treatment (`e = -1`) normalized to zero. Under
staggered adoption it must come from a heterogeneity-robust estimator, not from
TWFE leads and lags.

### Exclusion restriction
The assumption that the instrument affects the outcome *only* through the
endogenous regressor. It is defended by institutional argument and placebo
evidence, never by a statistical test; sensitivity to small violations is
quantified by *plausibly exogenous* bounds (`conley_hansen_rossi_2012`).

### Exogenous shares vs. exogenous shocks
The two mutually exclusive identification routes for a shift-share design.
*Exogenous shares*: the pre-period exposure shares are conditionally as-good-as-
random; diagnose with Rotemberg weights (`goldsmithpinkham_sorkin_swift_2020`).
*Exogenous shocks*: the aggregate shocks are as-good-as-random; do shock-level
inference (`borusyak_hull_jaravel_2022`, `adao_kolesar_morales_2019`).

### Forbidden comparison
In TWFE DiD with staggered timing, a 2×2 comparison that uses *already-treated*
units as controls for *newly-treated* units. When effects are dynamic, these
comparisons receive negative weight and can flip the sign of the estimate; the
*Goodman-Bacon decomposition* quantifies their weight (`goodmanbacon_2021`).

### Fuzzy RDD
A regression discontinuity where crossing the cutoff changes the *probability* of
treatment rather than treatment itself; estimated by IV, scaling the outcome jump
by the first-stage treatment jump.

### Generalized synthetic control (GSC)
An interactive-fixed-effects extension of SCM that handles multiple treated units
and estimates latent factors from the control pool (`xu_2017`).

### Goodman-Bacon decomposition
A decomposition of the TWFE DiD coefficient into a weighted average of all
underlying 2×2 comparisons, exposing how much weight comes from *forbidden
comparisons* (`goodmanbacon_2021`).

### Headline-number register
The audit table listing every number that appears more than once in the
manuscript, its single source of truth (table or replication output), and
each location quoting it. Prose must match tables to the digit; the abstract,
introduction, and conclusion must quote the same headline specification. See
[`aer-consistency`](../skills/aer-consistency/SKILL.md).

### Honest DiD (Rambachan-Roth)
A sensitivity analysis that replaces the untestable exact-parallel-trends
assumption with a bounded one — either *relative magnitudes* (post-trend
violation no larger than `M̄` × the worst pre-trend) or *smoothness* — and reports
the robust confidence set as a function of that bound (`rambachan_roth_2023`).

### Imputation estimator (Borusyak-Jaravel-Spiess)
A staggered-DiD estimator that fits the untreated-potential-outcome model on
not-yet-treated observations, imputes the counterfactual, and is efficient under
homoskedasticity (`borusyak_jaravel_spiess_2024`).

### Interaction-weighted estimator (Sun-Abraham)
An event-study estimator that interacts relative-time dummies with cohort
indicators and aggregates with proper weights, avoiding the contamination of
TWFE event-study coefficients (`sun_abraham_2021`).

### Local-linear regression (RDD)
The modern RDD workhorse: a first-order polynomial fit on each side of the cutoff
within an MSE-optimal bandwidth, usually with a triangular kernel that puts most
weight near the threshold (`calonico_cattaneo_titiunik_2014`).

### Manipulation / density test
A test for sorting around the RDD cutoff: if the density of the running variable
jumps at the threshold, units may be manipulating their assignment. Use the
local-polynomial density test (`cattaneo_jansson_ma_2020`), which supersedes the
original McCrary binned estimator (`mccrary_2008`).

### MSE-optimal bandwidth
The bandwidth that minimizes the mean squared error of the local-linear RDD
estimator; paired with a *robust bias-corrected* confidence interval so that the
optimal bandwidth does not invalidate inference (`calonico_cattaneo_titiunik_2014`).

### Multiple-hypothesis correction
Adjustment of p-values or confidence levels when several outcomes/subgroups are
tested, controlling the family-wise error rate (FWER) or false discovery rate
(FDR). Required when a paper reports many primary outcomes.

### Not-yet-treated control group
Using units that *will* be treated later (but are untreated now) as the
comparison group, which avoids the forbidden comparisons that arise from using
already-treated units as controls.

### openICPSR
The AEA's deposit repository for replication packages. The deposit is reviewed by
the AEA Data Editor against the *DCAP*. See
[`aer-replication`](../skills/aer-replication/SKILL.md).

### Oster's δ (coefficient stability)
A bounding method for omitted-variable bias that asks how strong selection on
unobservables would have to be (relative to observables, `δ`) to explain away the
result — scaling coefficient movement by the accompanying R² movement, not by
coefficient movement alone (`oster_2019`).

### Parallel trends (conditional)
The DiD identifying assumption: absent treatment, treated and control groups
would have followed the same outcome path (possibly after conditioning on
covariates). It is fundamentally untestable; pre-trends and Honest DiD probe it.

### Permutation / Fisher-exact inference
Inference based on re-randomizing or re-assigning treatment across units and
comparing the actual statistic to the resulting null distribution. Standard for
synthetic control (in-space placebo) and randomization inference in experiments.

### Plausibly exogenous (Conley-Hansen-Rossi)
A sensitivity framework for IV that relaxes the exclusion restriction by allowing
the instrument a *bounded* direct effect on the outcome and reporting how the
result changes across that bound (`conley_hansen_rossi_2012`).

### Pre-analysis plan (PAP)
A pre-registered specification of outcomes, subgroups, and the estimating
equation, filed (for AEA-journal field experiments) with the **AEA RCT Registry**
before unblinding. Keeps confirmatory analysis distinct from exploratory.

### Pre-trends joint test
A single test of the joint null that *all* pre-treatment event-study coefficients
equal zero — more informative than eyeballing the plot, but still low-powered,
which is why it is paired with Honest DiD (`roth_2022`).

### Quality gates
The pass/fail checkpoints that order end-to-end drafting in
[`aer-workflow`](../skills/aer-workflow/SKILL.md): design survives
identification review before prose; every claim traces to evidence before the
introduction; the consistency audit and citation ledger close before the
referee simulation; the simulated verdict reaches major R&R before
submission. A failed gate blocks advancement — it does not get noted and
passed.

### Referee simulation
The adversarial internal review of a finished draft: a desk screen plus three
independently drafted referee reports with distinct priors (identification
specialist, field expert, generalist), scored on the
[referee report rubric](./referee-report-rubric.md). Its only export is the
routed revise list; simulated praise certifies nothing. See
[`aer-referee-sim`](../skills/aer-referee-sim/SKILL.md).

### Robust bias-corrected (RBC) confidence interval
The RDD confidence interval that recenters for the bias introduced by the
MSE-optimal bandwidth and inflates the variance accordingly; the `rdrobust`
default (`calonico_cattaneo_titiunik_2014`).

### Rotemberg weights
The weights that reveal which exposure *shares* drive a Bartik/shift-share
estimate. Reporting them — and inspecting the top-weighted shares for
plausibility — is the key diagnostic under the exogenous-shares interpretation
(`goldsmithpinkham_sorkin_swift_2020`).

### Sharp RDD
A regression discontinuity where treatment is a *deterministic* step function of
the running variable at the cutoff (everyone above is treated, everyone below is
not).

### Specification curve
A display of the estimate across the full set of defensible analytic choices,
converting "you picked your specification" into a visible distribution of results
(`simonsohn_simmons_nelson_2020`).

### Synthetic difference-in-differences (SDID)
An estimator that combines synthetic-control unit weights with DiD time weighting,
relaxing both the parallel-trends assumption of DiD and the perfect-pre-fit
requirement of SCM (`arkhangelsky_etal_2021`).

### tF adjustment
A correction that maps the just-identified IV `t`-ratio to a weak-IV-robust
critical value (popularized as the "use `|t| > 3`, not `1.96`" rule), giving
correct size without computing the full AR set (`lee_mccrary_moreira_porter_2022`).

### TWFE (two-way fixed effects)
The regression of an outcome on a treatment dummy with unit and time fixed
effects. Unbiased for a single simultaneous treatment with homogeneous effects;
biased — sometimes sign-flipped — under staggered timing with dynamic effects
(`dechaisemartin_dhaultfoeuille_2020`).

### Weak instrument
An instrument only mildly correlated with the endogenous regressor, which biases
2SLS toward OLS and destroys the size of conventional `t`-tests. Diagnosed with
the *effective F* and handled with *AR* / *tF* inference, not the `F > 10` rule
of thumb.

### Wild cluster bootstrap
A bootstrap that resamples cluster-level residual signs to produce p-values and
confidence intervals valid with *few* or *unequal* clusters, where cluster-robust
SEs fail (`cameron_gelbach_miller_2008`, `mackinnon_webb_2017`).

---

*See the [methods reference](./methods-reference.md) for the command that
implements each term and the [pre-submission audit](./desk-rejection-audit.md)
for how a missing diagnostic turns into a desk rejection.*
