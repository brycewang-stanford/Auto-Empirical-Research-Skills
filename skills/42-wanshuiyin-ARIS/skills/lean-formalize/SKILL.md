---
name: lean-formalize
description: "Develop and verify a mathematical proof in Lean, continue an incomplete Lean project, or audit whether it proves the original statement. Connect actual inputs to intermediate lemmas, assemble the target theorem, check its transitive axioms, and provide a reproducible handoff. Use when Lean is requested or a specific proof obligation benefits from formal verification; use proof-writer for ordinary mathematical drafting."
argument-hint: "[statement, proof file, Lean project, or audit request]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, mcp__codex__codex, mcp__codex__codex-reply, mcp__antigravity__antigravity, mcp__antigravity__antigravity-reply, mcp__grok__grok, mcp__grok__grok-reply, mcp__claude-review__review, mcp__claude-review__review_reply, mcp__claude-review__review_start, mcp__claude-review__review_reply_start, mcp__claude-review__review_status
---

# Lean Formalize

> **Before each reviewer slot**, follow [Selectable Reviewers](../shared-references/reviewer-backends.md):
> resolve invocation → `.aris/reviewer.json` → Claude Code default (Codex MCP)
> with `reviewer_route.py` through the canonical helper resolver, preserving this
> slot's tier, fresh contexts, source/image inputs and deterministic gates.
> Codex examples/pins below apply only to `backend=codex`; other routes use their
> own first-call/reply contract. Save the route and actual returned identity;
> unavailable selections are `REVIEW_UNAVAILABLE`. Classify acceptance from actual
> families/completion/scope. Forward invocation reviewer/model/effort overrides
> to reviewer-bearing children. Generation workers are unchanged.


Turn the user's mathematical statement into a checked Lean theorem with its
meaning preserved. A compiled conditional lemma is progress; completion concerns
the original statement and the trust basis actually used.

## When to use Lean

Use this skill when the user requests Lean, when continuing an existing Lean
proof, or when formal verification addresses a concrete uncertainty in a central
claim—for example, a long dependency chain, a delicate reduction, or coverage of
a finite classification. State the obligation it will help resolve and proceed
within the authorized task. Difficulty alone is not a reason to formalize.
Ordinary derivations and short proofs can stay in `formula-derivation` or
`proof-writer`; do not make Lean a prerequisite for every mathematical result.
Respect the user's chosen proof method and the scale of the requested work.

## Core workflow

```text
Original statement and Lean definitions
  → A: cross-family adversarial statement alignment
  → Proof obligations, representations, and lemma interfaces
  → Lean implementation ↔ B: adversarial review of key arguments and connections
  → Actual inputs connected; original theorem assembled
  → Executed type, definition, and transitive-axiom audit
  → C: cross-family adversarial review of the final exported result
  → Reproducible delivery and research-state update
```

For substantial new proof projects, A/B/C are part of the workflow. For a
continuation, reuse completed checks on unchanged claims and revisit affected
ones. Small routine formalizations need checks proportional to the actual claim;
an explicit user request for cross-family review still applies to them.

Use the authorized reviewer families available in the current host. If the user
specifies both Grok and Gemini, obtain and record both; a same-family agent or
another provider does not silently satisfy either request. Unavailability leaves
that checkpoint pending while independent proof work continues. A checked theorem
and a fully completed requested review workflow are separate deliverables.

## Scope and entry

Follow the requested scope: implement, continue, audit, or package. For an audit,
inspect and report rather than silently repairing or weakening the theorem.
For implementation, develop the mathematical argument as well as its Lean
proof: search relevant literature or library results, explore alternative routes,
and discharge the missing lemmas. Continue through the remaining interfaces and
top-level assembly; do not stop at a target declaration or the first successful
compilation.

Read the authoritative statement, existing Lean entry point, toolchain and
lockfile, and latest progress record. Reuse the project and its document names.
Do not reinstall tools, change dependencies, or start a new proof framework when
the existing environment is suitable. Resolve APIs against the pinned library.

Use the existing proof route when it works. If the mathematical argument itself
is missing, isolate that obligation and use `proof-writer` or ordinary proof work.
A delegated `proof-writer` task develops that argument and returns its proof or
remaining gap to this run; it must not invoke `lean-formalize` again. Syntax
automation cannot discharge an unproved premise. Do not promise that an arbitrary
open problem can be formalized or solved.

### Start or resume the right work

