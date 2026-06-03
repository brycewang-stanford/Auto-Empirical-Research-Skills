---
name: econ-audit
description: Audit economic analysis outputs (fiscal briefings, macro briefings, market research, longlists, and other quantitative economic documents) against methodology standards, academic literature, and common errors. Runs structured checks across core categories including counterfactual, additionality, discounting, double counting, distributional analysis, Aqua Book RIGOUR, and Flyvbjerg-style strategic misrepresentation detection. Returns a RAG scorecard with issues ranked by severity.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
---

**Only stop to ask the user when:** the document type is unrecognised, or fix confirmation is needed under `--fix` mode.
**Never stop to ask about:** which checks to run (all applicable ones), grading methodology, or output filename.

<!-- preamble: update check -->
Before starting, run this silently. If it outputs UPDATE_AVAILABLE, tell the user:
"A new version of econstack is available. Run `cd ~/.claude/skills/econstack && git pull` to update."
Then continue with the skill normally.

```bash
~/.claude/skills/econstack/bin/econstack-update-check 2>/dev/null || true
```

<!-- preamble: project learnings -->
After the update check, run this silently to load prior learnings for this project:

```bash
eval "$(~/.claude/skills/econstack/bin/econstack-slug)"
~/.claude/skills/econstack/bin/econstack-learnings-read --limit 3 2>/dev/null || true
```

If learnings are found, apply them. When a prior learning influences a decision, note: "Prior learning applied: [key]".

**Capturing new learnings:** After completing this skill, log new insights via:

```bash
~/.claude/skills/econstack/bin/econstack-learnings-log '{"skill":"...","type":"...","key":"...","insight":"...","confidence":N,"source":"observed|user-stated|inferred"}'
```

Types: `framework` (preferred appraisal framework), `parameter` (custom overrides), `data-source` (preferred data), `output` (past report references), `operational` (tool/env quirks), `preference` (formatting/style). Confidence: 9-10 observed/stated, 6-8 strong inference, 4-5 weak. User-stated never decays; observed/inferred lose 1 point per 30 days. All data stored locally. Nothing transmitted.

<!-- preamble: parameter database check -->
After the update check, verify the parameter database is available and check staleness:

```bash
PARAMS_DIR="$HOME/econstack-data/parameters"
if [ -d "$PARAMS_DIR" ]; then
  PARAM_COUNT=$(find "$PARAMS_DIR" -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
  echo "PARAMS: $PARAM_COUNT files loaded from $PARAMS_DIR"

  # Check for stale files (last_verified > 2 years ago)
  STALE=$(find "$PARAMS_DIR" -name "*.json" -mtime +730 2>/dev/null | wc -l | tr -d ' ')
  if [ "$STALE" -gt 0 ]; then
    echo "PARAMS_WARNING: $STALE file(s) not updated in 2+ years. Run: cd ~/econstack-data && git pull"
  fi
else
  echo "PARAMS: not found. Using built-in defaults. For full parameter support: git clone https://github.com/charlescoverdale/econstack-data.git ~/econstack-data"
fi
```

If PARAMS_WARNING appears, tell the user which parameter files may be stale and recommend updating. Continue with the skill normally using whatever parameters are available.

<!-- preamble: safety hooks -->

**Safety rules for this skill:**

1. **Parameter database is read-only.** Never write to, modify, or delete files in `~/econstack-data/parameters/`. These are shared, versioned parameters maintained separately. If a parameter needs updating, tell the user to update the econstack-data repo.

2. **Confirm before overwriting.** Before writing an output file, check if a file with the same name already exists. If it does, ask the user: "A file named [filename] already exists. Overwrite it, or save with a new name?" Do not silently overwrite.

<!-- preamble: completion status -->
**At the end of every skill run, report one of these statuses:**

- **DONE**: Analysis complete, output generated, all sections finished.
- **DONE_WITH_CONCERNS**: Output generated but with caveats (e.g., data gaps, assumptions that need review, sections below expected depth).
- **BLOCKED**: Cannot proceed (e.g., missing critical input, parameter database unavailable, framework not supported).
- **NEEDS_CONTEXT**: Need more information from the user before continuing.

Format: `STATUS: [status] | [one-line reason]`

# /econ-audit: Economic Analysis Audit

Reviews any economic analysis output against methodology standards and practitioner best practice. Works on fiscal briefings, macro briefings, market research reports, longlists, or any document making economic claims with numbers.

Think of it as a senior partner and an economics professor going through your work and poking holes in it. Returns a RAG (red / amber / green) scorecard with issues ranked by severity, plus an optional `--fix` mode that proposes concrete corrections.

## Arguments

```
/econ-audit [file or directory] [options]
```

