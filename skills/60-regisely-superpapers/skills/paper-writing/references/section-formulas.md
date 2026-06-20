# Section Formulas

## Title

### Formulas

- Best form: "The Effect of [Treatment / Cause] on [Outcome]: Evidence from [Context]"
- Alternative: "[Treatment] and [Outcome]" (shorter, acceptable)
- For theory papers: name the key mechanism or insight, not the technique.
- For structural / counterfactual papers: "[Counterfactual Question]: Evidence from [Context]"
- Keep titles short. Shorter titles receive more citations.
- Do NOT emphasize methodology in the title unless you invented the method.

### Title Evaluation Criteria

When writing or reviewing a title, score on these dimensions:

1. **Clarity** — Can a non-specialist understand the topic in one reading?
2. **Specificity** — Are the treatment / cause and outcome / effect both named?
3. **Length** — Under 12 words is ideal; under 15 is acceptable.
4. **Memorability** — Would someone remember this title at a conference?
5. **No methodology** — Does it emphasize the finding, not the method?

### Examples

- Good (economics): "The Oregon Health Insurance Experiment: Evidence from the First Year"
- Good (medicine): "Lifetime Costs of Smoking: A Cohort Study from the Norwegian Population Register"
- Good (political science): "Pollution and Mortality: Evidence from the 1952 London Fog"
- Bad: "A Difference-in-Differences Analysis of Education Policy" (methodology, not finding)
- Bad: "On the Relationship Between Various Factors and Economic Outcomes" (says nothing)
- Bad: "Essays on Labor Economics" (acceptable for a dissertation, never for a paper)

---

## Abstract

### Formula

Write the abstract LAST, after the introduction is complete. Extract key sentences from the Hook, Research Question, and Findings paragraphs of your introduction, then polish.

### Structure (100–150 words)

1. **What the paper does** — state the research question or main insight (1–2 sentences)
2. **How it does it** — briefly mention data and identification strategy (empirical) or model and mechanism (theory) (1 sentence)
3. **What it finds** — state the central, concrete finding or result (1–2 sentences)
4. **Why it matters** — brief implication (optional, if space permits)

### Rules

- Be CONCRETE. Say what you find, not what you look for.
- Do NOT mention other literature in the abstract. Exception: one prior finding to establish a puzzle is acceptable if brief.
- Do NOT use passive voice.
- Do NOT use jargon unnecessarily — make it intelligible to a smart college-educated non-specialist in your field.
- Do NOT exceed 150 words. Some journals (finance, JEL articles) require 100 words.
- For empirical papers: include your identification strategy keyword (DiD, IV, RDD, RCT, cohort study, regression discontinuity, etc.).
- For theory papers: name the mechanism or key force.
- For structural papers: state the key counterfactual result.

### Examples

- Good (economics): "Two easily measured variables, size and book-to-market equity, combine to capture the cross-sectional variation in average stock returns associated with market beta, size, leverage, book-to-market equity, and earnings-price ratios."
- Good (medicine): "We estimate the effect of statin initiation on five-year all-cause mortality using a regression discontinuity design at the LDL-cholesterol prescribing threshold of 190 mg/dL in a national insurance database. Statin initiation reduces five-year mortality by 2.4 percentage points (95% CI: 1.6–3.2). Effects are concentrated in patients above age 65."
- Bad: "We analyze data on executive compensation and find many interesting results."

---

## Introduction

The introduction determines a large share of whether a paper is accepted or rejected. Write it first, rewrite it every time you work on the paper, expect to revise it dozens of times.

### The Introduction Formula

#### Paragraphs 1–2: THE HOOK

Attract reader interest by connecting to something important. Four hook strategies:

- **Y matters**: when Y rises or falls, people are hurt or helped.
- **Y is puzzling**: defies easy explanation or contradicts standard theory.
- **Y is controversial**: experts disagree about it.
- **Y is big or common**: large sector, widespread phenomenon, large affected population.

Start with a striking fact, a puzzle, or a bold claim grounded in data. Do NOT start with:

- Philosophy ("Researchers have long wondered…")
- Literature ("The literature has long been interested in…")
- Policy motivation ("Given the importance of X for society…")
- A cute quotation
- "The literature lacks a model of…" (for theory papers, start with the puzzle, not the literature gap)

