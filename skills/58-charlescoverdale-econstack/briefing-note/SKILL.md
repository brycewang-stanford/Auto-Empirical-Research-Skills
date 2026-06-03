---
name: briefing-note
description: Structured policy briefing note (1-2 pages). Issue, background, analysis, options, recommendation. UK GES, Australian Treasury, consulting formats. Auto-populates from econstack data skills.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
  - WebSearch
  - WebFetch
---

**Only stop to ask the user when:** the policy issue is unclear, the audience is ambiguous, or multiple conflicting options exist and the user needs to choose a framing.
**Never stop to ask about:** format (use the detected template), section ordering, data sources (use the best available), or citation style.
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

# /briefing-note: Policy Briefing Note

Generate a structured 1-2 page policy briefing note. The most common output of government and consulting economists: a short, decision-focused document that presents an issue, analyses it, sets out options, and makes a recommendation.

**This skill is interactive.** It confirms the topic, audience, and framing, then generates the note.

## Arguments

```
/briefing-note [topic] [options]
```

**Examples:**
```
/briefing-note "Impact of the new minimum wage increase on hospitality sector employment"
/briefing-note "Options for reforming business rates" --audience minister
/briefing-note "Economic case for extending childcare subsidies" --format au-ris
/briefing-note "Trade implications of US tariff changes for UK manufacturing" --format word
```

**Options:**
- `--audience <type>` : Target reader. `minister` (default), `board`, `cabinet`, `sr` (spending review), `public`. Adjusts tone and detail level.
- `--format <template>` : Briefing template. `uk-ges` (default), `au-treasury`, `consulting`, `think-tank`. See templates below.
- `--stance <position>` : `neutral` (default, present options equally), `recommend` (lead with a recommendation), `advocate` (make the case for a specific position, with caveats).
- `--length <pages>` : `1` or `2` (default). Page 1 is always the core brief; page 2 adds deeper analysis.
- `--data` : Auto-populate with live data from econstack R packages (ons, boe, fred, etc.) where relevant.
- `--with-cba <file>` : Import a CBA output to summarise in the options section.
- `--with-io <file>` : Import an IO report to summarise in the analysis section.
- `--client "Name"` : Add "Prepared for" metadata.
- `--format-output <type>` : Output format: `markdown`, `word`, `pptx`, `pdf`, or `all`. Default: markdown.
- `--exec` : Generate a 3-slide executive summary deck.

## Templates

### UK GES format (`uk-ges`, default)

The standard Government Economic Service briefing structure:

```
RESTRICTED / OFFICIAL-SENSITIVE [classification]

TO:        [Minister / Director / Board]
FROM:      [Team / Division]
DATE:      [Date]
SUBJECT:   [One-line topic]

1. ISSUE
[1-2 sentences. What decision is needed and why now?]

2. BACKGROUND
[3-5 sentences. Context the reader needs. What has happened,
what is the current position, why does it matter?]

3. ANALYSIS
[The core economic analysis. 1-3 key findings with numbers.
Each finding should be a bolded topic sentence followed by
1-2 sentences of evidence. Cite sources.]

4. OPTIONS
[2-4 options, each with:
  - What it involves (1 sentence)
  - Estimated cost/benefit (1 line)
  - Pros (1-2 bullets)
  - Cons (1-2 bullets)]

5. RECOMMENDATION
[1-2 sentences. Which option and why. If --stance neutral,
present the trade-off and leave the decision to the reader.]

6. NEXT STEPS
[2-3 bullet points. What happens if the recommendation
is accepted. Timeline.]

ANNEX: [Optional. Key data table or chart. 1 page max.]
```

### Australian Treasury format (`au-treasury`)

```
BRIEF FOR [Minister / Secretary / Board]

TOPIC:     [One-line subject]
TIMING:    [Why now? Decision deadline if applicable]
ACTION:    [What is the reader being asked to do?]

KEY POINTS
- [Bullet 1: the single most important thing]
- [Bullet 2: supporting point]
- [Bullet 3: risk or caveat]

BACKGROUND
[3-5 sentences of context]

ANALYSIS
[Core analysis with numbers. Include comparison to
other jurisdictions where relevant (UK, NZ, Canada).]

OPTIONS
[Structured as above. Australian briefs tend to include
fiscal impact explicitly for each option.]

RECOMMENDATION
[Direct. Australian briefs are typically more explicit
in their recommendation than UK ones.]

Cleared by: [Division Head]
Contact:    [Officer name, phone]
```

