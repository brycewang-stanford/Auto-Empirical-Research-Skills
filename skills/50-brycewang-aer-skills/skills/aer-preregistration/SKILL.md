---
name: aer-preregistration
description: Use when the project collects primary data or runs a field, lab, or survey experiment, before the intervention begins — write the pre-analysis plan, size the sample from a power calculation, and register with the AEA RCT Registry. Apply after the design is chosen in aer-identification and before any outcome data are seen.
---

# AER Pre-Registration

## Overview

For experimental and prospective-data AER-track work, credibility is bought
**before** the data exist. This skill writes the pre-analysis plan (PAP), sizes
the sample from a power calculation, and registers the study. Its job is to make
the eventual results un-p-hackable: a referee who sees a public PAP timestamp
predating data collection cannot accuse you of specification search.

Registration is not optional at AEA journals for RCTs. If the design is
observational, skip to `aer-robustness`; there is nothing to pre-register.

## When to Use

- The paper runs a randomized controlled trial (field, lab, or survey experiment)
- The project collects primary data whose analysis should be pre-committed
- A referee or editor asks for the trial registration number or the PAP
- Reviewers suspect the reported specification was chosen after seeing outcomes
- You must justify the sample size, or explain why an effect was "not detected"

## Register-or-Not Decision

```
Is treatment assigned by the researcher (randomization)?
├── Yes → register with the AEA RCT Registry BEFORE the intervention; write a PAP
├── No, but you collect new primary data → post a PAP for the pre-committed analysis
└── No, secondary/observational data already realized → do NOT pre-register
      (a PAP written after the outcomes exist is theater); go to aer-robustness
```

## Pre-Analysis Plan Contents

Pre-specify, in order, and timestamp before unblinding:

1. **Hypotheses** — each stated as a signed, testable prediction, not a topic:

   > H1: the cash transfer raises household consumption at endline by at
   > least 0.15 SD, estimated by OLS of log consumption on treatment with
   > strata fixed effects, clustered at the village level.

2. **Primary outcomes** — a short list (ideally 1-3). Everything else is
   secondary or exploratory and labeled as such.
3. **Estimating equation** — the exact regression, fixed effects, covariates,
   and the level at which standard errors cluster.
4. **Sample and inclusion rules** — who is in the analysis and how attrition is
   handled (pre-commit to bounds; see `examples/lee-bounds-demo/`).
5. **Multiple-testing correction** — the family and the method (e.g. Romano-Wolf,
   `romano_wolf_2005`), pre-specified, not chosen after the p-values land.
6. **Heterogeneity** — the subgroups you will test, fixed in advance; all others
   are exploratory.
7. **Power** — the MDE and the assumptions behind it (below).

Keep the PAP moderate in scope (Olken's advice): pre-specify the primary
analysis tightly, leave genuine discovery clearly flagged as exploratory. An
over-long PAP that pre-registers forty outcomes protects nothing.

## Power and the Minimum Detectable Effect

Size the sample from the MDE, not the other way around. For a two-arm trial with
equal allocation, size `sigma`, share `p`, total `N`:

```
MDE = (z_power + z_{1-alpha/2}) * sigma * sqrt(1 / (p (1 - p) N))
```

- Target **80% power** at a **5%** two-sided level: $z_{0.80} = 0.84$ and
  $z_{0.975} = 1.96$, so `z_power + z_alpha = 2.80`.
- State the MDE in the units the audience cares about, and benchmark it against
  the smallest effect that would be economically interesting. If the MDE exceeds
  that, the study is underpowered — do not run it as designed.
- Correct the variance for **clustered** assignment (design effect
  $1 + (m-1)\rho$ — e.g. $m = 30$ per cluster and $\rho = 0.05$ inflates the
  needed sample by a factor of $2.45$), for a baseline covariate ($R^2$ gain),
  and for expected attrition. A power number that ignores the ICC is fiction.
- Underpowered designs do not just miss: when they reach significance they
  **exaggerate** the effect (Type-M). See `examples/power-mde-demo/` for the
  MDE-attains-target-power check and the winner's-curse simulation.

Cite `mckenzie_2012` (more rounds beat larger cross-sections when outcomes are
noisy) and `duflo_glennerster_kremer_2007` (the design toolkit). Keys in
[`../../references.bib`](../../references.bib); defaults in
[`../../docs/methods-reference.md`](../../docs/methods-reference.md).

## Reporting Against the Plan

- Report the pre-specified primary result **first**, exactly as written, even if
  it is null. A pre-registered null is a publishable finding, not a failure.
- Mark every deviation from the PAP explicitly, with the reason, in a table.
- Separate confirmatory from exploratory results in the manuscript; never
  promote an exploratory subgroup to the headline.
- File the disclosure and IRB/ethics approvals; AEA journals require both.

## Red Flags for Referees

- No registration number on an RCT, or a timestamp *after* data collection began
- A power calculation that omits clustering, attrition, or the ICC
- Twenty "primary" outcomes with no multiplicity correction
- The headline result is an unregistered subgroup interaction
- "Not statistically significant" reported as "no effect" with no MDE stated
- Deviations from the PAP that are silent rather than disclosed

## Pre-Registration Gate

Do not advance to data collection until **all** are true:

- [ ] Primary outcomes and the estimating equation are pre-specified in writing
- [ ] The sample size is justified by an MDE with clustering and attrition built in
- [ ] The multiple-testing family and correction are fixed in advance
- [ ] The study is registered (AEA RCT Registry) with a pre-intervention timestamp
- [ ] Exploratory analyses are labeled as such, not disguised as confirmatory

## Repository Resources

Bundled with the installed skill, no repository checkout needed --- read it
before the repo resources below:

- `references/pap-template.md` --- PAP outline, power/MDE reporting template, registry field checklist

When working from the repo or plugin bundle, load only the relevant resource:

- Power/MDE worked simulation with the Type-M winner's-curse check: `examples/power-mde-demo/`
- Attrition bounds to pre-commit in the PAP: `examples/lee-bounds-demo/`
- Estimator defaults, diagnostics, and BibTeX keys: `docs/methods-reference.md`
- Multiple-testing correction methods: `skills/aer-robustness/SKILL.md`
- Verified references (`mckenzie_2012`, `duflo_glennerster_kremer_2007`): `references.bib`

Fix the MDE and the primary-outcome list before drafting; both feed the
`aer-identification` estimator choice and the `aer-consistency` audit.

## Handoff

```text
DESIGN: <RCT | primary-data collection | observational (no PAP)>
PRIMARY OUTCOMES: <list, 1-3>
MDE / POWER: <MDE in outcome units; power; assumptions incl. ICC and attrition>
MULTIPLICITY: <family + correction method>
REGISTRATION: <AEA RCT ID + timestamp, or "n/a">
NEXT SKILL: aer-identification (confirm estimator) then aer-robustness
```

## Anti-Patterns

- Writing the PAP after the endline data are in hand — the timestamp is the point
- Pre-registering so many outcomes that "confirmatory" loses all meaning
- Powering the study for the effect you hope for instead of the smallest one
  worth detecting
- Treating a registered null as a failed experiment rather than a clean result
- Reporting an exploratory subgroup as if it had been pre-specified
