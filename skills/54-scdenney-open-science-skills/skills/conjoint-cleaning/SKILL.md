---
name: conjoint-cleaning
description: Clean and reshape Qualtrics conjoint exports to analysis-ready long format.
argument-hint: "[describe your Qualtrics export or paste data sample]"
---

# Conjoint Data Cleaning Expert

## Instructions

### 1. Qualtrics Export Settings and Metadata

**Export format:** When exporting from Qualtrics, select **"Use choice text"** (not "Use numeric values") so that attribute levels appear as human-readable labels. If working with non-Latin scripts (Chinese, Korean, Arabic), export as XLSX rather than CSV to avoid UTF-8/ANSI encoding issues. On Windows with East Asian locales, `read.csv()` may still require `Sys.setlocale()` to match the file encoding before import (see `?cjoint::read.qualtrics` East Asian Language Support).

**Metadata rows:** Current Qualtrics CSV exports include **3 header rows** before respondent data: (1) variable identifiers, (2) question text/descriptions, (3) ImportId JSON. Legacy exports have 2 rows. The `cjoint::read.qualtrics()` parameter `new.format = TRUE` (set explicitly; default is `FALSE`) handles the 3-row format. For manual import via `readxl::read_excel()` or `readr::read_csv()`, skip the appropriate number of metadata rows after reading headers.

**Randomization order columns:** If "Export viewing order data" is enabled, Qualtrics adds `_DO_` columns (e.g., `Block1_DO`) containing pipe-separated integers showing element display order. These are useful for task-order robustness checks but are not needed for the core reshape.

### 2. Qualtrics Conjoint Implementation Methods

Qualtrics conjoint experiments use one of three implementation methods, each producing different column naming conventions:

**Method A — Conjoint Survey Design Tool (Strezhnev):** Generates JavaScript that Qualtrics executes to randomize profiles. Column naming follows `F-{task}-{profile}-{attribute}` for attribute levels and `F-{task}-{attribute}` for attribute names. The `cjoint` R package's `read.qualtrics()` function is purpose-built for this format.

**Method B — Custom JavaScript + Embedded Data:** Researchers write JavaScript to randomize attributes and store values in Qualtrics embedded data fields. Column naming is researcher-defined. Two common conventions: (i) `C{x}-F-{task}-{idx}` for attribute names and `C{x}-F-{task}-{profile}-{idx}` for profile values; (ii) the Graham (2020) convention, `choice{task}_{attr}{profile}` with fixed attribute order (e.g., `choice1_bread1`) or `c{task}_attrib{pos}_name` / `c{task}_attrib{pos}_sand{profile}` when attribute order is also randomized. Requires manual reshaping (Section 4).

**Method C — Loop & Merge:** Each loop iteration represents one conjoint task. Embedded data fields are referenced via `${e://Field/variable_name}` and displayed with `${lm://Field/N}`. Column names reflect the embedded data field structure. Requires manual reshaping.

**Before writing any cleaning code:** Inspect the actual column headers, the QSF survey definition file, or any JavaScript in the survey to determine which method was used. Do not assume a column naming convention.

### 3. Existing R Packages for Conjoint Data Import

Before writing custom reshaping code, check whether an existing package handles the data format:

**`cjoint::read.qualtrics()`** — Purpose-built for Conjoint SDT exports (Method A). Reads Qualtrics CSV directly, handles metadata rows, outputs one row per profile with a `selected` column. Parameters: `responses` (choice column names), `covariates` (respondent-level variables), `respondentID`, `new.format` (TRUE for 3-row headers), `ranks` (for rank/rating/top-L designs). Supports binary forced choice, profile ranks, per-profile ratings, and top-L choices; see `?cjoint::read.qualtrics` Details for the four response types. Requires PHP/JS output from the Conjoint Survey Design Tool.

**`cjdata::reshape_conjoint()`** — Lightweight alternative. Functions: `read_Qualtrics()` + `reshape_conjoint()`. Handles basic wide-to-long conversion. Requires the **terminal character** of each outcome string to be {"1","2"} or {"A","B"} (so "Candidate A" works; Japanese zenkaku digits supported). Respondent covariates merged separately.

