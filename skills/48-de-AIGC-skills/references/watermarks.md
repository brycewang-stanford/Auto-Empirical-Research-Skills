# Watermarks & provenance marks · 水印与溯源标记（2026 年版）

Since August 2026 "去水印 / remove the Claude watermark" has been one of the most
searched phrases around AI-assisted writing. Three very different things get
called an "AI watermark", and a skill that treats them as one thing will either
do useless work (hunting hidden characters that are not there) or damage the
manuscript (folding legitimate CJK typography into ASCII). This file is the
policy behind the provenance layer of `de-aigc-skills`: what each mark is, what
can and cannot be done about it, and the exact code-point rules that
`scripts/provenance_scrub.py` implements.

**2026-10 update.** Compared against the two dedicated text-watermark removers
on GitHub (Shreyan1/ai-text-watermark-remover "reweave", the most-starred at
19★; cyzanfar/text-watermark-remover, MIT) and im-not-ai's watermark runbook,
the provenance layer now also covers script-bound format characters, Latin
look-alikes (report-first, math- and Cyrillic-safe), whitespace-pattern
steganography, figures pasted *inside* a `.docx`, docx rsids / template paths /
sensitivity labels, compressed PDF streams and pdfTeX figure info, `__MACOSX`
entries in a submission zip, and macOS download-origin attributes — and gains
a *draft-retention* measurement for the ownership pass (§4.1). Neither upstream
repo has a detector that works on Claude or Gemini text (§7).

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
| U+0600–0605, 06DD, 0890–0891, 08E2 (Arabic number signs), U+070F (Syriac), U+17B4–17B5 (Khmer), U+110BD / 110CD (Kaithi), U+13430–1343F (Egyptian), U+1BCA0–1BCA3 (shorthand), U+1D173–1D17A (musical) | next to a letter of the same script. The ranges are hard-coded, not "any Cf", so the policy does not shift with the interpreter's Unicode version | removed |
| U+180B–U+180F (Mongolian selectors) | adjacent to Mongolian letters | removed |
| U+115F, U+1160, U+3164, U+FFA0 (Hangul fillers) | adjacent to Hangul | removed |

### 3.3 Normalised, not removed 规范化为普通空格

| Code point(s) | Action | Note |
|---|---|---|
| U+2000–U+200A, U+202F, U+205F, U+1680 (exotic spaces) | → U+0020 | look-alike spaces are the most common carrier in 2026 tooling |
| U+00A0 NBSP | → U+0020 (`--keep-nbsp` to preserve) | Word inserts NBSP deliberately ("Table 3"); the change is typographic, never semantic |
| U+3000 ideographic space | **kept** in Chinese manuscripts or next to CJK; → U+0020 in English prose | 中文段首两个全角空格是排版规范，不是水印 |
| Trailing spaces / tabs before a line break | removed in `.txt` `.tex` `.bib` `.html`; in Markdown exactly two trailing spaces (a hard break) are kept; **never** in `.csv` / `.tsv` (a trailing tab is an empty field) or inside docx runs | SNOW-style tools hide bits here. Three or more lines with trailing whitespace of different shapes, or a tab / space mix, raise a `whitespace_pattern` note. Double spaces *inside* a line are never collapsed (tables, alignment) |

### 3.3a Look-alikes 形近字符

