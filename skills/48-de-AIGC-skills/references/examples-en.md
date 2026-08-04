# English before/after pairs (8 cases)

Organized by empirical-paper section; each case lists the `patterns-en.md` rules
it fires. Chinese counterparts: `examples-zh.md`.

---

## Case 1 · Abstract (EN01, EN12, EN16)

### ❌ AI draft

> This study comprehensively examines the pivotal role of digital transformation
> in firm performance. Using extensive panel data and rigorous econometric
> methods, we demonstrate that digital transformation significantly enhances
> firm productivity. Our findings have important theoretical and practical
> implications for scholars and policymakers alike.

### ✅ Rewritten

> Does digital transformation raise productivity, or do productive firms simply
> digitize first? Using a 2015 pilot program that assigned digitalization
> subsidies by a formula firms could not manipulate, we estimate that treated
> firms' TFP rose 6.8% within three years (N = 2,341 listed firms, 2014-2022).
> Mechanism tests attribute most of the gain to management-process
> reorganization rather than technology adoption, consistent with Bloom et al.
> (2012) and at odds with adoption-centric accounts.

**Fixes**: reverse-causality question replaces "pivotal role" framing; three
concrete numbers replace "extensive" and "significantly"; a named literature
tension replaces "important implications".

---

## Case 2 · Introduction opener (EN05, EN04)

### ❌ AI draft

> In recent years, artificial intelligence has attracted increasing attention
> from scholars and policymakers. Studies have shown that AI has profound
> impacts on labor markets across various domains.

### ✅ Rewritten

> Acemoglu and Restrepo published two QJE papers on AI and labor within three
> years — and reached opposite emphases. The 2020 paper stresses displacement;
> the 2022 paper, reinstatement. Which force dominates is an empirical question,
> and it is the question this paper takes to Chinese manufacturing data.

**Fixes**: kills the "In recent years" formula (EN05); replaces "Studies have
shown" with named authors, years, and a real disagreement (EN04); short-long
sentence rhythm (EN19).

---

## Case 3 · Literature review (EN17, EN04)

### ❌ AI draft

> Many studies have examined FDI spillovers (Aitken and Harrison 1999; Javorcik
> 2004; Keller 2010; Havranek and Irsova 2011). Furthermore, various scholars
> have explored the role of absorptive capacity. Moreover, recent research has
> highlighted the importance of supply chain linkages.

### ✅ Rewritten

> The FDI spillover literature splits on sign. Aitken and Harrison (1999) find
> negative horizontal effects in Venezuelan plants; Javorcik (2004) finds gains,
> but only through backward linkages to suppliers. Havranek and Irsova's (2011)
> meta-analysis suggests the disagreement is mostly about specification. Our
> within-supply-chain data let us hold specification fixed and test the linkage
> channel directly.

**Fixes**: citation dump becomes an argued disagreement (EN17); Furthermore/
Moreover chain deleted (EN06); ends by positioning this paper's data against
the split.

---

## Case 4 · Empirical strategy (EN13, EN10)

### ❌ AI draft

> The 2015 reform serves as an ideal natural experiment for our identification
> strategy, which clearly establishes the causal effect of deregulation on firm
> entry.

### ✅ Rewritten

> The 2015 reform is a plausible natural experiment. Eligibility followed a
> pre-announced revenue formula, and bunching tests show no manipulation around
> the threshold (Figure 2). Identification still requires that untreated firms
> track treated firms' counterfactual trend; Section 5.2 probes this with
> placebo reforms and pre-trend tests.

**Fixes**: "serves as an ideal" → "is a plausible" (EN13, EN10); the
identification claim is argued with evidence and its remaining assumption is
stated, which is how referees actually read strategy sections.

---

## Case 5 · Baseline results (EN02, EN11)

### ❌ AI draft

> Table 3 shows that the coefficient is highly significant and positive,
> demonstrating the strong effect of deregulation, highlighting the robustness
> of our findings and underscoring the importance of entry barriers.

### ✅ Rewritten

> Column (1) of Table 3 reports the baseline: deregulated counties saw entry
> rise 12.4% (s.e. 3.1). Adding county and industry-year fixed effects in
> columns (2)-(4) moves the point estimate between 10.8% and 13.1%. The
> magnitude is about half of what Branstetter et al. (2014) report for
> Portugal, plausibly because Chinese entry was already partially liberalized.

**Fixes**: adjectives replaced by coefficients and standard errors (EN11); both
"-ing" tails deleted (EN02); magnitude benchmarked against a named paper, which
is a distinctly human move.

---

## Case 6 · Mechanisms (EN06, EN07)

### ❌ AI draft

> Moreover, we explore the underlying mechanisms. First, deregulation reduces
> registration costs. Second, it lowers compliance burdens. Third, it improves
> credit access. Furthermore, these three channels jointly explain the entry
> response, demonstrating the multifaceted nature of the reform.

### ✅ Rewritten

> What drives the entry response? Registration costs fall mechanically — the
> reform cut required capital to zero — but that alone cannot explain why entry
> rose most in credit-scarce counties. Column (3) of Table 6 shows the
> interaction: entry effects are 2.1 times larger where pre-reform loan
> rejection rates were above the median. Credit access, not paperwork, appears
> to be the binding margin.

**Fixes**: ordinal triad dissolved into an argued comparison (EN07); Moreover/
Furthermore deleted (EN06); a question opens the paragraph and a short verdict
sentence closes it (EN19).

---

## Case 7 · Discussion & limitations (EN15, EN16)

### ❌ AI draft

> Our findings provide valuable insights for policymakers and fill an important
> gap in the literature. However, this study has limitations. Future research
> could explore other contexts and employ additional methods.

### ✅ Rewritten

> Two limitations bound what these estimates can say. Our eight-year window
> cannot distinguish permanent entry gains from intertemporal displacement —
> firms that would have entered in 2024 entering in 2019 instead. And because
> the reform bundled registration and capital rules, we cannot fully separate
> their contributions; the credit-interaction results favor the capital channel
> but do not settle it. Matched firm-bank data could; ours end in 2022.

**Fixes**: generic boilerplate replaced by design-specific limitations (EN16);
each limitation is a real threat a referee would raise, stated plainly with one
hedge each (EN15).

---

## Case 8 · Conclusion (EN22)

### ❌ AI draft

> In conclusion, this study demonstrates that deregulation significantly
> increases firm entry. The findings underscore the importance of reducing entry
> barriers and provide important implications for policymakers. Future research
> can further explore the mechanisms.

### ✅ Rewritten

> Entry barriers, not credit supply alone, were the binding constraint on
> Chinese firm creation — that is the reading our evidence supports. It leaves
> open a harder question: whether the marginal entrants create jobs or churn.
> Our registry data see entry, not survival. Linking the reform to five-year
> exit and employment records is, to us, the natural next step, and one this
> pilot's staggered rollout makes feasible.

**Fixes**: no re-abstracting (EN22); introduces genuinely new content — an open
question, a data limitation, a concrete next design; "to us" is a researcher-
voice marker no template produces.

---

## Usage notes

- Do not transplant these sentences into your paper. The *moves* transfer —
  the numbers, citations, and tensions must come from your own research.
- After rewriting, self-score with `scoring.md` (English thresholds at the top).
