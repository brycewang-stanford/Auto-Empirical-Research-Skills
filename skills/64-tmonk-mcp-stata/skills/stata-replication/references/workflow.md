# Replication Workflow

1. Identify the authoritative entrypoint.
2. Run the baseline cleanly and save the full log.
3. Capture stored results after each model.
4. Compare requested variants systematically.
5. Distinguish environment failures from substantive result changes.

Do not say a result replicates unless the target output materially matches.

Use:

- `scripts/compare_specs.py` for structured coefficient/spec comparisons
- `scripts/summarize_log.py` for long replication logs
