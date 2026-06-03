<!-- Vendored into AERS from https://github.com/charlescoverdale/econstack on 2026-06-01. Upstream attribution + license preserved. -->

> **Vendored upstream skill.** Curated snapshot of [`charlescoverdale/econstack`](https://github.com/charlescoverdale/econstack) for the AERS catalog (license: MIT (declared in README; no LICENSE file upstream)). Vendored 2026-06-01. The original upstream README follows verbatim.

---

# econstack

![Version](https://img.shields.io/badge/version-0.14.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Skills](https://img.shields.io/badge/skills-7-orange)

Professional economic analysis, powered by AI.

econstack is a set of [Claude Code](https://claude.ai/code) skills that handle the mechanical parts of economic analysis: live macro and fiscal briefings, market research, policy briefing notes, pre-appraisal longlisting, full cost-benefit analysis, and methodology audit. 7 skills designed to work on the inputs and checks around a policy decision, so you can focus on the judgement calls. Supports HM Treasury Green Book, EU Better Regulation, World Bank, Asian Development Bank, and Australian Treasury (Victoria) frameworks with framework-native output.

Backed by 57 audited parameter files and 20+ R packages on CRAN.

### Who this is for

- An analyst pulling a macro briefing before a ministerial meeting
- A policy officer drafting a 2-page briefing note for a minister or board
- An economist brainstorming a benefits and costs longlist before a CBA
- A trade analyst assessing bilateral trade flows and comparative advantage
- A researcher auditing the methodology of an economic analysis output

If you spend time pulling macro and fiscal data, structuring briefing notes, scoping out benefits and costs, or auditing analysis, econstack automates the mechanical parts so you can focus on the judgment calls.

If you already have a report, model, or output format that you like, tell Claude where it is located and it will match your structure and style. Your previous work becomes the template for future analyses.

### How to integrate econstack into your workflow

Talk to econstack the way you would brief an analyst or junior staff member. Use Claude's voice input and speak naturally: "Give me a macro briefing on UK inflation and interest rates for next week's committee." econstack picks up the framework, parameters, and structure from context, so you do not need to remember flags or syntax. The more context you give up front (project documents, prior reports, costings, stakeholder feedback), the less back-and-forth you will have. Point it at your files and let it read them. Think of it as delegating the first draft to a competent analyst who knows the standard frameworks, then applying your own judgement to the output.

---

## Quick start

Copy and paste this chunk into Claude Code:

```bash
# Install the skills
git clone https://github.com/charlescoverdale/econstack.git ~/.claude/skills/econstack

# Register skills so Claude Code discovers them
~/.claude/skills/econstack/bin/econstack-relink

# Get the data (391 UK local authority datasets + CBA parameter database)
git clone https://github.com/charlescoverdale/econstack-data.git ~/econstack-data

# Optional: cut down permission prompts during long runs
# (copy into your project's .claude/ folder or merge into ~/.claude/settings.json)
cp ~/.claude/skills/econstack/.claude/settings.json.example .claude/settings.json
```

Your project files stay on your computer. When you run a skill, Claude Code reads the files you point it at, sends that content to Anthropic to generate the analysis (as with any LLM request), and writes the output back to your machine. That is the entire data flow. econstack itself has no server, no database, and does not share anything with third parties. Anthropic does not train on the content of API requests by default.

You can come to econstack with zero project documents and start from a one-line description, or you can point it to wherever your existing materials live: costings, design briefs, brainstorming notes, prior business cases, stakeholder correspondence. The skill reads them automatically and factors the bespoke context into the analysis, so you do not need to retype anything you have already captured elsewhere.

---

## Frameworks and output formats

### Frameworks

| Flag | Framework |
|------|-----------|
| `uk-gb` | [UK HM Treasury Green Book (November 2025)](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government) |
| `eu-brg` | [EU Better Regulation Guidelines (2021, SWD(2021) 305)](https://commission.europa.eu/law/law-making-process/planning-and-proposing-law/better-regulation/better-regulation-guidelines-and-toolbox_en) |
| `wb` | [World Bank Economic Analysis of Investment Operations (OP 10.04)](https://www.worldbank.org/en/projects-operations/products-and-services/brief/economic-analysis) |
| `adb` | [Asian Development Bank Guidelines for the Economic Analysis of Projects (2017)](https://www.adb.org/documents/guidelines-economic-analysis-projects) |
| `au-vic` | [Victorian Treasury High Value High Risk (HVHR) framework](https://www.dtf.vic.gov.au/infrastructure-investment/high-value-high-risk-framework) |

Framework defaults are applied automatically: the right discount rate, the right unit values (VSL, QALY, shadow wages, carbon prices), the right additionality conventions, and the right optimism bias uplift for the jurisdiction.

### Output formats

Every skill generates markdown by default, and can also export to Excel, Word, PowerPoint, or PDF via `--format`.

| Format | Flag | When to use |
|--------|------|-------------|
| Markdown | default, always generated | Plain text you can paste into any editor, issue tracker, wiki, or chat. Source of truth that other formats are rendered from. |
| Excel | `--format xlsx` | Full investment banking style spreadsheet workbooks with blue input cells and linked formulas. |
| Word | `--format word` | Formatted document for editing in Microsoft Word. Hyperlinked references, cover page, table of contents. |
| PowerPoint | `--format pptx` | Slide deck with action titles (sentences stating the insight) and 3-4 evidence bullets per slide. The kind of deck you'd take to a board, minister, or investment committee. |
| PDF | `--format pdf` | Consulting-quality PDF rendered through Quarto. |
| All | `--format all` | All of the above in one invocation. |

Combine formats with commas: `--format markdown,xlsx,pptx`.

---

## Skills

### `/longlist`

The messy-whiteboard-phase skill. Before you run a CBA, a business case, or an RIA, you need to know what benefits to measure and what costs to include. `/longlist` is a structured brainstorm that helps you think through both, systematically, using multiple lenses (stakeholder mapping, Theory of Change, framework taxonomy, sector template, commonly-missed checklist). It runs the brainstorm internally and shows you the result: two clean tables of benefits and costs that you can hand straight to any downstream CBA or business case workflow.

The headline output is a seven-column table of benefits and costs: number, name, plain-English description, materiality rating (H/M/L), cash flow tag (Cash in / Cash out / Non-cash), how to quantify, and how to monetise.

**The cash flow tag is the bridge to the financial case.** Every item is tagged from the sponsor's perspective: cash in (real money onto the sponsor's books), cash out (real money off the sponsor's books), or non-cash (social value with no money attached, like heat deaths avoided, WELLBYs, biodiversity). This drives the financial case downstream: only cash in and cash out items count for the Financial NPV, while the full set counts for the Economic NPV. That lets you tell whether a project is socially worthwhile AND financially self-sustaining in one go.

**How to quantify / monetise: the bridge to the NPV.** Every item gets a suggested estimation method, either a published unit value from a named data source, an analytical approach, or "qualitative only" if no defensible monetisation exists.

Recognises the three classic double-counting traps and flags them automatically: construction employment + capital cost, journey time savings + land value uplift, and gross earnings + tax revenue. Excludes sunk costs by default.

```
/longlist "New secondary school in Leeds" --framework uk-gb --format xlsx,word
```

---

### `/cost-benefit`

The full Green Book cost-benefit analysis. Takes a project description (or a `/longlist` markdown file via `--from`) and returns an economic NPV and a financial NPV side by side, with a one-line headline verdict telling you whether the project is socially worthwhile **and** financially self-sustaining. Backed by the [`greenbook` R package](https://github.com/charlescoverdale/greenbook) when available, with graceful fallback when not.

The skill closes the methodology gaps that most off-the-shelf CBAs miss: kinked Social Time Preference Rate (3.5/3.0/2.5/2.0/1.5% across 30/75/125/200/300-year bands), GDP-deflator real-terms rebasing, optimism bias with mitigation factor (Mott MacDonald 2002 categories), Marginal Excess Tax Burden of 20% on tax-financed costs (mandatory under Green Book 2022 §5.36), WELLBY / QALY / VPF wellbeing valuation routed through dedicated greenbook functions on the 1.5% health schedule, DESNZ Nov-2023 single-consolidated carbon series with low/central/high scenarios (the historical traded vs non-traded split has been retired), iso-elastic distributional weights at eta = 1.3, EANC for unequal-life options, sensitivity in one paragraph (scenario / switching / tornado / discount-rate), referent group identity check, validation gate that aborts on broken counterfactuals or missing METB, sidecar JSON for downstream Five Case Model handoff, and an automatic `/econ-audit` pass on the produced markdown. Supports `uk-gb`, `eu-brg`, `wb`, `adb`, `au-vic` with framework-native parameter sets.

Every output carries a vintage stamp: greenbook version, STPR vintage, GDP deflator vintage, OB / METB / carbon / VPF / QALY / WELLBY vintages. So an appraisal you ran today can be re-run a year from now and the numbers will still be reproducible against the same parameter set.

```
/cost-benefit --from longlist-leeds-school-2026-05-07.md
/cost-benefit "Rural water project, Indonesia" --framework adb
/cost-benefit "Victorian level crossing removal" --framework au-vic
/cost-benefit --from longlist.md --ob-mitigation 0.4 --carbon-scenario high --format xlsx,word
```

---

### `/macro-briefing`

Up-to-date macroeconomic reports for the UK, US, Euro area, and Australia. Tell it what you care about most (CPI, GDP growth, labour market, yield curves) or let it pick for you. Pulls live data from official government databases (ONS, FRED, ECB, ABS), structures it into a professional briefing following each central bank's reporting conventions, and lets you tailor the output to the indicators that matter for your work. Every number is traceable: full methodology, data sources, and vintage dates included.

Traffic-light macro assessment (GREEN/AMBER/RED) with quantitative thresholds. Good before a ministerial meeting, investment committee, or board paper.

```
/macro-briefing --country uk --format pdf
```

---

### `/fiscal-briefing`

Up-to-date public finances reports for the UK, US, and Australia. Pulls live data from official sources (ONS, OBR, FRED, ABS), covers borrowing, debt, receipts by tax, spending by category, and fiscal rules or sustainability context. Every number is traceable: full methodology, data sources, and vintage dates included. Optionally add a debt sustainability analysis powered by the `debtkit` R package.

```
/fiscal-briefing --country uk --format pdf
```

---

### `/market-research`

Industry and market analysis for any sector or product. Combines official statistics (ONS, BLS, Eurostat), regulatory data (CMA, FTC, EC), company filings, trade data (HMRC, UN Comtrade, Comext), and trade sources into a structured, source-cited research report. Covers market sizing, market segmentation, key players, M&A activity, pricing trends, market structure (HHI, CR4, contestability), Porter's Five Forces, PESTLE macro-environment, regulatory environment, supply chains, trade flows, demand drivers, industry history, and outlook with scenario analysis.

Supports UK, US, EU, Australia, and global scope. Multiple geographies can be combined for cross-market comparison (e.g. `--geo uk,us`). Adapts writing style to the client and audience (GOV.UK, European Commission, academic, board, public). Lets you specify preferred data sources or bring your own data. All data points are source-cited with full references.

```
/market-research "UK grocery retail"
/market-research "semiconductors" --geo global
/market-research "residential mortgages" --geo uk,us
/market-research "UK childcare" --focus regulation --depth quick
```

---

### `/briefing-note`

Two-page policy briefing note for ministers, boards, committees, and internal decision-makers. Problem, analysis, options, recommendation. Four templates covering minister submissions, board papers, committee briefings, and internal memos. This is the skill to use when you need to put something in front of a decision-maker quickly, with the right level of formality for the audience.

```
/briefing-note "Public transport fare cap policy"
/briefing-note "Response to consultation on XYZ"
```

---

### `/econ-audit`

Think of it as a senior partner and an economics professor going through your work and poking holes in it. Full methodology audit of any output from the skills above, or any economic analysis you point it at. Runs 124 checks across 17 categories and produces a RAG (red, amber, green) rating on how your methods and assumptions compare to best practice. Agnostic to region or asset class: it draws on government guidance (Green Book 2026, Aqua Book, EU Better Regulation Toolbox, World Bank Guidance Note) and published academic literature (Flyvbjerg, Moretti, Flegg) to assess numerical consistency, discount rates, additionality, multiplier plausibility, double counting, framing, Five Case Model completeness, distributional analysis, Aqua Book RIGOUR compliance, and strategic misrepresentation patterns.

When it finds issues, it gives you a structured step-by-step plan to fix them and updates the methodology accordingly. Designed to improve over time as the rest of the repo evolves: as the parameter database and skill coverage expand, so does the audit's ability to cross-check your work.

```
/econ-audit macro-uk-2026-04-03.md --strict
/econ-audit . --fix
```

Letter grade A-F, with auto-fix option.

---

## Data

econstack comes preloaded with the data you need for most economic analysis work: discount rates, carbon values, VSL, QALYs, shadow wages, optimism bias tables, additionality conventions, tax parameters, and more. It also carries 391 UK local authority datasets covering employment, earnings, IO multipliers, population, housing, GVA, deprivation, skills, and commuting. All of this lives in the second repo you clone during install (`~/econstack-data/`) and is versioned, source-cited, and checked for staleness so you can trust the numbers without chasing them down yourself.

You can always override any parameter or bring your own data. If you have in-house unit costs, bespoke discount assumptions, or project-specific inputs, point the skill at them and it will use yours instead of the defaults. For the full list of parameters, source citations, and vintage dates, see the [parameters README](https://github.com/charlescoverdale/econstack-data/blob/main/parameters/README.md).

---

## Structure

```
econstack/
├── macro-briefing/      /macro-briefing Macroeconomic monitor (UK, US, EU, AU)
├── fiscal-briefing/     /fiscal-briefing Public finances (UK, US, AU)
├── market-research/     /market-research Industry and market analysis (multi-geo)
├── briefing-note/       /briefing-note  Policy briefing note (4 templates)
├── longlist/            /longlist       Pre-appraisal benefits and costs longlist (5 frameworks)
├── cost-benefit/        /cost-benefit   Cost-benefit analysis (greenbook-backed, 5 frameworks)
├── econ-audit/          /econ-audit     Methodology audit (124 checks)
├── templates/
│   └── blocks/          Shared template blocks (preamble, formatting, rules)
├── scripts/
│   ├── gen-skill-docs.sh  Generate SKILL.md from SKILL.tmpl + blocks
│   └── render-report.sh   PDF rendering via Quarto
├── bin/
│   ├── econstack-relink       Register skills so Claude Code discovers them
│   └── econstack-update-check
└── README.md
```

Backed by 16 R packages on [CRAN](https://cran.r-project.org/) and a [57-file parameter database](https://github.com/charlescoverdale/econstack-data) and 8 reference case templates.

---

## Contributing

Edit the relevant `<skill>/SKILL.tmpl` and run `scripts/gen-skill-docs.sh <skill>` to regenerate the SKILL.md. Follow the format of existing skills, and open a PR.

## License

MIT
