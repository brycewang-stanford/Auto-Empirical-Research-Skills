# Venue Router — AER, AER: Insights, and the AEJ Family

*Bundled with the `aer-topic-selection` skill so the guidance works without the repository checkout. SKILL.md routes; this file carries the depth.*

Venue choice is a routing decision made before the abstract is written.
This file routes a given result across AER, AER: Insights, and the four
AEJ journals, then applies the novelty audit and the kill criteria.

## Routing Table

| Venue | Length constraint | Contribution profile | Desk-rejection risk | Turnaround expectation |
|---|---|---|---|---|
| **AER** | ~40 typeset pages; 100-word abstract | Cross-subfield interest plus a substantive contribution: new identification, new fact, new data, or a methodological advance — with 40 pages of substance to fill | High; acceptance historically on the order of 6-8 percent, and the first three pages decide the desk verdict | Slowest of the family: full referee process, often multiple revision rounds over a long horizon |
| **AER: Insights** | 7,000 words minus 200 per exhibit (five exhibits leave 6,000 words); 100-word abstract | One sharp result that makes one point clearly and needs no long literature review; the founding editor's stated bar — if you have a second point, write a second paper | Very high at the desk (roughly 45 percent desk-rejected) but the review that follows is streamlined | Designed for fast decisions; short-cycle review with a strong norm against multi-round revision |
| **AEJ: Applied Economics** | Full-length; follow current AEA submission guidelines | Strong applied-micro contribution — clean design, careful data — whose audience is subfield-bounded (labor, development, education, health) | Moderate; well-executed papers with honest positioning usually reach referees | Standard field-journal pace: slower than Insights, typically faster than an AER full cycle |
| **AEJ: Economic Policy** | Full-length; follow current AEA submission guidelines | Policy-relevant empirical work — taxation, transfers, regulation, public programs — where the policy lever is the point | Moderate; mismatch (no genuine policy margin) is the main desk risk | Standard field-journal pace |
| **AEJ: Macroeconomics** | Full-length; follow current AEA submission guidelines | Quantitative or empirical macro, growth, monetary and fiscal work; models disciplined by data | Moderate; reduced-form papers with no aggregate implication are the main desk risk | Standard field-journal pace |
| **AEJ: Microeconomics** | Full-length; follow current AEA submission guidelines | Theory, IO, mechanism and market design; a tractable result with a clear economic payoff | Moderate; applied papers with thin theory are the main desk risk | Standard field-journal pace |

Two constraints bind everywhere in the family: the 100-word abstract and
the AEA Data and Code Availability Policy.

## Decision Tree

```
Start: one-line contribution sentence exists (X, Y, Z, D, M, Q all filled)
│
├─ Would three or more subfields cite this paper?
│   ├─ NO ──► AEJ or field journal (skip to the AEJ fork below)
│   └─ YES
│       ├─ Is the contribution ONE sharp point, tellable in ~6,000-7,000
│       │  words with a handful of exhibits and no long lit review?
│       │   ├─ YES ──► AER: Insights
│       │   └─ NO
│       │       ├─ Is there ~40 pages of genuine substance —
│       │       │  mechanisms, dynamics, welfare or framework?
│       │       │   ├─ YES ──► AER
│       │       │   └─ NO ──► cut to the sharp point (Insights) or
│       │       │             deepen before submitting anywhere
│
├─ AEJ fork: which margin carries the paper?
│   ├─ Design-based applied micro, subfield audience ──► AEJ: Applied
│   ├─ A policy lever is the point ──────────────────► AEJ: Policy
│   ├─ Aggregate / monetary / fiscal / growth ───────► AEJ: Macro
│   ├─ Theory, IO, mechanism design ─────────────────► AEJ: Micro
│   └─ Conventional method, modest extension,
│      one-literature audience ──────────────────────► top field journal
│
└─ Any kill criterion live (below)? ──► do not write for a top-5 at all
```

Field experiments with a policy hook route to AER or AEJ: Applied and must
be registered in the AEA RCT Registry before submission.

## Novelty Audit Checklist

Run before the venue decision is final; answer with evidence (the search
protocol lives in the `aer-literature` skill), not recall.

**Nearest-neighbor papers.**

- [ ] The five closest papers are listed, including NBER / IZA / CEPR /
      SSRN working papers, not just published work
- [ ] For each: what it did, what it missed, and in one clause what this
      paper adds (new method, new setting, new mechanism, opposite sign)
- [ ] The closest neighbor is not so close that the value-added is a
      robustness check on someone else's paper

**The ONE contribution.**

- [ ] The contribution fits one sentence: "We show that X causes Y,
      identified by Z, using data D, with magnitude M, which changes how
      economists think about Q"
- [ ] No "and we also explore" — the *and* is where the paper dies
- [ ] The contribution survives the compression test: no senior referee
      could reduce it to "we already knew that" or "interesting, but it
      is not economics"

**Cross-field readability test.**

- [ ] An economist in a different subfield can state the contribution
      after reading only the first page
- [ ] The hook's stake is economic (welfare, policy, magnitudes), not
      internal to one literature's back-and-forth
- [ ] Three subfields that would plausibly cite the paper can be named —
      named, not gestured at

## Kill Criteria — When Not to Write for a Top-5

Any one of these live means the realistic ceiling is an AEJ or a top field
journal; write for that venue from the start rather than collecting a
desk rejection first.

1. **Toolkit application.** Competent application of an existing method to
   a new dataset, with no new fact, method, data, or identification.
2. **Single-literature audience.** Only one subfield would cite it, and
   the honest answer to "who else cares?" is nobody.
3. **Selection-on-observables identification.** The design is OLS with
   controls dressed in causal language; no venue upgrade fixes this —
   return to the `aer-identification` stage or accept a descriptive frame.
4. **"We already knew that."** The result confirms the literature's prior
   with a smaller standard error.
5. **The contribution needs the appendix.** If the point cannot be
   self-contained in the first three pages, it fails the ten-minute
   editor read at any top-5.
6. **Thin or unreplicable data.** Small-sample, proprietary-and-opaque, or
   off-the-shelf data with nothing new in the linkage.

Routing down is not failure: an AEJ acceptance beats two AER rejections,
and a field-journal paper that ships beats a top-5 draft that never
survives its own pre-mortem. Choose the venue by fit, then write the
paper for that venue's reader.

## Canonical repo sources

Distilled from these repository files (full versions require the
repository checkout):

- `skills/aer-topic-selection/SKILL.md`
- `docs/workflow-map.md`
- `README.en.md` (venue-constraint tables)
