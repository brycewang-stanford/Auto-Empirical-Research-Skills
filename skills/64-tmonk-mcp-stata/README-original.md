# Stata MCP Server (mcp-stata)

<a href="https://cursor.com/en-US/install-mcp?name=mcp-stata&config=eyJjb21tYW5kIjogInV2eCAtLXJlZnJlc2ggLS1yZWZyZXNoLXBhY2thZ2UgbWNwLXN0YXRhIC0tZnJvbSBtY3Atc3RhdGFAbGF0ZXN0IG1jcC1zdGF0YSJ9"><img src="https://cursor.com/deeplink/mcp-install-dark.svg" alt="Install MCP Server" height="20"></a>&nbsp;
<a href="https://pypi.org/project/mcp-stata/"><img src="https://img.shields.io/pypi/v/mcp-stata?style=flat&color=black" alt="PyPI - Version" height="20"></a> 

**mcp-stata** is an agentic toolkit for empirical researchers. It gives AI agents native control over a local Stata installation, allowing agents to run do-files, inspect data, check stored results, and export graphs. Contains a skills catalog for workflows researchers use often: auditing data, replication and robustness checks, specification comparisons, publication QA, referee responses, and modernization of legacy code. Featured in <a href="https://www.stata.com/stata-news/news41-2/community-corner-ai-tools/"><img src="https://raw.githubusercontent.com/tmonk/mcp-stata/refs/heads/main/img/stata.svg"  height="10px" alt="Stata" style="vertical-align:middle; margin-top: -5px;"/> News</a>.

> If you'd like a fully integrated VS Code extension to run Stata code without leaving your IDE, and also allow AI agent interaction, check out my other project: [<img src="https://raw.githubusercontent.com/tmonk/stata-workbench/refs/heads/main/img/icon.png" height="12px"> Stata Workbench](https://github.com/tmonk/stata-workbench/).

Built by <a href="https://tdmonk.com">Thomas Monk</a>, London School of Economics.
<!-- mcp-name: io.github.tmonk/mcp-stata -->

This server enables LLMs to:
- **Execute Stata code**: run any Stata command (e.g. `sysuse auto`, `regress price mpg`).
- **Inspect data**: retrieve dataset summaries and variable codebooks.
- **Export graphics**: generate and view Stata graphs (histograms, scatterplots).
- **Streaming graph caching**: automatically cache graphs during command execution for instant exports.
- **Verify results**: programmatically check stored results (`r()`, `e()`) for accurate validation.
- **Drive paper workflows**: run structured research audits, estimation planning, specification comparisons, publication checks, and reproducibility diagnostics.
- **Use modern MCP surfaces**: discover prompts, project/session resources, artifacts, and safety metadata through structured tool envelopes.

## Quickstart

### 1 · Install

macOS/Linux:
```bash
curl -LsSf https://mcp-stata-install.tdmonk.com/install.sh | bash
```

Windows (PowerShell):
```powershell
irm https://mcp-stata-install.tdmonk.com/install.ps1 | iex
```

Client-specific examples:

| Client | macOS/Linux | Windows (PowerShell) |
|--------|-------------|----------------------|
| **Claude Code** | `bash <(curl -LsSf https://mcp-stata-install.tdmonk.com/install.sh) --agent claude` | `& ([scriptblock]::Create((irm https://mcp-stata-install.tdmonk.com/install.ps1 &#124; iex))) --agent claude` |
| **Codex** | `bash <(curl -LsSf https://mcp-stata-install.tdmonk.com/install.sh) --agent codex` | `& ([scriptblock]::Create((irm https://mcp-stata-install.tdmonk.com/install.ps1 &#124; iex))) --agent codex` |
| **Gemini** | `bash <(curl -LsSf https://mcp-stata-install.tdmonk.com/install.sh) --agent gemini` | `& ([scriptblock]::Create((irm https://mcp-stata-install.tdmonk.com/install.ps1 &#124; iex))) --agent gemini` |
| **Cursor** | `bash <(curl -LsSf https://mcp-stata-install.tdmonk.com/install.sh) --agent cursor` | `& ([scriptblock]::Create((irm https://mcp-stata-install.tdmonk.com/install.ps1 &#124; iex))) --agent cursor` |
| **Windsurf** | `bash <(curl -LsSf https://mcp-stata-install.tdmonk.com/install.sh) --agent windsurf` | `& ([scriptblock]::Create((irm https://mcp-stata-install.tdmonk.com/install.ps1 &#124; iex))) --agent windsurf` |
| **VS Code** | `bash <(curl -LsSf https://mcp-stata-install.tdmonk.com/install.sh) --agent vscode` | `& ([scriptblock]::Create((irm https://mcp-stata-install.tdmonk.com/install.ps1 &#124; iex))) --agent vscode` |
| **Auto-detect / default** | `bash <(curl -LsSf https://mcp-stata-install.tdmonk.com/install.sh)` | `& ([scriptblock]::Create((irm https://mcp-stata-install.tdmonk.com/install.ps1 &#124; iex)))` |

