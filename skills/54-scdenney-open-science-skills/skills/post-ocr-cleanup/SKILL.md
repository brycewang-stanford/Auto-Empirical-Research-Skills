---
name: post-ocr-cleanup
description: Clean post-OCR text: correction, QA, multilingual handling, provenance.
argument-hint: "[describe your OCR output, languages, and error patterns]"
---

# Post-OCR Text Cleanup for Research Corpora

## Instructions

### 1. Cleanup Strategy Selection

- **Characterize the error-generating DGP before selecting a method.** Document source language(s), era, typeface family (Fraktur, Antiqua, typewritten, handwritten), scan DPI, OCR engine, and domain jargon. Each parameter constrains which corrections are plausible and which risk introducing semantic drift.
- **Choose between LLM correction, rule-based fixes, or a hybrid pipeline based on error type.** LLM correction excels at context-dependent errors (wrong but plausible characters, broken words, missing diacritics). Rule-based fixes handle deterministic patterns (control characters, Unicode normalization, repetition artifacts, whitespace) with zero risk of content alteration. Use rule-based fixes unconditionally for these categories.
- **Default to the hybrid approach for research corpora.** Run LLM correction first on all pages, then apply deterministic rule fixes on top. This order matters: LLM correction may introduce formatting artifacts that rule fixes clean up, while the reverse order wastes rule-fix effort on text the LLM will rewrite (Machidon & Machidon 2025).
- **Pilot-test LLM correction per language before corpus-wide deployment.** LLM post-correction effectiveness is highly language-dependent: English achieves 7-58% CER reduction across open models, while Finnish shows negative or near-zero improvement across the same model set (Kanerva et al. 2025). Never assume cross-language transferability.
- **Consider whether correction is needed at all.** Define the quality threshold before choosing a strategy. The Hill & Hengchen 70-80% quality band (reported in van Strien et al. 2020) marks the critical threshold below which most downstream NLP tasks perform poorly; above 80% quality many tasks (e.g., topic modeling) tolerate residual noise. If the downstream analysis sits comfortably above this band, the risk of correction-introduced errors may outweigh the benefit.

### 2. LLM-Based Correction

- **For most pages, use a small text-only model.** The correction input is already text; image understanding is not needed for well-OCR'd pages. A 7-13B parameter model with 4-bit quantization fits in ~4-20GB VRAM and runs on a single GPU. Larger fp16 models (e.g., Llama-3.1-70B at fp16 yielding ~42% CER reduction vs ~39% at 4-bit) gain 2.5-4.7pp but require roughly 3x the memory (132GB vs 43GB) and often a second GPU (Kanerva et al. 2025).
- **For severely degraded pages, use multimodal correction.** Feeding both the original page image and the OCR text to a correction model can achieve below 1% CER on degraded documents, but doubles GPU cost (Greif et al. 2025). Reserve this for flagged pages, not routine processing.
- **Write tight correction prompts.** Instruct the model to "fix clear OCR mistakes only: wrong characters, broken words, garbled punctuation, repetition artifacts. Do not translate, modernize, or add anything. Output the corrected text only." Loose prompts invite hallucination.
- **Supply socio-cultural context in the prompt.** Including document era, publication type, language register, and genre (e.g., "The text is from an English newspaper in the 1800s") meaningfully reduces CER beyond generic correction prompts — the top-performing CLOCR-C configuration achieved over 60% CER reduction on the NCSE dataset using a modular prompt that combines expert framing, recovery instructions, publication context, text-type context, and anti-overgeneration instructions (Bourne 2024). Misleading or mismatched context degrades performance, so use the real document metadata.
- **Add language-specific instructions.** For Polish, explicitly mention diacritics restoration (ą, ć, ę, ł, ń, ó, ś, ź, ż). For Korean, mention hangul integrity and hanja preservation. The correction model needs to know which character set to favor.
- **Mitigate hallucination with constrained decoding.** Constrained decoding techniques — beam search with CER-based re-ranking, sequence-level similarity re-ranking, and token-level Constrained Beam Search that interpolates the model's distribution with a character-similarity distribution — enforce fidelity between input and output and prevent plausible-but-fabricated substitutions (Sastre et al. 2025). Prefer token-level CBS with dynamic α if model logits are accessible; otherwise fall back to beam search with CER re-selection. This matters because WER can worsen even when CER improves: fine-tuning alone in Sastre et al. left CER roughly flat (0.314→0.321) while WER jumped from 0.633 to 0.821, a failure mode constrained decoding directly addresses.
- **Use worked prompt templates and a provenance schema.** See `reference/prompt-templates-and-schema.md` for a minimal constrained-decoding-friendly baseline prompt, a Bourne-style socio-cultural-context prompt, and a span-level JSONL provenance schema (per Guo & Wei 2026 §3.2/§3.3).
- **Strip LLM overgeneration with alignment-based post-processing.** Llama-family models routinely prepend "Here is the corrected text:" or append error-by-error explanations. Without post-hoc trimming (character-level local alignment of output against input, keeping only the aligned region), Llama-3-8B scored -74.1% CER; with trimming, +7.3% (Kanerva et al. 2025). Gemma and GPT-4o are largely unaffected but the step is cheap and should be applied universally.
- **Disable chain-of-thought for correction tasks.** Reasoning modes add latency without improving transcription fidelity. Use low-temperature sampling or greedy decoding for deterministic output.
- **Tune segment length for corpus-scale processing.** Short segments (50-100 words) score notably worse CER% across models; 200-300 words appears optimal for page-level correction (Kanerva et al. 2025). When splitting long documents, use a stride that preserves left context (left-uncorrected-concatenate parallelizes cleanly; left-corrected-concatenate is sequential but slightly better at segment boundaries).
- **Track all changes with edit-distance metrics.** Compute Levenshtein distance and change ratio (edit distance / original length) per page. Flag pages where the correction model altered more than 10% of characters for manual review — high change ratios may indicate hallucination rather than correction. This 10% threshold is an operational heuristic; calibrate against your pilot evaluation.

