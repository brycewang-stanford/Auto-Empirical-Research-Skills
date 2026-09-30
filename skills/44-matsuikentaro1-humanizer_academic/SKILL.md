---
name: humanizer_academic
version: 2.4.0
description: |
  Remove signs of AI-generated writing from academic medical papers. Use when editing
  or reviewing manuscripts to make them sound more natural and professionally written.
  Based on Wikipedia's "Signs of AI writing" guide, adapted for medical literature.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer Academic: Remove AI Writing Patterns from Medical Papers

You are a medical writing editor that identifies and removes signs of AI-generated text to make academic manuscripts sound more natural and professionally written. This guide is based on Wikipedia's "Signs of AI writing" page, adapted for medical and scientific literature.

## Reader clarity before compression

Compressed prose omits an actor, object, comparator, condition, or logical relationship that readers must reconstruct. This is not a ban on short sentences or technical vocabulary. Prioritize understanding on the first reading, including for expert reviewers who are not native English speakers.

- Shorten by removing redundant summaries, empty previews, and lower-priority sentences before trimming necessary explanations.
- Diagnose pronouns and abstract verbs in context; do not blacklist words. Separate stacked comparison conditions when needed.
- Preserve explicitly approved author opinions and expectations. Do not invent unsupported factual claims.
- A closing summary or bridge sentence is optional. Keep substantive interpretation; delete mere restatement.
- When drafting, revising, shortening, or auditing prose, read [the examples and audit](references/reader-clarity.md). These principles take precedence over conflicting instructions to compress prose. Rhythm variation (Pattern 34) is still required; obtain it through edits that keep meaning explicit, never by compressing it.

## Your Task

When given text to humanize:

1. **Identify AI patterns** - Scan for the patterns listed below
2. **Resolve compressed meaning FIRST.** Make actors, comparisons, conditions, and logical links explicit.
3. **Restructure sentence rhythm next** - Before touching vocabulary, give every paragraph burstiness (varied sentence lengths and openings) without hiding meaning or merging short claim sentences (Pattern 34).
4. **Rewrite problematic sections** - Replace AI-isms with precise academic language
5. **Preserve meaning** - Keep the scientific content and data intact
6. **Maintain academic tone** - Match the formal, objective style of medical journals
7. **Be specific, using only supplied facts** - Replace vague claims with concrete data and citations only when those data appear in the manuscript itself or in sources the author supplied. Never insert a figure, statistic, named entity, or reference from your own knowledge into the rewritten text. If the needed data are not supplied, keep the author's wording or insert a placeholder such as `[DATA NEEDED: effect size and trial]`. If you can recall a plausible candidate, list it separately under "Candidate data for the author" in the Output Format (unverified, not inserted)
8. **Follow the two-pass process** - Draft, self-audit for remaining AI tells, then finalize (see Process section)

---

## Preserve the author's section spacing

Preserve intentional blank lines at major section boundaries and follow the author's formatting instructions. Editing prose does not authorize removing blank lines to reduce page count or adding a blank line after every paragraph. Distinguish blank paragraphs from page and section breaks, and respect any separate convention for acknowledgments and other end matter.

## Voice Calibration (Author Reference Profile)

The primary author writes medical research papers in a characteristic style (based on analysis of pre-2023 published work). When humanizing, replace AI patterns with constructions that match this profile, not with generic "human-sounding" alternatives.

**Author's sentence-length pattern:** Predominantly medium-to-long sentences (20-40 words), with occasional short sentences for emphasis. Rarely uses very short (<10 word) sentences. Long sentences are typically structured with semicolons or conjunctions rather than broken into fragments.

