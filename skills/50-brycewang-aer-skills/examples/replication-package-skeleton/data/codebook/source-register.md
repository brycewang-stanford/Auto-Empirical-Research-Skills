# Data Source Register

Use this register to document every raw and derived dataset before running the
analysis. Keep it synchronized with the README sections titled "Data
Availability and Provenance Statement" and "Dataset List."

## Source Inventory

| Source ID | Source name | Raw file(s) | Provider or repository | URL / DOI / accession | License or access terms | Date accessed | Provided in package? | Restrictions / DUA | Used in exhibits |
|---|---|---|---|---|---|---|---|---|---|
| S1 | [Source name] | `data/raw/source1.csv` | [Provider] | [URL or DOI] | [License] | [YYYY-MM-DD] | Yes / No | [None or details] | Tables 1-3; Figure 2 |
| S2 | [Source name] | `data/raw/source2.dta` | [Provider] | [URL or DOI] | [License] | [YYYY-MM-DD] | Yes / No | [None or details] | Appendix Table A.1 |

## Variable Crosswalk

| Source ID | Source variable | Analytic variable | Type | Definition | Transformation script | Notes |
|---|---|---|---|---|---|---|
| S1 | `[raw_name]` | `[analytic_name]` | Numeric / string / date | [Definition] | `code/01_clean.do` | [Unit, coding, or recode note] |
| S2 | `[raw_name]` | `[analytic_name]` | Numeric / string / date | [Definition] | `code/01_clean.do` | [Unit, coding, or recode note] |

## Derived Files

| Derived file | Built by | Inputs | Row count | Unit of observation | Key identifiers | Last verified |
|---|---|---|---:|---|---|---|
| `data/intermediate/analytic.dta` | `code/01_clean.do` | S1, S2, S3 | [N] | [Unit] | [IDs] | [YYYY-MM-DD] |

## Audit Rules

- Every raw file listed in `README.md` must appear in the Source Inventory.
- Every source must have a provider, stable URL/DOI/accession, license or
  access terms, date accessed, and package availability status.
- Restricted or third-party data must include the exact access route and the
  legal, ethical, or logistical reason the raw file is not public.
- Every analytic variable used in a table or figure should appear in the
  Variable Crosswalk.
- Every derived file used by analysis scripts should appear in Derived Files
  with row count, unit of observation, and key identifiers.
