# Introduction Template — The Five-Paragraph Formula

*Bundled with the `aer-introduction` skill so the guidance works without the repository checkout. SKILL.md routes; this file carries the depth.*

Keith Head's five-paragraph formula is the load-bearing architecture of an
AER-style introduction: Hook, Question, Identification, Antecedents and
Value-Added, Roadmap — in that order, with no "Introduction" heading. Each
paragraph below gets a purpose, a sentence budget, topic-sentence patterns,
and a fill-in-the-blank template.

## Paragraph 1 — The Hook

**Purpose.** Convince the editor the outcome matters before saying anything
about this paper. Four admissible openings: Y matters (welfare or policy
stakes), Y is puzzling (a fact existing theory cannot explain), Y is
controversial (two camps disagree), Y is big (a first-order phenomenon).

**Length.** 2-3 sentences. Exactly one number anchoring the magnitude.

**Topic-sentence patterns.**

- "Between [year] and [year], [population] experienced [quantified change]."
- "[Institution] spends [amount] annually on [program], premised on [claim]."

**Template.**

```
[Quantified fact establishing that Y is large, costly, or contested].
[Sentence sharpening the stake: who is affected, what is unknown, or why
existing answers conflict — still without naming this paper].
```

## Paragraph 2 — The Question

**Purpose.** State exactly what this paper does: unit of observation,
outcome, and the variation that identifies the answer.

**Length.** 3-4 sentences, one paragraph. Prefer "this paper" over "we."

**Topic-sentence patterns.**

- "This paper estimates the causal effect of [X] on [Y]."
- "This paper documents [new fact] using [new data]."

**Template.**

```
This paper [estimates / documents / characterizes] [the causal effect of
X on Y / the response of Y to shock S]. The unit of observation is [unit];
the outcome is [precise outcome with units], measured [frequency, period]
using [data source]. Identification exploits [one-clause description of
the variation and why it is plausibly exogenous].
```

## Paragraph 3 — The Identification (or the Model)

**Purpose.** The desk-reject decision lives here. Name the strategy in one
sentence, then show the assumption is credible in this setting. Theory
papers substitute the modeling discipline: what is tractable, what is
general, what the comparative statics deliver.

**Length.** 4-7 sentences (1-2 paragraphs). The identifying assumption gets
exactly one sentence; the evidence for it gets two or three.

**Topic-sentence patterns.**

- "We implement [named modern estimator] for [estimand]."
- "The identifying assumption is [one clause]."

**Template.**

```
We implement [estimator, named] to recover [estimand]. The identifying
assumption is [one sentence, stated plainly]. We support it with [k]
pieces of evidence: (i) [pre-trend or placebo test with its statistic];
(ii) [design diagnostic]; (iii) [sensitivity or bounding exercise].
```

## Paragraph 4 — The Antecedents and Value-Added

**Purpose.** Position against the 3-6 closest published predecessors, then
state approximately three contributions the referee can quote verbatim.
Each contribution must make sense only in light of the prior work.

**Length.** Two paragraphs: antecedents 4-6 sentences; value-added 3-4
sentences or three bullets. Never more than four contributions.

**Topic-sentence patterns.**

- "Three prior papers study closely related questions."
- "Relative to this work, this paper makes three contributions."

**Template.**

```
[k] prior papers study related questions. [Author-year A] did [what]
but [what it missed]. [Author-year B] documented [fact] but did not
[limitation]. Closest to our setting, [Author-year C] examined [what]
using [method that cannot answer this question].

This paper makes three contributions. First, [contribution only
meaningful against A/B/C]. Second, [...]. Third, [...].
```

## Paragraph 5 — The Roadmap

**Purpose.** Orient the reader; nothing else. AER numbers sections with
Roman numerals and leaves the introduction unnumbered; short papers may
omit the roadmap entirely, full-length AER keeps it.

**Length.** 2-4 sentences, one per section or one clause per section.

**Template.**

```
Section I describes [setting/data]. Section II presents the empirical
strategy. Section III reports results. Section IV [mechanisms /
heterogeneity]. Section V concludes.
```

## Condensed Worked Example

Fictional paper: *County Earned-Income Top-Ups and Single-Parent
Employment* (full-length model: `examples/intro-example.md`, repo checkout).

1. **Hook.** "US counties now spend $2.1 billion per year topping up the
   federal EITC, on the premise that local supplements raise employment.
   Whether they do — or merely relabel transfers — is unresolved."
2. **Question.** "This paper estimates the causal effect of county EITC
   top-ups on single-parent employment. The unit is the county-year; the
   outcome is the employment rate of unmarried parents, 2004-2022.
   Identification exploits the staggered adoption of top-ups driven by
   budget cycles unrelated to local labor-market trends."
3. **Identification.** "We implement the Callaway and Sant'Anna (2021)
   group-time estimator. The identifying assumption is parallel employment
   trends between adopting and not-yet-adopting counties. Pre-period
   coefficients are jointly zero, the Goodman-Bacon (2021) decomposition
   shows the weight comes from clean comparisons, and Rambachan and Roth
   (2023) bounds keep the estimate positive under moderate violations."
4. **Antecedents and value-added.** "Saez (2010) documents bunching at
   EITC kink points; Kleven (2016) reviews the bunching evidence — both
   identify intensive-margin responses, not employment. Card and Krueger
   (1994) established the case-study template for local labor-market
   policy but studied a single border pair. This paper contributes: first,
   design-based employment effects of local supplements; second, dynamics
   over an 18-year panel; third, a cost-per-job calculation comparable
   across programs."
5. **Roadmap.** "Section I describes the top-up programs and data.
   Section II presents the strategy. Section III reports results.
   Section IV tests mechanisms. Section V concludes."

## The 100-Word Abstract

Results-first, no motivation-selling: the introduction's hook sells the
question; the abstract sells the answer. Word budget:

| Function | Sentences | Words |
|---|---|---|
| Question or setting | 1 | 15-20 |
| Method / data / identification | 1 | 15-20 |
| Main quantitative result | 1-2 | 30-40 |
| Implication | 1 | 15-20 |

**Template.**

```
[Setting and question — 1 sentence]. [Data and identification — 1
sentence]. [Main result with sign, magnitude, and units — 1-2 sentences].
[Implication — 1 sentence, droppable if over budget].
```

**Checklist.**

- [ ] At or under 100 words by actual count; numbers count as one word each
- [ ] Most words spent on results, not motivation
- [ ] Every result carries a magnitude with units
- [ ] No "we find that" scaffolding — active claims ("X raises Y by Z%")
- [ ] Implication sentence dropped first when over budget

## Anti-Patterns

- **Literature-review opening.** A hook that begins "A growing literature
  has studied..." is a gap claim, not a hook — no stake, no number.
- **Promise without delivery.** Contributions announced in paragraph 4
  that no body section delivers; write the body first, then the intro.
- **Roadmap bloat.** A roadmap paragraph that re-argues the paper section
  by section. One clause per section; some papers cut it entirely.
- **Contribution padding.** Five contributions with one weak entry; the
  referee quotes the weak one. Three strong beats five mixed.
- **Motivation-heavy abstract.** Two sentences of stakes, one of results —
  invert the budget.

## Canonical repo sources

Distilled from these repository files (full versions require the
repository checkout):

- `skills/aer-introduction/SKILL.md`
- `examples/intro-example.md`
- `docs/style-guide.md`
