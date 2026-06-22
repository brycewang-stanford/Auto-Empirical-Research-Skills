---
name: aer-literature
description: Use when positioning a manuscript against the existing economics literature, building the antecedents map for the introduction, deciding what to cite, or verifying that every reference in the bibliography is real, correctly attributed, and cited to the published version. Apply at topic selection for the novelty scan and again before drafting the introduction.
---

# AER Literature

## Overview

This skill does two jobs that AER referees grade separately:

1. **Positioning** — finding the closest predecessors, mapping what each did
   and missed, and choosing the value-added claim the paper can actually
   defend. A mispositioned paper draws the fatal report sentence "the authors
   appear unaware of [paper]."
2. **Citation integrity** — guaranteeing that every reference exists, says
   what the manuscript claims it says, and is cited to the right version.

The second job is **non-negotiable for AI-assisted manuscripts**. Language
models produce plausible-looking citations that do not exist, attach real
authors to invented titles, and attribute findings to papers that show the
opposite. One hallucinated reference, found by a referee, destroys the
credibility of every other sentence in the paper. The working rule:

> **No citation is written from memory. Every entry is verified against a
> fetched source before it enters the bibliography, and every claim about a
> paper is verified against that paper's actual text.**

## When to Use

- During `aer-topic-selection`, to run the novelty scan before committing
- Before `aer-introduction`, to build the antecedents paragraph
- When a referee names a missed paper and the positioning needs repair
- Before submission, as the bibliography verification pass (pairs with
  `aer-consistency`)

## Search Protocol

Run all five channels — each finds papers the others miss:

1. **Working-paper series**: NBER, CEPR, IZA, SSRN, BFI. Top-5 competitors
   live here for 2-4 years before publication; the novelty threat is almost
   always an unpublished working paper, not a published article.
