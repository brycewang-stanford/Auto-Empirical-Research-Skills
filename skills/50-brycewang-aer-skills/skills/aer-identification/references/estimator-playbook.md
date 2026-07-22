# Estimator Playbook

*Bundled with the `aer-identification` skill so the playbook works without the repository checkout. SKILL.md routes; this file carries the depth.*

One rule governs everything below: match the estimator to the variation that identifies the effect, then report the diagnostic that would expose the estimator if it were wrong. Each section gives the estimand, the modern default with exact calls, the diagnostics a referee will demand, the correct inference, response scripts for the most common objections, and a do-not list.

---

## 1. Staggered difference-in-differences

**Estimand.** ATT(g,t): the average treatment effect on the treated for adoption cohort g at calendar time t, aggregated to event-time or an overall ATT.

**Default estimator.** Callaway and Sant'Anna (2021): doubly robust ATT(g,t) with not-yet-treated controls.

| Stack | Call |
|---|---|
| Stata | `ssc install csdid drdid` then `csdid y x, ivar(id) time(t) gvar(first_treat) method(dripw)` then `estat event` |
| R | `did::att_gt(yname="y", tname="t", idname="id", gname="first_treat", est_method="dr", control_group="notyettreated")` then `aggte(..., type="dynamic")` |
| Python | `pip install differences`; `ATTgt(data=panel, cohort_column="first_treat").fit(formula="y ~ x", control_group="not_yet_treated")` |

Report at least one alternative estimator as a robustness row: imputation per Borusyak, Jaravel, and Spiess (2024) (`did_imputation` in Stata, `didimputation` or `did2s` in R, `did2s` in `pyfixest`), or `did_multiplegt` per de Chaisemartin and D'Haultfoeuille (2020).

**Required diagnostics.**

- [ ] Goodman-Bacon decomposition: share of TWFE weight on forbidden already-treated comparisons (`bacondecomp` in Stata, `bacondecomp::bacon` in R; run in R from Python)
- [ ] Event-study plot from the robust estimator, never from TWFE leads and lags
- [ ] Joint pre-trends test reported as a p-value, not an eyeball (Roth (2022))
- [ ] Honest DiD relative-magnitude or smoothness bounds (`honestdid` in Stata, `HonestDiD` in R; export `betahat` and `sigma` from Python)
- [ ] Heterogeneity by treatment cohort

**Inference.** Cluster at the level of treatment assignment. With fewer than roughly 50 clusters, wild cluster bootstrap (`boottest` / `fwildclusterboot` / `wildboottest`) per Cameron, Gelbach, and Miller (2008).

**Referee objections and response scripts.**

| Objection | Run | Reply sentence |
|---|---|---|
| "TWFE gives a different answer; which is right?" | Goodman-Bacon decomposition | "X% of the TWFE weight falls on forbidden already-treated comparisons, which explains the gap; the heterogeneity-robust estimate is the design-consistent one." |
| "The pre-trend test is underpowered" | Honest DiD bounds (Rambachan and Roth (2023)) | "The post-period effect remains bounded away from zero for violations up to M-bar = m of the largest pre-period deviation." |
| "Units anticipated treatment" | Re-estimate with anticipation periods (`anticipation` argument in `att_gt`) and a shifted treatment date | "Allowing k periods of anticipation leaves the dynamic path unchanged." |

**Do not.**

- Do not run TWFE with a single `treat` dummy on staggered data
- Do not use already-treated units as controls
- Do not declare parallel trends from a flat plot alone
- Do not aggregate cohorts without showing cohort-level heterogeneity

## 2. Canonical 2x2 difference-in-differences

**Estimand.** ATT for a single treated group at a single treatment date, in the mold of the minimum-wage design of Card and Krueger (1994).

**Default estimator.** TWFE is valid here, and only here: simultaneous treatment timing, never-treated controls, homogeneous effects plausible.

| Stack | Call |
|---|---|
| Stata | `reghdfe y i.treat#i.post, absorb(id t) vce(cluster id)` |
| R | `fixest::feols(y ~ treat:post \| id + t, data, cluster = ~id)` |
| Python | `pyfixest.feols("y ~ treat:post \| id + t", data, vcov={"CRV1": "id"})` |

**Required diagnostics.** Pre-period trend plot with CIs; joint pre-test if multiple pre-periods; a falsification outcome that should not respond.

