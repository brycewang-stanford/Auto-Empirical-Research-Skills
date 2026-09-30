# Humanizer Academic

A skill that removes signs of AI-generated writing from academic medical papers, making them sound more natural and professionally written.

The main instructions are in `SKILL.md`, with reusable examples in `references/reader-clarity.md`. Both are plain text, so you do not need Claude Code to use them.

## Usage

### In a browser (Claude, ChatGPT, or anything that takes an attachment)

1. Download [`SKILL.md`](SKILL.md) and [`references/reader-clarity.md`](references/reader-clarity.md) from this repository.
2. Upload both files to the chat along with the text you want to edit.
3. Ask: `Apply this skill to the following manuscript text: [your text]`

That is all. No installation.

### In Claude Code

Clone into your skills directory:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/matsuikentaro1/humanizer_academic.git ~/.claude/skills/humanizer_academic
```

Or, from a downloaded copy of the repository:

```bash
mkdir -p ~/.claude/skills/humanizer_academic/references
cp SKILL.md ~/.claude/skills/humanizer_academic/
cp references/reader-clarity.md ~/.claude/skills/humanizer_academic/references/
```

The skill loads itself when it is relevant, so you can simply ask:

```
Please humanize this academic text: [your text]
```

## Overview

Based on [Wikipedia's "Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide, adapted for medical and scientific literature. Examples are derived from the EMPA-REG OUTCOME trial publications and from the author's (K. Matsui) observations during academic manuscript editing.

### Key Insight from Wikipedia

> "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."

## 34 Patterns Detected (with Before/After Examples)

### Content Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 1 | **Significance inflation** | "represents a pivotal challenge in the evolving landscape" | "is highly prevalent in patients with diabetes" |
| 2 | **Notability claims** | "landmark trial, led by renowned investigators" | "A total of 7020 patients..." |
| 3 | **Superficial -ing analyses** | "highlighting the cardioprotective effects" | Report data without interpretation |
| 4 | **Promotional language** | "groundbreaking study showcases the profound impact" | "empagliflozin reduced heart failure hospitalization" |
| 5 | **Vague attributions** | "Studies have shown... Experts argue..." | "In the EMPA-REG OUTCOME trial..." |
| 6 | **Formulaic challenges** | "Despite challenges... future outlook" | State specific limitations |

### Language Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 7 | **AI vocabulary** | "pivotal... landscape... crucial" | Remove or replace with simple words (note: "Additionally" is allowed once per paragraph) |
| 8 | **Copula avoidance** | "serves as... standing as... representing" | "is" |
| 9 | **Negative parallelisms** | "Not only X but also Y" | "X and Y" |
| 10 | **Rule of three** | "efficacy, safety, and tolerability" | Use natural number of items |
| 11 | **Synonym cycling & term consistency** | "Patients... Participants... Subjects" | "Patients" throughout (same construct = same term) |
| 12 | **False ranges** | "from renal function to cardiac outcomes" | List benefits directly |

### Style Patterns

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 13 | **Em dash elimination** | "benefits—a 35% reduction—appeared early—" | Use commas, parentheses, or periods. Every em dash is replaced, including natural-looking ones |
| 14 | **Title Case Headings** | "Statistical Analysis And Primary Endpoints" | "Statistical analysis and primary endpoints" |
| 15 | **Curly quotes** | “clinically significant” | "clinically significant" |

### Filler and Hedging

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 16 | **Filler phrases** | "In order to", "Due to the fact that" | "To", "Because" |
| 17 | **Redundant multi-layered hedging** | "may suggest... have the potential to confer" | "suggest... may reduce" (keep 1-2 hedges) |
| 18 | **Generic conclusions** | "The future looks bright" | Specific findings and implications |

### LLM-Specific Word Choice Patterns (v1.1.0)

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 19 | **"linked to" → "associated with"** (context-dependent) | "has been linked to shorter sleep duration" | "has been reported to be associated with" |
| 20 | **"Beyond" → "In addition to"** | "Beyond the association with..." | "In addition to the association with..." |
| 21 | **"via" → "through"** | "obtained via the online form" | "obtained through an online form" |
| 22 | **Insufficient hedging** | "may reduce the risk of..." | "may help reduce the risk of..." |
| 23 | **Artificially condensed expressions** | "fatigue–sleepiness cycle", "mutual reinforcement" | "cycle of fatigue and sleepiness", "a self-reinforcing cycle, with each behavior possibly exacerbating the other" |
| 24 | **"where" as a non-locative connector** | "...at the most intensive level, where almost daily use was..." | "...at the most intensive level, with almost daily use..." |
| 25 | **"yield" as a result verb** | "did not yield stable estimates" | "failed to produce stable estimates" |
| 26 | **Minor word-choice refinements** | "interpretations remain speculative", "speculative given the small sizes" | "interpretations are still speculative", "speculative due to the small sizes" |

### Cohesion and Connective Patterns (v1.1.4–1.3.0)

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 27 | **Preserve logical discourse markers** + vary by relation (do NOT over-trim) | (aggressive removal of "Although / Whereas / Thus / Based on these results") | Keep connectives that make the logic explicit; vary them by relation (result / contrast / concession) only to avoid mechanical repetition, never for decoration |
| 28 | **Re-contextualize over-condensed semantic links** | "unmet needs to discuss their difficulties" | "unmet needs when it comes to discussing their difficulties" |
| 29 | **Ornamental -ly intensifier adverbs** | "markedly reduced", "critically important", "remarkably consistent" | Remove decorative intensifiers; keep functional ones ("slightly", "consistently", "approximately") |
| 30 | **Connective-preserving edits** (never bare-delete a transition) | "X reduced death. The benefit appeared within months." (choppy) | "X also reduced death, and this benefit appeared within months." |
| 31 | **Paragraph cohesion** (old-to-new flow + paragraph-opening markers) | Disconnected sentences after editing | Mandatory final check: each sentence links to the previous one; contrast/continuity openers (However / On the other hand / Overall / Taken together) survive |
| 32 | **Paraphrastic repetition** | "X is associated with Y. In other words, X may contribute to Y. That is, X plays a role in Y." | State each claim once; keep the most specific version |
| 33 | **Content-free evaluation sentences** | "This is a noteworthy finding." "This observation is of clinical significance." | Delete standalone verdicts; if important, show why with data or mechanism |

### Sentence Rhythm and Reader Clarity (v2.3)

| # | Pattern | Before | After |
|---|---------|--------|-------|
| 34 | **Sentence rhythm & burstiness, in the service of clarity** | Uniform 18-22 word sentences; stacked conditions and unclear comparisons | Vary sentence lengths and openings in every paragraph by splitting stacked sentences and combining related supporting sentences; keep short claim sentences short |

> **Reader clarity comes first.** Preserve actors, comparisons, conditions, and logical relationships. Shorten by removing low-priority or repetitive sentences rather than compressing essential meaning. Burstiness is still required in every paragraph (mandatory rhythm check), but it is obtained only through edits that keep meaning explicit, and never by merging the author's short claim sentences. See the [eight diagnostic examples](references/reader-clarity.md).

### Preserved Academic Writing (do NOT flag as AI)

The skill explicitly **preserves** standard academic writing that was previously over-corrected:

- Transitional phrases: "Notably,", "Furthermore,", "In contrast,", etc.
- Logical discourse markers: "Although", "Whereas", "Thus", "Based on these results", "As expected", etc. (Pattern 27)
- Functional -ly adverbs: "slightly", "consistently", "modestly", "approximately" (Pattern 29)
- Interrogative sentence openers: "Who selects into...", "What predicts...", etc.
- "Additionally" up to once per paragraph (Pattern 7 exception)
- Attribution phrases with citations: "Prior studies have shown that...", "Evidence suggests that...", etc.

These are only flagged when used in excessive clusters or without supporting citations/data.

## Full Example

**Before (AI-sounding):**
> Heart failure represents a pivotal challenge in the evolving landscape of diabetes care, underscoring the critical importance of addressing cardiovascular comorbidities. This groundbreaking study showcases the profound impact of empagliflozin. Additionally, empagliflozin reduced the risk of hospitalization for heart failure or cardiovascular death by 34%—a remarkable finding—highlighting the cardioprotective effects of this intervention. The future looks bright for patients with type 2 diabetes.

**After (Humanized):**
> Heart failure is highly prevalent in patients with diabetes, occurring in more than one in five patients with type 2 diabetes aged over 65 years. In the EMPA-REG OUTCOME trial, empagliflozin reduced the risk of hospitalization for heart failure or cardiovascular death by 34%. The benefit was consistent in patients with and without heart failure at baseline.

## References

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) - Primary source for AI writing patterns
- [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) - Maintaining organization

### Examples Source

Medical paper examples (Patterns 1–18) are adapted from:

> Fitchett D, Inzucchi SE, Cannon CP, et al. Empagliflozin Reduced Mortality and Hospitalization for Heart Failure Across the Spectrum of Cardiovascular Risk in the EMPA-REG OUTCOME Trial. *Circulation*. 2019;139(11):1384-1395. doi:10.1161/CIRCULATIONAHA.118.037778

This article is published under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) license.

Examples for Patterns 19–31 are based on the author's (K. Matsui) observations during academic manuscript editing in sleep medicine research.

The AI-vocabulary patterns (Pattern 7) draw on the following papers that quantified words and phrases with increased or decreased frequency in post-ChatGPT medical and scientific writing:

> Matsui K. Delving Into PubMed Records: How AI-Influenced Vocabulary has Transformed Medical Writing since ChatGPT. *Perspect Med Educ*. 2025;14(1):882-890. doi:[10.5334/pme.1929](https://doi.org/10.5334/pme.1929)

> Bao T, Zhao Y, Mao J, et al. Examining linguistic shifts in academic writing before and after the launch of ChatGPT: a study on preprint papers. *Scientometrics*. 2025;130:3597-3627. doi:[10.1007/s11192-025-05341-y](https://doi.org/10.1007/s11192-025-05341-y)

> Galpin R, Anderson B, Juzek TS. Exploring the Structure of AI-Induced Language Change in Scientific English. *Int FLAIRS Conf Proc*. 2025;38. doi:[10.32473/flairs.38.1.138958](https://doi.org/10.32473/flairs.38.1.138958)

## Related Work by the Author

> Matsui K. Delving Into PubMed Records: How AI-Influenced Vocabulary has Transformed Medical Writing since ChatGPT. *Perspect Med Educ*. 2025 Dec 2;14(1):882-890. doi:[10.5334/pme.1929](https://doi.org/10.5334/pme.1929)

This is a paper I wrote. Using PubMed records, I measured how frequently LLMs such as ChatGPT tend to overuse certain words in medical writing. Take a look if you're curious!

![Figure 1 from Matsui 2025 — AI-influenced vocabulary trends in PubMed](2025_Matsui_Delving_into_PubMed_Records_Fig1.png)

*The image above is Figure 1 from the paper cited above, reproduced under the [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.*

## Version History

- **2.4.0** - Keep model-recalled figures and citations out of the rewritten text. "Be specific" now uses only data from the manuscript or author-supplied sources; the `[verify: ...]` in-text insertion is removed. A new mandatory fidelity check confirms that every number, statistic, named entity, and citation in the output appears in the input, reverting any span that does not. Recalled candidates are listed separately in the output as unverified and not inserted (thanks to @kaicot for issue #5).
- **2.3.0** - Restore burstiness as a required step (Pattern 34 and the mandatory rhythm check) while keeping the v2.2 reader-clarity priority and the v2.1.1 rule that short claim sentences stay short. Rhythm variation now comes from splitting sentences that stack conditions, combining related supporting sentences, and varying openings. "Be specific" now replaces vague claims with real data, marks facts drawn from model knowledge with `[verify: ...]`, and uses `[DATA NEEDED: ...]` placeholders instead of inventing specifics. Pattern 13 keeps the zero-em-dash rule with a calmer tone (thanks to @kaicot for PR #3 and #4). Example Befores now contain every fact in their Afters, so the examples demonstrate style edits without adding facts; the Pattern 34 word counts, the rhythm criterion, and a wrong cross-reference were also corrected.
- **2.2.0** - Prioritize reader clarity over compressed prose and forced rhythm variation. Add eight reusable examples, sentence-level deletion guidance, abstract consistency checks, and protection for approved author opinions and intentional section spacing. Include the new reference file when installing or using the skill in a chat.
- **2.1.1** - Voice Calibration and Pattern 34: keep the author's short sentences that state a claim outright ("The largest difference was cost."). They are no longer merged into neighboring sentences to satisfy the rhythm check, because merging buries and softens the claim.
- **2.1.0** - Slimmed SKILL.md description to fit the 1024-character limit enforced by `claude install-skill`. No changes to patterns or skill behavior.
- **2.0.0** - Major update based on experimental validation with local AI detectors (desklib + Binoculars). Added Pattern 34 (Sentence rhythm & burstiness: experimentally verified as the single highest-impact intervention, accounting for ~90% of achievable AI-score reduction). Added Voice Calibration section with author reference profile. Upgraded Process to two-pass draft-audit loop with mandatory rhythm check. Strengthened Pattern 11 to explicitly require term consistency (same construct = same term throughout). Documented critical interaction: Pattern 29 adverb removal must always be paired with Pattern 34 sentence restructuring (standalone deletion increases AI scores).
- **1.4.0** - Added Pattern 32 (Paraphrastic repetition: detect and remove same-claim restatements joined by "In other words" / "That is" / "Essentially") and Pattern 33 (Content-free evaluation sentences: remove standalone verdicts like "This is a noteworthy finding" that add no data or mechanism). Extended Pattern 7 vocabulary with "comprehensive" (abstract use only), "holistic", and "multifaceted".
- **1.3.1** - Extended Pattern 27 to vary connectives by logical relation (result / addition / contrast / concession / reason / sequence groups) to avoid mechanical repetition, with a guardrail against decorative connective-sprinkling (this is NOT an exception to Pattern 11).
- **1.3.0** - Added Pattern 29 (Ornamental -ly intensifier adverbs: remove decorative "markedly/critically/remarkably" while keeping functional adverbs such as "slightly/consistently/approximately"), Pattern 30 (Connective-preserving edits: never bare-delete a transition — replace or restructure to avoid choppy asyndeton), and Pattern 31 (Paragraph cohesion: a mandatory final check for old-to-new flow and surviving paragraph-opening markers). Relaxed Pattern 7 so "Additionally" is allowed once per paragraph (only excessive use is flagged).
- **1.2.x** - Reworked Pattern 26 into "Minor word-choice refinements" (remain → be-verb, given → due to); added Pattern 27 (Preserve logical discourse markers), Pattern 28 (Re-contextualize over-condensed semantic links), and context-dependent handling of "linked/associated" (Pattern 19). (The earlier "Underused Classical Academic Terms" pattern was retired during this restructuring; its vocabulary is now covered by Pattern 7 and the cited author papers.)
- **1.1.3** - Added patterns 24 ("where" as a non-locative connector) and 25 ("yield" as a result verb); added author paper reference and Fig.1 to README
- **1.1.2** - Pattern 13: Em dash rule upgraded to zero-tolerance elimination (no exceptions, mandatory final check step)
- **1.1.1** - Merged compressed noun-dash phrases and vague abstractions into single "Artificially condensed expressions" pattern (23)
- **1.1.0** - Added LLM-specific word choice patterns (19-23), preserved legitimate academic phrases, fixed hedging guidance consistency
- **1.0.0** - Initial release adapted for academic medical writing

## Contributors

- [@kaicot](https://github.com/kaicot): found that the short-sentence rule still referred to a removed rhythm check ([#3](https://github.com/matsuikentaro1/humanizer_academic/pull/3)), found the broken Pattern 15 example, and proposed the data-sourcing rule for "Be specific", the calmer Pattern 13 wording, and the note on illustrative examples ([#4](https://github.com/matsuikentaro1/humanizer_academic/pull/4)). These were adopted in v2.3.0. Also proposed the fidelity check that keeps model-recalled data out of the rewritten text ([#5](https://github.com/matsuikentaro1/humanizer_academic/issues/5)), adopted in v2.4.0.

## License

MIT

Based on [blader/humanizer](https://github.com/blader/humanizer).
