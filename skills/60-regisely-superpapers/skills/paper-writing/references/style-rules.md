# Writing Style Rules

## Sentence Structure

- Use normal sentence structure: subject, verb, object.
- Keep sentences short. Keep down the number of clauses.
- Vary sentence length deliberately. Mix short sentences (8–12 words) with longer ones (15–25 words). Uniform medium-length sentences signal AI-generated prose.
- Every sentence must say something. Read each sentence aloud: does it mean what it says?

## Phrases to Delete

Cut these on sight — they add no information:

- "It should be noted that" → just say it
- "It is easy to show that" → if easy, just show it
- "A comment is in order" → just make the comment
- "In other words" → say it right the first time
- "It is worth noting that" → just say it
- "An important question in the literature is" → throat-clearing
- "This paper contributes to the literature by" → say what you find, not that you "contribute"
- "We investigate / examine / explore the relationship between" → say what you find
- "The remainder of this paper is organized as follows" → just give the roadmap directly
- "We perform / conduct / carry out a regression" → "I estimate" or "I regress Y on X"
- "Results are reported in Table X" → "Table X shows…" (tables can be subjects)
- Search for "that" and delete everything before it when possible

## Word Choice

- Use simple words: "use" not "utilize", "but" not "however", "so" not "consequently".
- Use concrete domain terms; avoid abstract jargon. Examples by field:
  - Economics: "workers" not "agents", "firms" not "production units"
  - Medicine: "patients" not "subjects" (when clinical context allows), "people who took the drug" not "the treatment-exposed cohort"
  - Political science: "voters", "candidates", "legislators" — avoid generic "actors"
  - Epidemiology: "people exposed to X" reads better than "the exposure group" in body text
- Do NOT use adjectives to describe your own work ("striking results", "very significant", "novel finding").
- Do NOT use double adjectives ("very novel").
- Clothe the naked "this": write "This regression shows…" not "This shows…".

## Voice and Perspective

- Use "I" for single-authored papers (not the royal "we").
- For multi-authored papers, "we" refers to the authors. Be consistent throughout.
- Use "we" to mean "you the reader and I" only in single-authored papers, and only when the context is clearly inclusive (e.g., "we can see from the figure").
- Tables and figures can be subjects: "Table 5 presents…", "Figure 2 shows…".
- Never write "one can see that…".
- Active voice by default. Passive voice is acceptable in two narrow contexts:
  - Methods descriptions where the agent is irrelevant: "Wages were measured using administrative tax records", "Blood pressure was recorded at baseline by trained nurses".
  - Table and figure captions: "Standard errors are clustered at the state level", "Outcomes were assessed at 12 months post-randomization".
- In all other prose, use active voice.

## Coauthorship and Multi-Author Writing

- Before writing, agree on voice: "we" throughout, or let the lead author use a consistent style.
- Designate one person as the "voice editor" — the coauthor responsible for ensuring consistent tone, tense, and style across all sections.
- When describing individual contributions (footnotes or author statements): "Author A conducted the empirical analysis; Author B developed the theoretical model".
- Do NOT let different writing styles coexist across sections. A paper that sounds like two different people wrote it signals careless editing.
- For job market papers and dissertations: the candidate's name appears first; the introduction makes clear which contributions are the candidate's.

## Pronouns and References

- "Where" refers to a place. "In which" refers to a model or framework.
- Write "models in which consumers have shocks" — not "models where consumers have shocks".
- Hyphenate compound modifiers before nouns: "risk-free rate", "after-tax income", "well-known result", "double-blind trial".
- But not when the first word is an adverb ending in *-ly*: "randomly assigned treatment", "highly cited paper".

## Footnotes

- Do NOT use footnotes for parenthetical comments.
- If it is important, put it in the text. If not, delete it.
- Use footnotes only for things typical readers can skip but some might want: data documentation, simple algebra, extended references, technical caveats that would interrupt the argument.

## Numbers and Notation

