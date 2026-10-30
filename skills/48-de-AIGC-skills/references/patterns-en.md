# English AI-signature pattern library (EN01–EN30)

For English-language empirical papers in economics, management, and the social
sciences. Severity: 🔴 must fix · 🟡 should fix · 🟢 optional.

Sources: adapted from Wikipedia's *Signs of AI writing* (WikiProject AI Cleanup),
the `humanizer_academic` and `academic-humanizer` skill lineages, and observed
LLM output on econ/management drafts — with all examples recast for empirical
social-science writing. EN23–EN30 and the EN08 / EN12 / EN19 revisions
(2026-10) come from a read of the most-starred English humanizer skills —
blader/humanizer, hardikpandya/stop-slop, conorbronsdon/avoid-ai-writing,
AIScientists-Dev/academic-humanizer and Nanako0129/sepia (all MIT); what was
taken and what was deliberately left out is in `lineage.md`.

**Deterministic subset**: `python3 scripts/aigc_audit.py audit draft.md` runs
every rule a regex can see (EN01–06, 08, 10–12, 14, 16–17, 23–29) after masking
quotations, math, `\cite{}` and tables, and prints the rest as "left to the
model". A hit is a place to look, not a verdict.

---

## Preserve-list — do NOT flag these 保留清单

Standard academic phrasing is not an AI tell. Removing it makes text *worse* and
reads as over-corrected. Keep, unless stacked (3+ in a paragraph) or citation-free:

- Transitions: "Notably, …", "Importantly, …", "In contrast, …", "Specifically, …"
- Attribution *with citations or data*: "Prior studies have shown that … (Smith
  2020; Li 2023)", "A growing body of evidence indicates … [refs]"
- Technical register: "statistically significant at the 1% level", "robust to",
  "identification strategy", "point estimate", "we cannot reject the null"
- Evidence-tied hedges: "suggests", "is consistent with", "may indicate"
- First-person plural "we" — standard in modern empirical writing
- Passive voice in methods sections ("Data were collected from…")
- "is associated with" for correlational evidence — the *correct* verb (Step 2),
  even though general-prose humanizers flag it as vague