### 2 · Verify

Ask your agent:

```
Do you have access to the Stata agentic toolkit? (mcp-stata)
```

It will confirm the connection and describe all available tools and skills.

### 3 · Try it

```
Load the auto dataset and run a regression of price on mpg
```

## Academic Research Workflows

The toolkit is designed for empirical economics research.

- Replication and robustness: rerun pipelines, compare specifications, and preserve an audit trail.
- Data audit: check structure, missingness, duplicate identifiers, suspicious coding, and documentation readiness.
- Publication QA: review tables and figures for paper-ready presentation.
- Referee response: organize reruns and evidence for critiques or coauthor requests.
- Environment diagnosis: troubleshoot Stata discovery, package availability, graph export, and managed-machine quirks.
- Safety and diagnostics: diagnose the MCP server, and enforce the safety of code run through the server.

## Prerequisites

- **Stata 17+** (Stata MP, SE, or BE). Must be licensed and installed locally.
- **Python 3.11+**
- **uv** (recommended)

> **Note on `pystata`**: This server uses the proprietary `pystata` module that is included with your Stata installation. There is a third-party package named `pystata` on PyPI that is **not** the official Stata package and should not be installed. MCP-Stata handles finding and loading the official module from your Stata directory automatically.

## Run as a published tool with `uvx`

```bash
uvx --refresh --refresh-package mcp-stata --from mcp-stata@latest mcp-stata
```

`uvx` is an alias for `uv tool run` and runs the tool in an isolated, cached environment.

## Configuration

This server attempts to automatically discover your Stata installation (supporting standard paths and StataNow).

If auto-discovery fails, set the `STATA_PATH` environment variable to your Stata executable:

```bash
# macOS example
export STATA_PATH="/Applications/StataNow/StataMP.app/Contents/MacOS/stata-mp"

# Windows example (cmd.exe)
set STATA_PATH="C:\Program Files\Stata18\StataMP-64.exe"
```

If you encounter write permission issues with temporary files (common on Windows), you can override the temporary directory location by setting `MCP_STATA_TEMP`:

```bash
# Example
export MCP_STATA_TEMP="/path/to/writable/temp"
```

The server will automatically try the following locations in order of preference:
1. `MCP_STATA_TEMP` environment variable
2. System temporary directory
3. `~/.mcp-stata/temp`
4. Current working directory subdirectory (`.tmp/`)

### Startup Do Files

When a session starts, MCP-Stata loads startup do files in the same order as native Stata:

1. **`MCP_STATA_STARTUP_DO_FILE`** (env var) — one or more custom do files, separated by `:` (Unix) or `;` (Windows).
2. **`sysprofile.do`** — the first one found along the Stata search path.
3. **`profile.do`** — the first one found along the Stata search path.

The search path mirrors native Stata: Stata install directory, current working directory, then the ado-path (PERSONAL, SITE, PLUS, OLDPLACE, ...). Only the first `sysprofile.do` and first `profile.do` found are executed, matching native Stata behavior. All paths are deduplicated so the same file is never run twice.

If a command clears programs (`clear all`, `clear programs`, or `program drop _all`), MCP-Stata automatically re-executes the startup files so that any programs they defined remain available. To disable this and let `clear all` behave exactly as in native Stata (programs are lost), set:

