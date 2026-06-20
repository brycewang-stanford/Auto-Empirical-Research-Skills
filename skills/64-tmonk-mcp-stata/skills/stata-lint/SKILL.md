---
name: stata-lint
description: Run static analysis on a Stata .do or .ado file and report style and best-practice issues.
---

The argument is the absolute path to a `.do` or `.ado` file.

1. Call `stata_inspect_data(action="lint", path=<argument>)`.

2. Display the lint results, grouping issues by severity or type:
   - Line number and issue description for each finding
   - Common issues: use of `cd`, `preserve`/`restore`, `#delimit`, hardcoded paths, long lines, missing `version` statement

3. For each category of issue found, briefly explain the modern alternative (refer to the **stata-modernize** skill for details).

4. If the file is clean, confirm: "No issues found in `<filename>`."

5. If the path argument is missing, tell the user to provide an absolute path to a `.do` or `.ado` file.
