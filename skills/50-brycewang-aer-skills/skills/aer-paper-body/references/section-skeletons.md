# Section Skeletons — Body Sections with Topic-Sentence Plans

*Bundled with the `aer-paper-body` skill so the guidance works without the repository checkout. SKILL.md routes; this file carries the depth.*

Per-section skeletons for a full-length empirical AER manuscript. Each
skeleton is a topic-sentence-first paragraph plan: the first sentence of
every paragraph states its claim, and the first sentences read alone should
reconstruct the section (the reverse-outline test in `docs/style-guide.md`).

## Section I — Institutional Background

Give exactly the detail needed to (a) locate the identifying variation and
(b) believe the identifying assumption. Length 1.5-3 typeset pages.

Paragraph plan (topic sentence first, one claim per paragraph):

1. **The institution.** "The [program/policy] was created in [year] to
   [purpose]." Lead with the institution, not the literature.
2. **The assignment rule.** "Treatment was assigned by [rule]: who is
   treated, when, by what criterion, and who decided." If assignment is
   discretionary, say so here and name how the design handles it.
3. **The variation.** "The feature we exploit is [timing / cutoff /
   formula], which generated [comparison] for reasons unrelated to
   [outcome trends]."
4. **What participants knew.** Anticipation, announcement dates, and
   phase-in — anything that shifts the treatment date the design uses.

Rules: cite a primary source (statute, agency document, administrative
report) for every institutional claim; history appears only if it explains
the variation; surplus pages are literature review in disguise — cut them.

## Section II — Data

Referees check this section against the replication package line by line.

Paragraph plan:

1. **Sources.** "Our data combine [dataset A] with [dataset B]." For each:
   producer, access mode, years, unit of observation, citation.
2. **Sample construction.** "From the raw file of [N0] units, we construct
   an analysis sample of [Nk]." Then the funnel, every drop with a count
   and a rationale.
3. **Variables and measurement.** "The outcome is [precise definition with
   units]; treatment is [precise definition]." Discuss measurement error
   where a referee would: self-reports, imputation, top-coding, deflators
   (name the index and base year).
4. **Summary statistics.** Two to four facts from Table 1, each tied to a
   design decision — representativeness, pre-treatment comparability,
   distributional features that shape specification choices. Narrate; do
   not re-read the table aloud.

### Sample-funnel table template (exact-N rows)

Every row carries an exact count; the arithmetic must reconcile and match
the replication package exactly.

| Step | Restriction | Dropped | Remaining N |
|---|---|---|---|
| 0 | Raw extract, [source], [years] | — | 31,184 |
| 1 | Fewer than 500 working-age residents | 4,212 | 26,972 |
| 2 | Already above eligibility benchmark pre-period | 7,861 | 19,111 |
| 3 | Suppressed outcome cells in more than 3 years | 1,287 | 17,824 |
| — | Analysis sample (× 15 years = 267,360 unit-years) | — | 17,824 |

Reconciliation rules: each Remaining N equals the previous row minus
Dropped; the panel multiplication is stated and checkable; consequential
restrictions are flagged with a pointer to the robustness check that
relaxes them.

## Section III — Empirical Strategy

Mandatory order: **estimand → equation → identifying assumption →
inference**.

Paragraph plan:

1. **Estimand.** One sentence before any equation: "Our object of interest
   is the average effect of [treatment] on [outcome] among [population]
   over [horizon]." If the design recovers a local effect (LATE, effect at
   the cutoff, ATT for switchers), say so here.
2. **Equation.** Display, numbered, then defined.
3. **Identifying assumption.** One sentence, formal and in words, then the
   evidence.
4. **Inference.** Clustering level and why it matches the design.

### Estimating-equation presentation rules

```latex
Y_{ict} = \beta\, D_{ct} + \alpha_c + \gamma_t + X_{ict}'\delta + \varepsilon_{ict}
```

- Define every symbol in the sentence after the equation, every subscript
  included: what each index ranges over, what the treatment variable codes.
- Number displayed equations; refer to "equation (1)" thereafter.
- State which coefficient is the object of interest and what variation
  identifies it once the fixed effects absorb the rest.
- Keep subscript order consistent across every equation and table.
- For staggered adoption, write the group-time estimand and its
  aggregation explicitly — do not present a two-way fixed-effects
  equation the estimator does not actually run.

### The identifying assumption in one sentence

```
The identifying assumption is that, absent [treatment], [treated units]
would have followed the same [outcome] trend as [comparison units].
```

Follow immediately with the "assumption — threat — evidence" unit: name
the two or three most plausible violations and point to where each is met
(pre-trend test, placebo, design diagnostic, sensitivity bounds).

