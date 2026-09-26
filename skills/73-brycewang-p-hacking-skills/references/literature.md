# Literature

What each source actually establishes, so claims can be sourced precisely.

## Foundational

**Simmons, Nelson & Simonsohn (2011),** "False-positive psychology", *Psych
Science* 22(11). Coins "researcher degrees of freedom". Shows via simulation and
two real experiments that four common flexibilities — outcome choice, sample
size, covariates, condition dropping — jointly push the false-positive rate from
5% to over 60%.

**Gelman & Loken (2013/2014),** "The garden of forking paths". The key
refinement: a researcher need never run multiple analyses to get an invalid
p-value. If the analysis chosen *would have been different* under different
data, the p-value is already wrong. This is why "I only ran one regression" is
not a defence.

**Kerr (1998),** "HARKing". Hypothesising after the results are known.

## Cataloguing and simulating

**Stefan & Schönbrodt (2023),** "Big little lies: a compendium and simulation of
p-hacking strategies", *Royal Society Open Science* 10:220346. Twelve strategies
with matched simulations. Two results this suite relies on: individual
strategies mostly land between 0.06 and 0.25 rather than the extreme rates often
quoted; and applied in sequence they reach roughly 0.5 with sharply diminishing
marginal returns. Also shows that lowering α to .005 helps in the presence of
p-hacking but by less than the tenfold reduction it would deliver in its
absence. Code: `astefan1/phacking_compendium` (R package `phackR`);
`scripts/phack/simulate.py` here is an independent Python re-implementation.

**Simonsohn, Simmons & Nelson (2020),** "Specification curve analysis", *Nature
Human Behaviour*. Descriptive and inferential statistics on all reasonable
specifications, including the joint permutation tests on the median effect,
the share significant and the share significant in the dominant direction —
implemented as `inference.ssn_joint_tests` and reported under `ssn_joint`.
Implementations: `masurp/specr`, `MUCollective/multiverse`.

**Steegen et al. (2016),** "Increasing transparency through a multiverse
analysis", *PPS*.

## Detecting

**Elliott, Kudrin & Wüthrich (2022),** "Detecting p-hacking", *Econometrica*
90(2):887–906. The theoretical basis for the detection module: absent p-hacking,
the p-curve is non-increasing, and for asymptotically normal statistics also
continuous and bounded. Proposes tests on each implication. R implementation:
`skranz/phack`.

**Elliott, Kudrin & Wüthrich (2024),** "The power of tests for detecting
p-hacking", *J. Business & Economic Statistics*. Combined upper-bound plus
monotonicity tests, and continuity tests, have the highest power — but power
against mild p-hacking is low for every test. Read alongside "When is p-hacking
detectable?" (arXiv 2506.20035).

**Brodeur, Lé, Sangnier & Zylberberg (2016),** "Star Wars: the empirics strike
back", *AEJ: Applied* 8(1). 50,000 tests from AER, JPE, QJE. The p-value
distribution is a two-humped camel: mass missing between .25 and .10 reappears
just below .05, amounting to 10–20% of marginally rejected tests.

**Brodeur, Cook & Heyes (2020),** "Methods matter: p-hacking and publication
bias in causal analysis in economics", *AER* 110(11). 13,440 tests across 25
journals. Selective publication and p-hacking are substantial in DiD and
especially IV; much smaller in RCT and RDD. Nearly a quarter of marginally
significant IV claims are judged misleading. This is the source for the
design-risk ordering in `references/econ-dof-maps.md`.

**Gerber & Malhotra (2008).** The caliper test.

**Adda, Decker & Ottaviani (2020),** "P-hacking in clinical trials and how
incentives shape the distribution of results across phases", *PNAS*
117(24):13386–13392. 12,621 primary-outcome p-values from 4,977 phase II and
III drug trials on ClinicalTrials.gov, converted to z = −Φ⁻¹(p/2). Three
findings this suite builds on. (i) No spike just past z = 1.96 anywhere, and
no density discontinuity in phase II: registered results look more honest
than published ones. (ii) A discontinuity at 1.96 in phase III for *small*
industry sponsors only — a level shift, not a spike, read as strategic
non-reporting of results below the line. (iii) The share significant rises
from 45.7% in phase II to 70.6% in phase III for industry sponsors (34.7% to
34.8% for non-industry) with a smooth distribution: sponsors continue to
phase III after promising phase II results, so the later stage inherits the
selection. A logit of continuation on the phase II z, and a reweighting of
the phase II distribution by the fitted continuation probabilities, explains
about 85% of the phase III excess for the ten largest sponsors and about 29%
for small ones; the unexplained 18.4 points for small sponsors is what is
left for selective reporting. Implemented as `detect.density_jump_test`,
`detect.phase_shift_test`, `detect.continuation_decomposition` and
`detect.phase_report`; simulated as `simulate.continuation_shift` and, at
the level of a single project, strategy `26_selective_continuation`; and
walked by the engine as the `split_sample` procedure. The lesson for the
red side is that *selection between stages is not p-hacking* — a fresh
confirmatory sample keeps its size — until the pilot is pooled into the
confirmatory test; the lesson for the blue side is that it leaves no
threshold signature at all.

