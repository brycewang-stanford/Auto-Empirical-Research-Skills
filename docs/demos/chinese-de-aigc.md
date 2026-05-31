# Demo: Chinese Academic De-AIGC Pass

This demo shows how to route a Chinese academic manuscript section through AERS's Chinese de-AIGC skills while preserving technical claims.

## Route

- Academic Chinese skill: [`chinese-de-aigc`](../../skills/48-copaper-ai-chinese-de-aigc/SKILL.md)
- Local CLI-style complementary skill: [`humanize-chinese`](../../skills/49-voidborne-d-humanize-chinese/SKILL.md)
- License note: `humanize-chinese` is MIT Non-Commercial; check [`LICENSE_AUDIT.md`](../LICENSE_AUDIT.md) before commercial use.

## Prompt

```text
Run a Chinese academic de-AIGC pass on the following section. First diagnose the visible AI-writing patterns. Then rewrite with academic precision, varied sentence rhythm, cautious causal language, concrete nouns, and implicit cohesion. Preserve all citations, variables, coefficients, p-values, sample definitions, and technical terms. End with a before/after issue table and a five-dimension self-score.
```

## Expected Output

| Section | What to inspect |
|---|---|
| Pattern diagnosis | Four-character cliches, hollow transitions, over-symmetric paragraph structure, inflated claims |
| Rewrite | Meaning preserved; academic voice less formulaic |
| Preservation check | Numbers, citations, variable names, and conclusions unchanged |
| Self-score | Concreteness, rhythm, caution, cohesion, researcher voice |

## Quality Bar

The rewrite should not make the paper casual, remove nuance, or distort empirical claims. The goal is lower AI-writing signal with better scholarly texture, not aggressive paraphrasing.