### Consulting format (`consulting`)

```
[CLIENT LOGO PLACEHOLDER]

ECONOMIC BRIEFING: [TOPIC]
[Date] | Prepared for [Client]

EXECUTIVE SUMMARY
[3-4 sentences covering the issue, key finding, and recommendation.
Bolded key numbers. Action-oriented language.]

CONTEXT
[Why this matters to the client specifically.
Link to their strategy / KPIs / current programme.]

KEY FINDINGS
[3-5 findings, each as a bolded headline sentence + 2-3 lines
of supporting evidence. Use bullet points for data.]

IMPLICATIONS AND OPTIONS
[2-3 options with estimated impact. Frame in terms of
the client's objectives, not abstract policy goals.]

RECOMMENDED APPROACH
[Clear recommendation with implementation steps.]

APPENDIX: METHODOLOGY AND SOURCES
[Brief note on data sources and analytical approach.
1-2 sentences, not a full methodology section.]
```

### Think-tank format (`think-tank`)

```
[TITLE: Provocative, insight-led headline]
[Subtitle: one sentence framing]

[Author name / Team] | [Date]

[Opening paragraph: the hook. Start with the most surprising
or important finding, not the background. Think Resolution
Foundation / IFS / Grattan Institute style.]

[2-3 sections of analysis with charts/tables. Each section
has a bolded finding as a heading.]

[Policy implications: what should government do?]

[Methodology note: 2-3 sentences at the end.]
```

## Instructions

### Step 1: Parse the request

Extract:
- **topic**: The policy issue or question
- **audience**: minister (default), board, cabinet, sr, public
- **template**: uk-ges (default), au-treasury, consulting, think-tank
- **stance**: neutral (default), recommend, advocate
- **length**: 1 or 2 pages
- **data**: whether to auto-populate with live data

If the topic is not provided, ask:
```
AskUserQuestion: "What is the policy issue or question for this briefing note?"
(Free text)
```

### Step 2: Confirm the framing

Before writing, confirm the framing with the user:

```
AskUserQuestion: "I'll write a [length]-page [template] briefing note on '[topic]' for [audience]. The stance will be [stance]. Is this right?"
Options:
  - "Yes, go ahead" (Recommended)
  - "Change the audience"
  - "Change the template"
  - "Change the stance"
```

### Step 3: Gather data (if --data or if topic is data-dependent)

If the topic relates to macroeconomic indicators, fiscal data, trade data, or local authority data, pull relevant data using econstack R packages:

```r
# Check which packages are available
macro_available <- requireNamespace("ons", quietly = TRUE) ||
                   requireNamespace("fred", quietly = TRUE)
trade_available <- requireNamespace("comtrade", quietly = TRUE)
```

Use the data to populate the Analysis section with specific numbers. Always cite the source and date of the data.

If the topic requires data that is not available via R packages, use WebSearch to find the latest figures from official sources.

### Step 4: Write the briefing note

Follow the selected template exactly. Key principles:

**Tone by audience:**
- `minister`: Short sentences. No jargon. Lead with "so what." Every paragraph earns its place.
- `board`: Slightly more technical. Can use economic terms without defining them. Focus on financial implications.
- `cabinet`: Political awareness. Flag distributional impacts and regional effects. Note any media/public sensitivity.
- `sr`: Fiscal focus. Everything framed in terms of spending, savings, and value for money. Reference Spending Review guidance.
- `public`: Plain English. No acronyms. Explain why this matters to people's lives.

**Tone by stance:**
- `neutral`: Present options equally. "On the one hand... on the other." End with "Ministers may wish to consider..."
- `recommend`: Lead with the recommendation. Present options but signal preference. "We recommend Option B because..."
- `advocate`: Make the strongest case for the preferred position, while honestly noting risks and counterarguments.

