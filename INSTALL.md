# Installation & Quick Start

There are four ways to use the skills in this collection, from "one command" to
"zero install". Pick the one that matches how you work.

> **Requirements for the plugin path:** [Claude Code](https://code.claude.com/docs)
> **v2.1+** (the `/plugin` marketplace commands). Run `claude --version` to check, and
> `claude` itself to upgrade if `/plugin` is missing.

> **Cloning the repo?** `skills/69-Paper-WorkFlow/` is a **git submodule**. Clone with
> `git clone --recurse-submodules`, or run `git submodule update --init` inside an
> existing clone — otherwise that folder is empty and `make validate` fails.

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
> use method 3 below.

---

## 2. Whole-repo import — Codex, CodeBuddy, and IDE skill folders

Some IDEs ask you to pick a folder and validate it as one skill. This repo now
supports that path with the root [`SKILL.md`](SKILL.md): importing the repository
root registers **one lightweight AERS catalog router**, not 1,150 separate child
skills. The router chooses the right vendored skill and then reads only that
child skill's `SKILL.md`.

For local Codex-style discovery:

```bash
# Run from the repository root.
mkdir -p ~/.codex/skills/auto-empirical-research-skills
rsync -a --exclude .git --exclude .pytest_cache --exclude __pycache__ --exclude '*.pyc' \
  ./ ~/.codex/skills/auto-empirical-research-skills/
```

If your IDE has a GitHub import flow, select the repository root and name the
skill `auto-empirical-research-skills`. If it asks for a path, use `.`.

Use this mode when you want a browse-and-route entry point. If you want the IDE
to register one specific skill directly, use method 3 and copy the exact folder
that contains that skill's `SKILL.md`.

---

## 3. Use any skill in the catalog — copy into a runtime skills folder

Every entry in this catalog is a folder containing a `SKILL.md`. To use one, copy that
folder into your project's (or your global) skills directory — no marketplace needed.

```bash
# Project-scoped (only this repo/project sees it)
mkdir -p .claude/skills
cp -R skills/00.1-Full-empirical-analysis-skill_Python  .claude/skills/empirical-python

# Or global (every project sees it)
cp -R skills/00.1-Full-empirical-analysis-skill_Python  ~/.claude/skills/empirical-python

# Codex global skill folder
mkdir -p ~/.codex/skills
cp -R skills/00.1-Full-empirical-analysis-skill_Python  ~/.codex/skills/empirical-python
```

The folder you copy must contain a `SKILL.md` at its top level (some catalog skills nest
theirs under `skills/<name>/SKILL.md` — copy the folder that holds the `SKILL.md`). Start
a new Claude Code session and the skill auto-loads; Claude invokes it when your request
matches its `description`.

> **Copy a handful, not the whole catalog.** Every installed skill's `description` is
> loaded into context at the start of every session. All 1,096 would cost about 64k tokens
> up front, and runtimes truncate long skill listings — so Claude would match requests
> *less* reliably, not more. For breadth, use the plugins (method 1) or the one-skill root
> router (method 2), which reads a single child skill on demand. To find the right folder
> to copy: `python3 scripts/find-skill.py "your task"`.

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

## 4. Zero install — let the Stanford methodology team run it

If you'd rather skip assembly entirely, [**CoPaper.AI**](https://copaper.ai) runs the full
empirical pipeline end-to-end (data → causal models → robustness → publication-quality
tables) with the same methodology these skills encode.

## 5. Score your own agent — the `aers-score` CLI

Not installing skills at all, but bringing your own agent and wanting to know
how it does? The repo's numeric benchmark is a shared exam — deterministic
datasets with known truth, and graders that recompute every gold from the
committed CSV so fabricated numbers fail by construction.

```bash
git clone https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills
cd Auto-Empirical-Research-Skills
pip install -e .                      # zero dependencies, Python 3.9+

aers-score tasks                      # what is on the exam
aers-score describe rdd-recovery      # what one task grades, and its trap
aers-score init ./my-run              # scaffold candidates with the right fields
#   ... run your agent over each task's dataset, fill in the numbers ...
aers-score grade ./my-run             # score yourself
```

Publishing the result on the public board takes one more command
(`aers-score submit`). Full guide: [`aers_score/README.md`](aers_score/README.md);
rules and ranking: [`docs/SCOREBOARD_RULES.md`](docs/SCOREBOARD_RULES.md); the
board itself: [`docs/EXTERNAL_SCOREBOARD.md`](docs/EXTERNAL_SCOREBOARD.md).

---

## Which method should I use?

| You want to… | Use |
|--------------|-----|
| Install a maintained, versioned skill stack and get updates | **Method 1** (marketplace) |
| Import the whole repo into Codex, CodeBuddy, or another IDE | **Method 2** (root router skill) |
| Grab one specific skill from the catalog and tweak it | **Method 3** (copy into `.claude/skills/` or `.codex/skills/`) |
| Try a skill for one session without installing | **Method 3** (`--plugin-dir`) |
| Get the result without installing anything | **Method 4** (CoPaper.AI) |
| Benchmark your own agent against this repo's exam | **Method 5** (`aers-score`) |

---

## Troubleshooting

- **`/plugin` command not found** — your Claude Code is too old. Upgrade to v2.1+.
- **Skill doesn't fire** — skills are model-invoked from their `description`. Name the
  method explicitly ("run a Callaway–Sant'Anna event study") or check the skill is loaded
  with `claude plugin list` / `/reload-plugins`.
- **Marketplace add failed** — confirm the repo slug is exact:
  `brycewang-stanford/Auto-Empirical-Research-Skills`. You can also add from a local clone:
  `claude plugin marketplace add /path/to/Auto-Empirical-Research-Skills`.
- **`skills/69-Paper-WorkFlow/` is empty / `make validate` fails on it** — the
  clone skipped submodules. Run `git submodule update --init` from the repo root,
  or `make setup` to bootstrap submodules and the scientific stack in one go.
- **`make validate` says `RIGOR.md is STALE` and regenerating does not help** —
  that gate executes a notebook and needs numpy/pandas/matplotlib/statsmodels.
  Run `make doctor` for a one-screen diagnosis, then `make setup`.
- **`aers-score` cannot find the exam** — it needs an AERS checkout. Set
  `export AERS_REPO=/path/to/Auto-Empirical-Research-Skills`, pass `--repo PATH`,
  or run from inside the checkout. `aers-score where` shows what it resolved.
- **Whole-repo import failed in Codex / CodeBuddy** — import the repository root
  as `auto-empirical-research-skills` so the root `SKILL.md` is the selected
  skill folder. Do not point a single-skill importer at `skills/` itself.
- **Expected every child skill to appear separately** — most runtimes do not
  recursively register nested skills from a repository root. Copy the specific
  child folder that directly contains the `SKILL.md`, or use the Claude Code
  marketplace plugins in method 1.

For the full plugin/skill model, see the
[Claude Code plugin docs](https://code.claude.com/docs/en/plugins).
