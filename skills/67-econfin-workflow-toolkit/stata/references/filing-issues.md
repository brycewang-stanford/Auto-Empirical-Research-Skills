# Filing an Issue on the Stata Skill Repository

When you identify a documentation gap that caused you to produce incorrect Stata code, help the user file an issue at **github.com/dylantmoore/stata-skill/issues**.

## What Makes a Good Issue

The goal is to give maintainers enough detail to reproduce the problem and improve the reference files. Do NOT include the user's actual data, code, or any identifying details.

### Title

Short, specific: what went wrong and where.

```
Bad:  "Stata skill has a bug"
Good: "Time series reference missing predict, y vs predict, xb distinction after ARIMA with differencing"
Good: "Bootstrap reference: simulate comma placement not documented, causes fatal syntax error"
```

### Body Template

```markdown
## What happened

[1-2 sentences: what Stata code error was produced]

Example: "Claude generated `predict yhat, xb` after `arima y, arima(1,1,1)`, which returns
predictions of the differenced series instead of levels. The correct option is `predict yhat, y`."

## Which reference file is involved

[The file that was loaded, or should have been loaded]

Example: `references/time-series.md`

## What's missing or wrong in the reference

[Specific gap: what content would have prevented the error]

Example: "The Forecasting section shows `predict gdp_forecast` without specifying the `y` option.
After ARIMA with d>0, omitting `y` defaults to `xb`, which returns the differenced series.
The reference should explicitly show `predict gdp_forecast, y` and warn about this distinction."

## Proposed fix

[If you have a concrete suggestion, include it. A WRONG/RIGHT code example is ideal.]

```stata
* WRONG — returns differenced series when d > 0
predict yhat, xb

* RIGHT — back-transforms to levels
predict yhat, y
```

## Context

- **Model used:** [Sonnet / Opus — helps maintainers assess if this is a doc gap vs. model limitation]
- **Task type:** [e.g., "ARIMA forecasting with confidence intervals"]
```

## Rules

- **Never include the user's actual data, variable names, file paths, or project details.** Describe the issue in the abstract using generic examples (e.g., `sysuse auto` or made-up variable names).
- **Never include the user's identity or organization.**
- **Focus on the skill documentation gap**, not on Claude's general capabilities. The issue should be actionable: "add X to file Y" or "fix example Z in file W."
- **One issue per bug.** Don't bundle multiple unrelated problems.
- **Skip trivial issues.** A typo or cosmetic problem isn't worth an issue. Focus on errors that would cause wrong results or code that doesn't run.
- **If the user is on Haiku**, the error may be a model capability issue rather than a documentation gap. Suggest trying Sonnet or Opus before filing.

## How to File

Use the GitHub CLI if available:

```bash
gh issue create --repo dylantmoore/stata-skill \
  --title "Brief description of the documentation gap" \
  --body "$(cat <<'EOF'
## What happened
...

## Which reference file is involved
...

## What's missing or wrong in the reference
...

## Proposed fix
...

## Context
- Model used: ...
- Task type: ...
EOF
)"
```

Or direct the user to open an issue manually at `github.com/dylantmoore/stata-skill/issues/new`.

## Filing a PR Instead

If the user prefers to fix the documentation directly, they can submit a pull request. Fork the repo, edit the relevant reference file, and open a PR with the same level of detail as an issue.

### PR Description Template

```markdown
## What this fixes

[Same "What happened" description as the issue template — what error was produced and why]

## Changes made

- **File:** `references/[file].md`
- **What was added/changed:** [Specific content added — gotcha warning, corrected example, etc.]

## How this was discovered

- **Model used:** [Sonnet / Opus]
- **Task type:** [e.g., "ARIMA forecasting with confidence intervals"]
- **Error pattern:** [Brief description of the mistake the model made]

## Example of the fix

```stata
* WRONG (what the model produced before)
...

* RIGHT (what the reference now teaches)
...
```
```

### How to Submit

```bash
# Fork and clone
gh repo fork dylantmoore/stata-skill --clone
cd stata-skill

# Create a branch, make edits, commit
git checkout -b fix/describe-the-gap
# ... edit the reference file ...
git add plugins/stata/skills/stata/references/[file].md
git commit -m "Fix [brief description of documentation gap]"

# Push and open PR
git push -u origin fix/describe-the-gap
gh pr create --repo dylantmoore/stata-skill \
  --title "Fix: [brief description]" \
  --body "$(cat <<'EOF'
## What this fixes
...

## Changes made
...

## How this was discovered
...
EOF
)"
```

The same privacy rules apply: never include user data, variable names, file paths, or project details in the PR description or commit messages. Use generic examples.
