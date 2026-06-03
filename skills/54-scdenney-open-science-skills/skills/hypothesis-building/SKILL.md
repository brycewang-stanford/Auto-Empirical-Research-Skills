---
name: hypothesis-building
description: Build falsifiable causal hypotheses: DAGs, FPCI, equivalence testing.
argument-hint: "[describe your theory or research question]"
---

# Causal Hypothesis Architect

## Instructions

### 1. The Identification Challenge
- **Verify FPCI Resolution:** Confirm that random assignment (or the identification strategy) solves the Fundamental Problem of Causal Inference for this design (Druckman 2022).
- **Four Prerequisites for Experiments:** Before proceeding, verify that the design meets the four prerequisites for causal inference from experiments: (1) *random assignment* to conditions, (2) *exclusion restriction* (the only difference between conditions is the treatment itself), (3) *SUTVA* (Stable Unit Treatment Value Assumption -- one subject's treatment does not affect another's outcome), and (4) *noninterference* between units (Druckman 2022).
- **Define the Data Generating Process (DGP):** Before drafting the hypothesis, describe the set of rules that governs how the data is created. What are the underlying mechanics of the world being studied?
- **Map the Causal Diagram:** Where appropriate, draw a DAG. Identify backdoor paths and confirm whether randomization closes them (Mutz 2011).
- **Close the Backdoors:** State which variables must be controlled for to isolate the treatment effect. If using an experiment, explain how random assignment closes these paths (Mutz 2011).
- **SATE vs. PATE:** Distinguish between the Sample Average Treatment Effect (SATE) and the Population Average Treatment Effect (PATE). A convenience-sample experiment estimates a SATE; a population-based experiment on a representative sample estimates the PATE directly by design, without requiring statistical modeling or extrapolation (Mutz 2011; Druckman 2022).

### 2. Hypothesis Formulation
- **Popperian Falsifiability:** Frame the hypothesis as a "basic statement", or a specific observation that, if found to be false, would invalidate the theory.
- **The Counterfactual Logic:** Every hypothesis must specify a comparison. Define the "untreated" world. If the hypothesis is that X causes Y, what is the specific state of the world where X is absent? Note that in many survey experiments there may be no "pure control" -- each condition provides information, just different information (Druckman 2022). Distinguish between *active* control groups (which receive different information on the same topic, controlling for the act of receiving information) and *passive* control groups (no information), as this choice defines the counterfactual and thus the estimand (Stantcheva 2023).
- **Directional Clarity:** Avoid "existence" claims (e.g., "there is an effect"). Use "ordinal" claims that specify the direction (higher/lower) and, where possible, the expected functional form.
- **Beat Credible Competitors:** The goal of a hypothesis test is not merely to reject the null of "no effect" but to beat credible alternative explanations. Design experiments that adjudicate between competing theories -- "the point of the experiment is explication, not demonstration" (Sniderman 2018). A hypothesis is stronger when it specifies which competing theoretical account would be undermined by the predicted result.
- **Null-by-Design Thinking:** If the theory predicts no effect below a threshold of treatment intensity, specify (a) the intensity threshold, (b) expert-panel review of treatment strength before fielding, and (c) the equivalence bounds for the statistical test. Route such designs to the equivalence test in §3 (Sniderman 2018).
- **Estimand Specification:** Every hypothesis must map to a specific estimand -- the statistical quantity that, if estimated, would test the hypothesis. State the *theoretical estimand* (the target quantity, defined outside any statistical model) before choosing the *empirical estimand* (a function of observable data) and the estimation strategy; each step requires different assumptions and should be argued separately (Lundberg, Johnson, & Stewart 2021). For experimental designs, this typically means specifying: (a) the treatment contrast (what is compared to what), (b) the outcome metric (probability, scale score, etc.), and (c) the model that produces the estimate (e.g., AMCE from a conjoint, ATE from a vignette experiment). A hypothesis without a named estimand is not pre-registrable. Where feasible, declare the design formally using the MIDA framework -- model, inquiry, data strategy, answer strategy -- so that power, bias, and estimator--estimand coherence can be diagnosed computationally before fielding (Blair, Cooper, Coppock, & Humphreys 2019). For information/pedagogical experiments, distinguish between *first-stage* estimands (the belief or knowledge the treatment shifts) and *second-stage* estimands (the policy views influenced by those beliefs), with the causal chain explicit (Stantcheva 2023).
- **Information Equivalence:** In survey experiments, the exclusion restriction manifests as "information equivalence" -- the assumption that a manipulation only affects the intended construct and not background beliefs. If a treatment shifts respondents' perceptions of multiple constructs simultaneously, the estimand becomes ambiguous. Name the information equivalence assumption for each treatment contrast and discuss what would violate it (Stantcheva 2023).
- **SESOI Requirement:** For every hypothesis test, state the Smallest Effect Size of Interest (SESOI) -- the smallest effect that would be theoretically or practically meaningful. Justify the SESOI based on (a) theoretical predictions, (b) practical significance thresholds, or (c) benchmarks from the literature. A hypothesis without a SESOI cannot be rigorously evaluated (Lakens 2025).
- **Disconfirming Evidence:** Beyond falsifiability in the abstract, specify concretely what pattern of results would constitute evidence *against* the hypothesis. For illustration, in a group-threat paradigm: "If the interaction coefficients are jointly significant and indicate that procedural effects vanish when group threat is activated, this would favor group-centric accounts over the normative baseline model."
- **Three-Level Specification:** Specify each hypothesis at three levels (Lakens 2025): (1) *conceptual* (the theoretical claim in plain language), (2) *operationalized* (the specific measures and contrasts), and (3) *statistical* (the exact test, estimand, and decision rule). The pre-analysis plan should bridge all three levels.

