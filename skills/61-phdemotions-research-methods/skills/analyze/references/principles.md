# Confirmatory Analysis Principles

## 1. Pre-registration is the contract

The pre-registration specifies what you will test and how. Deviations are allowed but must be documented, justified, and clearly labeled as exploratory. A pre-registered analysis that fails is more valuable than a thousand post-hoc analyses that succeed.

## 2. Assumptions first, always

Every statistical method rests on assumptions. If you skip assumption testing, you don't know if your results mean what you think they mean. Test assumptions before modeling, document violations, and adapt the method or report the limitation.

## 3. Effect sizes are not optional

Statistical significance tells you whether an effect is likely non-zero. Effect sizes tell you whether anyone should care. A p < .001 with d = 0.05 in a sample of 10,000 is statistically significant and practically meaningless. Always report both.

## 4. Confidence intervals convey uncertainty

A point estimate without a confidence interval is a claim without context. CIs show the precision of estimation and allow readers to assess practical significance. Report 95% CIs for all key estimates.

## 5. Report everything, not just what's significant

Publication bias starts in the analyst's decisions about what to include. Report all pre-registered analyses, including null results. The file drawer problem is solved by transparency, not by selective reporting.

## 6. The model must fit the design

Cross-sectional data cannot support causal claims without strong assumptions. Nested data requires multilevel models. Repeated measures require accounting for within-subject correlation. Panel data benefits from fixed effects. Match the model to the data-generating process, not to the hypothesis you wish you could test.

## 7. Robust alternatives are not cheating

When assumptions are violated, using heteroscedasticity-robust standard errors, bootstrap CIs, or nonparametric alternatives is not p-hacking — it's good methodology. Document the violation and the remedy. The deviation from the pre-registered method is justified if the pre-registered assumptions don't hold.

## 8. Transparency over elegance

A messy, fully documented analysis is better than a clean, opaque one. Show the assumption tests. Show the diagnostic plots. Show the sensitivity checks. Let the reader (and Reviewer 2) see everything.

## 9. One model per hypothesis, then robustness

Fit the pre-registered model first. Get the primary result. Then run alternatives in `/robustness`. Don't stack fifteen models and pick the best one — that's specification searching. The pre-registered model is the result; alternatives are sensitivity checks.

## 10. Code is the analysis

The analysis exists in the code, not in a paragraph describing what you did. If the code can't reproduce the result, the result doesn't exist. Write analysis functions for `targets`/Snakemake integration so every result is one pipeline run away from reproduction.
