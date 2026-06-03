---
name: slr-prisma
description: "Guide users through writing a systematic literature review (SLR) following the PRISMA 2020 framework. Use this skill whenever the user mentions 'systematic review', 'systematic literature review', 'SLR', 'PRISMA', 'PRISMA 2020', 'PRISMA flow diagram', 'PRISMA checklist', or asks for help writing, structuring, or auditing a literature review that follows reporting guidelines. Also trigger when the user asks about inclusion/exclusion criteria for a review, search strategies for databases like Scopus/WoS/PubMed, study selection processes, risk of bias assessment, or narrative synthesis for a review paper. This skill covers the full PRISMA 2020 checklist (27 items), produces a Word document manuscript in strict journal article format, generates an annotated PRISMA flow diagram, and enforces APA 7th Edition referencing throughout. It does NOT cover meta-analysis or statistical pooling. By Chuah Kee Man."
---

# Systematic Literature Review — PRISMA 2020

**Author:** Chuah Kee Man | **Based on:** PRISMA 2020 (Page et al., 2021)

This skill walks a user through writing a systematic literature review (SLR) that follows the PRISMA 2020 reporting guideline. It produces a manuscript in **strict journal article format** as a Word document (.docx), generates an **annotated PRISMA flow diagram**, and enforces **APA 7th Edition referencing** throughout.

## Before you begin

Read these reference files as needed:
- `references/prisma-2020-checklist.md` — The full 27-item PRISMA 2020 checklist. Consult this when drafting each section to make sure nothing is missed.
- `references/flow-diagram.md` — PRISMA flow diagram templates and guidance. Consult this when building the flow diagram.

Also read these skills before generating outputs:
- **docx skill** (`/mnt/skills/public/docx/SKILL.md`) — Critical rules for docx-js when generating the Word document.
- **apa-referencing skill** (`/mnt/skills/user/apa-referencing/SKILL.md`) — APA 7th Edition formatting rules. All citations and references in the manuscript must comply with APA 7th Edition. Consult `references/apa7-formatting-rules.md` within that skill for type-specific formatting.

If the user has a **writing-style skill**, apply it to all drafted prose (but note that academic writing conventions in the writing-style skill take precedence over informal style rules, e.g. no informal analogies in scholarly manuscripts).

---

## Phase 1: Interview

Before any drafting, gather the information needed to write the review. Offer the user two paths up front.

### Path A: Upload existing documents

The user may already have a proposal, protocol, draft manuscript, PROSPERO registration, data extraction sheet, or search log. At the start of the interview, ask whether they have any documents to share. Common uploads include:

- Research proposal or protocol (often contains RQs, eligibility criteria, databases, and methods)
- PROSPERO registration form
- Draft or partial manuscript
- Search strategy export or search log
- Data extraction spreadsheet (e.g. from Excel, Google Sheets, or Rayyan/Covidence export)
- List of included/excluded studies
- Completed PRISMA checklist from a previous attempt
- Reference list or bibliography file

If the user uploads a document, read it using the appropriate skill (docx skill for .docx, file-reading skill for other formats, pdf-reading skill for PDFs, or xlsx skill for spreadsheets). Extract as much of the essential information (listed below) as possible from the document. Then present a summary of what was extracted and ask the user to confirm, correct, or fill in the gaps.

If the user uploads multiple documents, read them all and cross-reference the information. Flag any contradictions (e.g. different inclusion criteria in the proposal vs. the draft).

### Path B: Conversational interview

If the user has no documents to share, or after extracting what is available from uploaded documents, gather the remaining information conversationally. Ask questions in a natural flow, not as a wall of text. Adapt to what the user already provides.

### Essential information to collect

**About the review itself:**
- Working title
- Research question(s) or objective(s)
- Type of review (e.g. intervention effectiveness, diagnostic accuracy, qualitative, scoping turned systematic, mixed methods)
- Whether this is a new review or an update of a previous one
- Registration status (e.g. PROSPERO number, or not registered)
- Protocol status (published, unpublished, not prepared)
- Target journal (if known) — this affects formatting, word limits, and referencing conventions

