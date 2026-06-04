# Tool Reference

Use these tools as the core Stata execution surface:

- `stata_run` for ad hoc commands and `.do` files.
- `stata_load_data` to load a dataset before analysis.
- `stata_inspect_data` for `describe`, `summary`, `codebook`, `search`, `list`, `get`, and `lint`.
- `stata_get_results` for stored `r()`, `e()`, and `s()` results.
- `stata_manage_graphs` for listing and exporting graphs.
- `stata_manage_session` for detection, session lifecycle, UI-channel access, and history diff.
- `stata_task_status` and `stata_control` for background jobs and interrupts.
- `stata_read_log` for full logs when direct output is truncated.

When the user asks whether mcp-stata is available, verify with `stata_manage_session(action="detect")` and include the detected Stata version and flavor in the reply.