All of these are throat-clearing. Start with your contribution.

#### Paragraph 3: THE RESEARCH QUESTION

State clearly what the paper does. A typical sentence:

> "This paper examines whether [X causes Y] using [method] and [data]."

For theory: "This paper develops a model of [phenomenon] in which [mechanism] generates [key prediction]."

The reader must understand what question will be answered by the end. Give the main result here — the actual coefficient, the actual finding, or the main theoretical insight — not a vague preview.

#### Paragraphs 4–6: MAIN RESULTS

State your key findings concretely. Top journals devote 25–30% of the introduction to results. Include:

- The central finding with magnitude and significance (empirical), or the main proposition and its intuition (theory).
- Key robustness results or extensions.
- Substantive (economic, clinical, political) significance — not just statistical significance.

#### Paragraphs 7–9: LITERATURE REVIEW & VALUE ADDED

This is where the literature review belongs — in the introduction, NOT as a separate section. It should occupy 20–30% of the introduction.

How to write it:

- It is a STORY, not an annotated bibliography. The narrative hinges on a "however" or "although" — here is what others have done, here is what remains incomplete, here is how this paper addresses it.
- Discuss only the 5–10 closest papers (closer to 5 is better).
- For each paper, explain what they did AND what limitation remains — do not just state their finding.
- Then describe approximately three contributions your paper makes:
  - Contribution to internal validity (better identification, cleaner design)
  - Contribution to external validity (new context, population, setting)
  - Methodological or theoretical contribution (new approach, data, model)
- Be generous in citations. You do not have to say everyone else was wrong. Do not insult prior authors.
- Spell out authors' full names. Never abbreviate ("FF" for Fama and French).
- Working papers are acceptable to cite but flag if key results are forthcoming or have changed.
- When citing published papers, prefer the journal version over the working paper version.

#### Final Paragraph: ROADMAP

Outline the paper's organization. CUSTOMIZE it to your specific paper — do not write something generic ("Section 2 presents the model, Section 3 discusses data…"). Mention specific landmarks: problems, solutions, key results. Keep it brief — readers are eager to get to the heart of the paper.

### Introduction Length

3–5 pages maximum. Applied papers should aim for 3 pages; theory and structural papers may need 4–5.

### Critical Mistakes to Avoid

1. **Burying the lead**: putting the main result on page 20 instead of page 1.
2. **Bait-and-switch**: promising something interesting but delivering something boring.
3. **Travelogue**: narrating your research journey instead of presenting the final product.
4. **Throat-clearing**: pages of motivation before stating what you do.
5. **Bland enumeration**: listing papers without telling a story ("Smith found X. Jones found Y.").
6. **No results in intro**: making readers wait until the results section for any findings.

---

## Methods / Empirical Strategy

This is where you describe the research design and estimation. Detailed narratives by design (RCT, DiD, IV, RDD, event study, ML/causal, structural, descriptive) live in `research-design-narratives.md`. The general structure below applies regardless of design.

### Structure

1. **Identify the design in plain English** before any equations.
2. **State the key identifying assumption** and defend it on substantive grounds (not just statistical).
3. **Specify the estimating equation** with notation defined immediately after.
4. **Describe inference**: clustering, robust standard errors, bootstrap, exact tests as appropriate.
5. **Address threats to validity** that the design implies (parallel trends for DiD, exclusion restriction for IV, manipulation for RDD, attrition and spillovers for RCTs, unmeasured confounding for observational designs, and so on).

### Rules

- Identification is the core of the Methods section. Devote a full paragraph to the identifying assumption and defend it substantively.
- For every coefficient you will report, describe what variation in the data identifies it.
- Define every variable on first appearance — do not make readers hunt through footnotes.
- If you use multiple specifications, designate one as primary and explain why.

---

## Data

### Structure

1. **Data source**: name the dataset, time period, geographic coverage, and unit of observation in the first sentence.
2. **Sample construction**: describe inclusion / exclusion criteria, merging procedures, and final sample size.
3. **Key variables**: define treatment, outcome, and control variables precisely. State how each is measured.
4. **Descriptive statistics**: present a summary statistics table (defer table production to `tables-and-figures`).
5. **Institutional / contextual background**: if the setting is unfamiliar, provide enough context for the reader to understand the identification strategy.