**`projoint::reshape_projoint()`** — For measurement-error-corrected analysis per Clayton, Horiuchi, Kaufman, King, and Komisarchik (2023). Built-in support for repeated tasks (IRR estimation), missing-agreement imputation (`.fill = TRUE`), and bias-corrected AMCEs. Outcome column names must contain task-ID digits, and the repeated-task outcome must be the **last** element of `.outcomes`. Expects wide columns named `K-{task}-{attribute}` and `K-{task}-{profile}-{attribute}` by default (`.alphabet = "K"`); selected profile is parsed from the final character of each outcome string via `.choice_labels` (default `c("A","B")`). Specify `.flipped = TRUE` when the repeated task presents profiles in reversed left/right order (see `exampleData1` vs. `exampleData2` in the manual); this changes how agreement is computed. **Trap:** `projoint::read_Qualtrics()` hard-codes a 2-row metadata skip (legacy format). For current 3-row Qualtrics exports, pre-strip the third metadata row or read manually via `readr::read_csv(skip = 3)` before calling `reshape_projoint()`.

**`cregg::cj_tidy()`** — Reshapes wide data across the three-level respondent/task/profile hierarchy via two named lists: `profile_variables` (features and profile-specific outcomes that vary within a task) and `task_variables` (variables that vary by task but not across profiles within it). Crucially, a choice variable that names the chosen profile ("left"/"right") goes in `task_variables` and must be recoded after reshaping, whereas per-profile "chosen" indicators go in `profile_variables` — getting this wrong silently corrupts the outcome. Constraint handling is **not** a `cj_tidy` feature; two-way design constraints are specified downstream via `*` in the `amce()`/`cj()` formula.

**Package decision rule (default then escape hatch):**
- Method A (SDT) export, no measurement-error correction needed → `cjoint::read.qualtrics()`
- Measurement-error / IRR correction via a repeated task → `projoint::reshape_projoint()`
- Simple Qualtrics CSV with binary outcome and default column naming → `cjdata::reshape_conjoint()`
- Complex wide data with non-standard column names that still map cleanly to profile/task variables → `cregg::cj_tidy()`
- Method B/C exports with custom embedded-data naming, language translation, attribute-level merges, or pilot-data exclusion that existing packages cannot handle → manual reshape (Section 4)

### 4. Manual Wide-to-Long Reshaping

When existing packages cannot handle the data format, reshape manually. The goal: one row per respondent x task x profile, one column per attribute.

**Step 1: Build a long table of (ResponseId, task, profile, attribute_name, attribute_value)**

Iterate over tasks, profiles, and attribute positions. For each combination, read the attribute name from the name column and the corresponding value from the value column. This naturally handles randomized attribute order.

```r
rows <- vector("list", T * P * K)
i <- 0L
for (task in seq_len(T)) {
  name_cols <- paste0(prefix, "-F-", task, "-", seq_len(K))
  for (profile in seq_len(P)) {
    val_cols <- paste0(prefix, "-F-", task, "-", profile, "-", seq_len(K))
    for (idx in seq_len(K)) {
      i <- i + 1L
      rows[[i]] <- data.frame(
        ResponseId      = data$ResponseId,
        task            = task,
        profile         = profile,
        attribute_name  = data[[name_cols[idx]]],
        attribute_value = data[[val_cols[idx]]],
        stringsAsFactors = FALSE
      )
    }
  }
}
long <- data.table::rbindlist(rows)
```

For Graham-style embedded fields (e.g., `choice1_bread1`, `c1_attrib1_name`/`c1_attrib1_sand1`), a `tidyr::pivot_longer(names_pattern = ...)` one-shot is often cleaner than the triple loop — match the numeric indices into task/profile/attribute-position columns, then pivot back wide on `attribute_name`. Use `data.table::rbindlist()` for performance on large datasets.

**Step 2: Filter missing data.** Remove rows where `attribute_name` or `attribute_value` is NA — these indicate respondents who skipped the conjoint section.

**Step 3: Apply attribute name and level merges** before pivoting. Fix typos, encoding variants, or synonymous levels.

**Step 4: Pivot to wide-by-attribute** using `data.table::dcast()` or `tidyr::pivot_wider()`:

```r
dcast(long, ResponseId + task + profile ~ attribute_name, value.var = "attribute_value")
```

If `dcast` warns about duplicate row/column combinations, two positions in the same task share an attribute name for some respondents — investigate the name merge.

### 5. Choice Variable Mapping

Choice variables are separate Qualtrics questions (MC type), one per task, placed after each conjoint display.

