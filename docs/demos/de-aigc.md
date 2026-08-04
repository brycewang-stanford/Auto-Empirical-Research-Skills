# Demo: Academic De-AIGC Pass (English + Chinese)

This demo routes an empirical-paper section — English or Chinese — through AERS's
bilingual de-AIGC skill while preserving every technical claim.

## Route

- Bilingual academic skill: [`de-aigc-skills`](../../skills/48-de-AIGC-skills/SKILL.md)
- Chinese CLI-style complementary skill: [`humanize-chinese`](../../skills/49-voidborne-d-humanize-chinese/SKILL.md)
- License note: `humanize-chinese` is MIT Non-Commercial; check [`LICENSE_AUDIT.md`](../LICENSE_AUDIT.md) before commercial use.

## Prompt

```text
Run an academic de-AIGC pass on the following section (auto-detect English vs
Chinese and use the matching pattern library). First produce the audit table of
AI-writing signatures — do not edit yet. Then run the claim-evidence check:
flag any verb stronger than the design supports. Then rewrite with varied
sentence rhythm, concrete anchors, calibrated hedging, and implicit cohesion.
Preserve all citations, variables, coefficients, p-values, sample definitions,
and technical terms. End with the five-dimension self-score and a change log.
```

## Expected Output

| Stage | What to inspect |
|---|---|
| Audit table | EN rules (inflated significance, -ing tails, uniform rhythm) or ZH rules (四字套话、虚词堆叠、总分总), with severity |
| Claim–evidence check | Overclaiming verbs flagged against the paper's actual design; no invented evidence |
| Rewrite | Meaning preserved; rhythm varies; academic register intact in the manuscript's language |
| Preservation check | Numbers, citations, variable names, and conclusions unchanged |
| Self-score | Concreteness, rhythm, calibration, cohesion, researcher voice — weighted ≥ 42/50 to pass |

## Quality Bar

The rewrite should not make the paper casual, remove nuance, or distort
empirical claims. The goal is lower AI-writing signal with better scholarly
texture, not aggressive paraphrasing — and for bilingual packages, the English
abstract must claim exactly what the Chinese text claims, at the same strength.
