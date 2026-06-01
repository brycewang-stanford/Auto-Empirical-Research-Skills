---
name: lifelines
description: Complete survival analysis library in Python. Handles right-censored data, Kaplan-Meier curves, and Cox regression. Standard for clinical trial analysis and epidemiology.
version: 0.28
license: MIT
---

# Lifelines - Survival Analysis

In medicine, we often care about "Time to Event" (death, recovery, relapse). Lifelines handles the complexity of "censored" data (patients who left the study).

## When to Use

- Analyzing clinical trial data (time to death, disease progression).
- Comparing survival between treatment groups.
- Identifying risk factors using Cox Proportional Hazards regression.
- Building survival models for prognosis.
- Epidemiology studies (time to infection, recovery).

## Core Principles

### Censoring

Patients who haven't experienced the event by the end of the study are "censored". Lifelines properly accounts for this.

### Hazard Ratios

In Cox regression, a hazard ratio > 1 means increased risk; < 1 means decreased risk.

### Survival Curves

Kaplan-Meier estimates the probability of survival over time without assuming a distribution.

## Quick Reference

### Standard Imports

```python
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
import pandas as pd
```

### Basic Patterns

```python
# 1. Kaplan-Meier (Visualizing survival)
kmf = KaplanMeierFitter()
kmf.fit(durations=df['days'], event_observed=df['died'])
kmf.plot_survival_function()
kmf.median_survival_time_  # Time when 50% have died

# 2. Cox Proportional Hazards (Risk factors)
cph = CoxPHFitter()
cph.fit(df, duration_col='days', event_col='died')
cph.print_summary() # See hazard ratios for age, drug type, etc.
cph.plot_partial_effects_on_outcome(covariates=['age'], values=[30, 50, 70])
```

## Critical Rules

### ✅ DO

- **Use event_observed correctly** - 1 = event occurred, 0 = censored.
- **Check proportional hazards assumption** - Use `cph.check_assumptions()` to validate Cox model.
- **Compare groups with logrank test** - Statistical test for survival curve differences.
- **Plot confidence intervals** - Survival estimates have uncertainty, especially with small samples.

### ❌ DON'T

- **Don't ignore censoring** - Treating censored patients as "survived" biases results.
- **Don't use regular regression** - Time-to-event data requires specialized methods.
- **Don't assume proportional hazards** - If violated, use stratified Cox or parametric models.

## Advanced Patterns

### Comparing Multiple Groups

```python
from lifelines.statistics import multivariate_logrank_test

# Compare survival across treatment groups
results = multivariate_logrank_test(df['days'], df['group'], df['died'])
print(results.p_value)
```

### Parametric Models

```python
from lifelines import WeibullFitter, ExponentialFitter

# When you need to extrapolate beyond observed data
wf = WeibullFitter()
wf.fit(df['days'], df['died'])
wf.plot()
```

Lifelines transforms complex survival data into actionable medical insights, enabling evidence-based decisions in clinical research and practice.
