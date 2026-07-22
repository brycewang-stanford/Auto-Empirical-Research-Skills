# Pre-Analysis Plan Template and Registry Checklist

*Bundled with the `aer-preregistration` skill so the checklist works without the repository checkout. SKILL.md routes; this file carries the depth.*

A pre-analysis plan (PAP) buys credibility before the data exist: a public timestamp predating data collection means no referee can attribute the result to specification search. Fill every [BRACKETED-CAPS] slot, timestamp the document, and register before the intervention begins.

## 1. PAP outline with fill-in slots

### 1.1 Study identification

- **Title:** [STUDY-TITLE]
- **Investigators:** [INVESTIGATOR-NAMES-AND-AFFILIATIONS]
- **Registry ID:** [AEA-RCT-REGISTRY-ID] (fill after registration)
- **IRB approval:** [IRB-NAME-AND-PROTOCOL-NUMBER], approved [APPROVAL-DATE]
- **PAP version and date:** v[VERSION-NUMBER], [PAP-DATE] — before any outcome data are seen

### 1.2 Hypotheses

State each as a signed, testable prediction, not a topic:

> H1: [TREATMENT-NAME] raises [PRIMARY-OUTCOME] at [ENDLINE-TIMING] by at least [EFFECT-SIZE-IN-SD-OR-UNITS], estimated by [ESTIMATOR] with [FIXED-EFFECTS], standard errors clustered at the [CLUSTER-LEVEL] level.

Repeat for H2, H3. Few hypotheses, each falsifiable.

### 1.3 Primary outcomes (keep this list short)

| # | Outcome | Exact variable definition | Measurement instrument | Timing |
|---|---|---|---|---|
| 1 | [OUTCOME-1-NAME] | [VARIABLE-CONSTRUCTION-RULE] | [SURVEY-OR-ADMIN-SOURCE] | [MEASUREMENT-WAVE] |
| 2 | [OUTCOME-2-NAME] | [VARIABLE-CONSTRUCTION-RULE] | [SURVEY-OR-ADMIN-SOURCE] | [MEASUREMENT-WAVE] |

Ideally 1-3 primary outcomes. Everything else is secondary or exploratory and is labeled as such in Section 1.7.

### 1.4 Exact estimating specification

Write the regression you will run, not a family of regressions:

```
Y_ic = alpha + beta * Treat_c + X_i'gamma + strata FE + epsilon_ic
```

- **Outcome transform:** [LEVELS-LOGS-OR-STANDARDIZED]
- **Covariates X:** [PRESPECIFIED-COVARIATE-LIST] (or a stated machine-selection rule fixed in advance)
- **Fixed effects:** [STRATA-OR-BLOCK-FE]
- **Clustering:** [CLUSTER-LEVEL], [N-CLUSTERS] clusters
- **Missing-data and attrition rule:** [IMPUTATION-OR-BOUNDS-RULE] — pre-commit to bounds for differential attrition in the spirit of Lee (2009)

### 1.5 Sample and randomization design

- **Sampling frame:** [FRAME-DESCRIPTION]; inclusion criteria: [INCLUSION-RULES]; exclusion criteria: [EXCLUSION-RULES]
- **Unit of randomization:** [INDIVIDUAL-OR-CLUSTER]
- **Stratification/blocking:** [STRATA-VARIABLES]
- **Arms and allocation:** [N-ARMS] arms; allocation ratio [ALLOCATION-RATIO]; assignment by [RANDOMIZATION-PROCEDURE] with seed [RANDOMIZATION-SEED] recorded
- **Target sample:** [N-CLUSTERS] clusters x [M-UNITS-PER-CLUSTER] units = [N-TOTAL]
- **Balance check:** joint test on [BALANCE-VARIABLE-LIST]; imbalance handled by [PRESPECIFIED-RESPONSE], not by re-randomizing after the fact

### 1.6 Power and minimum detectable effect (reporting template)

Size the sample from the MDE, not the other way around. For a two-arm trial:

```
MDE = (z_power + z_{1-alpha/2}) * sigma * sqrt(1 / (p (1 - p) N))
```

Report every assumption:

| Assumption | Value | Basis |
|---|---|---|
| Significance level (alpha, two-sided) | [ALPHA — e.g. 0.05] | convention |
| Power target | [POWER — e.g. 0.80] | convention |
| Outcome SD (sigma) | [SIGMA-VALUE] | [PILOT-OR-PRIOR-STUDY] |
| Treated share (p) | [TREATED-SHARE] | design |
| ICC (rho) | [ICC-VALUE] | [PILOT-OR-PRIOR-STUDY] |
| Cluster size (m) | [M-UNITS-PER-CLUSTER] | design |
| Design effect 1 + (m-1) * rho | [DESIGN-EFFECT] | computed |
| Baseline covariate R-squared gain | [R2-GAIN] | [PILOT-OR-PRIOR-STUDY] |
| Expected take-up (compliance) | [TAKEUP-RATE] | [PILOT-OR-PRIOR-STUDY] |
| Expected attrition | [ATTRITION-RATE] | [PILOT-OR-PRIOR-STUDY] |
| **Resulting MDE** | [MDE-IN-OUTCOME-UNITS] | computed |

