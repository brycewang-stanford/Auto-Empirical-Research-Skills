# Methods Reference

A single-page, citation-backed quick reference for the modern identification and
inference defaults assumed throughout AER-skills. It complements the prose in
[`aer-identification`](../skills/aer-identification/SKILL.md) and
[`aer-robustness`](../skills/aer-robustness/SKILL.md): the skills tell you *what*
design to defend and *how* to write it up; this page gives you the *estimator,
the exact command in each supported stack, the required diagnostics, and the
citation* to put in your paper.

- Every paper named here is in [`../references.bib`](../references.bib) with a
  Crossref-verified DOI. Cite by the bib key shown in the **Cite** column.
- The runnable, end-to-end versions live in the templates:
  [Stata](../templates/stata/03_main_did.do) ·
  [R](../templates/r/03_main_did.R) ·
  [Python](../templates/python/main_did.py).
- Terms in *italics* are defined in the [glossary](./glossary.md).
- "—" means no production-grade package exists in that language yet; export the
  estimation step to the language that does (usually R), or treat it as a
  known limitation.

---

## The one-line rule

> Match the estimator to the *variation that identifies the effect*, then report
> the diagnostic that would expose the estimator if it were wrong. A result that
> survives its own most dangerous diagnostic is publishable; one that dodges it
> is not.

The 1990s defaults below are not "wrong everywhere" — they are wrong in exactly
the settings that dominate modern applied work (staggered rollout, heterogeneous
effects, weak instruments, manipulable thresholds).

| Setting | 1990s default | Modern default | Why the default flips | Cite |
|---|---|---|---|---|
| Staggered DiD | TWFE with a single `treat` dummy | Callaway-Sant'Anna / BJS / Sun-Abraham | TWFE is a *forbidden-comparison*-weighted average that can sign-flip | `goodmanbacon_2021`, `dechaisemartin_dhaultfoeuille_2020` |
| Parallel trends | "pre-trends look flat" | Joint pre-test **+** Honest DiD bounds | A flat pre-trend is low-power, not proof | `roth_2022`, `rambachan_roth_2023` |
| Just-identified IV | first-stage `F > 10` | *Anderson-Rubin* CI; *effective F* | `F>10` controls bias, not the size of the `t`-test | `montielolea_pflueger_2013`, `lee_mccrary_moreira_porter_2022` |
| Shift-share | "the Bartik instrument is exogenous" | Pick *exogenous shares* **or** *exogenous shocks* | The two require different, non-overlapping assumptions | `goldsmithpinkham_sorkin_swift_2020`, `borusyak_hull_jaravel_2022` |
| RDD | 4th-order global polynomial | Local-linear, MSE-optimal bandwidth, RBC CI | High-order polynomials put huge weight at the boundary | `gelman_imbens_2019`, `calonico_cattaneo_titiunik_2014` |
| SCM | "the synthetic unit tracks well" | Placebo/permutation inference | Visual fit is not inference | `abadie_diamond_hainmueller_2010`, `abadie_2021` |
| Few clusters | cluster-robust SE | *Wild cluster bootstrap* | Cluster-robust SEs are anti-conservative with few clusters | `cameron_gelbach_miller_2008`, `mackinnon_webb_2017` |
| OVB defense | "results hold with controls" | *Oster* δ / bounding | Coefficient stability must be scaled by R² movement | `oster_2019` |

---

## 1. Difference-in-differences (staggered adoption)

**Primary estimator: Callaway & Sant'Anna (2021)** — group-time ATT(g,t),
doubly robust, not-yet-treated controls. This is the estimator the templates
implement in all three languages.

| Stack | Install | Canonical call |
|---|---|---|
| Stata | `ssc install csdid drdid` | `csdid y x, ivar(id) time(t) gvar(first_treat) method(dripw)` then `estat event` |
| R | `install.packages("did")` | `att_gt(yname="y", tname="t", idname="id", gname="first_treat", est_method="dr", control_group="notyettreated")` → `aggte(..., type="dynamic")` |
| Python | `pip install differences` | `ATTgt(data=panel, cohort_column="first_treat").fit(formula="y ~ x", control_group="not_yet_treated")` |

**Alternative estimators (report at least one as a robustness row):**