**Identify choice columns:** These are NOT part of the embedded data fields. Map each choice question to its task number (Q17 -> task 1, Q19 -> task 2, etc.). Inspect the QSF or survey flow to confirm the mapping.

**Text vs. numeric encoding:** Text exports produce labels like "Person A"/"Person B" or "Profile 1"/"Profile 2". Numeric exports produce 1/2. Always verify from the actual data — do not assume.

**Create the binary outcome:** Prefer matching the terminal character of the choice string so the same code handles "Person A"/"Person B", "Profile 1"/"Profile 2", "Candidate A"/"Candidate B", and "Sandwich 1"/"Sandwich 2" uniformly. If numeric exports are used, coerce directly.

```r
last_char <- stringr::str_sub(raw_choice, -1L)
chosen_profile <- dplyr::case_when(
  last_char %in% c("A", "1") ~ 1L,
  last_char %in% c("B", "2") ~ 2L,
  TRUE                       ~ NA_integer_
)
# Merge by (ResponseId, task), then:
chosen <- as.integer(profile == chosen_profile)
```

**Handle missing choices:** Drop rows where `chosen` is NA. Some tasks may have higher dropout rates than others (especially the last task).

### 6. Ratings and Secondary DVs

Ratings may be **per-profile** (one per profile per task — usable as a continuous conjoint DV) or **per-task** (one rating of the chosen profile — descriptive only, not a standard conjoint DV).

**Endpoint label recoding:** Qualtrics text exports encode scale endpoints as text labels (e.g., "Strongly disagree" = 1, "Strongly agree" = 7). Recode these before converting to numeric. Intermediate scale points are already numeric.

```r
rating_num <- dplyr::case_when(
  raw_rating == "Strongly disagree" ~ 1,
  raw_rating == "Strongly agree"    ~ 7,
  TRUE                              ~ suppressWarnings(as.numeric(raw_rating))
)
```

### 7. Attribute-Level Translation and Factor Ordering

**Use `recode_factor()` with deliberate level ordering.** The order of arguments sets the factor level order, which determines:
- The **AMCE reference category** (first level = baseline, shown at zero)
- The **display order** in figures

For Stata/SPSS/Qualtrics exports that already carry labels (e.g., loaded via `haven::read_stata()`), `haven::as_factor()` converts all labelled columns to factors in one pass (Heiss 2023). Combine with `forcats::fct_relevel()` to set the baseline without re-typing every level. Use `recode_factor()` when you also need translation or level merges.

**Reference category principles:**
- Ordinal attributes (time, income): **lowest** level as reference — AMCEs show benefit of higher levels
- In-group/out-group attributes (ethnicity): **majority/in-group** as reference — AMCEs show out-group penalty
- Status/legal attributes: **lowest status** as reference — AMCEs show benefit of higher status
- Nominal with neutral option: **neutral/no-opinion** as reference

**Catching unexpected values:** Set `.default = NA_character_` in `recode_factor()` to force unrecognized values to NA. Default handling of unmatched values has varied across `dplyr` versions, and unexpected pilot-only levels can otherwise pass through as new factor levels or quietly coerce to NA without surfacing. Set `.default` explicitly so pilot contamination and typos are visible in a post-reshape `table()` check, not masked by silent defaults.

**Drop unused levels:** After filtering, call `droplevels()` to remove factor levels with zero observations. `cregg::cj()` requires 2+ realized levels per factor.

### 8. Pilot and Data Quality Diagnostics

**Pilot detection:** Compare unique attribute levels in the data against the final design document. Extra levels (e.g., a country not in the final design) indicate pilot/pre-test respondents. Exclude these **as respondents** (all their rows), not just the anomalous rows — their entire randomization was generated by a different design.

**Pilot exclusion is an analytic choice, not just cleaning hygiene.** Under DA-RT/APSA transparency norms, the pilot-vs-final boundary should be specified in the pre-analysis plan. If it was not pre-registered, treat the exclusion as a researcher degree of freedom: log every excluded `ResponseId` with a reason code in a machine-readable exclusions file, and report both with-pilot and without-pilot estimates as a sensitivity check. See the pre-registration-writing and methods-reporting skills.

**Missing conjoint data:** Respondents who skipped the conjoint section produce all-NA attribute columns. The NA filter in Step 2 removes them. Respondents who dropped out mid-conjoint will have fewer than T x P rows — this is acceptable for `cregg::cj()`.

