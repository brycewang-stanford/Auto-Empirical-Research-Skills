---
name: novelty-check
description: Verify research idea novelty against recent literature. Use when user says "查新", "novelty check", "有没有人做过", "check novelty", or wants to verify a research idea is novel before implementing.
argument-hint: [method-or-idea-description]
allowed-tools: WebSearch, WebFetch, Grep, Read, Glob, mcp__codex__codex
---

# Novelty Check Skill

Check whether a proposed method/idea has already been done in the literature: **$ARGUMENTS**

## Constants

- **External cross-model verifier (Codex / `mcp__codex__codex`) is UNAVAILABLE** in this environment — persistent `401 Unauthorized` (no OpenAI bearer). Do **not** block on it and do **not** silently skip verification when it fails.
- **EVALUATOR = Claude itself**, acting as an impartial, adversarial referee (Phase C). If Codex ever comes back, it may serve as an optional *second* opinion only.
- Scoring is anchored to the **calibration rubric in Phase D.0** to prevent the score inflation observed when the Codex backend was down (2026-05: several econfin ideas were rated "9" but on rigorous re-check were 5–7.5).

## Instructions

Given a method description, systematically verify its novelty:

### Phase A: Extract Key Claims
1. Read the user's method description
2. Identify 3-5 core technical claims that would need to be novel:
   - What is the method?
   - What problem does it solve?
   - What is the mechanism?
   - What makes it different from obvious baselines?

### Phase B: Multi-Source Literature Search
For EACH core claim, search with ALL relevant sources — **adapt the source set to the idea's field**:

1. **Web Search** (via `WebSearch`): ≥3 different query formulations per claim; include recent-year filters (last 2–3 years).
   - **CS / ML idea** → arXiv, Semantic Scholar, OpenReview (ICLR / NeurIPS / ICML).
   - **Econ / finance / management idea** → SSRN, NBER, RePEc / IDEAS, Google Scholar, and the **top journals of the subfield** (JF / JFE / RFS / JFQA / AER / QJE / JPE / REStud / MS / RAND / Research Policy / JAR / JAE …).

2. **Known recent venues** for that field (last 6–12 months) — the obvious-competitor working papers matter most.

3. **Deep-read, not abstract-skim**: WebFetch the abstract of each potentially overlapping paper; for the **1–2 closest**, fetch the **full text** (PDF / NBER WP / SSRN / VoxEU / replication page). Reading the closest paper in full is mandatory before scoring (see Phase C).

### Phase C: Adversarial Self-Verification (impartial referee)

External cross-model verification is unavailable (see Constants). **Claude performs the cross-examination itself, in an explicitly adversarial, impartial-referee stance.** This is the step that catches inflated novelty — do not shortcut it.

1. **Read the closest work in FULL.** Fetch the full text of the 1–2 closest prior works from Phase B (PDF / WP / SSRN / VoxEU / replication), not just the abstract. **Do not assign a score before you have actually read the closest paper.** If everything is paywalled, say so and flag lower confidence.
2. **Steelman the REJECTION (default skeptical).** Write the strongest case a hostile, well-read referee would make that the idea is *already done / incremental* — name the single closest paper and the exact overlapping claim.
3. **Steelman the DEFENSE.** The strongest honest case for the delta.
4. **Reconcile per claim.** A core claim counts as novel ONLY if it survives the steelmanned rejection.
5. **Check the two inflation traps** (these silently produced false 9s in 2026-05):
   - **Identification confound** — if the headline result co-moves with an obvious confounder and there is no clean exogenous variation, the *causal* claim's novelty is capped LOW no matter how hot the topic.
   - **Obvious-next-paper / public-data scoop** — if the design is the evident follow-up to a recently public dataset or a well-known model, scoop risk caps the score at ≤7.
6. (Optional) If `mcp__codex__codex` ever responds, use it as a *second* opinion — never as a gate.

### Phase D.0: Score Calibration (anchor EVERY score here — prevents inflation)

