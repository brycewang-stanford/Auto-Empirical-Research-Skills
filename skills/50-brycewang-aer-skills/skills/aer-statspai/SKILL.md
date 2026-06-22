---
name: aer-statspai
description: Use when implementing or running the empirical analysis for an AER-track manuscript with StatsPAI — the agent-native unified Python engine and MCP server for causal inference and econometrics — as an alternative to hand-written Stata / R / Python template code. Covers DiD, IV, RDD, synthetic control, robustness, sensitivity, and publication-ready table export.
---

# AER StatsPAI

## Overview

`aer-statspai` is the **implementation engine** option for this stack. Where
`aer-identification` and `aer-robustness` decide *which* estimator and *which*
diagnostics a referee will demand, this skill is about *running* them — through
[StatsPAI](https://github.com/brycewang-stanford/StatsPAI), an open-source,
agent-native Python platform that exposes 1,000+ causal-inference and
econometrics functions behind one unified API, plus a machine-readable MCP
server an agent can drive directly.

It is **one more choice**, not a replacement. The Stata / R / Python templates in
`templates/` remain the default for users who want drop-in, version-pinned
scripts. Reach for StatsPAI when you want a single Python surface that covers the
whole AER identification toolkit, self-describes its assumptions to an agent, and
exports publication-ready LaTeX / Word / Excel tables from the estimator object.

This skill does **not** override the methodology. The modern-default rules in
`aer-identification` (no TWFE on staggered data, Anderson-Rubin under weak IV,
local-linear RDD, placebo inference for SCM) still bind. StatsPAI executes those
rules; it does not relax them.

## When to Use

- You want to **run** the empirical analysis interactively from the agent, not
  just receive template code to run later by hand
- You want one Python dependency covering DiD, IV, RDD, SCM, matching, DML, and
  causal forests instead of stitching together `fixest`, `did`, `rdrobust`,
  `linearmodels`, and `scdata`
- A StatsPAI MCP server is connected (tools prefixed `statspai`) and you can
  chain `detect_design → recommend → fit → audit_result → sensitivity → bibtex`
- You need publication-ready tables straight from the estimator object
  (`.to_latex()`, `.to_docx()`, `.to_excel()`) to hand to `aer-tables-figures`

## When NOT to Use

- The deposited replication package must be **Stata-only** (some coauthors /
  Data Editor workflows assume `.do` files) → use `templates/stata/`
- You want exact, pinned, language-native scripts to commit verbatim into an
  openICPSR deposit → use `templates/python/`, `templates/r/`, or
  `templates/stata/`
- The methodological *choice* is the open question — go to `aer-identification`
  first; come back here to execute once the design is fixed

## Install and Connect

Two ways to use StatsPAI; they share the same estimators.

```bash
pip install statspai
```

```python
import statspai as sp

df = sp.datasets.mpdta()                       # bundled teaching panel
cs = sp.callaway_santanna(data=df, y="lemp", t="year",
                          i="countyreal", g="first_treat")
print(sp.aggte(cs, type="simple").summary())   # staggered-robust ATT
```

**Agent-native (MCP) path.** When a StatsPAI MCP server is connected, the agent
calls the same methods as tools (`statspai` namespace) and gets back structured
result handles instead of parsing console output. This is the preferred path
inside an agent loop because every function publishes its assumptions,
preconditions, and failure modes for the agent to read before it runs.

## Recommended Agent-Native Workflow

Drive the MCP server as a chain, not as one-shot calls. Pass `as_handle=true`
(or `detail='agent'`) so each step returns a `result_id` the next step consumes —
no need to ferry betas, standard errors, or covariance matrices by hand.

1. **`detect_design`** — infer the study shape (DiD / IV / RDD / SCM / panel), or
   pass `design=` explicitly when you already know it.
2. **`preflight` + `recommend`** — surface design problems (no never-treated
   group, weak first stage, manipulation at the cutoff) and let the engine
   propose the modern-default estimator.
3. **Fit with `as_handle=true`** — e.g. `callaway_santanna`, `ivreg`,
   `rdrobust`, `synth`. You get a `result_id` you can chain downstream.
4. **`audit_result(result_id=...)`** — enumerate the robustness checks still
   missing; for each, call the `suggest_function` it emits. This is the
   referee-anticipation step from `aer-robustness`, automated.
5. **`honest_did_from_result` / `sensitivity_from_result`** — design-specific
   sensitivity (Rambachan-Roth honest bounds, Oster δ, etc.) directly off the
   handle.
6. **`bibtex(keys=[...])`** — pull verified citations for every estimator and
   diagnostic you used. **Never invent references** — `paper.bib` is the single
   source of truth.

Token economy: pass `detail='minimal'` on cheap sub-step calls; the default
`detail='agent'` carries the violations list and `next_steps` you actually need.

## Mapping AER Identification Strategies to StatsPAI

Each row keeps the modern default from `aer-identification`; StatsPAI is the
execution surface.

| Strategy | Modern default (see `aer-identification`) | StatsPAI entry point |
|---|---|---|
| Staggered DiD | Callaway-Sant'Anna ATT(g,t); never raw TWFE | `callaway_santanna`, `aggte`, `did_imputation`, `sun_abraham` |
| Forbidden-comparison check | Goodman-Bacon decomposition | `bacon_decomposition`, `bacon_plot` |
| Event study / pre-trends | Joint pre-period test, not just the plot | `event_study`, `pretrends_test`, `honest_did` |
| IV / weak instruments | Anderson-Rubin, not first-stage F > 10 | `ivreg`, `anderson_rubin_ci`, `effective_f_test`, `tF_adjustment` |
| Shift-share / Bartik | Rotemberg weights or shock-level inference | `bartik` |
| RDD | Local-linear, MSE-optimal bandwidth, RBC CI | `rdrobust`, `rdbwselect`, `rdplot`, `rddensity` (McCrary) |
| Synthetic control | Placebo inference; modern variants | `synth`, `gsynth`, `augsynth`, `sdid`, `synth_time_placebo`, `synth_loo` |
| DML / causal ML | Cross-fit nuisance; honest CIs | `dml`, `causal_forest`, `metalearner`, `tmle` |

When in doubt about *whether* an estimator is appropriate, that decision belongs
to `aer-identification`. This table is for *how* to run the one you've chosen.

## Robustness, Heterogeneity, Sensitivity

`audit_result` is the bridge to `aer-robustness`: it reads the fitted handle and
lists the checks a referee will expect — placebo, alternative samples,
heterogeneity by cohort, leave-one-out for SCM — emitting a `suggest_function`
for each. Drive that list to closure rather than guessing which robustness
checks to add.

For design-specific sensitivity, prefer the `*_from_result` tools so you never
re-specify the model:

- `honest_did_from_result` — Rambachan-Roth (2023) honest bounds for DiD
- `sensitivity_from_result` — Oster (2019) δ / unobserved-confounding bounds
- `evalue_from_result` — E-value for observational designs

## Publication Export — Hand Off to `aer-tables-figures`

StatsPAI result objects export directly, which removes manual table assembly:

```python
res.to_latex("output/tables/table3.tex")   # AER booktabs-compatible
res.to_docx("output/tables/table3.docx")
res.to_excel("output/tables/table3.xlsx")
```

The **house-style rules still come from `aer-tables-figures`** — column count,
note structure, significance-star policy, and the booktabs conventions. Use
StatsPAI to *emit* the table; use `aer-tables-figures` to decide what the table
should look like before you ship it.

## Validation Status — Read It Before Trusting a Number

StatsPAI labels every function with a `validation_status`. Treat these as a
trust tier, not decoration:

- **Certified** numerical evidence (benchmarked against Stata / R reference
  implementations) → safe for a main specification.
- **API-stable breadth** (broad coverage, not yet numerically certified
  end-to-end) → fine for exploration; **re-run the headline result against a
  reference implementation** (`templates/`) before it becomes a main table in a
  top-5 submission.

For an AER main result, cross-check at least the headline coefficient and its
inference against the language-native template. Convergent numbers across two
engines is itself a robustness signal a referee will respect.

## Red Flags

- Reporting a StatsPAI estimate as a main AER specification without confirming
  its `validation_status` is certified or cross-checking against `templates/`
- Letting the unified API tempt you into a *worse* estimator than
  `aer-identification` prescribes (e.g. plain TWFE because it is one call)
- Skipping `audit_result` and hand-picking robustness checks — the whole point
  of the agent-native loop is that it enumerates what you missed
- Pasting a citation StatsPAI did not return from `bibtex` — verified keys only

## Repository Resources

When working from the AER-skills repository or plugin bundle, load only the
relevant resource:

- Estimator defaults, diagnostics, and primary citations: `docs/methods-reference.md`
- The methodological decision that precedes execution: `skills/aer-identification/SKILL.md`
- Referee-anticipating checks `audit_result` should reproduce: `skills/aer-robustness/SKILL.md`
- House-style rules for the tables StatsPAI emits: `skills/aer-tables-figures/SKILL.md`
- Reference Python implementation to cross-check headline numbers: `templates/python/main_did.py`
- Pinned reference-engine dependencies: `templates/python/requirements.txt`

Use `aer-identification` to fix the design before running anything here; use
`docs/methods-reference.md` to confirm the estimand, diagnostic, and citation
the manuscript must report.

## Handoff

```text
ENGINE: StatsPAI (python-api | mcp)
DESIGN: <DiD | IV | RDD | SCM | DML | ...>
ESTIMATOR FUNCTION: <statspai function used>
VALIDATION STATUS: <certified | api-stable — cross-checked? yes/no>
AUDIT_RESULT CHECKS CLOSED: <list or "none">
SENSITIVITY RUN: <honest_did | oster | evalue | none>
TABLES EXPORTED: <paths or "none">
NEXT SKILL: aer-robustness (close audit) → aer-tables-figures (house style)
```

## Anti-Patterns

- Treating `aer-statspai` as a substitute for `aer-identification` — it executes
  the design, it does not choose it
- Shipping an `api-stable` result as a main top-5 table with no reference
  cross-check
- Using the unified API to add a fifth "robustness" estimator that shares the
  same identifying variation as the main result and calling it confirmation
- Exporting a table from StatsPAI and skipping `aer-tables-figures` — the engine
  emits a table, it does not enforce AER house style
