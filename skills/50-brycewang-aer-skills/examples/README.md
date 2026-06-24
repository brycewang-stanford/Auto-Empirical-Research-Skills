# Examples

Worked examples that show what the skills produce in practice.

## Contents

| File | What it shows |
|---|---|
| [`aer-exemplars.md`](aer-exemplars.md) | Classic AER and adjacent-top-5 papers mapped to each skill, with openICPSR / Dataverse links |
| [`modern-aer-exemplars.md`](modern-aer-exemplars.md) | 30+ recent (2018-2025) AER and AEJ papers organized by subfield (Labor, Public, Development, Trade, Macro, IO, Health, Environment, Urban, Education, Finance, Political Economy, Social Networks) plus an Identification-Methods table — all with deposit links |
| [`intro-example.md`](intro-example.md) | A full Keith Head five-paragraph introduction + 97-word abstract, written to AER house style |
| [`results-section-example.md`](results-section-example.md) | Worked body-section narration — sample funnel, finding-first results paragraphs, magnitude conversions, back-of-envelope calculation, mechanisms organized by channel — plus a table-walk-through counterexample |
| [`rebuttal-example.md`](rebuttal-example.md) | A complete R&R response letter with cover letter, editor response, three referee responses, and a triage summary table |
| [`referee-report-example.md`](referee-report-example.md) | A full internal referee simulation — desk screen, three adversarial reports with distinct priors, rubric-scored editor synthesis, and the routed revise list — run on the same fictional paper before submission |
| [`skillopt-routing-scenarios.json`](skillopt-routing-scenarios.json) | SkillOpt-style selection/test routing scenarios used by `scripts/run_skillopt_gate.py` |
| [`replication-package-skeleton/`](replication-package-skeleton/) | A deposit-ready directory layout with AEA-compliant README, master script, globals file, [`data/codebook/source-register.md`](replication-package-skeleton/data/codebook/source-register.md), and [`docs/exhibit-register.md`](replication-package-skeleton/docs/exhibit-register.md). Drop-in starting point for your own openICPSR submission |
| [`staggered-did-demo/`](staggered-did-demo/) | Runnable Python/R simulation showing why TWFE fails under staggered adoption with heterogeneous dynamic effects |
| [`iv-weak-instrument-demo/`](iv-weak-instrument-demo/) | Runnable Python simulation showing why conventional 2SLS inference can over-reject with weak instruments and why Anderson-Rubin inference is safer |
| [`rdd-polynomial-demo/`](rdd-polynomial-demo/) | Runnable Python simulation showing why high-order global polynomials mislead in RDD and local-linear `rdrobust` is safer |

## How to Use

These examples are **reference architectures**, not paste-able content.
The fictional broadband paper used in `intro-example.md` and
`rebuttal-example.md` is consistent across both files so you can see how
the same project moves from initial draft to R&R revision.

To start your own project:

1. **Pick 2-3 papers from `aer-exemplars.md`** that match your design
2. **Read them as architecture templates** (reverse-outline in 30 minutes)
3. **Scaffold `replication-package-skeleton/`** into your project
4. **Use `intro-example.md` and `rebuttal-example.md`** as reference for
   the writing skills (`aer-introduction`, `aer-rebuttal`)

```bash
python3 scripts/scaffold_project.py skeleton /path/to/new-replication-package
```

Add `--dry-run` first if you want to inspect the planned copies.

Before copying an example's structure into a manuscript, cross-check the design
against [`../docs/methods-reference.md`](../docs/methods-reference.md) and run
the [`../docs/desk-rejection-audit.md`](../docs/desk-rejection-audit.md). The
examples show architecture; the audit and methods reference decide whether that
architecture is defensible for your paper.