**About the search:**
- Databases searched (e.g. Scopus, Web of Science, PubMed, ERIC, IEEE Xplore, ProQuest)
- Other sources (websites, grey literature, citation searching, hand-searching, expert consultation)
- Date range and date of last search
- Search terms and Boolean strategy (or enough detail to reconstruct one)
- Any filters or limits applied (language, date, document type)

**About eligibility:**
- Inclusion criteria (population, intervention/exposure, comparator, outcome, study design — or the relevant framework like PICo, PICO, SPIDER, etc.)
- Exclusion criteria
- How studies were grouped for synthesis

**About screening and selection:**
- Number of reviewers at each stage
- Whether reviewers worked independently
- How disagreements were resolved
- Any automation tools used (e.g. Rayyan, ASReview, Covidence)

**About data extraction:**
- What data items were extracted (outcomes, variables, study characteristics)
- Data extraction tool or form used
- Number of reviewers, independence, and conflict resolution

**About quality appraisal:**
- Risk of bias tool used (e.g. RoB 2, ROBINS-I, Newcastle-Ottawa Scale, CASP, JBI, MMAT)
- Number of reviewers and independence

**About synthesis:**
- Synthesis approach (narrative synthesis, thematic synthesis, framework synthesis, vote counting, harvest plots, etc.)
- How results will be presented (tables, figures, summary of findings)

**About the numbers (for the flow diagram):**
- Records identified per database/source
- Duplicates removed
- Records screened and excluded
- Full-text reports retrieved and not retrieved
- Full-text reports assessed and excluded (with reasons)
- Final number of included studies

If the user does not have all the numbers yet (common for students mid-process), note which are missing and use placeholder values (n = ?) in the flow diagram. The user can fill these in later.

**About references:**
- Ask whether the user has a reference list or bibliography already. If so, it should be uploaded for APA formatting and verification.
- Ask whether references should be verified using web search. (Default: yes, verify.)

### How to run the interview

Start by asking the user whether they have any existing documents to share. If they do, read the documents first and extract what you can before asking follow-up questions.

If no documents are provided, or after processing uploads, work through the remaining gaps conversationally. Start with the big picture (title, RQ, databases) and work through the rest in 2–3 rounds of questions, grouping related items together. Use the ask_user_input tool where options are bounded (e.g. risk of bias tool choice, synthesis approach). Use open questions for things like research questions and search terms.

Once you have enough to begin, confirm the plan with the user before drafting.

---

## Phase 2: Section-by-section drafting (strict journal format)

The manuscript must follow **strict journal article format**. This means the document reads as a single, cohesive academic paper ready for submission, not a report or a student assignment. Every section must be written in formal academic prose, following the conventions of peer-reviewed journals.

Work through the manuscript one section at a time. After drafting each section, present it to the user and wait for feedback or approval before moving on.

### Manuscript structure and PRISMA mapping

Draft sections in this order. The PRISMA item numbers in brackets show which checklist items each section addresses. This structure mirrors the standard journal article format used by most peer-reviewed journals publishing systematic reviews.

**TITLE PAGE**
1. Title [Item 1]
2. Author name(s) and affiliation(s)
3. Corresponding author contact details
4. ORCID iD(s) (if available)
5. Word count
6. Number of tables and figures

**ABSTRACT** [Item 2]
- Use the PRISMA 2020 for Abstracts structure
- For journals requiring structured abstracts, include these subheadings: Background, Objectives, Data Sources, Study Eligibility Criteria, Participants and Interventions, Study Appraisal and Synthesis Methods, Results, Limitations, Conclusions, Registration Number
- For journals requiring unstructured abstracts, cover the same content in paragraph form
- Typically 200–300 words (check target journal requirements)
- Include 4–6 keywords below the abstract

**1. INTRODUCTION**
- 1.1 Rationale [Item 3] — Situate the review within existing knowledge. Identify the gap. Cite prior reviews and explain why a new or updated review is needed.
- 1.2 Objectives [Item 4] — State the review's objective(s) or research question(s) explicitly. If using a framework (PICO, PICo, SPIDER), present it here.

