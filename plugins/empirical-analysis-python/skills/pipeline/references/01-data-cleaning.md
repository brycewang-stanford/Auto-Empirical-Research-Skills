# Step 1 — Data Cleaning (Deep Reference)

Goal: turn a raw file into an **analysis-ready DataFrame** where every row exclusion, type decision, and merge has been made consciously and logged. When you hand this DataFrame to Step 2+, there should be zero silent surprises.

## Contents

1. Inspection before anything else
2. Reading non-CSV formats (Stata, SPSS, SAS, Parquet, Excel, JSON)
3. Dtype coercion — the #1 silent bug
4. Missing values — MCAR / MAR / MNAR and what to do about each
5. Outliers — flag, then decide (winsorize / trim / keep)
6. Deduplication & panel-key validation
7. Merging — `validate=` is not optional
8. Panel structure diagnostics
9. Time / date handling
10. String cleanup for categorical variables
11. A reusable `clean()` function skeleton

---

## 1. Inspection before anything else

```python
df.shape
df.info(memory_usage="deep")
df.head(10)
df.sample(10, random_state=0)           # random sample > head for spotting patterns
df.describe(include="all").T
df.isna().mean().sort_values(ascending=False).head(20)
df.nunique().sort_values()
df.select_dtypes("object").apply(lambda s: s.value_counts().head(3))
```

Visualize missing structure — patterns reveal mechanism:

```python
import missingno as msno
msno.matrix(df)                 # sparsity matrix
msno.heatmap(df)                # correlation of missingness
msno.dendrogram(df)             # hierarchical clustering of missingness
```

**Heuristic**: if missingness on two variables is highly correlated in `msno.heatmap`, they share a data-generating defect — treat them together.

---

## 2. Reading non-CSV formats

```python
# Stata
import pandas as pd, pyreadstat
df, meta = pyreadstat.read_dta("file.dta")
# meta.column_labels, meta.value_labels are often essential

# SPSS / SAS
df, meta = pyreadstat.read_sav("file.sav")
df, meta = pyreadstat.read_sas7bdat("file.sas7bdat")

# Parquet (preferred for > 1GB)
df = pd.read_parquet("file.parquet")

# Excel — specify sheet & header explicitly
df = pd.read_excel("file.xlsx", sheet_name="Sheet1", header=0, dtype={"id": str})

# JSON lines (common for API dumps)
df = pd.read_json("file.jsonl", lines=True)

# SQL
import sqlalchemy as sa
engine = sa.create_engine("postgresql://user:pass@host/db")
df = pd.read_sql("SELECT * FROM panel WHERE year >= 2000", engine)
```

---

## 3. Dtype coercion — the #1 silent bug

Strings-that-look-numeric silently break every statistical operation downstream. Fix them first.

```python
# Strict numeric
df["wage"] = pd.to_numeric(df["wage"], errors="coerce")

# Integer with NaN support — use pandas nullable Int
df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

# Categorical — saves memory, enables ordered comparisons
df["education"] = pd.Categorical(df["education"],
    categories=["<HS","HS","Some College","BA","BA+"], ordered=True)

# Boolean flags — keep as 0/1 int for regressions (NOT as bool)
df["treated"] = df["treated"].astype(int)

# Dates — always parse; never leave as string
df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce", format="%Y-%m-%d")
df["quarter"]   = df["hire_date"].dt.to_period("Q")
```

After all coercions, re-check:

```python
df.dtypes
df.select_dtypes("object").columns      # should be empty (or only truly-free-text columns)
```

---

## 4. Missing values

Classify the mechanism before choosing a treatment:

| Mechanism | Definition | Typical fix |
|-----------|-----------|-------------|
| MCAR (missing completely at random) | missingness independent of everything | listwise drop or any imputation ok |
| MAR (missing at random) | missingness depends on observed covariates | multiple imputation (`statsmodels.imputation.MICE`) |
| MNAR (missing not at random) | missingness depends on the unobserved value itself | Heckman selection / sensitivity analysis |

**Decisions, per variable type:**

