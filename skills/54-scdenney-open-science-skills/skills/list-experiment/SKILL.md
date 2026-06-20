---
name: list-experiment
description: Design and diagnose list experiments (item count technique).
argument-hint: "[describe your sensitive question or list experiment design]"
---

# List Experiment Designer

**Related skills:** Use alongside `hypothesis-building` (state π and a SESOI before design choices), `survey-design` (mode effects, question ordering, and pre-testing of control items), and `methods-reporting` (deposit list wording, randomization seed, `list` package version, and `ict.test` / `ict.hausman.test` / `ictreg()` output).

## Instructions

### 1. Pre-Design: Is a List Experiment Warranted?

- **Assess sensitivity bias first:** Before committing to a list experiment, consult domain-specific evidence on sensitivity bias. Blair, Coppock, and Moor's (2020) meta-analysis of 30 years of list experiments shows that sensitivity biases are typically smaller than 10 percentage points. A list experiment is not automatically the right choice for any sensitive topic.
- **Social reference theory:** Sensitivity bias is largest when (a) the social norm on the topic is strong, (b) the norm is clear and widely shared, and (c) respondents believe others can infer their true attitude from their response (Blair et al. 2020). Evaluate all three conditions before deciding.
- **Precision cost:** List experiments require approximately 10 times more respondents than a direct question to achieve equivalent precision. The trade-off is only favorable when the expected sensitivity bias exceeds the precision loss (Blair et al. 2020). If the topic is sensitive but the expected bias is small (< 5pp), a direct question with neutral framing is often preferable.
- **Empirical benchmarks by domain:** Voter turnout (~5–15pp overreport, wide confidence intervals), clientelism and vote-buying (~5–15pp underreport), racial prejudice (near-zero sensitivity bias — Blair et al. 2020 find little evidence respondents conceal prejudice on direct questions), authoritarian regime support (highly context-dependent and often dominated by artificial deflation rather than preference falsification). Use these as priors when no domain-specific estimates exist.

### 2. Basic Design

- **Core logic:** Assign respondents randomly to a control group (receives N baseline items) or a treatment group (receives N+1 items, including the sensitive item). Estimate prevalence as the difference in mean counts between treatment and control. This provides plausible deniability because no individual response can be traced to the sensitive item.
- **Number of control items:** Use 3–5 control items. Fewer items reduce plausible deniability (too easy to infer the sensitive item from a high count). More items increase cognitive load and floor/ceiling risk, and reduce statistical efficiency.
- **Randomize item order:** Randomize the order of all items within each respondent's list to prevent position effects from inflating or deflating specific items.
- **Wording parity:** Frame all items, including the sensitive item, in the same grammatical form and at the same abstraction level. Stylistic inconsistency makes the sensitive item stand out, undermining the design.

### 3. Control List Design

- **The floor/ceiling constraint:** Select control items so that virtually no respondent would endorse all N control items (ceiling) or zero control items (floor) when assigned to the treatment group. A respondent at the ceiling cannot truthfully report N+1 even if they hold the sensitive attitude; one at the floor cannot hide a "1" count. Both violations bias estimates downward (artificial deflation) and compromise identification (Blair & Imai 2012).
- **Target prevalence range for control items:** Each control item should have expected prevalence between 20% and 80% in the population. The sum of expected control item endorsements should have low variance — ideally each respondent endorses roughly 1–3 of N control items.
- **Item independence:** Control items should be uncorrelated with the sensitive item. If control items tap dimensions that predict the sensitive attitude, the no-design-effect assumption is threatened.
- **Conventional vs. placebo vs. mixed control list design:** Three design options exist for managing measurement error from inattentive respondents (Agerberg & Tannenberg 2021):
  - *Conventional:* Standard baseline items, no placebo. Biased if nonstrategic error inflates or deflates counts.
  - *Placebo:* Replace one control item with a universally false statement (all should answer "no") to equate list length in treatment and control. Riambau & Ostwald (2021) show this reduces mechanical inflation — the tendency for treatment group respondents to report more true items simply due to list length, especially among low-education respondents. However, Agerberg & Tannenberg (2021) show placebo items do not universally reduce bias and can increase it under some conditions.
  - *Mixed control list:* Combines conventional and placebo items. Preferred when the expected direction and magnitude of sensitivity bias is uncertain.
  - **Choice rule:** When mechanical inflation is the primary concern (inattentive or acquiescent respondents inflating counts), include a placebo item. When artificial deflation is the primary concern (ceiling effects), use a conventional design and select items with lower prevalence. When uncertain, use the mixed control list.

### 4. Design Variants

