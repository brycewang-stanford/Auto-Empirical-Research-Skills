# Final Pre-Submission Audit Checklist

*Bundled with the `aer-submission` skill so the checklist works without the repository checkout. SKILL.md routes; this file carries the depth.*

Policy anchors: AER submission rules, https://www.aeaweb.org/journals/aer/submissions; AER: Insights submission rules, https://www.aeaweb.org/journals/aeri/submissions. Every item below is something the editorial office or the editor can check without reading the paper closely — which is exactly why each one can decide the verdict on its own.

## 1. Abstract — exactly at or under 100 words

- [ ] Abstract is ≤ 100 words by a mechanical count, not a glance.
- [ ] The abstract leads with the result, not the motivation.
- [ ] No citations, no undefined acronyms, no "we also" clauses.
- [ ] The abstract pasted into the submission form is identical, word for word, to the abstract in the manuscript PDF.
- [ ] Recount after every revision round — abstracts drift over the limit during editing.

**Counting rule.** Copy the abstract text only — no title, byline, JEL codes, or keywords — into a plain-text word counter (`wc -w` on the pasted text, or `texcount` on the abstract environment). Count hyphenated compounds as one word, numbers and statistics as one word each, and spelled-out equation fragments word by word. If the mechanical count reads 101, cut a word; "should be fine" at 101+ is the classic avoidable bounce.

## 2. Length accounting

### AER (~40 typeset pages)

The guideline is approximately 40 pages at 11-point font, 1.5 spacing, 1-inch margins, counting:

- [ ] Main text and footnotes
- [ ] In-paper tables and figures
- [ ] References
- [ ] In-paper appendix

Not counted: title, abstract, and the separate supplemental/online appendix. If over 40 pages: cut, cut again, then move material to the online appendix — but note that heavy online-appendix reliance is itself a desk-rejection signal. The supplemental appendix holds *additional* material, never the main result.

### AER: Insights (7,000 words minus 200 per exhibit)

Budget formula: `word limit = 7,000 - 200 x (number of exhibits)`, with a hard cap of 5 exhibits. Worked arithmetic:

| Exhibits | Arithmetic | Word budget |
|---|---|---|
| 0 | 7,000 - 0 | 7,000 |
| 3 | 7,000 - 600 | 6,400 |
| 5 | 7,000 - 1,000 | 6,000 (maximum exhibits) |
| 7 | not allowed | exceeds the 5-exhibit cap; the formula never reaches 5,600 |

- [ ] Word count includes main body, footnotes, endnotes, and in-paper appendices.
- [ ] Word count excludes title, byline, abstract, acknowledgement footnote, references, the exhibits themselves, and the Supplemental Appendix.
- [ ] The count with the exhibit penalty applied is at or under budget. Over-length Insights submissions are returned without review, automatically.
- [ ] If it does not fit, reroute: it is an AER or AEJ paper, not an Insights paper. Brevity by design, not by truncation.

### Mechanical length-audit procedure

1. Build the review PDF exactly as it will be submitted (single self-contained file).
2. AER: check the compiled page count against the ~40-page guideline at the required font, spacing, and margins — do not shrink fonts or margins to pass.
3. Insights: run `texcount` (or an equivalent) on the main body including footnotes and in-paper appendices; subtract nothing by hand — instead confirm the excluded parts (references, exhibits, Supplemental Appendix) are outside the counted region.
4. Record the counts: [ABSTRACT-WORD-COUNT], [MAIN-TEXT-COUNT-OR-PAGES], [N-EXHIBITS], [WORD-BUDGET]. Keep the numbers for the resubmission audit.

## 3. First-three-pages desk-screen test

Simulate the editor's first ten minutes. All five must be Yes:

- [ ] The contribution is stated in **one sentence** with no "and we also".
- [ ] An economist **outside the subfield** would plausibly cite this paper.
- [ ] The venue routing (AER vs. AER: Insights vs. AEJ) is right for this paper's scope and length.
- [ ] The abstract leads with the finding — no throat-clearing sentences of motivation first.
- [ ] The identifying variation is named on the **first page** of text, not deferred to a footnote or Section 3.

Any No here is a likely desk rejection that no formatting polish can rescue. Fix the framing before auditing the format.

## 4. Disclosure statements

- [ ] One **separate Disclosure Statement PDF per coauthor** is prepared — required even when there is nothing to disclose; in that case the PDF says so explicitly.
- [ ] Each statement covers funding sources, paid or significant unpaid positions, and any party with a stake in the results, per current AEA disclosure policy.
- [ ] Coeditor conflicts of interest (recent coauthor, advisor or advisee, family member) are listed by name in the submission form.
- [ ] **AI usage disclosure** is completed if AI software was used in drafting or editing the manuscript — a brief description of what was used and for what.
- [ ] IRB or ethics approval is cited where the study design requires it.

