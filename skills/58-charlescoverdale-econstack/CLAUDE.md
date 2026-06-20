# EconStack

Claude Code skills for professional economic analysis.

## Skills

Each skill has its own directory with a `SKILL.md` defining the workflow.

- `macro-briefing/SKILL.md` : Macroeconomic monitor (UK, US, Euro area, Australia; --international for 30-country comparison)
- `fiscal-briefing/SKILL.md` : Public finances briefing (UK, US, Australia)
- `market-research/SKILL.md` : Industry and market analysis (sizing, structure, competition, M&A, multi-geo)
- `briefing-note/SKILL.md` : Policy briefing note (1-2 pages, UK GES / AU Treasury / consulting / think-tank formats)
- `longlist/SKILL.md` : Pre-appraisal longlist builder. Brainstorms benefits and costs across 6 benefit lenses (stakeholder, market failure, ToC, framework taxonomy, sector library, Flyvbjerg-informed commonly-missed checklist) and 5 cost lenses (direct, indirect/induced, compliance/SCM, other parties, risk). Framework-aware. Outputs two clean tables that hand off to any downstream CBA or business case workflow.
- `cost-benefit/SKILL.md` : Full cost-benefit analysis. Economic NPV + Financial NPV side by side, BCR, optimism bias with mitigation, METB, real-terms rebasing, WELLBY / QALY / VPF wellbeing valuation, DESNZ Nov-2023 carbon, distributional weights, EANC, validation gate, auto-audit. Backed by the `greenbook` R package via `bin/econstack-greenbook` bridge. Sidecar JSON for downstream business-case handoff.
- `econ-audit/SKILL.md` : Methodology audit (124 checks across 17 categories, RED/AMBER/GREEN grading, includes AU framework checks)

**Preamble tiers:** All 7 skills get update check, learnings, safety hooks, and completion status. 3 skills (longlist, cost-benefit, econ-audit) additionally get the parameter database check because they read from `~/econstack-data/parameters/`. The other 4 (macro-briefing, fiscal-briefing, market-research, briefing-note) pull live data and do not use the parameter database. The cost-benefit skill also runs Step 0 backend detection against `bin/econstack-greenbook` (the greenbook R package bridge); if greenbook is unavailable it falls back to LLM-side computation with reduced reproducibility.

## Important Rules

- Never include "Co-Authored-By: Claude" in commit messages
- Never use em dashes in prose. Use colons, periods, commas, or parentheses.
- Never connect econstack to any individual person. Present as a brand/product.
- Reports must always include methodology sections and caveats. Credibility comes from transparency.
- Type I multipliers are the default (conservative). Only use Type II when explicitly requested.
- Tax estimates always get the strongest caveats (30-50% margin of error).

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

**Proactive detection:** If the user describes a task without naming a skill, match their intent to the routing table below. You do not need to wait for an explicit `/command`. For example, "What's happening with UK inflation?" should route to `/macro-briefing`.

**Econstack routing rules:**
- GDP, inflation, unemployment, wages, interest rates, macro, "what's happening with the economy" → invoke macro-briefing
- Borrowing, debt, deficit, budget, fiscal rules, public finances → invoke fiscal-briefing
- Market size, industry, competition, M&A, Porter's Five Forces, HHI → invoke market-research
- Briefing note, policy brief, ministerial brief, "write me a 2-pager", decision brief → invoke briefing-note
- Brainstorm benefits, longlist, what costs should I include, beneficiary mapping, "what am I missing", benefit streams, benefits register, pre-CBA scoping, pre-appraisal scoping → invoke longlist
- CBA, cost-benefit, NPV, BCR, appraisal, "is this worth doing", "value for money", Green Book appraisal, business case economics, METB, optimism bias, WELLBY / QALY / VPF, equivalent annual cost, switching values → invoke cost-benefit
- Audit, check methodology, review my numbers, "is this analysis right" → invoke econ-audit

**Workflow chains:**
- `/longlist` → `/cost-benefit` → `/econ-audit` is the canonical appraisal pipeline. Each skill writes a markdown deliverable that the next reads. `/cost-benefit` also writes a sidecar JSON for future `/business-case` consumption.

## Versioning

Econstack uses semver-lite. The current version is in `VERSION`.

- **MAJOR** (X.0.0): Breaking change to the parameter database schema, JSON `--from` schema, or skill invocation syntax. Anything that would break existing `--from` JSON files or require users to change how they call a skill.
- **MINOR** (0.X.0): New skill added, new framework added to an existing skill, or significant new capability (e.g. Monte Carlo, new output format, new jurisdiction).
- **PATCH** (0.0.X): Bug fixes, audit fixes, parameter updates, wording improvements, template tweaks, heading corrections.

Always bump VERSION in the same commit as the change. Include the new version in the commit message (e.g. "v0.5.0: Add /briefing-note skill").

## Learned State

Econstack remembers per-project preferences across sessions. Learnings are stored locally at `~/.econstack/projects/{slug}/learnings.jsonl`. No data is transmitted to any server.

**How it works:**
- Every skill's preamble runs `econstack-learnings-read` to load prior learnings (framework choices, parameter overrides, data preferences, past outputs, operational quirks)
- After a skill completes, new insights are logged via `econstack-learnings-log`
- Dedup by key+type (latest wins). Observed/inferred learnings decay 1 confidence point per 30 days. User-stated learnings never decay.
- Top 3 learnings are surfaced at the start of each skill run

**Bin scripts:**
- `bin/econstack-slug` : Derive project slug from git remote or cwd
- `bin/econstack-learnings-log` : Append a learning (validates JSON, auto-timestamps)
- `bin/econstack-learnings-read` : Read, dedup, decay, sort, and format learnings

**Learning types:** framework, parameter, data-source, output, operational, preference.

## Data Dependencies

**CBA parameters:** The longlist and econ-audit skills read structured parameter files from `~/econstack-data/parameters/`. 57 JSON files covering UK, US, EU, AU, World Bank, ADB, and common parameters: discount rates, carbon values, VSL, QALY, VTTS, optimism bias, additionality, tax parameters, distributional weights, construction benchmarks, and unit costs for outcome monetisation. Skills fall back to built-in defaults if parameter files are not found.

**Trade data:** The market-research and macro-briefing skills optionally use the `comtrade` R package for UN Comtrade trade flow data. Install from GitHub: `devtools::install_github("charlescoverdale/comtrade")`. Works without an API key for basic queries (500 records). For full access, register for a free key at <https://comtradedeveloper.un.org/>. If comtrade is not installed, skills fall back to WebSearch for trade data.
