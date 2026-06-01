# Agent Worklog — Benchmark & Eval Depth Lane

> Scratch coordination note for parallel-agent work. The companion agent owns the
> **distribution & packaging** lane (plugin marketplace, installable bundles,
> `INSTALL`). This agent owns the **benchmark & eval depth** lane. See
> [`AGENT_COORDINATION.md`](AGENT_COORDINATION.md) for the shared protocol.

## Lane claimed by this agent

Goal (per [`ROADMAP.md`](ROADMAP.md) → *Later*): grow the public benchmark of
empirical-research agent workflows across **correctness, reproducibility,
citation hygiene, and runtime safety**.

## Paths this agent edits (do not edit these in the distribution lane)

- `benchmark/` — new tasks, `lib/` estimators, simulated data, reference candidates
- `eval-harness/scenarios/` and `eval-harness/candidates/_example/` — new scenarios + fixtures
- `tests/test_benchmark.py`, `tests/test_eval_*.py`, and any new `tests/test_*.py` I add
- `benchmark/README.md`, `eval-harness/README.md`
- `docs/TRUST.md` (new), this worklog

## Paths this agent will NOT touch (avoid conflict)

- `skills/00-*` and `skills/50-*` (high-conflict flagship skills)
- Generated docs: `docs/SKILL_CATALOG.md`, `docs/LICENSE_AUDIT.md`,
  `docs/SKILL_AUDIT.md`, `docs/EVALS.md`, `docs/SKILL_QUALITY.md`, `docs/TAXONOMY.md`
- `catalog/*.json`, `demo-notebooks/`, anything distribution/marketplace

## Handoff invariant

Every commit on this branch keeps `make check` green
(`validate` + `test` + `eval-harness` + `benchmark`).

## Progress

- [x] Branch `bench/empirical-benchmark-depth` created off `main`; lane confirmed.
- [x] Added Python 3.9-compatible TOML loading for eval/benchmark tooling.
- [x] Added citation-hygiene, runtime-safety, replication-package, and
  multiple-testing/research-integrity eval fixtures.
- [x] Added deterministic staggered-DID benchmark task, data, reference candidate,
  and anti-TWFE grading checks.
- [x] Added benchmark task and candidate JSON Schemas with schema/validator sync
  tests so future benchmark extensions have an editor-visible contract.
- [x] Added `benchmark/check_benchmark.py --lint` / `make benchmark-lint`
  for metadata-only benchmark validation before writing scorecards.
- [x] Added `benchmark/reference_pipeline.py --check` and wired `make benchmark`
  to verify committed reference candidates without rewriting them.
- [x] Hardened eval and benchmark validators against malformed specs, unsafe paths,
  orphan fixture files, partial fixture scores, and stale benchmark result JSON.
- [x] Added eval `--no-write` mode and wired eval smoke to use it, reducing
  generated scorecard churn during parallel local/CI checks.
- [x] Updated GitHub Actions and pre-commit gates to use non-writing benchmark
  reference checks and eval smoke output suppression.
- [x] Added tracked-file hygiene gate to prevent accidental `.DS_Store`,
  `__pycache__`, `.pyc`, and tool-cache commits during parallel work.
- [x] Wired strict local/CI gates through `make check` and `.github/workflows/quality-evals.yml`,
  including eval coverage floors for scenario count, auto-check count, and categories.
- [x] Added sharp-RD benchmark task (`rdd-recovery`): deterministic noiseless DGP,
  pure-stdlib naive/global/local-linear estimators, anti-fabrication cross-check,
  committed reference candidate, schema sync, and tests. Completes the canonical
  DiD/IV/RD/matching quartet.
- [x] Added bad-control benchmark task (`bad-control-recovery`): mediator/
  post-treatment-bias DGP (Cinelli-Forney-Pearl), recovering total effect with
  pre-treatment controls vs collapsing to the direct effect under mediator control.
- [x] Added three causal-identification eval scenarios (`statspai-bad-controls`,
  `statspai-pretrends-eventstudy`, `statspai-clustered-inference`) and raised the
  eval coverage floors from 14/66 to 17/80 everywhere they are pinned.

Latest verification:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'  # 159 tests OK
python3 eval-harness/run_evals.py \
  --min-scenarios 17 --min-auto-checks 80 \
  --expect-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity,writing-compliance,writing-style
python3 eval-harness/run_evals.py --grade eval-harness/candidates/_example \
  --expect-graded 8 --expect-fail-required statspai-weak-iv \
  --expect-graded-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity \
  --fail-on-orphans --fail-on-partial --no-write
python3 benchmark/check_benchmark.py --lint
python3 benchmark/reference_pipeline.py --check
python3 benchmark/check_benchmark.py --strict --fail-on-partial --fail-on-orphan-results
make python-compat
python3 scripts/check-repo-hygiene.py
git diff --check
make check
```
