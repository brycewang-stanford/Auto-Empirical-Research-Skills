# Watermarks & provenance marks · 水印与溯源标记（2026 年版）

Since August 2026 "去水印 / remove the Claude watermark" has been one of the most
searched phrases around AI-assisted writing. Three very different things get
called an "AI watermark", and a skill that treats them as one thing will either
do useless work (hunting hidden characters that are not there) or damage the
manuscript (folding legitimate CJK typography into ASCII). This file is the
policy behind the provenance layer of `de-aigc-skills`: what each mark is, what
can and cannot be done about it, and the exact code-point rules that
`scripts/provenance_scrub.py` implements.

2026 年 8 月起，"去 Claude 水印"成为 AI 辅助写作圈的高频需求。但被叫做"AI 水印"的其实是
三种完全不同的东西。把它们混为一谈，要么白忙（找根本不存在的隐藏字符），要么伤稿
（把合法的中文排版折叠成 ASCII）。本文件是本 skill 溯源层的政策依据。

---

## 1 · Three kinds of marks 三类标记

| | W1 · Statistical watermark 统计水印 | W2 · Character carriers 字符载体 | W3 · Container metadata 容器元数据 |
|---|---|---|---|
| **What it is** | A bias in *which words the model picks*, keyed by a secret (SynthID-Text lineage). Nothing is added to the string. | Invisible or look-alike code points inserted into the string: zero-width characters, bidi controls, tag characters, stray variation selectors, exotic spaces, soft hyphens. | Data in the file wrapper, not the text: C2PA manifests, EXIF/XMP, `.docx` docProps / comments / people.xml / customXml, PDF Info + XMP. |
| **Who uses it (2026)** | **Claude** — models launched on or after 2026-08-02, older models being added; applies across claude.ai, API, Claude Code. **Gemini** (SynthID). | **Not Claude** — Anthropic: "nothing is added to the text and there are no hidden characters." Seen from some third-party tools, browser copy-paste chains, PDF text extraction, some web "humanizers", and hidden-text plagiarism tricks. | **Claude** signs the PNG / JPG / SVG files it generates (C2PA). Every editor writes docProps (`python-docx`, Word, LibreOffice, pandoc). matplotlib / Inkscape write SVG `<metadata>`. |
| **Can you detect it?** | **No.** No public detector; Anthropic's detection API is a private preview for EU-eligible organisations. | **Yes**, deterministically: `provenance_scrub.py inspect`. | **Yes**: `inspect` for docx / png / jpg / svg / pdf; `exiftool`, `c2patool` for confirmation. |
| **Survives** | copy-paste, translation ("every word is chosen by Claude"), light editing; weaker on factual, constrained passages. | nothing — a find-and-replace removes it. | nothing — but PDF metadata can linger in incremental updates unless the file is rewritten. |
| **Removed by** | **Only replacing the words** — an author rewrite. Not synonym swaps, not sentence shuffles, not another LLM (that *re*-watermarks). | Layer A of this skill (`clean`). | Layer C of this skill (`clean` for docx / png / jpg / svg; `exiftool` + `qpdf` for pdf). Best for a paper: regenerate figures from the replication package. |
| **Where in the loop** | Step 3 · the ownership pass (§4) | before Step 1 and after Step 3 | Step 5 · on the submission package |

---

## 2 · What Anthropic actually says 官方口径（2026-08）