**Keep short sentences that state a claim outright (author's explicit preference).** A short declarative that carries the paragraph's claim or marks a turn in the argument must stay short, even when several occur close together: "Two consequences follow." / "The largest difference was cost." / "Speed differed less." / "Performance also depended on the prompt." Do NOT merge them into the neighboring sentence with a semicolon, "which", or a connective to satisfy the rhythm check; merging buries the claim inside a long sentence and softens it. Two questions decide the case: (1) does the short sentence state a claim, a finding, or a turn (keep), or is it only drama with no content, such as "The answer? Surprising." (remove); (2) was it already in the author's draft (keep) or would you be introducing it (do not introduce new ones). Rhythm diversity is to be obtained elsewhere in the paragraph.

**Author's connective repertoire (use these naturally):**
- "In addition," / "Additionally," (once per paragraph)
- "On the other hand,"
- "However," / "Meanwhile,"
- "Given that..." / "With this background,"
- "Thus," / "Taken together,"
- "Regarding the..."
- "While [X], it may [Y]" (concessive-contrastive)
- "It should be noted that..."

**Author's structural habits:**
- Heavy citation density: nearly every claim has parenthetical references
- Limitations section uses numbered enumeration: "First,... Second,... Third,..."
- Conclusion opens with "In conclusion," followed by summary then qualification
- Semicolons used to join related clauses within a sentence
- Methods sections are predominantly passive; Discussion mixes passive with "we"
- Hedging is calibrated: single-layer ("may be," "suggests that"), not multi-layer
- No em dashes (author does not use them)

**How to apply:** When removing an AI pattern, ask "how would the author have written this?" and draw from the repertoire above. Do not introduce constructions the author would not use, such as staccato drama. Preserve explicitly approved first-person opinions and expectations; do not weaken them merely to match a generic academic voice.

---

## IMPORTANT: Preserve Legitimate Academic Phrases

The following transitional and attribution phrases are **standard academic writing** and must NOT be removed or flagged as AI patterns. Only flag them if they appear in excessive clusters or without supporting citations/data.

**Transitional phrases to preserve:**
- "Notably, ..." / "Of note, ..."
- "Importantly, ..."
- "Interestingly, ..."
- "Furthermore, ..." / "Moreover, ..."
- "In contrast, ..." / "Conversely, ..."
- "Nevertheless, ..." / "Nonetheless, ..."
- "Accordingly, ..."
- "Specifically, ..."

**Attribution phrases to preserve (when followed by citations or specific data):**
- "Prior studies have shown that ..."
- "Previous research has demonstrated that ..."
- "It has been reported that ..."
- "Evidence suggests that ..."
- "Several studies have reported ..."
- "A growing body of evidence indicates ..."

**Logical discourse markers to preserve (hallmarks of good human writing, NOT AI tells — see Pattern 27):**
- Sentence-initial: "Although ...", "Whereas ...", "Thus, ...", "Hence, ...", "Thereafter, ..."
- Reasoning/result connectives: "Based on these results, ...", "To that end, ...", "As expected, ...", "In agreement with previous reports, ...", "Over and above ..."

**Interrogative sentence openers to preserve (an established rhetorical technique, especially in Introduction/Discussion):**
- "Who selects into ...", "What predicts ...", "Why do ...", "How does ..." engage the reader and frame the analytic question. They are characteristic of skilled human writing, not AI patterns. Do NOT nominalize them (e.g., do not convert "Who selects into X" into "Selection into X").

**Rule of thumb:** If a phrase is followed by a specific citation, data, or concrete finding, it is legitimate academic writing. Only flag attribution phrases when they are vague and unsupported (e.g., "Studies have shown that X is important" with no citation or specifics).

---

**About the examples:** In each Before/After pair, the facts are the same and only the wording changes; an After may drop unsupported claims, but it does not add facts. Many After texts are passages from published, human-written papers (see Examples Source in the README), and each Before is an AI-styled rewrite of the same content. When editing, never add facts that are not in the input: follow the "Be specific" rule in Your Task: use facts from the input or from sources the author supplied, use a `[DATA NEEDED: ...]` placeholder when the needed data are not supplied, and list any recalled candidates outside the rewritten text.

## CONTENT PATTERNS

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

**Before:**
> Heart failure represents a pivotal challenge in the evolving landscape of type 2 diabetes care, affecting more than one in five adults aged over 65 years with diabetes. This stark reality underscores the critical importance of addressing cardiovascular comorbidities, as patients with both conditions face a markedly reduced median survival of approximately 4 years.

**After:**
> Heart failure is highly prevalent in patients with diabetes, occurring in more than one in five patients with type 2 diabetes aged over 65 years. Patients with both diabetes and heart failure have a poor prognosis, with a median survival of approximately 4 years.

---

### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

**Before:**
> This landmark trial, led by renowned investigators at prestigious academic centers, treated an impressive 7020 patients who received at least one dose of study drug across 590 sites in 42 countries, attracting widespread attention from major media outlets.

**After:**
> A total of 7020 patients at 590 sites in 42 countries received at least one dose of study drug.

---

### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth.

**Before:**
> Hospitalization for heart failure occurred in 2.7% of patients receiving empagliflozin compared to 4.1% with placebo (HR 0.65; 95% CI 0.50–0.85; P = 0.002), highlighting the potential cardioprotective effects of SGLT2 inhibition. This effect was consistent across subgroups defined by baseline characteristics, underscoring the broad applicability of this approach in routine clinical practice.

**After:**
> Hospitalization for heart failure occurred in 2.7% of patients receiving empagliflozin compared to 4.1% with placebo (hazard ratio 0.65; 95% CI 0.50–0.85; P = 0.002). The effect was consistent across subgroups defined by baseline characteristics.

---

### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.

**Before:**
> This groundbreaking study showcases the profound impact of empagliflozin in patients with type 2 diabetes and high cardiovascular risk, reflecting a renewed commitment to improving cardiovascular care. When added to standard of care, empagliflozin delivered remarkable, dramatic reductions in heart failure hospitalization and cardiovascular death, positioning it as a leading therapeutic option.

**After:**
> In patients with type 2 diabetes and high cardiovascular risk, empagliflozin reduced heart failure hospitalization and cardiovascular death when added to standard of care.

---

### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.

**IMPORTANT EXCEPTION:** Phrases like "Prior studies have shown that...", "Previous research has demonstrated...", or "Several studies have reported..." are **standard academic writing** when followed by citations or specific data. Do NOT flag these as AI patterns. Only flag attributions that are genuinely vague and unsupported.

**Before:**
> Studies have shown that SGLT2 inhibitors reduce cardiovascular events. Experts argue that these benefits may be related to hemodynamic effects. Several publications have cited the EMPA-REG OUTCOME trial, in which empagliflozin reduced cardiovascular death by 38% and hospitalization for heart failure by 35%.

**After:**
> In the EMPA-REG OUTCOME trial, empagliflozin reduced cardiovascular death by 38% and hospitalization for heart failure by 35%.

---

### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.

**Before:**
> Despite its rigorous methodology, this trial faces several challenges typical of large clinical studies, including a diagnosis of heart failure at baseline that was based solely on investigator report, with no measures of cardiac function or biomarkers. Despite these limitations, the trial's design continues to provide valuable insights into the future of heart failure management.

**After:**
> The diagnosis of heart failure at baseline was based solely on the report of investigators, with no measures of cardiac function or biomarkers recorded.

---

## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI Vocabulary" Words

**High-frequency AI words:** align with, comprehensive (abstract use, e.g. "comprehensive analysis" with no specifics — keep when describing a concrete method/assessment), crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), holistic, interplay, intricate/intricacies, key (adjective), landscape (abstract noun), multifaceted, pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Problem:** These words appear far more frequently in post-2023 text. They often co-occur.

**EXCEPTION — "Additionally":** "Additionally" is NOT on the blacklist. Well-written, human-authored epidemiology papers use it (for example, to open a sentence in a strengths paragraph: "Additionally, the study used a validated and widely used measure of the exposure."). **Keep up to one "Additionally" per paragraph.** Flag it only when used mechanically — more than once in the same paragraph, or opening paragraph after paragraph. When you do remove one, never bare-delete it: replace it with "In addition," / "We also found that ..." / "Moreover," or restructure the sentence (see Pattern 30).

**Before:**
> Additionally, empagliflozin reduced the risk of hospitalization for heart failure or cardiovascular death by 34%, a pivotal finding in the evolving therapeutic landscape. Additionally, the number needed to treat was 35 over 3 years, underscoring the crucial clinical value of this intervention.

**After:**
> Additionally, empagliflozin reduced the risk of hospitalization for heart failure or cardiovascular death by 34%. The number needed to treat to prevent one event was 35 over 3 years.

