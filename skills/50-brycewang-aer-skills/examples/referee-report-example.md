# Example — Internal Referee Simulation

A worked example of `skills/aer-referee-sim/SKILL.md`, run against the same
fictional broadband paper as `intro-example.md`, `results-section-example.md`,
and `rebuttal-example.md`:

> *Broadband Expansion and Local Wage Inequality:
>  Evidence from the FCC's Connect America Fund*

In `rebuttal-example.md`, the authors submitted without an internal review
and spent a full R&R round fixing what referees found. This example shows
the counterfactual: the simulation run **before** submission catches the
same issues. Scores follow `docs/referee-report-rubric.md`.

---

## Run 1 — Draft v1

Draft v1 estimates a staggered two-way fixed-effects specification
(headline: 4.6 log points), reports a visual pre-trends plot with no joint
test, no Goodman-Bacon decomposition, no sensitivity bounds, and concludes
that "broadband expansion reduces welfare."

### Stage 1 — Desk screen

```text
DESK DECISION: reject

LETTER: Thank you for submitting your manuscript. The question is
important, and the ZIP-code-level deposit data appear genuinely novel.
I am nonetheless declining to send the paper to referees. The design
exploits staggered adoption across ZIP codes, but the estimates come
from a pooled two-way fixed-effects specification, which is biased
under heterogeneous treatment effects and which referees at this
journal reject on sight; the manuscript reports no decomposition or
heterogeneity-robust estimate that would bound the problem. Pre-trends
are asserted from a figure without a formal test. The welfare claim in
the conclusion also runs well ahead of the reduced-form evidence. I
would be willing to look at a substantially revised version built on a
heterogeneity-robust estimator.
```

The screen stops at desk-rejection-audit items 6-8 (heterogeneity-robust
estimator, Bacon weights, joint pre-trends test). Per the skill's
calibration rule, a Stage 1-2 audit failure ends the run — no referee
stage is simulated for v1. The revise list routes to `aer-identification`.

---

## Run 2 — Draft v2

Draft v2 is the version shown in `intro-example.md`: Callaway-Sant'Anna
estimator (4.2 log points, s.e. 1.1), joint pre-trends test (p = 0.71),
Goodman-Bacon decomposition, Honest DiD bounds, and a benefit-cost section
in place of the welfare claim.

### Stage 1 — Desk screen

```text
DESK DECISION: send to referees

LETTER: The contribution is stated by page 2, the design is modern and
defended with three pieces of evidence, and the exhibits are in house
style. I am sending the paper to three referees. My own reservation,
which the referees should weigh, is whether auction assignment based on
engineering costs is plausibly unrelated to local industry composition.
```

### Stage 2 — Referee 1 (identification specialist)

```text
SUMMARY: The paper estimates the effect of subsidized broadband on
within-ZIP wage inequality using staggered CAF II rollout and a
Callaway-Sant'Anna design. The design is competently executed; my
concerns are about what the identifying variation contains and how much
the conclusions lean on the point estimate.

MAJOR COMMENTS:
1. Assignment is by engineering-cost criteria (p. 7), and Table 2 shows
   funded ZIP codes have 14 percent lower baseline coverage and a
   different industry mix. Engineering costs plausibly correlate with
   terrain, density, and hence industry composition — a confounder with
   its own wage-inequality trend. Please add commuting-zone-by-year
   fixed effects as a main specification, not a robustness row, and
   show the result with a leave-one-out exposure measure.
2. The Honest DiD bounds (Fig. A.6) are reported but not interpreted:
   at M-bar = 1 the lower bound on the six-year effect is 1.1 log
   points. The abstract's "4.2 log points" should be accompanied in the
   text by what survives the sensitivity analysis (p. 19).
3. Anticipation: auction results were public roughly 18 months before
   build-out (p. 8). If employers or workers respond at announcement,
   the t = -1 baseline is contaminated. Please re-estimate dating
   treatment from the announcement and report both event studies.

MINOR COMMENTS:
1. Report the number of treated clusters per cohort under the
   bootstrap (Table 3 notes).
2. State the never-treated vs. not-yet-treated comparison-group choice
   in the text, not only in the table note.

RECOMMENDATION: major revision
```

### Stage 2 — Referee 2 (field expert)

