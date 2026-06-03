# Writing Methods by Research Design

The first nine designs are broadly transferable across the empirical sciences. The final three (bunching, shift-share, structural estimation) are most common in economics and are labeled accordingly.

## Randomized Controlled Trials (RCTs)

Common in economics (development, labor, public), political science (field experiments), medicine (clinical trials), public health (community trials), and education.

- Lead with the intervention and its policy or clinical relevance.
- Describe the randomization mechanism and balance tests early.
- Emphasize intent-to-treat (ITT) as the main specification; discuss compliance and per-protocol / LATE separately.
- Address attrition and spillovers as primary threats to identification.
- Report take-up rates — they are central to interpreting treatment effects.
- Pre-analysis plan: if registered, state the registry number in the introduction (AEA RCT Registry, ClinicalTrials.gov, AsPredicted, OSF).
- Structure results: ITT first; then LATE / IV if compliance is imperfect; then heterogeneity.
- External validity is often the main concern — discuss what populations the results generalize to.
- For clinical trials specifically, follow CONSORT reporting (flow diagram, primary vs secondary outcomes, adverse events).
- For development RCTs, report cost-effectiveness alongside treatment effects when possible.

---

## Difference-in-Differences (DiD)

Used in economics, political science (electoral and policy reforms), public health (policy adoption studies), epidemiology (natural experiments).

- Lead with the policy change or natural experiment that generates treatment variation.
- The parallel trends assumption is the core of your identification — devote a full paragraph to it.
- Show pre-trends visually; an event study plot is mandatory in modern DiD work.
- Discuss treatment timing variation and staggered adoption if relevant.
- For staggered DiD, address recent econometric concerns (Goodman-Bacon 2021; Sun and Abraham 2021; Callaway and Sant'Anna 2021; de Chaisemartin and D'Haultfœuille 2020).
- For staggered treatment: report the decomposition of the two-way fixed effects estimate (Goodman-Bacon 2021) to show which comparisons drive the result.
- Use appropriate estimators: Callaway and Sant'Anna for heterogeneous effects over time; Sun and Abraham for event-study specifications; de Chaisemartin and D'Haultfœuille for the no-sign-reversal assumption.
- Present results from BOTH the traditional TWFE and the robust estimator. If they differ, explain why (negative weights, treatment effect heterogeneity).
- Show the event-study plot from the robust estimator, not just the TWFE version.
- Report results with and without covariates to show sensitivity.
- Discuss anticipation effects if the policy was announced before implementation.
- Address compositional changes in treated vs. control groups over time.

---

## Instrumental Variables (IV)

Used in economics, political science, epidemiology (Mendelian randomization), public health (policy variation as instrument).

- Name the instrument in the first paragraph of the introduction.
- Devote a full paragraph to instrument relevance. Report the first-stage F-statistic (Kleibergen-Paap or effective F-statistic for clustered settings).
- Devote a full paragraph to the exclusion restriction — argue it on substantive grounds, not just statistically.
- Report both OLS and IV estimates; explain why they differ (measurement error, selection, LATE vs ATE).
- Discuss what the complier population looks like — who are the marginal individuals whose behavior is shifted by the instrument?
- If the instrument is weak (F < 10), use Anderson-Rubin confidence intervals.
- Address the monotonicity assumption if estimating LATE.
- Common instrument classes to discuss carefully: shift-share / Bartik (Goldsmith-Pinkham, Sorkin, and Swift 2020; Borusyak, Hull, and Jaravel 2022), judge / examiner leniency, historical / geographic instruments, genetic variants (Mendelian randomization).

---

## Regression Discontinuity Design (RDD)

Used in economics, political science (electoral RDDs), public health (clinical thresholds), epidemiology (age-based eligibility).

- Lead with the running variable and the cutoff.
- Show the discontinuity visually. The RD plot is mandatory — this is your "Figure 1".
- Discuss manipulation of the running variable (McCrary / density test).
- Present bandwidth sensitivity analysis — results should be stable across reasonable bandwidths.
- Report local polynomial estimates with optimal bandwidth (Calonico, Cattaneo, and Titiunik 2014).
- Emphasize that RDD estimates are LOCAL to the cutoff — discuss external validity explicitly.
- For fuzzy RDD: report both reduced form (jump in outcome) and first stage (jump in treatment) separately.
- Address any other discontinuities at the cutoff that might confound your estimates.

