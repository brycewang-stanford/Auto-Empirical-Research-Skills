# Referee Report Rubric

The scoring instrument used by `skills/aer-referee-sim/SKILL.md` in Stage 3.
Seven dimensions, each scored 0-5 against the anchors below. The anchors are
deliberately harsh: they describe how AER referees actually grade, not how
authors grade themselves.

Scores are assigned **only with evidence** — each score cites the page,
table, or section that justifies it. A dimension that cannot be scored from
the manuscript alone (e.g., replication readiness with no package available)
is scored from what the manuscript demonstrates and flagged.

---

## Dimensions and Anchors

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
| 5 | Design-based, modern estimator, assumption stated and stress-tested; survives the full `docs/methods-reference.md` battery |
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

---

## Verdict Mapping

Applied by the Stage 3 editor after scoring:

| Condition | Verdict |
|---|---|
| Any dimension 0-1, or Identification ≤ 2, or Integrity ≤ 2 | **Reject** (desk reject if visible in the first pass) |
| Contribution ≤ 2 | **Reject** — usually "better suited to a field journal" |
| All dimensions ≥ 2, Contribution ≥ 3, Identification ≥ 3 | **Major R&R** |
| All dimensions ≥ 4, no blocking comments | **Minor R&R** |
| Acceptance | Not issuable by simulation — the ceiling is minor R&R |

Calibration notes:

- Real AER acceptance is roughly 6-8 percent of submissions; most R&Rs
  still take two rounds. A simulated **major R&R is a strong result**.
- The mapping is a floor, not an average: one fatal dimension rejects a
  paper with six excellent ones. Referees veto; they do not average.
- If two consecutive fresh simulations return ≥ major R&R with no blocking
  comments, `aer-referee-sim`'s exit condition is met.

---

## What a Calibrated Major Comment Looks Like

> **Major comment (well-formed).** The identifying assumption (p. 9) is
> parallel trends between funded and not-yet-funded ZIP codes, but Table 2
> shows funded ZIP codes had 14 percent lower baseline broadband and
> different industry mix. The event study (Fig. 2) is consistent with flat
> pre-trends, yet the confidence intervals admit pre-trends half the size
> of the post-period effect. Please report Rambachan-Roth bounds and a
> specification with commuting-zone-by-year fixed effects; if the result
> survives M̄ = 1, I would consider identification adequate.

Anchored (page, table, figure), quantified, and resolvable — it states the
evidence that would change the referee's mind.

> **Major comment (malformed — do not emit).** The identification strategy
> is not fully convincing and the authors should do more to address
> potential confounders.

Unanchored, unquantified, unresolvable. A simulation producing comments
like this has failed its purpose, whatever the verdict.

---

## Related Pages

- The simulation that consumes this rubric: `skills/aer-referee-sim/SKILL.md`
- A complete worked simulation scored with these anchors:
  `examples/referee-report-example.md`
- The desk screen run before scoring: `docs/desk-rejection-audit.md`
- Estimator-level red flags behind the Identification anchors:
  `docs/methods-reference.md`
- Prose patterns behind the Exposition anchors: `docs/style-guide.md`
