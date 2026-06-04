---
name: stata-log
description: Tail, read, or search a Stata log file from a previous command or background task.
---

Parse the argument:
- First token: log file path or background task_id
- Second token (optional): search term

**If a search term is provided**, call:
```
stata_read_log(path=<first_token>, query=<second_token>, before=2, after=2, regex=False)
```
Display matching lines with context.

**If no search term**, call:
```
stata_read_log(path=<first_token>, tail_lines=50)
```
Display the last 50 lines of the log.

**If the argument looks like a task_id** (not a file path), call:
```
stata_read_log(task_id=<argument>, tail_lines=50)
```

If no argument is provided, tell the user to supply a log file path or task_id. These are returned by `stata_run` in the `log_path` field of the JSON response.

If the log is large and truncated, note the `offset` for reading more (the response includes the current byte offset).
