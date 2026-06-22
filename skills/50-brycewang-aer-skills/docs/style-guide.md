# Economics Prose Style Guide

Sentence- and paragraph-level rules for AER-track manuscripts, distilled from
the public writing advice of McCloskey (*Economical Writing*), Cochrane
(*Writing Tips for PhD Students*), Thomson (*A Guide for the Young
Economist*), and the editing patterns visible in published AER papers. The
section-level architecture lives in `skills/aer-paper-body/SKILL.md` and
`skills/aer-introduction/SKILL.md`; this page is the line editor.

It ends with the **AI-pattern scrub** — the tics that mark machine-assisted
prose. Editors and referees increasingly recognize them, and they read as
carelessness even when the economics is sound.

---

## Sentence Rules

1. **Finding first.** The main clause carries the result; subordinate
   clauses carry conditions. "Earnings rise 4.3 percent after the reform"
   beats "After the reform was implemented, it can be seen that earnings
   rose."
2. **Active voice by default.** "We estimate," "the model predicts," "the
   reform raised." Passive voice is acceptable only when the actor is
   genuinely irrelevant ("wages are top-coded at $150,000").
3. **Verbs do the work.** Prefer "prices fell" to "there was a decrease in
   prices." Every "there is/are" opening is a rewrite candidate.
4. **One thought per sentence.** A sentence with two "which" clauses and a
   parenthetical is three sentences in a trench coat.
5. **Concrete subjects.** "Counties that lost the auction" beats "the
   non-treated observational units."
6. **No throat-clearing.** Delete openers that defer the content: "It is
   important to note that," "It should be mentioned that," "Interestingly,"
   "As mentioned above." If the sentence survives without it, it was filler.
7. **Short words where they exist.** Use, not utilize; show, not
   demonstrate (when you mean show); about, not approximately (outside
   numbers).

## Person and Tense

- **"We"** for the authors' actions; **"this paper"** for the contribution
  statement. Never "the author(s)"; never "one can see."
- **Present tense** for what the paper does and finds: "we estimate," "the
  effect is concentrated." **Past tense** for history and data collection:
  "the program launched in 2015," "the survey was fielded."
- Results stay in present tense even in the conclusion. "We found" makes a
  finding sound provisional.

## Numbers, Units, and Statistics

- Report magnitudes with units in the same sentence as the claim: "4.2 log
  points (s.e. 1.1)," "23 percentage points off a 41 percent base."
- **Percent vs. percentage points** is a correctness issue, not style — see
  the conversion table in `skills/aer-consistency/SKILL.md`.
- "Statistically significant at the 5 percent level," written out. Never
  "highly significant," "very significant," "marginally significant," or
  significance asserted by stars alone.
- Never "almost significant" or "trending toward significance." Report the
  CI and move on.
- Spell out numbers that begin a sentence or recast the sentence. Use
  numerals with units and percentages.
- Round consistently: prose precision matches table precision exactly
  (`aer-consistency` Audit 1).

## Paragraph Discipline

- **Topic sentence first.** The first sentence states the paragraph's
  claim; the rest is evidence. A reader who reads only first sentences
  should reconstruct the whole argument — run this *reverse outline* test
  on every section.
- **One claim per paragraph.** When the evidence changes subject, the
  paragraph ends.
- Paragraphs vary in length naturally. Sequences of uniform 4-sentence
  paragraphs read as generated text (see the scrub below).
- Transitions come from content, not connectives. If paragraph B's topic
  sentence genuinely follows from A's claim, no "Moreover" is needed.

## Hedging Calibration

Hedge claims exactly as much as the evidence requires — no more, no less:

| Claim type | Correct register |
|---|---|
| Design-identified main effect | Plain assertion: "the reform raises X" |
| Mechanism evidence | "consistent with," "points to" — never "proves" |
| Extrapolation beyond the design | Explicit flag: "if effects scale linearly..." |
| Speculation | One sentence, labeled: "we speculate that" |

Uniform hedging — every sentence wearing "may," "might," "could
potentially" — is as wrong as uniform confidence. It also reads as
machine-generated caution.

## Word and Phrase Blacklist

Filler and inflation that AER editing removes on sight:

- *novel, importantly, notably, interestingly, crucially, clearly,
  obviously, very, quite, rather, arguably*
- *"plays a crucial/pivotal/vital role," "sheds light on," "underscores the
  importance of," "highlights the need for," "has important implications
  for policymakers"* (state the implication instead)
- *"a growing body of literature"* (name the papers), *"to the best of our
  knowledge"* (unverifiable — see `skills/aer-introduction/SKILL.md`)
- *"delve into," "navigate the landscape of," "in the realm of," "it is
  worth noting that," "in today's rapidly evolving world"*
- *"robust" as praise* — reserve it for actual robustness statements

## The AI-Pattern Scrub

Run this checklist over any machine-drafted text before a human reads it.
Each item is a pattern that referees now recognize:

1. **Triads everywhere.** "Clear, concise, and compelling" — lists of three
   used as rhythm rather than content. Break or shorten them.
2. **Symmetric contrast scaffolds.** "While X does A, Y does B"; "not only
   X but also Y"; "it is not merely X — it is Y." One per paper, at most.
3. **Connective overdose.** Moreover / Furthermore / Additionally /
   Overall opening consecutive paragraphs. Delete; let topic sentences
   carry the sequence.
4. **Uniform paragraph length** and uniform sentence length. Real arguments
   have short paragraphs where the point is sharp.
5. **Summary endings.** Paragraphs that close by restating their own
   opener ("Thus, the data show..."). Cut the echo sentence.
6. **Em-dash chains and semicolon stacking** used to glue three claims into
   one sentence.
7. **Inflated section openers.** "Having established X, we now turn to Y" —
   one "we now turn" per paper is plenty; section titles already signpost.
8. **Hedged symmetry.** "may potentially," "could possibly," "seems to
   suggest" — double hedges collapse to one or none.
9. **Vocabulary tells.** *delve, landscape, tapestry, multifaceted,
   nuanced interplay, paradigm shift, holistic, leverage* (as a verb for
   "use") — replace with the plain word.
10. **Imported structure.** Bullet lists inside Results or Mechanisms prose
    where AER papers use paragraphs; bold-faced inline headers mid-section.
    Body prose is paragraphs; lists belong in the appendix or in the few
    canonical places (contributions list, roadmap).

The scrub is not about disguising provenance — the AEA requires AI-use
disclosure (`skills/aer-submission/SKILL.md`). It is about removing
patterns that degrade readability and signal low editing effort.

## Before / After

> **Before.** It is important to note that our results suggest that the
> implementation of the broadband program may have potentially played a
> crucial role in shaping local wage dynamics, shedding light on the
> multifaceted relationship between connectivity and inequality.
>
> **After.** The broadband program raised the 90/10 wage ratio by 4.2 log
> points over six years (Table 3, column 4) — top-decile wages rose while
> the median was flat.

Every revision in the example is one of the rules above: finding first,
magnitude in the sentence, hedges calibrated to a design-identified effect,
filler deleted.

---

## How the Skills Use This Page

- `aer-paper-body` and `aer-introduction` apply these rules while drafting.
- `aer-consistency` enforces the numeric conventions (Audits 1, 3, 4).
- `aer-referee-sim`'s desk screen scans for blacklist phrases and
  AI-pattern density as part of the craft scan.
