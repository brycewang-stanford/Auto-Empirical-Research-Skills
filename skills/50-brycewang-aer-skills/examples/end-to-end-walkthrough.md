# Example — End-to-End Walkthrough: One Paper Through All Twelve Steps

The other examples in this directory each show one station of the pipeline.
This walkthrough shows the whole line: the same fictional paper —

> *Broadband Expansion and Local Wage Inequality:
>  Evidence from the FCC's Connect America Fund*

— traced from a topic memo to an R&R response, naming at every step the skill
that does the work, the gate that must pass before the next step, and the
artifact the step leaves behind. It stitches together the worked examples that
already exist ([`intro-example.md`](intro-example.md),
[`results-section-example.md`](results-section-example.md),
[`referee-report-example.md`](referee-report-example.md),
[`rebuttal-example.md`](rebuttal-example.md)) so you can see that they are not
independent demos but snapshots of one project moving through the gates in
[`../docs/workflow-map.md`](../docs/workflow-map.md).

## The route at a glance

| # | Step | Skill | Gate to pass before moving on | Artifact left behind |
|---|------|-------|-------------------------------|----------------------|
| 1 | Topic + venue | `aer-topic-selection` | one sharpest claim survives the "competent extension" test; venue routed | topic memo |
| 2 | Literature map | `aer-literature` | antecedents map built from fetched records; citation ledger opened | closest-papers map, `references.bib` |
| 3 | Identification | `aer-identification` | design survives the modern-estimator audit — no naive TWFE | design memo, estimator choice |
| 4 | Robustness plan | `aer-robustness` | referee-anticipating checks specified *before* estimation | pre-analysis robustness grid |
| 5 | Body sections | `aer-paper-body` | every claim traces to an exhibit or a ledger entry | data/strategy/results/mechanisms drafts |
| 6 | Introduction | `aer-introduction` | five-paragraph architecture; 100-word abstract | intro + abstract |
| 7 | Exhibits | `aer-tables-figures` | booktabs tables, self-contained notes | publication tables and figures |
| 8 | Consistency audit | `aer-consistency` | all-pass on numbers, funnels, cross-references; ledger closed | audit report |
| 9 | Referee simulation | `aer-referee-sim` | desk screen + three adversarial reports reach ≥ major R&R on a fresh run | verdicts, routed revise list |
| 10 | Replication package | `aer-replication` | `run_all` reproduces every exhibit from raw inputs | openICPSR-ready deposit |
| 11 | Submission | `aer-submission` | format preflight, disclosures, desk-rejection audit | submission bundle |
| 12 | Rebuttal (after decision) | `aer-rebuttal` | every referee point answered with a concede/clarify/push-back/decline decision | response letter + aligned edits |

The router `aer-workflow` is the entry point whenever you are unsure where you
are; it does not perform work — it picks the next skill and reports gate status.

## Step 1 — Topic selection (`aer-topic-selection`)

The project starts as three candidate questions about federal broadband
subsidies. The skill forces the "one contribution per paper" cut: the
distributional question (who within a place gains?) survives because it is the
only one with a credible design *and* cross-subfield reach — labor (wage
structure), public (program evaluation), urban (place-based policy). The venue
memo routes it to AER rather than *Insights*: the mechanism evidence needs more
than 6,000 words. **Gate:** if the sharpest claim reads as "competent but
expected," the step loops rather than proceeds.

## Step 2 — Literature positioning (`aer-literature`)

The antecedents map places the paper against the broadband-employment and
skill-biased-technology literatures, from fetched records — never from memory.
Every entry lands in `references.bib` with a DOI that must verify against the
index (in this repository, that is the `make verify-citations` gate), and the
citation ledger opens: each "X finds Y" sentence gets a row that must be
checked against the paper's text before Step 8 can close it. **Gate:** a
phantom citation or a dangling key is a hard stop, exactly as
[`../docs/citation-integrity-protocol.md`](../docs/citation-integrity-protocol.md)
specifies.

## Step 3 — Identification (`aer-identification`)

Treatment (Connect America Fund Phase II buildout) staggers across ZIP codes,
so the skill's modern-default rules bind: naive two-way fixed effects is
disallowed as the headline estimator under staggered adoption with
heterogeneous dynamics (`goodmanbacon_2021`); the design memo selects the
group-time estimator of `callaway_santanna_2021` with `sun_abraham_2021` as the
interaction-weighted check. The
[`staggered-did-demo/`](staggered-did-demo/) shows in simulation exactly the
failure this rule prevents. Estimation is routed to validated implementations
— the StatsPAI tools or the pinned `templates/` stacks — not hand-rolled code.
**Gate:** the design must survive this audit *before any prose is written*.

## Step 4 — Robustness plan (`aer-robustness`)

