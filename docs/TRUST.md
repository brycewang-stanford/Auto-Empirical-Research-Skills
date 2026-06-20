# AERS Trust Surface

This page summarizes the always-on checks that make AERS more than a large skill
catalog. The goal is to catch wrong empirical work, fabricated citations, and
unsafe runtime advice before a skill answer reaches a researcher.

## Quality Layers

| Layer | Path | What it catches |
|---|---|---|
| Repository validation | [`scripts/validate-repo.py`](../scripts/validate-repo.py) | Missing required files, stale generated artifacts, broken local links, malformed skill frontmatter warnings. |
| Workflow policy | [`scripts/validate-workflows.py`](../scripts/validate-workflows.py) | GitHub Actions without explicit permissions, persistent checkout credentials, untrusted-PR write permissions, floating action refs, `pull_request_target`, and pipe-to-shell workflow patterns. |
| Eval harness | [`eval-harness/`](../eval-harness/) | Rubric-level failures in flagship skill answers: weak-IV false reassurance, staggered-DID TWFE misuse, AER compliance gaps, citation fabrication, and runtime-safety mistakes. |
| Numeric benchmark | [`benchmark/`](../benchmark/) | Data-derived empirical results that must be recovered from real or deterministic datasets, with anti-fabrication cross-checks. |
| Python compatibility | [`Makefile`](../Makefile) | Syntax drift in repo-owned Python tooling across the Python 3.9/3.12 CI matrix. |
| Unit tests | [`tests/`](../tests/) | Parser behavior, scenario validation, benchmark truth computations, and grading edge cases. |

Run all local trust checks with:

```bash
make check
```

## Current Benchmark Coverage

The numeric benchmark is dependency-free and recomputes gold values every run.

| Task | Trap | Required proof |
|---|---|---|
| `lalonde-recovery` | Naive observational treated-minus-control comparison has the wrong sign. | Surface severe imbalance, report negative naive ATT, recover positive adjusted ATT, and match recomputed SMD/ATT values. |
| `card-iv-recovery` | IV result is easy to misreport or headline without instrument-strength evidence. | Recover positive OLS, IV > OLS, report first-stage F, and match recomputed OLS/IV/F values. |
| `did-staggered-recovery` | Plain TWFE is biased under staggered timing with dynamic heterogeneous effects. | Report biased TWFE as diagnostic, recover true ATT with group-time DID, and match recomputed simulated-panel values. |
| `rdd-recovery` | A naive across-cutoff mean difference confounds the jump with the running-variable trend. | Surface the biased naive jump, recover the true cutoff effect with a local-linear (running-variable-controlled) fit, and match recomputed RD estimands. |
| `bad-control-recovery` | Conditioning on a post-treatment mediator biases the estimate toward the direct effect (a "bad control"). | Recover the total effect with pre-treatment controls only, surface the mediator-adjusted estimate as biased, and match recomputed regression estimands. |

The benchmark deliberately checks reported numbers against recomputed truth. A
candidate cannot pass by inventing a clean balance table, a convenient first
stage, or a robust staggered-DID estimate. The CI benchmark gate runs with
`--strict --fail-on-partial --fail-on-orphan-results`, so reference candidates
must pass required golds and non-required diagnostic golds, and stale generated
scorecards from removed or renamed tasks fail the gate.

## Current Eval Coverage

`eval-harness/scenarios/*.toml` contains 17 scenarios and 95 rubric items.

| Category | Examples |
|---|---|
| Correctness | Staggered-DID estimator choice, weak-IV robust inference, RDD diagnostics, TWFE-trap warnings, bad-control/post-treatment bias, pre-trends discipline, and few-cluster inference. |
| Reproducibility | AER replication-package structure and AEA Data Editor readiness. |
| Citation hygiene | No fabricated DOI, URL, volume, issue, page-range, or other bibliographic metadata when the user only gives rough source anchors. |
| Runtime safety | Refusal to run `curl | bash` style replication setup, isolation before executing untrusted scripts, and protection of real credentials. |
| Research integrity | Multiple-testing discipline for post-hoc heterogeneity and mechanism claims. |
| Writing compliance | AER 100-word abstract, AER submission preflight, AER table/figure house style. |
| Style fidelity | Chinese and English de-AIGC/de-slop rewrites that preserve facts. |

The fixture smoke test is intentionally strict:

```bash
python3 eval-harness/run_evals.py \
  --min-scenarios 17 --min-auto-checks 80 \
  --expect-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity,writing-compliance,writing-style

python3 eval-harness/run_evals.py --grade eval-harness/candidates/_example \
  --expect-graded 8 --expect-fail-required statspai-weak-iv \
  --expect-graded-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity \
  --fail-on-orphans --fail-on-partial --no-write
```

Only the deliberately bad weak-IV fixture may fail required rubric items. Some
fixtures still report `needs-manual` for judgement-only rubric items; that is
intentional and prevents machine checks from being overstated as a complete
human review. The smoke gate also requires graded fixtures for causal
identification, reproducibility, citation hygiene, runtime safety, and research
integrity. Any new unexpected required failure, missing trust category, orphan
candidate file, or non-required machine-check regression breaks `make check`.
Routine gates use `--no-write` so scorecard files under `eval-harness/results/`
only change during intentional refreshes.

## Compatibility Floor

The quality job runs on Python 3.9 and 3.12. Python 3.9 matters because many
macOS contributors still use the system Python; `scripts/toml_compat.py` keeps
TOML-backed eval and benchmark tooling dependency-free on that floor.

## What This Does Not Prove

These checks are necessary, not sufficient. Regex rubrics do not certify prose
quality, and small numerical benchmarks do not cover every empirical design. The
trust surface is designed to fail fast on known high-cost mistakes and to make
future benchmark/eval expansion cheap and reviewable.