**Examples:**
```
/econ-audit longlist-schools-2026-04-10.md
/econ-audit fiscal-uk-2026-04-10.md --strict
/econ-audit . --fix
/econ-audit macro-uk-2026-04-10.md --framework uk-gb
```

**Options:**
- `--strict` : Apply higher bars. Green requires all checks pass cleanly; amber becomes red if material.
- `--fix` : After scoring, propose concrete corrections for each issue. Optionally apply them (prompted per-issue).
- `--framework <name>` : Override the auto-detected framework (`uk-gb`, `eu-brg`, `wb`, `adb`, `au-vic`).
- `--section <name>` : Emit only one sub-component. Options: `full` (default), `headline` (letter grade and count only), `issues` (issue list only), `methodology`, `fix-plan` (if --fix was used). Combinable.
- `--format <type>` : Output format(s). `markdown` (default, always generated), `xlsx`, `word`, or `pdf`.
- `--client "Name"` : Add "Prepared for" metadata.

## Check categories

The audit runs structured checks across these categories. Checks are framework-aware: some checks apply only to specific frameworks.

| Category | Checks | Applies to |
|---------|--------|-----------|
| **Counterfactual** | Is Do Nothing specified? Is it dynamic (not static)? Are all benefits incremental to it? | All |
| **Additionality** | Deadweight, displacement, leakage applied? Rates defensible? Not applied to carbon? | All |
| **Discounting** | Framework-appropriate rate? Declining vs flat correct? Health at 1.5% if applicable? | All |
| **Optimism bias** | Applied at the right rate for project type and stage? | `uk-gb` only |
| **Double counting** | Construction jobs + capex? Journey time + land value? Gross earnings + tax? | All |
| **Transfers** | Tax receipts, welfare payments correctly excluded from social CBA? | All |
| **Sunk costs** | Prior spend excluded? | All |
| **Cash vs non-cash** | Economic NPV includes all; Financial NPV includes only cash in / cash out? | All |
| **Five Case consistency** | Financial vs Economic capex, benefits register vs realisation, risk register vs contingency, preferred option consistent | `uk-gb`, `au-vic` business cases |
| **Distributional** | Is distributional incidence reported? Is it explicit for uk-gb if material, and mandatory for wb, adb, au-vic? | Framework-dependent |
| **Aqua Book RIGOUR** | Repeatable, Independent, Grounded, Objective, Uncertainty-managed, Robust | `uk-gb` |
| **Flyvbjerg indicators** | Scope near thresholds, low contingency, optimistic demand, benefit / cost asymmetry | All |
| **Data vintages** | All cited numbers have a vintage within a reasonable window | All |
| **Source quality** | Sources cited, from official or peer-reviewed origins | All |

## Instructions

### Step 1: Identify the document

If the user passes a single file path, load that file. If they pass a directory, glob for markdown files and audit each one in turn.

Auto-detect the document type from the file name or the KEY NUMBERS block at the top:
- `longlist-*.md`, `type: longlist` → Longlist
- `macro-*.md`, `type: macro-briefing` → Macro briefing
- `fiscal-*.md`, `type: fiscal-briefing` → Fiscal briefing
- `market-*.md`, `type: market-research` → Market research
- `briefing-*.md`, `type: briefing-note` → Briefing note
- Unknown → ask the user what it is once.

Auto-detect the framework from the document header or KEY NUMBERS. Default to `uk-gb` if missing.

### Step 2: Run all applicable checks (silent)

For each check in the category table above, evaluate:
- **Pass (green)**: the check is met or clearly met.
- **Warn (amber)**: the check is partially met or cannot be determined from the document.
- **Fail (red)**: the check is clearly violated or entirely absent when it should be present.

Checks are framework-aware. Do not apply optimism bias checks to a non-uk-gb document. Do not apply Aqua Book RIGOUR to a non-uk-gb document. Do apply Five Case consistency to uk-gb and au-vic business cases, and skip for other document types.

### Step 3: Score and rank

Compute:
- Count of passes, warnings, fails
- Overall letter grade: A (no fails, few warnings), B (few fails, some warnings), C (several fails, many warnings), D (serious methodology gaps), F (unusable)
- Under `--strict`: amber escalates to red for material issues.

Rank issues by severity:
- **Critical**: methodology gap that invalidates the conclusion (missing counterfactual, wrong discount rate, material double counting, transfers included in social NPV).
- **High**: material gap that weakens the conclusion but does not invalidate it.
- **Medium**: presentation or evidence gap that should be addressed before submission.
- **Low**: stylistic or completeness nit.

### Step 4: Fix plan (if `--fix`)

For each critical and high issue, propose a concrete fix. Example fixes:
- "Add a dynamic counterfactual describing deterioration of existing assets over the appraisal period."
- "Apply 24% optimism bias uplift to capital costs per HMT Table 1 for this project type and stage."
- "Remove council tax receipts from the benefits table; note in a separate fiscal annex."
- "Compute additionality using 20% deadweight, 25% displacement, 10% leakage; current analysis uses unadjusted gross benefits."

