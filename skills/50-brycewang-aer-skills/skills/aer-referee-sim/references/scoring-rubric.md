# Referee Simulation Scoring Rubric

*Bundled with the `aer-referee-sim` skill so the guidance works without the repository checkout. SKILL.md routes; this file carries the depth.*

Seven dimensions, each scored 0-5 against the anchors below, then mapped to a
verdict by a precedence ladder that is a **floor, not an average**: one fatal
dimension rejects a paper with six excellent ones. Referees veto; they do not
average. Scores are assigned only with evidence — each score cites the page,
table, or section that justifies it.

The mapping is executable: `scripts/referee_calibration.py` in the repository
parses the `RUBRIC SCORES:` / `VERDICT:` block from any scored run, recomputes
the verdict from the scores, and fails if a stated verdict disagrees, if a
dimension is missing, or if a score is out of the 0-5 range. Do not restate
these numbers from memory; this file mirrors that gate exactly.

## Dimensions and Anchors

The seven dimensions, in canonical order: contribution, identification, data,
robustness, magnitudes, exposition, integrity.

### 1. Contribution

| Score | Anchor |
|---|---|
| 5 | Changes how economists think about an important question; cited across subfields for a decade |
| 4 | Clear new fact, method, or identification on a first-order question; obvious top-5 interest |
| 3 | Solid contribution, but interest plausibly bounded to one subfield — AEJ territory |
| 2 | Competent extension of a known result; "we already knew that" is a fair summary |
| 1 | Contribution unclear after reading the whole paper |
| 0 | No identifiable contribution, or already published elsewhere |

### 2. Identification

| Score | Anchor |
|---|---|
| 5 | Design-based, modern estimator, assumption stated and stress-tested; survives the full methods battery |
| 4 | Credible design with minor gaps (one missing diagnostic; sensitivity not yet run) |
| 3 | Defensible but contestable — the key assumption has a plausible violation the paper acknowledges without fully answering |
| 2 | Outdated implementation (TWFE on staggered data, F=12 IV, high-order RDD polynomial) or assumption asserted rather than supported |
| 1 | Selection-on-observables presented as causal |
| 0 | Claims cause from correlation |

### 3. Data

| Score | Anchor |
|---|---|
| 5 | Data uniquely suited to the question; construction transparent; measurement discussed where it matters |
| 4 | Appropriate data, full sample funnel, minor measurement questions open |
| 3 | Usable but with unexplored measurement or representativeness concerns |
| 2 | Sample construction opaque; Ns do not reconcile across tables |
| 1 | Data cannot answer the question as posed |
| 0 | Provenance unclear or unverifiable |

### 4. Robustness and Inference

| Score | Anchor |
|---|---|
| 5 | The referee's first three objections are already answered in the paper; inference matches the design |
| 4 | Standard battery present; one obvious check missing |
| 3 | Robustness exists but is selective; clustering or small-sample inference questionable |
| 2 | Headline result visibly fragile to reasonable specification changes |
| 1 | No meaningful robustness; inference mismatched to the variation |
| 0 | Evidence of specification search |

### 5. Magnitudes and Interpretation

| Score | Anchor |
|---|---|
| 5 | Every headline coefficient converted, benchmarked, and tied to a disciplined aggregate calculation |
| 4 | Magnitudes interpreted; benchmarking thin |
| 3 | Coefficients reported with signs and significance; economic size left to the reader |
| 2 | Stars-only narration; or magnitudes implausible and undiscussed |
| 1 | Numbers in prose contradict the tables |
| 0 | Results section unintelligible |

### 6. Exposition

| Score | Anchor |
|---|---|
| 5 | First three pages self-contained; reverse-outline test passes; exhibits in house style |
| 4 | Clear with local lapses (one bloated section; minor table issues) |
| 3 | Followable with effort; structure visible but prose works against it |
| 2 | Key information buried (estimand in a footnote, design in section 4); style-guide blacklist density high |
| 1 | Disorganized; referee must reconstruct the argument |
| 0 | Unreadable |

### 7. Integrity and Compliance

| Score | Anchor |
|---|---|
| 5 | `aer-consistency` all-pass; citations verified; replication package deposit-ready; policies met |
| 4 | Consistent manuscript; package incomplete but planned |
| 3 | Minor inconsistencies (digit mismatches, dangling refs) — fixable but visible |
| 2 | Unverified or erroneous citations; text-table contradictions |
| 1 | Numbers irreproducible from the described methods |
| 0 | Fabrication indicators |

## Verdict Mapping

Applied by the Stage 3 editor after scoring, as a precedence ladder (first
matching rule wins). There are no dimension weights; the mapping uses floors.

