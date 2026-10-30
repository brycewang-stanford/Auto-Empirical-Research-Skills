# Lineage · 来源与取舍（2026-10 升级）

The 2026-10 upgrade of `de-aigc-skills` started from a ranking of the ten
most-starred dedicated de-AI-tone agent skills on GitHub (repos that ship a
`SKILL.md`; general writing suites and non-skill tools excluded), plus the two
dedicated text-watermark removers. Each was read at source — `SKILL.md`,
pattern catalogs, detector scripts, evidence write-ups — not from its README
pitch. This file records what was adopted, where it now lives, and what was
deliberately left out because it is wrong for an empirical paper.

本次升级以 GitHub 上星数前十的"去 AI 味"专用 skill（带 `SKILL.md`，不含通用写作套件和非 skill 工具）
以及两个专做文本去水印的仓库为参照，逐个读了源文件。下表记录取了什么、放在哪、哪些刻意没取。

Stars as of 2026-10-30. Licenses as read from each repository's LICENSE file.
Nothing below is copied verbatim; rules, regexes and wording were rewritten for
academic papers, and numbers are quoted with their source.

## The ten humanizer skills 十个去 AI 味 skill

| # | Repository | ★ | License | Adopted → where | Not adopted |
|---|---|---|---|---|---|
| 1 | [blader/humanizer](https://github.com/blader/humanizer) | 62,403 | MIT | chatbot residue, knowledge-cutoff talk, markup leaks (EN23, EN24); staged contrast (EN08); takeaway closers (EN26); "arguing with no one" (EN29); repeated openers (EN30); process narration (EN12); the draft → "what still reads as AI?" → final second pass (SKILL.md Step 5) | flagging "associated with" as vague (§14) — it is the correct correlational verb; en-dash removal (§8) — breaks 2014–2022; opinion / humour voice |
| 2 | [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 21,475 | MIT | 否定对举 (ZH18); 升华套话 (ZH23); 限定词堆叠 (ZH24); 加粗标签 (ZH25); the hard constraint "keep facts, certainty and author voice" → the protect list in `patterns-zh.md` and the no-new-facts rule | — (its 31 patterns are general prose; the academic-register exceptions it grants — passives, 四字格, nominalisation — are on our protect list) |
| 3 | [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | 18,472 | MIT | phrase and structure lists behind EN26 / EN27 / EN28; "questions answered immediately" as a tell (scoring.md rhythm) | blanket bans — all adverbs, all hedges, all passives, "two items beat three"; "false agency" for "the market rewards…" |
| 4 | [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) | 6,325 | MIT | translationese as a family (ZH21); the real rhythm signal is *missing long sentences* (ZH06, EN19); change-rate gate (warn 30% / roll back 50%) → per-section caps in `aigc_audit.py compare`; script-verified, not self-reported, gates; "never market a feature as watermark removal" | Korean assertion rules (turn hedges into assertions, "commit to one side") — conflict with claim–evidence calibration; Korean comma and pronoun rules |
| 5 | [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | 5,328 | MIT | detect / rewrite / edit modes → our three modes (SKILL.md); the "never inject" list (no invented perspective, stakes, contrarianism, slogan fragments, dash theatrics, specifics); masking quotations and code before scanning; its own measurement that a composite score is a coin flip at paragraph level (ROC-AUC 0.501) → we print no AI-probability | the Node detector and its probability output; LinkedIn / blunt voice profiles |
| 6 | [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) | 4,614 | **CC BY-NC 4.0** | measured human-vs-AI rates quoted with attribution (ZH18–ZH27); the demotion of ZH04 / ZH08 / ZH11 and the rewrite of ZH06 from its re-measurements; "every edit maps to a rule id or is reverted"; "stop after the audit" | its text, regexes and tables (non-commercial licence; ours is CC BY-SA); "制造跳跃" (rule 11) — papers need their links; questions-for-rhythm from general prose |
| 7 | [Nanako0129/sepia](https://github.com/Nanako0129/sepia) | 3,554 | MIT | review / refactor / recreate → our three modes; "recreate adds no doubt or limitation the source does not state" → limitations are flagged for the author; deletion and reversion tests; position tells that survive paraphrase (EN26); detectors read the *body* better than the bookends (`sections.md`); the evidence against sentence-length thresholds (EN19, scoring.md) | fiction passes, personas, journalism domain packs |
| 8 | [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) | 3,034 | MIT | novelty padding (EN25); vague-magnitude hedges (EN28); compare against the strongest prior estimate; paragraph count in = paragraph count out; numbers, citations and claims never change (already ours) | deleting every "Notably," (2.10); splitting every sentence over 30 words (2.11) |
| 9 | [MrGeDiao/shuorenhua](https://github.com/MrGeDiao/shuorenhua) | 2,363 | MIT | keep-rate ≥ 0.85 → the per-section caps; in-place / bounded / structural edit scopes → data–model / results / intro–discussion caps; "what is inside the quotation marks" → policy quotations masked and protected | colloquial target register |
| 10 | [LifelongLazyLearner/qu-ai-wei](https://github.com/LifelongLazyLearner/qu-ai-wei) | 706 | MIT | `editing-boundaries.md` → protect list (formulas, standard definitions, proper names, citation binding, exclusions are not positive claims, correlation is not causation); fact-and-claim ledger before rewriting | platform patterns (小红书 / 公众号), emoji rules |

## The two text-watermark removers 两个去水印仓库

| Repository | ★ | License | Adopted → where | Not adopted |
|---|---|---|---|---|
| [Shreyan1/ai-text-watermark-remover](https://github.com/Shreyan1/ai-text-watermark-remover) ("reweave") | 19 | none on GitHub (ideas only, no code) | remaining format characters, homoglyph list, metadata targets (xattrs, vendor file names, generator stamps) → `provenance_scrub.py` v1.1; meaning-constraint checks (numbers, entities, negation, antonym polarity) → `aigc_audit.py compare` | blanket Cf stripping and NFKC (breaks R², β₁, −, U+3000 indents); unconditional homoglyph folding (breaks Russian); the "regenerate with an unwatermarked local model" stage — evasion by design; the human-likeness score as a gate |
| [cyzanfar/text-watermark-remover](https://github.com/cyzanfar/text-watermark-remover) | 11 | MIT | two-way constraint counting (lost *and* introduced numbers, citations, modality) → `compare`; the honest label "uncalibrated integration fixture" for KGW / Unigram / SynthID adapters → our `B: unknown` | `bias_inversion` / `adversarial` / `mitigate` modes that search for the smallest edit clearing a detector; confusables-skeleton folding |

Neither repository has a detector that works on Claude or Gemini text: the
SynthID adapter needs an operator-supplied key, and reweave's SynthID is a
self-built toy. The draft-retention metrics in `watermarks.md` §4.1 are the
defensible part — they measure how much of a model draft's wording survives,
and say nothing about authorship.

## Corrections this read forced on the existing skill 由此修正的旧内容

| Was | Now | Evidence |
|---|---|---|
| "Per 200 words force one ≤ 8-word and one ≥ 40-word sentence" (EN19, ZH06, scoring.md) | length follows content; merge / split, never manufacture alternation; metrics report-only | sentence-length CV AUROC 0.521 (sepia); "vary sentence length" prompts raised detection (sepia, BAIDYA-2026); lieflat "机械参差化比不改更糟" |
| "Fixing the 🔴 set moves detectors from 70%+ to 15–25%" (both pattern files), "预期通过率高" (scoring.md), detector-to-rule mapping table | removed | no measurement behind any of them; avoid-ai-writing's own composite score: ROC-AUC 0.501 |
| ZH04 段首连接词 🔴, ZH11 序数链 🔴, ZH08 被动 🟡 | 🟢, ZH04 only on a 3-paragraph run | lieflat: 14.4% vs 15.1%; δ+0.02; 3.2% vs 4.5% |
| ZH03 listed 显著的 | excluded | collides with 在 1% 水平上显著 |
| ZH14 "inject one hedge per 300 字", scoring "≥ 2 limitations", "≥ 10 numbers", "我们 2–3 次", examples adding citations | calibrate, don't inject; missing anchors and limitations become `[作者补：…]` / `[author: …]` placeholders | every upstream forbids adding facts the source does not state |
| English ✅ examples with em dashes, "X, not Y" closers, a rhetorical question answered at once | rewritten; checked with `aigc_audit.py` | EN20, EN08, EN26 — our own rules |
