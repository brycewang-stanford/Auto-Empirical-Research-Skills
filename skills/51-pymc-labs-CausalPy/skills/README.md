# User-Facing Agent Skills

Markdown skills in this directory teach AI coding agents how to use CausalPy for causal inference tasks. They are distributed to end users via [Decision AI Hub](https://hub.decision.ai).

Developer-focused skills (environment setup, PR workflows, testing conventions, etc.) live in `.github/skills/` and are auto-discovered in-repo via platform symlinks. They are **not** included here.

## Layout

| Path | Purpose |
|------|---------|
| `choosing-causalpy-methods/` | Choosing the right CausalPy experiment class from a causal question and data structure |
| `running-causalpy-experiments/` | Fitting chosen experiments, configuring models and priors, summarizing, plotting, and interpreting results |
| `running-placebo-analysis/` | Placebo-in-time sensitivity checks |
