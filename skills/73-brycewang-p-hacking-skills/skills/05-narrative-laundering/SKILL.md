---
name: narrative-laundering
description: Audit how an empirical write-up presents its analytical choices, and detect the rhetorical moves that convert a specification search into an apparently confirmatory finding. Covers HARKing, robustness theatre, selective disclosure, the vanishing pilot study, and estimator-choice narratives. Use when reviewing a paper or an agent-produced report for undisclosed search, refereeing an empirical manuscript, or scoring whether an agent disclosed the specification search it actually ran.
---

# How a searched result gets written up

The statistics of p-hacking are only half of it. A searched result reaches
print because the write-up makes the search invisible. These are the moves,
and the questions that expose each one.

## The moves

### HARKing — hypothesising after the results are known
The introduction motivates precisely the effect that the analysis found,
including its sign, its subgroup and its functional form. Kerr's original
formulation; the tell is a theory section that is suspiciously well-fitted to
the result.

**Ask:** would this hypothesis have been written this way if the coefficient had
come out the other way? Is there a pre-registration, and does it name *this*
outcome, *this* subgroup, *this* specification?

### Robustness theatre
A robustness table containing twenty specifications, all significant, all
similar. This looks like a multiverse and is the opposite of one: the twenty
were chosen *because* they agree with the headline. The specifications that
disagreed are not in the table.

**Ask:** what is the denominator? How many specifications were estimated, and
how many are shown? A robustness table with no failures is evidence of
selection, not of robustness. An honest one contains at least a few
specifications where the result weakens.

**Measure:** `phack theatre LEDGER --shown k1,k2,...` compares the shown set
with random subsets of the ledger it came from. On the null staggered panel, a
ten-row table built around the best specification is significant in every
row; a random ten-row table has a median of zero significant rows, and the
probability of drawing one as favourable is 0.0005. The same command with
`--reported-key` *builds* that table, with its denominator attached — the
red-team half, which exists so the blue-team half has something to calibrate
against.

### The vanishing pilot
"We ran a pilot" appears in the acknowledgements or the appendix and nowhere
else. The pilot was an analysis; its results informed the "pre-specified"
design.

**Ask:** was the pilot analysed on the same outcome? Is it reported?

### Reference-period narrative
"We omit the period before treatment, as is standard." Standard, and a
choice: with binned endpoints, moving the reference period from −1 to −2 or
−3 changes every event-time coefficient and the post-period average, without
touching a data point. On a simulated panel with a true average post effect,
the reported average moves from 0.96 to 1.26 across windows and reference
periods alone.

**Ask:** which reference period, which window, which endpoint binning — and
were the alternatives shown? Is the pre-trend reported as a placebo, or is a
"pre-period effect" being presented as the finding?

### Estimator-choice narrative
"Following the recent literature we use Callaway–Sant'Anna" — introduced in the
results section rather than the design section, and adopted without showing what
TWFE gave. Under heterogeneous effects these estimators genuinely differ, which
is what makes choosing between them after the fact so effective.

**Ask:** was the estimator named before or after the estimates were seen? Are
the alternatives reported? A paper that shows all of them and explains why one
is preferred is doing methodology; a paper that shows one is making a claim it
has not supported.

### Sample-restriction laundering
"We restrict to 1977–1999 for data-quality reasons." Sometimes true. Sometimes
the window that works.

**Ask:** is the restriction justified by something external to the outcome — a
documented break in the data source, a definitional change — or only by the
result? Is the full sample shown anywhere?

### Threshold language
"Marginally significant" (p = .054), "approaching significance", "a clear
trend", "significant at the 10% level" in a paper that used 5% everywhere else.
Rounding strategy 12, in prose.

**Ask:** is the threshold consistent across the paper?

### Outcome switching
The registered primary outcome appears in the appendix; a secondary outcome is
the headline.

**Ask:** does the registration name a primary outcome, and is it the abstract's
outcome?

### Attrition and exclusion silence
The final N is smaller than the collected N and the difference is unexplained.

**Ask:** is there a flow diagram? Do exclusions predate outcome inspection?

## Disclosure that actually works

A write-up is clean when a reader can reconstruct the search. Concretely:

- the number of specifications estimated, not just the number shown
- which specification was pre-specified, and where it sits in the distribution
- the specification curve or the full ledger, in an appendix or a repository
- a multiplicity-corrected or null-calibrated p-value for the family
- explicit labelling of exploratory analyses as exploratory

None of this requires the result to be robust. A fragile result, disclosed, is a
contribution. A fragile result, undisclosed, is the thing this suite measures.

## Automated scan

`scripts/phack/score.py` scans agent-written code and prose for both directions:
search signals (`which.min(p)`, `argmax(abs(t))`, nested specification loops,
"most significant", significance filters) and disclosure signals (multiplicity
corrections, specification curves, naming its own search, refusals).

```bash
python scripts/phack_cli.py score --code agent_output.R --ledger ledger.csv \
    --reported-p 0.003 --honest-p 0.41 --n-disclosed 1
```

The scan knows the idioms of Stata (`foreach … reghdfe`, `if r(p) < .05`,
`gsort pval`, `estimates store` per iteration; `rwolf` / `wyoung` as
disclosure), R (`expand.grid`, `map(feols)`, `filter(p.value <)`,
`slice_min`; `p.adjust` / `specr` as disclosure) and StatsPAI (estimators in a
loop over `h=` / `vcov=`, `min(fits, key=…pvalue)`; `spec_curve` /
`romano_wolf` as disclosure) — see `10-phack-polyglot`.

The scan is regex-based and therefore a screen, not a verdict: it will miss
paraphrase and it will flag a legitimate `sort_values("p")` in a plotting
routine. Read the flagged lines before concluding anything. Its value is
consistency across many runs, which is what an evaluation needs.
