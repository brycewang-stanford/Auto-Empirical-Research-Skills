# Transparency & Documentation Standards

> Every skill enforces these. No exceptions.

## The Decision Log

Location: `docs/decisions/`

Every subjective analytical choice gets a decision log entry:

```markdown
## [YYYY-MM-DD] Decision Title

**Choice:** What was decided
**Alternatives considered:** What else could have been done
**Rationale:** Why this choice was made
**Impact:** How this affects results (if known)
**Pre-registration alignment:** Matches / Deviates (with justification)
```

Subjective choices include:
- Exclusion criteria (who was removed and why)
- Outlier handling method
- Missing data strategy
- Variable transformations (log, winsorize, etc.)
- Control variable selection
- Model specification choices
- Scale composition decisions
- Coding decisions (how categorical variables are coded)

## Data Provenance

Every dataset in `data/raw/` must have:
- Source documentation (where it came from, when it was collected)
- Data use agreement or IRB reference (if applicable)
- Original format preserved (even if you also save as CSV)

## Transformation Logging

Every cleaning/transformation step must log:
- N before the step
- What was done
- N after the step
- How many cases were affected

Example:
```
Step 3: Remove participants who failed attention check (Q15 != "blue")
  Before: N = 523
  Removed: 47 (9.0%)
  After: N = 476
```

## Codebook Requirements

Every variable in the analysis must have:
- Full name (not just abbreviation)
- Description
- Type (continuous, categorical, ordinal, binary)
- Scale/measurement info (e.g., "7-point Likert, 1=Strongly Disagree to 7=Strongly Agree")
- Source (which survey item, which database field)
- Missing data coding
- For composites: which items, reliability (alpha/omega)

## Pre-Registration Alignment

When the analysis deviates from the pre-registration:
1. Flag it explicitly in the output
2. Create a decision log entry
3. Report both the pre-registered and actual analysis (if different)
4. Clearly label exploratory analyses as such

## Session Info

Every analysis output includes computational environment info:
- R: `sessionInfo()` or `sessioninfo::session_info()`
- Python: `watermark` or `uv` environment snapshot
- Package versions for every package used
- OS and platform info
- Date and time of execution

## FAIR Compliance Checklist

- **Findable:** DOI assigned (via OSF/Zenodo), rich metadata
- **Accessible:** Open repository, no paywalls for code/data
- **Interoperable:** Standard formats (CSV, not proprietary), documented schemas
- **Reusable:** Clear license, complete documentation, runnable pipeline
