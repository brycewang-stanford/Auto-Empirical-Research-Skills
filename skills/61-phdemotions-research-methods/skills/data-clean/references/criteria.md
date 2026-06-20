# Data Cleaning Checklist

> Run through every applicable section. Document every decision.

---

## 1. Type Corrections

- [ ] Convert character columns that should be numeric
- [ ] Parse date/time columns correctly
- [ ] Convert categorical variables to factors with meaningful levels
- [ ] Ensure ID columns are treated as identifiers, not numbers
- [ ] Fix encoding issues in text fields

## 2. Missing Value Standardization

- [ ] Identify all missing value codes (-99, 999, "N/A", "", " ", "NA", etc.)
- [ ] Convert all to proper NA/null
- [ ] Document the original coding in the decision log
- [ ] Verify conversion didn't accidentally null valid values

## 3. Exclusions (each gets N before/after + decision log entry)

### 3.1 Pre-specified exclusions (from pre-registration)
- [ ] Apply each pre-registered exclusion criterion in order
- [ ] Log N removed at each step
- [ ] If any pre-registered criterion removes 0 participants, note this (still counts as applied)

### 3.2 Attention check exclusions
- [ ] Apply attention check failure criterion
- [ ] Document threshold (e.g., "failed 2+ of 3 attention checks")
- [ ] Report failure rate before exclusion
- [ ] Decision log: which items, what threshold, why

### 3.3 Manipulation check exclusions (if applicable)
- [ ] Apply manipulation check criterion
- [ ] Document threshold
- [ ] Note: some researchers prefer to analyze with and without manipulation check failures (robustness)

### 3.4 Response quality exclusions
- [ ] Straight-liners (zero variance across scale items)
- [ ] Impossibly fast completions (threshold documented)
- [ ] Duplicate responses (same IP, same responses)
- [ ] Each criterion gets its own decision log entry

### 3.5 Demographic exclusions (if applicable)
- [ ] Age outside target range
- [ ] Not in target population
- [ ] Each criterion documented

## 4. Reverse Coding

- [ ] Identify all reverse-coded items (from codebook or scale documentation)
- [ ] Apply reverse coding: `(max + min) - value`
- [ ] Document which items were reversed and the formula used
- [ ] Verify: reversed items should now correlate positively with other scale items

## 5. Scale Composites

For each multi-item scale:

- [ ] Compute reliability BEFORE creating composite
  - Cronbach's alpha (report)
  - McDonald's omega (report if available)
  - Flag if alpha < .70 (note in decision log, researcher decides whether to proceed)
- [ ] Report item-total correlations
- [ ] Report alpha-if-item-deleted
- [ ] Create composite (mean or sum — document which and why)
- [ ] Name the composite using construct name from codebook
- [ ] Add composite to codebook with: component items, reliability, computation method

## 6. Variable Transformations

For each transformation:

- [ ] Document the transformation and why it was applied
- [ ] Prefix the new variable name: `z_` (standardized), `log_` (log), `c_` (centered), `sq_` (squared)
- [ ] Keep the original variable alongside the transformed version
- [ ] Common transformations:
  - Grand-mean centering (for interaction terms)
  - Standardizing (z-scores) for comparing across scales
  - Log transformation (for skewed distributions — document skewness before/after)
  - Winsorizing (for outliers — document percentile thresholds)

## 7. Derived Variables

- [ ] Interaction terms (if needed for analysis — often better to let the model handle this)
- [ ] Condition dummy codes (for experimental studies)
- [ ] Binned/categorized versions of continuous variables (document cutpoints and rationale)
- [ ] Each derived variable added to codebook

## 8. Final Validation

- [ ] All variables within expected ranges
- [ ] No remaining missing value codes (all converted to NA)
- [ ] No duplicate IDs
- [ ] Correct N matches expected (after exclusions)
- [ ] All composites within theoretical range
- [ ] Factor levels are clean and meaningful

---

## CONSORT-Style Exclusion Flow

Every cleaning run produces an exclusion flow. See [templates/consort-flow.md](templates/consort-flow.md).
