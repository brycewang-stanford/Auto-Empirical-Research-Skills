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

## When to Loop

- **Identification rebuild** triggered by an R&R targeting the design → loop back to `aer-identification` then forward
- **Format-only revisions** → skip back only to `aer-tables-figures` or `aer-submission`
- **Venue change** after rejection → `aer-topic-selection` again, then `aer-introduction` for re-framing

## Cross-Cutting Checks

- Run [`desk-rejection-audit`](./desk-rejection-audit.md) before submission or
  after a rejection to find the first failure point in framing, identification,
  robustness, exhibits, or policy compliance.
- Use [`methods-reference`](./methods-reference.md) whenever
  `aer-identification` or `aer-robustness` asks for an estimator, diagnostic,
  package call, or primary citation.
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

`aer-workflow` is the entry point when the user is unsure where they are. It does not perform work — it picks the next skill.
