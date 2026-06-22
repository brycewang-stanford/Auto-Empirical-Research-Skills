# Classic AER Exemplars

A reference table of canonical *American Economic Review* (and adjacent
top-5) papers mapped to the AER-skills they best exemplify. Use these
papers as **architecture templates** — not as content to imitate.

> **See also:** [`modern-aer-exemplars.md`](modern-aer-exemplars.md) for a
> subfield-organized list of recent (2018-2025) papers that demonstrate
> *current* estimator practice — Callaway-Sant'Anna staggered DiD,
> Borusyak-Hull-Jaravel shift-share, Calonico-Cattaneo RDD, Anderson-
> Rubin weak-IV inference, and AEA-compliant openICPSR deposits.
> The two files are complementary: this one for **architecture**
> reference, the modern file for **estimator** reference.

All openICPSR / Dataverse links below resolve to publicly available
replication packages. They are the gold standard for what an AER deposit
should look like in 2026.

---

## By Identification Strategy

### Difference-in-Differences

| Paper | Year | Outlet | Why it's the exemplar | Deposit |
|---|---|---|---|---|
| Card & Krueger, "Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania" | 1994 | AER | The canonical 2×2 DiD. Read for narrative restraint, falsification design, and how to defend a single research design across multiple critiques. | n/a (pre-policy) |
| Autor, Dorn & Hanson, "The China Syndrome: Local Labor Market Effects of Import Competition in the United States" | 2013 | AER | Shift-share / Bartik IV done right; foreign-instrument exclusion restriction narrative; cross-subfield reach (labor + trade + macro). | [openICPSR 112670](https://www.openicpsr.org/openicpsr/project/112670) |
| Beraja, Hurst & Ospina, "The Aggregate Implications of Regional Business Cycles" | 2019 | Econometrica | Modern staggered DiD anchored in theory — read for how to integrate empirical design with structural modeling. | [Article DOI](https://doi.org/10.3982/ECTA14243) |

### Instrumental Variables

| Paper | Year | Outlet | Why it's the exemplar | Deposit |
|---|---|---|---|---|
| Acemoglu, Johnson & Robinson, "The Colonial Origins of Comparative Development" | 2001 | AER | The most-cited IV paper in modern economics. Settler-mortality instrument; defense of the exclusion restriction across 50+ pages of subsequent debate. Read alongside Albouy's comment and the AJR reply. | [openICPSR 112563](https://www.openicpsr.org/openicpsr/project/112563) / [112564](https://www.openicpsr.org/openicpsr/project/112564) |
| Angrist & Krueger, "Does Compulsory School Attendance Affect Schooling and Earnings?" | 1991 | QJE | Quarter-of-birth IV. Read for how to *structure* an IV introduction and how to anticipate weak-instrument critiques. | n/a |
| Nunn & Wantchekon, "The Slave Trade and the Origins of Mistrust in Africa" | 2011 | AER | Historical IV with cross-subfield reach (development + political economy). | [AEA article](https://www.aeaweb.org/articles?id=10.1257/aer.101.7.3221) |

### Regression Discontinuity

| Paper | Year | Outlet | Why it's the exemplar | Deposit |
|---|---|---|---|---|
| Dell, "The Persistent Effects of Peru's Mining Mita" | 2010 | Econometrica | Geographic (multidimensional) RDD. Read for spatial-discontinuity design, density tests, and historical narrative. | [Dell research site](https://dell-research-harvard.github.io/projects/498mita) |
| Lee, "Randomized Experiments from Non-random Selection in U.S. House Elections" | 2008 | J. Econometrics | The paper that established close-elections RDD as a workhorse. | n/a |
| Carrell, Sacerdote & West, "From Natural Variation to Optimal Policy?" | 2013 | Econometrica | RDD with a behavioral-mechanism twist; read for *negative* heterogeneity that forced the authors to update their structural prior. | [Article DOI](https://doi.org/10.3982/ECTA10168) |

### Synthetic Control

| Paper | Year | Outlet | Why it's the exemplar | Deposit |
|---|---|---|---|---|
| Abadie, Diamond & Hainmueller, "Comparative Politics and the Synthetic Control Method" | 2015 | AJPS | The methodological reference. Read alongside Abadie's 2021 JEL survey for the modern toolkit. | [Article DOI](https://doi.org/10.1111/ajps.12116) |
| Abadie & Gardeazabal, "The Economic Costs of Conflict" | 2003 | AER | The original SCM application. | [AEA article](https://www.aeaweb.org/articles?id=10.1257/000282803321455188) |

### Field Experiment / RCT

| Paper | Year | Outlet | Why it's the exemplar | Deposit |
|---|---|---|---|---|
| Banerjee, Duflo, Glennerster & Kinnan, "The Miracle of Microfinance? Evidence from a Randomized Evaluation" | 2015 | AEJ:App | Multi-site RCT with PAP, attrition, multiple-hypothesis correction. Cited as a model AEA RCT Registry entry. | [AEA RCT Registry](https://www.socialscienceregistry.org/) |
| Karlan & List, "Does Price Matter in Charitable Giving?" | 2007 | AER | Compact RCT design; read for power-calculation reporting. | [AEA article](https://www.aeaweb.org/articles?id=10.1257/aer.97.5.1774) |

---

## By Skill — Which Paper to Read

| AER-skill | Read this exemplar | What to study |
|---|---|---|
| `aer-topic-selection` | Card & Krueger (1994) | How a narrow setting becomes a cross-subfield contribution |
| `aer-introduction` | Acemoglu-Johnson-Robinson (2001), p. 1369-1373 | Keith Head five-paragraph formula in its purest form |
| `aer-identification` (DiD) | Autor-Dorn-Hanson (2013) §3 | Shift-share IV + first-stage narrative + placebo design |
| `aer-identification` (IV) | Nunn (2008), "The Long-Term Effects of Africa's Slave Trades" | Exclusion-restriction defense via institutional history |
| `aer-identification` (RDD) | Dell (2010) §4 | Geographic discontinuity + density test + bandwidth grid |
| `aer-identification` (SCM) | Abadie-Diamond-Hainmueller (2010), "Synthetic Control Methods for Comparative Case Studies" | Placebo inference + donor weighting |
| `aer-robustness` | Chetty et al. (2014), "Where is the Land of Opportunity?" | Specification curve presented as a *feature* |
| `aer-tables-figures` | Autor-Dorn-Hanson (2013), Table 3 | The canonical 6-column AER results table |
| `aer-replication` | Any 2023+ AER paper at openICPSR | Current AEA Data Editor expectations |
| `aer-rebuttal` | Albouy (2012) AER comment + AJR reply | How to push back substantively without ad hominem |

---

## Public Replication Repositories

Browse current AEA replication standards directly:

- **AEA Data and Code Repository at openICPSR** — https://www.openicpsr.org/openicpsr/aea
- **Harvard Dataverse — QJE Dataverse** — https://dataverse.harvard.edu/dataverse/qje
- **AEA Data Editor's Office** — https://aeadataeditor.github.io/
  - Look at the *example reports* of computational reproducibility checks
- **Daron Acemoglu's data archive** — https://economics.mit.edu/people/faculty/daron-acemoglu/data-archive
- **Opportunity Insights (Chetty et al.)** — https://opportunityinsights.org/data/

## What to Extract from Each Exemplar

When studying a classic, build a **3-bullet architecture note**:

1. **Identification one-liner.** "Causal variation comes from [...]; the
   exclusion restriction is [...]; defended by [...]."
2. **First-paragraph hook anatomy.** What number does the first paragraph
   anchor on? What stylized fact? What policy stake?
3. **Robustness battery.** Which 3-5 placebos / alternative samples /
   alternative estimators carry the most weight in the appendix?

Most AER-quality papers can be reverse-outlined into these three notes in
under 30 minutes. Do this for the three exemplars most relevant to your
own design before drafting your own introduction.

---

## Important Caveat

Several exemplars above predate the modern (post-2020) econometric
defaults. The Card-Krueger 1994 DiD is canonical *as a narrative
architecture*, but a 2026 staggered DiD using the same TWFE specification
would be flagged. Read these papers for **structure**, not for **estimator
choice**. For estimator choice, follow `aer-identification`.

---

## Sources

- [AEA Data and Code Repository at openICPSR](https://www.openicpsr.org/openicpsr/aea)
- [openICPSR project 112670 — Autor-Dorn-Hanson China Syndrome](https://www.openicpsr.org/openicpsr/project/112670)
- [openICPSR project 112563 — Acemoglu-Johnson-Robinson Colonial Origins (comment)](https://www.openicpsr.org/openicpsr/project/112563)
- [openICPSR project 112564 — Acemoglu-Johnson-Robinson Colonial Origins (reply)](https://www.openicpsr.org/openicpsr/project/112564)
- [Harvard Dataverse — Chetty-Hendren neighborhood mobility replication](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/CEMFTJ)
- [Dell Mita project page](https://dell-research-harvard.github.io/projects/498mita)
- [AEA Data Editor — guidance on replicability checks](https://aeadataeditor.github.io/aea-de-guidance/reproducibility-checks)
