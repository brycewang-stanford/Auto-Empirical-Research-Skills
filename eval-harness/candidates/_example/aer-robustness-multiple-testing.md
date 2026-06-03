Do not present the four unadjusted p<0.05 cells as the paper's mechanism.
Because you tested 20 outcomes across 6 demographic subgroups, this is a family
of all 120 post-hoc tests and creates a multiple testing problem.

For the AER write-up:

1. Define the testing family up front: 20 outcomes times 6 subgroups.
2. Report all 120 estimates in a single appendix table or specification-curve
   display, not just the significant cells.
3. Add adjusted inference for the family. I would report Benjamini-Hochberg FDR
   q-values and, for the most central family, a family-wise error-rate procedure
   such as Holm or Romano-Wolf.
4. Label these subgroup-outcome results as exploratory or hypothesis-generating
   unless they were pre-specified in a PAP or analysis plan.
5. In the main text, discuss only patterns that survive adjusted inference and
   line up with the theory. If none survive, say the mechanism evidence is weak
   and use the results to guide future work rather than to claim confirmation.

A defensible sentence is: "Because these heterogeneity tests were conducted
post hoc, we report the complete testing family with both unadjusted p-values
and FDR-adjusted q-values; the patterns should be read as exploratory evidence."
