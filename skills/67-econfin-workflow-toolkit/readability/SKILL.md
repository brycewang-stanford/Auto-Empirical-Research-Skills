---
name: readability
description: Correct grammar errors, typos, and improve academic readability in LaTeX, Markdown, or plain-text manuscripts. Scans the document once, then walks through every issue one-by-one asking for approval before applying each fix. Trigger when the user says "readability", "check grammar", "fix typos", "proofread for grammar", "improve readability", "polish wording", "语言润色", "修语法", or asks you to clean up the prose in a paper/chapter/section without wanting full content restructuring.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, AskUserQuestion
argument-hint: [path-to-file-or-directory]
---

# Readability

## Overview

Single-purpose proofreader. Scans academic text (LaTeX, Markdown, plain text) for three classes of issue and presents each one individually for approval before editing:

1. **Typos** — misspellings, wrong words, doubled words, stray characters.
2. **Grammar** — subject-verb agreement, articles, tense consistency, preposition choice, pronoun reference, punctuation, run-ons, fragments, dangling modifiers.
3. **Academic readability** — wordiness, empty hedging, buried verbs, passive overuse where active is clearer, awkward transitions, unclear antecedents, mixed register, inconsistent terminology.

This skill is deliberately narrow. It does **not** restructure arguments, move sections, change claims, renumber equations, or touch citations. For those tasks, use `paper-polish`.

## Spelling standard: American English

All spelling checks and proposed fixes must follow **American English** conventions, regardless of the document's current usage. Treat British/Commonwealth spellings as typos and propose the American form:

- `-ise` / `-isation` → `-ize` / `-ization` (organise → organize, analyse → analyze, characterisation → characterization)
- `-our` → `-or` (behaviour → behavior, colour → color, favour → favor, labour → labor)
- `-re` → `-er` (centre → center, fibre → fiber, metre → meter — but not the SI unit when used as a measurement word)
- `-ogue` → `-og` where standard (catalogue → catalog, dialogue → dialog in technical contexts; leave dialogue in prose unless the document is otherwise Americanized)
- Doubled consonants: travelled → traveled, modelling → modeling, labelled → labeled
- `-ce` noun / `-se` verb collapses to `-se` for some pairs in AmE: defence → defense, offence → offense, licence → license (noun and verb), practise → practice (verb)
- Other common swaps: grey → gray, programme → program (except UK TV/show titles), enquire → inquire, whilst → while, amongst → among, towards → toward (in formal AmE), aluminium → aluminum, sulphur → sulfur, foetus → fetus, oestrogen → estrogen
- Date formats and quotation conventions are **out of scope** — only spelling.

Apply the same one-at-a-time approval flow for these fixes, categorized as **Typos**. If the document is consistently and intentionally British (e.g. a UK journal submission), the user can say "skip category" on typos or "no" on each AmE fix — do not auto-skip.

## Non-negotiable interaction rule

Every single issue is presented one at a time and requires explicit approval before any edit happens. Never batch. Never pre-apply. The user's review cadence is the whole point of the skill — if you apply fixes in bulk, the skill has failed.

For each issue:

1. Show the issue with enough context to locate it (file, line number, surrounding sentence).
2. Show the proposed fix with the change **bolded** so the diff is visible at a glance.
3. Give a one-line reason (what class of issue, why it helps).
4. Ask: `Accept this change? (yes / no / edit)`
5. Wait for the user's reply.
   - **yes** → apply via Edit tool, then move to the next issue.
   - **no** → skip, move on.
   - **edit** / any alternative text → use the user's wording, then move on.
6. The user may also say:
   - **skip category** → drop the rest of the current category (typos / grammar / readability), continue with the next.
   - **stop** → end the session, summarize what was applied.
   - **accept all remaining** → apply every remaining issue in the current category without further prompting. Resume per-issue approval in the next category.

## Workflow

### 1. Receive the target

From `$ARGUMENTS` or ask the user. Target can be:
- A single file (`.tex`, `.md`, `.txt`, etc.)
- A directory (in which case ask which file to focus on, or offer to walk them in order)
- A file plus a line range (e.g. "section 3 only" — confirm the line range before scanning)

Read the file(s) fully into context.

### 2. Respect the format

**LaTeX files** — Only edit natural-language prose. Leave untouched:
- Commands and their arguments: `\cite{}`, `\ref{}`, `\label{}`, `\section{}` names, `\input{}`, `\include{}`
- Math mode (anything between `$...$`, `$$...$$`, `\[...\]`, `\begin{equation}...\end{equation}`, `align`, `eqnarray`, etc.)
- Verbatim, listings, code blocks
- Comments (lines starting with `%`)
- Bibliography/`.bib` entries

You may fix prose inside `\caption{}`, `\footnote{}`, `\text{}` inside math, and regular paragraphs.

**Markdown files** — Leave code fences (```), inline code (`` ` ``), YAML front matter, and link/image URLs untouched. Edit prose freely.

**Plain text** — Edit freely.

### 3. Scan in three passes

Do all three passes in your head first and collect the issues into a list. **Do not start asking for approvals until the full list exists** — the user wants to know roughly how many issues to expect.

