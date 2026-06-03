---
name: thematic-analysis
description: "Conduct rigorous thematic analysis (TA) of qualitative data following Braun and Clarke's (2006) six-phase framework. Use whenever the user mentions 'thematic analysis', 'TA', 'Braun and Clarke', 'qualitative coding', 'identifying themes', or asks for help analysing interviews, focus groups, open-ended survey responses, or transcripts to identify patterns. Also trigger for questions about inductive vs theoretical coding, semantic vs latent themes, essentialist vs constructionist epistemology, building a thematic map, or writing up a qualitative findings section. Covers all six phases, the four upfront analytic decisions, the 15-point quality checklist, and the five common pitfalls. Produces a Word document write-up and an annotated thematic map. Does NOT cover IPA, grounded theory, discourse analysis, conversation analysis, or narrative analysis — use a different method for those."
---

# Thematic Analysis — Braun & Clarke's Six-Phase Framework

This skill walks a user through conducting a rigorous thematic analysis (TA) on qualitative data, following the six-phase framework from Braun and Clarke (2006). It produces a **Word document (.docx)** write-up of the analysis and an **annotated thematic map** (PNG).

The skill is grounded in one source:

> Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Psychology, 3*(2), 77–101.

Where this skill cites the paper, treat those statements as the method's published position, not Claude's own.

## Before you begin

Read these reference files as needed:

- `references/upfront-decisions.md` — The four analytic decisions to settle **before** coding starts. Consult during Phase 1 (interview).
- `references/coding-guide.md` — How to generate codes well. Consult during Phase 3 (generating initial codes).
- `references/theme-development.md` — How to move from codes to themes, with worked examples. Consult during Phases 4–6.
- `references/thematic-map.md` — How to build and annotate the thematic map. Consult during Phase 6.
- `references/quality-checklist.md` — The 15-point checklist for assessing the analysis. Consult before producing the final write-up.
- `references/pitfalls.md` — The five common pitfalls. Consult after the first draft of the write-up.

Also read these skills before generating outputs:

- **docx skill** (`/mnt/skills/public/docx/SKILL.md`) — Required for the Word document.
- **apa-referencing skill** (`/mnt/skills/user/apa-referencing/SKILL.md`) — If the user wants citations to existing literature in the analysis, format them in APA 7th Edition.

If the user has a **writing-style skill**, do not apply it to the manuscript body — see "Writing register" under Phase 7. A writing-style skill may still apply to ancillary outputs (a plain-language summary, a blog version of the findings) if the user asks for those separately.

---

## Step 0: Establish the research question(s) or objective(s) first

Before any of the six phases begin, elicit the research question(s) or objective(s) explicitly. This is the **first action** of the skill and is non-negotiable. The research question disciplines what counts as interesting in the data, which codes earn their keep, and which patterns rise to the level of a theme. Coding without a clear question tends to drift into surface description.

Prompt the user along these lines:

> Before we begin the analysis, please state the research question(s) or objective(s) for this study. If there is more than one, list them in order of priority. If they are still in draft form, share the draft — we can sharpen them together before coding starts.

If the user is unsure or only has a study aim, help them work a draft into a workable analytic question. A good TA research question is broad enough to allow patterned meaning to surface across the data set, but narrow enough to discipline what is included and excluded.

Record the agreed research question(s) verbatim. They will be referenced explicitly in every subsequent phase:

- **Phase 3 (coding):** when generating codes, keep the research question in view. Ask of each segment, "does this speak to the research question, directly or obliquely?" Code inclusively, but the question anchors the work.
- **Phase 4 (searching for themes):** themes must capture something important *in relation to the research question*, not just frequent content.
- **Phase 5 (reviewing themes):** the second-level review checks the candidate map against the data set as a whole — also check it against the research question. A theme that is internally coherent but unrelated to the question is a candidate for the discard pile.
- **Phase 7 (report):** the introduction states the research question(s) verbatim, and the findings are organised to answer them.

If the analytic approach is **theoretical/deductive**, the research question is also tied to the theoretical framework being applied — make this link explicit at this stage, before any coding begins.

Save the agreed research question(s) to the workspace as `step0_research_questions.md`. Refer back to this file at the start of each subsequent phase.

---

## Phase 1 (skill workflow): Interview

Before any analysis, gather what is needed to plan the TA. Offer the user two paths up front.

### Path A: Upload existing materials

Ask the user whether they have any of the following:

