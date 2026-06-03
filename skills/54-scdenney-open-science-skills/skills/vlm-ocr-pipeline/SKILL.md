---
name: vlm-ocr-pipeline
description: VLM-based OCR pipeline: model selection, prompts, architecture, evaluation.
argument-hint: "[describe your document corpus, languages, and compute environment]"
---

# VLM-Based OCR Pipeline for Scanned Document Corpora

## Instructions

For a worked language-specific transcription prompt (pre-reform Cyrillic) and a per-page JSON output schema with `uncertain_spans`, `layout_markers`, and `flags`, see `reference/prompt-and-schema.md`.

### 1. Model Selection

- **Start from OCR benchmarks, not general VLM leaderboards.** OCRBench (Liu et al. 2024) tests across 29 document OCR dimensions; OCRBench v2 (Fu et al. 2025) extends to multilingual scripts and multi-page documents. General vision-language benchmarks (MMMU, VQAv2) do not predict OCR accuracy.
- **Verify language support explicitly.** Confirm the target language appears in the model's training set with per-language accuracy data. Qwen3-VL (Bai et al. 2025) enumerates 39 languages with OCR benchmarks; models that claim "multilingual support" without language-specific evidence may fail on non-Latin scripts.
- **Compare across models for your script family.** E-ARMOR (2025) compares five VLMs and two traditional OCR systems across 54 languages on a hand-annotated dataset. Use this or similar comparative studies rather than relying on a single model's self-reported scores.
- **Assess quantization tradeoffs before committing.** Low-bit quantization (e.g., W3A16, W4A8) enables single-GPU deployment but can degrade VLM accuracy non-uniformly across modalities. Li et al. (2025) show that **language tokens are an order of magnitude more sensitive to quantization than vision tokens**; treating them equally during calibration over-weights the insensitive modality and hurts performance. Always compare quantized output against a full-precision baseline on a pilot sample before committing to a bulk run.
- **Test the instruct variant against reasoning variants.** For OCR tasks, instruction-following models typically outperform chain-of-thought variants, which may add latency and fabricate content rather than improving transcription fidelity.

### 2. Image Handling and Preprocessing

- **Separate OCR input resolution from archival preservation.** For archival capture, FADGI (2016) prescribes 300-400 ppi across books, journals, and manuscripts (with 400+ ppi for 4-star compliance), and Metamorfoze (van Dormolen 2012) applies similar European standards. For VLM OCR input, resolution requirements are lower but not well-pinned by the KB: calibrate on a pilot, do not drop below ~150-200 ppi, and raise DPI for small type, faded ink, or pre-industrial typography.
- **Prefer native image extraction over rasterization.** Scanned PDFs store each page as an embedded image at the original scan resolution. Extract these byte-for-byte using PDF library methods rather than re-rasterizing, which downsamples and re-encodes (Pitt OCR Best Practices). Reserve rasterization for VLM input when a specific DPI is needed.
- **Test preprocessing on a sample before applying corpus-wide.** Learned image restoration combined with neural post-correction can yield large CER reductions on degraded historical documents — Guan et al. (2025) report 63.9-70.3% CER reduction for the full PreP-OCR pipeline (ResShift image restoration + ByT5 post-correction), not for classical deskew/binarization/contrast alone. Classical preprocessing alone may not help and can actively hurt: Machidon & Machidon (2025) find that grayscale conversion, binarization, and dilation did not improve OCR on degraded folkloristic scans and in some cases introduced artifacts that worsened recognition. Always run with and without preprocessing on a diverse sample and compare.
- **Store archival images separately from OCR derivatives.** Save native-resolution images for preservation and generate OCR-resolution images in memory for the VLM. Do not save OCR-resolution rasterizations as the archival copy.

### 3. Prompt Engineering