```
MCP_STATA_NO_RELOAD_ON_CLEAR=1
```

If you prefer, add these variables to your MCP config's `env` for any IDE shown below. It's optional and only needed when discovery cannot find Stata.

Optional `env` example (add inside your MCP server entry):

```json
"env": {
  "STATA_PATH": "/Applications/StataNow/StataMP.app/Contents/MacOS/stata-mp",
  "MCP_STATA_STARTUP_DO_FILE": "/path/to/my/startup.do",
  "MCP_STATA_NO_RELOAD_ON_CLEAR": "1"
}
```

## IDE Setup (MCP)

This MCP server uses the **stdio** transport (the IDE launches the process and communicates over stdin/stdout).

---

### Claude Desktop

Open Claude Desktop → **Settings** → **Developer** → **Edit Config**.
Config file locations include:

* macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
* Windows: `%APPDATA%\Claude\claude_desktop_config.json`

#### Published tool (uvx)

```json
{
  "mcpServers": {
    "mcp-stata": {
      "command": "uvx",
        "args": [
        "--refresh",
        "--refresh-package",
        "mcp-stata",
        "--from",
        "mcp-stata@latest",
        "mcp-stata"
      ]
    }
  }
}
```

After editing, fully quit and restart Claude Desktop to reload MCP servers.

---

### Cursor

Cursor supports MCP config at:

* Global: `~/.cursor/mcp.json`
* Project: `.cursor/mcp.json`

#### Published tool (uvx)

```json
{
  "mcpServers": {
    "mcp-stata": {
      "command": "uvx",
       "args": [
        "--refresh",
        "--refresh-package",
        "mcp-stata",
        "--from",
        "mcp-stata@latest",
        "mcp-stata"
      ]
    }
  }
}
```

---

### Windsurf

Windsurf supports MCP plugins and also allows manual editing of `mcp_config.json`. After adding/editing a server, use the UI’s refresh so it re-reads the config.

A common location is `~/.codeium/windsurf/mcp_config.json`.
#### Published tool (uvx)

```json
{
  "mcpServers": {
    "mcp-stata": {
      "command": "uvx",
        "args": [
        "--refresh",
        "--refresh-package",
        "mcp-stata",
        "--from",
        "mcp-stata@latest",
        "mcp-stata"
      ]
    }
  }
}
```

---

### Google Antigravity

In Antigravity, MCP servers are managed from the MCP store/menu; you can open **Manage MCP Servers** and then **View raw config** to edit `mcp_config.json`.

#### Published tool (uvx)

```json
{
  "mcpServers": {
    "mcp-stata": {
      "command": "uvx",
        "args": [
        "--refresh",
        "--refresh-package",
        "mcp-stata",
        "--from",
        "mcp-stata@latest",
        "mcp-stata"
      ]
    }
  }
}
```

---

### Visual Studio Code

VS Code supports MCP servers via a `.vscode/mcp.json` file. The top-level key is **`servers`** (not `mcpServers`).

Create `.vscode/mcp.json`:

#### Published tool (uvx)

```json
{
  "servers": {
    "mcp-stata": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--refresh",
        "--refresh-package",
        "mcp-stata",
        "--from",
        "mcp-stata@latest",
        "mcp-stata"
      ]
    }
  }
}
```

VS Code documents `.vscode/mcp.json` and the `servers` schema, including `type` and `command`/`args`.

---

## Skills Catalog

The toolkit includes a catalog of "Skills", providing domain knowledge to AI agents.

- **Base Skill**: [plugin/skills/stata-toolkit/SKILL.md](plugin/skills/stata-toolkit/SKILL.md) — Main Stata toolkit dispatcher.
- **Modernize Skill**: [plugin/skills/stata-modernize/SKILL.md](plugin/skills/stata-modernize/SKILL.md) — Replaces legacy Stata patterns (i.e. prefer frames over `preserve`, `restore`.)
- **Replication Skill**: [plugin/skills/stata-replication/SKILL.md](plugin/skills/stata-replication/SKILL.md) — Reproducibility and robustness workflows.
- **Data Audit Skill**: [plugin/skills/stata-data-audit/SKILL.md](plugin/skills/stata-data-audit/SKILL.md) — Dataset QA and sanity checks.
- **Publication QA Skill**: [plugin/skills/stata-publication-qa/SKILL.md](plugin/skills/stata-publication-qa/SKILL.md) — Tables and figures for paper readiness.
- **Environment Diagnose Skill**: [plugin/skills/stata-environment-diagnose/SKILL.md](plugin/skills/stata-environment-diagnose/SKILL.md) — Setup and platform troubleshooting.
- Additional plugin skills cover basic causal inference, table building, power analysis, data provenance, and referee-response work.