| Estimator | Stata | R | Python | Cite |
|---|---|---|---|---|
| Imputation (efficient under homoskedasticity) | `did_imputation` | `didimputation::did_imputation` / `did2s::did2s` | `pyfixest` `did2s` | `borusyak_jaravel_spiess_2024` |
| Interaction-weighted event study | `eventstudyinteract` | `fixest::sunab` | `pyfixest` `i(t, treat, ref)` | `sun_abraham_2021` |
| Multiple groups & periods | `did_multiplegt` / `did_multiplegt_dyn` | `DIDmultiplegtDYN` | — | `dechaisemartin_dhaultfoeuille_2020` |

**Required diagnostics** (see [`03_main_did`](../templates/stata/03_main_did.do)):

1. **Goodman-Bacon decomposition** — report the share of weight from forbidden
   (already-treated-as-control) comparisons. `bacondecomp` (Stata) · `bacondecomp::bacon` (R) · — (Python: run in R). `goodmanbacon_2021`
2. **Event-study plot** from the CS/BJS/SA estimator, *not* from TWFE leads/lags.
3. **Joint pre-trends test** (p-value), not just the eyeball. `roth_2022`
4. **Honest DiD sensitivity** — relative-magnitudes or smoothness bounds on the
   post-period effect. `honestdid` (Stata) · `HonestDiD` (R) · — (Python: export
   `betahat`/`sigma` to R). `rambachan_roth_2023`

> Single treatment date, never-treated controls, homogeneous effects plausible?
> Then — and only then — TWFE 2×2 is fine. Everything else needs a heterogeneity-
> robust estimator. Synthesis and decision rules: `roth_santanna_bilinski_poe_2023`.

---

## 2. Instrumental variables

**Weak instruments.** The first-stage `F > 10` rule controls *relative bias*, not
the *size* of the second-stage `t`-test. Report:

- **Effective F** (Montiel Olea-Pflueger) — valid under heteroskedastic /
  clustered / autocorrelated errors. Stata `weakivtest` · R `ivDiag::ivDiag` ·
  Python compute from `linearmodels` output. `montielolea_pflueger_2013`
- **Anderson-Rubin confidence set** as the *primary* inference for
  just-identified models — correct size for any instrument strength. Stata
  `weakiv` / `ivreg2` post-estimation · R `ivDiag` · Python `linearmodels`
  `.first_stage`/Wald inversion. `andrews_stock_sun_2019`
- For the just-identified case, the `tF` adjustment turns the usual `t`-ratio
  into a weak-IV-robust one (the "`|t|>3`" rule). `lee_mccrary_moreira_porter_2022`
- Stock-Yogo critical values assume homoskedasticity and rarely apply to
  modern clustered designs. `stock_yogo_2005`

| Stack | Install | Just-identified IV with FE |
|---|---|---|
| Stata | `ssc install ivreg2 ranktest weakivtest` | `ivreghdfe y x (d = z), absorb(id t) cluster(id)` then `weakivtest` |
| R | `install.packages("fixest")` | `feols(y ~ x | id + t | d ~ z, data=...)`; diagnostics via `ivDiag::ivDiag` |
| Python | `pip install linearmodels` | `IV2SLS.from_formula("y ~ 1 + x + [d ~ z]", data).fit(cov_type="clustered", clusters=df.id)` |

**Exclusion restriction** is defended with a *story*, not a test. State it in one
sentence in the introduction and back it with (i) an institutional narrative,
(ii) a placebo where the instrument should not predict the outcome, and (iii) a
*plausibly-exogenous* sensitivity bound (`conley_hansen_rossi_2012`).

---

## 3. Shift-share / Bartik

Two **mutually exclusive** identification stories. Pick one and report its
diagnostics — do not hand-wave between them.

| Identification | Assumption | Report | Cite |
|---|---|---|---|
| Exogenous **shares** | pre-period exposure shares are conditionally as-good-as-random | *Rotemberg weights*; inspect the top-5 shares driving identification | `goldsmithpinkham_sorkin_swift_2020` |
| Exogenous **shocks** | the aggregate shocks are as-good-as-random | shock-level (not region-level) inference; effective number of shocks | `borusyak_hull_jaravel_2022`, `adao_kolesar_morales_2019` |

Tooling: R `bartik.weight` (GPSS Rotemberg weights) and the shock-level SE
formulas in the BHJ / AKM replication code; Stata implementations exist via the
authors' packages. There is no single canonical Python package — port the
weight/inference step from the authors' R code.

---

## 4. Regression discontinuity

**Estimator: local-linear, triangular kernel, MSE-optimal bandwidth, robust
bias-corrected (RBC) confidence interval** — i.e. `rdrobust` defaults. High-order
global polynomials are discouraged (`gelman_imbens_2019`).

