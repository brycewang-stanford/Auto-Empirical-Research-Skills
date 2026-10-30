# Cross-family adversarial review in a Lean proof project

Use this protocol for the three mathematical review checkpoints in a substantial
formalization. It specifies what to send, what to attack, and what to do with the
answer. Use the host's existing reviewer tools and ARIS routing; no new service or
reviewer registry is needed.

## Review plan and independence

At project entry, identify the executor family, available authorized reviewer
families, user-requested reviewers, and the checkpoints still needing attention.
Reuse authorization and choices already established in the session. If the user
requests both Grok and Gemini, track both; one is not a replacement for the other.

Different agents or different model names in one family do not establish
cross-family review. Record the actual returned model identity and the source of
that information. A CLI-selected model is not independent server attestation.
Unknown identity remains unknown; do not upgrade a requested model to an observed
one. Codex peer review is useful same-family assistance and remains provisional.

Give each first reviewer the relevant original sources, not the executor's
conclusion or the other reviewer's opinion. Use a fresh context for initial
semantic translation and final assembly. For intermediate repair verification,
continuing the reviewer that raised the issue is useful; call it follow-up
verification, not a fresh blind review. When a named ARIS skill is invoked, retain
its own fresh-thread or continuation rules.

Reviewers need enough context to follow the dependency. Include the exact target,
local declarations, actual caller, definitions and lemma bodies it relies on, and
any required logs. Let a file-reading reviewer follow those dependencies inside
the authorized project. Shortening a packet must not hide a hypothesis.

## Review transport and source access

Choose tools that are actually registered in the current host. Reuse the user's
reviewer selection and existing authorization; do not probe or reconfigure a
working bridge solely to satisfy this workflow. The host-specific entry in
`SKILL.md` sets the default; these notes govern an explicitly selected direct
consultation, not ARIS-wide routing.

