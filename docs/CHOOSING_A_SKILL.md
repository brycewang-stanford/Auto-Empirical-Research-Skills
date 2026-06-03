# Which skill should I use?

1,052 skills is a lot. This guide routes you to the right one by **what you are
trying to do**, then by **method** and **language**. For interactive filtering
use [`search.html`](search.html); for the full tag index see
[`TAXONOMY.md`](TAXONOMY.md); for copy-paste end-to-end runs see
[`GOLDEN_WORKFLOWS.md`](GOLDEN_WORKFLOWS.md).

> Trust note: a green hygiene score in [`SKILL_QUALITY.md`](SKILL_QUALITY.md)
> means a skill is *well-formed*. Whether it makes an agent produce *correct*
> econometrics is what [`eval-harness/`](../eval-harness/) and [`benchmark/`](../benchmark/)
> measure. Prefer skills whose behavior is covered by an eval scenario.

## Start from your goal

| I want to… | Use | Notes |
|---|---|---|
| Run a full empirical pipeline in **Python** | [`StatsPAI`](../skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md) or [`00.1 Python`](../skills/00.1-Full-empirical-analysis-skill_Python/SKILL.md) | data → identification → estimation → robustness → tables/figures |
| Run the same pipeline in **Stata** / **R** | [`00.2 Stata`](../skills/00.2-Full-empirical-analysis-skill_Stata/SKILL.md) · [`00.3 R`](../skills/00.3-Full-empirical-analysis-skill_R/SKILL.md) | language-matched ports of the pipeline |
| **Audit my identification** before writing | [`aer-identification`](../skills/50-brycewang-aer-skills/skills/aer-identification/SKILL.md) | gates TWFE behind the 2×2 conditions; weak-IV / RDD pitfalls |
| Build the **robustness** gauntlet referees expect | [`aer-robustness`](../skills/50-brycewang-aer-skills/skills/aer-robustness/SKILL.md) | placebo triplet, spec curve, heterogeneity by theory |
| Write the **introduction / abstract** for a top-5 | [`aer-introduction`](../skills/50-brycewang-aer-skills/skills/aer-introduction/SKILL.md) | Keith Head 5-paragraph formula; 100-word abstract |
| Format **tables & figures** to AER house style | [`aer-tables-figures`](../skills/50-brycewang-aer-skills/skills/aer-tables-figures/SKILL.md) | booktabs, figure notes, one claim per exhibit |
| **Pre-submission** compliance check | [`aer-submission`](../skills/50-brycewang-aer-skills/skills/aer-submission/SKILL.md) | abstract length, disclosure, AI usage, ScholarOne package |
| Write a **R&R / rebuttal** letter | [`aer-rebuttal`](../skills/50-brycewang-aer-skills/skills/aer-rebuttal/SKILL.md) | written against the *revised* manuscript |
| Build a **replication package** | [`aer-replication`](../skills/50-brycewang-aer-skills/skills/aer-replication/SKILL.md) | AEA Data & Code Availability Policy, openICPSR-ready |
| Get **causal-method code templates** | [`causal-inference-mixtape`](../skills/10-Jill0099-causal-inference-mixtape/SKILL.md) · [`MixtapeTools`](../skills/13-scunning1975-MixtapeTools/) | 10 designs, Python/R/Stata |
| Lower the **AI-writing signal** of a Chinese draft | [`chinese-de-aigc`](../skills/48-copaper-ai-chinese-de-aigc/SKILL.md) | structural rewrite, facts preserved |
| De-slop **English** academic prose | [`avoid-ai-writing`](../skills/47-conorbronsdon-avoid-ai-writing/SKILL.md) · [`stop-slop`](../skills/46-hardikpandya-stop-slop/SKILL.md) | |
| Run a **literature review** | [`literature-review`](../skills/36-taoyunudt-literature-review-skill/SKILL.md) | see also stage:`literature` in the taxonomy |

## Then narrow by method

Pick the design, then jump to the method tag in [`TAXONOMY.md`](TAXONOMY.md#methods):

- **Staggered diff-in-diff?** You almost never want plain TWFE. Look for
  `staggered-did` skills (Callaway–Sant'Anna, Sun–Abraham, Borusyak et al.,
  de Chaisemartin–D'Haultfœuille). Covered by the eval
  [`statspai-staggered-did`](../eval-harness/scenarios/statspai-staggered-did.toml).
- **Instrumental variables?** Check the `iv` tag; you want first-stage F
  reporting and weak-IV-robust inference. Covered by
  [`statspai-weak-iv`](../eval-harness/scenarios/statspai-weak-iv.toml).
- **Regression discontinuity?** Check `rdd`; you want a density/manipulation
  test, bandwidth sensitivity, and robust bias-corrected CIs. Covered by
  [`statspai-rdd-diagnostics`](../eval-harness/scenarios/statspai-rdd-diagnostics.toml).
- **Synthetic control / matching / DML?** Tags `synthetic-control`, `matching`,
  `dml`.

## Then narrow by language

Filter the `language` facet (`python`, `r`, `stata`, `latex`) in
[`search.html`](search.html). The 00.x pipeline skills exist in all three
analysis languages so you can match your stack.

## A 30-second decision tree

```
Do you have a dataset and need results?
├─ yes → identification first:  aer-identification
│        then run the pipeline:  00 / 00.1 / 00.2 / 00.3 (by language)
│        then robustness:        aer-robustness
└─ no, I have results and need a paper
   ├─ intro/abstract           → aer-introduction
   ├─ tables/figures           → aer-tables-figures
   ├─ submission compliance    → aer-submission
   ├─ referee response (R&R)   → aer-rebuttal
   └─ reproducibility package  → aer-replication

Polishing prose?
├─ Chinese → chinese-de-aigc
└─ English → avoid-ai-writing / stop-slop
```

## See also

- [`GOLDEN_WORKFLOWS.md`](GOLDEN_WORKFLOWS.md) — ready-to-run multi-skill workflows
- The numbered workflow-stage notes: [`01-选题与研究设计`](01-选题与研究设计.md) … [`10-审稿回复与学术答辩`](10-审稿回复与学术答辩.md)
- [`SKILL_CATALOG.md`](SKILL_CATALOG.md) — the full generated catalog