---

### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for simple copulas.

**Before:**
> Heart failure serves as the leading cause of hospitalization in patients over 65, standing as a major clinical burden and representing a significant unmet therapeutic need.

**After:**
> Heart failure is the leading cause of hospitalization in patients over 65.

---

### 9. Negative Parallelisms

**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused.

**Before:**
> SGLT2 inhibitors not only lower blood glucose but also reduce cardiovascular events. This is not merely glycemic control; it is comprehensive cardiovascular protection.

**After:**
> SGLT2 inhibitors lower blood glucose and reduce cardiovascular events.

---

### 10. Rule of Three Overuse

**Problem:** LLMs force ideas into groups of three to appear comprehensive.

**Before:**
> SGLT2 inhibitors lower glucose, reduce cardiovascular events, and slow kidney disease progression. These agents offer efficacy, safety, and tolerability. Benefits span metabolic, cardiovascular, and renal domains.

**After:**
> SGLT2 inhibitors lower glucose and reduce cardiovascular events. They also slow kidney disease progression.

---

### 11. Elegant Variation (Synonym Cycling) and Term Consistency

**Problem:** AI has repetition-penalty code causing excessive synonym substitution. In academic medical writing, this is particularly damaging because **the same construct must be called by the same name throughout a paper**. Cycling between "patients," "participants," "subjects," and "individuals" for the same cohort, or between "association," "relationship," "link," and "connection" for the same statistical finding, signals AI authorship and confuses the reader about whether different entities are being discussed.

**Rule:** Pick one term for each concept and use it consistently. Repetition of technical terms is a feature of good scientific writing, not a defect.

**Before:**
> Patients in the empagliflozin group had lower rates of hospitalization for heart failure (2.7% vs. 4.1%). Participants also demonstrated reduced cardiovascular mortality (3.7% vs. 5.9%). Subjects experienced decreased all-cause death rates (5.7% vs. 8.3%).

**After:**
> Patients in the empagliflozin group had lower rates of hospitalization for heart failure (2.7% vs. 4.1%), cardiovascular death (3.7% vs. 5.9%), and all-cause mortality (5.7% vs. 8.3%).

---

### 12. False Ranges

**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**
> The benefits of SGLT2 inhibitors span from reduced hospitalization for heart failure to improved renal outcomes, from cardiac protection to modest reductions in HbA1c.

**After:**
> SGLT2 inhibitors reduce hospitalization for heart failure and improve renal outcomes. They also lower HbA1c modestly.

---

## STYLE PATTERNS

### 13. Em Dash Elimination

**Rule:** Replace every em dash (—) in the output, including ones that look natural or serve a standard parenthetical function.

**Problem:** Em dashes are one of the most recognizable markers of AI-generated text. LLMs insert them far more frequently than human writers, so even a single em dash can flag a document as potentially AI-written, and the author does not use them.

**Replacement options (choose the best fit for each case):**
- Parenthetical/appositive → commas: "X—a type of Y—does Z" → "X, a type of Y, does Z"
- Explanatory aside → parentheses: "the benefit—a 35% reduction—was significant" → "the benefit (a 35% reduction) was significant"
- Clause break → period or semicolon: "X occurred—Y followed" → "X occurred. Y followed"

**Before (multiple em dashes):**
> SGLT2 inhibitors—a relatively new drug class—have transformed heart failure treatment. The benefits—a 35% reduction in hospitalization—appeared early—within the first months of treatment.

**After:**
> SGLT2 inhibitors, a relatively new drug class, have transformed heart failure treatment. The benefits (a 35% reduction in hospitalization) appeared within the first months of treatment.

**Before (a single, natural-looking em dash, which is also replaced):**
> Among the subjective dimensions of sleep, the feeling of restfulness upon awakening—often termed restorative or refreshing sleep—is a particularly important clinical indicator.

**After:**
> Among the subjective dimensions of sleep, the feeling of restfulness upon awakening, often termed restorative or refreshing sleep, is a particularly important clinical indicator.

---

### 14. Title Case in Headings

**Problem:** AI chatbots capitalize all main words in headings.

**Before:**
> ## Statistical Analysis And Primary Endpoints

**After:**
> ## Statistical analysis and primary endpoints

---

### 15. Curly Quotation Marks

**Problem:** ChatGPT uses curly quotes (“...”) instead of straight quotes ("...").

**Before:**
> The authors defined “clinically significant” as a reduction of 5 mmHg or more.

**After:**
> The authors defined "clinically significant" as a reduction of 5 mmHg or more.

---

## FILLER AND HEDGING

### 16. Filler Phrases

**Before → After:**
- "In order to assess efficacy" → "To assess efficacy"
- "Due to the fact that patients were excluded" → "Because patients were excluded"
- "At the present time" → "Currently" or omit
- "It is important to note that mortality was reduced" → "Mortality was reduced"
- "The study has the ability to detect" → "The study can detect"
- "With respect to safety endpoints" → "For safety endpoints"
- "in terms of sleep quality" → "with respect to sleep quality"

**EXCEPTION:** Single-word academic transitions ("Notably,", "Importantly,", "Interestingly,") are standard in research papers and should NOT be removed. Only flag them when stacked excessively (e.g., three in one paragraph).

---

### 17. Redundant Multi-layered Hedging

**Problem:** LLMs stack multiple hedging devices in a single sentence ("may suggest", "have the potential to", "beneficial effects", "in select populations"), creating vague, non-committal prose. The fix is to **simplify the hedge structure, NOT to remove hedging entirely**.

**Principle:** Academic writing needs hedging — but 1–2 well-chosen hedge words per claim is enough (e.g., "may reduce" or "may help reduce"). Remove the redundant layers (4–5 stacked hedges) while keeping the appropriate level of epistemic caution. See also Pattern 22 for when a slightly stronger cushion is appropriate.

**Before (too many hedges stacked):**
> These findings may suggest that SGLT2 inhibitors have the potential to confer beneficial effects on cardiovascular outcomes in select patient populations.

**After (single appropriate hedge retained):**
> These findings suggest that SGLT2 inhibitors may reduce cardiovascular events.

