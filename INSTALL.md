# Installation & Quick Start

There are three ways to use the skills in this collection, from "one command" to
"zero install". Pick the one that matches how you work.

> **Requirements for the plugin path:** [Claude Code](https://code.claude.com/docs)
> **v2.1+** (the `/plugin` marketplace commands). Run `claude --version` to check, and
> `claude` itself to upgrade if `/plugin` is missing.

---

## 1. One-command install — first-party plugins (recommended)

This repository ships a **Claude Code plugin marketplace** for its first-party,
install-ready skill stacks. Add the marketplace once, then install any plugin from it.

**From your shell:**

```bash
# Add this repo as a marketplace (one time)
claude plugin marketplace add brycewang-stanford/Auto-Empirical-Research-Skills

# Install whichever stacks you want
claude plugin install aer-skills@auto-empirical-research-skills                 # AER manuscript lifecycle (9 skills)
claude plugin install empirical-analysis-python@auto-empirical-research-skills  # explicit Python pipeline
claude plugin install empirical-analysis-stata@auto-empirical-research-skills   # explicit Stata pipeline
claude plugin install empirical-analysis-r@auto-empirical-research-skills       # tidyverse + Quarto pipeline
```

**Or from inside Claude Code (slash commands):**

```text
/plugin marketplace add brycewang-stanford/Auto-Empirical-Research-Skills
/plugin install aer-skills@auto-empirical-research-skills
```

Then run `/reload-plugins` (or restart) and the skills are live. Verify with:

```bash
claude plugin details aer-skills    # shows the skills + token cost of any installed plugin
```

### Plugins available from this marketplace

| Plugin | Skills | What it does |
|--------|--------|--------------|
| `aer-skills` | 9 | Full top-5 economics manuscript lifecycle for **AER / AER: Insights / AEJ** — topic selection, modern causal identification (DiD / IV / RDD / SCM / Bartik), referee-anticipating robustness, Keith-Head-style introductions, AER booktabs tables, AEA Data & Code Availability deposits (openICPSR-ready), submission preflight, and R&R rebuttal letters. Ships Stata / R / Python templates. |
| `empirical-analysis-python` | 1 | Explicit 8-step empirical-analysis pipeline in the traditional **Python** econometrics stack (pandas + statsmodels + linearmodels + pyfixest + rdrobust + econml + causalml). Cleaning → variables → Table 1 → diagnostics → estimation (OLS/IV/DID/RDD/PSM/SCM/DML/Causal Forest) → robustness → mechanism/heterogeneity/mediation → publication-ready tables & figures. Includes epidemiology & ML-causal modes. |
| `empirical-analysis-stata` | 1 | The same 8-step pipeline in the traditional **Stata** ecosystem (reghdfe + ivreg2 + csdid + did_imputation + sdid + rdrobust + synth + psmatch2 + teffects + esttab). From `use`/`import` to `.tex`/`.rtf` tables and `.pdf` figures, with the full modern DID toolkit. The first choice for referee-level Stata replication packs. |
| `empirical-analysis-r` | 1 | The same 8-step pipeline in the modern **tidyverse + fixest** R stack (dplyr + haven + fixest + did + synthdid + rdrobust + MatchIt + grf + DoubleML + modelsummary). All eight steps fit in one `.qmd`; `quarto render` produces a unified PDF/HTML/Word reproducibility report. |

> The `empirical-analysis-*` plugins are projected from the browse-canonical sources under
> `skills/00.1` / `skills/00.2` / `skills/00.3` by [`plugins/build_plugins.py`](plugins/build_plugins.py)
> — edit the source skill and re-run the generator to update them.
>
> **StatsPAI** (`skills/00`) is intentionally *not* packaged as a plugin here because it is
> mirrored weekly from its upstream repo (a committed copy would drift). Install it from
> [its own repo](https://github.com/brycewang-stanford/StatsPAI) (`pip install StatsPAI`) or
> use method 2 below.

---

## 2. Use any skill in the catalog — copy into `.claude/skills/`

Every entry in this catalog is a folder containing a `SKILL.md`. To use one, copy that
folder into your project's (or your global) skills directory — no marketplace needed.

```bash
# Project-scoped (only this repo/project sees it)
mkdir -p .claude/skills
cp -R skills/00.1-Full-empirical-analysis-skill_Python  .claude/skills/empirical-python

# Or global (every project sees it)
cp -R skills/00.1-Full-empirical-analysis-skill_Python  ~/.claude/skills/empirical-python
```

The folder you copy must contain a `SKILL.md` at its top level (some catalog skills nest
theirs under `skills/<name>/SKILL.md` — copy the folder that holds the `SKILL.md`). Start
a new Claude Code session and the skill auto-loads; Claude invokes it when your request
matches its `description`.

> Tip: keep the `references/` subfolder when present — those are the progressive-disclosure
> deep-dives the skill loads on demand.

### Plugin-shaped skills via `--plugin-dir`

Some vendored skills are already packaged as plugins (they have a `.claude-plugin/plugin.json`
plus a `skills/` directory — e.g. `skills/50-brycewang-aer-skills`, `skills/32-dylantmoore-stata-skill`,
and the generated `plugins/empirical-analysis-*`). Load one for a single session without installing:

```bash
claude --plugin-dir ./plugins/empirical-analysis-python
```

---

## 3. Zero install — let the Stanford methodology team run it

If you'd rather skip assembly entirely, [**CoPaper.AI**](https://copaper.ai) runs the full
empirical pipeline end-to-end (data → causal models → robustness → publication-quality
tables) with the same methodology these skills encode.

---

## Which method should I use?

| You want to… | Use |
|--------------|-----|
| Install a maintained, versioned skill stack and get updates | **Method 1** (marketplace) |
| Grab one specific skill from the catalog and tweak it | **Method 2** (copy into `.claude/skills/`) |
| Try a skill for one session without installing | **Method 2** (`--plugin-dir`) |
| Get the result without installing anything | **Method 3** (CoPaper.AI) |

---

## Troubleshooting

- **`/plugin` command not found** — your Claude Code is too old. Upgrade to v2.1+.
- **Skill doesn't fire** — skills are model-invoked from their `description`. Name the
  method explicitly ("run a Callaway–Sant'Anna event study") or check the skill is loaded
  with `claude plugin list` / `/reload-plugins`.
- **Marketplace add failed** — confirm the repo slug is exact:
  `brycewang-stanford/Auto-Empirical-Research-Skills`. You can also add from a local clone:
  `claude plugin marketplace add /path/to/Auto-Empirical-Research-Skills`.

For the full plugin/skill model, see the
[Claude Code plugin docs](https://code.claude.com/docs/en/plugins).