Read the primary source before believing a "remover" tool's claims. Anthropic's
announcement (*How Claude's text watermarking works*, Aug 2026) and the help
article *How Claude marks AI-generated content* state:

| Statement | Implication for this skill |
|---|---|
| The watermark is a SynthID-Text-style change to the *source of randomness* when Claude chooses among equivalent words; "nothing is added to the text and there are no hidden characters." | Scanning for zero-width characters is **not** de-watermarking. Layer A is hygiene, not a watermark remover, and the report must never present it as one. |
| Confidence grows with passage length; the signal is "sparser on factual passages" with constrained word choice. | Data sections, model equations, tables and robustness text carry weak signal. Abstract, introduction, literature and discussion carry most of it — the same sections the de-AIGC loop already rewrites hardest (`sections.md`). |
| Light editing "probably won't remove watermarking completely"; a **complete rewrite** does, because "nearly all the words are the person's." | Layer B *is* the author rewriting. Step 3's model-suggested sentences do not count; only sentences the author writes do (§4). |
| Translation carries the mark forward because "every word is chosen by Claude." | Translating an English Claude draft into Chinese (or the reverse) does not help. The bilingual route through this skill is *two* ownership passes, not one translation. |
| C2PA signing applies to supported `.png`, `.jpg`, `.svg` files; "nothing in the file changes" — the manifest sits in metadata. | Figures a model produced carry a signed manifest. `inspect` reports it; regenerating the figure from your own code is the clean answer. DOCX / PDF C2PA support is **not** confirmed by Anthropic — but docProps still name the generator. |
| "A watermark only helps test whether Claude might have produced or processed the content. It doesn't say anything about ownership or authorship, and doesn't change a user's rights under our terms." | The skill's integrity line stands: the author must be able to defend every sentence, and where the venue asks for an AI-use disclosure, disclose. Cleaning marks on content you own is legitimate; misrepresenting authorship is not. |
| Detection API: private preview for regulators, fact-checkers, researchers, educational organisations, EU civil society, and enterprises with compliance needs. | You cannot verify removal. Every report ends with **"B: unknown."** |

---

## 3 · Layer A · code-point policy 字符层规则

Adapted from the open-source `watermarks-remover` skill (guillaumemeyer, MIT — the
most-starred de-watermark project of Aug 2026) and `claude-watermark-remover`
(growwithnouman), then **tightened for bilingual academic manuscripts**. Independent
testers reported that the general-purpose tools damaged Japanese text and emoji;
a Chinese thesis has far more to lose (indents, fullwidth punctuation, name
variants, dashes). Hence the CJK-aware context rules below.

### 3.1 Always removed 一律删除

| Code points | Name | Why it is never legitimate in prose |
|---|---|---|
| U+00AD | soft hyphen | invisible; a classic carrier; Word rehyphenates anyway |
| U+034F | combining grapheme joiner | steganography staple |
| U+2060–U+2064 | word joiner, invisible operators | invisible; `U+2061` is only legitimate inside MathML, which lives outside `<w:t>` |
| U+2065, U+206A–U+206F | reserved / deprecated format controls | no rendering, no meaning |
| U+FEFF | zero width no-break space / BOM | strip everywhere (a leading BOM is reported separately) |
| U+FFF0–U+FFFB | specials, interlinear annotation | never rendered |
| U+FDD0–U+FDEF, U+xxFFFE, U+xxFFFF | noncharacters | invalid in interchange |
| U+E0000, U+E0080–U+E00FF, U+E01F0–U+E0FFF | reserved tag-block ranges | no assigned meaning |
| C0 / C1 controls except TAB, LF, CR | control characters | corrupt copy-paste and search |
| U+2028, U+2029, U+0085 | line / paragraph separators, NEL | normalised to `\n` |

### 3.2 Removed unless the context is legitimate 视上下文保留

| Code point(s) | Kept when | Otherwise |
|---|---|---|
| U+200B ZWSP | adjacent to Thai, Lao, Myanmar, Khmer or Tibetan letters (word segmentation) | removed |
| U+200C ZWNJ | adjacent to Arabic / Persian / Syriac / Indic / Tibetan / Myanmar / Khmer / Mongolian letters | removed |
| U+200D ZWJ | inside an emoji sequence (👨‍👩‍👧, 👩🏽‍🔬) or between joiner-script letters | removed |
| U+200E, U+200F, U+061C, U+202A–U+202E, U+2066–U+2069 (bidi) | the same line contains right-to-left script (Hebrew, Arabic, Syriac, Thaana, N'Ko) or `--keep-bidi` | removed |
| U+E0001, U+E0020–U+E007F (tag characters) | preceded by 🏴 U+1F3F4 — a subdivision flag (🏴󠁧󠁢󠁳󠁣󠁴󠁿) | removed |
| U+FE00–U+FE0D (VS1–14) | after a CJK ideograph, a math symbol (∅︀) or an emoji base | removed |
| U+FE0E, U+FE0F (VS15/16) | after an emoji base, keycap base, CJK or math symbol (❤️, 1️⃣) | removed |
| U+E0100–U+E01EF (ideographic variation selectors) | after a CJK ideograph — glyph variants in personal and place names (邊󠄀 / 邊) | removed |
| U+180B–U+180F (Mongolian selectors) | adjacent to Mongolian letters | removed |
| U+115F, U+1160, U+3164, U+FFA0 (Hangul fillers) | adjacent to Hangul | removed |

### 3.3 Normalised, not removed 规范化为普通空格

| Code point(s) | Action | Note |
|---|---|---|
| U+2000–U+200A, U+202F, U+205F, U+1680 (exotic spaces) | → U+0020 | look-alike spaces are the most common carrier in 2026 tooling |
| U+00A0 NBSP | → U+0020 (`--keep-nbsp` to preserve) | Word inserts NBSP deliberately ("Table 3"); the change is typographic, never semantic |
| U+3000 ideographic space | **kept** in Chinese manuscripts or next to CJK; → U+0020 in English prose | 中文段首两个全角空格是排版规范，不是水印 |

### 3.4 Never touched 绝不改动

These are the places where a generic scrubber breaks an empirical paper:

- **U+2013 en dash** — year ranges 2014–2022, page ranges pp. 12–15, confidence intervals 7%–17%.
- **U+2212 minus sign** — negative coefficients in tables exported from Stata / R / LaTeX.
- **Superscripts and subscripts** — R², β₁, m³; **Greek letters**; **≤ ≥ × ‰**.
- **Fullwidth punctuation** in Chinese —，。；：（）《》「」— and Chinese dashes `——` and ellipsis `……`, which are *correct* Chinese typography. The English em-dash rule (EN20) never applies to Chinese text.
- **U+00B7 middle dot** in transliterated names (亚当·斯密) and U+30FB in Japanese.
- **Curly quotes** — standard in Word manuscripts and in Chinese; converted to straight quotes only with `--typography`, only in English source files (`.md`, `.tex`).
- **Em dashes in English** are counted and listed for the author (EN20 decides comma / parenthesis / period per case) — never auto-replaced.
- **NFKC normalisation is never applied.** It would fold R² → R2, ½ → 1/2, ﬁ → fi, fullwidth ＡＢ → AB, and turn a Chinese manuscript's punctuation into ASCII. Upstream tools offer `--nfkc` as an option; here it does not exist.
- **Code spans and fenced blocks** in Markdown / HTML are skipped, so a document *about* invisible characters keeps its examples.

### 3.5 Where Layer A runs in the loop

- **Before Step 1 (audit).** Hidden characters split words, so regex-based
  pattern scans and detector n-grams see `re​form` as two tokens. Clean first,
  then audit.
- **After Step 3 (rewrite).** Pasting between editors re-introduces NBSP / U+202F.
  Run `inspect` on the final text; the report goes into the change log.
- Turnitin's Similarity "Flags" (hidden text, replaced characters) treat
  carriers as manipulation. An honest author whose `.docx` picked them up through
  copy-paste is the person Layer A protects.

---

## 4 · Layer B · the ownership pass 作者重述

This is the only part of the skill that touches the statistical watermark, and it
has to be stated plainly:

> **Every sentence the agent writes is model output.** If the model carries a
> token-sampling watermark, so does its rewrite. Running the six-step loop and
> accepting the agent's Step 3 text wholesale does not remove a Claude watermark
> — it replaces one Claude passage with another.

So Step 3 splits into two deliverables:

1. **The brief (agent).** For every flagged paragraph: what it must say, which
   table / coefficient / citation anchors it, which rules fired (EN/ZH ids),
   what rhythm is missing (where the short sentence goes, where the long one), and
   a *suggested* rewrite marked as such.
2. **The sentences (author).** The author drafts the high-signal sections —
   abstract, introduction, literature, hypotheses framing, discussion,
   conclusion — from the brief, **without the suggested sentence in view**
   (close the pane, or dictate). Numbers, names and years come from the brief;
   the words come from the author. Low-signal sections (data, model equations,
   table notes, robustness lists) may keep model polish; say so in the change log.
3. **The check (agent).** Fidelity diff of every number / name / year /
   citation; fluency read; rule re-audit. The agent flags, it does not rewrite.

Change-log labels, per paragraph: `author-voiced` · `model-suggested, author-accepted` · `untouched`.

**What does not work — and why it is worse than nothing**

| Attempt | Outcome |
|---|---|
| Paraphrase with Claude / Gemini "to remove the watermark" | re-embeds a watermark (the same one, or SynthID's) |
| Back-translation through an LLM | same — every word is again the model's |
| Synonym swaps, sentence inversion, spinner tools | leave the token distribution largely intact and raise the AI-style score the rest of this skill lowers |
| Injecting typos / archaic words for perplexity | fails referees before it fails detectors |
| Stripping invisible characters and declaring "watermark-free" | false claim — the watermark was never in characters |

**Report line, always:** `B: unknown`. There is no public detector; nobody can
verify removal, and this skill will not pretend to.

---

## 5 · Layer C · package hygiene 投稿包元数据

Double-blind review already requires most of this; the AI-provenance angle adds
C2PA on figures and generator strings in docProps.

| Artifact | What to look for | Command |
|---|---|---|
| `.docx` | `docProps/core.xml`: `dc:creator`, `cp:lastModifiedBy` (e.g. `python-docx`, a real name), `dc:description`; `docProps/app.xml`: `Company`, `Manager`; `word/comments.xml`, `word/people.xml` (comment authors), tracked changes `<w:ins>/<w:del>`, `customXml/`, `docProps/thumbnail.*` | `provenance_scrub.py clean paper.docx` blanks the docProps fields and cleans Layer A inside text runs. Comments / tracked changes / people.xml are **reported**, not deleted — accept all changes and delete comments in Word, then re-run `inspect`. |
| `.pdf` | Info dictionary (`/Producer`, `/Creator`, `/Author`), XMP (`<x:xmpmeta>`), C2PA (`jumb`), incremental updates that keep old metadata alive | report only: `exiftool -all= -overwrite_original paper.pdf` then `qpdf --linearize paper.pdf paper.clean.pdf`; verify with `c2patool`. |
| `.png` / `.jpg` figures | C2PA manifest (`caBX` chunk / APP11 JUMBF), EXIF, XMP, `tEXt Software`, IPTC | `clean` drops those chunks / segments **losslessly** (no re-encode; ICC profiles and JFIF/Adobe markers are kept). Verify with `c2patool fig.png`. Better: re-export from the plotting script. |
| `.svg` figures | `<metadata>` (Inkscape RDF, matplotlib dates), generator comments, `c2pa` namespaces | `clean` removes `<metadata>` and comments; if `c2pa` strings remain, regenerate the figure. |
| `.tex` / `.md` / `.bib` | Layer A carriers only | `clean` |

The right instinct for an empirical paper is stronger than any scrubber: every
figure and table should come out of the replication package's own scripts.
Regenerated output has no manifest to remove.

---

## 6 · Report block 报告格式

Attach to the Step 1 audit and again to the Step 5 change log:

```
== Provenance-mark report · 溯源标记报告 · main.docx ==
kind: docx   lang: zh   mode: clean
Layer A · invisible-character carriers 隐藏字符
  U+200B ZERO WIDTH SPACE                     37   removed
  U+202F NARROW NO-BREAK SPACE                12   → U+0020
  U+3000 IDEOGRAPHIC SPACE                    48   kept
  U+E0100 VARIATION SELECTOR-17                1   kept
Layer C · container metadata 容器元数据
  core: {"dc:creator": "python-docx", "cp:lastModifiedBy": "python-docx"}
  core_scrubbed: ["dc:creator", "cp:lastModifiedBy"]
  has_comments: true
Layer B · statistical watermark 统计水印: unknown — no public detector; only an author rewrite changes it
verdict: A: 49 carrier(s) cleaned · C: scrubbed docProps; still review has_comments · B: unknown
```

Rules for the prose around it: name what was verified (A, C), name what was not
(B), never write "watermark-free", "无水印", "undetectable" or "过检".

---

## 7 · Sources 来源

- Anthropic, *How Claude's text watermarking works* (Aug 2026) — <https://www.anthropic.com/news/claude-text-watermark>
- Claude Help Center, *How Claude marks AI-generated content* — <https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content>
- Dathathri et al., *Scalable watermarking for identifying large language model outputs* (SynthID-Text), *Nature* 634, 2024
- guillaumemeyer/watermarks-remover (MIT) — layer model, code-point tables, honest-reporting rule — <https://github.com/guillaumemeyer/watermarks-remover>
- growwithnouman/claude-watermark-remover — report-only mode, optional typography layer — <https://github.com/growwithnouman/claude-watermark-remover>
- Independent tests of the August 2026 remover tools (pasqualepillitteri.it; BleepingComputer, *AI "watermark removers" flood the web. Almost none can prove they work.*) — the CJK / emoji breakage and the "no public detector" caveat come from here
- Turnitin, Similarity Report *Flags* (hidden text, replaced characters)

---

## 8 · Integrity 学术诚信

Cleaning provenance marks on content you own is legitimate hygiene, and
double-blind submission requires part of it. It is not a licence to present a
fully model-generated manuscript as your own. The tests in `SKILL.md` still
apply: the author owns every claim, every number stays, and where a venue asks
for a generative-AI disclosure, the disclosure is made. Academic integrity
outranks detection scores — and it outranks watermark reports too.
