---
name: aer-submission
description: Use when running the final pre-submission audit for an AER, AER:Insights, or AEJ manuscript — length, format, cover letter, per-author disclosure statements, file packaging, and routing among the AEA journal family. Apply immediately before clicking submit.
---

# AER Submission

## Overview

The final submission audit catches the formatting and routing mistakes that produce avoidable desk rejections. AER's editorial office returns submissions for non-compliance with length, format, or policy requirements before the editor sees the paper — a turnaround that can cost weeks.

This skill is the last gate.

## When to Use

- Within 48 hours of submission
- After every R&R, before resubmission
- When the user is undecided between AER and AER: Insights as the final target
- After a rejection elsewhere, when routing into the AEA family

## Hard Format Constraints

| Item                          | AER                                    | AER: Insights                          |
|-------------------------------|----------------------------------------|----------------------------------------|
| Abstract length               | ≤ 100 words                            | ≤ 100 words                            |
| Main text length              | ~40 pages (11-pt, 1.5-spaced, 1" margins) | ≤ 7,000 words minus 200 per exhibit; ≤ 6,000 with five exhibits |
| Maximum exhibits              | No formal cap                          | 5; each exhibit reduces budget by 200 words |
| Word-count basis              | Page guideline includes figures, tables, references, and in-paper appendices | Main body, footnotes, endnotes, and in-paper appendices; excludes references, exhibits, and Supplemental Appendix |
| File format                   | Single PDF for review                  | Single PDF for review                  |
| Separate title page           | None — title and byline on page 1      | Same                                   |
| Cover letter                  | Optional                               | Optional                               |
| Submission system             | ScholarOne (mc.manuscriptcentral.com/aer) | ScholarOne                             |

**Manuscripts exceeding AER: Insights length are returned without review.** This is enforced automatically.

## Length Audit (AER)

The 40-page guideline counts:

- Main text
- Footnotes
- In-paper tables and figures
- References
- In-paper appendix

The 40-page count does not include: title, abstract, supplemental appendix, online appendix.

If over 40 pages: cut, then cut again, then move material to the online appendix. AER editors explicitly state that excessive online-appendix reliance is itself a desk-rejection signal. The supplemental appendix is for *additional* material, not for the main result.

## Length Audit (AER: Insights)

Count main-body words including footnotes, endnotes, and in-paper appendices; exclude title, byline, abstract, acknowledgement footnote, references, exhibits, and Supplemental Appendix. Word-count discipline:

- One exhibit costs ~200 words
- Five exhibits leave 6,000 words
- Zero exhibits leave 7,000 words

If you cannot fit, the paper is an AER (or AEJ) paper, not an AER: Insights paper.

## Manuscript Structure

```
[Title]
[Authors and affiliations]
[Abstract — ≤ 100 words]
[JEL codes]
[Keywords]

[Introductory paragraphs — NO heading "Introduction"]

\section{Data}             (or whatever the next titled section is)
\section{...}
...
\section{Conclusion}

\bibliography{...}

[Tables in numerical order]
[Figures in numerical order]

\appendix
\section{...}              (in-paper appendix only — short)
```

AER numbers sections with **Roman numerals** (I., II., III.) and subsections with capital letters (A., B., C.); the introduction is unnumbered. In LaTeX, set `\renewcommand{\thesection}{\Roman{section}}` or use the AEA sample article class, which applies house style automatically.

Move long appendices to a separate Supplemental Appendix file.

## File Package for ScholarOne

Prepare in advance:

1. **Manuscript PDF** — single file: text + references + tables + figures + in-paper appendix
2. **Supplemental Appendix PDF** — optional, separate file
3. **Cover letter** — only if needed (see below); via form field, not separate document
4. **JEL classification codes** — primary and secondary
5. **Disclosure Statement PDFs** — one separate PDF per coauthor; if nothing to disclose, say that explicitly
6. **Coeditor conflict disclosures** — list any coeditor who has a personal or professional conflict
7. **Suggested editor** — optional, in form field
8. **AI usage disclosure** — required if AI software was used in drafting or editing; brief description

If the paper has supplementary materials (videos, large datasets), provide URLs to a public repository.

## Cover Letter — When and How

AER **does not require a cover letter**. Use one only to communicate substantive information:

- **Conflict of interest** with a coeditor (e.g., recent coauthor, advisor, family member). Identify by name.
- **Data access limitations** that the editor needs to know in advance (e.g., restricted data with specific replication arrangements).
- **Previous submission history** to another AEA journal if relevant.

If you include one, **keep it ≤ 200 words** and submit via the ScholarOne form field, not as a separate uploaded document.

Do **not** use the cover letter to:

- Pitch the paper's contribution (the abstract does that)
- List the seminars where the paper was presented (the title-page footnote does that)
- Argue against potential referees (this is counterproductive)

## Routing Decision: AER vs. AER: Insights vs. AEJ

Run this decision tree before submission:

```
Is the contribution sharp enough to fit the AER: Insights word/exhibit formula?
├── Yes → Is it cross-subfield interest?
│   ├── Yes → AER: Insights
│   └── No → AEJ: Applied / Policy / Macro / Micro (by subfield)
└── No → Does it have broad cross-subfield interest?
    ├── Yes → AER
    └── No → AEJ (most fitting)
```

Common mistakes:

- Submitting a long-form paper to Insights "in case." Insights requires *brevity by design*, not by truncation.
- Submitting to AER when the contribution is solidly within one subfield. AEJ acceptance is faster, cheaper, and similar in audience for many topics.
- Treating the AEJ family as a fallback after AER rejection. The clock resets; conditional probability of acceptance is unchanged. Submit where the paper actually fits.

## Submission Fees

AER charges a submission fee that scales with AEA membership status and country income group. Authors from low- and middle-income countries pay reduced or waived fees. Verify current fee schedule on the AEA submissions page before the corresponding author finalizes the form.

## Final Preflight Checklist

- [ ] Abstract ≤ 100 words (run a word count, not a glance)
- [ ] Main text within length limit (≤ 40 pages for AER; word-count for Insights)
- [ ] No "Introduction" heading; introductory material starts on page 1 after title
- [ ] All tables use booktabs rules; captions positioned correctly
- [ ] All figures are vector (PDF / EPS); each has a notes block
- [ ] References complete; in-text citations match bibliography
- [ ] JEL codes selected (primary + secondary)
- [ ] Disclosure Statement PDF prepared for each coauthor
- [ ] Coeditor conflicts disclosed
- [ ] AI usage disclosed if applicable
- [ ] Replication package deposit started (not required at submission but plan it now)
- [ ] If field experiment: AEA RCT Registry entry exists and is referenced
- [ ] Author contributions and acknowledgements present in the title-page footnote
- [ ] No tracked changes, no comments, no draft watermarks in the PDF
- [ ] Single self-contained PDF; supplemental appendix as separate file
- [ ] Corresponding author email and ORCID up to date

## Repository Resources

When working from the AER-skills repository or plugin bundle, load only the
relevant resource:

- Submission no-go checklist: `docs/desk-rejection-audit.md`
- Current policy source register: `docs/source-register.md`
- Replication planning surface: `skills/aer-replication/SKILL.md`
- Deposit-ready scaffold: `examples/replication-package-skeleton/`

## After Submission

- Expect 8-12 weeks to first decision for AER (median); shorter for Insights
- Desk rejection: typically within 2-4 weeks
- A "reject and resubmit" (rare) signals interest but requires substantial restructuring
- Track via ScholarOne; do not email the editorial office for status before 12 weeks

## Handoff

```text
TARGET VENUE: <AER | AER:Insights | AEJ:...>
LENGTH AUDIT: <pass / fail with details>
FORMAT AUDIT: <pass / fail with details>
COVER LETTER: <none / drafted, <n> words>
DISCLOSURE STATEMENTS: <complete / missing>
CONFLICTS DISCLOSED: <list / none>
REPLICATION DEPOSIT STATUS: <planned / drafted / complete>
READY TO SUBMIT: <yes / no — with blockers>
NEXT SKILL: <none — submit | aer-rebuttal once decision arrives>
```

## Anti-Patterns

- Submitting a manuscript whose abstract is 108 words "but should be fine"
- Including a 600-word cover letter that pitches the paper
- Uploading the LaTeX source as the review PDF
- Listing JEL codes that do not match the paper's content
- Submitting an Insights paper at 7,800 words because it has only two exhibits — the formula gives ≤ 6,600
- Holding the replication deposit until "after acceptance" — the Data Editor delay is now part of the publication timeline
