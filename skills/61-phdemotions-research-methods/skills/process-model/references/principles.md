# PROCESS Model Principles

## 1. Transparency is the entire point

The SPSS PROCESS macro is a black box: you enter variable names, pick a model number, and get output. The researcher cannot see the model specification, cannot modify it, and cannot verify what's happening. Our lavaan approach makes every path explicit and inspectable. This is the core value proposition.

## 2. Bootstrap CIs for indirect effects, always

Normal-theory tests (Sobel test) assume the sampling distribution of the indirect effect is normal. It usually isn't — it's skewed. Bootstrap confidence intervals (bias-corrected and accelerated) make no distributional assumptions and are the current gold standard. Minimum 5,000 draws; 10,000 for publication.

## 3. The index of moderated mediation is the test

For moderated mediation, researchers often test whether each conditional indirect effect is significant. This is wrong — you need to test whether the indirect effects differ across moderator levels. The index of moderated mediation (Hayes, 2015) does this. If its bootstrap CI excludes zero, the indirect effect is conditionally dependent on the moderator.

## 4. Johnson-Neyman over simple slopes

Simple slopes at ±1 SD of the moderator tell you whether the effect is significant at those specific values. Johnson-Neyman analysis tells you the exact moderator value where the effect transitions from significant to non-significant (or vice versa). J-N is strictly more informative. Report both: simple slopes for the familiar table, J-N for the precise boundary.

## 5. Mean-center moderators, not everything

Mean-centering the moderator reduces multicollinearity between the moderator and the interaction term, making coefficients more interpretable. It does not change the interaction test itself. Don't center the IV or mediator unless you have a specific reason.

## 6. Model numbers are a convenience, not a specification

"Model 14" means something specific in Hayes' taxonomy, but the lavaan syntax is the actual model. Always write out the full syntax so the researcher (and reviewers) can see exactly what was estimated. Use model numbers as shorthand for communication, not as a substitute for specification.

## 7. Verify with bruceR

Running the same model through `bruceR::PROCESS()` provides a verification check and produces the familiar PROCESS-style output tables that reviewers expect. Estimates should match within rounding. If they don't, investigate — different default settings (e.g., HC3 vs. regular SEs) can cause minor discrepancies.

## 8. Report all paths, not just the indirect effect

A mediation analysis estimates multiple paths. Report all of them: a (X → M), b (M → Y), c' (direct), indirect (a×b), and total (c). Reviewers want to see the full picture, and a significant indirect effect with a near-zero a path tells a very different story than one with a large a path.