- The roadmap paragraph ("Section 2 describes…") — a convention, not padding
- "robust", "comprehensive" in their technical senses ("robust standard
  errors", "comprehensive income")

**Rule of thumb**: a phrase followed by a citation, a number, or a test statistic
is legitimate academic writing.

---

## Content patterns

### EN01 · Inflated significance 🔴

**Watch for**: plays a pivotal/crucial/vital role, underscores/highlights the
importance, represents a paradigm shift, evolving landscape, key turning point,
testament to, far-reaching implications, in today's rapidly changing world

**Problem**: LLMs puff up every finding into a landmark.

- ❌ "Digital transformation plays a pivotal role in the evolving landscape of
  firm performance, underscoring the critical importance of technology adoption."
- ✅ "In our sample, a one-standard-deviation increase in the digitalization
  index is associated with 4.3% higher TFP (t = 3.81)."

### EN02 · Superficial "-ing" tails 🔴

**Watch for**: sentence-final ", highlighting…", ", underscoring…",
", emphasizing…", ", showcasing…", ", reflecting…", ", contributing to…"

**Problem**: participle tails bolt fake analysis onto a finding.

- ❌ "The coefficient remains stable across specifications, highlighting the
  robustness of our identification strategy and underscoring the broad
  applicability of our findings."
- ✅ "The coefficient remains between 0.038 and 0.045 across columns (2)–(4)."

### EN03 · Promotional language 🟡

**Watch for**: groundbreaking, remarkable, striking, dramatic, impressive,
comprehensive framework, cutting-edge, state-of-the-art, rich (figurative)

**Problem**: journal prose is flat by design; adjectives that sell are a tell.

- ❌ "Our groundbreaking difference-in-differences design yields remarkable
  evidence of a dramatic policy impact."
- ✅ "The difference-in-differences estimate implies a 12% decline in entry
  (95% CI: 7%–17%)."

### EN04 · Vague attribution 🔴

**Watch for**: Studies have shown, Research suggests, Experts argue, It is
widely believed, Scholars have noted — **with no citation attached**

**Problem**: LLMs attribute claims to nobody. Empirical readers ask "which study?"

- ❌ "Studies have shown that financial constraints hinder firm innovation."
- ✅ "Financially constrained firms patent less; Hall and Lerner (2010) survey
  the evidence, and Howell (2017) finds grants raise patenting by 30% among
  constrained applicants."

### EN05 · Formulaic openers 🔴

**Watch for**: "In recent years, X has attracted increasing/growing attention",
"With the rapid development of…", "In today's globalized economy…",
"Despite recent advances…"

**Problem**: the single most recognizable LLM opening move, in both languages.

- ❌ "In recent years, the digital economy has attracted increasing attention
  from scholars and policymakers alike."
- ✅ "Between 2015 and 2022, Chinese cities designated as 'big data pilot zones'
  attracted 38% of national venture funding. Whether the designation caused the
  inflow is contested (Chen 2023; Zhou and Li 2024)."

### EN06 · Connective chains 🔴

**Watch for**: consecutive sentences/paragraphs opening with Moreover,
Furthermore, Additionally, In addition, Also

**Problem**: mechanical scaffolding substitutes for argumentative flow.

**Fix**: delete the connective and relay semantically — open the next sentence
with the key noun of the previous one. Keep at most one explicit additive
connective per paragraph.

### EN07 · Rule-of-three padding 🟡

**Watch for**: every list has exactly three items; triads of abstract nouns
("efficiency, innovation, and growth")

**Fix**: keep the two items you can support with evidence; cut or elaborate the
third. Vary list lengths across the paper.

### EN08 · Negative parallelism 🟡

**Watch for**: "not only… but also…", "This is not just X; it is Y",
"…does not merely…, it…"

- ❌ "The reform not only reduced entry costs but also reshaped the competitive
  landscape."
- ✅ "The reform reduced entry costs. Competition effects appear only in
  downstream markets (Table 6)."

**Staged contrast** (same family, the tell upstream ranks highest): a contrast
split across two sentences ("This does not mean X. It means Y."), "The
question is not X; it is Y", a run of negations before the real claim.

- ❌ "The effect is not driven by demand. It is driven by credit."
- ✅ "Effects concentrate where pre-reform rejection rates were high (Table 6,
  col. 3)."

**Keep** a contrast that rules out a *named* alternative channel with evidence
("Demand-side explanations predict X; Table 5 shows the opposite").

### EN09 · Elegant variation 🟡

**Watch for**: cycling synonyms for one concept — firms/enterprises/companies/
organizations; respondents/participants/subjects; effect/impact/influence

**Problem**: repetition penalties make LLMs rotate synonyms; academic writing
fixes one term per concept and repeats it.

**Fix**: pick one term per concept (define it once) and use it consistently.

### EN10 · Overclaiming verbs 🔴

**Watch for**: prove(s), demonstrate(s), establish(es), confirm(s), guarantee(s),
"clearly shows" — attached to observational or suggestive evidence

**Problem**: verb strength must match design strength (see SKILL.md Step 2).

- ❌ "This proves that minimum wage increases cause unemployment."
- ✅ "These estimates are consistent with modest disemployment effects at the
  bottom of the wage distribution."

**Do not overcorrect**: a clean RCT or sharp RD *may* state "the program
reduced dropout by 8 percentage points" — direct verbs for direct evidence.

### EN11 · Unsupported "significant(ly)" 🔴

**Watch for**: "significantly improves/reduces" with no test statistic nearby;
conflating statistical and economic significance

