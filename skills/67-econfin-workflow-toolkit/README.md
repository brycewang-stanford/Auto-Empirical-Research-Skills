# Econ/Finance Workflow Toolkit

An end-to-end toolkit for empirical economics and finance research, covering the
full arc from idea generation and study design, through data work and
econometric estimation, to paper writing, internal review, and journal
submission. The skills are designed to compose: high-level orchestrators such as
`paper-pipeline` invoke the individual writing and review skills in a fixed
order.

## What Is Included

| Area | Skills |
|---|---|
| Ideation & design | [`econfin-idea-finder`](econfin-idea-finder/SKILL.md), [`econfin-proposal`](econfin-proposal/SKILL.md), [`novelty-check`](novelty-check/SKILL.md), [`significance-search`](significance-search/SKILL.md), [`journal-digest`](journal-digest/SKILL.md), [`master-thesis-review`](master-thesis-review/SKILL.md) |
| Data | [`data-fetcher`](data-fetcher/SKILL.md), [`data-cleaning`](data-cleaning/SKILL.md) |
| Econometric estimation | [`ols-regression`](ols-regression/SKILL.md), [`panel-data`](panel-data/SKILL.md), [`iv-estimation`](iv-estimation/SKILL.md), [`did-analysis`](did-analysis/SKILL.md), [`rdd-analysis`](rdd-analysis/SKILL.md), [`synthetic-control`](synthetic-control/SKILL.md), [`time-series`](time-series/SKILL.md), [`ml-causal`](ml-causal/SKILL.md), [`stata`](stata/SKILL.md), [`stats`](stats/SKILL.md) |
| Tables & figures | [`table`](table/SKILL.md), [`figure`](figure/SKILL.md) |
| Writing & polishing | [`paper-writer`](paper-writer/SKILL.md), [`paper-style`](paper-style/SKILL.md), [`paper-polish`](paper-polish/SKILL.md), [`paper-self-revise`](paper-self-revise/SKILL.md), [`paper-pipeline`](paper-pipeline/SKILL.md), [`readability`](readability/SKILL.md) |
| Review & references | [`referee-report`](referee-report/SKILL.md), [`paper-referee-revise`](paper-referee-revise/SKILL.md), [`reference-verify`](reference-verify/SKILL.md) |
| Submission | [`paper-submission`](paper-submission/SKILL.md) |
| Study templates | [`China-CF-study`](China-CF-study/SKILL.md), [`Foreign-CF-study`](Foreign-CF-study/SKILL.md) |
| Chinese writing | [`fix-chinese`](fix-chinese/SKILL.md), [`chinese-quote-converter`](chinese-quote-converter/SKILL.md) |
| Slides & conversion | [`marp-slides-creator`](marp-slides-creator/SKILL.md), [`marp-export`](marp-export/SKILL.md), [`chinese-ppt`](chinese-ppt/SKILL.md), [`md-to-docx`](md-to-docx/SKILL.md), [`markitdown`](markitdown/SKILL.md) |
| Web & search | [`web-research`](web-research/SKILL.md), [`web-access`](web-access/SKILL.md), [`arxiv`](arxiv/SKILL.md), [`agent-browser`](agent-browser/SKILL.md) |
| Authoring & automation | [`skill-creator`](skill-creator/SKILL.md), [`command-development`](command-development/SKILL.md), [`do-agent`](do-agent/SKILL.md) |

## Suggested Flow

1. `econfin-idea-finder` → `econfin-proposal` to scope a question and design the study.
2. `data-fetcher` → `data-cleaning` to assemble the working dataset.
3. Pick the estimator that matches the design (`ols-regression`, `panel-data`,
   `iv-estimation`, `did-analysis`, `rdd-analysis`, `synthetic-control`,
   `time-series`, `ml-causal`), reporting with `table` and `figure`.
4. `paper-writer` for the draft, then `paper-pipeline` to run the full
   polish → self-revise → style → polish → reference-verify sequence.
5. `referee-report` / `paper-referee-revise` for review rounds, then
   `paper-submission` for the target journal.

## Licensing Notes

This is a mixed-origin collection; check each skill folder and its upstream
project before redistribution or commercial reuse. This vendored copy
intentionally omits the proprietary Anthropic document-office skills
(`docx`/`pdf`/`pptx`/`xlsx`) and the general-purpose UI design skills
(`frontend-design`, `ui-ux-pro-max`) that the upstream toolkit bundled; install
those from their authorized source instead of copying them into this repository.