```python
# 4a. Key variables (treatment, outcome, panel keys) — DROP rows
key_vars = ["wage", "training", "worker_id", "year"]
n_before = len(df)
df = df.dropna(subset=key_vars)
print(f"Dropped {n_before-len(df)} rows missing on key vars ({100*(1-len(df)/n_before):.1f}%)")

# 4b. Numeric covariate, low missing (<5%) — median impute + missing-flag
for col in ["tenure", "assets", "firm_size"]:
    df[f"{col}_missing"] = df[col].isna().astype(int)
    df[col] = df[col].fillna(df[col].median())

# 4c. Categorical covariate — explicit "unknown" category (preserves signal)
df["union"]  = df["union"].fillna("unknown").astype("category")
df["region"] = df["region"].fillna("unknown").astype("category")

# 4d. High missing (>30%) — either drop the variable, impute via MICE, or redesign
high_miss = df.columns[df.isna().mean() > 0.3]
print(f"High-missing columns: {list(high_miss)} — decide individually")

# 4e. Multiple imputation (MICE) for MAR with non-trivial missingness
from statsmodels.imputation.mice import MICE, MICEData
imp = MICEData(df[["wage","age","edu","tenure"]])
for _ in range(10):  # 10 iterations, 5 imputed datasets
    imp.update_all()
df_imputed = imp.data
```

**Rule**: always print "Dropped N rows because X". Silent drops are bugs.

---

## 5. Outliers

Detect → decide → document. Never blindly clip.

```python
# Z-score (univariate, Gaussian tail assumption)
df["wage_z"] = (df["wage"] - df["wage"].mean()) / df["wage"].std()
z_outliers  = df["wage_z"].abs() > 4         # |z|>4 ≈ 1-in-15k under Normal

# IQR rule (robust, distribution-free)
q1, q3 = df["wage"].quantile([0.25, 0.75])
iqr    = q3 - q1
iqr_outliers = (df["wage"] < q1 - 1.5*iqr) | (df["wage"] > q3 + 1.5*iqr)

# Mahalanobis distance (multivariate)
from scipy.stats import chi2
X   = df[["wage","age","tenure"]].dropna().values
mu  = X.mean(0); S = np.cov(X, rowvar=False)
inv = np.linalg.inv(S)
d2  = np.einsum("ij,jk,ik->i", X-mu, inv, X-mu)
mah_outliers = d2 > chi2.ppf(0.999, df=X.shape[1])

# Decision tree:
# - Data-entry error (e.g. wage = 99999999)          → drop
# - Legitimate extreme (e.g. CEO in a wage dataset)   → winsorize in Step 2
# - Systematic (e.g. all outliers are in one firm)    → investigate; possible data issue
```

**Report**:
```python
print(f"|z|>4 on wage:      {z_outliers.sum()} rows")
print(f"IQR outliers wage:  {iqr_outliers.sum()} rows")
print(f"Mahalanobis 99.9%:  {mah_outliers.sum()} rows")
```

---

## 6. Deduplication & panel-key validation

```python
# Row-level duplicates
exact_dupes = df.duplicated().sum()
print(f"Exact duplicate rows: {exact_dupes}")

# Panel key duplicates (more common + more dangerous)
panel_dupes = df.duplicated(subset=["worker_id", "year"], keep=False)
if panel_dupes.any():
    print(df[panel_dupes].sort_values(["worker_id","year"]).head(20))
    # Typical fixes:
    # - Keep the most recent record:     df = df.sort_values("timestamp").drop_duplicates(["worker_id","year"], keep="last")
    # - Aggregate within key:            df = df.groupby(["worker_id","year"]).agg(...).reset_index()
    # - Genuine multi-record:            redefine the panel key (e.g. add spell_id)

assert not df.duplicated(subset=["worker_id","year"]).any(), "panel key not unique"
```

---

## 7. Merging — `validate=` catches silent m:m

```python
# Always specify how= AND validate=
df = df.merge(firm_chars, on="firm_id", how="left", validate="many_to_one")
#                                                        ^^^^^^^^^^^^^^^^^
# Options:
#   "one_to_one"    each key unique on both sides
#   "one_to_many"   unique on left
#   "many_to_one"   unique on right  (most common)
#   "many_to_many"  no constraint (usually a bug — pandas will blow up rows)

# After every merge, check you didn't lose rows accidentally:
assert len(df) == n_before_merge, "merge changed row count!"

# Fuzzy keys — normalize first
df["firm_id"] = df["firm_id"].astype(str).str.strip().str.upper()
firm_chars["firm_id"] = firm_chars["firm_id"].astype(str).str.strip().str.upper()

# Range / nearest merges (e.g. assign CPI by year+month)
df = pd.merge_asof(df.sort_values("date"), cpi.sort_values("date"),
                   on="date", direction="backward")
```

