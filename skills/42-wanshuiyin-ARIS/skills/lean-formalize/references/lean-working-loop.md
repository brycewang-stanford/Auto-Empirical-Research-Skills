# Lean working loop: find, apply, diagnose, improve

Read this when implementing an obligation, selecting a representation, or
repairing a failing or slow proof. Keep the original target and caller in view.
Use the existing Lean project and the tools actually available in the host.

## Make the next uncertainty small

Choose the next action by what is unknown:

- **Library availability:** find a declaration and try it at the actual goal.
- **Representation:** compare a constructor and one real downstream use before
  migrating the API.
- **Mathematical argument:** write the missing implication and its justification;
  choose a genuinely different route when the current one has an obstruction.
- **Lean implementation:** inspect the first causal diagnostic and its context.
- **Execution cost:** determine whether the time goes to queueing, downloads,
  imports, elaboration or proof checking before changing the proof.

A productive iteration leaves checked source, a more precise missing lemma, a
verified obstruction, or a useful representation choice. Repeating tactic
variants against the same unexplained failure does not narrow the problem.

## Search the pinned library, then exercise the result

Start with the mathematical objects, operation and desired conclusion. Search
the nearby project module, then the relevant part of the installed dependency.
Inspect neighboring results and existing callers; a stronger theorem or a
different characterization can avoid a long new development.

For a project using Mathlib, a local search might be:

```sh
rg -n 'card_union|card_image' .lake/packages/mathlib/Mathlib/Data/Finset
```

Resolve paths from the actual package. Use name/text search for likely names,
an available signature search for a known type shape, or an available semantic
search for an unfamiliar concept. A heuristic signature index returns candidates;
Lean must still elaborate the application. Neither an empty search nor a result
from a different Mathlib revision settles local availability.

Read the defining source and check the full declaration:

```lean
import Mathlib.Data.Finset.Card
#check @Finset.card_union_le
```

Then apply it with the original caller's parameters and hypotheses. In Mathlib
v4.24.0 the sets below are explicit arguments; the full application is:

```lean
theorem union_bound {α : Type*} [DecidableEq α]
    (s t : Finset α) (hs : s.card ≤ 12) (ht : t.card ≤ 20) :
    (s ∪ t).card ≤ 32 := by
  exact (Finset.card_union_le s t).trans (Nat.add_le_add hs ht)
```

This small application tests more than the name: it checks binders, instances,
coercions, imports and the implication the caller actually needs. Keep an import
that exposes the needed declarations; do not add an umbrella dependency simply
to hide an unresolved missing-name problem.

If available in the pinned environment, LSP goal inspection or exploratory
`exact?`, `apply?`, `rw?` and `simp?` can help find an application. Inspect
suggestions and keep an explicit result when it is clearer. Do not assume a
particular MCP, tactic import or search service is installed. Local source
search plus the Lean elaborator is a usable starting point.

## Choose representations by real use

Before a large rewrite, compare the current representation with a small
alternative in scratch. Construct an actual object and prove a representative
consumer with the same mathematical assumptions. Inspect where equality is
definitional and where a proved bridge or equivalence is needed.

Prefer a bridge lemma when it makes the caller straightforward. Consider a new
representation when independent consumers repeatedly reconstruct the same data
or require the same difficult transports. One failed tactic is not enough
evidence to redesign the objects.

For two instances on the same carrier, inspect which instance an expression
uses; print explicit parameters or give the intended instance locally. An alias,
a bundled structure and a type synonym have different costs. Choose according
to the actual constructors and consumers, not a blanket preference. A proposed
representation must still pass statement alignment.

## Repair the cause shown by Lean

Use live diagnostics when available. Otherwise compile the affected file or
module in the existing package. Keep diagnostic experiments outside the public
proof modules. Fix the first causal error before treating later failures as
independent problems.

| Observation | Inspect | Next useful action |
|---|---|---|
| Unknown name | Namespace, defining module, pinned revision | Find the real declaration and required import |
| Application mismatch | Full type, explicit arguments, coercions | Supply the actual parameters or a proved conversion |
| Instance synthesis fails | Requested class and intended carrier | Reuse the appropriate instance or clarify it locally |
| Rewrite misses | Elaborated expression and equality direction | Use the matching equality; `change` only for definitional equality |
| Simplification leaves a goal | Remaining proposition and hypotheses | Supply the missing mathematical fact |
| A downstream import fails | Changed source versus compiled dependency | Build the changed dependency, then check its consumer |
| Timeout | Slow step versus queue/import/download time | Isolate the expensive work before changing resource limits |