**Inference.** Cluster at the treatment-assignment level; with one or two treated clusters, permutation or randomization inference, not cluster-robust SEs.

**Referee objections and response scripts.**

| Objection | Run | Reply sentence |
|---|---|---|
| "Only a handful of clusters" | Wild cluster bootstrap per MacKinnon and Webb (2017) | "Bootstrap p-values are reported in every table; conclusions are unchanged." |
| "Effects may be heterogeneous after all" | Re-estimate with a heterogeneity-robust estimator as a robustness row | "The 2x2 and robust estimates coincide, as the design implies." |

**Do not.** Do not stretch the 2x2 label over quietly staggered adoption; do not pick the control group after seeing outcomes.

## 3. Event studies (Sun-Abraham and imputation)

**Estimand.** Dynamic ATT by event time relative to adoption, purged of cross-cohort contamination.

**Default estimator.** Interaction-weighted event study per Sun and Abraham (2021), or the imputation estimator per Borusyak, Jaravel, and Spiess (2024) when efficiency matters.

| Stack | Call |
|---|---|
| Stata | `eventstudyinteract` (Sun-Abraham) or `did_imputation y id t first_treat, horizons(0/5) pretrend(5)` |
| R | `fixest::feols(y ~ sunab(first_treat, t) \| id + t, data)` or `did2s::did2s(...)` |
| Python | `pyfixest` `did2s` for imputation; `i(t, treat, ref=-1)` interactions for the saturated regression |

**Required diagnostics.** Joint test on all leads; explicit reference period and endpoint binning stated in the note; side-by-side contrast with the naive TWFE event study when the two disagree.

**Inference.** Cluster as in section 1; report simultaneous (not pointwise) confidence bands when the claim concerns the whole dynamic path.

**Referee objections and response scripts.**

| Objection | Run | Reply sentence |
|---|---|---|
| "Your leads and lags are contaminated" | Re-estimate with `sunab` or imputation | "All event-study figures use the interaction-weighted estimator, which is immune to cross-cohort contamination." |
| "Results hinge on the reference period" | Re-estimate with alternative reference periods | "Estimates are invariant to the choice of base period, as shown in the appendix." |

**Do not.** Do not assemble leads and lags by hand on staggered data; do not bin endpoints silently; do not test each lead separately and call it a joint test.

## 4. Instrumental variables (including weak-IV-robust inference)

**Estimand.** The LATE for compliers with the instrument, under monotonicity; the ATE only under effect homogeneity.

**Default estimator.** 2SLS with fixed effects, with weak-IV-robust inference reported alongside.

| Stack | Call |
|---|---|
| Stata | `ssc install ivreg2 ranktest weakivtest`; `ivreghdfe y x (d = z), absorb(id t) cluster(id)` then `weakivtest` |
| R | `fixest::feols(y ~ x \| id + t \| d ~ z, data)`; diagnostics via `ivDiag::ivDiag` |
| Python | `linearmodels`: `IV2SLS.from_formula("y ~ 1 + x + [d ~ z]", data).fit(cov_type="clustered", clusters=df.id)` |

**Required diagnostics.**

- [ ] Effective F per Montiel Olea and Pflueger (2013), valid under clustering, not the homoskedastic first-stage F
- [ ] Anderson-Rubin confidence set as primary inference for just-identified models (Andrews, Stock, and Sun (2019))
- [ ] First stage and reduced form shown in full
- [ ] Placebo outcome the instrument should not predict
- [ ] Plausibly-exogenous sensitivity bound per Conley, Hansen, and Rossi (2012)

**Inference.** AR confidence sets keep correct size at any instrument strength; the tF adjustment of Lee, McCrary, Moreira, and Porter (2022) rescales the usual t-ratio in the just-identified case. Stock and Yogo (2005) critical values assume homoskedasticity and rarely apply to clustered designs.

**Referee objections and response scripts.**

| Objection | Run | Reply sentence |
|---|---|---|
| "First-stage F of 12 is not strong" | `weakivtest` or `ivDiag`; add the AR set | "We report the effective F and take the Anderson-Rubin confidence set as primary inference, which is valid at any instrument strength." |
| "The exclusion restriction is untestable" | Instrument-on-placebo regression plus Conley-Hansen-Rossi bounds | "The conclusion survives direct effects of the instrument up to gamma = g, several times any plausible violation." |
| "The LATE is not the policy parameter" | Characterize compliers (covariate means by complier status) | "Compliers resemble the policy-relevant population on the observables that drive the mechanism." |