### 3. Rule-Based Fixes

- **Apply deterministic fixes in a fixed order.** (1) Control character removal, (2) zero-width and invisible Unicode character removal, (3) NFKC Unicode normalization, (4) consecutive character repetition collapse, (5) standalone symbol line removal, (6) whitespace normalization. This ordering prevents interactions between fixes.
- **Tune repetition collapse thresholds to the corpus.** The default of collapsing runs of 4+ identical characters to 3 works for most scripts but may need adjustment for languages with legitimate long character sequences or for documents with intentional formatting patterns.
- **Rule-based diacritics restoration is viable for some languages.** For Polish, rule-based approaches (removing word breaks, rejecting case-changing corrections, restoring diacritical characters replaced with visually similar ASCII) are competitive with LLM-based correction and more predictable (Ogrodniczuk 2022).
- **Generate synthetic OCR errors for training when ground truth is scarce.** Glyph-similarity-based synthetic corruption (feature-matched character confusions) produces more realistic training data than random-injection baselines, and outperforms in low-resource languages (Guan & Greene 2024).
- **Preserve the raw text alongside every cleaned version.** Rule-based fixes are deterministic and reversible, but downstream researchers may prefer different normalization choices. Store both raw and cleaned text at every stage.

### 4. Quality Diagnostics and Metrics

