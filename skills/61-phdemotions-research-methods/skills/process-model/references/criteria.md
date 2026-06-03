# PROCESS Model Checklist

> For every PROCESS model: specify transparently, bootstrap properly, report fully.

---

## 1. Model Specification

### 1.1 Variable identification
- [ ] X (IV) clearly identified
- [ ] Y (DV) clearly identified
- [ ] M (mediator(s)) clearly identified (if mediation)
- [ ] W (moderator(s)) clearly identified (if moderation)
- [ ] Covariates listed
- [ ] Model number confirmed with researcher

### 1.2 Centering
- [ ] Continuous moderators mean-centered
- [ ] Centering documented in decision log
- [ ] IV and mediator NOT centered (unless specifically justified)

### 1.3 lavaan syntax
- [ ] Full model written as explicit lavaan syntax
- [ ] All paths labeled (a, b, c_prime, etc.)
- [ ] Indirect effects defined with `:=` operator
- [ ] Syntax is readable and commented

---

## 2. Estimation

### 2.1 Bootstrap
- [ ] Bootstrap CIs used for indirect effects (not Sobel test)
- [ ] Minimum 5,000 bootstrap draws (10,000 for publication)
- [ ] BCa (bias-corrected accelerated) CI method preferred
- [ ] Seed set for reproducibility

### 2.2 Estimator
- [ ] MLR if non-normality detected (Mardia's test)
- [ ] ML otherwise
- [ ] For ordinal mediators or DVs: WLSMV

### 2.3 Verification
- [ ] Same model run through bruceR::PROCESS() for verification
- [ ] Estimates match within rounding tolerance
- [ ] Discrepancies investigated and documented

---

## 3. Reporting — Mediation (Models 4, 6, 80, 81, etc.)

### 3.1 Path coefficients
- [ ] a path (X → M): b, SE, t, p, 95% CI
- [ ] b path (M → Y): b, SE, t, p, 95% CI
- [ ] c' path (direct: X → Y): b, SE, t, p, 95% CI
- [ ] c path (total: X → Y): b, SE, t, p, 95% CI
- [ ] For serial mediation: each a and b path separately

### 3.2 Indirect effects
- [ ] Indirect effect: b, BootSE, 95% bootstrap CI
- [ ] CI interpretation: excludes zero = significant
- [ ] For multiple mediators: specific indirect effects + contrasts
- [ ] Proportion mediated (if total effect is significant)

### 3.3 Effect sizes
- [ ] Standardized indirect effect (or partially standardized: a×b in SD units of Y)
- [ ] R² for each equation (M equation, Y equation)
- [ ] kappa-squared or R²_mediated if requested

---

## 4. Reporting — Moderation (Models 1, 2, 3)

### 4.1 Interaction
- [ ] Interaction term: b, SE, t, p, 95% CI
- [ ] ΔR² for the interaction term
- [ ] F-test for interaction significance

### 4.2 Simple slopes
- [ ] Effect of X on Y at W = -1 SD: b, SE, t, p, CI
- [ ] Effect of X on Y at W = mean: b, SE, t, p, CI
- [ ] Effect of X on Y at W = +1 SD: b, SE, t, p, CI

### 4.3 Johnson-Neyman
- [ ] Transition point(s) where effect becomes (non)significant
- [ ] Percentage of sample above/below transition point
- [ ] J-N plot with significance region shaded

### 4.4 Visualization
- [ ] Interaction plot: Y by X at W levels (±1 SD + mean)
- [ ] Error bars or bands (95% CI)
- [ ] APA formatted

---

## 5. Reporting — Moderated Mediation (Models 7, 8, 14, 15, etc.)

### 5.1 All paths (as in mediation)
- [ ] a, b, c', indirect, total paths

### 5.2 Conditional indirect effects
- [ ] Indirect effect at W = -1 SD: b, BootSE, 95% bootstrap CI
- [ ] Indirect effect at W = mean: b, BootSE, 95% bootstrap CI
- [ ] Indirect effect at W = +1 SD: b, BootSE, 95% bootstrap CI

### 5.3 Index of moderated mediation
- [ ] Index value, BootSE, 95% bootstrap CI
- [ ] Interpretation: CI excludes zero → indirect effect depends on moderator

### 5.4 Visualization
- [ ] Conditional indirect effect plot across moderator range
- [ ] J-N regions for the indirect effect (if applicable)
- [ ] Path diagram with all coefficients

---

## 6. Output Artifacts

- `output/tables/process-results.html` + `.docx` — PROCESS-style results tables
- `output/figures/path-diagram.png` — path diagram with coefficients
- `output/figures/interaction-plot.png` — interaction visualization (if moderation)
- `output/figures/jn-plot.png` — Johnson-Neyman plot (if moderation)
- `output/results/process-fit.rds` (R) or `.pkl` (Python) — fitted model objects
- `docs/decisions/process-decisions.md` — any deviations from pre-registration