| Order | Condition | Verdict |
|---|---|---|
| 1 | Any dimension 0-1, or Identification ≤ 2, or Integrity ≤ 2, or Contribution ≤ 2 | **Reject** |
| 2 | All seven dimensions ≥ 4 (and no blocking comments) | **Minor R&R** |
| 3 | All dimensions ≥ 2, Contribution ≥ 3, Identification ≥ 3 | **Major R&R** |
| 4 | Anything left | **Reject** |

Notes on the ladder:

- A Contribution ≤ 2 reject is usually "better suited to a field journal";
  an Identification ≤ 2 or Integrity ≤ 2 reject is a desk reject if visible
  in the first pass. No robustness round fixes a broken design.
- **Acceptance is not issuable by simulation** — the ceiling is minor R&R.
- Real AER acceptance is roughly 6-8 percent of submissions; most R&Rs still
  take two rounds. A simulated **major R&R is a strong result**. A minor R&R
  on a first run should be suspected as leniency: rerun Stage 2 with the
  referee priors sharpened.

## The Desk Screen (Stage 1)

Before any scoring, simulate the editor's first pass: ten minutes, first
three pages, then the main tables, then the bibliography. The editor decides
one thing — is this worth three referees' time? Run the desk-rejection audit
items 1-5 plus three scans:

- **Contribution scan.** Contribution statable in one sentence after page 3;
  interesting to an economist outside the subfield; venue routing right.
- **Design scan.** Identification strategy named on page 1-2, and modern
  (staggered DiD heterogeneity-robust, weak-IV-robust inference, local-linear
  RDD with density test — outdated implementations reject on sight).
- **Craft scan.** Tables in house style, abstract within 100 words, prose
  free of the style-guide failure patterns. Editors read craft as a proxy
  for care in the empirics.

Calibration: if any Stage 1-2 desk-audit item fails, the decision is
**reject** — write the letter and stop; do not soften a desk reject into
"borderline" to keep the simulation going.

## The Three-Referee Panel (Stage 2)

Three referees, three priors, three reading orders — drafted independently,
never letting one inherit another's findings:

| Referee | Persona | Reading order | Prior | Attacks |
|---|---|---|---|---|
| R1 | Identification specialist | Strategy, then Data, then robustness appendix | "The design is broken until proven otherwise" | Assumption plausibility in this setting, missing diagnostics, inference level, estimand-population gaps; re-derives one magnitude from the tables |
| R2 | Field expert | Introduction, antecedents, Results vs. literature | "We probably already knew this" | Novelty against the working-paper frontier, magnitude plausibility, mechanism vs. rival channel, institutional errors |
| R3 | Generalist | Linear, as an editor-board member from another subfield | "Why should I care, and can I follow it?" | Cross-subfield interest, self-contained first three pages, under-interpreted results, exhibit disorder, overreaching conclusion, external validity |

## Report Structure (each referee)

```text
SUMMARY: <2-3 sentences — the paper as the referee understood it>
MAJOR COMMENTS: <numbered; each one: quote or cite the page/table,
  state the problem, state what evidence would resolve it>
MINOR COMMENTS: <numbered, brief>
RECOMMENDATION: <reject | major revision | minor revision | accept>
```

Rules: every major comment **anchored** (quotes the manuscript or names the
exact table/figure) and **resolvable** (states what would satisfy the
referee); at least three major comments per referee or an explicit
certification of why fewer exist; no praise sandwiches — one sentence of
genuine strengths in the summary is the cap.

The Stage 3 editor synthesis then emits the machine-checkable block:

```text
RUBRIC SCORES: <dimension: score, ...>   # all seven, each 0-5
VERDICT: <desk reject | reject after review | major R&R | minor R&R>
DECISION LETTER: <editor's letter, naming the comments that drove it>
REVISE LIST: <every major comment, deduplicated, ordered by severity:
  blocking -> major -> minor, each tagged with the skill that fixes it>
```

## The Loop Rule

Rerun the full simulation with **fresh** reports after each revision round —
re-grading old comments measures compliance, not quality. The exit condition
is **two consecutive fresh runs at major R&R or better with no blocking
comments**; only then hand off to submission. One lucky major-R&R run is not
the exit condition, and rerunning without changing the draft is variance,
not improvement.

## Canonical repo sources

Distilled from these repository files (they require the repository checkout):

- `docs/referee-report-rubric.md` — the anchors, verdict mapping, and a
  calibrated sample major comment
- `scripts/referee_calibration.py` — the executable gate that recomputes
  verdicts from scores
- `skills/aer-referee-sim/SKILL.md` — the three-stage procedure this rubric
  scores
- `docs/desk-rejection-audit.md` — the full 25-item desk-screen checklist
- `examples/referee-report-example.md` — a complete worked simulation scored
  with these anchors
