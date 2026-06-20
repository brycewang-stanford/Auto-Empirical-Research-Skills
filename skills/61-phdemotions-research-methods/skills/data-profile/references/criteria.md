# Data Profile Checklist

> Generate the complete manuscript-ready data package. Every section produces an artifact.

---

## 0. Best Practices Check (Run First)

### 0.1 Current standards
- [ ] Read today's date
- [ ] Web search: current APA JARS requirements for sample and measures reporting
- [ ] Web search: current TOP Guidelines version and data documentation expectations
- [ ] If target journal specified: check their current author guidelines for measures reporting
- [ ] Note any changes from known baseline (FRAMEWORKS.md) — flag if recommendations need updating

### 0.2 Date stamp
- [ ] All output includes: "Generated following best practices as of [Month Year]"
- [ ] If standards have changed since last check, note what changed

---

## 1. Scale Identification

### 1.1 Multi-item scales
- [ ] Identify all item groups by naming convention (prefix_1, prefix_2, ...)
- [ ] Cross-reference with codebook, survey instrument, or pre-registration
- [ ] For each scale: name, number of items, response format, anchors, source citation
- [ ] Identify reverse-coded items and verify they are properly handled

### 1.2 Single-item measures
- [ ] Identify standalone measures
- [ ] Document response format and anchors
- [ ] Note if single-item by design (e.g., NPS) or limitation

### 1.3 Condition variables
- [ ] Identify experimental conditions
- [ ] Document levels and coding
- [ ] Report cell sizes

---

## 2. Reliability (Per Scale)

### 2.1 Cronbach's alpha
- [ ] Computed for every multi-item scale
- [ ] Item-total correlations reported
- [ ] Alpha-if-item-deleted checked for problematic items
- [ ] Flag: alpha < .70

### 2.2 McDonald's omega
- [ ] Omega total computed (preferred over alpha)
- [ ] Omega hierarchical if scale has subfactors
- [ ] R: `psych::omega()` — also produces factor solution

### 2.3 CFA-based reliability (if N sufficient)
- [ ] Unidimensional CFA for each scale
- [ ] Factor loadings reported (flag < .40)
- [ ] Model fit: CFI, RMSEA, SRMR
- [ ] Composite reliability (CR) from CFA: `semTools::reliability()`
- [ ] AVE (Average Variance Extracted) for discriminant validity

### 2.4 Summary
- [ ] Measures summary table with all reliability indices
- [ ] Flag any scales with concerns (low reliability, poor fit, problematic items)

---

## 3. Demographics Table

### 3.1 Required variables
- [ ] Age: M (SD), range, or n (%) by category
- [ ] Gender/sex: n (%) per category
- [ ] Race/ethnicity: n (%) per category (use census categories or study-appropriate)
- [ ] Education: n (%) per level
- [ ] Additional demographics relevant to the study

### 3.2 Formatting
- [ ] APA-compliant table format
- [ ] By condition if experimental design (with overall column)
- [ ] Percentages sum to approximately 100% within each category
- [ ] Missing data reported if any demographics have missingness

### 3.3 Export
- [ ] `output/tables/demographics.html`
- [ ] `output/tables/demographics.docx`
- [ ] R: `gtsummary::tbl_summary()` with `add_overall()`
- [ ] Python: `great_tables` formatted output

---

## 4. Comprehensive Codebook

### 4.1 Per-variable fields (minimum)
- [ ] Variable name (as in data)
- [ ] Human-readable label
- [ ] Construct (theoretical concept)
- [ ] Type (continuous, categorical, ordinal, binary, text, date)
- [ ] Measurement details (scale, anchors, format)
- [ ] Source citation
- [ ] Valid range
- [ ] Missing value code
- [ ] N valid and N missing (%)
- [ ] Distribution summary (M/SD or n/%)
- [ ] Scale membership (which composite)
- [ ] Reverse coding status
- [ ] Notes

### 4.2 For composite scores (additional)
- [ ] Component items listed
- [ ] Scoring method (mean, sum, factor score)
- [ ] Reliability (alpha, omega)
- [ ] Factor loadings per item

### 4.3 Export formats
- [ ] `data/codebook/codebook.html` — browsable HTML
- [ ] `data/codebook/codebook.csv` — machine-readable data dictionary
- [ ] `data/codebook/codebook.docx` — for manuscript appendix

---

## 5. Measures Summary Table (for Methods Section)

### 5.1 Contents per row
- [ ] Construct name
- [ ] Number of items
- [ ] Scale and anchors
- [ ] Source citation (APA format)
- [ ] Cronbach's alpha
- [ ] McDonald's omega
- [ ] Sample item (representative item text)

### 5.2 Export
- [ ] `output/tables/measures-summary.html`
- [ ] `output/tables/measures-summary.docx`

---

## 6. Sample Flow

### 6.1 If exclusions occurred
- [ ] Starting N (raw data)
- [ ] Each exclusion step: criterion, N removed, N remaining
- [ ] Final analytic N
- [ ] CONSORT-style flow (integrate with `/data-clean` output if available)

### 6.2 Data completeness
- [ ] Overall completeness rate
- [ ] Per-variable completeness for key measures
- [ ] Missing data handling strategy noted

---

## 7. Data Profile Report

### 7.1 Compile all sections
- [ ] Best practices statement with date
- [ ] Sample overview
- [ ] Demographics table
- [ ] Measures summary with reliability
- [ ] Full codebook
- [ ] Sample flow (if applicable)
- [ ] Scale psychometric details

### 7.2 Export
- [ ] `reports/data-profile.html` — standalone Quarto report
