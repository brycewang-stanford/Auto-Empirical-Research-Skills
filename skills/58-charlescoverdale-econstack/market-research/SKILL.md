---
name: market-research
description: Industry and market research. Market sizing, structure, competition, regulation, supply chains, pricing, M&A. Produces a single compact, source-cited research report with Porter's Five Forces, HHI / CR4, PESTLE, and trade flows. Supports UK, US, EU, Australia, and global scope, with multi-geography comparison.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
  - Skill
  - WebSearch
  - WebFetch
---

**Only stop to ask the user when:** the sector or geography is undefined, or a non-standard analysis focus is requested.
**Never stop to ask about:** data source selection (use the source hierarchy), section ordering, Porter / PESTLE structure, or output filename.

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

# /market-research: Industry and Market Analysis

Produces a structured, source-cited market research report for any industry or product. First-time users get a complete analysis from one invocation covering market sizing, key players, concentration, Porter's Five Forces, PESTLE macro-environment, regulatory environment, supply chains, and outlook. Every data point is cited.

## Arguments

```
/market-research [sector or product] [options]
```

**Examples:**
```
/market-research "UK grocery retail"
/market-research "semiconductors" --geo global
/market-research "residential mortgages" --geo uk,us
/market-research "UK childcare" --focus regulation
/market-research "EV batteries" --depth quick --format pptx
```

**Options:**
- `--geo <code(s)>` : `uk` (default), `us`, `eu`, `au`, or `global`. Multi-geography via commas: `--geo uk,us`.
- `--depth <level>` : `quick` (one-page briefing), `standard` (default, full report), `deep` (extended with primary research pointers).
- `--focus <topic>` : Narrow to a theme. Options: `sizing`, `competition`, `regulation`, `supply-chain`, `pricing`, `outlook`. Reduces the report to the relevant sections.
- `--section <name>` : Emit only one sub-component. Options: `full` (default), `summary`, `sizing`, `players`, `concentration`, `porter`, `pestle`, `regulation`, `supply`, `trade`, `pricing`, `outlook`. Combinable with commas.
- `--format <type>` : Output format(s). `markdown` (default, always generated), `xlsx`, `word`, `pptx`, `pdf`, or `all`.
- `--client "Name"` : Add "Prepared for" metadata. Also shapes writing register.

## Supported geographies

| Code | Scope | Primary sources |
|------|-------|----------------|
| `uk` | United Kingdom (default) | ONS, CMA, ORR, Ofgem, Ofcom, FCA, HMRC trade data |
| `us` | United States | BLS, Census, FTC, FCC, NAICS data, BEA |
| `eu` | European Union | Eurostat, European Commission DG COMP, Comext trade |
| `au` | Australia | ABS, ACCC, APRA, industry code ANZSIC, DFAT trade |
| `global` | Global / multi-region | UN Comtrade, IMF, OECD, World Bank, UNCTAD |

Multi-geography via commas: `--geo uk,us,eu`. Each geography is reported side by side in the main tables.

## Instructions

### Step 1: Detect sector, geography, and focus

If the user argument does not specify a sector, ask once. Detect geography from context ("UK grocery" → `uk`). Default to `uk` and `standard` depth if unclear.

Parse `--focus` if set to narrow the scope.

### Step 2: Source hierarchy

When gathering data, prefer sources in this order:

1. **Official statistics**: ONS, BLS, Eurostat, ABS (for sizing, employment, GVA)
2. **Regulatory filings**: CMA, FTC, EC DG COMP, ACCC (for competition structure, M&A history)
3. **Trade data**: HMRC, UN Comtrade, Comext, DFAT (for imports and exports)
4. **Industry codes**: SIC (UK), NAICS (US), NACE (EU), ANZSIC (AU) for precise scoping
5. **Company filings**: Annual reports, 10-Ks, competition merger notifications (for player-level data)
6. **Trade associations**: sector-specific reports (with caveats on methodology)
7. **News and trade press**: recent M&A, pricing moves, regulatory announcements

