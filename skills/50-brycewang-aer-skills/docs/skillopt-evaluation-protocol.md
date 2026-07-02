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
5. The document-quality score does not regress **and the substance anchors do
   not drop** (see below): take a baseline before editing, then confirm the
   edited skill scores no lower and has not had a worked example trimmed away.

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
python3 scripts/skill_audit.py --gate 85 --substance-gate 8  # CI floor: score + substance
python3 scripts/skill_audit.py --selftest            # scorer self-tests (run by preflight)
```

`make audit-skills` runs the table; `make audit-skills-gate` enforces both the
85-point document-quality floor and the 8-anchor substance floor. The auditor is
advisory by default — `make preflight` runs only its
`--selftest` so a broken heuristic is caught without blocking unrelated work.

### The score is a tripwire, not a target

Treat the 0-100 score as a **floor to clear, not a number to maximize**. It
measures *form* — token budget, trigger sharpness, directive density, house
structure, filler hygiene. It cannot see whether the economics is current or
correct, so a high mean is not evidence the skills are good, only that they are
well-shaped. Two rules follow:

- Do **not** edit a skill to raise its score. Edit a skill to fix an observed
  routing or content failure, then confirm the score did not *regress*.
- Never delete a worked example, magnitude, or equation to gain budget points,
  and never flatten nuanced judgment into bare imperatives to gain directive
  density. Both trade the skill's actual value for a prettier number.

### Substance Floor

The budget dimension rewards deletion. Its dual, the **substance anchor count**,
rewards keeping the concrete, imitable content — worked figures, quoted
exemplars, equations and code — that makes a domain skill teach. It is reported
beside the score (`anch` column) but deliberately **not folded into it**:

```text
python3 scripts/skill_audit.py --substance-gate 8   # exit 1 if a skill is below the substance floor
python3 scripts/skill_audit.py --against before.json  # exit 1 if score OR substance dropped
```

`--against` is the SkillOpt do-not-regress gate on both axes at once: an edit
that raises the quality score by trimming a worked example trips the substance
guard (default: a >15% anchor loss). The advisory table flags any skill below
the `SUBSTANCE_FLOOR` (8) as `THIN`; those are the highest-value targets for the
domain pass below, not for more trimming.

## Primary Axis: Domain Correctness

The gates above protect routing, form, and substance — none of them protects
*correctness*. That is the higher-value axis and it is not mechanizable here. A
domain-correctness pass is where editing effort should now go:

- **Econometric currency.** Are the default methods still 2026 best practice
  (Callaway-Sant'Anna / BJS over TWFE, AR sets over first-stage F, MSE-optimal
  RDD)? See `docs/design-principles.md` §4.
- **Worked-number arithmetic.** Do the magnitudes in each worked example
  actually compute (log-point↔percent, percent↔percentage-point, back-of-
  envelope chains)?
- **Referee-anticipation realism.** Do the anticipated-objection lists still
  match what AER referees actually demand?

A skill can score 100/100 and fail all three. Run this pass by reading, not by
re-running the auditor.
