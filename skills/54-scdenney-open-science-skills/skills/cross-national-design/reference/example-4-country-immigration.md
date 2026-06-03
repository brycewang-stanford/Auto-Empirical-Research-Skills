# Worked Example: Four-Country Immigration Conjoint Cascade

A concrete application of the `cross-national-design` skill end-to-end. The example uses a labor-vs-asylum immigrant-preference conjoint as the illustrative design. Substitute your own theoretical dimension, attributes, and origin countries as appropriate; the structure is what transfers.

## 1. Case-Selection Rationale

**Theoretical dimension.** Welfare-state generosity and immigration history -- two correlated but separable macro-features that shape how natives evaluate immigrants' economic contribution versus cultural distance (cf. Hainmueller & Hopkins 2014; Bansak, Hainmueller, & Hangartner 2016 for the 15-country asylum precedent).

**Why this dimension, not just "four Western democracies."** The theoretical question is whether the *relative* weight on economic-contribution attributes (education, job offer, language) versus cultural-proximity attributes (origin country, religion) tracks the country's welfare-state generosity and the public's prior exposure to large-scale immigration. A design that picks four similar cases (e.g., UK, France, Germany, Netherlands) collapses variation on both dimensions and produces a weak test. A design that varies the two macro-features independently produces a cross-classified 2 x 2 that actually identifies which feature does the work.

**Four cases, 2 x 2 on welfare generosity x immigration history.**

| Country | Welfare Generosity | Immigration History | Justification |
|---|---|---|---|
| Sweden | High | High (post-1970 labor + refugees) | High-generosity + long-history baseline; tests whether economic-contribution weight is *down-regulated* when the welfare state is robust and the native public is accustomed to immigration. |
| United States | Low | High (multi-era settler and labor) | Low-generosity + long-history; tests whether economic-contribution weight *dominates* cultural-proximity weight when the welfare state is thin. |
| Japan | Low | Low (historically closed, post-2018 reforms) | Low-generosity + short-history; tests whether cultural-proximity weight is *amplified* in contexts where immigration is politically novel. |
| Denmark | High | Medium (concentrated post-1990) | High-generosity + medium-history; separates welfare effect from history effect when paired with Sweden (same welfare tier, different history depth). |

**Case-selection logic in one line.** The 2 x 2 isolates welfare-generosity and immigration-history as theoretically distinct moderators of the economic-vs-cultural weighting of immigrant-admission preferences. If you cannot draw a 2 x 2 (or equivalent typology) for your own theoretical dimension, the case set is probably decorative rather than diagnostic. Return to `hypothesis-building`.

**What this design does *not* claim.** Four cases cannot identify interactions between welfare generosity and immigration history with confidence -- the design uses each cell to establish a scope condition, not to test a saturated interaction model. Honest framing of case count (see SKILL.md §1, "Typical Case Count") is part of the design, not a caveat tacked on at the end.

## 2. Shared Conjoint Attributes with Origin-Country Calibration

**Shared attribute schema (same across all four respondent countries).**

| Attribute | Levels (constant across countries) |
|---|---|
| Age | 21, 35, 50 |
| Gender | Female, Male |
| Education | Primary, Secondary, University |
| Job offer | Yes (skilled), Yes (low-skill), No job offer |
| Language proficiency (local) | Fluent, Basic, None |
| Reason for migration | Work, Family reunification, Asylum |
| Country of origin | **Calibrated per respondent country (see below)** |

**Origin-country calibration: top-5 origins per destination.** The calibration rule: choose five origins per respondent country that (a) appear in the destination's top migration inflows (ecological validity), (b) vary on cultural proximity from the respondent's perspective (theoretical leverage), and (c) do not carry overwhelming current-events confounds unless that confound is intended (SKILL.md §3).

