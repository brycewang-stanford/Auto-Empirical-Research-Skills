---
name: conjoint-diagnostics
description: Diagnose conjoint design integrity, estimation choices, and validity.
argument-hint: "[describe your conjoint study or paste analysis code]"
---

# Conjoint Experiment Diagnostics

## Instructions

Work through each section below for the conjoint study under review. Assess whether the study addresses each item adequately, partially, or not at all. Flag items that pose threats to inference and prioritize recommendations by severity.

Branch on input:
- **If a paper or manuscript is provided**, proceed through Sections 1–5 sequentially and produce a verdict per section.
- **If analysis code or data is provided**, verify the actual implementation rather than just what the paper claims: (a) confirm clustering specification, (b) confirm the estimand matches the reported quantity, (c) if IRR is unmeasured, compute within-respondent task-pair agreement as a function of attribute-level differences (Clayton et al. 2023 §3.3 method 2 / `projoint`).

For neighboring concerns, invoke sibling skills: `conjoint-design` (design choices), `conjoint-cleaning` (Qualtrics exports → long format), `hypothesis-building` (linking estimands to "If-Then" predictions), `methods-reporting` (full JARS/DA-RT compliance and replication archive), `cross-national-design` (multi-country / multilingual conjoints).

---

## 1. Design Diagnostics

### 1.1 Attribute and Level Selection
- Are attributes conceptually distinct and non-overlapping?
- Are levels realistic and mutually exclusive within each attribute?
- Is the number of attributes justified? (Bansak et al. 2021 PSRM "Beyond the Breaking Point": response quality is generally robust even at 35 filler attributes, with detectable but modest satisficing — use as a ceiling, not an endorsement of 35 attributes as optimal. Distinct from Bansak et al. 2018 on task counts below.)
- For cross-national or multilingual designs, verify construct equivalence of attribute labels across languages (see `cross-national-design`).
- Are there "dominant" attributes that might crowd out attention to others?
- Do the attribute levels span a meaningful range of the construct of interest?

### 1.2 Profile Restrictions
- Are implausible or contradictory attribute combinations allowed?
- If restrictions are imposed, are they documented and justified?
- If no restrictions, does the paper acknowledge potential odd profiles? (Bansak & Jenke 2025: odd profiles have minimal impact on first-order inferences, but should be acknowledged)