### Rules

- Answer every question a reader might have about the data BEFORE the reader asks it.
- Define every variable the first time it appears.
- Describe any data cleaning decisions that materially affect results (winsorizing, dropping outliers, exclusion windows).
- Address sample selection: who is in the sample, who is excluded, and why.
- For restricted-access data: describe how other researchers can access it.
- If using multiple datasets, describe the merge procedure and match rates.
- Do NOT bury important data limitations in footnotes — state them in the text.

### Descriptive Statistics Table Conventions

- Report N, mean, SD, min, max for key variables.
- Separate panels for treatment vs. control groups when applicable.
- Report balance tests in a separate column or table for RCTs and quasi-experiments.
- Define every variable in the table notes (not just in the text).
- Round to 2–3 meaningful decimal places.
- Defer to `tables-and-figures` for the LaTeX/booktabs implementation.

---

## Theory / Model Section (Theory and Structural Papers)

Skip if your paper is purely applied empirical with no formal model.

### Core Principles

- Start with an example. A good example is worth more than a theorem.
- Use the simplest model that generates the key insight. If a two-period model works, do not use infinite horizon.
- Every assumption should earn its place: explain which are essential to the result and which are simplifying.

### Structure

1. **Setup paragraph**: describe the environment, agents (or actors, or units), timing, and information structure in plain English BEFORE any math.
2. **Formal model**: present primitives, preferences, technology, constraints.
3. **Equilibrium definition**: state the solution concept clearly.
4. **Main results**: propositions with substantive intuition BEFORE the formal proof.
5. **Comparative statics**: discuss verbally first ("When X increases, Y falls because…"), then formally.
6. **Extensions**: relax key assumptions one at a time to show robustness.

### Writing Propositions and Proofs

- State each proposition in plain English, then formally.
- Provide intuition immediately after the proposition, before the proof.
- Proofs belong in the appendix UNLESS they illuminate the mechanism.
- For complex proofs, give a sketch in text and the full proof in appendix.
- Number only the propositions, lemmas, and corollaries you reference elsewhere.

### Writing Assumptions

- List assumptions explicitly and number them.
- For each: (a) the formal statement, (b) its content in plain English, (c) whether it is essential or simplifying.
- Discuss what happens when key assumptions are relaxed — this builds credibility.

### Equations in Text

- Number only equations you reference later.
- Always introduce an equation verbally before displaying it: "Firm i's profit is…" then the equation.
- Define every variable immediately after the equation, even if defined earlier.
- Do not display trivial equations that can be stated in words.
- Use consistent notation throughout: Latin for variables, Greek for parameters.

### Testable Predictions

- Generate testable predictions explicitly — even if you do not test them, state what data would be needed.
- For mixed theory-empirical papers: the empirical section should explicitly test the model's predictions. Map each regression to a specific proposition.

---

## Results

### Structure

1. **Main result first** — no warmup exercises.
2. **Most parsimonious to least parsimonious specifications** — show the result is not an artifact of one specification.
3. **Substantive magnitude**, not just statistical significance — translate coefficients into meaningful units (dollars, percentage points, standard deviations of the outcome, lives saved, vote shares).
4. **Heterogeneity** — pre-specified subgroups, AFTER the main result.
5. **Mechanisms** — test specific channels, do not speculate.
6. **Robustness** — see `robustness-checks` skill for the canonical set; in writing, summarize and refer to a robustness table or appendix.
7. **Limitations** — placed near the relevant analysis, not as a separate "limitations" subsection in the conclusion.

### Translating Coefficients

- Compare your effect size to: (a) the mean of the dependent variable, (b) the effect of a well-known intervention, or (c) a policy-relevant threshold.
  - Economics: "The effect equals 40% of the black-white test score gap."
  - Public health: "The reduction in infant mortality equals one-third of the decline observed after the 1995 vaccination rollout."
  - Political science: "The shift in vote share equals the average effect of an incumbency advantage in midterm elections."
- For elasticities, state whether they are at the mean, at the median, or arc elasticities.
- Back-of-envelope calculations are encouraged: "At the sample mean, this implies X additional dollars per household per year".

### Presenting Null Results

