# Error Handling

- Surface `rc` codes explicitly when Stata returns an error.
- If output is truncated, read the full `log_path` with `stata_read_log`.
- Use `trace=True` for unclear do-file failures.
- Use `background=True` plus `stata_task_status` for long-running jobs.
- Use `stata_control(action="break", id=<session_id>)` to interrupt a running command in-session.
- Use `stata_control(action="cancel", id=<task_id>)` for background-task cancellation.
