---
name: paper-polish
description: Proofread and verify academic papers in LaTeX. Runs 19 sequential checks covering titles, consistency, citations, formatting, theoretical tension in motivation, concise results reporting, cross-section repetition, em-dash usage, and auxiliary-text-to-footnote conversion. Trigger when user says "check paper" / "proofread" / "paper-checker" / "校对" / "核查论文".
allowed-tools: Read, Bash, Edit, Write, Glob, Grep, AskUserQuestion, WebSearch, WebFetch
argument-hint: [path-to-paper-directory]
---

# Paper Checker

## Overview

This skill performs a comprehensive 19-step proofreading and verification of academic papers in LaTeX. Each step is run sequentially. Within each step, every individual issue found is presented to the user one at a time for approval before applying the change.

**CRITICAL INTERACTION RULE**: For every issue found in every check, you MUST:
1. Present the issue clearly (original vs. proposed change, or finding).
2. Ask the user: "Accept this change? (yes/no/edit)"
3. Wait for the user's response before proceeding to the next issue.
4. If the user says "yes", apply the change using the Edit tool.
5. If the user says "no", skip and move to the next issue.
6. If the user says "edit" or provides alternative text, apply the user's version instead.
7. After all issues in a check are resolved, announce completion and move to the next check.

**All output must be in English** unless the user specifies otherwise.

## Initialization

1. **Receive the paper directory path** from user (via `$ARGUMENTS` or ask).
2. **Scan the directory** to identify:
   - Main LaTeX file (`main.tex`)
   - Bibliography file (`ref.bib` or `*.bib`)
   - Results directory with table/figure .tex files
   - Any PDF with original tables/figures
3. **Read all files** into context (main.tex in chunks if large, all table .tex files, ref.bib, PDF pages).
4. **Present inventory** and confirm with user before proceeding.

---

## The 19 Checks

Run these checks in order. For each check, present ALL findings, then ask the user to approve/reject each one individually.

---

### Check 1: Section and Subsection Titles

Optimize all `\section{}` and `\subsection{}` titles to reflect full academic rigor. Modified titles must NOT use colons.

**Output format** (present one row at a time for approval):

```
## Check 1: Section & Subsection Titles

Issue 1/N:
| Original Title | Proposed Title |
|----------------|----------------|
| Robustness Checks | Sensitivity and Robustness Analyses |

Accept this change? (yes/no/edit)
```

---

### Check 2: Table and Figure Titles

Optimize all `\caption{}` in table/figure .tex files to reflect full academic rigor. Modified titles must NOT use colons.

**Output format** (one at a time):

```
## Check 2: Table & Figure Titles

Issue 1/N:
| Original Title | Proposed Title |
|----------------|----------------|
| Summary Statistics | Descriptive Statistics of Key Variables |

Accept this change? (yes/no/edit)
```

---

### Check 3: Internal Consistency of Arguments

Check the entire paper for contradictory or inconsistent claims across sections.

**Output format** (one issue at a time):

```
## Check 3: Internal Consistency

Issue 1/N:
Location: [Section X, paragraph Y] vs. [Section Z, paragraph W]
Problem: [description of inconsistency]

| Original Text | Proposed Revision |
|---------------|-------------------|
| "...excerpt..." | "...**revised** excerpt..." |

Accept this change? (yes/no/edit)
```

---

### Check 4: Introduction Logic and Flow

Check whether the introduction's logic is tight and flows smoothly from motivation to findings to contributions.

**Output format** (one issue at a time):

```
## Check 4: Introduction Logic

Issue 1/N:
Location: [paragraph N of Introduction]
Problem: [e.g., abrupt transition, missing logical link, redundancy]

| Original Paragraph | Proposed Revision |
|---------------------|-------------------|
| "...excerpt..." | "...**revised** excerpt..." |

Accept this change? (yes/no/edit)
```

---

### Check 5: Storyline Coherence

Evaluate whether the full paper's storyline is tight and coherent. If any table is not essential to the main story, suggest moving it to the appendix.

**Output**:
- Assessment of overall storyline flow
- For each potentially non-essential table:

```
Table X: [name]
Recommendation: Move to appendix / Keep in main body
Rationale: [explanation]

Accept this recommendation? (yes/no)
```

---

### Check 6: Theoretical Tension in Introduction Motivation

