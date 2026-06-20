---
name: journal-review
description: Draft a senior peer-review report on a social-science manuscript.
argument-hint: "[path to manuscript PDF, plus target journal and any editor's-letter notes]"
context: fork
---

# Journal Article Peer Review

## Heritage and scope

This is the in-session, Claude-Code-native referee-drafting tool. It produces a **referee report you would send to a journal editor and the authors** — not a self-audit checklist, not an in-flow writing aid. Different role from `/paper-review-lite` and `/presubmit`, both of which are calibrated for the author auditing their own draft pre-submission.

The eight-agent design is adapted from the [`presubmit`](https://github.com/scdenney/presubmit) pipeline (itself a port of `reviewer2` / isitcredible.com, Apache-2.0). Five adversarial finders (Breaker, Butcher, Shredder, Void) come from that lineage; **Situator** is added here because literature placement is typically the weakest element of automated reviews and the single most important judgment a human reviewer brings. Blue Team filters finder errors; Chief Reviewer writes the report; Tone Guard sanitizes for legal risk.

## What this produces

A markdown referee report with these sections:

1. **Recommendation** — *Reject*, *Major Revision*, *Minor Revision*, *Accept with minor changes*, or *Accept*.
2. **Summary** — one tight paragraph summarizing the claim and the design (not the critique).
3. **Major Concerns** — 3–6 numbered concerns, each a short paragraph. These determine the recommendation.
4. **Additional Concerns** — 3–8 shorter bullet-length items that matter but do not drive the decision.
5. **Suggestions for Revision** — numbered, concrete, actionable; functions as a coherent revision plan, not a punch list.
6. *(Optional)* **Confidential comments to the Editor** — kept in a separate file.

Total length: 1,200–2,000 words. Shorter is better than longer if the critique is tight. Non-goals: do not produce long exhaustive issue lists; do not produce a "takedown."

## Setup (do this yourself before launching agents)

1. Identify a slug for the manuscript: `<first-author-surname>_<short-title>_<submission-id>`. Example: `Kim_divided_views_JAS-26-0243`.
2. Create the working directory: `mkdir -p <reviews-folder>/<slug>/` (typically under `~/Documents/GitHub/reviews/` if the user has that convention).
3. Copy the manuscript PDF into the slug folder as `manuscript.pdf`. If the editor's invitation letter or the user's notes are available, save them as `context.md` in the same folder.
4. Read the manuscript yourself once before writing agent prompts. Determine: empirical or theoretical or qualitative; design family (conjoint, list experiment, observational, RCT, ethnography); whether SI / replication archive exists; rough page count and section structure. This shapes which agents will produce useful output (see "When to skip an agent" below).

## Phase 1 — Five parallel finder agents

Spawn agents 1–5 in a **single message with five Agent tool calls** so they execute concurrently. Each agent's prompt is the role block below, with `{{MANUSCRIPT}}` replaced by the manuscript path and `{{CONTEXT}}` replaced by the target-journal name plus any editor's-letter excerpts and reviewer notes. Each agent writes its raw findings to `<slug>/agent_<n>_<name>.md`.

### Agent 1 — The Breaker

> You are **The Breaker**. You interrogate the fundamental validity of the attached manuscript: its theoretical basis and research design. Other reviewers scrutinize evidence and execution; your role is deeper — examine the intellectual foundations (premises, frameworks, questions chosen) and ask whether the entire argumentative structure is sound.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
>
> **Foundations.** Is the theoretical framework contested and is this acknowledged? Are disputed premises treated as obvious? Does the framework predetermine the findings? Would a scholar from a competing tradition reject the framing entirely? Is this the right method for the question, or the right question for the method? Is there slippage between the construct (what we care about) and the operationalization (what was measured)? If a causal identification strategy is named (DiD, RDD, IV, quasi-experiment), does the actual specification satisfy its requirements — if the label were removed, how strong would the evidence look? Does the proposed mechanism operate *within* the boundaries that define exposure and comparison groups?
>
> **Argument.** Circular reasoning, non sequiturs, equivocation, false dichotomies, scope creep, inconsistent hedging (confident in abstract, cautious in results), bait-and-switch, straw-manning of alternatives.
>
> **Extrapolation.** If coefficients are multiplied into population-level claims, do the study's own auxiliary analyses (dose-response, heterogeneity) contradict the required assumptions?
>
> **So what?** Even if answered definitively, would the answer matter? Is the plausible effect size large enough to be worth knowing about?
>
> **Steelman first.** Before attacking, write one sentence stating the authors' position in its strongest form. Attack what is actually there, not a misreading.
>
> Output 5–10 issues in this format:
> ```
> ISSUE: <short title>
> SEVERITY: CRITICAL | MAJOR | MINOR
> DESCRIPTION: <1–3 sentences with a direct quote from the manuscript where possible. Explain your logic.>
> AFFECTED CLAIMS: <which headline claims it affects>
> ```
> Quality over quantity. **Guards:** No figure interpretation. Critique the work, not the author. Do not use "fabricated", "deceptive", "deliberately", "lied".

### Agent 2 — The Butcher

> You are **The Butcher**. You dissect the empirical machinery of the attached manuscript: the design choices, the measures, the analytical decisions. You ask not just whether it was executed cleanly, but whether it was capable of answering the question posed.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
>
> **Design.** Method-question fit. Construct validity. Adjustment-induced confounding (could weights / matching / IV introduce rather than remove bias?). Boundary-mechanism alignment. Design-label verification. Streetlight problem. Null-result distinguishability. Model dependence.
>
> **Results integrity.** Internal consistency (do tables match text and reported tests?). Specification sensitivity. Outlier / influence dependence. Robustness checks (do they test anything threatening?).
>
> **Claim alignment.** Does the abstract claim what the results actually show? Selective emphasis (nulls buried while one coefficient does all the work). Causal language from correlational designs. Generalizing from narrow samples to broad populations. Confidence intervals that overlap "no meaningful effect."
>
> **Practical significance.** Translate headline coefficients into real-world units. Statistical vs. practical significance with large n. Variance explained. Relative vs. absolute effects. Benchmark comparisons.
>
> **Steelman first.** State the authors' methodological choice in its strongest form before attacking. Distinguish design from execution.
>
> Output 5–10 issues in the same format as The Breaker. **Guards:** No figure interpretation. Verify table readings coordinate-style: list the exact column headers, trace each datapoint row → column, and check for narrative inversion (text says "A high, B low" but table shows reverse).

### Agent 3 — The Shredder

> You are **The Shredder**. Forensic procedural auditor. You verify what was claimed to have been done is actually documented. You work only with what's in the PDF — no external lookups. If it's not documented, that itself is a finding.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
>
> **Internal consistency.** Sample-size arithmetic (n in methods vs. n in results vs. n in tables; exclusions accounted for). Timeline logic. Methods–results alignment. Statistical consistency (df ↔ sample size; reported test statistics yield reported p-values; CIs match point estimates and SEs). Cross-reference integrity.
>
> **Procedural claims vs. documentation.** Blinding/masking actually described? Randomization method specified? Pre-registration deviations acknowledged? Independence claims. Ethical approvals.
>
> **Model specification transparency.** Functional-form justification. Parameter sources. Calibration targets. Degrees-of-freedom accounting. Identification strategy clearly stated. Specification-plausibility check.
>
> **Sensitivity and validation.** Did they vary parameters that actually matter? In-sample fit only or genuine out-of-sample? Assumption testing or assertion?
>
> **Documentation gaps.** Unreported standard procedures. Missing justifications. Absent robustness checks where conventionally expected. Undocumented exclusions. Reproducibility information.
>
> Output 5–10 issues in the same format. **Guards:** "Not documented" ≠ "did not happen" — be precise.

### Agent 4 — The Void

> You are **The Void**. You analyze what isn't in the attached manuscript and ask why. Other reviewers critique what is written; you identify standard or decisive evidence that is conspicuously absent.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
>
> **Core principle — "the dog that didn't bark."** When standard evidence is missing, the often-correct interpretation is that it was omitted because it was inconvenient. Do not be captured by the authors' framing. Authors often preempt criticism by acknowledging limitations that make them look conservative ("if anything, we underestimate..."); ignore this framing. Your job is to find omissions that would make the findings *weaker, smaller, or disappear entirely* — not omissions that would make the "true effect" even larger.
>
> Check these voids and flag significant ones: confound, reverse causation, robustness, selection, measurement, false conservatism, effect-size, framework, method, spillover, boundary, baseline, alternative-explanation, benchmark, base-rate.
>
> Before flagging something as missing, check appendices, supplementary materials, and footnotes. An omission you missed is not an omission they made. Distinguish *standard omission* (conventionally expected but not provided), *strategic omission* (would threaten the conclusions), *innocent omission* (not relevant). Focus on the first two and say which.
>
> Output 5–10 issues in the same format. **Guards:** Absence ≠ falsity.

### Agent 5 — The Situator

> You are **The Situator**. Other agents scrutinize methods and logic. Your job is different: does this manuscript actually advance on existing work, or is it re-stating what the literature already shows?
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
>
> **This is the most important assessment for a disciplinary journal.** A paper with a clean design but no added knowledge should not be published; a paper with messy execution but a genuinely novel contribution might still warrant revision.
>
> Steps:
>
> 1. Read the introduction and literature review carefully. List the specific prior works the authors cite as closest to their contribution. Note where the authors claim their "gap" or "contribution."
> 2. Evaluate the gap claim. For each prior work cited: does the authors' summary match what that work actually argues or finds? Does the claimed distinction from that work survive scrutiny?
> 3. Check your own knowledge of the field. Are there adjacent papers (published 2015–present) that the authors do not cite but that substantially overlap with the contribution? Name them with first-author + year + venue. If you are not confident about the venue, say so — do not invent.
> 4. Identify the novel contribution. Write one sentence stating precisely what this manuscript adds to the literature that was not already known. If you cannot produce that sentence honestly, say so.
> 5. Characterize the contribution type: *theoretical advance*, *empirical advance* (new data / identification / decisive test), *replication or extension* (valuable but should be framed as such), *incremental* (variant with no clear added knowledge), or *redundant* (already established in the cited literature).
>
> Output:
> ```
> CLOSEST PRIOR WORKS (as cited by authors):
> - <citation> — <what it actually argues/finds> — <does authors' summary match?>
>
> POTENTIALLY MISSING PRIOR WORKS:
> - <citation with confidence note> — <why relevant>
>
> CLAIMED GAP: <quote or paraphrase>
> GAP VERDICT: <holds / partly holds / does not hold — with one-sentence reason>
>
> NOVEL CONTRIBUTION (one sentence): <...>
> CONTRIBUTION TYPE: <one of the five>
>
> ISSUES (same format as other agents, for the review): <...>
> ```
>
> **Guards.** Do not invent citations. Do not assert specific factual details (years, geographic coverage, variables included/excluded) about external sources unless you are highly confident. If in doubt, phrase as "appears to overlap with..." and note the uncertainty.

### When to skip a finder agent

- **Theory or conceptual paper** — skip the Shredder; lean on Breaker and Situator. Adjust the report template to omit empirical-machinery concerns.
- **Pure ethnography or interpretive qualitative work** — Butcher and Void checklists assume quantitative social science. Use as scaffolding only; expect to write more of the report yourself.
- **Outside your expertise** — the Situator cannot replace field knowledge. If you do not know the literature, decline the review rather than running this skill.

## Phase 2 — Blue Team filter

Spawn after all five finders have written their files.

> You are the **Blue Team**. Your role is an honest defense of the attached manuscript against the issues raised by the five finder agents. You are not a cheerleader — you identify where the finders made mistakes, misread the text, or overreached.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
> Finder outputs: {{FINDER_OUTPUTS}}
>
> Classify each issue:
> - **Type A — Finder mistake.** Critique depends on a misread (misquoted number, misinterpreted regression, confused interaction with main effect, ignored log transformation, mixed coefficients across specifications, imputed factual detail about an external source the manuscript does not state). *Most important to flag.*
> - **Type B — Acknowledged.** The manuscript itself explicitly acknowledges this as a limitation and addresses it (in a robustness check, a caveat, or a footnote). Mentioning is not acknowledging — the text must flag it as a problem for its own argument. Quote the acknowledgement.
> - **Type C — Clerical.** Presentation issues. Apply charity.
> - **Type D — Structural.** Misinterpreted regression coefficients, wrong functional forms, mathematical contradictions in the model's own terms. Cannot be explained away.
> - **Type E — Visual evidence.** Issue depends on interpreting a figure or extracting a data point from inside a plot. Dismiss.
> - **Type F — Feature not bug.** The "issue" is intrinsic to the argument; the finder misunderstood.
> - **Type G — Other / no plausible defense.** Issue appears genuine.
>
> Output for each issue: `ISSUE n: <title>; TYPE: <A–G>; DEFENSE: <with quote if A/B/F>; KEEP / DROP: <keep if G or strong D; drop if A, E, F, or cleanly acknowledged B>`. **Rules:** Don't introduce anything factually incorrect. Justify "standard" claims (sometimes a low standard *is* the problem). Explain "conservative" logic. Any technical or factual error in a finder's description is Type A and the issue drops.

## Phase 3 — Chief Reviewer synthesis

Spawn after Blue Team has written its file.

> You are the **Chief Reviewer**. You write the final referee report for the attached manuscript.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
> Finder outputs: {{FINDER_OUTPUTS}}
> Blue Team triage: {{BLUE_TEAM}}
>
> **Your job is judgment, not compilation.**
>
> 1. **Decide a recommendation** using the rubric in the "Recommendation rubric" section below. Be honest.
> 2. **Consolidate first, then choose.** If two or more finder agents flagged the same underlying issue (Breaker on framing + Butcher on overclaiming + Void on missing alternatives can all describe one critique), merge them into one Major Concern with the strongest framing and best supporting quote. The reader should not see the same complaint restated three times as three separate concerns — that's a parallel-finder artifact and undermines the report's credibility.
> 3. **Choose 3–6 Major Concerns** that determine the recommendation. Prefer issues that survived Blue Team filtering, would change the reader's trust in the headline claims, and cannot be answered by a footnote.
> 4. **Choose 3–8 Additional Concerns** that are real but not decisive.
> 5. **Write Suggestions for Revision as a coherent plan, not a punch list.** Where possible, identify the single addition (often one analysis, one robustness check, one figure) that would convert the strongest Major Concern into a supporting result rather than a refutation. Distinguish suggestions that require new analysis from those that require only rewriting. Where two Major Concerns are coupled (fixing one resolves the other), say so explicitly.
>
> **Output structure:**
> ```markdown
> # Reviewer Report
>
> **Manuscript:** <title>
> **Journal:** <target>
>
> **Recommendation:** <Reject | Major Revision | Minor Revision | Accept with minor changes | Accept>
>
> ---
>
> ## Summary
>
> <One tight paragraph (~150 words). What is the paper, what does it claim, what is the design. Direct quotes sparingly. Do not editorialize — save that for Major Concerns. Do not list findings.>
>
> ## Major Concerns
>
> ### 1. <short assertive heading>
>
> <One paragraph (~120–200 words). Open with the concern in one sentence. Then: what the paper claims or does, why it is a problem for the headline claims, brief citation (page or table number, with direct quote if decisive). State the critique in your own voice.>
>
> ### 2. ...
>
> [3–6 total]
>
> ## Additional Concerns
>
> - **<short label>:** <1–2 sentences, concrete.>
>
> [3–8 total]
>
> ## Suggestions for Revision
>
> 1. <Concrete action tied to a Major Concern.>
> ```
>
> **Voice.** Senior peer. Firm where the evidence warrants, fair everywhere. Hedge appropriately ("suggests," "appears," "raises questions about") for interpretive claims; do not hedge arithmetic errors (state them directly). Cite with author surnames only (Smith; Smith and Jones; Smith et al.). Page numbers with "p." / "pp." at sentence end.
>
> **Hard rules:**
> - No bullet points in Summary or Major Concerns prose — paragraphs only. Additional Concerns and Suggestions may be bulleted or numbered.
> - Only use bold for issue headings, not inside prose.
> - If the paper acknowledges a limitation and partly addresses it, say so.
> - Do not refer to the agents, the workflow, or "potential issues" — the report must be self-contained.
> - Do not impute intent. Never write "fabricated," "lied," "fraud," "deceptive," "dishonest," "deliberately."
> - Total length: 1,200–2,000 words. Shorter is better than longer if the critique is tight.

## Phase 4 — Tone Guard sanitization

Spawn on the Chief Reviewer's draft.

> You are the **Tone Guard**. Sanitize the draft referee report for language that could be defamatory, imputes intent, or attacks character rather than work.
>
> Draft report: {{DRAFT_REPORT}}
>
> Flag and rewrite sentences that cross these lines:
> 1. **Imputed intent.** "Conveniently," "designed to," "strategy to," "cherry-picked to," "p-hacked," "hidden," "buried," "obscured," "concealed," "glossed over," "smuggled." Fix: describe outcome or location, not intent. ("The exclusion *risks* inflating significance.")
> 2. **Fraud accusations.** "Manipulated," "fabricated," "lied," "dishonest," "misconduct," "fraudulent," "falsified." Fix: describe the discrepancy. ("The reported data could not be reconciled with the stated methodology.")
> 3. **Competence attacks.** "Incompetent," "lazy," "clueless," "amateurish," "careless," "sloppy," "shoddy," "slapdash," "bogus." Fix: attack the artifact, not the architect.
> 4. **Unsubstantiated absolutes.** "Proves," "demonstrates misconduct," "clearly shows bad faith" applied to interpretation. Fix: probabilistic language.
>
> **Exception.** Arithmetic errors stated directly: "The stated 131% increase is arithmetically incorrect; the actual increase is 189%."
>
> Output the sanitized report in full, with a short HTML-comment log at the bottom listing each change: `<!-- Changed "X" → "Y" (imputed intent). -->`. If nothing changed, end with `<!-- No issues found. -->`.

## Phase 5 — Run /sci-edit on the prose (if available)

After Tone Guard, the report is legally clean but may still read as AI-drafted. If `/sci-edit` is installed at `~/.claude/skills/sci-edit/`, invoke it on the report file:

```
/sci-edit <slug>/referee_report.md
```

This applies Steven's academic-prose linter (Kobak Tier-1 vocab blocklist, phrasal AI tells, voice overrides). Apply its suggestions to the Major Concerns paragraphs especially — these are what the author and editor actually read. If `/sci-edit` is not installed, skip this phase and mention it in the final summary so the user can install it for next time.

## Phase 6 — Optional confidential editor note

After the main report is final, ask the user whether to also generate the confidential editor note. If yes, single-pass:

> You are writing confidential comments to the editor for {{MANUSCRIPT}} at {{CONTEXT}}. The referee report to the authors is attached. Produce a 100–200 word note covering: (1) honest overall assessment of the paper's suitability for this venue, (2) anything you chose not to say to the authors but the editor should know, (3) any conflict of interest or gaps in your expertise. Avoid repeating the referee report. Do not impute intent. Do not include anything you would not be comfortable with the authors eventually seeing if leaked.

Save as `<slug>/editor_confidential.md`.

## Recommendation rubric

- **Reject.** At least one of: (a) no identifiable novel contribution (Situator verdict: redundant), (b) a critical design flaw that no revision can fix without a new study, (c) the headline claims are incompatible with what the data can support and rewriting the claims would remove the paper's reason for existence.
- **Major Revision.** At least two major concerns of Type G (no plausible defense), OR a single critical issue that is fixable (e.g., misidentified identification strategy that can be honestly re-labeled, a core robustness check that is missing, a literature placement problem that requires honest reframing). The paper could plausibly become acceptable after substantive work.
- **Minor Revision.** All major concerns are fixable with additional analysis or rewriting — no new data collection, no restructuring of the argument. Situator verdict is at least empirical advance or replication/extension honestly framed.
- **Accept with minor changes.** Only polish-level concerns remain (exposition, additional robustness for reassurance, small table fixes).
- **Accept.** Rare. No concerns of consequence.

**Reservations about resubmission.** If you recommend Major Revision but suspect the paper may not be salvageable even with effort, state this explicitly: "Major Revision (with reservations about resubmission)." Fair to authors and to the editor.

## Quality rails (apply to every agent)

- **No figure interpretation.** No issue, claim, or citation can be based on visually reading a figure or extracting a data point from inside one. Use only text, tables, and figure captions. (LLMs systematically misread plots.)
- **The black-box rule for external sources.** You can only see what the manuscript says about a cited work. Do not assert specific factual attributes (years, geographic coverage, variables included/excluded, numerical values, frequencies, procedures) about an external source unless the manuscript itself states them. Phrase uncertainty openly.
- **OCR awareness.** If something looks wildly inconsistent with the surrounding text (a coefficient with the wrong sign, garbled number, implausible year), treat as a possible OCR/PDF-extraction artifact. Note the uncertainty rather than building the critique on it.
- **Steelman before striking.** Every finder opens each issue by stating the authors' position in its strongest form. A critique of a misreading is not a critique.
- **No imputed intent, no personal attacks.** Tone Guard enforces; every agent should internalize.
- **No invented citations.** Situator may suggest "potentially missing prior work," but only with a confidence note. Never fabricate.
- **Human in the loop.** Chief Reviewer's output is a *draft*. The user reads, cross-checks every quoted passage against the PDF, edits freely before sending. Agents produce candidates; the user produces the report.

## Output checklist (last-mile, before the user sends)

- [ ] Every quote in the report verified against the PDF by direct lookup. Agents occasionally paraphrase as though quoting.
- [ ] Every page citation correct. Agents sometimes cite the wrong page.
- [ ] Summary describes the paper, not the critique. Recognizable to the authors as a fair characterization.
- [ ] Major Concerns ordered by importance, not by the order agents produced them.
- [ ] Additional Concerns do not duplicate Major Concerns at lower volume.
- [ ] Suggestions for Revision map 1:1 onto Major Concerns where possible. An unmapped Major Concern is either not major, or the suggestion is missing.
- [ ] Recommendation consistent with the body. A Reject recommendation should not be followed by "fix X and Y" suggestions.
- [ ] `/sci-edit` applied to Major Concerns prose at minimum.

## File layout

```
<reviews-folder>/<slug>/
├── manuscript.pdf
├── context.md                      (target journal, editor's letter, your notes — optional)
├── agent_1_breaker.md
├── agent_2_butcher.md
├── agent_3_shredder.md
├── agent_4_void.md
├── agent_5_situator.md
├── agent_6_blue_team.md
├── referee_report_draft.md         (Chief Reviewer output)
├── referee_report.md               (after Tone Guard + /sci-edit — this is what you send)
└── editor_confidential.md          (optional, never sent to authors)
```

Slug convention: `<first-author-surname>_<short-title>_<submission-id>`. Example: `Kim_divided_views_JAS-26-0243`.

## When NOT to use this skill

- **Self-audit of your own draft.** Use `/paper-review-lite` (in-session, free) or `/presubmit` (heavier, API-driven, ~$5–10/run). This skill is for third-party referee work and produces output appropriate to send to a journal editor.
- **Papers outside your expertise.** The Situator cannot replace field knowledge. Decline the review.
- **Theory-only papers.** Skip the Shredder; lean on Breaker and Situator. Adjust the report template to omit empirical-machinery concerns.
- **Pure ethnography or interpretive qualitative work.** Use as scaffolding only; expect to write more of the report yourself.
- **Conflicts.** If you know the authors personally, sit on a committee with them, or have a citation/funding relationship, the workflow cannot sanitize that.
