---
name: de-aigc-skills
description: 中英双语学术降 AIGC / bilingual academic de-AIGC skill. Removes AI-generated writing signatures from empirical papers in economics, management, and the social sciences — in both English and Chinese. Covers Turnitin AI, GPTZero, Originality.ai on the English side and 知网 AMLC, 万方, 维普 on the Chinese side. Uses a six-step loop (intake → audit → claim-evidence check → differentiated rewrite → five-dimension self-score → cold-reader recheck) with two pattern libraries (22 English + 17 Chinese patterns), section-by-section strategies for empirical papers, and hard protections that keep every number, coefficient, and citation intact. Since 2026-08 it also carries a provenance layer (去水印): deterministic, CJK-safe cleaning of invisible-character carriers and file metadata (docx / png / jpg / svg / pdf, incl. C2PA), an honest account of Claude's statistical text watermark, and an author "ownership pass" — it never claims a text is watermark-free.
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
  - 去水印
  - 去 AI 水印
  - Claude 水印
  - remove Claude watermark
  - AI watermark
  - 零宽字符 / invisible Unicode
allowed-tools:
  - Bash(python3 scripts/provenance_scrub.py:*)
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
- Cleaning a submission package before (double-blind) review: invisible
  characters picked up through copy-paste, `.docx` author fields, C2PA
  manifests on model-generated figures — the provenance layer below

## What does NOT work 无效做法

1. ❌ **Synonym replacement** — detectors read n-gram distributions, not word lists.
   把"关键"改成"核心"、"important" 改成 "crucial" 毫无作用。
2. ❌ **Sentence inversion** — flipping "Because A, B" to "B, because A" leaves the
   syntactic template intact.
3. ❌ **Feeding the text to another AI for a "rewrite"** — swaps one AI's signature
   for another's. Paraphraser tools are the fastest way to a *higher* AI score.
   Since 2026-08 it also *re-embeds* a statistical watermark: Claude's and
   Gemini's marks live in the word choices, so a model paraphrase is a fresh mark.
4. ❌ **Injecting typos or awkward grammar to "look human"** — human experts do not
   write badly; graders and reviewers notice, and modern detectors are not fooled.
5. ❌ **Stripping invisible characters and calling the text "de-watermarked"** —
   Claude's watermark is not made of characters (Anthropic: "there are no hidden
   characters"). Character hygiene is still necessary — carriers split tokens in
   n-gram scans and trip Turnitin's hidden-text flags — but it proves nothing
   about the watermark.

**What works**: targeted destruction of the *structural* signatures listed below,
plus restoring the concrete, hedged, evidence-anchored voice of a real researcher.

## Watermarks are not writing signatures 水印 ≠ 文风

Three different things are called an "AI watermark" in 2026. The skill treats
them differently, and every report says which layer was actually verified
(full policy and code-point tables: `references/watermarks.md`):

| Layer | What it is | Handled by |
|---|---|---|
| **A · character carriers** 隐藏字符 | zero-width characters, bidi controls, tag characters, stray variation selectors, exotic spaces, soft hyphens — *not* used by Claude, but common in copy-paste chains and third-party tools | `scripts/provenance_scrub.py` — deterministic and CJK-safe: keeps U+3000 indents, fullwidth punctuation, ideographic variation selectors in names, en dashes in ranges, R²; NFKC is not an option |
| **B · statistical watermark** 统计水印 | Claude (models launched ≥ 2026-08-02) and Gemini bias *which words* are sampled; nothing is added to the string; survives copy, translation and light edits; no public detector | the **ownership pass** in Step 3 — the author writes the high-signal sentences; the agent's own rewrite is model output and does not count |
| **C · container metadata** 容器元数据 | C2PA manifests on model-generated PNG / JPG / SVG, `.docx` docProps / comments / people.xml, PDF Info + XMP | `provenance_scrub.py clean` (docx / png / jpg / svg, lossless); report plus `exiftool` / `qpdf` commands for PDF; best of all, regenerate figures from the replication package |

```bash
python3 scripts/provenance_scrub.py inspect main.docx figures/*.png   # report only; exit 1 if anything is found
python3 scripts/provenance_scrub.py clean   main.docx --lang zh        # writes main.clean.docx, docProps blanked
python3 scripts/provenance_scrub.py clean   draft.md --diff            # carriers shown as ⟨U+200B⟩ in the diff
python3 scripts/provenance_scrub.py self-test                          # 39 keep / strip fixtures
```

Every report ends with **`B: unknown`**. Nobody outside Anthropic can verify
that a statistical watermark is gone, and this skill will not claim it.

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

