# Auto-Chaining — Next Steps Rules

> Every skill prints a "Next steps" suggestion at the end of its run.
> These are suggestions, never automatic dispatches. The researcher is always in control.

## Chaining rules

| After this skill... | Suggest... | Condition |
|---------------------|-----------|-----------|
| `/research-intake` | `/research-init` | If project not scaffolded yet |
| `/research-intake` | `/data-validate` | If project exists but no codebook |
| `/research-intake` | `/data-clean` | If codebook exists but no cleaning docs |
| `/research-intake` | `/analyze` | If cleaned data exists, continue from there |
| `/research-init` | `/data-validate` | If data exists in `data/raw/` |
| `/data-validate` | `/data-clean` | If validation found issues to address |
| `/data-clean` | `/data-profile` | Always (manuscript-ready documentation) |
| `/data-clean` | `/eda` | Always |
| `/data-profile` | `/eda` | If EDA not yet done |
| `/data-profile` | `/report` | If writing the manuscript |
| `/eda` | `/analyze` | Always |
| `/analyze` | `/robustness` | If primary results are significant |
| `/analyze` | `/research-audit --quick` | If this is a milestone |
| `/robustness` | `/visualize` | Always |
| `/visualize` | `/report` | Always |
| `/report` | `/pre-submit` | If targeting a specific journal |
| `/report` | `/reproduce` | If preparing for OSF |
| `/reproduce` | `/research-audit --full` | Before public sharing |
| `/research-zeitgeist` | Skill updates | If new best practices found |
| `/research-feedback` | Skill updates | When researcher provides input |

## How to present next steps

At the end of every skill run, print a short block:

```
---
**Next steps:**
- `/data-clean` — Your validation found 47 failed attention checks and 12 impossible values. Clean these with documented exclusion criteria.
- `/eda` — Once cleaned, run exploratory analysis to understand distributions and correlations.
```

Rules:
1. **Always contextualize.** Don't just say "run /eda" — say why, based on what was just found.
2. **Max 2-3 suggestions.** Don't overwhelm.
3. **Most urgent first.** If there are blockers, the next step is fixing them.
4. **Note the current pipeline state.** "Your project is at: data validated, not yet cleaned."
