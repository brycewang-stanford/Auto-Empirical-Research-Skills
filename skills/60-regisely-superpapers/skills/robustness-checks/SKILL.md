---
name: robustness-checks
description: Use when a main specification has produced a result, when preparing a paper appendix, when a reviewer requests robustness, or before declaring any empirical finding final. Guides selection of design-appropriate checks without mandating a fixed checklist.
---

# Robustness Checks

## Overview

This skill applies canonical robustness checks appropriate to the research design. It is open-ended — the skill suggests checks that fit the specific identification strategy, not a blanket checklist. YAGNI applies aggressively: a paper with 5 well-chosen robustness checks is stronger than one with 30 redundant ones.

## When to Use

- After `statistical-modeling` has produced a main result
- A reviewer has requested robustness tests
- Preparing the paper's robustness section or appendix
- Before submitting to a journal
- The user asks "is this result robust?"

## The YAGNI Principle

Include only checks that meet at least one criterion:

1. **Canonical for the design** — the standard literature expects them (e.g., pre-trends for DiD, McCrary density for RD)
2. **Plausibly challenging** — the check probes an assumption that could realistically fail
3. **Specifically requested** — a reviewer asked for it

Do not pile on tests to signal rigor. Thirty robustness checks produce noise, not evidence. Referees read a crowded appendix as defensive, not thorough.

## Mandatory Steps

1. **Identify the identification strategy of the main result.** The design determines which assumptions are load-bearing and therefore which checks are informative.

2. **List the canonical challenges to that strategy.** For DiD, parallel trends is key, so checks should probe it (pre-trends, placebo periods, event studies). For RD, continuity and non-manipulation. For IV, exclusion and weakness. For SC, donor pool and pre-treatment fit.

3. **Pick 4-8 checks that address those challenges.** More is rarely better. If you cannot justify each check in one sentence, drop it.

4. **Run each check as a separate script** under `code/`, following `replication-driven-research`. Each check should be reproducible independently.

5. **Report all checks in a dedicated section or appendix table**, including checks where the result does NOT survive. Transparency about failures is credibility, not weakness.

6. **Discuss failures openly.** If a check fails, explain what the failure means and whether it changes the interpretation of the main result.

## Starting-Point Recipe by Design

**Not exhaustive.** Pick what fits your specific design and question.

### Any Design

- **Alternative standard errors:** Robust vs clustered vs bootstrap; clustering at different levels
- **Sample splits:** By period, by subgroup, excluding outliers or influential observations
- **Alternative specifications:** Adding or removing controls, alternative functional forms, alternative outcome definitions
- **Sensitivity to outliers:** Winsorization, trimming, removing high-leverage points

### Difference-in-Differences

- **Pre-trends test:** Event-study plot with pre-period coefficients
- **Placebo periods:** Fake treatment dates before the actual one
- **Alternative comparison groups:** Different control-group definitions
- **Triple-diff:** A third dimension to rule out confounding trends
- **For staggered adoption:** Callaway-Sant'Anna, de Chaisemartin-D'Haultfoeuille, or BJS imputation as alternatives to two-way FE

### Regression Discontinuity

- **Bandwidth sensitivity:** Vary the bandwidth above and below the optimal choice
- **Polynomial order:** Local linear, local quadratic, higher order with caution
- **McCrary density test:** Check for manipulation at the cutoff
- **Covariate balance at the cutoff:** Pre-determined covariates should be smooth
- **Donut RD:** Drop observations very close to the cutoff

### Instrumental Variables

- **Weak-IV diagnostics:** Montiel-Pflueger F, Stock-Yogo critical values
- **Reduced-form plot:** Inspect the direct relationship between instrument and outcome
- **Alternative instruments:** If multiple available, check consistency
- **Overidentification tests:** Sargan or Hansen (with caveats on size)
- **LATE interpretation:** Explicit discussion of which compliers the estimate applies to

### Synthetic Control

- **Placebo tests in space:** Apply method to each donor
- **Placebo tests in time:** Move the treatment date back
- **Leave-one-out donors:** Drop each donor, re-estimate
- **Pre-treatment RMSPE comparison:** Treated unit vs placebo distribution

### Time-Series

- **Alternative lag length:** AIC vs BIC vs HQ
- **Structural breaks:** Test for and accommodate breaks
- **Alternative stationarity assumptions:** Robustness to trend specification

### Panel / Fixed Effects

- **Alternative FE structures:** Unit-only, time-only, two-way
- **Alternative clustering levels**
- **Nickell bias in dynamic panels:** Check with GMM alternatives if relevant

## Reporting Format

Example narrative structure for a robustness section:

```markdown
## Robustness

Table A1 reports alternative specifications. Column (1) reproduces the main
result from Table 3. Column (2) excludes the 2020 shock. Column (3) uses an
alternative outcome measure. Column (4) clusters at the municipality level
instead of state. The coefficient remains statistically significant and
economically meaningful across all variations, except for Column (2), where
the point estimate falls by 40% and is no longer significant at conventional
levels. This sensitivity to the 2020 period is discussed in Section 6 and
reflects the extraordinary conditions of the COVID-19 recession.

Figure A1 presents the event-study plot testing the parallel trends
assumption. Pre-period coefficients are close to zero and jointly
insignificant (p = 0.42), supporting the parallel trends interpretation.
```

## Anti-Patterns

- Running 30 robustness checks without any criterion for selection
- Reporting only the checks where the result survived
- A robustness check that tests a different estimand than the main result
- Running the wrong check for the design (e.g., McCrary for a DiD)
- Not discussing checks that fail
- Adding a check because "another paper did it", not because it probes a real assumption
- Framing robustness as "passed all tests" without nuance

## Verification Before Completion

- [ ] Each check is justified by the identification strategy of the main result
- [ ] 4-8 checks total (not 30)
- [ ] Every check run by a script in `code/` that reproduces independently
- [ ] Results tabulated, including failures
- [ ] Narrative in the paper discusses both survivors and failures
- [ ] YAGNI respected — no check included "just to be safe"
- [ ] Paper text in the user's paper language; scripts and file names in English
