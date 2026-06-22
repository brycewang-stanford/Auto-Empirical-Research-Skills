# Example — Body-Section Narration (Data, Results, Mechanisms)

A worked example of the body-writing rules in
`skills/aer-paper-body/SKILL.md`, using the same fictional paper as
`intro-example.md`:

> *Broadband Expansion and Local Wage Inequality:
>  Evidence from the FCC's Connect America Fund*

All numbers are invented but internally consistent with the introduction
example (headline effect: 4.2 log points, s.e. 1.1). Read this alongside
`docs/style-guide.md` for the sentence-level rules each excerpt applies.

---

## Excerpt 1 — The Sample Funnel (Data Section)

> Our raw extract covers 31,184 ZIP codes observed annually from 2010 to
> 2024. We exclude ZIP codes with fewer than 500 working-age residents
> (4,212), those already at the FCC's 25/3 Mbps benchmark before 2015 and
> hence never eligible for auction funding (7,861), and those with
> suppressed ACS wage cells in more than three years (1,287). The analysis
> sample is 17,824 ZIP codes — 267,360 ZIP-code-years — of which 6,418
> receive Connect America funding during our window.

*Why this works:* every drop has a count and a rationale; the arithmetic
reconciles (31,184 − 4,212 − 7,861 − 1,287 = 17,824); the panel
multiplication is checkable (17,824 × 15 = 267,360). `aer-consistency`
Audit 2 verifies exactly these identities against Table 1 and the
replication package.

---

## Excerpt 2 — The Headline Result (Results Section)

> Broadband expansion widens local wage inequality. Table 3 reports our
> Callaway-Sant'Anna estimates: funding raises the within-ZIP-code 90/10
> log wage ratio by 4.2 log points (s.e. 1.1) over the six years following
> deployment — 4.3 percent, or 0.12 standard deviations of the
> cross-sectional 90/10 distribution in 2014. The estimate is stable as we
> move from the baseline specification (column 1) to commuting-zone-by-year
> fixed effects (column 3) and an auction-eligibility matched sample
> (column 4); it is the column 4 estimate we carry through the paper. For
> scale, the effect is roughly one-third of the 90/10 widening attributed
> to Chinese import competition in comparable local labor markets over a
> similar horizon.
>
> The widening comes from the top of the distribution. Decomposing the
> ratio (Table 4), 90th-percentile wages rise 3.6 log points while
> 10th-percentile wages are statistically indistinguishable from zero; the
> 95 percent confidence interval for the 10th percentile excludes losses
> larger than 1.0 log point, so broadband does not appear to harm
> low-wage workers — it leaves them behind.

*Why this works:*

| Rule applied | Where |
|---|---|
| Finding-first sentence, not "Table 3 presents..." | Opening sentence of each paragraph |
| All three magnitude conversions (exact percent, vs. SD, vs. literature) | "4.3 percent... 0.12 standard deviations... one-third of" |
| Specification walk with a named headline column | "stable as we move... column 4 we carry through" |
| Null result reported as what the CI rules out | "excludes losses larger than 1.0 log point" |
| Interpretation sentence that earns the paragraph | "does not harm — it leaves them behind" |

---

## Excerpt 3 — The Back-of-Envelope (Results Section Close)

> The estimates imply a sizable distributional cost per program dollar.
> Phase II disbursed $1.49 billion annually across funded ZIP codes
> housing 9.1 million workers, or $164 per covered worker per year. Our
> column 4 estimate implies the program moved $620 of annual wage growth
> per worker from the area median to the top decile (4.2 log points ×
> $14,800 baseline top-decile premium). Whether this redistribution is an
> acceptable price for the aggregate gains in Section V's benefit-cost
> framework depends on the welfare weights; under equal weights the
> program passes, under weights that prioritize the bottom quartile it
> does not.

*Why this works:* one calculation, every input sourced in-line, the chain
visible and multipliable by the reader, and an honest statement of what the
number does and does not settle.

---

## Excerpt 4 — Mechanisms Organized by Channel

> Three channels could produce top-skewed gains: skill-biased adoption
> (broadband complements high-skill tasks), firm sorting (connected areas
> attract high-wage employers), and simple compositional change (high
> earners migrate in). The evidence favors skill-biased adoption. Effects
> concentrate in tradeable-services occupations — 7.1 log points, against
> 0.4 (s.e. 1.2) in retail and construction (Table 5) — exactly the
> occupations where remote delivery of output became feasible. Firm
> sorting predicts entry of new high-wage establishments; we find no
> effect on establishment counts or entry rates (Table 6, columns 1-2).
> Composition predicts migration responses; in-migration of college
> graduates is small and statistically indistinguishable from zero, and
> our estimates are unchanged in a balanced panel of never-moving workers
> (Table 6, columns 3-5). We read the pattern as most consistent with
> skill-biased technology adoption, while noting that the design
> identifies the reduced-form effect, not the channel decomposition.

*Why this works:* channels named up front, including the two being ruled
out; each rival channel gets its sharpest prediction and a direct test;
the closing sentence calibrates the claim ("most consistent with") and
separates mechanism evidence from design-based identification, as
`aer-paper-body` and `aer-identification` require.

---

## Counterexample — The Table Walk-Through

The same headline result, written the way referees complain about:

> Table 3 presents the results of estimating equation (1). Column 1 shows
> the baseline specification. The coefficient on broadband is 0.045 and
> is significant at the 1% level. Column 2 adds controls and the
> coefficient is 0.044. Column 3 adds commuting-zone-by-year fixed
> effects and the coefficient becomes 0.043. Column 4 uses the matched
> sample and the coefficient is 0.042, also highly significant. These
> results suggest that broadband may play an important role in shaping
> local wage dynamics.

What is wrong, line by line:

- No sentence states the economic finding; the reader does the work
- Coefficients recited without units — log points? percent? of what?
- "Significant at the 1% level" carries the narration; magnitude never
  interpreted, never benchmarked
- "Highly significant" and "may play an important role" — both on the
  `docs/style-guide.md` blacklist
- The closing sentence hedges a design-identified effect into mush while
  claiming nothing checkable

---

## How to Use This Example

1. Draft each results paragraph with the three-part anatomy from
   `skills/aer-paper-body/SKILL.md`: finding → evidence → interpretation.
2. Run the magnitude conversions before writing the paragraph, not after —
   the conversions usually *are* the interpretation.
3. After drafting, reverse-outline: the first sentences of the results
   paragraphs, read alone, should narrate the paper's entire empirical
   arc. In the excerpts above they read: "Broadband expansion widens local
   wage inequality. The widening comes from the top of the distribution.
   The estimates imply a sizable distributional cost per program dollar."
4. Hand the draft to `aer-consistency` to verify every quoted number
   against the tables, then to `aer-referee-sim` for the adversarial pass.