## 5. Cover letter — optional, at most 200 words

A cover letter is **not required**. Include one only to communicate:

- a conflict of interest with a coeditor (identify by name);
- data-access constraints the editor must know in advance (e.g., restricted data with a specific verification arrangement);
- relevant prior submission history within the AEA family.

Never use it to pitch the contribution, list seminar presentations, or argue against potential referees. Submit via the form field, not as an uploaded document, and keep it at or under 200 words.

**Template:**

> Dear Editors: We submit "[PAPER-TITLE]" for consideration at [VENUE-NAME]. We note one item for the editorial office: [COI-OR-DATA-ACCESS-NOTE — e.g., Coeditor [COEDITOR-NAME] was a coauthor of [AUTHOR-NAME] within the past five years; or, the [DATASET-NAME] microdata are held under a data use agreement with [PROVIDER-NAME], and a verification copy can be provided to the Data Editor under [ARRANGEMENT]]. All other submission materials are complete. Sincerely, [CORRESPONDING-AUTHOR-NAME], on behalf of the authors.

## 6. Formatting pre-check

- [ ] **No separate title page** — title, authors, and affiliations sit at the top of page 1, followed by the abstract.
- [ ] Title-page footnote carries acknowledgements, funding, and author contact; it is not numbered as footnote 1.
- [ ] **JEL codes** chosen (primary and secondary) and matching the paper's actual content.
- [ ] **Keywords** listed after the abstract.
- [ ] Introductory paragraphs start immediately after the front matter with **no "Introduction" heading**.
- [ ] Sections numbered in Roman numerals (I., II., III.), subsections in capital letters (A., B.), introduction unnumbered — the AEA sample article class applies this automatically.
- [ ] Footnotes numbered consecutively in a single series; substantive material in the text, not smuggled into footnotes.
- [ ] Tables use booktabs-style rules; captions positioned correctly; magnitudes shown, not just stars.
- [ ] Figures are vector (PDF/EPS); every figure note states method, CI type, sample, and N.
- [ ] References complete; every in-text citation matches a bibliography entry and vice versa.
- [ ] No tracked changes, reviewer comments, or draft watermarks anywhere in the PDF.

## 7. Submission portal checklist (in the order the portal asks)

Work through ScholarOne (mc.manuscriptcentral.com/aer) with these ready, in order:

1. [ ] **Title, abstract, keywords** — pasted into form fields; abstract identical to the manuscript's.
2. [ ] **Author list** — all coauthors with affiliations and current emails; corresponding author's email and ORCID up to date.
3. [ ] **JEL classification codes** — primary and secondary selected from the picker.
4. [ ] **Manuscript PDF** — one self-contained file: text, references, tables, figures, in-paper appendix.
5. [ ] **Supplemental Appendix PDF** — separate file, only if applicable.
6. [ ] **Disclosure Statement PDFs** — one per coauthor, uploaded individually.
7. [ ] **Cover letter** — form field, only if needed, ≤ 200 words (Section 5).
8. [ ] **Coeditor conflict declarations** — names entered where asked.
9. [ ] **Suggested editor** — optional form field.
10. [ ] **AI usage disclosure** — completed if applicable.
11. [ ] **Submission fee** — current fee schedule verified on the AEA submissions page (fees vary by membership status and country income group).
12. [ ] **Final proof view** — open the system-built proof and re-check page 1 (no "Introduction" heading, abstract intact) before clicking submit.

Related but out of portal scope: the replication deposit is not required at submission, but plan it now — the Data Editor check is part of the publication timeline. If the paper reports a field experiment, the AEA RCT Registry entry must exist and be referenced in the paper.

## 8. After submission — expectations

- Median time to first decision at AER is roughly 8-12 weeks; Insights is typically faster.
- Desk rejections usually arrive within 2-4 weeks.
- Track status via ScholarOne; do not email the editorial office before 12 weeks.
- A "reject and resubmit" is rare and signals interest, but requires substantial restructuring — treat it as a new submission and rerun this entire checklist.
- On any R&R resubmission, the format rules apply again in full: recount the abstract, redo the length audit (revisions grow), refresh disclosure statements if affiliations or funding changed, and update the AI usage disclosure if tools were used during revision.

## Go / No-Go

- Any failure in Sections 1-3: do not submit; fix content or reroute the venue first.
- Any failure in Sections 4-7: fixable within hours; clear every box, then submit.
- All boxes checked: submit, and archive this checklist — it becomes the spine of the compliance section in any resubmission.

## Canonical repo sources

Distilled from these repository surfaces, which require the repository checkout:

- `skills/aer-submission/SKILL.md`
- `docs/desk-rejection-audit.md`
- `docs/source-register.md`