---

## 8. Panel structure diagnostics

```python
# 8a. Coverage table: how many units and years
n_units = df["worker_id"].nunique()
n_years = df["year"].nunique()
years_range = (df["year"].min(), df["year"].max())
print(f"{n_units} units × {n_years} years, {years_range}, {len(df)} rows "
      f"(implied rect = {n_units*n_years}, coverage = {100*len(df)/(n_units*n_years):.1f}%)")

# 8b. Per-unit observation count
unit_counts = df.groupby("worker_id")["year"].count()
print(unit_counts.describe())
unit_counts.hist(bins=30); plt.xlabel("# years observed per worker")

# 8c. Entry / exit patterns
df_sorted = df.sort_values(["worker_id","year"])
first_year = df_sorted.groupby("worker_id")["year"].first()
last_year  = df_sorted.groupby("worker_id")["year"].last()
print("Entry-year distribution:")
print(first_year.value_counts().sort_index())

# 8d. Gap detection — some units have holes in the middle of their panel
def has_gap(g):
    years = sorted(g["year"].unique())
    return (max(years) - min(years) + 1) != len(years)
gap_units = df.groupby("worker_id").apply(has_gap)
print(f"{gap_units.sum()} units have year gaps")

# 8e. Force to balanced panel (if design requires it) — and LOG what you drop
def make_balanced(df, entity, time):
    full_years = set(df[time].unique())
    complete_units = df.groupby(entity)[time].apply(lambda s: set(s) == full_years)
    keep = complete_units[complete_units].index
    return df[df[entity].isin(keep)].copy()
df_bal = make_balanced(df, "worker_id", "year")
print(f"Balanced panel: dropped {df['worker_id'].nunique() - df_bal['worker_id'].nunique()} units")
```

---

## 9. Time / date handling

```python
df["date"] = pd.to_datetime(df["date"])
df["year"]    = df["date"].dt.year
df["quarter"] = df["date"].dt.to_period("Q")
df["month"]   = df["date"].dt.month
df["dow"]     = df["date"].dt.dayofweek

# Relative time to an event (for event studies)
df["event_date"] = pd.to_datetime(df["policy_date"])
df["days_since_event"]   = (df["date"] - df["event_date"]).dt.days
df["months_since_event"] = ((df["date"].dt.year  - df["event_date"].dt.year) * 12 +
                            (df["date"].dt.month - df["event_date"].dt.month))

# Business calendar alignment (finance)
df["bdate"] = pd.bdate_range(start=df["date"].min(), end=df["date"].max())

# Timezone-aware
df["date_utc"] = df["date"].dt.tz_localize("America/New_York").dt.tz_convert("UTC")
```

---

## 10. String cleanup for categorical variables

```python
s = df["industry"]
s = s.astype(str).str.strip().str.lower()
s = s.str.replace(r"\s+", " ", regex=True)           # collapse whitespace
s = s.str.replace(r"[^\w\s]", "", regex=True)        # strip punctuation
df["industry_clean"] = s

# Value-level fuzzy dedupe
from rapidfuzz import process, fuzz
unique_vals = df["industry_clean"].unique()
# canonical_map = {raw: canonical_form, ...}
```

---

## 11. Reusable `clean()` skeleton

```python
def clean(raw: pd.DataFrame, *, key_vars, numeric, categorical, dates) -> pd.DataFrame:
    df = raw.copy()

    # dtypes
    for c in numeric:      df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in categorical:  df[c] = df[c].astype("category")
    for c in dates:        df[c] = pd.to_datetime(df[c], errors="coerce")

    # missing on key vars -> drop with a log line
    n0 = len(df)
    df = df.dropna(subset=key_vars)
    print(f"[clean] dropped {n0-len(df):,} rows missing on key vars")

    # impute numeric covariates (median + flag)
    for c in numeric:
        if c in key_vars: continue
        df[f"{c}_missing"] = df[c].isna().astype(int)
        df[c] = df[c].fillna(df[c].median())

    # explicit "unknown" for categoricals
    for c in categorical:
        df[c] = df[c].cat.add_categories("unknown").fillna("unknown")

    # dedupe panel key
    if {"id","year"}.issubset(df.columns):
        df = df.sort_values(["id","year"]).drop_duplicates(["id","year"], keep="last")

    return df
```

Log every decision; every row deletion prints a count. The rest of the pipeline inherits a clean, predictable DataFrame.