Evaluate whether the motivation paragraphs of the introduction establish sufficient **theoretical tension** — i.e., competing economic forces or theoretical perspectives that make the central research question genuinely interesting *ex ante*. A motivation that points in only one direction reads as "the answer is obvious, so why run this regression?" and weakens the paper's contribution.

**What to look for**:

- The central $X \to Y$ relationship the paper examines is identified, but only one mechanism / one direction is articulated (e.g., the intro only argues "$X$ raises $Y$" with no countervailing reason $X$ could lower $Y$ or leave $Y$ unchanged).
- Prior literature is described as a one-directional consensus instead of as a genuine debate or open question.
- The motivation paragraphs read like a *summary of the eventual finding* ("we show that $X$ raises $Y$, which is consistent with [single theory]") rather than as a setup of a puzzle.
- No mention of plausible alternative predictions, opposing theoretical traditions, or institutional features that could push the effect the other way.
- The contribution is framed as "we confirm [obvious prior]" rather than "we resolve a tension between [view A] and [view B]".
- Hypotheses development (if previewed in intro) immediately commits to a signed prediction without acknowledging that the opposite is also plausible under a different framework.

**How to revise — apply these rules**:

1. **Identify the focal $X \to Y$ relationship** and the paper's actual finding (do NOT change the finding).
2. **Articulate at least two competing predictions** that are each individually plausible *before* the data is examined. Typical sources of tension:
   - Opposing theoretical traditions (e.g., agency theory vs. stakeholder theory; risk-shifting vs. risk-management; information asymmetry vs. monitoring).
   - Direct vs. indirect / countervailing channels (e.g., $X$ raises $Y$ through channel A but lowers $Y$ through channel B).
   - Conflicting prior empirical findings in the literature.
   - Institutional or contextual features that could flip the sign (e.g., regulation, ownership structure, market frictions).
3. **Reframe the motivation as a puzzle**, with a structure such as:
   > "On the one hand, [theory / mechanism A] predicts that $X$ should increase $Y$, because [reason]. On the other hand, [theory / mechanism B] predicts that $X$ should decrease $Y$ (or leave it unchanged), because [reason]. Which force dominates is ultimately an empirical question."
4. **Cite competing prior work** to anchor each side of the tension. If one side has no direct prior, cite the theoretical paper or a related literature that motivates that prediction.
5. **Position the contribution as resolving the tension**, not as confirming an expected result. Phrasing like "we provide evidence that helps adjudicate between …" or "our findings reconcile …" is stronger than "we document that …".
6. **Do not introduce strawman alternatives.** The competing prediction must be one a reasonable referee in the field would actually find plausible.
7. **Do not contradict the paper's actual findings.** Tension is about the *ex ante* prediction, not the *ex post* result.
8. **Do not invent mechanisms not supported by economics / finance / accounting literature.** If unsure, search for relevant theoretical or empirical citations before proposing the alternative force.

**Severity assessment** — flag the motivation as deficient in theoretical tension if **any** of the following hold:

- Only one signed prediction is articulated in the motivation paragraphs.
- No prior work is cited as offering a competing view.
- The motivation paragraph and the hypothesis statement give the same one-directional argument with no opposing consideration.
- The wording reveals the empirical sign before the puzzle is established (e.g., "We argue and find that $X$ raises $Y$" stated up front, with no setup of why the opposite was plausible).

**Output format** (one issue at a time):

```
## Check 6: Theoretical Tension in Introduction Motivation

Issue 1/N:
Location: Introduction, paragraph(s) [N]
Focal relationship: $X \to Y$ ([brief description of X and Y])
Problem: [e.g., "Only one mechanism is articulated; no countervailing force is acknowledged; prior literature framed as one-directional consensus."]
Proposed competing prediction: [one-sentence summary of the alternative force / theory and its source]

| Original Motivation Excerpt | Proposed Revision |
|------------------------------|-------------------|
| "...[single-directional motivation passage]..." | "**On the one hand, [mechanism A] suggests that $X$ raises $Y$, because [reason A] (Author, Year). On the other hand, [mechanism B] suggests that $X$ may instead lower $Y$, because [reason B] (Author, Year). Which force dominates is an empirical question.**" |

Accept this change? (yes/no/edit)
```

If the motivation already exhibits adequate theoretical tension (at least one explicitly stated, plausibly opposing prediction with a citation), report:

```
## Check 6: Theoretical Tension in Introduction Motivation

Assessment: The introduction's motivation establishes adequate theoretical tension between [mechanism A] and [mechanism B], with prior literature cited on both sides. No revision proposed.
```

---

### Check 7: Section Ordering

Check whether the ordering of sections and subsections is logical and follows academic conventions for the target field.

**Output**: Assessment of current ordering with specific reordering suggestions if needed. Present each suggestion for approval.

---

### Check 8: Table/Figure References in Text

Verify that every table and figure included in the paper is mentioned/referenced in the main text.

**Output format**:

```
## Check 8: Unreferenced Tables/Figures

| # | Table/Figure | File | Referenced in Text? |
|---|-------------|------|---------------------|
| 1 | Table X | results/xxx.tex | NOT referenced |

[If all referenced]: All tables and figures are referenced in the text.
```

For unreferenced items, suggest where to add a reference. Ask user for approval.

---

### Check 9: Variable Definition Table Completeness

Check whether the variable definition table (if present) includes all key variables discussed in the text.

**Output format**:

```
## Check 9: Missing Variables in Definition Table

| # | Variable | Mentioned in Section | Missing from Definition Table |
|---|----------|---------------------|-------------------------------|
| 1 | FiscalTransparency | Section 6.3 | Yes |

Suggest adding these variables? (yes/no)
```

---

### Check 10: Abbreviation and Nomenclature Consistency

Check that all abbreviations/acronyms are defined on first use and used consistently throughout.

**Output format** (one issue at a time):

```
## Check 10: Abbreviation Issues

Issue 1/N:
| Abbreviation | Issue | Location | Suggested Fix |
|-------------|-------|----------|---------------|
| PSM | Used without definition | Section 6.2 | Define as "propensity score matching (PSM)" on first use |

Accept this fix? (yes/no/edit)
```

---

### Check 11: Content and Logic Completeness

Check whether the paper's arguments, reasoning, and evidence are complete. Flag any gaps where claims lack support or transitions are missing.

**Output format** (one issue at a time):

```
## Check 11: Content/Logic Gaps

Issue 1/N:
Location: [Section, paragraph]
Gap: [description]

| Original Text | Proposed Addition/Revision |
|---------------|---------------------------|
| "...excerpt..." | "...**added/revised** text..." |

Accept this change? (yes/no/edit)
```

---

### Check 12: Text-Table/Figure Data Consistency

**This is the most critical check.** Verify that EVERY specific data point in the prose matches the corresponding table/figure.

Cross-check ALL of the following:
- Coefficient values and signs
- t-statistics / standard errors
- Significance levels (stars)
- R-squared / Pseudo R-squared
- Observation counts
- Column references
- Qualitative claims ("positive and significant" — verify)
- Economic magnitude calculations
- Subsample labels
- Fixed effects specifications
- p-values for group differences

**Output format** (one issue at a time):

```
## Check 12: Text-Table Consistency

Issue 1/N:
Section: [section name], referencing Table X

| Original Text | Corrected Text |
|---------------|----------------|
| "the coefficient on AIHype is $0.3880$ ($t = 12.49$)" | "the coefficient on AIHype is **$0.3951$** ($t = **12.82**$)" |

Table value: Column (2), AIHype = 0.3951 (12.82)

Accept this correction? (yes/no/edit)
```

---

### Check 13: Citations → Reference List

Extract all `\cite{}`, `\citep{}`, `\citet{}` keys from text. Verify each exists in `ref.bib`.

**Output format**:

```
## Check 13: Citations Missing from ref.bib

| # | Citation Key | Location |
|---|-------------|----------|
| 1 | smith2020 | Section 3, line 154 |

[If none]: All citations have corresponding ref.bib entries.
```

For each missing entry, offer to add it. Ask user for approval.

---

### Check 14: Reference List → Citations

Check each `ref.bib` entry against the text. List any uncited references.

**Output format**:

```
## Check 14: Uncited References in ref.bib

| # | Citation Key | Reference |
|---|-------------|-----------|
| 1 | smith2020 | Smith, J. (2020). Title. Journal. |

Remove this entry from ref.bib? (yes/no)
```

---

### Check 15: Reference Format

Check each BibTeX entry for formatting correctness. Ignore italics requirements.