- Interview, focus group or open-ended survey transcripts (the data corpus itself)
- A research question or research aim document
- A proposal or protocol that specifies the analytic approach
- An existing coding frame or codebook (for theoretical/deductive work)
- Field notes, memos, or reflexive journal entries

Read uploaded transcripts using the appropriate tool (file-reading skill for .txt/.md, docx skill for .docx, pdf-reading skill for PDFs, xlsx skill for spreadsheet-formatted survey data). Then summarise what is in the corpus and ask the user to confirm.

### Path B: Conversational interview

If the user has no materials, gather the essentials conversationally. Adapt to what they offer; do not interrogate.

### Essential information to collect

**About the project:**

- Working title of the study
- Research question(s) — already collected in Step 0; carry these forward, do not re-elicit
- The data corpus: what kind of data, how many items, who from
- The data set for this particular analysis (may be the whole corpus or a subset — see Braun & Clarke, p. 6)

**The four upfront analytic decisions** (see `references/upfront-decisions.md` for full guidance):

1. **Rich description of the whole data set, or detailed account of one aspect?**
2. **Inductive (bottom-up) or theoretical/deductive (top-down) coding?**
3. **Semantic themes (surface meaning) or latent themes (underlying ideas, assumptions, ideologies)?**
4. **Epistemology: essentialist/realist, contextualist, or constructionist?**

These decisions are inter-related. Tendencies cluster: realist + semantic + inductive + rich description; constructionist + latent + theoretical + detailed account. But other combinations are valid — what matters is that the choices are explicit and internally consistent.

Walk the user through each decision. Do not assume realist + semantic + inductive by default just because the paper notes this is the common (often unspoken) default. Ask.

### Confirm the plan

Before moving to Phase 2, produce a short plan summary and ask the user to confirm:

- Research question
- Data set (what items, how many)
- The four decisions (with one-sentence rationale for each)
- Whether engagement with prior literature happens before or after coding (inductive work usually delays it; theoretical work requires it upfront)

---

## Phase 2 (skill workflow): Familiarising yourself with the data

The first of Braun and Clarke's six phases. This phase is **immersion**.

Ask the user to confirm that transcription (if needed) has been done. The transcript must be at minimum a rigorous orthographic verbatim record — every word spoken, including non-verbal utterances where they carry meaning (laughter, sighs, "um", "you know"). TA does not require Jefferson-style detail.

In this phase:

- Read every data item at least once before coding starts.
- Read actively — search for meanings, oddities, contradictions, patterns.
- Take notes as you read. Jot down initial ideas, hunches, and possible codes. These are not yet codes; they are a starting list to feed Phase 3.

Output of this phase: a familiarisation note for the user — a paragraph per data item summarising what struck you, plus a running list of initial ideas across the data set. Save this to the workspace as `phase2_familiarisation.md`.

If the data set is too large for full re-reading in one pass, do it in batches and combine the notes.

---

## Phase 3 (skill workflow): Generating initial codes

Before coding starts, re-read the research question(s) saved in `step0_research_questions.md`. Coding is inclusive but not undisciplined — the question is the compass.

A **code** identifies a feature of the data — semantic content or latent meaning — that appears interesting to the analyst. A code is the **most basic segment** of raw data that can be assessed in a meaningful way (Braun & Clarke, 2006, p. 18, citing Boyatzis).

Codes are not themes. Codes are smaller, narrower, more numerous. Themes come later.

For full guidance on what good coding looks like (including data-driven vs theory-driven approaches, manual vs software coding, inclusive coding, and contradictions), read `references/coding-guide.md`.

In this phase:

- Work systematically through every data item. Give equal attention to each.
- Code for as many potential themes/patterns as possible — you do not yet know what will matter.
- Code extracts inclusively — keep a little surrounding context so meaning is not lost.
- A single extract can be coded under multiple codes, or none.
- Retain accounts that depart from the dominant story; do not smooth them out.

Output of this phase: a coded data table. For each data item, list the extracts and the code(s) applied to each. Save as `phase3_codes.md`. At the end, produce a consolidated **code list** with every code and the data extracts that sit under it.

A short worked example showing data → code, modelled on Braun and Clarke's Figure 1:

| Data extract | Codes applied |
|---|---|
| "it's too much like hard work I mean how much paper have you got to sign to change a flippin' name no I I mean no I no we we have thought about it half heartedly and thought no no I jus- I can't be bothered" | (1) Talked about with partner; (2) Too much hassle to change name |

---

## Phase 4 (skill workflow): Searching for themes

