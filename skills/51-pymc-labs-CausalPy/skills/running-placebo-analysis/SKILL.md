---
name: running-placebo-analysis
description: Performs placebo-in-time sensitivity analysis with hierarchical null model and optional Bayesian assurance. Use when checking model robustness, verifying lack of pre-intervention effects, or estimating study power.
---

# Running Placebo Analysis

Executes placebo-in-time sensitivity analysis using the core `PlaceboInTime` check. Builds a hierarchical Bayesian model of the "status quo" (no-effect) distribution, then compares the actual intervention effect against that learned null. Optionally computes Bayesian assurance (operating characteristics).

## Workflow

1.  **Fit your experiment**: Run a CausalPy experiment (ITS, SC) with a PyMC model.
2.  **Configure the check**: Create a `PlaceboInTime` with `n_folds`, optional `experiment_factory`, and optional assurance parameters.
3.  **Run**: Call `.run(experiment)` (standalone) or use within a `Pipeline` + `SensitivityAnalysis`.
4.  **Evaluate**: Inspect the null distribution (`theta_new`), `p_effect_outside_null`, and optional assurance results.

## Key Concepts

*   **Placebo-in-time**: Simulating an intervention at a time when none occurred to check if the model falsely detects an effect.
*   **Hierarchical null model**: A Bayesian model fitted on fold-level summaries that characterises the distribution of effects under no intervention.
*   **Assurance**: Bayesian operating characteristics — the probability of correctly detecting a real effect given your expected-effect prior and ROPE.
*   **Factory Pattern**: Decouples the placebo logic from the specific CausalPy experiment type.

## References

*   [Placebo-in-time Implementation](reference/placebo_in_time.md): Core API reference, usage examples, and hierarchical status-quo modeling.
