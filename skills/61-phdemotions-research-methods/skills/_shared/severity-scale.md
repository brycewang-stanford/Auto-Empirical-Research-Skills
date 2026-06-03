# Severity Scale for Research Review Skills

> Used by /research-review, /pre-submit, and /reproduce-check.
> Calibrated to research context: "would this cause a desk rejection or a retraction?"

## Severity Levels

### BLOCKER — Would cause rejection or retraction
- Wrong statistical test for the data/design
- No assumption testing before parametric tests
- Missing effect sizes for primary analyses
- Raw data modified in place (no audit trail)
- Results cannot be reproduced from code
- P-hacking indicators (e.g., sequential testing without correction)
- Undisclosed deviations from pre-registration

### MAJOR — Would draw reviewer criticism, likely R&R condition
- Missing confidence intervals
- Incomplete reporting (e.g., only significant results shown)
- No robustness checks for primary findings
- Codebook incomplete or missing
- No session info / environment documentation
- Exclusion criteria not documented with counts
- Scale reliability not reported

### MINOR — Should be fixed, reviewer might notice
- Inconsistent decimal places in tables
- Figures not colorblind-safe
- Variable names in output instead of construct labels
- Missing exact p-values (using stars only)
- Redundant analyses without clear purpose
- Minor APA formatting errors

### POLISH — Nice to have, differentiates excellent from good
- No CONSORT-style flow diagram for exclusions
- Decision log entries could be more detailed
- Figures could be more elegant
- Code comments could be more informative
- README could be more thorough