- **Single list experiment:** Standard design. Simplest to implement; most commonly used. The sensitive item appears only in the treatment list.
- **Double list experiment (DLE):** Each respondent sees the sensitive item in one of two lists (as a treatment item in one list, as part of a second control list in another). Reduces variance by using all respondents for estimation. However, Diaz (2024) shows that DLEs require additional diagnostic testing for carryover design effects — if respondents respond differently to control items after having seen the sensitive item in another list, the DLE identification assumption fails.
  - *Design preconditions for diagnostics:* Diaz's (2024) tests apply only to fixed-randomized or randomized-randomized DLEs (the location of the sensitive item must be randomized across respondents); they cannot diagnose carryover in fixed-fixed DLEs.
  - *Two tests, both to be reported:* (i) a difference-in-differences test on the paired list means (equivalent to the Chuang et al. 2021 consistency test in the fixed-randomized case) and (ii) Stephenson's signed-rank test (Rosenbaum 2007, 2020) on the paired within-respondent differences. The difference-in-differences test has more power under response deflation than inflation; the signed-rank statistic can be positive under either inflation or non-zero true prevalence, so interpret one-sided deflation alternatives. Report both.
- **Placebo-item design (Riambau & Ostwald 2021):** A universally-false statement (e.g., "I have been invited to have dinner with PM Lee at Sri Temasek next week") added to the control list to equalize list length at J+1 / J+1. The placebo should be implausible enough to be false for all respondents but not so disruptive that it degrades attention on the remaining items. This is the design the placebo/mixed options in §3 rely on; do not confuse it with respondent-tailored ("piped-in") placebos, which are a separate and not-yet-validated variant.

### 5. Estimators

- **Difference-in-means:** $\hat{\pi} = \bar{Y}_{T} - \bar{Y}_{C}$. Unbiased estimator of the target estimand π — the population prevalence of the sensitive behavior or attitude (state π explicitly before design choices, per Lundberg, Johnson & Stewart 2021). Standard errors: $SE \approx \sqrt{Var(Y_T)/n_T + Var(Y_C)/n_C}$. Simple and transparent; appropriate when no covariate adjustment is needed and the research question is purely about aggregate prevalence.
- **Multivariate NLSreg:** Nonlinear least squares regression that models the list experiment outcome as a function of covariates. More robust to nonstrategic measurement error than MLreg when respondents answer inattentively or randomly — NLSreg is more robust to misspecification because it does not impose a parametric distribution on the sensitive item (Blair et al. 2019). **Prefer NLSreg over MLreg as the primary multivariate estimator** in online and panel surveys where inattentive responding is common.
- **Multivariate MLreg:** Maximum likelihood regression imposing a logistic model on the sensitive item. More efficient than NLSreg when correctly specified, but vulnerable to misspecification bias under measurement error (Blair et al. 2019). Use as a robustness check.
- **Combined estimator (Aronow et al. 2015):** When both list experiment and direct question data are available, and partial honesty is suspected in direct responses, the Aronow et al. (2015) estimator improves precision by pooling both sources nonparametrically. Use when power is limited and some direct responses are likely truthful. Implemented in the `list` R package.
- **All estimators:** Implement via the `list` R package (Blair, Chou & Imai), which provides a unified interface for difference-in-means, NLSreg, MLreg, combined estimator, and Bayesian MCMC hierarchical models, along with all standard diagnostic tests.

### 6. Identifying Assumptions and Diagnostics

- **No design effect (NDE):** Respondents answer the control items identically regardless of whether the sensitive item is present in their list. Violation means the presence of the sensitive item changes responses to other items (e.g., emotional or cognitive spillover). Test formally using `ict.test()` in Blair & Imai's (2012) `list` package.
- **No floor/ceiling (NFC):** No respondent who endorses the sensitive item would endorse 0 of the control items (floor) or all N of the control items (ceiling) if they were in the treatment group. Ceiling effects cause artificial deflation — treatment respondents who hold the sensitive attitude cannot truthfully report N+1 and instead undercount. Assess by examining response distributions at the extremes and using ceiling/floor liar model options within `ictreg()`.
- **Placebo diagnostics:** Include a placebo experiment — a list experiment on a non-sensitive topic where the true prevalence is known — as an additional diagnostic (Frye et al. 2023). Significant artificial deflation on a placebo topic indicates systematic design problems, not preference falsification. Especially important in authoritarian contexts where ceiling effects on regime support items are common.
- **Nonstrategic error diagnostics:** Test whether the variance of responses in the treatment group is substantially higher than in the control group. Inflated treatment variance relative to control may indicate inattentive responding producing noise (Blair et al. 2019). The operational test is the NLSreg-vs-MLreg specification test (a Hausman-style contrast of the two fits) proposed in Blair, Chou & Imai (2019) and implemented as `ict.hausman.test()` in the `list` package — reject model specification if the Hausman statistic is large and positive, or if it takes a negative value (which itself signals misspecification). If detected, use NLSreg as the primary estimator and consider including a placebo item.

### 7. Common Problems and Corrections

