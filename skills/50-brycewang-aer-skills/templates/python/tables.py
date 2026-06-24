"""
tables.py
AER-style regression tables via pyfixest.etable.

pyfixest provides AER-class booktabs LaTeX output natively.
"""

from __future__ import annotations

import logging
import pandas as pd
import pyfixest as pf

import setup

log = logging.getLogger(__name__)


def run() -> None:
    df = pd.read_parquet(setup.INTERMEDIATE / "analytic.parquet")

    m1 = pf.feols("outcome ~ treat",                        data=df, vcov={"CRV1": "unit_id"})
    m2 = pf.feols("outcome ~ treat + x1 + x2",              data=df, vcov={"CRV1": "unit_id"})
    m3 = pf.feols("outcome ~ treat + x1 + x2 | unit_id + year",
                                                            data=df, vcov={"CRV1": "unit_id"})
    m4 = pf.feols("outcome ~ x1 + x2 | unit_id + year | endog ~ iv",
                                                            data=df, vcov={"CRV1": "unit_id"})
    m5 = pf.feols("outcome ~ x1 + x2 | unit_id + year | endog ~ iv",
                                                            data=df.query("balanced == 1"),
                                                            vcov={"CRV1": "unit_id"})

    pf.etable(
        models      = [m1, m2, m3, m4, m5],
        type        = "tex",
        file_name   = str(setup.TABLES / "tab_main.tex"),
        signif_code = [0.01, 0.05, 0.10],
        digits      = 3,
        keep        = ["treat", "endog"],
        labels      = {"treat": "Treatment", "endog": "Endogenous regressor"},
        custom_stats = {
            "Controls":      ["No", "Yes", "Yes", "Yes", "Yes"],
            "Fixed effects": ["None", "None", "Unit+Year", "Unit+Year", "Unit+Year"],
            "Sample":        ["Full", "Full", "Full", "Full", "Balanced"],
        },
        notes = (
            "Standard errors in parentheses, clustered at the unit level. "
            "*** p<0.01, ** p<0.05, * p<0.10."
        ),
    )
    log.info("Wrote tab_main.tex")
