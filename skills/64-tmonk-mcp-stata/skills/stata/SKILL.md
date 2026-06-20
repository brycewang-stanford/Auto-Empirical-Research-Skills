---
name: stata
description: Show mcp-stata identity, connected tools, and status. Use when the user asks if mcp-stata is available, asks about access to the toolkit, or asks what Stata tools are connected.
---

ToolSearch query="select:stata_manage_session"

Call `stata_manage_session(action="detect")` to verify the Stata connection. If `stata_manage_session(action="detect")` fails, report the error and suggest the user set `STATA_PATH` to the Stata executable path.

Then respond with:
```
                                    __        __       
   ____ ___  _________        _____/ /_____ _/ /_____ _
  / __ `__ \/ ___/ __ \______/ ___/ __/ __ `/ __/ __ `/
 / / / / / / /__/ /_/ /_____(__  ) /_/ /_/ / /_/ /_/ / 
/_/ /_/ /_/\___/ .___/     /____/\__/\__,_/\__/\__,_/  
              /_/                                        mcp-stata

mcp-stata is connected. Stata {version} ({flavor}) detected.

MCP Tools:
  stata_run              — execute do-file code & ad-hoc commands
  stata_load_data        — load datasets (sysuse / webuse / path)
  stata_inspect_data     — describe, codebook, summary, list, get rows
  stata_manage_graphs    — list, export, or export_all graphs
  stata_get_help         — Stata command documentation
  stata_get_results      — fetch r() / e() / s() stored results
  stata_read_log         — tail or search log output
  stata_manage_session   — create/stop sessions, history diff, UI channel
  stata_task_status      — poll background task progress
  stata_control          — break or cancel running work

Slash Commands:
  /stata-run <code>      — run arbitrary Stata code
  /stata-inspect [var]   — describe/summarize current dataset
  /stata-results         — fetch stored r()/e()/s() results
  /stata-graph [name]    — export graph(s)
  /stata-lint <path>     — lint a .do or .ado file
  /stata-log [path]      — tail log output
  /stata-help <topic>    — look up Stata documentation

Resources (MCP):
  stata://data/summary        stata://data/metadata
  stata://graphs/list         stata://variables/list
  stata://results/stored
```