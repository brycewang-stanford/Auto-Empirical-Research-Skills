<!-- Vendored into AERS from https://github.com/phdemotions/research-methods on 2026-06-01. Upstream attribution + license preserved. -->

> **Vendored upstream skill.** Curated snapshot of [`phdemotions/research-methods`](https://github.com/phdemotions/research-methods) for the AERS catalog (license: MIT). Vendored 2026-06-01. The original upstream README follows verbatim.

---

# research-methods

Gold-standard Claude Code skills for reproducible quantitative research in R and Python.

Built for business, marketing, consumer behavior, management, and organizational behavior researchers. Designed so a senior faculty member at a top business school would be proud to put their name on the code.

## Install

**Plugin (recommended):**

```
/plugin marketplace add phdemotions/research-methods
/plugin install research-methods@phdemotions-research-methods
```

Skills are available as `/research-methods:skill-name` in any project. Hooks activate automatically. Auto-updates on version bump.

**Quick start (no plugin system):**

```bash
git clone https://github.com/phdemotions/research-methods ~/tools/research-methods
claude --add-dir ~/tools/research-methods
```

Skills load automatically. Hooks do not load via `--add-dir` — use the plugin method for full functionality.

**Direct use (contributors):**

```bash
git clone https://github.com/phdemotions/research-methods
cd research-methods
claude
```

Everything loads natively when working inside the repo.

## Skills

### The Workflow

| Skill | What it does |
|-------|-------------|
| `/research-intake` | **Start here.** Reviews your materials, identifies gaps, suggests what to do first |
| `/research-init` | Scaffolds a project with full reproducibility infrastructure (targets/Snakemake, renv/uv, decision log, pre-registration) |
| `/data-validate` | Checks data quality — completeness, ranges, duplicates, attention checks — and generates a codebook |
| `/data-clean` | Produces cleaning scripts that log every transformation with CONSORT-style exclusion flow |
| `/data-profile` | Manuscript-ready data documentation: demographics table, scale reliability (alpha, omega, CFA), comprehensive codebook |
| `/eda` | Table 1, correlation matrix, distributions, assumption pre-checks — all publication-quality |
| `/analyze` | Confirmatory analysis matched to your pre-registration. Supports OLS/GLM, panel FE (fixest), mixed models (lme4), SEM (lavaan), meta-analysis (metafor) |
| `/process-model` | Hayes PROCESS models as transparent lavaan code. Bootstrap CIs, index of moderated mediation, Johnson-Neyman plots |
| `/visualize` | APA 7th figures: interaction plots, path diagrams, forest plots, marginal effects, J-N plots. Colorblind-safe, multi-format export |

### Coming Soon

| Skill | What it does |
|-------|-------------|
| `/report` | Manuscript-ready APA results paragraphs and tables |
| `/robustness` | Specification curves, alternative estimators, sensitivity analysis |
| `/reproduce` | OSF/repository packaging with FAIR compliance |
| `/research-review` | Methods code review from a senior methodologist's perspective |
| `/pre-submit` | JARS compliance, journal-specific pre-submission checklist |
| `/research-zeitgeist` | Date-aware scan of current best practices — the self-improvement engine |
| `/method-advisor` | "What test should I use?" with citations, assumptions, and code skeletons |

### Hooks (automatic)

- **raw-data-guard** — Blocks any attempt to modify files in `data/raw/`. Raw data is sacred.
- **prereg-drift-check** — Advises when analysis code changes and a pre-registration exists. Reminds you to check alignment.

## Three Principles

1. **Raw data is sacred.** Never modified, only read. Cleaning writes to `data/processed/`.
2. **One command reproduces everything.** `tar_make()` (R) or `snakemake` (Python).
3. **Every subjective decision is documented.** Exclusion criteria, outlier handling, model choices — all in the decision log.

## Framework Stack

**R:** targets + renv + tidyverse + pointblank + ggplot2 + gtsummary + modelsummary + easystats + fixest + lavaan + bruceR + metafor + Quarto

**Python:** Snakemake + uv + polars + pandera + plotnine + great_tables + statsmodels + pingouin + Quarto

Every framework choice was verified against current best practices. See [docs/FRAMEWORKS.md](docs/FRAMEWORKS.md) for the full rationale.

## Date-Aware

Skills like `/data-profile` and `/research-zeitgeist` check current reporting standards (JARS, TOP, journal guidelines) via web search before generating output. Recommendations stay current regardless of when you run them.

## IDE

Built with [Positron](https://positron.posit.co/). Compatible with VS Code, JetBrains, or any IDE supporting Claude Code.

## Typical Workflow

```
/research-intake     → Review what you have, identify gaps
/research-init       → Scaffold project structure
/data-validate       → Check data quality, generate codebook
/data-clean          → Clean with documented exclusions
/data-profile        → Demographics, scales, reliability for Methods section
/eda                 → Descriptive stats, correlations, assumptions
/analyze             → Hypothesis testing matched to pre-registration
/process-model       → Mediation/moderation if applicable
/visualize           → Publication figures
```

## For Research Labs

Add the marketplace to your lab's shared settings so all members have access:

```json
// .claude/settings.json (shared across the lab)
{
  "extraKnownMarketplaces": ["phdemotions/research-methods"]
}
```

Then each lab member runs:
```
/plugin install research-methods@phdemotions-research-methods
```

## Version

Pin a specific version in your project if reproducibility matters:
```
/plugin install research-methods@phdemotions-research-methods --version 0.2.0
```

## License

MIT

## Contributing

Issues and PRs welcome at [github.com/phdemotions/research-methods](https://github.com/phdemotions/research-methods).
