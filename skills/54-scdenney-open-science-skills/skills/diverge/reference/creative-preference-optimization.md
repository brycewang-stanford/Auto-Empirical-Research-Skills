# Creative Preference Optimization (CrPO) — background

Background note for the `diverge` and `diverge-codex` skills. Source:

> Ismayilzada, M., Laverghetta Jr., A., Luchini, S. A., Patel, R., Bosselut, A., van der Plas, L., & Beaty, R. E. (2025). [Creative Preference Optimization](https://arxiv.org/abs/2505.14442). *Findings of the Association for Computational Linguistics: EMNLP 2025*, 9580–9609.

## The problem

Standard alignment (RLHF/DPO) optimizes for human-preferred outputs — which in practice means the most expected, least surprising ones. Ismayilzada et al. show this actively reduces creativity: aligned models converge on high-quality but low-novelty, low-surprise outputs. Claude 3.7 Sonnet and GPT-4o are tested as baselines and cluster in exactly this region.

## CrPO

**Creative Preference Optimization (CrPO)** modifies the preference-alignment objective by injecting four independently weighted signals:

- **Novelty** — semantic distance from other known responses (divergent semantic integration)
- **Diversity** — pairwise semantic distance from other responses to the same prompt
- **Surprise** — negative log-likelihood under a reference model (how unexpected the output is)
- **Quality** — reward-model score

They train and evaluate using **MUCE**, a dataset of 200,000+ human responses and creativity ratings across 30+ psychological creativity assessments.

## Findings

- Small models (7–8B parameters) fine-tuned with CrPO outperform GPT-4o and Claude 3.7 on human creativity judgments.
- The winning variant — **CrPO-nov-div-sur** (novelty + diversity + surprise, no quality injection) — had the highest head-to-head human win rate on creativity.
- Adding a quality signal recovers some quality but reduces creativity, confirming a real tradeoff.
- Prompting ("brainstorm, then select") and decoding (min-p sampling) both improved creativity over the base model — though CrPO models with standard prompting still beat them.

## Why a skill, not a fine-tune

The core problem is structural: any model trained with standard alignment tends toward its most probable output, which is by definition the least surprising one. CrPO fixes this at the weight level, which is not accessible for closed models like Claude or Codex.

But the paper's own prompting baseline — **brainstorm-then-select** — produced meaningful gains and is fully accessible through prompt engineering. Its mechanics:

1. Generate multiple approaches before committing to any.
2. Require that approaches differ in underlying mechanism, not just vocabulary.
3. Require at least one approach that is explicitly surprising or non-obvious.
4. Defer quality and implementation until after selection.

These do not require fine-tuning. They require enforcing a structure the model will not enforce on its own. The `diverge` and `diverge-codex` skills encode exactly that structure as invocable behavior.
