# VLM-OCR Prompt and Output Schema Reference

Worked examples of a language-specific transcription prompt and a per-page JSON output schema. Use as a starting point; adapt to your corpus, model, and language.

---

## (a) Language-Specific Transcription Prompt — Cyrillic (Pre-Reform Russian, 18th–19th c.)

The following prompt is designed for pre-reform Russian (before the 1918 orthographic reform), where the letters ѣ (yat), і (decimal i), ѳ (fita), and ѵ (izhitsa) appear alongside the modern Cyrillic alphabet. It enforces orthographic fidelity to the source, blocks modernization, and forces the model to mark uncertainty rather than guess. Levchenko (2025) documents that GPT-4o-class models insert archaic characters in ~59% of 18th-century Russian files *even when not prompted to do so*; this prompt does not eliminate that failure mode, but combined with stratified ground-truth validation (see SKILL.md §6) it at least prevents the opposite failure (silent modernization).

```
You are transcribing a scanned page from a pre-reform Russian printed
document. Your sole task is faithful transcription. Do not interpret,
translate, summarize, or normalize.

ALPHABET AND ORTHOGRAPHY
- Transcribe the exact characters visible on the page.
- The document uses pre-1918 Russian orthography. The following
  characters may appear and must be preserved when present:
    ѣ (yat), і (decimal i), ѳ (fita), ѵ (izhitsa),
    ъ at word ends, and archaic ligatures.
- Do NOT substitute modern equivalents (e.g., do not replace ѣ with е,
  і with и, ѳ with ф, or drop terminal ъ).
- Do NOT add any pre-reform character that is not visibly present on
  the page. If the page uses modern orthography, transcribe it as
  modern. Never "historicize" based on context or expectation.

LAYOUT
- Preserve reading order (top-to-bottom, left-to-right, columns in
  order).
- Mark layout features inline:
    [HEADING] ... [/HEADING] for titles and section heads
    [FOOTNOTE n] ... [/FOOTNOTE] for footnotes, numbered as printed
    [TABLE] ... [/TABLE] for tabular material (preserve row breaks
      with newlines and column breaks with tab characters)
    [FIGURE: brief literal description] for illustrations; do not
      invent captions
    [PAGE_NUMBER: n] for printed folio or page numbers
- Preserve hyphenation at line ends as printed. Do not silently merge
  across line breaks.

UNCERTAINTY
- If a character, word, or span is illegible, damaged, or genuinely
  ambiguous, wrap it in [UNCERTAIN: best_guess] tags. Do not guess
  silently. Do not produce a character you cannot see.
- If an entire region is unreadable (tear, stain, binding shadow),
  mark it [ILLEGIBLE: approximate_length_in_characters].

NEGATIVE CONSTRAINTS
- Do not translate to modern Russian or any other language.
- Do not modernize spelling, punctuation, or typography.
- Do not add commentary, explanation, headers, or markdown outside
  the tags defined above.
- Do not hallucinate text for blank pages, illustration-only pages,
  or pages containing only a page number. For those, return only
  the appropriate layout marker.

OUTPUT
Return the transcription as a single UTF-8 string using the layout
markers above. Do not wrap it in code fences. Do not add a preamble
or postscript.
```

Adaptations for other scripts follow the same structure: enumerate the expected character set, forbid substitution in either direction, define a fixed set of layout markers, and require explicit uncertainty tags. For English historical documents, enumerate the long s (ſ), ligatures (æ, œ, ct, st), and manicules. For Chinese, distinguish simplified from traditional, list expected variant characters, and instruct the model on handling mixed hanzi / hanja / kana and punctuation (。、「」).

---

## (b) Per-Page JSON Output Schema

The VLM returns the transcription as a string. A thin post-processing wrapper parses the inline layout and uncertainty markers into the structured record below. Store one record per page; aggregate into per-document and per-corpus reports as described in SKILL.md §7.

