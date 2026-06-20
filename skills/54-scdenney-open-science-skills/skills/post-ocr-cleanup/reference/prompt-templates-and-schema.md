# Post-OCR Correction: Prompt Templates and Provenance JSONL Schema

Worked prompt templates and a span-level provenance schema to accompany SKILL.md §2 (LLM-Based Correction) and §7 (Provenance and Documentation). All three prompt templates are written to be compatible with constrained decoding (Sastre et al. 2025) — they do not ask the model to produce commentary, and they instruct the model to emit *only* corrected text so token-level Constrained Beam Search or beam + CER re-ranking can score output fidelity against the input string directly.

---

## A. Baseline correction prompt (minimal, constrained-decoding friendly)

Use this as the default template for routine page-level correction. The instruction set is intentionally tight: no explanations, no modernization, no translation. This is the version that pairs cleanly with token-level CBS because every output character has a direct correspondence to an input character and the model is not asked to produce any "scaffolding" tokens.

```
System:
You are an OCR correction assistant. Fix clear OCR mistakes only: wrong
characters, broken words, garbled punctuation, repetition artifacts, and
spurious whitespace. Do not translate, modernize spelling, expand
abbreviations, add commentary, or invent content. Preserve original line
breaks. Output only the corrected text, with no preamble and no trailing
notes.

User:
<OCR_TEXT>
{ocr_text}
</OCR_TEXT>

Return the corrected text between <CORRECTED> and </CORRECTED> tags.
```

Generation parameters (recommended defaults):

- Temperature: 0.0 (greedy) or 0.2 with top-p 0.9 if sampling is required.
- Max new tokens: 1.3 x input token count (leaves headroom for legitimate expansions such as split tokens without inviting hallucinated appendices).
- Stop sequences: `</CORRECTED>`.
- Reasoning / chain-of-thought: disabled.
- If model logits are accessible, apply token-level CBS with a character-similarity-biased distribution (α tuned on pilot data) per Sastre et al. 2025.
- Apply alignment-based overgeneration stripping unconditionally after decoding (Kanerva et al. 2025): character-level local alignment of output against input, keep only the aligned region, discard any preamble like "Here is the corrected text:" or trailing explanations.

---

## B. Bourne-style socio-cultural context prompt

This template implements the modular CLOCR-C prompt structure from Bourne (2024), which achieved over 60% CER reduction on the NCSE dataset relative to a generic correction baseline. The prompt combines (a) expert framing, (b) a recovery objective, (c) publication-context sub-prompt, (d) text-type context sub-prompt, and (e) an anti-overgeneration instruction. Supply real document metadata; misleading context degrades performance.

```
System:
You are an expert transcriber and historical-text philologist. Your job is
to recover the original text of a scanned document whose OCR output is
noisy. Produce the most faithful reconstruction of the original text that
the evidence in the OCR output will support.

The text is a {document_type} (e.g., newspaper article, parliamentary
debate, parish record, literary novel) published in {publication_context}
(e.g., "an English provincial newspaper in the 1830s", "a German
scientific journal in the late 19th century"). The language is
{language} and the expected register is {register} (e.g., formal
journalistic prose, vernacular dialogue, technical scientific writing).

Typography: the source is printed in {typeface} (e.g., "19th-century
Antiqua with long-s ligatures", "Fraktur with standard blackletter
ligatures", "mid-20th-century typewritten text"). Preserve period-correct
orthography, including archaic or dialectal forms; do not modernize
spelling, punctuation, or capitalization.

Correction scope: fix clear OCR mistakes (wrong characters, broken words,
garbled punctuation, repetition artifacts, spurious whitespace). Do not
translate, summarize, expand abbreviations, or add explanatory content.
Do not generate content that is not evidenced in the OCR output. If a
passage is irrecoverably garbled, mark it with [illegible] rather than
guessing.

User:
<OCR_TEXT>
{ocr_text}
</OCR_TEXT>

Return the corrected text between <CORRECTED> and </CORRECTED> tags and
nothing else.
```

Notes:

- Populate every `{placeholder}` from document metadata. Omitted or wrong values degrade performance (Bourne 2024).
- For dialectal or archaic corpora, add an explicit "Preserve dialectal/archaic tokens without normalization" line and test against a held-out sample before corpus-wide deployment (Machidon & Machidon 2025 document *žlahnega* -> *glavnega* modernization drift; Kanerva et al. 2025 document long-s and v/w substitutions).
- The `[illegible]` convention is an operational choice; if your downstream pipeline cannot handle the marker, substitute your preferred tag and record the choice in the provenance log.
- Same constrained-decoding and overgeneration-stripping recommendations as Template A apply.