Match automation to the mathematical operation. For example, `omega` addresses
natural/integer linear arithmetic; `ring` handles polynomial identities in
appropriate algebraic structures; `linarith` uses supplied ordered-field
linear constraints. Division manipulations still need the relevant nonzero
conditions. A tactic choice cannot manufacture a missing hypothesis or witness.

For rewriting, first inspect the post-simplification goal. Use local equalities
or a focused `simp only` when one proof needs a particular form. Promote a rule
to the global simp set only when it serves the shared API and works in its
actual consumers. Preserve readable automation when it already behaves well.

## Change the right level of the argument

Separate three kinds of failed attempt:

1. **Proof implementation:** the argument is suitable but an application,
   inference or tactic fails. Repair that step.
2. **Chosen decomposition:** one intermediate lemma is false, too strong or
   unreachable. Revise the route and reconnect its obligations to the goal.
3. **Underlying method:** the same mathematical obstruction defeats the route
   even after its local repairs. Seek a method that avoids that obstruction.

Rejecting a sufficient condition rejects that route, not the original theorem.
For example, cardinality of a union is at most the sum in general; equality
without disjointness is false for two identical singleton sets. That witness
rejects the equality-based step, while the upper-bound route remains available.

Record a failed route with the exact obstruction and the conditions under which
it applies. Keep useful partial lemmas. A changed hypothesis or new theorem can
justify reopening it; a failure log is not a permanent ban on related ideas.
A counterexample must satisfy the actual premises, and any formal refutation
needs its own trustworthy dependency chain.

For exploratory parallel work, give workers materially different approaches
when their possible failure mechanisms differ. For implementation, split stable
lemma interfaces and file ownership. In both cases name the integration point.
A list of completed child lemmas still requires the parent implication to the
original target. Reuse the existing obligation and research records.

## Keep compilation and performance evidence useful

Check local edits promptly, then build affected dependencies and consumers at
integration. A standalone `lake env lean Scratch.lean` can read existing imported
artifacts; it does not rebuild changed imports. Use the host's managed build
entry if one is configured. A queued or deferred check is pending verification,
not a failed theorem.

When a build is genuinely expensive, use compatible dependency caches and
serialize competing builds in the same mutable checkout. Continue independent
mathematical work while waiting. Reuse completed checks for unchanged sources.
Do not add a scheduler for a project whose existing build loop is sufficient.

For a measured hotspot, try explicit intermediate types, a reusable named lemma,
a smaller rewrite context or a repaired instance before enlarging global limits.
Scope profiling to the suspected declaration and the pinned Lean version's
supported options. Compare equivalent targets and cache conditions; a warm
incremental build does not demonstrate a faster proof than a cold build.
A justified local resource increase is an option, not evidence of a new argument.

Retain the smallest useful record: changed declaration, actual caller, command
and outcome, remaining mathematical issue, and next action. Remove abandoned
tactic branches and diagnostic settings from the delivered proof. The final
completion and trust checks remain those in `SKILL.md` and
[verification-and-handoff.md](verification-and-handoff.md).

## Source basis

These practices were selected after reading implementation and skill sources;
they do not require installing either platform.

- [Horizon Lean search](https://github.com/frenzymath/Archon-Horizon/blob/0df5571f81aae29130c8ec621c9fe7419ca28d6a/src/archon_horizon/pipeline/skills/lean/lean-search/SKILL.md),
  [proof cycle](https://github.com/frenzymath/Archon-Horizon/blob/0df5571f81aae29130c8ec621c9fe7419ca28d6a/src/archon_horizon/pipeline/skills/lean/lean-cycle/SKILL.md),
  [repair](https://github.com/frenzymath/Archon-Horizon/blob/0df5571f81aae29130c8ec621c9fe7419ca28d6a/src/archon_horizon/pipeline/skills/lean/lean-proof-repair/SKILL.md),
  and [representation experiments](https://github.com/frenzymath/Archon-Horizon/blob/0df5571f81aae29130c8ec621c9fe7419ca28d6a/src/archon_horizon/pipeline/skills/review/definition-quality/references/representation-experiments.md).
- Horizon acknowledges its selected MIT-licensed adaptations from
  [cameronfreer/lean4-skills](https://github.com/frenzymath/Archon-Horizon/blob/0df5571f81aae29130c8ec621c9fe7419ca28d6a/src/archon_horizon/pipeline/skills/_sources/lean4-skills/PROVENANCE.md).
- [Argus mathematical execution](https://github.com/lbx154/Argus/blob/9cfe9129fd90511c3a1865844ec7dfda1b5d1008/argus/verticals/math/skills/engineer/math-research-execution.md)
  and [planning](https://github.com/lbx154/Argus/blob/9cfe9129fd90511c3a1865844ec7dfda1b5d1008/argus/verticals/math/skills/planner/math-research-planning.md).

