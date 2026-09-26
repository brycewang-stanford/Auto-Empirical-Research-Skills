---
name: phack-immunization
description: Make an empirical analysis robust to specification search, before or after the fact. Covers pre-registration and pre-analysis plans encoded as design cards, specification-curve reporting with the Simonsohn joint tests, Romano-Wolf and effective-multiplicity corrections, full-procedure null calibration including for sequential searches, the distance-from-pre-registration diagnostic, split-sample and holdout designs, and the auto-generated honest report. Use when asked how to protect an analysis against p-hacking, how to correct inference after a search has happened, how to write a pre-analysis plan, or how to report a multiverse credibly.
---

# Immunising an analysis

Two situations, two answers.

## A. Before the data are analysed

**Pre-specify one specification, and pre-specify the grid around it.**

A pre-analysis plan that names a single specification is good. One that also
names the *set* of defensible alternatives is better, because it converts every
later robustness check from a discretionary choice into a committed one. Write
the design card (`02-forking-paths`) with a `preregistered` block and a
`direction`, deposit it, and let `phack size` print its key and its
multiplicity. The card *is* the pre-analysis plan for the analytical part.

Contents that matter, in order of how often they are omitted:

1. primary outcome, named singly, with its exact construction
2. the estimating equation, including fixed effects, the estimator (under
   staggered adoption: which one, and why) and the clustering level
3. sample inclusion rules, the exact date window, and the comparison group
4. the outlier rule and the missing-data rule
5. the subgroups to be examined, and that they are secondary
6. the multiplicity correction to be applied across outcomes and subgroups
7. the sign the hypothesis predicts, so a two-sided test cannot be swapped
   in later
8. what would count as a null result

**Split the sample.** Where N allows, hold out a confirmation sample and lock
it. Explore freely in the training half; the held-out half gets exactly one
analysis, the one that exploration selected. This converts a search into a
legitimate two-stage design and is by far the strongest available protection.
It is also measurable: `--procedure split_sample --stage holdout` runs it,
and the null replay prices it (`09-search-procedures`). On the null panel an
exhaustive search over 400 specifications reports p < .05 on 86% of null
datasets when the pilot estimate is reported, 45% when the pilot is pooled
into the confirmatory sample, and 10% on the held-out units alone; a greedy
walk from the pre-analysis plan with a continuation rule at pilot p < .10
reports on the held-out units at 4.8%. Two conditions, both from Adda,
Decker & Ottaviani (2020): the confirmatory sample must be **fresh** — pooling
the pilot in keeps half the inflation, and "we explored on half and confirmed
on everything" is optional stopping — and the held-out estimate must be run
with a **fixed inference doctrine**, because a pilot that picks the smallest p
picks anti-conservative standard errors, and fresh data does not cure a
standard error that under-states uncertainty everywhere (on this panel the
held-out estimate of a pilot-chosen `hc1` specification rejects 19% of the
time; a unit-clustered one, 5.6%). Selective *continuation* — running the
confirmatory stage only after a promising pilot — is fine on its own: it
changes which projects a registry sees, not the size of their tests.

**Blind the analysis.** Analyse with the treatment label permuted, fix every
analytical choice, then unblind. Everything decided under blinding is
pre-specified by construction. `search._draw_null` is exactly this
permutation and can be used to produce the blinded dataset.

## B. After a search has happened

The search is not the problem. Reporting one point from it as a confirmatory
test is. Five escalating repairs, all of which `phack search` performs at once:

### 1. Report the curve, not the point
Median coefficient, interquartile range, share significant, share flipping
sign, and the full ledger in a repository.

### 2. Test the curve, not the point
The Simonsohn–Simmons–Nelson joint tests (`ssn_joint`): is the median effect,
the share of significant specifications, or the share significant in the
predicted direction unusual against the null re-runs of the same curve? These
are the inferential statements a multiverse supports.

### 3. Correct the point for multiplicity, using the dependence
Bonferroni over S specifications is valid but badly conservative, because
specifications reuse the same rows. **Romano–Wolf stepdown** bootstraps the
joint distribution of the family and controls FWER while exploiting the
correlation. `effective_tests` (Li & Ji) tells you how much over-correction you
avoided.

### 4. Calibrate the whole search
The strongest repair. Re-run the *identical* search on data where the null
holds by construction, and report the share of null datasets on which the
search found something at least as significant. That is
`min_p_test.honest_p`, and it needs no assumption about how the specifications
are correlated because it re-runs the procedure rather than modelling it.

If the search was sequential rather than exhaustive — it usually was — replay
*that* procedure (`09-search-procedures`): `procedure_test.honest_p` is the
calibration for what was actually done, and
`null_share_reporting_significant` is its false-positive rate.

```bash
python scripts/phack_cli.py search DATA CARD --direction + \
    --null-draws 500 --null-scheme cluster_permute --n-jobs 8
```

Pick the null scheme to match the design — `cluster_permute` for a panel with
unit-level or staggered treatment, `permute_within_time` for within-period
assignment. A mis-specified null gives a too-tight reference distribution and
an honest p-value that is not honest.

### 5. Randomisation inference for the reported specification
Where treatment assignment is known, permutation inference on the single
reported specification is exact and assumption-free about the error structure.
The null draws already contain it: the column of `p_null.npy` for the reported
specification is its randomisation distribution. It does not fix multiplicity
— combine it with 3 or 4.

## Two diagnostics worth reporting even when nothing is significant

**Distance from pre-registration** (`nearest_significant`). How many
analytical choices separate the committed specification from the nearest
significant one, and which. Distance 1 is a design whose conclusion rests on a
single defensible-looking choice; say so.

**Attribution** (`axis_influence`). Which axis has the largest spread in the
share significant across its levels. If it is the standard-error doctrine or
the inference mode, the finding is about inference, not about the world.

## The honest report

`phack search` writes `report.md` from the audit; `phack report RUN_DIR`
regenerates it. It contains, in order: what was searched and its multiplicity;
the curve and the joint tests; the pre-registered specification and where it
sits; the most favourable specification, with every correction from
"as reported" down to the null-calibrated value; which choices did the work;
and a conclusion that follows from the honest p rather than the reported one.
The paragraph it produces reads like this:

> We estimated the effect under 301 defensible specifications, enumerated in
> advance and listed in the replication package. The pre-registered
> specification gives β̂ = −0.050 (SE 0.064, p = 0.44). Across the family the
> median estimate is −0.028, 1% of specifications are significant at 5% and
> none in the predicted direction; the Simonsohn joint test on the share
> significant gives p = 0.56. The most favourable specification gives
> β̂ = 0.214 (one-sided p = 0.036) and is eight analytical choices away from the
> pre-registered one; calibrated against 200 re-runs of the identical search on
> null data, the probability of a result at least this significant is 0.59. We
> therefore do not treat the result as evidence of a non-zero effect.

That paragraph is publishable and it is honest. The temptation it resists is
reporting only the sixth sentence — and because the report is generated from
the ledger, the sixth sentence cannot be produced without the others.

## What immunisation cannot do

None of this makes a fragile result robust. It makes fragility *visible* and
correctly priced. If the honest p-value is 0.59, the analysis has not found an
effect, and the right conclusion is that the design cannot resolve one — which
is itself worth reporting, and which pre-registration makes publishable.