```json
{
  "page_id": "doc-00042_p017",
  "document_id": "doc-00042",
  "page_index": 17,
  "text": "[HEADING]О воспитаніи дѣтей[/HEADING]\n\nВоспитаніе [UNCERTAIN: юношества] есть ...",
  "confidence": 0.86,
  "uncertain_spans": [
    {
      "start_char": 48,
      "end_char": 58,
      "surface": "юношества",
      "best_guess": "юношества",
      "reason": "faded_ink"
    }
  ],
  "layout_markers": [
    {"type": "HEADING", "start_char": 0, "end_char": 28},
    {"type": "FOOTNOTE", "number": 1, "start_char": 412, "end_char": 530}
  ],
  "flags": {
    "handwritten": false,
    "low_resolution": false,
    "table": false,
    "figure": true,
    "blank": false,
    "page_number_only": false
  },
  "pipeline": {
    "model": "Qwen3-VL-32B-Instruct",
    "model_revision": "sha256:a1b2c3...",
    "quantization": "bf16",
    "dpi": 300,
    "prompt_id": "cyrillic-pre-reform-v1.2",
    "generation": {"temperature": 0.0, "max_tokens": 4096, "seed": 42},
    "software": {"transformers": "4.48.0", "vllm": "0.7.2"},
    "hardware": "1x A100-80GB",
    "timestamp_utc": "2026-04-18T14:32:11Z"
  }
}
```

Field notes:

- `confidence` is a model-reported or heuristic per-page score on [0, 1]; document the source in the pipeline record (self-reported log-probabilities, dictionary hit rate, or a learned classifier).
- `uncertain_spans` is the parsed form of `[UNCERTAIN: ...]` tags; always populated (empty array if none). `reason` is optional but encouraged (`faded_ink`, `torn`, `bleed_through`, `ambiguous_character`, `damaged_scan`).
- `layout_markers` is the parsed form of layout tags; downstream diagnostics consume this to distinguish body text from tables, footnotes, and figures.
- `flags` is a closed set of page-type indicators used by the diagnostic stage (SKILL.md §4) to route pages (OK / rule-fixable / LLM-fixable / manual review).
- `pipeline` carries every parameter needed to re-run the exact page through the same model; it is the minimal unit of machine-readable reproducibility metadata (SKILL.md §7).

---

## (c) Why This Schema Matters for Reproducibility (DA-RT)

The Data Access and Research Transparency (DA-RT) framework treats reproducibility as a first-class methodological obligation: other researchers must be able to verify, re-run, and build on the corpus. A structured per-page record — rather than a flat `.txt` file — makes this obligation operational in three specific ways.

1. **Machine-readable provenance.** Every page carries the exact model revision, quantization, DPI, prompt identifier, and generation parameters used to produce it. Barrie, Palmer and Spirling (2025) show that LM-based pipelines in political science often fail the most basic replication tests because this metadata is not captured; pinning revisions and recording generation parameters is their explicit recommendation. The schema embeds it per page.

2. **Separable quality signal.** `uncertain_spans`, `flags`, and `confidence` are first-class fields, not prose annotations. A downstream auditor can compute corpus-level statistics (fraction of pages flagged `low_resolution`, mean span-level uncertainty density, share of pages with tables) without re-parsing the transcription. This is what allows the corpus-level batch summary in SKILL.md §7 to be produced mechanically, and what lets van Strien et al. (2020) style downstream-task impact assessments proceed without rerunning OCR.

3. **Cleanly composable with downstream skills.** The `post-ocr-cleanup` skill consumes `text`, `uncertain_spans`, and `flags` to route pages to the appropriate correction strategy (rule-based, constrained LLM decoding, or manual review) and records its own provenance in a parallel structure. The `methods-reporting` skill consumes the `pipeline` record directly into the methods section and replication archive. Without a structured schema, each downstream skill would need to re-parse free-text output and reconstruct provenance by hand, which is both error-prone and a barrier to pre-publication audit.

The schema itself is not a standard — adapt field names and add domain-specific fields as needed — but the principle is: every piece of information a re-runner or auditor would need should be a named field, not a convention buried in a text file.
