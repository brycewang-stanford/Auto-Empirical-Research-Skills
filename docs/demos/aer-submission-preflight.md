# Demo: AER Submission Preflight

This demo is a ready-to-run prompt for a manuscript that is close to AER, AER:Insights, or AEJ submission.

## Route

- Router: [`aer-workflow`](../../skills/50-brycewang-aer-skills/skills/aer-workflow/SKILL.md)
- Submission check: [`aer-submission`](../../skills/50-brycewang-aer-skills/skills/aer-submission/SKILL.md)
- Replication check: [`aer-replication`](../../skills/50-brycewang-aer-skills/skills/aer-replication/SKILL.md)
- Tables/figures check: [`aer-tables-figures`](../../skills/50-brycewang-aer-skills/skills/aer-tables-figures/SKILL.md)

## Prompt

```text
Run an AER-track submission preflight on this manuscript and replication folder. Use aer-workflow to route the work, then check topic fit, identification strength, 100-word abstract, manuscript length, exhibit quality, table/figure style, disclosure statements, cover letter, conflicts, replication README, code/data deposit structure, and whether the paper can be reproduced from a clean checkout. Return blocking issues first, then non-blocking polish items, with exact file paths and line-level edit targets where possible.
```

## Expected Output

| Section | What the agent should return |
|---|---|
| Blocking issues | Problems that should stop submission |
| Identification audit | Whether the design is defensible at top-5 economics level |
| Exhibit audit | Oversized tables, weak figures, inconsistent notes |
| Replication audit | README, data provenance, environment, commands, outputs |
| Submission packet | Cover letter, disclosures, conflicts, metadata |
| Final decision | Submit / submit after minor fixes / do not submit yet |

## Why This Demo Matters

Generic writing skills can polish prose, but AER-track submission fails on specific constraints: identification credibility, exhibit economy, strict abstract length, disclosure requirements, and AEA replication expectations. This route keeps those constraints explicit.
