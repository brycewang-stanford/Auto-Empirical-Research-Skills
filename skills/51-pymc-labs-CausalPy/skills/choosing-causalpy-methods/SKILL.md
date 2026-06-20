---
name: choosing-causalpy-methods
description: Choose the appropriate CausalPy experiment class from a causal question, data structure, treatment assignment, and identification assumptions. Use before writing analysis code when the method is not yet settled.
---

# Choosing CausalPy Methods

Use this skill to translate a user's causal question into a CausalPy experiment choice. This is the design-intake skill, not the implementation skill. Once the method is chosen, hand off to `running-causalpy-experiments` for constructor details, model configuration, priors, summaries, plots, and interpretation.

## Intake Checklist

1. Restate the estimand: ATE, ATT, local threshold effect, treatment-on-treated over time, cumulative impact, or a policy/campaign lift.
2. Identify the data shape: single time series, wide panel of units, long panel of unit-time rows, cross-section, or pre/post group data.
3. Identify treatment assignment: known intervention time, staggered adoption, threshold/cutoff, kink, instrument, observed treatment with confounders, or treated unit plus donor pool.
4. Check the identifying story: parallel trends, no anticipation, no manipulation at cutoff, valid instrument, overlap/positivity, convex hull/donor support, or trend continuity.
5. Recommend one primary CausalPy experiment and any plausible alternatives, then explain the extra data or assumptions needed to choose among them.

## Fast Routing

- One treated time series, known intervention time, no donor pool: `InterruptedTimeSeries`.
- Known level/slope changes in one time series, especially multiple interruptions: `PiecewiseITS`.
- Treated and control groups observed before and after one intervention: `DifferenceInDifferences`.
- Units adopt treatment at different times: `StaggeredDifferenceInDifferences`.
- One or more treated units with multiple untreated donor units in wide panel format: `SyntheticControl`.
- Synthetic-control setting where both unit weights and pre-period time weights are part of the design: `SyntheticDifferenceInDifferences`.
- Panel regression or fixed-effects adjustment is the target rather than a named quasi-experimental design: `PanelRegression`.
- Pretest/posttest nonequivalent groups with a baseline outcome: `PrePostNEGD`.
- Treatment assigned by crossing a cutoff in a running variable: `RegressionDiscontinuity`.
- Treatment intensity changes slope at a threshold rather than jumping in level: `RegressionKink`.
- Treatment is endogenous but there is a credible instrument: `InstrumentalVariable`.
- Observational binary treatment with measured confounders and overlap: `InversePropensityWeighting`.

## Output Pattern

When you use this skill, return:

- Recommended method: name the CausalPy experiment class.
- Why it fits: tie the recommendation to data shape, assignment mechanism, and estimand.
- Required columns/data layout: list the minimal data structure needed.
- Key assumptions: state what must be credible for a causal interpretation.
- Main risks: name obvious failure modes or sensitivity checks.
- Next step: route to `running-causalpy-experiments` and the relevant method reference.

## References

- [Experiment decision guide](reference/experiment_decision_guide.md)