### Inference paragraph

One paragraph: clustering level and why it matches the level of the
identifying variation, the number of clusters, and any correction (wild
cluster bootstrap for few clusters; design-specific inference where the
design demands it). Never leave inference to the table notes alone.

## Section IV — Results

### Conclusion-first narration rules

One paragraph per claim, not per table. Anatomy of every results paragraph:

1. **Finding first.** The opening sentence states the economic finding
   with its magnitude: "The reform raises earnings by 4.2 percent
   (Table 3, column 4)" — never "Table 3 presents the results."
2. **Evidence.** Where the number comes from and how it moves across
   specifications; name the headline column carried through the paper.
3. **Interpretation.** Convert the coefficient and benchmark it.

The first sentences of the results paragraphs, read alone, must narrate
the paper's entire empirical arc.

### Effect-size triple conversion

Every headline coefficient gets all three:

| Conversion | Rule |
|---|---|
| **Percent** | Exact units: a log-outcome coefficient is log points; use 100·(e^β − 1) whenever the coefficient exceeds 0.10 in absolute value; never confuse percent with percentage points |
| **Percentile / SD** | Relative to the sample: against the outcome mean or standard deviation, or as a move in the outcome distribution |
| **Money metric** | Dollars (or the local currency) per unit treated per period, so the magnitude is comparable to program cost and to the literature |

Report the baseline rate next to every binary marginal effect. If the
implied magnitude is implausible, say so and investigate before a referee
does.

### Back-of-envelope paragraph template

Close a high-impact results section with one disciplined aggregate
calculation — every input sourced, one visible chain, honest rounding:

```
The estimates imply [aggregate quantity]. [Program] disbursed [$A] per
year across [B units] holding [C people], or [$A/C] per person per year.
Our column [k] estimate implies [effect × base = $X] per person per year
in [outcome]. Whether this passes a cost-benefit test depends on
[the one assumption that decides it]; under [assumption 1] it does,
under [assumption 2] it does not.
```

If it needs more than a paragraph, it becomes its own short section.

### Anti-pattern contrast — reading a regression table aloud

**Bad (column-by-column narration).**

> Table 3 presents the results of estimating equation (1). Column 1 shows
> the baseline specification; the coefficient is 0.038 and is significant
> at the 1% level. Column 2 adds controls and the coefficient is 0.037.
> Column 3 adds region-by-year fixed effects and the coefficient becomes
> 0.036. These results suggest the program may play an important role.

No sentence states the finding; coefficients recited without units;
significance carries the narration; the close hedges an identified effect
into mush.

**Good (conclusion-first paragraph).**

> The program raises single-parent employment by 3.7 percentage points off
> a 61 percent base (Table 3, column 3) — a 6 percent increase, 0.11
> standard deviations of the county distribution, and roughly one new job
> per $23,000 of program spending. The estimate is stable as controls and
> region-by-year fixed effects are added (columns 1-3); column 3 is the
> specification we carry through the paper.

Finding first with magnitude; the triple conversion in one sentence; the
specification walk compressed to one sentence with a named headline column.

### Robustness pointers

The results section cites robustness, it does not contain it: one summary
paragraph plus the single most important check shown inline; the full
battery lives in the appendix.

## Section V — Mechanisms

Organize by candidate explanation — by channel, not by table.

Paragraph plan:

1. **Name the channels.** "Three channels could produce [pattern]:
   [channel A], [channel B], [channel C]" — including the ones to be
   ruled out.
2. **Favored channel.** Its theory-predicted heterogeneity and auxiliary
   outcomes: "if the channel is [A], effects should concentrate in
   [subgroup] — they do (Table 5)."
3. **Each alternative, steelmanned.** State the sharpest version of the
   referee's objection, then the evidence against it.
4. **Calibrated close.** "Most consistent with [channel]" — never "we
   prove the mechanism." Mechanism evidence is consistency evidence; only
   the main effect carries design-based identification.

## Section VI — Conclusion

Half a page to one page. What belongs, in order:

1. The question and the headline magnitude restated in fresh words — no
   sentence copied from the abstract.
2. The external-validity boundary: population, period, policy margin, and
   the complier or locality caveat if the design implies one.
3. The one policy or theory implication the evidence supports — one step
   beyond the results, never three.
4. At most two sentences on specific open questions this paper makes
   answerable.

What does not belong: new results, new citations, new caveats that should
have appeared in Results, a rewritten abstract, or "more research is
needed."

## Canonical repo sources

Distilled from these repository files (full versions require the
repository checkout):

- `skills/aer-paper-body/SKILL.md`
- `examples/results-section-example.md`
- `docs/style-guide.md`