Referee-anticipating checks are specified before estimation so they cannot be
cherry-picked after: pre-trends power (not just a flat plot), honest-DiD
relative-magnitude bounds (`rambachan_roth_2023`; see
[`honest-did-demo/`](honest-did-demo/)), a specification curve over defensible
choices (see [`spec-curve-demo/`](spec-curve-demo/)), Oster's R²-scaled
selection bound (`oster_2019`; see [`oster-ovb-demo/`](oster-ovb-demo/)), and
family-wise error control across the occupation-level outcomes (see
[`multiple-testing-demo/`](multiple-testing-demo/)). **Gate:** the grid exists
and is costed before a single headline regression runs.

## Step 5 — Body sections (`aer-paper-body`)

Body-first, introduction-last. The data section walks the sample funnel; the
results section narrates findings first and tables second, with the headline
effect — the 90/10 log wage ratio rising 4.2 log points (s.e. 1.1) over six
years — converted into magnitudes a reader can price (dollars per worker,
share of the observed inequality rise). See
[`results-section-example.md`](results-section-example.md) for the worked
version, including the "reading the table aloud" counterexample. **Gate:**
every claim traces to an exhibit or to a closed ledger row.

## Step 6 — Introduction (`aer-introduction`)

Only now, with results known, the five-paragraph introduction: hook (the $84
billion premise), question, design, findings-with-magnitudes, contribution.
The 97-word abstract sells results, not motivation. The full worked text is
[`intro-example.md`](intro-example.md). **Gate:** the abstract stays ≤ 100
words; the first three pages could survive a desk screen alone.

## Step 7 — Exhibits (`aer-tables-figures`)

Regression tables move to booktabs with per-column estimator labels and
self-contained notes; the event-study figure gets confidence bands and a note
that states the estimator, the comparison group, and the clustering level.
Every exhibit registers in the exhibit register of the replication skeleton
(see
[`replication-package-skeleton/docs/exhibit-register.md`](replication-package-skeleton/docs/exhibit-register.md)).

## Step 8 — Consistency audit (`aer-consistency`)

The audit reconciles every number in prose against its table cell, the sample
funnel against every N, units across conversions, cross-references, and the
bibliography — and closes the citation ledger opened in Step 2. In this
repository the same discipline is machine-enforced on the examples themselves:
prose citations must ground to verified bib keys (the groundedness gate) and
demo estimates must hit pinned targets (the `NUMERIC-CHECK` contract described
in [`README.md`](README.md)). **Gate:** all-pass, or the manuscript does not
advance.

## Step 9 — Referee simulation (`aer-referee-sim`)

A desk screen plus three adversarial referees with distinct priors, scored
against [`../docs/referee-report-rubric.md`](../docs/referee-report-rubric.md).
[`referee-report-example.md`](referee-report-example.md) shows both runs on
this paper: draft v1 (TWFE headline, visual-only pre-trends) desk-rejects;
the revised draft — after the revise list routed fixes back through Steps 3–8
— reaches major R&R. **Gate:** ≥ major R&R on a *fresh* simulation, not on the
run that generated the fixes.

## Step 10 — Replication package (`aer-replication`)

The deposit is built from
[`replication-package-skeleton/`](replication-package-skeleton/): raw → clean →
estimate → exhibits, one master script, a source register for every input, and
an AEA Data and Code Availability README. **Gate:** `run_all` reproduces every
exhibit from raw inputs on a fresh machine; a README that does not run is
grounds for Data Editor delay.

## Step 11 — Submission (`aer-submission`)

Format preflight (length vs. exhibit count, abstract word cap), disclosure
statements for each coauthor, and a final pass of
[`../docs/desk-rejection-audit.md`](../docs/desk-rejection-audit.md). The cover
letter stays minimal — COI disclosure and data-access notes only.

## Step 12 — Rebuttal (`aer-rebuttal`)

After the (real) referee reports arrive, every point gets one of four
dispositions — concede, clarify, push back, decline — each with aligned
manuscript edits. [`rebuttal-example.md`](rebuttal-example.md) is the complete
worked letter for this paper. The counterfactual claim of this walkthrough is
Step 9's: the internal simulation caught, before submission, the same issues
that cost the fictional authors a full R&R round.

## Reproducing this route on your own project

```bash
# scaffold the replication package
python3 scripts/scaffold_project.py skeleton /path/to/your-project

# then, inside your agent, start at the router
#   "Use aer-workflow: where am I, and what gate is next?"
```

The gates that guard this repository's own examples — citation verification,
groundedness, numeric-check smoke, skill audits (`make preflight`,
`make smoke-examples`) — are the same discipline the skills impose on a
manuscript: nothing advances on assertion; everything advances on a checked
artifact.