| Current input | First useful action |
|---|---|
|Only a mathematical statement|Fix definitions and quantifiers, then develop a proof route and its first difficult obligation|
|A prose proof|Identify nontrivial dependencies and choose Lean representations; expose any missing argument before coding it|
|A partial Lean project|Inspect the target and its actual callers, read the last useful build/error record, and continue at the highest unclosed connection|
|An audit request|Read definitions and exported types, run applicable checks, and report; do not silently repair the target|
|A completed proof to hand off|Check the current entry point and evidence, then prepare portable sources and commands without restarting the mathematical search|

Name the intended main module, exported declaration, and current next obligation
early. If no complete mathematical route is known, say which statement is being
attempted; do not mark it provable merely because the implementation has started.
Tool/API problems and missing mathematical arguments require different next steps.

## 1. Fix meaning before implementation

Record a short mathematical specification, or reference the existing one:

- Objects, domains, quantifiers, original hypotheses, and conclusion.
- Equivalence of convenient representations to the original objects.
- User constraints on computation, external certificates, and logical foundations.
- The Lean declarations intended to express and prove the result.

Separate original hypotheses from properties introduced by a reduction. Identify
where finiteness, nonemptiness, decidability, normalization, and index conventions
change the statement or require a bridge. Check plausible vacuity and quantifier
failures in the actual theorem, rather than inventing unrelated edge cases.

Keep the user's original statement as the comparison baseline until the user
changes the goal. A working specification rewritten to match the implementation
does not change that baseline. Record authorized scope changes explicitly; do not
request confirmation again for a change already authorized in the session.
If a repair yields only a stronger assumption or weaker conclusion, identify the
proved variant and the original obligation still open. A stronger proved result
can establish the original claim when its implication is supplied.

Run checkpoint A on the actual definition bodies and proposed target. Ask for
independent back-translation before comparison with the original mathematics.
The input packet and prompt are in
[references/adversarial-review.md](references/adversarial-review.md). A reviewer
who saw only the intended prose has not checked the encoding.

## 2. Design the connections, then build useful pieces

Map the path from an arbitrary original input to the conclusion. For every
substantial interface, record:

| Declaration / obligation | What it assumes | Where actual inputs come from | Evidence / remaining gap |
|---|---|---|---|
|A conditional result|Its extra hypotheses|A named construction or theorem from the original input|Actual state|

Prioritize the highest unclosed connection. In particular, distinguish:

1. A formula or certificate computes the desired number.
2. The actual mathematical object realizes that formula or certificate.
3. The computed fact implies the original conclusion.

All three may require separate proofs. A structure that stores its desired
properties as fields, a supplied probability bound, or an assumption equivalent
to the conclusion does not remove the obligation to construct that input.

Use conditional lemmas as development interfaces, explicitly marked as such.
Keep incomplete experiments outside the certified target's dependency chain;
any temporary `sorry` remains visible as unfinished work and cannot survive the
final target audit. Prefer enough intermediate compilation to localize errors,
without interpreting file counts or proved arithmetic statements as completion.

Split parallel work along stable lemma signatures and module ownership. Give
each worker its assumptions, conclusion, dependencies, and concrete compile
target. Integrate its result against the actual caller before closing the ledger.
Do not let parallel workers silently redefine shared objects to suit their proofs.

### Implementation loop

Read [references/lean-working-loop.md](references/lean-working-loop.md) when
implementing or repairing an obligation. It develops the search → actual-caller
experiment → diagnostic → repair cycle, including representation choices and
performance problems, with a compiled library-application example.

1. Select a missing connection or mathematical lemma that changes what the main
   theorem can prove. State its exact Lean interface and its caller's obligations.
2. Look for the required results in the pinned library and project. Test unfamiliar
   declarations locally with `#check`; use existing equivalent representations
   when they simplify a real bottleneck.
3. Implement the lemma and an actual use site. Compile the affected module; after
   integration, compile the downstream target whose status depends on it.
4. Diagnose the first relevant error. An elaboration/API mismatch calls for a
   local implementation fix. An unavailable assumption calls for its derivation,
   a different argument, or an explicit remaining mathematical obligation.
5. When finite reduction becomes expensive, consider a general counting lemma,
   recurrence or smaller checked certificate. Do not silently enlarge the trust
   basis merely to make a tactic finish.
6. At a new load-bearing argument or interface, run checkpoint B. Implement valid
   fixes, compile them, and request follow-up on the changed obligation.
7. Update the existing ledger with the declaration, actual caller, verification
   evidence and remaining premise; then advance to the next connection.

For example, a theorem of type `Certificate x → Desired x` is useful only after
the project constructs `Certificate x` for every original input it needs. Closing
that construction and connecting the caller is a distinct result from proving
the conditional theorem. Kernel checking does not discharge a parameter merely
because its type has a reassuring name.