```text
SUMMARY: The question — distributional incidence of broadband — is well
chosen and the CAF II variation is new to this literature. The marginal
contribution over Akerman, Gaarder and Mogstad (2015) and Hjort and
Poulsen (2019) is the within-area distributional margin; that claim
survives my reading of the antecedents.

MAJOR COMMENTS:
1. The mechanism evidence (Table 5) cannot yet separate skill-biased
   adoption from industry composition: tradeable services are also the
   sector with the strongest secular wage growth in this period. An
   industry-by-year control set, or a shift-share placebo using
   pre-period industry shares, would distinguish the two.
2. Magnitudes are asserted to be "roughly one-third of the import-
   competition effect" (p. 21) without aligning horizons or treatment
   intensities. Either do the alignment explicitly or drop the
   comparison.
3. Composition: the in-migration null (Table 6, cols 3-5) uses ACS
   one-year flows, which are noisy at the ZIP level. The balanced
   never-mover panel is the better test; promote it to the main text
   and report its power against the migration story.

MINOR COMMENTS:
1. Cite the published AEJ version of one antecedent currently cited as
   a working paper.
2. The 90/10 ratio should be defined in levels or logs consistently in
   Section II.

RECOMMENDATION: major revision
```

### Stage 2 — Referee 3 (generalist)

```text
SUMMARY: A clean design on a first-order policy question, readable by a
non-specialist. The paper under-delivers on interpretation relative to
the quality of its empirics.

MAJOR COMMENTS:
1. The benefit-cost section (Sec. V) reports a ratio of 1.3 under
   equal welfare weights but does not say what weights flip the sign.
   One paragraph and one appendix figure would make this the paper's
   most-quoted result.
2. External validity is unaddressed: CAF II targets high-cost rural
   areas, so the estimate speaks to the rural margin of the subsidy
   debate, not to urban broadband policy. Say so in the conclusion.
3. Exhibits: Figure 3 (distributional decomposition) carries the
   paper's second headline claim but sits in the appendix while Table 6
   (null migration checks) occupies the main text. Swap them.

MINOR COMMENTS:
1. Two table notes omit the number of clusters.
2. Two instances of "highly significant" (pp. 19, 23) — report the
   level.

RECOMMENDATION: major revision
```

### Stage 3 — Editor synthesis

```text
RUBRIC SCORES: contribution 4, identification 3, data 4, robustness 3,
magnitudes 3, exposition 4, integrity 4

VERDICT: major R&R

DECISION LETTER: All three referees see a publishable contribution.
The revision must (i) address the cost-criteria confounding with
commuting-zone-by-year fixed effects and a leave-one-out exposure
measure (R1.1, R2.1 — these are the same concern from two directions),
(ii) re-date treatment from auction announcement (R1.3), and (iii)
re-anchor the headline claims to what the sensitivity bounds support
(R1.2). The interpretive requests (R3.1-R3.3) are inexpensive and
should all be taken.

REVISE LIST:
  blocking: none
  major: R1.1 + R2.1 (confounding)        -> aer-identification / aer-robustness
         R1.3 (anticipation dating)        -> aer-identification
         R1.2 (bounds-aware headline)      -> aer-paper-body / aer-consistency
         R2.2 (magnitude benchmarking)     -> aer-paper-body
         R2.3 (composition test power)     -> aer-robustness
         R3.1 (welfare-weight threshold)   -> aer-paper-body
  minor: R3.2, R3.3, all referee minors    -> aer-paper-body / aer-tables-figures
```

A third run on the revised draft returned major R&R again with no new
major comments; with two consecutive runs at the threshold and zero
blocking comments, the exit condition in `aer-referee-sim` is met and the
draft proceeds to `aer-replication` and `aer-submission`.

---

## What This Example Demonstrates

| Element | Where | Why it matters |
|---|---|---|
| Desk screen ends Run 1 | Stage 1, v1 | Audit failures stop the run; no referee time on a broken design |
| Three distinct priors | Stage 2 | R1 attacks variation, R2 attacks novelty/mechanism, R3 attacks interpretation — no overlap padding |
| Anchored comments | All reports | Every major comment cites a page, table, or figure and states what would resolve it |
| Convergent findings | R1.1 + R2.1 | Independent reports converging on one flaw is the strongest internal signal a real referee will find it too |
| Calibrated verdict | Stage 3 | Scores map through the rubric; major R&R is the *good* outcome, not a disappointment |
| Routed revise list | Stage 3 | Each comment is assigned to the skill that fixes it, closing the loop in `aer-workflow` |

The overlap with the real reports in `rebuttal-example.md` is the point:
the simulation surfaces the TWFE critique, the industry-composition
concern, and the welfare overclaim **before** submission — the issues that
cost the fictional authors a full R&R round.