---

## C. Provenance JSONL schema (per Guo & Wei 2026 §3.2 / §3.3)

Write one JSON object per line, one line per correction event. Every event is anchored to the base (raw OCR) revision — offsets never drift across downstream transformations, and downstream NLP outputs can be traced back to the specific edits they depend on. This is a minimal subset of the canonical schema in Guo & Wei 2026 Appendix A (Table 6); extend with optional fields as needed.

Required fields per event:

| Field | Type | Notes |
|---|---|---|
| `event_id` | string | UUID-style unique id within the corpus. |
| `doc_id` | string | Stable document identifier. |
| `page_id` | string or int | Page or region identifier. |
| `base_revision` | int | Revision index of anchor text (0 = raw OCR). |
| `span_start` | int | Inclusive Unicode-codepoint offset in base revision. |
| `span_end` | int | Exclusive offset; must satisfy `span_start < span_end`. |
| `orig_text` | string | Exact base substring at `[span_start, span_end)` (integrity check). |
| `new_text` | string | Replacement string; empty string indicates deletion. |
| `edit_type` | enum | One of `substitute`, `insert`, `delete`, `split`, `merge`, `normalize`. |
| `source` | enum | One of `rule`, `model`, `human`. |
| `confidence` | float or null | In `[0, 1]`; tool-specific ranking score, not a calibrated probability. |
| `review_status` | enum | One of `unreviewed`, `approved`, `rejected`. |

Optional but recommended:

| Field | Type | Notes |
|---|---|---|
| `schema_version` | string | Semantic version, e.g., `"1.0.0"`. |
| `reviewer_id` | string | Pseudonymous reviewer identifier, if applicable. |
| `layout_zone` | enum | e.g., `body`, `header`, `footnote`, `caption` — a strong instability predictor per Guo & Wei 2026 Table 4. |
| `model_name` | string | For `source=model`: model identifier and version (e.g., `"gemma-2-9b-it@4bit"`). |
| `rule_name` | string | For `source=rule`: rule identifier (e.g., `"nfkc_normalize"`). |
| `note` | string | Free-form rationale (e.g., `"hyphenation repair"`). |

Canonical example (JSONL, one record per line):

```jsonl
{"schema_version":"1.0.0","event_id":"c2f1a4e0-...","doc_id":"doc_017","page_id":3,"base_revision":0,"span_start":1284,"span_end":1291,"orig_text":"Madifon","new_text":"Madison","edit_type":"substitute","source":"model","model_name":"gemma-2-9b-it@4bit","confidence":0.74,"review_status":"unreviewed","layout_zone":"body"}
{"schema_version":"1.0.0","event_id":"91a8d2b3-...","doc_id":"doc_017","page_id":3,"base_revision":0,"span_start":1312,"span_end":1328,"orig_text":"inter-\nnational","new_text":"international","edit_type":"normalize","source":"rule","rule_name":"hyphenation_repair","confidence":0.98,"review_status":"approved","layout_zone":"body","note":"line-break hyphenation repair"}
{"schema_version":"1.0.0","event_id":"4e7c9f11-...","doc_id":"doc_017","page_id":4,"base_revision":0,"span_start":812,"span_end":819,"orig_text":"NewYork","new_text":"New York","edit_type":"split","source":"model","model_name":"gemma-2-9b-it@4bit","confidence":0.81,"review_status":"unreviewed","layout_zone":"body"}
```

Replay and trust-policy filtering:

- To reconstruct a variant under a trust policy, select events matching the policy predicate (e.g., `confidence >= 0.70`, or `review_status == approved`), sort by `span_start` (tie-break by `event_id`), and apply as base-anchored replacements.
- Overlapping events must be resolved explicitly under a fixed, reportable rule (Guo & Wei 2026 §3.5): prefer `human` over `model` over `rule`; prefer `approved` over `unreviewed`; otherwise defer to adjudication. Silent overwriting defeats the purpose of provenance.
- Encode hyphenation repair, line-break normalization, whitespace reflow, and split/merge boundary edits as span-replacement events with explicit boundaries, not as micro-edits. Record large reflow regions as a single replacement.
- When registering a correction pipeline in a pre-analysis plan, the trust policy (threshold or approval filter), the overlap-resolution rule, and the base-anchoring convention are all pre-registerable design choices.
