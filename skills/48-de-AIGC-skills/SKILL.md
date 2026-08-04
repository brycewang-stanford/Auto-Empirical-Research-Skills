---
name: de-aigc-skills
description: 中英双语学术降 AIGC / bilingual academic de-AIGC skill. Removes AI-generated writing signatures from empirical papers in economics, management, and the social sciences — in both English and Chinese. Covers Turnitin AI, GPTZero, Originality.ai on the English side and 知网 AMLC, 万方, 维普 on the Chinese side. Uses a six-step loop (intake → audit → claim-evidence check → differentiated rewrite → five-dimension self-score → cold-reader recheck) with two pattern libraries (22 English + 17 Chinese patterns), section-by-section strategies for empirical papers, and hard protections that keep every number, coefficient, and citation intact.
triggers:
  - de-AIGC
  - 降 AIGC
  - 降低 AIGC
  - 去 AI 味
  - 去 AI 痕迹
  - humanize academic paper
  - remove AI writing patterns
  - AI detection academic
  - 知网 AIGC 检测
  - 万方 AIGC
  - 维普检测
  - Turnitin AI
  - GPTZero
  - humanize empirical paper
  - 人工化重写
---

# De-AIGC Skills · 中英双语学术降 AIGC

> Restore the language distribution of a real researcher — in English or Chinese —
> for empirical papers in economics, management, and the social sciences.
> Not synonym swapping. Not sentence shuffling. **Systematic reconstruction of the
> statistical signatures that mark a manuscript as AI-generated.**

## Scope 适用范围

**Papers**: empirical work in economics, management, finance, accounting, sociology,
political science, education, public policy — anything built on data, identification,
and regression tables. Theory papers and pure humanities essays are out of scope
(most patterns still transfer, but the section strategies assume an empirical skeleton).

**Languages**:

- **English manuscripts** — targets Turnitin AI, GPTZero, Originality.ai, Copyleaks
- **Chinese manuscripts** — targets 知网 AMLC、万方、维普通达、Turnitin 中文版
- **Mixed manuscripts** — a Chinese paper with an English abstract, or a bilingual
  submission package: run each part through its own pattern library, then check
  cross-language consistency (the English abstract must not overclaim what the
  Chinese conclusion hedges, and vice versa)

**Typical situations**:

- Self-checking AIGC rate before journal submission (中文期刊投稿 / SSCI submission)
- Dissertations facing 知网 AMLC or a university's Turnitin AI screen
- Grant proposals, working papers, and reports drafted with AI assistance
- A human-written draft that detectors misclassify as AI (this happens often —
  formulaic academic prose looks like AI to n-gram detectors)

## What does NOT work 无效做法

1. ❌ **Synonym replacement** — detectors read n-gram distributions, not word lists.
   把"关键"改成"核心"、"important" 改成 "crucial" 毫无作用。
2. ❌ **Sentence inversion** — flipping "Because A, B" to "B, because A" leaves the
   syntactic template intact.
3. ❌ **Feeding the text to another AI for a "rewrite"** — swaps one AI's signature
   for another's. Paraphraser tools are the fastest way to a *higher* AI score.
4. ❌ **Injecting typos or awkward grammar to "look human"** — human experts do not
   write badly; graders and reviewers notice, and modern detectors are not fooled.

**What works**: targeted destruction of the *structural* signatures listed below,
plus restoring the concrete, hedged, evidence-anchored voice of a real researcher.

## Structural signatures 结构性特征

The two languages fail differently. English LLM output leans on inflated
significance and participle padding; Chinese LLM output leans on four-character
formulas and connective scaffolding. The one signature they share — and the single
highest-impact fix in either language — is **uniform sentence rhythm**.

**English AI text** (details and fixes: `references/patterns-en.md`, EN01–EN22):

1. Inflated significance — "pivotal", "underscores the importance", "paves the way"
2. Superficial "-ing" tails — "…, highlighting the need for further research"
3. Formulaic scaffolding — "In recent years…", Moreover/Furthermore chains,
   rule-of-three lists, "not only… but also"
4. Overclaiming verbs with underpowered evidence — "proves", "demonstrates",
   "establishes" hanging off an observational coefficient
5. Low sentence-length variance — nearly all sentences 20–30 words

**Chinese AI text** (details and fixes: `references/patterns-zh.md`, ZH01–ZH17):

1. 四字套话密度过高 — 每 200 字 3+ 个"综上所述/毋庸置疑/显而易见"
2. 虚词与关联词冗余 — "此外/因此/而且/在此基础上"机械堆叠
3. 主语回避 — 满篇"本文认为/相关研究表明"，没有具体的研究者和文献
4. 句长方差低 — 句子集中在 20–35 字，缺乏节奏跳跃
5. 结论绝对化 — "充分证明了/必然导致/毫无疑问"

