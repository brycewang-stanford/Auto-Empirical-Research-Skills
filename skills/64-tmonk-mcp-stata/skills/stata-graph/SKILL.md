---
name: stata-graph
description: List, export, and review Stata graphs from the current session.
---

1. Call `stata_manage_graphs(action="list")` to see all graphs in memory, with the active graph marked.

2. If an argument (graph name) was provided:
   - Call `stata_manage_graphs(action="export", graph_name=<argument>, format="png")` and display the exported file path.

3. If no argument was provided and graphs exist:
   - Call `stata_manage_graphs(action="export_all", format="png")` to export all graphs.
   - Display all exported file paths for the user to inspect.

4. If no graphs are in memory, tell the user to create a graph first (e.g., `/stata-run histogram price` or `/stata-run scatter price mpg`).

After export, review the graph(s): check titles, axis labels, legends, and whether the plot matches expectations. Report any issues.