- **Build language-specific prompts that enumerate expected characters.** For diacritics-heavy languages (Polish, Czech, Vietnamese, Turkish), list every expected diacritical character explicitly in the prompt. For CJK scripts, instruct the model to handle mixed-script content (e.g., Korean hangul with classical Chinese hanja).
- **Specify structured output format.** Instruct the model to output markdown preserving headings, paragraphs, footnotes, and tables. Structured prompts with explicit output format significantly outperform generic "extract text" instructions.
- **Include negative instructions.** "Do not translate," "do not interpret," "do not add content not present in the image." VLMs will summarize, translate, or describe images unless explicitly constrained.
- **Handle page-type edge cases in the prompt.** Instruct the model on what to return for blank pages, illustration-only pages, and pages with only page numbers. Without this guidance, models may hallucinate content for non-text pages (Gbelidji 2026).
- **Guard against over-historicization on period documents.** VLMs trained with broad historical exposure may project archaic orthography anachronistically. Levchenko (2025) documents GPT-4o inserting historical characters in 59% of 18th-century Russian files regardless of prompt. Validate on the target period and stratify ground-truth sampling by decade (see §6) to detect this failure mode; no prompt will fully suppress it.

### 4. Pipeline Architecture

- **Separate GPU-intensive OCR from CPU-only post-processing.** The minimum viable pipeline has three stages: (1) VLM OCR producing per-page raw text, (2) quality diagnostics classifying problem pages, (3) assembly into combined document-level output. olmOCR (Poznanski et al. 2025) demonstrates this extract-describe-assemble pattern at scale.
- **Integrate diagnostics as automated gates.** Diagnostics should classify each page into action categories (OK, rule-fixable, LLM-fixable, manual review) using language-aware detection: diacritic-to-Latin ratios for European scripts, CJK character ratios for East Asian scripts, repetition density, symbol density, and page length anomalies.
- **Store all results as structured JSON with full metadata.** Every pipeline stage should output structured data (model name, quantization, DPI, timestamps, per-page results) rather than flat text files. This enables automated aggregation and corpus-level quality dashboards.
- **Design for resumability.** The pipeline should detect already-processed documents and skip them on re-run. Store a completion marker (e.g., `results_raw.json`) per document so partial runs can resume without re-processing.

### 5. Batch Strategy and Resource Planning

- **Calibrate GPU-hour estimates from a measured run.** Process 10-20 pages, measure per-page time, multiply by corpus page count, and add 30% buffer for variance and failed retries. Do not rely on model documentation or theoretical throughput.
- **Structure batch processing as one job per document.** This minimizes job scheduling overhead, simplifies failure recovery (re-run one document, not one page), and produces self-contained output directories.
- **Use the tranche/gate pattern.** Split the corpus into a small test tranche (3-5 documents per language) and bulk tranches. Complete accuracy evaluation on the test tranche before committing GPU-hours to bulk runs. This is the single most important resource management decision.
- **Handle large documents explicitly.** Books exceeding the job wall-clock limit should be split into page-range chunks submitted as separate jobs writing to the same output directory. The assembly stage must merge chunks.
- **Track all jobs in a manifest.** Maintain a CSV or database mapping each document to its tranche, job ID, status, GPU-hours consumed, and quality metrics. This supports both operational monitoring and post-hoc reporting.

### 6. Accuracy Evaluation

- **Combine ground-truth sampling with automated proxies.** Human-transcribed ground truth with CER/WER computation gives a rigorous accuracy number; dictionary-based hit rates give a scalable quality signal across every page. Neither alone is sufficient.
- **Stratify the ground-truth sample.** Select pages spanning languages, decades (older print is harder), print quality (faded vs. clean), and content type (body text, tables, captions). A sample of 20-30 pages per language is a practical minimum for a reliable CER estimate (Levchenko 2025).
- **Document the evaluation tool.** CER/WER scores differ across evaluation tools due to normalization differences (whitespace handling, Unicode normalization, punctuation treatment). Neudecker et al. (2021) demonstrate that tool choice changes reported accuracy. Specify which tool you used, which normalization was applied, and whether the comparison was case-sensitive.
- **Acknowledge CER/WER limitations.** Character-level edit distance does not capture layout errors, semantic correctness, or structural fidelity. A model can scramble column order while achieving low CER (Beyene & Dancy 2026). Supplement with dictionary hit rates, manual inspection of representative pages, and downstream task performance.
- **Set go/no-go thresholds relative to downstream needs.** A mean CER below 5% is excellent; below 10% is acceptable for most computational text analysis. Calibrate against what your analysis pipeline can tolerate rather than pursuing absolute accuracy — van Strien et al. (2020) show that the impact of OCR quality on downstream NLP tasks is task-specific (topic modeling, NER, dependency parsing, and retrieval degrade at different thresholds), so the right threshold depends on which downstream task consumes the text.

### 7. Reproducibility and Documentation