- **Mechanical inflation:** Treatment group respondents endorse more true items due to list length alone, not because of the sensitive item. Most pronounced among low-education respondents in face-to-face contexts (Riambau & Ostwald 2021). Address with placebo statement design.
- **Artificial deflation:** Ceiling effects prevent respondents with the sensitive attitude from truthfully reporting their count. Produces downward-biased estimates that look like low sensitivity bias but actually reflect design failure (Frye et al. 2023). Address by selecting lower-prevalence control items; diagnostic via placebo experiment.
- **The misreporting trade-off:** List experiments reduce strategic misreporting (social desirability-driven lying in direct questions) but increase nonstrategic misreporting (confusion, inattention, random answers inflated by list length). Kuhn & Vivyan (2022) show that for voter turnout in New Zealand and the UK, nonstrategic misreporting inflated by list experiments substantially exceeds strategic misreporting eliminated by them — yielding a net negative compared to direct questions. This trade-off is empirically domain-dependent; do not assume list experiments dominate direct questions for any sensitive topic.
- **SUTVA and item independence:** If control items are conceptually close to the sensitive item, their interpretation may change when presented alongside it (design effect). Pre-test item independence in cognitive interviews.

### 8. Statistical Power

- **Power formula:** The variance of the difference-in-means estimator is approximately $4 \times Var(Y_C) / N_{total}$ for balanced designs ($n_T = n_C = N/2$), where $Var(Y_C)$ is the variance of the control group count. This is substantially larger than the binomial variance of a single direct question item, requiring ~10× more respondents for equivalent precision at typical effect sizes (Blair et al. 2020).
- **Control list variance matters:** High-variance control lists (where individual endorsement probabilities are close to 0.5) increase the variance of the estimator. Design control items to minimize total control list variance while keeping each item's prevalence within the 20–80% range.
- **Power analysis:** Use simulation. For a target effect size $\pi$ (true sensitive item prevalence), simulate $B$ datasets under the design and compute rejection rates. The `list` package's simulation tools support this. Rule of thumb: assume effective sample sizes 5–10× below what a direct question study would require.
- **NFC check:** Power calculations are only valid if the no-floor/ceiling assumption is plausible. Conduct a hypothetical NFC diagnostic using expected prevalence priors before data collection.

## Quality Checks

- [ ] **Sensitivity justified:** Was the need for a list experiment established using domain-specific evidence on sensitivity bias magnitude? Is the expected bias large enough to justify the ~10× power cost?
- [ ] **Social reference conditions:** Are the three conditions for substantial sensitivity bias present (strong norm, clear norm, inferability)?
- [ ] **Control items in range:** Are all control items expected to have prevalence between 20% and 80%? Is there minimal variance at the extremes of the control list count distribution?
- [ ] **Floor/ceiling pre-checked:** Was the no-floor/ceiling assumption evaluated prior to data collection using prevalence priors?
- [ ] **Design variant justified:** Has the choice between single, double, and placebo variants been justified based on expected sources of error?
- [ ] **Placebo decision:** If placebo items are used, was it to address mechanical inflation specifically? Has the risk of placebo bias (Agerberg & Tannenberg 2021) been considered?
- [ ] **DLE carryover tested:** If a double list experiment is used, is it fixed-randomized or randomized-randomized (so that Diaz's 2024 tests apply), and are both the difference-in-differences test and Stephenson's signed-rank test planned and reported?
- [ ] **NLSreg as primary:** Is NLSreg (not MLreg) used as the primary multivariate estimator, especially in online surveys with likely inattentive respondents?
- [ ] **NDE test:** Is the no-design-effect assumption tested formally with `ict.test()` and reported?
- [ ] **Hausman spec test:** Is the NLSreg-vs-MLreg specification test (`ict.hausman.test()`; Blair, Chou & Imai 2019) reported when a multivariate estimator is used?
- [ ] **NFC test:** Is the no-floor/ceiling assumption tested formally and reported?
- [ ] **Placebo experiment:** For politically sensitive contexts (regime support, discrimination), is a placebo experiment included to distinguish preference falsification from artificial deflation?
- [ ] **Trade-off acknowledged:** Is the misreporting trade-off (reduced strategic, increased nonstrategic) discussed, with reference to domain-specific evidence?
- [ ] **Power simulation:** Was a simulation-based power analysis conducted accounting for the ~10× variance multiplier?
- [ ] **`list` package cited:** Is the `list` R package (Blair, Chou & Imai) cited as the implementation source?
- [ ] **Direct comparison:** If results are compared to direct question estimates, is the comparison treated as a diagnostic rather than a validation (since the direct question is the biased baseline)?

## Example

For a worked illustration — a four-item control list for a clientelism / vote-buying sensitive item, with expected prevalences, floor/ceiling tail calculations, a pre-field NFC simulation, and the specific `ict.test()` / `ict.hausman.test()` diagnostic calls — see `reference/example-clientelism.md`.