Do NOT use unverifiable blog posts, low-credibility aggregators, or AI-generated summaries.

### Step 3: Build the report (silent)

Walk through the standard sections internally. Do not narrate.

1. **Executive summary**: one paragraph, the three things the decision-maker needs.
2. **Market sizing**: total addressable market, served market, growth rate, historical 5-year context.
3. **Segmentation**: 3-5 key segments with size shares.
4. **Key players**: top 5-10 with market share, recent strategic moves.
5. **Concentration**: HHI and CR4 from public data. Note if data is incomplete.
6. **Porter's Five Forces**: one paragraph per force with a qualitative rating (Low / Moderate / High threat or rivalry).
7. **PESTLE**: one line per factor covering Political, Economic, Social, Technological, Legal, Environmental.
8. **Regulatory environment**: main regulators, recent or upcoming regulatory changes.
9. **Supply chain**: upstream inputs, midstream transformation, downstream distribution, vulnerability points.
10. **Trade flows**: imports and exports, tariff position, trade balance in the sector.
11. **Pricing and margins**: price trends, margin profile, elasticity if known.
12. **Outlook and scenarios**: 3-year outlook, upside and downside scenarios.

### Step 4: Write the output

Save `market-[slug]-[YYYY-MM-DD].md` with this structure.

```markdown
<!-- KEY NUMBERS
type: market-research
sector: [sector]
geography: [geo]
depth: [depth]
market_size_m: [value]
growth_rate_pct: [value]
hhi: [value]
cr4: [value]
date: [YYYY-MM-DD]
-->

# Market Research: [Sector] ([Geography])

**Date**: [YYYY-MM-DD] · **Geography**: [geography] · **Depth**: [depth]

## Executive summary

[One paragraph, three takeaways. Written for the decision-maker the report is for. No filler.]

## Market sizing

[Two paragraphs: total addressable market, served market, growth rate, historical 5-year context. One small table.]

| Metric | Value | Source |
|--------|------:|--------|
| Total market size (latest year) | [currency][val] | [Source] |
| 5-year CAGR | [val]% | [Calculated from Source] |
| Forecast growth (3-year) | [val]% | [Forecast source] |

## Segmentation

Table: Market segments.

| Segment | Size ([currency]) | Share | Growth |
|---------|------------------:|------:|-------:|
| [Segment 1] | [val] | [val]% | [val]% |
| [Segment 2] | [val] | [val]% | [val]% |
| [Segment 3] | [val] | [val]% | [val]% |

## Key players

Table: Top players.

| Player | Market share | Strategic move |
|--------|-------------:|----------------|
| [Player 1] | [val]% | [Recent move, one line] |
| [Player 2] | [val]% | [Recent move, one line] |
| [Player 3] | [val]% | [Recent move, one line] |

## Market structure

| Metric | Value | Interpretation |
|--------|------:|----------------|
| HHI | [val] | [Unconcentrated / Moderately concentrated / Highly concentrated] |
| CR4 | [val]% | [Competitive / Moderate / Concentrated] |
| Barriers to entry | [Low / Moderate / High] | [One line] |

## Porter's Five Forces

| Force | Rating | Key drivers |
|-------|:------:|-------------|
| Competitive rivalry | [L/M/H] | [one line] |
| Threat of new entrants | [L/M/H] | [one line] |
| Bargaining power of suppliers | [L/M/H] | [one line] |
| Bargaining power of buyers | [L/M/H] | [one line] |
| Threat of substitutes | [L/M/H] | [one line] |

**Overall attractiveness**: [Unattractive / Moderate / Attractive]. [One-line reason.]

## PESTLE

| Factor | Key point |
|--------|-----------|
| Political | [One line] |
| Economic | [One line] |
| Social | [One line] |
| Technological | [One line] |
| Legal | [One line] |
| Environmental | [One line] |

## Regulatory environment

[Two paragraphs: main regulators, upcoming changes, compliance burden.]

## Supply chain

[Two paragraphs: upstream inputs and their sourcing, midstream transformation, downstream distribution, points of vulnerability.]

## Trade flows

Table: Trade position.

| Flow | Value ([currency]) | Top partner | Tariff regime |
|------|-------------------:|-------------|---------------|
| Imports | [val] | [country] | [regime] |
| Exports | [val] | [country] | [regime] |
| **Net trade** | **[val]** | | |

## Pricing and margins

[One paragraph: price trends, margin profile, elasticity if known.]

## Outlook and scenarios

**Central**: [One paragraph, 3-year outlook.]

**Upside scenario**: [One-liner on what would make it better.]

**Downside scenario**: [One-liner on what would make it worse.]

## References

[List of all cited sources with URLs. Every data point in the report must map to one of these sources.]
```