| Score | Meaning |
|---|---|
| **9–10** | Core claim survives a steelmanned rejection; closest paper read in full and clearly distinct; clean identification OR a genuinely new measure/setting; NOT the obvious next paper for anyone holding the same data/model. |
| **7–8** | Real contribution, but **one of**: crowded space / scoop risk / identification not airtight / incremental to one known paper. |
| **5–6** | Substantial overlap with 1–2 existing papers; the delta is a refinement. |
| **<5** | Already done, or trivial "apply X to Y". |

**Default skeptical**: when torn between two scores, pick the lower. A false 9 costs months.
**Honesty rule**: state the score's basis explicitly — e.g. *"web search + full-text read of [closest paper] + adversarial self-review; no external cross-model check available."* Never present a self-review score as if externally verified.

### Phase D: Novelty Report
Output a structured report:

```markdown
## Novelty Check Report

### Proposed Method
[1-2 sentence description]

### Core Claims
1. [Claim 1] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
2. [Claim 2] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
...

### Closest Prior Work
| Paper | Year | Venue | Overlap | Key Difference |
|-------|------|-------|---------|----------------|

### Overall Novelty Assessment
- Score: X/10
- Recommendation: PROCEED / PROCEED WITH CAUTION / ABANDON
- Key differentiator: [what makes this unique, if anything]
- Risk: [what a reviewer would cite as prior work]

### Suggested Positioning
[How to frame the contribution to maximize novelty perception]
```

### Important Rules
- Be BRUTALLY honest — false novelty claims waste months of research time
- "Applying X to Y" is NOT novel unless the application reveals surprising insights
- Check both the method AND the experimental setting for novelty
- If the method is not novel but the FINDING would be, say so explicitly
- Always check the most recent 6 months of arXiv — the field moves fast
- **A "9" is only allowed if you READ the closest prior work in full AND wrote its steelmanned rejection** — no exceptions, no scoring from abstracts alone
- **Score identification confound and public-data scoop risk DOWN, don't ignore them** — for econ/finance/management, "novelty" includes identification credibility, not just topic newness (these two traps sank real ideas in 2026-05: Secondary-Market collapsed on a confound; Bayh-Dole capped at 7.5 on public-data scoop risk)
- **Label the score's basis** (Phase D.0 honesty rule); when the closest work is paywalled and unread, flag reduced confidence rather than guessing high
- **🚫 NO SUPERFICIAL-SIMILARITY CAPS (hard rule, 2026-05-30, user-mandated).** Never cap a score on title/slogan/topic similarity, a shared dataset, or an "obvious next paper" vibe. Cap for overlap ONLY after establishing, from the prior work's **actual content (method/results read, not just abstract)**, a concrete overlap on the tuple **(research question × mechanism × identification/setting × outcome variable)**, stated as a point-by-point delta table (theirs vs candidate's). If you cannot fill that table from content you actually read, you have NOT established overlap and must NOT cap.
- **Get ungated full text before capping.** If the journal/SSRN PDF is 403, obtain the ungated version (NBER/arXiv/CEPR/author homepage WP, Semantic Scholar abstract+TLDR+references). If none obtainable, mark "unverified" and score on the *verifiable* delta, defaulting toward MORE novel — unproven overlap is not overlap.
- **"Same shock/dataset, different mechanism or outcome" is usually NOVEL, not scooped.** Two papers on the same event/data are not substitutes unless they share BOTH mechanism AND outcome.
- **🔀 SEPARATE NOVELTY FROM IDENTIFICATION (hard rule, 2026-05-30).** Report two distinct axes; never let one masquerade as the other: (i) Novelty = is the contribution new? (ii) Identification credibility = can it be cleanly identified? An idea can be Novelty-9 but Identification-⚠️ (needs a clean shock it lacks) — say exactly that ("novel; proceed only if you secure shock X"); do NOT collapse it into a low novelty score. Output both axes in Phase D.