- A null result IS a result. Frame it as informative, not as failure.
- Distinguish "no effect" (precisely estimated zero) from "imprecisely estimated" (wide CI including zero and meaningful effects).
- Report confidence intervals alongside or instead of p-values: "we can rule out effects larger than X".
- Discuss statistical power: was the study powered to detect substantively meaningful effects?
- If pre-registered, emphasize that the null was not the result of specification searching.
- Relate to prior literature: does the null contradict or refine previous findings?

---

## Discussion

Often combined with Results in shorter papers; separate in medical and clinical journals.

### Structure

1. **Restate the main finding in substantive terms** (one short paragraph).
2. **Place the finding in the literature**: which prior debate does this resolve, refine, or complicate?
3. **Mechanisms**: what does the evidence say about why the effect appears?
4. **External validity**: what populations, settings, time periods does this generalize to?
5. **Limitations**: what does the design *not* identify? Avoid over-claiming.

### Rules

- Do not introduce new results in Discussion.
- Distinguish what the data show from what you speculate about.
- Limitations belong here when the journal expects them; otherwise place each limitation near the analysis it qualifies.

---

## Conclusion

### Formula

#### Part 1: SUMMARY (1–2 paragraphs)

Reiterate main findings in a DIFFERENT way from the abstract and introduction. Tell a story. Do not copy-paste earlier text. The conclusion, abstract, and introduction each state the same findings phrased differently.

#### Part 2: IMPLICATIONS (1 paragraph)

- Applied empirical: policy implications with rough cost-benefit assessment (back-of-the-envelope is fine). Identify winners and losers. Do NOT make claims unsupported by your results.
- Theory: broader applicability of the mechanism, relationship to other theoretical frameworks, what the model says about unresolved debates.
- Structural: what the counterfactuals imply for policy, welfare calculations.

#### Part 3: FUTURE RESEARCH (1 paragraph)

Identify 1–2 specific, concrete directions:

- Better identification strategies or richer data
- Broader external validity (new populations, settings)
- Extensions of the model or relaxation of key assumptions
- Follow-up questions raised by your findings

### Rules

- Keep it SHORT. One single-spaced page for a 20-page paper.
- Do NOT restate all findings verbatim. One statement in the abstract, one in the introduction, once more in the body is enough.
- Do NOT speculate beyond what the data or model show.
- Do NOT write your grant application here.
- Do NOT say "I leave X for future research" — describe concretely what the extension would look like.
- Do NOT add a separate "limitations" or "caveats" subsection in the conclusion. Limitations belong in the body, near the analysis they qualify. The conclusion should project confidence.
- For applied micro / policy-relevant empirical work, consider framing the conclusion like a policy brief.

---

## Paper Structures by Type

### Standard Applied Empirical Paper

1. Title
2. Abstract (100–150 words, concrete findings)
3. Introduction (3–5 pages, includes literature review)
4. Theoretical Framework (optional; only if it adds to understanding the empirics)
5. Data and Descriptive Statistics
6. Empirical Framework (estimation + identification strategy)
7. Results (main, robustness, mechanisms, limitations)
8. Conclusion (summary, implications, future research)
9. References
10. Appendix / Online Supplement

### Theory Paper

1. Title, 2. Abstract (state the main insight), 3. Introduction (motivate the puzzle, state the insight, describe the mechanism, relate to literature), 4. Model Setup, 5. Analysis / Main Results (propositions with intuition before proofs), 6. Extensions, 7. Discussion / Empirical Implications, 8. Conclusion, 9. References, 10. Appendix (proofs, technical details).

### Mixed Theory–Empirical Paper