## Tools Available (from server.py)

* `stata_run(code, is_file=False, background=False, echo=True, as_json=True, trace=False, raw=False, max_output_lines=None, cwd=None, session_id="default", strip_smcl=True, filter_pattern=None, exclude_pattern=None)`: Execute Stata commands or a `.do` file.
  - Set `is_file=True` to treat `code` as an absolute path to a `.do` file.
  - Set `background=True` to start long jobs asynchronously (returns `task_id`).
  - Always writes output to a temporary log file and emits `notifications/logMessage` containing `{"event":"log_path","path":"..."}`.
  - May emit `notifications/progress` when the client provides a progress token/callback.
* `stata_task_status(task_id, wait=False, timeout=60.0, poll_interval=1.0, tail_lines=0)`: Query or wait on background task status.
* `stata_control(action, id)`: Control active work.
  - `action="break"` with `id=<session_id>` to interrupt a running session.
  - `action="cancel"` with `id=<task_id>` to cancel a background task.
* `stata_read_log(path, offset=0, max_bytes=262144, tail_lines=0, query=None, before=2, after=2, case_sensitive=False, regex=False, max_matches=50)`: Read, tail, or search a log file.
* `stata_load_data(source, clear=True, as_json=True, raw=False, max_output_lines=None, session_id="default")`: Heuristic loader (sysuse/webuse/use/path/URL) for the specified session.
* `stata_inspect_data(action, query=None, variables=None, start=0, count=50, session_id="default")`: Unified data inspector.
  - `action`: `describe`, `codebook`, `summary`, `search`, `list`, `get`, or **`lint`**.
  - `lint`: performs static analysis of `.do` and `.ado` files for modern best practices.
* `stata_manage_graphs(action, graph_name=None, format="svg", session_id="default")`: Graph management (`list`, `export`, `export_all`).
* `stata_get_results(session_id="default", include_formatting=False, include_matrices=True, matrix_max_rows=200, matrix_max_cols=200, include_mata=False, as_json=True)`: Unified stored-results tool for coherent structured `r()`/`e()`/`s()` payloads with optional structured Mata snapshot.
* `stata_get_help(topic, plain_text=False, merge_paragraphs=True, session_id="default")`: Markdown or plain-text Stata help.
* `stata_manage_session(action, session_id="default", code=None, since_command=None)`: Session lifecycle, state history, and UI channel orchestration.
  - `action`: `create`, `stop`, `list`, `set_profile`, `history_diff`, `history_stats`, `get_ui_channel`, or **`detect`**.
  - `detect`: Returns metadata about the Stata installation (version, flavor, OS) and optionally SSC packages.
  - `history_diff` returns tracked changes in variables/macros and dataset dimensions.
  - `history_stats` returns retained window metadata (`history_size`, `earliest_command`, `latest_command`, `max_history_entries`).

### Common action examples

```python
# Session lifecycle
stata_manage_session(action="create", session_id="analysis")
stata_manage_session(action="list")
stata_manage_session(action="stop", session_id="analysis")

# Session history tracking
stata_manage_session(action="history_stats", session_id="analysis")
stata_manage_session(action="history_diff", session_id="analysis")
stata_manage_session(action="history_diff", session_id="analysis", since_command=42)

# Run a do-file (replacement for run_do_file)
stata_run("/path/to/analysis.do", is_file=True, session_id="analysis")

# Data inspection (describe, codebook, variable list)
stata_inspect_data(action="describe", session_id="analysis")
stata_inspect_data(action="codebook", query="price", session_id="analysis")
stata_inspect_data(action="list", session_id="analysis")

# Graph operations
stata_manage_graphs(action="list", session_id="analysis")
stata_manage_graphs(action="export", graph_name="Graph", format="png", session_id="analysis")
stata_manage_graphs(action="export_all", session_id="analysis")

# Help and stored results
stata_get_help(topic="regress", session_id="analysis")
stata_get_results(session_id="analysis", include_mata=True)

# UI data browser channel
stata_manage_session(action="get_ui_channel", session_id="analysis")

# Interrupt / cancel / background status
stata_control(action="break", id="analysis")
stata_run("quietly do /path/to/long_job.do", background=True, session_id="analysis")
stata_task_status(task_id="...", wait=True, timeout=30)
stata_control(action="cancel", id="...")
```