| Respondent country | Five origin levels (ordered by ecological prevalence) | Proximity spread (near -> far) |
|---|---|---|
| Sweden | Poland, Syria, Iraq, Somalia, India | Poland (near), India (mid), Syria/Iraq/Somalia (far) |
| United States | Mexico, India, China, Philippines, Nigeria | Mexico/Philippines (near), India/China (mid), Nigeria (far) |
| Japan | China, Vietnam, Philippines, Nepal, Brazil | Brazil (near via Nikkei diaspora), China/Vietnam/Philippines (mid), Nepal (far) |
| Denmark | Poland, Syria, Turkey, Romania, Ukraine | Poland/Romania/Ukraine (near), Turkey (mid), Syria (far) |

**Ecological-vs-comparability trade-off.** Because origin-country lists differ across respondent countries, the "origin country" attribute cannot be compared as a single AMCE across all four destinations. The analyzable cross-national object is the *proximity ordering* of the origin effect (e.g., rank correlation of AMCEs across origins within each country), not the level-specific AMCE. This is a deliberate commitment to ecological validity (SKILL.md §2, "Ecological Validity Check") over apparent comparability (cf. Sniderman 2018's "coarse measurement as principled commitment"). Behavioral benchmarking of at least one case -- for example, against Swiss-style naturalization-referendum data in Sweden or Denmark if available -- strengthens the claim that stated preferences track behavior (Hainmueller, Hangartner, & Yamamoto 2015).

**No-overlap rule.** Within each respondent country, no origin country appears in two experimental roles (e.g., Poland cannot be used as both the "near" labor origin and the "near" family-reunification origin). See SKILL.md §3, "Avoiding Origin Overlap."

## 3. Translation Protocol (CCSG 2016 TRAPD)

The instrument is authored in English (source), then produced in Swedish, US English (minor localization), Japanese, and Danish. Localization is not just translation -- institutional referents, visa categories, and policy vocabulary are adapted per the Instrument Localization guidance in SKILL.md §2. The CCSG 2016 team translation model structures this work.

### Stage T -- Translation (parallel drafts)

- Two independent professional translators per target language produce parallel drafts of the full instrument, including the conjoint attribute labels and level strings.
- Each translator keeps a note file logging: ambiguous source terms, non-equivalent institutional referents, and flagged terms where the conceptual equivalent required substantive rather than literal adaptation (e.g., "skilled worker visa" -> Japan's Specified Skilled Worker, Denmark's Positivlisten).

### Stage R -- Review (team session)

- Both translators, a bilingual subject-matter reviewer, and the lead researcher meet to reconcile drafts item by item.
- Output: a single reconciled draft per target language, with a review log recording resolved disagreements and any items deferred to adjudication.

### Stage A -- Adjudication

- A designated adjudicator (typically the country PI or a senior bilingual researcher familiar with the experimental design, not just the language) rules on items flagged in review.
- The adjudicator signs off on a pretest-ready version. Unresolved items carry an explicit note for pretest attention rather than a silent choice.

### Stage P -- Pretesting

- Cognitive interviews with 8-12 respondents per country on the full localized instrument. Focus on: (a) whether attribute labels and level strings are interpreted as intended, (b) whether origin-country labels cue the intended proximity contrast, and (c) whether the qualitative framing of any information treatment is comparable across countries.
- Findings feed back into a second R/A cycle where needed (CCSG Figure 2 depicts this iteration). Do not treat pretesting as a sign-off ritual -- TRAPD explicitly allows stages to repeat.

### Stage D -- Documentation

- Every stage produces a dated artifact: parallel drafts (T), review log (R), adjudication decisions (A), cognitive-interview protocols and summary (P). These are archived with the pre-analysis plan and referenced in the methods section.
- Documentation is what allows a reviewer or replicator to audit whether the "same" instrument was fielded across countries; without it, the claim of conceptual equivalence is untestable.

**One-paragraph summary for the PAP.** "The instrument was developed in English and produced in Swedish, Japanese, and Danish following the Cross-Cultural Survey Guidelines TRAPD team-translation model (CCSG 2016). Two independent professional translators per target language produced parallel drafts (T), a review session reconciled them with a bilingual subject-matter reviewer (R), a country-PI adjudicator resolved remaining disputes and signed off the pretest-ready version (A), cognitive interviews with 8-12 respondents per country surfaced remaining issues and triggered a second R/A cycle where needed (P), and all stages were logged in a versioned documentation file archived with this PAP (D)."

## 4. Per-Country SESOI and Per-Country Predictions (Why -> If-Then)

**Why -> If-Then, per country.** Articulate the prediction *before* the case set is locked (SKILL.md §1).

### Why (theoretical claim)

The relative weight natives place on economic-contribution attributes (education, job offer, language) versus cultural-proximity attributes (origin country, reason-for-migration) in evaluating immigrants depends on the welfare-state context and the native public's prior exposure to large-scale immigration. Where welfare is generous, natives focus less on immigrants' fiscal contribution and more on cultural fit; where immigration is historically novel, cultural proximity dominates.

### If-Then, per country

| Country | Prediction (If-Then) | Primary estimand | SESOI rationale |
|---|---|---|---|
| Sweden | If welfare-down-regulates-economics holds, then the AMCE on "University education" will be smaller in Sweden than in the US, and the AMCE on origin-country proximity will be *larger*. | Country-specific AMCE on University (vs. Primary) and on proximity-ordered origin contrast. | 3 pp is substantively meaningful: Swedish immigration policy debates center on cultural integration, and a 3 pp shift in the origin contrast would move a marginal admission decision. |
| United States | If the low-generosity + long-history case anchors the *economic-contribution dominant* end of the spectrum, then the University AMCE and Job-Offer AMCE will be larger than in Sweden or Denmark, and the origin AMCE will be smaller. | Country-specific AMCE on University, Job-Offer, and origin contrast. | 4 pp for the US because the larger sample (2,500) permits tighter inference and because US immigration debates hinge on economic-contribution framing; smaller shifts are not policy-relevant. |
| Japan | If cultural-proximity amplifies when immigration is politically novel, the origin-country AMCEs will show the *steepest* proximity gradient of the four cases, and the Language-proficiency AMCE will be unusually large. | Country-specific AMCE on origin contrast and on Language (Fluent vs. None). | 5 pp for Japan because per-country N is budget-constrained to ~1,800, and smaller effects cannot be reliably distinguished from noise (compromise power; Lakens 2025). |
| Denmark | If welfare-generosity moderates economic-contribution weight independently of immigration-history depth, then Denmark's AMCE profile will resemble Sweden's (both high-generosity) more than the US's (low-generosity) despite Denmark's shorter history. | Country-specific AMCE profile; rank correlation of attribute AMCEs with Sweden vs. US. | 3 pp, matching Sweden's threshold for symmetry. |

**What would disconfirm the theory.** The predicted pattern is joint: the US should look different from Sweden (welfare effect) and Japan should show the steepest proximity gradient (history effect). If Denmark looks like the US rather than Sweden, or if Japan's proximity gradient is no steeper than the other three, the welfare/history account is not supported. This is the specific pattern of falsification that locks the design in place before fielding -- and it is why a per-country estimand (Lundberg, Johnson, & Stewart 2021) rather than a pooled "average effect" is the primary object of inference.

**Lock this table in the PAP before fielding.** The per-country predictions must be pre-registered alongside the case set. Adding a case after fielding, or revising a prediction after seeing pilot data, collapses the cross-national leverage back to running-the-same-experiment-four-times.

## 5. Pooled vs Per-Country Analytical Strategy

The analysis plan is organized as a tier rather than a single model.

| Tier | Estimand | Model | What it answers | Inference threshold |
|---|---|---|---|---|
| **T1. Per-country (primary)** | Country-specific AMCEs and marginal means for each attribute, on the respondent's own population | Separate AMCE regression per country with respondent fixed effects and clustered SEs; seven attributes (six shared + origin, with origin analyzed via proximity-ordered contrast) | Within each country, which attributes drive admission preferences? | Country-specific SESOI from §4; report MDE, not just p-values (Lakens 2025). |
| **T2. Pooled with country interactions** | Differential AMCE (attribute x country interaction coefficient) | Pooled regression with attribute main effects, country dummies, and attribute x country interactions; Wald tests on interaction blocks | Does a given attribute's effect size differ systematically across countries? | Minimum-effect test against the per-country-average SESOI, not against zero, to avoid over-rejecting trivial differences in the large pooled N. |
| **T3. Proximity-gradient across origins** | Slope of the AMCE on origin ordered from "near" to "far" within each country | Per-country regression of AMCE on proximity rank; cross-country comparison of slopes | Does the proximity gradient steepen where immigration is historically novel (Japan prediction)? | Pre-registered ranking: Japan > Sweden, US, Denmark on the slope. |
| **T4. Welfare-vs-history decomposition (exploratory)** | Decomposition of pooled attribute x country interaction into welfare-tier and history-tier components using the 2 x 2 | Pooled regression with welfare-tier, history-tier, and attribute interactions | Which macro-feature does more work in explaining cross-national variation? | Explicitly exploratory; four cases cannot identify interaction reliably. Report as a descriptive decomposition, not a confirmatory test. |
| **T5. Sensitivity and measurement-equivalence checks** | Response-style-adjusted AMCEs; DIF / measurement-equivalence diagnostics on Likert-style post-conjoint items | Country-by-country extreme/moderacy checks; configural / metric / scalar invariance on constructs measured via Likert items (CCSG 2016 discusses exact vs. approximate measurement equivalence where exact scalar invariance is too strict) | Are apparent cross-national differences driven by response-style differences or measurement non-equivalence rather than substantive attitudes? | Report invariance results alongside the substantive analysis. Approximate-equivalence approaches (Davidov et al. 2015, cited in CCSG 2016) may be appropriate with four countries where exact scalar equivalence is implausible. |

**Visualization.** Present the per-country AMCEs as side-by-side forest plots (SKILL.md §5, "Visualization"). The cross-national story is usually clearer from a two-panel figure (Tier 1 forest + Tier 3 proximity-slope panel) than from a formal test on interaction coefficients.

**What does *not* go in the primary analysis.** Any attribute x country interaction that was not pre-specified in the PAP; any post-hoc case addition; any "pooled effect" reported without the per-country breakdown. The skill's quality checks apply to this example by construction -- a reader should be able to tick each of them off from the materials above plus the PAP.

---

## References cited in this example

- **Bansak, K., Hainmueller, J., & Hangartner, D.** (2016). "How Economic, Humanitarian, and Religious Concerns Shape European Attitudes Toward Asylum Seekers." *Science* 354(6309): 217-222.
- **Cross-Cultural Survey Guidelines (CCSG).** (2016). *Guidelines for Best Practice in Cross-Cultural Surveys* (4th ed.). Survey Research Center, University of Michigan.
- **Hainmueller, J., Hangartner, D., & Yamamoto, T.** (2015). "Validating Vignette and Conjoint Survey Experiments against Real-World Behavior." *PNAS* 112(8): 2395-2400.
- **Hainmueller, J., & Hopkins, D. J.** (2014). "Public Attitudes Toward Immigration." *Annual Review of Political Science* 17: 225-249.
- **Hainmueller, J., Hopkins, D. J., & Yamamoto, T.** (2014). "Causal Inference in Conjoint Analysis." *Political Analysis* 22(1): 1-30.
- **Lakens, D.** (2025). *Improving Your Statistical Inferences*.
- **Lundberg, I., Johnson, R., & Stewart, B. M.** (2021). "What Is Your Estimand?" *American Sociological Review* 86(3): 532-565.
- **Sniderman, P. M.** (2018). "Some Advances in the Design of Survey Experiments." *Annual Review of Political Science*.
