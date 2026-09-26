"""Read tabular data in the formats empirical researchers actually keep it in."""
from __future__ import annotations

import os
import pandas as pd

READERS = {
    ".csv": lambda p, **k: pd.read_csv(p, **k),
    ".tsv": lambda p, **k: pd.read_csv(p, sep="\t", **k),
    ".txt": lambda p, **k: pd.read_csv(p, sep=None, engine="python", **k),
    ".dta": lambda p, **k: pd.read_stata(p, convert_categoricals=False, **k),
    ".parquet": lambda p, **k: pd.read_parquet(p, **k),
    ".pq": lambda p, **k: pd.read_parquet(p, **k),
    ".feather": lambda p, **k: pd.read_feather(p, **k),
    ".arrow": lambda p, **k: pd.read_feather(p, **k),
    ".xlsx": lambda p, **k: pd.read_excel(p, **k),
    ".xls": lambda p, **k: pd.read_excel(p, **k),
    ".json": lambda p, **k: pd.read_json(p, **k),
    ".jsonl": lambda p, **k: pd.read_json(p, lines=True, **k),
}


def read_table(path, **kw) -> pd.DataFrame:
    """CSV / TSV / Stata .dta / parquet / feather / Excel / JSON by extension.
    Column names are left exactly as they are; Stata value labels are not
    applied (the card refers to the numeric codes)."""
    ext = os.path.splitext(str(path))[1].lower()
    if ext not in READERS:
        raise ValueError(f"unsupported data format {ext!r}; known: {sorted(READERS)}")
    try:
        return READERS[ext](path, **kw)
    except ImportError as exc:                    # pyarrow / openpyxl missing
        raise ImportError(f"reading {ext} needs an optional dependency: pip install 'phack[formats]' ({exc})") from exc
