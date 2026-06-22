# SkillOpt-Style Optimization Pass

These skills were reviewed with the discipline behind [Microsoft SkillOpt](https://github.com/microsoft/SkillOpt):
treat each skill document as a trainable artifact, and accept only **bounded edits that
strictly improve** it against a clear rubric — never a wholesale rewrite of content that
already works.

## Rubric applied

A skill is scored on four axes:

1. **Activation** — does the frontmatter `description` fire the skill exactly when it should
   (third-person, concrete "use when…" triggers, full documented scope)?
2. **Execution** — are the body instructions concrete, ordered, and free of vague filler?
3. **Compactness** — every line earns its place; reference-heavy detail lives in `templates/`
   and `examples/`, loaded on demand.
4. **Self-verification** — does the skill end with a binary gate the agent can check before
   handing off? (SkillOpt's validation-gate concept, made local.)

## What this pass changed

The collection already scored high on axes 1–3, so edits were deliberately small and additive:

| Skill | Edit | Axis |
|---|---|---|
| `aer-topic-selection` | Added **Go / No-Go Gate** before Handoff | self-verification |
| `aer-identification` | Added **Identification Gate** before Handoff | self-verification |
| `aer-robustness` | Added **Coverage Gate** before Handoff | self-verification |
| `aer-introduction` | Added **Pre-Handoff Gate** before Handoff | self-verification |
| `aer-rebuttal` | Broadened `description` to cover reject-and-resubmit and conditional acceptance (already in the body) | activation |
| `docs/design-principles.md` | Added principle #11, *Self-Verifying Gates* | documentation |

Each new gate is **binary and skill-specific**, derived from that skill's own hard rules — it
is not a restatement of the existing *Anti-Patterns* (narrative warnings) or *Handoff* (a
reporting contract). The four skills that already shipped explicit checklists
(`aer-tables-figures`, `aer-submission`, `aer-replication`, `aer-rebuttal`) and the router
(`aer-workflow`, whose Handoff Contract is its gate) were left unchanged.

After this pass, **all nine sub-skills end with a self-verification mechanism.**

## Reproducing a future optimization loop

To run an actual SkillOpt training loop (rather than this manual pass) against a skill:

1. Define an eval set of held-out tasks for the skill (e.g., real AER intros to compress, real
   referee reports to triage) with a scorer (word-count gate, rubric LLM-judge, or human label).
2. Point SkillOpt's optimizer model at the single `SKILL.md` as the trainable state.
3. Let it propose bounded add/delete/replace edits; **accept only those that raise the held-out
   score**, exactly as the gates above encode acceptance for the agent at run time.
4. Deploy the resulting `best_skill.md` in place of the current `SKILL.md`.