### Cancellation

- Clients may cancel an in-flight request by sending the MCP notification `notifications/cancelled` with `params.requestId` set to the original tool call ID.
- Client guidance:
  1. Pass a `_meta.progressToken` when invoking the tool if you want progress updates (optional).
  2. If you need to cancel, send `notifications/cancelled` with the same requestId. You may also stop tailing the log file path once you receive cancellation confirmation (the tool call will return an error indicating cancellation).
  3. Be prepared for partial output in the log file; cancellation is best-effort and depends on Stata surfacing `BreakError`.

### Output and results behavior

- `stata_run` defaults to `strip_smcl=True`, so responses are plain-text oriented unless you explicitly disable stripping.
- `stata_get_results` returns structured stored results and can include Mata state (`include_mata=True`) with typed object/function payloads suitable for downstream programmatic checks.

Resources exposed for MCP clients:

* `stata://data/summary` → `summarize`
* `stata://data/metadata` → `describe`
* `stata://graphs/list` → graph list (resource handler delegates to `stata_manage_graphs(action="list")`)
* `stata://variables/list` → variable list (resource wrapper)
* `stata://results/stored` → stored `r()`/`e()`/`s()` results

## UI-only Data Browser (Local HTTP API)

This server also hosts a **localhost-only HTTP API** intended for a VS Code extension UI to browse data at high volume (paging, filtering) without sending large payloads over MCP.

Important properties:

- **Loopback only**: binds to `127.0.0.1`.
- **Bearer auth**: every request requires an `Authorization: Bearer <token>` header.
- **Short-lived tokens**: clients should call `stata_manage_session(action="get_ui_channel")` to obtain a fresh token as needed.
- **Session Isolate**: caches (views, sorting) are isolated per `sessionId`.
- **No Stata dataset mutation** for browsing/filtering:
  - No generated variables.
  - Paging uses `sfi.Data.get`.
  - Filtering is evaluated in Python over chunked reads.

### Discovery via MCP (`stata_manage_session`)

Call the MCP tool `stata_manage_session(action="get_ui_channel")` and parse the JSON:

```json
{
  "baseUrl": "http://127.0.0.1:53741",
  "token": "...",
  "expiresAt": 1730000000,
  "capabilities": {
    "dataBrowser": true,
    "filtering": true,
    "sorting": true,
    "arrowStream": true
  }
}
```

Server-enforced limits (current defaults):

- **maxLimit**: 500
- **maxVars**: 32,767
- **maxChars**: 500
- **maxRequestBytes**: 1,000,000
- **maxArrowLimit**: 1,000,000 (specific to `/v1/arrow`)

### Endpoints

All endpoints are under `baseUrl` and require the bearer token.

- `GET /v1/dataset?sessionId=default`
  - Returns dataset identity and basic state (`id`, `frame`, `n`, `k`) for the given session.
- `GET /v1/vars?sessionId=default`
  - Returns full variable list with labels, types, and formats.
- `POST /v1/page`
  - Paged data retrieval. Supports `sortBy`, `filterExpr` (ephemeral), and `sessionId`.
- `POST /v1/arrow`
  - Returns a binary Arrow IPC stream (same input as `/v1/page`).
- `POST /v1/views`
  - Create a long-lived filtered view. Returns a `viewId`. Requires `sessionId`.
- `POST /v1/views/<viewId>/page`
  - Paged retrieval from a previously created view. Supports `sortBy` and `sessionId`.
- `POST /v1/views/:viewId/arrow`
  - Returns a binary Arrow IPC stream from a filtered view.
