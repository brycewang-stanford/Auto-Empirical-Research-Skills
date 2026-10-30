# Demo: Academic De-AIGC Pass (English + Chinese)

This demo routes an empirical-paper section — English or Chinese — through AERS's
bilingual de-AIGC skill while preserving every technical claim.

## Route

- Bilingual academic skill: [`de-aigc-skills`](../../skills/48-de-AIGC-skills/SKILL.md)
- Chinese CLI-style complementary skill: [`humanize-chinese`](../../skills/49-voidborne-d-humanize-chinese/SKILL.md)
- License note: `humanize-chinese` is MIT Non-Commercial; check [`LICENSE_AUDIT.md`](../LICENSE_AUDIT.md) before commercial use.
- Provenance layer (去水印): [`references/watermarks.md`](../../skills/48-de-AIGC-skills/references/watermarks.md) + [`scripts/provenance_scrub.py`](../../skills/48-de-AIGC-skills/scripts/provenance_scrub.py) — run `inspect` on the file before the audit.
- Deterministic audit and fidelity gate: [`scripts/aigc_audit.py`](../../skills/48-de-AIGC-skills/scripts/aigc_audit.py) — `audit` before the rewrite, `compare original revised --section <name>` after it (exit 1 if a number, citation or table reference was lost or invented).

## Prompt

```text
Run an academic de-AIGC pass on the following section (auto-detect English vs
Chinese and use the matching pattern library). Start with the provenance-mark
report (invisible-character carriers, docx / figure metadata; the statistical
watermark is reported as unknown). Then produce the audit table of
AI-writing signatures — do not edit yet. Then run the claim-evidence check:
flag any verb stronger than the design supports. Then rewrite so that sentence
length follows content, packaging is replaced by anchors the section already
contains (flag missing ones for the author; never invent them), hedging is
calibrated, and paragraphs relay by meaning.
Preserve all citations, variables, coefficients, p-values, sample definitions,
and technical terms. End with the five-dimension self-score and a change log.
```

## Expected Output

| Stage | What to inspect |
|---|---|
| Provenance report | Layer A carriers counted by code point (kept vs removed, with context); docx docProps / figure C2PA noted; ends with `B: unknown` — never "watermark-free" |
| Audit table | EN rules (inflated significance, -ing tails, chatbot residue, staged contrast) or ZH rules (四字套话、否定对举、升华套话、翻译腔), with severity and whether the script or the model found each hit |
| Claim–evidence check | Overclaiming verbs flagged against the paper's actual design; no invented evidence |
| Rewrite | Meaning preserved; no manufactured rhythm or invented anchors; academic register intact in the manuscript's language |
| Preservation check | `aigc_audit.py compare` passes: numbers, citations, table references unchanged; no negation, direction or verb-strength drift; change rate within the section cap |
| Self-score | Concreteness, rhythm, calibration, cohesion, researcher voice — weighted ≥ 42/50 to pass |

## Quality Bar

The rewrite should not make the paper casual, remove nuance, or distort
empirical claims. The goal is lower AI-writing signal with better scholarly
texture, not aggressive paraphrasing — and for bilingual packages, the English
abstract must claim exactly what the Chinese text claims, at the same strength.