---

## Event Studies

Used in economics, finance (event-study methodology for asset returns), political science (political shocks), public health (interventions over time).

- Lead with the event and its substantive significance.
- Present the event study plot as the central figure.
- Include pre-event coefficients to assess pre-trends (at least 3–4 pre-periods).
- Normalize one pre-period coefficient to zero (typically t = -1).
- Discuss the interpretation of post-event dynamics: is the effect immediate, gradual, or temporary?
- For staggered events: use appropriate estimators (Sun and Abraham; Callaway and Sant'Anna) and discuss treatment effect heterogeneity.
- Report point estimates and confidence intervals for key post-event periods.
- Address anticipation effects if the event was foreseeable.

---

## Synthetic Control

Used in economics, political science (case studies of policy changes), and increasingly in public health (single-region interventions).

- Lead with the treated unit and the event / policy.
- Describe donor pool selection criteria (why these comparison units?).
- Show pre-treatment fit visually — this is your identification (if pre-treatment fit is poor, the method fails).
- Present placebo tests (permutation inference) as the primary inference tool.
- Discuss what the synthetic counterfactual means substantively.
- Report donor weights — which comparison units receive the most weight?
- Address concerns about interpolation bias if donor units are very different from treated unit.
- For multiple treated units, consider the augmented / penalized synthetic control or the synthetic DiD (Arkhangelsky et al. 2021).

---

## Synthetic Difference-in-Differences (Arkhangelsky et al.)

Increasingly used in policy evaluation across economics, political science, and public health.

- Lead with the policy change and why neither standard DiD nor synthetic control alone is sufficient.
- Explain the doubly robust property: valid if either the parallel trends assumption OR the synthetic control weights are correct.
- Present standard DiD, synthetic control, and synthetic DiD estimates alongside each other for comparison.
- Show unit weights and time weights — readers need to understand which comparison units and pre-treatment periods drive the estimate.
- For inference: use the placebo-based procedure (permuting treatment assignment) rather than asymptotic standard errors.
- Discuss when synthetic DiD is preferred: settings with few treated units where DiD is noisy, or many pre-periods where synthetic control may overfit.

---

## Machine Learning for Causal Inference

Used across the empirical sciences for heterogeneity, prediction, and high-dimensional control.

- Clearly state whether ML is used for prediction, heterogeneity, or causal estimation.
- For heterogeneous treatment effects (Causal Forests, Athey and Imbens 2016; Wager and Athey 2018): describe the sample splitting procedure and how overfitting is avoided.
- For double / debiased ML (Chernozhukov et al. 2018): explain the cross-fitting procedure and why it is necessary.
- Report traditional standard errors and confidence intervals — ML does not change inference requirements.
- Discuss the interpretability trade-off: more flexible models may sacrifice substantive intuition.
- Compare ML estimates to simpler parametric estimates for credibility.
- For LASSO-based variable selection: justify why data-driven selection is appropriate and report sensitivity to penalization.

---

## Descriptive and Measurement Papers

Universal across the empirical sciences. Despite being "descriptive", these papers can be among the most influential when the measurement is novel or the patterns are surprising.

- Lead with why the measurement / description matters substantively.
- Be explicit: "This paper does not estimate a causal effect. It documents [pattern / fact / measurement]."
- Describe the data construction process in detail — this IS the contribution.
- Show robustness of descriptive patterns to alternative definitions and samples.
- Discuss what causal questions the new facts enable future researchers to answer.
- Relate your descriptive findings to existing theoretical predictions.

---

## Designs Most Common in Economics

The following designs appear primarily in economics and adjacent quantitative fields. Use them where appropriate; do not force them into work in other disciplines.

### Bunching Estimation (Saez 2010; Kleven 2016)

- Lead with the policy kink or notch that generates the bunching.
- Show the bunching visually — the bunching plot is your central figure.
- Describe the counterfactual distribution and how it is estimated.
- Report the elasticity implied by the amount of bunching.
- Discuss optimization frictions: bunching estimates are lower bounds if adjustment costs exist.
- Address manipulation vs. real responses (for tax bunching: evasion vs. real labor supply).
- Present robustness to bandwidth and polynomial order of the counterfactual.
- For notch designs: discuss the dominated region and the implications for rationality.

### Shift-Share / Bartik Instruments

- Name the shift-share instrument explicitly in the introduction.
- Describe both components clearly: the "shares" (exposure weights) and the "shifts" (national / sectoral shocks).
- State which source of variation you rely on for identification:
  - If relying on exogeneity of shares: argue why pre-period industry composition is exogenous (Goldsmith-Pinkham, Sorkin, and Swift 2020).
  - If relying on exogeneity of shifts: argue why the shocks are as-good-as-random (Borusyak, Hull, and Jaravel 2022).
- Report the effective F-statistic for the shift-share instrument.
- Discuss the granularity of shares and the number of shocks driving variation.
- Present "leave-one-out" estimates to show results are not driven by a single shock or sector.
- Address pre-trends using the shift-share structure.

### Structural Estimation

- Clearly state the substantive model and its key assumptions in plain English before the math.
- Distinguish identifying assumptions (testable or untestable) from functional form assumptions.
- Explain identification intuitively: what variation in the data pins down each parameter?
- Report model fit — show the model can replicate key moments in the data.
- Validate with out-of-sample predictions when possible.
- Counterfactual simulations are the payoff — present them prominently.
- Discuss sensitivity to key assumptions: what if risk aversion is different? What if agents have different information?
- Compare structural estimates to reduced-form estimates where possible for credibility.

---

## Papers Using Multiple Designs

Many modern papers combine designs (e.g., DiD as main specification + IV as robustness, or RDD + synthetic control).

- Designate one design as "primary" and present it first. Additional designs should be framed as robustness or complementary evidence.
- When designs yield similar estimates, emphasize convergence: "The IV estimate is statistically indistinguishable from the DiD estimate, reinforcing the causal interpretation."
- When designs yield different estimates, explain why: different local populations (LATE vs ATT), different identifying assumptions, different margins of adjustment.
- Do NOT present multiple designs as equally weighted unless you genuinely have no reason to prefer one. Readers want to know which result you stand behind.
- In the introduction, name the primary design. Mention the secondary design briefly: "I confirm these findings using [alternative method]."

---

## Adapting the Introduction by Design

| Design | Hook Strategy | What Goes in Paragraphs 4–6 | Key Threat to Discuss |
|---|---|---|---|
| RCT | Substantive relevance of the intervention | ITT and LATE estimates | Attrition, spillovers, external validity |
| DiD | Policy change or natural experiment | Main DiD estimate + event study plot | Parallel trends, anticipation |
| IV | The instrument and why it's clever | OLS vs. IV comparison | Exclusion restriction, weak instruments |
| RDD | The cutoff and its stakes | RD estimate + bandwidth sensitivity | Manipulation, other discontinuities |
| Event Study | The event and its stakes | Event study plot + key coefficients | Pre-trends, anticipation |
| Synthetic Control | The treated unit and the event | Synthetic vs. actual trajectory | Pre-treatment fit, donor pool |
| Synthetic DiD | Policy change + few treated units | Synthetic DiD vs. DiD vs. SC comparison | Parallel trends, synthetic control fit |
| ML / Causal | The prediction or heterogeneity question | ML vs. parametric comparison | Overfitting, interpretability |
| Descriptive | Why the fact / measurement matters | Key patterns with magnitudes | Measurement validity, sample selection |
| Bunching (econ) | The policy kink / notch and who is affected | Elasticity estimate + bunching plot | Optimization frictions, manipulation |
| Shift-Share (econ) | The shock and local exposure | Main estimate + leave-one-out | Share exogeneity, shock exogeneity |
| Structural (econ) | The substantive question that requires a model | Key counterfactual results | Model assumptions, external validity |
| Theory | The puzzle the model resolves | Main proposition and intuition | Robustness of mechanism to assumptions |

