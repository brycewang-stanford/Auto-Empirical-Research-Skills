# Quality scorecard

<!-- GENERATED FILE. Edit scripts/quality_scorecard.py, then run: make scorecard -->

Machine-generated for **v1.5.0** by `scripts/quality_scorecard.py`; regenerate with `make scorecard`. Preflight fails if this page drifts from what the tooling measures.

## Headline numbers

| Metric | Value |
|---|---|
| Skills in the bundle | 15 |
| Skills at grade A (score >= 90) | 14 |
| Lowest skill-audit score (gate: >= 85) | 89.6 |
| Lowest substance-anchor count (gate: >= 8) | 9 |
| Runnable demos under the numeric-check contract | 20 |
| NUMERIC-CHECK assertions across demos | 88 |
| Verified bibliography entries | 50 |
| Recorded index responses (hermetic offline verification) | 52 |
| Citation gold tuples / groundedness cases | 12 / 15 |
| Validated StatsPAI tool bindings | 53 |
| Bundled skill depth references (self-contained installs) | 14 |
| Enforced quality gates | 10 |

## Gate inventory

| Gate | Command | What it enforces |
|---|---|---|
| Repository validator | `make validate` | structure, registration, dependency pins, manifest invariants, link integrity |
| Strict optional-tool coverage | `make validate-strict` | every optional tool documented and registered |
| SkillOpt routing gate | `make skillopt-gate` | routing scenarios select the intended skill |
| Skill document-quality floor | `make audit-skills-gate` | score >= 85 and >= 8 substance anchors per skill |
| Citation verification (offline) | `make verify-citations` | every bib entry matches its recorded Crossref response |
| Citation groundedness | `make verify-citations-groundedness` | every prose citation resolves to a verified bib entry |
| Example smoke + numeric contract | `make smoke-examples` | every demo runs and every NUMERIC-CHECK passes |
| Referee-simulation calibration | `make referee-calibration` | every scored referee run maps to the rubric verdict it states |
| Quality-tooling unit tests | `make test` | the validators themselves are tested |
| Scorecard drift | `make scorecard` | this page always matches what the tooling measures |

## Skill audit

| Skill | Score | Grade | Substance anchors |
|---|---|---|---|
| `aer-preregistration` | 100.0 | A | 22 |
| `aer-topic-selection` | 100.0 | A | 12 |
| `aer-tables-figures` | 99.7 | A | 36 |
| `aer-introduction` | 97.5 | A | 17 |
| `aer-submission` | 96.8 | A | 16 |
| `aer-robustness` | 96.6 | A | 15 |
| `aer-literature` | 96.3 | A | 9 |
| `aer-workflow` | 96.0 | A | 21 |
| `aer-consistency` | 95.8 | A | 34 |
| `aer-referee-sim` | 95.4 | A | 13 |
| `aer-replication` | 94.6 | A | 15 |
| `aer-rebuttal` | 93.9 | A | 10 |
| `aer-identification` | 93.6 | A | 12 |
| `aer-statspai` | 93.5 | A | 14 |
| `aer-paper-body` | 89.6 | B | 19 |

## Demo numeric contracts

| Demo | Script(s) | NUMERIC-CHECK assertions |
|---|---|---|
| [`bunching-demo/`](../examples/bunching-demo/) | bunching_demo.py | 4 |
| [`dml-plr-demo/`](../examples/dml-plr-demo/) | dml_plr_demo.py | 5 |
| [`few-clusters-demo/`](../examples/few-clusters-demo/) | few_clusters_demo.py | 4 |
| [`honest-did-demo/`](../examples/honest-did-demo/) | honest_did_demo.py | 4 |
| [`iv-weak-instrument-demo/`](../examples/iv-weak-instrument-demo/) | iv_weak_instrument_demo.py | 3 |
| [`lee-bounds-demo/`](../examples/lee-bounds-demo/) | lee_bounds_demo.py | 5 |
| [`lp-did-demo/`](../examples/lp-did-demo/) | lp_did_demo.py | 4 |
| [`matrix-completion-demo/`](../examples/matrix-completion-demo/) | matrix_completion_demo.py | 4 |
| [`multiple-testing-demo/`](../examples/multiple-testing-demo/) | multiple_testing_demo.py | 6 |
| [`oster-ovb-demo/`](../examples/oster-ovb-demo/) | oster_ovb_demo.py | 4 |
| [`power-mde-demo/`](../examples/power-mde-demo/) | power_mde_demo.py | 5 |
| [`qte-demo/`](../examples/qte-demo/) | qte_demo.py | 5 |
| [`randomization-inference-demo/`](../examples/randomization-inference-demo/) | randomization_inference_demo.py | 4 |
| [`rdd-polynomial-demo/`](../examples/rdd-polynomial-demo/) | rdd_polynomial_demo.py | 4 |
| [`sensitivity-rv-demo/`](../examples/sensitivity-rv-demo/) | sensitivity_rv_demo.py | 6 |
| [`shift-share-demo/`](../examples/shift-share-demo/) | shift_share_demo.py | 4 |
| [`spec-curve-demo/`](../examples/spec-curve-demo/) | spec_curve_demo.py | 4 |
| [`staggered-did-demo/`](../examples/staggered-did-demo/) | staggered_did_demo.R, staggered_did_demo.py | 5 |
| [`sun-abraham-demo/`](../examples/sun-abraham-demo/) | sun_abraham_demo.py | 4 |
| [`synthetic-control-demo/`](../examples/synthetic-control-demo/) | synthetic_control_demo.py | 4 |

Every assertion pins an estimate to a known truth within a stated tolerance; `make smoke-examples` fails a demo that emits none or reports a FAIL. See [`../examples/README.md`](../examples/README.md) for the contract and [`roadmap.md`](roadmap.md) for the operating definition these numbers serve.
