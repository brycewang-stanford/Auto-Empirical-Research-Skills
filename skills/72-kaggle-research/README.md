# Kaggle Research

First-party AERS integration for safe, reproducible access to datasets,
competitions, notebooks/kernels, and models through the official Kaggle CLI.

Open [`kaggle-research/SKILL.md`](kaggle-research/SKILL.md) for agent
instructions. Runtime code and tests are self-contained inside the skill
directory and use only the Python standard library. The integration provides:

- deny-by-default policy checks for remote writes and deletes;
- path-confined downloads with SHA-256 manifests;
- bounded, credential-redacted audit records;
- offline unit/contract tests and an opt-in real Kaggle read-only smoke test.
