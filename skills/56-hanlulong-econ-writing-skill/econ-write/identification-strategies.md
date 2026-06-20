# Writing by Identification Strategy

Different identification strategies and paper types require different narrative structures. Adapt your writing to the method.

---

## Randomized Controlled Trials (RCTs)
- Intuition: randomization makes treatment independent of potential outcomes, so treatment and control groups are comparable in expectation and a simple difference in means is unbiased for the average treatment effect
- Lead with the intervention and its policy relevance
- Describe randomization mechanism and balance tests early
- Emphasize intent-to-treat (ITT) as main specification; discuss compliance and LATE separately
- Address attrition and spillovers as primary threats to identification
- Report take-up rates -- they are central to interpreting treatment effects
- Pre-analysis plan: if registered, state the registry number in the introduction
- Structure results as: ITT first, then LATE/IV if compliance is imperfect, then heterogeneity
- External validity is often the main concern -- discuss what populations the results generalize to

## Difference-in-Differences (DiD)
- Lead with the policy change or natural experiment that generates treatment variation
- The parallel trends assumption is the core of your identification -- devote a full paragraph to it
- Intuition: under parallel trends (and no anticipation), the control group's before-after change is the counterfactual change the treated group would have experienced absent treatment, so the second difference nets out fixed group differences and shocks common to both, leaving the effect on the treated (ATT, not the ATE)
- Show pre-trends visually (event study plot is mandatory for modern DiD papers)
- A flat, non-significant pre-trend does not prove parallel counterfactual trends, and pre-tests are often underpowered -- report sensitivity to violations of parallel trends using HonestDiD (Rambachan and Roth 2023)
- Discuss treatment timing variation and staggered adoption if relevant
- If using staggered DiD, address recent econometric concerns (Goodman-Bacon, Sun and Abraham, Callaway and Sant'Anna)
- For staggered treatment: report the decomposition of the two-way fixed effects estimate (Goodman-Bacon 2021) to show which comparisons drive the result
- Use an appropriate estimator for the setting: Callaway and Sant'Anna (2021) for heterogeneous effects over event time, Sun and Abraham (2021) for event-study specifications, and de Chaisemartin and D'Haultfoeuille (2020), whose estimator guards against the sign reversal that TWFE can produce under heterogeneous effects
- Present results from BOTH the traditional TWFE and the robust estimator. If they differ, explain why (negative weights, treatment effect heterogeneity)
- Show the event-study plot from the robust estimator, not just the TWFE version
- Report results with and without covariates to show sensitivity
- Discuss anticipation effects if the policy was announced before implementation
- Address compositional changes in treated vs. control groups over time

## Instrumental Variables (IV)
- Intuition: a valid instrument moves the endogenous regressor only through a channel unrelated to the outcome's error, so 2SLS uses just that exogenous variation; under monotonicity it recovers a local average treatment effect (LATE) for the compliers whose behavior the instrument shifts, which generally differs from both OLS and the population ATE
- Name the instrument in the first paragraph of the introduction
- Devote a full paragraph to instrument relevance: report the effective (Montiel Olea and Pflueger 2013) or Kleibergen-Paap F-statistic. Treat the old "F > 10" rule as a minimal screen, not a guarantee
- Devote a full paragraph to the exclusion restriction -- argue it economically, not just statistically
- Report both OLS and IV estimates; explain why they differ (measurement error, selection, LATE vs. ATE)
- Discuss what the complier population looks like -- who are the marginal individuals whose behavior is shifted by the instrument?
- For weak or moderate instruments, report Anderson-Rubin confidence intervals (robust to any instrument strength); for single-instrument t-tests, apply the tF standard-error adjustment of Lee, McCrary, Moreira, and Porter (2022)
- Address the monotonicity assumption if estimating LATE
- Common instruments to discuss carefully: Bartik/shift-share (Goldsmith-Pinkham, Sorkin, and Swift 2020), judge/examiner leniency, historical/geographic instruments

## Regression Discontinuity (RDD)
- Intuition: if potential outcomes vary smoothly through the cutoff, units just above and just below are comparable in everything except treatment, so a jump in the outcome at the threshold is the causal effect -- but only locally, at the cutoff (sharp RDD) or for compliers at the cutoff (fuzzy RDD)
- Lead with the running variable and the cutoff
- Show the discontinuity visually (RD plot is mandatory -- this is your "figure 1")
- Discuss manipulation of the running variable (McCrary/density test)
- Present bandwidth sensitivity analysis -- results should be stable across reasonable bandwidths
- Report local polynomial estimates with optimal bandwidth (Calonico, Cattaneo, and Titiunik)
- Emphasize that RDD estimates are LOCAL to the cutoff -- discuss external validity explicitly
- For fuzzy RDD: report both reduced form (jump in outcome) and first stage (jump in treatment) separately
- Address any other discontinuities at the cutoff that might confound your estimates

## Synthetic Control
- Intuition: a weighted average of untreated donor units (non-negative weights summing to one), chosen so the synthetic unit tracks the treated unit's pre-treatment path and predictors, proxies its no-treatment counterfactual; given close pre-period fit, the post-intervention gap between the actual and synthetic series is the estimated effect
- Lead with the treated unit and the event/policy
- Describe donor pool selection criteria (why these comparison units?)
- Show pre-treatment fit visually -- this is your identification (if pre-treatment fit is poor, the method fails)
- Present placebo tests (permutation inference) as the primary inference tool
- Discuss what the synthetic counterfactual means substantively
- Report donor weights -- which comparison units receive the most weight?
- Address concerns about interpolation bias if donor units are very different from treated unit
- For multiple treated units, consider the augmented/penalized synthetic control or the synthetic DiD

## Synthetic Difference-in-Differences (Arkhangelsky et al.)
- Lead with the policy change and why neither standard DiD nor synthetic control alone is sufficient
- Explain the doubly robust property: valid if either the parallel trends assumption OR the synthetic control weights are correct
- Present both the standard DiD and synthetic control estimates alongside the synthetic DiD estimate for comparison
- Show unit weights and time weights -- readers need to understand which comparison units and pre-treatment periods drive the estimate
- For inference: use the placebo-based procedure (permuting treatment assignment) rather than asymptotic standard errors
- Discuss when synthetic DiD is preferred: settings with few treated units where DiD is noisy, or many pre-periods where synthetic control may overfit

## Structural Estimation
- Clearly state the economic model and its key assumptions in plain English before the math
- Distinguish between identifying assumptions (testable or untestable) and functional form assumptions
- Explain identification intuitively: what variation in the data pins down each parameter?
- Report model fit -- show the model can replicate key moments in the data
- Validate with out-of-sample predictions when possible
- Counterfactual simulations are the payoff -- present them prominently
- Discuss sensitivity to key assumptions: what if risk aversion is different? What if agents have different information?
- Compare structural estimates to reduced-form estimates where possible for credibility
- Report the sensitivity of key estimates to the identifying moments (Andrews, Gentzkow, and Shapiro 2017) to show which moments drive each parameter

## Descriptive and Measurement Papers
- Lead with why the measurement/description matters for economics
- Be explicit: "This paper does not estimate a causal effect. It documents [pattern/fact/measurement]."
- Describe the data construction process in detail -- this IS the contribution
- Show robustness of descriptive patterns to alternative definitions and samples
- Discuss what causal questions the new facts enable future researchers to answer
- Relate your descriptive findings to existing theoretical predictions

## Bunching Estimation (Saez, Kleven)
- Intuition: a kink changes the marginal incentive (the slope of the choice set) and a notch changes the level; either way, agents who would have optimized just past the threshold relocate to it, and the excess mass relative to a smooth counterfactual density reveals how strongly behavior responds -- which maps to a structural elasticity under an optimization model
- Lead with the policy kink or notch that generates the bunching
- Show the bunching visually -- the bunching plot is your central figure
- Describe the counterfactual distribution and how it is estimated
- Report the elasticity implied by the amount of bunching
- Discuss optimization frictions: bunching estimates are lower bounds if adjustment costs exist
- Address manipulation vs. real responses (for tax bunching: evasion vs. real labor supply)
- Present robustness to bandwidth and polynomial order of the counterfactual
- For notch designs: discuss the dominated region and the implications for rationality

## Shift-Share / Bartik Instruments
- Name the shift-share instrument explicitly in the introduction
- Describe both components clearly: the "shares" (exposure weights) and the "shifts" (national/sectoral shocks)
- Intuition: the instrument isolates the variation in the regressor driven by pre-period industry shares interacting with common sectoral shocks; it is valid only if that predicted variation is uncorrelated with the local error -- either because the initial shares are as-good-as-randomly assigned, or because the many shocks are themselves quasi-random
- State which source of variation you rely on for identification:
  - If relying on exogeneity of shares: argue why pre-period industry composition is exogenous (Goldsmith-Pinkham, Sorkin, and Swift 2020)
  - If relying on exogeneity of shifts: argue why the shocks are as-good-as-random (Borusyak, Hull, and Jaravel 2022)
- Report the effective F-statistic for the shift-share instrument
- Discuss the granularity of shares and the number of shocks driving variation
- Present "leave-one-out" estimates to show results are not driven by a single shock or sector
- Address pre-trends using the shift-share structure

## Event Studies
- Lead with the event and its economic significance
- Present the event study plot as the central figure
- Include pre-event coefficients to assess pre-trends (at least 3-4 pre-periods)
- Intuition: identification is the dynamic form of parallel trends (plus no anticipation) -- pre-event coefficients near zero are consistent with, but do not prove, treated and control units evolving together absent the event; post-event coefficients then trace the dynamic effect relative to the omitted base period. Under staggered timing with heterogeneous effects, raw TWFE leads/lags can be contaminated (Sun and Abraham 2021), so use a robust estimator
- Normalize one pre-period coefficient to zero (typically t = -1)
- Discuss the interpretation of post-event dynamics: is the effect immediate, gradual, or temporary?
- For staggered events: use appropriate estimators (Sun and Abraham, Callaway and Sant'Anna) and discuss treatment effect heterogeneity
- Report point estimates and confidence intervals for key post-event periods
- Address anticipation effects if the event was foreseeable

## Machine Learning for Causal Inference
- Clearly state whether ML is used for prediction, heterogeneity, or causal estimation
- For heterogeneous treatment effects (Causal Forests, Wager and Athey 2018, building on the honest sample-splitting trees of Athey and Imbens 2016): describe the sample splitting procedure and how overfitting is avoided
- For double/debiased ML (Chernozhukov et al. 2018): explain the cross-fitting procedure and why it is necessary
- Report traditional standard errors and confidence intervals -- ML does not change inference requirements
- Discuss the interpretability trade-off: more flexible models may sacrifice economic intuition
- Compare ML estimates to simpler parametric estimates for credibility
- For LASSO-based variable selection: justify why data-driven selection is appropriate and report sensitivity to penalization

## Papers Using Multiple Identification Strategies
- Many modern papers combine strategies (e.g., DiD as main specification + IV as robustness, or RDD + synthetic control)
- Designate one strategy as "primary" and present it first. Additional strategies should be framed as robustness or complementary evidence
- When strategies yield similar estimates, emphasize convergence: "The IV estimate of X is statistically indistinguishable from the DiD estimate of Y, reinforcing the causal interpretation"
- When strategies yield different estimates, explain why: different local populations (LATE vs. ATT), different identifying assumptions, or different margins of adjustment
- Do NOT present multiple strategies as equally weighted unless you genuinely have no reason to prefer one. Readers want to know which result you stand behind
- In the introduction, name the primary strategy. Mention the secondary strategy briefly: "I confirm these findings using [alternative method]"

---

## Adapting the Introduction by Paper Type

| Paper Type | Hook Strategy | What Goes in Paragraphs 4-6 | Key Threat to Discuss |
|-----------|--------------|-----------------------------|-----------------------|
| RCT | Policy relevance of intervention | ITT and LATE estimates | Attrition, spillovers, external validity |
| DiD | Policy change or natural experiment | Main DiD estimate + event study | Parallel trends, anticipation |
| IV | The instrument and why it's clever | OLS vs. IV comparison | Exclusion restriction, weak instruments |
| RDD | The cutoff and its stakes | RD estimate + bandwidth sensitivity | Manipulation, other discontinuities |
| Synthetic Control | The treated unit and the event | Synthetic vs. actual trajectory | Pre-treatment fit, donor pool |
| Synthetic DiD | Policy change + few treated units | Synthetic DiD vs. DiD vs. SC comparison | Parallel trends, synthetic control fit |
| Structural | The economic question that requires a model | Key counterfactual results | Model assumptions, external validity |
| Theory | The puzzle or paradox the model resolves | Main proposition and intuition | Robustness of mechanism to assumptions |
| Descriptive | Why the fact/measurement matters | Key patterns with magnitudes | Measurement validity, sample selection |
| Bunching | The policy kink/notch and who is affected | Elasticity estimate + bunching plot | Optimization frictions, manipulation |
| Shift-Share | The shock and local exposure | Main estimate + leave-one-out | Share exogeneity, shock exogeneity |
| Event Study | The event and its stakes | Event study plot + key coefficients | Pre-trends, anticipation |
| ML/Causal | The prediction or heterogeneity question | ML vs. parametric comparison | Overfitting, interpretability |