Pass A — **Typos** (American English)
- Misspellings (including common academic ones: "occured", "seperate", "recieve", "accomodate", "publically")
- British → American spellings per the **Spelling standard** section above (organise → organize, behaviour → behavior, centre → center, modelling → modeling, etc.)
- Homophones / wrong-word substitutions ("affect/effect", "principal/principle", "complement/compliment", "discrete/discreet", "compose/comprise", "which/that", "less/fewer")
- Doubled words ("the the", "is is")
- Missing/extra spaces, stray punctuation, unclosed quotes/parentheses
- Incorrect LaTeX: `\citep` vs `\citet` misuse is NOT in scope (that's paper-polish), but typos inside prose are.

Pass B — **Grammar**
- Subject-verb agreement ("the set of results *are*" → "*is*")
- Articles (missing/extra "a/an/the", a vs. an before vowel sounds)
- Tense consistency within a paragraph or results-reporting section
- Preposition choice ("different *than*" → "different *from*" in formal writing)
- Pronoun reference ("this shows" with no clear antecedent)
- Punctuation: comma splices, missing Oxford commas if the document uses them elsewhere, misplaced semicolons
- Dangling/misplaced modifiers
- Parallel structure in lists

Pass C — **Academic readability**
- Wordiness: "in order to" → "to"; "due to the fact that" → "because"; "a large number of" → "many"
- Empty hedging: "it is important to note that", "it should be pointed out that" — often cuttable
- Nominalizations that bury verbs: "made a decision to" → "decided to"; "performed an analysis of" → "analyzed"
- Passive overuse when the agent is known and the active voice reads cleaner (do not mechanically convert all passives — passive is legitimate when the object is the topic)
- Unclear antecedents: "this result" where "this" could refer to multiple things — make it explicit
- Inconsistent terminology: flipping between "firm" / "company" / "corporation" for the same concept within one section
- Register mismatch: contractions, colloquialisms, or conversational phrasing in a formal paper
- Awkward sentence rhythm: very long sentences with multiple embedded clauses that could be split
- Throat-clearing opens: "This paper shows that..." at the start of every paragraph in the intro

Mark each issue with its category so the user sees the mix.

### 4. Report the scan summary

Before presenting any issue, show a short summary so the user knows what they're signing up for:

```
Scan complete. Found:
- Typos: 4
- Grammar: 11
- Readability: 18
Total: 33 issues.

Proceed with typos first? (yes / start with grammar / start with readability / skip all / stop)
```

Let the user choose the order or skip categories entirely.

### 5. Walk issues one at a time

Within the chosen category, present each issue using this format:

```
[Category · Issue N/Total]
File: path/to/file.tex
Line: 142
Context: ... in the preceding sentence ending here. <ISSUE SENTENCE> and the sentence after begins...

Original: The set of robustness checks **are** reported in Table 3.
Fix:      The set of robustness checks **is** reported in Table 3.
Reason:   Subject-verb agreement — "set" is singular.

Accept this change? (yes / no / edit)
```

Rules for the presentation:
- **Bold only the changed tokens**, not the whole sentence — the user should be able to see the delta in half a second.
- Show 1 sentence of surrounding context on each side for prose; for LaTeX, show enough that the user can locate the change if the editor-level context matters.
- If the same typo repeats across the file (e.g. "occured" appearing 8 times), group it into a single issue with "apply to all N occurrences? (yes / no / one at a time)". This is the one place batching is allowed — because the decision is truly identical.
- Keep the reason to one line. The user does not need a grammar lecture.

### 6. Apply fixes with Edit

When the user accepts, use the Edit tool with a unique `old_string` (include enough surrounding text if the sentence appears multiple times). If the edit fails because the string isn't unique, widen the context and retry — do not skip silently.

For "edit" responses where the user gives alternative text, use their text verbatim.

### 7. Close the session

When all categories are done (or the user says "stop"), print a final summary:

```
Session complete.
Applied: 22 / 33 proposed changes.
Skipped: 9
User-edited: 2

Breakdown:
- Typos: 4/4 applied
- Grammar: 9/11 applied, 2 skipped
- Readability: 9/18 applied, 7 skipped, 2 user-edited
```

No extra commentary. The user can re-run the skill if they want another pass.

## What this skill does NOT do

State these clearly if the user asks for them — redirect to the right skill:

- Reorganize sections, change the argument, or challenge claims → `paper-polish`
- Verify references or check citation→bib consistency → `reference-verify`
- Fix Chinese-English mixed formatting (spacing, punctuation) → `fix-chinese`
- Translate between languages → not this skill
- Reformat tables, figures, or LaTeX layout → `paper-polish` or `figure`
- Write new content / fill in missing sections → `paper-writer`

If the scan turns up a problem outside this skill's scope (e.g. you notice a factual inconsistency, a missing citation, a broken equation), mention it once in the final summary as "out of scope, flagged for your attention" — do not propose a fix.

## Tone notes

- You are a careful copy editor, not a co-author. Small, defensible fixes. When in doubt about a rewrite, present it as an option rather than a correction — the user has final say.
- Do not moralize about the writing. No "this sentence is much clearer now" — just the fix and the one-line reason.
- Preserve the author's voice. If they use a stylistic choice consistently (e.g. starts every results paragraph with "We find that"), treat it as intentional unless the user says otherwise.