**2. METHODS**
- 2.1 Protocol and registration [Items 24a–24c] — State registration number (e.g. PROSPERO CRD...) or declare unregistered. Note any amendments.
- 2.2 Eligibility criteria [Item 5] — Present inclusion and exclusion criteria explicitly, ideally in a table. Use the relevant framework (PICO, PICo, etc.).
- 2.3 Information sources [Item 6] — List all databases, registers, websites, and other sources. State the date of last search for each.
- 2.4 Search strategy [Item 7] — Present the full Boolean search string for at least the primary database. If the user provides keywords but not a Boolean string, help them construct one. State any filters or limits.
- 2.5 Selection process [Item 8] — Describe the screening procedure, number of reviewers, independence, disagreement resolution, and any automation tools.
- 2.6 Data collection process [Item 9] — Describe how data were extracted, by how many reviewers, and how conflicts were resolved.
- 2.7 Data items [Items 10a, 10b] — List all outcome variables and other data items sought.
- 2.8 Study risk of bias assessment [Item 11] — Name the tool (e.g. RoB 2, CASP, JBI, MMAT) and describe the assessment process.
- 2.9 Effect measures [Item 12] — Specify effect measures if applicable. Skip or mark "Not applicable" for purely qualitative reviews.
- 2.10 Synthesis methods [Items 13a–13f] — Describe the synthesis approach. For narrative synthesis, explain how studies were grouped, compared, and synthesised. Address each applicable sub-item (13a through 13f).
- 2.11 Reporting bias assessment [Item 14]
- 2.12 Certainty assessment [Item 15] — e.g. GRADE approach, if applicable.

**3. RESULTS**
- 3.1 Study selection [Items 16a, 16b] — Describe the selection process in narrative form AND include the PRISMA flow diagram (see Phase 3). Cite any studies that appear to meet inclusion criteria but were excluded, and explain why.
- 3.2 Study characteristics [Item 17] — Present a summary table of included studies (author/year, country, study design, population, intervention/exposure, outcome, key findings). This table is a standard feature of SLR journal articles.
- 3.3 Risk of bias in studies [Item 18] — Present risk of bias assessments, typically as a summary table or figure.
- 3.4 Results of individual studies [Item 19] — Present findings from each study.
- 3.5 Results of syntheses [Items 20a–20d] — Present the synthesis findings. Organise by theme, outcome, or research question as appropriate.
- 3.6 Reporting biases [Item 21]
- 3.7 Certainty of evidence [Item 22]

**4. DISCUSSION**
- 4.1 Summary of evidence [Item 23a] — Interpret the main findings in the context of other evidence.
- 4.2 Limitations [Items 23b, 23c] — Address limitations of the evidence (23b) and limitations of the review process (23c) separately.
- 4.3 Implications [Item 23d] — Discuss implications for practice, policy, and future research.

**5. CONCLUSIONS**
- A concise paragraph summarising the key findings and their significance. Some journals merge this into the Discussion; adapt to the target journal's convention.

**DECLARATIONS**
- Funding [Item 25]
- Competing interests [Item 26]
- Data availability [Item 27]
- Author contributions (if required by the target journal)
- Ethics approval (if applicable)
- Acknowledgements

**REFERENCES**
- All references must be formatted in APA 7th Edition style. See the "Referencing" section below for detailed rules.

**APPENDICES** (if needed)
- Full search strategies for each database
- Data extraction form
- Completed PRISMA 2020 checklist

### Drafting conventions for journal format

These conventions apply throughout the manuscript:

- **Academic register throughout.** No conversational language, informal analogies, or hedging phrases like "it seems" or "it appears". Use precise disciplinary language.
- **Third person and passive voice where appropriate.** "Studies were screened by two reviewers" rather than "We screened the studies". (Some journals now accept first person; adapt if the user specifies.)
- **Past tense for methods and results.** "A systematic search was conducted..." / "Twenty-three studies met the inclusion criteria..."
- **Present tense for established knowledge and discussion.** "Evidence suggests that..." / "These findings are consistent with..."
- **Every claim must be supported by a citation.** Do not leave factual claims uncited in the Introduction or Discussion. Use APA 7th Edition in-text citations.
- **Tables and figures are numbered sequentially.** Table 1, Table 2, etc. Figure 1, Figure 2, etc. Each must have a title (above for tables, below for figures in APA style) and be referenced in the text.
- **No bullet points in the body text.** Journal manuscripts use continuous prose. The only exceptions are the eligibility criteria table and the PRISMA flow diagram. Bullet points may appear in Appendices if appropriate.
- **Section numbering.** Use numbered sections (1., 1.1, 1.2, 2., 2.1, etc.) unless the target journal prohibits it.

