---
name: macro-briefing
description: Macroeconomic monitor. Supports UK, US, Euro area, and Australia. Pulls GDP, inflation, employment, wages, rates, trade, housing, and fiscal data. Each country follows its central bank's reporting structure. Produces a single clean briefing with a traffic-light assessment and user-selectable sub-components.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Skill
---

**Only stop to ask the user when:** the country is ambiguous or specific indicators are requested that need clarification.
**Never stop to ask about:** section ordering, table formatting, data source preferences (use the country's official sources), or output filename.

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

# /macro-briefing: Macroeconomic Monitor

Produces an up-to-date macroeconomic briefing for the UK, US, Euro area, or Australia. Pulls live data from official sources, structures it into a professional briefing following each central bank's reporting conventions, and emits a single one-page deliverable with a traffic-light macro assessment.

Good before a ministerial meeting, investment committee, exam, or as a regular pre-brief for macro-relevant work. Every number is traceable: methodology, data sources, and vintage dates included in the output.

## Arguments

```
/macro-briefing [country or topic] [options]
```

**Example:**
```
/macro-briefing --country uk --format pdf
```

**Options:**
- `--country <code>` : `uk` (default), `us`, `eu`, or `au`. Auto-detected from context if not set.
- `--focus <topic>` : Narrow to a theme. Options: `inflation`, `labour`, `growth`, `rates`, `housing`, `fiscal`, `trade`. Reduces the briefing to the relevant sections.
- `--international` : Add a cross-country comparison section (G7 and major peers).
- `--section <name>` : Emit only one sub-component. Options: `full` (default), `headline` (traffic-light table only), `activity`, `labour`, `prices`, `rates`, `financial`, `fiscal`, `trade`, `housing`. Combinable with commas.
- `--format <type>` : Output format(s). `markdown` (default, always generated), `xlsx`, `word`, `pptx`, `pdf`, or `all`. Comma-separate for multiple.
- `--client "Name"` : Add "Prepared for" metadata.

## Supported countries

| Code | Country | Reporting structure | Primary data sources | Key policy rate |
|------|---------|--------------------|--------------------|-----------------|
| `uk` | United Kingdom (default) | Bank of England Monetary Policy Report (MPR) | ONS, BoE, OBR, HMRC | Bank Rate |
| `us` | United States | Federal Reserve FOMC / Beige Book | BLS, BEA, FRED, Fed, CBO | Federal Funds Rate |
| `eu` | Euro area | ECB Economic Bulletin | Eurostat, ECB | ECB deposit rate |
| `au` | Australia | RBA Statement on Monetary Policy | ABS, RBA, Treasury | Cash Rate |

**Auto-detection rules:**
- "UK", "Britain", "England", "BoE", "gilt", "PSNB", "Bank Rate" → `uk`
- "US", "USA", "America", "Fed", "FOMC", "Treasury yield" → `us`
- "Euro area", "ECB", "EUR", "bund", "eurozone" → `eu`
- "Australia", "RBA", "AUD", "ASX", "cash rate" → `au`
- Default → `uk`

## Instructions

### Step 1: Detect country and focus

If `--country` is not set, detect from the first user argument. If unclear, default to `uk` and note the assumption.

If `--focus` is set, narrow the briefing to the relevant sections only. If `--section` is set, emit only the requested sub-components.

### Step 2: Fetch data (silent)

For the detected country, fetch the core indicators from the official sources listed below. If a series is unavailable or stale, note it in the output with a vintage date rather than silently skipping.

**UK core indicators** (ONS CDIDs and BoE series):
- GDP level and growth (ABMI, IHYQ, chained volume)
- Inflation: CPI (D7G7), core CPI (L55O), RPI (CHAW), services CPI (D7BT)
- Labour: employment rate (LF24), unemployment rate (MGSX), vacancies (AP2Y)
- Wages: AWE regular pay (KAB9), AWE total pay (KAC3)
- Bank Rate (IUMAIBR) and gilt yields (2yr, 10yr, 30yr)
- Trade: current account balance (AA6H), goods exports (BOKG)
- Housing: ONS House Price Index, Halifax, Nationwide
- Fiscal: PSNB (J5II), PSND (HF6X), OBR forecast

**US core indicators** (BLS, BEA, FRED):
- GDP growth (real, SAAR) and components
- Inflation: CPI-U headline, core CPI, PCE, core PCE
- Labour: payrolls, unemployment rate, labour force participation, ECI
- Federal Funds target rate, 2yr / 10yr Treasury yields
- Housing: Case-Shiller, S&P CoreLogic, mortgage rates
- Consumer: retail sales, personal income, consumer confidence (UMich, Conf Board)
- ISM manufacturing and services PMIs

**Euro area core indicators** (Eurostat, ECB):
- GDP growth (quarterly), country breakdowns for the big four (DE, FR, IT, ES)
- HICP headline, HICPX core, energy and services components
- Unemployment rate (area and by country), labour productivity
- ECB deposit rate, 10yr bund yield, peripheral spreads (IT-DE, ES-DE, PT-DE)
- Composite PMI, European Commission sentiment indicator
- Fiscal: deficit and debt by country

**Australia core indicators** (ABS, RBA):
- GDP growth (quarterly) and components
- Inflation: headline CPI, trimmed mean CPI, weighted median CPI
- Labour: employment, unemployment, participation rate, wages (WPI)
- RBA Cash Rate, 3yr / 10yr AGB yields
- Housing: CoreLogic home value index, building approvals, rental vacancy
- Trade: current account, terms of trade, commodity prices (iron ore, coal, LNG)
- Fiscal: Underlying Cash Balance, net debt (Treasury)

Fetching is silent. Do not narrate which source you pulled each number from in the body text; cite sources in the References footer.

### Step 3: Build the briefing (silent)

Structure by country, using the central bank's native reporting order.

- **UK (BoE MPR)**: activity, labour market, prices, financial conditions, monetary policy, fiscal, trade, housing, productivity.
- **US (FOMC / Beige Book)**: output and activity, labour, prices, monetary policy, financial conditions, housing, consumer.
- **EU (ECB Economic Bulletin)**: external environment, economic activity, labour, prices, monetary and financial conditions, fiscal.
- **AU (RBA SoMP)**: international environment, domestic economy, labour, inflation, financial conditions, housing, fiscal.

Do not invent a new section order. Use the canonical one.

### Step 4: Apply the traffic-light assessment

Score each dimension on a GREEN / AMBER / RED scale with quantitative thresholds:

| Dimension | Green | Amber | Red |
|-----------|-------|-------|-----|
| Growth | Above trend (typically >1.5% YoY for developed) | Near trend (0 to 1.5%) | Below trend or recession (<0%) |
| Inflation | On target (± 0.5pp) | Slightly off (± 0.5 to 1.5pp) | Materially off (>1.5pp) |
| Labour | Unemployment near NAIRU, wages supportive | Some slack or overheating | Material slack or overheating |
| Rates | Policy rate near neutral, yield curve normal | Off-neutral, curve flat | Inverted curve, rate far from neutral |
| Fiscal | Sustainable deficit, debt stable or falling | Rising but manageable | Unsustainable trajectory |

Report the composite assessment at the top: "UK macro assessment: AMBER — growth slowing, inflation above target, labour market tight, fiscal position deteriorating."

### Step 5: Write the output

Save `macro-[country]-[YYYY-MM-DD].md` with this structure.

```markdown
<!-- KEY NUMBERS
type: macro-briefing
country: [uk|us|eu|au]
vintage: [latest data date]
headline_gdp_growth: [value]
headline_inflation: [value]
unemployment: [value]
policy_rate: [value]
assessment: [GREEN|AMBER|RED]
date: [YYYY-MM-DD]
-->

# Macro Briefing: [Country]

**Date**: [YYYY-MM-DD] · **Data vintage**: [latest release across all sections]
**Assessment**: **[GREEN / AMBER / RED]** — [one-line summary of the key dynamics]

## Headline

| Indicator | Latest | Prior | Change | Assessment |
|-----------|-------:|------:|:------:|:----------:|
| GDP growth (YoY) | [val]% | [val]% | [↑/↓/=] | [G/A/R] |
| Inflation (headline) | [val]% | [val]% | [↑/↓/=] | [G/A/R] |
| Unemployment | [val]% | [val]% | [↑/↓/=] | [G/A/R] |
| Policy rate | [val]% | [val]% | [↑/↓/=] | [G/A/R] |
| 10-year yield | [val]% | [val]% | [↑/↓/=] | [G/A/R] |
| Fiscal balance (% GDP) | [val] | [val] | [↑/↓/=] | [G/A/R] |

## Activity and output

[Two or three paragraphs covering GDP growth, PMIs, business surveys, main drivers and drags.]

## Labour market

[Two or three paragraphs covering employment, unemployment, wages, vacancies. Note tightness or slack.]

## Prices and inflation

[Two or three paragraphs covering headline, core, services, goods, energy. Note the gap to target and trajectory.]

## Monetary policy and financial conditions

[Policy rate, forward guidance, yield curve, credit conditions, currency. Reference the central bank's latest statement or minutes.]

## Fiscal position

[Deficit, debt, fiscal rules or limits, outlook. Link to budget or fiscal council forecast.]

## Trade, housing, productivity

[Compact paragraph each. Include only sections that are material this period.]

## Outlook and risks

[Three bullet points: upside risks, downside risks, key data releases to watch in the next 4-6 weeks.]

## Data sources

[One-line references with vintages: e.g. "ONS GDP output (ABMI), latest 2026-Q1 released 2026-04-10; BoE Bank Rate announcement 2026-04-03; HMT PSNB March 2026 release."]
```

That is the full default deliverable.

**International comparison** (if `--international` is set): append a section after Outlook and risks with a table comparing the UK, US, Euro area, Germany, Japan, Australia, and Canada on GDP growth, inflation, unemployment, and policy rate.

**Sub-component selection** (via `--section`): emit only the requested sections. Always include the header block and Headline table.

- `full` (default): all sections.
- `headline`: headline table only.
- `activity`, `labour`, `prices`, `rates`, `financial`, `fiscal`, `trade`, `housing`: that one section only.
- Combinable: `--section headline,prices,labour`.

**Format-specific output structure** (only produce formats explicitly requested; see dispatcher below):
- **Markdown (.md)**: `macro-[country]-[date].md` with the structure shown above.
- **Excel (.xlsx)**: one workbook with sheets per dimension (Activity, Labour, Prices, Rates, Fiscal, Trade, Housing). Each sheet has the latest print plus prior 12 months of history. Conditional formatting on the assessment column.
- **Word (.docx)**: one document with cover page, table of contents, full briefing.
- **PowerPoint (.pptx)**: 6 slides: (1) Assessment, (2) Activity, (3) Labour and inflation, (4) Monetary policy, (5) Fiscal and trade, (6) Outlook and risks. Action titles.
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
Macro briefing complete. [Country] assessment: [GREEN/AMBER/RED].

Saved:
  macro-[country]-[date].md
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

Before asserting any factual claim about how a central bank target works, what an indicator is measuring, or what a recent decision did, ground the claim in the most recent statement from the relevant official source (BoE MPC minutes, FOMC statement, ECB Monetary Policy Statement, RBA SoMP). Do not assert from training-data recall. Common gotchas: BoE inflation target is CPI 2% (not RPI), Fed has a dual mandate (not just inflation), ECB primary objective is price stability defined as 2% over the medium term, RBA target is 2 to 3% on average.

## Out of scope (unless explicitly requested)

The following are NOT produced unless the user explicitly asks for them via flags or natural language:

- **Predictions of central bank decisions.** Do not say "the BoE will cut at the next meeting". Quote the official forward guidance and market-implied path; let the reader form a view.
- **Market price forecasts.** Do not predict where bond yields, FX rates, or equity indices will go.
- **Recommendations.** State what the data shows; do not recommend monetary or fiscal action.
- **Party-political or politician rankings.**

If the user's request requires content from this list, ask first.

## Important rules

- **Data sources are official.** ONS and BoE for UK, BLS / BEA / FRED / Fed for US, Eurostat / ECB for EU, ABS / RBA for AU. Do not substitute third-party aggregators unless official data is unavailable.
- **Every number has a vintage AND an inline citation.** See Citation discipline above. Flag any series more than one release cycle stale.
- **Use the central bank's own reporting order.** UK follows BoE MPR; US follows FOMC / Beige Book; EU follows ECB Economic Bulletin; AU follows RBA SoMP. Do not reorder.
- **One traffic-light assessment at the top**, backed by quantitative thresholds. Do not bury the assessment inside body text.
- **No new forecasts.** Quote OBR, CBO, EC DG ECFIN, or Treasury forecasts directly. Do not generate new forecasts in this skill.
- **Em dashes**: never use em dashes. Use commas, colons, parentheses, or "and".

## Integration with other skills

- `/fiscal-briefing` is the deep-dive companion on public finances. This skill summarises fiscal; `/fiscal-briefing` gives the full picture with optional DSA.
- `/market-research` may reference the macro assessment as background for sector reports.
- `/econ-audit` can audit this skill's output for vintage staleness and consistency.