Verify:
- Required fields present (author, title, journal/booktitle, year, volume)
- Author name format consistency
- Valid year
- Title capitalization protection for proper nouns
- Full journal names (not abbreviated)
- DOI presence
- No duplicate entries
- No encoding issues

**Output format** (one issue at a time):

```
## Check 15: Reference Format Issues

Issue 1/N:
| Citation Key | Issue | Current | Suggested Fix |
|-------------|-------|---------|---------------|
| chen2011 | Missing pages | — | pages={259--271} |

Accept this fix? (yes/no/edit)
```

---

### Check 16: Concise Results Reporting

Scan all empirical results sections for **wordy, mechanical restatement** of numbers that are already visible in the cited table. The prose should interpret the result, not transcribe the table cell.

**What to look for**:
- Sentences that report **both** the coefficient value **and** the t-statistic when one of them suffices (e.g., "the coefficient on $X$ is 0.035 with a $t$-statistic of 2.41, which is significant at the 5\% level" — three pieces of information for what is essentially one finding).
- Paragraphs where every sentence follows the rigid template "the coefficient on [var] is [value] ($t = [stat]$)" — monotonous and reads like a table dump.
- Restating standard errors, R-squared, or N in prose when these belong in the table.
- Repeating the same column reference and the same fixed-effects qualifier across consecutive sentences.

**How to revise** — apply these rules:

1. **Drop redundant numbers.** For each result, keep the coefficient OR the t-stat — not both — unless the magnitude is itself the substantive point. Pair the kept number with a brief qualitative descriptor.
2. **Mix two concise forms** within a paragraph (do NOT use p-values, confidence intervals, or star notation):
   - Coefficient + significance level: "$X$ raises $Y$ by 0.035, significant at the 5\% level"
   - Sign/direction + t-statistic: "$X$ enters positively ($t = 2.41$)"
3. **Lead with the economic claim, not the number.** Prefer "$X$ is positively associated with $Y$ (column 2)" over "in column 2, the coefficient on $X$ is 0.035 ($t = 2.41$)".
4. **Collapse parallel results.** When two columns yield the same conclusion, summarize jointly rather than restating column-by-column.
5. **Preserve numerical accuracy.** If a number is kept, it must match the table; if a "significant at X\% level" descriptor is used, it must be consistent with the underlying $t$-value.
6. Focus on paragraphs with **3 or more consecutive** sentences using the wordy "coefficient = X ($t = Y$)" template, OR any paragraph where more than 50\% of the words are number-restatement rather than interpretation.

**Output format** (one issue at a time):

```
## Check 16: Concise Results Reporting

Issue 1/N:
Location: [Section X, paragraph Y]
Problem: [e.g., "4 consecutive sentences each restate coefficient + t-stat already shown in Table 3"]

| Original Paragraph | Proposed Revision |
|---------------------|-------------------|
| "In column 1, the coefficient on $X$ is 0.035 ($t = 2.41$). In column 2, the coefficient on $X$ is 0.041 ($t = 2.78$). In column 3, the coefficient on $X$ is 0.038 ($t = 2.55$)..." | "**$X$ is positively associated with $Y$ across columns 1–3, with effects ranging from 0.035 to 0.041 and significant at the 5\% level or better.**" |

Accept this change? (yes/no/edit)
```

---

### Check 17: Cross-Section Repetition (Introduction / Literature Review / Hypotheses)

Detect content that is **repeated across the introduction, literature review, and hypotheses development sections**. These three sections typically restate the same motivation, the same prior findings, and the same theoretical mechanism, which inflates page count without adding information.

**What to look for**:
- The same prior study cited to make the **same point** in two or more of: intro, literature review, hypotheses.
- The same motivating fact (stylized fact, policy event, statistic) restated in near-identical wording across sections.
- The same theoretical mechanism described twice — once narratively in the intro and again in the hypotheses development.
- The same gap-in-the-literature framing repeated in the intro and in the literature review.
- The hypotheses development reproducing literature review paragraphs almost verbatim before stating H1/H2.

**How to revise**:
- The **introduction** should briefly motivate, summarize the contribution, and preview findings. It should **not** rehearse the literature in detail.
- The **literature review** should organize prior work and identify the gap. It should **not** re-motivate the paper.
- The **hypotheses development** should derive testable predictions from a tight theoretical argument. It should **cite** the relevant prior work but not re-summarize it.
- For each repetition, propose: (a) which section keeps the content in full, (b) which section shortens it to a one-clause cross-reference, and (c) the revised wording for the shortened version.