**Do not.** Do not cite F > 10 as evidence about test size; do not defend exclusion with "we control for X"; do not hide the reduced form.

## 5. Shift-share / Bartik

**Estimand.** The effect of an exposure-weighted aggregate shock; what is identified depends on which of two mutually exclusive assumptions you commit to.

**Default estimator.** Bartik IV in the 2SLS framework of section 4, with the identification route chosen explicitly.

| Route | Assumption | Report | Tooling |
|---|---|---|---|
| Exogenous shares (Goldsmith-Pinkham, Sorkin, and Swift (2020)) | Pre-period exposure shares conditionally as-good-as-random | Rotemberg weights; top-5 shares scrutinized | R `bartik.weight` |
| Exogenous shocks (Borusyak, Hull, and Jaravel (2022)) | Aggregate shocks as-good-as-random | Shock-level inference; effective number of shocks | Shock-level SE code from the BHJ and AKM replication files; no canonical Python package |

**Required diagnostics.** Rotemberg weights (shares route) or effective number of shocks and shock-level SEs (shocks route); pre-trends of outcomes against the instrument; balance of shares or shocks against predetermined characteristics.

**Inference.** Region-level clustering understates uncertainty when shocks are the identifying variation; use shock-level standard errors per Adao, Kolesar, and Morales (2019).

**Referee objections and response scripts.**

| Objection | Run | Reply sentence |
|---|---|---|
| "Which exogeneity assumption are you making?" | Commit to one route; run its diagnostics | "Identification comes from exogenous shocks; shares serve only as exposure weights, and inference is at the shock level." |
| "A few industries drive everything" | Rotemberg weight table | "The top-5 Rotemberg-weight shares are examined individually and none is confounded by the obvious alternative channel." |

**Do not.** Do not hand-wave between the shares and shocks stories; do not cluster only by region when shocks identify; do not omit the weight diagnostics.

## 6. Regression discontinuity

**Estimand.** The average effect at the cutoff (sharp), or the effect for cutoff compliers (fuzzy).

**Default estimator.** Local-linear regression, triangular kernel, MSE-optimal bandwidth, robust bias-corrected CI, i.e. the `rdrobust` defaults of Calonico, Cattaneo, and Titiunik (2014).

| Stack | Call |
|---|---|
| Stata | `ssc install rdrobust rddensity`; `rdrobust y x, c(0) p(1) kernel(triangular) bwselect(mserd)` |
| R | `rdrobust::rdrobust(y, x, c = 0, p = 1, kernel = "triangular", bwselect = "mserd")` |
| Python | `pip install rdrobust rddensity`; `rdrobust(y, x, c=0, p=1, kernel="triangular", bwselect="mserd")` |

**Required diagnostics.**

- [ ] Manipulation density test at the cutoff: `rddensity` (Cattaneo, Jansson, and Ma (2020)), preferred to the original test of McCrary (2008)
- [ ] Covariate balance at the cutoff, predetermined covariates as placebo outcomes
- [ ] Placebo cutoffs away from the true threshold
- [ ] Bandwidth sensitivity across at least three bandwidths around `mserd`
- [ ] RD plot via `rdplot` with the binning method stated
- [ ] Donut RDD if there is bunching immediately at the cutoff

**Inference.** The robust bias-corrected confidence interval, not the conventional one; cluster on the running variable only when it is discrete.

**Referee objections and response scripts.**

| Objection | Run | Reply sentence |
|---|---|---|
| "Agents manipulate the running variable" | `rddensity` plus a donut specification | "The density test does not reject (p = p), and the donut estimate excluding observations within h of the cutoff is unchanged." |
| "The bandwidth was chosen to get the result" | Estimate across a bandwidth grid | "The estimate is stable from half to twice the MSE-optimal bandwidth." |
| "Why not a global polynomial?" | Local-linear per Gelman and Imbens (2019) | "High-order global polynomials place extreme weight at the boundary; we follow the local-linear default throughout." |

**Do not.** Do not fit polynomials of order above 2; do not report a single hand-picked bandwidth; do not skip the density test because the plot "looks smooth".

## 7. Synthetic control

**Estimand.** The treated unit's post-period outcome gap relative to a weighted synthetic counterfactual built from the donor pool.

