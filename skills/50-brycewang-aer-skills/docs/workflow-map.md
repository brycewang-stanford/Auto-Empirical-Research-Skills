# Workflow Map

The intended journey through the AER-skills stack.

## Linear Default

```
┌─────────────────────┐
│  aer-topic-selection│   Topic + venue routing (AER / Insights / AEJ)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   aer-literature    │   Closest-papers map, novelty scan, citation integrity
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  aer-identification │   Design-based identification, modern estimators
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   aer-robustness    │   Heterogeneity, mechanism, placebo, anticipation
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   aer-paper-body    │   Data, strategy, results narration, magnitudes, conclusion
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  aer-introduction   │   Five-paragraph intro + 100-word abstract
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ aer-tables-figures  │   Booktabs, regression tables, figure notes
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   aer-consistency   │   Numbers vs tables, sample sizes, refs, citations
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   aer-referee-sim   │   Desk screen + three adversarial referee reports
└──────────┬──────────┘   (loop back to the routed fix skill until ≥ major R&R)
           │
           ▼
┌─────────────────────┐
│   aer-replication   │   AEA Data and Code Availability deposit
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   aer-submission    │   Format preflight, cover letter, conflicts
└──────────┬──────────┘
           │
           ▼ (after decision)
┌─────────────────────┐
│    aer-rebuttal     │   R&R response letter + aligned manuscript edits
└─────────────────────┘
```

## Quality Gates

For end-to-end drafting, the sequence is a set of gates (details in
`aer-workflow`): the design must survive `aer-identification` before any
prose; every claim must trace to an exhibit or a verified citation before
the introduction; `aer-consistency` must report all-pass and the
`aer-literature` citation ledger must be closed before `aer-referee-sim`;
and the simulated verdict must reach major R&R on fresh runs before
`aer-submission`.

## When to Loop

- **Identification rebuild** triggered by an R&R or by `aer-referee-sim`
  targeting the design → loop back to `aer-identification` then forward
- **Novelty hit** (a closer paper surfaces) → `aer-literature` then
  `aer-topic-selection` to re-cut the contribution
- **Format-only revisions** → skip back only to `aer-tables-figures` or `aer-submission`
- **Venue change** after rejection → `aer-topic-selection` again, then `aer-introduction` for re-framing
- **Any revision round** → re-run `aer-consistency` before anything ships

## Cross-Cutting Checks

- Run [`desk-rejection-audit`](./desk-rejection-audit.md) before submission or
  after a rejection to find the first failure point in framing, identification,
  robustness, exhibits, or policy compliance.
- Use [`methods-reference`](./methods-reference.md) whenever
  `aer-identification` or `aer-robustness` asks for an estimator, diagnostic,
  package call, or primary citation.
- Apply [`style-guide`](./style-guide.md) to every page of prose the writing
  skills (`aer-paper-body`, `aer-introduction`) produce.
- Score internal reviews with the
  [`referee-report-rubric`](./referee-report-rubric.md) so `aer-referee-sim`
  verdicts stay calibrated across runs.
- Check [`source-register`](./source-register.md) before changing journal
  policy, AEA replication, or submission-limit language.

## Optional Implementation Engine

The `aer-identification` → `aer-robustness` stages decide *what* to estimate and
*which* diagnostics to report. To actually *run* them you have two choices:

- the language-native `templates/` (Stata / R / Python), or
- [`aer-statspai`](../skills/aer-statspai/SKILL.md) — an agent-native unified
  Python engine + MCP server (`detect_design → recommend → fit → audit_result →
  sensitivity → bibtex`) that also exports publication-ready tables for
  `aer-tables-figures`.

`aer-statspai` executes the design; it does not override the modern-default
rules in `aer-identification`. For a top-5 main result, cross-check a StatsPAI
estimate against a `templates/` reference implementation.

## The Router

`aer-workflow` is the entry point when the user is unsure where they are. It does not perform work — it picks the next skill and reports gate status.
