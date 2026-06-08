# Pre-Submission Desk-Rejection Audit

A desk rejection is a *no* delivered in the editor's first ten minutes, before any
referee sees the paper. This page is the self-audit that buys those ten minutes.
Run it against the finished draft; every **No** is a likely desk reject, and the
linked skill is where you fix it.

> Editor time is the scarcest resource in the system. Each row below is something
> an AER or AER: Insights editor can check *without reading the paper closely* —
> which is exactly why it decides the verdict. See
> [`design-principles`](./design-principles.md) and [`workflow-map`](./workflow-map.md).

How to use: answer each item **Yes / No** honestly. Stop and fix on the first
**No** in Stages 1-2 — no amount of polish downstream survives a broken
contribution or a fragile design.

---

## Stage 1 — Framing and contribution *(the first three pages)*

| # | Self-check | If No, the editor thinks… | Fix with |
|---|---|---|---|
| 1 | Can you state the contribution in **one sentence** with no "and we also"? | "Competent but unfocused — minor revision at a field journal." | [`aer-topic-selection`](../skills/aer-topic-selection/SKILL.md) |
| 2 | Would an economist **outside your subfield** cite this? | "Solid, but this is an AEJ paper." | [`aer-topic-selection`](../skills/aer-topic-selection/SKILL.md) |
| 3 | Is the journal routing right (AER vs AER: Insights vs AEJ) *before* the abstract? | "Wrong venue — desk reject and suggest elsewhere." | [`aer-topic-selection`](../skills/aer-topic-selection/SKILL.md) |
| 4 | Does the abstract (≤ 100 words) **lead with the result**, not the motivation? | "Four sentences of throat-clearing, no finding." | [`aer-introduction`](../skills/aer-introduction/SKILL.md) |
| 5 | Is the identifying variation named in the **first page**, not footnoted? | "Where's the design? Probably weak." | [`aer-introduction`](../skills/aer-introduction/SKILL.md) |

## Stage 2 — Identification *(the part that cannot be rewritten away)*

| # | Self-check | If No, the editor thinks… | Fix with |
|---|---|---|---|
| 6 | If staggered DiD, is the main estimator **heterogeneity-robust** (not TWFE)? | "Modern referees reject this on sight." | [`aer-identification`](../skills/aer-identification/SKILL.md) · [methods](./methods-reference.md#1-difference-in-differences-staggered-adoption) |
| 7 | Did you report the **Goodman-Bacon weight** on forbidden comparisons? | "They don't know their TWFE is biased." | [methods §1](./methods-reference.md#1-difference-in-differences-staggered-adoption) |
| 8 | DiD pre-trends shown as a **joint test + Honest DiD bounds**, not just a plot? | "A flat eyeball is not identification." | [`glossary`](./glossary.md) — *Honest DiD* |
| 9 | IV: is inference **weak-IV-robust** (effective F + AR / `tF`), not `F > 10`? | "First-stage F = 12 is not a defense." | [methods §2](./methods-reference.md#2-instrumental-variables) |
| 10 | Is the **exclusion restriction** one clear sentence with placebo + sensitivity? | "Hand-waved — the instrument isn't credible." | [`aer-identification`](../skills/aer-identification/SKILL.md) |
| 11 | Shift-share: did you commit to **shares-exogenous OR shocks-exogenous**? | "They don't know which assumption they need." | [methods §3](./methods-reference.md#3-shift-share--bartik) |
| 12 | RDD: local-linear + MSE bandwidth + **density and placebo-cutoff tests**? | "4th-order polynomial — desk reject." | [methods §4](./methods-reference.md#4-regression-discontinuity) |
| 13 | SCM: **placebo/permutation inference**, not just a good-looking fit? | "Visual fit is not a p-value." | [methods §5](./methods-reference.md#5-synthetic-control) |

## Stage 3 — Robustness and inference

| # | Self-check | If No, the editor thinks… | Fix with |
|---|---|---|---|
| 14 | Are robustness, heterogeneity, and **mechanism** all pre-empted in the paper? | "This will need a 6-month robustness round." | [`aer-robustness`](../skills/aer-robustness/SKILL.md) |
| 15 | Is heterogeneity **theory-predicted**, not mined across every demographic? | "Fishing." | [`aer-robustness`](../skills/aer-robustness/SKILL.md) |
| 16 | Is inference matched to the cluster structure (**wild bootstrap** if few clusters)? | "Standard errors are too small." | [methods §6](./methods-reference.md#6-inference-and-sensitivity-applies-to-all-designs) |
| 17 | For a null result, is there **demonstrated power** and a tight CI? | "Absence of evidence sold as evidence of absence." | [`aer-robustness`](../skills/aer-robustness/SKILL.md) |

## Stage 4 — Exhibits *(referees read tables first)*

| # | Self-check | If No, the editor thinks… | Fix with |
|---|---|---|---|
| 18 | **booktabs** rules, captions placed correctly, ≤ ~7 main tables? | "Careless — what else is sloppy?" | [`aer-tables-figures`](../skills/aer-tables-figures/SKILL.md) |
| 19 | Do tables show **magnitudes**, not just significance stars? | "I can't tell if the effect matters." | [`aer-tables-figures`](../skills/aer-tables-figures/SKILL.md) |
| 20 | Every figure note states **method, CI type, sample, N**; vector format? | "Unreadable in grayscale; unverifiable." | [`aer-tables-figures`](../skills/aer-tables-figures/SKILL.md) |

## Stage 5 — Format, length, and policy

| # | Self-check | If No, the editor thinks… | Fix with |
|---|---|---|---|
| 21 | AER: Insights length within **≤ 7,000 words − 200 per exhibit**? | "Over length — auto reject." | [`aer-submission`](../skills/aer-submission/SKILL.md) |
| 22 | Cover letter ≤ 200 words (or omitted), COI **disclosures** filed per author? | "Policy non-compliance before review." | [`aer-submission`](../skills/aer-submission/SKILL.md) |
| 23 | Replication package built **README-first**, DCAP-compliant, openICPSR-ready? | "Data Editor will stall this for months." | [`aer-replication`](../skills/aer-replication/SKILL.md) |
| 24 | Field experiment: **AEA RCT Registry** entry + PAP before unblinding? | "Unregistered RCT — not submittable." | [`aer-identification`](../skills/aer-identification/SKILL.md) |
| 25 | Every method cited to a **primary source**, not a textbook? | "Citing Angrist-Pischke instead of running the diagnostic." | [`../references.bib`](../references.bib) |

---

## Go / No-Go

- **Any No in Stage 1 or 2** → not ready. Return to the linked skill; the
  contribution or the design needs work, and downstream polish cannot rescue it.
- **Only Stage 3-5 No's** → close. Clear them, then run
  [`aer-submission`](../skills/aer-submission/SKILL.md) for the final format
  preflight.
- **All Yes** → submit, and keep this list — it is also the spine of the
  point-by-point response if an R&R comes back
  ([`aer-rebuttal`](../skills/aer-rebuttal/SKILL.md)).

*This audit composes the whole stack; the routing logic that orders the skills is
in [`aer-workflow`](../skills/aer-workflow/SKILL.md).*