## The six-step loop 六步闭环

```
0. 定位路由      1. 审计扫描      2. 主张-证据核对
   Intake     →     Audit     →     Claim–evidence
                                        │
5. 冷读复查      4. 五维自评      3. 差异化改写
   Recheck    ←    Self-score  ←     Rewrite
```

### Step 0 · Intake & routing 定位路由

Before touching the text:

1. **Detect language(s)** — route each part to the right pattern library
   (`patterns-en.md` / `patterns-zh.md`). For mixed manuscripts, note which
   sections are which.
2. **Map sections** — abstract, intro, literature, data, empirical strategy,
   results, mechanisms, robustness, discussion, conclusion. Rewrite intensity
   differs sharply by section (`references/sections.md`).
3. **Identify the venue** — a Chinese CSSCI journal, an SSCI field journal, and a
   dissertation committee have different tolerances for first-person voice and
   hedging. Ask the user if unclear.
4. **Ask for a voice sample** (optional but powerful) — if the author has earlier
   *human-written* papers or paragraphs, match their sentence rhythm, connective
   habits, and hedging placement instead of a generic "human" style.

### Step 1 · Audit scan 审计扫描

Scan the full text against both pattern libraries and output a **structured audit
report — do not edit anything yet**. The author must see the whole picture first.

```markdown
## AI-signature audit / AI 痕迹审计

| ¶ | Excerpt 原文片段 | Rule 规则 | Severity 严重度 |
|---|-----------------|----------|----------------|
| 2 | "毋庸置疑，数字化转型…" | ZH01 四字套话 | 🔴 |
| 5 | "…, underscoring the importance of digital…" | EN02 -ing tail | 🔴 |
| 7 | "This proves that the reform caused…" | EN10 overclaiming verb | 🔴 |
```

Include a summary line: total hits per severity, the 3 worst sections, and the
estimated rewrite depth (light polish / section rewrites / full-pass rewrite).

### Step 2 · Claim–evidence audit 主张-证据核对

Empirical papers live or die on the match between **verbs and evidence strength**.
This step is what makes de-AIGC for empirical work different from generic humanizing:

- Every causal or quantitative claim must anchor to a **number, table, figure, or
  citation**. "显著提升企业绩效" → which table, which column, which coefficient?
- **Verb ↔ design match**:
  - Clean identification (RCT, sharp RD, well-defended DiD) → direct statements
    are fine: "the reform *reduced* entry by 12%"
  - Observational / correlational → "is associated with", "与…相关"
  - Suggestive / mechanism evidence → "is consistent with", "为…提供了证据",
    "这与…的解释一致"
- Flag every "prove/demonstrate/establish/充分证明/必然导致" whose design cannot
  carry that weight — and every unsupported "significant/显著" with no test statistic.
- **Never resolve a mismatch by inventing evidence.** If a claim has no anchor,
  flag it for the author; weakening the verb is the default fix.

### Step 3 · Differentiated rewrite 差异化改写

Work through the audit list, section by section, using the per-section strategies
in `references/sections.md`. Priorities, in order of impact:

1. **Break the rhythm ceiling first** 先砸句长方差 — this is the single
   highest-leverage fix in both languages. Per ~200 words (or 200 字): at least
   one short sentence (≤8 words / ≤15 字) and one long sentence (≥40 words /
   ≥50 字). Short sentences open questions or land emphasis ("The data say
   otherwise." / "数据讲了另一个故事。"); long sentences carry the evidence.
2. **Concretize** 具体化 — replace vague attributions and inflated adjectives
   with data, authors, years: "相关研究表明" → "Acemoglu and Restrepo (2020)
   estimate…"; "profound impact" → "raised TFP by 4.3% (t = 3.81)".
3. **De-scaffold** 拆脚手架 — remove paragraph-initial connectives
   (Moreover/Furthermore/此外/因此) and ordinal chains (首先…其次…最后 /
   First… Second… Finally) outside genuine enumerations; connect paragraphs by
   **semantic relay** (the next sentence picks up the previous sentence's key noun).
4. **Recalibrate claims** 校准断言 — apply Step 2's verb ↔ design matches; add
   epistemic hedges where missing, and *simplify* stacked hedges where the model
   piled up "may potentially suggest the possibility that…".
5. **Restore researcher voice** 恢复研究者声音 — show choices and trade-offs:
   "We use X rather than Y because…" / "受限于数据，我们无法识别…". Admitting a
   limitation or a surprise is the hardest pattern for an LLM to fake.

**Hard protections 硬性红线** — regardless of what the patterns say:

- Never alter numbers, coefficients, standard errors, p-values, sample sizes,
  equations, variable names, or citation contents. 数据、系数、引用一律不动。
- Never fabricate data, results, citations, or "surprising findings" for flavor.
- Never inject errors, slang, or archaic vocabulary to game perplexity.
- Never change what the paper claims — only how it says it.
- **Do not over-correct**: standard academic phrases are not AI tells. Keep
  "Notably," / "Prior studies have shown that… (with citations)" / "在 1% 水平上
  显著" / "稳健性检验" — flag such phrases only when stacked or citation-free.
  Full preserve-list: top of `references/patterns-en.md`.

### Step 4 · Five-dimension self-score 五维自评

Score the rewritten text 1–10 per dimension (rubric: `references/scoring.md`):

| Dimension 维度 | Weight | Checkpoint |
|---|---|---|
| Concreteness 具体性 | 1.5× | Vague claims replaced by data / authors / cases? |
| Rhythm 节奏性 | 1.2× | Sentence-length variance high enough? Short-long mix? |
| Calibration 谨慎性 | 1.3× | Verbs match evidence? Hedges present but not stacked? |
| Implicit cohesion 隐衔接 | 1.0× | Paragraphs relay by meaning, not connectives? |
| Researcher voice 研究者语气 | 1.0× | Choices, trade-offs, limitations visible? |

**Weighted total < 35 → back to Step 3. ≥ 42 → pass.**

### Step 5 · Cold-reader recheck 冷读复查

Re-read the full text as a stranger and run three final checks:

1. **Fluency** — did any fix damage the argument's flow or academic register?
2. **Fidelity** — diff every number, name, year, and citation against the
   original. Zero drift allowed.
3. **Consistency** — one voice throughout; no visible seam between rewritten and
   untouched paragraphs; for bilingual packages, EN and ZH parts must make the
   same claims at the same strength.

Deliver: **final text + change log** (which sections changed, which rules fired,
what was deliberately left alone) + any unresolved flags from Step 2 that need
the author's judgment.

## Works well with 配合使用

- [`44-matsuikentaro1-humanizer_academic`](../44-matsuikentaro1-humanizer_academic/) —
  English medical/academic pattern source; use for biomedical manuscripts
- [`45-stephenturner-skill-deslop`](../45-stephenturner-skill-deslop/) /
  [`46-hardikpandya-stop-slop`](../46-hardikpandya-stop-slop/) — general English
  prose de-slopping outside the academic register
- [`47-conorbronsdon-avoid-ai-writing`](../47-conorbronsdon-avoid-ai-writing/) —
  structured audit format for non-academic documents
- [`49-voidborne-d-humanize-chinese`](../49-voidborne-d-humanize-chinese/) —
  general Chinese humanizing beyond the academic register
- [`70-ssci-polish`](../70-ssci-polish/) — SSCI-oriented English polish after
  de-AIGC is done
- Draft first, de-AIGC last: run this skill on a *finished* draft, not during
  drafting — mid-draft humanizing fights the writing process.

## References 参考文件

- `references/patterns-en.md` — 22 English AI-signature patterns (EN01–EN22),
  each with detection rule + empirical-paper before/after, plus the preserve-list
- `references/patterns-zh.md` — 17 类中文 AI 痕迹模式（ZH01–ZH17），含识别规则与修复策略
- `references/sections.md` — section-by-section rewrite strategies for empirical
  papers, bilingual symptoms and red lines（分章节差异化策略，中英对照）
- `references/scoring.md` — five-dimension rubric, bilingual（五维评分量表）
- `references/examples-en.md` — English before/after pairs across an empirical
  paper's sections
- `references/examples-zh.md` — 12 组中文改写前后对照（覆盖实证论文各章节）

## Integrity statement 学术诚信声明

The goal is to **return human-written and AI-assisted text to the language
distribution of a real researcher** — not to help fully AI-generated work evade
detection.

- ✅ A researcher's own draft misclassified as AI by a detector
- ✅ AI-assisted drafting + human revision, where the author owns every claim
- ❌ A fully AI-generated paper the "author" hopes to pass off unread
- ❌ Ghostwriting, plagiarism laundering, or data fabrication of any kind

**Academic integrity outranks detection scores.** No rewrite may touch the
research claims, the data, or the citations — and when a claim lacks evidence,
the fix is to flag it, not to hide it.
