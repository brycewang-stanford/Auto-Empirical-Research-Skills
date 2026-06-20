---
name: stata-replication
description: Run replication, robustness, and specification-sensitivity workflows for Stata projects. Use when a researcher wants to reproduce a result, rerun a pipeline, compare specifications, audit a do-file sequence, or check whether a claim is stable.
---

# Replication And Robustness

Use this skill for reproducibility work rather than one-off execution.

1. Identify the replication entrypoint.
2. Run the baseline cleanly and capture logs and stored results.
3. Compare requested variants in a structured way.
4. Say whether the result truly replicates, partly matches, or breaks.

Read `references/workflow.md` for the replication checklist and use `scripts/compare_specs.py` and `scripts/summarize_log.py` for deterministic comparisons.