**Sub-component selection** (via `--section`): emit only the requested parts. Always include the header block and Executive summary.

- `full` (default): the whole structure above.
- `summary`: executive summary only.
- `sizing` / `players` / `concentration` / `porter` / `pestle` / `regulation` / `supply` / `trade` / `pricing` / `outlook`: that single section only.
- Combinable: `--section summary,porter,outlook`.

**Format-specific output structure** (only produce formats explicitly requested; see dispatcher below):
- **Markdown (.md)**: `market-[slug]-[date].md` with the structure shown above.
- **Excel (.xlsx)**: workbook with sheets: `Summary`, `Sizing`, `Players`, `Segments`, `Trade`, `Porter` (one row per force), `PESTLE`.
- **Word (.docx)**: one document, full report with cover page, hyperlinked sources.
- **PowerPoint (.pptx)**: 7 slides: (1) Exec summary, (2) Market sizing, (3) Players and concentration, (4) Porter's Five Forces, (5) PESTLE and regulation, (6) Trade and supply chain, (7) Outlook. Action titles.
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
Market research complete. [Sector] ([Geography]). Market size [val], CAGR [val]%, HHI [val].

Saved:
  market-[slug]-[date].md
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

Before asserting any factual claim about an industry classification, concentration threshold, or framework definition, ground it in the canonical source. Common gotchas: HHI thresholds (US DOJ 2023 guidelines: <1,000 unconcentrated, 1,000-1,800 moderately concentrated, >1,800 highly concentrated; the older 1,500/2,500 thresholds are deprecated), industry classification systems (SIC, NAICS, ANZSIC, NACE differ; cite which one), Porter's Five Forces are forces NOT determinants (use the canonical names: rivalry, threat of new entrants, threat of substitutes, supplier power, buyer power). Do not assert market sizes from training-data recall; pull from a primary publication.

## Out of scope (unless explicitly requested)

The following are NOT produced unless the user explicitly asks for them via flags or natural language:

- **Investment recommendations.** Do not say "this is a good market to enter" or "investors should". State the structural facts; let the reader judge.
- **M&A predictions.** Do not name specific deals as "likely". Cite announced deals only.
- **Stock recommendations.** No buy/sell/hold language on listed companies.
- **Litigation predictions.** Do not forecast regulatory or antitrust outcomes.
- **Forward private-firm valuations** unless the user supplies them.

If the user's request requires content from this list, ask first.

## Important rules

- **Credibility is everything.** Every data point is cited inline (see Citation discipline above). No unverifiable claims. Prefer official sources.
- **Source hierarchy is strict.** Official → regulatory → trade → industry codes → company filings → trade associations → news. Use the highest available.
- **Porter ratings are qualitative with drivers.** Do not assign a rating without naming the drivers.
- **HHI and CR4 use public data.** If data is incomplete, note it explicitly rather than inventing numbers.
- **Multi-geography reports use side-by-side tables**, not separate country sections.
- **No AI-generated sources.** Do not cite ChatGPT outputs, GPT summaries, or unverifiable aggregators as sources.
- **Em dashes**: never use em dashes. Use commas, colons, parentheses, or "and".

## Integration with other skills

- `/macro-briefing` provides the macro context; this skill references it for PESTLE Economic.
- `/econ-audit` can audit this skill's output for source quality and HHI / CR4 calculation consistency.
