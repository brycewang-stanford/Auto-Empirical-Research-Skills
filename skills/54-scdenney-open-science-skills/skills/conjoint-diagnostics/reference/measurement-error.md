# Measurement Error Diagnostics for Conjoint Experiments (Clayton et al. 2023)

This reference expands §3 of the `conjoint-diagnostics` skill. Load it when auditing a conjoint study for measurement error, specifying Intra-Respondent Reliability (IRR) estimation, or applying Clayton-Horiuchi-Imai bias correction. Citations preserved here: Clayton et al. 2023 (primary); Bansak et al. 2021; Hainmueller-Hopkins-Yamamoto 2014.

Measurement error in conjoint experiments is a critical and often-overlooked diagnostic. Conjoint experiments produce substantial measurement error due to the inherent complexity of multi-attribute trade-offs.

## 1. Understanding the Problem

- Conjoint responses have **swapping error**: respondents sometimes select the opposite of their true preference. This is NOT classical measurement error.
- For binary outcomes, swapping error biases both MMs (toward 0.5) and AMCEs (toward 0).
- Intra-Respondent Reliability (IRR) in conjoint experiments averages ~77% (range 73-81% across eight replicated studies). This means roughly 15-25% of responses are effectively random noise.
- IRR does NOT vary systematically with attribute combinations but DOES vary with respondent characteristics (younger, male, non-white respondents tend to have lower reliability).
- For subgroup comparisons, bias can attenuate, exaggerate, or flip the sign of differences.

## 2. Does the Study Estimate IRR?

Four methods, in order of ease:

1. **Borrow from similar studies**: Use IRR ≈ 0.75 from Clayton et al.'s replications of similar conjoint studies. Justify the chosen value.
2. **Extrapolate from existing data**: Use within-respondent task-pair agreement as a function of attribute-level differences, extrapolating to zero differences (no repeated tasks needed).
3. **Repeat-task design** (recommended for new studies): Repeat the first conjoint task at the end of the survey (with left/right profiles flipped). IRR = proportion agreement.
4. **Full attribute-specific IRR**: Estimate IRR for each attribute value separately (most intensive).

## 3. Does the Study Apply Bias Correction?

- Corrected MM: ρ̃(a) = (ρ̂(a) − τ) / (1 − 2τ)
- Corrected AMCE: θ̃(a, a') = θ̂(a, a') / (1 − 2τ)
- Where τ is the swapping error probability, estimated from IRR via: τ̂ = (1 − √(1 − 2(1 − IRR))) / 2
- The correction ALWAYS increases absolute value of AMCEs and distance of MMs from 0.5.
- For subgroup differences, the correction can increase (~82%), decrease (~12%), or flip sign (~5%).
- Software: `projoint` R package (Clayton et al.)

## 4. If No Correction, What Is the Risk?

- Sensitivity analysis: Report results for a range of plausible IRR values (e.g., 0.70, 0.75, 0.80)
- At minimum, acknowledge measurement error as a limitation
- For subgroup analyses, this concern is especially acute since bias direction is unpredictable

## Code/Data Audit Hook

If analysis code or data is provided and IRR is unmeasured, compute within-respondent task-pair agreement as a function of attribute-level differences (Clayton et al. 2023 §3.3 method 2 / `projoint`).
