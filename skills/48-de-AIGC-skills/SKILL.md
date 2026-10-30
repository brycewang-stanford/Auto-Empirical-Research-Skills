---
name: de-aigc-skills
description: 中英双语学术降 AIGC + 去水印 / bilingual academic de-AIGC and provenance skill for empirical papers in economics, management and the social sciences (Turnitin AI, GPTZero, 知网 AMLC, 万方, 维普). Six-step loop (intake → audit → claim-evidence check → rewrite → self-score → cold-reader recheck) in three modes (audit-only / edit / author-voiced), 30 English + 28 Chinese patterns revised in 2026-10 against the ten most-starred humanizer skills, a protect-list, per-section edit caps, and hard rules that keep every number, coefficient and citation intact and never invent anchors. Two stdlib scripts - aigc_audit.py (deterministic rule scan; fidelity gate for numbers, citations, negation and verb strength; draft-retention metrics) and provenance_scrub.py (CJK-safe invisible-character, look-alike and whitespace cleaning; docx / figure / PDF / zip metadata incl. C2PA). Claude's statistical watermark is handled by an author ownership pass and always reported as unknown; the skill never claims a text is watermark-free.
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
  - 翻译腔
  - AI 痕迹审计
allowed-tools:
  - Bash(python3 scripts/provenance_scrub.py:*)
  - Bash(python3 scripts/aigc_audit.py:*)
---

# De-AIGC Skills · 中英双语学术降 AIGC

> Restore the language distribution of a real researcher — in English or Chinese —
> for empirical papers in economics, management, and the social sciences.
> Not synonym swapping. Not sentence shuffling. **Systematic reconstruction of the
> statistical signatures that mark a manuscript as AI-generated.**

**2026-10 upgrade.** The pattern libraries, rubric and provenance layer were
re-read against the ten most-starred de-AI-tone skills on GitHub and the two
dedicated text-watermark removers. Eight English and eleven Chinese patterns
were added. Three Chinese rules were demoted on their measured data. Two
"fixes" that invented content were withdrawn, and so were the claims about
detector scores that had no measurement behind them. Two deterministic scripts
now do what the loop used to leave to judgement. Details and licences:
`references/lineage.md`.

## Scope 适用范围

**Papers**: empirical work in economics, management, finance, accounting, sociology,
political science, education, public policy — anything built on data, identification,
and regression tables. Theory papers and pure humanities essays are out of scope
(most patterns still transfer, but the section strategies assume an empirical skeleton).

**Languages**:

- **English manuscripts** — Turnitin AI, GPTZero, Originality.ai, Copyleaks
- **Chinese manuscripts** — 知网 AMLC、万方、维普通达、Turnitin 中文版
- **Mixed manuscripts** — a Chinese paper with an English abstract, or a bilingual
  submission package: run each part through its own pattern library, then check
  cross-language consistency (the English abstract must not overclaim what the
  Chinese conclusion hedges, and vice versa)

**Typical situations**:

- Self-checking a draft before journal submission (中文期刊投稿 / SSCI submission)
- Dissertations facing 知网 AMLC or a university's Turnitin AI screen
- Grant proposals, working papers, and reports drafted with AI assistance
- A human-written draft that detectors misclassify as AI (this happens often —
  formulaic academic prose looks like AI to n-gram detectors)
- Cleaning a submission package before (double-blind) review: invisible
  characters picked up through copy-paste, `.docx` author fields and revision
  ids, C2PA manifests on model-generated figures, `__MACOSX` entries in the zip

## Three modes 三种模式

Pick one at intake; say which in the first line of the reply.

| Mode | Steps | Output | When |
|---|---|---|---|
| **audit-only** 只诊断 | 0 → 1 → 2, then stop | audit table + claim–evidence flags + provenance report | co-authored or published text; the author wants to fix it personally; the default when the user only says "check" / "诊断" |
| **edit** 编辑 | full loop, agent edits within the per-section caps | revised text + change log + fidelity report | low-signal sections, a human draft misread as AI, polishing |
| **author-voiced** 作者重述 | full loop; Step 3 delivers briefs, the author writes the high-signal sections | briefs + fidelity and draft-retention report | the draft or a section came from a model launched after 2026-08-02 (Layer B), or the venue requires the author's own words |