### 3. Hypothesis Testing Logic
- **Choose the Test Type:** Select among NHST, interval, equivalence, and minimum-effect tests based on the theoretical claim (Lakens 2025). Not every hypothesis calls for NHST.
- **Equivalence Testing for Null Predictions:** When a hypothesis predicts "no meaningful effect," use the TOST (Two One-Sided Tests) procedure rather than interpreting a non-significant p-value as evidence of absence. Specify the equivalence bounds in raw effect size units and justify them. The R `TOSTER` package implements this procedure (Lakens 2025).
- **The Four-Outcome Grid:** When combining NHST with equivalence testing, state in advance which of the four outcomes (inconclusive, effect present, effect absent, trivially small) would corroborate, falsify, or leave the hypothesis inconclusive (Lakens 2025).
- **Severity as Evaluation Standard:** Ensure the preregistered analysis has high power and the prediction is specific enough to be wrong in multiple ways (Lakens 2025).
- **Compromise Power for Fixed N:** When sample size is constrained by resources or population size, use a compromise power analysis that minimizes the combined Type I + Type II error rate. An alpha > 0.05 may be defensible if it reduces total error (Lakens 2025).

### 4. Scope and Generalization
- **Defining the Target Population:** A hypothesis is not universal. Explicitly name the population for whom the theory should hold. Distinguish between the target population (who the theory applies to) and the accessible population (who can be sampled). If using a convenience sample, acknowledge that the estimand is a SATE, and specify what assumptions would be needed to generalize to the PATE.
- **Mechanism vs. Effect:** Distinguish between a hypothesis about a *causal effect* (did it happen?) and a hypothesis about a *causal mechanism* (why did it happen?). In audit studies and some survey experiments, the design may identify the effect but not the mechanism -- a rejection letter sent to a minority applicant shows discrimination occurred but does not reveal whether it was driven by taste-based or statistical discrimination (Druckman 2022). Similarly, distinguish *priming* hypotheses (salience activation without new information) from *information* hypotheses (belief updating through new facts) -- these have different identifying assumptions, and if a prime causes learning, the identification breaks down (Stantcheva 2023).
- **Experimenter Demand Effects (EDE):** Respondents may form views about the experimenter's expectations and adjust responses accordingly. EDE threatens the validity of both treatment effects and descriptive statistics. Specify EDE-mitigation strategies in the design: obfuscated follow-ups, monetary incentives for questions with correct answers, neutral framing, and multi-block survey designs that separate treatment from outcome elicitation (Stantcheva 2023).
- **Measurement Hypotheses:** Some hypotheses concern *measurement bias* rather than causal effects. For example, a list experiment tests whether respondents underreport a sensitive attitude. The estimand is the difference between the direct-report prevalence and the list-experiment-estimated prevalence. Treat these as a distinct hypothesis class (Mutz 2011; Blair et al. 2020).
- **Scope Conditions vs. Hypotheses:** Demote context-variation expectations to scope conditions when the theory does not make precise directional predictions about *which* context produces the largest effect. Examine scope conditions descriptively rather than through confirmatory tests. Reserve confirmatory status for directional claims that can be powered, and avoid proliferating underpowered cross-context hypotheses.

### 5. Hypothesis Architecture in Multi-Experiment Designs
- **Sequential Numbering:** When a study includes multiple experiments, number hypotheses sequentially across experiments (e.g., H1--H2 for Experiment 1, H3--H5 for Experiment 2) to maintain clarity and enable cross-referencing.
- **Micro-Macro Bridging:** When experiments target different levels of analysis (e.g., individual-level preferences vs. institutional-level legitimacy), hypotheses should explicitly bridge across levels. State how the macro-level prediction extends or parallels the micro-level one.
- **Three-Tier Hypothesis Hierarchy:** Expand beyond the binary confirmatory/exploratory distinction. Classify every hypothesis as (Appelbaum et al. 2018 JARS-Quant; Lakens 2025):
    - *Primary:* Both Type I and Type II error rates are controlled and minimized. These are the study's central claims.
    - *Secondary:* Type I error rate is controlled, but the study may be underpowered (Type II error not controlled). These are theoretically motivated but not the main focus.
    - *Exploratory:* Error rates are uncontrolled. These arise during analysis and must be reported with appropriate caveats. Common candidates: individual-level moderators, three-way interactions, and cross-national comparisons where the theory underdetermines the expected pattern.
