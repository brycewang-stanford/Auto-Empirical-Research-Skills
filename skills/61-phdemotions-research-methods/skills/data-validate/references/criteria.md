# Data Validation Rubric

> Run every check. Report every finding. Organize by category.

---

## 1. Structural Integrity

### 1.1 File readability
- Can the file be read without errors?
- Is the encoding correct (UTF-8 preferred)?
- Are delimiters consistent (for CSV)?
- Are there header issues (duplicate column names, unnamed columns)?

### 1.2 Dimensions
- How many rows (observations)?
- How many columns (variables)?
- Does this match what was expected? (If researcher specified N, compare)

### 1.3 Duplicates
- Are there duplicate rows (exact matches across all columns)?
- Are there duplicate IDs (if an ID column exists)?
- Report count of duplicates and which IDs are affected

### 1.4 Variable types
- Are numeric variables stored as numeric (not character/string)?
- Are categorical variables properly typed?
- Are dates parsed correctly?
- Flag any variables where the inferred type doesn't match the expected type

---

## 2. Completeness

### 2.1 Overall completeness
- What percentage of the full data matrix is non-missing?

### 2.2 Variable-level missingness
- For each variable: count and percentage missing
- Flag variables with >5% missing (note), >20% missing (warning), >50% missing (critical)

### 2.3 Row-level missingness
- For each row: how many variables are missing?
- Flag rows that are mostly empty (possible incomplete submissions)

### 2.4 Missingness patterns
- Is missingness random or patterned?
- Use `naniar::vis_miss()` (R) or `missingno.matrix()` (Python) to visualize
- Are certain variables always missing together? (suggests a survey branch or skip pattern)

### 2.5 Missing value coding
- Are missing values coded consistently? (NA, -99, 999, blank, "N/A", etc.)
- Flag non-standard missing codes that need conversion

---

## 3. Value Validity

### 3.1 Range checks
- For Likert scales: are all values within the expected range? (e.g., 1-7)
- For continuous variables: are there implausible outliers?
- For age: within expected range for the population?
- For percentages: between 0 and 100?
- For counts: non-negative?

### 3.2 Distribution checks
- For continuous variables: compute mean, SD, median, min, max, skewness, kurtosis
- Flag extreme skewness (>|2|) or kurtosis (>|7|) — may need transformation
- Visualize distributions (histograms or density plots)

### 3.3 Categorical value checks
- For categorical variables: what are the unique values?
- Are there unexpected categories? (typos, encoding issues, extra whitespace)
- Are factor levels sensible and consistent?

### 3.4 Impossible value combinations
- Age < 18 in an adults-only study
- Response time < 30 seconds for a 10-minute survey
- Start date after end date
- Contradictory responses (if logic checks are specified)

---

## 4. Survey-Specific Checks

### 4.1 Attention checks
- Identify attention check items (e.g., "Please select 'Strongly Agree' for this item")
- Count and percentage of failures
- Report which participants failed
- DO NOT exclude — just report. Exclusion is a cleaning decision.

### 4.2 Manipulation checks
- Identify manipulation check items
- Report success/failure rates by condition
- Flag if manipulation check failure rate is unusually high

### 4.3 Straight-lining
- For matrix questions: did any participants select the same response for all items?
- Report count and percentage of potential straight-liners
- Compute variance per participant across scale items — zero variance = straight-lining

### 4.4 Response time
- If completion time is available: what is the distribution?
- Flag suspiciously fast completions (threshold depends on survey length)
- Flag suspiciously slow completions (may indicate distraction or break)

### 4.5 Bot detection
- If IP, geolocation, or reCAPTCHA data available: flag suspicious patterns
- Duplicate IP addresses
- Responses from unexpected geographic locations

---

## 5. Scale Reliability

### 5.1 Internal consistency
- For each multi-item scale: compute Cronbach's alpha
- Report McDonald's omega if available (more robust than alpha)
- Flag scales with alpha < .70 (conventional threshold, but context-dependent)

### 5.2 Item-level diagnostics
- Item-total correlations: flag items with r < .30 (poor discrimination)
- Alpha-if-item-deleted: would removing any item substantially improve reliability?

### 5.3 Reverse-coded items
- Are reverse-coded items identified?
- Have they been reverse-scored already, or is this needed?
- Warning if reverse-coded items correlate positively with other items (suggests they haven't been reversed)

---

## 6. Data Provenance

### 6.1 Source documentation
- Where did this data come from?
- When was it collected?
- What platform? (Qualtrics, Prolific, MTurk, institutional survey, database extract)
- Is there a data use agreement?

### 6.2 Format preservation
- Is the original format preserved in `data/raw/`?
- If converted, is the original also kept?

---

## Output

Validation produces two artifacts:

1. **Validation report** (HTML) — saved to `output/results/validation-report.html`
   - R: `pointblank` agent report
   - Python: Custom report from `pandera` validation results

2. **Codebook** (HTML + CSV) — saved to `data/codebook/`
   - R: `codebook::codebook()` HTML report + CSV data dictionary
   - Python: Custom codebook in HTML via Quarto + CSV data dictionary