Do not use a timer, repeated unchanged builds, or repeated model calls as a proxy
for progress. After a concrete failure, try another justified representation or
proof path; preserve the exact blocker if the requested work cannot yet finish.
Distinguish an implementation failure from a failed intermediate claim and an
obstruction to the whole method. Retire an unsuccessful route with its reason;
rejecting that route does not refute the original theorem. Parallel exploration
is most useful when the proposed approaches can fail for different reasons.

## 3. Use computation with a proved interpretation

Distinguish finite examples, exhaustive computation over a proved domain,
checked certificates, and symbolic/general proof. A bounded search is evidence
about its searched inputs. Exhaustive finite verification can be a proof when
coverage, encoding correspondence, and the verification procedure are established
and the user's constraints permit it. For an end-to-end Lean result, the coverage
and interpretation must themselves lie in the proved dependency chain under the
declared foundations. A comment claiming that a finite list is exhaustive does
not turn checked list entries into a universal Lean theorem.

For numeric arguments, use exact arithmetic where the claim needs exactness.
Prove the connection between actual objects/events and the finite data before
using the numeric conclusion. Document conventions that matter: ordered versus
unordered pairs, multiplicities, indices, zero cases, and rounding.

Agree on the intended trust basis from the specification and project conventions.
Do not silently introduce axioms or compiler-backed computation to make an
otherwise incomplete kernel-level proof appear complete. Conversely, do not turn
one project's prohibition on enumeration or `native_decide` into a universal
ban. Explain any extra trust assumption and whether it satisfies this task.

## 4. Review the mathematical obligations that remain uncertain

Run A, B and C as described in the core workflow. Read
[references/adversarial-review.md](references/adversarial-review.md) for stage
triggers, source packets, adversarial prompts, objection handling, resumption and
stopping rules. These are mathematical checks, not votes on whether to trust the
executor's summary.

Use `proof-checker` for the existing ARIS proof-audit/submission role. This skill
does not replace its artifact or reviewer contract. When invoked by a parent
proof audit, return the checked scope and evidence to that run; do not recursively
invoke `proof-checker`. A standalone Lean task does not automatically require a
separate paper-audit workflow. Where installed, use
`research-review` / `auto-review-loop` for targeted discussion and repair, with
the current host's reviewer routing.

For direct model consultations, use available authorized tools and their actual
contracts. A Grok or Antigravity MCP consultation is not automatically an ARIS
reviewer overlay. Do not hard-code vendor availability, quotas, retry counts,
proxy settings, or a particular model into the portable workflow.

Ask concrete questions: translate this declaration; discharge these caller
hypotheses; find a counterexample to this new lemma; check this reduction's
coverage. Preserve raw responses, actual reading/execution scope, and the
executor's disposition of each issue. Model agreement is not a proof. Same-family
opinions remain provisional; cross-family opinions are additional review
evidence, not mathematical truth certificates.

An unread artifact, an unanswered question, a failed call or an empty response
provides no substantive review verdict. A plan review is not a final-code review;
reading existing logs is not executing a build. Preserve which claim/version was
actually examined. Retry only within current authorization and provider rules;
do not rewrite failures as passes after a later success.

Close objections with a specific derivation, verified witness, correction or
justified rejection. Preserve unresolved disputes. Apply an invoked ARIS loop's
own round/continuation contract; do not create an outer polling loop around it.
For direct consultations, re-review changed obligations and stop when settled or
when a real availability/budget limit is reached. Unresolved mathematics remains
open; an unavailable requested review remains pending. Neither a reviewer score
nor exhaustion of rounds is a proof-completion rule.

### Host execution and review

Read the local host's [reviewer routing](../shared-references/reviewer-routing.md)
for its current model/effort policy and tool contracts. Use the A/B/C mathematical
packets in this skill; they do not require a paper, publication score, or a new
review service. For delegated proof work, follow the applicable
[fan-out convention](../shared-references/fan-out-pattern.md), assign stable lemma
interfaces, and integrate each result at its real caller.

On Claude Code, use the host's file/shell tools for Lean and `Agent` for useful
parallel proof work. The default reviewer is Codex MCP: start with
`mcp__codex__codex`, an explicit project `cwd`, read-only sandbox, and the
model/effort pair resolved from the routing reference. Continue that review with
`mcp__codex__codex-reply` using its saved session identity and prompt. Start fresh
contexts for A and C; B repair checks may continue the reviewer that found the
issue. Verify the executor/reviewer families rather than assuming that every
host running this mainline skill is Claude.

