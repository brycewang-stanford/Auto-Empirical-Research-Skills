# Worked Example: Three-Level Specification for a Framing Experiment

A single hypothesis carried through each level required by the skill --
conceptual, operationalized, statistical -- with the theoretical and
empirical estimands, the regression specification, the SESOI, the
decision rule, and the tier classification.

**Substantive setting.** A 2-condition online survey experiment in a
U.S. adult sample. The treatment is a news excerpt that frames a
proposed carbon tax in *economic-cost* terms (prices rise, wages stall)
vs. a length-matched control excerpt on an unrelated topic (local
transit). The outcome is support for the carbon tax.

## 1. Conceptual hypothesis

> **H1 (conceptual).** Framing a carbon tax in terms of its near-term
> economic costs to households reduces public support for the tax,
> relative to a neutral information baseline.

The theoretical claim is that loss-framed cost information activates
short-horizon economic self-interest and dominates diffuse environmental
benefit considerations at the moment of policy evaluation.

## 2. Operationalized hypothesis

> **H1 (operationalized).** Respondents randomly assigned to the
> economic-cost frame will, on average, express lower support for the
> carbon tax on a 7-point Likert item (1 = strongly oppose, 7 =
> strongly support) than respondents assigned to the unrelated-topic
> control, measured 30--90 seconds after treatment exposure within the
> same survey block.

- **Treatment contrast:** economic-cost frame (T = 1) vs. unrelated
  transit passage of matched word count and reading grade (T = 0).
- **Outcome measure:** single pre-registered 7-point Likert item; no
  composite scale, no post-hoc recoding.
- **Unit of analysis:** individual respondent; one observation per
  unit.
- **Target population:** U.S. adult internet users reachable via a
  large opt-in panel; the sample yields a SATE. Generalization to the
  PATE requires the weighting assumptions stated in §4.
- **Information equivalence assumption (Stantcheva 2023):** the
  treatment shifts beliefs about the *economic cost* of the tax and
  nothing else. Violations would include the treatment also shifting
  beliefs about the tax's environmental effectiveness, the
  trustworthiness of the source, or the political coalition backing the
  policy. A manipulation check asks respondents to rate perceived
  household cost of the tax on an 11-point scale; a separate item asks
  perceived environmental effectiveness (used as a placebo check).

## 3. Statistical hypothesis

### Theoretical estimand (Lundberg, Johnson, & Stewart 2021)

Let $Y_i(1)$ be the potential Likert support score for respondent $i$
if exposed to the economic-cost frame and $Y_i(0)$ the potential score
if exposed to the control. The theoretical estimand is the SATE in the
realized sample:

$$
\tau_{\text{SATE}} \;=\; \frac{1}{n} \sum_{i=1}^{n} \big[Y_i(1) - Y_i(0)\big].
$$

This quantity is defined outside any statistical model; the regression
below is one way to estimate it.

### Empirical estimand

Under random assignment, $\tau_{\text{SATE}}$ is identified as the
difference in observed means
$E[Y_i \mid T_i = 1] - E[Y_i \mid T_i = 0]$ in the analytic sample
(respondents who complete the treatment and outcome items and pass the
attention check stated in the PAP).

### Regression specification

Pre-registered primary specification:

```
Y_i = beta_0 + beta_1 * T_i + epsilon_i
```

estimated by OLS with HC2 robust standard errors. Covariate
adjustment, if used, follows the Lin (2013) interacted specification
with pre-treatment demographics (age, education, 7-point party ID, and
pre-treatment environmental concern on a 5-point item); covariate
adjustment is specified *in the PAP* as a secondary estimator and is
not allowed to determine which set of covariates enters. The primary
estimand is $\beta_1 = \hat\tau_{\text{SATE}}$.

### Hypotheses and decision rule

- $H_0: \beta_1 \geq 0$ (treatment does not reduce support).
- $H_1: \beta_1 < 0$ (treatment reduces support).
- **Test:** one-sided t-test on $\beta_1$ at $\alpha = 0.025$
  (equivalent to a two-sided test at 0.05 with a pre-registered sign
  prediction).
- **SESOI:** $|\beta_1| = 0.25$ Likert scale points, or $d \approx 0.15$
  in standardized units given a prior SD of $\approx 1.65$ on the
  pre-test. Justification: (a) below 0.25 scale points the effect is
  smaller than a single-respondent response-style drift observed in
  pilot retest data, and (b) 0.15 SD is roughly the 25th percentile of
  framing-effect sizes reported in the meta-analysis benchmarks the
  team pre-specified. A smaller estimate would not meaningfully update
  the theoretical claim.
- **Power / sample size:** N = 1{,}800 (900 per arm) delivers 0.90
  power to detect the SESOI at $\alpha = 0.025$ one-sided; pre-computed
  via `pwr::pwr.t.test` and cross-checked with a `DeclareDesign`
  diagnosis of the full design (Blair, Cooper, Coppock, & Humphreys
  2019).

### Four-outcome interpretation (Lakens 2025)

Combine the directional test above with an equivalence test (TOST)
using bounds $\pm 0.25$ scale points:

| NHST result | TOST result | Interpretation                          |
|-------------|-------------|-----------------------------------------|
| Reject $H_0$ | Reject equiv. | Effect present in predicted direction  |
| Fail to reject | Reject equiv. | Effect trivially small (no support)  |
| Reject $H_0$ | Fail to reject | Effect present but inconclusive size |
| Fail to reject | Fail to reject | Inconclusive; under-powered         |

## 4. Tier classification and scope

- **Tier (Appelbaum et al. 2018 JARS-Quant):** Primary. Type I error
  controlled at 0.025 one-sided; Type II error controlled at 0.10 for
  the SESOI.
- **Scope condition, not a sub-hypothesis:** the team expects the
  effect to be larger among respondents with lower prior environmental
  concern. Because the theory does not make a precise directional claim
  about *how much* larger, this is registered as a descriptive scope
  exploration with uncorrected confidence intervals, not a confirmatory
  hypothesis (per §4 of the skill).
- **Disconfirming pattern:** a pre-registered $\hat\beta_1 \geq 0$ with
  the 95% CI excluding the SESOI magnitude would falsify the directional
  claim.

## Cross-references

- For PAP structure, decision-rule registration, and deviation
  protocols: hand this specification to `pre-registration-writing`.
- For JARS/DA-RT methods-section reporting of the primary/secondary
  classification and the four-outcome grid: route to
  `methods-reporting`.
- If the same question were fielded as a conjoint on a package of
  climate-policy attributes, the AMCE on the economic-cost frame level
  would be the analogous estimand: see `conjoint-design`.
