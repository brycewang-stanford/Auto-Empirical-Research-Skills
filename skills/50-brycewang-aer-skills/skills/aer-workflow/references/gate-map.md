# Gate Map: The 12-Step Manuscript Lifecycle

*Bundled with the `aer-workflow` skill so the guidance works without the repository checkout. SKILL.md routes; this file carries the depth.*

The lifecycle below is a set of **gates, not suggestions**. Each step names its
entry criteria, the skill that does the work, the gate that must pass before
advancing, the artifact the step must leave behind, and the next step. Do not
advance past a failing gate.

## Global ordering principles

1. **Identification before writing.** No prose is drafted until the design
   survives the identification stress test. A paper written around a broken
   design cannot be repaired by editing.
2. **Body before introduction.** The introduction summarizes a body that
   exists; writing it first bends results prose to fit promises.
3. **Consistency and referee simulation before submission.** The integrity
   audit must report all-pass and the simulated verdict must reach at least
   major R&R before the preflight even starts.
4. **Rebuttal always against the revised manuscript.** Revise first, then
   write the response letter pointing at the new draft — never against the
   version the referees read.
5. **Replication package before submission, not after acceptance.** The AEA
   Data Editor's report is part of the production timeline; a late package
   delays publication.

## The 12 steps

### Step 1 — Topic selection and venue routing

- **Enter when**: the project is new, the venue (AER / AER: Insights / AEJ) is
  undecided, or the contribution cannot be stated in one line.
- **Skill**: `aer-topic-selection`
- **Gate**: a one-sentence contribution claim exists and a target venue is
  chosen. Fail if the claim needs two sentences or hedges the venue.
- **Artifact**: contribution sentence + venue decision with rationale.
- **Next**: Step 2.

### Step 2 — Literature positioning and novelty scan

- **Enter when**: the contribution sentence exists but the closest papers are
  unmapped, or any citation needs verifying.
- **Skill**: `aer-literature`
- **Gate**: closest-papers table filled and verified; no unresolved scoop. A
  novelty hit (same question, same data, defensible design) fails the gate —
  return to Step 1 to re-cut the contribution.
- **Artifact**: antecedents map, search log, opened citation ledger.
- **Next**: Step 3.

### Step 3 — Identification design

- **Enter when**: positioning is settled and the empirical design is the
  bottleneck (DiD, IV, RDD, SCM, shift-share, event study, RCT analysis).
- **Skill**: `aer-identification`
- **Gate**: the design survives the red-flag checks with modern estimator
  defaults. If it fails here, no later step saves the paper.
- **Artifact**: written identification strategy — assumptions, estimator
  choice, inference plan.
- **Next**: Step 3a for experiments or primary data collection; otherwise
  Step 4.

### Step 3a — Preregistration detour (experiments / primary data only)

- **Enter when**: the design randomizes treatment or collects new data, and
  the intervention has **not yet run**. Skip entirely for observational data
  already realized.
- **Skill**: `aer-preregistration`
- **Gate**: pre-analysis plan written, sample size justified by a power/MDE
  calculation, AEA RCT Registry entry timestamped **before** the intervention.
- **Artifact**: PAP + registry ID.
- **Next**: Step 4 (after data are in hand).

### Step 4 — Robustness program

- **Enter when**: main results exist but referee-anticipating checks are
  missing or weak.
- **Skill**: `aer-robustness` (execute via the language templates or the
  optional `aer-statspai` engine)
- **Gate**: the three checks the median referee will demand — placebo,
  heterogeneity, alternative samples — are run and reconciled with the main
  result.
- **Artifact**: robustness results and a consolidated robustness exhibit plan.
- **Next**: Step 5.

### Step 5 — Paper body

- **Enter when**: empirics are done; body sections need drafting or repair.
- **Skill**: `aer-paper-body`
- **Gate**: every claim in the body traces to an exhibit or a verified
  citation — no orphaned assertions.
- **Artifact**: complete background, data, strategy, results, mechanisms, and
  conclusion sections.
- **Next**: Step 6.

### Step 6 — Introduction and abstract