**Cattaneo, Jansson & Ma (2020),** "Simple local polynomial density
estimators", *JASA* 115(531):1449–1455. The density-jump test in
`detect.density_jump_test`: regress the empirical CDF on a local polynomial
in (z − c) with kernel weights on each side of the cutoff; the density is the
fitted slope. No pre-binning, so no bin-alignment choice. Standard errors here
are bootstrapped rather than taken from their asymptotic formula. **McCrary
(2008),** *J. Econometrics* 142(2), is the binned predecessor.

**Simonsohn, Nelson & Simmons (2014),** "p-curve: a key to the file drawer",
*JEP: General*. The p-curve power estimate implemented in `detect.pcurve_power`.

## Estimators the engine implements, and why they are axes

**Imbens & Kalyanaraman (2012),** "Optimal bandwidth choice for the regression
discontinuity estimator", *REStud* 79(3). The MSE-optimal bandwidth in
`core.ik_bandwidth`. One of several "optimal" choices, which is what makes the
selector an axis.

**Calonico, Cattaneo & Titiunik (2014),** "Robust nonparametric confidence
intervals for regression-discontinuity designs", *Econometrica* 82(6). Bias
correction plus a variance that accounts for it. With b = h the robust
bias-corrected estimator equals the (p+1) local polynomial with its own SE,
which is how `rdd_inference: robust` is computed; `bias_corrected` without the
robust SE is the under-covering combination the paper warns against.

**Gardner (2022),** "Two-stage differences in differences", arXiv 2207.05943.
Fit unit and time effects on untreated observations, remove them everywhere,
regress the residual on treatment. `did_estimators: did2s`.

**Cengiz, Dube, Lindner & Zipperer (2019),** "The effect of minimum wages on
low-wage jobs", *QJE* 134(3). The stacked clean-control design.
`did_estimators: stacked`.

**Goodman-Bacon (2021),** "Difference-in-differences with variation in
treatment timing", *J. Econometrics*. Why TWFE under staggered adoption is a
weighted average of 2×2 comparisons including forbidden ones, and therefore
why the comparison group is an axis. **Callaway & Sant'Anna (2021)**,
**Sun & Abraham (2021)**, **Borusyak, Jaravel & Spiess (2024)** and
**de Chaisemartin & D'Haultfœuille (2020)** are the alternatives the taxonomy
names; the engine ships the two that need no additional machinery.

**Anderson & Rubin (1949).** The weak-instrument-robust test recorded as
`ar_p` for every IV specification. **Andrews, Stock & Sun (2019),** "Weak
instruments in IV regression: theory and practice", *Annual Review of
Economics*, on why screening on the first-stage F invalidates second-stage
inference.

## Correcting

**Romano & Wolf (2005),** "Exact and approximate stepdown methods for multiple
hypothesis testing", *JASA*. The stepdown procedure in `inference.romano_wolf`.

**Li & Ji (2005),** "Adjusting multiple testing in multilocus analyses using the
eigenvalues of a correlation matrix", *Heredity*. The effective-test count in
`inference.effective_tests`.

**Benjamini & Hochberg (1995).** FDR control.

**Cameron, Gelbach & Miller (2011),** "Robust inference with multiway
clustering", *JBES*. Source of the two-way variance estimator — and of the
warning that it is not guaranteed positive semi-definite, which is why
`flag_nonpsd_vcov` exists.

**McCloskey & Michaillat (2026),** "Critical values robust to p-hacking",
*Review of Economics and Statistics*. Critical values that remain valid when
the researcher has searched. Code: `pmichaillat/p-hacking`.

## Agents

**Asher, Malzahn, Paschal, Persano, Myers & Hall (2026),** "Do Claude Code and
Codex p-hack? Sycophancy and statistical analysis in large language models".
640 runs, two frontier coding agents, four published null-result papers, 2 × 4
factorial over research framing and significance pressure. Three findings this
suite is built around: standard prompting produces stable textbook-default
estimates even with a directional prior; explicit significance pressure triggers
refusal, named as misconduct; a reframing of specification search as uncertainty
reporting bypasses the refusal entirely and produces nested loops ranked by
significance. Susceptibility tracks design flexibility: selection-on-observables
≈ RDD > DiD > RCT. Replication archive: `janetmalzahn/llm-phacking`.

**Baumann et al. (2025).** LLM-based text annotation is steerable to almost any
desired significant result — the measurement-side analogue.

## Adjacent tooling

`nicebread/p-hacker` (teaching Shiny app), `shoal-rat/econoclast` (adversarial
referee), `bluesHeart/PhackingDetect` (PDF screening),
`kadubon/audit-closed-ai-scientist` (audit-closed protocols for autonomous
research agents), `JesseRWeigel/forking-paths` (multiverse simulator).
