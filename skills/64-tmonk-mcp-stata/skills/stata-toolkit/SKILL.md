---
name: stata-toolkit
description: Activate when users mention Stata commands, .do files, regressions, econometrics, stored results, graphs, dataset inspection, replication, or Stata errors. Route the task through mcp-stata tools and the specialized research skills instead of treating it as plain text coding.
---

# Stata Toolkit Dispatcher

Use this skill as the default router for Stata work.

1. Confirm the `mcp-stata` MCP server is available.
2. Route quick tasks to the direct slash-style skills:
   - `stata-run`
   - `stata-inspect`
   - `stata-results`
   - `stata-graph`
   - `stata-help`
   - `stata-log`
   - `stata-lint`
3. Route research workflows to the specialized skills:
   - `stata-data-audit`
   - `stata-environment-diagnose`
   - `stata-modernize`
   - `stata-publication-qa`
   - `stata-replication`
   - `stata-causal-inference`
   - `stata-table-builder`
   - `stata-power-analysis`
   - `stata-data-provenance`
   - `stata-referee-response`
4. Use the MCP tools directly when the user needs ad hoc Stata execution or a mixed workflow.

Read these references when needed:
- `references/tool-reference.md` for the tool map and identity response.
- `references/research-workflows.md` for end-to-end economics workflows.
- `references/error-handling.md` for log, `rc`, and background-task handling.