2. **RePEc / IDEAS and Google Scholar**, searching by question ("effect of X
   on Y"), by method-in-setting, and by dataset name. Dataset search catches
   the most dangerous neighbor: someone using the same data.
3. **Forward citations** of the two or three obvious antecedents — everyone
   who cited them since, sorted by recency.
4. **Recent tables of contents**: AER, QJE, JPE, Econometrica, ReStud, AEJ
   family, ReStat, JEEA — last 3-5 years, scanning titles in the subfield.
5. **Handbook chapters and *Journal of Economic Perspectives* / *Annual
   Review of Economics* surveys** for the field's own map of itself.

Log every search (channel, query, date, hits) — the log answers the referee
who asks "did you know about X?" and feeds the novelty audit in
`aer-topic-selection`.

## The Antecedents Map

Reduce the search to the **3-6 closest papers** and fill this table honestly
— it is the skeleton of the introduction's antecedents paragraph and the
evidence base for the contribution claim:

| Paper | Question | Data / setting | Identification | Headline finding | What it does not do |
|---|---|---|---|---|---|
| A (2019) | ... | ... | ... | ... | ... |

Rules:

- "What it does not do" must be a fact about the paper, not a slight. The
  introduction will say it in neutral language; referees include these
  authors.
- If the closest paper answers the same question with the same data and a
  defensible design, the contribution claim must change — return to
  `aer-topic-selection` rather than writing around the conflict.
- Verify each row against the paper's **published version** — abstracts and
  early working papers often differ from the final result.

## Positioning Moves

The value-added paragraph claims one primary move (plus at most two
supporting ones):

| Move | Defensible when |
|---|---|
| New question | No antecedent asks it — and it matters that nobody has |
| New identification | Antecedents are correlational or use a now-rejected design |
| New data | Resolution, coverage, or linkage the literature lacked |
| New mechanism | The *why* was open even though the *whether* was settled |
| Opposite / corrected finding | A credibly identified sign flip or magnitude revision |
| Unification | Two literatures explained by one framework or fact |

Match the claim to the map: a "new identification" claim dies instantly if
row 3 of the antecedents table already used the same design.

## Citation Coverage Norms

- A full-length empirical AER paper typically carries **50-110 references**;
  *AER: Insights* far fewer. Padding is as suspicious as thinness.
- Cite: every antecedent in the map; the primary source for every estimator
  and diagnostic (keys in `docs/methods-reference.md`, entries in
  `references.bib`); the source for every institutional fact and every
  benchmark magnitude used in Results.
- Do not cite: textbooks in place of original methods papers; surveys as
  stand-ins for the specific result being invoked; papers included only to
  flatter potential referees.
- Cite the **published version** wherever one exists. Citing the 2019 NBER
  version of a 2021 AER paper signals a stale literature review. Cite a
  working paper only when it is genuinely unpublished — and re-check its
  status at submission time.

## Citation Integrity Protocol

Run this pipeline for **every** reference. No step is skippable for entries
the model "remembers."

### Step 1 — Existence

Verify against an authoritative record: resolve the DOI (Crossref /
doi.org), or match the exact title and author list on the journal page,
RePEc, or the NBER/SSRN abstract page. A reference with no resolvable DOI
and no locatable landing page does not go in the bibliography. Use a web
search or fetch for every entry; if a Zotero or reference-manager connection
is available, import from the verified record rather than typing fields.

### Step 2 — Field accuracy

Check, character by character, against the verified record: full author
list and order, spelling and diacritics, year, exact title, journal, volume,
issue, pages, DOI. The most common AI corruption modes: swapped coauthors,
off-by-one years (working paper vs. publication), a real author pair
attached to an invented title, and the wrong journal in the right family
(AEJ: Applied vs. AEJ: Policy).

### Step 3 — Claim accuracy

For every in-text sentence of the form "[Author (year)] find/show/argue X,"
read at least the abstract — and the relevant table if a magnitude is
quoted. The claim must match what the paper actually establishes, including
sign, population, and design caveats. Misattribution to a *real* paper is
more damaging than a fake one, because the referee may be its author.

### Step 4 — Status

Check that the paper has not been retracted or corrected, and whether a
cited working paper has since been published (then cite the journal
version). For replication-contested results, cite the dispute or choose a
different benchmark.

### Step 5 — Ledger

Maintain a verification ledger alongside `references.bib`:

```text
KEY                  DOI-OK  FIELDS-OK  CLAIM-OK  VERSION      CHECKED
goodman_bacon_2021   yes     yes        yes       published    2026-06-12
hjort_poulsen_2019   yes     yes        yes       published    2026-06-12
```

Any row that cannot reach all-yes is removed from the manuscript or
explicitly flagged to the user as unverified. **Never silently keep an
unverified citation.**

## BibTeX Hygiene

- One key convention, applied everywhere: `author_author_year` lowercase
  (matching `references.bib` in this repository).
- Every entry carries a DOI, or an explicit no-DOI note with a stable URL.
- No duplicate entries under variant keys; no fields invented to fill gaps.
- In-text citations compile against the bibliography with zero unresolved
  keys — `aer-consistency` runs this check as part of the full-manuscript
  audit.

## Common Failure Modes

- A bibliography assembled from model memory and "cleaned up" afterward —
  verification is the assembly step, not a post-process
- The novelty scan run only on Google Scholar, missing the NBER working
  paper that scoops the contribution
- "X et al. (2020) show that..." where the paper *suggests* it in the
  discussion section
- Antecedents described from their abstracts, then misrepresented in the
  introduction's value-added contrast
- Citing five surveys to establish a fact one primary source established

## Repository Resources

When working from the AER-skills repository or plugin bundle, load only the
relevant resource:

- Verified estimator and diagnostic citations with BibTeX keys:
  `docs/methods-reference.md` and `references.bib`
- Recent papers by subfield for positioning benchmarks:
  `examples/modern-aer-exemplars.md`
- Classic contribution archetypes: `examples/aer-exemplars.md`
- The novelty-audit questions this skill's search must answer:
  `skills/aer-topic-selection/SKILL.md`

## Handoff

```text
CLOSEST PAPERS MAPPED: <n> (target 3-6)
SCOOP RISK: <none found / named paper + implication>
POSITIONING MOVE: <new question | identification | data | mechanism | correction | unification>
REFERENCES VERIFIED: <n>/<total> (existence / fields / claim / version)
UNVERIFIED ENTRIES: <list, or "none — all verified">
NEXT SKILL: <aer-introduction | aer-topic-selection | aer-consistency>
```

## Anti-Patterns

- Writing the antecedents paragraph before building the antecedents map
- Treating citation verification as a formatting task to do "at the end"
- Keeping a citation because it "is probably real" — probability is not the
  standard; a fetched record is
- Softening "what it does not do" into vagueness, leaving the value-added
  claim uncontrasted
- Citing the referee-bait paper without reading it — referees test exactly
  those sentences