Under `--fix`, for each proposed fix, ask the user to confirm application. If confirmed, edit the source document in place. If not, record in the fix plan and move on.

### Step 5: Write the output

Save `audit-[target-slug]-[YYYY-MM-DD].md` with this structure.

```markdown
<!-- KEY NUMBERS
type: econ-audit
target: [target file or directory]
framework: [framework]
strict: [true|false]
passes: [count]
warnings: [count]
fails: [count]
grade: [A|B|C|D|F]
critical_issues: [count]
high_issues: [count]
fixes_applied: [count]
date: [YYYY-MM-DD]
-->

# Audit: [target file name]

**Date**: [YYYY-MM-DD] · **Framework**: [framework] · **Strict mode**: [on/off]

## Headline

**Grade**: **[A / B / C / D / F]**
**Checks**: [passes] pass, [warnings] warn, [fails] fail
**Critical issues**: [count]

[One-sentence summary: e.g. "Grade B. The CBA is sound in structure but applies additionality inconsistently and is missing a distributional analysis."]

## Scorecard

| Category | Result | Notes |
|----------|:------:|-------|
| Counterfactual | [G/A/R] | [one line] |
| Additionality | [G/A/R] | [one line] |
| Discounting | [G/A/R] | [one line] |
| Optimism bias (if uk-gb) | [G/A/R] | [one line] |
| Double counting | [G/A/R] | [one line] |
| Transfers | [G/A/R] | [one line] |
| Sunk costs | [G/A/R] | [one line] |
| Cash vs non-cash | [G/A/R] | [one line] |
| Five Case consistency (if applicable) | [G/A/R] | [one line] |
| Distributional | [G/A/R] | [one line] |
| Aqua Book RIGOUR (if uk-gb) | [G/A/R] | [one line] |
| Flyvbjerg indicators | [G/A/R] | [one line] |
| Data vintages | [G/A/R] | [one line] |
| Source quality | [G/A/R] | [one line] |

## Issues (ranked by severity)

### Critical

- **[Issue 1]**: [description] · Location: [section / line] · Fix: [suggested fix]
- **[Issue 2]**: [description] · Location: [section / line] · Fix: [suggested fix]

### High

- **[Issue 3]**: [description] · Fix: [suggested fix]

### Medium

- **[Issue 4]**: [description]

### Low

- [Issue 5]

## Methodology notes

[One paragraph: which framework was applied, which checks were skipped and why, any caveats on the audit itself.]

[If --fix]
## Fix plan

[List of proposed fixes with confirmation status: Applied / Rejected / Pending.]
```

**Sub-component selection** (via `--section`): emit only the requested parts.

- `full` (default): the whole structure above.
- `headline`: grade and count only.
- `issues`: issue list only.
- `methodology`: methodology notes only.
- `fix-plan`: fix plan only (requires `--fix`).
- Combinable: `--section headline,issues`.

**Format-specific output structure** (only produce formats explicitly requested; see dispatcher below):
- **Markdown (.md)**: `audit-[target-slug]-[date].md` with the structure shown above.
- **Excel (.xlsx)**: one workbook with sheets: `Scorecard`, `Issues`, `Fix plan`. Conditional formatting on the Result column.
- **Word (.docx)**: one document, full audit.
- **PDF**: render markdown through econstack Quarto template.

## Output formats

The user requests format(s) via `--format`. Default: `md`. Comma-separated lists are allowed (e.g. `--format md,pdf`); `all` expands to every supported format.

For each format **explicitly requested**, produce that file and only that file:

- `md`: write the markdown inline (only when `md` is in the requested set).
- `docx`: invoke the `docx` skill with the rendered content.
- `pdf`: render via the econstack Quarto template (or invoke the `pdf` skill if no template exists for this skill).
- `xlsx`: invoke the `xlsx` skill with the structured tables.
- `pptx`: invoke the `pptx` skill with the briefing as a deck.

**Do NOT produce formats that were not requested.** This is the v0.4 fix for the multi-format leak that previously caused `--format pdf` to also write `.md` and `.docx` files alongside the PDF. Any intermediate files needed during rendering must go to a temp directory and be cleaned up before the skill returns.

When you finish, the file listing in your "Saved:" message must contain exactly the files the user asked for, no extras.


Tell the user (listing only files produced):
```
Audit complete. Grade [X]. [N] critical, [M] high, [K] medium issues.

Saved:
  audit-[target-slug]-[date].md
  [other formats if requested]
```

## Citation discipline

