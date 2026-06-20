# Worked Example: Methods Paragraphs Satisfying Checklist Items 1--19

This example illustrates the paragraph-level output that the `methods-reporting` skill is designed to produce. It is a *hypothetical* survey experiment on immigration attitudes, written to comply with the 19 APSA Experimental Section items (Gerber et al. 2014) that form the core of the checklist. Item numbers (1--19) are annotated in square brackets at the end of each sentence or clause so the mapping is inspectable; in production prose the bracketed labels would be removed. Where an item is satisfied via an appendix, supplementary document, or linked replication archive, that location is named explicitly -- the checklist closes the researcher degree of freedom only if the reader can find the item.

The aim is to demonstrate compactness: all 19 items can be reported in roughly six paragraphs (~650 words) without an appendix dump. Deeper evidence (exact wordings, balance tables, flow diagrams) lives in the supplementary materials, which this example names but does not reproduce.

---

## Sample Paragraphs

### Subjects, Recruitment, and Setting

We fielded an online survey experiment between 14 March and 28 March 2025 [2] among U.S. adults aged 18 and older residing in one of the 50 states or the District of Columbia [1]. The sample was recruited through YouGov, which maintains a nonprobability opt-in panel matched to ACS benchmarks on age, gender, race, education, and region of residence; details of YouGov's sample-matching procedure are documented in their public methodology statement (https://today.yougov.com/about/panel-methodology) [3]. Of 3,421 panelists invited, 2,147 began the survey and 1,982 completed it, for a completion rate (AAPOR COOP3) of 57.9%; the cumulative response rate (AAPOR RR3) incorporating panel recruitment and profile completion is 5.2%, computed following AAPOR (2023) standard definitions [4].

### Allocation and Treatment

Respondents were randomly assigned to one of four experimental conditions using Qualtrics's built-in randomizer with balanced assignment across conditions [5]; the unit of randomization was the individual respondent [6]. Conditions varied on two 2×2 factors: (a) the *framing* of an immigration vignette (economic vs. cultural) and (b) the *nationality* attributed to the hypothetical migrant (Mexican vs. Ukrainian). Each condition presented a 120-word vignette followed by an identical six-item attitude battery; the full vignette text for each of the four conditions, along with images used, is reproduced in Appendix A [8, 9]. Respondents in all four arms received the same pre-treatment covariate battery (age, gender, education, race, household income, 7-point party identification, and 2024 presidential vote) before assignment; baseline means and standard deviations by condition are reported in Supplementary Table S1 and show no statistically significant imbalance (all joint-F p > 0.18) [7].

### Measurement

The primary outcome is a three-item *restrictionist policy support* index (alpha = 0.81), averaging 7-point Likert responses to items on border enforcement, deportation, and reduction of legal immigration; exact item wordings appear in Appendix B [10]. The index is constructed as the respondent-level mean of the three items, after recoding all items so that higher values indicate stronger restrictionist support and reverse-coding Item 2; respondents missing all three items are excluded, while respondents missing one or two items are retained using the mean of non-missing items [11]. Secondary outcomes include an affect thermometer toward immigrants (0--100) and a four-item *perceived economic threat* index (alpha = 0.74). All covariates are coded as described in Appendix C, which also reports coding for the stratification variables used in weight construction [12].

### Sample Flow

Of 3,421 panelists invited, 3,150 were assessed for eligibility after screen-out for residing outside the United States [13]; 78 were excluded prior to randomization for failing a pre-treatment attention check ("Please select 'Strongly agree' to continue"), leaving 3,072 available for assignment [14]. Of these, 768, 770, 767, and 767 were assigned to the economic-Mexican, economic-Ukrainian, cultural-Mexican, and cultural-Ukrainian conditions, respectively [15]. All assigned respondents received the intended vignette (100% intervention receipt; no crossovers) [16]. A total of 165 respondents (5.4%) dropped out before completing the primary outcome battery -- 41, 39, 43, and 42 per condition -- with dropout uncorrelated with condition (chi-squared(3) = 0.15, p = 0.985) [17]. We retain all 2,907 respondents with complete outcome data in the primary analysis and provide results from a multiple-imputation sensitivity analysis retaining the full N = 3,072 in Appendix D [18].

### Results Reporting

Following intent-to-treat principles, we report means, standard deviations, and Ns for the primary outcome by assigned condition regardless of attention-check status: economic-Mexican M = 4.12 (SD = 1.64, N = 727), economic-Ukrainian M = 3.87 (SD = 1.68, N = 731), cultural-Mexican M = 4.28 (SD = 1.61, N = 724), cultural-Ukrainian M = 3.91 (SD = 1.65, N = 725) [19]. Full regression results, ITT and modified-ITT comparisons, and robustness checks are reported in Section 4 and Appendix E.

---

## Notes on Using this Example

1. **What this example demonstrates.** Items 1--19 can be reported compactly *if* the methods section names its supplementary documents (Appendices A--E and Table S1) and defers exact wordings, balance tables, and flow diagrams to those documents. A methods section that tries to inline every item becomes unreadable; a methods section that omits the supplementary pointers fails the reporting standard.
2. **What this example does not cover.** Items 20--28 (conjoint-specific), 29--40 (design transparency, pre-registration, sensitivity, open science), and 41--45 (survey-quality) are not illustrated here. Conjoint-specific reporting requires the attribute table and randomization-constraint disclosure described in Section 6 of the skill; design-transparency items require explicit pre-registration ID, SESOI, and deviation disclosures. Those add roughly two further paragraphs to a full methods section.
3. **CONSORT-style flow diagram.** The sample-flow paragraph above is the *prose* counterpart to a CONSORT 2010 flow diagram (Schulz, Altman, and Moher 2010). For experimental research with non-trivial attrition or multi-stage allocation, a figure is generally clearer than prose; see the CONSORT 2010 four-stage template (enrollment → allocation → follow-up → analysis).
4. **Exact-wording disclosure.** Appendix B (not reproduced here) is the load-bearing element for item 10. Skills and checklists that accept paraphrased question wordings as satisfying item 10 admit a researcher degree of freedom; the rule is reproduction of the exact stimulus text, not description.
5. **The "see Appendix X" pattern is not an escape hatch.** Every appendix pointer in the sample paragraphs above is specific (Appendix A for vignettes, Appendix B for wordings, Appendix C for coding, Appendix D for imputation sensitivity, Appendix E for full results, Supplementary Table S1 for balance). "See supplementary materials" without a named section is insufficient.