- **Gate-Check -- Is the Theory Ready?** Before committing to confirmatory hypotheses, ask: Is the theory sufficiently developed to generate falsifiable predictions? If predictions require arbitrary choices (e.g., picking a specific effect size threshold without justification), the study may be better framed as exploratory (Lakens 2025).
- **Hypothesis-to-Model Mapping:** Each confirmatory hypothesis should be explicitly linked to a specific regression model in the empirical strategy. This mapping prevents "analytical degrees of freedom" (Simmons, Nelson, & Simonsohn 2011) -- the researcher must commit in advance to which model tests which claim. Pre-specification also disciplines the "garden of forking paths," in which data-contingent but individually reasonable analytic choices inflate false-positive rates even without conscious fishing (Gelman & Loken 2014). Pre-registration in a public registry (EGAP, OSF, or AsPredicted) is the institutional commitment mechanism for this mapping (Humphreys, Sanchez de la Sierra, & van der Windt 2013; Nosek et al. 2018).
- **Counter-Hypothesis Design:** Where possible, design the experiment to test two competing hypotheses against each other (e.g., fairness-based reasoning vs. group-threat reasoning) rather than a single hypothesis against the null. This provides richer theoretical information regardless of the result (Sniderman 2018).
- **Sequential Factorial Logic:** In multi-experiment designs, use the "sequential factorial" approach: Experiment 1 establishes the basic effect; Experiment 2 splices in additional factors to probe mechanisms or boundary conditions. State how later-experiment hypotheses depend on earlier-experiment results so cumulative theoretical leverage is explicit in the PAP (Sniderman 2018).

## Related Skills
- Hand the finished hypothesis set to `pre-registration-writing` for PAP structuring, locked/conditional/exploratory tiers, and decision rules.
- Route JARS-compliant reporting of primary/secondary/exploratory hypotheses and the APSA/DA-RT transparency checks to `methods-reporting`.
- For conjoint-specific estimand choices (AMCE vs. marginal means, interaction AMIEs), see `conjoint-design`.
- For list-experiment measurement hypotheses, see `list-experiment`.
- For cross-national scope conditions and per-country power, see `cross-national-design`.
- For survey-level treatment delivery, question wording, and attention checks that affect estimand validity, see `survey-design`.
- For the theoretical "Why" that grounds the counterfactual "If-Then," see `narrative-building`.

## Quality Checks
- [ ] **Falsifiability:** Can I describe a specific data result that would force the rejection of this theory?
- [ ] **FPCI:** Have I identified how the design solves the Fundamental Problem of Causal Inference?
- [ ] **Identifying Assumptions:** Have I stated what must be true (random assignment, exclusion restriction, SUTVA) for this comparison to be interpreted as causal?
- [ ] **Counterfactual:** Is the point of comparison (the control group) clearly defined?
- [ ] **Population:** Is the scope of the claim limited to a specific, named population? Is the estimand a SATE or PATE?
- [ ] **Estimand:** Does each hypothesis name the specific statistical quantity (AMCE, ATE, interaction coefficient) that would test it?
- [ ] **SESOI:** Is the smallest effect size of interest stated and justified?
- [ ] **Three-Level Specification:** Is each hypothesis stated at the conceptual, operationalized, and statistical levels?
- [ ] **Test Type:** Is the appropriate test type identified (NHST, equivalence, minimum effect, or interval)?
- [ ] **Disconfirming Pattern:** Is the specific data pattern that would undermine the theory described?
- [ ] **Competitor Theories:** Does the design test the hypothesis against a credible alternative, not just the null?
- [ ] **Three-Tier Classification:** Are hypotheses classified as primary, secondary, or exploratory?
- [ ] **Scope Conditions:** Are context-dependent expectations framed as scope conditions rather than confirmatory hypotheses?
- [ ] **Model Mapping:** Is each hypothesis linked to a specific regression specification?
- [ ] **Registry:** Is the pre-analysis plan registered in a public repository (EGAP, OSF, AsPredicted)?
- [ ] **Information Equivalence:** Is the information equivalence assumption stated for each survey experiment treatment contrast (Stantcheva 2023)?
- [ ] **EDE Mitigation:** Are experimenter demand effect mitigation strategies specified (Stantcheva 2023)?
- [ ] **First/Second Stage:** For information experiments, are first-stage (belief-shifting) and second-stage (policy view) estimands clearly distinguished (Stantcheva 2023)?

## Example

> **Worked example:** see [reference/example.md](reference/example.md).