**Data presentation:**
- Bold the key number in every analytical paragraph.
- Use "X is Y% higher/lower than Z" format, not "X is Y."
- Always state the comparator (vs last year, vs the national average, vs the counterfactual).
- Round to meaningful precision (GDP growth to 1dp, employment to nearest thousand, spending to nearest million).

**Length control:**
- 1 page = ~500 words. Issue (2 sentences), Background (3 sentences), Analysis (3 findings x 2 sentences each), Options (2-3 x 3 lines each), Recommendation (2 sentences).
- 2 pages = ~1000 words. Same structure but Analysis section expands to include a data table or chart, and Options section adds fiscal impact estimates.

### Step 5: Generate the KEY NUMBERS block

```markdown
<!-- KEY NUMBERS
type: briefing-note
topic: [topic]
template: [template]
audience: [audience]
stance: [stance]
date: [date]
key_finding: [one sentence]
-->
```

### Step 6: Output

Save as `briefing-{slugified-topic}-{date}.md` if and only if markdown is in the requested output set (the default).

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


(Note: in this skill `--format` selects the briefing template, not the output format. Output format is controlled by `--format-output`. The dispatcher above applies to whatever the user passes via `--format-output`.)

If `--exec` specified, generate a 3-slide deck:
1. Title + issue statement
2. Key finding + supporting evidence (3 bullets)
3. Recommendation + next steps

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

Briefing notes are decision tools and so factual errors are particularly damaging. Before asserting any quantitative or technical claim, verify it against a primary source. If a needed fact is not available in the fetched data or supplied context, say so explicitly rather than recall from memory:

> The latest [indicator] for [period] has not yet been published.

Common gotchas in policy briefing: definitions drift between governments (e.g. "free school meals", "hate crime", "rough sleeping" all have specific operational definitions that have changed); thresholds and rates change frequently; "the government has committed to X" requires a citation to a specific document.

## Out of scope (unless explicitly requested)

A briefing note is constrained by `--stance`. Do not exceed it:

- If `--stance neutral`, do NOT smuggle a recommendation into analysis sections. Keep analysis and recommendation strictly separate.
- If `--stance advocate`, do NOT hide counterarguments; the reader's trust depends on acknowledging downsides.
- Do NOT predict election outcomes, party positions, or politician behaviour.
- Do NOT generate options the user did not ask for; if scope feels limited, ask whether to expand.

## Important Rules

- Never use em dashes.
- Never attribute econstack to any individual.
- Every section stands alone.
- **Numbering**: Every table is "Table 1: [short description]", every figure/chart is "Figure 1: [short description]". Numbering restarts at 1 for each report. The caption goes above the table/figure.
- **Source note**: Below every table and figure: "Source: [Author/Publisher] ([year])." If multiple sources: "Sources: [Source 1]; [Source 2]."
- **Notes line**: Below the source, if needed: "Notes: [caveats, e.g. 'real 2026 prices', '2024-25 data', 'estimated from available figures']."
- **Minimal formatting (low ink-to-data ratio)**: No heavy borders or gridlines. Thin rule under the header row only. No shading on data cells (light grey alternating rows permitted in Excel/HTML only). Right-align all numbers. Left-align all text. Bold totals rows only. No decorative elements.
- **Number formatting**: Currency with comma separators and 1 decimal place for millions (e.g. "GBP 45.2m" / "AUD 45.2m"), whole numbers for counts (e.g. "1,250 jobs"), percentages to 1 decimal place (e.g. "3.5%").
- **Consistency**: The same metric must use the same unit and precision throughout the report. Do not switch between "GBP m" and "GBP bn" for the same order of magnitude.
- A briefing note is not a report. It is a decision tool. Every sentence must serve the decision.
- Never exceed the requested page length. If in doubt, cut. Senior readers stop reading after page 1.
- The Issue section is the most important sentence in the document. If the reader reads nothing else, they should understand what decision is needed.
- Numbers must have context. "Unemployment is 4.2%" is meaningless without "up from 3.8% a year ago" or "the highest since 2021."
- Never present analysis without a "so what." Every finding must connect to the decision at hand.
- If --stance is neutral, do not smuggle a recommendation into the analysis section. Keep analysis and recommendation separate.
- If --stance is advocate, be honest about counterarguments. The reader's trust depends on acknowledging downsides.