- ❌ "The coefficient is highly significant, demonstrating a strong effect."
- ✅ "The coefficient (0.043, s.e. 0.011) is significant at the 1% level; the
  implied elasticity of 0.12 is modest relative to the 0.3–0.5 range in prior
  work."

### EN12 · Empty intensifiers 🟡

**Watch for**: comprehensive, extensive, thorough, various, numerous, a wide
range of, multifaceted, holistic

- ❌ "We conduct comprehensive robustness checks using various alternative
  specifications."
- ✅ "Four concerns could threaten identification; we address each in turn
  (Section 6)."

**Process narration** (same family): "meticulously cleaned", "rigorously
verified to ensure accuracy", "carefully constructed". Say what was done:
"We drop 312 firm-years with negative assets and winsorize at 1%."

### EN13 · Copula avoidance 🟢

**Watch for**: serves as, stands as, acts as, functions as, represents (for "is")

- ❌ "The 2015 reform serves as an ideal natural experiment."
- ✅ "The 2015 reform is a plausible natural experiment: assignment was
  formula-based and firms could not manipulate eligibility."

### EN14 · AI vocabulary 🟡

**Watch for** (post-2023 frequency spike; they co-occur): delve, intricate,
interplay, tapestry, landscape (abstract), realm, pivotal, crucial, foster,
leverage (verb), showcase, underscore (verb), garner, seamless, robustly nuanced

**Fix**: replace with the plain term — examine, complex, interaction, setting,
important, encourage, use, show. One instance is fine; clusters are the tell.

### EN15 · Miscalibrated hedging (both directions) 🔴

**Two failure modes**:

- **Stacked hedges** — "may potentially suggest the possibility that X could
  contribute to…" → one hedge: "suggests that X may raise…"
- **Missing hedges** — observational finding stated as causal fact. Add exactly
  one evidence-tied hedge: "is associated with", "consistent with".

**Calibration rule**: one hedge per claim, chosen by design strength; never zero
for observational claims, never three.

### EN16 · Generic contributions and conclusions 🔴

**Watch for**: "Our findings have important implications for policymakers and
practitioners", "This study contributes to the literature in three ways" followed
by restated results, "fills a gap in the literature"

- ❌ "This study fills an important gap and provides valuable insights for
  policymakers."
- ✅ "Relative to Duflo (2001), our design separates supply- from demand-side
  responses; the policy implication is that subsidies targeting only
  construction would forgo roughly half the enrollment gain."

### EN17 · Citation dumping 🟡

**Watch for**: five-plus references bracketed after a bland claim, none engaged

- ❌ "Many studies examine FDI spillovers (Aitken and Harrison 1999; Javorcik
  2004; Keller 2010; Havranek and Irsova 2011; Alfaro 2017)."
- ✅ "Evidence on horizontal FDI spillovers is mixed: Aitken and Harrison (1999)
  find negative effects in Venezuela, while Javorcik (2004) finds gains only
  through backward linkages — a pattern our within-supply-chain data can test
  directly."

### EN18 · False ranges 🟢

**Watch for**: "from X to Y" where X and Y are not on a scale

- ❌ "Our results matter for everything from industrial policy to household
  welfare."
- ✅ Name the two audiences and one sentence each on why.

---

## Style and rhythm patterns

### EN19 · Uniform sentence rhythm 🔴

**Detection**: 4+ consecutive sentences within ±15% of each other's length;
evidence chains chopped into medium-length sentences. `aigc_audit.py` reports
`similar_length_runs_4plus`, `long_share` and `short_share` — report only.

