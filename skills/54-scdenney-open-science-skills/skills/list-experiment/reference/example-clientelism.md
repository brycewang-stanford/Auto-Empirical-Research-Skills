# Worked Example: A Clientelism Control List

A concrete illustration of §2–§3 and §6 of the parent `SKILL.md`. Numbers are realistic but illustrative; in practice, calibrate prevalences from pilot data or domain priors (e.g., Afrobarometer, LAPOP benchmarks).

## Context

Estimate the prevalence of election-related vote-buying in a developing-democracy survey. Direct questions are expected to underreport by ~5–15pp (Blair, Coppock & Moor 2020 domain benchmark). The sensitive behavior carries legal and social stigma, justifying the ~10× power cost of a list experiment.

**Estimand (π):** population share of voting-age adults who accepted money, gifts, or favors from a candidate or party in exchange for their vote during the most recent national election.

**SESOI:** 3 percentage points (smaller effects are not policy-relevant given the survey sample size and the cost of the design).

## Control items

All four items describe election-season political behaviors that are (a) non-sensitive, (b) plausibly uncorrelated with cash-for-vote transactions, and (c) calibrated so no single item is near 0 or 1. Expected prevalences in square brackets are priors from comparable surveys:

1. *Attended a political rally or campaign event during this election season.* [≈ 0.35]
2. *Displayed a political sign, poster, or bumper sticker for any party.* [≈ 0.20]
3. *Discussed candidates with family members or neighbors.* [≈ 0.65]
4. *Listened to or watched a politician's speech on the radio or television.* [≈ 0.70]

All items share grammatical form and abstraction level (past-tense, behavior-based, election-scoped), per the wording-parity rule.

## Sensitive item (treatment list only)

*Received money, gifts, or favors from a political candidate or party in exchange for voting for them.*

## Expected control-list distribution

Under approximate independence of the four items, the joint tails are:

- **Floor (sum = 0):** ≈ (1 − 0.35)(1 − 0.20)(1 − 0.65)(1 − 0.70) ≈ 0.055
- **Ceiling (sum = 4):** ≈ 0.35 × 0.20 × 0.65 × 0.70 ≈ 0.032

Both tails fall below the 10% rule-of-thumb threshold for the NFC assumption. If a pilot shows either tail > 10%, swap the offending item for one with more mid-range prevalence (0.30–0.70) or one that is less correlated with the others.

## Pre-field diagnostic (NFC priors)

Before fielding, simulate B = 10,000 synthetic respondents under the prior joint distribution (treating item correlations explicitly if pilot data allow) and confirm P(sum = 0) and P(sum = 4) each remain < 0.10. Record the simulation seed and code; deposit alongside the PAP.

## Post-field diagnostics

- **No-design-effect (NDE) test:** `ict.test(y, treat, J = 4)` from the `list` R package (Blair & Imai 2012). Null hypothesis: no design effect. Report the p-value, the number of bootstrap iterations, and the `list` package version.
- **Floor/ceiling check:** Tabulate the control-group count distribution. Compare observed P(Y = 0) and P(Y = 4) to the pre-field priors above. Flag divergences > 10pp as potential design failures, not preference falsification (Frye et al. 2023).
- **Hausman specification test** (if a multivariate estimator is reported): `ict.hausman.test()` from the same package (Blair, Chou & Imai 2019). Large positive or any negative statistic indicates misspecification; prefer NLSreg if triggered.

## Reporting

Deposit (a) the exact wording of all four control items and the sensitive item, (b) the randomization seed and the R session info, (c) the `list` package version, (d) full output of `ict.test()` and (if applicable) `ict.hausman.test()`, and (e) the pre-field NFC simulation. Coordinate with `methods-reporting` for the full checklist.