**Rules**:
- Do NOT delete content the paper genuinely needs — only collapse duplication.
- When the same citation appears in all three sections for the same point, keep the most substantive treatment and reduce the others to a parenthetical citation.
- Aim to cut total length across the three sections, not to redistribute words evenly.
- Present each repetition individually for approval.

**Output format** (one issue at a time):

```
## Check 17: Cross-Section Repetition

Issue 1/N:
Repeated content: [one-line description, e.g., "Mechanism by which X affects Y via channel Z"]
Locations: Introduction (paragraph 3) + Hypotheses Development (paragraph 1)
Recommendation: Keep full treatment in Hypotheses Development; shorten Introduction to a one-sentence preview.

| Original Introduction Excerpt | Proposed Revision |
|-------------------------------|-------------------|
| "...[long passage describing the mechanism in detail, citing Smith (2018) and Jones (2020)]..." | "**We argue that $X$ affects $Y$ through channel $Z$ (developed formally in Section 3).**" |

Accept this change? (yes/no/edit)
```

---

### Check 18: Em-Dash (`---`) Usage

Scan the entire `main.tex` (and any included section .tex files) for the LaTeX em-dash symbol `---`. Em-dashes are a common AI-writing tell and tend to clutter academic prose; replace each occurrence with a more precise punctuation choice that preserves the sentence's logic.

**What to look for**:
- Any literal `---` in body text (not inside comments, table column specifiers, or code/listings).
- Pairs of em-dashes used as parenthetical inserts: `clause---inserted phrase---rest of clause`.
- Single em-dashes used as a colon, semicolon, or "namely" connector: `result---we conclude X`.
- Em-dashes inside math or page-range contexts are NOT in scope (e.g., `pages={259--271}` uses an en-dash `--`, not an em-dash; leave it untouched).

**How to revise** — choose the replacement based on the dash's grammatical role:

1. **Parenthetical aside** (`A---B---C`): replace with parentheses `A (B) C`, or with commas `A, B, C` if B is short and the sentence remains readable.
2. **Connector before an explanation or amplification** (`X---namely Y` / `X---Y`): replace with a colon `X: Y`, a semicolon `X; Y`, or split into two sentences.
3. **Dash signaling abrupt shift or emphasis** (`...the result was clear---no effect`): replace with a period and rewrite as two sentences, or with a comma if the clauses are tightly bound.
4. **List-continuation dash** (`A, B, C---all of which`): replace with a comma plus connecting word, e.g., `A, B, and C, all of which`.
5. Preserve any em-dash that is genuinely necessary for clarity only if no other punctuation captures the same meaning — but the default disposition is **replace, not preserve**.

**Output format** (one issue at a time):

```
## Check 18: Em-Dash Usage

Issue 1/N:
Location: [Section X, paragraph Y]
Role: [parenthetical / connector / abrupt shift / list-continuation]

| Original Text | Proposed Revision |
|---------------|-------------------|
| "the hub firm---unlike its peripheral suppliers---internalizes a larger share of rents" | "the hub firm (unlike its peripheral suppliers) internalizes a larger share of rents" |

Accept this change? (yes/no/edit)
```

---

### Check 19: Auxiliary Text → Footnote Conversion

Scan the **entire paper** for sentences and clauses that function as **auxiliary explanation** rather than as part of the main argumentative flow, and propose moving them into LaTeX `\footnote{}` commands. The goal is to keep the body text driving the argument while preserving secondary detail in footnotes.

**What counts as "auxiliary" — flag candidates of any of these types**:

- **Definitional asides**: a parenthetical clarification of a term, acronym, or institutional concept that is not strictly necessary to follow the sentence (e.g., "The Inflation Reduction Act (IRA), signed into law by President Biden in August 2022, ...").
- **Data-source / sample-construction details**: notes about which database was queried, why a particular filter was applied, how missing values were handled, version numbers, vintage dates, or download dates that interrupt the substantive prose.
- **Technical implementation details**: small methodological choices (e.g., "we winsorize at the 1\% and 99\% levels", "we cluster standard errors at the firm level following Petersen (2009)", "we use the 2017 NAICS classification") that belong below the line rather than inside the main argument.
- **Tangential examples / illustrative anecdotes**: a concrete example offered to illustrate a general claim, when the general claim already stands on its own.
- **Caveats, qualifications, and disclaimers**: sentences beginning with "Note that ...", "It is worth noting that ...", "We acknowledge that ...", "Although ...", which qualify a claim without changing its substance.
- **Cross-references to ancillary results**: sentences mentioning that a robustness check, an alternative specification, or an appendix table delivers the same finding, when the cross-reference is not load-bearing for the current paragraph.
- **Historical / institutional background**: dates, statutes, agency names, or background that contextualizes but does not advance the argument.
- **Reconciliations with prior literature**: side comments comparing the present finding to one specific prior paper's coefficient or sample, when the comparison is informational rather than central.
- **Construction details for variables already defined in the variable definition table**: re-explaining a variable's construction inline when the table already does so.

**Do NOT flag for footnote conversion**:

- Claims that carry the paper's argument forward (hypotheses, main mechanism statements, headline results).
- Sentences that the next sentence directly builds on (their removal would break flow).
- Numbers cited from the paper's own tables that interpret the main finding (those belong in body text).
- Anything inside captions, table notes, equations, or already inside a footnote.
- Content the user has explicitly told you to keep in the body.

**Rules for the conversion**:

1. **Preserve every word** of the flagged sentence/clause unless the user requests trimming — wrapping in `\footnote{...}` does not delete content.
2. **Choose a clean anchor point** in the body text. Common patterns:
   - Replace the entire sentence with a `\footnote{}` attached to the end of the preceding sentence.
   - Replace a parenthetical clause `(... aside ...)` with a `\footnote{... aside ...}` attached to the word before the parenthesis.
   - For a sentence-final caveat starting with "Note that ..." or "Although ...", attach the footnote to the end of the previous claim.
3. **Adjust grammar** in the footnote so it reads as a standalone note (e.g., start with a capital letter, end with a period). If trimming is needed for readability, show the trim explicitly in the diff.
4. **Keep citations and references intact** when moving content — `\citep{}`, `\citet{}`, `\ref{}`, `\autoref{}` should travel with the text into the footnote.
5. **One footnote per logical aside.** Do NOT merge unrelated asides into one footnote.
6. **Be conservative.** When the auxiliary nature of a sentence is borderline, present it as a candidate but flag the borderline judgment in the "Rationale" field so the user can reject quickly.

**Where to look — sweep these sections systematically**:

- Introduction (often padded with institutional context).
- Institutional background / setting section.
- Data and sample (typically the densest source of footnote candidates).
- Variable definitions in the body (cross-check against the variable definition table).
- Empirical strategy (methodological details).
- Results sections (caveats and cross-references to robustness).
- Conclusion (often contains qualifications worth demoting).

**Output format** (one issue at a time):

```
## Check 19: Auxiliary Text → Footnote Conversion

Issue 1/N:
Location: [Section X, paragraph Y]
Type: [definitional aside / data detail / technical detail / example / caveat / cross-reference / institutional background / literature reconciliation / variable construction]
Rationale: [one-line explanation of why this is auxiliary; flag if borderline]

| Original (body text) | Proposed (footnote conversion) |
|----------------------|--------------------------------|
| "The Inflation Reduction Act (IRA), signed into law by President Biden in August 2022, allocates roughly \$370 billion to clean-energy tax credits over a decade. We exploit ..." | "The Inflation Reduction Act (IRA)\footnote{The IRA was signed into law by President Biden in August 2022 and allocates roughly \$370 billion to clean-energy tax credits over a decade.} allocates clean-energy tax credits that we exploit ..." |

Accept this change? (yes/no/edit)
```

If no auxiliary text warrants footnote demotion in a given section, state so briefly and move on. After all candidates across the paper have been resolved, announce completion of Check 19.

---

## Important Notes

- **Never batch approvals.** Each issue must be presented and approved individually.
- **Preserve exact formatting.** When showing original vs. corrected text, include enough context (full sentence or clause) for the user to locate the issue.
- **Bold the specific changes** within the proposed revision so the user can quickly see what changed.
- **Be exhaustive in Check 12.** Read every number in every empirical section and cross-check against the table. This is the highest-value check.
- If the user says "accept all remaining" during any check, apply all remaining changes in that check without further prompting, then resume individual approval for the next check.
- If the user says "skip" during any check, skip the entire remaining check and move to the next one.