Provenance layer, threaded through the loop: `inspect` before Step 1 (hidden
characters split tokens and corrupt the pattern scan) · ownership pass inside
Step 3 · package `clean` at Step 5.

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
5. **Scan for provenance marks** — `python3 scripts/provenance_scrub.py inspect
   <files>` on the draft and any figures. Clean Layer A carriers *before* the
   audit; note docx / figure metadata for Step 5. Ask whether the draft (or any
   figure) came out of a model launched after 2026-08-02 — if so, the ownership
   pass in Step 3 is mandatory for the high-signal sections, not optional.

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
estimated rewrite depth (light polish / section rewrites / full-pass rewrite) —
and attach the provenance-mark report from Step 0 (Layer A counts by code point,
docx / figure metadata found, `B: unknown`).

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

**Ownership pass 作者重述 (Layer B)** — the only thing that touches a statistical
watermark, so it has to be said plainly: any sentence the agent writes is model
output, and if the model carries a token-sampling watermark, so does its
rewrite. For the high-signal sections (abstract, introduction, literature,
hypotheses framing, discussion, conclusion) Step 3 therefore delivers a
**brief**, not final copy: what the paragraph must say, which table /
coefficient / citation anchors it, which rules fired, where the short and the
long sentence go, plus a rewrite *marked as a suggestion*. The author writes the
sentences from the brief with the suggestion out of view; the agent then checks
fidelity and fluency and flags, but does not rewrite. Low-signal sections (data,
model equations, table notes, robustness lists) may keep model polish. Label
every paragraph in the change log: `author-voiced` · `model-suggested,
author-accepted` · `untouched`. Details: `references/watermarks.md` §4.

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
- **Never ASCII-fold or NFKC-normalise.** En dashes in ranges (2014–2022),
  minus signs (−0.043), R², β₁, fullwidth Chinese punctuation, 中文 `——` and
  `……` are typography, not tells. `provenance_scrub.py` is built to leave them
  alone; do not "fix" them by hand either.
- **Never write "watermark-free", "无水印", "undetectable" or "过检".** Report
  what was verified (Layers A and C) and what was not (B).

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
4. **Package hygiene** — `provenance_scrub.py clean` on the final `.docx`,
   `.md` / `.tex` and figures (lossless; docProps blanked); PDF via the
   `exiftool` + `qpdf` commands it prints; comments, tracked changes and
   `people.xml` are reported and must be cleared in Word. Re-run `inspect` and
   keep the report. Double-blind venues require most of this anyway.

Deliver: **final text + change log** (which sections changed, which rules fired,
what was deliberately left alone, which paragraphs are author-voiced) + the
**provenance-mark report** (A and C verified, `B: unknown`) + any unresolved
flags from Step 2 that need the author's judgment.

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
- [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover)
  (MIT) — the heavier multi-format toolkit (audio / video / pixel-domain, HTTP
  service) when a package goes beyond text, `.docx` and figures; its layer model
  is what `references/watermarks.md` adapts for academic manuscripts
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
- `references/watermarks.md` — the 2026 provenance layer: three kinds of marks
  (statistical / character / metadata), what Anthropic states, the CJK-safe
  code-point policy, the ownership pass, package hygiene, report format
  （水印与溯源标记政策，中英对照）
- `scripts/provenance_scrub.py` — stdlib Python 3.9+: `inspect` / `clean` for
  text, `.docx`, `.png`, `.jpg`, `.svg`; `.pdf` report + commands; `self-test`
  with 39 fixtures（隐藏字符与元数据扫描 / 清理脚本）

## Integrity statement 学术诚信声明

The goal is to **return human-written and AI-assisted text to the language
distribution of a real researcher** — not to help fully AI-generated work evade
detection.

- ✅ A researcher's own draft misclassified as AI by a detector
- ✅ AI-assisted drafting + human revision, where the author owns every claim
- ❌ A fully AI-generated paper the "author" hopes to pass off unread
- ❌ Ghostwriting, plagiarism laundering, or data fabrication of any kind
- ✅ Cleaning provenance marks on content you own — double-blind review demands
  half of it, and Anthropic itself states the watermark "doesn't say anything
  about ownership or authorship"
- ❌ Using the provenance layer to hide model authorship of text the author
  cannot defend, or to dodge a venue's generative-AI disclosure requirement —
  where disclosure is asked for, disclose

**Academic integrity outranks detection scores.** No rewrite may touch the
research claims, the data, or the citations — and when a claim lacks evidence,
the fix is to flag it, not to hide it.
