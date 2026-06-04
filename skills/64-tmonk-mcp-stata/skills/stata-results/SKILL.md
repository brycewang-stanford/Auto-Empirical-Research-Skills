---
name: stata-results
description: Fetch and display stored r(), e(), and s() results from the last Stata command.
---

Call `stata_get_results(include_matrices=True, as_json=True)`.

Present the results in a structured format:
- **r() scalars**: name → value pairs (e.g., r(N), r(mean), r(sd))
- **e() scalars**: model-level results (e.g., e(N), e(r2), e(F))
- **e() matrices**: if present, display b (coefficients) and V (variance-covariance) as formatted tables
- **s() macros**: string results if any

If no results are stored (empty response), tell the user to run a Stata command first (e.g., `regress`, `summarize`, `ttest`).

If the user needs Mata state, note they can ask you to call `stata_get_results(include_mata=True)`.