For every A/B/C checkpoint, resolve the selected route through
[Selectable Reviewers](../shared-references/reviewer-backends.md). Honor explicit
family requirements and leave unmet checkpoints pending. Direct Claude, Grok and Gemini
transports have different file-access and continuation contracts; read
[review transport notes](references/adversarial-review.md#review-transport-and-source-access)
when using them. These Lean consultations do not change another skill's reviewer
backend or its acceptance rules.

## 5. Verify the actual final target

Use [references/verification-and-handoff.md](references/verification-and-handoff.md)
when preparing the final build, trust audit, or portable package.

For completed delivery, establish the applicable evidence below. Keep a proved
theorem distinct from any still-pending reproduction or review requirement:

- **The proposition has a proof:** inspect the exported declaration's actual
  type, not its keyword. `theorem`, `lemma`, or `def` may supply a proof term of
  the target proposition. Merely defining that proposition, proving `P → P`, or
  proving an unrelated proposition does not discharge the original target.
- **Statement alignment:** its expanded type and definitions express the original
  claim; no internal profile, certificate-validity, coverage, or success premise
  is left for the user to supply unless the original claim included it.
- **Actual assembly:** reductions, cases, witnesses, and return to the original
  conclusion are connected, with all caller hypotheses discharged.
- **Executed verification:** explicitly build the module that proves the target
  and print its type and transitive axioms. For a multi-module project, also
  independently import the actual entry point to check its exported result.
  Direct compilation plus type/axiom output suffices for a small self-contained
  file; do not build a new project just to create another import. Save commands,
  exit status, and output. A successful build of a different root module does
  not count.
- **Trust accounting:** no `sorryAx` or unapproved extra axiom lies on the target's
  dependency chain. Explain the actual dependencies against the intended basis;
  the required list need not be exactly any fixed set of axiom names.
- **Reproducibility:** retain the relevant source and pinned environment, and
  provide commands that another reader can run.
- **Requested review:** C concerns the final exported type, definition bodies,
  axiom output and original claim, not an earlier plan. Record each required
  reviewer's substantive findings or unavailability separately.

These checks establish the formal result under its stated foundations. A prose
proof or HTML edition requires its own correspondence check; Lean does not certify
every sentence in a separate exposition. An explicitly required import audit,
external reproduction, or review may remain pending even after the formal theorem
is checked. Report that missing evidence as such, not as a newly discovered
mathematical gap.

An illustrative audit can distinguish `available_interface : Target → Target`
from `original_proof : Target`, even if both compile without extra axioms. The
first leaves the original claim open; the second supplies its proof when `Target`
matches the user's statement. A failed reviewer call changes neither type.

## 6. Persist and hand off the evidence actually obtained

Reuse the existing specification, proof ledger, and continuation file. A short
progress report plus Lean sources, lockfiles, an audit entry point, and logs is
usually enough. Add new files only for a concrete reader or execution need.

Report distinct facts rather than a single ambiguous PASS:

- Original theorem: checked, partial, changed claim only, or disproved by a
  verified counterexample; name the declaration and any remaining obligation.
- Statement alignment and the actual logical trust basis.
- Reproduction: existing/incremental build, clean project rebuild, or another
  person's independent reproduction—whichever actually happened.
- Reviews: who read what, who ran code, and any requested review still pending.

For unfinished work, save the smallest remaining mathematical/Lean obligation,
its known dependencies, the last useful error, and the next action. For completed
work, record completion so the next session does not revive obsolete gaps.

Use a compact continuation note rather than a second state system:

```text
Original target and source:
Current exported declaration / main module:
Closed connections and actual build evidence:
Next unclosed obligation or completion:
A/B/C reviews: source scope, reviewer, raw record, remaining issue:
Next action:
```

Resolve current state from actual artifacts, not an old narrative saying either
“finished” or “not finished.” On resume, check what changed before repeating work.
Do not merge historical and current reviewer scopes into a larger claimed audit.

If a research wiki is active, update the affected claim through the existing
`research-wiki` / `proof-checker` workflow with precise evidence and scope; do not
overwrite its generated graph or invent a second acceptance format. Literature
search should resolve a mathematical gap, API question, or relevant prior result,
not become an unrelated requirement to exhaust the literature.

For handoff, provide a reader-oriented proof, source, pinned dependencies,
independent audit command, and known trust boundary. Use `render-html` when a
single-file reading edition would help. Mathematical source changes require
appropriate rebuild and statement/axiom checks. A theorem or hypothesis changed
in Markdown or HTML is also a claim change: redo alignment and affected requested
review. Layout or wording that preserves the claim needs presentation checks.
Keep change histories in the research record and present the finished proof
directly. Do not restart completed proof work solely to satisfy a workflow ritual.
