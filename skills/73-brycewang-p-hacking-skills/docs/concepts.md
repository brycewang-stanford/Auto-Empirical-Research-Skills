# Concepts

## The garden, the card, the grid

A **design card** is JSON: one key per researcher degree of freedom, each
listing the levels a referee would accept. The engine enumerates the
Cartesian product (with design-specific constraints) into a **grid** of
specifications; each has a label and a 12-character **key** (sha1 of the
label) that is the same in every language and every run. `phack size`
prints the multiplicity before anything is estimated.

## The ledger contract

Every search writes `ledger.csv` — one row per specification estimated,
with every analytical choice, `spec_json`, the estimate, its SE, t, p, the
one-sided p in the declared direction, and the **pathology flags**. A
search that cannot produce a ledger is a bug. The "best specification" is
never emitted alone.

## What a searched p-value is worth

For the best specification the audit reports, in increasing order of
trust: Bonferroni; Li–Ji effective tests; Romano–Wolf stepdown; and the
**null-calibrated p** — the share of null datasets on which *the identical
search* finds something at least as significant. For the whole curve it
reports the Simonsohn–Simmons–Nelson joint tests. `min_p_test_unflagged`
does the same for the best specification carrying no pathology flag,
against the unflagged part of the grid.

## Procedures

Exhaustive enumeration is what a multiverse does; a pressured analyst walks
sequentially with a stopping rule. `--procedure first_significant | random |
greedy | hill_climb` walks the grid that way, and the null calibration
replays the procedure, so the audit reports the **false-positive rate of
that way of searching** on that design. `--procedure split_sample` walks
in two stages — a search on a pilot share of the units, then the chosen
specification reported on the held-out units (`--stage holdout`, valid),
on all of them (`--stage pooled`, the pilot's luck inside the reported
test) or as the pilot estimate — and with `--continue-at` only continues
after a promising pilot, which is the selective continuation of Adda,
Decker & Ottaviani (2020).

## Distance and attribution

`nearest_significant` counts the analytical choices separating the
pre-registered specification from the nearest significant one;
`axis_influence` ranks the axes by how much the share significant varies
across their levels. Together they say *what* the search did.

## Pathology flags

Specifications that are citable but wrong stay in the ledger, flagged:
non-PSD two-way variance, few clusters, weak instruments, Wald/AR
disagreement, thin RDD sides, bias-corrected estimates with conventional
SEs, single stacks, extreme-group splits, event-study misuse. Null
calibration alone does not protect against a numerically broken corner
whose statistics are heavy-tailed; the flag does.

## Honest report

`report.md` is generated from the audit so its numbers cannot drift from
the ledger. It cannot be reduced to its sixth sentence because the sixth
sentence is not produced without the others.
