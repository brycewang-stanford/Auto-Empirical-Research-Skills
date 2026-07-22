# Response-Letter Patterns

*Bundled with the `aer-rebuttal` skill so the guidance works without the repository checkout. SKILL.md routes; this file carries the depth.*

The goal of an R&R response is not to defend the paper; it is to give the
editor a credible package they can send back to referees with confidence.
Everything below serves the editor's three-question scan on each comment:
do the authors agree, what concrete revision was made, and where can it be
found. Write the first sentence of every response so all three answers are
visible.

## Taxonomy of Referee Comments

Classify every atomized comment into exactly one type before choosing a
move. The type predicts the move; severity (minor / major / blocking)
predicts how much manuscript work the move requires.

| Type | Signature | Default move |
|---|---|---|
| Demand-for-analysis | "Please add / re-estimate / report X" — a genuine evidence gap | Concede: run the analysis, report it |
| Misunderstanding | The paper already answers this, but the answer was buried or worded poorly | Clarify: surface the buried fact, add a cross-reference |
| Scope-expansion | Reasonable question, but it belongs to a different paper | Decline: name the scope boundary, flag as future direction |
| Taste | A preference about framing, emphasis, or style with no evidence stake | Concede cheaply if harmless; decline briefly if it degrades the paper |
| Fatal-flaw claim | Challenges identification, novelty, or the central claim | Rebut or concede head-on — never deflect, never partial-answer |

Rules of classification:

- A misunderstanding is still the authors' problem: if a competent referee
  missed it, the writing caused it. The fix is discoverability, not a lecture.
- A fatal-flaw claim resting on a false premise is rebutted with manuscript
  evidence; one resting on a real gap is conceded even if expensive.
- When two referees contradict each other on the same point, target the
  supportive reviewer's position, address the dissent respectfully, and do
  not make the manuscript worse to satisfy a minority view.

## Decision Rules: Concede / Clarify / Rebut / Decline

Every comment ends in **exactly one** of the four moves — no vague middle.

**Concede** when a claim is stronger than the evidence, a control or
limitation statement is genuinely missing, or the gap is real and feasible
to fill. Best move: narrow the claim, add the evidence, thank the reviewer
explicitly for improving precision. A concession requires a visible
manuscript change — a concession with no diff is a promise, not a response.

**Clarify** when the requested result exists but is hard to find, or the
referee missed a definition or setup. Revise for discoverability (move the
buried fact forward, add a cross-reference) — and never imply a scientific
issue was fixed when only presentation changed.

**Rebut** when the comment rests on a false premise or the current evidence
already answers the concern. Acknowledge the concern as reasonable, point to
the specific exhibit or derivation that refutes it, and invite further
guidance rather than closing the door.

**Decline** when the request is outside the paper's contribution or would
require a fundamentally different paper. Explain the boundary precisely,
optionally add a sentence in the conclusion flagging the question, and do
not pretend the request is unreasonable.

## Paragraph Templates

Reproduce the comment verbatim in italics; respond in plain text; lead with
the action verb. Slots are in bracketed caps.

### Concede

```text
*[COMMENT-QUOTE]*

**Response.** Agreed and revised. We have [ACTION-TAKEN: replaced /
added / re-estimated] [SPECIFIC-CHANGE]. The new result is
[KEY-NUMBER] ([UNCERTAINTY]), compared with [OLD-NUMBER] in the
original draft; [ONE-SENTENCE-WHY-IT-MOVED-OR-DID-NOT]. See revised
manuscript, [REVISED-SECTION], [REVISED-EXHIBIT], page [PAGE-NUMBER].
We are grateful to the referee for prompting this change.
```

### Clarify

```text
*[COMMENT-QUOTE]*

**Response.** Clarified. The [REQUESTED-FACT] appears in
[ORIGINAL-LOCATION] of the original draft; we recognize it was easy
to miss. To make it discoverable we have [DISCOVERABILITY-FIX: moved
it to / added a cross-reference at] [REVISED-LOCATION], page
[PAGE-NUMBER]. No analysis changed.
```

### Rebut

```text
*[COMMENT-QUOTE]*

**Response.** Respectfully disagree. The concern rests on
[PREMISE-AT-ISSUE]; in fact [MANUSCRIPT-EVIDENCE: exhibit, derivation,
or institutional fact] shows [WHY-THE-PREMISE-FAILS]. We have added
[CLARIFYING-ADDITION] at [REVISED-LOCATION], page [PAGE-NUMBER], to
make this explicit for future readers. If the referee intended a
different reading, we would welcome further guidance.
```

