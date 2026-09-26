---
name: New ground-truth dataset
about: Contribute a generated dataset with a known effect
labels: enhancement, dataset
---

**Design**: ols / rct / did / staggered / rdd / iv

**DGP** (units, periods, error structure, what is endogenous)

**True effect**: 0 (null) or a known value (positive control)

**Generator**: a function for `scripts/make_null_data.py` with a fixed seed

**Card**: the `preregistered` block and the axes you consider defensible