| Code point(s) | Action | Why it is safe |
|---|---|---|
| U+037E → `;`, U+0387 → `·`, U+0374 → `ʹ`, U+1FEF → `` ` ``, U+1FFD → `´`, U+212A Kelvin → `K`, U+212B Ångström → `Å`, U+2126 Ohm → `Ω`, U+0340 / 0341 / 0343 → their canonical combining marks | → canonical | each is a *singleton* canonical decomposition: the fold is exactly what NFC does to that character and nothing else (the test suite checks this against `unicodedata`). Whole-text NFC is still never applied — it rewrites CJK compatibility ideographs (U+F900 → U+8C48) that appear in names |
| Fullwidth Latin letters / digits (U+FF10–FF19, FF21–FF3A, FF41–FF5A) | → ASCII **only inside an otherwise-ASCII word in an English manuscript** ("ＴFP" → "TFP", "Table３" → "Table3") | a standalone "ＡＢ" is left alone, and Chinese text keeps fullwidth digits (GB/T 15835 prefers half-width, but that is the author's call) |
| Cyrillic / Greek letters inside a Latin word ("Тhe" with Cyrillic Т; "rеform" with Cyrillic е) | **reported** as `review (homoglyph)`; folded only with `--fold-homoglyphs` | a word is flagged only if it has ≥ 2 ASCII letters and *every* non-ASCII letter in it is a known look-alike; words with no Latin letters (a Russian citation, a standalone β) are never touched; `$…$`, `\(…\)`, `\[…\]` and equation environments are skipped; μ, β, Δ and other Greek notation are not on the list. Upstream folds 25 letters with no context check and turns *Экономика России* into *Экoнoмикa Рoccии* |

### 3.4 Never touched 绝不改动

These are the places where a generic scrubber breaks an empirical paper:

- **U+2013 en dash** — year ranges 2014–2022, page ranges pp. 12–15, confidence intervals 7%–17%.
- **U+2212 minus sign** — negative coefficients in tables exported from Stata / R / LaTeX.
- **Superscripts and subscripts** — R², β₁, m³; **Greek letters**; **≤ ≥ × ‰**.
- **Fullwidth punctuation** in Chinese —，。；：（）《》「」— and Chinese dashes `——` and ellipsis `……`, which are *correct* Chinese typography. The English em-dash rule (EN20) never applies to Chinese text.
- **U+00B7 middle dot** in transliterated names (亚当·斯密) and U+30FB in Japanese.
- **Curly quotes** — standard in Word manuscripts and in Chinese; converted to straight quotes only with `--typography`, only in English source files (`.md`, `.tex`).
- **Em dashes in English** are counted and listed for the author (EN20 decides comma / parenthesis / period per case) — never auto-replaced.
- **NFKC normalisation is never applied.** It would fold R² → R2, ½ → 1/2, ﬁ → fi, fullwidth ＡＢ → AB, and turn a Chinese manuscript's punctuation into ASCII. Upstream tools offer `--nfkc` as an option; here it does not exist. A simulation of reweave's scrubber on an econ manuscript turned `R²` into `R2`, `β₁` into `β1`, `−0.043` into `-0.043`, `（2014–2022）` into `(2014-2022)`, `——` into `--`, and deleted every Chinese paragraph indent; cyzanfar's "safe" mode turns U+3000 into a plain space.
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

### 4.1 Draft retention — the one number available 草稿保留率

There is no detector, but there is arithmetic. A SynthID-style mark scores each
token against the few tokens before it, so only stretches that survive
*verbatim* from the model draft still carry the bias. Run the author's text
against the model draft:

```bash
python3 scripts/aigc_audit.py compare model_draft.md author_final.md --by author
```

| Metric | Formula | Reads as |
|---|---|---|
| `R_n` (n = 2–5 words; 3, 4, 6, 8 characters for Chinese) | Σ_g min(c_final(g), c_draft(g)) / Σ_g c_final(g) over n-grams g | share of the final text's n-grams that were already in the draft |
| `V_k` (k = 8 words / 12 characters) | final-text tokens inside verbatim runs of ≥ k tokens ÷ final-text tokens | how much of the text is long copied stretches |
| `longest_verbatim_run` | longest matching block | the single worst stretch |

The report line reads `B: unknown · draft-retention R2=…, R3=…, R4=…, R5=…,
V8=…`. What it can and cannot say:

- High `R4` / `V8` → most of the draft's wording is still there; the paragraph
  is not yet `author-voiced`, whatever the change log says.
- Low numbers bound how much draft wording survives. They do **not** show
  authorship: a paraphrase by another model also drives them down while
  writing a fresh watermark (§4, "What does not work"). That is why the
  labels stay with the author and the report still says `B: unknown`.
- No threshold turns these into a verdict. reweave's own toy experiment
  (a word-level SynthID with its own key) still detected the mark 99% of the
  time after ~10% of words changed and about 8% of the time after half — the
  direction is clear, the operating point for Claude is not public.

The same command runs the fidelity gate (every number, citation, table
reference and significance statement must survive the author's rewrite), so
one call answers both "is it still the model's wording?" and "did the facts
survive?".

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
| `.docx` (2026-10) | `docProps/custom.xml` sensitivity labels (`MSIP_Label_*`: owner e-mail, tenant id) and WPS stamps (`KSOProductBuildVer`, `ICV`); `w:rsid*` revision-session ids in every part; the attached-template path in `word/_rels/settings.xml.rels` (often `C:\Users\<name>\…\Normal.dotm`); figures pasted into the document (`word/media/*.png|jpg`) with their own C2PA / EXIF / XMP | `clean` removes the identifying custom properties (Zotero / Mendeley properties are **kept** — citations need them), strips rsids, reduces the template path to its file name, and cleans embedded figures losslessly |
| `.pdf` (2026-10) | XMP and Info hidden in Flate-compressed object streams; pdfTeX's `/PTEX.FileName` / `/PTEX.InfoDict` (each included figure's own Info, e.g. Matplotlib); absolute paths (`/Users/<name>/…`) | `inspect` now inflates streams before scanning and prints the pdfLaTeX fix: `\pdfsuppressptexinfo=-1 \pdftrailerid{} \pdfinfoomitdate=1` |
| `.zip` submission package | `__MACOSX/._*` AppleDouble entries (they carry each file's extended attributes, including the download URL), `.DS_Store`, `Thumbs.db`; every member of a known kind | `clean` drops the junk entries and cleans members in memory (docx / md / tex / png / jpg / svg) |
| any file on macOS | `com.apple.quarantine`, `kMDItemWhereFroms` (download URL), `kMDItemDownloadedDate` | reported; `xattr -c FILE` |
| file names | `claude_draft_v3.docx`, `gpt4-figure2.png` | reported — rename before submission |
| source files | front matter `generator:` / `model:`, `<meta name="generator">`, `<!-- generated by … -->`, "Generated with ChatGPT" lines | reported, never auto-removed (front matter can be load-bearing) |
| `.tex` / `.md` / `.bib` | Layer A carriers and trailing-whitespace patterns | `clean` |

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
- Shreyan1/ai-text-watermark-remover ("reweave"; no license file — ideas only, no code) — the blanket format-character list, homoglyph and metadata scrub lists, and the meaning-constraint checker (numbers, entities, negation, antonym polarity) that `aigc_audit.py compare` adapts for papers. Its headline claim to remove "SynthID-Text, KGW, Unigram" rests on a self-built word-level SynthID toy (KGW and Unigram are never run), and its "regenerate with an unwatermarked local model" stage is evasion by design — not adopted
- cyzanfar/text-watermark-remover (MIT) — two-way constraint counting (lost *and* introduced numbers, citations, modality) and the honest labelling of its KGW / Unigram / SynthID adapters as uncalibrated integration fixtures that need an operator-supplied key; its `bias_inversion` / `adversarial` / `mitigate` modes search for the smallest edit that clears a detector — not adopted
- epoko77-ai/im-not-ai, `docs/watermark-baseline-runbook.md` (MIT) — never market a feature as watermark removal; baselines are estimates

---

## 8 · Integrity 学术诚信

Cleaning provenance marks on content you own is legitimate hygiene, and
double-blind submission requires part of it. It is not a licence to present a
fully model-generated manuscript as your own. The tests in `SKILL.md` still
apply: the author owns every claim, every number stays, and where a venue asks
for a generative-AI disclosure, the disclosure is made. Academic integrity
outranks detection scores — and it outranks watermark reports too.