### Decline

```text
*[COMMENT-QUOTE]*

**Response.** Declined with justification. [REQUESTED-EXTENSION]
would require [WHY-OUT-OF-SCOPE: a different identification strategy /
data the setting cannot provide / a separate paper]. The present
paper's contribution is [SCOPE-BOUNDARY-SENTENCE]. We have added a
sentence in [REVISED-LOCATION], page [PAGE-NUMBER], flagging
[REQUESTED-EXTENSION] as a distinct question, but do not extend the
analysis here.
```

Note that even the rebut and decline templates cite a revised location: a
push-back that leaves zero trace in the manuscript reads as stonewalling.

## Response-Letter Layout

- **One cover letter to the editor** (one page): thanks, manuscript title
  and number, then 2-3 numbered bullets naming the most substantive
  revisions so the editor knows what to look for in 60 seconds.
- **Then one response document per reviewer**, in order: Response to the
  Editor, Response to Referee 1, Response to Referee 2, and so on.
- **Number every comment**: E1, E2 for the editor; R1.1, R1.2 for Referee
  1; R2.1 for Referee 2. Atomize multi-part comments into separate numbers
  rather than answering three questions in one paragraph.
- **Cross-reference between referees** when two comments converge: "This is
  the same concern as R1.1; the new specification in Table 5 addresses
  both" — and repeat the key numbers rather than forcing the referee to
  flip to another referee's section. Each referee typically sees only their
  own responses plus the editor letter.
- **State the convention once, up front**: comments reproduced in italics,
  responses in plain text, all page and line references to the revised
  manuscript.
- Keep a one-line ledger row per comment (id | move | key evidence |
  pages) for the pre-submission cross-check.

## Tone Rules

- Respectful, direct, specific, non-defensive, evidence-led. Never
  sarcastic, never wounded, never a rebuttal of the referee's tone or
  competence.
- Never "as we already said" or "as should be clear from Section 3" — if
  the referee missed it, the burden was on the writing. Say where the fact
  lives and how the revision makes it easier to find.
- No over-thanking ("profound insight"), no hype in reply to criticism, no
  evasive constructions ("we believe the point is consistent with our
  interpretation").
- If a claim was softened, say so plainly. Do not hide a concession in
  passive voice; editors read a visible concession as strength.
- Quote or paraphrase each comment fairly — never paraphrase a sharp
  criticism into a gentler version before answering it.

## The Revised-Manuscript Rule

Revise the manuscript first; write the response letter against the revised
manuscript, never the old draft. Every page, section, table, and line
reference in the letter resolves in the **revised** version. Mechanics:
make every change first, generate marked-up and clean versions, cross-check
every reference in the letter against the clean revision, renumber exhibit
citations if exhibits moved, and re-run the consistency audit — revision
rounds are where headline numbers and numbering desynchronize.

## Common Failure Modes

- **Responding to the old draft**: page references that resolve in the
  submitted version but not the revision; a "see Figure 2" pointing at an
  exhibit the revision renumbered.
- **Burying the concession**: three sentences of context before admitting
  the claim was narrowed, or a softened claim never acknowledged as
  softened.
- **Promising future work instead of doing it**: "we will consider adding
  this analysis" on a feasible request. Feasible requests are done or
  declined with justification — deferral of a blocking comment to future
  work is a rejection invitation.
- **Thanks-without-action**: quoting the comment, thanking the reviewer,
  and never stating what changed or where.
- **Concede-everything agreeableness**: conceding to every comment to seem
  cooperative. Defending the design when it is correct signals confidence.
- **Padding**: inventing robustness checks nobody asked for, or a response
  letter longer than the paper — editors compress.
- **Forgetting the abstract**: editing headline claims without re-checking
  the 100-word limit and the headline numbers on the revised version.

## Canonical repo sources

Distilled from these repository files (they require the repository checkout):

- `skills/aer-rebuttal/SKILL.md` — triage workflow, category and severity
  tables, response principle, and the pre-submission checklist
- `examples/rebuttal-example.md` — a complete worked response letter
  showing all four moves on a fictional broadband paper