- **Record every pipeline parameter in machine-readable format.** Model name and exact version, quantization method, DPI, prompt text, generation parameters (temperature, max tokens, sampling strategy), software versions, and hardware specifications. Store as JSON alongside the output.
- **Produce per-document processing reports.** Each document should have a JSON report recording pipeline stages completed, timestamps, page counts (processed, failed), quality summary, and output file manifest.
- **Aggregate into a corpus-level batch summary.** A single CSV mapping all documents to their quality metrics, processing metadata, and tranche membership supports both quality monitoring and methods reporting.
- **Archive the complete pipeline code and prompts.** The OCR can only be reproduced if the exact code, prompts, and model weights are available. Pin model versions and software dependencies. If using a model from a hub (HuggingFace, etc.), record the commit hash.
- **Treat hosted-API non-determinism as a reproducibility hazard.** Levchenko (2025) measured coefficient-of-variation (CV) of daily word-accuracy over seven days and found roughly a 10x spread across models (e.g., CV=0.307 vs. 0.037). Commercial hosted APIs can silently change underneath you. Barrie, Palmer & Spirling (2025) generalize the point for political-science LM work: temperature=0 does not fix it, many LM-based pipelines fail the re-runnable and repeatable sub-standards of replication, and the disciplinary recommendation is locally-hosted, versioned open-weight models. Prefer local open-weight models pinned to a specific revision when publication-grade reproducibility is required; otherwise, report the evaluation window and replicate the pilot run before and after any bulk campaign.
- **Compose with downstream skills.** After OCR, pass raw per-page output through the `post-ocr-cleanup` skill (LLM-based correction, constrained decoding, Unicode normalization, provenance). Before publication, audit the pipeline documentation with the `methods-reporting` skill (APSA/JARS/DA-RT standards for methods sections).

## Quality Checks

- [ ] **Model benchmarked for task:** VLM selected based on document-OCR benchmarks (OCRBench or equivalent), not general VLM leaderboards (Liu et al. 2024; Fu et al. 2025)
- [ ] **Language support verified:** Target language confirmed in the model's explicit training set with per-language accuracy data (Bai et al. 2025)
- [ ] **Quantization tradeoff assessed:** If using 4-bit or 8-bit quantization, accuracy impact measured on a pilot sample against full-precision baseline (Li et al. 2025)
- [ ] **DPI justified:** OCR input DPI calibrated on a pilot (not dropped below ~150-200 ppi without evidence), with archival images stored separately at FADGI/Metamorfoze targets (FADGI 2016; van Dormolen 2012)
- [ ] **Native extraction preferred:** Embedded images extracted byte-for-byte from scanned PDFs rather than re-rasterized, when available
- [ ] **Preprocessing tested on sample:** Any image preprocessing (classical or learned restoration) validated on a diverse sample before corpus-wide application; headline CER reductions from PreP-OCR-style pipelines reflect combined restoration + post-correction, not classical preprocessing alone (Guan et al. 2025; Machidon & Machidon 2025)
- [ ] **Prompts are language-specific:** OCR prompts explicitly name the script system, enumerate expected diacritics or character sets, and include negative instructions
- [ ] **Pipeline stages separated:** GPU-intensive OCR decoupled from CPU-only diagnostics and assembly, with structured JSON output at each stage
- [ ] **Diagnostics integrated:** Automated quality diagnostics classify every page by action category with language-aware character detection
- [ ] **Resource estimate calibrated:** GPU-hours estimated from a measured calibration run, not assumed from model documentation
- [ ] **Test tranche gated:** Accuracy evaluation completed on a test tranche before committing to bulk GPU-hours
- [ ] **Ground truth sampled:** Human-transcribed ground truth created for a stratified sample of pages, with CER/WER computed and reported (Levchenko 2025)
- [ ] **Evaluation tool documented:** CER/WER tool identified and normalization choices recorded, given known tool discrepancies (Neudecker et al. 2021)
- [ ] **Pipeline fully documented:** Model version, quantization, DPI, prompts, generation parameters, and software versions recorded in machine-readable format
- [ ] **Model stability acknowledged:** If using a hosted API, evaluation window recorded and pilot re-run before and after the bulk campaign; publication-grade corpora use pinned open-weight models (Levchenko 2025; Barrie, Palmer & Spirling 2025)
- [ ] **Processing reports generated:** Per-document JSON reports and corpus-level batch summary CSV produced and archived