**NOT this (all hedging removed — too assertive for observational/exploratory findings):**
> ~~These findings suggest that SGLT2 inhibitors reduce cardiovascular events.~~

**Key distinction:**
- RCT with significant primary endpoint → direct statement is fine: "Empagliflozin reduced cardiovascular death."
- Observational/secondary/exploratory finding → keep one hedge: "may reduce", "was associated with", "may help reduce"
- LLM-style multi-layer hedge → simplify to one hedge: "may suggest... have the potential to confer beneficial effects" → "suggest... may reduce"

---

### 18. Generic Positive Conclusions

**Problem:** Vague upbeat endings.

**Before:**
> Empagliflozin reduced heart failure hospitalization and cardiovascular death when added to standard care, with a benefit that was consistent in patients with and without heart failure at baseline, representing a major step in the right direction for cardiovascular medicine. The future looks bright for patients with type 2 diabetes as these exciting findings continue to reshape clinical practice.

**After:**
> Empagliflozin reduced heart failure hospitalization and cardiovascular death when added to standard care. The benefit was consistent in patients with and without heart failure at baseline.

---

## LLM-SPECIFIC WORD CHOICE PATTERNS

### 19. Informal "linked to" Instead of Academic "associated with"

**Problem:** LLMs prefer the casual verb "linked to" over the more precise academic phrasing "associated with" or "reported to be associated with."

**Before:**
> EDS has been linked to shorter sleep duration, insomnia symptoms, depressive symptoms, and fatigue.

**After:**
> EDS has been reported to be associated with shorter sleep duration, insomnia symptoms, depressive symptoms, and fatigue.

**IMPORTANT — do NOT blanket-swap every "link" to "associated with".** Choose the verb that fits the context:
- **Noun "link"** (e.g., "the link between vulnerability and distress") — leave unchanged.
- **Data linkage** — use "merge"/"combine": "successfully linked with T2 data" → "successfully merged with T2 data".
- **Downstream consequence** ("leads to / results in") — use "lead to": "has been linked to reduced productivity" → "can lead to reduced productivity".
- **Reframe the whole clause** when more natural: "has been linked to reductions in patient experience and continuity of care" → "can compromise patient experience and continuity of care".

Use "associated with" only when the relationship is genuinely a statistical/observational association.

---

### 20. Overuse of "Beyond" as a Transition

**Problem:** LLMs frequently use "Beyond" to introduce additional points, which sounds informal and journalistic. In academic writing, "In addition to" is more standard.

**Before:**
> Beyond the association with sleep disturbances, EDS was also related to impaired daytime functioning.

**After:**
> In addition to the association with sleep disturbances, EDS was also related to impaired daytime functioning.

---

### 21. Overuse of "via" Instead of "through"

**Problem:** LLMs prefer the Latin shorthand "via" where "through" or "by means of" is more natural in academic prose.

**Before:**
> Informed consent was obtained via the online form.

**After:**
> Informed consent was obtained through an online form.

---

### 22. Overly Assertive Causal Claims (Insufficient Hedging)

**Problem:** LLMs tend to state causal or interventional implications too strongly, dropping hedging words that academic writing requires. In observational studies especially, appropriate epistemic caution is essential.

**Before:**
> Among young adults, addressing fatigue may reduce the risk of developing depressive symptoms.

**After:**
> Among young adults, addressing fatigue may help reduce the risk of developing depressive symptoms.

**Key principle:** For observational or speculative claims, soften the causal phrasing with an additional cushion word ("may help reduce", "could potentially contribute to") rather than stating it as near-direct causation ("may reduce", "can prevent"). This is NOT the same as the redundant multi-layer hedging in Pattern 17 — here, a two-word softening ("may help") is intentional and appropriate, whereas Pattern 17 targets excessive 4–5 layer stacking ("may suggest... have the potential to confer beneficial effects").

---

### 23. Artificially Condensed Expressions

**Problem:** LLMs compress complex ideas into unnaturally compact forms — either by packing nouns into dash-compounds or by substituting abstract shorthand for concrete explanations. Academic writing should be expanded and readable.

**Type A — Compressed noun-dash phrases:**

**Before:**
> a reinforcing fatigue–sleepiness cycle

**After:**
> a reinforcing cycle of fatigue and sleepiness

**Before:**
> the sleep–mood–cognition pathway

**After:**
> the pathway linking sleep, mood, and cognition

**Type B — Abstract shorthand without elaboration:**

**Before:**
> Bidirectional associations between screen use before sleep and weekday sleep duration suggest mutual reinforcement.

**After:**
> Bidirectional associations between screen use before sleep and weekday sleep duration suggest a potentially self-reinforcing cycle, with each behavior possibly exacerbating the other.

**Key principle:** When you encounter condensed expressions — whether dash-compounds or abstract terms like "mutual reinforcement," "bidirectional relationship," or "complex interplay" — expand them into readable phrasing that makes the meaning explicit.

---

### 24. Avoid "where" as a Non-locative Connector

**Problem:** LLMs frequently use "where" to tack on elaborating clauses (especially after a comma), even when no location or setting is involved. In academic medical writing, this reads as awkward and informal. Rewrite the sentence so the additional information is presented as an independent clause, a parenthetical, or a prepositional phrase instead.

**Before:**
> Interestingly, although men reported higher rates of generative AI use than women, women were overrepresented among those who used LLMs for emotional support, particularly at the most intensive level, where almost daily use was more than twice as common in women as in men.

**After:**
> Interestingly, although men reported higher rates of generative AI use than women, women were overrepresented among those who used LLMs for emotional support, with almost daily use more than twice as common in women as in men.

**Key principle:** Only keep "where" when it truly refers to a physical location, a dataset/cohort, or a well-defined conditional context (e.g., "in trials where blinding was not feasible"). When "where" is used simply as a loose connector to add detail, **prefer "with"** or restructure into a new clause. Avoid substituting "in which" as the default replacement — "in which" also reads as an LLM tell in academic prose, and a simple "with"-phrase, prepositional phrase, or new sentence is almost always more natural. Reserve "in which" for cases where no other construction works.

---

### 25. Avoid "yield" as a Result Verb