### Tone calibration

**For postgraduate students (first-time reviewers):**
- Explain what each section needs to achieve before drafting it
- Flag common mistakes (e.g. writing eligibility criteria as vague narrative instead of explicit include/exclude lists)
- Offer brief rationale for why PRISMA requires certain details (transparency and reproducibility)

**For experienced researchers:**
- Skip the explanations and draft directly
- Focus on completeness and precision

**When in doubt:** briefly explain and offer to skip ("I can walk you through what this section needs, or just draft it directly. Your call.")

---

## Phase 3: PRISMA flow diagram

After drafting the Results section (specifically Item 16a), generate the PRISMA flow diagram. The flow diagram serves two purposes: it satisfies the PRISMA reporting requirement, and it gives readers an at-a-glance summary of the study selection process.

### Step 1: Select the correct template

Read `references/flow-diagram.md` to determine which template applies:

| Review type | Sources searched | Template |
|-------------|-----------------|----------|
| New review | Databases and registers only | Template A |
| New review | Databases, registers, and other sources | Template B |
| Updated review | Databases and registers only | Template C |
| Updated review | Databases, registers, and other sources | Template D |

Most student and first-time SLRs use Template A or Template B.

### Step 2: Confirm the numbers

Before building the diagram, confirm every number with the user. Present a structured summary of what goes in each box so the user understands what to fill in. Use this annotated guide:

**IDENTIFICATION phase — what goes here:**
- Total records identified from each database (e.g. Scopus: 245, WoS: 189, PubMed: 112). This is the raw count before any deduplication.
- Records from registers, if any.
- If Template B/D: records from other methods (websites, citation searching, grey literature, expert consultation), listed by source.
- Records removed before screening: duplicate records, records marked ineligible by automation tools, records removed for other reasons (e.g. non-English, outside date range).

**SCREENING phase — what goes here:**
- Records screened (= total identified minus those removed before screening). This is typically title-and-abstract screening.
- Records excluded at screening (with or without reasons at this stage).
- Reports sought for retrieval (= records that passed screening). "Reports" means the full-text documents.
- Reports not retrieved (= full texts that could not be obtained, with reasons if possible).
- Reports assessed for eligibility (= full texts actually read and evaluated against inclusion criteria).
- Reports excluded at eligibility, with reasons. List each reason and its count, e.g. "Wrong population (n = 8), Wrong outcome (n = 5), Not empirical (n = 3)".

**INCLUDED phase — what goes here:**
- Studies included in the review (the final count).
- Reports of included studies (may differ from the study count if one study produced multiple publications, or one publication reports multiple studies).

If the user does not have all the numbers yet, use placeholder values (n = ?) and note which are missing.

### Step 3: Generate the flow diagram

Build the flow diagram in two formats:

**A. As a table in the Word document.** This goes in the Results section.
- Use a table-based layout with merged cells to represent the flow.
- Shaded header rows for each phase (Identification, Screening, Included).
- Arrow indicators between stages (use "↓" or "→" text within cells).
- Clear box borders for each step.
- Label it as "Figure 1. PRISMA 2020 flow diagram of study selection."

**B. As a standalone visual using the Visualizer tool.** Generate an SVG PRISMA flow diagram so the user can see the flow visually and understand the structure. This serves as a learning aid and reference. Use the annotated labels from Step 2 so the user can see exactly what information belongs in each box. The visual should clearly show:
- The three phases (Identification, Screening, Included) as distinct horizontal bands
- Boxes for each step with arrows connecting them
- Side branches for exclusions at each stage
- Placeholder counts (n = ?) or actual counts if available
- Colour coding: blue/grey for main flow, amber/orange for exclusion branches

### Key distinctions to explain to users