The audit is the one point where the author confirms before anything is
rewritten (lieflat's "唯一的改前确认点"): in edit and author-voiced modes, show
the Step 1–2 report and wait for a go-ahead unless the user already gave one.

## What does NOT work 无效做法

1. ❌ **Synonym replacement** — detectors read n-gram distributions, not word lists.
   把"关键"改成"核心"、"important" 改成 "crucial" 毫无作用。
2. ❌ **Sentence inversion** — flipping "Because A, B" to "B, because A" leaves the
   syntactic template intact.
3. ❌ **Feeding the text to another AI for a "rewrite"** — swaps one AI's signature
   for another's, and *re-embeds* a statistical watermark: Claude's and Gemini's
   marks live in the word choices, so a model paraphrase is a fresh mark.
4. ❌ **Injecting typos or awkward grammar to "look human"** — human experts do not
   write badly; graders and reviewers notice, and modern detectors are not fooled.
5. ❌ **Manufacturing rhythm** — forcing a short sentence and a long one into every
   200 words, slogan fragments ("The data say otherwise." / "数据讲了另一个故事。"),
   rhetorical questions answered in the next breath. Prompting a model to "vary
   sentence length" made text *easier* to detect, and no study supports a fixed
   sentence-length threshold (sepia `research/rhythm-syntax.md`).
6. ❌ **Adding content to sound human** — invented numbers, citations, limitations,
   "surprising findings", researcher anecdotes. Every top humanizer skill forbids
   it; for a paper it is fabrication.
7. ❌ **Stripping invisible characters and calling the text "de-watermarked"** —
   Claude's watermark is not made of characters (Anthropic: "there are no hidden
   characters"). Character hygiene is still necessary, but it proves nothing about
   the watermark.

**What works**: targeted removal of the *structural* signatures listed below,
restoring the concrete, calibrated, evidence-anchored voice of a real researcher
using only what the paper already contains.

## Watermarks are not writing signatures 水印 ≠ 文风

Three different things are called an "AI watermark" in 2026. The skill treats
them differently, and every report says which layer was actually verified
(full policy and code-point tables: `references/watermarks.md`):

| Layer | What it is | Handled by |
|---|---|---|
| **A · character carriers** 隐藏字符 | zero-width characters, bidi controls, tag characters, stray variation selectors, script-bound format characters, exotic spaces, soft hyphens, trailing-whitespace patterns, Cyrillic / Greek look-alikes inside Latin words — *not* used by Claude, but common in copy-paste chains and third-party tools | `scripts/provenance_scrub.py` — deterministic and CJK-safe: keeps U+3000 indents, fullwidth punctuation, ideographic variation selectors in names, en dashes in ranges, R², β, Russian citations; look-alikes are reported first and folded only on request; NFKC is not an option |
| **B · statistical watermark** 统计水印 | Claude (models launched ≥ 2026-08-02) and Gemini bias *which words* are sampled; nothing is added to the string; survives copy, translation and light edits; no public detector | the **ownership pass** in Step 3, measured by `aigc_audit.py compare --by author` (draft-retention n-gram containment) — which bounds how much model wording survives and still reports `B: unknown` |
| **C · container metadata** 容器元数据 | C2PA manifests on model-generated PNG / JPG / SVG (also when pasted *into* a `.docx`); `.docx` docProps, sensitivity labels, revision ids, template paths, comments; PDF Info + XMP incl. compressed streams and pdfTeX figure info; `__MACOSX` in a zip; macOS download-origin attributes | `provenance_scrub.py clean` (docx / png / jpg / svg / zip, lossless); report plus `exiftool` / `qpdf` / pdfLaTeX / `xattr` commands for the rest; best of all, regenerate figures from the replication package |

```bash
python3 scripts/provenance_scrub.py inspect main.docx figures/*.png   # report only; exit 1 if anything is found
python3 scripts/provenance_scrub.py clean   main.docx --lang zh        # main.clean.docx: runs, docProps, rsids, embedded figures
python3 scripts/provenance_scrub.py clean   submission.zip             # members cleaned, __MACOSX / .DS_Store dropped
python3 scripts/provenance_scrub.py clean   draft.md --diff            # carriers shown as ⟨U+200B⟩ in the diff
python3 scripts/provenance_scrub.py self-test                          # 54 keep / strip fixtures
```

Every report ends with **`B: unknown`**. Nobody outside Anthropic can verify
that a statistical watermark is gone, and this skill will not claim it.

## Structural signatures 结构性特征

The two languages fail differently. English LLM output leans on inflated
significance, participle padding and chatbot residue; Chinese LLM output leans
on four-character formulas, 否定对举 and elevation endings. What they share is
**claims stronger than the evidence** and **packaging in place of content**.

**English AI text** (details: `references/patterns-en.md`, EN01–EN30):

1. Inflated significance and takeaway closers — "pivotal", "underscores the
   importance", "Taken together, these results highlight…"
2. Superficial "-ing" tails — "…, highlighting the need for further research"
3. Formulaic scaffolding — "In recent years…", Moreover/Furthermore chains,
   staged contrasts ("This does not mean X. It means Y.")
4. Overclaiming verbs with underpowered evidence — "proves", "demonstrates",
   "establishes" hanging off an observational coefficient
5. Residue and artifacts — "Certainly! Here is…", `[oaicite:2]`,
   `utm_source=chatgpt.com`, "[Author, 20XX]"

**Chinese AI text** (details: `references/patterns-zh.md`, ZH01–ZH28):

1. 套路开篇与四字套话 — "近年来…引起了广泛关注"、"毋庸置疑/综上所述"
2. 否定对举 / 假揭示 — "不是 A，而是 B"、"核心发现是："
3. 结论绝对化 — "充分证明了/必然导致/毫无疑问"
4. 升华套话 — "为…提供了有益借鉴"、"具有重要的理论意义和现实价值"
5. 翻译腔与限定词堆叠 — "当…时，"、"作为…之一的"、"在一定程度上或许可能"

**Protect-list** (both languages; full lists at the top of each pattern file):
statistical stock phrases ("significant at the 1% level", 在 1% 水平上显著),
method terms, table / figure / equation references, citations, policy text
inside quotation marks, numbered headings, academic passives and
nominalisations, "is associated with" for correlational evidence. These are
not tells and are never "fixed".

## The six-step loop 六步闭环

```
0. 定位路由      1. 审计扫描      2. 主张-证据核对
   Intake     →     Audit     →     Claim–evidence      ← audit-only stops here
                                        │
5. 冷读复查      4. 五维自评      3. 差异化改写
   Recheck    ←    Self-score  ←     Rewrite
```

Provenance layer, threaded through the loop: `inspect` before Step 1 (hidden
characters split tokens and corrupt the pattern scan) · ownership pass inside
Step 3 · package `clean` at Step 5.

### Step 0 · Intake & routing 定位路由

Before touching the text:

1. **Pick the mode** (table above). Default to audit-only when unclear.
2. **Detect language(s)** — route each part to `patterns-en.md` / `patterns-zh.md`.
3. **Map sections** — abstract, intro, literature, data, empirical strategy,
   results, mechanisms, robustness, discussion, conclusion. Rewrite intensity and
   the agent's edit cap differ by section (`references/sections.md`).
4. **Identify the venue** — a CSSCI journal, an SSCI field journal, a
   dissertation committee and a grant panel differ on first person and hedging;
   grant prose keeps its ambition language. Ask if unclear.
5. **Calibrate voice** — if the author has earlier *human-written* papers, note
   their sentence-length mix, connective habits, hedge placement and how
   sections open; that sample overrides the pattern defaults (including the
   dash rate). Without one, use 3–5 recent papers in the target journal.
6. **Build a ledger** — every number, citation, table / figure reference and
   claim (with its strength) in the original. Step 5 checks against it;
   `aigc_audit.py compare` automates most of it.
7. **Scan for provenance marks** — `python3 scripts/provenance_scrub.py inspect
   <files>`. Clean Layer A carriers *before* the audit; note container metadata
   for Step 5. Ask whether the draft came out of a model launched after
   2026-08-02 — if so, author-voiced mode for the high-signal sections.

### Step 1 · Audit scan 审计扫描

Run the deterministic scan first, then read for the rules a regex cannot see:

```bash
python3 scripts/aigc_audit.py audit draft.md            # or .tex / .docx; --json for tooling
```

It masks quotations, math, `\cite{}`, tables and code; reports hits by rule id
and paragraph; lists the rules left to the model (rhythm quality, total-score
structure, elegant variation, echo …); and prints report-only metrics
(sentence-length spread, long-sentence share, dash rate, hedge density,
abstract↔conclusion similarity). It prints no AI probability. The composite
scores of upstream detectors were measured near a coin flip at paragraph level.

Then output the **structured audit report — do not edit anything yet**:

```markdown
## AI-signature audit / AI 痕迹审计

| ¶ | Excerpt 原文片段 | Rule 规则 | Severity 严重度 | Source |
|---|-----------------|----------|----------------|--------|
| 2 | "毋庸置疑，数字化转型…" | ZH01 高危套话 | 🟡 | script |
| 5 | "…, underscoring the importance of digital…" | EN02 -ing tail | 🔴 | script |
| 7 | "This proves that the reform caused…" | EN10 overclaiming verb | 🔴 | script |
| 9 | 三段都是"观点—例子—重申" | ZH10 总分总 | 🔴 | model |
```

Include a summary line — hits per severity, the 3 worst sections, the proposed
mode and depth — and attach the provenance-mark report from Step 0.

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

Work through the audit list, section by section (`references/sections.md`).
Every edit must map to a rule id from the audit; an edit that maps to none is
reverted. Priorities, in order:

1. **Remove residue and artifacts** (EN23, EN24) — unambiguous and cheap.
   Placeholders are flagged for the author, never filled.
2. **Recalibrate claims** 校准断言 — apply Step 2's verb ↔ design matches; one
   hedge per observational claim, chosen by design strength: never zero, never
   three (EN15, ZH14, ZH24).
3. **Replace packaging with what the paper already says** 用原稿内容替代空话 —
   "profound impact" → the coefficient from Table 4; "相关研究表明" → the
   author-year already in the reference list. **Anchors come only from the paper
   or the author.** When none exists, write `[author: which table?]` /
   `[作者补：表X第(2)列]` and move on.
4. **De-scaffold** 拆脚手架 — formulaic openers, staged contrasts, 否定对举,
   takeaway closers, elevation endings, ordinal chains in prose (not in real
   enumerations or numbered headings); connect by **semantic relay** (the next
   sentence picks up the previous sentence's key noun).
5. **Let length follow content** 句长跟内容走 — merge adjacent sentences that
   make one point into one sentence that carries the evidence chain; split a
   sentence that makes two claims. Do not add slogan sentences or rhetorical
   questions for rhythm.
6. **Restore researcher voice** 恢复研究者声音 — show the choices the paper
   actually made ("We use X rather than Y because…" with the reason from the
   paper). Limitations, surprises and trade-offs come from the original or the
   author; when they are missing, flag them (`[作者补：局限]`).

**Never inject** (avoid-ai-writing's list, adopted whole): invented speaker
perspective, manufactured stakes, forced contrarianism, staccato fragments,
em-dash theatrics, invented specifics.

**Deletion and reversion tests** (sepia): after editing, cross out each word
you added — if the sentence still works, delete it; put each replaced word back —
if the original is shorter and means the same, keep the original. Apart from
evidence pointers, the rewrite should not be longer than the source.

**Edit caps** (agent edits, measured by `aigc_audit.py compare --section`):
data / model / robustness 15%, results / mechanisms / heterogeneity 25%,
abstract / introduction / literature / discussion / conclusion 40%. Over the
cap means edits no rule asked for; revert them. The author's own rewrite is not
capped.

**Ownership pass 作者重述 (Layer B, author-voiced mode)** — any sentence the
agent writes is model output, and if the model carries a token-sampling
watermark, so does its rewrite. For the high-signal sections (abstract,
introduction, literature, hypotheses framing, discussion, conclusion) Step 3
therefore delivers a **brief**, not final copy: what the paragraph must say,
which table / coefficient / citation anchors it, which rules fired, plus a
rewrite *marked as a suggestion*. The author writes the sentences from the brief
with the suggestion out of view; the agent then checks fidelity and draft
retention and flags, but does not rewrite:

```bash
python3 scripts/aigc_audit.py compare model_draft.md author_final.md --by author
```

Label every paragraph in the change log: `author-voiced` · `model-suggested,
author-accepted` · `untouched`. A paragraph whose draft retention is still
high (most 4-grams survive) is not `author-voiced`. Details:
`references/watermarks.md` §4.

**Hard protections 硬性红线** — regardless of what the patterns say:

- Never alter numbers, coefficients, standard errors, p-values, sample sizes,
  equations, variable names, or citation contents. 数据、系数、引用一律不动。
- Never fabricate data, results, citations, limitations, or "surprising
  findings". Missing anchors become placeholders for the author.
- Never inject errors, slang, or archaic vocabulary to game perplexity.
- Never change what the paper claims — only how it says it. An exclusion stays
  an exclusion; a correlation stays a correlation.
- **Do not over-correct**: the protect-list phrases are not AI tells.
- **Never ASCII-fold or NFKC-normalise.** En dashes in ranges (2014–2022),
  minus signs (−0.043), R², β₁, fullwidth Chinese punctuation, 中文 `——` and
  `……` are typography, not tells.
- **Never write "watermark-free", "无水印", "undetectable" or "过检".** Report
  what was verified (Layers A and C) and what was not (B).

### Step 4 · Five-dimension self-score 五维自评

Score the rewritten text 1–10 per dimension (rubric: `references/scoring.md`):

| Dimension 维度 | Weight | Checkpoint |
|---|---|---|
| Concreteness 具体性 | 1.5× | Packaging replaced by the paper's own data / authors / cases? |
| Rhythm 节奏性 | 1.2× | Length follows content? No runs of 4+ same-length sentences, no manufactured fragments? |
| Calibration 谨慎性 | 1.3× | Verbs match evidence? One hedge per claim, not zero, not stacked? |
| Implicit cohesion 隐衔接 | 1.0× | Paragraphs relay by meaning, not connectives? |
| Researcher voice 研究者语气 | 1.0× | The paper's real choices, trade-offs, limitations visible? |

**Weighted total < 35 → back to Step 3. ≥ 42 → pass to Step 5.** The score is a
revision checklist and predicts no detector's output.

### Step 5 · Cold-reader recheck 冷读复查

Re-read the full text as a stranger and run the final checks:

1. **Second pass: "what still reads as AI?"** (blader) — re-search the tells that
   most often survive *or get introduced by* a rewrite: staged contrasts,
   takeaway closers, triads, dashes, bold labels, question openers. Re-run
   `aigc_audit.py audit` on the result.
2. **Fidelity** — `python3 scripts/aigc_audit.py compare original.md revised.md
   --section <name>`: every number, citation, table / figure reference and
   significance statement must survive (exit 1 otherwise); negation, direction
   words, evidence-verb strength and hedges are checked for drift. Zero drift
   allowed; roll back any edit that fails.
3. **Fluency and consistency** — one voice throughout; no seam between rewritten
   and untouched paragraphs; paragraph count in = paragraph count out unless the
   author asked otherwise; for bilingual packages, EN and ZH make the same
   claims at the same strength.
4. **Package hygiene** — `provenance_scrub.py clean` on the final `.docx`,
   `.md` / `.tex`, figures and the submission `.zip`; PDF via the `exiftool` +
   `qpdf` (+ pdfLaTeX) commands it prints; comments, tracked changes and
   `people.xml` are reported and must be cleared in Word. Re-run `inspect` and
   keep the report.

Deliver: **final text + change log** (sections changed, rules fired per edit,
what was deliberately left alone, which paragraphs are author-voiced) +
**verification block** (scripts run and their verdicts, which checks were
deterministic and which were model judgement, residual hits, placeholders still
open, why the work stopped) + **provenance-mark report** (A and C verified,
`B: unknown`, draft retention where measured) + any unresolved Step 2 flags.

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
  service) when a package goes beyond text, documents and figures
- Draft first, de-AIGC last: run this skill on a *finished* draft, not during
  drafting — mid-draft humanizing fights the writing process.

## References 参考文件

- `references/patterns-en.md` — 30 English AI-signature patterns (EN01–EN30),
  preserve-list, and the general-prose rules deliberately not adopted
- `references/patterns-zh.md` — 28 类中文 AI 痕迹模式（ZH01–ZH28），保护清单、改动幅度、
  不采纳的做法
- `references/sections.md` — section-by-section strategies and per-section edit
  caps, bilingual（分章节差异化策略与改动上限）
- `references/scoring.md` — five-dimension rubric, bilingual（五维评分量表）
- `references/examples-en.md` — English before/after pairs (8 cases; the
  rewrites fire no audit rule)
- `references/examples-zh.md` — 12 组中文改写前后对照（锚点均取自论文正文）
- `references/watermarks.md` — the provenance layer: three kinds of marks, what
  Anthropic states, the CJK-safe code-point and look-alike policy, the
  ownership pass and draft-retention metrics, package hygiene, report format
- `references/lineage.md` — the ten most-starred humanizer skills and two
  watermark removers: what was adopted, where it lives, what was left out and
  why, licences, and the corrections they forced（来源与取舍）
- `scripts/aigc_audit.py` — stdlib Python 3.9+: `audit` (rule scan + report-only
  metrics) and `compare` (fidelity gate, change rate vs section cap, draft
  retention); `self-test` with 31 fixtures
- `scripts/provenance_scrub.py` — stdlib Python 3.9+: `inspect` / `clean` for
  text, `.docx`, `.png`, `.jpg`, `.svg`, `.zip`; `.pdf` report + commands;
  `self-test` with 54 fixtures（隐藏字符、形近字符与元数据扫描 / 清理脚本）

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
- ❌ Regenerating text through another model, or searching for the smallest edit
  that clears a detector — the evasion stages of upstream watermark removers are
  deliberately not part of this skill

**Academic integrity outranks detection scores.** No rewrite may touch the
research claims, the data, or the citations — and when a claim lacks evidence,
the fix is to flag it, not to hide it.
