# Troubleshooting Flow

Start with:

1. `stata_manage_session(action="detect", include_packages=True)`
2. the smallest failing `stata_run(...)`
3. `stata_read_log` if the result is truncated

Common buckets:

- `STATA_PATH` missing or wrong
- missing user-written packages such as `reghdfe` or `gtools`
- startup/profile side effects
- permissions problems affecting temp files, logs, or graphs
- workstation differences across lab or coauthor machines

Use `scripts/report_environment.py` to summarize the environment deterministically before recommending a fix.
