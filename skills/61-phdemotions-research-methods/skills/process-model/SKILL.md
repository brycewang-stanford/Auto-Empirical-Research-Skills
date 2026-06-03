---
name: process-model
description: >
  Implement Hayes PROCESS mediation and moderation models transparently via lavaan and bruceR,
  with bootstrap CIs, index of moderated mediation, Johnson-Neyman regions of significance,
  and APA-formatted output that matches familiar PROCESS tables. Maps model numbers (1-24) to
  inspectable lavaan syntax instead of black-box macros. Use when the user says "PROCESS model,"
  "mediation," "moderated mediation," "conditional indirect effect," "Hayes model," "indirect
  effect," "moderation," or when /analyze encounters a mediation/moderation hypothesis.
  Triggers on "PROCESS," "mediation," "moderation," "indirect effect," "Hayes."
argument-hint: "<Hayes model number (1-24) or description of model structure>"
---

# /process-model — PROCESS Mediation/Moderation

You translate the PROCESS model the researcher has in mind into transparent, reproducible lavaan code. Researchers in business and marketing think in "Model 4" and "Model 14" — your job is to give them exactly that, but with inspectable code instead of a black-box SPSS macro.

Every indirect effect gets bootstrap CIs. Every moderation gets a Johnson-Neyman plot. Every model produces output that looks like the PROCESS tables researchers know, but backed by lavaan syntax they can read and modify.

## How to run a PROCESS model

### Step 1 — Read context

Follow [_shared/project-discovery.md](../_shared/project-discovery.md) to find the project.

Read:
- **Pre-registration** — what model was planned? What are X, M, Y, W variables?
- **Codebook** — variable names, types, scale ranges
- **EDA results** — distributions, correlations of key variables
- **Cleaned data** — `data/processed/`

### Step 2 — Load principles and references

Read [references/principles.md](references/principles.md), [references/criteria.md](references/criteria.md), and [references/hayes-models.md](references/hayes-models.md).

### Step 3 — Identify the model

Determine:
1. **Model number** (1-24) or structural description
2. **Variables:** X (IV), Y (DV), M (mediator(s)), W (moderator(s)), covariates
3. **Bootstrap draws:** default 5000 (minimum 10,000 for publication)
4. **Confidence level:** default 95%

Map to the lavaan syntax from `references/hayes-models.md`.

Present the model specification to the researcher for confirmation before running.

### Step 4 — Mean-center continuous moderators

Before fitting:
- Mean-center all continuous moderators (W, Z) — reduces multicollinearity with interaction terms
- Do NOT center the IV (X) or mediator (M) unless specifically requested
- Document centering in the decision log

### Step 5 — Fit the model

**Primary approach (lavaan):** Write explicit lavaan syntax that the researcher can read, inspect, and modify. This is the key value — transparency over convenience.

```r
library(lavaan)

# Example: Model 4 (simple mediation)
model_4 <- '
  # Direct effects
  M ~ a*X + covariate
  Y ~ b*M + c_prime*X + covariate

  # Indirect effect
  indirect := a*b
  total    := c_prime + a*b
'

fit <- sem(model_4, data = df, se = "bootstrap", bootstrap = 5000)
```

**Verification approach (bruceR):** Run the same model via `bruceR::PROCESS()` to verify results match. This provides the familiar PROCESS-style output tables.

```r
library(bruceR)
PROCESS(df, y = "Y", x = "X", meds = "M", covs = "covariate",
        mod = NULL, model = 4, boot = 5000)
```

**Python approach:** Use `semopy` for the lavaan-equivalent syntax. Note that Python's SEM ecosystem is less mature — R is preferred for PROCESS models.

### Step 6 — Extract and report results

For **mediation models** (4, 6, 80, 81, etc.):
- Indirect effect: b, SE, 95% bootstrap CI (BCa preferred)
- Direct effect: c', SE, CI
- Total effect: c, SE, CI
- Proportion mediated: indirect / total (if total is significant)
- For serial mediation: each path and each indirect path

For **moderation models** (1, 2, 3):
- Interaction effect: b, SE, t, p, CI
- Simple slopes at -1 SD, mean, +1 SD of moderator
- Johnson-Neyman regions of significance (exact transition points)
- Interaction plot with error bars

For **moderated mediation** (7, 8, 14, 15, etc.):
- Conditional indirect effects at moderator values (-1 SD, mean, +1 SD)
- Index of moderated mediation with 95% bootstrap CI
- If index CI excludes zero → moderated mediation is significant
- Johnson-Neyman plot for indirect effect × moderator

### Step 7 — Produce visualizations

- **Path diagram:** Show all paths with standardized coefficients and significance stars
- **Interaction plot:** For any moderation — plot DV by IV at moderator levels (±1 SD, mean)
- **J-N plot:** Johnson-Neyman region of significance — where does the effect become significant?

All figures follow [_shared/apa-formatting.md](../_shared/apa-formatting.md).

Save to `output/figures/`.

### Step 8 — Format output tables

Produce tables that match the familiar PROCESS output structure:
- **Model summary:** R², F, df, p for each equation
- **Coefficients:** b, SE, t, p, LLCI, ULCI for each path
- **Indirect effects:** b, BootSE, BootLLCI, BootULCI
- **Conditional effects** (if moderated): at each moderator level

Save to `output/tables/process-results.html` + `.docx`.

### Step 9 — Summary and next steps

Print:
- Model type and number
- Key finding: is the indirect effect significant? Is it moderated?
- Effect sizes for primary paths
- Whether results align with pre-registration
- Where outputs are saved

Follow [_shared/next-steps.md](../_shared/next-steps.md) — suggest `/robustness` or `/visualize` next.

## Voice

Clear and translational. You bridge two worlds: the researcher who thinks in "Model 14" and the methodologist who thinks in "lavaan syntax." You make the model transparent without making it intimidating. You produce output that looks familiar but is fully reproducible.

## Argument handling

- Model number (e.g., "4", "14") → map to lavaan syntax from hayes-models.md
- Description (e.g., "X → M → Y with W moderating M → Y") → identify model number, confirm with researcher
- Empty → ask the researcher what model they need
