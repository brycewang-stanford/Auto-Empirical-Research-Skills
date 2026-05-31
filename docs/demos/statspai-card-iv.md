# Demo: StatsPAI IV Pipeline

This demo shows the flagship StatsPAI empirical-analysis skill applied to Card (1995), the canonical college-proximity instrument for returns to schooling.

## Route

- Skill: [`StatsPAI_skill`](../../skills/00-Full-empirical-analysis-skill_StatsPAI/SKILL.md)
- Demo folder: [`demo-StatsPAI-skill/`](../../demo-StatsPAI-skill/)
- Script: [`card_returns_to_schooling_pipeline.py`](../../demo-StatsPAI-skill/card_returns_to_schooling_pipeline.py)
- Notebook: [`card_returns_to_schooling_pipeline.ipynb`](../../demo-StatsPAI-skill/card_returns_to_schooling_pipeline.ipynb)

## Research Design

| Item | Value |
|---|---|
| Outcome | `lwage` |
| Treatment | `educ` |
| Instrument | `nearc4` |
| Estimand | LATE for schooling compliers shifted by college proximity |
| Main estimator | 2SLS with robust standard errors |
| Sample | NLSYM men aged 24-34 in 1976, n = 3,010 |

## Generated Artifacts

- Pre-analysis/identification: [`artifacts/empirical_strategy.md`](../../demo-StatsPAI-skill/artifacts/empirical_strategy.md)
- Data contract: [`artifacts/data_contract.json`](../../demo-StatsPAI-skill/artifacts/data_contract.json)
- Table 1: [`tables/table1_summary.tex`](../../demo-StatsPAI-skill/tables/table1_summary.tex)
- IV triplet: [`tables/table2b_iv_triplet.tex`](../../demo-StatsPAI-skill/tables/table2b_iv_triplet.tex)
- Robustness table: [`tables/tableA1_robustness.tex`](../../demo-StatsPAI-skill/tables/tableA1_robustness.tex)
- Replication bundle: [`replication/paper.md`](../../demo-StatsPAI-skill/replication/paper.md)

## Headline Result

The demo produces:

- OLS with controls: return to schooling around 7.5%.
- 2SLS using `nearc4`: return to schooling around 13.2%.
- First-stage F around 13-14.
- Robustness artifacts for Oster, E-value, specification curve, DML, and subgroup checks.

## Reproduce

```bash
cd demo-StatsPAI-skill
python3 card_returns_to_schooling_pipeline.py
```

The bundled `data/card.csv` keeps the demo self-contained.
