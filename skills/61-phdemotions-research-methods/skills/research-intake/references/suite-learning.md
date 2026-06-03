# Suite Learning Rubric — Inward Review

> For each category: does the researcher's project reveal something our skill suite should learn?
> Findings are saved as proposals, not auto-applied. The researcher approves changes.

---

## 1. New Methods

Does the researcher use analytical methods that our skills don't currently cover?

### Methods to watch for:
- **Conjoint analysis** — common in marketing for preference measurement
- **Choice modeling** (discrete choice, MaxDiff) — consumer decision research
- **Experience sampling / diary studies** — intensive longitudinal data
- **Text analysis / NLP** — sentiment analysis, topic modeling on open-ended responses
- **Network analysis** — social networks, citation networks, organizational networks
- **Qualitative coding** — for mixed-methods studies
- **Survival / event history analysis** — time-to-event in organizational research
- **Propensity score matching** — causal inference from observational data
- **Difference-in-differences** — quasi-experimental designs
- **Regression discontinuity** — quasi-experimental designs
- **Instrumental variables** — endogeneity correction
- **Machine learning** beyond basic classification — ensemble methods, deep learning for prediction
- **Bayesian methods** (currently on our roadmap but not yet implemented)
- **Item Response Theory (IRT)** — psychometric modeling
- **Latent class / profile analysis** — person-centered approaches
- **Multilevel SEM** — combining SEM with multilevel structure
- **Dynamic panel models** (Arellano-Bond, etc.) — for panel data with lagged DVs

### What to capture:
- Which method was used
- Which R/Python packages were employed
- Whether our current skills could handle this with modification or need a new skill entirely
- How common this method is in the researcher's target journals

---

## 2. New Packages / Tools

Does the researcher use packages or tools not in our FRAMEWORKS.md?

### What to look for:
- Packages in their `renv.lock`, `uv.lock`, `requirements.txt`, or library() calls that we don't recommend
- Are these packages better than our current recommendations? More widely adopted?
- Are these packages specific to their domain (e.g., `psych` for scale analysis, `ltm` for IRT)?
- New versions of packages we do recommend that add capabilities we should document

### What to capture:
- Package name and version
- What it does and why the researcher chose it
- Whether it should replace, supplement, or be noted alongside our current recommendation
- Which FRAMEWORKS.md section would be affected

---

## 3. New Documentation Patterns

Does the researcher have documentation patterns we should adopt?

### What to look for:
- Codebook format that's more detailed or better structured than our template
- Decision log entries with additional useful fields
- README structure that covers things our Cornell template doesn't
- Data provenance documentation that's more thorough
- Supplementary materials organization that's worth emulating
- Lab notebook or research diary practices
- Version control conventions for data files

### What to capture:
- What the pattern is
- Why it's better than or complementary to what we have
- Which template or reference file should be updated

---

## 4. New Domain Conventions

Does the researcher's work reveal field-specific conventions we haven't documented?

### What to look for:
- Journal-specific formatting requirements not in our APA overrides
- Field-specific reporting conventions (e.g., how consumer psychology reports mediation differently from management)
- Citation conventions for specific methods papers (e.g., the expected Hayes citation format for PROCESS)
- Scale citation conventions (e.g., citing the original validation paper for established scales)
- Reviewer expectations at specific journals that we haven't documented
- Conference presentation norms that affect how results are formatted

### What to capture:
- The convention
- Which journal(s) or sub-field it applies to
- Which skill or reference file should be updated

---

## 5. New Workflow Patterns

Does the researcher's workflow reveal efficiency patterns we should adopt?

### What to look for:
- Ways of structuring analysis scripts that are cleaner than our templates
- Pipeline configurations that handle common edge cases
- Quality control steps we don't currently include
- Data collection protocols that would strengthen `/data-acquire`
- Collaboration patterns (multi-author workflows, code review processes)

### What to capture:
- The pattern
- Why it's an improvement
- Which skill would benefit

---

## Producing the report

For each finding:
1. **What we found:** Describe what the researcher has/does
2. **What our suite currently covers:** What we have that's related (or nothing)
3. **Proposed update:** Specific skill or reference file to modify, with concrete change
4. **Priority:** How common is this need? How many researchers would benefit?
5. **Effort:** How much work to implement? (trivial / moderate / significant / new skill needed)
