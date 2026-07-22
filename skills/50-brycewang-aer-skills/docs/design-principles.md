# Design Principles

The opinions baked into AER-skills.

## 1. Identification Before Prose

A weak identification strategy cannot be rescued by writing. The skill order enforces this: `aer-identification` runs *before* `aer-introduction`. If the design fails, the contribution sentence cannot survive.

## 2. One Contribution Per Paper

AER editors desk-reject competent extensions. The `aer-topic-selection` skill forces the contribution into a single sentence. If the sentence requires "and we also explore ...", that *and* is where the paper dies.

## 3. Cross-Subfield Interest Is the Top-5 Filter

The AER bar is *not* technical quality. It is whether economists outside the author's subfield will cite the paper. Many strong subfield papers belong in the AEJ family or a top field journal. AER-skills makes this routing explicit.

## 4. Modern Econometrics, Not 1990s Defaults

The skill stack assumes 2026 best practice:

- Staggered DiD → Callaway-Sant'Anna or Borusyak-Jaravel-Spiess, not TWFE
- Weak IV → Anderson-Rubin confidence sets, not first-stage F > 10
- RDD → local linear with MSE-optimal bandwidth, not polynomials of order 4
- SCM → permutation inference and placebo grid, not just visual fit
- Shift-share → explicit choice between exogenous-shares and exogenous-shocks identification

## 5. The Replication Package Is Part of the Paper

The AEA Data Editor's review is enforced and gates publication. `aer-replication` runs early, not after acceptance. README-first development eliminates retrofitting cost.

## 6. Editor Time Is the Scarcest Resource

The desk-rejection rate at AER is high. Every formatting, length, and clarity rule in the skill stack is designed to make the first 10 minutes of editor review as efficient as possible:

- ≤ 100-word abstract
- No "Introduction" heading
- ≤ 200-word cover letter
- Tables that read in one glance
- Response letters where action and location are visible in the first sentence

## 7. Anticipate, Don't React

`aer-robustness` runs before submission to pre-empt the three demands every referee makes (robustness, heterogeneity, mechanism). Reactive revision after the report is twice as expensive and twice as slow.

## 8. The AEJ Family Is Not a Consolation Prize

Routing a subfield-bounded paper to AEJ:Applied or AEJ:Policy from the start is faster, cheaper, and produces equivalent visibility for many topics. Pride-driven AER submissions cost ~6 months of life per round.

## 9. Skills Are Routers, Not Replacements

Each skill in this repository solves one slice. `aer-workflow` exists to compose them. None of them replaces the user's judgment about what makes a good economics paper.

## 10. English-First, Globally Usable

All skill content is in English so the agent can apply it regardless of the user's primary language. The default landing page `README.md` is in Chinese for discoverability, with a full English version at `README.en.md`.

## 11. Self-Verifying Gates

Every skill ends with a binary, checkable gate — a checklist or a Handoff contract — that the agent must satisfy before declaring the stage done. The skills are self-verifying, not merely advisory. This is the same validation-gate discipline that text-space skill optimizers such as Microsoft SkillOpt use to accept only strictly-improving edits, brought *inside* each skill so an agent can apply it without an external evaluation harness. See `docs/skillopt-evaluation-protocol.md` for how these gates feed the held-out evaluation.

## 12. Route to Validated Tools, Don't Hand-Roll

When a StatsPAI MCP server is connected, a method skill should **select the validated estimator and let it run**, not teach the agent to hand-roll a regression. This is the "select the vetted tool, then generate code" discipline (the design lesson from agentic econometrics systems such as the Econometrics-Agent project): confining the agent to *picking and parameterizing* curated implementations is what removes a whole class of estimator mistakes — a TWFE on staggered data, a first-stage-F-only IV, a high-order-polynomial RDD.

The contract is enforced, not aspirational. `skills/aer-statspai/SKILL.md` is the human-facing hub; `scripts/statspai_tools.txt` is the machine-readable registry of blessed StatsPAI tools (each one a real tool on the live MCP server). `aer-identification` and `aer-robustness` carry a `<!-- tool-bindings -->` block routing each design or robustness check to its registry tool with an explicit "do not hand-roll" counterpart. `scripts/validate_repo.py::check_tool_bindings` fails the build if a skill binds to a tool absent from the registry (a typo or hallucinated name), if a designated method skill ships no bindings, or if the registry and the hub drift apart. The methodological *choice* still comes from `aer-identification`; the binding only fixes *how* the chosen design is executed.
