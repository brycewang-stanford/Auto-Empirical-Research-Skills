# SkillOpt Evaluation Protocol

This repository adapts the SkillOpt loop to AER-Skills without requiring model
training during normal validation. Treat each `skills/aer-*/SKILL.md` file as a
trainable skill document, but accept edits only when they improve a checkable
workflow surface.

Reference: [microsoft/SkillOpt](https://github.com/microsoft/SkillOpt).

## Mapping

| SkillOpt stage | AER-Skills equivalent |
|---|---|
| Rollout | Run a realistic manuscript prompt through `aer-workflow` and the routed skill. |
| Reflect | Summarize the failure as a bounded edit to a skill, doc, script, or example. |
| Aggregate | Merge duplicate failures into one small patch with one owner. |
| Select | Prefer high-frequency failures that affect routing, gates, citation integrity, identification, or replication. |
| Update | Change the smallest skill surface that fixes the observed failure. |
| Gate | Run `python3 scripts/run_skillopt_gate.py` and `make preflight`; use fresh agent forward-tests for risky behavior changes. |

## Scenario Bank

The fixed routing bank lives in
[`../examples/skillopt-routing-scenarios.json`](../examples/skillopt-routing-scenarios.json).
It is the repository's lightweight selection/test split for the router:

- `selection` scenarios cover common routing and handoff behavior.
- `test` scenarios cover edge cases that should not be tuned away.
- Every non-router skill must have at least one scenario.

Keep prompts user-like. Do not write prompts that merely quote skill names; the
gate is meant to protect triggering and routing behavior.

## Edit Budget

Use a small textual learning rate:

- Patch at most two `SKILL.md` files per optimization step.
- Prefer one docs/example/script change plus one skill change when the failure is
  caused by missing reusable context.
- Do not update journal policy wording unless `docs/source-register.md` also
  identifies the official source and affected surfaces.
- Do not broaden a skill's scope to cover another skill's job; route through
  `aer-workflow` instead.

## Reflection Record

For each failed rollout, record:

```text
SCENARIO:
OBSERVED FAILURE:
EXPECTED BEHAVIOR:
PATCH TARGET:
ACCEPTANCE GATE:
```

The record belongs in the PR, issue, or worklog that motivates the patch. Avoid
embedding training logs inside skill folders.

## Acceptance

A skill optimization patch is acceptable when:

1. `python3 scripts/run_skillopt_gate.py` passes.
2. `make preflight` passes.
3. Any changed behavior has a scenario, example, or reviewer-facing document that
   would catch a regression.
4. The final skill still obeys the repository's progressive-disclosure rule:
   `SKILL.md` stays compact, and reusable detail lives in `docs/`, `examples/`,
   `templates/`, or `scripts/`.
5. The document-quality score does not regress (see below): take a baseline
   before editing, then confirm the edited skill scores no lower.

## Document-Quality Gate

The behavioral gate above protects *routing*; `scripts/skill_audit.py`
protects *document quality* — the second axis SkillOpt optimizes. It scores
each `SKILL.md` 0-100 on a compact token budget (SkillOpt's 300-2,000-token
band), trigger sharpness, directive density, the house section structure, and
this repository's own `style-guide.md` discipline.

Use it as the "Reflect/score" step and as the executable form of acceptance
criterion 5:

```text
python3 scripts/skill_audit.py                       # ranked table (advisory)
python3 scripts/skill_audit.py --skill <name> -v     # one skill + edit tips
python3 scripts/skill_audit.py --baseline before.json   # snapshot, then edit
python3 scripts/skill_audit.py --against before.json     # exit 1 if a score dropped
python3 scripts/skill_audit.py --gate 85             # exit 1 if any skill < 85
python3 scripts/skill_audit.py --selftest            # scorer self-tests (run by preflight)
```

`make audit-skills` runs the table; `make audit-skills-gate` enforces a floor.
The auditor is advisory by default — `make preflight` runs only its
`--selftest` so a broken heuristic is caught without blocking unrelated work.