### 1.3 Number of Tasks and Satisficing
- How many tasks per respondent? (Bansak et al. 2018: up to 30 tasks with limited satisficing)
- Are attention checks embedded? Are pass rates reported by task position?
- Is there evidence of survey fatigue or satisficing in later tasks? Look for: (a) response-time distributions by task position (not just means), (b) always-same-side / always-left or always-right rates, (c) random-choice / trembling-hand rates relative to Bansak et al. 2021 baselines, (d) attention-check failure rates by task position.
- Have profile-order, carryover, and fatigue assumptions been tested empirically? (Ham, Imai & Janson 2024 §3.5: `CRTConjoint` provides conditional randomization tests for all three of Hainmueller-Hopkins-Yamamoto 2014's identifying assumptions.)

### 1.4 Randomization
- Is attribute-level assignment fully randomized (uniform distribution)?
- If non-uniform, is this justified and documented?
- Are profile-pair attributes independent or dependent? (Clayton et al. 2023 distinguish independent, dependent, and pair-level attributes)

### 1.5 Sample and Power
- Is the sample size justified with a power analysis? (Schuessler & Freitag 2020 cjpowR; Stefanelli & Lukac 2020)
- What is the effective sample size (N respondents x T tasks)?
- Are Type S (sign) and Type M (magnitude/exaggeration) errors considered?
- For subgroup analyses, is there adequate power within each subgroup?

---

## 2. Estimation Diagnostics

### 2.1 Estimand Clarity
- Verify the estimand is clearly defined (AMCE, MM, AMIE, or pAMCE) and the choice is justified.
- Check whether AMCEs are interpreted with awareness that they depend on the attribute distribution used for averaging (Hainmueller et al. 2014).
- Check whether MMs are used where reference-category-free comparisons are needed (Leeper et al. 2020).

### 2.2 Reference Levels
- Are reference levels clearly specified and substantively meaningful?
- Are AMCEs interpreted relative to the correct reference category?
- For subgroup comparisons, is the reference category consistent across groups? (Leeper et al. 2020: conditional AMCEs are sensitive to reference choice)

### 2.3 Subgroup Analysis
- Are subgroups defined by pre-treatment characteristics (not post-treatment)?
- **Use marginal means and diff-in-MMs for subgroup comparisons**, not conditional AMCEs. (Leeper, Hobolt & Tilley 2020: conditional AMCEs are reference-category dependent and can yield arbitrary subgroup differences)
- Are diff-in-MMs presented alongside MMs for interpretability?
- Is heterogeneity detection systematic or ad hoc? (Robinson & Duch 2024 cjbart; Goplerud et al. 2025 FactorHet)

### 2.4 Standard Errors and Clustering
- Are standard errors clustered at the respondent level? Clustering is conventional with T > 1 tasks per respondent, though Schuessler & Freitag (2020) show the adjustment averages only ~2% across published conjoints and is not strictly necessary for sample causal effects. Flag clustering absent without justification, but do not auto-fail.
- Is the clustering variable correctly specified?
- Are confidence intervals reported? At what level? (Convention: 95%, some papers use 90% or dual CI bars)

### 2.5 Multiple Testing
- How many AMCEs/MMs are estimated in total?
- Is there a correction for multiple comparisons? (Liu & Shiraito 2023: >90% chance of at least one spurious significant AMCE with no correction when no true effects exist)
- If no correction, is this limitation acknowledged?
- Consider: Bonferroni (conservative), Benjamini-Hochberg (FDR), adaptive shrinkage (recommended as default when limited prior knowledge)

---

## 3. Measurement Error Diagnostics (Clayton et al. 2023)

Worry about measurement error whenever the study draws subgroup comparisons, reports small-to-moderate AMCEs/MMs near zero, or forgoes any IRR estimate. Conjoint responses carry **swapping error** (not classical noise): average Intra-Respondent Reliability is ~77% across Clayton et al.'s eight replications, biasing MMs toward 0.5 and AMCEs toward 0. For subgroup diff-in-AMCEs, correction can attenuate, exaggerate, or flip sign (~82/12/5% split). Audit the study for (a) an IRR estimate or justified borrow (≈0.75 default), (b) bias correction via the `projoint` R package (Clayton et al.), and (c) sensitivity analysis across plausible IRR values if uncorrected.

> **Detailed measurement-error workflow:** see [reference/measurement-error.md](reference/measurement-error.md).

---

## 4. External Validity Diagnostics

### 4.1 Behavioral Benchmarking
- Does the paper position its design against the Hainmueller-Hangartner-Yamamoto 2015 benchmark, or provide other behavioral validation? HHY 2015 compared conjoint and vignette estimates to a Swiss naturalization referendum natural experiment; the paired forced-choice conjoint recovered behavioral effects to within ~2 percentage points. Absent a direct behavioral benchmark, the paper should at minimum reference HHY 2015's evidence that paired forced-choice designs have strong external validity for comparable decision contexts.

### 4.2 Profile Distribution
- Does the uniform attribute distribution match real-world frequencies? (de la Cuesta et al. 2022)
- If not, does the paper discuss how this affects interpretation?
- Are pAMCEs computed for comparison?

### 4.3 Forced Choice vs. Real-World Behavior
- Does the forced-choice format accurately reflect the decision context? (Visconti & Yang 2024)
- Should an abstention/neither option be offered? (Miller & Ziegler 2024: preferential abstention can produce different-sign AMCEs)
- Is there a rating outcome alongside forced choice? (Treger 2025: forced-choice and rating elicit distinct preferences)
- **Outcome-type robustness**: If both forced-choice and rating were collected, do AMCEs/MMs agree in sign and ranking across outcome types? Divergence is substantive, not a nuisance.

### 4.4 Attention and Salience
- Does the conjoint format artificially inflate attention to attributes that respondents would ignore in real decisions? (Fu & Li 2024)
- Could this lead to effect magnitude amplification, sign reversal, or importance reversal?
- What real-world decision process is the conjoint trying to simulate? State the target DGP explicitly — without it, "attention inflation" cannot be assessed.

---

## 5. Interpretation Diagnostics

### 5.1 AMCE Interpretation
- Does the paper correctly interpret AMCEs as average effects on choice probability, not majority preferences? (Abramson et al. 2022; Ganter 2023 sharpens this: AMCE identifies a choice-probability effect, not a parameter of the underlying preference distribution.)
- Does the paper acknowledge that AMCEs depend on the distribution of other attributes? (Bansak et al. 2023 respond that AMCEs map to vote share changes)
- Are AMCEs interpreted as causal effects or merely as preference rankings?
- If the design relies on the SDB-mitigation argument for conjoints, is the claim hedged in light of Horiuchi, Markovich, and Yamamoto (2022)? Their direct test shows conjoints reduce SDB on some attributes but not others; the mitigation is not automatic.

### 5.2 Lexicographic / Categorical Preferences
- Could respondents be applying a categorical veto (always rejecting profiles with a given attribute level)?
- If so, standard AMCEs and MMs may be misleading due to co-occurrence rates across task pairs.
- Are nested marginal means used to detect attribute ranking? (Dill, Howlett & Müller-Crepon 2024; `cjRank` R package)
- Does the paper test whether lower-ranked attributes matter conditional on the veto attribute being held constant?

### 5.3 Magnitude Reporting
- Are effect sizes reported in interpretable units (percentage points)?
- Are substantive significance thresholds discussed alongside statistical significance?
- Is there comparison to benchmark effect sizes in similar studies?
- **Cross-attribute magnitude comparisons require caution.** Leeper et al. 2020 (fn 3): in forced-choice designs where both profiles can share a level, MMs are bounded by the co-occurrence probability (for 5 equally likely levels, MMs are bounded to ~(0.04, 0.96)); AMCEs for binary attributes are bounded to (−0.5, 0.5). Comparing raw AMCE magnitudes across attributes with different level counts conflates the effect with its mechanical bound.

### 5.4 Interaction Effects
- If interactions are examined, are AMIEs used rather than conditional AMCEs? (Egami & Imai 2019)
- Are interaction coefficients from dummy-coded regressions interpreted? If so, flag: these are baseline-dependent artifacts (Egami & Imai 2019).
- Is there a test for whether a factor matters at all? (Ham et al. 2024 CRTConjoint: conditional randomization test)
- **Configural vs additive claims:** If the paper argues that one attribute's effect is fundamentally interactive with the rest of the profile ("the effect of X depends on the full bundle"), check whether the analysis reports the *range* of focal-attribute effects across the context space — $\theta(\vec{x}_{Max})$ and $\theta(\vec{x}_{Min})$ in the sense of Gosciak, Molitor, and Lundberg (2026) — rather than only an AMCE that marginalizes over context. AMIE captures low-order interactions and CRT detects whether *any* heterogeneity exists, but neither localizes the contexts at which the focal attribute matters most or least. With non-adaptive data, this surface is recoverable observationally from cell means at the cost of thin cells in rare context combinations; flag the substantive coarsening choices and the cell-size distribution. With an adaptive design, audit the warm-up/adaptive/validation phase allocations, the choice of focal attribute (must be ex ante), and the two-signal construction for each context value.

---

## Quality Checks

A well-reported conjoint study should include:

- [ ] Clear statement of the estimand (AMCE, MM, or both)
- [ ] Reference levels for all attributes
- [ ] Number of respondents, tasks per respondent, and effective sample size
- [ ] Attention check protocol and pass rates
- [ ] Randomization procedure (uniform or weighted)
- [ ] Any profile restrictions and justification
- [ ] Clustering specification for standard errors
- [ ] Confidence interval level(s) reported
- [ ] Discussion of measurement error / IRR (Clayton et al. 2023)
- [ ] Multiple testing approach or acknowledgment of concern (Liu & Shiraito 2023)
- [ ] Pre-registration status and any deviations
- [ ] Software and packages used for estimation

For full JARS/DA-RT compliance — replication archive, seeds, preprocessing code, IRB, consent, and funding statements — invoke the `methods-reporting` skill.

## Example Finding

A HIGH-severity finding should name the rule violated, cite the source, and recommend a fix. For example: *"The paper compares AMCEs for gender across subgroups A and B (−0.04 vs. +0.02) and concludes preferences differ. Per Leeper, Hobolt & Tilley (2020), diff-in-AMCEs is reference-category dependent and can flip sign under a different baseline. Recommendation: recompute as diff-in-MMs and report both; interpret any sign change as evidence the original claim was reference-artifact driven."*

## Software

The skill references several R packages; the one whose use is strictly load-bearing for the skill is `projoint` (Clayton et al. 2023) for IRR estimation and bias correction. Others that may appear in a conjoint workflow: `cjoint` (Strezhnev et al., AMCE estimation), `cregg` (Leeper, MMs and diff-in-MMs), `cjbart` (Robinson & Duch 2024, BART-based heterogeneity), `FactorHet` (Goplerud-Imai-Pashley 2025, principled heterogeneity detection), `CRTConjoint` (Ham-Imai-Janson 2024, conditional randomization tests and assumption tests), `cjRank` (Dill-Howlett-Müller-Crépon 2024, nested MMs for lexicographic preferences), and `cjpowR` (Schuessler & Freitag 2020, power analysis).