Every numerical claim in the output must be followed by an inline citation in the form `[SOURCE_CODE, vintage]`. `SOURCE_CODE` is a short tag (e.g. `ONS_PSF`, `OBR_EFO`, `BoE_MPR`, `Fed_FOMC`, `ECB_EB`, `RBA_SoMP`, `IMF_WEO`, `OECD_EO`, `Eurostat`, `BLS`, `BEA`, `FRED`, `ABS`, `Comtrade`) matching an entry in the References footer. `vintage` is the publication date of the source data (e.g. `Mar 2026`, `Q4 2025`, `Jan 2026`).

**Examples:**

> CPI was 3.4% YoY in March 2026 [ONS_CPI, Mar 2026].

> The OBR forecasts borrowing falling to 1.6% of GDP by 2028-29 [OBR_EFO, Mar 2026].

> Industry concentration is moderate: HHI is 1,820 across the top 8 firms [Companies_House, Q4 2025].

**Numbers that cannot be sourced to a primary publication must NOT appear in the output.** No exceptions: do not estimate, infer from training data, interpolate, or recall from memory. If a needed number isn't in fetched data, state it explicitly:

> [Source] has not yet published this measure for [period].

**Self-check before output**: scan the draft for every number. If any number lacks an inline citation, either add the citation or remove the number. Citation density should be roughly even across sections; a section with no citations is a red flag that the section was generated rather than sourced.


## Factuality

Audit findings carry weight only if they cite the framework rule being audited against. Every issue in the Issues table needs a citation to the canonical source: Green Book paragraph or annex, Magenta Book chapter, Aqua Book principle, EU Better Regulation toolbox tool number, World Bank OP, ADB project guidelines, AU Treasury CBA guide, Victorian HVHR Investment Lifecycle Guide. Do not paraphrase or invent rules.

Common gotchas: STPR is 3.5% (Green Book Annex 6) with a declining schedule, NOT a flat 3.5% across all horizons; optimism bias rates depend on project type AND stage (Outline vs Final Business Case); ADB EIRR hurdle is 9% (general) or 6% (climate, health, education); HMT shadow carbon comes from DESNZ, not Treasury directly.

## Out of scope (unless explicitly requested)

An audit is a methodology check, not a redo of the analysis:

- Do NOT re-compute NPV / BCR / EIRR yourself unless the user asks.
- Do NOT propose alternative parameter values; flag the issue and reference the canonical source.
- Do NOT make a positive recommendation about whether the option should proceed.
- Do NOT extend beyond the framework the audit is targeting (the `--framework` flag bounds the audit scope).
- Where issues cross framework boundaries, surface them as a "framework choice" finding rather than auditing against a framework the user did not select.

## Framework-specific checks

### `uk-gb`
- Optimism bias at Table 1 rates per project type and stage.
- Distributional weights applied if benefits materially affect low-income groups (Annex 4).
- Aqua Book RIGOUR: Repeatable, Independent, Grounded, Objective, Uncertainty-managed, Robust.
- Green Book 2026 updates: BCR misuse, health discount rate (1.5%), carbon pre-discounting, wellbeing valuation.

### `eu-brg`
- SME test applied if business-affecting.
- Fundamental rights screening performed.
- Proportionality and subsidiarity addressed.
- REFIT alignment stated for amendments to existing legislation.

### `wb`
- Distributional incidence by income decile.
- Poverty headcount impact reported.
- Shadow wages applied consistently for labour benefits.
- OP 10.04 structure followed.

### `adb`
- 9% EIRR hurdle (or 6% for climate / health / education).
- Switching values mandatory on all major variables.
- Poverty and gender disaggregation reported.
- Climate Typology tagging if climate co-benefits claimed.

### `au-vic`
- Investment Logic Map present, with problem-benefit traceability.
- Benefit Management Plan has owner, KPI, baseline, target, timeframe for every benefit.
- Disbenefits captured explicitly.
- P50 / P90 risk allowance applied.

## Important rules

- **Framework-aware.** Do not apply uk-gb checks to an eu-brg or wb document. Only run checks applicable to the detected framework.
- **Honest about limits.** Some checks cannot be fully verified from a written document alone (e.g. whether the counterfactual is truly dynamic). Use warn (amber) in those cases, not pass.
- **Severity drives grading.** A single critical issue caps the grade at C regardless of how clean the other checks are.
- **Fix plans are concrete.** Do not propose vague "improve the counterfactual" fixes. Specify what to add and where.
- **Do not rewrite the document unilaterally.** Under `--fix`, always confirm each edit with the user before applying.
- **Em dashes**: never use em dashes. Use commas, colons, parentheses, or "and".

## Integration with other skills

- Audits outputs from `/longlist`, `/macro-briefing`, `/fiscal-briefing`, `/market-research`, and `/briefing-note`.
- Can be run automatically via the `--audit` flag on most econstack skills (they invoke `/econ-audit` on their own output after generation).