These distinctions trip up many first-time reviewers:
- **Records ≠ Reports ≠ Studies.** A record is a database entry (title/abstract). A report is a full document (article, thesis, etc.). A study is the underlying investigation. One study can produce multiple reports, and one report can describe multiple studies.
- **Screening vs. Eligibility.** Screening is typically at the title-and-abstract level. Eligibility assessment happens at the full-text level.
- **Exclusion reasons at eligibility.** These must be specific and countable. "Not relevant" is too vague. Use criteria-linked reasons such as "Wrong population", "Wrong study design", "No relevant outcome measured".

---

## Phase 4: Referencing (APA 7th Edition)

All references in the manuscript must follow APA 7th Edition formatting. This is non-negotiable regardless of the target journal's house style, unless the user explicitly requests a different citation style.

### In-text citations

- **Parenthetical:** (Author, Year) or (Author & Author, Year) or (Author et al., Year)
- **Narrative:** According to Author (Year) or Author and Author (Year) reported that...
- For 1–2 authors, list all names in every citation.
- For 3 or more authors, use "et al." after the first author from the first citation onward.
- Multiple citations in parentheses are separated by semicolons and ordered alphabetically: (Adams, 2019; Chen et al., 2021; Roberts & Lee, 2020).

### Reference list

- Placed after the Declarations section, before Appendices.
- Alphabetical order by first author's surname.
- Hanging indent (first line flush left, subsequent lines indented 0.5 inches / 1.27 cm).
- All authors listed (up to 20). For 21 or more, list the first 19, then an ellipsis, then the last author.
- DOIs formatted as `https://doi.org/10.xxxx/xxxx` — no full stop after a DOI.
- Sentence case for article, chapter, and book titles. Title case for journal names.
- Italicise book titles, journal names, and volume numbers. Do not italicise article titles or issue numbers.

### Verification

When the user provides references:
1. Read the apa-referencing skill (`/mnt/skills/user/apa-referencing/SKILL.md`) and its `references/apa7-formatting-rules.md` file.
2. Check each reference for APA 7th compliance.
3. Use web_search to verify that each reference is real. Flag any that cannot be verified.
4. Present corrections with brief explanations of what was wrong.

When generating references during drafting (e.g. citing the PRISMA 2020 statement itself, or citing methodological sources), always use web_search to find the real source first. Never fabricate any part of a reference.

### Mandatory references

Every PRISMA 2020 systematic review should cite the PRISMA 2020 statement. Verify the correct reference via web search before including it. The statement is typically cited in the Introduction (when explaining the reporting framework used) and in the Methods (when describing the review methodology).

---

## Phase 5: Generate the Word document

Once all sections are drafted and approved, compile the full manuscript into a .docx file.

### Document formatting

Read the **docx skill** (`/mnt/skills/public/docx/SKILL.md`) before generating the document. Apply these specifications:

- **Page size:** A4 (11906 × 16838 DXA) — standard for Malaysian and international journal submissions.
- **Margins:** 1 inch on all sides (1440 DXA).
- **Font:** Times New Roman, 12pt body text. (Some journals require Arial; adapt if the user specifies.)
- **Line spacing:** Double-spaced throughout (standard for manuscript submission).
- **Paragraph spacing:** No extra spacing between paragraphs beyond double-spacing.
- **Alignment:** Left-aligned (ragged right), not justified. (Standard for manuscript submission; justified text is for final published layout.)
- **Page numbers:** In the header or footer, right-aligned.
- **Running head:** Optional; include if the target journal requires it.

### Document structure in the .docx

Organise the document in this order:

1. **Title page** — Title, authors, affiliations, corresponding author, word count, table/figure count.
2. **Abstract page** — Abstract text, keywords.
3. **Main text** — Sections 1 through 5 as outlined in Phase 2.
4. **Declarations** — Funding, competing interests, data availability, author contributions, acknowledgements.
5. **References** — APA 7th Edition reference list with hanging indents.
6. **Tables** — Each table on a separate page, numbered sequentially, with title above.
7. **Figures** — Each figure on a separate page, numbered sequentially, with caption below. The PRISMA flow diagram is typically Figure 1.
8. **Appendices** — Full search strategies, data extraction form, PRISMA checklist (if included).