A **theme** captures something important about the data in relation to the research question, and represents some level of patterned response or meaning across the data set.

Prevalence matters but is not decisive. A theme can appear in many items briefly, or in a few items at length. Researcher judgement — guided by the research question — decides what is a theme.

In this phase:

- Sort codes into candidate themes. Some codes will become themes, some will be sub-themes, some will be discarded, some will sit in a temporary "miscellaneous" pile.
- Look for relationships between codes, between themes, and between levels of themes (overarching themes vs sub-themes).
- Produce an **initial thematic map** — a visual sketch (mind-map style) showing candidate themes and how codes feed into them. See `references/thematic-map.md`.

Output of this phase: a draft thematic map (saved as `phase4_initial_map.png` or as a markdown outline if a visual is not yet practical) and a candidate theme list with the codes under each.

End this phase with candidate themes, sub-themes, and all coded extracts grouped under them. Do not discard anything yet — Phase 5 will tell you whether the themes hold.

---

## Phase 5 (skill workflow): Reviewing themes

Refining the candidate themes. Some candidate themes will not survive. Some will collapse together. Some will split.

Use Patton's dual criterion (cited in Braun & Clarke, 2006, p. 20):

- **Internal homogeneity** — data within a theme cohere meaningfully.
- **External heterogeneity** — themes are clearly distinct from each other.

This phase has two levels of review.

**Level 1 — Review at the level of the coded extracts.** Read all the collated extracts under each candidate theme. Do they form a coherent pattern? If yes, move on. If no, decide whether the theme is broken or whether some extracts simply belong elsewhere. Rework as needed.

**Level 2 — Review against the entire data set.** Re-read the full data set. Two questions: (a) Does the candidate thematic map accurately reflect the meanings in the data set as a whole? (b) Has any new relevant data been missed in earlier coding? If so, code it now.

When refinements stop adding anything substantial, **stop**. Endless re-coding has diminishing returns — Braun and Clarke compare further fiddling to "rearranging the hundreds and thousands on an already nicely decorated cake" (p. 21).

Output of this phase: a refined thematic map (`phase5_refined_map.png`) and a refined theme list.

---

## Phase 6 (skill workflow): Defining and naming themes

Now define what each theme **is** and what it is **not**.

For each theme:

- Identify the essence — what aspect of the data this theme captures.
- Write a short definition (a couple of sentences). If you cannot describe the scope of a theme in two or three sentences, the theme needs more work.
- Identify any sub-themes (themes within a theme). Use these to give structure to large themes.
- Give the theme a **concise, punchy name** that immediately signals to the reader what the theme is about. Working titles from earlier phases are usually too descriptive — sharpen them now.
- Check the theme against the others: does it overlap too much? Does it add something distinctive to the overall story?

Output of this phase: the final theme list with definitions, sub-themes, and final names. Save as `phase6_definitions.md`.

Also produce the **final thematic map** (`phase6_final_map.png`) — this is the version that will appear in the write-up.

---

## Phase 7 (skill workflow): Producing the report

The final write-up. This is the last phase of Braun and Clarke's framework and the deliverable of the skill.

### Run the quality checklist first

Before drafting the report, run through the 15-point checklist in `references/quality-checklist.md`. Flag any items the analysis does not yet meet and fix them.

Then read `references/pitfalls.md` and audit the draft against the five common pitfalls. The most frequent failures: (1) describing extracts instead of analysing them, and (2) using interview questions as themes.

### Writing register: strictly academic

The write-up must use a formal academic register suitable for peer-reviewed publication. This is the deliverable standard for the manuscript body and it **overrides any personal writing-style skill the user has loaded**. Those preferences apply to blogs, op-eds and informal pieces — not to the findings of a thematic analysis.

Concretely, the manuscript body follows these conventions:

- Third person throughout. No "I think", "I feel", "in my view". The reflexivity statement (if the user wants one) is the only place where first person is admissible, and it is used sparingly.
- Hedged, evidenced claims: "Participants tended to...", "The data suggest...", "This pattern is consistent with...", rather than "Participants clearly...", "Obviously...".
- No colloquialisms, no figurative analogies, no rhetorical questions to the reader, no exclamations.
- Active voice when describing what the analyst did ("I identified...", "The analysis generated...", "This study constructed..."). Do not use the passive voice as a vehicle for evasion ("themes emerged" is forbidden — see Important Reminders).
- Tense conventions: methods in past tense; results in present tense (or past when describing what participants said); discussion blends both as appropriate.
- Citations integrated grammatically, not appended as parenthetical afterthoughts. APA 7th Edition throughout — use the apa-referencing skill for any reference list entries and in-text citations.
- Sentences disciplined: one main idea per sentence where possible. Paragraphs follow a claim → evidence (extract plus analytic commentary) → link-back structure, where the link-back ties the point to the research question or the broader theme.
- No metadiscourse padding. Avoid "It is interesting to note that...", "It should be mentioned that...", "It is worth pointing out...". State the point directly.
- Analytic commentary on extracts must go beyond paraphrase. Address what the extract means, what it assumes, what it implies, and why participants might frame the matter in this way rather than another (see Braun & Clarke, 2006, p. 24).

If the user has a writing-style skill loaded, apply it only to ancillary outputs they request separately — for instance, a plain-language summary or a blog adaptation of the findings — not to the manuscript itself.

### Generate the Word document

Use the docx skill to produce a manuscript-style .docx with this structure:

```
Title
Author / affiliation (if provided)

1. Introduction
   - Research question(s) and rationale
   - Brief note on the analytic approach and the four decisions
     (e.g. "An inductive, semantic, realist thematic analysis was conducted,
      aiming for a rich description across the full data set.")

2. Method
   - Data corpus and data set
   - Participants / sources (anonymised)
   - Data collection (brief, if relevant)
   - Analytic procedure — describe the six phases in your own words,
     citing Braun and Clarke (2006). Make the "how" explicit, not implicit.
   - Researcher positionality / reflexivity (if the user wants this)

3. Findings
   - Overview paragraph that names the themes and sketches the overall story
   - One section per theme. For each theme:
       * A definition paragraph
       * Sub-themes (if any), each with a brief definition
       * 2 to 4 illustrative data extracts per theme, each followed by
         analytic commentary that goes BEYOND paraphrase
       * Where relevant, link to existing literature
   - Include the final thematic map as a figure

4. Discussion (optional, depending on what the user wants)
   - Overall story across themes
   - Theoretical implications
   - Practical implications
   - Limitations
   - Future directions

References (APA 7th Edition, including Braun & Clarke, 2006)
```

For the findings section, **do not paraphrase the extracts** — paraphrasing is the most common failure of weak TA. The commentary should answer questions like: What does this theme mean? What assumptions underpin it? What are its implications? Why might participants talk about this in this way rather than another? (See Braun & Clarke, 2006, p. 24.)

Data extracts in the report should be:

- Verbatim from the transcript
- Anonymised (use participant pseudonyms or codes, e.g. P03, Kate F07a)
- Long enough to retain meaning, short enough to be readable — typically one to four sentences per extract
- Vivid and illustrative — pick the extracts that capture the point most clearly, not the first one you find

Save the file as `<study_title>_thematic_analysis.docx` in `/mnt/user-data/outputs/`.

### Include the thematic map as a figure

The thematic map (`phase6_final_map.png`) goes into the findings section as a figure. See `references/thematic-map.md` for how to generate it (use matplotlib with networkx-style layout, or a simple node-and-edge diagram).

Caption the figure with theme names, sub-theme names, and a short explanation of relationships if relevant.

### Present the files

Use `present_files` to give the user the .docx and the .png. Lead with the .docx.

---

## Iteration

After the first version is produced, expect revisions. Common iteration requests:

- Rename a theme
- Split or merge themes
- Add or remove an extract
- Re-balance commentary vs description
- Shift register (more academic / more accessible)
- Re-draw the thematic map
- Add or trim the discussion section

Treat each iteration as a targeted edit, not a full rewrite, unless the user asks for one.

---

## Important reminders

- TA is a **method**, not just a technique. Make the four upfront decisions explicit in the write-up.
- Themes do not "emerge". The analyst identifies them. Do not use "themes emerged" in the write-up — it is a passive construction that hides the analyst's active role (see Braun & Clarke, 2006, pp. 7, Note 4, and item 15 of the checklist).
- Prevalence does not require a number. If you describe prevalence, be consistent ("most participants", "a number of participants", "in over half the data set") and pick a unit of analysis (data item, participant, occurrence) and stick to it.
- Coding can take much longer than expected. Do not rush it. Phase 1 (familiarisation) is the bedrock of everything that follows.
- If the data are weak (thin, surface-level, common-sense), a good analysis is much harder. Flag this to the user early rather than over-claiming at the write-up stage.