- **Claude review MCP:** use `review` / `review_reply`, or the asynchronous
  `review_start` / `review_reply_start` plus `review_status` for long reviews.
  For artifact-path review, pass `tools: "Read,Grep,Glob"` on every call, including
  replies; file tools are otherwise disabled. Pass the saved `threadId` (or the
  bridge's `thread_id` alias) to `review_reply` / `review_reply_start` as well as
  the prompt and file-tool setting; continuation requires that session identity.
  Use the registered tool schema for other arguments rather than copying another
  bridge's fields. Keep review read-only.
- **Gemini review MCP:** its `review*` tools have their own saved conversation.
  With the API backend, include the relevant primary source text, definitions,
  caller and logs in the prompt; a remote model cannot read local paths. The
  compatibility `tools` field does not enable file access. Select source content
  without replacing it by the executor's interpretation.
- **Grok MCP:** first call `grok` with the prompt and explicit project `cwd`;
  continue via `grok-reply` with the saved session and prompt. Preserve the first
  call's model, effort, tools and read-only setting on continuation.
- **Antigravity MCP:** first call `antigravity` with prompt and project `cwd`;
  continue through `antigravity-reply`. It is a separate CLI bridge from
  `gemini-review`, with its own native conversation and fixed initial workspace.

Read the bridge's current schema/documentation when needed; names may be
namespaced differently by the host. Verify that the reviewer actually received
or read the necessary source before treating the checkpoint as reviewed. Keep
transport errors separate from mathematical findings. These calls cannot
silently satisfy an unrelated skill's formal acceptance gate or replace a named
reviewer the user still requires.

## Checkpoint A — original statement and representation

**When:** a new theorem is formalized, the mathematical specification changes, or
a representation change affects what its declarations mean. An unchanged,
previously reviewed specification can be reused on continuation.

**Packet:** prepare the original mathematical statement, Lean object definitions
and proposed target, representation/equivalence arguments, and user constraints.
A full proof need not exist yet. For the first back-translation, send the Lean
definitions and target without the intended prose interpretation or prior
verdicts. Include notation and dependencies needed to read them correctly.

**Task:** obtain the independent translation before disclosing the intended
statement, then compare them. Supply the original statement and any discrepancy
for focused follow-up when needed. Do not call a translation blind if its packet
already reveals the intended interpretation. No automated comment-stripping or
source-rewriting system is needed. Attack quantifier order, implicit parameters,
domains, and equivalence of representations. An allowed empty case is not itself
a defect; do not add nonemptiness unless the original mathematics requires it.

```text
Translate these Lean definitions and this target into a precise mathematical
statement, including hidden/instance parameters and quantifier order. Identify
domains on which it is vacuously true and distinguish those cases from an
encoding error, which requires comparison with the intended claim. Do not infer
the intended theorem from declaration names. State anything needed to interpret
the source that is missing from the packet.
```

**Action:** correct a representation mismatch before building its downstream
proof. If the source mathematics itself is ambiguous, identify the consequential
choice and resolve it with the user when existing context does not decide it.
Continue independent setup or unaffected lemmas while a review is pending.
Where the encoding proves a stronger result, establish the implication to the
original claim; a different quantifier order is not automatically a weakening.

## Checkpoint B — new argument and actual-input connections

**When:** a new key lemma, reduction, case split, computational interpretation,
or interface connects previously independent pieces. Batch related obligations
into a coherent packet; do not call a model for every routine tactic change.

**Packet:** precise lemma and proof attempt; definitions and assumptions; caller
that supplies those assumptions; relevant type counts, certificates or formulas;
the local change since an earlier review, if any.

**Task:** attempt to falsify the mathematical obligation. Construct candidate
counterexamples, seek a missed case, trace each input premise back to the
original object, and check whether a number or certificate actually means what
the caller needs. For a probabilistic proof, inspect event inclusion and joint
sampling before trusting arithmetic. For other domains, choose the analogous
load-bearing connection rather than importing a probability checklist.

```text
Try to break this lemma or its use at the listed caller. Check the supplied
assumptions against the original input, not just the lemma's own statement.
If you propose a counterexample, verify that it satisfies the premises and
violates the conclusion; otherwise label it a candidate. For computation,
check coverage and the encoding-to-mathematics connection. Return the smallest
specific gap or counterexample you can justify, or state that none was found
in the inspected argument. Do not manufacture a criticism to appear adversarial.
```

**Action:** verify a proposed counterexample or gap yourself, repair the actual
argument and affected callers, compile them, and send the resulting artifacts for
targeted follow-up. A reviewer suggestion to weaken the theorem must remain an
explicit scope change, not a quiet way to close the original task.

## Checkpoint C — final original theorem

**When:** the theorem has been assembled and the local type/axiom audit is ready;
repeat only when a substantive later change affects this conclusion.

**Packet:** authoritative original statement; final definitions; top-level proof
and reductions/branch entry points; actual build target and logs; expanded type
and transitive axiom output; the finished prose proof when it is part of delivery.

**Task:** trace arbitrary original inputs through the final argument and back to
the stated conclusion. Check that no conditional interface remains an input to
the exported theorem. Compare the prose route with the encoded route and report
each actual difference by its effect. Read logs as logs; claim execution only if
the reviewer actually executes the commands in its authorized environment.

```text
Audit this final assembly against the original statement. Follow the actual
declarations and their uses: reductions, domain coverage, witness construction,
and all extra premises at the calls. Check the printed definitions/type and
reported axiom basis. Distinguish a mathematical or semantic defect from a
missing reproduction record or exposition issue. State exactly what you read
and ran. Do not inherit earlier positive opinions or treat a kernel check as
certification of every sentence in the separate prose proof.
```

**Action:** repair any concrete remaining defect, rerun the affected verification,
and request scoped re-review of that change. If the proof is checked while a
required reviewer is unavailable, deliver the formal result with that review
listed as pending; do not label the entire requested workflow finished.

## A review response that can drive work

Ask for a concise response containing:

1. Files/declarations actually read and commands actually executed.
2. Specific objections: location, claimed step, why it fails, a verified witness
   or derivation when possible, and the downstream consequence.
3. Minimum correction or evidence needed for each objection.
4. Scope-limited conclusion and anything material not checked.

A number or “ready” label alone cannot close a mathematical obligation. When an
ARIS reviewer contract requires its own score or verdict, preserve it as review
metadata and still judge the actual mathematical evidence.

## Resolve objections, then re-review the change

Keep the raw response and the executor's decisions separate. One short table in
the existing proof/review log is sufficient:

| Finding and location | Decision and reason | Correction / evidence | Remaining action |
|---|---|---|---|
|Actual reviewer objection|Accept, partially accept, or reject with reasoning|Changed declaration, derivation, or checked witness|Affected obligation or none|

Reproduce the reasoning before accepting a finding. An invalid counterexample,
misread premise, or irrelevant proposed restriction should be rejected with its
specific mathematical reason. For a substantive dispute, send the evidence back
for focused checking; do not count reviewers or average their judgments. A
contradictory pair of opinions is a question to resolve, not a consensus score.

Choose evidence that addresses the objection. A claim that the encoded step does
not compile can be checked against that exact declaration, its expanded type and
actual axiom output. A semantic mismatch cannot be dismissed by a successful
build. A candidate counterexample must satisfy the original premises and negate
the stated conclusion; verify it by an exact argument or checked certificate.
A small Lean example can help, but is not mandatory for every rejected candidate.
Audit the proof declaration's axioms, not merely a `Target : Prop` definition.

Implement an accepted repair before requesting its validation. Identify the
changed statements/callers, provide the new proof and actual output, and ask
whether the particular objection remains. Reopen only affected descendants of
the changed obligation. Routine tactic edits with unchanged meaning and trust
basis need the affected compilation, not another model opinion. A changed trust
basis, actual argument, or claimed theorem can require review even if the public
signature is unchanged. Wording-only changes do not restart mathematical review.

Use the invoked ARIS loop's existing round limit when applicable. Direct
consultations end when the concrete obligations and requested checkpoint reviews
are settled, or when an applicable budget/availability limit prevents progress.
Do not resubmit unchanged artifacts merely to obtain more agreement. If a real
gap survives the available review rounds, keep working on the authorized proof
or hand off the precise gap as the task permits; never convert exhaustion into
proof completion. Do not invent a new user-approval checkpoint for each repair.

## Failure and continuation

On timeout, empty response, interrupted output, quota exhaustion or provider
error, retain the actual failure and keep that review pending. Follow the current
tool/session retry policy; do not count failure as rejection of the theorem or
as a successful review. Continue meaningful local proof work. If both reviewers
were required and only one returned, record that exact state. Same-family help
does not fulfill the missing cross-family review.

At a continuation boundary, save the checkpoint, exact reviewed files or existing
revision/diff, pending concrete findings, reviewer/thread and model metadata, raw
response locations, and next action in the project's existing progress record.
Reuse current evidence for unchanged obligations. No separate scheduling service,
identity framework or additional content-hash system is required.

## Keep the review proportional

The adversary here is a flawed mathematical argument. Review actual quantified
inputs, interfaces and trust assumptions; do not build defenses against unrelated
operational threats. State correct results plainly. Keep source/history logs
separate from the finished proof. Requested verification is real work; repeated
ceremonies with no new mathematical question are not.
