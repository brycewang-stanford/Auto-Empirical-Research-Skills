# Python Coding Standards for Research

> Every Python skill in this suite follows these standards.

## Style

- **PEP 8** — snake_case, 4-space indentation
- **Type hints** on all function signatures
- Maximum line length: 88 characters (Black formatter default)
- Format with `ruff format` (via uv)

## Package Management

- All packages managed via `uv`
- `uv.lock` committed to git for reproducibility
- `pyproject.toml` as the single source of truth for dependencies
- Never `pip install` directly — use `uv add`

## Reproducibility

- **Set seed** at the top of any script using randomization:
  ```python
  import numpy as np
  np.random.seed(42)  # documented in decision log
  ```
- **Environment info** captured via `watermark` at end of every pipeline run
- **No hardcoded absolute paths** — use `pathlib.Path` relative to project root
- **uv sync** before every pipeline run

## Data Handling — Polars First

- Use `polars` as the primary DataFrame library
- Use `pandas` only at boundaries where other packages require it (`.to_pandas()`)
- Lazy evaluation preferred: build the query, then `.collect()` once
- Raw data read with `pl.read_csv()`, `pl.read_parquet()`, `pl.read_excel()`
- Processed data saved as `.parquet` (fast, typed, interoperable) or `.csv` (human-readable)

```python
import polars as pl

# Good: polars-native
df = pl.scan_csv("data/raw/survey.csv").filter(
    pl.col("attention_check") == "blue"
).collect()

# At package boundary:
model = sm.OLS.from_formula("purchase_intention ~ brand_auth", data=df.to_pandas())
```

## Function Design (for Snakemake pipeline)

- Each analysis step is a **function** in a module file
- Modules live in `python/`, organized by pipeline stage
- Functions take explicit inputs and return explicit outputs
- Type hints on all arguments and return values
- Docstrings with: purpose, parameters, returns, example

```python
def clean_survey_data(
    raw: pl.DataFrame,
    min_duration_seconds: int = 120,
) -> tuple[pl.DataFrame, dict[str, int]]:
    """Clean survey data with documented exclusions.

    Parameters
    ----------
    raw : pl.DataFrame
        Raw survey responses from data/raw/
    min_duration_seconds : int
        Minimum completion time to keep participant

    Returns
    -------
    tuple[pl.DataFrame, dict[str, int]]
        Cleaned data and exclusion counts at each step
    """
```

## Variable Naming in Analysis Code

- Same as R standards: use construct names from the codebook
- `brand_authenticity` not `x1`
- `purchase_intention` not `dv`
- Prefix computed variables: `z_` for standardized, `log_` for log-transformed, `c_` for centered

## Commenting

- Same principles as R: why, not what
- Reference hypotheses, pre-registration, and codebook
- Docstrings on all functions

## Validation with Pandera

```python
import pandera as pa
import pandera.polars as pap

class SurveySchema(pap.DataFrameModel):
    participant_id: int = pap.Field(unique=True)
    brand_authenticity: float = pap.Field(ge=1, le=7)
    purchase_intention: float = pap.Field(ge=1, le=7)
    age: int = pap.Field(ge=18, le=100)
    gender: str = pap.Field(isin=["male", "female", "non-binary", "prefer_not_say"])
```

## Snakemake Pipeline Pattern

```python
# Snakefile
rule all:
    input:
        "output/tables/hypothesis-tests.html",
        "output/figures/main-results.png",
        "reports/manuscript.html"

rule clean:
    input: "data/raw/survey.csv"
    output: "data/processed/survey_clean.parquet"
    script: "python/02_clean.py"

rule analyze:
    input: "data/processed/survey_clean.parquet"
    output: "output/results/models.pkl"
    script: "python/04_analyze.py"
```