**Duplicate attribute names:** Each task should have exactly K unique attribute names. If a merge creates duplicates within a task, the merge is incorrect.

**Choice completeness:** `chosen` should sum to T per respondent (one chosen profile per task). Fewer indicates missing choices for some tasks.

### 9. Subgroup Variables

Include respondent-level covariates in the analysis-ready dataset even for main-effects-only analysis. Future subgroup and interaction analyses should not require re-running data prep.

Merge demographics (age, gender, education, urban/rural, ethnicity, party membership), treatment assignments, randomization indicators, and open-text responses by ResponseId after reshaping.

### 10. Output Format and Package Compatibility

**Target shape is not arbitrary.** The "one row per respondent x task x profile" unit of observation is dictated by the Hainmueller, Hopkins, and Yamamoto (2014) potential-outcomes framework, under which the AMCE is defined at the profile level with profile-level randomization and a no-carryover / stability assumption across tasks. Collapsing to one-row-per-task (e.g., keeping only the chosen profile's attributes) destroys the identification strategy. Ratings used as a continuous DV must also be per-profile, not per-task.

Save as `.rds` files (one per conjoint). The output should have:

- One row per respondent x task x profile
- One column per attribute (**factor type**, not character — `cregg::cj()` will error on character columns)
- `ResponseId`: respondent identifier (character or numeric)
- `task`: task number (integer)
- `profile`: profile number (integer)
- `chosen`: binary outcome (**numeric 0/1**, not logical or factor)
- Optional: `rating` (numeric)
- Subgroup variables at the respondent level

**cregg compatibility:** `cj(data, chosen ~ Attr1 + Attr2 + ..., id = ~ResponseId)`. The `id` parameter requires a **tilde formula** (`~ResponseId`), not a bare name. The `estimate` parameter accepts `"amce"`, `"mm"`, `"mm_differences"`, `"amce_differences"`, and `"frequencies"`.

**cjoint compatibility:** Expects a `selected` column (logical) and attributes named with the F-based convention. Use `cjoint::amce()` for estimation.

**projoint compatibility:** Requires a `projoint_data` object created via `reshape_projoint()`. Supports repeated-task IRR estimation and bias-corrected AMCEs.

## Quality Checks

- [ ] **Implementation method identified:** Determined which of the three Qualtrics methods was used (SDT, custom JS, Loop & Merge) by inspecting column headers or QSF file
- [ ] **Existing packages evaluated:** Checked whether `cjoint`, `cjdata`, or `projoint` can handle the data format before writing custom reshaping code
- [ ] **Metadata rows handled:** Skipped the correct number of header rows (3 for current Qualtrics, 2 for legacy)
- [ ] **Column convention verified:** Conjoint column naming pattern confirmed from actual data, not assumed
- [ ] **Attribute randomization handled:** Reshape pairs each name column with its value column at the same position
- [ ] **Choice encoding verified:** Choice values confirmed from actual data, including text-encoded choices
- [ ] **Pilot data excluded:** Attribute levels compared against design document; pilot respondents excluded entirely
- [ ] **Missing data filtered:** Skipped-section respondents and missing-choice tasks properly removed
- [ ] **Attributes are factors:** All attribute columns are factor type (not character) with 2+ realized levels
- [ ] **Outcome is numeric 0/1:** `chosen` column is numeric, not logical or factor
- [ ] **Reference categories set:** Factor levels ordered with intended AMCE baseline first
- [ ] **Unmapped values caught:** `recode_factor(.default = NA_character_)` used to surface unexpected values
- [ ] **Validation passed:** Row counts, choice sums, and factor levels match expectations
- [ ] **Subgroup variables included:** Respondent-level covariates present for future interaction analyses
- [ ] **Cleaning is deterministic and scripted:** Raw-to-analysis-ready pipeline runs end-to-end from a single script with no manual steps (DA-RT)
- [ ] **Exclusions logged with reason codes:** Every dropped `ResponseId` has a machine-readable reason (pilot, no-consent, all-NA conjoint, etc.); raw export is preserved unmodified
- [ ] **Package versions pinned:** `sessionInfo()` captured; `cjoint`, `projoint`, `cregg`, `dplyr` behaviors differ across versions and should be fixed for reproducibility