- Use 2–3 significant digits, not whatever the software outputs. "0.45" or "0.453", not "0.4528347".
- Use sensible units (percentages, percentage points, dollars, deaths per 100,000 — not 0.0000023 of a probability).
- Define Greek letters clearly. Give them names, not just symbols: "the elasticity of substitution, σ, equals 3".
- Remind readers of definitions on later use, especially across distant sections.
- Convention: Latin letters for variables (Y, X, D), Greek letters for parameters and coefficients (β, γ, σ).
- Include subscripts on all variables (i, j, k, t) from smallest to largest unit.

## Paragraphs

- One idea per paragraph.
- Topic sentence first.
- Paragraphs should flow logically from one to the next.
- Minimize forward references ("As we will see in Table 6") and backward references ("Recall from Section 2 that…"). Heavy use of either signals that material is in the wrong order. If a reader needs information now, present it now. Brief backward references are acceptable when actively building on earlier results.
- Do not fragment a section into many short subsections when the content flows naturally as paragraphs (this echoes the academic-baseline principle 9).

## Causal vs Correlational Phrasing

Applied sentence by sentence per academic-baseline principle 4:

- With identification (RCT, DiD, IV, RDD, defended natural experiment): "The minimum wage increase reduced teen employment by 3 percentage points."
- Without identification (OLS on observational data, no instrument): "Higher minimum wages are associated with lower teen employment in the cross-section."

## Avoiding AI-Generated Writing Patterns

AI-assisted writing has telltale patterns. Eliminate these:

- **Banned words** (in addition to the phrases listed above):
  - Never use: "delve", "landscape" (as metaphor), "multifaceted", "notably", "leverage" (as verb meaning "use"), "robust" (outside its statistical meaning), "pivotal", "groundbreaking", "shed light on", "pave the way", "tapestry", "intricate", "underscore", "comprehensive" (as filler).
- **Vary sentence length**: mix short and long. AI tends toward uniform medium-length sentences.
- **Use field-specific vocabulary naturally**:
  - Labor economics: "extensive margin", "intensive margin"
  - Industrial organization: "pass-through", "markup"
  - Program evaluation: "treatment on the treated", "ITT"
  - Epidemiology: "incidence rate ratio", "person-years at risk"
  - Political science: "valence", "issue ownership"
  - Generic phrasing across all fields signals AI.
- **Include parenthetical asides and em-dashes — sparingly**. Real writers use these for qualifications and side notes. The academic-baseline principle 9 cautions against overusing them; the goal is *natural* use, not heavy use.
- **Allow natural roughness**: not every transition needs to be perfectly smooth. Real papers have some friction between sections. A period and a new topic sentence is fine.
- **Be specific about institutions**: name the actual dataset, agency, policy, or country. AI defaults to generic placeholder language.
- **Avoid perfect parallel structure in every list**: vary your constructions. Real writing is slightly irregular.
- **Hedge appropriately**: write "This likely reflects…" or "One interpretation is…" when warranted. AI either over-hedges everything or never hedges.
- **Avoid bullet-list-heavy prose**: in academic body text, flowing paragraphs are the default. Bullets belong in tables, captions, and procedural sections (Methods steps), not in Introduction, Results discussion, or Conclusion.

## Quick Self-Check Before Submitting a Section

Run this five-pass review on every section you draft:

1. **Throat-clearing pass**: search for "It is", "There is", "There are" at sentence start. Most should be cut.
2. **Passive pass**: search for " was ", " were ", " is ", " are " in body prose (not captions or methods). Convert most to active.
3. **Adjective pass**: search for "novel", "robust", "important", "interesting", "significant" applied to your own work. Cut or replace with magnitudes.
4. **Forbidden-word pass**: search for the AI-pattern banned words above. Replace.
5. **Concreteness pass**: every claim about findings should have a magnitude or a specific institution attached. "The effect is large" → "The effect equals 0.4 standard deviations of the outcome distribution".
