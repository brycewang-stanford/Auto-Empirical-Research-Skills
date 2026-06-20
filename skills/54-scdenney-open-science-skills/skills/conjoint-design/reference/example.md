# Worked Example: A 4-Attribute Immigration Conjoint

A compact, end-to-end illustration of the design pipeline this skill teaches:
**attribute table → SESOI-anchored power calculation → PAP tier assignment**.
Numbers are illustrative, grounded in Schuessler and Freitag (2020) and
Stefanelli and Lukac (2020). Not a template to copy verbatim — adapt to your
theory, DGP, and literature.

## 1. Research Question and DGP

*Theory:* Voters in high-immigration democracies weigh prospective immigrants
on a mix of economic contribution, cultural compatibility, and legal status.
*Estimand (Lundberg, Johnson, and Stewart 2021):* population-average AMCE of
each attribute level on the probability of being selected for admission,
aggregated over a uniform randomization distribution (with a secondary
target-distribution AMCE per De la Cuesta, Egami, and Imai 2022).

## 2. Attribute Table

Forced-choice paired conjoint, 2 profiles per task, 7 tasks per respondent.
Reference level in bold.

| # | Attribute          | Levels (reference first)                                                                 | L |
|---|--------------------|-------------------------------------------------------------------------------------------|---|
| 1 | Country of origin  | **Germany** / Mexico / Syria / Philippines                                                 | 4 |
| 2 | Occupation         | **Software developer** / Nurse / Construction worker / Unemployed                          | 4 |
| 3 | Language ability   | **Fluent in host language** / Conversational / Limited                                     | 3 |
| 4 | Legal status       | **Documented with visa** / Asylum seeker / Undocumented                                    | 3 |

Notes:
- Attribute order is randomized at the **respondent level** (Stantcheva 2023).
- No hard attribute-level restrictions; odd combinations (e.g., "undocumented
  software developer from Germany") are retained per Bansak and Jenke (2025)
  eye-tracking evidence.
- A repeated task is appended at the end of the block with left/right reversed
  for IRR estimation (Clayton et al. 2023).

## 3. Power Calculation (illustrative)

**SESOI:** 0.04 (4-percentage-point AMCE). Anchor: median published AMCE is
~0.05 and the median insignificant AMCE is ~0.02 (Stefanelli and Lukac 2020),
so 0.04 is near the floor of substantively meaningful effects.

**Closed-form SE (Schuessler and Freitag 2020):**
SE ≈ √(Var(Y) × L / N_eff), with Var(Y) = 0.25 under the forced-choice LPM
approximation and L = 4 (the largest attribute).

Target: SE ≈ 0.013 (so the SESOI of 0.04 is ~3 SEs, powering the two-sided
t-test at ~80% with α = 0.05).

Solve for N_eff: 0.013² ≈ 0.25 × 4 / N_eff → N_eff ≈ 5,917 profile
evaluations. With 7 tasks × 2 profiles = 14 profiles per respondent, that is
~423 respondents for main effects. Rounding up for clustering losses and one
tossed repeated task: **target N ≈ 600 respondents**.

**Interaction budget:** A confirmatory 2×2 interaction between Occupation
("Unemployed" vs. reference) and Legal Status ("Undocumented" vs. reference)
requires roughly 2× that N_eff in the canonical balanced case (SE inflates by
~√2; Schuessler and Freitag 2020). So **~1,200 respondents** if the
interaction is confirmatory.

**Diagnostic cross-checks:**
- N_eff at 600 respondents ≈ 8,400 — well above the ~3,000 pragmatic
  rule-of-thumb floor.
- `cjpowR` simulation to confirm the closed-form estimate.
- Optional: `DeclareDesign` declare–diagnose–redesign pass to check the
  estimator against alternative target distributions and to simulate the
  multiple-testing correction under the sharp null (Blair, Cooper, Coppock,
  and Humphreys 2019).

## 4. PAP Tier Assignment

| Tier        | Specification                                                                                 | Rationale |
|-------------|-----------------------------------------------------------------------------------------------|-----------|
| **Primary (locked)**   | AMCE of each of the 4 attributes on forced-choice selection, over uniform distribution, with Benjamini-Hochberg correction across the family of AMCEs. | Core theoretical claims; pre-specification controls family-wise error (Liu and Shiraito 2023; Gelman and Loken 2014; Simmons, Nelson, and Simonsohn 2011). |
| **Primary (locked)**   | AMCE of "Undocumented" vs. "Documented with visa" has a negative sign and magnitude ≥ 0.04 (SESOI).                                                     | Directional hypothesis on the legal-status attribute. |
| **Secondary (conditional)** | If the main-effect AMCE for "Unemployed" is statistically significant and negative, estimate the Occupation × Legal Status AMIE via `FindIt::CausalANOVA()` (Egami and Imai 2019). | Interaction powered only conditional on main-effect detection; requires the 1,200-respondent budget if run regardless. |
| **Secondary (conditional)** | Marginal means (Leeper, Hobolt, and Tilley 2020) reported alongside AMCEs for subgroup visualization across pre-registered respondent ideology tertiles. | Subgroup comparison as robustness. |
| **Secondary**          | Target-distribution AMCE weighted to match U.S. Census immigrant-stock distribution via `factorEx` (De la Cuesta, Egami, and Imai 2022).                 | External-validity variant of the primary estimand. |
| **Exploratory**        | `cjbart` heterogeneity scan of IMCEs by respondent covariates (Robinson and Duch 2024); `CRTConjoint` assumption-free factor tests (Ham, Imai, and Janson 2024). | Hypothesis-generating; results labeled exploratory unless moderators were pre-registered. |
| **Exploratory**        | Nested marginal means check for lexicographic veto on Legal Status (Dill, Howlett, and Müller-Crepon 2024).                                              | Diagnostic for whether a veto attribute dominates other AMCEs. |

## 5. Cross-References

- `hypothesis-building` — for three-level specification (conceptual,
  operationalized, statistical) of each primary hypothesis.
- `pre-registration-writing` — for tier templates, contingency-tree
  conventions, and deviation-reporting norms.
- `methods-reporting` — for the 45-item checklist that this design must
  satisfy at submission.
- `conjoint-diagnostics` — for the post-data audit pass.
- `conjoint-cleaning` — for the Qualtrics-to-long-format reshape before
  estimation.
