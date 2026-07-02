---
name: aer-rebuttal
description: Use when responding to a Revise & Resubmit decision from AER, AER:Insights, or an AEJ, and a point-by-point response letter plus aligned manuscript revisions are needed. Handles triage, the concede / clarify / push-back decision, and the response-letter format that editors actually read.
---

# AER Rebuttal

## Overview

A Revise & Resubmit at AER is precious. The rebuttal goal is **not** to "defend the paper"; it is to give the editor a credible package they can send back to referees with confidence.

Rule: **revise the manuscript first; write the response letter against the revised manuscript, never the old draft.**

## When to Use

- An R&R decision has arrived
- A "reject and resubmit" requires a structured response
- A conditional acceptance comes with minor revisions
- The user needs to decide which reviewer comments to concede, clarify, or push back on

Do not use this skill for:

- Initial submission (use `aer-submission`)
- Pre-emptive robustness drafting (use `aer-robustness`)
- Writing referee reports as a reviewer (different conventions)

## Response Principle

Every reviewer comment ends in **exactly one** of:

1. **Clarified in response only** — no manuscript change; the answer was already there but hard to find
2. **Revised in manuscript only** — change made, briefly noted in response
3. **Revised in both manuscript and response** — change made, response explains the substance
4. **Respectfully declined with justification** — change not made, explicit rationale given

No comment ends in the vague middle ground.

## Triage Workflow

### Step 1 — Parse

Convert the editor letter and each referee report into an **atomized list** of comments. Number them: E1, E2, ... for editor; R1.1, R1.2, ... for Referee 1; R2.1, ... for Referee 2.

### Step 2 — Classify

For each comment, assign **one** category:

| Category              | Definition                                                                 |
|-----------------------|----------------------------------------------------------------------------|
| `misunderstanding`    | The paper answers this, but the answer was buried                          |
| `clarity_problem`     | The argument is fine; the prose caused confusion                           |
| `evidence_gap`        | A genuine missing analysis or robustness check                             |
| `scope_mismatch`      | Reasonable request, but outside the paper's contribution                   |
| `incorrect_premise`   | Comment based on a factual or interpretive error                           |
| `high_risk`           | Challenges novelty, validity, identification, or central claim             |

### Step 3 — Severity

| Severity   | When to assign                                                            |
|------------|---------------------------------------------------------------------------|
| `minor`    | Presentation, citation, small method detail                               |
| `major`    | Evidence, statistics, method, scope — affects editorial confidence        |
| `blocking` | Identification flaw, ethics, central-claim challenge — cannot draft around |
| `unclear`  | Insufficient information; ask the editor for clarification                |

### Step 4 — Action

Based on category + severity:

| Category × Severity                  | Action                                                  |
|--------------------------------------|---------------------------------------------------------|
| `misunderstanding` × any             | Clarify in response; add cross-reference in manuscript  |
| `clarity_problem` × any              | Revise manuscript; brief response                       |
| `evidence_gap` × minor               | Add robustness check; report in appendix                |
| `evidence_gap` × major               | Add analysis; report in main text or substantial appendix |
| `evidence_gap` × blocking            | Restructure paper or escalate — may need new identification |
| `scope_mismatch`                     | Push back politely; cite scope boundary                 |
| `incorrect_premise`                  | Push back; cite the manuscript evidence that refutes    |
| `high_risk` × any                    | Address head-on; never deflect                          |

## When to Concede

Concede when:

- A claim is stronger than the evidence supports
- A control, comparison, or limitation statement is genuinely missing
- The reviewer correctly identifies an evidence gap that is feasible to fill
- Wording created a reasonable misunderstanding

Best move:

- **Narrow the claim** in the manuscript
- **Add the missing evidence** if feasible
- **Thank the reviewer explicitly** for improving precision

## When to Clarify Without Major Work

Clarify when:

- The requested result exists but is hard to find
- The reviewer missed a definition or setup
- The point can be addressed by reorganization or cross-reference

Best move:

- **Revise for discoverability** (move the buried fact forward, add a cross-reference)
- **Do not imply** that a major scientific issue was fixed if only presentation changed

## When to Push Back

Push back only when:

- The request depends on a false premise
- The requested analysis is outside the paper's scope
- The request would require a fundamentally different paper
- The current evidence already answers the concern

Best move:

- **Acknowledge** the concern as reasonable
- **Explain** the boundary precisely
- **Point to** the existing evidence
- Avoid defensive tone

## Handling Reviewer Disagreement

When R1 and R2 contradict on the same point: **target the supportive reviewer.** The editor's own preferences usually align with the more enthusiastic report. Address the dissenting reviewer respectfully, explain the alternative interpretation, and avoid making the manuscript worse to satisfy a minority view.

## Response Letter Format

### Structure

