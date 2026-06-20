# AERS Eval-Harness (executable layer)

A lightweight, **dependency-free** evaluation harness for the flagship skills in
this repo. It answers the question a maintainer of a 1,052-skill collection
actually has to answer: *do these skills make an agent produce correct,
referee-proof empirical work — or just plausible-looking text?*

> Two complementary eval layers live in this repo. `docs/EVALS.md` (generated
> from `evals/flagship-evals.json`) is the **declarative** layer: it defines, per
> flagship skill, a prompt + the expected artifacts and human/agent review checks
> — expectations, not an automatic grade. This `eval-harness/` is the
> **executable** layer: it auto-grades machine-checkable rubric items and emits
> judge prompts for the rest. Use the declarative matrix to know *what good looks
> like*; use the harness to *enforce it in CI*. The numeric counterpart is
> [`benchmark/`](../benchmark/).

## Why rubric-based?

The skills here are **prompt-context, not executable code**. There is no
function to unit-test. What you *can* test is whether an agent that has the skill
loaded produces output with the right **properties**: it refuses to headline a
naive TWFE estimate under staggered timing, it reports a first-stage F and
switches to weak-IV-robust inference when the instrument is weak, it compresses
an AER abstract to ≤ 100 words, it lowers Chinese AI-writing markers without
touching the facts, it avoids fake citation metadata, and it refuses unsafe
runtime instructions for untrusted replication packages.

So each eval is a **scenario** (a realistic user request) plus a **rubric** (a
list of checkable properties). Rubric items are one of:

- **machine-checkable** — deterministic regex / word-count / numeric assertions
  that the harness verifies with no API key (see [`lib/checks.py`](lib/checks.py)).
- **`manual`** — needs a human or an LLM judge. The harness never silently
  passes these; it emits a ready-to-paste judge prompt instead.

When a candidate passes every machine-checkable item but still has unresolved
manual rubric items, the scorecard status is `needs-manual`, not `pass`.
`pass` means no required failures, no partial machine score, and no open manual
items.

This is deliberately a *necessary-not-sufficient* gate. Passing every
machine-checkable item does not prove an answer is correct; **failing** a
required one proves it is wrong (e.g. it endorsed an `F = 8` instrument as
strong). That asymmetry is exactly what you want from a cheap, always-on CI gate.

## Layout

```
eval-harness/
  run_evals.py            # the harness (dependency-free; uses scripts/toml_compat.py)
  lib/checks.py           # machine-checkable rubric primitives
  schema/scenario.schema.json   # documents the scenario shape
  scenarios/*.toml        # one file per scenario; stem == id
  candidates/_example/    # sample agent outputs (fixtures for the grader)
  results/                # generated scorecards (results.json + RESULTS.md)
```

## Run it

```bash
# 1. Lint every scenario + coverage report (stdlib-only; needs no outputs)
python3 eval-harness/run_evals.py

# 1b. CI lint gate: fail if scenario/category/auto-check coverage regresses
python3 eval-harness/run_evals.py \
  --min-scenarios 17 --min-auto-checks 80 \
  --expect-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity,writing-compliance,writing-style

# 2. List scenarios
python3 eval-harness/run_evals.py --list

# 3. Grade candidate agent outputs (one file per scenario: <id>.md or <id>.txt)
python3 eval-harness/run_evals.py --grade eval-harness/candidates/_example
#    -> writes eval-harness/results/RESULTS.md and results.json

# 3b. CI smoke: only the deliberately weak fixture may fail required items
python3 eval-harness/run_evals.py --grade eval-harness/candidates/_example \
  --expect-graded 8 --expect-fail-required statspai-weak-iv \
  --expect-graded-categories causal-identification,reproducibility,citation-hygiene,runtime-safety,research-integrity \
  --fail-on-orphans --fail-on-partial --no-write

# 4. Emit judge prompts for the manual items (paste into any LLM or hand to a human)
python3 eval-harness/run_evals.py --judge-prompts /tmp/judge --grade eval-harness/candidates/_example

# 5. Auto-grade the manual items with an LLM judge (optional; degrades gracefully)
ANTHROPIC_API_KEY=sk-... python3 eval-harness/run_evals.py --grade eval-harness/candidates/_example --judge
#    needs `pip install anthropic`; without a key it just grades machine-checkable items
```

To evaluate a real agent: run each scenario's `prompt` against your agent with
the named skill loaded, save the reply as `candidates/<run-name>/<id>.md`, then
`--grade candidates/<run-name>`.

For fixture directories used in CI, add `--fail-on-orphans` so typoed or stale
`*.md` / `*.txt` files whose stem no longer matches a scenario id cannot be
silently ignored. Add `--fail-on-partial` when fixture outputs should keep all
machine-checkable, non-required rubric items green too.
Add `--no-write` when the gate should avoid touching generated scorecards under
`eval-harness/results/`.

## Authoring a scenario

Scenarios are TOML so prompts and regexes stay readable (no escaping pain). The
file stem **must** equal the `id`. Minimal shape:

```toml
id = "statspai-weak-iv"
skill = "skills/00-Full-empirical-analysis-skill_StatsPAI"
title = "Weak instrument must trigger weak-IV-robust inference"
category = "causal-identification"
severity = "critical"        # critical | high | medium | low
prompt = """ ...the user request handed to the agent... """

[[rubric]]
id = "flags-weak-instrument"
check = "regex_any"          # see check types below
required = true              # a failed required item fails the whole scenario
weight = 4
description = "Flags F~8 as weak."
patterns = ['(?i)weak instrument', '(?i)below (the )?(threshold|10|23)']
```

`skill` must be a repo-relative path to an existing skill directory. If
`context_data` is present, it must be an array of repo-relative paths that exist
and stay inside the repo; absolute paths and `..` escapes are rejected. `rubric`
must be an array of TOML tables (`[[rubric]]`), even for a single item.

### Check types (`lib/checks.py`)

| check | passes when |
|---|---|
| `regex_any` | at least one `patterns` entry matches |
| `regex_all` | every `patterns` entry matches |
| `regex_none` | no `patterns` entry matches (forbidden content absent) |
| `regex_count_max` | total matches of `pattern` ≤ `target` (optionally per `per_chars`) |
| `word_count_max` / `word_count_min` | unit count of section/doc within `target` (`unit` = words\|chars\|cjk) |
| `numeric_tolerance` | number from `extract` (group 1) is within `tol` of `expected` |
| `numeric_sign` | number from `extract` has the expected `sign` |
| `manual` | never auto-passes; routed to a judge with `guidance` |

`section` (a regex whose group 1 is captured) scopes a check to part of the
output — e.g. count cliché phrases only in the rewritten body, not in a change
summary that quotes them. If `section` does not match, the check falls back to
the whole document.

## Honest limitations

- Regex rubric items are coarse by design. They catch the **specific failure
  modes** the flagship skills exist to prevent; they do not certify overall
  quality. Treat green machine-checks as "didn't trip a known wire," and use the
  `manual` items + judge prompts for substance.
- Scenarios are pinned to skill content that was verified to exist at authoring
  time. When a skill's methodology changes, update the matching scenario.
- `candidates/_example/` is a fixture set (some good, one deliberately weak) used
  to prove the grader discriminates — not a real model run.