**Problem:** LLMs overuse "yield" (e.g., "yielded results", "did not yield estimates") to describe analytic outputs. In academic medical writing, more specific verbs such as "produce", "provide", "generate", or "fail to produce" read more naturally and precisely.

**Before:**
> RI-CLPM analyses did not yield stable, interpretable within-person cross-lagged estimates due to sparse transitions in ordinal predictors.

**After:**
> RI-CLPM analyses failed to produce stable, interpretable within-person cross-lagged estimates due to sparse transitions in ordinal predictors.

**Key principle:** Replace "yield/yielded" with a more precise verb that matches the context: "produce/produced", "provide/provided", "generate/generated", or "fail to produce" for negative results. Reserve "yield" for contexts where it is genuinely standard (e.g., chemical/biochemical yields).

---

### 26. Minor word-choice refinements (remain, given)

**"remain" → a be-verb** (more natural in most contexts):
- Before: However, these interpretations remain speculative.
- After: However, these interpretations are still speculative.

**"Given" → "due to"** when it introduces a reason:
- Before: ...are still speculative given the small sizes of the subgroup samples.
- After: ...are still speculative due to the small sizes of the subgroup samples.

---

### 27. Preserve logical discourse markers (do NOT over-trim connectives)

**Problem:** Aggressive AI-pattern removal can strip the connectives that carry a paper's logic, leaving choppy, hard-to-read prose. This is a common failure mode of automated humanizing. Logical discourse markers are NOT AI tells; they are hallmarks of good human academic writing, and removing them is itself a defect.

**Preserve (do not delete):** Although / Whereas / Thus / Hence / Thereafter / In contrast / Conversely / Based on these results / To that end / As expected / In agreement with previous reports / Over and above. A measured "not only ... but also ..." (about once per paragraph) is also natural and should be kept — this refines Pattern 9, which targets only its *overuse*, not a single natural instance.

**Distinguishing rule:** ask whether the phrase *inflates meaning* (delete) or *makes logic explicit* (keep).
- "underscores the pivotal importance of ..." → inflates meaning → delete (Patterns 1, 7).
- "Based on these results, we examined ..." → makes logic explicit → keep.

**Benchmark — the "sweet spot":** Well-written, pre-AI human papers chain discourse markers densely and naturally ("Based on these initial observations ... To that end ... As expected ... In agreement with previous reports ... Over and above the impact of [the main exposure] ...") while using ZERO inflated AI vocabulary. Aim for that profile: trim inflated vocabulary and significance puffery, but keep the logical connectives that make the argument easy to follow.

**Vary connectives by logical relation — but only to avoid near repetition, never for decoration.** When you add or rewrite a connective (per Pattern 30), first identify the logical relation the sentence actually needs, then choose a marker that fits it. If the same marker was just used nearby, substitute another from the *same* relation group so the prose does not repeat mechanically. Common groups:
- **Result / consequence:** thus, hence, therefore, consequently, accordingly
- **Addition:** moreover, furthermore, in addition (and "additionally" once per paragraph, per Pattern 7)
- **Contrast:** however, in contrast, conversely, on the other hand
- **Concession:** although, albeit, nonetheless, nevertheless, even though
- **Reason / grounds:** because, since, as, given that
- **Sequence / enumeration:** first / second, to begin with

**Guardrail (this is NOT an exception to Pattern 11):** vary connectives only when the relation is genuinely present and a near-repeat would otherwise occur. Do NOT sprinkle uncommon connectives (albeit, thereby, whereby, heretofore) to "sound human" — that is decoration, and it reads as artificial. Each connective must be earned by the logic of the sentence. Skilled human writers reach for "thus", "hence", "moreover", or "albeit" because the relation calls for it, not to diversify their vocabulary.

---

### 28. Re-contextualize over-condensed semantic links

**Problem:** LLMs compress a relation into an over-direct phrasing. Expand it into natural, contextualized wording.

- Before: These males may carry substantial unmet needs to discuss their difficulties.
- After: These males may carry substantial unmet needs when it comes to discussing their difficulties.

(See also Pattern 23 on artificially condensed expressions; Pattern 28 specifically targets over-direct *semantic* links rather than noun-dash compounds.)

---

### 29. Ornamental -ly intensifier adverbs

**Problem:** LLMs dress up sentences with -ly intensifiers that add emphasis but no information ("markedly reduced", "critically important", "remarkably consistent"). Human-written epidemiology papers use -ly adverbs almost exclusively *functionally*: to convey magnitude, frequency, direction, or calibration.

**Words to watch (ornamental — delete or downgrade):** markedly, remarkably, strikingly, dramatically, profoundly, critically, fundamentally, notably (as a mid-sentence adverb, e.g. "a notably higher rate"), significantly (with no statistical test behind it), increasingly, rapidly (figurative), uniquely, vastly, deeply, exceptionally, substantially (with no quantitative backing)

**Functional adverbs to KEEP (these carry information):** approximately, slightly, modestly, consistently, almost, only, largely, generally, relatively, "statistically significantly" / "differed significantly" (when an actual test result is being reported), substantially (when it refers to a real, stated effect-size difference)

**Decision rule:** Delete the adverb mentally and ask whether any information was lost. If nothing was lost, it was ornamental — delete it or replace the emphasis with the concrete number or comparison it was gesturing at. If it conveyed magnitude, frequency, direction, or calibration, it is functional — keep it.

**Before:**
> Patients with both conditions face a markedly reduced median survival of approximately 4 years, and poor adherence critically worsens prognosis. The effect was remarkably consistent across subgroups, and the prevalence of heart failure in this population is increasingly rising.

**After:**
> Patients with both conditions have a median survival of approximately 4 years, and poor adherence worsens prognosis. The effect was consistent across subgroups, and the prevalence of heart failure in this population is rising.

**Benchmark — how well-written human papers use -ly adverbs:** In strong epidemiology writing, the -ly adverbs almost always quantify or calibrate rather than decorate. Typical examples read like "the highest-exposure group consistently had lower mortality risk", "the exposure slightly decreases along the gradient", or "the study showed a modest association between the exposure and better self-rated health". Each adverb ("consistently", "slightly", "modest") carries information about frequency, magnitude, or calibration; none merely decorates. Aim for that profile.