1. Title, 2. Abstract (state both theoretical insight and empirical finding), 3. Introduction, 4. Model (derive testable predictions), 5. Data and Background, 6. Empirical Strategy (test the model's predictions), 7. Results (map back to propositions), 8. Conclusion, 9. References, 10. Appendix.

### Structural Paper

1. Title, 2. Abstract (state the key counterfactual finding), 3. Introduction, 4. Model, 5. Data and Background, 6. Estimation (identification, method, computation), 7. Model Fit and Validation, 8. Counterfactual Analysis, 9. Conclusion, 10. Appendix.

### Descriptive / Measurement Paper

1. Title, 2. Abstract (state the new fact and why it matters), 3. Introduction (why measurement matters; explicit "this paper does not estimate a causal effect"), 4. Data and Construction (this IS the contribution), 5. Patterns (with robustness to alternative definitions and samples), 6. Discussion (relation to existing theoretical predictions), 7. Conclusion (which causal questions the new facts enable), 8. References.

---

## Job Market Paper (JMP) and Dissertation Notes

These conventions apply primarily to economics and adjacent disciplines that hire on the academic job market via a single signature paper.

### JMP

- Calling card. Demonstrate ability to identify an important question, execute credibly, and write clearly — by yourself (even if coauthored, your contribution must be unmistakable).
- Title: memorable, signal your field. Avoid generic titles.
- Abstract: elevator pitch. Lead with the finding, not the method. Make it intelligible to researchers outside your subfield.
- Introduction: exceptionally polished. Many committee members read only the introduction.
- Length: aim for 30–35 pages.
- Signal awareness of the broader literature beyond your subfield.
- If you use a novel method, emphasize the substantive insight it delivers, not the method itself.

### Three-Essays Dissertation

- Standard structure: introduction chapter, three standalone papers, conclusion chapter (~150 pages total).
- **Introduction chapter** (10–15 pages): thematic linkage between the three papers. NOT a literature review.
- **Each essay must be free-standing**: own abstract, introduction, conclusion.
- **Conclusion chapter** (5–10 pages): unified contribution, cross-cutting future directions.
- At least one essay should be sole-authored. The JMP should ideally be sole-authored.
- Order essays by quality: strongest first.

---

## Specialized Output Types

### Survey / Review Paper (handbook chapter, JEL-style review, systematic review)

- Contribution is the synthesis and framing, not new results. State your organizing framework in the introduction.
- Structure by research question or theme, NOT by method or chronology.
- Build a narrative argument about where the field stands and where it should go — not an annotated bibliography.
- Citation density is much higher than original papers (50–200+ references).

### Working Paper → Journal Version Conversion

1. Identify the core 15-page paper (the essential contribution); separate everything else into appendix.
2. Cut in this order: (a) redundant motivation, (b) literature tangents, (c) robustness checks that don't change the story, (d) restating well-known results (cite instead), (e) verbose table / figure captions.
3. Move extended robustness, data appendices, and proofs to an online supplement — but reference every appendix item from the main text.
4. Anticipate referees: organize defensively by separating the core contribution from extensions that can be cut if demanded.

### Grant Proposal

1. Lead with the research question and why it matters NOW.
2. State the expected contribution in one sentence: "This project will [produce / estimate / test] [specific output] that [specific benefit to knowledge / policy]".
3. Demonstrate feasibility: data already in hand, methods already mastered, preliminary results when available.
4. Research design must be concrete: name datasets, identification strategy, sample period.
5. Budget justification connects costs to research activities.
6. Common mistake: writing a grant proposal like a finished paper. A proposal sells a research PLAN, not completed findings.

### Policy Brief / Op-Ed / Blog Post (non-academic audience)

1. Lead with the policy implication, not the research question.
2. State the finding in plain language — no jargon, no Greek letters, no regression terminology.
3. Use one concrete example or anecdote to illustrate the mechanism.
4. Magnitudes in everyday terms: "equivalent to $X per household" or "the same as adding one teacher per school".
5. One figure maximum. Self-explanatory without reading text.
6. Length: under 1,500 words for a policy brief, under 800 for an op-ed.
7. Do NOT cite standard errors, p-values, confidence intervals. Instead: "The effect is large and precisely estimated" or "We can confidently rule out effects smaller than X".
8. End with a concrete recommendation, not "more research is needed".

### Referee Response

1. Begin with a brief, respectful summary: thank the editor and referees for their time and constructive feedback.
2. Structure point by point: quote each comment, then provide your response immediately below.
3. For each comment, state clearly: (a) what you changed, (b) where in the paper (page / line), (c) why.
4. When you disagree with a referee, be respectful but direct. Provide evidence or reasoning.
5. If you added new analyses, describe them briefly and reference the new table / figure.
6. Never be defensive or dismissive. Even unhelpful comments deserve a measured response.
7. End with a brief statement that you believe the paper is improved.