**What the evidence says (2026-10 revision).** The old rule here ("per 200
words, force one ≤8-word and one ≥40-word sentence") is withdrawn:

- No study supports a fixed spread threshold. At a 1% false-positive rate, the
  sentence-length coefficient of variation catches 2.5% of machine text
  (AUROC 0.521; sepia `research/rhythm-syntax.md`).
- Recent models write too *few short* sentences (1–4% vs 32–33% for humans)
  and run longer on average, so "add a ≥40-word sentence" pushes the wrong way.
- Prompting a model to "vary sentence length" *raised* detector accuracy
  (sepia, BAIDYA-2026). Mechanical alternation is worse than no edit.

**Fix**: let length follow content. Merge adjacent sentences that make one
point into a single sentence that carries the evidence chain; split a
sentence that makes two claims. Do not manufacture slogan sentences ("The data
say otherwise.") or a rhetorical question answered in the next breath — both
are tells in their own right (EN26, stop-slop `structures.md`). Where an author
sample exists, match *its* long/short mix; otherwise use 3–5 recent papers in
the target journal as the baseline.

### EN20 · Typographic tells 🔴

- **Em dashes (—)**: replace every one — commas for appositives, parentheses for
  asides, periods/semicolons for clause breaks. Zero em dashes in final output;
  verify with a literal search before delivering.
- **Curly quotes** ("…") → straight quotes in source files.
- **Title Case Headings** → sentence case ("Robustness checks", not "Robustness
  Checks") unless the venue's style says otherwise.

### EN21 · LLM word-choice tells 🟡

| LLM habit | Academic norm |
|---|---|
| "linked to" | "associated with" |
| "via" | "through" |
| "yield(ed)" (results) | "produce(d)", "provide(d)" |
| "Beyond X, …" (transition) | "In addition to X, …" |
| non-locative "where" (", where the effect was larger") | "with", new sentence |
| "in which" as default fix for "where" | prefer "with"-phrase or restructure |

### EN22 · Echo-chamber conclusion 🔴

**Detection**: the conclusion re-states the abstract with the same vocabulary
(cosine similarity of word frequencies > 0.75); "limitations and future research"
boilerplate that any paper could carry.

**Fix**: the conclusion must add something — an unresolved question specific to
this design, a policy margin the estimates cannot speak to, the next dataset that
would settle what this one cannot. Limitations must be *this paper's* limitations
("our eight-year window cannot identify long-run effects"), not generic ones.

---

## 2026-10 additions (EN23–EN30)

### EN23 · Chatbot and drafting residue 🔴

**Watch for**: chat wrappers ("Certainly! Here is a revised…", "I hope this
helps", "Let me know if…"); flattery ("Great question", "You're absolutely
right"); knowledge-cutoff talk ("as of my last update", "based on available
information"); tour-guide openers ("Let's dive in", "Here's what you need to
know"). An author's own dated statement ("as of 2023, 41 provinces…") is fine.

- ❌ "Certainly! Below is the revised results section. Table 3 shows… I hope
  this helps!"
- ✅ Keep only the Table 3 sentences.

Source: blader/humanizer §4, §22, §23; avoid-ai-writing P0 tier.

### EN24 · Generation artifacts 🔴

**Watch for**: Markdown leaking into `.tex` / `.docx` (`**bold**`, `##`,
bold-label bullets "- **Key finding:** …"); citation-markup leaks
(`[oaicite:2]`, `【4†source】`, `turn0search3`, `utm_source=chatgpt.com` in a
reference URL); unfilled placeholders ("[Author, 20XX]", "XX%", "[insert
coefficient]").

**Fix**: remove the markup; strip tracking parameters from URLs; **flag
placeholders for the author — never fill them in**.

Source: blader §19; avoid-ai-writing `detector/CATEGORIES.md`.

### EN25 · Novelty padding 🟡 (🔴 if stacked)

**Watch for**: "to the best of our knowledge" + "first to"; "for the first
time"; "novel" more than once per section; universal gap claims ("no study
has examined…").

- ❌ "To our knowledge, this is the first paper to use a novel dataset to
  examine…"
- ✅ "Aaronson et al. (2018) use county aggregates; establishment-level
  registrations let us separate entry from relocation."

Source: academic-humanizer; stop-slop `structures.md`.

### EN26 · Takeaway closers 🟡

**Watch for**: a paragraph-final sentence that tells the reader what the
numbers "show" ("This finding underscores the critical role of…", "Taken
together, these results highlight…"); one-sentence paragraphs restating the
previous one; the same closer after every subsection.

- ❌ "…0.043 (s.e. 0.011). This underscores the critical role of credit."
- ✅ Cut it, or replace it with a fact the table does not show.

Source: blader §2; stop-slop; sepia `discourse-pass.md` (the key line always
closing the paragraph is a position tell that survives paraphrase).

### EN27 · Boilerplate emphasis and filler 🟡

**Watch for**: "It is worth noting that", "It should be emphasized that", "It
is important to note", "in order to", "At its core", "When it comes to". A
single "Notably," stays (preserve-list).

- ❌ "It is worth noting that, in order to address endogeneity, we…"
- ✅ "To address endogeneity, we…"

### EN28 · Vague-magnitude hedges 🟡 (🔴 in abstract / results)

**Watch for**: somewhat, relatively, fairly, to some extent, quite, "large" /
"substantial" with no number in the sentence; "The implications are
significant."

- ❌ "Treated firms perform relatively better."
- ✅ "Treated firms' ROA rises 1.2 pp (Table 4, col. 2) on a pre-period mean of
  6.1%."

Prefer a comparison to the strongest prior estimate over a bare adjective
(academic-humanizer). The number must already be in the paper.

### EN29 · Arguing with no one 🟡

**Watch for**: "One might argue…", "Some may argue", "This is not to say",
"To be clear" — when the objection is never answered with evidence. A real
referee concern answered with a test is the opposite of this tell.

- ❌ "One might argue the results reflect chance; this is unlikely given our
  robustness."
- ✅ "Randomly reassigned reform years give estimates ≥ 0.043 in 7 of 1,000
  draws (Figure 5)."

### EN30 · Repeated openers 🟢

**Watch for**: three or more consecutive sentences with the same subject ("We…
We… We…"); the same section-transition formula every time ("Turning to…").

**Fix**: merge, or lead with the result instead of the actor.

---

## Severity priorities

**Must fix (🔴)**: EN01, EN02, EN04, EN05, EN06, EN10, EN11, EN15, EN16, EN19,
EN20, EN22, EN23, EN24
**Should fix (🟡)**: EN03, EN07, EN08, EN09, EN12, EN14, EN17, EN21, EN25, EN26,
EN27, EN28, EN29
**Optional (🟢)**: EN13, EN18, EN30

Fix order: EN23 / EN24 first (residue and artifacts are unambiguous and cheap),
then the claim-level 🔴 set (EN10, EN11, EN15, EN16 — these change what a
referee believes), then EN19 by merging and splitting, then 🟡 as time allows.

**No detector promise.** Earlier versions of this file said the 🔴 set "moves
mainstream detectors from 70%+ into the human band". No measurement backs that
sentence, so it is gone. avoid-ai-writing measured its own composite score at
paragraph-level ROC-AUC 0.501 (`PROOF.md`); a cleaner manuscript is the goal,
not a number.

---

## Not adopted from general-prose humanizers

These are good rules for blog posts and wrong for papers:

- stop-slop's blanket bans — "kill all adverbs", "no hedges", "no passive",
  "two items beat three". They destroy calibrated hedging (EN15) and methods
  passives.
- Flagging "associated with" as vague (blader §14) — it is the correct verb
  for correlational evidence.
- Removing en dashes (blader §8) — breaks ranges like 2014–2022.
- Deleting every "Notably," (academic-humanizer 2.10) — on our preserve-list.
- Splitting every sentence over 30 words (academic-humanizer 2.11) —
  conflicts with letting length follow content.
- "False agency" for "the market rewards…" (stop-slop) — ordinary economics.
- Personality / opinion / humour voice profiles — not a register any journal
  accepts. blader §26 ("lead with the decision") does fit **referee response
  letters**; use it there.