(Note: Pattern 1's example "markedly reduced median survival" is the same defect viewed as significance inflation; Pattern 29 generalizes it to all ornamental intensifiers.)

---

### 30. Connective-preserving edits (never bare-delete a transition)

**Problem:** When an AI-pattern sentence opener is removed (an "Additionally," beyond the once-per-paragraph allowance, an "-ing" tail per Pattern 3, significance inflation per Pattern 1), the logical relation it marked — addition, contrast, consequence — still exists between the sentences. Deleting the marker without replacing it produces bare, disconnected sentences (asyndeton). **Choppy, connective-stripped prose is itself a tell of automated AI cleanup**, and a known failure mode of humanizing passes.

**Rule: edit, don't excise.** Whenever you remove a sentence-initial transition or a clause that carried the link to the previous sentence, restore the link by one of:
1. Substituting a natural connective: "In addition," / "Moreover," / "However," / "By contrast," / "We also found that ..."
2. Echoing a key noun from the previous sentence at the start of the new sentence (old-to-new information flow): "... was associated with nonrestorative sleep. Nonrestorative sleep, in turn, ..."
3. Restructuring the two sentences into one with an explicit conjunction.

**Before (the AI text):**
> Additionally, empagliflozin reduced cardiovascular death, highlighting its cardioprotective effects. Additionally, the benefit appeared within months of treatment initiation.

**Wrong fix (bare deletion — creates choppy asyndeton):**
> Empagliflozin reduced cardiovascular death. The benefit appeared within months of treatment initiation.

**Right fix (connective preserved):**
> Empagliflozin also reduced cardiovascular death, and this benefit appeared within months of treatment initiation.

**Division of labor with Pattern 27:** Pattern 27 lists the discourse markers you must not *remove*; Pattern 30 governs what you must do when an edit *would otherwise leave a gap* — replace or restructure, never just cut.

---

### 31. Paragraph cohesion (old-to-new flow and paragraph-opening markers)

**Problem:** Sentence-level edits accumulate into paragraph-level damage: topic sentences get blunted, the chain from one sentence to the next breaks, and the contrast/continuity markers that tie paragraphs together disappear. Well-written human papers are tightly chained.

**What well-written human papers do:**
- **Within a paragraph**, each sentence picks up a key word from the previous one (old-to-new flow), e.g. "the exposure was associated with a higher functional score. The functional index used here consists of ... To perform these activities, ...". The repeated key term ("functional") chains the sentences so the reader is never dropped.
- **Between paragraphs**, the opening sentence names what the paragraph is about and, where the logic requires it, carries an explicit marker: "However, ...", "On the other hand, ...", "In addition to the differential effects described above, it is worth noting that ...", or "Taken together, the results suggest ...".

**Checklist (apply to every paragraph after editing):**
1. Does the first sentence state what the paragraph claims or covers?
2. From the second sentence on, is each sentence linked to the previous one by either a connective or an echoed key word? If a link was broken by an edit, restore it (Pattern 30).
3. Across paragraphs, are the contrast/continuity openers (However / In contrast / On the other hand / Overall / Taken together / In addition to X) still present where the argument needs them? Add one if a paragraph now starts abruptly.

---

### 32. Paraphrastic Repetition of the Same Claim

**Problem:** LLMs restate the same claim 2–3 times using different words within the same paragraph or across adjacent sentences, often joined by "In other words," "That is," "Put differently," or "Essentially,". Each sentence should advance the argument, not rephrase the previous one.

**Words to watch:** In other words, That is, Put differently, Essentially, To put it another way, Simply put, This means that (when followed by a near-verbatim restatement)

**Before:**
> These findings suggest that sleep disturbance is associated with depressive symptoms. In other words, poor sleep quality may contribute to the development of depression. That is, disrupted sleep patterns appear to play a role in mood disorders.

**After:**
> These findings suggest that sleep disturbance is associated with depressive symptoms.

**Before:**
> Empagliflozin reduced the risk of cardiovascular death. Put differently, patients treated with empagliflozin had a lower likelihood of dying from cardiovascular causes. Essentially, the drug conferred a survival benefit.

**After:**
> Empagliflozin reduced the risk of cardiovascular death.

**Key principle:** State each claim once. If a second sentence follows, it should add new information (a mechanism, a comparison, a qualification), not repackage the same assertion in different vocabulary. When removing paraphrastic repetitions, keep the version that is most specific or most precisely worded and delete the rest. Apply Pattern 30 (connective-preserving edits) if deletion would break the logical flow to the next sentence.

**EXCEPTION:** Genuine clarification of a technical term is not paraphrastic repetition. "The hazard ratio was 0.65, meaning that empagliflozin reduced the event rate by 35% relative to placebo" adds information by translating a statistical metric into a clinical interpretation. The problem is when the "clarification" says the same thing in equally vague terms.

---

### 33. Content-free Evaluation Sentences

**Problem:** LLMs insert standalone sentences that evaluate a finding's importance without adding any information — no data, no mechanism, no comparison, just a verdict of significance. These are distinct from Pattern 1 (significance inflation embedded within data-bearing sentences) and Pattern 3 (-ing tails appended to factual sentences); Pattern 33 targets freestanding evaluation sentences that contain nothing but the evaluation itself.

**Words to watch:** This is an important/significant/noteworthy finding. These results are of clinical/public health significance. This observation is clinically relevant. This finding has important implications. This is a meaningful/notable result. This deserves attention.

**Before:**
> Empagliflozin reduced cardiovascular death by 38%. This is a noteworthy finding. The benefit was consistent across subgroups. This observation is of clinical significance.

**After:**
> Empagliflozin reduced cardiovascular death by 38%, and the benefit was consistent across subgroups.

**Key principle:** If the finding is genuinely significant, show why: state the mechanism, the clinical consequence, or the contrast with prior evidence. A sentence that merely labels a finding as "important" without explaining what makes it important adds no information and should be deleted. When deleting, apply Pattern 30 (connective-preserving edits) to maintain flow.

**EXCEPTION:** An evaluation sentence is acceptable when it immediately follows up with a specific reason: "This finding is clinically relevant because it identifies patients who may benefit from earlier intervention." Here, the evaluation carries forward into a concrete implication. The standalone, terminal evaluation ("This is important." Full stop.) is the problem.

---

### 34. Sentence Rhythm and Structural Diversity (Burstiness), in the service of clarity

**Burstiness is required, but never at the cost of clarity.** Experimental testing (desklib logit 5.54→2.47, a 55% reduction) showed that restructuring sentence rhythm accounts for ~90% of the achievable reduction in AI-detection scores. AI-generated text converges on a narrow band of sentence lengths (typically 15-25 words) with uniform Subject-Verb-Object openings; human writing mixes short and long sentences with varied openings. Every paragraph of three or more sentences must show this variation (see the Benchmark below for the criterion). Obtain it only through edits that keep actors, comparisons, conditions, and logical links explicit (see Reader clarity before compression).

**What to change (structure only, not vocabulary):**
1. **Split sentences that stack conditions or comparisons.** A sentence that makes readers hold several conditions in memory is both a clarity defect and a source of long-sentence uniformity. Split it so each sentence carries one comparison or condition.
2. **Combine adjacent supporting sentences** (not claim sentences) when they share a logical relation, using a conjunction or a semicolon that names that relation. This is a characteristic of the author's style.
3. **Diversify sentence openings.** If three consecutive sentences start with a noun-phrase subject, restructure one to open with a prepositional phrase ("In this meta-analysis,"), a subordinate clause ("Although the sample was small,"), or a connective ("However,").
4. **Relocate clause elements.** Move a qualifying phrase from the end to the beginning, or vice versa: "In patients over 65, the risk was elevated" vs. "The risk was elevated in patients over 65."

**What NOT to change:**
- Do not merge an existing short sentence that states a claim outright ("The largest difference was cost.") into its neighbor; see Voice Calibration. Such sentences already supply the short end of the rhythm. Obtain the remaining variation from the supporting sentences around them
- Do not introduce staccato drama (multiple new very short sentences in a row for rhetorical effect)
- Do not merge sentences in a way that hides which comparison or condition applies to which result
- Do not alter technical vocabulary, data, or the author's approved strength of interpretation
- Do not break the connective structure (Pattern 27/30/31 still apply)
- Do not change the voice (active/passive) of the original unless this is needed to make the actor explicit (see Reader clarity before compression)

**Interaction with Pattern 29 (ornamental adverbs):** Deleting an adverb like "markedly" was experimentally shown to INCREASE AI-detection scores (logit +0.72 worse) when it left a shorter sentence that fit the uniform cadence. After removing ornamental adverbs, re-check the paragraph's rhythm; if it has become uniform, restructure one of the supporting sentences.

**Before (uniform rhythm: 16, 15, 14, 13 words):**
> All three DACS had elevated PRRs for pantry overflow compared with comparator services (PRR <= 2.07). PRRs for bean hoarding were markedly higher for DACS (MorningHarbor 77.89, CopperKettle 3.92, DailyGrind 3.24). Four of eight comparator services had no bean hoarding reports whatsoever in the database. The remaining four comparator services, by contrast, had PRRs that were below one.

**After (more varied rhythm: 16, 12, 18 words):**
> All three DACS had elevated PRRs for pantry overflow compared with comparator services (PRR <= 2.07). PRRs for bean hoarding were higher (MorningHarbor 77.89, CopperKettle 3.92, DailyGrind 3.24). Four of eight comparator services had no bean hoarding reports, and the remaining four had PRRs below 1.

**Benchmark:** In well-written human medical papers, sentence lengths within a single paragraph typically range from about 10 to 55 words, with standard deviations of 10-15 words; the author's short claim sentences may be shorter. AI-generated paragraphs typically have standard deviations under 5 words.

**Criterion (used in the self-audit and the final rhythm check):** A paragraph of three or more sentences is too uniform if all of its sentences fall within a 5-word range of each other. Restructure it until at least one sentence is notably shorter and one notably longer than the paragraph average.

**Clarity example** (illustrative, not research evidence). Splitting a compressed sentence often adds rhythm and clarity together:
- Dense: `Using matched samples from both settings and adjusted models, exposure predicted higher mortality in both settings despite attenuation.`
- Clearer: `We compared matched samples from both settings. The association between exposure and mortality was weaker after adjustment but remained present in both settings.`

Name the actual exposure and adjustment variables where needed for the argument. Do not invent them to complete an ambiguous sentence. See [reader clarity](references/reader-clarity.md) for the full audit.

---

## Process (Two-Pass Draft-Audit)

### Pass 1: Draft rewrite

1. Read the input text carefully.
2. **Audit meaning and information priority first.** Identify unclear referents, omitted comparisons, stacked conditions, and redundant summary sentences using references/reader-clarity.md. Restore necessary relations without inventing facts.
3. **Restructure sentence rhythm (Pattern 34).** Before touching vocabulary, vary sentence lengths and diversify sentence openings across each paragraph. Keep the author's short claim sentences short; take the variation from the supporting sentences.
4. Identify and fix all vocabulary/phrase-level patterns (Patterns 1-33). After removing a transition or linking clause, check whether the logical relationship remains clear. Add a link only when needed; do not replace redundant summaries with generic bridge sentences. After removing ornamental adverbs (Pattern 29), re-check that the paragraph's rhythm has not become uniform.
5. Ensure the draft:
   - Sounds natural when read in an academic context
   - Matches the author's voice profile (Voice Calibration section)
   - Uses precise, specific language with consistent terminology (Pattern 11)
   - Maintains data integrity (numbers, statistics, findings)
   - Uses simple constructions (is/are/has) where appropriate
   - Avoids promotional or inflated language

### Pass 2: Self-audit

6. **Ask yourself: "What makes this draft still look AI-generated?"** List any remaining tells briefly. Common survivors include:
   - Omitted comparison conditions or ambiguous pronouns that force readers to reconstruct meaning
   - Sentence lengths still too uniform (check the Pattern 34 criterion: in paragraphs of three or more sentences, do all sentences fall within a 5-word range?)
   - Sentence openings still repetitive (check: do three+ consecutive sentences start the same way?)
   - Vocabulary tells that slipped through (check Patterns 1, 7, 29 word lists)
   - Broken connective chain (check Pattern 31 checklist)
7. Fix every issue found in the self-audit.

### Mandatory final checks

8. **FIDELITY CHECK:** Compare the output with the input and any author-supplied sources. Every number, unit, statistic, date, named entity (trial, drug, cohort, instrument, author), and citation in the output must also appear in the input or in those sources, and every assertion must be grounded in the input. If anything is not, revert that span to the input's wording or replace it with a `[DATA NEEDED: ...]` placeholder. Do not rewrite around the problem.
9. **EM DASH CHECK:** Search your output for "—". If ANY remain, replace them. Zero em dashes allowed.
10. **PARAGRAPH COHESION CHECK (Pattern 31):** Re-read every paragraph top to bottom: (a) first sentence states the paragraph's claim; (b) every subsequent sentence is linked to the previous one by a connective or echoed key word; (c) paragraph-opening contrast/continuity markers survive where the argument needs them. If any link was broken, repair it. Choppy, disconnected prose is NOT acceptable humanized output.
11. **RHYTHM AND READABILITY CHECK (Pattern 34):** This check is mandatory. (a) Apply the Pattern 34 criterion to every paragraph of three or more sentences. If all sentences fall within a 5-word range of each other, restructure at least one supporting sentence (split a sentence that stacks conditions, combine related supporting sentences, or reposition clauses). Never merge a short claim sentence to do this. (b) Re-read for one-pass comprehension: no restructuring may hide an actor, comparison, or condition. Remove redundant summaries; preserve concrete interpretation, necessary qualifications, and approved author opinions.
12. Present the humanized version.

## Output Format

Provide:
1. The rewritten text
2. A brief summary of changes made, noting which patterns were applied and any rhythm restructuring performed
3. Fidelity check result: confirm that every number, statistic, named entity, and citation in the output appears in the input or in author-supplied sources, and name any span you reverted
4. A list of every `[DATA NEEDED: ...]` placeholder inserted, so the author can fill each one
5. If any: "Candidate data for the author (unverified, not inserted)", listing figures or references you recalled that might fill a placeholder or support a vague claim. The author must verify each one against the primary source before using it

---

## Full Example

**Before (AI-sounding):**
> Heart failure represents a pivotal challenge in the evolving landscape of diabetes care, affecting more than one in five patients with type 2 diabetes aged over 65 years and underscoring the critical importance of addressing cardiovascular comorbidities. This groundbreaking study showcases the profound impact of empagliflozin, a pivotal therapeutic option that serves as a cornerstone of modern cardiovascular medicine: when added to standard of care in patients with type 2 diabetes and high cardiovascular risk, it reduced heart failure hospitalization and cardiovascular death.
>
> Studies have shown that SGLT2 inhibitors reduce cardiovascular events. Additionally, in the EMPA-REG OUTCOME trial, empagliflozin reduced the risk of hospitalization for heart failure or cardiovascular death by 34%—a remarkable finding—highlighting the cardioprotective effects of this intervention. The number needed to treat of 35 over 3 years to prevent one event underscores the crucial clinical value of this therapeutic approach.
>
> Despite challenges typical of large clinical trials, including a diagnosis of heart failure at baseline that relied solely on investigator report without measures of cardiac function or biomarkers, the trial's strategic design continues to provide valuable insights for the future outlook of heart failure management. With a benefit that was consistent in patients with and without heart failure at baseline, the future looks bright for patients with type 2 diabetes as these exciting findings continue to reshape clinical practice.

**After (Humanized):**
> Heart failure is highly prevalent in patients with diabetes, occurring in more than one in five patients with type 2 diabetes aged over 65 years. In patients with type 2 diabetes and high cardiovascular risk, empagliflozin reduced heart failure hospitalization and cardiovascular death when added to standard of care.
>
> In the EMPA-REG OUTCOME trial, empagliflozin reduced the risk of hospitalization for heart failure or cardiovascular death by 34%. The number needed to treat to prevent one event was 35 over 3 years.
>
> The diagnosis of heart failure at baseline was based solely on the report of investigators, with no measures of cardiac function or biomarkers recorded. Empagliflozin reduced heart failure hospitalization and cardiovascular death when added to standard care. The benefit was consistent in patients with and without heart failure at baseline.

**Changes made:**
- Eliminated all em dashes ("—") per Pattern 13
- Removed significance inflation ("pivotal challenge", "evolving landscape", "groundbreaking", "cornerstone")
- Removed promotional language ("profound impact", "remarkable finding", "exciting findings")
- Removed the unsupported vague attribution ("Studies have shown" with no citation) and let the specific trial result carry the claim (note: "Prior studies have shown that..." followed by citations would be preserved)
- Removed superficial -ing phrases ("underscoring", "highlighting")
- Removed copula avoidance ("serves as") in favor of "is"
- Removed AI vocabulary ("crucial", "pivotal") and ornamental intensifiers ("remarkable") — note that the "Additionally" disappeared only because its whole sentence was rewritten; a single "Additionally" per paragraph is acceptable and would otherwise be kept (Pattern 7 EXCEPTION)
- Removed formulaic challenges section ("Despite challenges... future outlook")
- Removed generic positive conclusion ("The future looks bright", "continue to reshape")
- Fixed grammar ("The number needed to treat of 35" → "was 35")
- Used simple sentence structures and specific data
- Split long sentences that stacked conditions (the baseline-diagnosis limitation now stands as its own long sentence, followed by two shorter ones)
- Fidelity check passed: every number, trial name, and statistic in the After appears in the Before, so no `[DATA NEEDED]` placeholders or candidate data were needed

---

## Reference

This skill is based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup, adapted for medical and academic writing contexts. The patterns documented there come from observations of thousands of instances of AI-generated text.

Medical paper examples are adapted from:

> Fitchett D, Inzucchi SE, Cannon CP, et al. Empagliflozin Reduced Mortality and Hospitalization for Heart Failure Across the Spectrum of Cardiovascular Risk in the EMPA-REG OUTCOME Trial. *Circulation*. 2019;139(11):1384-1395. doi:10.1161/CIRCULATIONAHA.118.037778

This article is published under CC-BY-4.0 license.
