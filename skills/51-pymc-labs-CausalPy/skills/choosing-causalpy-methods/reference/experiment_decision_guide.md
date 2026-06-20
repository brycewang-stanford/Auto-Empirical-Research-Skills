# Experiment Decision Guide

Use this guide when an agent needs to choose a CausalPy experiment before writing analysis code. Prefer the simplest design that matches the data-generating story and has defensible identification assumptions.

## Time-Series Designs

| Situation | CausalPy class | Data shape | Main assumption | Common alternative |
|---|---|---|---|---|
| One outcome series, one intervention time, forecast counterfactual from pre-period | `InterruptedTimeSeries` | DataFrame indexed by time or with a time column | Pre-intervention trend model remains valid absent treatment | `PiecewiseITS` when estimating explicit level/slope changes in the full series |
| Known level or slope changes, possibly multiple interruptions | `PiecewiseITS` | Single time series with time variable used in `step()` / `ramp()` formula terms | Functional form captures untreated trend plus intervention changes | `InterruptedTimeSeries` when the goal is pre-period forecasting |
| Treated series plus donor units measured over time | `SyntheticControl` | Wide panel, columns are units | Donor pool can reproduce treated pre-period and supports counterfactual | `SyntheticDifferenceInDifferences` when time weights are part of the design |
| Synthetic-control setting with unit weights and pre-period time weights | `SyntheticDifferenceInDifferences` | Wide panel, columns are units | Weighted controls and weighted pre-periods provide a credible counterfactual | `SyntheticControl` for simpler donor-weight-only analysis |

## Panel And Group Designs

| Situation | CausalPy class | Data shape | Main assumption | Common alternative |
|---|---|---|---|---|
| One treated group and one control group before/after treatment | `DifferenceInDifferences` | Long panel or repeated group-time observations with treatment and post indicators | Parallel trends between treated and control groups | `StaggeredDifferenceInDifferences` for staggered adoption |
| Units adopt treatment at different times | `StaggeredDifferenceInDifferences` | Long unit-time panel with treatment timing | Parallel trends, no anticipation, absorbing treatment | `PanelRegression` for fixed-effects association or simpler adjustment |
| Fixed-effects regression is the analysis target | `PanelRegression` | Long panel with unit identifiers and optional time identifiers | Fixed effects control relevant unit/time confounding | DiD variants when treatment timing is central |
| Treated/control groups with baseline and post outcome | `PrePostNEGD` | Cross-sectional or group data with pre and post outcomes | Baseline outcome adjustment captures pre-existing group differences | `DifferenceInDifferences` when repeated observations over time are available |

## Threshold And Cross-Sectional Designs

| Situation | CausalPy class | Data shape | Main assumption | Common alternative |
|---|---|---|---|---|
| Treatment switches at a cutoff in a running variable | `RegressionDiscontinuity` | Cross-section or repeated observations with running variable and threshold | Units near cutoff are comparable and cannot precisely manipulate assignment | `RegressionKink` when slope changes rather than treatment level |
| Treatment intensity changes slope at a threshold | `RegressionKink` | Cross-section or repeated observations with running variable and kink point | Smooth potential outcomes around the kink absent treatment-intensity change | `RegressionDiscontinuity` for jump discontinuities |
| Endogenous treatment with valid instrument | `InstrumentalVariable` | DataFrame for outcome/treatment covariates plus instruments | Instrument relevance, exclusion, and no unblocked instrument-outcome path | `InversePropensityWeighting` if treatment is confounded but not instrumented |
| Observed binary treatment with measured confounders | `InversePropensityWeighting` | Cross-section or panel rows with treatment, outcome, and confounders | Conditional exchangeability and overlap/positivity | Outcome regression or doubly robust workflows when available |

## Method Selection Questions

- Is treatment assigned by time, by unit, by threshold, by instrument, or by observed covariates?
- Is the estimand a total post-period impact, an event-study path, a local threshold effect, or an adjusted treatment contrast?
- Are controls actual untreated units, donor time series, never-treated cohorts, or measured covariates?
- Does the data have enough pre-treatment history to support trend, donor, or placebo checks?
- Is the assignment mechanism credible enough for causal language, or should the agent frame the result as descriptive?

## Handoff To Execution

After selecting a method, use `running-causalpy-experiments` for the concrete workflow: data preparation, constructor arguments, model choice, scale-aware priors, summaries, plots, effect summaries, and sensitivity checks.