- State the MDE in units the audience cares about and benchmark it against the **smallest economically interesting effect**, [SMALLEST-INTERESTING-EFFECT]. If the MDE exceeds that benchmark, the design is underpowered — redesign, do not run.
- Imperfect take-up scales the detectable intent-to-treat effect: divide the target treatment-on-treated effect by the compliance differential [TAKEUP-RATE] when sizing.
- A power number that omits the ICC, take-up, or attrition is fiction, and underpowered designs exaggerate when they do reach significance (the Type-M winner's curse). Design references: Duflo, Glennerster, and Kremer (2007) for the toolkit; McKenzie (2012) for when more measurement rounds beat a larger cross-section.

### 1.7 Multiple-testing plan

- **Families:** [FAMILY-DEFINITIONS — e.g. primary outcomes; secondary outcomes by domain]
- **Correction method:** [CORRECTION-METHOD — e.g. Romano and Wolf (2005) stepdown; or the List, Shaikh, and Xu (2019) implementation for experiments]
- Fixed now, before any p-value exists; never chosen after the results land.

### 1.8 Heterogeneity: pre-specified vs. exploratory

| Dimension | Status | Rationale |
|---|---|---|
| [SUBGROUP-1 — e.g. baseline income below median] | Pre-specified | [THEORY-BASED-REASON] |
| [SUBGROUP-2] | Pre-specified | [THEORY-BASED-REASON] |
| Anything else | Exploratory | labeled as such in the paper, never the headline |

## 2. AEA RCT Registry field-by-field checklist

Complete before the intervention begins; the registry timestamp is the evidence.

- [ ] Title and acronym
- [ ] Country/countries and locations
- [ ] Status (in development / on-going) and trial start and end dates
- [ ] Intervention description (can be hidden until trial end if needed)
- [ ] Primary outcomes — end points and exact definitions matching Section 1.3
- [ ] Secondary outcomes, labeled as secondary
- [ ] Experimental design summary and randomization method
- [ ] Randomization unit, planned number of clusters, planned number of observations
- [ ] Treatment arms and sample size per arm
- [ ] Minimum detectable effect size with assumptions, matching Section 1.6
- [ ] IRB name, approval number, and approval date
- [ ] PAP uploaded as an attachment (can be embargoed/hidden until trial completion)
- [ ] Analysis-plan visibility setting chosen deliberately
- [ ] Registration citation copied into the paper's front-matter footnote: "This trial is registered as [AEA-RCT-REGISTRY-ID]."

## 3. The moderate-scope principle

Pre-specify the primary analysis tightly; leave genuine discovery clearly flagged as exploration. Per Olken's guidance on moderate PAPs, an over-long plan that pre-registers forty outcomes protects nothing — "confirmatory" loses meaning, and the multiple-testing burden explodes. The test: every pre-specified item should be one you are prepared to report first, exactly as written, even if null. A pre-registered null is a publishable finding, not a failure.

## 4. Deviations-from-PAP protocol

Deviations happen; silent deviations are the sin. In the paper:

1. Report the pre-specified primary estimate **first**, exactly as registered, even when a deviation exists alongside it.
2. Include a deviations table (main text or appendix):

| # | PAP said | Paper does | Reason | When decided |
|---|---|---|---|---|
| 1 | [ORIGINAL-SPEC] | [ACTUAL-SPEC] | [REASON — e.g. survey item dropped in wave 2] | [DECISION-DATE], [BEFORE-OR-AFTER-UNBLINDING] |

3. Distinguish deviation types: implementation failures (attrition, take-up shortfalls), measurement changes (instrument revisions), and analytic changes (specification edits). Analytic changes decided after unblinding carry the least credibility — say so plainly.
4. Never promote an unregistered subgroup or secondary outcome to the headline result.
5. If the registry entry was amended, cite the amendment history; amendments before unblinding are ordinary, amendments after are disclosures.

## 5. Timing rules

- **Register before the intervention begins.** A timestamp after treatment delivery started defeats the purpose and is a referee red flag.
- **Finalize the PAP before unblinding** — before anyone on the team sees outcome data by arm. Baseline data may inform the PAP; endline data may not.
- Registering before baseline is stronger than registering after baseline but before endline; both beat registering after data collection.
- Observational designs on already-realized data: do not pre-register — a PAP written after the outcomes exist is theater. Route to `aer-robustness` instead.
- Log the dates: [REGISTRATION-DATE] < [INTERVENTION-START-DATE] and [PAP-FINAL-DATE] < [UNBLINDING-DATE]. These four dates belong in the paper.

## Pre-registration gate

- [ ] Primary outcomes and the exact estimating equation are written down (Sections 1.3-1.4)
- [ ] Sample size is justified by an MDE with ICC, take-up, and attrition built in (Section 1.6)
- [ ] Multiple-testing families and correction fixed (Section 1.7)
- [ ] Heterogeneity split into pre-specified vs. exploratory (Section 1.8)
- [ ] Registry entry complete with a pre-intervention timestamp (Section 2)
- [ ] Deviations protocol understood before it is needed (Section 4)

## Canonical repo sources

Distilled from these repository surfaces, which require the repository checkout:

- `skills/aer-preregistration/SKILL.md`
- `examples/power-mde-demo/README.md`
- `examples/lee-bounds-demo/`
- `docs/methods-reference.md`
- `references.bib`
