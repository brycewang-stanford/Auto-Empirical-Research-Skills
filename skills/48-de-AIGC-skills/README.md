# De-AIGC Skills · 中英双语学术降 AIGC + 去水印

> **作者 Author**: CoPaper.AI · Stanford REAP
> **许可证 License**: CC-BY-SA-4.0 (repository default)
> **适用工具 Works with**: Claude Code / Cursor / Codex / Gemini CLI / any agent that speaks the Agent Skills standard

A bilingual (English + Chinese) skill that removes AI-generated writing
signatures from **empirical papers in economics, management, and the social
sciences** — 面向经管社科实证论文的中英双语降 AIGC Skill — and, since 2026-08,
handles the three things people call an "AI watermark" without pretending
they are one thing（去水印层）.

- **English side**: Turnitin AI, GPTZero, Originality.ai, Copyleaks
- **中文侧**: 知网 AMLC、万方、维普通达、Turnitin 中文版
- **Provenance layer 溯源层**: invisible-character carriers and look-alikes,
  `.docx` / figure / PDF / zip metadata (incl. C2PA), and an honest protocol for
  Claude's statistical text watermark

**2026-10 upgrade 升级** — re-read against the **ten most-starred de-AI-tone
skills on GitHub** (blader/humanizer 62k★, op7418/Humanizer-zh 21k★,
hardikpandya/stop-slop 18k★, epoko77-ai/im-not-ai, conorbronsdon/avoid-ai-writing,
larashero3-dotcom/lieflat-less-ai-tone, Nanako0129/sepia,
AIScientists-Dev/academic-humanizer, MrGeDiao/shuorenhua,
LifelongLazyLearner/qu-ai-wei) and the two dedicated text-watermark removers.
What changed:

- **Patterns** EN01–EN22 → **EN01–EN30**, ZH01–ZH17 → **ZH01–ZH28** (chatbot
  residue, generation artifacts, staged contrast, 否定对举, 翻译腔, 升华套话,
  限定词堆叠 …), plus a protect-list of academic phrasing that is never "fixed".
- **Corrections** where the upstream evidence said our rules pushed the wrong
  way: the "one short + one long sentence per 200 words" quota is gone (no
  study supports a length threshold, and "vary sentence length" prompts made
  text *easier* to detect); rules that invented anchors or limitations now
  emit `[作者补：…]` placeholders; ZH04 / ZH08 / ZH11 demoted on measured data;
  unmeasured detector-score claims deleted.
- **Three modes** — audit-only / edit / author-voiced — and **per-section edit
  caps** (15% / 25% / 40%).
- **`scripts/aigc_audit.py`** (new) — a deterministic rule scan with report-only
  metrics, and a fidelity gate that fails when a number, citation or table
  reference is lost or invented, warns on negation / direction / verb-strength
  drift, and measures **draft retention** for the ownership pass.
- **`scripts/provenance_scrub.py` 1.1** — script-bound format characters,
  Cyrillic / Greek look-alikes (reported first; Russian citations and β are
  safe), trailing-whitespace steganography, figures pasted *inside* a `.docx`,
  rsids / template paths / sensitivity labels, compressed PDF streams and
  pdfTeX figure info, `__MACOSX` in a submission zip, macOS download-origin
  attributes.

The full adopted / not-adopted map, licences included, is
[`references/lineage.md`](references/lineage.md).

## Why this skill 为什么需要它

Most humanizer skills handle one language and generic prose. Empirical papers
fail differently: the tell is not just "delve" and em dashes — it is
**overclaiming verbs hanging off observational coefficients, citation dumps,
uniform sentence rhythm, and conclusions that echo the abstract**. And Chinese
academic AI text has its own signature set (四字套话、虚词堆叠、总分总结构)
that English humanizers never touch.

This skill combines both, tuned for papers built on data and regression tables:

| Reference lineage | Language / layer | What we took |
|-------------------|------------------|--------------|
| [matsuikentaro1/humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic) | EN | academic pattern catalog; rhythm-first insight |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) (MIT) | EN | claim–evidence discipline; voice matching; novelty padding and vague-magnitude rules (EN25, EN28) |
| [blader/humanizer](https://github.com/blader/humanizer) (MIT) · [Nanako0129/sepia](https://github.com/Nanako0129/sepia) (MIT) | EN | chatbot residue and artifacts (EN23–24), staged contrast, takeaway closers, the second "what still reads as AI?" pass; sepia's evidence on rhythm thresholds, modes, deletion / reversion tests |
| [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) · [MrGeDiao/shuorenhua](https://github.com/MrGeDiao/shuorenhua) · [LifelongLazyLearner/qu-ai-wei](https://github.com/LifelongLazyLearner/qu-ai-wei) (MIT) | ZH | 否定对举、升华套话、限定词堆叠、加粗标签 (ZH18, 23–25); protect-list and editing boundaries; keep-rate → edit caps |
| [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) (CC BY-NC 4.0 — numbers cited, nothing copied) · [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) (MIT) | ZH | measured human-vs-AI rates behind ZH18–ZH27 and the ZH04 / 08 / 11 demotions; translationese (ZH21); change-rate gates |
| [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) · [harshaneel/humanize](https://harshaneel.github.io/humanize/) | EN | pattern taxonomy breadth |
| [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) · [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) · [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | EN | audit-report format; scoring discipline; the "never inject" list and detect / rewrite / edit modes |
| 本仓库前身 `chinese-de-aigc`（v1） | ZH | 17 类中文模式库、分章节策略、五维量表 |
| [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) (MIT; the most-starred de-watermark skill of Aug 2026) | provenance | the three-layer model (Unicode hygiene / statistical rewrite / container metadata), the code-point tables, and the rule that a report must state what it could *not* verify |
| [growwithnouman/claude-watermark-remover](https://github.com/growwithnouman/claude-watermark-remover) | provenance | report-only mode; typography as an opt-in layer, never a default |
| [Shreyan1/ai-text-watermark-remover](https://github.com/Shreyan1/ai-text-watermark-remover) (no licence — ideas only) · [cyzanfar/text-watermark-remover](https://github.com/cyzanfar/text-watermark-remover) (MIT) | provenance | remaining format characters, look-alike and metadata targets; two-way meaning-constraint checks. Their regenerate / detector-search evasion stages are **not** adopted |
| Anthropic, [*How Claude's text watermarking works*](https://www.anthropic.com/news/claude-text-watermark) (2026-08) | provenance | what the watermark is (word-choice bias, SynthID-Text lineage) and is not (no hidden characters); what survives editing and translation; C2PA on PNG / JPG / SVG |

What we changed relative to the upstream de-watermark tools: independent
testers found them damaging Japanese text and emoji, and a Chinese thesis has
more to lose — so the scrubber here is **CJK-aware** (keeps U+3000 indents,
fullwidth punctuation, ideographic variation selectors in names, `——` / `……`),
**never NFKC-folds** (R², ½, ＡＢ survive), leaves **en dashes and minus signs**
in tables alone, and skips code spans. And it refuses to describe anything as
"watermark-free".

## What's inside 结构

**Six-step loop 六步闭环**: intake/routing 定位路由 → audit 审计扫描 →
claim–evidence check 主张-证据核对 → differentiated rewrite 差异化改写 →
five-dimension self-score 五维自评 → cold-reader recheck 冷读复查 — with the
provenance layer threaded through it (`inspect` before the audit, the author's
ownership pass inside the rewrite, package `clean` at the recheck).

**Three modes 三种模式**: audit-only 只诊断 · edit 编辑 (per-section caps) ·
author-voiced 作者重述 (briefs for the high-signal sections; the author writes).

**Two pattern libraries 两套模式库**:

- [`references/patterns-en.md`](references/patterns-en.md) — EN01–EN30, with a
  preserve-list of legitimate academic phrases that must NOT be "fixed"
- [`references/patterns-zh.md`](references/patterns-zh.md) — ZH01–ZH28 中文模式库，含保护清单

**Section strategies 分章节策略**: [`references/sections.md`](references/sections.md)
— abstract through conclusion, bilingual symptoms, rewrite intensity per section

**Scoring 评分**: [`references/scoring.md`](references/scoring.md) — concreteness,
rhythm, calibration, implicit cohesion, researcher voice（含中英不同的句长阈值）

**Worked examples 案例**: [`references/examples-en.md`](references/examples-en.md)
(8 English cases) + [`references/examples-zh.md`](references/examples-zh.md)（12 组中文案例）

**Audit and fidelity 审计与保真**: [`scripts/aigc_audit.py`](scripts/aigc_audit.py)
(stdlib Python 3.9+) — `audit` runs every regex-visible rule after masking
quotations, math, citations and tables, and prints report-only metrics;
`compare` fails on any lost or invented number / citation / table reference and
reports change rate against the section cap plus draft retention. No AI
probability is ever printed.

```bash
python3 scripts/aigc_audit.py audit   draft.md                         # Step 1: rule hits by ¶ + metrics
python3 scripts/aigc_audit.py compare draft.md revised.md --section results   # Step 5: exit 1 if facts drifted
python3 scripts/aigc_audit.py compare model_draft.md mine.md --by author      # ownership pass: draft retention
```

**Provenance layer 溯源层（去水印）**: [`references/watermarks.md`](references/watermarks.md)
— the policy — and [`scripts/provenance_scrub.py`](scripts/provenance_scrub.py)
— the tool (stdlib Python 3.9+, no dependencies).

**Lineage 来源**: [`references/lineage.md`](references/lineage.md) — the
top-10 humanizer skills and two watermark removers, what was adopted and what
was not.

## The provenance layer in one table 去水印层一览

| Layer | What it is | Can you detect it? | What this skill does |
|---|---|---|---|
| **A · character carriers** 隐藏字符 | zero-width characters, bidi controls, tag characters, stray variation selectors, script-bound format characters, exotic spaces, soft hyphens, trailing-whitespace patterns, Cyrillic / Greek look-alikes in Latin words. *Not* used by Claude (Anthropic: "no hidden characters"); common from copy-paste chains and third-party tools; flagged by Turnitin as hidden text / replaced characters | yes, deterministically | `provenance_scrub.py inspect` / `clean` — context-aware, so emoji ZWJ sequences, Persian ZWNJ, Thai ZWSP, subdivision flags, CJK variation selectors, Russian citations and Greek notation survive; look-alikes are reported first and folded only with `--fold-homoglyphs` |
| **B · statistical watermark** 统计水印 | Claude (models launched ≥ 2026-08-02) and Gemini bias *which words* get sampled; survives copy, translation and light edits; only a complete rewrite in the author's words removes it; **no public detector** | no | the **ownership pass**: the agent delivers a brief, the author writes the high-signal sentences; `aigc_audit.py compare --by author` measures how much draft wording survives; every report ends `B: unknown` |
| **C · container metadata** 容器元数据 | C2PA manifests on model-generated PNG / JPG / SVG, including figures pasted into a `.docx`; `.docx` docProps (`python-docx`, real names), sensitivity labels, rsids, template paths, comments, people.xml, tracked changes; PDF Info + XMP incl. compressed streams and pdfTeX figure info; `__MACOSX` in a zip; macOS download-origin xattrs | yes | lossless `clean` for docx / png / jpg / svg / zip; report + `exiftool` / `qpdf` / pdfLaTeX / `xattr` commands for the rest; and the advice that matters most for a paper — regenerate figures from the replication package |

```bash
cd ~/.claude/skills/de-aigc-skills
python3 scripts/provenance_scrub.py inspect main.docx figures/*.png    # report only; exit 1 if anything is found
python3 scripts/provenance_scrub.py clean   main.docx --lang zh         # main.clean.docx: text runs cleaned, docProps blanked
python3 scripts/provenance_scrub.py clean   draft.md --diff             # carriers rendered as ⟨U+200B⟩ in the diff
python3 scripts/provenance_scrub.py clean   fig1.png                    # drops C2PA / EXIF / XMP chunks, pixels untouched
python3 scripts/provenance_scrub.py clean   submission.zip              # members cleaned in memory, __MACOSX / .DS_Store dropped
python3 scripts/provenance_scrub.py self-test                           # 54 keep / strip fixtures
```

A report looks like this — note the last two lines, which are the point:

```
== Provenance-mark report · 溯源标记报告 · main.docx ==
kind: docx   lang: zh   mode: clean
Layer A · invisible-character carriers 隐藏字符
  U+200B ZERO WIDTH SPACE                     37   removed
  U+202F NARROW NO-BREAK SPACE                12   → U+0020
  U+3000 IDEOGRAPHIC SPACE                    48   kept
Layer C · container metadata 容器元数据
  core: {"dc:creator": "python-docx", "cp:lastModifiedBy": "python-docx"}
  core_scrubbed: ["dc:creator", "cp:lastModifiedBy"]
  has_comments: true
Layer B · statistical watermark 统计水印: unknown — no public detector; only an author rewrite changes it
verdict: A: 49 carrier(s) cleaned · C: scrubbed docProps; still review has_comments · B: unknown
```

## Install 安装

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills.git /tmp/aers
cp -r /tmp/aers/skills/48-de-AIGC-skills ~/.claude/skills/de-aigc-skills
```

Or project-local: copy into `.claude/skills/de-aigc-skills`.

## Use 使用

Any of these triggers work 触发词示例:

- "Humanize this section / remove the AI writing patterns"
- "请对这段文本降 AIGC 检测率"
- "把这篇论文改得不像 AI 写的（中英文都要处理）"
- "Audit this draft for AI signatures before I submit"
- "诊断这段文字的 AI 痕迹，给出修改建议"
- "先扫一下这个 docx 有没有隐藏字符和元数据，再去水印"
- "Strip the invisible Unicode and C2PA from my submission package — report first"
- "这篇初稿是 Claude 写的，帮我做作者重述，处理统计水印"
- "只诊断，不要改：这段有哪些翻译腔和否定对举？"
- "Check that my revision kept every number and citation from the original"

## Works well with 配合

| 场景 Scenario | 组合 Combo |
|------|---------|
| 中文论文投稿 | `de-aigc-skills` + [49 humanize-chinese](../49-voidborne-d-humanize-chinese/)（非学术语域）|
| SSCI submission | `de-aigc-skills` + [70 ssci-polish](../70-ssci-polish/) |
| Biomedical manuscripts | [44 humanizer_academic](../44-matsuikentaro1-humanizer_academic/) first, then this skill's Step 2 claim–evidence audit |
| General prose | [45 deslop](../45-stephenturner-skill-deslop/) / [46 stop-slop](../46-hardikpandya-stop-slop/) |
| Audio / video / pixel-domain marks, whole-site audits | [guillaumemeyer/watermarks-remover](https://github.com/guillaumemeyer/watermarks-remover) — this skill covers text, `.docx`, figures and PDF |

## Integrity statement 学术诚信声明

The goal is to return human-written and AI-assisted text to a real researcher's
language distribution — **not** to help fully AI-generated work evade detection.

- ✅ 研究者自己的初稿被检测器误判；AI 辅助起草 + 人工修改定稿
- ✅ 清理自己稿件里的隐藏字符和元数据——双盲评审本来就要求这样做；Anthropic 也说明水印"不涉及所有权或作者身份"
- ❌ 完全 AI 生成的论文求"零改动过检"；代写、抄袭、数据造假
- ❌ 用溯源层掩盖作者无法为之负责的模型文本，或规避期刊的生成式 AI 披露要求——要求披露就披露

**Academic integrity outranks detection scores. 学术诚信优先于检测率。**
Numbers, coefficients, citations, and claims are never altered — when a claim
lacks evidence, the skill flags it instead of hiding it. And no report from
this skill will ever say "watermark-free" / "无水印" / "过检".

## Contributing 贡献

PRs welcome: new patterns (either language), discipline-specific hedge
libraries (finance vs. sociology differ), more section-level cases, paired
human / model corpora of *academic* Chinese and English to recalibrate the
report-only metrics (the upstream numbers come from general prose), new
`aigc_audit.py` fixtures (especially false positives on human-written papers),
and new keep / strip fixtures for `scripts/provenance_scrub.py` (especially
other scripts' legitimate format controls).