- **Enter when**: the body exists and is stable.
- **Skill**: `aer-introduction`
- **Gate**: five-paragraph introduction summarizing the real body; abstract at
  or under 100 words.
- **Artifact**: introduction + abstract.
- **Next**: Step 7.

### Step 7 — Tables and figures

- **Enter when**: exhibits exist but are inconsistent, oversized, or off
  house style.
- **Skill**: `aer-tables-figures`
- **Gate**: booktabs style throughout, notes complete (estimator, SE
  structure, sample, N), figures vector and grayscale-legible.
- **Artifact**: final main-text and appendix exhibits.
- **Next**: Step 8.

### Step 8 — Consistency audit

- **Enter when**: the manuscript is assembled end to end.
- **Skill**: `aer-consistency`
- **Gate**: all-pass on numbers vs. tables, sample sizes, conversions,
  cross-references, and the two-way citation match; the citation ledger from
  Step 2 is fully closed. Any fail loops back to the owning step.
- **Artifact**: consistency report.
- **Next**: Step 9.

### Step 9 — Referee simulation (the loop)

- **Enter when**: the consistency audit is all-pass on a complete draft.
- **Skill**: `aer-referee-sim`
- **Gate**: simulated desk screen plus three adversarial reports reach a
  verdict of **at least major R&R on two consecutive fresh runs**. Anything
  worse routes the named weakness back to its fix skill (design issues to
  Step 3, robustness to Step 4, framing to Step 6, exhibits to Step 7), then
  re-runs Steps 8-9. **Iterate until the gate passes — this loop has no skip.**
- **Artifact**: the revise list; the reports' praise is not an artifact.
- **Next**: Step 10 (only on a passing verdict).

### Step 10 — Replication package

- **Enter when**: results are final and still fresh in code.
- **Skill**: `aer-replication`
- **Gate**: the deposit reproduces every exhibit from raw inputs; README meets
  AEA Data and Code Availability policy.
- **Artifact**: deposit-ready package + README.
- **Next**: Step 11.

### Step 11 — Submission preflight

- **Enter when**: everything upstream is green.
- **Skill**: `aer-submission`
- **Gate**: length, format, cover letter, and conflict-of-interest disclosures
  all pass — no partial credit.
- **Artifact**: submitted manuscript + cover letter.
- **Next**: Step 12, after the editorial decision arrives.

### Step 12 — Rebuttal

- **Enter when**: reviewer reports exist (R&R or reject-and-resubmit).
- **Skill**: `aer-rebuttal`
- **Gate**: manuscript revised **first**; point-by-point letter written
  against the revised version, every point either implemented or respectfully
  rebutted with evidence.
- **Artifact**: response letter + revised manuscript, kept in lockstep.
- **Next**: re-run Step 8 (consistency) on the revised draft before it ships;
  identification-targeting reports loop back to Step 3 and forward again.

## Where am I? Triage table

| Manuscript state | Resume at |
|---|---|
| Idea only; venue undecided | Step 1 |
| "Has someone already done this?" / citations unverified | Step 2 |
| Design questions open (staggered DiD, weak first stage, bandwidth) | Step 3 |
| About to run an experiment or collect data | Step 3a |
| Main estimate exists; no placebo or heterogeneity checks | Step 4 |
| Results exist; body sections missing or table-walking | Step 5 |
| Body done; intro missing, bloated, or abstract over 100 words | Step 6 |
| Exhibits off house style or overstuffed | Step 7 |
| Full draft; numbers never reconciled against tables | Step 8 |
| Draft "done"; wants tearing apart before submission | Step 9 |
| Package or README not yet reproducible | Step 10 |
| Submitting imminently | Step 11 |
| Reports in hand | Step 12 |
| Rejected, changing venue | Step 1, then Step 6 for re-framing |

## Canonical repo sources

These require the repository checkout:

- `docs/workflow-map.md` — the full lifecycle diagram, loop rules, and
  cross-cutting checks
- `skills/aer-workflow/SKILL.md` — the router skill this file deepens, with
  the decision cues and handoff contract
- `docs/desk-rejection-audit.md` — the pre-submission first-failure-point
  audit referenced by Steps 9 and 11
