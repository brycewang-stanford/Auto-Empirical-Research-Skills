# Methods coverage matrix

One place to see, for every method the stack teaches, the runnable demo that
pins it to a known truth, the skill that routes to it, the verified reference,
and the StatsPAI tool that executes it. This is the navigational dual of the
machine-generated [quality scorecard](./quality-scorecard.md): the scorecard
counts, this page maps.

Every demo below runs under the numeric-correctness contract — it asserts an
estimate against a known target and fails the smoke gate otherwise (see
[`examples/README.md`](../examples/README.md)). Estimator defaults and per-stack
package calls are in the [methods reference](./methods-reference.md); term
definitions are in the [glossary](./glossary.md).

## Identification designs

| Method | Demo | Skill | Reference | StatsPAI tool |
|---|---|---|---|---|
| Staggered DiD, forbidden comparison | [`staggered-did-demo/`](../examples/staggered-did-demo/) | `aer-identification` | `goodmanbacon_2021`, `callaway_santanna_2021` | `callaway_santanna`, `bacon_decomposition` |
| Sun-Abraham interaction-weighted event study | [`sun-abraham-demo/`](../examples/sun-abraham-demo/) | `aer-identification` | `sun_abraham_2021` | `sun_abraham` |
| LP-DiD (clean-control local projections) | [`lp-did-demo/`](../examples/lp-did-demo/) | `aer-identification` | `dube_girardi_jorda_taylor_2023`, `jorda_2005` | `lp_did` |
| Weak-IV-robust inference (Anderson-Rubin) | [`iv-weak-instrument-demo/`](../examples/iv-weak-instrument-demo/) | `aer-identification` | `andrews_stock_sun_2019` | `anderson_rubin_ci`, `effective_f_test` |
| RDD polynomial order | [`rdd-polynomial-demo/`](../examples/rdd-polynomial-demo/) | `aer-identification` | `gelman_imbens_2019`, `calonico_cattaneo_titiunik_2014` | `rdrobust` |
| Synthetic control placebo inference | [`synthetic-control-demo/`](../examples/synthetic-control-demo/) | `aer-identification` | `abadie_diamond_hainmueller_2010` | `synth`, `synth_time_placebo` |
| Shift-share shock-level inference | [`shift-share-demo/`](../examples/shift-share-demo/) | `aer-identification` | `adao_kolesar_morales_2019` | `bartik` |
| Matrix completion (interactive FE) | [`matrix-completion-demo/`](../examples/matrix-completion-demo/) | `aer-identification` | `athey_etal_2021` | `matrix_completion`, `interactive_fe` |
| Bunching at a kink | [`bunching-demo/`](../examples/bunching-demo/) | `aer-identification` | `saez_2010`, `kleven_2016` | `bunching`, `notch` |
| DML partially linear + cross-fitting | [`dml-plr-demo/`](../examples/dml-plr-demo/) | `aer-identification` | `chernozhukov_etal_2018`, `robinson_1988` | `dml` |
| Quantile treatment effects | [`qte-demo/`](../examples/qte-demo/) | `aer-identification` | `koenker_bassett_1978` | `qte` |

## Robustness, inference, and sensitivity

| Method | Demo | Skill | Reference | StatsPAI tool |
|---|---|---|---|---|
| Honest DiD pre-trends bounds | [`honest-did-demo/`](../examples/honest-did-demo/) | `aer-robustness` | `rambachan_roth_2023` | `honest_did` |
| Oster δ coefficient-stability bounding | [`oster-ovb-demo/`](../examples/oster-ovb-demo/) | `aer-robustness` | `oster_2019` | `oster_delta`, `oster_bounds` |
| Cinelli-Hazlett robustness value (partial R²) | [`sensitivity-rv-demo/`](../examples/sensitivity-rv-demo/) | `aer-robustness` | `cinelli_hazlett_2020` | `robustness_value` |
| Lee bounds under differential attrition | [`lee-bounds-demo/`](../examples/lee-bounds-demo/) | `aer-robustness` | `lee_2009` | `lee_bounds` |
| Few-cluster wild bootstrap | [`few-clusters-demo/`](../examples/few-clusters-demo/) | `aer-robustness` | `cameron_gelbach_miller_2008`, `mackinnon_webb_2017` | `wild_cluster_bootstrap` |
| Multiple-testing FWER control | [`multiple-testing-demo/`](../examples/multiple-testing-demo/) | `aer-robustness` | `list_shaikh_xu_2019`, `romano_wolf_2005` | `romano_wolf` |
| Specification curve | [`spec-curve-demo/`](../examples/spec-curve-demo/) | `aer-robustness` | `simonsohn_simmons_nelson_2020` | `spec_curve` |
| Randomization (Fisher) inference | [`randomization-inference-demo/`](../examples/randomization-inference-demo/) | `aer-robustness` | `young_2019` | `ri_test` |

## Ex-ante design

| Method | Demo | Skill | Reference | StatsPAI tool |
|---|---|---|---|---|
| Power / minimum detectable effect + Type-M | [`power-mde-demo/`](../examples/power-mde-demo/) | `aer-preregistration` | `mckenzie_2012`, `duflo_glennerster_kremer_2007` | — (design, not estimation) |

## How to read this

- **Demo** is runnable and asserted; start there to see the failure mode and the
  fix side by side.
- **Skill** is the routing entry point — it decides *whether* the method fits
  before any code runs.
- **Reference** is a Crossref-verified key in [`../references.bib`](../references.bib);
  no citation here is written from memory.
- **StatsPAI tool** is the validated execution surface (registry:
  [`../scripts/statspai_tools.txt`](../scripts/statspai_tools.txt), hub:
  [`../skills/aer-statspai/SKILL.md`](../skills/aer-statspai/SKILL.md)); the
  method skill binds to it rather than hand-rolling the estimator.
