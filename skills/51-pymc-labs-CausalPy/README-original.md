<!-- Vendored into AERS from https://github.com/pymc-labs/CausalPy on 2026-06-01. Upstream attribution + license preserved. -->

> **Vendored upstream skill.** Curated snapshot of [`pymc-labs/CausalPy`](https://github.com/pymc-labs/CausalPy) for the AERS catalog (license: Apache-2.0). Vendored 2026-06-01. The original upstream README follows verbatim.

---

<div align="center">
  <a href="https://github.com/pymc-labs/CausalPy"><img width="40%" src="https://raw.githubusercontent.com/pymc-labs/CausalPy/main/docs/source/_static/logo.png"></a>
</div>

----

[![PyPI version](https://badge.fury.io/py/CausalPy.svg)](https://badge.fury.io/py/CausalPy)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/causalpy.svg?color=green)](https://anaconda.org/conda-forge/causalpy)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

![Build Status](https://github.com/pymc-labs/CausalPy/actions/workflows/ci.yml/badge.svg?branch=main)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![Interrogate](https://raw.githubusercontent.com/pymc-labs/CausalPy/interrogate-badges/interrogate_badge.svg)
[![codecov](https://codecov.io/gh/pymc-labs/CausalPy/branch/main/graph/badge.svg?token=FDKNAY5CZ9)](https://codecov.io/gh/pymc-labs/CausalPy)

![GitHub Repo stars](https://img.shields.io/github/stars/pymc-labs/causalpy?style=flat)
![Read the Docs](https://img.shields.io/readthedocs/causalpy)
[![Downloads](https://static.pepy.tech/badge/causalpy)](https://pepy.tech/project/causalpy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/causalpy)

<!-- docs-start -->

# Causal Inference for Quasi-Experiments

**Research-grade causal inference workflows** for quasi-experimental designs in Python.

CausalPy helps you estimate causal effects with transparent assumptions, uncertainty-aware modeling, and reproducible outputs:

- **Quasi-experimental methods:** Difference-in-differences, synthetic control, regression discontinuity, interrupted time series, instrumental variables, and more
- **Bayesian-first estimation** via [PyMC](https://www.pymc.io/) with full uncertainty quantification, plus traditional OLS via [scikit-learn](https://scikit-learn.org)
- **Decision-ready outputs:** Effect summaries with credible intervals (HDI), practical significance (ROPE), and publication-quality plots

## 📞 [**Book a consulting call**](https://calendly.com/benjamin-vincent/causalpy)

CausalPy is built and maintained by [PyMC Labs](https://www.pymc-labs.com). If your team is exploring a consulting engagement for lift testing, complex or high-stakes causal work, you can book an introductory call. _These calls are for consulting inquiries only. For technical usage questions and free community support, please use GitHub Discussions and the documentation below._

## Help and documentation

- Ask usage questions in [GitHub Discussions Q&A](https://github.com/pymc-labs/CausalPy/discussions/categories/q-a) so the issue tracker stays focused on bugs and enhancements.
- Report bugs and feature requests in [Issues](https://github.com/pymc-labs/CausalPy/issues)
- Browse detailed guides in the [documentation](https://causalpy.readthedocs.io)

## Installation

To get the latest release:

```bash
pip install CausalPy
```

or via conda:

```bash
conda install causalpy -c conda-forge
```

Alternatively, if you want the very latest version of the package you can install from GitHub:

```bash
pip install git+https://github.com/pymc-labs/CausalPy.git
```

## AI Agent Skills

CausalPy includes agent skills that teach AI coding assistants how to use the library for causal inference. Skills are available via [Decision AI Hub](https://hub.decision.ai) and live in `causalpy/skills/` in the source tree.

## Quickstart

```python
import causalpy as cp
import matplotlib.pyplot as plt

# Import and process data
df = (
    cp.load_data("drinking")
    .rename(columns={"agecell": "age"})
    .assign(treated=lambda df_: df_.age > 21)
)

# Run the analysis
result = cp.RegressionDiscontinuity(
    df,
    formula="all ~ 1 + age + treated",
    running_variable_name="age",
    model=cp.pymc_models.LinearRegression(),
    treatment_threshold=21,
)

# Visualize the causal effect at the threshold
fig, ax = result.plot()

# Get a results summary with posterior estimates
result.summary()
```

The `result.plot()` visualizes the regression discontinuity design, showing the estimated jump at the treatment threshold. The `result.summary()` prints posterior estimates of the causal effect with uncertainty intervals.

## Videos

Click on the thumbnail below to watch a video about CausalPy on YouTube.

[![Youtube video thumbnail image](https://img.youtube.com/vi/gV6wzTk3o1U/maxresdefault.jpg)](https://www.youtube.com/watch?v=gV6wzTk3o1U)

## When CausalPy is a good fit

- You have a plausible quasi-experimental design (threshold rule, policy change, staggered rollout, geo lift, etc.)
- You want uncertainty-aware estimates and diagnostics, not only point estimates
- You need reproducible analysis artifacts for review and communication

## When CausalPy is not a fit

- You need causal discovery from weakly identified observational data
- You want fully automated "black box" causal answers without specifying assumptions
- You primarily need production workflow tooling (pipelines, governance, multi-user collaboration)

## Methods and Workflows

CausalPy provides methods for common causal inference decision contexts:

| Decision context | Methods |
|------------------|---------|
| Focussed testing on certain units (geos, products) | Synthetic control, Geographical lift |
| Evaluate before/after changes, launches, policy changes | Differences in Differences, Staggered DiD, Interrupted time series |
| Exploit cutoff rules, score-based eligibility (credit, age) | Regression discontinuity, Regression kink |
| Can't randomize, correct for selection | Instrumental variables, Inverse propensity weighting |
| Group differences, control for covariates | ANCOVA |

### Available methods

| Method | Description |
|-|-|
| Synthetic control | Constructs a synthetic version of the treatment group from a weighted combination of control units. Used for causal inference in comparative case studies when a single unit is treated, and there are multiple control units. |
| Geographical lift | Measures the impact of an intervention in a specific geographic area by comparing it to similar areas without the intervention. Commonly used in marketing to assess regional campaigns. |
| ANCOVA | Analysis of Covariance combines ANOVA and regression to control for the effects of one or more quantitative covariates. Used when comparing group means while controlling for other variables. |
| Differences in Differences | Compares the changes in outcomes over time between a treatment group and a control group. Used in observational studies to estimate causal effects by accounting for time trends. |
| Staggered Difference-in-Differences | Estimates event-time treatment effects when different units adopt treatment at different times, using an imputation approach that models untreated outcomes and compares observed outcomes to counterfactual predictions. |
| Regression discontinuity | Identifies causal effects by exploiting a cutoff or threshold in an assignment variable. Used when treatment is assigned based on a threshold value of an observed variable, allowing comparison just above and below the cutoff. |
| Regression kink designs | Focuses on changes in the slope (kinks) of the relationship between variables rather than jumps at cutoff points. Used to identify causal effects when treatment intensity changes at a threshold. |
| Interrupted time series | Analyzes the effect of an intervention by comparing time series data before and after the intervention. Used when data is collected over time and an intervention occurs at a known point, allowing assessment of changes in level or trend. |
| Instrumental variable regression | Addresses endogeneity by using an instrument variable that is correlated with the endogenous explanatory variable but uncorrelated with the error term. Used when explanatory variables are correlated with the error term, providing consistent estimates of causal effects. |
| Inverse Propensity Score Weighting | Weights observations by the inverse of the probability of receiving the treatment. Used in causal inference to create a synthetic sample where the treatment assignment is independent of measured covariates, helping to adjust for confounding variables in observational studies. |

## Diagnostics-first by design

CausalPy emphasizes transparent, uncertainty-aware outputs for rigorous causal analysis:

- **Effect summaries:** Every experiment provides `effect_summary()` returning decision-ready statistics with both tabular and prose formats
- **Uncertainty quantification:** Bayesian models report HDI (Highest Density Intervals); OLS models report confidence intervals
- **Practical significance:** ROPE (Region of Practical Equivalence) analysis to assess whether effects exceed meaningful thresholds
- **Direction testing:** Tail probabilities (e.g., P(effect > 0)) for directional inference

## Citing CausalPy

If you use CausalPy in your research, please cite it. A Zenodo DOI for stable releases is planned. In the meantime, you can cite the repository:

```bibtex
@software{causalpy,
  author = {{PyMC Labs}},
  title = {CausalPy: Causal inference for quasi-experiments in Python},
  url = {https://github.com/pymc-labs/CausalPy},
  year = {2026}
}
```

## Roadmap

Plans for the repository can be seen in the [Issues](https://github.com/pymc-labs/CausalPy/issues).

## License

[Apache License 2.0](https://github.com/pymc-labs/CausalPy/blob/main/LICENSE)

## Thanks to our contributors

<a href="https://github.com/pymc-labs/CausalPy/graphs/contributors">
  <img src="https://raw.githubusercontent.com/pymc-labs/CausalPy/main/docs/source/_static/contributors.svg" alt="CausalPy contributors" />
</a>

The contributor image is regenerated weekly by a GitHub Actions workflow (`.github/workflows/contributors.yml`) that opens a PR when the contributor list changes.