- `DELETE /v1/views/:viewId`
  - Deletes a view handle.
- `POST /v1/filters/validate`
  - Validates a filter expression.

### Paging request example

```bash
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"datasetId":"...","frame":"default","offset":0,"limit":50,"vars":["price","mpg"],"includeObsNo":true,"maxChars":200}' \
  "$BASE_URL/v1/page"
```

#### Sorting

The `/v1/page` and `/v1/views/:viewId/page` endpoints support sorting via the optional `sortBy` parameter:

```bash
# Sort by price ascending
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"datasetId":"...","offset":0,"limit":50,"vars":["price","mpg"],"sortBy":["price"]}' \
  "$BASE_URL/v1/page"

# Sort by price descending
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"datasetId":"...","offset":0,"limit":50,"vars":["price","mpg"],"sortBy":["-price"]}' \
  "$BASE_URL/v1/page"

# Multi-variable sort: foreign ascending, then price descending
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"datasetId":"...","offset":0,"limit":50,"vars":["foreign","price","mpg"],"sortBy":["foreign","-price"]}' \
  "$BASE_URL/v1/page"
```

**Sort specification format:**
- `sortBy` is an array of strings (variable names with optional prefix)
- No prefix or `+` prefix = ascending order (e.g., `"price"` or `"+price"`)
- `-` prefix = descending order (e.g., `"-price"`)
- Multiple variables are supported for multi-level sorting
- Uses the native Rust sorter when available, with a Polars fallback

**Sorting with filtered views:**
- Sorting is fully supported with filtered views
- The sort is computed in-memory over the sort columns, then filtered indices are re-applied
- Example: Filter for `price < 5000`, then sort descending by price

```bash
# Create a filtered view
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"datasetId":"...","frame":"default","filterExpr":"price < 5000"}' \
  "$BASE_URL/v1/views"
# Returns: {"view": {"id": "view_abc123", "filteredN": 37}}

# Get sorted page from filtered view
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"offset":0,"limit":50,"vars":["price","mpg"],"sortBy":["-price"]}' \
  "$BASE_URL/v1/views/view_abc123/page"
```

Notes:

- `datasetId` is used for cache invalidation. If the dataset changes due to running Stata commands, the server will report a new dataset id and view handles become invalid.
- Filter expressions are evaluated in Python using values read from Stata via `sfi.Data.get`. Use boolean operators like `==`, `!=`, `<`, `>`, and `and`/`or` (Stata-style `&`/`|` are also accepted).
- Sorting does **not** mutate the dataset order in Stata; it computes sorted indices for the response and caches them for subsequent requests.
- The Rust sorter is the primary implementation; Polars is used only as a fallback when the native extension is unavailable.

## License

This project is licensed under the GNU Affero General Public License v3.0 or later.
See the LICENSE file for the full text.

## Error reporting

- All tools that execute Stata commands support JSON envelopes (`as_json=true`) carrying:
  - `rc` (from r()/c(rc)), `stdout`, `stderr`, `message`, optional `line` (when Stata reports it), `command`, optional `log_path` (for log-file streaming), and a `snippet` excerpt of error output.
- Stata-specific cues are preserved:
  - `r(XXX)` codes are parsed when present in output.
  - “Red text” is captured via stderr where available.
  - `trace=true` adds `set trace on` around the command/do-file to surface program-defined errors; the trace is turned off afterward.

## Logging

Set `MCP_STATA_LOGLEVEL` (e.g., `DEBUG`, `INFO`) to control server logging. Logs include discovery details (edition/path) and command-init traces for easier troubleshooting.

## Development & Contributing

For detailed information on building, testing, and contributing to this project, see [CONTRIBUTING.md](CONTRIBUTING.md).

Quick setup:

```bash
# Install dependencies
uv sync --extra dev --no-install-project

# Run tests (requires Stata)
pytest

# Run tests without Stata
pytest -v -m "not requires_stata"

# Build the package
python -m build
```

[![Tests](https://github.com/tmonk/mcp-stata/actions/workflows/build-test.yml/badge.svg)](https://github.com/tmonk/mcp-stata/actions/workflows/build-test.yml)
