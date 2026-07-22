# Citation Verification Protocol

*Bundled with the `aer-literature` skill so the guidance works without the repository checkout. SKILL.md routes; this file carries the depth.*

The governing rule: **no citation is written from memory.** Every reference is
verified against a fetched source record before it enters the bibliography, and
every claim about a paper is verified against that paper's actual text. Language
models produce plausible-looking references that do not exist, attach real
authors to invented titles, and attribute findings to papers that show the
opposite. One hallucinated reference, found by a referee, destroys the
credibility of every other sentence in the manuscript.

## A. Fetch-before-cite

Every entry in the bibliography must be verified against an authoritative
fetched record — not against what the model remembers.

Lookup order:

1. **Crossref REST API** — `https://api.crossref.org/works/<DOI>` when a DOI is
   in hand, or `https://api.crossref.org/works?query.bibliographic=<title>` to
   locate one.
2. **OpenAlex** — `https://api.openalex.org/works/doi:<DOI>` (or a title
   search) as the fallback index when Crossref does not resolve.
3. If neither index resolves the work, match the exact title and author list on
   the publisher landing page, RePEc/IDEAS, or the NBER/SSRN abstract page.
4. A reference with no resolvable DOI **and** no locatable landing page does
   not go in the bibliography. Full stop.

Fields to confirm against the fetched record, character by character:

| Field | Check |
|---|---|
| Authors | Full list, order, spelling, diacritics, hyphenated surnames |
| Year | Publication year of the version cited (print vs. online-first can differ by one) |
| Title | Exact, including subtitle |
| Venue | Exact journal name — beware siblings in the same family (AEJ: Applied vs. AEJ: Policy) |
| Volume / issue / pages | As printed |
| DOI | Resolves, and resolves to *this* work |

Cite the **published version** wherever one exists; cite a working paper only
when it is genuinely unpublished, and re-check its status at submission time.
Also confirm the work has not been retracted or corrected.

## B. Claim-level verification

Verifying that a paper exists is not enough. For every in-text sentence of the
form "[Author (year)] find/show/argue X," read at least the abstract — and the
relevant table if a magnitude is quoted. The claim must match what the paper
actually establishes, including sign, population, design caveats, and whether
the result is a main finding or a discussion-section suggestion.
Misattribution to a *real* paper is more damaging than a fake one, because the
referee may be its author.

Maintain a claim-audit table alongside the draft:

| Manuscript sentence (abbrev.) | Bib key | What the paper actually establishes | Sign / magnitude match? | Checked against | Verdict |
|---|---|---|---|---|---|
| "... estimator is biased under heterogeneous effects ..." | `goodmanbacon_2021` | Decomposition of the two-way FE estimand under staggered timing | yes | published article, Section 3 | keep |
| "... bounds under proportional selection ..." | `oster_2019` | Bias-adjusted treatment effect bounds from coefficient and R-squared movements | yes | published article, abstract + Table 2 | keep |

Rules for the table:

- One row per "X finds Y" sentence, not per reference — a paper cited three
  times gets three rows.
- "Checked against" names the artifact actually read (abstract, section,
  table), never "memory" or "summary of the abstract from search results."
- Any row that cannot reach a clean verdict is rewritten or removed. Never
  silently keep an unverified attribution.

## C. BibTeX hygiene

- **One key convention everywhere**: lowercase `author_author_year` (first one
  or two author surnames, underscore-separated, then the year), e.g.
  `oster_2019`, `callaway_santanna_2021`. Stable keys make the two-way
  cite-bibliography match auditable.
- **Every entry carries a DOI**, or an explicit `note` explaining why none
  exists (e.g. the article predates publisher DOI assignment) plus a stable
  URL. A silent DOI-less entry is indistinguishable from an invented one.
- No duplicate entries under variant keys; no fields invented to fill gaps —
  a blank field is honest, a guessed page range is a corruption.
- In-text citations must compile against the bibliography with zero unresolved
  keys, and every bibliography entry should be cited at least once.

## D. Phantom-citation red flags

Treat any of these as a signal to stop and fetch before the reference survives
another draft:

- **Plausible-sounding author-year combos**: two real, frequently co-cited
  authors attached to a title neither wrote. The authors exist; the paper does
  not.
- **Wrong-venue tells**: the right paper in the wrong journal of the right
  family (AEJ: Applied vs. AEJ: Policy, AER vs. AER: Insights), or a field
  journal upgraded to a top-5 outlet.
- **Year off-by-one**: the working-paper year cited as the publication year,
  or vice versa. A one-year gap is the single most common corruption in
  machine-drafted bibliographies.
- **Swapped or reordered coauthors**, or a middle author promoted to first —
  breaks author-year resolution and insults the actual first author.
- **Suspiciously convenient findings**: a citation that says exactly what the
  argument needs, located nowhere the search protocol actually surfaced it.
- **Unfetchable DOIs**: a DOI that resolves in no index is the hallmark of an
  invented citation, not a network hiccup — distinguish "not found" from
  "index unreachable" before concluding either way.

## E. Nearest-neighbor literature mapping

Positioning and citation integrity share a data structure: the closest-papers
table. Build it before writing the introduction.

1. Search five channels — working-paper series (NBER, CEPR, IZA, SSRN),
   RePEc/IDEAS and Google Scholar (by question, by method-in-setting, by
   dataset name), forward citations of the obvious antecedents, recent tables
   of contents of the top general-interest and field journals, and survey
   articles. Log every search (channel, query, date, hits).
2. Reduce the results to the **5-10 closest papers** and fill this table
   honestly, verifying each row against the paper's published version:

| Paper | Question | Data / setting | Identification | Headline finding | What it does not do |
|---|---|---|---|---|---|

3. "What it does not do" must be a fact about the paper, not a slight — the
   introduction will state it in neutral language, and referees include these
   authors.
4. Write one positioning sentence per neighbor from the last two columns:
   *"[Neighbor] establishes [headline finding] in [setting]; it does not
   [gap]. This paper [contribution that fills the gap]."* The introduction's
   antecedents paragraph is these sentences compressed, with the 2-3 closest
   neighbors named explicitly.
5. If the closest paper answers the same question with the same data and a
   defensible design, the contribution claim must change — re-cut the
   contribution rather than writing around the conflict.

## Mechanized checks

When the repository checkout is available, `scripts/verify_citations.py`
mechanizes checks (A) and (C): it resolves every bibliography DOI against
Crossref with an OpenAlex fallback, compares title, first author, and year
against the fetched record, flags DOI-less entries lacking an explanatory
note, and runs the two-way match between manuscript citation keys and the
bibliography (`--online`, `--manuscript`, and `--groundedness` modes). Checks
(B), (D)-triage, and (E) remain judgment work: read the paper, fill the
tables, keep the ledger.

## Canonical repo sources

These require the repository checkout:

- `docs/citation-integrity-protocol.md` — the executable verification design,
  verdict taxonomy, and CI integration
- `skills/aer-literature/SKILL.md` — the routing skill this file deepens
- `scripts/verify_citations.py` — the runnable verifier
- `references.bib` — the verified bibliography the keys above resolve against
