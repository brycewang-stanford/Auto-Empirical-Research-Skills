# English AI-signature pattern library (EN01–EN22)

For English-language empirical papers in economics, management, and the social
sciences. Severity: 🔴 must fix · 🟡 should fix · 🟢 optional.

Sources: adapted from Wikipedia's *Signs of AI writing* (WikiProject AI Cleanup),
the `humanizer_academic` and `academic-humanizer` skill lineages, and observed
LLM output on econ/management drafts — with all examples recast for empirical
social-science writing.

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

### EN19 · Uniform sentence rhythm (burstiness) 🔴 — highest impact

**Detection**: 5+ consecutive sentences of 20–30 words; low variance in sentence
length across a paragraph.

**Why first**: practitioner reports on academic humanizer skills consistently
find rhythm repair delivers the large majority of achievable AI-score reduction —
more than all vocabulary fixes combined.

**Fix**: per ~200 words, force at least one ≤8-word sentence and one ≥40-word
sentence. Short sentences ask questions or land conclusions ("The data say
otherwise."); long sentences carry evidence chains with subordinate clauses.
Vary paragraph lengths too — a two-sentence paragraph after two long ones reads
human.

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

## Severity priorities

**Must fix (🔴)**: EN01, EN02, EN04, EN05, EN06, EN10, EN11, EN15, EN16, EN19,
EN20, EN22
**Should fix (🟡)**: EN03, EN07, EN08, EN09, EN12, EN14, EN17, EN21
**Optional (🟢)**: EN13, EN18

Fix order: EN19 (rhythm) first, then the remaining 🔴 set, then 🟡 as time allows.
Empirical observation across the humanizer-skill lineage: repairing rhythm plus
the 🔴 set moves mainstream English detectors from 70%+ AI probability into the
ambiguous-to-human band; 🟡 fixes buy polish more than score.