| Stack | Install | Canonical call |
|---|---|---|
| Stata | `ssc install rdrobust rddensity` | `rdrobust y x, c(0) p(1) kernel(triangular) bwselect(mserd)` |
| R | `install.packages(c("rdrobust","rddensity"))` | `rdrobust(y, x, c = 0, p = 1, kernel = "triangular", bwselect = "mserd")` |
| Python | `pip install rdrobust rddensity` | `rdrobust(y, x, c=0, p=1, kernel="triangular", bwselect="mserd")` |

**Required diagnostics:** `calonico_cattaneo_titiunik_2014`

1. **Manipulation / density test** at the cutoff — `rddensity` (local-polynomial
   density, preferred over the original `DCdensity`). `cattaneo_jansson_ma_2020`, `mccrary_2008`
2. **Covariate balance** at the cutoff (predetermined covariates as placebo
   outcomes).
3. **Placebo cutoffs** away from the true threshold.
4. **Bandwidth sensitivity** — estimate across ≥ 3 bandwidths around `mserd`.
5. **RD plot** with an explicit, stated binning method (`rdplot`).
6. **Donut RDD** if there is bunching immediately at the cutoff.

---

## 5. Synthetic control

For one or a few treated units with a long pre-period and a clean donor pool.

| Estimator | When | Stata | R | Cite |
|---|---|---|---|---|
| Classic SCM | one treated unit | `synth` / `synth2` | `Synth` | `abadie_diamond_hainmueller_2010`, `abadie_gardeazabal_2003` |
| Generalized SCM | several treated units, IFE | — | `gsynth::gsynth` | `xu_2017` |
| Augmented SCM | poor pre-fit / bias correction | — | `augsynth::augsynth` | `benmichael_feller_rothstein_2021` |
| Synthetic DiD | SCM × DiD weighting | — | `synthdid::synthdid_estimate` | `arkhangelsky_etal_2021` |

**Required diagnostics** (`abadie_2021` is the practitioner's checklist):

1. **In-space placebo** — apply SCM to every donor; report the distribution of
   placebo effects and the treated unit's rank.
2. **In-time placebo** — fake pre-treatment intervention dates.
3. **Permutation / Fisher exact p-value** from the placebo distribution.
4. **Weight vector** in the appendix; discuss any donor with > 10% weight.

---

## 6. Inference and sensitivity (applies to all designs)

| Concern | Fix | Stata | R | Python | Cite |
|---|---|---|---|---|---|
| Few clusters (< ~50) | wild cluster bootstrap | `boottest` | `fwildclusterboot` | `wildboottest` | `cameron_gelbach_miller_2008`, `mackinnon_webb_2017` |
| Unequal cluster sizes | wild bootstrap (not CRVE) | `boottest` | `fwildclusterboot` | `wildboottest` | `mackinnon_webb_2017` |
| Many hypotheses | FWER / FDR control | `wyoung` | `multcomp`, `fixest` | `statsmodels` `multipletests` | `roth_santanna_bilinski_poe_2023` |
| Omitted-variable bias | Oster δ bounding | `psacalc` | `robomit` | — | `oster_2019` |
| "Researcher-chose-the-spec" | specification curve | `speccurve` | `specr` | — | `simonsohn_simmons_nelson_2020` |

See [`aer-robustness`](../skills/aer-robustness/SKILL.md) for *which* of these a
referee will demand, and [`04_robustness`](../templates/stata/04_robustness.do)
for a worked battery.

---

## Reporting checklist (paste into the appendix plan)

- [ ] Main estimator is heterogeneity-robust (not TWFE) where the design is staggered
- [ ] Goodman-Bacon weight on forbidden comparisons reported
- [ ] Event-study plot from the robust estimator, with a joint pre-trends p-value
- [ ] Honest DiD (or design-appropriate) sensitivity bounds reported
- [ ] IV: effective F **and** an Anderson-Rubin / `tF` weak-IV-robust CI
- [ ] Shift-share: exogenous-shares **or** exogenous-shocks story chosen and diagnosed
- [ ] RDD: density test, covariate balance, placebo cutoffs, bandwidth grid
- [ ] SCM: in-space + in-time placebo and a permutation p-value
- [ ] Inference matched to the cluster structure (wild bootstrap if few clusters)
- [ ] Every method above cited to `../references.bib`, not to a textbook

---

*Worked, paper-grade applications of each design are catalogued in
[`examples/modern-aer-exemplars.md`](../examples/modern-aer-exemplars.md). The
opinions behind these defaults are in [`design-principles.md`](./design-principles.md).*