**Default estimator.** Classic SCM per Abadie, Diamond, and Hainmueller (2010); generalized SCM (`gsynth`) for several treated units per Xu (2017); augmented SCM (`augsynth`) for poor pre-fit per Ben-Michael, Feller, and Rothstein (2021); synthetic DiD (`synthdid`) per Arkhangelsky et al. (2021).

| Stack | Call |
|---|---|
| Stata | `synth` or `synth2` (classic SCM only) |
| R | `Synth`, `gsynth::gsynth`, `augsynth::augsynth`, `synthdid::synthdid_estimate` |
| Python | No production-grade package; export the estimation step to R |

**Required diagnostics.** The practitioner's checklist of Abadie (2021):

- [ ] In-space placebo: apply SCM to every donor; report the treated unit's rank in the placebo distribution
- [ ] In-time placebo: fake pre-treatment intervention dates
- [ ] Permutation (Fisher exact) p-value from the placebo distribution
- [ ] Weight vector in the appendix; discuss any donor above 10% weight

**Inference.** Permutation inference from the in-space placebo distribution; visual fit is not inference.

**Referee objections and response scripts.**

| Objection | Run | Reply sentence |
|---|---|---|
| "The synthetic unit tracks well, so what?" | Full in-space placebo distribution | "The treated unit's post/pre RMSPE ratio ranks 1st of N donors, a permutation p-value of 1/N." |
| "One donor drives the counterfactual" | Leave-one-out over high-weight donors | "Dropping each donor above 10% weight in turn leaves the gap intact." |
| "Pre-treatment fit is mediocre" | `augsynth` bias correction | "The augmented estimator corrects the pre-fit bias and delivers the same conclusion." |

**Do not.** Do not present SCM with no placebo inference; do not keep donors exposed to spillovers in the pool; do not tune the predictor set after seeing the post-period gap.

## 8. Randomized controlled trials

**Estimand.** ITT from random assignment; LATE under imperfect compliance with assignment as the instrument (section 4 machinery).

**Default estimator.** OLS of the outcome on assignment with randomization-strata fixed effects; ANCOVA with the baseline outcome when available (McKenzie (2012)).

| Stack | Call |
|---|---|
| Stata | `reghdfe y treat, absorb(strata) vce(cluster cluster_id)`; power via `power` and `clustersampsi` |
| R | `fixest::feols(y ~ treat \| strata, data, cluster = ~cluster_id)`; power via `pwr` |
| Python | `pyfixest.feols("y ~ treat \| strata", data)`; power via `statsmodels.stats.power` |

**Required diagnostics.**

- [ ] AEA RCT Registry registration and PAP posted before unblinding
- [ ] Balance table on baseline covariates by arm
- [ ] Attrition by arm, with Lee (2009) trimming bounds if differential (`leebounds`)
- [ ] MDE and power calculation in the manuscript or appendix (Duflo, Glennerster, and Kremer (2007))
- [ ] Multiple-hypothesis correction over the pre-specified outcome family (Romano and Wolf (2005); `wyoung` for the stepdown per List, Shaikh, and Xu (2019))

**Inference.** Cluster at the unit of randomization; randomization inference per Young (2019) (`ritest` in Stata, `ri2` in R) when N is small or leverage is concentrated.

**Referee objections and response scripts.**

| Objection | Run | Reply sentence |
|---|---|---|
| "Too many outcomes, some significance is chance" | Romano-Wolf stepdown over the pre-specified family | "All primary outcomes survive the Romano-Wolf FWER correction; exploratory outcomes are labeled as such." |
| "Differential attrition breaks randomization" | Lee trimming bounds | "The Lee bounds interval excludes zero, so attrition cannot account for the effect." |
| "The null arms are just underpowered" | Report the MDE against the CI | "The design had 80% power to detect an effect of size m, and the CI rules out effects above that magnitude." |

**Do not.** Do not report "not significant" as "no effect" without the MDE; do not mine subgroups outside the PAP without labeling them exploratory; do not ignore the design effect when assignment is clustered.

---

## Canonical repo sources

Distilled from these repository files, which require the repository checkout:

- `docs/methods-reference.md` (estimator defaults, package calls, diagnostics, citations)
- `skills/aer-identification/SKILL.md` (design decision tree, gates, handoff)
- `templates/stata/03_main_did.do`, `templates/r/03_main_did.R`, `templates/python/main_did.py` (runnable end-to-end implementations)