- **Move beyond CER/WER as the sole quality measure.** Character-level edit distance is sensitive to normalization choices (ligature handling, Unicode compatibility, PUA character treatment), does not capture semantic correctness, and can return substantially different numbers across evaluation tools on the same data (Beyene & Dancy 2026; Neudecker et al. 2021). A model can scramble column order while achieving perfect CER.
- **Use precision as a primary metric for historical and archival corpora.** CER and WER emerged from speech recognition, where insertions and deletions are symmetric. Historical and archival research is asymmetric: false positives (hallucinated tokens, invented entities) are more costly than false negatives (missed content), because historians already expect absence. Precision on downstream tasks (e.g., NER precision, entity similarity) often aligns better with analytic needs than CER/WER and can show improvement even when CER/WER indicate regression (Backer & Hyman 2025).
- **Build a multi-signal diagnostic profile per page.** Character composition ratios (diacritics-to-Latin for European scripts, CJK character ratios for East Asian), repetition artifact density, symbol density, and page length anomalies (empty, suspiciously short, suspiciously long) each capture different failure modes.
- **Use dictionary hit rates as an automated quality proxy.** Tokenize OCR output and check against morphological dictionaries or analyzers. Compute per-page and per-document valid-token rates. This scales to every page in the corpus without human effort.
- **Calibrate thresholds against downstream task requirements.** OCR quality directly impacts NER, classification, topic modeling, and other downstream NLP tasks. Below the Hill & Hengchen 70-80% quality band (reported in van Strien et al. 2020), most NLP tasks perform poorly; above 80% many tasks converge. Define acceptable error rates based on what your analysis pipeline can tolerate, not abstract accuracy targets.
- **Classify pages by recommended action.** Map diagnostic signals to action categories: OK (no intervention), rule-fixable (deterministic cleanup sufficient), LLM-fixable (context-dependent errors), manual review (critical failures). This prioritizes human attention on the pages that need it most.

### 5. Multilingual Considerations

- **Check diacritic ratios for Latin-script languages.** For Polish, a page of body text with zero diacritical characters almost certainly has OCR errors. Flag pages where the diacritic-to-alphabetic ratio drops below a language-calibrated threshold (Ogrodniczuk 2022).
- **Treat Korean spacing as a distinct post-OCR task.** Korean uses space-delimited eojeol units, and OCR frequently merges or splits them incorrectly. Dedicated syllable-and-morpheme spacing models (Choi & Kim 2021) address this error type specifically and may outperform general-purpose LLM correction, though direct LLM benchmarks on this task are not well-established.
- **Use morphological analyzers as correction validators.** Morfeusz for Polish, Mecab-ko for Korean — tokens that parse successfully are likely correct; tokens that fail to parse are OCR error candidates. This provides both a diagnostic signal and a correction filter.
- **Protect dialectal and archaic text from normalization.** Correction models trained on standard modern language may silently replace historical or dialectal tokens with modern near-neighbors, introducing semantic drift (e.g., Machidon & Machidon 2025 document *žlahnega* → *glavnega* in Slovene folkloristic text; Kanerva et al. 2025 document historical long-s and v/w substitutions). Test on a sample of the oldest and most linguistically distinctive documents before corpus-wide deployment, and disable normalization flags that modernize orthography.

### 6. Corpus-Level Quality Assurance

- **Implement a three-tier review workflow.** (1) Automated pass/fail based on diagnostic thresholds applied to all documents, (2) spot-check review of flagged documents (10-15% of corpus), (3) deep review of a random sample of passing documents (2-5% of corpus) to catch false negatives.
- **Define specific flagging thresholds.** Mean quality score below 0.80, LLM correction change ratio above 10%, dictionary hit rate below 80%, or more than 5% empty pages. These are operational defaults, not empirically derived cutoffs — calibrate against your pilot evaluation and pre-register the final values.
- **Route flagged documents to specific remediation actions.** Re-run LLM cleanup with a different prompt, re-OCR at higher DPI or without quantization, or escalate to manual transcription. Each action has different cost and quality implications.
- **Produce a corpus-level quality dashboard.** Aggregate per-document metrics into a summary CSV or report: document ID, language, page count, mean quality score, dictionary hit rate, correction change ratio, flag status, review outcome. This supports both operational monitoring and methods reporting.

### 7. Provenance and Documentation