Note: Some journals want tables and figures embedded in the text. Others want them at the end. Default to placing them at the end (standard manuscript submission format) unless the user specifies otherwise.

### Heading styles

Use docx-js heading styles:
- **Heading 1** for main sections (1. INTRODUCTION, 2. METHODS, 3. RESULTS, 4. DISCUSSION, 5. CONCLUSIONS)
- **Heading 2** for subsections (2.1 Protocol and Registration, 2.2 Eligibility Criteria, etc.)
- **Heading 3** for sub-subsections if needed
- Include `outlineLevel` for Table of Contents compatibility (0 for H1, 1 for H2, 2 for H3)

### Tables

- Use docx-js Table with proper borders, cell margins, and column widths.
- Table titles go above the table (APA style): "Table 1\n*Title of Table in Italics*"
- Notes go below the table in a smaller font size.
- The study characteristics table (Table 1 or 2) is a standard feature. Typical columns: Author(s) (Year), Country, Study Design, Sample/Population, Intervention/Exposure, Outcome(s), Key Findings.

### After generating

1. Validate the document: `python scripts/office/validate.py doc.docx`
2. Copy to `/mnt/user-data/outputs/` and present to the user.
3. Offer to generate a separate filled PRISMA checklist document if the user wants one.

---

## Phase 6: PRISMA checklist audit (optional)

If the user asks for a checklist audit, or after the manuscript is complete, offer to produce a filled PRISMA 2020 checklist. This is a table with three columns:

| Item # | Checklist item | Reported in section / page |

Read `references/prisma-2020-checklist.md` and map each of the 27 items to where it appears in the manuscript. Flag any items that are missing or incomplete so the user can address them.

This can be produced as a separate Word document or appended to the manuscript as an Appendix.

---

## Handling partial requests

Not every user will want the full pipeline. Common partial requests and how to handle them:

- **"Help me write my Methods section"** — Run a targeted interview for Methods-related info only, then draft the Methods subsections with PRISMA items 5–15 in journal format.
- **"Create a PRISMA flow diagram"** — Ask for the numbers, select the right template, generate the diagram in a Word doc AND as a visual using the Visualizer. Explain what goes in each box.
- **"Check my SLR against PRISMA"** — Ask the user to upload their manuscript, read it, audit against the 27-item checklist, and report which items are missing or incomplete.
- **"Help me build a search strategy"** — Interview about topic, databases, and terms, then construct Boolean search strings.
- **"I just need the Results section"** — Gather the relevant data and draft Results with items 16–22 in journal format.
- **"Check my references"** — Read the apa-referencing skill, check all references for APA 7th compliance, verify them via web search, and present corrections.
- **"Show me what a PRISMA diagram looks like"** — Generate an annotated example PRISMA flow diagram using the Visualizer, with labels explaining what goes in each box.

Always anchor partial work to the relevant PRISMA items so the user knows which parts of the checklist they are addressing.

---

## Important reminders

- PRISMA is a **reporting** guideline, not a **conduct** guideline. It tells you what to report, not how to do the review. If the user needs methodological guidance (e.g. how to actually screen studies), help them, but be clear about the distinction.
- The 2020 version supersedes the original 2009 PRISMA statement. If the user references the old version, gently steer them to PRISMA 2020.
- PRISMA 2020 is primarily designed for reviews of interventions. For other types (scoping reviews, diagnostic test accuracy, network meta-analysis), there are PRISMA extensions. If the user's review type clearly falls under an extension, mention it and offer to adapt the guidance. For most SLRs in social science, education, and health, the main PRISMA 2020 checklist is appropriate.
- Not every item applies to every review. Qualitative or mixed-methods reviews may skip or adapt items like Effect Measures (12) or statistical synthesis (13d, 20b). Help the user identify which items are relevant and which can be marked "Not applicable".
- **The manuscript must read as a journal article**, not as a template, checklist walkthrough, or student report. Every section should use continuous academic prose, with tables and figures integrated at the appropriate points.
- **All references must be real.** Never fabricate a reference. Always verify via web search when the apa-referencing skill's verification process is triggered.
- **APA 7th Edition is the default citation style.** If the user specifies a different style required by their target journal, adapt accordingly, but default to APA 7th.