```
[Date]
[Editor name]
[Journal]

Dear [Editor],

Thank you for the opportunity to revise our manuscript [Title], MS#[XXX].
We are grateful for the constructive comments from you and both referees.
This revision addresses all comments as detailed below. Major changes include
[2-3 sentences summarizing the most substantive revisions].

Below we reproduce each comment in italics, followed by our response in
plain text. Page and line references are to the revised manuscript.

[Sincerely,]
[Authors]

---

# Response to the Editor

## Comment E1
*[Verbatim quote of editor comment.]*

**Response.** We agree. We have [action taken]. See revised manuscript,
page 4, lines 14-22.

---

# Response to Referee 1

## Comment R1.1
*[Verbatim quote.]*

**Response.** [State the action in the first 1-2 sentences.]
[Then provide substance.] See revised manuscript, page X, Section Y.

## Comment R1.2
*[...]*

---

# Response to Referee 2
...
```

### Per-Comment Discipline

- **Quote or paraphrase** the comment fairly. Do not paraphrase a sharp criticism into a gentler version.
- **Lead with the action.** The first 1-2 sentences of the response must state what was done: revised / clarified / declined.
- **State agreement explicitly** when not obvious from the action.
- **Distinguish** between what was changed, what was clarified, and what was not changed and why.
- **Cite the revised location** by page, section, table, figure, or line number. AER reviewers verify.
- **If a claim was softened, say so.** Do not hide a concession in passive voice.

### Editor-Efficiency Rule

Assume the editor scans for three things on each comment:

1. Do the authors agree or disagree?
2. What concrete revision was made?
3. Where can that revision be found?

Write the first sentence of every response so all three answers are visible.

### Per-Comment Action Ledger

Keep one ledger row per comment:

```text
R2.3 | both | Table A.4 placebo: beta = 0.006, SE = 0.019, p = 0.74 | pp. 18-19
```

## Tone

Prefer:

- Respectful
- Direct
- Specific
- Non-defensive
- Evidence-led

Avoid:

- Over-thanking ("we deeply appreciate the reviewer's profound insight ...")
- Vague promises ("we have improved the discussion of ...")
- Evasive wording ("the reviewer raises an important point that we believe is consistent with our interpretation")
- Replying to criticism with hype
- Claiming a concern was addressed when only wording changed

## Revision Mechanics

1. **Edit the manuscript first.** Make every change the response will reference.
2. **Generate a marked-up version** (LaTeX `latexdiff`, or Word track-changes) and a clean version.
3. **Cross-check** the response letter against the revised manuscript — every page/line reference must resolve.
4. **Update table and figure numbering** if exhibits were added or removed; cite the new identifiers.
5. **Re-run the replication package** if results changed; re-deposit if material.
6. **Re-run `aer-consistency`** on the revised manuscript — revisions are where headline numbers, exhibit numbering, and citations desynchronize.

## Decision Letter Conventions

If the editor wrote a summary letter with their own priorities (common at AER), treat the **editor's letter as authoritative**. When editor and referee disagree, follow the editor. Acknowledge the conflict in your response to the relevant referee comment.

## What Not to Do

- Write the response before deciding the manuscript revisions
- Quote a comment, thank the reviewer, then never state the action
- Promise to "consider" a request without specifying outcome
- Argue with a reviewer's tone or competence
- Send a 50-page response letter — editors compress
- Concede to every comment to seem agreeable — at AER, defending the design when correct signals confidence
- Submit a revision without re-reading the editor letter as if it were a fresh referee report

## Pre-Submission Checklist

- [ ] Every comment numbered and addressed
- [ ] Each response leads with the action taken
- [ ] Every page/line reference resolves in the revised manuscript
- [ ] Marked-up and clean versions of the manuscript both prepared
- [ ] Cover letter to the editor summarizing the major revisions (1 page)
- [ ] Updated replication package if results changed
- [ ] Tone is direct, not defensive
- [ ] Pushed-back comments have substantive rationale, not stonewalling
- [ ] Conceded comments have visible manuscript changes
- [ ] Revision timeline within the editor's window

## Repository Resources

When working from the AER-skills repository or plugin bundle, read `examples/rebuttal-example.md` only when the user needs a complete response-letter model or a concrete triage example.

## Handoff

```text
COMMENTS TOTAL: <n>
COMMENTS BY ACTION: <conceded / clarified / both / declined>
SEVERITY DISTRIBUTION: <minor / major / blocking>
MANUSCRIPT CHANGES MADE: <yes — list / no>
RESPONSE LETTER LENGTH: <n> pages
READY TO SUBMIT REVISION: <yes / no — with blockers>
NEXT SKILL: aer-submission (final preflight on the revised package)
```

## Anti-Patterns

- A response letter longer than the paper
- "We agree with the reviewer" followed by no manuscript change
- Hedging on identification — at AER, the identification strategy is either defensible or it is not
- Deferring blocking comments to "future work"
- Inventing robustness checks the reviewer did not ask for, to pad the response — referees notice
- Changing the abstract without re-checking the 100-word limit on the revised version