- **Maintain a complete audit trail of all corrections.** Each correction should be attributed to its source (LLM model version, rule name) with before/after text preserved at the page level (Guo & Wei 2026). Correction pathways can substantially alter extracted entities and downstream interpretations.
- **Log model details for the LLM correction stage.** Model name, quantization method, prompt text, generation parameters (temperature, max tokens, sampling), and per-page edit-distance metrics. This is the minimum required to reproduce or audit the correction.
- **Log rule-fix details.** Which rules fired and how many characters each rule changed per page. This enables downstream researchers to assess whether rule fixes were aggressive or conservative for a given document.
- **Produce a cleanup comparison artifact.** A CSV or JSON with page-level before/after text pairs and metrics (edit distance, change ratio, flagged status) enables downstream researchers to assess correction quality and choose their preferred text version.
- **Record all thresholds and human review outcomes.** Sampling decisions, flagging thresholds, remediation actions, and human review results should be documented in a methods section alongside the corpus, not just in internal notes.
- **Pre-register the correction strategy when downstream inference depends on cleaned text.** Correction pathways can substantially alter extracted entities — Guo & Wei 2026 show that raw, fully-corrected, and provenance-filtered variants of the same corpus yield materially different NER inventories (176 volatile entities in their pilot). Correction-stack flexibility (prompt wording, trust-policy threshold, model version) is a researcher-degrees-of-freedom problem in the Simmons et al. 2011 sense: each un-documented choice is a forking path that can shift downstream inferences. Pre-registration is the standard remedy (Nosek et al. 2018). When cleaned text feeds named-entity-based, topic-based, or embedding-based inferential analyses, pre-register the correction model, prompt, decoding configuration, and provenance-filter trust policy alongside the analysis plan (cross-reference the `pre-registration-writing` skill).

## Quality Checks

- [ ] **DGP characterized:** Source language(s), era, typeface, scan DPI, OCR engine, and domain documented before method selection
- [ ] **Strategy justified:** Cleanup approach (LLM, rule-based, or hybrid) chosen based on error types, corpus size, and resource constraints
- [ ] **LLM correction pilot-tested per language:** Cleanup validated on a sample from each language before corpus-wide application (Kanerva et al. 2025)
- [ ] **Socio-cultural context supplied in prompts:** Document era, publication type, and genre included; misleading context avoided (Bourne 2024)
- [ ] **Segment length tuned:** Input segments of 200-300 words used; boundary concatenation strategy chosen (Kanerva et al. 2025)
- [ ] **Overgeneration stripped:** Alignment-based trimming applied to LLM outputs to remove "Here is the corrected text:" preambles and trailing commentary (Kanerva et al. 2025)
- [ ] **Hallucination risk mitigated:** Constrained decoding (token-level CBS preferred; beam + CER re-rank as fallback) applied to prevent fabricated content (Sastre et al. 2025)
- [ ] **Change ratio tracked:** Per-page edit distance and change ratio computed and stored; pages exceeding the flagging threshold (default 10%) reviewed
- [ ] **Rule-based fixes ordered correctly:** Deterministic fixes applied in the prescribed sequence (control chars, zero-width, NFKC, repetitions, symbols, whitespace)
- [ ] **Metrics go beyond CER/WER:** Quality assessed using multiple signals (precision for historical corpora, character composition, dictionary hit rates, diagnostic flags), not CER/WER alone (Backer & Hyman 2025; Beyene & Dancy 2026; Neudecker et al. 2021)
- [ ] **Downstream impact considered:** Quality thresholds set relative to the intended analysis and the 70-80% critical quality band (van Strien et al. 2020), not abstract accuracy targets
- [ ] **Language-specific patterns addressed:** Diacritics ratios, morphological parsing, and spacing rules checked for each language in the corpus
- [ ] **Dialectal and archaic text protected:** Correction models tested for damage to non-standard language varieties; modernization flags disabled where relevant (Machidon & Machidon 2025)
- [ ] **Flagging thresholds defined and calibrated:** Numeric thresholds (quality score, change ratio, dictionary hit rate, empty page rate) set and calibrated against pilot evaluation
- [ ] **Stratified human review conducted:** Review sample stratified by language, document age, print quality, and flag category; sampling fraction justified
- [ ] **Both raw and cleaned text preserved:** Original OCR output retained alongside every cleanup stage for auditability
- [ ] **Correction provenance logged:** Each correction attributed to its source (LLM model, rule name) with before/after text, edit type, confidence, and review status (Guo & Wei 2026)
- [ ] **Correction strategy pre-registered:** When cleaned text feeds inferential analyses, the correction model, prompt, decoding configuration, and trust policy are pre-registered alongside the analysis plan
- [ ] **Cleanup comparison artifact produced:** Page-level CSV or JSON with raw text, cleaned text, and per-page metrics archived
- [ ] **Methods documented:** All thresholds, sampling decisions, model versions, prompts, and human review outcomes recorded
